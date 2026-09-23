#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Weekly Report V3.3

======================================================================
核心架构
======================================================================

Skill
  +
Task 4 Analysis
  ↓
按事件分批
  ↓
Batch Summary（单个 ≤1200 字符）
  ↓
持久化 Batch Cache
  ↓
最终 Weekly Synthesis
  ↓
Wxx.md

======================================================================
V3.3 核心规则
======================================================================

1. 周报每天滚动更新：

   周一 → 周一
   周二 → 周一 + 周二
   周三 → 周一 + 周二 + 周三
   ...
   周日 → 周一 ~ 周日

2. 已存在 Wxx.md 不再 SKIP。

3. 只处理：

       Monday → Business Date

   不读取未来日期。

4. ISO Week 自动切换。

5. 同一个 EVT-ID 的 en / zh 只计一次。

6. Batch Summary：

       单个最大 1200 字符。

   多个 Batch Summary 可以共同超过 1200 字符。

7. 最终 Weekly Report：

       不受 1200 字符限制。

8. Batch Cache 使用 SHA256 input_hash。

   Task 4 输入发生变化：
       Cache 自动失效。

9. Task 1–4 不在本脚本中修改。

10. 不写入 10_用户资料。

11. 不修改 00_System。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import requests


# ======================================================================
# 基础路径
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

DAILY_DIR = ROOT / "05_日报"
WEEKLY_DIR = ROOT / "06_周报"

KNOWLEDGE_DIR = ROOT / "08_知识库"
GRAPH_DIR = ROOT / "09_知识图谱"
TOPIC_DIR = ROOT / "07_专题报告"

WEEKLY_CACHE_DIR = WEEKLY_DIR / ".cache"


# ======================================================================
# 周报 Skill
#
# 重要：
# 仓库真实目录为：
#
# Skills/
# └── 05.汇报写作/
#     └── 周报编写助手.md
# ======================================================================

SKILL_FILE = (
    ROOT
    / "Skills"
    / "05.汇报写作"
    / "周报编写助手.md"
)


# ======================================================================
# 时间
# ======================================================================

TIMEZONE = ZoneInfo("Asia/Shanghai")


# ======================================================================
# AGNES
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1",
).rstrip("/")

AGNES_MODEL = os.getenv(
    "AGNES_MODEL",
    "agnes-2.5-flash",
)

AGNES_API_KEY = os.getenv(
    "AGNES_API_KEY"
)

AI_TIMEOUT = int(
    os.getenv(
        "WEEKLY_REPORT_TIMEOUT",
        "240",
    )
)

AI_RETRIES = int(
    os.getenv(
        "WEEKLY_REPORT_RETRIES",
        "3",
    )
)

AI_THROTTLE = float(
    os.getenv(
        "WEEKLY_REPORT_THROTTLE",
        "2.0",
    )
)


# ======================================================================
# Batch 参数
# ======================================================================

TASK4_BATCH_MAX_EVENTS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_EVENTS",
        "20",
    )
)

TASK4_BATCH_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_CHARS",
        "28000",
    )
)


# ======================================================================
# 最终 AI 输入上下文
#
# 注意：
# 这些不是最终周报输出长度限制。
# ======================================================================

KNOWLEDGE_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_KNOWLEDGE_FINAL_CHARS",
        "30000",
    )
)

GRAPH_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_GRAPH_FINAL_CHARS",
        "18000",
    )
)

TOPIC_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_TOPIC_FINAL_CHARS",
        "18000",
    )
)


# ======================================================================
# Batch Summary 硬限制
# ======================================================================

BATCH_SUMMARY_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_SUMMARY_CHARS",
        "1200",
    )
)


# ======================================================================
# 日志
# ======================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(
    "weekly_report"
)


def log(message: str) -> None:
    logger.info(message)


# ======================================================================
# Skill
# ======================================================================

