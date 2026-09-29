#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Full English Exam Runner V8.0

============================================================
目标
============================================================

直接运行真实 61 题英语考试。

题型：
- listening      15
- single_choice  10
- multiple_choice 10
- cloze          10
- reading        5
- translation    10
- writing        1

总计：
61 题

============================================================
数据流
============================================================

English Exam Parser V1.6 JSON
        ↓
feishu_english_exam.py V1.0
        ↓
安全答题数据
        ↓
Feishu Full Exam Runner V8.0
        ↓
61 张独立题卡
        ↓
card.action.trigger
        ↓
原卡片原地更新
        ↓
全部完成
        ↓
answers.json
        ↓
English Exam Grader V1.0
        ↓
最终成绩卡

============================================================
原则
============================================================

1. 不修改 Parser V1.6
2. 不修改 Adapter V1.0
3. 不修改 Grader V1.0
4. 初始飞书卡片绝不发送 correct_answer
5. 初始飞书卡片绝不发送 explanation
6. 初始飞书卡片绝不发送 reference_answer
7. 自动题自动判断
8. 翻译/作文保存提交结果，交给人工批改
9. 每题独立卡片
10. 不把 61 题合并成一张巨型卡片
11. 最终单独发送总结卡

============================================================
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
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
# 路径配置
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent
ENGLISH_ROOT = SCRIPT_DIR.parent

REPO_ROOT = ENGLISH_ROOT.parent

ADAPTER_PATH = (
    SCRIPT_DIR / "feishu_english_exam.py"
)

GRADER_PATH = (
    SCRIPT_DIR / "english_exam_grader.py"
)

DEFAULT_EXAM_JSON = (
    "/tmp/748686_exam_parser_v1_6.json"
)

EXAM_JSON = Path(
    os.environ.get(
        "EXAM_JSON",
        DEFAULT_EXAM_JSON,
    )
).resolve()

ANSWERS_JSON = Path(
    "/tmp/748686_feishu_answers.json"
).resolve()

GRADER_OUTPUT = Path(
    "/tmp/748686_feishu_grader_result.json"
).resolve()


# ============================================================
# 考试配置
# ============================================================

EXAM_DATE = (
    os.environ.get(
        "EXAM_DATE",
        "",
    ).strip()
)

AUDIO_FORMAT = (
    os.environ.get(
        "AUDIO_FORMAT",
        "mp3",
    ).strip().lower()
)

CHAT_NAME = (
    os.environ.get(
        "FEISHU_CHAT_NAME",
        "748686知识系统",
    ).strip()
)


# ============================================================
# 题型
# ============================================================

CHOICE_TYPES = {
    "single_choice",
    "cloze",
    "reading",
    "listening",
}

MULTIPLE_TYPE = "multiple_choice"

MANUAL_TYPES = {
    "translation",
    "writing",
}


# ============================================================
# 全局考试状态
# ============================================================

QUESTIONS: list[dict[str, Any]] = []

QUESTION_MAP: dict[str, dict[str, Any]] = {}

ANSWER_STATE: dict[str, dict[str, Any]] = {}

MULTIPLE_SELECTION: dict[str, set[str]] = {}

AUDIO_FILE_KEYS: dict[str, str] = {}

SUMMARY_SENT = False


# ============================================================
# 基础工具
# ============================================================

def load_json(path: Path) -> Any:

    if not path.exists():
        raise RuntimeError(
            f"JSON 文件不存在：{path}"
        )

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        raise RuntimeError(
            f"JSON 读取失败：{path}\n{exc}"
        ) from exc


