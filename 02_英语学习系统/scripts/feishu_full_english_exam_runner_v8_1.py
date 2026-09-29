#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Full English Exam Runner V8.1

职责
----
1. 读取 Parser V1.6.1 生成的完整考试 JSON
2. 使用 Feishu Adapter 构建安全题目数据
3. 向指定飞书群发送完整 61 题
4. 支持：
   - 单选
   - 多选
   - 完形
   - 阅读
   - 听力
   - 翻译
   - 写作
5. 用户提交后立即更新题卡
6. 61 题全部提交后调用 Grader V1.0
7. 生成最终成绩卡
8. 每次提交都保存答案状态
9. 不向飞书初始题卡泄露正确答案
10. 不在生产日志中打印正确答案

听力处理
--------
- 飞书文件上传 API 不接受 file_type=mp3
- MP3 自动转换为 OPUS
- 使用 file_type=opus 上传
- 上传后取得 file_key
- 听力题卡使用 file_key 播放

原则
----
- Parser V1.6.1 不修改
- Grader V1.0 不修改
- Adapter 不修改
- 初始题卡只使用安全题目数据
- 正确答案只存在 Runner 内部
- 多选必须完全匹配
- 翻译 / 写作进入人工批改
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any

import requests

import lark_oapi as lark

from lark_oapi.event.callback.model.p2_card_action_trigger import (
    P2CardActionTrigger,
    P2CardActionTriggerResponse,
    CallBackCard,
)


# ============================================================
# 基础配置
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SCRIPTS_DIR = BASE_DIR / "scripts"

ADAPTER_PATH = SCRIPTS_DIR / "feishu_english_exam.py"

GRADER_PATH = SCRIPTS_DIR / "english_exam_grader.py"

EXAM_JSON = Path(
    os.environ.get(
        "EXAM_JSON",
        "/tmp/748686_exam_parser_v1_6.json",
    )
)

ANSWERS_JSON = Path(
    os.environ.get(
        "ANSWERS_JSON",
        "/tmp/748686_feishu_answers.json",
    )
)

GRADER_OUTPUT = Path(
    os.environ.get(
        "GRADER_OUTPUT",
        "/tmp/748686_feishu_grader_result.json",
    )
)

STATE_FILE = Path(
    os.environ.get(
        "FEISHU_STATE_FILE",
        "/tmp/748686_feishu_exam_state.json",
    )
)

APP_ID = os.environ.get(
    "APP_ID",
    "",
).strip()

APP_SECRET = os.environ.get(
    "APP_SECRET",
    "",
).strip()

FEISHU_CHAT_NAME = os.environ.get(
    "FEISHU_CHAT_NAME",
    "748686知识系统",
).strip()

EXAM_DATE = os.environ.get(
    "EXAM_DATE",
    "",
).strip()

AUDIO_FORMAT = os.environ.get(
    "AUDIO_FORMAT",
    "mp3",
).strip().lower()

PERSIST_GITHUB = (
    os.environ.get(
        "PERSIST_GITHUB",
        "false",
    ).lower()
    == "true"
)

PERSIST_GITHUB_PATH = os.environ.get(
    "PERSIST_GITHUB_PATH",
    ".feishu_state",
).strip()

EXPECTED_TOTAL = 61

EXPECTED_COUNTS = {
    "listening": 15,
    "single_choice": 10,
    "multiple_choice": 10,
    "cloze": 10,
    "reading": 5,
    "translation": 10,
    "writing": 1,
}


# ============================================================
# 全局状态
# ============================================================

QUESTIONS: list[dict[str, Any]] = []

SAFE_QUESTIONS: list[dict[str, Any]] = []

QUESTION_MAP: dict[str, dict[str, Any]] = {}

SAFE_QUESTION_MAP: dict[str, dict[str, Any]] = {}

ANSWER_STATE: dict[str, dict[str, Any]] = {}

MULTIPLE_SELECTION: dict[str, set[str]] = {}

AUDIO_FILE_KEYS: dict[str, str] = {}

SUMMARY_SENT = False

STATE_LOCK = threading.RLock()

WS_CLIENT = None

RUNTIME_TOKEN = ""

RUNTIME_CHAT_ID = ""


# ============================================================
# 通用工具
# ============================================================

def log(message: str) -> None:

    print(
        message,
        flush=True,
    )


def fail(message: str) -> None:

    print(
        f"❌ {message}",
        flush=True,
    )

    raise SystemExit(1)