def load_weekly_skill() -> str:

    if not SKILL_FILE.exists():
        raise FileNotFoundError(
            f"周报 Skill 不存在：{SKILL_FILE}"
        )

    content = SKILL_FILE.read_text(
        encoding="utf-8",
        errors="ignore",
    ).strip()

    if not content:
        raise RuntimeError(
            f"周报 Skill 为空：{SKILL_FILE}"
        )

    return content


# ======================================================================
# 日期
# ======================================================================

def parse_business_date(
    value: str,
) -> date:

    try:
        return datetime.strptime(
            value,
            "%Y-%m-%d",
        ).date()

    except ValueError as exc:
        raise ValueError(
            f"非法日期：{value}，必须使用 YYYY-MM-DD"
        ) from exc


def current_week(
    target_date: date,
) -> tuple[int, int, date, date]:

    iso = target_date.isocalendar()

    year = iso.year
    week = iso.week

    monday = (
        target_date
        - timedelta(
            days=target_date.weekday()
        )
    )

    sunday = (
        monday
        + timedelta(days=6)
    )

    return (
        year,
        week,
        monday,
        sunday,
    )


# ======================================================================
# 参数
# ======================================================================

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "748686 自生长知识系统 "
            "Weekly Report V3.3"
        )
    )

    parser.add_argument(
        "--day-before",
        required=False,
        help="前前一天 YYYY-MM-DD",
    )

    parser.add_argument(
        "--yesterday",
        required=False,
        help="前一天 YYYY-MM-DD",
    )

    parser.add_argument(
        "--today",
        required=True,
        help="当前业务日期 YYYY-MM-DD",
    )

    return parser.parse_args()


# ======================================================================
# 文件读取
# ======================================================================

def safe_read_text(
    path: Path,
) -> str:

    try:

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        ).strip()

    except Exception as exc:

        log(
            f"⚠️ 无法读取文件："
            f"{path} | {exc}"
        )

        return ""


# ======================================================================
# 日报
# ======================================================================

def load_week_daily_reports(
    monday: date,
    business_date: date,
) -> list[dict[str, Any]]:
    """
    只读取 Monday → Business Date。

    不读取未来日期。
    """

    reports: list[
        dict[str, Any]
    ] = []

    current = monday

    while current <= business_date:

        date_text = current.isoformat()

        candidates = sorted(
            DAILY_DIR.glob(
                f"{date_text}*.md"
            )
        )

        for path in candidates:

            if "_带图" in path.name:
                continue

            if not path.is_file():
                continue

            content = safe_read_text(
                path
            )

            if not content:
                continue

            reports.append(
                {
                    "date": date_text,
                    "path": str(path),
                    "content": content,
                }
            )

        current += timedelta(
            days=1
        )

    return reports


# ======================================================================
# EVT-ID
# ======================================================================

EVT_PATTERN = re.compile(
    r"EVT-\d{8}-\d+",
    re.IGNORECASE,
)


def event_id(
    path: Path,
    content: str,
) -> str:

    match = EVT_PATTERN.search(
        content
    )

    if match:
        return match.group(0).upper()

    match = EVT_PATTERN.search(
        path.name
    )

    if match:
        return match.group(0).upper()

    digest = hashlib.sha256(
        str(path).encode("utf-8")
    ).hexdigest()[:16]

    return f"NO-EVT-{digest}"


# ======================================================================
# Task 4 Analysis 文件
# ======================================================================

def analysis_files_for_date(
    target_date: date,
) -> list[tuple[str, Path]]:

    date_text = target_date.isoformat()

    result: list[
        tuple[str, Path]
    ] = []

    language_dirs = [
        (
            "en",
            RAW_NEWS
            / f"{date_text}-EventUnit"
            / "en"
            / "event_units",
        ),
        (
            "zh",
            RAW_NEWS
            / f"{date_text}-EventUnit"
            / "zh"
            / "event_units",
        ),
    ]

    for language, directory in (
        language_dirs
    ):

        if not directory.exists():
            continue

        files = sorted(
            directory.glob(
                "*_analysis.md"
            )
        )

        for path in files:

            if path.is_file():

                result.append(
                    (
                        language,
                        path,
                    )
                )

    return result