def save_json(
    path: Path,
    data: Any,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def safe_text(value: Any) -> str:

    if value is None:
        return ""

    return str(value)


# ============================================================
# Parser JSON
# ============================================================

def load_exam() -> None:

    global QUESTIONS
    global QUESTION_MAP

    print("")
    print("=" * 70)
    print("LOADING PARSER V1.6 JSON")
    print("=" * 70)

    print(
        "exam_json =",
        EXAM_JSON,
    )

    parser_data = load_json(
        EXAM_JSON
    )

    questions = parser_data.get(
        "questions",
        [],
    )

    if not isinstance(
        questions,
        list,
    ):
        raise RuntimeError(
            "Parser JSON questions 不是数组"
        )

    QUESTIONS = questions

    QUESTION_MAP = {}

    for question in QUESTIONS:

        qid = safe_text(
            question.get(
                "question_id",
                "",
            )
        )

        if not qid:
            raise RuntimeError(
                "发现没有 question_id 的题目"
            )

        if qid in QUESTION_MAP:
            raise RuntimeError(
                f"发现重复 question_id：{qid}"
            )

        QUESTION_MAP[qid] = question

    print(
        f"Parser questions = {len(QUESTIONS)}"
    )


# ============================================================
# 61题结构检查
# ============================================================

def validate_exam() -> None:

    print("")
    print("=" * 70)
    print("VALIDATING 61-QUESTION EXAM")
    print("=" * 70)

    expected = {
        "listening": 15,
        "single_choice": 10,
        "multiple_choice": 10,
        "cloze": 10,
        "reading": 5,
        "translation": 10,
        "writing": 1,
    }

    actual: dict[str, int] = {}

    for q in QUESTIONS:

        qtype = safe_text(
            q.get("type")
        )

        actual[qtype] = (
            actual.get(qtype, 0)
            + 1
        )

    print("实际题型：")

    for qtype, count in actual.items():

        print(
            f"  {qtype}: {count}"
        )

    if len(QUESTIONS) != 61:

        raise RuntimeError(
            f"正式考试必须是 61 题，"
            f"当前为 {len(QUESTIONS)}"
        )

    if actual != expected:

        raise RuntimeError(
            "题型数量不符合正式考试契约\n"
            f"expected = {expected}\n"
            f"actual   = {actual}"
        )

    print("")
    print("✓ 总题数 = 61")
    print("✓ 听力 = 15")
    print("✓ 单选 = 10")
    print("✓ 多选 = 10")
    print("✓ 完形 = 10")
    print("✓ 阅读 = 5")
    print("✓ 翻译 = 10")
    print("✓ 作文 = 1")


# ============================================================
# Adapter 安全检查
# ============================================================

def validate_adapter_security() -> dict[str, Any]:

    print("")
    print("=" * 70)
    print("BUILDING FEISHU SAFE EXAM DATA")
    print("=" * 70)

    if not ADAPTER_PATH.exists():

        raise RuntimeError(
            f"找不到 Adapter：{ADAPTER_PATH}"
        )

    # --------------------------------------------------------
    # 直接导入 Adapter
    # --------------------------------------------------------

    import importlib.util

    spec = (
        importlib.util.spec_from_file_location(
            "feishu_english_exam",
            str(ADAPTER_PATH),
        )
    )

    if spec is None:
        raise RuntimeError(
            "无法加载 feishu_english_exam.py"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    if spec.loader is None:
        raise RuntimeError(
            "无法初始化 Adapter loader"
        )

    spec.loader.exec_module(module)

    parser_data = load_json(
        EXAM_JSON
    )

    safe_exam = (
        module.build_feishu_exam(
            parser_data
        )
    )

    module.validate_no_answer_leak(
        safe_exam
    )

    module.validate_exam_structure(
        safe_exam
    )

    print("")
    print("✓ Adapter V1.0 已接入")
    print("✓ correct_answer 未进入安全答题数据")
    print("✓ explanation 未进入安全答题数据")
    print("✓ reference_answer 未进入安全答题数据")

    return safe_exam


# ============================================================
# 飞书 Tenant Access Token
# ============================================================

def get_tenant_access_token() -> str:

    response = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={
            "app_id": APP_ID,
            "app_secret": APP_SECRET,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") not in (None, 0):

        raise RuntimeError(
            "获取 tenant_access_token 失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )
        )

    token = data.get(
        "tenant_access_token"
    )

    if not token:

        raise RuntimeError(
            "飞书没有返回 tenant_access_token"
        )

    return token


# ============================================================
# 查找聊天
# ============================================================

def find_chat_id() -> str:

    print("")
    print("=" * 70)
    print("FINDING FEISHU CHAT")
    print("=" * 70)

    token = (
        get_tenant_access_token()
    )

    headers = {
        "Authorization":
            f"Bearer {token}",
    }

    page_token = None

    while True:

        params = {
            "page_size": 100,
        }

        if page_token:
            params["page_token"] = (
                page_token
            )

        response = requests.get(
            "https://open.feishu.cn/open-apis/im/v1/chats",
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            raise RuntimeError(
                "获取群聊列表失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        items = (
            data.get("data", {})
            .get("items", [])
        )

        for item in items:

            name = safe_text(
                item.get("name")
            )

            chat_id = safe_text(
                item.get("chat_id")
            )

            print(
                f"chat: {name} | {chat_id}"
            )

            if name == CHAT_NAME:

                print("")
                print(
                    "✓ 找到目标群：",
                    CHAT_NAME,
                )

                return chat_id

        has_more = (
            data.get("data", {})
            .get("has_more", False)
        )

        if not has_more:
            break

        page_token = (
            data.get("data", {})
            .get("page_token")
        )

        if not page_token:
            break

    raise RuntimeError(
        f"找不到飞书群：{CHAT_NAME}"
    )


# ============================================================
# 上传文件到飞书
# ============================================================

def upload_feishu_file(
    path: Path,
) -> str:

    if not path.exists():

        raise RuntimeError(
            f"音频文件不存在：{path}"
        )

    token = (
        get_tenant_access_token()
    )

    headers = {
        "Authorization":
            f"Bearer {token}",
    }

    mime = "audio/mpeg"

    if path.suffix.lower() == ".m4a":
        mime = "audio/mp4"

    elif path.suffix.lower() == ".wav":
        mime = "audio/wav"

    with path.open(
        "rb"
    ) as file_handle:

        response = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers=headers,
            data={
                "file_type": "stream",
                "file_name": path.name,
            },
            files={
                "file": (
                    path.name,
                    file_handle,
                    mime,
                )
            },
            timeout=120,
        )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:

        raise RuntimeError(
            "上传飞书音频失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )
        )

    file_key = (
        data.get("data", {})
        .get("file_key")
    )

    if not file_key:

        raise RuntimeError(
            "飞书上传成功但没有返回 file_key"
        )

    print(
        f"✓ 上传音频：{path.name}"
    )

    print(
        f"  file_key = {file_key}"
    )

    return file_key


# ============================================================
# 查找并上传听力文件
# ============================================================

def prepare_audio() -> None:

    listening_questions = [
        q
        for q in QUESTIONS
        if q.get("type") == "listening"
    ]

    if not listening_questions:
        return

    if not EXAM_DATE:

        raise RuntimeError(
            "正式考试包含听力题，"
            "必须提供 EXAM_DATE"
        )

    audio_dir = (
        ENGLISH_ROOT
        / "output"
        / EXAM_DATE
        / "配套试卷"
        / "听力"
    )

    if not audio_dir.exists():

        raise RuntimeError(
            f"听力目录不存在：{audio_dir}"
        )

    print("")
    print("=" * 70)
    print("PREPARING LISTENING AUDIO")
    print("=" * 70)

    for part in (
        "A",
        "B",
        "C",
    ):

        candidates = sorted(
            audio_dir.glob(
                f"Listening_{part}.*"
            )
        )

        candidates = [
            p
            for p in candidates
            if p.suffix.lower()
            in {
                ".mp3",
                ".m4a",
                ".wav",
            }
        ]

        if not candidates:

            raise RuntimeError(
                f"找不到听力文件："
                f"Listening_{part}.*"
            )

        preferred = [
            p
            for p in candidates
            if p.suffix.lower()
            == f".{AUDIO_FORMAT}"
        ]

        path = (
            preferred[0]
            if preferred
            else candidates[0]
        )

        AUDIO_FILE_KEYS[part] = (
            upload_feishu_file(path)
        )

    print("")
    print("✓ Listening A/B/C 音频准备完成")


# ============================================================
# 卡片 Markdown
# ============================================================

def option_lines(question):

    lines = []

    options = (
        question.get(
            "options",
            {}
        )
    )

    if isinstance(
        options,
        dict,
    ):

        for key, value in options.items():

            lines.append(
                f"**{key}.** {value}"
            )

    elif isinstance(
        options,
        list,
    ):

        for item in options:

            if isinstance(
                item,
                dict,
            ):

                key = safe_text(
                    item.get("key")
                    or item.get("label")
                    or ""
                )

                value = safe_text(
                    item.get("value")
                    or item.get("text")
                    or ""
                )

                if key:
                    lines.append(
                        f"**{key}.** {value}"
                    )

    return lines


# ============================================================
# 初始选择题卡
# ============================================================

def build_choice_card(
    question,
) -> dict[str, Any]:

    qtype = question["type"]

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
    # 听力音频
    # --------------------------------------------------------

    if qtype == "listening":

        part = safe_text(
            question.get("part")
        )

        if part in AUDIO_FILE_KEYS:

            elements.append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"🎧 **听力 Part {part}**\n\n"
                        "请先播放音频，再选择答案。"
                    ),
                },
            })

            elements.append({
                "tag": "audio",
                "file_key": AUDIO_FILE_KEYS[part],
                "show_time": True,
            })

    # --------------------------------------------------------
    # 原选项
    # --------------------------------------------------------

    lines = option_lines(
        question
    )

    if lines:

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(lines),
            },
        })

    elements.append({
        "tag": "hr",
    })

    # --------------------------------------------------------
    # A-D 按钮
    # --------------------------------------------------------

    keys = list(
        question.get(
            "options",
            {}
        ).keys()
    )

    keys = [
        k
        for k in keys
        if k in {"A", "B", "C", "D"}
    ]

    if not keys:
        keys = ["A", "B", "C", "D"]

    buttons = []

    for key in keys:

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
                        "action": "answer",
                        "question_id":
                            question[
                                "question_id"
                            ],
                        "answer": key,
                    },
                }
            ],
        })

    columns = []

    for button in buttons:

        columns.append({
            "tag": "column",
            "width": "weighted",
            "elements": [button],
        })

    elements.append({
        "tag": "column_set",
        "columns": columns,
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
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
# 多选题卡
# ============================================================

def build_multiple_card(
    question,
    selected: set[str] | None = None,
) -> dict[str, Any]:

    if selected is None:
        selected = set()

    elements = []

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**第 {question['number']} 题 · 多选题**\n\n"
                f"**{question['question']}**"
            ),
        },
    })

    lines = option_lines(
        question
    )

    if lines:

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(lines),
            },
        })

    elements.append({
        "tag": "hr",
    })

    selected_text = (
        "、".join(
            sorted(selected)
        )
        if selected
        else "尚未选择"
    )

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**当前选择：** {selected_text}"
            ),
        },
    })

    elements.append({
        "tag": "hr",
    })

    buttons = []

    for key in ["A", "B", "C", "D"]:

        if key not in question.get(
            "options",
            {}
        ):
            continue

        label = (
            f"✓ {key}"
            if key in selected
            else key
        )

        buttons.append({
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": label,
            },
            "type": "default",
            "behaviors": [
                {
                    "type": "callback",
                    "value": {
                        "action":
                            "toggle_multiple",
                        "question_id":
                            question[
                                "question_id"
                            ],
                        "answer": key,
                    },
                }
            ],
        })

    columns = []

    for button in buttons:

        columns.append({
            "tag": "column",
            "width": "weighted",
            "elements": [button],
        })

    elements.append({
        "tag": "column_set",
        "columns": columns,
    })

    elements.append({
        "tag": "hr",
    })

    elements.append({
        "tag": "button",
        "text": {
            "tag": "plain_text",
            "content": "提交多选答案",
        },
        "type": "primary",
        "behaviors": [
            {
                "type": "callback",
                "value": {
                    "action":
                        "submit_multiple",
                    "question_id":
                        question[
                            "question_id"
                        ],
                },
            }
        ],
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"英语答题测试 · "
                    f"第 {question['number']} 题 · 多选"
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 文本题卡
# ============================================================

def build_text_card(
    question,
) -> dict[str, Any]:

    qtype = question["type"]

    if qtype == "translation":

        title = (
            f"英语答题测试 · "
            f"第 {question['number']} 题 · 翻译"
        )

        placeholder = (
            "请输入你的中文/英文翻译答案"
        )

        label = "翻译答案"

        max_length = 5000

    else:

        title = (
            f"英语答题测试 · "
            f"第 {question['number']} 题 · 作文"
        )

        placeholder = (
            "请输入你的英语作文"
        )

        label = "作文答案"

        max_length = 10000

    elements = []

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

    elements.append({
        "tag": "hr",
    })

    elements.append({
        "tag": "form",
        "name": (
            f"form_{question['question_id']}"
        ),
        "elements": [
            {
                "tag": "input",
                "name": "answer",
                "placeholder": {
                    "tag": "plain_text",
                    "content": placeholder,
                },
                "label": {
                    "tag": "plain_text",
                    "content": label,
                },
                "label_position": "top",
                "input_type": (
                    "multiline_text"
                ),
                "max_length": max_length,
                "required": True,
            },
            {
                "action_type":
                    "form_submit",
                "name":
                    f"submit_{question['question_id']}",
                "tag": "button",
                "text": {
                    "tag": "plain_text",
                    "content": "提交答案",
                },
                "type": "primary",
            },
        ],
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title,
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 已完成自动评分题卡
# ============================================================

def build_answered_card(
    question,
    user_answer,
) -> dict[str, Any]:

    correct_answer = safe_text(
        question.get(
            "correct_answer"
        )
    )

    normalized_user = safe_text(
        user_answer
    ).strip()

    normalized_correct = (
        correct_answer.strip()
    )

    # --------------------------------------------------------
    # 多选标准化
    # --------------------------------------------------------

    if question["type"] == "multiple_choice":

        def normalize_multi(value):

            if isinstance(
                value,
                list,
            ):

                return set(
                    str(x).strip().upper()
                    for x in value
                )

            text = str(
                value
            ).upper()

            for sep in [
                "、",
                ",",
                "，",
                " ",
                ";",
                "；",
            ]:
                text = text.replace(
                    sep,
                    "",
                )

            return set(text)

        is_correct = (
            normalize_multi(
                normalized_user
            )
            == normalize_multi(
                normalized_correct
            )
        )

    else:

        is_correct = (
            normalized_user
            == normalized_correct
        )

    if is_correct:

        result_text = (
            "✅ **回答正确**"
        )

        template = "green"

    else:

        result_text = (
            "❌ **回答错误**"
        )

        template = "red"

    elements = []

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

    lines = option_lines(
        question
    )

    if lines:

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(lines),
            },
        })

    elements.append({
        "tag": "hr",
    })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**你的答案：{normalized_user}**"
            ),
        },
    })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": result_text,
        },
    })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**正确答案："
                f"{correct_answer}**"
            ),
        },
    })

    explanation = safe_text(
        question.get(
            "explanation"
        )
    )

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**解析：**\n"
                f"{explanation}"
            ),
        },
    })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
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
# 翻译 / 作文已提交卡
# ============================================================

