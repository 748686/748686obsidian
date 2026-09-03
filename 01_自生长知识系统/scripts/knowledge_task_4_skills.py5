#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4 — Event Analysis / Skill Router
V6.5.4

======================================================================
TASK 4 职责
======================================================================

Task 4 只负责：

    Task 3 EventUnit
        ↓
    Event Type / Route 判断
        ↓
    Skill Router
        ↓
    候选 Analysis Skills
        ↓
    AI 选择 2–6 个 Skills
        ↓
    Python 严格验证
        ↓
    仅加载被选中的 Skills
        ↓
    AI 生成 Event Analysis
        ↓
    EVT-xxxx_analysis.md
        ↓
    _SKILLS_COMPLETE

本任务绝不负责：

    ❌ Event 聚类
    ❌ Global Merge
    ❌ EventUnit 创建
    ❌ ARTICLE 重新归属
    ❌ 修复 Task 3
    ❌ 内容创作
    ❌ 小红书生成
    ❌ 故事生成
    ❌ 日报生成
    ❌ 周报生成

======================================================================
LANGUAGE CONTRACT
======================================================================

语言永久锁死：

    en
    zh

只允许：

    --language en
    --language zh

以下全部非法：

    EN
    ZH
    En
    Zh

禁止：

    .lower()
    .upper()
    .casefold()

======================================================================
SKILL ROUTER CONTRACT
======================================================================

skill_routes.json V2.0：

    routes:
        新闻
        商业
        战略
        决策
        营销
        内容创作
        小红书
        故事
        汇报

Task 4 只允许：

    role == "analysis"

禁止：

    role == "output"

Skill 数量：

    selection.min_skills
    selection.max_skills

从 skill_routes.json 读取。

默认：

    2–6

但 Python 不把 2–6 作为业务规则写死。

======================================================================
OUTPUT
======================================================================

Raw News/
└── YYYY-MM-DD-EventUnit/
    └── en/
        ├── _COMPLETE
        ├── _SKILLS_COMPLETE
        └── event_units/
            ├── EVT-YYYYMMDD-000001_xxx.md
            ├── EVT-YYYYMMDD-000001_xxx_analysis.md
            └── ...

zh 同理。

======================================================================
V6.5.4 核心原则
======================================================================

不要：

    EventUnit
        ↓
    27 个 Skill 全部发送给 AI

而是：

    EventUnit
        ↓
    Route Selection
        ↓
    Analysis Candidate Skills
        ↓
    Skill Selection
        ↓
    Python Validation
        ↓
    Selected Skill Content
        ↓
    Integrated Event Analysis

======================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# ======================================================================
# COMMON
# ======================================================================

try:
    from knowledge_common import (
        RAW_NEWS,
        EVENT_UNITS_COMPLETE_FILE,
        SKILLS_COMPLETE_FILE,
        call_ai,
        event_units_dir,
        load_routes,
        load_skills,
        now,
        write_text_atomic,
    )

except ImportError:
    print("❌ Cannot import knowledge_common.py")
    raise


# ======================================================================
# CONSTANTS
# ======================================================================

VERSION = "V6.5.4"

SUPPORTED_LANGUAGES = {"en", "zh"}

ANALYSIS_ROLE = "analysis"

DEFAULT_MIN_SKILLS = 2
DEFAULT_MAX_SKILLS = 6

MAX_SKILL_SELECTION_RETRIES = 3
MAX_ANALYSIS_RETRIES = 3

GLOBAL_EVENT_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

EVENT_ID_FROM_FILENAME_PATTERN = re.compile(
    r"(EVT-\d{8}-\d{6})"
)

REQUIRED_ANALYSIS_SECTIONS = [
    "## Event Analysis",
    "## Event Information",
    "## Selected Skills",
    "## Core Facts",
    "## What Happened",
    "## Why It Matters",
    "## Cause / Mechanism",
    "## Impact",
    "## Stakeholders",
    "## Risks",
    "## Opportunities",
    "## Strategic / Business / Decision Implications",
    "## Uncertainty",
    "## Follow-up Questions",
]


# ======================================================================
# LANGUAGE
# ======================================================================

def validate_language(language: str) -> str:
    """
    严格语言验证。

    绝不进行大小写转换。
    """

    if language not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Invalid language: {language!r}. "
            "Only lowercase 'en' or 'zh' are allowed."
        )

    return language


# ======================================================================
# DATE
# ======================================================================

def validate_date(date_text: str) -> str:
    """
    严格验证 YYYY-MM-DD。
    """

    try:
        datetime.strptime(
            date_text,
            "%Y-%m-%d",
        )

    except ValueError:
        raise ValueError(
            f"Invalid date: {date_text!r}. "
            "Expected YYYY-MM-DD."
        )

    return date_text


def default_processing_dates() -> list[str]:
    """
    北京时间：

        前天
        昨天
        今天

    固定顺序：

        older → newer
    """

    current = now()

    today = current.date()

    return [
        (today - timedelta(days=2)).isoformat(),
        (today - timedelta(days=1)).isoformat(),
        today.isoformat(),
    ]


# ======================================================================
# FRONTMATTER
# ======================================================================

