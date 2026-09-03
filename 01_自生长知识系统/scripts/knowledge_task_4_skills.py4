#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4 — Event Analysis
V6.5.3

============================================================
TASK 4 — 三日检查 / 补全 / 断点续跑
============================================================

职责
====

    1. 自动检查：
           今天
           昨天
           前天

    2. 每一天严格按照：

           en
           zh

       的顺序处理。

    3. 读取 Task 3 生成的 EventUnit：

           Raw News/
           YYYY-MM-DD-EventUnit/
               en/
                   event_units/
                       EVT-xxxx.md
               zh/
                   event_units/
                       EVT-xxxx.md

    4. 每一个 EventUnit 必须对应一个：

           EVT-xxxx_analysis.md

    5. 如果已经全部生成并验证通过：

           → SKIP

    6. 如果只生成一部分：

           → 保留已有文件
           → 只生成缺失文件

    7. 如果一个都没有：

           → 生成全部分析文件

    8. 最终必须验证：

           Task 3 _COMPLETE
           EventUnit 数量
           Analysis 数量
           Event ID 一一对应
           Analysis 文件非空
           _SKILLS_COMPLETE
           expected count = actual count

    9. Task 4 不负责修复 Task 3。

============================================================
LANGUAGE CONTRACT
============================================================

永久锁死：

    en
    zh

只允许：

    en
    zh

禁止：

    EN
    ZH
    En
    Zh
    eN
    zH

禁止任何大小写自动转换。

绝对不要：

    .lower()
    .upper()
    .casefold()

语言验证必须是严格字符串匹配。

============================================================
PROCESS ORDER
============================================================

今天、昨天、前天：

    Date 1 / en
    Date 1 / zh

    Date 2 / en
    Date 2 / zh

    Date 3 / en
    Date 3 / zh

例如今天是 2026-09-03：

    2026-09-01 / en
    2026-09-01 / zh

    2026-09-02 / en
    2026-09-02 / zh

    2026-09-03 / en
    2026-09-03 / zh

============================================================
OUTPUT
============================================================

原始 EventUnit：

    EVT-20260903-000001_xxx.md

分析文件：

    EVT-20260903-000001_xxx_analysis.md

两者位于同一个：

    event_units/

目录。

