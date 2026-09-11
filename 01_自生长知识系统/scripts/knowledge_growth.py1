#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Growth Engine V3.2
======================================================================

V3.2 核心目标
----------------------------------------------------------------------

解决 V3.1 出现的：

    1. AI Request Timeout
    2. AI JSON 输出过长
    3. JSON 被截断
    4. 单 Batch 失败导致整日失败
    5. Knowledge Context 过大
    6. Graph Context 过大
    7. Report Context 过大
    8. 同一 Event 的 en / zh 重复计算
    9. 单次 AI 输出包含过多 source_event_ids
   10. 一次性处理过多事件导致上下文膨胀

======================================================================
核心架构
----------------------------------------------------------------------

Task 4
   ↓
knowledge_daily.py
   ↓
05_日报
   ↓
knowledge_asset.py
   ↓
08_知识库 + 09_知识图谱
   ↓
weekly_report.py
   ↓
06_周报
   ↓
knowledge_growth.py
   ↓
知识系统成长

======================================================================
V3.2 批处理架构
----------------------------------------------------------------------

一个日期：

    Task 4 Analysis
          ↓
    Event ID 去重
          ↓
    Batch 10 events
          ↓
    AI Growth Analysis
          ↓
    JSON Normalize
          ↓
    Merge Batch Results
          ↓
    Deduplicate
          ↓
    写入知识库 / 图谱 / 缺口 / 矛盾 / 专题

======================================================================
重要原则
----------------------------------------------------------------------

❌ 不修改 Task 4
❌ 不修改 Raw News
❌ 不修改 10_用户资料
❌ 不把所有新闻复制进知识库
❌ 不因为单次新闻出现就机械 CREATE
❌ 不因为单个 Batch 失败就结束整日
❌ 不写知识成果到 00_System

00_System 只保存：

    运行状态
    Batch 状态
    错误诊断
    COMPLETE marker

======================================================================
语言契约
----------------------------------------------------------------------

语言目录只允许：

    en
    zh

禁止：

    EN
    ZH

不会进行大小写转换。

======================================================================
时间
----------------------------------------------------------------------