def atomic_write_json(
    path: Path,
    data: Any,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_suffix(
        path.suffix + ".tmp"
    )

    with open(
        tmp,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )

    tmp.replace(path)


def load_json(
    path: Path,
) -> Any:

    if not path.exists():

        fail(
            f"JSON 文件不存在: {path}"
        )

    with open(
        path,
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


# ============================================================
# Parser JSON
# ============================================================

def load_exam() -> None:

    global QUESTIONS
    global QUESTION_MAP

    data = load_json(
        EXAM_JSON
    )

    QUESTIONS = data.get(
        "questions",
        [],
    )

    if not isinstance(
        QUESTIONS,
        list,
    ):

        fail(
            "Parser JSON 的 questions 不是列表"
        )

    QUESTION_MAP = {
        q["question_id"]: q
        for q in QUESTIONS
        if q.get("question_id")
    }


def validate_exam() -> None:

    if len(QUESTIONS) != EXPECTED_TOTAL:

        fail(
            f"题目数量错误: "
            f"{len(QUESTIONS)} / {EXPECTED_TOTAL}"
        )

    counts: dict[str, int] = {}

    seen: set[str] = set()

    for q in QUESTIONS:

        qid = q.get(
            "question_id"
        )

        if not qid:

            fail(
                "存在没有 question_id 的题目"
            )

        if qid in seen:

            fail(
                f"重复 question_id: {qid}"
            )

        seen.add(qid)

        qtype = q.get(
            "type",
            "",
        )

        counts[qtype] = (
            counts.get(
                qtype,
                0,
            )
            + 1
        )

    for qtype, expected in EXPECTED_COUNTS.items():

        actual = counts.get(
            qtype,
            0,
        )

        if actual != expected:

            fail(
                f"{qtype} 数量错误: "
                f"{actual} / {expected}"
            )

    log("")

    log(
        "=" * 70
    )

    log(
        "748686 FEISHU FULL ENGLISH EXAM V8.1"
    )

    log(
        "=" * 70
    )

    log(
        f"考试日期: "
        f"{EXAM_DATE or '未指定'}"
    )

    log(
        f"总题数: {len(QUESTIONS)}"
    )

    for qtype, expected in EXPECTED_COUNTS.items():

        log(
            f"  {qtype:<16} {expected}"
        )

    log(
        "=" * 70
    )


# ============================================================
# Adapter
# ============================================================

def load_adapter_module():

    if not ADAPTER_PATH.exists():

        fail(
            f"Feishu Adapter 不存在: "
            f"{ADAPTER_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "feishu_english_exam_adapter",
        ADAPTER_PATH,
    )

    if (
        spec is None
        or spec.loader is None
    ):

        fail(
            "无法加载 Feishu Adapter"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def build_safe_exam() -> None:

    global SAFE_QUESTIONS
    global SAFE_QUESTION_MAP

    adapter = load_adapter_module()

    builder = getattr(
        adapter,
        "build_feishu_exam",
        None,
    )

    if builder is None:

        builder = getattr(
            adapter,
            "build_exam_for_feishu",
            None,
        )

    if builder is None:

        fail(
            "Feishu Adapter 中找不到 "
            "build_feishu_exam / build_exam_for_feishu"
        )

    safe_exam = builder(
        {
            "questions": QUESTIONS,
            "total_questions": len(QUESTIONS),
        }
    )

    SAFE_QUESTIONS = (
        safe_exam.get(
            "exam",
            {},
        )
        .get(
            "questions",
            [],
        )
    )

    if len(SAFE_QUESTIONS) != EXPECTED_TOTAL:

        fail(
            "Adapter 安全题目数量错误: "
            f"{len(SAFE_QUESTIONS)} / {EXPECTED_TOTAL}"
        )

    SAFE_QUESTION_MAP = {
        q["question_id"]: q
        for q in SAFE_QUESTIONS
    }

    forbidden = {
        "correct_answer",
        "answer",
        "explanation",
        "reference_answer",
    }

    for q in SAFE_QUESTIONS:

        leaked = forbidden.intersection(
            q.keys()
        )

        if leaked:

            fail(
                f"Adapter 安全检查失败: "
                f"{q['question_id']} "
                f"存在禁止字段 {sorted(leaked)}"
            )

    log(
        "✅ Feishu Adapter 安全检查通过"
    )


# ============================================================
# Feishu Token
# ============================================================

def get_tenant_access_token() -> str:

    if not APP_ID or not APP_SECRET:

        fail(
            "APP_ID / APP_SECRET 未设置"
        )

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

    if data.get("code") != 0:

        fail(
            "获取 tenant_access_token 失败: "
            + json.dumps(
                data,
                ensure_ascii=False,
            )
        )

    return data["tenant_access_token"]


# ============================================================
# Chat
# ============================================================

def find_chat_id(
    token: str,
) -> str:

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
                "读取飞书群失败: "
                + json.dumps(
                    data,
                    ensure_ascii=False,
                )
            )

        for chat in data.get(
            "data",
            {},
        ).get(
            "items",
            [],
        ):

            name = chat.get(
                "name",
                "",
            )

            if name == FEISHU_CHAT_NAME:

                return chat["chat_id"]

        page_token = (
            data.get(
                "data",
                {},
            )
            .get(
                "page_token"
            )
        )

        if not page_token:

            break

    fail(
        f"没有找到飞书群: "
        f"{FEISHU_CHAT_NAME}"
    )

    return ""


# ============================================================
# 听力格式转换
# ============================================================

def find_ffmpeg() -> str:

    ffmpeg = shutil.which(
        "ffmpeg"
    )

    if ffmpeg:

        return ffmpeg

    fail(
        "系统中没有找到 ffmpeg，"
        "无法将 MP3 转换为 OPUS"
    )

    return ""


def convert_audio_to_opus(
    source_path: Path,
) -> Path:

    if not source_path.exists():

        fail(
            f"源听力文件不存在: "
            f"{source_path}"
        )

    if source_path.stat().st_size <= 0:

        fail(
            f"源听力文件为空: "
            f"{source_path}"
        )

    if (
        source_path.suffix
        .lower()
        == ".opus"
    ):

        return source_path

    ffmpeg = find_ffmpeg()

    output_dir = (
        Path("/tmp")
        / "748686_feishu_opus"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        output_dir
        / f"{source_path.stem}.opus"
    )

    # --------------------------------------------------------
    # 每次重新生成，避免旧 OPUS 与新 MP3 不一致
    # --------------------------------------------------------

    if output_path.exists():

        try:

            output_path.unlink()

        except Exception:

            pass

    log(
        f"  🎧 MP3 → OPUS: "
        f"{source_path.name}"
    )

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(source_path),
        "-acodec",
        "libopus",
        "-ac",
        "1",
        "-ar",
        "16000",
        str(output_path),
    ]

    result = subprocess.run(
        command,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:

        log(
            result.stdout
        )

        log(
            result.stderr
        )

        fail(
            f"MP3 转 OPUS 失败: "
            f"{source_path.name}"
        )

    if not output_path.exists():

        fail(
            f"ffmpeg 执行成功但没有生成 OPUS: "
            f"{output_path}"
        )

    if output_path.stat().st_size <= 0:

        fail(
            f"生成的 OPUS 文件为空: "
            f"{output_path}"
        )

    log(
        f"  ✅ OPUS 已生成: "
        f"{output_path.name}"
    )

    return output_path


# ============================================================
# 文件上传
# ============================================================

def upload_feishu_file(
    token: str,
    file_path: Path,
) -> str:

    if not file_path.exists():

        fail(
            f"听力文件不存在: {file_path}"
        )

    if file_path.stat().st_size <= 0:

        fail(
            f"听力文件为空: {file_path}"
        )

    # --------------------------------------------------------
    # 飞书音频上传：
    # file_type 必须使用 opus
    # file_name 必须包含 .opus 后缀
    # --------------------------------------------------------

    if (
        file_path.suffix
        .lower()
        != ".opus"
    ):

        fail(
            "Feishu 音频上传函数收到的不是 OPUS 文件: "
            f"{file_path.name}"
        )

    headers = {
        "Authorization":
            f"Bearer {token}",
    }

    with open(
        file_path,
        "rb",
    ) as f:

        files = {
            "file": (
                file_path.name,
                f,
                "audio/ogg",
            )
        }

        data = {
            "file_type": "opus",
            "file_name": file_path.name,
        }

        response = requests.post(
            "https://open.feishu.cn/open-apis/im/v1/files",
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    # --------------------------------------------------------
    # HTTP 错误诊断
    # --------------------------------------------------------

    if not response.ok:

        print()

        print(
            "=" * 70
        )

        print(
            "❌ 飞书文件上传失败"
        )

        print(
            "=" * 70
        )

        print(
            "HTTP:",
            response.status_code,
        )

        print(
            "URL:",
            response.url,
        )

        print(
            "File:",
            file_path.name,
        )

        print(
            "File Type: opus"
        )

        print(
            "Response:",
            response.text,
        )

        print(
            "=" * 70
        )

        print()

        response.raise_for_status()

    result = response.json()

    # --------------------------------------------------------
    # Feishu API code 检查
    # --------------------------------------------------------

    if result.get("code") != 0:

        print()

        print(
            "=" * 70
        )

        print(
            "❌ 飞书文件上传 API 返回错误"
        )

        print(
            "=" * 70
        )

        print(
            "Code:",
            result.get("code"),
        )

        print(
            "Message:",
            result.get("msg"),
        )

        print(
            "File:",
            file_path.name,
        )

        print(
            "Response:",
            response.text,
        )

        print(
            "=" * 70
        )

        print()

        raise RuntimeError(
            "Feishu file upload failed: "
            f"code={result.get('code')}, "
            f"msg={result.get('msg')}"
        )

    file_key = (
        result.get(
            "data",
            {},
        )
        .get(
            "file_key"
        )
    )

    if not file_key:

        fail(
            "飞书文件上传成功但没有 "
            f"file_key: {file_path.name}"
        )

    return file_key


def prepare_audio(
    token: str,
) -> None:

    if not EXAM_DATE:

        log(
            "⚠️ 未设置 EXAM_DATE，"
            "跳过听力文件准备"
        )

        return

    audio_dir = (
        BASE_DIR
        / "output"
        / EXAM_DATE
        / "配套试卷"
        / "听力"
    )

    if not audio_dir.exists():

        log(
            f"⚠️ 听力目录不存在: "
            f"{audio_dir}"
        )

        return

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

        if not candidates:

            log(
                f"⚠️ 未找到听力 {part}"
            )

            continue

        audio_path = None

        # ----------------------------------------------------
        # 优先使用指定 AUDIO_FORMAT
        # ----------------------------------------------------

        for candidate in candidates:

            if (
                candidate.suffix
                .lower()
                .lstrip(".")
                == AUDIO_FORMAT
            ):

                audio_path = candidate

                break

        # ----------------------------------------------------
        # 找不到指定格式时使用第一个
        # ----------------------------------------------------

        if audio_path is None:

            audio_path = candidates[0]

        log(
            f"准备听力 {part}: "
            f"{audio_path.name}"
        )

        # ----------------------------------------------------
        # 转 OPUS
        # ----------------------------------------------------

        opus_path = convert_audio_to_opus(
            audio_path
        )

        log(
            f"上传听力 {part}: "
            f"{opus_path.name}"
        )

        file_key = upload_feishu_file(
            token,
            opus_path,
        )

        AUDIO_FILE_KEYS[part] = file_key

        log(
            f"  ✅ 听力 {part} 上传成功"
        )

    if len(AUDIO_FILE_KEYS) == 3:

        log(
            "✅ 听力 A/B/C 三组文件全部准备完成"
        )

    else:

        log(
            f"⚠️ 听力文件准备完成: "
            f"{len(AUDIO_FILE_KEYS)}/3 组"
        )


# ============================================================
# 卡片基础
# ============================================================

def md_escape(
    value: Any,
) -> str:

    if value is None:

        return ""

    return str(value)


def question_header(
    question: dict[str, Any],
) -> str:

    number = question.get(
        "number",
        "",
    )

    return (
        f"英语答题测试 · 第 {number} 题"
    )


def get_option_lines(
    question: dict[str, Any],
) -> str:

    options = question.get(
        "options",
        {},
    )

    lines = []

    for key in (
        "A",
        "B",
        "C",
        "D",
    ):

        if key in options:

            lines.append(
                f"**{key}.** "
                f"{md_escape(options[key])}"
            )

    return "\n".join(lines)


# ============================================================
# 单选 / 完形 / 阅读 / 听力
# ============================================================

def build_choice_card(
    question: dict[str, Any],
) -> dict[str, Any]:

    qid = question["question_id"]

    qtype = question.get(
        "type",
        "",
    )

    elements: list[dict[str, Any]] = []

    question_text = (
        f"**第 {question.get('number', '')} 题**\n\n"
        f"**{md_escape(question.get('question', ''))}**"
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": question_text,
            },
        }
    )

    if qtype == "listening":

        part = question.get(
            "part",
            "",
        )

        file_key = AUDIO_FILE_KEYS.get(
            part
        )

        if file_key:

            elements.append(
                {
                    "tag": "audio",
                    "file_key": file_key,
                }
            )

        else:

            elements.append(
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            "⚠️ **听力音频暂不可用**"
                        ),
                    },
                }
            )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": get_option_lines(
                    question
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    actions = []

    for key in (
        "A",
        "B",
        "C",
        "D",
    ):

        if key not in question.get(
            "options",
            {},
        ):

            continue

        actions.append(
            {
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
                    }
                ],
            }
        )

    if len(actions) < 4:

        return build_error_card(
            f"题目 {qid} 的选项不足 4 个"
        )

    elements.append(
        {
            "tag": "column_set",
            "flex_mode": "none",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[0]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[1]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[2]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[3]],
                },
            ],
        }
    )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": question_header(
                    question
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 多选
# ============================================================

