#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu E2E Interactive Exam V7.2

目标
----
1. 飞书发送 3 张独立题目卡
2. 用户点击 A / B / C
3. card.action.trigger 到达 GitHub Actions
4. 程序立即判断答案
5. 当前题目卡原地更新
6. 保留漂亮的原 V7.0 结果卡样式：
   - 正确 = green
   - 错误 = red
   - 用户答案
   - 正确答案
   - 解析
7. 三道题全部完成后
8. 额外发送第 4 张总结卡
9. 总结卡显示：
   - 总题数
   - 已作答
   - 答对
   - 答错
   - 正确率
   - 每题结果

V7.2
----
本版本以 V7.0 的前三张卡视觉样式为绝对基准。

只增加 V7.1 已验证成功的：
- 独立 API Client
- 第4张总结卡发送

不改变：
- WebSocket 回调
- card.action.trigger
- 原地更新逻辑
- 前三张结果卡视觉结构

注意
----
- 本程序仅用于 E2E 测试
- 不修改 Parser V1.6
- 不修改 Grader V1.0
- 不读取正式 61 题试卷
- 不调用 AI
- 不修改正式考试数据
"""

import os
import sys
import json
import traceback

import lark_oapi as lark

from lark_oapi.ws.client import Client

from lark_oapi.event.callback.model.p2_card_action_trigger import (
    P2CardActionTrigger,
    P2CardActionTriggerResponse,
    CallBackCard,
)

from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
)


# ============================================================
# 基本配置
# ============================================================

APP_ID = os.environ.get("APP_ID", "").strip()
APP_SECRET = os.environ.get("APP_SECRET", "").strip()

if not APP_ID:
    raise RuntimeError("缺少环境变量 APP_ID")

if not APP_SECRET:
    raise RuntimeError("缺少环境变量 APP_SECRET")


# ============================================================
# E2E 测试题
# ============================================================

QUESTIONS = [
    {
        "question_id": "e2e_test_001",
        "number": 1,
        "question": "1 + 1 = ?",
        "options": {
            "A": "1",
            "B": "2",
            "C": "3",
        },
        "correct_answer": "B",
        "explanation": "1 + 1 等于 2。",
    },
    {
        "question_id": "e2e_test_002",
        "number": 2,
        "question": "2 + 3 = ?",
        "options": {
            "A": "4",
            "B": "5",
            "C": "6",
        },
        "correct_answer": "B",
        "explanation": "2 + 3 等于 5。",
    },
    {
        "question_id": "e2e_test_003",
        "number": 3,
        "question": "5 - 2 = ?",
        "options": {
            "A": "2",
            "B": "3",
            "C": "4",
        },
        "correct_answer": "B",
        "explanation": "5 - 2 等于 3。",
    },
]


# ============================================================
# 运行状态
# ============================================================

answer_state = {}


# ============================================================
# 找题
# ============================================================

def get_question(question_id):
    for q in QUESTIONS:
        if q["question_id"] == question_id:
            return q

    return None


# ============================================================
# 构造原始题目卡
#
# 注意：
# 这里完全保留 V7.0 的漂亮题卡结构。
# ============================================================

def build_question_card(question):

    elements = []

    # --------------------------------------------------------
    # 题目
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**第 {question['number']} 题**\n\n"
                f"**{question['question']}**"
            ),
        },
    })

    # --------------------------------------------------------
    # 选项
    # --------------------------------------------------------

    option_lines = []

    for key, value in question["options"].items():
        option_lines.append(
            f"**{key}.** {value}"
        )

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "\n".join(option_lines),
        },
    })

    # --------------------------------------------------------
    # 分割线
    # --------------------------------------------------------

    elements.append({
        "tag": "hr",
    })

    # --------------------------------------------------------
    # 按钮
    # --------------------------------------------------------

    buttons = []

    for key in ["A", "B", "C"]:

        buttons.append({
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": key,
            },
            "type": "default",
            "behaviors": [
                {
                    "type": "callback",
                    "value": {
                        "question_id": question["question_id"],
                        "answer": key,
                    },
                }
            ],
        })

    elements.append({
        "tag": "column_set",
        "columns": [
            {
                "tag": "column",
                "width": "weighted",
                "elements": [buttons[0]],
            },
            {
                "tag": "column",
                "width": "weighted",
                "elements": [buttons[1]],
            },
            {
                "tag": "column",
                "width": "weighted",
                "elements": [buttons[2]],
            },
        ],
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"英语答题测试 · "
                    f"第 {question['number']} 题"
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 构造“已作答”卡片
#
# 这里完全保留你确认过的 V7.0 漂亮版本。
#
# 正确：
#   green
#
# 错误：
#   red
#
# 并保留：
#   原题
#   原选项
#   用户答案
#   对错
#   正确答案
#   解析
# ============================================================

def build_answered_card(question, user_answer):

    correct_answer = question["correct_answer"]

    is_correct = user_answer == correct_answer

    if is_correct:

        result_text = "✅ **回答正确**"
        template = "green"

    else:

        result_text = "❌ **回答错误**"
        template = "red"

    elements = []

    # --------------------------------------------------------
    # 题目
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**第 {question['number']} 题**\n\n"
                f"**{question['question']}**"
            ),
        },
    })

    # --------------------------------------------------------
    # 原选项
    # --------------------------------------------------------

    option_lines = []

    for key, value in question["options"].items():

        option_lines.append(
            f"**{key}.** {value}"
        )

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": "\n".join(option_lines),
        },
    })

    # --------------------------------------------------------
    # 分割线
    # --------------------------------------------------------

    elements.append({
        "tag": "hr",
    })

    # --------------------------------------------------------
    # 用户答案
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**你的答案：{user_answer}**"
            ),
        },
    })

    # --------------------------------------------------------
    # 对错
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": result_text,
        },
    })

    # --------------------------------------------------------
    # 正确答案
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**正确答案：{correct_answer}**"
            ),
        },
    })

    # --------------------------------------------------------
    # 解析
    # --------------------------------------------------------

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**解析：**\n"
                f"{question['explanation']}"
            ),
        },
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"第 {question['number']} 题 · "
                    + (
                        "正确"
                        if is_correct
                        else "错误"
                    )
                ),
            },
            "template": template,
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 构造最终总结卡
#
# 这是 V7.2 新增/优化部分。
#
# 前三张卡不动。
# 这里只负责第4张。
# ============================================================

def build_summary_card():

    total = len(QUESTIONS)

    completed = 0
    correct = 0

    result_lines = []

    for q in QUESTIONS:

        state = answer_state.get(
            q["question_id"],
            {},
        )

        if state.get("answered"):

            completed += 1

            if state.get("correct"):

                correct += 1

                result_lines.append(
                    f"🟢 **第 {q['number']} 题：正确**"
                )

            else:

                result_lines.append(
                    f"🔴 **第 {q['number']} 题：错误**"
                )

        else:

            result_lines.append(
                f"⚪ **第 {q['number']} 题：未作答**"
            )

    wrong = completed - correct

    if total:

        percentage = (
            correct / total * 100
        )

    else:

        percentage = 0

    # --------------------------------------------------------
    # 总成绩
    # --------------------------------------------------------

    score_content = (
        "### 🎯 答题完成\n\n"
        f"**{correct} / {total}**\n\n"
        f"正确率：**{percentage:.1f}%**"
    )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": score_content,
            },
        },

        {
            "tag": "hr",
        },

        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**总题数：** {total}\n\n"
                    f"**已作答：** {completed}\n\n"
                    f"**答对：** {correct}\n\n"
                    f"**答错：** {wrong}\n\n"
                    f"**正确率：** {percentage:.1f}%"
                ),
            },
        },

        {
            "tag": "hr",
        },

        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "### 📋 每题结果\n\n"
                    + "\n\n".join(result_lines)
                ),
            },
        },
    ]

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "🎯 本次答题结果",
            },
            "template": "green",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 构造原地更新卡片响应
# ============================================================

def make_card_callback_response(card_data):

    response = P2CardActionTriggerResponse()

    card = CallBackCard()

    card.type = "raw"
    card.data = card_data

    response.card = card

    return response


# ============================================================
# 发送第4张总结卡
#
# 这里使用 V7.1 已验证成功的：
#
#   API Client
#       ↓
#   client.im.v1.message.create()
#
# 而不是 WebSocket Client。
# ============================================================

def send_summary_card(
    api_client,
    chat_id,
):

    print("")
    print("=" * 70)
    print("SENDING SUMMARY CARD")
    print("=" * 70)

    if not chat_id:

        print(
            "WARNING: chat_id 为空，无法发送总结卡"
        )

        return False

    summary_card = build_summary_card()

    content = json.dumps(
        summary_card,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    request = (
        CreateMessageRequest
        .builder()
        .receive_id_type("chat_id")
        .request_body(
            CreateMessageRequestBody
            .builder()
            .receive_id(chat_id)
            .msg_type("interactive")
            .content(content)
            .build()
        )
        .build()
    )

    print(
        "chat_id =",
        chat_id,
    )

    print(
        "msg_type = interactive"
    )

    print(
        "creating summary message..."
    )

    try:

        response = (
            api_client
            .im
            .v1
            .message
            .create(request)
        )

        print(
            "summary response =",
            response,
        )

        if not response.success():

            print("")
            print("=" * 70)
            print("SUMMARY CARD SEND FAILED")
            print("=" * 70)

            print(
                "code =",
                response.code,
            )

            print(
                "msg =",
                response.msg,
            )

            try:

                print(
                    "request_id =",
                    response.request_id(),
                )

            except Exception:

                pass

            print("=" * 70)

            return False

        print("")
        print("=" * 70)
        print("SUMMARY CARD SENT SUCCESSFULLY")
        print("=" * 70)

        print(
            "第4张总结卡发送成功"
        )

        print("=" * 70)

        return True

    except Exception as exc:

        print("")
        print("=" * 70)
        print("SUMMARY CARD EXCEPTION")
        print("=" * 70)

        print(
            repr(exc)
        )

        traceback.print_exc()

        print("=" * 70)

        return False


# ============================================================
# 卡片点击处理
# ============================================================

def do_card_action_trigger(
    event: P2CardActionTrigger,
    api_client,
):

    print("")
    print("=" * 70)
    print("CARD ACTION RECEIVED")
    print("=" * 70)

    try:

        action = event.event.action

        value = action.value or {}

        question_id = value.get(
            "question_id"
        )

        user_answer = value.get(
            "answer"
        )

        print(
            "question_id =",
            question_id,
        )

        print(
            "answer      =",
            user_answer,
        )

        # ----------------------------------------------------
        # 找题
        # ----------------------------------------------------

        question = get_question(
            question_id
        )

        if not question:

            print(
                "ERROR: unknown question_id"
            )

            return P2CardActionTriggerResponse(
                {
                    "toast": {
                        "type": "error",
                        "content": "题目不存在",
                    }
                }
            )

        # ----------------------------------------------------
        # 重复作答保护
        # ----------------------------------------------------

        if question_id in answer_state:

            print(
                "Duplicate answer"
            )

            return P2CardActionTriggerResponse(
                {
                    "toast": {
                        "type": "warning",
                        "content": (
                            f"第 {question['number']} 题已经回答"
                        ),
                    }
                }
            )

        # ----------------------------------------------------
        # 判断答案
        # ----------------------------------------------------

        correct_answer = (
            question["correct_answer"]
        )

        is_correct = (
            user_answer == correct_answer
        )

        answer_state[question_id] = {
            "answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
            "correct": is_correct,
            "answered": True,
        }

        score = sum(
            1
            for item in answer_state.values()
            if item.get("is_correct")
        )

        completed = len(answer_state)

        total = len(QUESTIONS)

        if is_correct:

            print(
                "RESULT = CORRECT"
            )

        else:

            print(
                "RESULT = WRONG"
            )

            print(
                "correct =",
                correct_answer,
            )

        print(
            "score =",
            score,
        )

        print(
            f"completed = {completed}/{total}"
        )

        # ----------------------------------------------------
        # 当前题目原地更新
        #
        # 这里完全使用漂亮版 V7.0。
        # ----------------------------------------------------

        updated_card = build_answered_card(
            question,
            user_answer,
        )

        print(
            "RETURNING UPDATED CARD"
        )

        print(
            "card.type = raw"
        )

        print(
            "card update prepared"
        )

        # ----------------------------------------------------
        # 三题全部完成
        # ----------------------------------------------------

        if completed == total:

            print("")
            print("=" * 70)
            print("E2E TEST COMPLETE")
            print("=" * 70)

            percentage = (
                score / total * 100
            )

            print(
                f"Score: {score}/{total}"
            )

            print(
                f"Percentage: {percentage:.1f}%"
            )

            # ------------------------------------------------
            # 获取当前聊天 ID
            # ------------------------------------------------

            chat_id = None

            try:

                chat_id = (
                    event
                    .event
                    .context
                    .open_chat_id
                )

            except Exception:

                chat_id = None

            print(
                "chat_id =",
                chat_id,
            )

            # ------------------------------------------------
            # 发送第4张总结卡
            # ------------------------------------------------

            if chat_id:

                send_summary_card(
                    api_client,
                    chat_id,
                )

            else:

                print(
                    "ERROR: open_chat_id not found"
                )

        # ----------------------------------------------------
        # 返回当前题目的更新卡片
        # ----------------------------------------------------

        return make_card_callback_response(
            updated_card
        )

    except Exception as exc:

        print("")
        print("=" * 70)
        print("CARD ACTION EXCEPTION")
        print("=" * 70)

        print(
            repr(exc)
        )

        traceback.print_exc()

        print("=" * 70)

        return P2CardActionTriggerResponse(
            {
                "toast": {
                    "type": "error",
                    "content": "处理失败，请稍后重试",
                }
            }
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("748686 FEISHU E2E V7.2")
    print("=" * 70)

    print("")

    print("目标：")
    print("1. 原地更新第1张题卡")
    print("2. 原地更新第2张题卡")
    print("3. 原地更新第3张题卡")
    print("4. 三题完成后发送第4张总结卡")

    print("")

    print("Questions:")

    for q in QUESTIONS:

        print(
            f"  {q['question_id']} | "
            f"第 {q['number']} 题 | "
            f"答案 = {q['correct_answer']}"
        )

    # ========================================================
    # API CLIENT
    #
    # 专门负责：
    # 发送第4张总结卡
    # ========================================================

    print("")
    print(
        "Creating Feishu API client..."
    )

    api_client = (
        lark.Client
        .builder()
        .app_id(APP_ID)
        .app_secret(APP_SECRET)
        .build()
    )

    print(
        "Feishu API client ready."
    )

    # ========================================================
    # EVENT CALLBACK
    # ========================================================

    def callback(event):

        return do_card_action_trigger(
            event,
            api_client,
        )

    # ========================================================
    # EVENT HANDLER
    # ========================================================

    event_handler = (
        lark.EventDispatcherHandler
        .builder(
            "",
            "",
            lark.LogLevel.DEBUG,
        )
        .register_p2_card_action_trigger(
            callback
        )
        .build()
    )

    # ========================================================
    # WEBSOCKET CLIENT
    #
    # 专门负责：
    # 接收 card.action.trigger
    # ========================================================

    print("")
    print(
        "Connecting to Feishu..."
    )

    ws_client = Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.DEBUG,
    )

    # ========================================================
    # START
    # ========================================================

    ws_client.start()


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("")
        print(
            "Stopped by user."
        )

    except Exception as exc:

        print("")
        print("=" * 70)
        print("FATAL ERROR")
        print("=" * 70)

        print(
            repr(exc)
        )

        traceback.print_exc()

        sys.exit(1)
