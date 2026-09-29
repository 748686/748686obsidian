#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Full English Exam Runner V8.1

正式版职责
----------
1. 从 GitHub 工作区扫描 output/ 日期
2. 飞书选择考试日期
3. 飞书选择对应试卷
4. 自动定位：
   - 试卷 Markdown
   - 答案与解析 Markdown
   - Listening A/B/C
5. 自动运行 English Exam Parser V1.6
6. 通过 Feishu Adapter V1.0 做安全检查
7. 发送完整 61 道考试题
8. 接收 Feishu card.action.trigger
9. 自动评分：
   - listening
   - single_choice
   - multiple_choice
   - cloze
   - reading
10. 翻译 / 写作进入人工批改
11. 全部完成后运行 English Exam Grader V1.0
12. 发送最终成绩卡

重要安全原则
------------
- 飞书初始题卡绝不包含 correct_answer
- 飞书初始题卡绝不包含 explanation
- 飞书初始题卡绝不包含 reference_answer
- GitHub Actions 日志不打印正确答案
- Parser / Adapter / Grader 不修改
- /tmp JSON 每次考试自动生成，不依赖旧 Runner
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import re
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import requests
import lark_oapi as lark

from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
)

from lark_oapi.event.callback.model.p2_card_action_trigger import (
    P2CardActionTrigger,
    P2CardActionTriggerResponse,
)

from lark_oapi.api.card.v1 import (
    CallBackCard,
)


# ======================================================================
# 基础路径
# ======================================================================

ROOT = Path(__file__).resolve().parents[2]

ENGLISH_ROOT = ROOT / "02_英语学习系统"

SCRIPTS_DIR = ENGLISH_ROOT / "scripts"

OUTPUT_DIR = ENGLISH_ROOT / "output"

PARSER_PATH = SCRIPTS_DIR / "english_exam_parser.py"

ADAPTER_PATH = SCRIPTS_DIR / "feishu_english_exam.py"

GRADER_PATH = SCRIPTS_DIR / "english_exam_grader.py"

TMP_DIR = Path("/tmp")

EXAM_JSON = TMP_DIR / "748686_exam_parser_v1_6.json"

SAFE_EXAM_JSON = TMP_DIR / "748686_feishu_safe_exam.json"

ANSWERS_JSON = TMP_DIR / "748686_feishu_answers.json"

GRADER_OUTPUT = TMP_DIR / "748686_feishu_grader_result.json"

SESSION_JSON = TMP_DIR / "748686_feishu_exam_session.json"


# ======================================================================
# 环境
# ======================================================================

APP_ID = os.environ.get("APP_ID", "").strip()
APP_SECRET = os.environ.get("APP_SECRET", "").strip()

FEISHU_CHAT_NAME = os.environ.get(
    "FEISHU_CHAT_NAME",
    "748686知识系统",
).strip()

AUDIO_FORMAT = os.environ.get(
    "AUDIO_FORMAT",
    "mp3",
).strip()

MAX_DATES = int(
    os.environ.get("FEISHU_MAX_EXAM_DATES", "30")
)

MAX_EXAMS = int(
    os.environ.get("FEISHU_MAX_EXAMS", "30")
)


# ======================================================================
# 全局运行状态
# ======================================================================

QUESTIONS: List[Dict[str, Any]] = []

QUESTION_MAP: Dict[str, Dict[str, Any]] = {}

ANSWER_STATE: Dict[str, Dict[str, Any]] = {}

MULTIPLE_SELECTION: Dict[str, Set[str]] = {}

AUDIO_FILE_KEYS: Dict[str, str] = {}

SUMMARY_SENT = False

CURRENT_DATE: Optional[str] = None
CURRENT_EXAM_FILE: Optional[str] = None
CURRENT_ANSWER_FILE: Optional[str] = None

SESSION_ID = uuid.uuid4().hex[:16]

API_CLIENT: Optional[lark.Client] = None

CHAT_ID: Optional[str] = None

STATE_LOCK = threading.RLock()


# ======================================================================
# 工具
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    print(f"❌ {message}", flush=True)
    raise RuntimeError(message)


def safe_filename(value: str) -> str:
    value = str(value)
    value = value.replace("\\", "_")
    value = value.replace("/", "_")
    value = value.replace("..", "_")
    return value


def json_dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    tmp = path.with_suffix(path.suffix + ".tmp")

    with tmp.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    tmp.replace(path)


def json_load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ======================================================================
# GitHub Output 扫描
# ======================================================================

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def list_exam_dates() -> List[str]:
    if not OUTPUT_DIR.exists():
        return []

    dates = []

    for item in OUTPUT_DIR.iterdir():
        if not item.is_dir():
            continue

        if not DATE_RE.match(item.name):
            continue

        exam_dir = item / "配套试卷"

        if not exam_dir.is_dir():
            continue

        dates.append(item.name)

    dates.sort(reverse=True)

    return dates[:MAX_DATES]


def list_exam_files(date_value: str) -> List[Path]:
    date_dir = OUTPUT_DIR / date_value / "配套试卷"

    if not date_dir.is_dir():
        return []

    result = []

    for path in sorted(date_dir.glob("*_试卷.md")):
        if path.is_file() and path.stat().st_size > 0:
            result.append(path)

    return result[:MAX_EXAMS]