def build_manual_submitted_card(
    question,
    user_answer,
) -> dict[str, Any]:

    qtype = question["type"]

    if qtype == "translation":

        title = (
            f"第 {question['number']} 题 · "
            "翻译已提交"
        )

        template = "orange"

        status = (
            "🟠 **已提交，待人工批改**"
        )

    else:

        title = (
            f"第 {question['number']} 题 · "
            "作文已提交"
        )

        template = "orange"

        status = (
            "🟠 **已提交，待人工批改**"
        )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**第 {question['number']} 题**\n\n"
                    f"**{question['question']}**"
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
                    f"**你的提交：**\n\n"
                    f"{user_answer}"
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
                "content": status,
            },
        },
    ]

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title,
            },
            "template": template,
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 多选选择中卡
# ============================================================

def make_card_callback_response(
    card_data,
):

    response = (
        P2CardActionTriggerResponse()
    )

    card = CallBackCard()

    card.type = "raw"
    card.data = card_data

    response.card = card

    return response


# ============================================================
# Toast
# ============================================================

def toast_response(
    content: str,
    toast_type: str = "info",
):

    return P2CardActionTriggerResponse(
        {
            "toast": {
                "type": toast_type,
                "content": content,
            }
        }
    )


# ============================================================
# 发送单张卡片
# ============================================================

