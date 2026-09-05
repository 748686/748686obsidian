#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Daily V3.0

======================================================================
职责
======================================================================

读取指定日期的全部 Task 4 Analysis，
让 AI 调取：

    Skills/05.汇报写作/日报编写助手.md

并严格按照该 Skill 的要求生成日报。

======================================================================
数据流
======================================================================

Raw News
    ↓
Task 3 EventUnit
    ↓
Task 4 Analysis
    ↓
knowledge_daily.py
    ↓
AI 调取「日报编写助手」
    ↓
05_日报/YYYY/MM/YYYY-MM-DD.md


======================================================================
重要原则
======================================================================

1. 日报格式由 Skill 决定。
2. Python 不硬编码日报章节结构。
3. AI 必须读取日报 Skill。
4. Skill 不存在或为空 → 直接失败。
5. 当天全部 Analysis 一次性提供给 AI。
6. en / zh 同一个 EVT-ID 视为同一个事件。
7. 不编造没有证据的内容。
8. 不修改 Task 4。
9. 使用 Asia/Shanghai。
10. 处理顺序：前天 → 昨天 → 今天。
11. 已存在非空日报则跳过。
12. 原子写入。
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
    / "日报编写助手.md"
)

DAILY_DIR = ROOT / "05_日报"

TIMEZONE = ZoneInfo("Asia/Shanghai")


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
        "KNOWLEDGE_DAILY_TIMEOUT",
        "180"
    )
)

AI_RETRIES = int(
    os.getenv(
        "KNOWLEDGE_DAILY_RETRIES",
        "3"
    )
)