def load_week_analysis_records(
    monday: date,
    business_date: date,
) -> list[dict[str, Any]]:
    """
    读取 Monday → Business Date。

    en / zh 相同 EVT-ID：
    只保留一条。

    en 优先。
    """

    records: list[
        dict[str, Any]
    ] = []

    seen_event_ids: set[str] = set()

    current = monday

    while current <= business_date:

        files = (
            analysis_files_for_date(
                current
            )
        )

        for language, path in files:

            content = safe_read_text(
                path
            )

            if not content:
                continue

            eid = event_id(
                path,
                content,
            )

            if eid in seen_event_ids:
                continue

            seen_event_ids.add(eid)

            records.append(
                {
                    "date":
                        current.isoformat(),

                    "language":
                        language,

                    "event_id":
                        eid,

                    "path":
                        str(path),

                    "content":
                        content,
                }
            )

        current += timedelta(
            days=1
        )

    return records


# ======================================================================
# Task 4 Batch
# ======================================================================

def make_task4_block(
    record: dict[str, Any],
) -> str:

    return (
        "===== EVENT =====\n"
        f"Date: {record['date']}\n"
        f"Language: {record['language']}\n"
        f"Event ID: {record['event_id']}\n"
        f"Path: {record['path']}\n"
        "\n"
        f"{record['content']}\n"
        "\n"
    )


def split_task4_batches(
    records: list[dict[str, Any]],
) -> list[
    list[dict[str, Any]]
]:

    batches: list[
        list[dict[str, Any]]
    ] = []

    current_batch: list[
        dict[str, Any]
    ] = []

    current_chars = 0

    for record in records:

        block = make_task4_block(
            record
        )

        block_chars = len(block)

        if current_batch:

            exceeds_event_limit = (
                len(current_batch)
                >= TASK4_BATCH_MAX_EVENTS
            )

            exceeds_char_limit = (
                current_chars
                + block_chars
                > TASK4_BATCH_MAX_CHARS
            )

            if (
                exceeds_event_limit
                or exceeds_char_limit
            ):

                batches.append(
                    current_batch
                )

                current_batch = []
                current_chars = 0

        current_batch.append(
            record
        )

        current_chars += block_chars

    if current_batch:

        batches.append(
            current_batch
        )

    return batches


# ======================================================================
# Cache
# ======================================================================