固定 Asia/Shanghai
"""

from __future__ import annotations

import os
import re
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from zoneinfo import ZoneInfo
from urllib import request, error


# ======================================================================
# 基础配置
# ======================================================================

TIMEZONE = ZoneInfo("UTC")

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

DAILY_DIR = ROOT / "05_日报"
WEEKLY_DIR = ROOT / "06_周报"
TOPIC_DIR = ROOT / "07_专题报告"
KNOWLEDGE_DIR = ROOT / "08_知识库"
GRAPH_DIR = ROOT / "09_知识图谱"

SYSTEM_LOG_DIR = (
    ROOT
    / "00_System"
    / "运行日志"
    / "knowledge_growth"
)


# ======================================================================
# AI 配置
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1"
).rstrip("/")

AGNES_MODEL = os.getenv(
    "AGNES_MODEL",
    "agnes-3.0-flash"
)

AGNES_API_KEY = os.getenv(
    "AGNES_API_KEY"
)

AI_TIMEOUT = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_TIMEOUT",
        "240"
    )
)

AI_RETRIES = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_RETRIES",
        "3"
    )
)

AI_THROTTLE_SECONDS = float(
    os.getenv(
        "KNOWLEDGE_GROWTH_THROTTLE",
        "1.5"
    )
)

# ----------------------------------------------------------------------
# V3.2 批次控制
# ----------------------------------------------------------------------

BATCH_EVENTS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_BATCH_EVENTS",
        "10"
    )
)

BATCH_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_BATCH_CHARS",
        "30000"
    )
)

# ----------------------------------------------------------------------
# 上下文限制
# ----------------------------------------------------------------------

KNOWLEDGE_CONTEXT_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_KNOWLEDGE_CONTEXT",
        "40000"
    )
)

GRAPH_CONTEXT_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_GRAPH_CONTEXT",
        "12000"
    )
)

REPORT_CONTEXT_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_REPORT_CONTEXT",
        "6000"
    )
)

# ----------------------------------------------------------------------
# AI 输出限制
#
# OpenAI-compatible API 通常支持 max_tokens。
# 如果 Agnes 网关拒绝该参数，可以设置：
#
# KNOWLEDGE_GROWTH_USE_MAX_TOKENS=false
#
# 默认开启。
# ----------------------------------------------------------------------

USE_MAX_TOKENS = (
    os.getenv(
        "KNOWLEDGE_GROWTH_USE_MAX_TOKENS",
        "true"
    ).strip().lower()
    in {
        "1",
        "true",
        "yes",
        "on",
    }
)

AI_MAX_TOKENS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_MAX_TOKENS",
        "5000"
    )
)


# ======================================================================
# 知识类型
# ======================================================================

KNOWLEDGE_TYPES = [
    "主题",
    "产品",
    "人物",
    "公司",
    "技术",
    "概念",
    "行业",
]

KNOWLEDGE_TYPE_DIR = {
    "主题": "主题",
    "产品": "产品",
    "人物": "人物",
    "公司": "公司",
    "技术": "技术",
    "概念": "概念",
    "行业": "行业",
}


# ======================================================================
# 工具
# ======================================================================

def now_local() -> datetime:
    return datetime.now(TIMEZONE)


def today_str() -> str:
    return now_local().strftime("%Y-%m-%d")


def log(message: str) -> None:
    print(message, flush=True)


def ensure_dir(path: Path) -> None:
    path.mkdir(
        parents=True,
        exist_ok=True
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def safe_filename(name: str) -> str:

    name = str(name).strip()

    name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    name = name.strip(" .")

    if not name:
        name = "未命名"

    return name[:180]


def read_text(path: Path) -> str:

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except Exception:
        return ""


def atomic_write(
    path: Path,
    content: str
) -> None:

    ensure_dir(
        path.parent
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    tmp.write_text(
        content,
        encoding="utf-8"
    )

    tmp.replace(path)


def nonempty_files(
    directory: Path,
    pattern: str = "*.md"
) -> List[Path]:

    if not directory.exists():
        return []

    result = []

    for path in directory.rglob(pattern):

        if not path.is_file():
            continue

        try:
            if path.stat().st_size <= 0:
                continue
        except Exception:
            continue

        result.append(path)

    return sorted(
        result,
        key=lambda p: p.as_posix()
    )


def truncate_text(
    text: str,
    max_chars: int
) -> str:

    text = str(text or "")

    if len(text) <= max_chars:
        return text

    if max_chars <= 20:
        return text[:max_chars]

    return (
        text[:max_chars - 20]
        + "\n...[TRUNCATED]..."
    )


# ======================================================================
# AI 错误分类
# ======================================================================

def classify_ai_error(
    exc: Exception
) -> str:

    text = str(exc).lower()

    if (
        "timed out" in text
        or "timeout" in text
    ):
        return "TIMEOUT"

    if (
        "http error 400" in text
        or "400 bad request" in text
    ):
        return "HTTP_400"

    if (
        "http error 401" in text
        or "401" in text
    ):
        return "HTTP_401"

    if (
        "http error 429" in text
        or "429" in text
        or "rate limit" in text
    ):
        return "HTTP_429"

    if (
        "http error 500" in text
        or "http error 502" in text
        or "http error 503" in text
        or "server error" in text
    ):
        return "SERVER_ERROR"

    return "OTHER"


# ======================================================================
# AI 调用
# ======================================================================

def build_ai_payload(
    system_prompt: str,
    user_prompt: str,
    compact: bool = False,
) -> Dict[str, Any]:

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    payload: Dict[str, Any] = {
        "model": AGNES_MODEL,
        "temperature": 0.0,
        "messages": messages,
    }

    if USE_MAX_TOKENS:

        payload["max_tokens"] = (
            2800
            if compact
            else AI_MAX_TOKENS
        )

    return payload


def call_ai(
    system_prompt: str,
    user_prompt: str,
    compact: bool = False,
) -> str:

    if not AGNES_API_KEY:
        raise RuntimeError(
            "缺少 AGNES_API_KEY"
        )

    url = (
        AGNES_BASE_URL
        + "/chat/completions"
    )

    payload = build_ai_payload(
        system_prompt,
        user_prompt,
        compact=compact,
    )

    body = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")

    headers = {
        "Authorization":
            f"Bearer {AGNES_API_KEY}",
        "Content-Type":
            "application/json",
        "Accept":
            "application/json",
    }

    log(
        f"   AI REQUEST SIZE : "
        f"{len(body):,} bytes"
    )

    last_error: Exception | None = None

    for attempt in range(
        1,
        AI_RETRIES + 1
    ):

        try:

            if attempt > 1:

                sleep_seconds = (
                    AI_THROTTLE_SECONDS
                    * attempt
                )

                time.sleep(
                    sleep_seconds
                )

            req = request.Request(
                url,
                data=body,
                headers=headers,
                method="POST",
            )

            with request.urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as response:

                raw = response.read().decode(
                    "utf-8",
                    errors="replace"
                )

            if not raw.strip():
                raise RuntimeError(
                    "AI HTTP 200 但返回为空"
                )

            try:

                data = json.loads(
                    raw
                )

            except Exception as exc:

                raise RuntimeError(
                    "AI 返回不是合法 HTTP JSON: "
                    + str(exc)
                )

            if not isinstance(
                data,
                dict
            ):
                raise RuntimeError(
                    "AI 返回 JSON 不是对象"
                )

            if data.get("error"):

                raise RuntimeError(
                    "AI API error: "
                    + json.dumps(
                        data.get("error"),
                        ensure_ascii=False
                    )
                )

            choices = data.get(
                "choices"
            )

            if not isinstance(
                choices,
                list
            ) or not choices:

                raise RuntimeError(
                    "AI 返回缺少 choices"
                )

            first = choices[0]

            if not isinstance(
                first,
                dict
            ):
                raise RuntimeError(
                    "AI choices[0] 格式错误"
                )

            message = first.get(
                "message",
                {}
            )

            if not isinstance(
                message,
                dict
            ):
                raise RuntimeError(
                    "AI message 格式错误"
                )

            content = message.get(
                "content",
                ""
            )

            if not isinstance(
                content,
                str
            ):
                content = str(
                    content
                )

            if not content.strip():
                raise RuntimeError(
                    "AI 返回内容为空"
                )

            return content.strip()

        except error.HTTPError as exc:

            try:
                error_body = (
                    exc.read()
                    .decode(
                        "utf-8",
                        errors="replace"
                    )
                )
            except Exception:
                error_body = ""

            detail = (
                f"HTTP Error "
                f"{exc.code}: "
                f"{exc.reason}"
            )

            if error_body:

                detail += (
                    " | "
                    + truncate_text(
                        error_body,
                        1500
                    )
                )

            last_error = RuntimeError(
                detail
            )

            log(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{classify_ai_error(last_error)} | "
                f"{detail}"
            )

        except Exception as exc:

            last_error = exc

            log(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{classify_ai_error(exc)} | "
                f"{exc}"
            )

    raise RuntimeError(
        f"AI 请求失败: {last_error}"
    )


# ======================================================================
# JSON 提取
# ======================================================================

def strip_code_fence(
    text: str
) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    return text.strip()


def extract_balanced_json(
    text: str
) -> str | None:

    """
    从 AI 输出中寻找完整 JSON 对象。

    不使用简单 rfind("{}")，
    因为字符串内部可能包含大括号。

    同时处理：

        {}
        ""
        \\

    """

    start = -1
    depth = 0

    in_string = False
    escape = False

    for index, char in enumerate(text):

        if start < 0:

            if char == "{":

                start = index
                depth = 1
                in_string = False
                escape = False

            continue

        if in_string:

            if escape:

                escape = False

            elif char == "\\":

                escape = True

            elif char == '"':

                in_string = False

            continue

        if char == '"':

            in_string = True
            continue

        if char == "{":

            depth += 1

        elif char == "}":

            depth -= 1

            if depth == 0:

                return text[
                    start:index + 1
                ]

    return None


def extract_json(
    text: str
) -> Dict[str, Any]:

    text = strip_code_fence(
        text
    )

    if not text:
        raise ValueError(
            "AI 输出为空"
        )

    try:

        value = json.loads(
            text
        )

        if isinstance(
            value,
            dict
        ):
            return value

    except Exception:
        pass

    candidate = extract_balanced_json(
        text
    )

    if candidate:

        try:

            value = json.loads(
                candidate
            )

            if isinstance(
                value,
                dict
            ):
                return value

        except Exception:
            pass

    raise ValueError(
        "无法解析 AI JSON 输出"
    )


# ======================================================================
# 日期
# ======================================================================

def target_dates() -> List[str]:

    today = now_local().date()

    return [
        (
            today
            - timedelta(days=2)
        ).strftime("%Y-%m-%d"),

        (
            today
            - timedelta(days=1)
        ).strftime("%Y-%m-%d"),

        today.strftime("%Y-%m-%d"),
    ]


# ======================================================================
# Task 4 Analysis
# ======================================================================

def find_analysis_files(
    date_str: str
) -> List[Path]:

    base = (
        RAW_NEWS
        / f"{date_str}-EventUnit"
    )

    result = []

    # ==============================================================
    # 严格遵守语言目录契约：
    #
    #     en
    #     zh
    #
    # 不允许 EN / ZH
    # 不做大小写转换
    # ==============================================================

    for language in (
        "en",
        "zh",
    ):

        directory = (
            base
            / language
            / "event_units"
        )

        if not directory.exists():
            continue

        for path in sorted(
            directory.glob(
                "*_analysis.md"
            )
        ):

            if not path.is_file():
                continue

            try:

                if (
                    path.stat().st_size
                    <= 0
                ):
                    continue

            except Exception:

                continue

            result.append(
                path
            )

    return result


def extract_event_id(
    path: Path
) -> str:

    match = re.search(
        r"(EVT-\d{8}-\d+)",
        path.name
    )

    if match:
        return match.group(1)

    return path.stem.replace(
        "_analysis",
        ""
    )


def load_analysis_records(
    paths: List[Path]
) -> List[Dict[str, str]]:

    records = []

    seen_ids = set()

    for path in paths:

        content = read_text(
            path
        ).strip()

        if not content:
            continue

        event_id = extract_event_id(
            path
        )

        if event_id in seen_ids:

            # 同一 EVT 的 en / zh
            # 只进入一个事件记录。
            #
            # 优先保留第一次发现的版本。
            continue

        seen_ids.add(
            event_id
        )

        language = (
            "en"
            if path.parent.parent.name
            == "en"
            else "zh"
        )

        records.append(
            {
                "event_id": event_id,
                "language": language,
                "file": str(
                    path.relative_to(ROOT)
                ),
                "content": content,
            }
        )

    return records


def load_analysis(
    paths: List[Path]
) -> str:

    records = load_analysis_records(
        paths
    )

    chunks = []

    for record in records:

        chunks.append(
            "\n".join([
                "==================================================",
                f"EVENT_ID: {record['event_id']}",
                f"LANGUAGE: {record['language']}",
                f"FILE: {record['file']}",
                "==================================================",
                record["content"],
            ])
        )

    return "\n\n".join(
        chunks
    )


# ======================================================================
# 批次
# ======================================================================

def split_into_batches(
    records: List[Dict[str, str]]
) -> List[List[Dict[str, str]]]:

    batches = []

    current = []
    current_chars = 0

    for record in records:

        event_block = (
            "\n".join([
                "==================================================",
                f"EVENT_ID: {record['event_id']}",
                f"LANGUAGE: {record['language']}",
                f"FILE: {record['file']}",
                "==================================================",
                record["content"],
            ])
        )

        event_chars = len(
            event_block
        )

        # ----------------------------------------------------------
        # 单事件超过 BATCH_CHARS
        # 必须独立成为一个 Batch
        # ----------------------------------------------------------

        if (
            event_chars
            > BATCH_CHARS
        ):

            if current:

                batches.append(
                    current
                )

                current = []
                current_chars = 0

            batches.append(
                [record]
            )

            continue

        # ----------------------------------------------------------
        # 数量 / 字符限制
        # ----------------------------------------------------------

        if (
            current
            and (
                len(current)
                >= BATCH_EVENTS
                or (
                    current_chars
                    + event_chars
                    > BATCH_CHARS
                )
            )
        ):

            batches.append(
                current
            )

            current = []
            current_chars = 0

        current.append(
            record
        )

        current_chars += (
            event_chars
        )

    if current:

        batches.append(
            current
        )

    return batches


def batch_text(
    batch: List[Dict[str, str]]
) -> str:

    chunks = []

    for record in batch:

        chunks.append(
            "\n".join([
                "==================================================",
                f"EVENT_ID: {record['event_id']}",
                f"LANGUAGE: {record['language']}",
                "==================================================",
                record["content"],
            ])
        )

    return "\n\n".join(
        chunks
    )


def batch_event_ids(
    batch: List[Dict[str, str]]
) -> List[str]:

    return [
        record["event_id"]
        for record in batch
    ]


# ======================================================================
# 日报 / 周报 / 专题
# ======================================================================

def find_daily_report(
    date_str: str
) -> Path | None:

    year, month, _ = (
        date_str.split("-")
    )

    path = (
        DAILY_DIR
        / year
        / month
        / f"{date_str}.md"
    )

    if (
        path.exists()
        and path.stat().st_size > 0
    ):
        return path

    return None


def find_recent_weekly_reports(
    limit: int = 2
) -> List[Path]:

    files = nonempty_files(
        WEEKLY_DIR
    )

    return files[-limit:]


def find_recent_topic_reports(
    limit: int = 4
) -> List[Path]:

    files = nonempty_files(
        TOPIC_DIR
    )

    return files[-limit:]


def build_report_context(
    date_str: str
) -> str:

    sections = []

    daily = find_daily_report(
        date_str
    )

    if daily:

        text = truncate_text(
            read_text(daily),
            REPORT_CONTEXT_CHARS // 2
        )

        sections.append(
            "================ 日报 ================\n"
            + text
        )

    weekly_files = (
        find_recent_weekly_reports()
    )

    if weekly_files:

        weekly_chunks = []

        for path in weekly_files:

            text = truncate_text(
                read_text(path),
                REPORT_CONTEXT_CHARS // 4
            )

            weekly_chunks.append(
                f"\n--- "
                f"{path.relative_to(ROOT)} "
                f"---\n"
                + text
            )

        sections.append(
            "================ 最近周报 ================\n"
            + "\n".join(
                weekly_chunks
            )
        )

    topic_files = (
        find_recent_topic_reports()
    )

    if topic_files:

        topic_chunks = []

        for path in topic_files:

            text = truncate_text(
                read_text(path),
                REPORT_CONTEXT_CHARS // 8
            )

            topic_chunks.append(
                f"\n--- "
                f"{path.relative_to(ROOT)} "
                f"---\n"
                + text
            )

        sections.append(
            "================ 最近专题 ================\n"
            + "\n".join(
                topic_chunks
            )
        )

    return truncate_text(
        "\n\n".join(sections),
        REPORT_CONTEXT_CHARS
    )


# ======================================================================
# 当前知识库
# ======================================================================

def knowledge_files() -> List[Path]:

    result = []

    for knowledge_type in (
        KNOWLEDGE_TYPES
    ):

        directory = (
            KNOWLEDGE_DIR
            / KNOWLEDGE_TYPE_DIR[
                knowledge_type
            ]
        )

        result.extend(
            nonempty_files(
                directory
            )
        )

    return sorted(
        result,
        key=lambda p: p.as_posix()
    )


def compact_knowledge_inventory(
    max_chars: int = KNOWLEDGE_CONTEXT_CHARS
) -> str:

    """
    V3.2：

    不再把每个知识文件完整塞给 AI。

    只保留：

        FILE
        type
        name
        核心知识前若干字符

    """

    files = knowledge_files()

    chunks = []

    total = 0

    for path in files:

        text = read_text(
            path
        ).strip()

        if not text:
            continue

        knowledge_type = ""

        match = re.search(
            r"^type:\s*(.+)$",
            text,
            flags=re.MULTILINE
        )

        if match:
            knowledge_type = (
                match.group(1).strip()
            )

        name = path.stem

        name_match = re.search(
            r"^name:\s*(.+)$",
            text,
            flags=re.MULTILINE
        )

        if name_match:

            name = (
                name_match
                .group(1)
                .strip()
            )

        core = ""

        core_match = re.search(
            r"## 核心知识\s*\n(.*?)(?=\n## |\Z)",
            text,
            flags=re.S
        )

        if core_match:

            core = (
                core_match
                .group(1)
                .strip()
            )

        if not core:

            core = text[:500]

        core = truncate_text(
            core,
            700
        )

        block = (
            f"- FILE: "
            f"{path.relative_to(ROOT)}\n"
            f"  TYPE: {knowledge_type}\n"
            f"  NAME: {name}\n"
            f"  CORE: {core}\n"
        )

        if (
            total
            + len(block)
            > max_chars
        ):
            break

        chunks.append(
            block
        )

        total += len(
            block
        )

    return "\n".join(
        chunks
    )


def graph_inventory(
    max_chars: int = GRAPH_CONTEXT_CHARS
) -> str:

    files = nonempty_files(
        GRAPH_DIR
    )

    chunks = []

    total = 0

    for path in files:

        text = read_text(
            path
        ).strip()

        if not text:
            continue

        block = (
            f"\n--- "
            f"{path.relative_to(ROOT)} "
            f"---\n"
            + truncate_text(
                text,
                2500
            )
        )

        if (
            total
            + len(block)
            > max_chars
        ):
            break

        chunks.append(
            block
        )

        total += len(
            block
        )

    return "\n".join(
        chunks
    )


# ======================================================================
# Prompt
# ======================================================================

SYSTEM_PROMPT = """
你是 748686 自生长知识系统的长期知识成长引擎。