def send_card(
    api_client,
    chat_id: str,
    card_data: dict[str, Any],
) -> bool:

    content = json.dumps(
        card_data,
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

    response = (
        api_client
        .im
        .v1
        .message
        .create(request)
    )

    if not response.success():

        print("")
        print(
            "FEISHU SEND FAILED"
        )

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

        return False

    return True


# ============================================================
# 构造题卡
# ============================================================

def build_initial_card(
    question,
):

    qtype = question["type"]

    if qtype in CHOICE_TYPES:

        return build_choice_card(
            question
        )

    if qtype == MULTIPLE_TYPE:

        return build_multiple_card(
            question,
            set(),
        )

    if qtype in MANUAL_TYPES:

        return build_text_card(
            question
        )

    raise RuntimeError(
        f"未知题型：{qtype}"
    )


# ============================================================
# 发送全部 61 张题卡
# ============================================================

def send_all_questions(
    api_client,
    chat_id: str,
) -> None:

    print("")
    print("=" * 70)
    print("SENDING ALL 61 QUESTION CARDS")
    print("=" * 70)

    success = 0

    for index, question in enumerate(
        QUESTIONS,
        start=1,
    ):

        qid = question[
            "question_id"
        ]

        qtype = question[
            "type"
        ]

        print(
            f"[{index}/61] "
            f"{qid} | {qtype}"
        )

        card = build_initial_card(
            question
        )

        if not send_card(
            api_client,
            chat_id,
            card,
        ):

            raise RuntimeError(
                f"第 {index} 题发送失败："
                f"{qid}"
            )

        success += 1

        # 避免连续 API 请求过快
        time.sleep(0.15)

    print("")
    print(
        f"✓ 已发送 {success}/61 张题卡"
    )


# ============================================================
# 获取 form value
# ============================================================

def get_form_values(action) -> dict[str, Any]:

    form_value = getattr(
        action,
        "form_value",
        None,
    )

    if isinstance(
        form_value,
        dict,
    ):
        return form_value

    # 有些 SDK 对象可以转换为 dict
    try:

        if hasattr(
            action,
            "to_dict",
        ):

            raw = action.to_dict()

            if isinstance(
                raw,
                dict,
            ):

                value = raw.get(
                    "form_value",
                    {},
                )

                if isinstance(
                    value,
                    dict,
                ):

                    return value

    except Exception:

        pass

    return {}


# ============================================================
# 获取 action name
# ============================================================

def get_action_name(action) -> str:

    value = getattr(
        action,
        "name",
        None,
    )

    if value:
        return str(value)

    try:

        if hasattr(
            action,
            "to_dict",
        ):

            raw = action.to_dict()

            if isinstance(
                raw,
                dict,
            ):

                return safe_text(
                    raw.get("name")
                )

    except Exception:

        pass

    return ""


# ============================================================
# 运行 Grader
# ============================================================

def run_grader() -> dict[str, Any]:

    print("")
    print("=" * 70)
    print("RUNNING ENGLISH EXAM GRADER V1.0")
    print("=" * 70)

    if not GRADER_PATH.exists():

        raise RuntimeError(
            f"找不到 Grader：{GRADER_PATH}"
        )

    command = [
        sys.executable,
        str(GRADER_PATH),
        "--exam-json",
        str(EXAM_JSON),
        "--answers-json",
        str(ANSWERS_JSON),
        "--output",
        str(GRADER_OUTPUT),
    ]

    print(
        "COMMAND:",
        " ".join(command),
    )

    result = subprocess.run(
        command,
        text=True,
    )

    if result.returncode != 0:

        raise RuntimeError(
            "English Exam Grader V1.0 执行失败"
        )

    if not GRADER_OUTPUT.exists():

        raise RuntimeError(
            "Grader 没有生成输出文件"
        )

    grader_result = load_json(
        GRADER_OUTPUT
    )

    print("")
    print("✓ Grader V1.0 完成")

    print(
        json.dumps(
            grader_result,
            ensure_ascii=False,
            indent=2,
        )
    )

    return grader_result


# ============================================================
# 构造最终总结卡
# ============================================================

def build_final_summary_card(
    grader_result,
) -> dict[str, Any]:

    total = grader_result.get(
        "total_questions",
        len(QUESTIONS),
    )

    auto_graded = grader_result.get(
        "auto_graded_questions",
        0,
    )

    auto_correct = grader_result.get(
        "auto_correct",
        0,
    )

    auto_wrong = grader_result.get(
        "auto_wrong",
        0,
    )

    manual_review = grader_result.get(
        "manual_review_questions",
        0,
    )

    accuracy = grader_result.get(
        "accuracy",
        0,
    )

    if isinstance(
        accuracy,
        float,
    ):

        accuracy_text = (
            f"{accuracy:.1f}%"
        )

    else:

        accuracy_text = str(
            accuracy
        )

    result_lines = []

    results = grader_result.get(
        "results",
        [],
    )

    for result in results:

        number = result.get(
            "number"
        )

        qtype = result.get(
            "type",
            "",
        )

        user_answer = safe_text(
            result.get(
                "user_answer",
                "",
            )
        )

        graded = result.get(
            "graded",
            False,
        )

        correct = result.get(
            "correct"
        )

        if not graded:

            icon = "🟠"

            text = (
                f"{icon} 第 {number} 题 · "
                f"{qtype} · 待人工批改"
            )

        elif correct:

            icon = "🟢"

            text = (
                f"{icon} 第 {number} 题 · 正确"
            )

        else:

            icon = "🔴"

            text = (
                f"{icon} 第 {number} 题 · 错误"
            )

        result_lines.append(
            text
        )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "### 🎯 本次英语考试完成\n\n"
                    f"**自动评分："
                    f"{auto_correct} / "
                    f"{auto_graded}**\n\n"
                    f"自动正确率："
                    f"**{accuracy_text}**"
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
                    f"**总题数：** {total}\n\n"
                    f"**自动评分题：** {auto_graded}\n\n"
                    f"**自动答对：** {auto_correct}\n\n"
                    f"**自动答错：** {auto_wrong}\n\n"
                    f"**待人工批改：** {manual_review}"
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
                    + "\n\n".join(
                        result_lines
                    )
                ),
            },
        },
    ]

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
            "enable_forward": False,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    "🎯 英语考试最终结果"
                ),
            },
            "template": "green",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 发送最终总结
