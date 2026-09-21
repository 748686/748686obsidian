#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Weekly Report V3.2

======================================================================
核心架构
======================================================================

V3.1：

    Skill
      +
    Daily
      +
    559 Task 4 Analysis
      +
    Knowledge
      +
    Graph
      +
    Topics
            ↓
       单次超大 AI Request
            ↓
          Weekly

V3.2：

    Skill
      +
    Task 4 Analysis
            ↓
       分批 AI 编译
            ↓
    持久化 Batch Summary
            ↓
       周级综合 AI
            ↓
          Weekly

======================================================================
V3.2 核心目标
======================================================================

1. Task 4 Analysis 不再一次性全部发送给 AI。
2. 每批 Task 4 Analysis 独立生成 Batch Summary。
3. Batch Summary 本地持久化。
4. 已成功的 Batch Summary 下次运行直接 SKIP。
5. 中途 429 / 5xx / 网络错误不会导致已经成功的批次重新生成。
6. 400 / 401 / 403 等请求错误输出 API response body，方便定位。
7. 429 / 5xx 使用退避重试。
8. 400 不进行无意义的重复 retry。
9. 最终周报只在最终 AI 成功后写入正式 Wxx.md。
10. Workflow --today 优先作为业务日期。
11. 不修改 Task 1 / Task 2 / Task 3 / Task 4。
12. 不写 00_System 知识成果。
13. 不允许 Runner 当前日期覆盖 Workflow 业务日期。
14. 同一个 EVT-ID 的 en / zh Analysis 只计算一次。
15. 周报格式完全由周报 Skill 决定。
16. 批次结果属于 Weekly Report 工作缓存，不属于知识成果。

======================================================================
时间
======================================================================

Workflow 传入 --today 时：

    --today = 唯一业务日期来源

Workflow 未传 --today 时：

    使用 Asia/Shanghai
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib import error, request
from zoneinfo import ZoneInfo


# ======================================================================
# PATH
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

SKILL_FILE = (
    ROOT
    / "Skills"
    / "05.汇报写作"
    / "周报编写助手.md"
)

DAILY_DIR = ROOT / "05_日报"

WEEKLY_DIR = ROOT / "06_周报"

KNOWLEDGE_DIR = ROOT / "08_知识库"

GRAPH_DIR = ROOT / "09_知识图谱"

TOPIC_DIR = ROOT / "07_专题报告"

# ----------------------------------------------------------------------
# Weekly Report 工作缓存
#
# 注意：
# 这里只保存周报编译过程中的中间 Batch Summary。
# 不属于 08_知识库 / 09_知识图谱 / 00_System。
# ----------------------------------------------------------------------

WEEKLY_CACHE_DIR = (
    WEEKLY_DIR
    / ".cache"
)


# ======================================================================
# TIMEZONE
# ======================================================================

TIMEZONE = ZoneInfo(
    "Asia/Shanghai"
)


# ======================================================================
# AI
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1"
).rstrip("/")

AGNES_MODEL = os.getenv(
    "AGNES_MODEL",
    "agnes-2.5-flash"
)

AGNES_API_KEY = os.getenv(
    "AGNES_API_KEY"
)

AI_TIMEOUT = int(
    os.getenv(
        "WEEKLY_REPORT_TIMEOUT",
        "240"
    )
)

AI_RETRIES = int(
    os.getenv(
        "WEEKLY_REPORT_RETRIES",
        "3"
    )
)

AI_THROTTLE = float(
    os.getenv(
        "WEEKLY_REPORT_THROTTLE",
        "2.0"
    )
)

# ----------------------------------------------------------------------
# Task 4 Batch
# ----------------------------------------------------------------------

TASK4_BATCH_MAX_EVENTS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_EVENTS",
        "20"
    )
)

TASK4_BATCH_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_CHARS",
        "28000"
    )
)

# 最终周报阶段允许使用的材料大小。
# 这里不再直接把完整 Knowledge / Graph / Topic 全部塞入。
KNOWLEDGE_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_KNOWLEDGE_FINAL_CHARS",
        "30000"
    )
)

GRAPH_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_GRAPH_FINAL_CHARS",
        "18000"
    )
)

TOPIC_FINAL_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_TOPIC_FINAL_CHARS",
        "18000"
    )
)

# 每个 Batch Summary 最多保留多少字符。
# 防止最终周报 Prompt 因批次数量再次膨胀。
BATCH_SUMMARY_MAX_CHARS = int(
    os.getenv(
        "WEEKLY_REPORT_BATCH_SUMMARY_CHARS",
        "1200"
    )
)