AI_THROTTLE = float(
    os.getenv(
        "KNOWLEDGE_DAILY_THROTTLE",
        "1.2"
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

def read_text(path: Path) -> str:

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


# ======================================================================
# DATE
# ======================================================================

def today() -> datetime:

    return datetime.now(
        TIMEZONE
    )


def target_dates():

    current = today().date()

    return [
        (
            current
            - timedelta(days=2)
        ).strftime("%Y-%m-%d"),

        (
            current
            - timedelta(days=1)
        ).strftime("%Y-%m-%d"),

        current.strftime("%Y-%m-%d"),
    ]


# ======================================================================
# SKILL
# ======================================================================

def load_daily_skill() -> str:

    if not SKILL_FILE.exists():

        raise RuntimeError(
            "日报 Skill 不存在：\n"
            f"{SKILL_FILE}"
        )

    content = read_text(
        SKILL_FILE
    ).strip()

    if not content:

        raise RuntimeError(
            "日报 Skill 文件为空：\n"
            f"{SKILL_FILE}"
        )

    return content


# ======================================================================
# TASK 4
# ======================================================================

def analysis_directory(
    date_str: str,
    language: str
) -> Path:

    return (
        RAW_NEWS
        / f"{date_str}-EventUnit"
        / language
        / "event_units"
    )


def event_id_from_file(
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


def find_analysis_files(
    date_str: str
):

    files = []

    # 严格使用小写 en / zh
    for language in (
        "en",
        "zh"
    ):

        directory = analysis_directory(
            date_str,
            language
        )

        if not directory.exists():
            continue

        files.extend(
            sorted(
                directory.glob(
                    "*_analysis.md"
                )
            )
        )

    return [
        p
        for p in files
        if p.is_file()
        and p.stat().st_size > 0
    ]


def load_all_analysis(
    files
) -> str:

    chunks = []

    seen_events = set()

    for path in files:

        event_id = (
            event_id_from_file(path)
        )

        language = (
            "en"
            if (
                "/en/"
                in path.as_posix()
            )
            else "zh"
        )

        content = read_text(
            path
        ).strip()

        if not content:
            continue

        duplicate_note = ""

        if event_id in seen_events:

            duplicate_note = (
                "\n"
                "NOTE: This EVT-ID has "
                "already appeared in another "
                "language. Treat it as the "
                "same event and do not "
                "double-count it.\n"
            )

        else:

            seen_events.add(
                event_id
            )

        chunks.append(
            "\n".join([
                "=" * 70,
                f"EVENT_ID: {event_id}",
                f"LANGUAGE: {language}",
                f"FILE: {path.relative_to(ROOT)}",
                duplicate_note,
                "=" * 70,
                content,
            ])
        )

    return "\n\n".join(
        chunks
    )


# ======================================================================
# OPTIONAL ORIGINAL EVENTUNIT
# ======================================================================

def find_eventunit_for_analysis(
    analysis_path: Path
) -> Path | None:

    name = analysis_path.name

    if not name.endswith(
        "_analysis.md"
    ):
        return None

    original_name = name[
        :-len("_analysis.md")
    ] + ".md"

    candidate = (
        analysis_path.parent
        / original_name
    )

    if (
        candidate.exists()
        and candidate.stat().st_size > 0
    ):
        return candidate

    return None


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

    req_headers = {
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
                headers=req_headers,
                method="POST"
            )

            with request.urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as response:

                response_data = (
                    response
                    .read()
                    .decode("utf-8")
                )

            result = json.loads(
                response_data
            )

            content = (
                result
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
你是 748686 自生长知识系统的日报编写执行器。

你必须严格执行用户提供的：

「Skills/05.汇报写作/日报编写助手.md」

该 Skill 是本次日报生成的正式规范。

重要：

1. 必须先完整阅读并理解日报 Skill。
2. 日报的结构、栏目、格式、表达方式、排序方式，
   全部以 Skill 为准。
3. 不得自行发明另一套日报模板。
4. 不得因为你习惯某种格式而改变 Skill。
5. 数据来源只允许使用本次提供的数据。
6. 不得编造事实。
7. 同一个 EVT-ID 的 en / zh Analysis 是同一个事件。
8. 不得因为双语文件而重复计算同一个事件。
9. 如果数据不足，按照 Skill 中规定的方法处理。
10. 最终只输出日报正文。
11. 不要输出“以下是日报”之类的解释。
12. 不要输出 markdown code fence。
"""


def build_prompt(
    date_str: str,
    skill: str,
    analysis_text: str
) -> str:

    return f"""
当前日报日期：

{date_str}

============================================================
日报编写 Skill
============================================================

{skill}

============================================================
当天全部 Task 4 Analysis
============================================================

{analysis_text}

============================================================

现在执行日报编写任务。

要求：

- 严格按照日报编写 Skill；
- 综合当天全部 Task 4 Analysis；
- 对同一个 EVT-ID 的中英文 Analysis 去重；
- 不遗漏重要事件；
- 不虚构信息；
- 不添加 Skill 没有要求的栏目；
- 最终只返回可以直接保存为 Markdown 文件的日报正文。
"""


# ======================================================================
# OUTPUT
# ======================================================================

def daily_output_path(
    date_str: str
) -> Path:

    year, month, _ = (
        date_str.split("-")
    )

    return (
        DAILY_DIR
        / year
        / month
        / f"{date_str}.md"
    )


def save_daily(
    path: Path,
    content: str
) -> None:

    content = content.strip()

    if not content:

        raise RuntimeError(
            "AI 生成的日报为空"
        )

    atomic_write(
        path,
        content + "\n"
    )

    if (
        not path.exists()
        or path.stat().st_size <= 0
    ):

        raise RuntimeError(
            f"日报保存失败：{path}"
        )


# ======================================================================
# PROCESS DATE
# ======================================================================

def process_date(
    date_str: str,
    skill: str
) -> None:

    log("")
    log("=" * 72)
    log(
        f"DAILY REPORT | {date_str}"
    )
    log("=" * 72)

    output = daily_output_path(
        date_str
    )

    if (
        output.exists()
        and output.stat().st_size > 0
    ):

        log(
            f"⏭️ SKIP | "
            f"日报已存在：{output}"
        )

        return

    files = find_analysis_files(
        date_str
    )

    log(
        f"Task 4 Analysis : "
        f"{len(files)}"
    )

    if not files:

        log(
            "⚠️ 没有 Task 4 Analysis"
        )

        log(
            "本日不生成日报。"
        )

        return

    unique_events = set()

    for path in files:

        unique_events.add(
            event_id_from_file(path)
        )

    log(
        f"Unique Events   : "
        f"{len(unique_events)}"
    )

    analysis_text = (
        load_all_analysis(files)
    )

    if not analysis_text.strip():

        raise RuntimeError(
            f"{date_str} Analysis 内容为空"
        )

    log(
        "🧠 AI 调取："
        "Skills/05.汇报写作/日报编写助手.md"
    )

    prompt = build_prompt(
        date_str,
        skill,
        analysis_text
    )

    result = call_ai(
        SYSTEM_PROMPT,
        prompt
    )

    save_daily(
        output,
        result
    )

    log(
        f"✅ SAVED | {output}"
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
        "KNOWLEDGE DAILY V3.0"
    )
    log("#" * 72)

    if not AGNES_API_KEY:

        raise RuntimeError(
            "未设置 AGNES_API_KEY"
        )

    log(
        f"ROOT : {ROOT}"
    )

    log(
        f"DATE : {today().strftime('%Y-%m-%d')}"
    )

    # --------------------------------------------------------------
    # Skill 必须存在
    # --------------------------------------------------------------

    skill = load_daily_skill()

    log(
        "✅ 日报 Skill 已加载"
    )

    log(
        f"   {SKILL_FILE}"
    )

    # --------------------------------------------------------------
    # 前天 → 昨天 → 今天
    # --------------------------------------------------------------

    for date_str in target_dates():

        process_date(
            date_str,
            skill
        )

        time.sleep(
            AI_THROTTLE
        )

    log("")
    log("#" * 72)
    log(
        "KNOWLEDGE DAILY FINISHED"
    )
    log("#" * 72)


if __name__ == "__main__":
    main()