def batch_cache_dir(
    year: int,
    week: int,
) -> Path:

    directory = (
        WEEKLY_CACHE_DIR
        / str(year)
        / f"W{week:02d}"
        / "task4_batches"
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


def batch_summary_path(
    year: int,
    week: int,
    batch_index: int,
) -> Path:

    return (
        batch_cache_dir(
            year,
            week,
        )
        / f"batch_{batch_index:04d}.md"
    )


def batch_metadata_path(
    year: int,
    week: int,
    batch_index: int,
) -> Path:

    return (
        batch_cache_dir(
            year,
            week,
        )
        / f"batch_{batch_index:04d}.json"
    )


def batch_input_hash(
    records: list[dict[str, Any]],
) -> str:
    """
    对 Batch 当前实际输入计算 SHA256。
    """

    hasher = hashlib.sha256()

    for record in records:

        payload = (
            f"DATE={record['date']}\n"
            f"EVENT_ID={record['event_id']}\n"
            f"LANGUAGE={record['language']}\n"
            f"PATH={record['path']}\n"
            f"CONTENT=\n"
            f"{record['content']}\n"
            "---\n"
        )

        hasher.update(
            payload.encode("utf-8")
        )

    return hasher.hexdigest()


def valid_batch_cache(
    year: int,
    week: int,
    batch_index: int,
    records: list[dict[str, Any]],
) -> bool:

    summary_path = (
        batch_summary_path(
            year,
            week,
            batch_index,
        )
    )

    metadata_path = (
        batch_metadata_path(
            year,
            week,
            batch_index,
        )
    )

    if not summary_path.exists():
        return False

    if not metadata_path.exists():
        return False

    summary = safe_read_text(
        summary_path
    )

    if not summary:
        return False

    try:

        metadata = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:

        log(
            f"⚠️ Batch metadata 损坏："
            f"{metadata_path} | {exc}"
        )

        return False

    current_event_ids = [
        record["event_id"]
        for record in records
    ]

    if (
        metadata.get(
            "event_count"
        )
        != len(records)
    ):
        return False

    if (
        metadata.get(
            "event_ids"
        )
        != current_event_ids
    ):
        return False

    current_hash = (
        batch_input_hash(records)
    )

    if (
        metadata.get(
            "input_hash"
        )
        != current_hash
    ):
        return False

    if (
        len(summary)
        > BATCH_SUMMARY_MAX_CHARS
    ):
        return False

    return True


# ======================================================================
# AI
# ======================================================================

def call_ai(
    prompt: str,
    *,
    temperature: float = 0.2,
) -> str:

    if not AGNES_API_KEY:
        raise RuntimeError(
            "缺少 AGNES_API_KEY"
        )

    url = (
        f"{AGNES_BASE_URL}"
        "/chat/completions"
    )

    headers = {
        "Authorization":
            f"Bearer {AGNES_API_KEY}",
        "Content-Type":
            "application/json",
    }

    payload = {
        "model": AGNES_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": temperature,
    }

    last_error: Exception | None = None

    for attempt in range(
        1,
        AI_RETRIES + 1,
    ):

        try:

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=AI_TIMEOUT,
            )

            status = (
                response.status_code
            )

            # ----------------------------------------------------------
            # 成功
            # ----------------------------------------------------------

            if 200 <= status < 300:

                data = response.json()

                choices = data.get(
                    "choices",
                    [],
                )

                if not choices:
                    raise RuntimeError(
                        "AGNES 返回中没有 choices"
                    )

                message = choices[0].get(
                    "message",
                    {},
                )

                content = message.get(
                    "content",
                    "",
                )

                if not isinstance(
                    content,
                    str,
                ):
                    content = str(
                        content
                    )

                content = content.strip()

                if not content:
                    raise RuntimeError(
                        "AGNES 返回空内容"
                    )

                if AI_THROTTLE > 0:
                    time.sleep(
                        AI_THROTTLE
                    )

                return content

            # ----------------------------------------------------------
            # 400
            # ----------------------------------------------------------

            if status == 400:

                raise RuntimeError(
                    "AGNES 400 Bad Request："
                    + response.text[:2000]
                )

            # ----------------------------------------------------------
            # 401 / 403
            # ----------------------------------------------------------

            if status in (
                401,
                403,
            ):

                raise RuntimeError(
                    f"AGNES {status}："
                    + response.text[:2000]
                )

            # ----------------------------------------------------------
            # 429 / 5xx
            # ----------------------------------------------------------

            if (
                status == 429
                or status >= 500
            ):

                last_error = RuntimeError(
                    f"AGNES HTTP {status}："
                    + response.text[:1000]
                )

                log(
                    f"⚠️ AI 请求失败 "
                    f"{status}，"
                    f"attempt="
                    f"{attempt}/{AI_RETRIES}"
                )

                if (
                    attempt
                    < AI_RETRIES
                ):

                    sleep_seconds = min(
                        30,
                        2 ** attempt,
                    )

                    time.sleep(
                        sleep_seconds
                    )

                    continue

                raise last_error

            raise RuntimeError(
                f"AGNES HTTP {status}："
                + response.text[:2000]
            )

        except (
            requests.RequestException,
            RuntimeError,
        ) as exc:

            last_error = exc

            if (
                attempt
                >= AI_RETRIES
            ):
                raise

            log(
                f"⚠️ AI 请求异常："
                f"{exc} | "
                f"attempt="
                f"{attempt}/{AI_RETRIES}"
            )

            sleep_seconds = min(
                30,
                2 ** attempt,
            )

            time.sleep(
                sleep_seconds
            )

    if last_error:
        raise last_error

    raise RuntimeError(
        "AI 调用失败"
    )