# ======================================================================
# LOG
# ======================================================================

def log(message: str) -> None:

    print(
        message,
        flush=True
    )


# ======================================================================
# FILE
# ======================================================================

def read_text(
    path: Path
) -> str:

    if not path.exists():
        return ""

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

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    tmp.write_text(
        content,
        encoding="utf-8"
    )

    tmp.replace(
        path
    )


def nonempty_files(
    directory: Path
):

    if not directory.exists():
        return []

    result = []

    for path in directory.rglob(
        "*.md"
    ):

        if not path.is_file():
            continue

        try:

            if path.stat().st_size <= 0:
                continue

        except Exception:

            continue

        result.append(
            path
        )

    return sorted(
        result,
        key=lambda x: x.as_posix()
    )


# ======================================================================
# SKILL
# ======================================================================

def load_weekly_skill() -> str:

    if not SKILL_FILE.exists():

        raise RuntimeError(
            "周报 Skill 不存在：\n"
            f"{SKILL_FILE}"
        )

    content = read_text(
        SKILL_FILE
    ).strip()

    if not content:

        raise RuntimeError(
            "周报 Skill 文件为空：\n"
            f"{SKILL_FILE}"
        )

    return content


# ======================================================================
# DATE / ISO WEEK
# ======================================================================

def now_local() -> datetime:

    return datetime.now(
        TIMEZONE
    )


def parse_business_date(
    value: str
) -> date:

    try:

        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

    except ValueError as exc:

        raise RuntimeError(
            "业务日期格式错误，必须为 YYYY-MM-DD："
            f"{value}"
        ) from exc


def current_week(
    business_date: date | None = None
):

    if business_date is None:

        current = now_local().date()

    else:

        current = business_date

    iso_year, iso_week, iso_weekday = (
        current.isocalendar()
    )

    monday = (
        current
        - timedelta(
            days=iso_weekday - 1
        )
    )

    sunday = (
        monday
        + timedelta(
            days=6
        )
    )

    return (
        iso_year,
        iso_week,
        monday,
        sunday
    )


# ======================================================================
# ARGUMENTS
# ======================================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "748686 自生长知识系统 "
            "Weekly Report V3.2"
        )
    )

    parser.add_argument(
        "--day-before",
        required=False,
        default=None
    )

    parser.add_argument(
        "--yesterday",
        required=False,
        default=None
    )

    parser.add_argument(
        "--today",
        required=False,
        default=None
    )

    return parser.parse_args()


# ======================================================================
# DAILY REPORTS
# ======================================================================

def daily_path(
    date_obj
) -> Path:

    date_str = date_obj.strftime(
        "%Y-%m-%d"
    )

    return (
        DAILY_DIR
        / date_obj.strftime("%Y")
        / date_obj.strftime("%m")
        / f"{date_str}.md"
    )


def load_week_daily_reports(
    monday,
    sunday
):

    reports = []

    current = monday

    while current <= sunday:

        path = daily_path(
            current
        )

        if (
            path.exists()
            and path.stat().st_size > 0
        ):

            reports.append(
                (
                    current.strftime(
                        "%Y-%m-%d"
                    ),
                    path,
                    read_text(path)
                )
            )

        current += timedelta(
            days=1
        )

    return reports


# ======================================================================
# TASK 4
# ======================================================================

def analysis_files_for_date(
    date_str: str
):

    result = []

    for language in (
        "en",
        "zh"
    ):

        directory = (
            RAW_NEWS
            / f"{date_str}-EventUnit"
            / language
            / "event_units"
        )

        if not directory.exists():
            continue

        result.extend(
            sorted(
                directory.glob(
                    "*_analysis.md"
                )
            )
        )

    return [
        path
        for path in result
        if (
            path.is_file()
            and path.stat().st_size > 0
        )
    ]


def event_id(
    path: Path
) -> str:

    match = re.search(
        r"EVT-\d{8}-\d+",
        path.name
    )

    if match:
        return match.group(0)

    return path.stem.replace(
        "_analysis",
        ""
    )


def load_week_analysis_records(
    monday,
    sunday
):

    records = []

    seen_events = set()

    current = monday

    file_count = 0

    while current <= sunday:

        date_str = current.strftime(
            "%Y-%m-%d"
        )

        files = analysis_files_for_date(
            date_str
        )

        for path in files:

            file_count += 1

            eid = event_id(
                path
            )

            if eid in seen_events:

                continue

            seen_events.add(
                eid
            )

            path_text = path.as_posix()

            if "/en/" in path_text:

                language = "en"

            else:

                language = "zh"

            content = read_text(
                path
            ).strip()

            if not content:
                continue

            records.append(
                {
                    "date": date_str,
                    "event_id": eid,
                    "language": language,
                    "path": str(
                        path.relative_to(ROOT)
                    ),
                    "content": content,
                }
            )

        current += timedelta(
            days=1
        )

    return (
        records,
        file_count,
        len(seen_events)
    )


