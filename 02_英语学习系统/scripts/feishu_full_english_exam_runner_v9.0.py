#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu Full English Exam Runner V9.0

职责
----
1. 读取 Parser V1.6.2 生成的完整考试 JSON
2. 使用 Feishu Adapter 构建安全题目数据
3. 按完整考试结构向飞书群发送 61 题
4. 支持：
   - 听力 15
   - 单项选择 10
   - 多选题 10
   - 完形填空 10
   - 阅读理解 5
   - 翻译 10
   - 写作 1
5. 听力 A/B/C 独立发送音频消息
6. 用户提交后立即更新对应题卡
7. 多选支持 A/B/C/D 独立选择后提交
8. 翻译 / 写作支持文本表单
9. 61 题全部提交后：
      🎉 完成
          ↓
      Grader V1.0
          ↓
      最终成绩卡
10. 每次提交都保存答案状态
11. 不向初始题卡泄露正确答案
12. 不在生产日志打印正确答案
13. Parser / Adapter / Grader 均不修改

V9.0 核心结构
--------------
📘 试卷首页

一、听力
  Part A
    Listening_A 音频
    1–5
  Part B
    Listening_B 音频
    1–5
  Part C
    Listening_C 音频
    1–5

二、单项选择
  1–10

三、多选题
  1–10

四、完形填空
  完整文章
  1–10

五、阅读理解
  文章
  1–5

六、翻译
  Part A 汉译英
  Part B 英译汉
  10 题

七、写作
  1 题

🎉 完成
  ↓
Grader V1.0
  ↓