def parse_frontmatter(
    text: str,
) -> dict[str, str]:
    """
    解析简单 YAML frontmatter。

    只处理：

        ---
        key: value
        ---
    """

    result: dict[str, str] = {}

    if not text.startswith("---"):
        return result

    lines = text.splitlines()

    if len(lines) < 3:
        return result

    end_index: int | None = None

    for index in range(
        1,
        len(lines),
    ):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return result

    for line in lines[1:end_index]:

        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1,
        )

        key = key.strip()
        value = value.strip()

        if (
            len(value) >= 2
            and value.startswith('"')
            and value.endswith('"')
        ):
            value = value[1:-1]

        elif (
            len(value) >= 2
            and value.startswith("'")
            and value.endswith("'")
        ):
            value = value[1:-1]

        result[key] = value

    return result


# ======================================================================
# EVENT ID
# ======================================================================

def extract_event_id(
    path: Path,
    text: str,
) -> str:
    """
    优先从 frontmatter 获取 Event ID。

    如果 frontmatter 没有，
    再从文件名获取。
    """

    metadata = parse_frontmatter(text)

    event_id = metadata.get(
        "event_id",
        "",
    ).strip()

    if GLOBAL_EVENT_ID_PATTERN.fullmatch(
        event_id
    ):
        return event_id

    match = EVENT_ID_FROM_FILENAME_PATTERN.search(
        path.name
    )

    if match:
        candidate = match.group(1)

        if GLOBAL_EVENT_ID_PATTERN.fullmatch(
            candidate
        ):
            return candidate

    return ""


# ======================================================================
# EVENT TITLE
# ======================================================================

def extract_event_title(
    path: Path,
    text: str,
) -> str:
    """
    获取 Event Title。
    """

    metadata = parse_frontmatter(text)

    event_title = metadata.get(
        "event_title",
        "",
    ).strip()

    if event_title:
        return event_title

    title = metadata.get(
        "title",
        "",
    ).strip()

    if title:
        return title

    for line in text.splitlines():

        stripped = line.strip()

        if stripped.startswith("# "):
            return stripped[2:].strip()

    return path.stem


# ======================================================================
# TASK 3 COMPLETE
# ======================================================================

def task3_complete_marker(
    date: str,
    language: str,
) -> Path:

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / language
        / EVENT_UNITS_COMPLETE_FILE
    )


def require_task3_complete(
    date: str,
    language: str,
) -> None:

    marker = task3_complete_marker(
        date,
        language,
    )

    if not marker.exists():
        raise RuntimeError(
            "❌ Task 3 EventUnit is not complete.\n"
            f"DATE     : {date}\n"
            f"LANGUAGE : {language}\n"
            f"Missing  : {marker}"
        )


# ======================================================================
# EVENTUNIT DISCOVERY
# ======================================================================

def discover_event_units(
    date: str,
    language: str,
) -> list[Path]:

    directory = event_units_dir(
        date,
        language,
    )

    if not directory.exists():
        raise RuntimeError(
            "❌ EventUnit directory does not exist:\n"
            f"{directory}"
        )

    paths = sorted(
        path
        for path in directory.glob("*.md")
        if not path.name.endswith(
            "_analysis.md"
        )
    )

    return paths


# ======================================================================
# ANALYSIS PATH
# ======================================================================

def analysis_path(
    event_path: Path,
) -> Path:

    return event_path.with_name(
        event_path.stem
        + "_analysis.md"
    )


# ======================================================================
# VALIDATE EXISTING ANALYSIS
# ======================================================================

def validate_existing_analysis(
    event_path: Path,
    expected_event_id: str,
) -> bool:

    target = analysis_path(
        event_path
    )

    if not target.exists():
        return False

    try:
        text = target.read_text(
            encoding="utf-8"
        )

    except Exception:
        return False

    if not text.strip():
        return False

    metadata = parse_frontmatter(
        text
    )

    actual_event_id = metadata.get(
        "event_id",
        "",
    ).strip()

    if actual_event_id != expected_event_id:
        return False

    for section in REQUIRED_ANALYSIS_SECTIONS:

        if section not in text:
            return False

    return True


# ======================================================================
# ROUTE CONFIG
# ======================================================================

def load_route_config() -> tuple[
    dict[str, Any],
    int,
    int,
]:
    """
    读取 skill_routes.json V2.0。

    返回：

        routes
        min_skills
        max_skills
    """

    config = load_routes()

    if not isinstance(config, dict):
        raise RuntimeError(
            "❌ skill_routes.json must contain an object."
        )

    routes = config.get(
        "routes"
    )

    if not isinstance(routes, dict):
        raise RuntimeError(
            "❌ skill_routes.json missing object: routes"
        )

    selection = config.get(
        "selection",
        {},
    )

    if not isinstance(selection, dict):
        raise RuntimeError(
            "❌ skill_routes.json selection "
            "must be an object."
        )

    min_skills = selection.get(
        "min_skills",
        DEFAULT_MIN_SKILLS,
    )

    max_skills = selection.get(
        "max_skills",
        DEFAULT_MAX_SKILLS,
    )

    if (
        isinstance(min_skills, bool)
        or not isinstance(min_skills, int)
    ):
        raise RuntimeError(
            "❌ selection.min_skills "
            "must be integer."
        )

    if (
        isinstance(max_skills, bool)
        or not isinstance(max_skills, int)
    ):
        raise RuntimeError(
            "❌ selection.max_skills "
            "must be integer."
        )

    if min_skills < 1:
        raise RuntimeError(
            "❌ selection.min_skills "
            "must be >= 1."
        )

    if max_skills < min_skills:
        raise RuntimeError(
            "❌ selection.max_skills "
            "must be >= min_skills."
        )

    return (
        routes,
        min_skills,
        max_skills,
    )