# ======================================================================
# TASK 4 BATCHING
# ======================================================================

def make_task4_block(
    record: dict
) -> str:

    return "\n".join([
        "=" * 70,
        f"DATE: {record['date']}",
        f"EVENT_ID: {record['event_id']}",
        f"LANGUAGE: {record['language']}",
        f"FILE: {record['path']}",
        "=" * 70,
        record["content"],
    ])


def split_task4_batches(
    records
):

    batches = []

    current = []

    current_chars = 0

    for record in records:

        block = make_task4_block(
            record
        )

        block_chars = len(
            block
        )

        # --------------------------------------------------------------
        # 如果当前 batch 已经达到事件数量限制
        # --------------------------------------------------------------

        if (
            current
            and len(current)
            >= TASK4_BATCH_MAX_EVENTS
        ):

            batches.append(
                current
            )

            current = []

            current_chars = 0

        # --------------------------------------------------------------
        # 如果加入该事件会超过字符限制
        # --------------------------------------------------------------

        if (
            current
            and
            current_chars
            + block_chars
            > TASK4_BATCH_MAX_CHARS
        ):

            batches.append(
                current
            )

            current = []

            current_chars = 0

        # --------------------------------------------------------------
        # 单个事件本身超过 batch 字符限制
        #
        # 不截断。
        # 单事件单独作为一个 batch，保证 Task 4 内容不丢失。
        # --------------------------------------------------------------

        if (
            not current
            and block_chars
            > TASK4_BATCH_MAX_CHARS
        ):

            batches.append(
                [record]
            )

            continue

        current.append(
            record
        )

        current_chars += (
            block_chars
        )

    if current:

        batches.append(
            current
        )

    return batches


# ======================================================================
# BATCH CACHE
# ======================================================================

def batch_cache_dir(
    year: int,
    week: int
) -> Path:

    return (
        WEEKLY_CACHE_DIR
        / str(year)
        / f"W{week:02d}"
        / "task4_batches"
    )


def batch_cache_path(
    year: int,
    week: int,
    batch_index: int
) -> Path:

    return (
        batch_cache_dir(
            year,
            week
        )
        / f"batch_{batch_index:04d}.md"
    )


def batch_meta_path(
    year: int,
    week: int,
    batch_index: int
) -> Path:

    return (
        batch_cache_dir(
            year,
            week
        )
        / f"batch_{batch_index:04d}.json"
    )


def valid_batch_cache(
    path: Path
) -> bool:

    return (
        path.exists()
        and path.is_file()
        and path.stat().st_size > 0
    )