成绩卡
"""


from __future__ import annotations

import copy
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
# 版本
# ============================================================

RUNNER_VERSION = "9.0"


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


# ============================================================
# 试卷结构
# ============================================================

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


CHOICE_TYPES = {
    "listening",
    "single_choice",
    "multiple_choice",
    "cloze",
    "reading",
}


MANUAL_TYPES = {
    "translation",
    "writing",
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

SUMMARY_RUNNING = False

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


def safe_int(
    value: Any,
    default: int = 0,
) -> int:

    try:

        return int(value)

    except Exception:

        return default


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

    QUESTION_MAP = {}

    for q in QUESTIONS:

        qid = q.get(
            "question_id"
        )

        if qid:

            QUESTION_MAP[
                qid
            ] = q


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
    log("=" * 72)
    log(
        f"748686 FEISHU FULL ENGLISH EXAM V{RUNNER_VERSION}"
    )
    log("=" * 72)

    log(
        f"Runner 文件: {Path(__file__).name}"
    )

    log(
        f"考试日期: {EXAM_DATE or '未指定'}"
    )

    log(
        f"总题数: {len(QUESTIONS)}"
    )

    for qtype, expected in EXPECTED_COUNTS.items():

        log(
            f"  {qtype:<16} {expected}"
        )

    log("=" * 72)


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

    # --------------------------------------------------------
    # Adapter 当前可能接收：
    #   Parser JSON 路径
    # 或：
    #   {"questions": [...]}
    #
    # V1.0 Adapter 已验证采用 JSON 数据结构。
    # --------------------------------------------------------

    safe_exam = builder(
        {
            "questions": QUESTIONS,
            "total_questions": len(QUESTIONS),
        }
    )

    if not isinstance(
        safe_exam,
        dict,
    ):

        fail(
            "Feishu Adapter 返回值不是 dict"
        )

    raw_safe_questions = (
        safe_exam.get(
            "exam",
            {},
        )
        .get(
            "questions",
            [],
        )
    )

    if not isinstance(
        raw_safe_questions,
        list,
    ):

        fail(
            "Feishu Adapter exam.questions 不是列表"
        )

    if len(raw_safe_questions) != EXPECTED_TOTAL:

        fail(
            "Adapter 安全题目数量错误: "
            f"{len(raw_safe_questions)} / {EXPECTED_TOTAL}"
        )

    forbidden = {
        "correct_answer",
        "answer",
        "explanation",
        "reference_answer",
    }

    SAFE_QUESTIONS = []

    # --------------------------------------------------------
    # Adapter 安全层 + Parser 显示字段兜底
    # --------------------------------------------------------

    for safe_q in raw_safe_questions:

        if not isinstance(
            safe_q,
            dict,
        ):

            fail(
                "Adapter 返回存在非 dict 题目"
            )

        qid = safe_q.get(
            "question_id"
        )

        if not qid:

            fail(
                "Adapter 返回存在没有 question_id 的题目"
            )

        raw_q = QUESTION_MAP.get(
            qid,
            {},
        )

        merged = copy.deepcopy(
            safe_q
        )

        # ----------------------------------------------------
        # 恢复题干
        # ----------------------------------------------------

        if not merged.get("question"):

            if raw_q.get("question"):

                merged["question"] = raw_q.get(
                    "question"
                )

        # ----------------------------------------------------
        # 恢复题号
        # ----------------------------------------------------

        if merged.get("number") in {
            None,
            "",
        }:

            if raw_q.get("number") is not None:

                merged["number"] = raw_q.get(
                    "number"
                )

        # ----------------------------------------------------
        # 恢复 Part
        # ----------------------------------------------------

        if not merged.get("part"):

            if raw_q.get("part"):

                merged["part"] = raw_q.get(
                    "part"
                )

        # ----------------------------------------------------
        # 恢复 passage / article 等非秘密显示字段
        # ----------------------------------------------------

        display_fields = (
            "passage",
            "article",
            "context",
            "reading_passage",
            "cloze_passage",
            "passage_text",
            "article_text",
        )

        for field in display_fields:

            if not merged.get(field):

                if raw_q.get(field):

                    merged[field] = copy.deepcopy(
                        raw_q.get(field)
                    )

        # ----------------------------------------------------
        # options 兜底
        # ----------------------------------------------------

        current_options = normalize_options(
            merged.get("options")
        )

        raw_options = normalize_options(
            raw_q.get("options")
        )

        if len(current_options) < 4:

            if len(raw_options) >= 4:

                merged["options"] = copy.deepcopy(
                    raw_q.get("options")
                )

                log(
                    f"  🔧 {qid}: "
                    "Adapter options 不完整，"
                    "已从 Parser 恢复 A/B/C/D"
                )

        # ----------------------------------------------------
        # choices 兜底
        # ----------------------------------------------------

        if len(
            normalize_options(
                merged.get("options")
            )
        ) < 4:

            raw_choices = normalize_options(
                raw_q.get("choices")
            )

            if len(raw_choices) >= 4:

                merged["options"] = copy.deepcopy(
                    raw_q.get("choices")
                )

        # ----------------------------------------------------
        # 安全检查
        # ----------------------------------------------------

        leaked = forbidden.intersection(
            merged.keys()
        )

        if leaked:

            fail(
                f"Adapter 安全检查失败: "
                f"{qid} "
                f"存在禁止字段 {sorted(leaked)}"
            )

        SAFE_QUESTIONS.append(
            merged
        )

    SAFE_QUESTION_MAP = {
        q["question_id"]: q
        for q in SAFE_QUESTIONS
    }

    if len(SAFE_QUESTION_MAP) != EXPECTED_TOTAL:

        fail(
            "SAFE_QUESTION_MAP 数量错误"
        )

    # --------------------------------------------------------
    # 最终结构检查
    # --------------------------------------------------------

    for q in SAFE_QUESTIONS:

        qtype = q.get(
            "type",
            "",
        )

        if qtype not in CHOICE_TYPES:

            continue

        options = get_question_options(
            q
        )

        if len(options) != 4:

            qid = q.get(
                "question_id",
                "",
            )

            fail(
                f"SAFE 题目 {qid} 最终缺少 4 个选项: "
                f"{list(options.keys())}"
            )

    log(
        "✅ Feishu Adapter 安全检查通过"
    )

    log(
        "✅ SAFE_QUESTIONS 61 题结构检查通过"
    )

    log(
        "✅ 所有选择题均已确认 A/B/C/D"
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

    if not response.ok:

        fail(
            "获取 tenant_access_token HTTP 失败: "
            f"{response.status_code} "
            f"{response.text}"
        )

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

        if not response.ok:

            fail(
                "读取飞书群 HTTP 失败: "
                f"{response.status_code} "
                f"{response.text}"
            )

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
# 音频
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

    if source_path.suffix.lower() == ".opus":

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

        log(result.stdout)
        log(result.stderr)

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

    if file_path.suffix.lower() != ".opus":

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

    if not response.ok:

        print()
        print("=" * 72)
        print("❌ 飞书文件上传失败")
        print("=" * 72)
        print("HTTP:", response.status_code)
        print("URL:", response.url)
        print("File:", file_path.name)
        print("Response:", response.text)
        print("=" * 72)
        print()

        response.raise_for_status()

    result = response.json()

    if result.get("code") != 0:

        fail(
            "飞书文件上传 API 返回错误: "
            + json.dumps(
                result,
                ensure_ascii=False,
            )
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
            "飞书文件上传成功但没有 file_key: "
            f"{file_path.name}"
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

        for candidate in candidates:

            if (
                candidate.suffix
                .lower()
                .lstrip(".")
                == AUDIO_FORMAT
            ):

                audio_path = candidate
                break

        if audio_path is None:

            audio_path = candidates[0]

        log(
            f"准备听力 {part}: "
            f"{audio_path.name}"
        )

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
# Markdown
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


# ============================================================
# Options 标准化
# ============================================================

def normalize_options(
    options: Any,
) -> dict[str, str]:

    result: dict[str, str] = {}

    allowed = {
        "A",
        "B",
        "C",
        "D",
    }

    if options is None:

        return result

    if isinstance(
        options,
        dict,
    ):

        for raw_key, raw_value in options.items():

            key = str(
                raw_key
            ).strip().upper()

            if key not in allowed:

                continue

            if isinstance(
                raw_value,
                str,
            ):

                result[key] = raw_value
                continue

            if isinstance(
                raw_value,
                dict,
            ):

                text = raw_value.get(
                    "text",
                    raw_value.get(
                        "label",
                        raw_value.get(
                            "value",
                            raw_value.get(
                                "value_text",
                                "",
                            ),
                        ),
                    ),
                )

                if isinstance(
                    text,
                    dict,
                ):

                    text = text.get(
                        "text",
                        text.get(
                            "value",
                            "",
                        ),
                    )

                result[key] = str(
                    text
                    if text is not None
                    else ""
                )

                continue

            if raw_value is not None:

                result[key] = str(
                    raw_value
                )

        return result

    if isinstance(
        options,
        list,
    ):

        for item in options:

            if not isinstance(
                item,
                dict,
            ):

                continue

            key = str(
                item.get(
                    "key",
                    item.get(
                        "value",
                        "",
                    ),
                )
            ).strip().upper()

            if key not in allowed:

                continue

            text = item.get(
                "text",
                item.get(
                    "label",
                    item.get(
                        "value_text",
                        item.get(
                            "value",
                            "",
                        ),
                    ),
                ),
            )

            if isinstance(
                text,
                dict,
            ):

                text = text.get(
                    "text",
                    text.get(
                        "value",
                        "",
                    ),
                )

            result[key] = str(
                text
                if text is not None
                else ""
            )

        return result

    return {}


def get_question_options(
    question: dict[str, Any],
) -> dict[str, str]:

    options = normalize_options(
        question.get(
            "options"
        )
    )

    if len(options) >= 4:

        return options

    choices = normalize_options(
        question.get(
            "choices"
        )
    )

    if len(choices) >= 4:

        return choices

    qid = str(
        question.get(
            "question_id",
            "",
        )
    )

    original = QUESTION_MAP.get(
        qid,
        {},
    )

    original_options = normalize_options(
        original.get(
            "options"
        )
    )

    if len(original_options) >= 4:

        return original_options

    original_choices = normalize_options(
        original.get(
            "choices"
        )
    )

    if len(original_choices) >= 4:

        return original_choices

    return {}


def get_option_lines(
    question: dict[str, Any],
) -> str:

    options = get_question_options(
        question
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
# Passage
# ============================================================

def get_passage_text(
    question: dict[str, Any],
) -> str:

    keys = (
        "passage",
        "article",
        "context",
        "reading_passage",
        "cloze_passage",
        "passage_text",
        "article_text",
    )

    for key in keys:

        value = question.get(
            key
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    qid = str(
        question.get(
            "question_id",
            "",
        )
    )

    original = QUESTION_MAP.get(
        qid,
        {},
    )

    for key in keys:

        value = original.get(
            key
        )

        if isinstance(
            value,
            str,
        ) and value.strip():

            return value.strip()

    return ""


def build_passage_card(
    title: str,
    passage: str,
) -> dict[str, Any]:

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title,
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
                            f"**{md_escape(passage)}**"
                        ),
                    },
                },
            ],
        },
    }


# ============================================================
# 首页
# ============================================================

def build_home_card() -> dict[str, Any]:

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "📘 748686 英语测试",
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
                            "## 英语综合能力测试\n\n"
                            f"**共 {EXPECTED_TOTAL} 题**\n\n"
                            "请按照题目顺序完成全部测试。\n\n"
                            "提交后题目会立即记录。"
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
                            "**考试结构**\n\n"
                            "🎧 一、听力：15 题\n"
                            "📝 二、单项选择：10 题\n"
                            "☑️ 三、多选题：10 题\n"
                            "📖 四、完形填空：10 题\n"
                            "📚 五、阅读理解：5 题\n"
                            "🔤 六、翻译：10 题\n"
                            "✍️ 七、写作：1 题"
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
                            "⚠️ **注意**\n\n"
                            "选择题提交后不能修改。\n\n"
                            "多选题需要选择完成后点击“提交多选答案”。\n\n"
                            "翻译和写作提交后进入人工批改。"
                        ),
                    },
                },
            ],
        },
    }


# ============================================================
# Section / Part 卡
# ============================================================

def build_section_card(
    title: str,
    subtitle: str = "",
) -> dict[str, Any]:

    content = f"## {title}"

    if subtitle:

        content += (
            f"\n\n{subtitle}"
        )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title,
            },
            "template": "blue",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content,
                    },
                },
            ],
        },
    }


def build_part_card(
    title: str,
    subtitle: str = "",
) -> dict[str, Any]:

    content = f"### {title}"

    if subtitle:

        content += (
            f"\n\n{subtitle}"
        )

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": title,
            },
            "template": "blue",
        },
        "body": {
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": content,
                    },
                },
            ],
        },
    }


# ============================================================
# 选择题
# ============================================================

def build_choice_card(
    question: dict[str, Any],
) -> dict[str, Any]:

    qid = question["question_id"]

    qtype = question.get(
        "type",
        "",
    )

    options = get_question_options(
        question
    )

    if len(options) < 4:

        return build_error_card(
            f"题目 {qid} 的选项不足4个"
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

        part = str(
            question.get(
                "part",
                "",
            )
        ).strip().upper()

        if AUDIO_FILE_KEYS.get(part):

            elements.append(
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"🎧 **Listening {part} 音频已在本题前发送，"
                            "请先播放后答题。**"
                        ),
                    },
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

    options = get_question_options(
        question
    )

    if len(options) < 4:

        return build_error_card(
            f"题目 {qid} 的选项不足4个"
        )

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
        }
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

    # --------------------------------------------------------
    # Feishu 当前 interactive form input
    # max_length 默认最大值 1000。
    #
    # V8.3 曾使用 2000 / 5000，
    # 导致：
    # max_length exceed the default maximum 1000
    #
    # V9.0 统一使用 1000。
    # --------------------------------------------------------

    max_length = 1000

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
                            "action_type": "form_submit",
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
# Answer normalize
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
# 听力独立消息
# ============================================================

def send_audio_message(
    token: str,
    chat_id: str,
    part: str,
    file_key: str,
) -> str:

    headers = {
        "Authorization":
            f"Bearer {token}",
        "Content-Type":
            "application/json; charset=utf-8",
    }

    payload = {
        "receive_id": chat_id,
        "msg_type": "audio",
        "content": json.dumps(
            {
                "file_key": file_key,
            },
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

    if not response.ok:

        print()
        print("=" * 72)
        print("❌ 飞书听力消息发送失败")
        print("=" * 72)
        print("HTTP:", response.status_code)
        print("URL:", response.url)
        print("Part:", part)
        print("Response:", response.text)
        print("=" * 72)
        print()

        response.raise_for_status()

    result = response.json()

    if result.get("code") != 0:

        fail(
            "发送听力消息失败: "
            + json.dumps(
                result,
                ensure_ascii=False,
            )
        )

    message_id = (
        result.get(
            "data",
            {},
        )
        .get(
            "message_id",
            "",
        )
    )

    log(
        f"  🎧 听力 {part} 音频消息已发送"
    )

    return message_id


# ============================================================
# Card 发送
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

    if not response.ok:

        header = card_data.get(
            "header",
            {},
        )

        title_obj = (
            header.get(
                "title",
                {},
            )
            if isinstance(
                header,
                dict,
            )
            else {}
        )

        title = (
            title_obj.get(
                "content",
                "",
            )
            if isinstance(
                title_obj,
                dict,
            )
            else ""
        )

        print()
        print("=" * 72)
        print("❌ 飞书卡片发送失败")
        print("=" * 72)
        print("HTTP:", response.status_code)
        print("URL:", response.url)
        print("Card Header:", title)
        print("Response:", response.text)
        print("=" * 72)
        print()

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


# ============================================================
# 发送试卷首页 + 分区
# ============================================================

def send_exam_home(
    token: str,
    chat_id: str,
) -> None:

    send_card(
        token,
        chat_id,
        build_home_card(),
    )

    log(
        "  📘 已发送试卷首页"
    )

    time.sleep(
        0.3
    )


def send_section(
    token: str,
    chat_id: str,
    title: str,
    subtitle: str = "",
) -> None:

    send_card(
        token,
        chat_id,
        build_section_card(
            title,
            subtitle,
        ),
    )

    log(
        f"  📚 已发送章节: {title}"
    )

    time.sleep(
        0.2
    )


def send_part(
    token: str,
    chat_id: str,
    title: str,
    subtitle: str = "",
) -> None:

    send_card(
        token,
        chat_id,
        build_part_card(
            title,
            subtitle,
        ),
    )

    log(
        f"  ▪️ 已发送: {title}"
    )

    time.sleep(
        0.2
    )


# ============================================================
# 翻译 Part
# ============================================================

def translation_part(
    question: dict[str, Any],
    index_in_translation: int,
) -> str:

    part = str(
        question.get(
            "part",
            "",
        )
    ).strip().lower()

    if part:

        part_lower = part.replace(
            " ",
            "",
        )

        if (
            "a" in part_lower
            or "汉译英" in part
            or "中译英" in part
        ):

            return "A"

        if (
            "b" in part_lower
            or "英译汉" in part
            or "英译中" in part
        ):

            return "B"

    return (
        "A"
        if index_in_translation <= 5
        else "B"
    )


# ============================================================
# 按正式考试结构发送全部 61 题
# ============================================================

def send_all_questions(
    token: str,
    chat_id: str,
) -> None:

    log("")
    log("=" * 72)
    log("开始发送 V9.0 完整英语试卷")
    log("=" * 72)

    # --------------------------------------------------------
    # 试卷首页
    # --------------------------------------------------------

    send_exam_home(
        token,
        chat_id,
    )

    # --------------------------------------------------------
    # 建立类型列表
    # --------------------------------------------------------

    listening_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "listening"
    ]

    single_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "single_choice"
    ]

    multiple_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "multiple_choice"
    ]

    cloze_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "cloze"
    ]

    reading_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "reading"
    ]

    translation_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "translation"
    ]

    writing_questions = [
        q
        for q in SAFE_QUESTIONS
        if q.get("type") == "writing"
    ]

    sent_count = 0

    # ========================================================
    # 一、听力
    # ========================================================

    send_section(
        token,
        chat_id,
        "一、听力",
        "共 15 题，请按照 Part A / B / C 顺序完成。",
    )

    current_part = ""

    for question in listening_questions:

        part = str(
            question.get(
                "part",
                "",
            )
        ).strip().upper()

        if part != current_part:

            current_part = part

            subtitle = (
                f"Listening_{part} 音频 + "
                "5 道题"
            )

            send_part(
                token,
                chat_id,
                f"Part {part}",
                subtitle,
            )

            file_key = AUDIO_FILE_KEYS.get(
                part
            )

            if file_key:

                send_audio_message(
                    token,
                    chat_id,
                    part,
                    file_key,
                )

                time.sleep(
                    0.4
                )

            else:

                log(
                    f"  ⚠️ Listening {part} 没有可用音频"
                )

        card = build_choice_card(
            question
        )

        send_card(
            token,
            chat_id,
            card,
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 二、单项选择
    # ========================================================

    send_section(
        token,
        chat_id,
        "二、单项选择",
        "共 10 题，每题选择一个答案。",
    )

    for question in single_questions:

        send_card(
            token,
            chat_id,
            build_choice_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 三、多选题
    # ========================================================

    send_section(
        token,
        chat_id,
        "三、多选题",
        "共 10 题，可选择多个答案，完成后点击提交。",
    )

    for question in multiple_questions:

        send_card(
            token,
            chat_id,
            build_multiple_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 四、完形填空
    # ========================================================

    send_section(
        token,
        chat_id,
        "四、完形填空",
        "先阅读完整文章，再完成 10 道题。",
    )

    passage = ""

    for question in cloze_questions:

        candidate = get_passage_text(
            question
        )

        if candidate:

            passage = candidate

            break

    if passage:

        send_card(
            token,
            chat_id,
            build_passage_card(
                "📖 完形填空文章",
                passage,
            ),
        )

        log(
            "  📖 已发送完形填空完整文章"
        )

        time.sleep(
            0.3
        )

    else:

        log(
            "  ⚠️ Parser JSON 未发现独立完形文章字段"
        )

    for question in cloze_questions:

        send_card(
            token,
            chat_id,
            build_choice_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 五、阅读理解
    # ========================================================

    send_section(
        token,
        chat_id,
        "五、阅读理解",
        "阅读文章后完成 5 道题。",
    )

    reading_passages: list[str] = []

    seen_passages: set[str] = set()

    for question in reading_questions:

        candidate = get_passage_text(
            question
        )

        if (
            candidate
            and candidate not in seen_passages
        ):

            reading_passages.append(
                candidate
            )

            seen_passages.add(
                candidate
            )

    for index, passage in enumerate(
        reading_passages,
        start=1,
    ):

        send_card(
            token,
            chat_id,
            build_passage_card(
                f"📚 阅读文章 {index}",
                passage,
            ),
        )

        log(
            f"  📚 已发送阅读文章 {index}"
        )

        time.sleep(
            0.3
        )

    if not reading_passages:

        log(
            "  ⚠️ Parser JSON 未发现独立阅读文章字段"
        )

    for question in reading_questions:

        send_card(
            token,
            chat_id,
            build_choice_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 六、翻译
    # ========================================================

    send_section(
        token,
        chat_id,
        "六、翻译",
        "Part A：汉译英；Part B：英译汉。",
    )

    current_translation_part = ""

    for index, question in enumerate(
        translation_questions,
        start=1,
    ):

        part = translation_part(
            question,
            index,
        )

        if part != current_translation_part:

            current_translation_part = part

            if part == "A":

                send_part(
                    token,
                    chat_id,
                    "Part A · 汉译英",
                    "Translate the Chinese sentences into English.",
                )

            else:

                send_part(
                    token,
                    chat_id,
                    "Part B · 英译汉",
                    "Translate the English sentences into Chinese.",
                )

        send_card(
            token,
            chat_id,
            build_text_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 七、写作
    # ========================================================

    send_section(
        token,
        chat_id,
        "七、写作",
        "完成 1 道写作题。",
    )

    for question in writing_questions:

        send_card(
            token,
            chat_id,
            build_text_card(
                question
            ),
        )

        sent_count += 1

        log(
            f"  ✅ 已发送 {sent_count}/61 "
            f"{question.get('question_id')}"
        )

        time.sleep(
            0.15
        )

    # ========================================================
    # 最终检查
    # ========================================================

    if sent_count != EXPECTED_TOTAL:

        fail(
            f"发送题目数量异常: "
            f"{sent_count}/{EXPECTED_TOTAL}"
        )

    log("")
    log("=" * 72)
    log(
        "✅ V9.0 61 道题全部发送完成"
    )
    log("=" * 72)


# ============================================================
# 状态持久化
# ============================================================

def state_payload() -> dict[str, Any]:

    with STATE_LOCK:

        return {
            "version": RUNNER_VERSION,
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
                "chore(feishu): save exam answer state",
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
# Grader V1.0
# ============================================================

def run_grader() -> dict[str, Any]:

    save_answers()

    log("")
    log("=" * 72)
    log("开始调用 Grader V1.0...")
    log("=" * 72)

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

    if result.stdout:

        log(
            result.stdout
        )

    if result.stderr:

        log(
            result.stderr
        )

    if result.returncode != 0:

        fail(
            "Grader V1.0 执行失败"
        )

    grading = load_json(
        GRADER_OUTPUT
    )

    return grading


# ============================================================
# Grader 字段兼容
# ============================================================

def grading_value(
    grading: dict[str, Any],
    keys: list[str],
    default: Any = 0,
) -> Any:

    for key in keys:

        if key in grading:

            return grading[key]

    return default


# ============================================================
# 最终成绩卡
# ============================================================

def build_completion_card() -> dict[str, Any]:

    return {
        "schema": "2.0",
        "config": {
            "wide_screen_mode": True,
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "🎉 完成",
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
                            "## 🎉 英语测试已完成\n\n"
                            f"**61 / 61 道题全部提交。**"
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
                            "正在进行自动评分。\n\n"
                            "翻译和写作将进入人工批改流程。"
                        ),
                    },
                },
            ],
        },
    }


def build_final_summary_card(
    grading: dict[str, Any],
) -> dict[str, Any]:

    total = grading_value(
        grading,
        [
            "total_questions",
            "total",
        ],
        EXPECTED_TOTAL,
    )

    auto_total = grading_value(
        grading,
        [
            "auto_graded_questions",
            "auto_graded",
        ],
        50,
    )

    correct = grading_value(
        grading,
        [
            "auto_correct",
            "correct",
            "correct_answers",
        ],
        0,
    )

    wrong = grading_value(
        grading,
        [
            "auto_wrong",
            "wrong",
            "wrong_answers",
        ],
        0,
    )

    accuracy = grading_value(
        grading,
        [
            "accuracy",
            "accuracy_percent",
        ],
        0,
    )

    manual = grading_value(
        grading,
        [
            "manual_review_questions",
            "manual_review",
            "manual",
        ],
        11,
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
# 回答后的题卡
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
                    f"**{md_escape(question.get('question', ''))}**"
                ),
            },
        }
    )

    options = get_question_options(
        question
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

    if option_lines:

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
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": (
                            f"**第 {question['number']} 题**\n\n"
                            f"**{md_escape(question.get('question', ''))}**"
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
            ],
        },
    }


# ============================================================
# 回调响应
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
# 回调解析
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

        elif "text" in value:

            value = value["text"]

    return str(
        value or ""
    ).strip()


# ============================================================
# 单选 / 听力 / 阅读 / 完形
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

    answer = str(
        answer
    ).strip().upper()

    if answer not in {
        "A",
        "B",
        "C",
        "D",
    }:

        return build_error_card(
            "答案必须是 A / B / C / D"
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
# 多选
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

    answer = str(
        answer
    ).strip().upper()

    if answer not in {
        "A",
        "B",
        "C",
        "D",
    }:

        return build_error_card(
            "无效选项"
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

        if not selected:

            return build_error_card(
                "请至少选择一个答案"
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
# 翻译 / 写作
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

    answer = str(
        answer
    ).strip()

    if not answer:

        return build_error_card(
            "答案不能为空"
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

        if len(ANSWER_STATE) < EXPECTED_TOTAL:

            return False

        for q in SAFE_QUESTIONS:

            qid = q.get(
                "question_id"
            )

            if not qid:

                return False

            if qid not in ANSWER_STATE:

                return False

            answer = ANSWER_STATE[
                qid
            ].get(
                "user_answer",
                "",
            )

            if not str(
                answer
            ).strip():

                return False

        return True


# ============================================================
# 最终成绩流程
# ============================================================

def send_final_summary_once(
    token: str,
    chat_id: str,
) -> None:

    global SUMMARY_SENT
    global SUMMARY_RUNNING

    with STATE_LOCK:

        if SUMMARY_SENT:

            return

        if SUMMARY_RUNNING:

            return

        if not all_questions_answered():

            return

        SUMMARY_RUNNING = True

    try:

        # ----------------------------------------------------
        # 1. 先发送完成卡
        # ----------------------------------------------------

        send_card(
            token,
            chat_id,
            build_completion_card(),
        )

        log(
            "🎉 完成卡已发送"
        )

        time.sleep(
            0.5
        )

        # ----------------------------------------------------
        # 2. Grader V1.0
        # ----------------------------------------------------

        grading = run_grader()

        # ----------------------------------------------------
        # 3. 最终成绩
        # ----------------------------------------------------

        card = build_final_summary_card(
            grading
        )

        send_card(
            token,
            chat_id,
            card,
        )

        with STATE_LOCK:

            SUMMARY_SENT = True

        log(
            "📊 最终成绩卡已发送"
        )

    finally:

        with STATE_LOCK:

            SUMMARY_RUNNING = False


# ============================================================
# WebSocket Callback
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

        action_name = str(
            action.get(
                "name",
                "",
            )
        )

        # ----------------------------------------------------
        # Form Submit
        # ----------------------------------------------------

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
        # 单选 / 听力 / 完形 / 阅读
        # ----------------------------------------------------

        if action_type == "answer":

            card = handle_single_answer(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选 Toggle
        # ----------------------------------------------------

        elif action_type == "toggle_multiple":

            card = handle_multiple_toggle(
                question_id,
                str(answer),
            )

        # ----------------------------------------------------
        # 多选 Submit
        # ----------------------------------------------------

        elif action_type == "submit_multiple":

            card = handle_multiple_submit(
                question_id,
            )

        # ----------------------------------------------------
        # 文本题
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

        elif (
            action_name.startswith(
                "submit_"
            )
            and qtype in MANUAL_TYPES
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
        # 最后一题提交后启动最终流程
        # ----------------------------------------------------

        if action_type in {
            "answer",
            "submit_multiple",
            "submit_text",
        }:

            if all_questions_answered():

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


# ============================================================
# WebSocket 生命周期
# ============================================================

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
# 恢复状态
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

    # --------------------------------------------------------
    # 1. Parser V1.6.2
    # --------------------------------------------------------

    load_exam()

    validate_exam()

    # --------------------------------------------------------
    # 2. Adapter 安全层
    # --------------------------------------------------------

    build_safe_exam()

    # --------------------------------------------------------
    # 3. 恢复历史答题状态
    # --------------------------------------------------------

    load_existing_state()

    # --------------------------------------------------------
    # 4. Token
    # --------------------------------------------------------

    token = get_tenant_access_token()

    RUNTIME_TOKEN = token

    # --------------------------------------------------------
    # 5. 找群
    # --------------------------------------------------------

    chat_id = find_chat_id(
        token
    )

    RUNTIME_CHAT_ID = chat_id

    log(
        f"✅ 找到飞书群: "
        f"{FEISHU_CHAT_NAME}"
    )

    # --------------------------------------------------------
    # 6. 准备听力
    # --------------------------------------------------------

    prepare_audio(
        token
    )

    # --------------------------------------------------------
    # 7. WebSocket
    # --------------------------------------------------------

    ws_thread = threading.Thread(
        target=start_websocket,
        daemon=True,
    )

    ws_thread.start()

    time.sleep(
        3
    )

    log(
        "✅ WebSocket 监听线程已启动"
    )

    # --------------------------------------------------------
    # 8. 正式发送 V9.0 完整试卷
    # --------------------------------------------------------

    send_all_questions(
        token,
        chat_id,
    )

    # --------------------------------------------------------
    # 9. 如果启动时已经全部完成
    # --------------------------------------------------------

    if all_questions_answered():

        send_final_summary_once(
            token,
            chat_id,
        )

    log("")
    log("=" * 72)
    log(
        "🟢 V9.0 61 题英语答题系统正在运行"
    )
    log(
        "🟢 等待飞书用户提交答案"
    )
    log("=" * 72)

    # --------------------------------------------------------
    # 10. GitHub Actions 保持运行
    # --------------------------------------------------------

    while True:

        time.sleep(
            30
        )

        if (
            all_questions_answered()
            and SUMMARY_SENT
        ):

            time.sleep(
                10
            )

            break

    log("")
    log("=" * 72)
    log(
        "✅ V9.0 本次 61 题答题流程完成"
    )
    log("=" * 72)


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":

    main()