def answer_file_for_exam(exam_file: Path) -> Optional[Path]:
    candidates = [
        exam_file.with_name(
            exam_file.name.replace(
                "_试卷.md",
                "_答案与解析.md",
            )
        ),
        exam_file.with_name(
            exam_file.name.replace(
                "_试卷.md",
                "_答案解析.md",
            )
        ),
    ]

    for candidate in candidates:
        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate

    return None


def audio_path(date_value: str, part: str) -> Optional[Path]:
    audio_dir = (
        OUTPUT_DIR
        / date_value
        / "配套试卷"
        / "听力"
    )

    if not audio_dir.is_dir():
        return None

    preferred = audio_dir / f"Listening_{part}.{AUDIO_FORMAT}"

    if preferred.is_file() and preferred.stat().st_size > 0:
        return preferred

    for ext in ("mp3", "m4a", "wav"):
        candidate = audio_dir / f"Listening_{part}.{ext}"

        if candidate.is_file() and candidate.stat().st_size > 0:
            return candidate

    return None


# ======================================================================
# Parser V1.6
# ======================================================================

def run_parser(
    exam_file: Path,
    answer_file: Path,
) -> None:

    if not PARSER_PATH.is_file():
        fail(f"Parser 不存在：{PARSER_PATH}")

    if not exam_file.is_file():
        fail(f"试卷不存在：{exam_file}")

    if not answer_file.is_file():
        fail(f"答案解析不存在：{answer_file}")

    if EXAM_JSON.exists():
        EXAM_JSON.unlink()

    command = [
        sys.executable,
        str(PARSER_PATH),
        "--exam",
        str(exam_file),
        "--answers",
        str(answer_file),
        "--output",
        str(EXAM_JSON),
    ]

    log()
    log("============================================================")
    log("PARSER V1.6")
    log("============================================================")
    log(f"Exam    : {exam_file}")
    log(f"Answers : {answer_file}")

    result = subprocess.run(
        command,
        cwd=str(ROOT),
        text=True,
    )

    if result.returncode != 0:
        fail("Parser V1.6 执行失败")

    if not EXAM_JSON.is_file():
        fail(
            "Parser 执行结束，但没有生成 "
            f"{EXAM_JSON}"
        )

    log("✓ Parser JSON 已生成")


# ======================================================================
# Exam 数据验证
# ======================================================================

EXPECTED_COUNTS = {
    "listening": 15,
    "single_choice": 10,
    "multiple_choice": 10,
    "cloze": 10,
    "reading": 5,
    "translation": 10,
    "writing": 1,
}


def validate_exam(data: Dict[str, Any]) -> None:

    questions = data.get("questions")

    if not isinstance(questions, list):
        fail("Parser JSON 缺少 questions")

    if len(questions) != 61:
        fail(
            f"试卷题数错误：{len(questions)}，"
            f"期望 61"
        )

    counts: Dict[str, int] = {}

    ids = set()

    for q in questions:

        qid = str(q.get("question_id", "")).strip()

        if not qid:
            fail("发现空 question_id")

        if qid in ids:
            fail(f"重复 question_id：{qid}")

        ids.add(qid)

        qtype = str(q.get("type", "")).strip()

        counts[qtype] = counts.get(qtype, 0) + 1

    for key, expected in EXPECTED_COUNTS.items():

        actual = counts.get(key, 0)

        if actual != expected:
            fail(
                f"{key} 数量错误："
                f"{actual}，期望 {expected}"
            )

    log()
    log("✓ 61题结构验证通过")

    for key in EXPECTED_COUNTS:
        log(f"  {key:16s}: {counts.get(key, 0)}")


# ======================================================================
# Adapter V1.0 安全层
# ======================================================================

SAFE_FIELDS = {
    "question_id",
    "type",
    "id",
    "section",
    "number",
    "part",
    "question",
    "options",
}


FORBIDDEN_FIELDS = {
    "correct_answer",
    "answer",
    "explanation",
    "reference_answer",
}


def build_safe_exam(
    parser_data: Dict[str, Any],
) -> Dict[str, Any]:

    safe_questions = []

    for source_q in parser_data["questions"]:

        safe_q = {}

        for key in SAFE_FIELDS:

            if key not in source_q:
                continue

            value = source_q[key]

            safe_q[key] = copy.deepcopy(value)

        for forbidden in FORBIDDEN_FIELDS:

            if forbidden in safe_q:
                del safe_q[forbidden]

        safe_questions.append(safe_q)

    safe_exam = {
        "version": "1.0",
        "source": {
            "exam_date": CURRENT_DATE,
            "exam_file": (
                str(CURRENT_EXAM_FILE)
                if CURRENT_EXAM_FILE
                else ""
            ),
        },
        "exam": {
            "total_questions": len(safe_questions),
            "questions": safe_questions,
        },
        "security": {
            "correct_answers_removed": True,
            "answer_explanations_removed": True,
            "reference_answers_removed": True,
            "grading_hidden": True,
        },
    }

    return safe_exam


def validate_safe_exam(
    safe_exam: Dict[str, Any],
) -> None:

    payload = json.dumps(
        safe_exam,
        ensure_ascii=False,
    )

    for forbidden in FORBIDDEN_FIELDS:

        if forbidden in payload:
            fail(
                f"安全检查失败：发现禁止字段 "
                f"{forbidden}"
            )

    questions = safe_exam.get("exam", {}).get(
        "questions",
        [],
    )

    if len(questions) != 61:
        fail(
            "安全考试数据题数不是 61"
        )

    json_dump(
        SAFE_EXAM_JSON,
        safe_exam,
    )

    log("✓ Adapter 安全隔离通过")
    log("✓ 初始答题数据不包含答案与解析")