# ============================================================

def send_final_summary(
    api_client,
    chat_id: str,
) -> None:

    global SUMMARY_SENT

    if SUMMARY_SENT:
        return

    SUMMARY_SENT = True

    grader_result = run_grader()

    card = build_final_summary_card(
        grader_result
    )

    ok = send_card(
        api_client,
        chat_id,
        card,
    )

    if not ok:

        raise RuntimeError(
            "最终总结卡发送失败"
        )

    print("")
    print("=" * 70)
    print("FINAL SUMMARY SENT")
    print("=" * 70)


# ============================================================
# 检查是否全部完成
# ============================================================

def all_completed() -> bool:

    return (
        len(ANSWER_STATE)
        == len(QUESTIONS)
    )


# ============================================================
# 保存答案
# ============================================================

def save_answers() -> None:

    answers = {}

    for qid, state in (
        ANSWER_STATE.items()
    ):

        answers[qid] = state.get(
            "answer",
            "",
        )

    save_json(
        ANSWERS_JSON,
        answers,
    )

    print("")
    print(
        "答案已保存：",
        ANSWERS_JSON,
    )


# ============================================================
# 单选/听力/完形/阅读
# ============================================================

def handle_single_answer(
    question,
    user_answer,
    api_client,
    chat_id,
):

    qid = question[
        "question_id"
    ]

    if qid in ANSWER_STATE:

        return toast_response(
            f"第 {question['number']} 题已经回答",
            "warning",
        )

    if user_answer not in {
        "A",
        "B",
        "C",
        "D",
    }:

        return toast_response(
            "答案无效",
            "error",
        )

    correct_answer = safe_text(
        question.get(
            "correct_answer"
        )
    )

    is_correct = (
        user_answer
        == correct_answer
    )

    ANSWER_STATE[qid] = {
        "answer": user_answer,
        "correct": is_correct,
        "graded": True,
        "answered": True,
    }

    print("")
    print("=" * 70)
    print("ANSWER RECEIVED")
    print("=" * 70)

    print(
        "question_id =",
        qid,
    )

    print(
        "answer =",
        user_answer,
    )

    print(
        "correct =",
        correct_answer,
    )

    print(
        "RESULT =",
        "CORRECT"
        if is_correct
        else "WRONG",
    )

    print(
        f"completed = "
        f"{len(ANSWER_STATE)}/{len(QUESTIONS)}"
    )

    card = build_answered_card(
        question,
        user_answer,
    )

    if all_completed():

        save_answers()

        send_final_summary(
            api_client,
            chat_id,
        )

    return make_card_callback_response(
        card
    )