def build_multiple_card(
    question: dict[str, Any],
    selected: set[str] | None = None,
) -> dict[str, Any]:

    qid = question["question_id"]

    selected = selected or set()

    elements: list[dict[str, Any]] = []

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**第 {question.get('number', '')} 题**\n\n"
                    f"**{md_escape(question.get('question', ''))}**"
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": get_option_lines(
                    question
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "hr",
        },
    )

    selected_text = (
        "、".join(
            key
            for key in (
                "A",
                "B",
                "C",
                "D",
            )
            if key in selected
        )
        or "未选择"
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**当前选择：{selected_text}**"
                ),
            },
        }
    )

    actions = []

    for key in (
        "A",
        "B",
        "C",
        "D",
    ):

        if key not in question.get(
            "options",
            {},
        ):

            continue

        label = (
            f"✓ {key}"
            if key in selected
            else key
        )

        button_type = (
            "primary"
            if key in selected
            else "default"
        )

        actions.append(
            {
                "tag": "button",
                "text": {
                    "tag": "plain_text",
                    "content": label,
                },
                "type": button_type,
                "behaviors": [
                    {
                        "type": "callback",
                        "value": {
                            "action": "toggle_multiple",
                            "question_id": qid,
                            "answer": key,
                        },
                    }
                ],
            }
        )

    if len(actions) < 4:

        return build_error_card(
            f"题目 {qid} 的选项不足 4 个"
        )

    elements.append(
        {
            "tag": "column_set",
            "flex_mode": "none",
            "columns": [
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[0]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[1]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[2]],
                },
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [actions[3]],
                },
            ],
        }
    )

    elements.append(
        {
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
                        "action": "submit_multiple",
                        "question_id": qid,
                    },
                }
            ],
        }
    )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": question_header(
                    question
                ),
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# 翻译 / 写作
# ============================================================