# ======================================================================
# 加载完整考试数据
# ======================================================================

def load_exam() -> None:

    global QUESTIONS
    global QUESTION_MAP

    parser_data = json_load(EXAM_JSON)

    validate_exam(parser_data)

    QUESTIONS = parser_data["questions"]

    QUESTION_MAP = {
        str(q["question_id"]): q
        for q in QUESTIONS
    }

    safe_exam = build_safe_exam(parser_data)

    validate_safe_exam(safe_exam)


# ======================================================================
# 飞书 Token
# ======================================================================

def get_tenant_access_token() -> str:

    url = (
        "https://open.feishu.cn/open-apis/"
        "auth/v3/tenant_access_token/internal"
    )

    response = requests.post(
        url,
        json={
            "app_id": APP_ID,
            "app_secret": APP_SECRET,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:
        fail(
            "获取 tenant_access_token 失败："
            + json.dumps(
                data,
                ensure_ascii=False,
            )
        )

    return data["tenant_access_token"]


# ======================================================================
# 查找群
# ======================================================================

def find_chat_id() -> str:

    token = get_tenant_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    page_token = ""

    while True:

        params = {
            "page_size": 100,
        }

        if page_token:
            params["page_token"] = page_token

        response = requests.get(
            "https://open.feishu.cn/open-apis/im/v1/chats",
            headers=headers,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:
            fail(
                "获取群列表失败："
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        for chat in data.get("data", {}).get(
            "items",
            [],
        ):

            if chat.get("name") == FEISHU_CHAT_NAME:
                return chat["chat_id"]

        page_token = (
            data.get("data", {}).get(
                "page_token"
            )
            or ""
        )

        if not page_token:
            break

    fail(
        f"没有找到飞书群：{FEISHU_CHAT_NAME}"
    )

    return ""


# ======================================================================
# 飞书发送卡片
# ======================================================================

def send_card(
    card_data: Dict[str, Any],
) -> str:

    if API_CLIENT is None:
        fail("API_CLIENT 尚未初始化")

    if not CHAT_ID:
        fail("CHAT_ID 尚未初始化")

    content = json.dumps(
        card_data,
        ensure_ascii=False,
    )

    request = (
        CreateMessageRequest.builder()
        .receive_id_type("chat_id")
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(CHAT_ID)
            .msg_type("interactive")
            .content(content)
            .build()
        )
        .build()
    )

    response = API_CLIENT.im.v1.message.create(
        request
    )

    if not response.success():
        fail(
            "发送飞书卡片失败："
            + str(response)
        )

    data = response.data

    return getattr(data, "message_id", "") or ""


# ======================================================================
# 选卷卡
# ======================================================================

def build_exam_selector_card(
    dates: List[str],
) -> Dict[str, Any]:

    options = []

    for date_value in dates:

        options.append({
            "text": {
                "tag": "plain_text",
                "content": date_value,
            },
            "value": date_value,
        })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "748686 英语考试中心",
            },
            "template": "blue",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            "### 📚 开始英语考试\n\n"
                            "请选择你要参加的考试日期。"
                        ),
                    },
                },
                {
                    "tag": "hr",
                },
                {
                    "tag": "form",
                    "name": "exam_selector_form",
                    "elements": [
                        {
                            "tag": "select_static",
                            "name": "exam_date",
                            "required": True,
                            "placeholder": {
                                "tag": "plain_text",
                                "content": "请选择考试日期",
                            },
                            "options": options,
                        },
                        {
                            "tag": "button",
                            "name": "continue_date",
                            "action_type": "form_submit",
                            "type": "primary",
                            "text": {
                                "tag": "plain_text",
                                "content": "下一步：选择试卷",
                            },
                        },
                    ],
                },
            ],
        },
    }


def build_exam_list_card(
    date_value: str,
    exams: List[Path],
) -> Dict[str, Any]:

    options = []

    for exam in exams:

        options.append({
            "text": {
                "tag": "plain_text",
                "content": exam.stem,
            },
            "value": exam.name,
        })

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "748686 英语考试中心",
            },
            "template": "blue",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            "### 📅 已选择考试日期\n\n"
                            f"**{date_value}**\n\n"
                            "请选择对应试卷。"
                        ),
                    },
                },
                {
                    "tag": "hr",
                },
                {
                    "tag": "form",
                    "name": "exam_file_form",
                    "elements": [
                        {
                            "tag": "select_static",
                            "name": "exam_file",
                            "required": True,
                            "placeholder": {
                                "tag": "plain_text",
                                "content": "请选择试卷",
                            },
                            "options": options,
                        },
                        {
                            "tag": "button",
                            "name": "start_exam",
                            "action_type": "form_submit",
                            "type": "primary",
                            "text": {
                                "tag": "plain_text",
                                "content": "🚀 开始考试",
                            },
                        },
                    ],
                },
            ],
        },
    }


# ======================================================================
# 题目卡
# ======================================================================