# ============================================================
# 多选切换
# ============================================================

def handle_multiple_toggle(
    question,
    answer,
):

    qid = question[
        "question_id"
    ]

    if qid in ANSWER_STATE:

        return toast_response(
            f"第 {question['number']} 题已经提交",
            "warning",
        )

    selected = (
        MULTIPLE_SELECTION
        .setdefault(
            qid,
            set(),
        )
    )

    if answer in selected:

        selected.remove(
            answer
        )

    else:

        selected.add(
            answer
        )

    print("")
    print(
        f"MULTIPLE SELECT "
        f"{qid} = "
        f"{sorted(selected)}"
    )

    card = build_multiple_card(
        question,
        selected,
    )

    return make_card_callback_response(
        card
    )


# ============================================================
# 多选提交
# ============================================================

def handle_multiple_submit(
    question,
    api_client,
    chat_id,
):

    qid = question[
        "question_id"
    ]

    if qid in ANSWER_STATE:

        return toast_response(
            f"第 {question['number']} 题已经提交",
            "warning",
        )

    selected = (
        MULTIPLE_SELECTION
        .get(
            qid,
            set(),
        )
    )

    if not selected:

        return toast_response(
            "请至少选择一个答案",
            "warning",
        )

    user_answer = ",".join(
        sorted(selected)
    )

    correct_answer = safe_text(
        question.get(
            "correct_answer"
        )
    )

    def normalize_multi(
        value,
    ):

        if isinstance(
            value,
            list,
        ):

            return set(
                str(x).strip().upper()
                for x in value
            )

        text = str(
            value
        ).upper()

        for sep in [
            "、",
            ",",
            "，",
            " ",
            ";",
            "；",
        ]:

            text = text.replace(
                sep,
                "",
            )

        return set(text)

    is_correct = (
        normalize_multi(
            user_answer
        )
        == normalize_multi(
            correct_answer
        )
    )

    ANSWER_STATE[qid] = {
        "answer": user_answer,
        "correct": is_correct,
        "graded": True,
        "answered": True,
    }

    print("")
    print("=" * 70)
    print("MULTIPLE ANSWER SUBMITTED")
    print("=" * 70)

    print(
        "question_id =",
        qid,
    )

    print(
        "answer =",
        user_answer,
    )

    print(
        "correct =",
        correct_answer,
    )

    print(
        "RESULT =",
        "CORRECT"
        if is_correct
        else "WRONG",
    )

    card = build_answered_card(
        question,
        user_answer,
    )

    if all_completed():

        save_answers()

        send_final_summary(
            api_client,
            chat_id,
        )

    return make_card_callback_response(
        card
    )