def build_text_card(
    question: dict[str, Any],
) -> dict[str, Any]:

    qid = question["question_id"]

    qtype = question.get(
        "type",
        "",
    )

    label = (
        "请输入你的翻译答案"
        if qtype == "translation"
        else "请输入你的作文"
    )

    max_length = (
        2000
        if qtype == "translation"
        else 5000
    )

    form_name = (
        f"form_{qid}"
    )

    submit_name = (
        f"submit_{qid}"
    )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": question_header(
                    question
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
                            f"**第 {question.get('number', '')} 题**\n\n"
                            f"**{md_escape(question.get('question', ''))}**"
                        ),
                    },
                },
                {
                    "tag": "hr",
                },
                {
                    "tag": "form",
                    "name": form_name,
                    "elements": [
                        {
                            "tag": "input",
                            "name": "answer",
                            "input_type": "multiline_text",
                            "placeholder": {
                                "tag": "plain_text",
                                "content": label,
                            },
                            "max_length": max_length,
                            "required": True,
                        },
                        {
                            "tag": "button",
                            "name": submit_name,
                            "form_action_type": "submit",
                            "text": {
                                "tag": "plain_text",
                                "content": "提交答案",
                            },
                            "type": "primary",
                        },
                    ],
                },
            ],
        },
    }


# ============================================================
# 答题结果卡
# ============================================================

def build_answered_card(
    question: dict[str, Any],
    user_answer: Any,
) -> dict[str, Any]:

    correct_answer = str(
        question.get(
            "correct_answer",
            "",
        )
    ).strip()

    user_answer_text = str(
        user_answer
        if user_answer is not None
        else ""
    ).strip()

    is_correct = (
        normalize_answer(
            user_answer_text
        )
        == normalize_answer(
            correct_answer
        )
    )

    if is_correct:

        result_text = "✅ **回答正确**"

        template = "green"

        title = "正确"

    else:

        result_text = "❌ **回答错误**"

        template = "red"

        title = "错误"

    elements: list[dict[str, Any]] = []

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**第 {question['number']} 题**\n\n"
                    f"**{md_escape(question['question'])}**"
                ),
            },
        }
    )

    options = question.get(
        "options",
        {},
    )

    option_lines = []

    for key in (
        "A",
        "B",
        "C",
        "D",
    ):

        if key in options:

            option_lines.append(
                f"**{key}.** "
                f"{md_escape(options[key])}"
            )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": "\n".join(
                    option_lines
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "hr",
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**你的答案："
                    f"{md_escape(user_answer_text)}**"
                ),
            },
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": result_text,
            },
        }
    )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**正确答案："
                    f"{md_escape(correct_answer)}**"
                ),
            },
        }
    )

    explanation = question.get(
        "explanation",
        "",
    )

    if explanation:

        elements.append(
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        f"**解析：**\n"
                        f"{md_escape(explanation)}"
                    ),
                },
            }
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
                    f"第 {question['number']} 题 · "
                    f"{title}"
                ),
            },
            "template": template,
        },
        "body": {
            "elements": elements,
        },
    }