def build_choice_card(
    question: Dict[str, Any],
) -> Dict[str, Any]:

    qid = question["question_id"]

    qtype = question["type"]

    number = question.get(
        "number",
        "?",
    )

    question_text = question.get(
        "question",
        "",
    )

    options = question.get(
        "options",
        {},
    )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{question_text}**"
                ),
            },
        },
        {
            "tag": "hr",
        },
    ]

    option_lines = []

    if isinstance(options, dict):

        for key, value in options.items():

            option_lines.append(
                f"**{key}.** {value}"
            )

    elif isinstance(options, list):

        for item in options:
            option_lines.append(str(item))

    if option_lines:

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(
                    option_lines
                ),
            },
        })

        elements.append({
            "tag": "hr",
        })

    buttons = []

    for key in ("A", "B", "C", "D"):

        if isinstance(options, dict):
            if key not in options:
                continue

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
                        "question_id": qid,
                        "answer": key,
                    },
                },
            ],
        })

    if buttons:

        elements.append({
            "tag": "column_set",
            "flex_mode": "none",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [button],
                }
                for button in buttons
            ],
        })

    if qtype == "listening":

        part = question.get("part")

        audio_key = AUDIO_FILE_KEYS.get(
            str(part),
            "",
        )

        if audio_key:

            elements.insert(
                1,
                {
                    "tag": "audio",
                    "file_key": audio_key,
                    "name": (
                        f"Listening_{part}"
                    ),
                },
            )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"英语答题测试 · 第 {number} 题"
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ======================================================================
# 多选卡
# ======================================================================

def build_multiple_card(
    question: Dict[str, Any],
) -> Dict[str, Any]:

    qid = question["question_id"]

    number = question.get(
        "number",
        "?",
    )

    options = question.get(
        "options",
        {},
    )

    selected = MULTIPLE_SELECTION.get(
        qid,
        set(),
    )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**{question['question']}**"
                ),
            },
        },
        {
            "tag": "hr",
        },
    ]

    for key, value in options.items():

        prefix = (
            "☑️"
            if key in selected
            else "⬜"
        )

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"{prefix} **{key}.** {value}"
                ),
            },
        })

    elements.append({
        "tag": "hr",
    })

    current = (
        "、".join(sorted(selected))
        if selected
        else "尚未选择"
    )

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                f"**当前选择：{current}**"
            ),
        },
    })

    elements.append({
        "tag": "hr",
    })

    buttons = []

    for key in ("A", "B", "C", "D"):

        if key not in options:
            continue

        buttons.append({
            "tag": "button",
            "text": {
                "tag": "plain_text",
                "content": key,
            },
            "type": (
                "primary"
                if key in selected
                else "default"
            ),
            "behaviors": [
                {
                    "type": "callback",
                    "value": {
                        "action": "toggle_multiple",
                        "question_id": qid,
                        "answer": key,
                    },
                },
            ],
        })

    elements.append({
        "tag": "column_set",
        "flex_mode": "none",
        "columns": [
            {
                "tag": "column",
                "width": "weighted",
                "weight": 1,
                "elements": [button],
            }
            for button in buttons
        ],
    })

    elements.append({
        "tag": "button",
        "name": f"submit_{qid}",
        "type": "primary",
        "text": {
            "tag": "plain_text",
            "content": "提交多选答案",
        },
        "behaviors": [
            {
                "type": "callback",
                "value": {
                    "action": "submit_multiple",
                    "question_id": qid,
                },
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
                    f"英语答题测试 · 第 {number} 题"
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ======================================================================
# 文本题卡
# ======================================================================

def build_text_card(
    question: Dict[str, Any],
) -> Dict[str, Any]:

    qid = question["question_id"]

    number = question.get(
        "number",
        "?",
    )

    qtype = question["type"]

    if qtype == "translation":
        title = "翻译题"
        placeholder = "请输入你的翻译答案"
        max_length = 4000
    else:
        title = "写作题"
        placeholder = "请输入你的作文"
        max_length = 12000

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"{title} · 第 {number} 题"
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**{question['question']}**"
                        ),
                    },
                },
                {
                    "tag": "hr",
                },
                {
                    "tag": "form",
                    "name": f"form_{qid}",
                    "elements": [
                        {
                            "tag": "input",
                            "name": "answer",
                            "required": True,
                            "input_type": "multiline_text",
                            "placeholder": {
                                "tag": "plain_text",
                                "content": placeholder,
                            },
                            "max_length": max_length,
                        },
                        {
                            "tag": "button",
                            "name": f"submit_{qid}",
                            "action_type": "form_submit",
                            "type": "primary",
                            "text": {
                                "tag": "plain_text",
                                "content": "提交答案",
                            },
                        },
                    ],
                },
            ],
        },
    }


# ======================================================================
# 已回答卡片
# ======================================================================

def build_answered_card(
    question: Dict[str, Any],
    user_answer: str,
) -> Dict[str, Any]:

    correct_answer = str(
        question.get(
            "correct_answer",
            "",
        )
    )

    is_correct = (
        user_answer == correct_answer
    )

    if is_correct:

        result_text = "✅ **回答正确**"
        template = "green"

    else:

        result_text = "❌ **回答错误**"
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

    options = question.get(
        "options",
        {},
    )

    option_lines = []

    if isinstance(options, dict):

        for key, value in options.items():
            option_lines.append(
                f"**{key}.** {value}"
            )

    if option_lines:

        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(
                    option_lines
                ),
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
                f"**你的答案：{user_answer}**"
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
                f"**正确答案：{correct_answer}**"
            ),
        },
    })

    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": (
                "**解析：**\n"
                f"{question.get('explanation', '')}"
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