# ======================================================================
# ANALYSIS ROUTES
# ======================================================================

def build_analysis_routes(
    routes: dict[str, Any],
) -> dict[str, list[str]]:
    """
    只保留 role == analysis 的路线。

    output 路线完全排除。
    """

    result: dict[str, list[str]] = {}

    for route_name, route_data in routes.items():

        if not isinstance(
            route_name,
            str,
        ):
            continue

        if not isinstance(
            route_data,
            dict,
        ):
            continue

        role = route_data.get(
            "role"
        )

        if role != ANALYSIS_ROLE:
            continue

        skills = route_data.get(
            "skills"
        )

        if not isinstance(
            skills,
            list,
        ):
            raise RuntimeError(
                f"❌ Route {route_name!r} "
                "skills must be a list."
            )

        clean_skills: list[str] = []

        for skill_name in skills:

            if not isinstance(
                skill_name,
                str,
            ):
                raise RuntimeError(
                    f"❌ Route {route_name!r} "
                    "contains non-string Skill."
                )

            skill_name = skill_name.strip()

            if not skill_name:
                continue

            if skill_name not in clean_skills:
                clean_skills.append(
                    skill_name
                )

        if not clean_skills:
            raise RuntimeError(
                f"❌ Analysis route "
                f"{route_name!r} "
                "contains no Skills."
            )

        result[route_name] = clean_skills

    if not result:
        raise RuntimeError(
            "❌ No analysis routes found."
        )

    return result


# ======================================================================
# SKILL LIBRARY
# ======================================================================

def build_skill_catalog() -> dict[str, Any]:
    """
    加载 Skills Library。

    注意：

    所有 Skill 只在 Python 内存中加载。

    不会把 27 个 Skill 全部发送给 AI。
    """

    skills = load_skills()

    if not isinstance(
        skills,
        dict,
    ):
        raise RuntimeError(
            "❌ load_skills() must return dict."
        )

    return skills


# ======================================================================
# VALIDATE ROUTE → SKILL LIBRARY
# ======================================================================

def validate_route_skill_library(
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
) -> None:

    for route_name, skill_names in (
        analysis_routes.items()
    ):

        for skill_name in skill_names:

            if skill_name not in skill_catalog:

                raise RuntimeError(
                    "❌ Skill Router references "
                    "missing Skill.\n"
                    f"Route : {route_name}\n"
                    f"Skill : {skill_name}"
                )


# ======================================================================
# CANDIDATE SKILLS
# ======================================================================

def build_candidate_skills(
    selected_routes: list[str],
    analysis_routes: dict[str, list[str]],
) -> list[str]:

    candidates: list[str] = []

    for route_name in selected_routes:

        if route_name not in analysis_routes:
            continue

        for skill_name in analysis_routes[
            route_name
        ]:

            if skill_name not in candidates:
                candidates.append(
                    skill_name
                )

    return candidates


# ======================================================================
# JSON EXTRACTION
# ======================================================================

def extract_json_object(
    text: str,
) -> dict[str, Any]:
    """
    从 AI 输出中提取 JSON object。

    支持：

        {...}

    以及：

        ```json
        {...}
        ```
    """

    text = text.strip()

    if text.startswith("```"):

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        )

        text = text.strip()

    try:

        data = json.loads(
            text
        )

        if isinstance(
            data,
            dict,
        ):
            return data

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:

        candidate = text[
            start:end + 1
        ]

        try:

            data = json.loads(
                candidate
            )

            if isinstance(
                data,
                dict,
            ):
                return data

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "AI output does not contain "
        "a valid JSON object."
    )


# ======================================================================
# ROUTER PROMPT
# ======================================================================

def build_skill_selection_prompt(
    event_id: str,
    event_title: str,
    event_text: str,
    analysis_routes: dict[str, list[str]],
    min_skills: int,
    max_skills: int,
    previous_error: str | None = None,
) -> str:

    route_catalog = json.dumps(
        analysis_routes,
        ensure_ascii=False,
        indent=2,
    )

    retry_instruction = ""

    if previous_error:

        retry_instruction = f"""

============================================================
PREVIOUS OUTPUT ERROR
============================================================

上一轮输出没有通过 Python 验证。

错误：

{previous_error}

本轮必须修正这个错误。

"""

    return f"""
你是 748686 自生长知识系统的 Skill Router。

你的任务不是写分析。

你的任务只有：

1. 判断当前 EventUnit 最适合哪些分析路线
2. 从这些路线允许的 Skills 中选择 {min_skills}–{max_skills} 个 Skill

{retry_instruction}

============================================================
EVENT
============================================================

Event ID:
{event_id}

Event Title:
{event_title}

EventUnit:
{event_text}

============================================================
AVAILABLE ANALYSIS ROUTES
============================================================

唯一允许使用的路线：

{route_catalog}

注意：

这里只包含：

role == "analysis"

任何 output 类型路线都不能选择。

============================================================
ROUTE RULES
============================================================

你可以选择：

1–3 个最相关的 analysis routes。

不要选择无关路线。

============================================================
SKILL RULES
============================================================

最终必须选择：

至少 {min_skills} 个 Skill
最多 {max_skills} 个 Skill

必须：

1. Skill 名称逐字匹配提供的 Skill
2. 不得创造 Skill
3. 不得修改 Skill 名称
4. 不得选择 output Skill
5. 不得重复 Skill
6. 所有 Skill 必须属于你选择的 routes
7. 优先选择互补的分析方法
8. 不要为了凑数量选择明显无关的 Skill

============================================================
OUTPUT
============================================================

只能输出 JSON。

严格格式：

{{
  "event_type": "新闻",
  "routes": [
    "新闻"
  ],
  "selected_skills": [
    "总结文章.md",
    "四维价值模型.md"
  ],
  "reason": "简短说明选择原因"
}}

不要输出：

Markdown
代码块
解释文字
JSON 之外的任何内容

只输出 JSON。
""".strip()