def build_manual_submitted_card(
    question: dict[str, Any],
    user_answer: str,
) -> dict[str, Any]:

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    f"**第 {question['number']} 题**\n\n"
                    f"**{md_escape(question['question'])}**"
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
                    f"**你的答案：**\n"
                    f"{md_escape(user_answer)}"
                ),
            },
        },
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "🟠 **已提交，待人工批改**"
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
                "content": (
                    f"第 {question['number']} 题 · 已提交"
                ),
            },
            "template": "orange",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# normalize
# ============================================================

def normalize_answer(
    value: Any,
) -> str:

    if value is None:

        return ""

    if isinstance(
        value,
        list,
    ):

        value = ",".join(
            str(x)
            for x in value
        )

    value = (
        str(value)
        .strip()
        .upper()
    )

    value = value.replace(
        "，",
        ",",
    )

    value = value.replace(
        "、",
        ",",
    )

    value = value.replace(
        ";",
        ",",
    )

    value = value.replace(
        "；",
        ",",
    )

    value = value.replace(
        " ",
        "",
    )

    if "," in value:

        parts = [
            x
            for x in value.split(",")
            if x
        ]

        parts = sorted(
            set(parts)
        )

        return ",".join(parts)

    if (
        len(value) > 1
        and value.isalpha()
    ):

        return ",".join(
            sorted(
                set(value)
            )
        )

    return value


# ============================================================
# 卡片发送
# ============================================================

def send_card(
    token: str,
    chat_id: str,
    card_data: dict[str, Any],
) -> str:

    headers = {
        "Authorization":
            f"Bearer {token}",
        "Content-Type":
            "application/json; charset=utf-8",
    }

    payload = {
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(
            card_data,
            ensure_ascii=False,
        ),
    }

    response = requests.post(
        "https://open.feishu.cn/open-apis/im/v1/messages",
        headers=headers,
        params={
            "receive_id_type": "chat_id",
        },
        json=payload,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    if result.get("code") != 0:

        fail(
            "发送飞书卡片失败: "
            + json.dumps(
                result,
                ensure_ascii=False,
            )
        )

    return (
        result.get(
            "data",
            {},
        )
        .get(
            "message_id",
            "",
        )
    )


def send_all_questions(
    token: str,
    chat_id: str,
) -> None:

    log("")

    log(
        "开始发送 61 道题..."
    )

    for index, question in enumerate(
        SAFE_QUESTIONS,
        start=1,
    ):

        qtype = question.get(
            "type",
            "",
        )

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

        send_card(
            token,
            chat_id,
            card,
        )

        if (
            index == 1
            or index % 10 == 0
        ):

            log(
                f"  已发送 {index}/61"
            )

        time.sleep(
            0.15
        )

    log(
        "✅ 61 道题全部发送完成"
    )


# ============================================================
# 状态持久化
# ============================================================

def state_payload() -> dict[str, Any]:

    with STATE_LOCK:

        return {
            "version": "8.1",
            "exam_date": EXAM_DATE,
            "total_questions": EXPECTED_TOTAL,
            "answers": ANSWER_STATE,
            "updated_at": int(
                time.time()
            ),
        }


def persist_state() -> None:

    payload = state_payload()

    atomic_write_json(
        STATE_FILE,
        payload,
    )

    if not PERSIST_GITHUB:

        return

    repo_root = BASE_DIR.parent

    target_dir = (
        repo_root
        / PERSIST_GITHUB_PATH
    )

    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    target_file = (
        target_dir
        / f"{EXAM_DATE or 'unknown'}_answers.json"
    )

    atomic_write_json(
        target_file,
        payload,
    )

    try:

        subprocess.run(
            [
                "git",
                "add",
                str(target_file),
            ],
            cwd=repo_root,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                (
                    "chore(feishu): save exam "
                    "answer state"
                ),
            ],
            cwd=repo_root,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.run(
            [
                "git",
                "push",
            ],
            cwd=repo_root,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    except Exception as exc:

        log(
            "⚠️ GitHub 状态持久化失败，"
            f"本地状态仍已保存: {exc}"
        )


def save_answers() -> None:

    with STATE_LOCK:

        answers = {
            qid: state.get(
                "user_answer",
                "",
            )
            for qid, state
            in ANSWER_STATE.items()
        }

    atomic_write_json(
        ANSWERS_JSON,
        answers,
    )

    persist_state()


# ============================================================
# Grader
# ============================================================

def run_grader() -> dict[str, Any]:

    save_answers()

    log(
        "开始调用 Grader V1.0..."
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

    result = subprocess.run(
        command,
        cwd=BASE_DIR,
        text=True,
        capture_output=True,
    )

    if result.returncode != 0:

        log(
            result.stdout
        )

        log(
            result.stderr
        )

        fail(
            "Grader V1.0 执行失败"
        )

    grading = load_json(
        GRADER_OUTPUT
    )

    return grading


# ============================================================
# 最终成绩卡
# ============================================================

def build_final_summary_card(
    grading: dict[str, Any],
) -> dict[str, Any]:

    total = grading.get(
        "total_questions",
        0,
    )

    auto_total = grading.get(
        "auto_graded_questions",
        0,
    )

    correct = grading.get(
        "auto_correct",
        0,
    )

    wrong = grading.get(
        "auto_wrong",
        0,
    )

    accuracy = grading.get(
        "accuracy",
        0,
    )

    manual = grading.get(
        "manual_review_questions",
        0,
    )

    elements = [
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "🎉 **本次英语测试已完成**"
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
                    f"**总题数：{total}**\n\n"
                    f"**自动评分：{auto_total} 题**\n\n"
                    f"**答对：{correct} 题**\n\n"
                    f"**答错：{wrong} 题**\n\n"
                    f"**自动评分正确率：{accuracy}%**\n\n"
                    f"**待人工批改：{manual} 题**"
                ),
            },
        },
        {
            "tag": "hr",
        },
    ]

    if manual:

        elements.append(
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": (
                        "🟠 翻译和写作已经提交，"
                        "等待人工批改。"
                    ),
                },
            }
        )

    elements.append(
        {
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": (
                    "所有 61 道题的提交状态已经记录。"
                ),
            },
        }
    )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📊 英语测试最终成绩",
            },
            "template": "blue",
        },
        "body": {
            "elements": elements,
        },
    }