# ======================================================================
# 主观题提交后
# ======================================================================

def build_manual_submitted_card(
    question: Dict[str, Any],
    answer: str,
) -> Dict[str, Any]:

    number = question.get(
        "number",
        "?",
    )

    qtype = question.get(
        "type",
        "",
    )

    title = (
        "翻译题"
        if qtype == "translation"
        else "写作题"
    )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": (
                    f"{title} · 第 {number} 题"
                    " · 已提交"
                ),
            },
            "template": "orange",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
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
                            "**你的答案：**\n"
                            f"{answer}"
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
                            "📝 **已提交，待人工批改**"
                        ),
                    },
                },
            ],
        },
    }


# ======================================================================
# 音频上传
# ======================================================================

def upload_feishu_file(
    path: Path,
) -> str:

    token = get_tenant_access_token()

    headers = {
        "Authorization": f"Bearer {token}",
    }

    with path.open("rb") as f:

        response = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers=headers,
            params={
                "parent_type": "im",
                "parent_node": CHAT_ID or "",
            },
            files={
                "file": (
                    path.name,
                    f,
                    "audio/mpeg",
                ),
            },
            data={
                "file_type": "stream",
            },
            timeout=120,
        )

    response.raise_for_status()

    data = response.json()

    if data.get("code") != 0:
        fail(
            "飞书音频上传失败："
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
        fail("飞书音频上传没有返回 file_key")

    return file_key


def prepare_audio(
    date_value: str,
) -> None:

    AUDIO_FILE_KEYS.clear()

    for part in ("A", "B", "C"):

        path = audio_path(
            date_value,
            part,
        )

        if not path:
            log(
                f"⚠️ Listening {part} "
                "音频不存在，跳过上传"
            )
            continue

        log(
            f"上传 Listening {part}："
            f"{path.name}"
        )

        key = upload_feishu_file(path)

        AUDIO_FILE_KEYS[part] = key

    log("✓ Listening 音频处理完成")


# ======================================================================
# Session 状态
# ======================================================================

def save_session_state() -> None:

    with STATE_LOCK:

        payload = {
            "session_id": SESSION_ID,
            "date": CURRENT_DATE,
            "exam_file": CURRENT_EXAM_FILE,
            "answer_state": ANSWER_STATE,
            "multiple_selection": {
                key: sorted(value)
                for key, value
                in MULTIPLE_SELECTION.items()
            },
            "updated_at": time.time(),
        }

        json_dump(
            SESSION_JSON,
            payload,
        )


def load_session_state() -> None:

    if not SESSION_JSON.is_file():
        return

    try:

        data = json_load(SESSION_JSON)

        stored_session = data.get(
            "session_id"
        )

        if stored_session != SESSION_ID:
            return

        ANSWER_STATE.update(
            data.get(
                "answer_state",
                {},
            )
        )

        for key, value in data.get(
            "multiple_selection",
            {},
        ).items():

            MULTIPLE_SELECTION[key] = set(
                value
            )

    except Exception as exc:

        log(
            f"⚠️ 恢复考试状态失败：{exc}"
        )


# ======================================================================
# 答案保存
# ======================================================================

def save_answers() -> None:

    payload = {
        "version": "1.0",
        "session_id": SESSION_ID,
        "exam_date": CURRENT_DATE,
        "exam_file": CURRENT_EXAM_FILE,
        "answers": ANSWER_STATE,
    }

    json_dump(
        ANSWERS_JSON,
        payload,
    )

    log("✓ 答案 JSON 已保存")


# ======================================================================
# Grader
# ======================================================================

def run_grader() -> Dict[str, Any]:

    if not GRADER_PATH.is_file():
        fail(
            f"Grader 不存在：{GRADER_PATH}"
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

    log()
    log("============================================================")
    log("ENGLISH EXAM GRADER V1.0")
    log("============================================================")

    result = subprocess.run(
        command,
        cwd=str(ROOT),
        text=True,
    )

    if result.returncode != 0:
        fail("Grader V1.0 执行失败")

    if not GRADER_OUTPUT.is_file():
        fail(
            "Grader 没有生成结果文件"
        )

    data = json_load(GRADER_OUTPUT)

    return data


# ======================================================================
# 最终成绩卡
# ======================================================================

def build_final_summary_card(
    result: Dict[str, Any],
) -> Dict[str, Any]:

    total = result.get(
        "total_questions",
        61,
    )

    auto_total = result.get(
        "auto_graded_questions",
        0,
    )

    correct = result.get(
        "auto_correct",
        0,
    )

    wrong = result.get(
        "auto_wrong",
        0,
    )

    manual = result.get(
        "manual_review_questions",
        0,
    )

    accuracy = result.get(
        "accuracy",
        0,
    )

    if isinstance(accuracy, float):
        accuracy_text = (
            f"{accuracy * 100:.1f}%"
            if accuracy <= 1
            else f"{accuracy:.1f}%"
        )
    else:
        accuracy_text = str(accuracy)

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "## 🎉 英语考试完成\n\n"
                    f"**考试日期：** {CURRENT_DATE}\n\n"
                    f"**试卷：** "
                    f"{Path(CURRENT_EXAM_FILE).stem "
                    f"if CURRENT_EXAM_FILE else ''}"
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
                    f"### 成绩\n\n"
                    f"**总题数：** {total}\n\n"
                    f"**自动评分：** {auto_total}\n\n"
                    f"**答对：** {correct}\n\n"
                    f"**答错：** {wrong}\n\n"
                    f"**正确率：** {accuracy_text}\n\n"
                    f"**人工批改：** {manual}"
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
                    "📝 翻译和写作已经提交，"
                    "等待人工批改。"
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
                "content": "748686 英语考试成绩",
            },
            "template": "green",
        },
        "body": {
            "elements": elements,
        },
    }