# ======================================================================
# VALIDATE SKILL SELECTION
# ======================================================================

def validate_skill_selection(
    result: dict[str, Any],
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
    min_skills: int,
    max_skills: int,
) -> tuple[
    list[str],
    list[str],
]:

    routes = result.get(
        "routes"
    )

    if not isinstance(
        routes,
        list,
    ):
        raise ValueError(
            "routes must be a list."
        )

    if not routes:
        raise ValueError(
            "routes cannot be empty."
        )

    if len(routes) > 3:
        raise ValueError(
            "Too many routes. Maximum is 3."
        )

    if len(routes) != len(set(routes)):
        raise ValueError(
            "Duplicate routes detected."
        )

    for route_name in routes:

        if not isinstance(
            route_name,
            str,
        ):
            raise ValueError(
                "route name must be string."
            )

        if route_name not in analysis_routes:
            raise ValueError(
                f"Illegal analysis route: "
                f"{route_name!r}"
            )

    selected_skills = result.get(
        "selected_skills"
    )

    if not isinstance(
        selected_skills,
        list,
    ):
        raise ValueError(
            "selected_skills must be a list."
        )

    # --------------------------------------------------------------
    # Skill 数量
    # --------------------------------------------------------------

    if len(selected_skills) < min_skills:

        raise ValueError(
            f"Too few Skills: "
            f"{len(selected_skills)}. "
            f"Minimum is {min_skills}."
        )

    if len(selected_skills) > max_skills:

        raise ValueError(
            f"Too many Skills: "
            f"{len(selected_skills)}. "
            f"Maximum is {max_skills}."
        )

    # --------------------------------------------------------------
    # Duplicate
    # --------------------------------------------------------------

    if len(selected_skills) != len(
        set(selected_skills)
    ):

        raise ValueError(
            "Duplicate Skills detected."
        )

    # --------------------------------------------------------------
    # Candidate
    # --------------------------------------------------------------

    candidates = build_candidate_skills(
        selected_routes=routes,
        analysis_routes=analysis_routes,
    )

    if len(candidates) < min_skills:

        raise ValueError(
            "Selected routes do not provide "
            "enough candidate Skills.\n"
            f"Candidates : {len(candidates)}\n"
            f"Minimum    : {min_skills}"
        )

    # --------------------------------------------------------------
    # Validate each Skill
    # --------------------------------------------------------------

    for skill_name in selected_skills:

        if not isinstance(
            skill_name,
            str,
        ):
            raise ValueError(
                "Skill name must be string."
            )

        if skill_name not in skill_catalog:

            raise ValueError(
                f"Skill does not exist "
                f"in Library: {skill_name!r}"
            )

        if skill_name not in candidates:

            raise ValueError(
                f"Skill {skill_name!r} is not allowed "
                "by the selected analysis routes."
            )

    return (
        routes,
        selected_skills,
    )


# ======================================================================
# SELECT SKILLS
# ======================================================================

def select_skills(
    event_id: str,
    event_title: str,
    event_text: str,
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
    min_skills: int,
    max_skills: int,
) -> tuple[
    list[str],
    list[str],
]:

    previous_error: str | None = None

    for attempt in range(
        1,
        MAX_SKILL_SELECTION_RETRIES + 1,
    ):

        prompt = build_skill_selection_prompt(
            event_id=event_id,
            event_title=event_title,
            event_text=event_text,
            analysis_routes=analysis_routes,
            min_skills=min_skills,
            max_skills=max_skills,
            previous_error=previous_error,
        )

        try:

            result_text = call_ai(
                prompt,
                temperature=0.1,
            )

            result = extract_json_object(
                result_text
            )

            routes, selected_skills = (
                validate_skill_selection(
                    result=result,
                    analysis_routes=analysis_routes,
                    skill_catalog=skill_catalog,
                    min_skills=min_skills,
                    max_skills=max_skills,
                )
            )

            return (
                routes,
                selected_skills,
            )

        except Exception as exc:

            previous_error = str(exc)

            print(
                f"   ⚠️ Skill Router retry "
                f"{attempt}/"
                f"{MAX_SKILL_SELECTION_RETRIES}"
            )

            print(
                f"      {exc}"
            )

            if attempt < MAX_SKILL_SELECTION_RETRIES:

                time.sleep(2)

    raise RuntimeError(
        "❌ Skill selection failed "
        "after retries.\n"
        f"Event ID : {event_id}\n"
        f"Error    : {previous_error}"
    )