# ============================================================
# WebSocket 回调响应
# ============================================================

def make_card_callback_response(
    card_data: dict[str, Any],
) -> P2CardActionTriggerResponse:

    response = (
        P2CardActionTriggerResponse()
    )

    card = CallBackCard()

    card.type = "raw"

    card.data = card_data

    response.card = card

    return response


# ============================================================
# 回调数据解析
# ============================================================

def event_to_dict(
    data: P2CardActionTrigger,
) -> dict[str, Any]:

    try:

        raw = lark.JSON.marshal(
            data
        )

        return json.loads(
            raw
        )

    except Exception:

        try:

            return data.to_dict()

        except Exception:

            return {}


def extract_action(
    data: P2CardActionTrigger,
) -> dict[str, Any]:

    payload = event_to_dict(
        data
    )

    event = payload.get(
        "event",
        {},
    )

    action = event.get(
        "action",
        {},
    )

    if not isinstance(
        action,
        dict,
    ):

        return {}

    value = action.get(
        "value",
        {},
    )

    if isinstance(
        value,
        str,
    ):

        try:

            value = json.loads(
                value
            )

        except Exception:

            value = {}

    if not isinstance(
        value,
        dict,
    ):

        value = {}

    merged = dict(
        value
    )

    if action.get(
        "name"
    ):

        merged.setdefault(
            "name",
            action["name"],
        )

    if action.get(
        "form_value"
    ) is not None:

        merged["form_value"] = (
            action.get(
                "form_value"
            )
        )

    return merged


def extract_form_answer(
    action: dict[str, Any],
) -> str:

    form_value = action.get(
        "form_value",
        {},
    )

    if not isinstance(
        form_value,
        dict,
    ):

        return ""

    value = form_value.get(
        "answer",
        "",
    )

    if isinstance(
        value,
        dict,
    ):

        if "value" in value:

            value = value["value"]

    return str(
        value or ""
    ).strip()


# ============================================================
# 单选处理
# ============================================================

def handle_single_answer(
    question_id: str,
    answer: str,
) -> dict[str, Any]:

    question = QUESTION_MAP.get(
        question_id
    )

    safe_question = SAFE_QUESTION_MAP.get(
        question_id
    )

    if (
        not question
        or not safe_question
    ):

        return build_error_card(
            "题目不存在"
        )

    with STATE_LOCK:

        existing = ANSWER_STATE.get(
            question_id
        )

        if existing:

            return build_answered_card(
                question,
                existing.get(
                    "user_answer",
                    "",
                ),
            )

        ANSWER_STATE[
            question_id
        ] = {
            "user_answer": answer,
            "submitted_at": int(
                time.time()
            ),
            "graded": True,
        }

    persist_state()

    return build_answered_card(
        question,
        answer,
    )


# ============================================================
# 多选处理
# ============================================================

def handle_multiple_toggle(
    question_id: str,
    answer: str,
) -> dict[str, Any]:

    question = SAFE_QUESTION_MAP.get(
        question_id
    )

    if not question:

        return build_error_card(
            "题目不存在"
        )

    with STATE_LOCK:

        if question_id in ANSWER_STATE:

            return build_error_card(
                "本题已经提交，不能重复修改"
            )

        selected = MULTIPLE_SELECTION.setdefault(
            question_id,
            set(),
        )

        if answer in selected:

            selected.remove(
                answer
            )

        else:

            selected.add(
                answer
            )

        current = set(
            selected
        )

    return build_multiple_card(
        question,
        current,
    )


def handle_multiple_submit(
    question_id: str,
) -> dict[str, Any]:

    question = QUESTION_MAP.get(
        question_id
    )

    if not question:

        return build_error_card(
            "题目不存在"
        )

    with STATE_LOCK:

        if question_id in ANSWER_STATE:

            existing = ANSWER_STATE[
                question_id
            ]

            return build_answered_card(
                question,
                existing.get(
                    "user_answer",
                    "",
                ),
            )

        selected = set(
            MULTIPLE_SELECTION.get(
                question_id,
                set(),
            )
        )

        answer = ",".join(
            sorted(
                selected
            )
        )

        ANSWER_STATE[
            question_id
        ] = {
            "user_answer": answer,
            "submitted_at": int(
                time.time()
            ),
            "graded": True,
        }

    persist_state()

    return build_answered_card(
        question,
        answer,
    )