你的任务不是写新闻摘要。

你必须从当前 Batch 的 Task 4 Analysis 中判断：

1. 哪些信息值得进入长期知识库；
2. 哪些已有知识需要更新；
3. 哪些信息只是短期新闻，不值得进入知识库；
4. 哪些实体之间存在可靠的新关系；
5. 哪些地方存在知识缺口；
6. 哪些地方存在潜在矛盾；
7. 哪些方向值得形成专题。

严格规则：

- 不编造事实；
- 不把普通新闻机械复制进知识库；
- 已有知识优先 update；
- 只有长期价值明确时才 create；
- confidence < 0.5 的内容必须 skip；
- 关系必须有明确证据；
- knowledge_gaps 只能记录真正缺失的信息；
- contradictions 只能记录有证据支持的潜在冲突；
- topic_candidates 必须具有长期研究价值；
- 不推断用户个人信息；
- 不生成 10_用户资料；
- 不修改 Task 4；
- 不修改 Raw News；
- 同一 EVT-ID 只算一个事件；
- en 和 zh 如果是同一 EVT-ID，不得重复计算。

最重要：

这是 Batch 分析。

每个 Batch 只有少量事件。

不要为了填满 JSON 而制造大量结果。

宁可返回空数组，也不要编造。

输出必须是：

合法 JSON

不得输出：