# ======================================================================
# SELECTED SKILL CONTENT
# ======================================================================

def build_selected_skill_context(
    selected_skills: list[str],
    skill_catalog: dict[str, Any],
) -> str:

    blocks: list[str] = []

    for skill_name in selected_skills:

        data = skill_catalog.get(
            skill_name
        )

        if not isinstance(
            data,
            dict,
        ):
            raise RuntimeError(
                f"❌ Invalid Skill record: "
                f"{skill_name}"
            )

        content = data.get(
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
                f"❌ Selected Skill "
                f"has empty content: "
                f"{skill_name}"
            )

        blocks.append(
            "\n".join(
                [
                    "============================================================",
                    f"SKILL: {skill_name}",
                    "============================================================",
                    content,
                ]
            )
        )

    return "\n\n".join(
        blocks
    )


# ======================================================================
# ANALYSIS PROMPT
# ======================================================================

def build_analysis_prompt(
    event_id: str,
    event_title: str,
    event_text: str,
    language: str,
    selected_routes: list[str],
    selected_skills: list[str],
    selected_skill_context: str,
) -> str:

    validate_language(
        language
    )

    if language == "zh":
        output_language = "简体中文"

    elif language == "en":
        output_language = "English"

    else:
        raise ValueError(
            f"Invalid language: {language!r}"
        )

    routes_text = ", ".join(
        selected_routes
    )

    skills_text = ", ".join(
        selected_skills
    )

    return f"""
你是 748686 自生长知识系统的 Event Analysis AI。

你现在负责分析一个已经由：

    Task 1 Cluster
    Task 2 Global Merge
    Task 3 EventUnit

完成处理的事件。

你不能重新聚类。

你不能修改 Event ID。

你不能重新分配 ARTICLE。

你只负责对当前 EventUnit 进行深度分析。

============================================================
EVENT
============================================================

Event ID:
{event_id}

Event Title:
{event_title}

Language:
{language}

============================================================
SELECTED ROUTES
============================================================

{routes_text}

============================================================
SELECTED SKILLS
============================================================

{skills_text}

============================================================
SELECTED SKILL CONTENT
============================================================

{selected_skill_context}

============================================================
ORIGINAL EVENTUNIT
============================================================

{event_text}

============================================================
LANGUAGE
============================================================

最终分析语言：

{output_language}

============================================================
ANALYSIS RULES
============================================================

必须：

1. 只分析当前 EventUnit
2. 不编造事实
3. 不增加原 EventUnit 中不存在的确定性事实
4. 明确区分事实、推断和不确定性
5. 真正使用 Selected Skills
6. 不机械解释 Skill
7. 将多个 Skill 综合为一个完整分析
8. 强调事件为什么重要
9. 分析原因和机制
10. 分析影响
11. 分析利益相关者
12. 分析风险
13. 分析机会
14. 分析战略、商业或决策含义
15. 明确不确定信息
16. 提出值得继续追踪的问题

禁止：

1. 内容创作
2. 小红书文案
3. 故事
4. 日报
5. 周报
6. 广告文案
7. 与当前 Event 无关的扩展

============================================================
OUTPUT STRUCTURE
============================================================

必须严格包含：

## Event Analysis

## Event Information

## Selected Skills

## Core Facts

## What Happened

## Why It Matters

## Cause / Mechanism

## Impact

## Stakeholders

## Risks

## Opportunities

## Strategic / Business / Decision Implications

## Uncertainty

## Follow-up Questions

============================================================
SELECTED SKILLS SECTION
============================================================

必须在：

## Selected Skills

中明确列出：

{skills_text}

只能列出本次实际选择的 Skills。

不要增加其他 Skill。

============================================================
QUALITY
============================================================

分析应该：

- 事实准确
- 逻辑清晰
- 有因果关系
- 有机制解释
- 有影响分析
- 有风险分析
- 有机会分析
- 有战略 / 商业 / 决策含义
- 有不确定性
- 有后续问题
- 避免空泛
- 避免机械套模型
- 避免简单重复 EventUnit

直接输出 Markdown。

不要输出代码块。

不要输出 JSON。

不要输出额外说明。
""".strip()


# ======================================================================
# GENERATE ANALYSIS
# ======================================================================

def generate_analysis(
    event_id: str,
    event_title: str,
    event_text: str,
    language: str,
    selected_routes: list[str],
    selected_skills: list[str],
    skill_catalog: dict[str, Any],
) -> str:

    selected_skill_context = (
        build_selected_skill_context(
            selected_skills=selected_skills,
            skill_catalog=skill_catalog,
        )
    )

    prompt = build_analysis_prompt(
        event_id=event_id,
        event_title=event_title,
        event_text=event_text,
        language=language,
        selected_routes=selected_routes,
        selected_skills=selected_skills,
        selected_skill_context=selected_skill_context,
    )

    last_error: Exception | None = None

    for attempt in range(
        1,
        MAX_ANALYSIS_RETRIES + 1,
    ):

        try:

            result = call_ai(
                prompt,
                temperature=0.2,
            )

            result = result.strip()

            if not result:

                raise ValueError(
                    "AI returned empty analysis."
                )

            if len(result) < 100:

                raise ValueError(
                    "AI analysis is "
                    "suspiciously short."
                )

            return result

        except Exception as exc:

            last_error = exc

            print(
                f"   ⚠️ Analysis retry "
                f"{attempt}/"
                f"{MAX_ANALYSIS_RETRIES}: "
                f"{exc}"
            )

            if attempt < MAX_ANALYSIS_RETRIES:

                time.sleep(2)

    raise RuntimeError(
        "❌ Event Analysis generation "
        "failed after retries.\n"
        f"Event ID : {event_id}\n"
        f"Error    : {last_error}"
    )