============================================================
"""

from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ==========================================================
# Common
# ==========================================================

try:
    from knowledge_common import (
        ROOT,
        SYSTEM,
        SKILLS,
        RAW_NEWS,
        ROUTES_FILE,
        EVENT_UNITS_COMPLETE_FILE,
        SKILLS_COMPLETE_FILE,
        event_units_dir,
        load_saved_event_units,
        load_skills,
        load_routes,
        call_ai,
        now,
        safe_name,
        write_text_atomic,
    )
except ImportError as exc:
    print("=" * 70)
    print("ERROR: cannot import knowledge_common")
    print("=" * 70)
    print(exc)
    sys.exit(1)


# ==========================================================
# Constants
# ==========================================================

VERSION = "V6.5.3"

ALLOWED_LANGUAGES = {"en", "zh"}

ANALYSIS_SUFFIX = "_analysis.md"

GLOBAL_EVENT_ID_RE = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

FRONTMATTER_EVENT_ID_RE = re.compile(
    r"^event_id:\s*(.+?)\s*$",
    re.MULTILINE,
)

FRONTMATTER_TITLE_RE = re.compile(
    r"^event_title:\s*(.+?)\s*$",
    re.MULTILINE,
)

MAX_RETRY = 3

RETRY_SLEEP_SECONDS = 5


# ==========================================================
# Language Contract
# ==========================================================

def validate_language(language: str) -> str:
    """
    严格语言验证。

    注意：
    绝对不进行 lower / upper / casefold。
    """

    if language not in ALLOWED_LANGUAGES:
        raise ValueError(
            f"Invalid language: {language!r}. "
            "Only lowercase 'en' or 'zh' are allowed."
        )

    return language


# ==========================================================
# Date
# ==========================================================

def today_date() -> str:
    """
    使用 common.now() 获取系统时间。

    common.now() 已经负责系统时间。
    """

    current = now()

    if isinstance(current, datetime):
        dt = current
    else:
        dt = datetime.now()

    return dt.strftime("%Y-%m-%d")


def three_days() -> List[str]:
    """
    今天、昨天、前天。

    返回顺序：

        前天
        昨天
        今天

    这样可以让旧数据优先完成，
    然后逐步推进到今天。
    """

    current = datetime.strptime(
        today_date(),
        "%Y-%m-%d",
    )

    return [
        (current - timedelta(days=2)).strftime("%Y-%m-%d"),
        (current - timedelta(days=1)).strftime("%Y-%m-%d"),
        current.strftime("%Y-%m-%d"),
    ]


# ==========================================================
# Paths
# ==========================================================

def get_event_units_dir(
    date: str,
    language: str,
) -> Path:

    validate_language(language)

    return event_units_dir(
        date,
        language,
    )


def get_task3_complete_path(
    date: str,
    language: str,
) -> Path:

    return (
        get_event_units_dir(
            date,
            language,
        ).parent
        / EVENT_UNITS_COMPLETE_FILE
    )


def get_task4_complete_path(
    date: str,
    language: str,
) -> Path:

    return (
        get_event_units_dir(
            date,
            language,
        ).parent
        / SKILLS_COMPLETE_FILE
    )


# ==========================================================
# Completion Marker
# ==========================================================

def marker_is_valid(path: Path) -> bool:

    if not path.exists():
        return False

    if not path.is_file():
        return False

    try:
        text = path.read_text(
            encoding="utf-8"
        ).strip()
    except Exception:
        return False

    return bool(text)


# ==========================================================
# Event ID
# ==========================================================

def extract_event_id(
    metadata: Dict,
    path: Path,
) -> Optional[str]:

    event_id = metadata.get("event_id")

    if event_id is None:
        try:
            text = path.read_text(
                encoding="utf-8"
            )
        except Exception:
            return None

        match = FRONTMATTER_EVENT_ID_RE.search(
            text
        )

        if match:
            event_id = match.group(1).strip()

    if not event_id:
        return None

    if not GLOBAL_EVENT_ID_RE.fullmatch(
        str(event_id)
    ):
        return None

    return str(event_id)


# ==========================================================
# Event Title
# ==========================================================

def extract_event_title(
    metadata: Dict,
    path: Path,
) -> str:

    title = metadata.get("event_title")

    if title:
        return str(title).strip()

    try:
        text = path.read_text(
            encoding="utf-8"
        )
    except Exception:
        return path.stem

    match = FRONTMATTER_TITLE_RE.search(
        text
    )

    if match:
        return match.group(1).strip()

    return path.stem


# ==========================================================
# Load EventUnits
# ==========================================================

def load_event_units_strict(
    date: str,
    language: str,
) -> List[Tuple[Dict, Path]]:

    validate_language(language)

    directory = get_event_units_dir(
        date,
        language,
    )

    if not directory.exists():
        raise RuntimeError(
            f"EventUnit directory does not exist: "
            f"{directory}"
        )

    if not directory.is_dir():
        raise RuntimeError(
            f"EventUnit path is not a directory: "
            f"{directory}"
        )

    try:
        units = load_saved_event_units(
            date,
            language,
        )
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load Task 3 EventUnits "
            f"for {date}/{language}: {exc}"
        ) from exc

    if not units:
        raise RuntimeError(
            f"No EventUnits found for "
            f"{date}/{language}"
        )

    validated = []

    seen_ids = set()

    for metadata, path in units:

        if not isinstance(metadata, dict):
            raise RuntimeError(
                f"Malformed EventUnit metadata: "
                f"{path}"
            )

        path = Path(path)

        if not path.exists():
            raise RuntimeError(
                f"EventUnit file does not exist: "
                f"{path}"
            )

        if not path.is_file():
            raise RuntimeError(
                f"EventUnit path is not a file: "
                f"{path}"
            )

        try:
            text = path.read_text(
                encoding="utf-8"
            ).strip()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot read EventUnit: "
                f"{path}: {exc}"
            ) from exc

        if not text:
            raise RuntimeError(
                f"Empty EventUnit: {path}"
            )

        event_id = extract_event_id(
            metadata,
            path,
        )

        if not event_id:
            raise RuntimeError(
                f"Invalid or missing Event ID: "
                f"{path}"
            )

        if event_id in seen_ids:
            raise RuntimeError(
                f"Duplicate Event ID: "
                f"{event_id}"
            )

        seen_ids.add(event_id)

        metadata = dict(metadata)

        metadata["event_id"] = event_id
        metadata["event_title"] = (
            extract_event_title(
                metadata,
                path,
            )
        )

        metadata["date"] = date
        metadata["language"] = language

        validated.append(
            (
                metadata,
                path,
            )
        )

    validated.sort(
        key=lambda item: item[0]["event_id"]
    )

    return validated


# ==========================================================
# Task 3 Completion Validation
# ==========================================================

def validate_task3_complete(
    date: str,
    language: str,
) -> None:

    validate_language(language)

    complete_path = get_task3_complete_path(
        date,
        language,
    )

    if not marker_is_valid(
        complete_path
    ):
        raise RuntimeError(
            "Task 3 is NOT complete.\n"
            f"Missing or empty marker:\n"
            f"{complete_path}"
        )

    # 重新加载并验证全部 EventUnit
    units = load_event_units_strict(
        date,
        language,
    )

    if not units:
        raise RuntimeError(
            f"Task 3 COMPLETE exists but "
            f"EventUnits are empty: "
            f"{date}/{language}"
        )


# ==========================================================
# Analysis Path
# ==========================================================

def analysis_path(
    event_path: Path,
) -> Path:

    return event_path.with_name(
        event_path.stem + ANALYSIS_SUFFIX
    )


# ==========================================================
# Existing Analysis Validation
# ==========================================================

def analysis_file_is_valid(
    path: Path,
    expected_event_id: str,
) -> bool:

    if not path.exists():
        return False

    if not path.is_file():
        return False

    try:
        text = path.read_text(
            encoding="utf-8"
        ).strip()
    except Exception:
        return False

    if not text:
        return False

    match = FRONTMATTER_EVENT_ID_RE.search(
        text
    )

    if not match:
        return False

    actual_event_id = match.group(1).strip()

    if actual_event_id != expected_event_id:
        return False

    return True


# ==========================================================
# Existing Analysis Scan
# ==========================================================

def scan_analysis_files(
    units: List[Tuple[Dict, Path]],
) -> Dict[str, Path]:

    existing = {}

    for metadata, event_path in units:

        event_id = metadata["event_id"]

        target = analysis_path(
            event_path
        )

        if analysis_file_is_valid(
            target,
            event_id,
        ):
            existing[event_id] = target

    return existing


# ==========================================================
# Skill Catalog
# ==========================================================

def build_skill_catalog(
    skills: Dict,
) -> str:

    lines = []

    for name in sorted(skills.keys()):

        item = skills[name]

        content = item.get(
            "content",
            "",
        )

        content = str(content).strip()

        lines.append(
            f"### Skill: {name}\n"
        )

        if content:
            lines.append(
                content
            )
        else:
            lines.append(
                "(Skill content unavailable)"
            )

        lines.append("\n")

    return "\n".join(lines)


# ==========================================================
# Route Catalog
# ==========================================================

def build_route_catalog(
    routes: Dict,
) -> str:

    lines = []

    for category in sorted(
        routes.keys()
    ):

        values = routes[category]

        if not isinstance(
            values,
            list,
        ):
            continue

        lines.append(
            f"- {category}:"
        )

        for skill in values:

            lines.append(
                f"  - {skill}"
            )

    return "\n".join(lines)


# ==========================================================
# AI Prompt
# ==========================================================

def build_analysis_prompt(
    metadata: Dict,
    event_text: str,
    skill_catalog: str,
    route_catalog: str,
) -> str:

    event_id = metadata["event_id"]
    event_title = metadata.get(
        "event_title",
        event_id,
    )

    date = metadata["date"]
    language = metadata["language"]

    return f"""