# ======================================================================
# Batch Summary Prompt
# ======================================================================

def build_batch_summary_prompt(
    skill: str,
    batch: list[dict[str, Any]],
    batch_index: int,
    batch_total: int,
    monday: date,
    business_date: date,
) -> str:

    blocks = "\n".join(
        make_task4_block(record)
        for record in batch
    )

    return f"""
你是 748686 自生长知识系统的
“周报 Batch Summary 编译器”。

请严格依据下面的周报 Skill 和
Task 4 Analysis，
提炼这一批事件中对本周周报真正有价值的信息。

============================================================
周报 Skill
============================================================

{skill}

============================================================
本次周报周期
============================================================

ISO 周：

{monday.isoformat()}
→
{monday + timedelta(days=6)}

本次实际数据范围：

{monday.isoformat()}
→
{business_date.isoformat()}

============================================================
当前 Batch
============================================================

Batch：
{batch_index} / {batch_total}

事件数量：
{len(batch)}

============================================================
Task 4 Analysis
============================================================

{blocks}

============================================================
输出要求
============================================================

1. 只输出 Batch Summary。
2. 不输出解释。
3. 不输出“以下是总结”等套话。
4. 保留关键事实、重要变化、趋势、
   事件关联和重要意义。
5. 删除重复信息和低价值细节。
6. 不得虚构事实。
7. 按周报 Skill 的语言要求输出。
8. 单个 Batch Summary 必须严格控制在
   {BATCH_SUMMARY_MAX_CHARS} 个字符以内。
9. 不要为了凑长度添加无意义内容。
""".strip()


def build_batch_summary_text(
    raw_summary: str,
) -> str:

    summary = (
        raw_summary
        .replace("\x00", "")
        .strip()
    )

    if (
        len(summary)
        > BATCH_SUMMARY_MAX_CHARS
    ):

        log(
            f"⚠️ Batch Summary 超过 "
            f"{BATCH_SUMMARY_MAX_CHARS} "
            f"字符，执行硬截断："
            f"{len(summary)} → "
            f"{BATCH_SUMMARY_MAX_CHARS}"
        )

        summary = (
            summary[
                :BATCH_SUMMARY_MAX_CHARS
            ]
            .rstrip()
        )

    return summary