# ======================================================================
# WRAP ANALYSIS
# ======================================================================

def escape_yaml_value(
    value: str,
) -> str:

    return value.replace(
        '"',
        '\\"',
    )


def wrap_analysis(
    event_id: str,
    event_title: str,
    date: str,
    language: str,
    selected_routes: list[str],
    selected_skills: list[str],
    analysis: str,
) -> str:

    validate_language(
        language
    )

    generated_at = now().isoformat()

    routes_text = ", ".join(
        selected_routes
    )

    skills_text = ", ".join(
        selected_skills
    )

    safe_title = escape_yaml_value(
        event_title
    )

    return f"""---
event_id: "{event_id}"
event_title: "{safe_title}"
date: "{date}"
language: "{language}"
task: "Knowledge Task 4 — Event Analysis"
version: "{VERSION}"
generated_at: "{generated_at}"
---

# {event_title}

## Event Analysis

**Event ID:** `{event_id}`

**Analysis Routes:** {routes_text}

**Selected Skills:** {skills_text}

{analysis}
""".strip() + "\n"


# ======================================================================
# VALIDATE GENERATED ANALYSIS
# ======================================================================

def validate_generated_analysis(
    text: str,
    event_id: str,
    selected_skills: list[str],
) -> None:

    if not text.strip():

        raise RuntimeError(
            "Generated analysis is empty."
        )

    metadata = parse_frontmatter(
        text
    )

    actual_event_id = metadata.get(
        "event_id",
        "",
    ).strip()

    if actual_event_id != event_id:

        raise RuntimeError(
            "Generated analysis Event ID mismatch.\n"
            f"Expected: {event_id}\n"
            f"Actual  : {actual_event_id}"
        )

    for section in REQUIRED_ANALYSIS_SECTIONS:

        if section not in text:

            raise RuntimeError(
                "Generated analysis missing section:\n"
                f"{section}"
            )

    # --------------------------------------------------------------
    # Selected Skill 记录验证
    # --------------------------------------------------------------

    selected_section_match = re.search(
        r"## Selected Skills\s*\n(.*?)(?=\n## |\Z)",
        text,
        flags=re.DOTALL,
    )

    if selected_section_match is None:

        raise RuntimeError(
            "Generated analysis missing "
            "Selected Skills content."
        )

    selected_section = (
        selected_section_match.group(1)
    )

    for skill_name in selected_skills:

        if skill_name not in selected_section:

            raise RuntimeError(
                "Generated analysis Selected Skills "
                "section missing Skill:\n"
                f"{skill_name}"
            )


# ======================================================================
# SKILLS COMPLETE MARKER
# ======================================================================

def skills_complete_marker(
    date: str,
    language: str,
) -> Path:

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / language
        / SKILLS_COMPLETE_FILE
    )


def remove_stale_complete_marker(
    date: str,
    language: str,
) -> None:

    marker = skills_complete_marker(
        date,
        language,
    )

    if marker.exists():

        marker.unlink()

        print(
            f"   🧹 Removed stale marker | "
            f"{marker}"
        )


def write_skills_complete(
    date: str,
    language: str,
    expected_count: int,
    actual_count: int,
) -> None:

    marker = skills_complete_marker(
        date,
        language,
    )

    payload = {
        "task": "Knowledge Task 4 — Event Analysis",
        "version": VERSION,
        "date": date,
        "language": language,
        "expected_event_units": expected_count,
        "actual_analysis_files": actual_count,
        "status": "COMPLETE",
        "completed_at": now().isoformat(),
    }

    write_text_atomic(
        marker,
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ) + "\n",
    )


# ======================================================================
# ANALYSIS SCAN
# ======================================================================

def scan_analysis_files(
    event_paths: list[Path],
) -> dict[str, Path]:

    result: dict[str, Path] = {}

    for event_path in event_paths:

        target = analysis_path(
            event_path
        )

        if not target.exists():
            continue

        try:

            text = target.read_text(
                encoding="utf-8"
            )

        except Exception:
            continue

        metadata = parse_frontmatter(
            text
        )

        event_id = metadata.get(
            "event_id",
            "",
        ).strip()

        if not event_id:
            continue

        if event_id in result:

            raise RuntimeError(
                "❌ Duplicate analysis Event ID detected:\n"
                f"{event_id}"
            )

        result[event_id] = target

    return result


# ======================================================================
# PROCESS ONE EVENT
# ======================================================================

