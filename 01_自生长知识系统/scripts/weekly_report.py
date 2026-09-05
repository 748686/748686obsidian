#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Weekly Report V3.0

======================================================================
职责
======================================================================

让 AI 调取：

    Skills/05.汇报写作/周报编写助手.md

然后基于：

    本周日报
    +
    本周 Task 4 Analysis
    +
    08_知识库
    +
    09_知识图谱
    +
    07_专题报告

严格按照「周报编写助手」要求生成周报。

======================================================================
重要原则
======================================================================

1. 周报格式完全由 Skill 决定。
2. Python 不硬编码周报章节。
3. AI 必须读取周报 Skill。
4. Skill 不存在或为空 → 直接失败。
5. 日报不是唯一数据来源。
6. 周报是独立的周级知识编译。
7. 使用真实 ISO 周。
8. 使用 Asia/Shanghai。
9. 不修改 Task 4。
10. 不写 00_System 知识成果。
"""

from __future__ import annotations

import os
import re
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib import request


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
        "1.5"
    )
)


# ======================================================================
# LOG
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


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

    tmp.replace(path)


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

        result.append(path)

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


def current_week():

    current = now_local().date()

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
        + timedelta(days=6)
    )

    return (
        iso_year,
        iso_week,
        monday,
        sunday
    )


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


def load_week_analysis(
    monday,
    sunday
):

    chunks = []

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

            eid = event_id(path)

            if eid in seen_events:
                duplicate = (
                    "\nNOTE: Duplicate language "
                    "version of the same EVT-ID. "
                    "Do not double-count.\n"
                )
            else:
                seen_events.add(eid)
                duplicate = ""

            language = (
                "en"
                if "/en/"
                in path.as_posix()
                else "zh"
            )

            content = read_text(
                path
            ).strip()

            if not content:
                continue

            chunks.append(
                "\n".join([
                    "=" * 70,
                    f"DATE: {date_str}",
                    f"EVENT_ID: {eid}",
                    f"LANGUAGE: {language}",
                    f"FILE: {path.relative_to(ROOT)}",
                    duplicate,
                    "=" * 70,
                    content,
                ])
            )

        current += timedelta(
            days=1
        )

    return (
        "\n\n".join(chunks),
        file_count,
        len(seen_events)
    )


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

        chunks.append(block)

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

        chunks.append(block)

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

        chunks.append(block)

        total += len(block)

    return "\n".join(
        chunks
    )


# ======================================================================
# AI
# ======================================================================

def call_ai(
    system_prompt: str,
    user_prompt: str
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
    }

    last_error = None

    for attempt in range(
        1,
        AI_RETRIES + 1
    ):

        try:

            if attempt > 1:

                time.sleep(
                    AI_THROTTLE
                    * attempt
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
                    .decode("utf-8")
                )

            data = json.loads(
                raw
            )

            content = (
                data
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content.strip():

                raise RuntimeError(
                    "AI 返回为空"
                )

            return content.strip()

        except Exception as exc:

            last_error = exc

            log(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

    raise RuntimeError(
        f"AI 请求失败：{last_error}"
    )


# ======================================================================
# PROMPT
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
8. 同一个 EVT-ID 的 en / zh Analysis 只能计算一次。
9. 如果资料之间存在不确定性，应按 Skill 的要求处理。
10. 最终只输出可以直接保存的 Markdown 周报正文。
11. 不要输出解释。
12. 不要输出 markdown code fence。
"""


def build_prompt(
    year: int,
    week: int,
    monday,
    sunday,
    skill: str,
    daily_text: str,
    analysis_text: str,
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
本周全部 Task 4 Analysis
============================================================

{analysis_text or "本周没有可用 Task 4 Analysis。"}

============================================================
当前长期知识库
============================================================

{knowledge_text or "当前没有可用知识库内容。"}

============================================================
当前知识图谱
============================================================

{graph_text or "当前没有可用知识图谱内容。"}

============================================================
近期专题报告
============================================================

{topic_text or "当前没有可用专题报告。"}

============================================================

现在开始编写本周周报。

严格执行「周报编写助手」中的全部要求。

特别注意：

- 周报不是日报简单拼接；
- 必须进行周级综合；
- 必须利用已有长期知识判断本周变化；
- 必须区分新事实、已有知识和新的判断；
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

    log("")
    log("#" * 72)
    log(
        "748686 自生长知识系统"
    )
    log(
        "WEEKLY REPORT V3.0"
    )
    log("#" * 72)

    if not AGNES_API_KEY:

        raise RuntimeError(
            "未设置 AGNES_API_KEY"
        )

    year, week, monday, sunday = (
        current_week()
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

    for date_str, path, content in (
        daily_reports
    ):

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
        analysis_text,
        analysis_file_count,
        unique_event_count
    ) = load_week_analysis(
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
    # AI
    # --------------------------------------------------------------

    log(
        "🧠 AI 调取："
        "Skills/05.汇报写作/周报编写助手.md"
    )

    prompt = build_prompt(
        year,
        week,
        monday,
        sunday,
        skill,
        daily_text,
        analysis_text,
        knowledge_text,
        graph_text,
        topic_text
    )

    result = call_ai(
        SYSTEM_PROMPT,
        prompt
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
