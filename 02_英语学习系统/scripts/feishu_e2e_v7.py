#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu E2E Interactive Exam V7.0

目标
----
验证完整的飞书交互答题闭环：

1. 飞书发送 3 张独立题目卡
2. 用户点击 A / B / C
3. card.action.trigger 到达 GitHub Actions
4. 程序立即判断答案
5. 当前题目卡原地更新
6. 卡片显示：
   - 用户答案
   - 正确 / 错误
   - 正确答案
   - 解析
7. 三道题全部完成后
8. 程序额外发送第 4 张总结卡
9. 总结卡显示：
   - 总题数
   - 答对
   - 答错
   - 正确率
   - 每题结果

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
import time
import traceback

import lark_oapi as lark

from lark_oapi.ws.client import Client

from lark_oapi.event.callback.model.p2_card_action_trigger import (
    P2CardActionTrigger,
    P2CardActionTriggerResponse,
    CallBackCard,
)

from lark_oapi.event.dispatcher_handler import EventDispatcherHandler

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

for q in QUESTIONS:
    answer_state[q["question_id"]] = {
        "answered": False,
        "answer": None,
        "correct": False,
    }


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
# ============================================================

def build_question_card(question):
    """
    生成最开始发送给用户的题目卡。

    注意：
    这里使用 schema 2.0。
    按钮使用 behaviors callback。
    """

    elements = []

    # 题目
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

    # 选项
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

    # 分割线
    elements.append({
        "tag": "hr",
    })

    # 按钮
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
                "content": f"英语答题测试 · 第 {question['number']} 题",
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 构造“已作答”卡片
# ============================================================

def build_answered_card(question, user_answer):
    """
    原地替换当前题目卡。

    这是本版本最关键的地方。
    """

    correct_answer = question["correct_answer"]
    is_correct = user_answer == correct_answer

    if is_correct:
        result_text = "✅ **回答正确**"
        template = "green"
    else:
        result_text = "❌ **回答错误**"
        template = "red"

    elements = []

    # 题目
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

    # 原选项
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

    elements.append({
        "tag": "hr",
    })

    # 用户答案
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**你的答案：{user_answer}**"
            ),
        },
    })

    # 对错
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": result_text,
        },
    })

    # 正确答案
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**正确答案：{correct_answer}**"
            ),
        },
    })

    # 解析
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
                    + ("正确" if is_correct else "错误")
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
# ============================================================

def build_summary_card():
    total = len(QUESTIONS)

    completed = 0
    correct = 0

    result_lines = []

    for q in QUESTIONS:
        state = answer_state[q["question_id"]]

        if state["answered"]:
            completed += 1

            if state["correct"]:
                correct += 1
                result_lines.append(
                    f"第 {q['number']} 题：✅"
                )
            else:
                result_lines.append(
                    f"第 {q['number']} 题：❌"
                )
        else:
            result_lines.append(
                f"第 {q['number']} 题：未作答"
            )

    wrong = completed - correct

    if total:
        percentage = correct / total * 100
    else:
        percentage = 0

    content = (
        "## 🎯 答题完成\n\n"
        f"**总题数：** {total}\n\n"
        f"**已作答：** {completed}\n\n"
        f"**答对：** {correct}\n\n"
        f"**答错：** {wrong}\n\n"
        f"**正确率：** {percentage:.1f}%\n\n"
        "---\n\n"
        + "\n".join(result_lines)
    )

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
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content,
                    },
                }
            ],
        },
    }


# ============================================================
# 用 SDK 正确构造“原地更新卡片”响应
# ============================================================

def make_card_callback_response(card_data):
    """
    关键修复：

    不能：
        P2CardActionTriggerResponse({
            "card": {
                "type": "card",
                "data": card_data
            }
        })

    必须使用：
        CallBackCard()
        card.type = "raw"
        card.data = card_data
        response.card = card
    """

    response = P2CardActionTriggerResponse()

    card = CallBackCard()

    card.type = "raw"
    card.data = card_data

    response.card = card

    return response


# ============================================================
# 发送第4张总结卡
# ============================================================

def send_summary_card(chat_id):
    """
    三道题全部完成以后，额外发送第4张总结卡。
    """

    if not chat_id:
        print("WARNING: 没有获得 open_chat_id，无法发送总结卡")
        return

    card_data = build_summary_card()

    content = json.dumps(
        card_data,
        ensure_ascii=False,
        separators=(",", ":"),
    )

    request = (
        CreateMessageRequest.builder()
        .receive_id_type("chat_id")
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(chat_id)
            .msg_type("interactive")
            .content(content)
            .build()
        )
        .build()
    )

    try:
        response = client.im.v1.message.create(request)

        if response.success():
            print("")
            print("=" * 70)
            print("SUMMARY CARD SENT")
            print("=" * 70)
            print(f"chat_id = {chat_id}")
            print("第4张总结卡发送成功")
            print("=" * 70)
        else:
            print("")
            print("=" * 70)
            print("SUMMARY CARD SEND FAILED")
            print("=" * 70)
            print(response.raw.content if response.raw else response)
            print("=" * 70)

    except Exception as exc:
        print("")
        print("=" * 70)
        print("SUMMARY CARD EXCEPTION")
        print("=" * 70)
        print(repr(exc))
        traceback.print_exc()
        print("=" * 70)