# ============================================================
# 文本题处理
# ============================================================

def handle_manual_submit(
    question_id: str,
    answer: str,
) -> dict[str, Any]:

    question = QUESTION_MAP.get(
        question_id
    )

    if not question:

        return build_error_card(
            "题目不存在"
        )

    with STATE_LOCK:

        if question_id in ANSWER_STATE:

            existing = ANSWER_STATE[
                question_id
            ]

            return build_manual_submitted_card(
                question,
                existing.get(
                    "user_answer",
                    "",
                ),
            )

        ANSWER_STATE[
            question_id
        ] = {
            "user_answer": answer,
            "submitted_at": int(
                time.time()
            ),
            "graded": False,
            "review_required": True,
        }

    persist_state()

    return build_manual_submitted_card(
        question,
        answer,
    )


# ============================================================
# 错误卡
# ============================================================

def build_error_card(
    message: str,
) -> dict[str, Any]:

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "操作提示",
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
                            f"⚠️ **{message}**"
                        ),
                    },
                }
            ],
        },
    }


# ============================================================
# 最终提交检测
# ============================================================

def all_questions_answered() -> bool:

    with STATE_LOCK:

        return (
            len(ANSWER_STATE)
            >= EXPECTED_TOTAL
        )


def send_final_summary_once(
    token: str,
    chat_id: str,
) -> None:

    global SUMMARY_SENT

    with STATE_LOCK:

        if SUMMARY_SENT:

            return

        if not all_questions_answered():

            return

        SUMMARY_SENT = True

    grading = run_grader()

    card = build_final_summary_card(
        grading
    )

    send_card(
        token,
        chat_id,
        card,
    )

    log(
        "🎉 最终成绩卡已发送"
    )


# ============================================================
# WebSocket callback
# ============================================================