你现在是 748686 自生长知识系统的 Task 4 Event Analysis。

============================================================
SYSTEM
============================================================

Task:
    Event Analysis

Version:
    {VERSION}

Event ID:
    {event_id}

Event Title:
    {event_title}

Date:
    {date}

Language:
    {language}

============================================================
IMPORTANT LANGUAGE CONTRACT
============================================================

系统语言字段永久锁死为：

    en
    zh

当前语言：

    {language}

不要修改 language。
不要输出 EN。
不要输出 ZH。
不要进行大小写转换。

============================================================
YOUR TASK
============================================================

你将收到一个完整的 Task 3 EventUnit。

你的工作：

    1. 理解整个事件。
    2. 从 Skills Library 中选择真正适用于该事件的 Skills。
    3. 不要机械地执行全部 Skills。
    4. 不要为了数量而选择 Skill。
    5. 选择最有价值的分析方法。
    6. 使用这些 Skills 对事件进行综合分析。
    7. 最终输出一个完整的 Markdown 分析文件。

原则：

    EventUnit = 事实输入
    Skill = 分析方法
    Analysis = 综合结果

============================================================
FACTUAL DISCIPLINE
============================================================

绝对不能：

    - 编造事实
    - 编造人物
    - 编造公司
    - 编造数字
    - 编造时间
    - 编造因果关系
    - 把推测写成事实