# ======================================================================
# 完成判断
# ======================================================================

def is_exam_complete() -> bool:

    return len(ANSWER_STATE) >= len(QUESTIONS)


# ======================================================================
# 单选 / 单项客观题
# ======================================================================

def handle_single_answer(
    question_id: str,
    user_answer: str,
) -> Dict[str, Any]:

    question = QUESTION_MAP[question_id]

    if question_id in ANSWER_STATE:
        return build_answered_card(
            question,
            str(
                ANSWER_STATE[question_id][
                    "answer"
                ]
            ),
        )

    ANSWER_STATE[question_id] = {
        "question_id": question_id,
        "answer": user_answer,
        "graded": True,
        "review_required": False,
    }

    save_session_state()

    # 注意：
    # 这里不向日志输出 correct_answer。

    card = build_answered_card(
        question,
        user_answer,
    )

    if is_exam_complete():
        finish_exam()

    return card


# ======================================================================
# 多选
# ======================================================================

def handle_multiple_toggle(
    question_id: str,
    answer: str,
) -> Dict[str, Any]:

    if question_id in ANSWER_STATE:
        return build_multiple_card(
            QUESTION_MAP[question_id]
        )

    selected = MULTIPLE_SELECTION.setdefault(
        question_id,
        set(),
    )

    if answer in selected:
        selected.remove(answer)
    else:
        selected.add(answer)

    save_session_state()

    return build_multiple_card(
        QUESTION_MAP[question_id]
    )


def normalize_answer_set(value: Any) -> Set[str]:

    if isinstance(value, str):

        value = value.replace(
            "，",
            ",",
        )

        return {
            item.strip().upper()
            for item in value.split(",")
            if item.strip()
        }

    if isinstance(value, list):

        return {
            str(item).strip().upper()
            for item in value
            if str(item).strip()
        }

    return set()


def handle_multiple_submit(
    question_id: str,
) -> Dict[str, Any]:

    question = QUESTION_MAP[question_id]

    if question_id in ANSWER_STATE:

        return build_answered_card(
            question,
            str(
                ANSWER_STATE[question_id][
                    "answer"
                ]
            ),
        )

    selected = MULTIPLE_SELECTION.get(
        question_id,
        set(),
    )

    answer_text = ",".join(
        sorted(selected)
    )

    ANSWER_STATE[question_id] = {
        "question_id": question_id,
        "answer": answer_text,
        "graded": True,
        "review_required": False,
    }

    save_session_state()

    if is_exam_complete():
        finish_exam()

    return build_answered_card(
        question,
        answer_text,
    )


# ======================================================================
# 翻译 / 写作
# ======================================================================

def handle_manual_submit(
    question_id: str,
    answer: str,
) -> Dict[str, Any]:

    question = QUESTION_MAP[question_id]

    if question_id in ANSWER_STATE:

        return build_manual_submitted_card(
            question,
            str(
                ANSWER_STATE[question_id][
                    "answer"
                ]
            ),
        )

    ANSWER_STATE[question_id] = {
        "question_id": question_id,
        "answer": answer,
        "graded": False,
        "review_required": True,
    }

    save_session_state()

    if is_exam_complete():
        finish_exam()

    return build_manual_submitted_card(
        question,
        answer,
    )


# ======================================================================
# 完成考试
# ======================================================================

def finish_exam() -> None:

    global SUMMARY_SENT

    with STATE_LOCK:

        if SUMMARY_SENT:
            return

        if not is_exam_complete():
            return

        save_answers()

        result = run_grader()

        SUMMARY_SENT = True

        card = build_final_summary_card(
            result
        )

        send_card(card)

        log()
        log("============================================================")
        log("✓ 61题考试完成")
        log("✓ 最终成绩卡已发送")
        log("============================================================")


# ======================================================================
# Form value
# ======================================================================

def get_form_values(
    action: Any,
) -> Dict[str, Any]:

    value = getattr(
        action,
        "form_value",
        None,
    )

    if value:
        return value

    try:

        data = action.to_dict()

        return data.get(
            "form_value",
            {},
        )

    except Exception:
        return {}


def get_action_name(
    action: Any,
) -> str:

    name = getattr(
        action,
        "name",
        None,
    )

    if name:
        return str(name)

    try:

        data = action.to_dict()

        return str(
            data.get(
                "name",
                "",
            )
        )

    except Exception:
        return ""


def get_action_dict(
    action: Any,
) -> Dict[str, Any]:

    try:
        return action.to_dict()
    except Exception:
        return {}


# ======================================================================
# Card callback
# ======================================================================

def make_card_callback_response(
    card_data: Dict[str, Any],
) -> P2CardActionTriggerResponse:

    response = P2CardActionTriggerResponse()

    card = CallBackCard()

    card.type = "raw"

    card.data = json.dumps(
        card_data,
        ensure_ascii=False,
    )

    response.card = card

    return response