markdown
解释
代码块
前言
后记
"""


def build_growth_prompt(
    date_str: str,
    batch: List[Dict[str, str]],
    report_context: str,
    inventory: str,
    graph: str,
    compact: bool = False,
) -> str:

    events = batch_text(
        batch
    )

    allowed_ids = ", ".join(
        batch_event_ids(batch)
    )

    if compact:

        output_instruction = """
这是 Compact Retry。

只输出最重要的结果。

最多：
- knowledge_updates：5
- relationships：5
- knowledge_gaps：3
- contradictions：3
- topic_candidates：3

每个 source_event_ids 最多保留 3 个最直接的事件来源。

summary 最多 180 字。

new_facts 最多 3 条。

不要输出任何不必要的解释。
"""

    else:

        output_instruction = """
严格控制输出规模。

最多：
- knowledge_updates：8
- relationships：8
- knowledge_gaps：4
- contradictions：4
- topic_candidates：4

每个 source_event_ids 最多 5 个。

summary 最多 250 字。

new_facts 最多 4 条。

如果没有真正有价值的结果，数组返回 []。
"""

    return f"""
当前处理日期：

{date_str}

当前 Batch 允许引用的 Event IDs：

{allowed_ids}

========================
最近报告上下文
========================

{report_context}

========================
已有知识库索引
========================

{inventory}

========================
已有知识图谱
========================

{graph}

========================
当前 Batch Task 4 Analysis
========================

{events}

========================
输出要求
========================

{output_instruction}

严格输出：

{{
  "knowledge_updates": [
    {{
      "type": "公司|产品|人物|技术|概念|行业|主题",
      "name": "实体名称",
      "action": "create|update|skip",
      "importance": 1,
      "confidence": 0.0,
      "summary": "长期知识摘要",
      "new_facts": [
        "新增事实"
      ],
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "related_entities": [
        {{
          "type": "公司|产品|人物|技术|概念|行业|主题",
          "name": "相关实体"
        }}
      ]
    }}
  ],

  "relationships": [
    {{
      "from_type": "公司|产品|人物|技术|概念|行业|主题",
      "from": "实体A",
      "relation": "关系",
      "to_type": "公司|产品|人物|技术|概念|行业|主题",
      "to": "实体B",
      "evidence": "关系依据",
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "confidence": 0.0
    }}
  ],

  "knowledge_gaps": [
    {{
      "topic": "知识缺口",
      "reason": "为什么存在缺口",
      "priority": 1,
      "suggested_research": "建议研究方向",
      "source_event_ids": []
    }}
  ],

  "contradictions": [
    {{
      "topic": "可能矛盾",
      "description": "矛盾描述",
      "evidence": "证据",
      "source_event_ids": []
    }}
  ],

  "topic_candidates": [
    {{
      "title": "专题名称",
      "reason": "为什么值得形成专题",
      "priority": 1,
      "related_entities": [
        "实体名称"
      ]
    }}
  ]
}}

重要：

只能使用当前 Batch 中实际出现的 Event ID。

不得虚构 Event ID。

source_event_ids 不是越多越好。

只保留直接支持该结论的事件。