def process_event(
    event_path: Path,
    date: str,
    language: str,
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
    min_skills: int,
    max_skills: int,
) -> str:

    text = event_path.read_text(
        encoding="utf-8"
    ).strip()

    if not text:

        raise RuntimeError(
            "❌ EventUnit is empty:\n"
            f"{event_path}"
        )

    event_id = extract_event_id(
        path=event_path,
        text=text,
    )

    if not event_id:

        raise RuntimeError(
            "❌ Invalid Event ID:\n"
            f"{event_path}"
        )

    if not GLOBAL_EVENT_ID_PATTERN.fullmatch(
        event_id
    ):

        raise RuntimeError(
            "❌ Invalid Global Event ID:\n"
            f"{event_id}"
        )

    event_title = extract_event_title(
        path=event_path,
        text=text,
    )

    target = analysis_path(
        event_path
    )

    # --------------------------------------------------------------
    # 已有合法分析
    # --------------------------------------------------------------

    if validate_existing_analysis(
        event_path=event_path,
        expected_event_id=event_id,
    ):

        print(
            f"   ⏭️ EXISTS | {event_id}"
        )

        return "existing"

    # --------------------------------------------------------------
    # 已有非法分析
    # --------------------------------------------------------------

    if target.exists():

        print(
            f"   ♻️ REGENERATE INVALID | "
            f"{event_id}"
        )

    # --------------------------------------------------------------
    # Router
    # --------------------------------------------------------------

    print(
        f"   🧭 ROUTING | {event_id}"
    )

    selected_routes, selected_skills = (
        select_skills(
            event_id=event_id,
            event_title=event_title,
            event_text=text,
            analysis_routes=analysis_routes,
            skill_catalog=skill_catalog,
            min_skills=min_skills,
            max_skills=max_skills,
        )
    )

    print(
        "   🧠 ROUTES  | "
        + ", ".join(
            selected_routes
        )
    )

    print(
        "   🧩 SKILLS  | "
        + ", ".join(
            selected_skills
        )
    )

    # --------------------------------------------------------------
    # Analysis
    # --------------------------------------------------------------

    print(
        f"   🔨 ANALYSIS | {event_id}"
    )

    analysis = generate_analysis(
        event_id=event_id,
        event_title=event_title,
        event_text=text,
        language=language,
        selected_routes=selected_routes,
        selected_skills=selected_skills,
        skill_catalog=skill_catalog,
    )

    wrapped = wrap_analysis(
        event_id=event_id,
        event_title=event_title,
        date=date,
        language=language,
        selected_routes=selected_routes,
        selected_skills=selected_skills,
        analysis=analysis,
    )

    validate_generated_analysis(
        text=wrapped,
        event_id=event_id,
        selected_skills=selected_skills,
    )

    write_text_atomic(
        target,
        wrapped,
    )

    print(
        f"   ✅ SAVED | {target}"
    )

    return "generated"


# ======================================================================
# FINAL VALIDATION
# ======================================================================

def final_validate_unit(
    date: str,
    language: str,
    event_paths: list[Path],
) -> int:

    expected_count = len(
        event_paths
    )

    actual_count = 0

    event_ids: set[str] = set()

    for event_path in event_paths:

        event_text = event_path.read_text(
            encoding="utf-8"
        )

        event_id = extract_event_id(
            path=event_path,
            text=event_text,
        )

        if not event_id:

            raise RuntimeError(
                "❌ EventUnit has no valid Event ID:\n"
                f"{event_path}"
            )

        if event_id in event_ids:

            raise RuntimeError(
                "❌ Duplicate Event ID in EventUnits:\n"
                f"{event_id}"
            )

        event_ids.add(
            event_id
        )

        target = analysis_path(
            event_path
        )

        if not target.exists():

            raise RuntimeError(
                "❌ Task 4 incomplete. "
                "Missing analysis:\n"
                f"Event ID : {event_id}\n"
                f"Path     : {target}"
            )

        if not validate_existing_analysis(
            event_path=event_path,
            expected_event_id=event_id,
        ):

            raise RuntimeError(
                "❌ Task 4 analysis validation failed:\n"
                f"Event ID : {event_id}\n"
                f"Path     : {target}"
            )

        actual_count += 1

    if actual_count != expected_count:

        raise RuntimeError(
            "❌ Task 4 coverage failure.\n"
            f"Expected : {expected_count}\n"
            f"Actual   : {actual_count}"
        )

    return actual_count


# ======================================================================
# PROCESS ONE DATE × LANGUAGE UNIT
# ======================================================================