def save_batch_cache(
    year: int,
    week: int,
    batch_index: int,
    records: list[dict[str, Any]],
    summary: str,
) -> None:

    summary_path = (
        batch_summary_path(
            year,
            week,
            batch_index,
        )
    )

    metadata_path = (
        batch_metadata_path(
            year,
            week,
            batch_index,
        )
    )

    summary = (
        build_batch_summary_text(
            summary
        )
    )

    if (
        len(summary)
        > BATCH_SUMMARY_MAX_CHARS
    ):

        raise RuntimeError(
            "内部错误："
            "Batch Summary 超过硬限制"
        )

    summary_path.write_text(
        summary + "\n",
        encoding="utf-8",
    )

    metadata = {
        "version": "3.3",
        "year": year,
        "week": week,
        "batch_index":
            batch_index,
        "event_count":
            len(records),
        "event_ids": [
            record["event_id"]
            for record in records
        ],
        "dates": sorted(
            {
                record["date"]
                for record in records
            }
        ),
        "input_hash":
            batch_input_hash(records),
        "created_at":
            datetime.now(
                TIMEZONE
            ).isoformat(),
    }

    metadata_path.write_text(
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def process_task4_batches(
    skill: str,
    records: list[dict[str, Any]],
    year: int,
    week: int,
    monday: date,
    business_date: date,
) -> list[str]:
    """
    返回全部 Batch Summary。

    每一个 ≤1200 字符。

    所有 Batch Summary 总长度不限。
    """

    if not records:

        log(
            "ℹ️ 本周暂无 Task 4 Analysis"
        )

        return []

    batches = (
        split_task4_batches(
            records
        )
    )

    log(
        f"📦 Task 4 分成 "
        f"{len(batches)} 个 Batch"
    )

    summaries: list[str] = []

    for index, batch in enumerate(
        batches,
        start=1,
    ):

        if valid_batch_cache(
            year,
            week,
            index,
            batch,
        ):

            summary = safe_read_text(
                batch_summary_path(
                    year,
                    week,
                    index,
                )
            )

            log(
                f"♻️ Batch "
                f"{index}/{len(batches)} "
                f"复用 Cache | "
                f"events={len(batch)} | "
                f"chars={len(summary)}"
            )

        else:

            log(
                f"🤖 Batch "
                f"{index}/{len(batches)} "
                f"调用 AI | "
                f"events={len(batch)}"
            )

            prompt = (
                build_batch_summary_prompt(
                    skill,
                    batch,
                    index,
                    len(batches),
                    monday,
                    business_date,
                )
            )

            raw_summary = call_ai(
                prompt,
                temperature=0.2,
            )

            summary = (
                build_batch_summary_text(
                    raw_summary
                )
            )

            if not summary:

                raise RuntimeError(
                    f"Batch {index} "
                    f"AI 返回空 Summary"
                )

            save_batch_cache(
                year,
                week,
                index,
                batch,
                summary,
            )

            log(
                f"💾 Batch "
                f"{index}/{len(batches)} "
                f"已缓存 | "
                f"chars={len(summary)}"
            )

        summaries.append(
            summary
        )

    return summaries


# ======================================================================
# Knowledge / Graph / Topic
# ======================================================================

def load_directory_markdown(
    directory: Path,
    max_chars: int,
) -> str:

    if not directory.exists():
        return ""

    chunks: list[str] = []

    total = 0

    files = sorted(
        directory.rglob("*.md")
    )

    for path in files:

        if not path.is_file():
            continue

        content = safe_read_text(
            path
        )

        if not content:
            continue

        block = (
            f"\n===== {path.name} =====\n"
            f"{content}\n"
        )

        if (
            total + len(block)
            > max_chars
        ):

            remaining = (
                max_chars - total
            )

            if remaining > 0:

                chunks.append(
                    block[:remaining]
                )

            break

        chunks.append(block)

        total += len(block)

    return "".join(
        chunks
    ).strip()


def load_knowledge_context() -> str:

    return load_directory_markdown(
        KNOWLEDGE_DIR,
        KNOWLEDGE_FINAL_MAX_CHARS,
    )


def load_graph_context() -> str:

    return load_directory_markdown(
        GRAPH_DIR,
        GRAPH_FINAL_MAX_CHARS,
    )


def load_topic_context() -> str:

    return load_directory_markdown(
        TOPIC_DIR,
        TOPIC_FINAL_MAX_CHARS,
    )


# ======================================================================
# Final Prompt
# ======================================================================

def build_final_prompt(
    skill: str,
    batch_summaries: list[str],
    daily_reports: list[dict[str, Any]],
    knowledge_context: str,
    graph_context: str,
    topic_context: str,
    year: int,
    week: int,
    monday: date,
    sunday: date,
    business_date: date,
) -> str:

    summary_blocks: list[str] = []

    for index, summary in enumerate(
        batch_summaries,
        start=1,
    ):

        summary_blocks.append(
            f"""
===== BATCH SUMMARY {index} =====

{summary}
""".strip()
        )

    all_batch_summaries = (
        "\n\n".join(
            summary_blocks
        )
    )

    daily_blocks: list[str] = []

    for report in daily_reports:

        daily_blocks.append(
            f"""
===== DAILY REPORT {report['date']} =====

{report['content']}
""".strip()
        )

    all_daily_reports = (
        "\n\n".join(
            daily_blocks
        )
    )

    return f"""
你是 748686 自生长知识系统的最终周报编写器。

请严格依据周报 Skill 和系统提供的数据，
生成当前 ISO Week 的最终周报。

============================================================
周报 Skill
============================================================

{skill}

============================================================
ISO Week
============================================================

Year：
{year}

Week：
W{week:02d}

完整周周期：

{monday.isoformat()}
→
{sunday.isoformat()}

本次实际纳入数据：

{monday.isoformat()}
→
{business_date.isoformat()}

注意：

今天是 {business_date.isoformat()}。

因此：

- 星期一至今天的数据可以使用。
- 今天之后的数据绝对不能写入。
- 不要为了“完整周报”而虚构未来日期的信息。
- 周报标题和周期可以使用完整 ISO Week。
- 周报内容只能基于当前已经发生并进入系统的数据。

============================================================
关于 1200 字符限制
============================================================

特别注意：

1200 字符限制只针对“单个 Batch Summary”。

当前可能存在：

Batch Summary 1
Batch Summary 2
Batch Summary 3
...
Batch Summary N

这些 Batch Summary 的总长度可以远远超过 1200 字符。

你必须综合全部 Batch Summary。

最终 Weekly Report：

不受 1200 字符限制。

不要把最终周报压缩到 1200 字符以内。

============================================================
Batch Summaries
============================================================

{all_batch_summaries}

============================================================
Daily Reports
============================================================

{all_daily_reports}

============================================================
Knowledge Base
============================================================

{knowledge_context}

============================================================
Knowledge Graph
============================================================

{graph_context}

============================================================
Topic Reports
============================================================

{topic_context}

============================================================
最终写作要求
============================================================

1. 严格遵守周报 Skill。
2. 以本周真实发生的事件为核心。
3. 对多个事件进行归纳，而不是简单罗列新闻。
4. 强调：
   - 本周发生了什么
   - 为什么重要
   - 事件之间有什么联系
   - 对技术、产业、科研、社会或知识体系有什么意义
   - 哪些趋势正在形成
5. Knowledge / Graph / Topic 只能作为辅助上下文。
6. 不得凭空增加事实。
7. 不得把未来日期写成已经发生。
8. 不要机械重复 Daily Report。
9. 不要机械重复 Batch Summary。
10. 必须进行真正的综合、归纳和结构化。
11. 最终报告可以明显长于 1200 字符。
12. 不要输出“AI生成”“Batch Summary”
    等内部处理说明。
13. 直接输出最终周报正文。
""".strip()


# ======================================================================
# 输出
# ======================================================================

def weekly_output_path(
    year: int,
    week: int,
) -> Path:

    directory = (
        WEEKLY_DIR
        / str(year)
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return (
        directory
        / f"W{week:02d}.md"
    )


def save_weekly(
    output: Path,
    content: str,
    *,
    year: int,
    week: int,
    monday: date,
    sunday: date,
    business_date: date,
) -> None:

    content = content.strip()

    if not content:
        raise RuntimeError(
            "最终周报为空"
        )

    header = f"""---
type: weekly_report
year: {year}
week: {week}
week_label: W{week:02d}
week_start: {monday.isoformat()}
week_end: {sunday.isoformat()}
updated_to: {business_date.isoformat()}
generated_at: {datetime.now(TIMEZONE).isoformat()}
---

"""

    output.write_text(
        header
        + content
        + "\n",
        encoding="utf-8",
    )


# ======================================================================
# Main
# ======================================================================

def main() -> int:

    args = parse_args()

    business_date = (
        parse_business_date(
            args.today
        )
    )

    (
        year,
        week,
        monday,
        sunday,
    ) = current_week(
        business_date
    )

    log("=" * 72)

    log(
        "748686 自生长知识系统 "
        "Weekly Report V3.3"
    )

    log("=" * 72)

    log(
        f"📅 Business Date : "
        f"{business_date.isoformat()}"
    )

    log(
        f"📅 ISO Week      : "
        f"{year}-W{week:02d}"
    )

    log(
        f"📅 Week Range    : "
        f"{monday.isoformat()} → "
        f"{sunday.isoformat()}"
    )

    log(
        f"📅 Actual Range  : "
        f"{monday.isoformat()} → "
        f"{business_date.isoformat()}"
    )

    output = weekly_output_path(
        year,
        week,
    )

    if output.exists():

        log(
            f"🔄 ROLLING UPDATE | "
            f"当前周报已存在，将重新生成："
            f"{output}"
        )

    else:

        log(
            f"🆕 NEW WEEKLY REPORT | "
            f"创建：{output}"
        )

    # ------------------------------------------------------------------
    # API Key
    # ------------------------------------------------------------------

    if not AGNES_API_KEY:

        raise RuntimeError(
            "缺少环境变量 AGNES_API_KEY"
        )

    # ------------------------------------------------------------------
    # Skill
    # ------------------------------------------------------------------

    skill = load_weekly_skill()

    log(
        f"📘 Skill loaded | "
        f"{SKILL_FILE}"
    )

    # ------------------------------------------------------------------
    # Daily
    # ------------------------------------------------------------------

    daily_reports = (
        load_week_daily_reports(
            monday,
            business_date,
        )
    )

    log(
        f"📰 Daily Reports : "
        f"{len(daily_reports)}"
    )

    # ------------------------------------------------------------------
    # Task 4
    # ------------------------------------------------------------------

    analysis_records = (
        load_week_analysis_records(
            monday,
            business_date,
        )
    )

    log(
        f"🧠 Task 4 Analysis : "
        f"{len(analysis_records)} events"
    )

    # ------------------------------------------------------------------
    # Batch
    # ------------------------------------------------------------------

    batch_summaries = (
        process_task4_batches(
            skill,
            analysis_records,
            year,
            week,
            monday,
            business_date,
        )
    )

    log(
        f"📦 Batch Summaries : "
        f"{len(batch_summaries)}"
    )

    total_batch_chars = sum(
        len(summary)
        for summary in batch_summaries
    )

    log(
        f"📊 Batch Summary total chars : "
        f"{total_batch_chars}"
    )

    # ------------------------------------------------------------------
    # Knowledge
    # ------------------------------------------------------------------

    knowledge_context = (
        load_knowledge_context()
    )

    graph_context = (
        load_graph_context()
    )

    topic_context = (
        load_topic_context()
    )

    log(
        f"📚 Knowledge chars : "
        f"{len(knowledge_context)}"
    )

    log(
        f"🕸️ Graph chars     : "
        f"{len(graph_context)}"
    )

    log(
        f"📑 Topic chars     : "
        f"{len(topic_context)}"
    )

    # ------------------------------------------------------------------
    # Final AI
    #
    # 这里没有 1200 字符限制。
    # ------------------------------------------------------------------

    final_prompt = (
        build_final_prompt(
            skill=skill,
            batch_summaries=
                batch_summaries,
            daily_reports=
                daily_reports,
            knowledge_context=
                knowledge_context,
            graph_context=
                graph_context,
            topic_context=
                topic_context,
            year=year,
            week=week,
            monday=monday,
            sunday=sunday,
            business_date=
                business_date,
        )
    )

    log(
        "🤖 正在生成最终 Weekly Report..."
    )

    final_report = call_ai(
        final_prompt,
        temperature=0.2,
    )

    final_report = (
        final_report
        .replace("\x00", "")
        .strip()
    )

    if not final_report:

        raise RuntimeError(
            "最终 Weekly Report 为空"
        )

    log(
        f"📝 Final Weekly Report chars : "
        f"{len(final_report)}"
    )

    # ------------------------------------------------------------------
    # 保存
    #
    # 无论 Wxx.md 是否存在，
    # 当前业务日都重新覆盖。
    # ------------------------------------------------------------------

    save_weekly(
        output,
        final_report,
        year=year,
        week=week,
        monday=monday,
        sunday=sunday,
        business_date=
            business_date,
    )

    log(
        f"✅ Weekly Report saved："
        f"{output}"
    )

    log("=" * 72)

    log(
        "🎉 Weekly Report V3.3 完成"
    )

    log("=" * 72)

    return 0


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    try:

        sys.exit(
            main()
        )

    except KeyboardInterrupt:

        log(
            "⛔ 用户中断"
        )

        sys.exit(130)

    except Exception as exc:

        log(
            f"❌ Weekly Report 失败："
            f"{exc}"
        )

        sys.exit(1)