# ============================================================
# 翻译 / 作文提交
# ============================================================

def handle_manual_submit(
    question,
    user_answer,
    api_client,
    chat_id,
):

    qid = question[
        "question_id"
    ]

    if qid in ANSWER_STATE:

        return toast_response(
            f"第 {question['number']} 题已经提交",
            "warning",
        )

    user_answer = safe_text(
        user_answer
    ).strip()

    if not user_answer:

        return toast_response(
            "答案不能为空",
            "warning",
        )

    ANSWER_STATE[qid] = {
        "answer": user_answer,
        "correct": None,
        "graded": False,
        "review_required": True,
        "answered": True,
    }

    print("")
    print("=" * 70)
    print("MANUAL ANSWER SUBMITTED")
    print("=" * 70)

    print(
        "question_id =",
        qid,
    )

    print(
        "type =",
        question["type"],
    )

    print(
        "answer length =",
        len(user_answer),
    )

    card = build_manual_submitted_card(
        question,
        user_answer,
    )

    if all_completed():

        save_answers()

        send_final_summary(
            api_client,
            chat_id,
        )

    return make_card_callback_response(
        card
    )


# ============================================================
# card.action.trigger
# ============================================================

def do_card_action_trigger(
    event: P2CardActionTrigger,
    api_client,
    chat_id: str,
):

    try:

        action = event.event.action

        # ----------------------------------------------------
        # 普通 callback value
        # ----------------------------------------------------

        value = (
            getattr(
                action,
                "value",
                None,
            )
            or {}
        )

        if not isinstance(
            value,
            dict,
        ):

            value = {}

        action_type = safe_text(
            value.get(
                "action"
            )
        )

        question_id = safe_text(
            value.get(
                "question_id"
            )
        )

        user_answer = value.get(
            "answer"
        )

        # ----------------------------------------------------
        # form_submit
        # ----------------------------------------------------

        if not action_type:

            action_name = (
                get_action_name(
                    action
                )
            )

            form_values = (
                get_form_values(
                    action
                )
            )

            if action_name.startswith(
                "submit_"
            ):

                question_id = (
                    action_name[
                        len("submit_"):
                    ]
                )

                action_type = (
                    "submit_text"
                )

                user_answer = (
                    form_values.get(
                        "answer",
                        "",
                    )
                )

        print("")
        print("=" * 70)
        print("CARD ACTION RECEIVED")
        print("=" * 70)

        print(
            "action =",
            action_type,
        )

        print(
            "question_id =",
            question_id,
        )

        print(
            "answer =",
            user_answer,
        )

        # ----------------------------------------------------
        # 找题
        # ----------------------------------------------------

        question = QUESTION_MAP.get(
            question_id
        )

        if not question:

            return toast_response(
                "题目不存在",
                "error",
            )

        # ----------------------------------------------------
        # 单选
        # ----------------------------------------------------

        if action_type == "answer":

            return handle_single_answer(
                question,
                safe_text(
                    user_answer
                ).upper(),
                api_client,
                chat_id,
            )

        # ----------------------------------------------------
        # 多选切换
        # ----------------------------------------------------

        if action_type == "toggle_multiple":

            return handle_multiple_toggle(
                question,
                safe_text(
                    user_answer
                ).upper(),
            )

        # ----------------------------------------------------
        # 多选提交
        # ----------------------------------------------------

        if action_type == "submit_multiple":

            return handle_multiple_submit(
                question,
                api_client,
                chat_id,
            )

        # ----------------------------------------------------
        # 翻译 / 作文
        # ----------------------------------------------------

        if action_type == "submit_text":

            return handle_manual_submit(
                question,
                safe_text(
                    user_answer
                ),
                api_client,
                chat_id,
            )

        return toast_response(
            "未知操作",
            "error",
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

        return toast_response(
            "处理失败，请稍后重试",
            "error",
        )


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 70)
    print("748686 FEISHU FULL ENGLISH EXAM V8.0")
    print("=" * 70)

    print("")
    print(
        "正式考试：61 题"
    )

    print(
        "群聊：",
        CHAT_NAME,
    )

    print(
        "Parser JSON：",
        EXAM_JSON,
    )

    # --------------------------------------------------------
    # 1. 加载考试
    # --------------------------------------------------------

    load_exam()

    # --------------------------------------------------------
    # 2. 检查 61 题契约
    # --------------------------------------------------------

    validate_exam()

    # --------------------------------------------------------
    # 3. Adapter 安全转换
    # --------------------------------------------------------

    safe_exam = (
        validate_adapter_security()
    )

    print("")
    print(
        "Safe exam total =",
        safe_exam[
            "exam"
        ][
            "total_questions"
        ],
    )

    # --------------------------------------------------------
    # 4. 找群
    # --------------------------------------------------------

    chat_id = find_chat_id()

    # --------------------------------------------------------
    # 5. API Client
    # --------------------------------------------------------

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
        "✓ Feishu API client ready"
    )

    # --------------------------------------------------------
    # 6. 听力资源
    # --------------------------------------------------------

    prepare_audio()

    # --------------------------------------------------------
    # 7. 发送全部 61 张题卡
    # --------------------------------------------------------

    send_all_questions(
        api_client,
        chat_id,
    )

    # --------------------------------------------------------
    # 8. WebSocket callback
    # --------------------------------------------------------

    print("")
    print("=" * 70)
    print("STARTING FEISHU CARD CALLBACK SERVER")
    print("=" * 70)

    def callback(event):

        return do_card_action_trigger(
            event,
            api_client,
            chat_id,
        )

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

    ws_client = Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.DEBUG,
    )

    print("")
    print("=" * 70)
    print("61 QUESTION EXAM IS LIVE")
    print("=" * 70)

    print("")
    print(
        "现在可以直接在飞书完成全部 61 题。"
    )

    print("")
    print(
        "GitHub Actions 将保持长连接，"
        "等待全部答案提交。"
    )

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