必须明确区分：

    已知事实
    分析判断
    不确定性
    后续需要确认的信息

如果资料不足：

    明确写出“信息不足”或“不确定”。

============================================================
SKILL ROUTES
============================================================

下面是系统提供的候选路由。

它们只是候选提示。

最终是否使用某个 Skill，
必须由你根据 EventUnit 判断。

不要机械执行全部 Skill。

{route_catalog}

============================================================
SKILL LIBRARY
============================================================

{skill_catalog}

============================================================
EVENTUNIT
============================================================

{event_text}

============================================================
OUTPUT REQUIREMENTS
============================================================

只输出完整 Markdown。

不要输出：

    ```markdown
    ```

不要解释你正在做什么。

输出必须包含以下部分：

# Event Analysis

## Event Information

包含：

    Event ID
    Event Title
    Date
    Language

## Selected Skills

列出真正使用的 Skills。

说明：

    为什么选择这些 Skill。

## Core Facts

只写 EventUnit 能够支持的核心事实。

## What Happened

清楚说明事件发生了什么。

## Why It Matters

解释事件的重要性。

## Cause / Mechanism

分析：

    为什么发生
    如何发生
    主要机制是什么

如果无法确定，必须说明不确定。

## Impact

分析：

    短期影响
    中期影响
    长期潜在影响

区分事实与推断。

## Stakeholders

分析主要相关方。

## Risks

分析风险。

## Opportunities

分析机会。

## Strategic / Business / Decision Implications

分析：

    战略意义
    商业意义
    决策意义

不适用的部分可以明确说明“不适用”。

## Uncertainty

明确列出：

    哪些信息已经确认
    哪些信息尚未确认
    哪些判断属于推测

## Follow-up Questions

列出值得继续追踪的问题。

============================================================
FINAL RULE
============================================================

这是一个事件分析文件。

不是新闻摘要。

不是重新写一篇新闻。

不是虚构评论。

必须以 EventUnit 为事实基础，
再使用适当 Skills 进行分析。