只输出合法 JSON。
"""


# ======================================================================
# JSON Normalize
# ======================================================================

def normalize_result(
    data: Dict[str, Any]
) -> Dict[str, Any]:

    result = {
        "knowledge_updates": [],
        "relationships": [],
        "knowledge_gaps": [],
        "contradictions": [],
        "topic_candidates": [],
    }

    if not isinstance(
        data,
        dict
    ):
        return result

    for key in result:

        value = data.get(
            key
        )

        if isinstance(
            value,
            list
        ):

            result[key] = value

    return result


def valid_knowledge_type(
    value: Any
) -> bool:

    return value in KNOWLEDGE_TYPES


def clean_event_ids(
    value: Any,
    allowed_event_ids: set[str] | None = None,
) -> List[str]:

    if not isinstance(
        value,
        list
    ):
        return []

    result = []

    for item in value:

        if not isinstance(
            item,
            str
        ):
            continue

        match = re.search(
            r"EVT-\d{8}-\d+",
            item
        )

        if not match:
            continue

        event_id = (
            match.group(0)
        )

        if (
            allowed_event_ids is not None
            and event_id
            not in allowed_event_ids
        ):
            continue

        if event_id not in result:

            result.append(
                event_id
            )

    return result


# ======================================================================
# Batch Result Sanitization
# ======================================================================

def sanitize_batch_result(
    result: Dict[str, Any],
    allowed_event_ids: set[str],
) -> Dict[str, Any]:

    result = normalize_result(
        result
    )

    clean = {
        "knowledge_updates": [],
        "relationships": [],
        "knowledge_gaps": [],
        "contradictions": [],
        "topic_candidates": [],
    }

    # ------------------------------------------------------------------
    # knowledge_updates
    # ------------------------------------------------------------------

    for item in result[
        "knowledge_updates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        item = dict(
            item
        )

        item["source_event_ids"] = (
            clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                ),
                allowed_event_ids,
            )[:5]
        )

        related = item.get(
            "related_entities",
            []
        )

        if not isinstance(
            related,
            list
        ):
            related = []

        cleaned_related = []

        for entity in related[:6]:

            if not isinstance(
                entity,
                dict
            ):
                continue

            entity_type = str(
                entity.get(
                    "type",
                    ""
                )
            ).strip()

            entity_name = str(
                entity.get(
                    "name",
                    ""
                )
            ).strip()

            if (
                valid_knowledge_type(
                    entity_type
                )
                and entity_name
            ):

                cleaned_related.append({
                    "type":
                        entity_type,
                    "name":
                        entity_name,
                })

        item["related_entities"] = (
            cleaned_related
        )

        item["summary"] = (
            truncate_text(
                str(
                    item.get(
                        "summary",
                        ""
                    )
                ).strip(),
                250
            )
        )

        facts = item.get(
            "new_facts",
            []
        )

        if not isinstance(
            facts,
            list
        ):
            facts = []

        item["new_facts"] = [
            truncate_text(
                str(f).strip(),
                500
            )
            for f in facts[:4]
            if str(f).strip()
        ]

        clean[
            "knowledge_updates"
        ].append(item)

    # ------------------------------------------------------------------
    # relationships
    # ------------------------------------------------------------------

    for item in result[
        "relationships"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        item = dict(
            item
        )

        item["source_event_ids"] = (
            clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                ),
                allowed_event_ids,
            )[:5]
        )

        item["evidence"] = (
            truncate_text(
                str(
                    item.get(
                        "evidence",
                        ""
                    )
                ).strip(),
                500
            )
        )

        clean[
            "relationships"
        ].append(item)

    # ------------------------------------------------------------------
    # gaps
    # ------------------------------------------------------------------

    for item in result[
        "knowledge_gaps"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        item = dict(
            item
        )

        item["source_event_ids"] = (
            clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                ),
                allowed_event_ids,
            )[:5]
        )

        clean[
            "knowledge_gaps"
        ].append(item)

    # ------------------------------------------------------------------
    # contradictions
    # ------------------------------------------------------------------

    for item in result[
        "contradictions"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        item = dict(
            item
        )

        item["source_event_ids"] = (
            clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                ),
                allowed_event_ids,
            )[:5]
        )

        item["description"] = (
            truncate_text(
                str(
                    item.get(
                        "description",
                        ""
                    )
                ).strip(),
                600
            )
        )

        item["evidence"] = (
            truncate_text(
                str(
                    item.get(
                        "evidence",
                        ""
                    )
                ).strip(),
                600
            )
        )

        clean[
            "contradictions"
        ].append(item)

    # ------------------------------------------------------------------
    # topic candidates
    # ------------------------------------------------------------------

    for item in result[
        "topic_candidates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        item = dict(
            item
        )

        clean[
            "topic_candidates"
        ].append(item)

    return clean


# ======================================================================
# Batch JSON Retry
# ======================================================================

def run_batch_analysis(
    date_str: str,
    batch: List[Dict[str, str]],
    report_context: str,
    inventory: str,
    graph: str,
    batch_index: int,
    total_batches: int,
) -> Dict[str, Any]:

    allowed_event_ids = set(
        batch_event_ids(
            batch
        )
    )

    log("")
    log("-" * 60)
    log(
        f"🧠 BATCH "
        f"{batch_index}/{total_batches}"
    )

    log(
        f"   EVENTS : "
        f"{len(batch)}"
    )

    log(
        f"   IDS    : "
        + ", ".join(
            batch_event_ids(batch)
        )
    )

    # --------------------------------------------------------------
    # First attempt
    # --------------------------------------------------------------

    prompt = build_growth_prompt(
        date_str=date_str,
        batch=batch,
        report_context=report_context,
        inventory=inventory,
        graph=graph,
        compact=False,
    )

    try:

        raw = call_ai(
            SYSTEM_PROMPT,
            prompt,
            compact=False,
        )

        try:

            data = extract_json(
                raw
            )

            return sanitize_batch_result(
                data,
                allowed_event_ids,
            )

        except Exception as exc:

            log(
                "⚠️ BATCH JSON ERROR | "
                + str(exc)
            )

            log(
                "   First output length : "
                f"{len(raw):,} chars"
            )

            log(
                "   Entering COMPACT RETRY"
            )

    except Exception as exc:

        error_type = (
            classify_ai_error(
                exc
            )
        )

        log(
            f"⚠️ BATCH AI ERROR | "
            f"{error_type} | "
            f"{exc}"
        )

        log(
            "   Entering COMPACT RETRY"
        )

    # --------------------------------------------------------------
    # Compact retry
    # --------------------------------------------------------------

    time.sleep(
        AI_THROTTLE_SECONDS
    )

    compact_prompt = build_growth_prompt(
        date_str=date_str,
        batch=batch,
        report_context=truncate_text(
            report_context,
            2500
        ),
        inventory=truncate_text(
            inventory,
            12000
        ),
        graph=truncate_text(
            graph,
            4000
        ),
        compact=True,
    )

    try:

        raw = call_ai(
            SYSTEM_PROMPT,
            compact_prompt,
            compact=True,
        )

        try:

            data = extract_json(
                raw
            )

            return sanitize_batch_result(
                data,
                allowed_event_ids,
            )

        except Exception as exc:

            log(
                "❌ COMPACT JSON ERROR | "
                + str(exc)
            )

            log(
                "   Compact output length : "
                f"{len(raw):,} chars"
            )

            log(
                "   RAW OUTPUT:"
            )

            log(
                truncate_text(
                    raw,
                    6000
                )
            )

            raise RuntimeError(
                "Batch JSON 无法解析"
            )

    except Exception as exc:

        log(
            f"❌ BATCH FAILED | "
            f"{classify_ai_error(exc)} | "
            f"{exc}"
        )

        raise


# ======================================================================
# 知识资产路径
# ======================================================================

def knowledge_path(
    knowledge_type: str,
    name: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / KNOWLEDGE_TYPE_DIR[
            knowledge_type
        ]
        / (
            safe_filename(name)
            + ".md"
        )
    )


# ======================================================================
# 已有事件检查
# ======================================================================

def event_already_in_file(
    path: Path,
    event_ids: List[str]
) -> bool:

    if not path.exists():
        return False

    text = read_text(
        path
    )

    if not text:
        return False

    for event_id in event_ids:

        if event_id in text:
            return True

    return False


# ======================================================================
# 创建知识
# ======================================================================

def create_knowledge_file(
    path: Path,
    knowledge_type: str,
    name: str,
    date_str: str,
    item: Dict[str, Any],
) -> bool:

    summary = str(
        item.get(
            "summary",
            ""
        )
    ).strip()

    facts = item.get(
        "new_facts",
        []
    )

    if not isinstance(
        facts,
        list
    ):
        facts = []

    event_ids = clean_event_ids(
        item.get(
            "source_event_ids",
            []
        )
    )

    related = item.get(
        "related_entities",
        []
    )

    lines = [
        "---",
        f"type: {knowledge_type}",
        f"name: {name}",
        "status: active",
        f"created_at: {date_str}",
        f"last_updated: {date_str}",
        "---",
        "",
        f"# {name}",
        "",
        "## 核心知识",
        "",
        summary or "待进一步完善。",
        "",
        f"## 知识更新｜{date_str}",
        "",
    ]

    if facts:

        for fact in facts:

            fact = str(
                fact
            ).strip()

            if fact:

                lines.append(
                    f"- {fact}"
                )

        lines.append("")

    if event_ids:

        lines.extend([
            "### 来源 EventUnit",
            "",
        ])

        for event_id in event_ids:

            lines.append(
                f"- `{event_id}`"
            )

        lines.append("")

    if related:

        lines.extend([
            "### 相关实体",
            "",
        ])

        for entity in related:

            if not isinstance(
                entity,
                dict
            ):
                continue

            entity_type = str(
                entity.get(
                    "type",
                    ""
                )
            ).strip()

            entity_name = str(
                entity.get(
                    "name",
                    ""
                )
            ).strip()

            if (
                valid_knowledge_type(
                    entity_type
                )
                and entity_name
            ):

                lines.append(
                    f"- {entity_type}："
                    f"{entity_name}"
                )

        lines.append("")

    lines.extend([
        "## 知识生命周期",
        "",
        f"- 首次创建：{date_str}",
        f"- 最近更新：{date_str}",
        "",
    ])

    content = (
        "\n".join(
            lines
        ).rstrip()
        + "\n"
    )

    atomic_write(
        path,
        content
    )

    return (
        path.exists()
        and path.stat().st_size > 0
    )


# ======================================================================
# 更新知识
# ======================================================================

def update_knowledge_file(
    path: Path,
    date_str: str,
    item: Dict[str, Any],
) -> bool:

    existing = read_text(
        path
    )

    if not existing:
        return False

    event_ids = clean_event_ids(
        item.get(
            "source_event_ids",
            []
        )
    )

    # --------------------------------------------------------------
    # 防止同一个事件重复更新
    # --------------------------------------------------------------

    if event_ids:

        if event_already_in_file(
            path,
            event_ids
        ):
            return False

    facts = item.get(
        "new_facts",
        []
    )

    if not isinstance(
        facts,
        list
    ):
        facts = []

    summary = str(
        item.get(
            "summary",
            ""
        )
    ).strip()

    lines = [
        "",
        f"## 知识更新｜{date_str}",
        "",
    ]

    if summary:

        lines.extend([
            summary,
            "",
        ])

    if facts:

        lines.append(
            "### 新增事实"
        )

        lines.append("")

        for fact in facts:

            fact = str(
                fact
            ).strip()

            if fact:

                lines.append(
                    f"- {fact}"
                )

        lines.append("")

    if event_ids:

        lines.extend([
            "### 来源 EventUnit",
            "",
        ])

        for event_id in event_ids:

            lines.append(
                f"- `{event_id}`"
            )

        lines.append("")

    new_content = (
        existing.rstrip()
        + "\n"
        + "\n".join(
            lines
        )
        + "\n"
    )

    # --------------------------------------------------------------
    # 更新 frontmatter
    # --------------------------------------------------------------

    new_content = re.sub(
        r"^last_updated:\s*.*$",
        f"last_updated: {date_str}",
        new_content,
        count=1,
        flags=re.MULTILINE,
    )

    atomic_write(
        path,
        new_content
    )

    return True


# ======================================================================
# 知识图谱
# ======================================================================

def graph_path(
    date_str: str
) -> Path:

    year, month, _ = (
        date_str.split("-")
    )

    return (
        GRAPH_DIR
        / year
        / month
        / f"{date_str}.md"
    )


def append_relationships(
    date_str: str,
    relationships: List[Dict[str, Any]]
) -> int:

    if not relationships:
        return 0

    path = graph_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识图谱关系｜"
            f"{date_str}\n\n"
        )

    added = 0

    for rel in relationships:

        if not isinstance(
            rel,
            dict
        ):
            continue

        from_name = str(
            rel.get(
                "from",
                ""
            )
        ).strip()

        relation = str(
            rel.get(
                "relation",
                ""
            )
        ).strip()

        to_name = str(
            rel.get(
                "to",
                ""
            )
        ).strip()

        if not (
            from_name
            and relation
            and to_name
        ):
            continue

        from_type = str(
            rel.get(
                "from_type",
                ""
            )
        ).strip()

        to_type = str(
            rel.get(
                "to_type",
                ""
            )
        ).strip()

        if not (
            valid_knowledge_type(
                from_type
            )
            and valid_knowledge_type(
                to_type
            )
        ):
            continue

        evidence = str(
            rel.get(
                "evidence",
                ""
            )
        ).strip()

        event_ids = clean_event_ids(
            rel.get(
                "source_event_ids",
                []
            )
        )

        relation_key = (
            f"{from_type}:{from_name}"
            f"→{relation}→"
            f"{to_type}:{to_name}"
        )

        if relation_key in existing:
            continue

        lines = [
            f"- **{from_name}**"
            f"（{from_type}）"
            f" → **{relation}** → "
            f"**{to_name}**"
            f"（{to_type}）"
        ]

        if evidence:

            lines.append(
                f"  - 依据：{evidence}"
            )

        if event_ids:

            lines.append(
                "  - 来源："
                + "、".join(
                    f"`{x}`"
                    for x in event_ids
                )
            )

        lines.append("")

        existing += (
            "\n".join(
                lines
            )
            + "\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 专题候选
# ======================================================================

def topic_candidate_path(
    date_str: str
) -> Path:

    year, _, _ = (
        date_str.split("-")
    )

    return (
        TOPIC_DIR
        / year
        / "候选专题"
        / f"{date_str}.md"
    )


def append_topic_candidates(
    date_str: str,
    candidates: List[Dict[str, Any]]
) -> int:

    if not candidates:
        return 0

    path = topic_candidate_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 专题候选｜"
            f"{date_str}\n\n"
            "> 本文件记录值得进一步研究的专题方向，"
            "不等于正式专题报告。\n\n"
        )

    added = 0

    for item in candidates:

        if not isinstance(
            item,
            dict
        ):
            continue

        title = str(
            item.get(
                "title",
                ""
            )
        ).strip()

        reason = str(
            item.get(
                "reason",
                ""
            )
        ).strip()

        priority = item.get(
            "priority",
            1
        )

        entities = item.get(
            "related_entities",
            []
        )

        if not title:
            continue

        if title in existing:
            continue

        if not isinstance(
            entities,
            list
        ):
            entities = []

        entity_text = "、".join(
            str(x).strip()
            for x in entities
            if str(x).strip()
        )

        existing += (
            f"## {title}\n\n"
            f"- 优先级：{priority}\n"
            f"- 形成原因：{reason}\n"
        )

        if entity_text:

            existing += (
                f"- 相关实体："
                f"{entity_text}\n"
            )

        existing += "\n"

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 知识缺口
# ======================================================================

def gap_path(
    date_str: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / "主题"
        / "知识缺口"
        / f"{date_str}.md"
    )


def append_gaps(
    date_str: str,
    gaps: List[Dict[str, Any]]
) -> int:

    if not gaps:
        return 0

    path = gap_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识缺口｜"
            f"{date_str}\n\n"
        )

    added = 0

    for gap in gaps:

        if not isinstance(
            gap,
            dict
        ):
            continue

        topic = str(
            gap.get(
                "topic",
                ""
            )
        ).strip()

        reason = str(
            gap.get(
                "reason",
                ""
            )
        ).strip()

        priority = gap.get(
            "priority",
            1
        )

        research = str(
            gap.get(
                "suggested_research",
                ""
            )
        ).strip()

        if not topic:
            continue

        marker = (
            f"## {topic}"
        )

        if marker in existing:
            continue

        existing += (
            f"{marker}\n\n"
            f"- 优先级：{priority}\n"
            f"- 缺口原因：{reason}\n"
            f"- 建议研究：{research}\n\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 矛盾
# ======================================================================

def contradiction_path(
    date_str: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / "主题"
        / "知识矛盾"
        / f"{date_str}.md"
    )


def append_contradictions(
    date_str: str,
    contradictions: List[Dict[str, Any]]
) -> int:

    if not contradictions:
        return 0

    path = contradiction_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识矛盾待核查｜"
            f"{date_str}\n\n"
            "> 这里记录待验证的潜在矛盾，"
            "不代表系统已经判定事实冲突。\n\n"
        )

    added = 0

    for item in contradictions:

        if not isinstance(
            item,
            dict
        ):
            continue

        topic = str(
            item.get(
                "topic",
                ""
            )
        ).strip()

        description = str(
            item.get(
                "description",
                ""
            )
        ).strip()

        evidence = str(
            item.get(
                "evidence",
                ""
            )
        ).strip()

        if not topic:
            continue

        marker = (
            f"## {topic}"
        )

        if marker in existing:
            continue

        existing += (
            f"{marker}\n\n"
            f"- 矛盾描述："
            f"{description}\n"
            f"- 证据："
            f"{evidence}\n\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# Batch 日志
# ======================================================================

def batch_log_path(
    date_str: str
) -> Path:

    return (
        SYSTEM_LOG_DIR
        / f"{date_str}_batches.json"
    )


def write_batch_state(
    date_str: str,
    state: Dict[str, Any]
) -> None:

    ensure_dir(
        SYSTEM_LOG_DIR
    )

    atomic_write(
        batch_log_path(
            date_str
        ),
        json.dumps(
            state,
            ensure_ascii=False,
            indent=2
        )
    )


# ======================================================================
# COMPLETE
# ======================================================================

def complete_marker(
    date_str: str
) -> Path:

    return (
        SYSTEM_LOG_DIR
        / f"{date_str}_COMPLETE"
    )


def write_run_state(
    date_str: str,
    state: Dict[str, Any]
) -> None:

    ensure_dir(
        SYSTEM_LOG_DIR
    )

    marker = complete_marker(
        date_str
    )

    content = json.dumps(
        state,
        ensure_ascii=False,
        indent=2
    )

    atomic_write(
        marker,
        content
    )


# ======================================================================
# 合并 Batch Results
# ======================================================================

def merge_results(
    results: List[Dict[str, Any]]
) -> Dict[str, Any]:

    merged = {
        "knowledge_updates": [],
        "relationships": [],
        "knowledge_gaps": [],
        "contradictions": [],
        "topic_candidates": [],
    }

    for result in results:

        result = normalize_result(
            result
        )

        for key in merged:

            merged[key].extend(
                result.get(
                    key,
                    []
                )
            )

    return merged


def deduplicate_merged_result(
    result: Dict[str, Any]
) -> Dict[str, Any]:

    result = normalize_result(
        result
    )

    clean = {
        "knowledge_updates": [],
        "relationships": [],
        "knowledge_gaps": [],
        "contradictions": [],
        "topic_candidates": [],
    }

    # --------------------------------------------------------------
    # Knowledge
    # --------------------------------------------------------------

    seen_knowledge = set()

    for item in result[
        "knowledge_updates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        knowledge_type = str(
            item.get(
                "type",
                ""
            )
        ).strip()

        name = str(
            item.get(
                "name",
                ""
            )
        ).strip()

        if not (
            valid_knowledge_type(
                knowledge_type
            )
            and name
        ):
            continue

        key = (
            knowledge_type,
            name,
        )

        if key in seen_knowledge:
            continue

        seen_knowledge.add(
            key
        )

        clean[
            "knowledge_updates"
        ].append(
            item
        )

    # --------------------------------------------------------------
    # Relationships
    # --------------------------------------------------------------

    seen_relationships = set()

    for item in result[
        "relationships"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        key = (
            str(
                item.get(
                    "from_type",
                    ""
                )
            ).strip(),
            str(
                item.get(
                    "from",
                    ""
                )
            ).strip(),
            str(
                item.get(
                    "relation",
                    ""
                )
            ).strip(),
            str(
                item.get(
                    "to_type",
                    ""
                )
            ).strip(),
            str(
                item.get(
                    "to",
                    ""
                )
            ).strip(),
        )

        if key in seen_relationships:
            continue

        seen_relationships.add(
            key
        )

        clean[
            "relationships"
        ].append(
            item
        )

    # --------------------------------------------------------------
    # Gaps
    # --------------------------------------------------------------

    seen_gaps = set()

    for item in result[
        "knowledge_gaps"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        topic = str(
            item.get(
                "topic",
                ""
            )
        ).strip()

        if not topic:
            continue

        key = topic

        if key in seen_gaps:
            continue

        seen_gaps.add(
            key
        )

        clean[
            "knowledge_gaps"
        ].append(
            item
        )

    # --------------------------------------------------------------
    # Contradictions
    # --------------------------------------------------------------

    seen_contradictions = set()

    for item in result[
        "contradictions"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        topic = str(
            item.get(
                "topic",
                ""
            )
        ).strip()

        description = str(
            item.get(
                "description",
                ""
            )
        ).strip()

        key = (
            topic,
            description,
        )

        if key in seen_contradictions:
            continue

        seen_contradictions.add(
            key
        )

        clean[
            "contradictions"
        ].append(
            item
        )

    # --------------------------------------------------------------
    # Topics
    # --------------------------------------------------------------

    seen_topics = set()

    for item in result[
        "topic_candidates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        title = str(
            item.get(
                "title",
                ""
            )
        ).strip()

        if not title:
            continue

        if title in seen_topics:
            continue

        seen_topics.add(
            title
        )

        clean[
            "topic_candidates"
        ].append(
            item
        )

    return clean


# ======================================================================
# 单日处理
# ======================================================================

def process_date(
    date_str: str
) -> Dict[str, Any]:

    log("")
    log("=" * 72)
    log(
        f"KNOWLEDGE GROWTH | "
        f"{date_str}"
    )
    log("=" * 72)

    marker = complete_marker(
        date_str
    )

    if marker.exists():

        log(
            f"⏭️ SKIP | "
            f"{date_str} 已完成"
        )

        return {
            "date": date_str,
            "status":
                "already_complete",
        }

    # --------------------------------------------------------------
    # Analysis files
    # --------------------------------------------------------------

    analysis_files = (
        find_analysis_files(
            date_str
        )
    )

    log(
        f"Task 4 Analysis : "
        f"{len(analysis_files)}"
    )

    if not analysis_files:

        log(
            "⚠️ 没有 Task 4 Analysis，"
            "本日不标记 COMPLETE"
        )

        return {
            "date": date_str,
            "status":
                "no_input",
        }

    # --------------------------------------------------------------
    # 去重
    # --------------------------------------------------------------

    records = (
        load_analysis_records(
            analysis_files
        )
    )

    event_ids = [
        record["event_id"]
        for record in records
    ]

    log(
        f"Unique Event IDs  : "
        f"{len(event_ids)}"
    )

    if not records:

        log(
            "⚠️ 没有有效 Event Records"
        )

        return {
            "date": date_str,
            "status":
                "no_valid_events",
        }

    # --------------------------------------------------------------
    # Batch
    # --------------------------------------------------------------

    batches = split_into_batches(
        records
    )

    log(
        f"AI Batches        : "
        f"{len(batches)}"
    )

    for index, batch in enumerate(
        batches,
        start=1
    ):

        text = batch_text(
            batch
        )

        log(
            f"   Batch "
            f"{index:02d} | "
            f"events={len(batch)} | "
            f"chars={len(text):,}"
        )

    # --------------------------------------------------------------
    # Context
    # --------------------------------------------------------------

    inventory = (
        compact_knowledge_inventory()
    )

    graph = (
        graph_inventory()
    )

    report_context = (
        build_report_context(
            date_str
        )
    )

    log(
        f"Knowledge Context : "
        f"{len(inventory):,} chars"
    )

    log(
        f"Graph Context     : "
        f"{len(graph):,} chars"
    )

    log(
        f"Report Context    : "
        f"{len(report_context):,} chars"
    )

    # --------------------------------------------------------------
    # Batch processing
    # --------------------------------------------------------------

    batch_results = []

    failed_batches = []

    batch_states = []

    for index, batch in enumerate(
        batches,
        start=1
    ):

        batch_ids = (
            batch_event_ids(
                batch
            )
        )

        started_at = (
            now_local().isoformat()
        )

        try:

            result = run_batch_analysis(
                date_str=date_str,
                batch=batch,
                report_context=report_context,
                inventory=inventory,
                graph=graph,
                batch_index=index,
                total_batches=len(batches),
            )

            batch_results.append(
                result
            )

            batch_states.append({
                "batch":
                    index,
                "status":
                    "success",
                "events":
                    len(batch),
                "event_ids":
                    batch_ids,
                "finished_at":
                    now_local().isoformat(),
            })

            log(
                f"   ✅ BATCH "
                f"{index}/{len(batches)} "
                f"SUCCESS"
            )

        except Exception as exc:

            failed_batches.append(
                index
            )

            batch_states.append({
                "batch":
                    index,
                "status":
                    "failed",
                "events":
                    len(batch),
                "event_ids":
                    batch_ids,
                "error":
                    str(exc),
                "started_at":
                    started_at,
                "finished_at":
                    now_local().isoformat(),
            })

            log(
                f"   ❌ BATCH "
                f"{index}/{len(batches)} "
                f"FAILED"
            )

        write_batch_state(
            date_str,
            {
                "date":
                    date_str,
                "total_batches":
                    len(batches),
                "completed_batches":
                    len(batch_states),
                "successful_batches":
                    len(batch_results),
                "failed_batches":
                    failed_batches,
                "batches":
                    batch_states,
            }
        )

        time.sleep(
            AI_THROTTLE_SECONDS
        )

    # --------------------------------------------------------------
    # 关键安全机制
    #
    # 只要存在失败 Batch：
    #
    #     ❌ 不写知识成果
    #     ❌ 不写 COMPLETE
    #
    # 下一次运行会重新处理整个日期。
    #
    # 这样避免“半天知识”被永久写入。
    # --------------------------------------------------------------

    if failed_batches:

        log("")
        log(
            "❌ DATE INCOMPLETE"
        )

        log(
            f"   FAILED BATCHES: "
            + ", ".join(
                str(x)
                for x in failed_batches
            )
        )

        log(
            "   NO KNOWLEDGE "
            "WRITE"
        )

        log(
            "   NO COMPLETE MARKER"
        )

        return {
            "date":
                date_str,
            "status":
                "batch_failed",
            "total_batches":
                len(batches),
            "successful_batches":
                len(batch_results),
            "failed_batches":
                failed_batches,
        }

    # --------------------------------------------------------------
    # 合并
    # --------------------------------------------------------------

    merged = merge_results(
        batch_results
    )

    merged = deduplicate_merged_result(
        merged
    )

    log("")
    log(
        "MERGED AI RESULT"
    )

    log(
        f"   KNOWLEDGE : "
        f"{len(merged['knowledge_updates'])}"
    )

    log(
        f"   RELATION  : "
        f"{len(merged['relationships'])}"
    )

    log(
        f"   GAPS      : "
        f"{len(merged['knowledge_gaps'])}"
    )

    log(
        f"   CONFLICTS : "
        f"{len(merged['contradictions'])}"
    )

    log(
        f"   TOPICS    : "
        f"{len(merged['topic_candidates'])}"
    )

    # --------------------------------------------------------------
    # 知识资产
    # --------------------------------------------------------------

    created = 0
    updated = 0
    skipped = 0

    for item in merged[
        "knowledge_updates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        knowledge_type = str(
            item.get(
                "type",
                ""
            )
        ).strip()

        name = str(
            item.get(
                "name",
                ""
            )
        ).strip()

        action = str(
            item.get(
                "action",
                "skip"
            )
        ).strip().lower()

        confidence = item.get(
            "confidence",
            0
        )

        try:

            confidence = float(
                confidence
            )

        except Exception:

            confidence = 0.0

        if not valid_knowledge_type(
            knowledge_type
        ):
            skipped += 1
            continue

        if not name:
            skipped += 1
            continue

        if (
            confidence < 0.5
            and action != "skip"
        ):

            log(
                f"⏭️ LOW CONFIDENCE | "
                f"{knowledge_type} | "
                f"{name}"
            )

            skipped += 1
            continue

        path = knowledge_path(
            knowledge_type,
            name
        )

        # ----------------------------------------------------------
        # CREATE
        # ----------------------------------------------------------

        if action == "create":

            if path.exists():

                changed = (
                    update_knowledge_file(
                        path,
                        date_str,
                        item
                    )
                )

                if changed:
                    updated += 1
                else:
                    skipped += 1

            else:

                if create_knowledge_file(
                    path,
                    knowledge_type,
                    name,
                    date_str,
                    item
                ):
                    created += 1
                else:
                    skipped += 1

        # ----------------------------------------------------------
        # UPDATE
        # ----------------------------------------------------------

        elif action == "update":

            if path.exists():

                changed = (
                    update_knowledge_file(
                        path,
                        date_str,
                        item
                    )
                )

                if changed:
                    updated += 1
                else:
                    skipped += 1

            else:

                if create_knowledge_file(
                    path,
                    knowledge_type,
                    name,
                    date_str,
                    item
                ):
                    created += 1
                else:
                    skipped += 1

        else:

            skipped += 1

    # --------------------------------------------------------------
    # Graph
    # --------------------------------------------------------------

    relationships_added = (
        append_relationships(
            date_str,
            merged[
                "relationships"
            ]
        )
    )

    # --------------------------------------------------------------
    # Gaps
    # --------------------------------------------------------------

    gaps_added = append_gaps(
        date_str,
        merged[
            "knowledge_gaps"
        ]
    )

    # --------------------------------------------------------------
    # Contradictions
    # --------------------------------------------------------------

    contradictions_added = (
        append_contradictions(
            date_str,
            merged[
                "contradictions"
            ]
        )
    )

    # --------------------------------------------------------------
    # Topics
    # --------------------------------------------------------------

    topic_candidates_added = (
        append_topic_candidates(
            date_str,
            merged[
                "topic_candidates"
            ]
        )
    )

    # --------------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------------

    state = {
        "date":
            date_str,

        "status":
            "complete",

        "processed_analysis_files":
            len(analysis_files),

        "unique_event_ids":
            len(event_ids),

        "total_batches":
            len(batches),

        "successful_batches":
            len(batch_results),

        "failed_batches":
            [],

        "knowledge_created":
            created,

        "knowledge_updated":
            updated,

        "knowledge_skipped":
            skipped,

        "relationships_added":
            relationships_added,

        "knowledge_gaps_added":
            gaps_added,

        "contradictions_added":
            contradictions_added,

        "topic_candidates_added":
            topic_candidates_added,

        "finished_at":
            now_local().isoformat(),
    }

    write_run_state(
        date_str,
        state
    )

    log("")
    log(
        f"✅ KNOWLEDGE GROWTH "
        f"COMPLETE | {date_str}"
    )

    log(
        f"   CREATED       : "
        f"{created}"
    )

    log(
        f"   UPDATED       : "
        f"{updated}"
    )

    log(
        f"   SKIPPED       : "
        f"{skipped}"
    )

    log(
        f"   RELATIONSHIPS : "
        f"{relationships_added}"
    )

    log(
        f"   GAPS          : "
        f"{gaps_added}"
    )

    log(
        f"   CONTRADICTION : "
        f"{contradictions_added}"
    )

    log(
        f"   TOPIC         : "
        f"{topic_candidates_added}"
    )

    return state


# ======================================================================
# Main
# ======================================================================

def main() -> None:

    log("")
    log("#" * 72)
    log(
        "748686 自生长知识系统"
    )
    log(
        "KNOWLEDGE GROWTH ENGINE V3.2"
    )
    log("#" * 72)

    log(
        f"ROOT     : "
        f"{ROOT}"
    )

    log(
        f"TIMEZONE : "
        f"{TIMEZONE}"
    )

    log(
        f"DATE     : "
        f"{today_str()}"
    )

    log(
        f"AI MODEL : "
        f"{AGNES_MODEL}"
    )

    log(
        f"AI URL   : "
        f"{AGNES_BASE_URL}"
        f"/chat/completions"
    )

    log(
        f"BATCH EVENTS : "
        f"{BATCH_EVENTS}"
    )

    log(
        f"BATCH CHARS  : "
        f"{BATCH_CHARS:,}"
    )

    log(
        f"AI TIMEOUT   : "
        f"{AI_TIMEOUT}s"
    )

    log(
        f"MAX TOKENS   : "
        f"{AI_MAX_TOKENS}"
        if USE_MAX_TOKENS
        else
        "DISABLED"
    )

    if not AGNES_API_KEY:

        raise RuntimeError(
            "未设置 AGNES_API_KEY"
        )

    dates = target_dates()

    log(
        "TARGET DATES:"
    )

    for date_str in dates:

        log(
            f"  - {date_str}"
        )

    results = []

    # ==============================================================
    # 严格按日期顺序
    #
    # 如果某一天失败：
    #
    #     仍然尝试后续日期
    #
    # 这样不会因为 09-05 的单次 AI 故障，
    # 直接阻断 09-06 / 09-07。
    #
    # 失败日期不会产生 COMPLETE。
    # ==============================================================

    for date_str in dates:

        try:

            result = process_date(
                date_str
            )

        except Exception as exc:

            log("")
            log(
                f"❌ FATAL DATE ERROR | "
                f"{date_str}"
            )

            log(
                f"   {exc}"
            )

            result = {
                "date":
                    date_str,
                "status":
                    "fatal_error",
                "error":
                    str(exc),
            }

        results.append(
            result
        )

        time.sleep(
            AI_THROTTLE_SECONDS
        )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    log("")
    log("#" * 72)
    log(
        "KNOWLEDGE GROWTH FINISHED"
    )
    log("#" * 72)

    for result in results:

        log(
            f"{result.get('date')} "
            f"| "
            f"{result.get('status')}"
        )

    failed = [
        result
        for result in results
        if result.get(
            "status"
        ) not in {
            "complete",
            "already_complete",
        }
    ]

    if failed:

        log("")
        log(
            "⚠️ KNOWLEDGE GROWTH "
            "FINISHED WITH INCOMPLETE DATES"
        )

        for result in failed:

            log(
                f"   "
                f"{result.get('date')} "
                f"| "
                f"{result.get('status')}"
            )

        # ----------------------------------------------------------
        # 不主动 raise。
        #
        # 原因：
        #
        # 某个日期失败时，前面的成功日期已经合法完成，
        # 后面的日期也已经有机会继续。
        #
        # COMPLETE marker 是日期级别的真正完成依据。
        # ----------------------------------------------------------

    else:

        log("")
        log(
            "✅ ALL TARGET DATES COMPLETE"
        )


if __name__ == "__main__":
    main()
