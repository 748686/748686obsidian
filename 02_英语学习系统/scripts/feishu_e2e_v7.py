#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu E2E Callback Test V7.1

目标
----
1. 第1张题卡点击后原地更新
2. 第2张题卡点击后原地更新
3. 第3张题卡点击后原地更新
4. 三题完成后，发送第4张总结卡

V7.1 修复
----------
V7.0 的 WebSocket Client 没有 .im API。
V7.1 将：

- WebSocket Client
  用于接收 card.action.trigger

- API Client
  用于发送最终总结卡

彻底分离。

注意
----
本测试不修改：
- English Exam Parser
- English Exam Grader
- 正式试卷
- 正式答案
- 正式考试数据
"""

import os
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

from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
)


# ============================================================
# CONFIG
# ============================================================

APP_ID = os.environ.get("APP_ID")
APP_SECRET = os.environ.get("APP_SECRET")

if not APP_ID:
    raise RuntimeError("APP_ID is missing")

if not APP_SECRET:
    raise RuntimeError("APP_SECRET is missing")


# ============================================================
# QUESTIONS
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
# STATE
# ============================================================

answer_state = {}


# ============================================================
# QUESTION HELPERS
# ============================================================

def get_question(question_id):
    for q in QUESTIONS:
        if q["question_id"] == question_id:
            return q
    return None


# ============================================================
# QUESTION CARD
# ============================================================

def build_question_card(question):
    """
    初始题卡
    """

    elements = [
        {
            "tag": "markdown",
            "content": (
                f"### 第 {question['number']} 题\n\n"
                f"**{question['question']}**"
            ),
        }
    ]

    for key, value in question["options"].items():
        elements.append(
            {
                "tag": "button",
                "text": {
                    "tag": "plain_text",
                    "content": f"{key}. {value}",
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
            }
        )

    return {
        "schema": "2.0",
        "body": {
            "elements": elements
        },
    }


# ============================================================
# ANSWERED CARD
# ============================================================

def build_answered_card(question, user_answer):
    """
    用户回答后：
    原题卡原地替换成结果卡。
    """

    correct_answer = question["correct_answer"]

    is_correct = user_answer == correct_answer

    if is_correct:
        result_text = "### ✅ 回答正确"
    else:
        result_text = "### ❌ 回答错误"

    user_option_text = question["options"].get(
        user_answer,
        user_answer
    )

    correct_option_text = question["options"].get(
        correct_answer,
        correct_answer
    )

    elements = [
        {
            "tag": "markdown",
            "content": (
                f"### 第 {question['number']} 题\n\n"
                f"**{question['question']}**"
            ),
        },
        {
            "tag": "markdown",
            "content": (
                f"{result_text}\n\n"
                f"**你的答案：** {user_answer}. {user_option_text}\n\n"
                f"**正确答案：** "
                f"{correct_answer}. {correct_option_text}"
            ),
        },
        {
            "tag": "hr"
        },
        {
            "tag": "markdown",
            "content": (
                f"**解析：**\n\n"
                f"{question['explanation']}"
            ),
        },
    ]

    return {
        "schema": "2.0",
        "body": {
            "elements": elements
        },
    }


# ============================================================
# SUMMARY CARD
# ============================================================

def build_summary_card():
    total = len(QUESTIONS)

    answered = len(answer_state)

    correct = sum(
        1
        for item in answer_state.values()
        if item["is_correct"]
    )

    wrong = answered - correct

    if answered:
        accuracy = correct / answered * 100
    else:
        accuracy = 0

    elements = [
        {
            "tag": "markdown",
            "content": "## 📊 本次答题总结",
        },
        {
            "tag": "hr",
        },
        {
            "tag": "markdown",
            "content": (
                f"**总题数：** {total}\n\n"
                f"**已答：** {answered}\n\n"
                f"**正确：** {correct}\n\n"
                f"**错误：** {wrong}\n\n"
                f"**正确率：** {accuracy:.1f}%"
            ),
        },
        {
            "tag": "hr",
        },
    ]

    for question in QUESTIONS:
        result = answer_state.get(question["question_id"])

        if not result:
            continue

        if result["is_correct"]:
            icon = "✅"
            result_text = "正确"
        else:
            icon = "❌"
            result_text = "错误"

        elements.append(
            {
                "tag": "markdown",
                "content": (
                    f"{icon} **第 {question['number']} 题："
                    f"{result_text}**\n\n"
                    f"你的答案：{result['answer']}\n\n"
                    f"正确答案：{question['correct_answer']}"
                ),
            }
        )

    return {
        "schema": "2.0",
        "body": {
            "elements": elements
        },
    }


# ============================================================
# CALLBACK CARD RESPONSE
# ============================================================

def make_card_callback_response(card_data):
    """
    将更新后的卡片返回给飞书，
    实现原地更新。
    """

    response = P2CardActionTriggerResponse()

    card = CallBackCard()

    card.type = "raw"
    card.data = card_data

    response.card = card

    return response


# ============================================================
# SEND SUMMARY CARD
# ============================================================

def send_summary_card(api_client, chat_id):
    """
    使用普通 API Client 发送第4张总结卡。

    注意：
    这里不能使用 WebSocket Client，
    因为 WebSocket Client 没有 .im。
    """

    print("=" * 70)
    print("SENDING SUMMARY CARD")
    print("=" * 70)

    summary_card = build_summary_card()

    content = json.dumps(
        summary_card,
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

    print("chat_id =", chat_id)
    print("msg_type = interactive")
    print("creating summary message...")

    response = api_client.im.v1.message.create(request)

    print("summary response =", response)

    if not response.success():
        print("=" * 70)
        print("SUMMARY CARD SEND FAILED")
        print("=" * 70)
        print("code =", response.code)
        print("msg  =", response.msg)
        print("request_id =", response.request_id())
        return False

    print("=" * 70)
    print("SUMMARY CARD SENT SUCCESSFULLY")
    print("=" * 70)

    return True


# ============================================================
# CARD ACTION HANDLER
# ============================================================

def do_card_action_trigger(
    event: P2CardActionTrigger,
    api_client,
):
    """
    处理飞书卡片点击。
    """

    print("=" * 70)
    print("CARD ACTION RECEIVED")
    print("=" * 70)

    try:

        action = event.event.action

        value = action.value

        question_id = value.get("question_id")
        answer = value.get("answer")

        print("question_id =", question_id)
        print("answer      =", answer)

        question = get_question(question_id)

        if not question:
            print("ERROR: unknown question_id")

            return P2CardActionTriggerResponse(
                {
                    "toast": {
                        "type": "error",
                        "content": "题目不存在",
                    }
                }
            )

        # ----------------------------------------------------
        # Duplicate protection
        # ----------------------------------------------------

        if question_id in answer_state:

            print("Duplicate answer")

            return P2CardActionTriggerResponse(
                {
                    "toast": {
                        "type": "warning",
                        "content": f"第 {question['number']} 题已经回答",
                    }
                }
            )

        # ----------------------------------------------------
        # Judge
        # ----------------------------------------------------

        correct_answer = question["correct_answer"]

        is_correct = answer == correct_answer

        answer_state[question_id] = {
            "answer": answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
        }

        score = sum(
            1
            for item in answer_state.values()
            if item["is_correct"]
        )

        completed = len(answer_state)
        total = len(QUESTIONS)

        if is_correct:

            print("RESULT = CORRECT")

        else:

            print("RESULT = WRONG")
            print("correct =", correct_answer)

        print("score =", score)
        print(
            f"completed = {completed}/{total}"
        )

        # ----------------------------------------------------
        # Build updated card
        # ----------------------------------------------------

        updated_card = build_answered_card(
            question,
            answer,
        )

        print("RETURNING UPDATED CARD")
        print("card.type = raw")
        print("card update prepared")

        # ----------------------------------------------------
        # Final summary
        # ----------------------------------------------------

        if completed == total:

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

            chat_id = None

            try:
                chat_id = (
                    event.event.context.open_chat_id
                )
            except Exception:

                pass

            if not chat_id:

                print(
                    "ERROR: open_chat_id not found"
                )

            else:

                print(
                    "chat_id =",
                    chat_id,
                )

                try:

                    send_summary_card(
                        api_client,
                        chat_id,
                    )

                except Exception as exc:

                    print("=" * 70)
                    print("SUMMARY CARD EXCEPTION")
                    print("=" * 70)

                    print(
                        repr(exc)
                    )

                    traceback.print_exc()

        # ----------------------------------------------------
        # Return updated original card
        # ----------------------------------------------------

        return make_card_callback_response(
            updated_card
        )

    except Exception as exc:

        print("=" * 70)
        print("CARD ACTION EXCEPTION")
        print("=" * 70)

        print(
            repr(exc)
        )

        traceback.print_exc()

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
    print("748686 FEISHU E2E V7.1")
    print("=" * 70)

    print("目标：")
    print("1. 原地更新第1张题卡")
    print("2. 原地更新第2张题卡")
    print("3. 原地更新第3张题卡")
    print("4. 三题完成后发送第4张总结卡")

    print("Questions:")

    for q in QUESTIONS:

        print(
            f"  {q['question_id']} | "
            f"第 {q['number']} 题 | "
            f"答案 = {q['correct_answer']}"
        )

    # ========================================================
    # API CLIENT
    # ========================================================

    print()
    print("Creating Feishu API client...")

    api_client = (
        lark.Client.builder()
        .app_id(APP_ID)
        .app_secret(APP_SECRET)
        .build()
    )

    print("Feishu API client ready.")

    # ========================================================
    # EVENT HANDLER
    # ========================================================

    def callback(event):

        return do_card_action_trigger(
            event,
            api_client,
        )

    event_handler = (
        lark.EventDispatcherHandler.builder(
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
    # ========================================================

    print()
    print("Connecting to Feishu...")

    client = Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.DEBUG,
    )

    client.start()


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":
    main()