现在开始。
""".strip()


# ==========================================================
# AI Call With Retry
# ==========================================================

def generate_analysis(
    metadata: Dict,
    event_path: Path,
    skill_catalog: str,
    route_catalog: str,
) -> str:

    try:
        event_text = event_path.read_text(
            encoding="utf-8"
        )
    except Exception as exc:
        raise RuntimeError(
            f"Cannot read EventUnit: "
            f"{event_path}: {exc}"
        ) from exc

    if not event_text.strip():
        raise RuntimeError(
            f"Empty EventUnit: "
            f"{event_path}"
        )

    prompt = build_analysis_prompt(
        metadata=metadata,
        event_text=event_text,
        skill_catalog=skill_catalog,
        route_catalog=route_catalog,
    )

    last_error = None

    for attempt in range(
        1,
        MAX_RETRY + 1,
    ):

        try:

            result = call_ai(
                prompt,
                temperature=0.2,
            )

            if result is None:
                raise RuntimeError(
                    "AI returned None"
                )

            result = str(result).strip()

            if not result:
                raise RuntimeError(
                    "AI returned empty output"
                )

            return result

        except Exception as exc:

            last_error = exc

            print(
                f"      AI attempt "
                f"{attempt}/{MAX_RETRY} failed: "
                f"{exc}"
            )

            if attempt < MAX_RETRY:
                time.sleep(
                    RETRY_SLEEP_SECONDS
                )

    raise RuntimeError(
        f"AI generation failed after "
        f"{MAX_RETRY} attempts: "
        f"{last_error}"
    )


# ==========================================================
# Analysis Front Matter
# ==========================================================

def wrap_analysis(
    metadata: Dict,
    ai_content: str,
) -> str:

    event_id = metadata["event_id"]

    event_title = str(
        metadata.get(
            "event_title",
            event_id,
        )
    ).replace(
        "\n",
        " ",
    ).strip()

    date = metadata["date"]

    language = validate_language(
        metadata["language"]
    )

    generated_at = now()

    if isinstance(
        generated_at,
        datetime,
    ):
        generated_at_text = (
            generated_at.isoformat()
        )
    else:
        generated_at_text = str(
            generated_at
        )

    return (
        "---\n"
        f"event_id: {event_id}\n"
        f"event_title: {event_title}\n"
        f"date: {date}\n"
        f"language: {language}\n"
        "task: Event Analysis\n"
        f"version: {VERSION}\n"
        f"generated_at: {generated_at_text}\n"
        "---\n\n"
        f"{ai_content.strip()}\n"
    )


# ==========================================================
# Generate One Missing Analysis
# ==========================================================

def generate_one(
    metadata: Dict,
    event_path: Path,
    skill_catalog: str,
    route_catalog: str,
) -> Path:

    event_id = metadata["event_id"]

    target = analysis_path(
        event_path
    )

    print(
        f"      GENERATE "
        f"{event_id}"
    )

    ai_content = generate_analysis(
        metadata=metadata,
        event_path=event_path,
        skill_catalog=skill_catalog,
        route_catalog=route_catalog,
    )

    output = wrap_analysis(
        metadata=metadata,
        ai_content=ai_content,
    )

    if not output.strip():
        raise RuntimeError(
            f"Generated analysis is empty: "
            f"{event_id}"
        )

    write_text_atomic(
        target,
        output,
    )

    if not analysis_file_is_valid(
        target,
        event_id,
    ):
        raise RuntimeError(
            f"Generated analysis failed "
            f"validation: {target}"
        )

    return target


# ==========================================================
# Final Task 4 Validation
# ==========================================================

def validate_task4_complete(
    date: str,
    language: str,
    units: List[Tuple[Dict, Path]],
) -> Tuple[int, int]:

    validate_language(language)

    # ------------------------------------------------------
    # 1. Task 3 COMPLETE
    # ------------------------------------------------------

    task3_complete = (
        get_task3_complete_path(
            date,
            language,
        )
    )

    if not marker_is_valid(
        task3_complete
    ):
        raise RuntimeError(
            f"Task 3 COMPLETE missing: "
            f"{task3_complete}"
        )

    # ------------------------------------------------------
    # 2. EventUnit validation
    # ------------------------------------------------------

    if not units:
        raise RuntimeError(
            f"No EventUnits: "
            f"{date}/{language}"
        )

    expected_ids = []

    for metadata, path in units:

        event_id = metadata["event_id"]

        if not GLOBAL_EVENT_ID_RE.fullmatch(
            event_id
        ):
            raise RuntimeError(
                f"Invalid Event ID: "
                f"{event_id}"
            )

        if not path.exists():
            raise RuntimeError(
                f"EventUnit missing: "
                f"{path}"
            )

        expected_ids.append(
            event_id
        )

    expected_ids = sorted(
        set(expected_ids)
    )

    # ------------------------------------------------------
    # 3. Scan Analysis
    # ------------------------------------------------------

    existing = scan_analysis_files(
        units
    )

    actual_ids = sorted(
        existing.keys()
    )

    # ------------------------------------------------------
    # 4. Count
    # ------------------------------------------------------

    expected_count = len(
        expected_ids
    )

    actual_count = len(
        actual_ids
    )

    if actual_count != expected_count:

        missing = sorted(
            set(expected_ids)
            - set(actual_ids)
        )

        extra = sorted(
            set(actual_ids)
            - set(expected_ids)
        )

        raise RuntimeError(
            "Task 4 validation failed.\n"
            f"Expected: {expected_count}\n"
            f"Actual:   {actual_count}\n"
            f"Missing:  {len(missing)}\n"
            f"Extra:    {len(extra)}"
        )

    # ------------------------------------------------------
    # 5. Exact Event ID Match
    # ------------------------------------------------------

    if actual_ids != expected_ids:

        missing = sorted(
            set(expected_ids)
            - set(actual_ids)
        )

        extra = sorted(
            set(actual_ids)
            - set(expected_ids)
        )

        raise RuntimeError(
            "Event ID mismatch.\n"
            f"Missing: {missing}\n"
            f"Extra:   {extra}"
        )

    # ------------------------------------------------------
    # 6. Every analysis non-empty
    # ------------------------------------------------------

    for event_id, path in existing.items():

        try:
            text = path.read_text(
                encoding="utf-8"
            ).strip()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot read analysis: "
                f"{path}: {exc}"
            ) from exc

        if not text:
            raise RuntimeError(
                f"Empty analysis: "
                f"{path}"
            )

        if event_id not in text:
            raise RuntimeError(
                f"Analysis does not contain "
                f"expected Event ID: "
                f"{event_id}"
            )

    # ------------------------------------------------------
    # 7. _SKILLS_COMPLETE
    # ------------------------------------------------------

    skills_complete = (
        get_task4_complete_path(
            date,
            language,
        )
    )

    if not marker_is_valid(
        skills_complete
    ):
        raise RuntimeError(
            f"_SKILLS_COMPLETE missing or empty: "
            f"{skills_complete}"
        )

    # ------------------------------------------------------
    # 8. Marker count validation
    # ------------------------------------------------------

    try:
        marker_text = skills_complete.read_text(
            encoding="utf-8"
        ).strip()
    except Exception as exc:
        raise RuntimeError(
            f"Cannot read _SKILLS_COMPLETE: "
            f"{skills_complete}: {exc}"
        ) from exc

    expected_text = (
        f"expected_count: {expected_count}"
    )

    actual_text = (
        f"actual_count: {actual_count}"
    )

    if expected_text not in marker_text:
        raise RuntimeError(
            f"_SKILLS_COMPLETE expected count "
            f"does not match: "
            f"{skills_complete}"
        )

    if actual_text not in marker_text:
        raise RuntimeError(
            f"_SKILLS_COMPLETE actual count "
            f"does not match: "
            f"{skills_complete}"
        )

    return (
        expected_count,
        actual_count,
    )


# ==========================================================
# Write Completion Marker
# ==========================================================

def write_task4_complete(
    date: str,
    language: str,
    expected_count: int,
    actual_count: int,
) -> None:

    validate_language(language)

    path = get_task4_complete_path(
        date,
        language,
    )

    generated_at = now()

    if isinstance(
        generated_at,
        datetime,
    ):
        generated_at = (
            generated_at.isoformat()
        )

    text = (
        "TASK 4 COMPLETE\n"
        f"date: {date}\n"
        f"language: {language}\n"
        f"expected_count: {expected_count}\n"
        f"actual_count: {actual_count}\n"
        f"generated_at: {generated_at}\n"
        f"version: {VERSION}\n"
    )

    write_text_atomic(
        path,
        text,
    )


# ==========================================================
# Remove Stale Completion Marker
# ==========================================================

def remove_stale_task4_marker(
    date: str,
    language: str,
) -> None:

    path = get_task4_complete_path(
        date,
        language,
    )

    if path.exists():

        try:
            path.unlink()

            print(
                f"  Removed stale "
                f"_SKILLS_COMPLETE"
            )

        except Exception as exc:

            raise RuntimeError(
                f"Cannot remove stale "
                f"_SKILLS_COMPLETE: "
                f"{path}: {exc}"
            ) from exc


# ==========================================================
# Process One Date + Language
# ==========================================================

def process_date_language(
    date: str,
    language: str,
    skill_catalog: str,
    route_catalog: str,
) -> None:

    validate_language(language)

    print()
    print("=" * 70)
    print(
        f"DATE     : {date}"
    )
    print(
        f"LANGUAGE : {language}"
    )
    print("=" * 70)

    # ------------------------------------------------------
    # Task 3 must already be complete
    # ------------------------------------------------------

    print()
    print(
        "Checking Task 3..."
    )

    validate_task3_complete(
        date,
        language,
    )

    print(
        "Task 3 COMPLETE ✓"
    )

    # ------------------------------------------------------
    # Load EventUnits
    # ------------------------------------------------------

    units = load_event_units_strict(
        date,
        language,
    )

    expected_count = len(
        units
    )

    print(
        f"EventUnits : {expected_count}"
    )

    # ------------------------------------------------------
    # Scan current analyses
    # ------------------------------------------------------

    existing = scan_analysis_files(
        units
    )

    actual_count = len(
        existing
    )

    print(
        f"Analyses   : {actual_count}"
    )

    # ------------------------------------------------------
    # Already complete?
    # ------------------------------------------------------

    task4_marker = (
        get_task4_complete_path(
            date,
            language,
        )
    )

    if (
        actual_count == expected_count
        and marker_is_valid(task4_marker)
    ):

        try:

            validate_task4_complete(
                date,
                language,
                units,
            )

            print()
            print(
                "Task 4 COMPLETE ✓"
            )
            print(
                "→ SKIP"
            )

            return

        except Exception as exc:

            print()
            print(
                "Existing completion marker "
                "failed validation."
            )

            print(
                f"Reason: {exc}"
            )

            remove_stale_task4_marker(
                date,
                language,
            )

    # ------------------------------------------------------
    # Incomplete
    # ------------------------------------------------------

    remove_stale_task4_marker(
        date,
        language,
    )

    expected_ids = {
        metadata["event_id"]
        for metadata, _ in units
    }

    existing_ids = set(
        existing.keys()
    )

    missing_ids = (
        expected_ids
        - existing_ids
    )

    # ------------------------------------------------------
    # Nothing missing
    # ------------------------------------------------------

    if not missing_ids:

        print()
        print(
            "All analysis files exist."
        )

        print(
            "Running final validation..."
        )

        validate_task4_complete(
            date,
            language,
            units,
        )

        print(
            "Task 4 COMPLETE ✓"
        )

        return

    # ------------------------------------------------------
    # Recovery
    # ------------------------------------------------------

    print()
    print(
        f"Missing : {len(missing_ids)}"
    )

    if actual_count == 0:

        print(
            "→ GENERATE ALL"
        )

    else:

        print(
            f"→ RECOVER {len(missing_ids)}"
        )

    print()

    # ------------------------------------------------------
    # Generate in EventUnit order
    # ------------------------------------------------------

    for index, (
        metadata,
        event_path,
    ) in enumerate(
        units,
        start=1,
    ):

        event_id = metadata[
            "event_id"
        ]

        if event_id not in missing_ids:
            continue

        print(
            f"[{index}/{expected_count}] "
            f"{event_id}"
        )

        generate_one(
            metadata=metadata,
            event_path=event_path,
            skill_catalog=skill_catalog,
            route_catalog=route_catalog,
        )

    # ------------------------------------------------------
    # Final validation
    # ------------------------------------------------------

    print()
    print(
        "Final Task 4 validation..."
    )

    expected_count, actual_count = (
        validate_task4_complete_without_marker(
            date,
            language,
            units,
        )
    )

    # ------------------------------------------------------
    # Only after validation passes,
    # create _SKILLS_COMPLETE
    # ------------------------------------------------------

    write_task4_complete(
        date=date,
        language=language,
        expected_count=expected_count,
        actual_count=actual_count,
    )

    # ------------------------------------------------------
    # Validate marker itself
    # ------------------------------------------------------

    validate_task4_complete(
        date,
        language,
        units,
    )

    print()
    print(
        f"Task 4 COMPLETE ✓ "
        f"{actual_count}/{expected_count}"
    )


# ==========================================================
# Validation Before Completion Marker
# ==========================================================

def validate_task4_complete_without_marker(
    date: str,
    language: str,
    units: List[Tuple[Dict, Path]],
) -> Tuple[int, int]:

    validate_language(language)

    # Task 3
    task3_complete = (
        get_task3_complete_path(
            date,
            language,
        )
    )

    if not marker_is_valid(
        task3_complete
    ):
        raise RuntimeError(
            f"Task 3 COMPLETE missing: "
            f"{task3_complete}"
        )

    # EventUnits
    if not units:
        raise RuntimeError(
            f"No EventUnits: "
            f"{date}/{language}"
        )

    expected_ids = []

    for metadata, path in units:

        event_id = metadata[
            "event_id"
        ]

        if not GLOBAL_EVENT_ID_RE.fullmatch(
            event_id
        ):
            raise RuntimeError(
                f"Invalid Event ID: "
                f"{event_id}"
            )

        expected_ids.append(
            event_id
        )

        target = analysis_path(
            path
        )

        if not analysis_file_is_valid(
            target,
            event_id,
        ):
            raise RuntimeError(
                f"Missing or invalid analysis: "
                f"{target}"
            )

    expected_ids = sorted(
        expected_ids
    )

    existing_ids = []

    for metadata, path in units:

        event_id = metadata[
            "event_id"
        ]

        target = analysis_path(
            path
        )

        existing_ids.append(
            event_id
        )

        try:
            text = target.read_text(
                encoding="utf-8"
            ).strip()
        except Exception as exc:
            raise RuntimeError(
                f"Cannot read analysis: "
                f"{target}: {exc}"
            ) from exc

        if not text:
            raise RuntimeError(
                f"Empty analysis: "
                f"{target}"
            )

    existing_ids = sorted(
        existing_ids
    )

    if existing_ids != expected_ids:
        raise RuntimeError(
            "Analysis Event ID mismatch."
        )

    expected_count = len(
        expected_ids
    )

    actual_count = len(
        existing_ids
    )

    if actual_count != expected_count:
        raise RuntimeError(
            f"Analysis count mismatch: "
            f"{actual_count}/{expected_count}"
        )

    return (
        expected_count,
        actual_count,
    )


# ==========================================================
# Three-Day Runner
# ==========================================================

def run_three_days() -> None:

    print()
    print("#" * 70)
    print(
        "KNOWLEDGE TASK 4"
    )
    print(
        "THREE-DAY EVENT ANALYSIS CHECK"
    )
    print(
        VERSION
    )
    print("#" * 70)

    dates = three_days()

    print()
    print(
        "Checking dates:"
    )

    for date in dates:
        print(
            f"  {date}"
        )

    print()
    print(
        "Fixed language order:"
    )
    print(
        "  en"
    )
    print(
        "  zh"
    )

    # ------------------------------------------------------
    # Load Skills once
    # ------------------------------------------------------

    print()
    print(
        "Loading Skills..."
    )

    try:
        skills = load_skills()
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load Skills: {exc}"
        ) from exc

    if not skills:
        raise RuntimeError(
            "Skills library is empty."
        )

    print(
        f"Skills loaded: {len(skills)}"
    )

    # ------------------------------------------------------
    # Load routes once
    # ------------------------------------------------------

    print()
    print(
        "Loading Skill Routes..."
    )

    try:
        routes = load_routes()
    except Exception as exc:
        raise RuntimeError(
            f"Failed to load skill routes: "
            f"{exc}"
        ) from exc

    if not routes:
        print(
            "WARNING: Skill routes are empty."
        )

    skill_catalog = build_skill_catalog(
        skills
    )

    route_catalog = build_route_catalog(
        routes
    )

    # ------------------------------------------------------
    # Six processing units
    # ------------------------------------------------------

    total_units = len(
        dates
    ) * 2

    completed_units = 0

    for date in dates:

        # ==================================================
        # EN
        # ==================================================

        process_date_language(
            date=date,
            language="en",
            skill_catalog=skill_catalog,
            route_catalog=route_catalog,
        )

        completed_units += 1

        # ==================================================
        # ZH
        # ==================================================

        process_date_language(
            date=date,
            language="zh",
            skill_catalog=skill_catalog,
            route_catalog=route_catalog,
        )

        completed_units += 1

    # ------------------------------------------------------
    # Final
    # ------------------------------------------------------

    print()
    print("#" * 70)
    print(
        "TASK 4 THREE-DAY SUCCESS"
    )
    print(
        f"{completed_units}/{total_units} "
        "date-language units complete"
    )
    print("#" * 70)


# ==========================================================
# Optional Manual Single Date
# ==========================================================

def run_manual(
    date: str,
    language: str,
) -> None:

    validate_language(
        language
    )

    skills = load_skills()

    routes = load_routes()

    skill_catalog = build_skill_catalog(
        skills
    )

    route_catalog = build_route_catalog(
        routes
    )

    process_date_language(
        date=date,
        language=language,
        skill_catalog=skill_catalog,
        route_catalog=route_catalog,
    )


# ==========================================================
# CLI
# ==========================================================

def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Knowledge Task 4 — "
            "Three-Day Event Analysis"
        )
    )

    parser.add_argument(
        "--date",
        required=False,
        help=(
            "Manual single-date recovery. "
            "If omitted, automatically checks "
            "today, yesterday and the day before."
        ),
    )

    parser.add_argument(
        "--language",
        required=False,
        help=(
            "Manual language. "
            "ONLY exact lowercase 'en' or 'zh'."
        ),
    )

    args = parser.parse_args()

    try:

        # --------------------------------------------------
        # Normal pipeline mode
        # --------------------------------------------------

        if (
            args.date is None
            and args.language is None
        ):

            run_three_days()

            return

        # --------------------------------------------------
        # Manual mode requires both
        # --------------------------------------------------

        if (
            args.date is None
            or args.language is None
        ):

            raise ValueError(
                "Manual mode requires BOTH "
                "--date and --language."
            )

        # --------------------------------------------------
        # Strict language
        # --------------------------------------------------

        validate_language(
            args.language
        )

        # --------------------------------------------------
        # Strict date
        # --------------------------------------------------

        try:
            datetime.strptime(
                args.date,
                "%Y-%m-%d",
            )
        except ValueError:
            raise ValueError(
                f"Invalid date: "
                f"{args.date!r}. "
                "Expected YYYY-MM-DD."
            )

        run_manual(
            date=args.date,
            language=args.language,
        )

    except KeyboardInterrupt:

        print()
        print(
            "Interrupted."
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print("=" * 70)
        print(
            "TASK 4 FAILED"
        )
        print("=" * 70)
        print(
            str(exc)
        )
        print()
        print(
            "Completed files have been preserved."
        )
        print(
            "The next run can resume from the "
            "missing EventUnit analyses."
        )
        print("=" * 70)

        sys.exit(1)


# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":
    main()