def save_batch_summary(
    year: int,
    week: int,
    batch_index: int,
    records,
    summary: str
) -> None:

    cache_dir = batch_cache_dir(
        year,
        week
    )

    cache_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    summary = summary.strip()

    if not summary:

        raise RuntimeError(
            f"Batch {batch_index} AI 摘要为空"
        )

    summary_path = batch_cache_path(
        year,
        week,
        batch_index
    )

    meta_path = batch_meta_path(
        year,
        week,
        batch_index
    )

    event_ids = [
        record["event_id"]
        for record in records
    ]

    dates = sorted(
        {
            record["date"]
            for record in records
        }
    )

    metadata = {
        "version": "V3.2",
        "year": year,
        "week": week,
        "batch_index": batch_index,
        "event_count": len(records),
        "event_ids": event_ids,
        "dates": dates,
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    atomic_write(
        summary_path,
        summary + "\n"
    )

    atomic_write(
        meta_path,
        json.dumps(
            metadata,
            ensure_ascii=False,
            indent=2
        ) + "\n"
    )


def load_existing_batch_summary(
    year: int,
    week: int,
    batch_index: int
) -> str:

    path = batch_cache_path(
        year,
        week,
        batch_index
    )

    if not valid_batch_cache(path):
        return ""

    return read_text(
        path
    ).strip()


# ======================================================================
# AI HTTP ERROR DIAGNOSTICS
# ======================================================================

def http_error_body(
    exc: error.HTTPError
) -> str:

    try:

        raw = exc.read()

        if not raw:
            return ""

        return raw.decode(
            "utf-8",
            errors="replace"
        )

    except Exception:

        return ""


def should_retry_http_status(
    status: int
) -> bool:

    if status == 429:
        return True

    if status in (
        500,
        502,
        503,
        504
    ):
        return True

    return False


def retry_delay(
    attempt: int,
    status: int | None = None
) -> float:

    # --------------------------------------------------------------
    # 429 使用更长退避。
    # --------------------------------------------------------------

    if status == 429:

        return max(
            AI_THROTTLE * attempt * 2,
            5.0
        )

    return (
        AI_THROTTLE
        * attempt
    )


# ======================================================================
# AI
# ======================================================================

def call_ai(
    system_prompt: str,
    user_prompt: str,
    purpose: str = "AI"
) -> str:

    if not AGNES_API_KEY:

        raise RuntimeError(
            "缺少 AGNES_API_KEY"
        )

    url = (
        AGNES_BASE_URL
        + "/chat/completions"
    )

    payload = {
        "model": AGNES_MODEL,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }

    data = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    headers = {
        "Authorization":
            f"Bearer {AGNES_API_KEY}",
        "Content-Type":
            "application/json",
        "Accept":
            "application/json",
    }

    last_error = None

    for attempt in range(
        1,
        AI_RETRIES + 1
    ):

        try:

            if attempt > 1:

                time.sleep(
                    retry_delay(
                        attempt
                    )
                )

            req = request.Request(
                url,
                data=data,
                headers=headers,
                method="POST"
            )

            with request.urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as response:

                raw = (
                    response
                    .read()
                    .decode(
                        "utf-8",
                        errors="replace"
                    )
                )

            response_data = json.loads(
                raw
            )

            choices = (
                response_data.get(
                    "choices"
                )
                or []
            )

            if not choices:

                raise RuntimeError(
                    f"{purpose}："
                    "AI response 缺少 choices"
                )

            message = (
                choices[0].get(
                    "message"
                )
                or {}
            )

            content = (
                message.get(
                    "content",
                    ""
                )
            )

            if not isinstance(
                content,
                str
            ):

                raise RuntimeError(
                    f"{purpose}："
                    "AI content 不是字符串"
                )

            if not content.strip():

                raise RuntimeError(
                    f"{purpose}："
                    "AI 返回为空"
                )

            return content.strip()

        except error.HTTPError as exc:

            status = exc.code

            body = http_error_body(
                exc
            )

            last_error = exc

            log(
                f"⚠️ {purpose} | "
                f"HTTP {status} | "
                f"attempt {attempt}/{AI_RETRIES}"
            )

            if body:

                # 防止错误 response 无限刷日志。
                diagnostic = body[:6000]

                log(
                    "   AGNES RESPONSE:"
                )

                log(
                    diagnostic
                )

            # ------------------------------------------------------
            # 400：
            # 请求本身有问题。
            # 不重复发送完全相同的请求。
            # ------------------------------------------------------

            if status == 400:

                raise RuntimeError(
                    f"{purpose}："
                    f"HTTP 400 Bad Request\n"
                    f"AGNES RESPONSE:\n"
                    f"{body[:6000]}"
                ) from exc

            # ------------------------------------------------------
            # 401 / 403：
            # API Key / 权限问题。
            # ------------------------------------------------------

            if status in (
                401,
                403
            ):

                raise RuntimeError(
                    f"{purpose}："
                    f"HTTP {status}\n"
                    f"AGNES RESPONSE:\n"
                    f"{body[:6000]}"
                ) from exc

            # ------------------------------------------------------
            # 其他 HTTP 错误：
            # 只有明确属于可恢复状态才 retry。
            # ------------------------------------------------------

            if should_retry_http_status(
                status
            ):

                if attempt < AI_RETRIES:

                    delay = retry_delay(
                        attempt,
                        status
                    )

                    log(
                        f"   → {delay:.1f}s 后重试"
                    )

                    time.sleep(
                        delay
                    )

                    continue

            raise RuntimeError(
                f"{purpose}："
                f"HTTP {status}\n"
                f"AGNES RESPONSE:\n"
                f"{body[:6000]}"
            ) from exc

        except (
            TimeoutError,
            ConnectionError
        ) as exc:

            last_error = exc

            log(
                f"⚠️ {purpose} | "
                f"NETWORK ERROR | "
                f"attempt {attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            if attempt < AI_RETRIES:

                delay = retry_delay(
                    attempt
                )

                log(
                    f"   → {delay:.1f}s 后重试"
                )

                time.sleep(
                    delay
                )

                continue

            raise RuntimeError(
                f"{purpose}："
                f"网络请求失败：{exc}"
            ) from exc

        except Exception as exc:

            last_error = exc

            log(
                f"⚠️ {purpose} | "
                f"ERROR | "
                f"attempt {attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            # ------------------------------------------------------
            # 普通 JSON / 解析错误允许 retry。
            # ------------------------------------------------------

            if attempt < AI_RETRIES:

                delay = retry_delay(
                    attempt
                )

                log(
                    f"   → {delay:.1f}s 后重试"
                )

                time.sleep(
                    delay
                )

                continue

            raise RuntimeError(
                f"{purpose}："
                f"{exc}"
            ) from exc

    raise RuntimeError(
        f"{purpose} 请求失败："
        f"{last_error}"
    )


# ======================================================================
# BATCH AI PROMPT
# ======================================================================

BATCH_SYSTEM_PROMPT = """
你是 748686 自生长知识系统的「周级 Task 4 编译器」。

你的任务不是写最终周报。

你的任务是：

把这一批 Task 4 Event Analysis 编译成一个高度压缩、
事实准确、可用于最终周报综合的「Weekly Batch Summary」。

严格要求：

1. 只能使用输入材料。
2. 不得编造事实。
3. 保留重要的新事实、产品、公司、技术、人物、行业变化。
4. 识别同一主题下的多个事件。
5. 优先保留真正有周级意义的信息。
6. 区分事实与分析。
7. 不要简单逐条复述事件。
8. 进行批次内部综合。
9. 最终输出纯 Markdown。
10. 不要输出 markdown code fence。
11. 不要解释你做了什么。
12. 这是中间摘要，不是最终周报。

建议结构：

### 本批核心变化
### 重要事实
### 重要趋势
### 值得进入周报的判断
### 关键实体与关系

如果某项没有足够证据，可以省略。
"""


def build_batch_prompt(
    year: int,
    week: int,
    batch_index: int,
    total_batches: int,
    records
) -> str:

    blocks = []

    for record in records:

        blocks.append(
            make_task4_block(
                record
            )
        )

    analysis_text = "\n\n".join(
        blocks
    )

    event_ids = ", ".join(
        record["event_id"]
        for record in records
    )

    return f"""
当前周：

ISO YEAR: {year}
ISO WEEK: {week:02d}

这是本周 Task 4 Analysis 的：

BATCH: {batch_index}/{total_batches}

本批事件数：

{len(records)}

本批 EVT-ID：

{event_ids}

============================================================
TASK 4 ANALYSIS
============================================================

{analysis_text}

============================================================

请把以上 Task 4 Analysis 编译为一个高度压缩的 Weekly Batch Summary。

要求：

- 不遗漏真正重要的信息；
- 不重复同一个 EVT-ID；
- 不编造；
- 不把没有证据的推断写成事实；
- 关注本批事件之间的共同主题；
- 关注变化、趋势、技术演进和重要实体；
- 这是最终周报的中间材料；
- 输出尽可能紧凑；
- 最终只输出 Markdown。
"""


# ======================================================================
# BATCH COMPILATION
# ======================================================================

def compile_task4_batches(
    year: int,
    week: int,
    records
):

    batches = split_task4_batches(
        records
    )

    total_batches = len(
        batches
    )

    log("")
    log(
        "============================================================"
    )
    log(
        "TASK 4 → WEEKLY BATCH COMPILATION"
    )
    log(
        "============================================================"
    )

    log(
        f"Task 4 Unique Events : "
        f"{len(records)}"
    )

    log(
        f"Batch Count          : "
        f"{total_batches}"
    )

    log(
        f"Batch Max Events     : "
        f"{TASK4_BATCH_MAX_EVENTS}"
    )

    log(
        f"Batch Max Chars      : "
        f"{TASK4_BATCH_MAX_CHARS}"
    )

    summaries = []

    for index, batch in enumerate(
        batches,
        start=1
    ):

        cache_path = batch_cache_path(
            year,
            week,
            index
        )

        existing = (
            load_existing_batch_summary(
                year,
                week,
                index
            )
        )

        if existing:

            log(
                f"⏭️ BATCH {index}/{total_batches} "
                f"| CACHE HIT "
                f"| events={len(batch)} "
                f"| {cache_path}"
            )

            summaries.append(
                {
                    "batch_index": index,
                    "event_count": len(batch),
                    "event_ids": [
                        record["event_id"]
                        for record in batch
                    ],
                    "summary": existing,
                }
            )

            continue

        log(
            f"🧠 BATCH {index}/{total_batches} "
            f"| AI "
            f"| events={len(batch)}"
        )

        prompt = build_batch_prompt(
            year,
            week,
            index,
            total_batches,
            batch
        )

        summary = call_ai(
            BATCH_SYSTEM_PROMPT,
            prompt,
            purpose=(
                f"Task4 Batch "
                f"{index}/{total_batches}"
            )
        )

        # --------------------------------------------------------------
        # 限制最终摘要大小。
        # --------------------------------------------------------------

        if len(summary) > BATCH_SUMMARY_MAX_CHARS:

            summary = (
                summary[
                    :BATCH_SUMMARY_MAX_CHARS
                ]
                + "\n\n"
                + "（Batch Summary 已按周报编译限制压缩。）"
            )

        save_batch_summary(
            year,
            week,
            index,
            batch,
            summary
        )

        log(
            f"✅ BATCH {index}/{total_batches} "
            f"| SAVED "
            f"| {cache_path}"
        )

        summaries.append(
            {
                "batch_index": index,
                "event_count": len(batch),
                "event_ids": [
                    record["event_id"]
                    for record in batch
                ],
                "summary": summary,
            }
        )

    return summaries


# ======================================================================
# KNOWLEDGE BASE
# ======================================================================

def load_knowledge_base(
    max_chars: int = 90000
) -> str:

    files = nonempty_files(
        KNOWLEDGE_DIR
    )

    chunks = []

    total = 0

    for path in files:

        content = read_text(
            path
        ).strip()

        if not content:
            continue

        block = (
            "\n"
            + "=" * 60
            + "\n"
            + f"FILE: {path.relative_to(ROOT)}\n"
            + "=" * 60
            + "\n"
            + content
            + "\n"
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

        total += len(block)

    return "\n".join(
        chunks
    )


# ======================================================================
# GRAPH
# ======================================================================

def load_graph(
    max_chars: int = 50000
) -> str:

    files = nonempty_files(
        GRAPH_DIR
    )

    chunks = []

    total = 0

    for path in files:

        content = read_text(
            path
        ).strip()

        if not content:
            continue

        block = (
            "\n"
            + "=" * 60
            + "\n"
            + f"FILE: {path.relative_to(ROOT)}\n"
            + "=" * 60
            + "\n"
            + content
            + "\n"
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

        total += len(block)

    return "\n".join(
        chunks
    )


# ======================================================================
# TOPICS
# ======================================================================

def load_topic_reports(
    max_files: int = 20,
    max_chars: int = 50000
) -> str:

    files = nonempty_files(
        TOPIC_DIR
    )

    files = files[-max_files:]

    chunks = []

    total = 0

    for path in files:

        content = read_text(
            path
        ).strip()

        if not content:
            continue

        block = (
            "\n"
            + "=" * 60
            + "\n"
            + f"FILE: {path.relative_to(ROOT)}\n"
            + "=" * 60
            + "\n"
            + content
            + "\n"
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

        total += len(block)

    return "\n".join(
        chunks
    )


# ======================================================================
# FINAL MATERIAL COMPRESSION
# ======================================================================

def limit_text(
    text: str,
    max_chars: int
) -> str:

    text = (
        text or ""
    ).strip()

    if len(text) <= max_chars:

        return text

    return (
        text[:max_chars]
        + "\n\n"
        + "（本节已达到周报最终 Prompt 字符限制。）"
    )


def build_batch_summary_text(
    summaries
) -> str:

    chunks = []

    for item in summaries:

        summary = limit_text(
            item["summary"],
            BATCH_SUMMARY_MAX_CHARS
        )

        chunks.append(
            "\n".join([
                "=" * 60,
                (
                    f"BATCH: "
                    f"{item['batch_index']}"
                ),
                (
                    f"EVENTS: "
                    f"{item['event_count']}"
                ),
                (
                    "EVT-ID: "
                    + ", ".join(
                        item["event_ids"]
                    )
                ),
                "=" * 60,
                summary,
            ])
        )

    return "\n\n".join(
        chunks
    )


# ======================================================================
# FINAL PROMPT
# ======================================================================

SYSTEM_PROMPT = """
你是 748686 自生长知识系统的周报编写执行器。

你必须严格执行：

「Skills/05.汇报写作/周报编写助手.md」

该 Skill 是本次周报生成的正式规范。

重要：

1. 必须完整阅读周报 Skill。
2. 周报结构完全服从 Skill。
3. 不得自行发明新的周报模板。
4. 不得简单复制日报。
5. 必须进行周级综合判断。
6. 必须区分本周新事实与历史知识。
7. 不得编造事实。
8. 同一个 EVT-ID 只能计算一次。
9. Batch Summary 是 Task 4 的压缩编译结果。
10. 如果不同材料之间存在冲突或不确定性，应按 Skill 的要求处理。
11. 最终只输出可以直接保存的 Markdown 周报正文。
12. 不要输出解释。
13. 不要输出 markdown code fence。

重要：

本次 Task 4 已经经过批次编译。

不要试图把 Batch Summary 当成日报。
必须把所有 Batch Summary 作为本周事件层面的综合材料。

知识库、知识图谱、专题报告属于长期背景材料。
不要把历史知识误写成本周新事件。

最终周报必须体现：

    本周发生了什么
    +
    为什么重要
    +
    与已有知识有什么关系
    +
    出现了什么变化
    +
    可以形成什么有依据的判断

但所有事实必须来自输入材料。
"""


def build_final_prompt(
    year: int,
    week: int,
    monday,
    sunday,
    skill: str,
    daily_text: str,
    batch_summary_text: str,
    knowledge_text: str,
    graph_text: str,
    topic_text: str
) -> str:

    missing_daily = []

    current = monday

    while current <= sunday:

        path = daily_path(
            current
        )

        if not (
            path.exists()
            and path.stat().st_size > 0
        ):

            missing_daily.append(
                current.strftime(
                    "%Y-%m-%d"
                )
            )

        current += timedelta(
            days=1
        )

    missing_text = (
        "无"
        if not missing_daily
        else "、".join(
            missing_daily
        )
    )

    return f"""
当前周：

ISO YEAR: {year}
ISO WEEK: {week:02d}

本周：

{monday.strftime("%Y-%m-%d")}
至
{sunday.strftime("%Y-%m-%d")}

缺失日报日期：

{missing_text}

============================================================
周报编写 Skill
============================================================

{skill}

============================================================
本周日报
============================================================

{daily_text or "本周没有可用日报。"}

============================================================
本周 Task 4 Batch Summaries
============================================================

{batch_summary_text or "本周没有可用 Task 4 Batch Summary。"}

============================================================
当前长期知识库
============================================================

{limit_text(
    knowledge_text,
    KNOWLEDGE_FINAL_MAX_CHARS
) or "当前没有可用知识库内容。"}

============================================================
当前知识图谱
============================================================

{limit_text(
    graph_text,
    GRAPH_FINAL_MAX_CHARS
) or "当前没有可用知识图谱内容。"}

============================================================
近期专题报告
============================================================

{limit_text(
    topic_text,
    TOPIC_FINAL_MAX_CHARS
) or "当前没有可用专题报告。"}

============================================================

现在开始编写本周周报。

严格执行「周报编写助手」中的全部要求。

特别注意：

- 周报不是日报简单拼接；
- Task 4 Batch Summary 已经是本周事件层面的压缩综合；
- 必须综合全部 Batch Summary；
- 必须利用已有长期知识判断本周变化；
- 必须区分新事实、已有知识和新的判断；
- 不得把历史知识误写成新事件；
- 不得编造；
- 不得因为资料缺失而虚构内容；
- 最终只输出周报正文。
"""


# ======================================================================
# OUTPUT
# ======================================================================

def weekly_output_path(
    year: int,
    week: int
) -> Path:

    return (
        WEEKLY_DIR
        / str(year)
        / f"W{week:02d}.md"
    )


def save_weekly(
    path: Path,
    content: str
) -> None:

    content = content.strip()

    if not content:

        raise RuntimeError(
            "AI 生成的周报为空"
        )

    atomic_write(
        path,
        content + "\n"
    )

    if not (
        path.exists()
        and path.stat().st_size > 0
    ):

        raise RuntimeError(
            f"周报保存失败：{path}"
        )


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    args = parse_args()

    log("")
    log("#" * 72)
    log(
        "748686 自生长知识系统"
    )
    log(
        "WEEKLY REPORT V3.2"
    )
    log("#" * 72)

    if not AGNES_API_KEY:

        raise RuntimeError(
            "未设置 AGNES_API_KEY"
        )

    # --------------------------------------------------------------
    # BUSINESS DATE
    # --------------------------------------------------------------

    if args.today:

        business_date = parse_business_date(
            args.today
        )

        log(
            f"BUSINESS DATE : "
            f"{business_date}"
        )

        if args.yesterday:

            log(
                f"YESTERDAY     : "
                f"{args.yesterday}"
            )

        if args.day_before:

            log(
                f"DAY BEFORE    : "
                f"{args.day_before}"
            )

        log(
            "DATE SOURCE   : "
            "Workflow --today"
        )

    else:

        business_date = (
            now_local().date()
        )

        log(
            f"BUSINESS DATE : "
            f"{business_date}"
        )

        log(
            "DATE SOURCE   : "
            "Asia/Shanghai system time"
        )

    # --------------------------------------------------------------
    # ISO WEEK
    # --------------------------------------------------------------

    year, week, monday, sunday = (
        current_week(
            business_date
        )
    )

    log(
        f"ISO WEEK : "
        f"{year}-W{week:02d}"
    )

    log(
        f"PERIOD   : "
        f"{monday} → {sunday}"
    )

    # --------------------------------------------------------------
    # Skill
    # --------------------------------------------------------------

    skill = load_weekly_skill()

    log(
        "✅ 周报 Skill 已加载"
    )

    log(
        f"   {SKILL_FILE}"
    )

    # --------------------------------------------------------------
    # Output exists
    # --------------------------------------------------------------

    output = weekly_output_path(
        year,
        week
    )

    if (
        output.exists()
        and output.stat().st_size > 0
    ):

        log(
            f"⏭️ SKIP | "
            f"周报已存在：{output}"
        )

        return

    # --------------------------------------------------------------
    # Daily
    # --------------------------------------------------------------

    daily_reports = (
        load_week_daily_reports(
            monday,
            sunday
        )
    )

    daily_chunks = []

    for (
        date_str,
        path,
        content
    ) in daily_reports:

        daily_chunks.append(
            "\n".join([
                "=" * 70,
                f"DATE: {date_str}",
                f"FILE: {path.relative_to(ROOT)}",
                "=" * 70,
                content,
            ])
        )

    daily_text = (
        "\n\n".join(
            daily_chunks
        )
    )

    log(
        f"Daily Reports : "
        f"{len(daily_reports)}"
    )

    # --------------------------------------------------------------
    # Task 4
    # --------------------------------------------------------------

    (
        analysis_records,
        analysis_file_count,
        unique_event_count
    ) = load_week_analysis_records(
        monday,
        sunday
    )

    log(
        f"Task 4 Files  : "
        f"{analysis_file_count}"
    )

    log(
        f"Unique Events : "
        f"{unique_event_count}"
    )

    # --------------------------------------------------------------
    # Knowledge
    # --------------------------------------------------------------

    knowledge_text = (
        load_knowledge_base()
    )

    knowledge_count = len(
        nonempty_files(
            KNOWLEDGE_DIR
        )
    )

    log(
        f"Knowledge Files : "
        f"{knowledge_count}"
    )

    # --------------------------------------------------------------
    # Graph
    # --------------------------------------------------------------

    graph_text = load_graph()

    graph_count = len(
        nonempty_files(
            GRAPH_DIR
        )
    )

    log(
        f"Graph Files     : "
        f"{graph_count}"
    )

    # --------------------------------------------------------------
    # Topics
    # --------------------------------------------------------------

    topic_text = (
        load_topic_reports()
    )

    topic_count = len(
        nonempty_files(
            TOPIC_DIR
        )
    )

    log(
        f"Topic Files     : "
        f"{topic_count}"
    )

    # --------------------------------------------------------------
    # Task 4 → Batch Summary
    # --------------------------------------------------------------

    summaries = (
        compile_task4_batches(
            year,
            week,
            analysis_records
        )
    )

    batch_summary_text = (
        build_batch_summary_text(
            summaries
        )
    )

    log("")
    log(
        f"Batch Summaries : "
        f"{len(summaries)}"
    )

    # --------------------------------------------------------------
    # FINAL AI
    # --------------------------------------------------------------

    log("")
    log(
        "============================================================"
    )

    log(
        "🧠 AI FINAL — WEEKLY SYNTHESIS"
    )

    log(
        "============================================================"
    )

    prompt = build_final_prompt(
        year,
        week,
        monday,
        sunday,
        skill,
        daily_text,
        batch_summary_text,
        knowledge_text,
        graph_text,
        topic_text
    )

    result = call_ai(
        SYSTEM_PROMPT,
        prompt,
        purpose="Weekly Final"
    )

    # --------------------------------------------------------------
    # Save
    # --------------------------------------------------------------

    save_weekly(
        output,
        result
    )

    log(
        f"✅ SAVED | {output}"
    )

    log("")
    log("#" * 72)
    log(
        "WEEKLY REPORT FINISHED"
    )
    log("#" * 72)


if __name__ == "__main__":
    main()