def do_card_action_trigger(
    data: P2CardActionTrigger,
) -> P2CardActionTriggerResponse:

    try:

        action = extract_action(
            data
        )

        action_type = action.get(
            "action",
            "",
        )

        question_id = action.get(
            "question_id",
            "",
        )

        answer = action.get(
            "answer",
            "",
        )

        # ----------------------------------------------------
        # Card JSON 2.0 表单提交
        #
        # 新版 form button 不再使用 value 携带 question_id。
        # 我们使用：
        #
        # submit_translation_A_1
        # submit_translation_B_1
        # submit_writing_1
        #
        # 作为按钮 name，从 name 中恢复 question_id。
        # ----------------------------------------------------

        action_name = str(
            action.get(
                "name",
                "",
            )
        )

        if (
            not question_id
            and action_name.startswith(
                "submit_"
            )
        ):

            question_id = action_name[
                len("submit_"):
            ]

            action["action"] = (
                "submit_text"
            )

            action_type = (
                "submit_text"
            )

        # ----------------------------------------------------
        # 兼容旧版已经携带 action/question_id 的事件
        # ----------------------------------------------------

        if not question_id:

            return make_card_callback_response(
                build_error_card(
                    "缺少题目 ID"
                )
            )

        question = QUESTION_MAP.get(
            question_id
        )

        if not question:

            return make_card_callback_response(
                build_error_card(
                    "题目不存在"
                )
            )

        qtype = question.get(
            "type",
            "",
        )

        # ----------------------------------------------------
        # 单选 / 完形 / 阅读 / 听力
        # ----------------------------------------------------

        if action_type == "answer":

            card = handle_single_answer(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选选择
        # ----------------------------------------------------

        elif action_type == "toggle_multiple":

            card = handle_multiple_toggle(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选提交
        # ----------------------------------------------------

        elif action_type == "submit_multiple":

            card = handle_multiple_submit(
                question_id,
            )

        # ----------------------------------------------------
        # 翻译 / 写作
        # ----------------------------------------------------

        elif action_type == "submit_text":

            text_answer = extract_form_answer(
                action
            )

            if not text_answer:

                card = build_error_card(
                    "答案不能为空"
                )

            else:

                card = handle_manual_submit(
                    question_id,
                    text_answer,
                )

        # ----------------------------------------------------
        # 兼容部分飞书表单事件
        # ----------------------------------------------------

        elif (
            action_name.startswith(
                "submit_"
            )
            and qtype in {
                "translation",
                "writing",
            }
        ):

            text_answer = extract_form_answer(
                action
            )

            if not text_answer:

                card = build_error_card(
                    "答案不能为空"
                )

            else:

                card = handle_manual_submit(
                    question_id,
                    text_answer,
                )

        else:

            card = build_error_card(
                "未知操作"
            )

        # ----------------------------------------------------
        # 61 题完成后，发送最终成绩
        # ----------------------------------------------------

        if (
            action_type
            in {
                "answer",
                "submit_multiple",
                "submit_text",
            }
            and all_questions_answered()
        ):

            threading.Thread(
                target=send_final_summary_once,
                args=(
                    RUNTIME_TOKEN,
                    RUNTIME_CHAT_ID,
                ),
                daemon=True,
            ).start()

        return make_card_callback_response(
            card
        )

    except Exception as exc:

        log(
            "❌ 卡片回调处理异常: "
            f"{type(exc).__name__}: {exc}"
        )

        return make_card_callback_response(
            build_error_card(
                "本次操作处理失败，请稍后重试"
            )
        )

        # ----------------------------------------------------
        # 单选 / 完形 / 阅读 / 听力
        # ----------------------------------------------------

        if action_type == "answer":

            card = handle_single_answer(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选选择
        # ----------------------------------------------------

        elif action_type == "toggle_multiple":

            card = handle_multiple_toggle(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选提交
        # ----------------------------------------------------

        elif action_type == "submit_multiple":

            card = handle_multiple_submit(
                question_id,
            )

        # ----------------------------------------------------
        # 翻译 / 写作
        # ----------------------------------------------------

        elif action_type == "submit_text":

            text_answer = extract_form_answer(
                action
            )

            if not text_answer:

                card = build_error_card(
                    "答案不能为空"
                )

            else:

                card = handle_manual_submit(
                    question_id,
                    text_answer,
                )

        # ----------------------------------------------------
        # 兼容部分飞书表单事件
        # ----------------------------------------------------

        elif (
            action.get(
                "name",
                "",
            ).startswith("submit_")
            and qtype in {
                "translation",
                "writing",
            }
        ):

            text_answer = extract_form_answer(
                action
            )

            if not text_answer:

                card = build_error_card(
                    "答案不能为空"
                )

            else:

                card = handle_manual_submit(
                    question_id,
                    text_answer,
                )

        else:

            card = build_error_card(
                "未知操作"
            )

        # ----------------------------------------------------
        # 61 题完成后，发送最终成绩
        # ----------------------------------------------------

        if (
            action_type
            in {
                "answer",
                "submit_multiple",
                "submit_text",
            }
            and all_questions_answered()
        ):

            threading.Thread(
                target=send_final_summary_once,
                args=(
                    RUNTIME_TOKEN,
                    RUNTIME_CHAT_ID,
                ),
                daemon=True,
            ).start()

        return make_card_callback_response(
            card
        )

    except Exception as exc:

        log(
            "❌ 卡片回调处理异常: "
            f"{type(exc).__name__}: {exc}"
        )

        return make_card_callback_response(
            build_error_card(
                "本次操作处理失败，请稍后重试"
            )
        )


def on_error(
    data: Any,
) -> None:

    log(
        f"⚠️ Feishu WebSocket error: {data}"
    )


def on_reconnecting(
    data: Any,
) -> None:

    log(
        "🔄 Feishu WebSocket 正在重连..."
    )


def on_reconnected(
    data: Any,
) -> None:

    log(
        "✅ Feishu WebSocket 已重连"
    )


def start_websocket() -> None:

    global WS_CLIENT

    handler = (
        lark.EventDispatcherHandler
        .builder(
            "",
            "",
        )
        .register_p2_card_action_trigger(
            do_card_action_trigger
        )
        .build()
    )

    WS_CLIENT = lark.ws.Client(
        APP_ID,
        APP_SECRET,
        event_handler=handler,
        log_level=lark.LogLevel.INFO,
    )

    log(
        "🔌 启动 Feishu 长连接..."
    )

    WS_CLIENT.start()


# ============================================================
# 启动前状态
# ============================================================

def load_existing_state() -> None:

    if not STATE_FILE.exists():

        return

    try:

        data = load_json(
            STATE_FILE
        )

        saved_date = data.get(
            "exam_date",
            "",
        )

        if saved_date != EXAM_DATE:

            return

        answers = data.get(
            "answers",
            {},
        )

        if not isinstance(
            answers,
            dict,
        ):

            return

        for qid, value in answers.items():

            if qid not in QUESTION_MAP:

                continue

            if isinstance(
                value,
                dict,
            ):

                ANSWER_STATE[
                    qid
                ] = value

        if ANSWER_STATE:

            log(
                f"♻️ 恢复已有答题状态: "
                f"{len(ANSWER_STATE)}/{EXPECTED_TOTAL}"
            )

    except Exception as exc:

        log(
            "⚠️ 恢复状态失败，"
            f"忽略旧状态: {exc}"
        )


# ============================================================
# 主程序
# ============================================================

def main() -> None:

    global RUNTIME_TOKEN
    global RUNTIME_CHAT_ID

    load_exam()

    validate_exam()

    build_safe_exam()

    load_existing_state()

    token = get_tenant_access_token()

    RUNTIME_TOKEN = token

    chat_id = find_chat_id(
        token
    )

    RUNTIME_CHAT_ID = chat_id

    log(
        f"✅ 找到飞书群: "
        f"{FEISHU_CHAT_NAME}"
    )

    # --------------------------------------------------------
    # 准备听力
    # MP3 → OPUS → Feishu file_key
    # --------------------------------------------------------

    prepare_audio(
        token
    )

    # --------------------------------------------------------
    # 先启动 WebSocket
    # --------------------------------------------------------

    ws_thread = threading.Thread(
        target=start_websocket,
        daemon=True,
    )

    ws_thread.start()

    # 给长连接一点初始化时间

    time.sleep(
        3
    )

    log(
        "✅ WebSocket 监听线程已启动"
    )

    # --------------------------------------------------------
    # 再发送 61 题
    # --------------------------------------------------------

    send_all_questions(
        token,
        chat_id,
    )

    # --------------------------------------------------------
    # 如果状态已经完成，则直接生成最终成绩
    # --------------------------------------------------------

    if all_questions_answered():

        send_final_summary_once(
            token,
            chat_id,
        )

    log("")

    log(
        "=" * 70
    )

    log(
        "🟢 61 题英语答题系统正在运行"
    )

    log(
        "🟢 等待飞书用户提交答案"
    )

    log(
        "=" * 70
    )

    # --------------------------------------------------------
    # GitHub Actions runner 保持运行
    # --------------------------------------------------------

    while True:

        time.sleep(
            30
        )

        if all_questions_answered():

            time.sleep(
                10
            )

            break

    log(
        "✅ 本次 61 题答题流程完成"
    )


if __name__ == "__main__":

    main()