def do_card_action_trigger(
    event: P2CardActionTrigger,
) -> P2CardActionTriggerResponse:

    action = event.event.action

    action_dict = get_action_dict(action)

    value = getattr(
        action,
        "value",
        None,
    )

    if value is None:
        value = action_dict.get(
            "value",
            {},
        )

    if not isinstance(value, dict):
        value = {}

    action_name = get_action_name(action)

    form_values = get_form_values(action)

    log()
    log("============================================================")
    log("FEISHU CARD ACTION")
    log("============================================================")
    log(f"action_name : {action_name}")
    log(f"value       : {value}")

    # --------------------------------------------------------------
    # 日期选择
    # --------------------------------------------------------------

    if (
        "exam_date" in form_values
        and action_name == "continue_date"
    ):

        selected_date = str(
            form_values["exam_date"]
        ).strip()

        dates = list_exam_dates()

        if selected_date not in dates:

            return make_card_callback_response(
                build_exam_selector_card(
                    dates
                )
            )

        exams = list_exam_files(
            selected_date
        )

        if not exams:

            return make_card_callback_response(
                {
                    "schema": "2.0",
                    "config": {
                        "wide_screen_mode": True,
                    },
                    "header": {
                        "title": {
                            "tag": "plain_text",
                            "content": "没有可用试卷",
                        },
                        "template": "red",
                    },
                    "body": {
                        "elements": [
                            {
                                "tag": "div",
                                "text": {
                                    "tag": "lark_md",
                                    "content": (
                                        f"日期 **{selected_date}** "
                                        "没有发现可用试卷。"
                                    ),
                                },
                            }
                        ],
                    },
                }
            )

        return make_card_callback_response(
            build_exam_list_card(
                selected_date,
                exams,
            )
        )

    # --------------------------------------------------------------
    # 试卷选择
    # --------------------------------------------------------------

    if (
        "exam_file" in form_values
        and action_name == "start_exam"
    ):

        selected_file = str(
            form_values["exam_file"]
        ).strip()

        if not CURRENT_DATE:
            # 当前 runner 尚未建立考试日期
            return make_card_callback_response(
                build_exam_selector_card(
                    list_exam_dates()
                )
            )

        candidate = (
            OUTPUT_DIR
            / CURRENT_DATE
            / "配套试卷"
            / safe_filename(selected_file)
        )

        if not candidate.is_file():
            return make_card_callback_response(
                build_exam_list_card(
                    CURRENT_DATE,
                    list_exam_files(
                        CURRENT_DATE
                    ),
                )
            )

        start_selected_exam(
            CURRENT_DATE,
            candidate,
        )

        # start_selected_exam 会准备题目并发送题卡。
        # 当前选择卡片只需要更新为“考试已启动”。
        return make_card_callback_response(
            {
                "schema": "2.0",
                "config": {
                    "wide_screen_mode": True,
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "考试已启动",
                    },
                    "template": "green",
                },
                "body": {
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    "## 🚀 考试已经开始\n\n"
                                    "试卷已经发送到群聊。\n\n"
                                    "请按照题目顺序完成 61 道题。"
                                ),
                            },
                        }
                    ],
                },
            }
        )

    # --------------------------------------------------------------
    # 普通选择题
    # --------------------------------------------------------------

    action_type = value.get(
        "action"
    )

    question_id = value.get(
        "question_id"
    )

    if (
        action_type == "answer"
        and question_id
    ):

        answer = str(
            value.get(
                "answer",
                "",
            )
        ).strip().upper()

        card = handle_single_answer(
            str(question_id),
            answer,
        )

        return make_card_callback_response(
            card
        )

    # --------------------------------------------------------------
    # 多选切换
    # --------------------------------------------------------------

    if (
        action_type == "toggle_multiple"
        and question_id
    ):

        answer = str(
            value.get(
                "answer",
                "",
            )
        ).strip().upper()

        card = handle_multiple_toggle(
            str(question_id),
            answer,
        )

        return make_card_callback_response(
            card
        )

    # --------------------------------------------------------------
    # 多选提交
    # --------------------------------------------------------------

    if (
        action_type == "submit_multiple"
        and question_id
    ):

        card = handle_multiple_submit(
            str(question_id)
        )

        return make_card_callback_response(
            card
        )

    # --------------------------------------------------------------
    # 文本题
    # --------------------------------------------------------------

    if (
        form_values
        and action_name.startswith("submit_")
    ):

        qid = action_name[
            len("submit_"):
        ]

        answer = str(
            form_values.get(
                "answer",
                "",
            )
        ).strip()

        if qid in QUESTION_MAP:

            card = handle_manual_submit(
                qid,
                answer,
            )

            return make_card_callback_response(
                card
            )

    # 未识别动作
    return make_card_callback_response(
        {
            "schema": "2.0",
            "config": {
                "wide_screen_mode": True,
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "操作未识别",
                },
                "template": "orange",
            },
            "body": {
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": (
                                "⚠️ 当前操作没有被识别。\n\n"
                                "请重新操作。"
                            ),
                        },
                    }
                ],
            },
        }
    )


# ======================================================================
# WebSocket callback
# ======================================================================