def process_unit(
    date: str,
    language: str,
) -> None:

    validate_date(
        date
    )

    validate_language(
        language
    )

    print()
    print("=" * 70)
    print("KNOWLEDGE TASK 4 — EVENT ANALYSIS")
    print("=" * 70)
    print(
        f"DATE     : {date}"
    )
    print(
        f"LANGUAGE : {language}"
    )
    print(
        f"VERSION  : {VERSION}"
    )
    print("=" * 70)

    # --------------------------------------------------------------
    # Task 3 必须完成
    # --------------------------------------------------------------

    require_task3_complete(
        date=date,
        language=language,
    )

    # --------------------------------------------------------------
    # Router Config
    # --------------------------------------------------------------

    (
        routes,
        min_skills,
        max_skills,
    ) = load_route_config()

    analysis_routes = build_analysis_routes(
        routes
    )

    # --------------------------------------------------------------
    # Skill Library
    # --------------------------------------------------------------

    skill_catalog = build_skill_catalog()

    validate_route_skill_library(
        analysis_routes=analysis_routes,
        skill_catalog=skill_catalog,
    )

    print(
        f"Analysis Routes : "
        f"{len(analysis_routes)}"
    )

    print(
        f"Skill Range     : "
        f"{min_skills}–{max_skills}"
    )

    print(
        f"Skill Library   : "
        f"{len(skill_catalog)}"
    )

    # --------------------------------------------------------------
    # EventUnits
    # --------------------------------------------------------------

    event_paths = discover_event_units(
        date=date,
        language=language,
    )

    expected_count = len(
        event_paths
    )

    if expected_count == 0:

        raise RuntimeError(
            "❌ No EventUnit files found."
        )

    print(
        f"EventUnits      : "
        f"{expected_count}"
    )

    # --------------------------------------------------------------
    # 删除旧 Complete Marker
    # --------------------------------------------------------------

    remove_stale_complete_marker(
        date=date,
        language=language,
    )

    # --------------------------------------------------------------
    # Existing
    # --------------------------------------------------------------

    existing = scan_analysis_files(
        event_paths
    )

    print(
        f"Existing analysis candidates : "
        f"{len(existing)}"
    )

    # --------------------------------------------------------------
    # Sequential processing
    # --------------------------------------------------------------

    generated = 0
    preserved = 0

    for index, event_path in enumerate(
        event_paths,
        start=1,
    ):

        print()
        print(
            f"[{index}/{expected_count}] "
            "PROCESSING EVENTUNIT"
        )

        result = process_event(
            event_path=event_path,
            date=date,
            language=language,
            analysis_routes=analysis_routes,
            skill_catalog=skill_catalog,
            min_skills=min_skills,
            max_skills=max_skills,
        )

        if result == "generated":
            generated += 1

        elif result == "existing":
            preserved += 1

    # --------------------------------------------------------------
    # Final validation
    # --------------------------------------------------------------

    actual_count = final_validate_unit(
        date=date,
        language=language,
        event_paths=event_paths,
    )

    # --------------------------------------------------------------
    # Complete
    # --------------------------------------------------------------

    write_skills_complete(
        date=date,
        language=language,
        expected_count=expected_count,
        actual_count=actual_count,
    )

    print()
    print("=" * 70)
    print("TASK 4 COMPLETE")
    print("=" * 70)
    print(
        f"DATE              : {date}"
    )
    print(
        f"LANGUAGE          : {language}"
    )
    print(
        f"EVENTUNITS        : {expected_count}"
    )
    print(
        f"GENERATED         : {generated}"
    )
    print(
        f"PRESERVED         : {preserved}"
    )
    print(
        f"ANALYSIS          : {actual_count}"
    )
    print(
        f"SKILL RANGE       : "
        f"{min_skills}–{max_skills}"
    )
    print(
        f"COMPLETE MARKER   : "
        f"{skills_complete_marker(date, language)}"
    )
    print("=" * 70)


# ======================================================================
# SIX PROCESSING UNITS
# ======================================================================

def process_all_units() -> None:

    dates = default_processing_dates()

    units = [
        (dates[0], "en"),
        (dates[0], "zh"),
        (dates[1], "en"),
        (dates[1], "zh"),
        (dates[2], "en"),
        (dates[2], "zh"),
    ]

    print()
    print("#" * 70)
    print("KNOWLEDGE TASK 4 — SIX PROCESSING UNITS")
    print("#" * 70)

    for index, (
        date,
        language,
    ) in enumerate(
        units,
        start=1,
    ):

        print()
        print(
            f"PROCESSING UNIT "
            f"{index} / {len(units)}"
        )

        print(
            f"DATE     : {date}"
        )

        print(
            f"LANGUAGE : {language}"
        )

        process_unit(
            date=date,
            language=language,
        )

    print()
    print("#" * 70)
    print(
        "KNOWLEDGE TASK 4 — "
        "ALL SIX UNITS COMPLETE"
    )
    print("#" * 70)


# ======================================================================
# CLI
# ======================================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 4 "
            "— Event Analysis / Skill Router"
        )
    )

    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help=(
            "Process one date only. "
            "Format: YYYY-MM-DD"
        ),
    )

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help=(
            "Process one language only. "
            "Only exact lowercase "
            "'en' or 'zh'."
        ),
    )

    return parser


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    # --------------------------------------------------------------
    # Manual single unit
    # --------------------------------------------------------------

    if (
        args.date is not None
        or args.language is not None
    ):

        if args.date is None:

            raise ValueError(
                "When using --language, "
                "--date is also required."
            )

        if args.language is None:

            raise ValueError(
                "When using --date, "
                "--language is also required."
            )

        date = validate_date(
            args.date
        )

        language = validate_language(
            args.language
        )

        process_unit(
            date=date,
            language=language,
        )

        return

    # --------------------------------------------------------------
    # Normal six-unit mode
    # --------------------------------------------------------------

    process_all_units()


# ======================================================================
# ENTRY
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print(
            "❌ Interrupted by user."
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print("=" * 70)
        print("KNOWLEDGE TASK 4 FAILED")
        print("=" * 70)
        print(
            str(exc)
        )
        print("=" * 70)

        sys.exit(1)