# ============================================================
# 卡片点击处理
# ============================================================

def do_card_action_trigger(
    data: P2CardActionTrigger,
) -> P2CardActionTriggerResponse:

    print("")
    print("=" * 70)
    print("CARD ACTION RECEIVED")
    print("=" * 70)

    try:
        event = data.event

        action = event.action
        action_value = action.value or {}

        question_id = action_value.get("question_id")
        user_answer = action_value.get("answer")

        print(f"question_id = {question_id}")
        print(f"answer      = {user_answer}")

        # ----------------------------------------------------
        # 找题
        # ----------------------------------------------------

        question = get_question(question_id)

        if question is None:
            print("ERROR: unknown question_id")

            return P2CardActionTriggerResponse({
                "toast": {
                    "type": "error",
                    "content": "未知题目",
                }
            })

        # ----------------------------------------------------
        # 检查重复作答
        # ----------------------------------------------------

        state = answer_state[question_id]

        if state["answered"]:
            print("Duplicate answer")

            # 已经答过：
            # 不再重新计算，也不重新修改卡片。
            return P2CardActionTriggerResponse({
                "toast": {
                    "type": "info",
                    "content": "这道题已经回答过了",
                }
            })

        # ----------------------------------------------------
        # 判断答案
        # ----------------------------------------------------

        correct_answer = question["correct_answer"]
        is_correct = user_answer == correct_answer

        state["answered"] = True
        state["answer"] = user_answer
        state["correct"] = is_correct

        print(
            "RESULT = "
            + ("CORRECT" if is_correct else "WRONG")
        )

        if not is_correct:
            print(f"correct = {correct_answer}")

        # ----------------------------------------------------
        # 统计
        # ----------------------------------------------------

        completed = 0
        score = 0

        for q in QUESTIONS:
            q_state = answer_state[q["question_id"]]

            if q_state["answered"]:
                completed += 1

            if q_state["correct"]:
                score += 1

        total = len(QUESTIONS)

        print(f"score = {score}")
        print(f"completed = {completed}/{total}")

        # ----------------------------------------------------
        # 生成“当前题目”的已作答卡
        # ----------------------------------------------------

        updated_card = build_answered_card(
            question,
            user_answer,
        )

        print("RETURNING UPDATED CARD")
        print("card.type = raw")
        print("card update prepared")

        # ----------------------------------------------------
        # 三题完成
        # ----------------------------------------------------

        if completed == total:
            print("")
            print("=" * 70)
            print("E2E TEST COMPLETE")
            print("=" * 70)

            percentage = score / total * 100

            print(f"Score: {score}/{total}")
            print(f"Percentage: {percentage:.1f}%")

            # 从 callback event 获取当前卡片所在 chat
            context = getattr(event, "context", None)

            chat_id = ""

            if context is not None:
                chat_id = str(
                    getattr(
                        context,
                        "open_chat_id",
                        "",
                    )
                    or ""
                )

            print(f"chat_id = {chat_id}")

            # ------------------------------------------------
            # 注意：
            #
            # 当前 callback 必须先返回“第3题更新后的卡片”。
            #
            # 总结卡单独发送。
            #
            # 这里直接发送第4张。
            # ------------------------------------------------

            try:
                send_summary_card(chat_id)
            except Exception:
                traceback.print_exc()

        # ----------------------------------------------------
        # 返回当前题目的更新卡片
        # ----------------------------------------------------

        return make_card_callback_response(updated_card)

    except Exception as exc:

        print("")
        print("=" * 70)
        print("CARD ACTION HANDLER ERROR")
        print("=" * 70)

        print(repr(exc))
        traceback.print_exc()

        print("=" * 70)

        # 出错时不要返回错误卡片，
        # 返回 Toast 方便定位。
        return P2CardActionTriggerResponse({
            "toast": {
                "type": "error",
                "content": "处理失败，请查看 GitHub Actions 日志",
            }
        })


# ============================================================
# SDK Handler
# ============================================================

event_handler = (
    lark.EventDispatcherHandler
    .builder(
        "",
        "",
        lark.LogLevel.DEBUG,
    )
    .register_p2_card_action_trigger(
        do_card_action_trigger
    )
    .build()
)


# ============================================================
# WebSocket Client
# ============================================================

client = Client(
    APP_ID,
    APP_SECRET,
    event_handler=event_handler,
    log_level=lark.LogLevel.DEBUG,
)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    print("")
    print("=" * 70)
    print("748686 FEISHU E2E V7.0")
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

    print("")
    print("Connecting to Feishu...")
    print("")

    try:
        client.start()

    except KeyboardInterrupt:
        print("")
        print("Stopped by user.")

    except Exception as exc:
        print("")
        print("=" * 70)
        print("FATAL ERROR")
        print("=" * 70)
        print(repr(exc))
        traceback.print_exc()
        sys.exit(1)