def callback(
    event: P2CardActionTrigger,
) -> P2CardActionTriggerResponse:

    try:
        return do_card_action_trigger(event)

    except Exception as exc:

        log(
            f"❌ Card callback error: {exc}"
        )

        return make_card_callback_response(
            {
                "schema": "2.0",
                "config": {
                    "wide_screen_mode": True,
                },
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": "考试系统错误",
                    },
                    "template": "red",
                },
                "body": {
                    "elements": [
                        {
                            "tag": "div",
                            "text": {
                                "tag": "lark_md",
                                "content": (
                                    "❌ 当前操作处理失败。\n\n"
                                    "请稍后重试。"
                                ),
                            },
                        }
                    ],
                },
            }
        )


# ======================================================================
# 启动考试
# ======================================================================

def start_selected_exam(
    date_value: str,
    exam_file: Path,
) -> None:

    global CURRENT_DATE
    global CURRENT_EXAM_FILE
    global CURRENT_ANSWER_FILE

    CURRENT_DATE = date_value

    CURRENT_EXAM_FILE = str(
        exam_file.relative_to(ROOT)
    )

    answer_file = answer_file_for_exam(
        exam_file
    )

    if not answer_file:
        fail(
            "没有找到对应答案解析："
            f"{exam_file}"
        )

    CURRENT_ANSWER_FILE = str(
        answer_file.relative_to(ROOT)
    )

    log()
    log("============================================================")
    log("START SELECTED ENGLISH EXAM")
    log("============================================================")
    log(f"DATE    : {CURRENT_DATE}")
    log(f"EXAM    : {CURRENT_EXAM_FILE}")
    log(f"ANSWER  : {CURRENT_ANSWER_FILE}")

    run_parser(
        exam_file,
        answer_file,
    )

    load_exam()

    prepare_audio(
        date_value
    )

    ANSWER_STATE.clear()
    MULTIPLE_SELECTION.clear()

    save_session_state()

    # --------------------------------------------------------------
    # 发送全部 61 题
    # --------------------------------------------------------------

    log()
    log("============================================================")
    log("SEND 61 QUESTIONS")
    log("============================================================")

    for index, question in enumerate(
        QUESTIONS,
        start=1,
    ):

        qtype = question["type"]

        if qtype == "multiple_choice":

            card = build_multiple_card(
                question
            )

        elif qtype in {
            "translation",
            "writing",
        }:

            card = build_text_card(
                question
            )

        else:

            card = build_choice_card(
                question
            )

        send_card(card)

        log(
            f"✓ 已发送第 {index}/61 题"
        )

        time.sleep(0.15)

    log()
    log("✓ 61题全部发送完成")


# ======================================================================
# 发送入口卡
# ======================================================================

def send_selector() -> None:

    dates = list_exam_dates()

    if not dates:
        fail(
            "Output 中没有发现可用英语试卷日期"
        )

    card = build_exam_selector_card(
        dates
    )

    send_card(card)

    log(
        "✓ 飞书英语考试选择卡已发送"
    )


# ======================================================================
# 主程序
# ======================================================================

def main() -> None:

    global API_CLIENT
    global CHAT_ID

    if not APP_ID:
        fail("APP_ID 未配置")

    if not APP_SECRET:
        fail("APP_SECRET 未配置")

    if not ENGLISH_ROOT.exists():
        fail(
            f"英语学习系统目录不存在："
            f"{ENGLISH_ROOT}"
        )

    if not OUTPUT_DIR.exists():
        fail(
            f"英语 Output 不存在："
            f"{OUTPUT_DIR}"
        )

    log()
    log("######################################################################")
    log("748686 英语学习系统")
    log("Feishu Full English Exam Runner V8.1")
    log("######################################################################")

    log()
    log(f"ROOT       : {ROOT}")
    log(f"OUTPUT     : {OUTPUT_DIR}")
    log(f"FEISHU CHAT: {FEISHU_CHAT_NAME}")
    log(f"SESSION    : {SESSION_ID}")

    CHAT_ID = find_chat_id()

    log(f"✓ Chat ID：{CHAT_ID}")

    API_CLIENT = (
        lark.Client.builder()
        .app_id(APP_ID)
        .app_secret(APP_SECRET)
        .build()
    )

    # --------------------------------------------------------------
    # 关键：
    # WebSocket 必须先启动
    # 再发送选择卡。
    #
    # 防止“卡片已经出现，但 callback 尚未监听”的竞态。
    # --------------------------------------------------------------

    event_handler = (
        lark.EventDispatcherHandler.builder(
            "",
            "",
        )
        .register_p2_card_action_trigger(
            callback
        )
        .build()
    )

    ws_client = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=event_handler,
        log_level=lark.LogLevel.INFO,
    )

    log()
    log("============================================================")
    log("START FEISHU LONG CONNECTION")
    log("============================================================")

    # WebSocket 放到后台线程。
    ws_thread = threading.Thread(
        target=ws_client.start,
        daemon=True,
    )

    ws_thread.start()

    time.sleep(3)

    send_selector()

    log()
    log("============================================================")
    log("✓ FEISHU EXAM CENTER READY")
    log("============================================================")
    log("等待飞书选择日期 / 试卷并开始考试……")

    try:

        while True:

            if SUMMARY_SENT:
                log(
                    "考试已经完成，保持 Runner "
                    "短暂在线后退出。"
                )

                time.sleep(10)

                break

            time.sleep(5)

    except KeyboardInterrupt:

        log("收到终止信号")

    finally:

        save_session_state()


if __name__ == "__main__":
    main()
