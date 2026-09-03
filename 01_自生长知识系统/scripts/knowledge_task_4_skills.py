#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4 — Event Analysis / Skill Router
V6.5.4

======================================================================
TASK 4 职责
======================================================================

本任务只负责：

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
    ❌ 日报 / 周报生成

======================================================================
LANGUAGE CONTRACT
======================================================================

语言永久锁死：

    en
    zh

只允许：

    --language en
    --language zh

禁止：

    EN
    ZH
    En
    Zh

禁止任何：

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

    role:
        analysis
        output

Task 4 只允许：

    role == "analysis"

禁止使用：

    role == "output"

Skill 数量：

    min_skills = 2
    max_skills = 6

该数量从 skill_routes.json 读取。
不在 Python 中硬编码业务规则。

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

======================================================================
V6.5.4 核心原则
======================================================================

    EventUnit
        ↓
    Route Selection
        ↓
    Candidate Skills
        ↓
    Skill Selection
        ↓
    Validation
        ↓
    Selected Skill Content
        ↓
    Integrated Analysis

而不是：

    EventUnit
        ↓
    27 个 Skill 全部发送给 AI
        ↓
    AI 自己乱选

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
        ROUTES_FILE,
        SKILLS,
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

GLOBAL_EVENT_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

LOCAL_EVENT_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}"
)

DEFAULT_MIN_SKILLS = 2
DEFAULT_MAX_SKILLS = 6

MAX_SKILL_SELECTION_RETRIES = 3
MAX_ANALYSIS_RETRIES = 3

ANALYSIS_ROLE = "analysis"

COMPLETE_FILE = EVENT_UNITS_COMPLETE_FILE
SKILLS_COMPLETE_FILE = SKILLS_COMPLETE_FILE


# ======================================================================
# LANGUAGE
# ======================================================================

def validate_language(language: str) -> str:
    """
    严格验证语言。

    禁止大小写转换。
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
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(
            f"Invalid date: {date_text!r}. "
            "Expected YYYY-MM-DD."
        )

    return date_text


def default_processing_dates() -> list[str]:
    """
    根据北京时间 now() 自动得到：

        前天
        昨天
        今天

    顺序固定：
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
# MARKDOWN FRONTMATTER
# ======================================================================

def parse_frontmatter(text: str) -> dict[str, str]:
    """
    读取简单 YAML frontmatter。

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

    end_index = None

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end_index = index
            break

    if end_index is None:
        return result

    for line in lines[1:end_index]:
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip()

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]

        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]

        result[key] = value

    return result


# ======================================================================
# EVENT ID
# ======================================================================

def extract_event_id(path: Path, text: str) -> str:
    """
    从 frontmatter 或文件名中读取 Event ID。
    """

    metadata = parse_frontmatter(text)

    event_id = metadata.get("event_id", "").strip()

    if event_id and GLOBAL_EVENT_ID_PATTERN.fullmatch(event_id):
        return event_id

    match = LOCAL_EVENT_ID_PATTERN.search(path.name)

    if match:
        candidate = match.group(0)

        if GLOBAL_EVENT_ID_PATTERN.fullmatch(candidate):
            return candidate

    return ""


# ======================================================================
# EVENT TITLE
# ======================================================================

def extract_event_title(path: Path, text: str) -> str:
    """
    优先读取 frontmatter event_title。
    """

    metadata = parse_frontmatter(text)

    title = metadata.get("event_title", "").strip()

    if title:
        return title

    title = metadata.get("title", "").strip()

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
        / COMPLETE_FILE
    )


def require_task3_complete(
    date: str,
    language: str,
) -> None:

    marker = task3_complete_marker(date, language)

    if not marker.exists():
        raise RuntimeError(
            "❌ Task 3 EventUnit is not complete.\n"
            f"DATE     : {date}\n"
            f"LANGUAGE : {language}\n"
            f"Missing  : {marker}\n"
        )


# ======================================================================
# EVENTUNIT DISCOVERY
# ======================================================================

def discover_event_units(
    date: str,
    language: str,
) -> list[Path]:

    directory = event_units_dir(date, language)

    if not directory.exists():
        raise RuntimeError(
            "❌ EventUnit directory does not exist:\n"
            f"{directory}"
        )

    paths = sorted(
        path
        for path in directory.glob("*.md")
        if not path.name.endswith("_analysis.md")
    )

    return paths


# ======================================================================
# ANALYSIS PATH
# ======================================================================

def analysis_path(event_path: Path) -> Path:
    """
    EventUnit：

        EVT-xxx_title.md

    Analysis：

        EVT-xxx_title_analysis.md
    """

    return event_path.with_name(
        event_path.stem + "_analysis.md"
    )


# ======================================================================
# VALID EXISTING ANALYSIS
# ======================================================================

def validate_existing_analysis(
    event_path: Path,
    expected_event_id: str,
) -> bool:

    target = analysis_path(event_path)

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

    metadata = parse_frontmatter(text)

    actual_event_id = metadata.get(
        "event_id",
        "",
    ).strip()

    if actual_event_id != expected_event_id:
        return False

    required_sections = [
        "## Event Analysis",
        "## Core Facts",
        "## What Happened",
        "## Why It Matters",
    ]

    for section in required_sections:
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

    routes = config.get("routes")

    if not isinstance(routes, dict):
        raise RuntimeError(
            "❌ skill_routes.json missing object: routes"
        )

    selection = config.get("selection", {})

    if not isinstance(selection, dict):
        raise RuntimeError(
            "❌ skill_routes.json selection must be an object."
        )

    min_skills = selection.get(
        "min_skills",
        DEFAULT_MIN_SKILLS,
    )

    max_skills = selection.get(
        "max_skills",
        DEFAULT_MAX_SKILLS,
    )

    if not isinstance(min_skills, int):
        raise RuntimeError(
            "❌ selection.min_skills must be integer."
        )

    if not isinstance(max_skills, int):
        raise RuntimeError(
            "❌ selection.max_skills must be integer."
        )

    if min_skills < 1:
        raise RuntimeError(
            "❌ selection.min_skills must be >= 1."
        )

    if max_skills < min_skills:
        raise RuntimeError(
            "❌ selection.max_skills must be >= min_skills."
        )

    return routes, min_skills, max_skills


# ======================================================================
# ANALYSIS ROUTES
# ======================================================================

def build_analysis_routes(
    routes: dict[str, Any],
) -> dict[str, list[str]]:
    """
    只保留：

        role == analysis

    的路线。

    output 路线完全排除。
    """

    result: dict[str, list[str]] = {}

    for route_name, route_data in routes.items():

        if not isinstance(route_name, str):
            continue

        if not isinstance(route_data, dict):
            continue

        role = route_data.get("role")

        if role != ANALYSIS_ROLE:
            continue

        skills = route_data.get("skills")

        if not isinstance(skills, list):
            raise RuntimeError(
                f"❌ Route {route_name!r} skills must be a list."
            )

        clean_skills: list[str] = []

        for skill_name in skills:

            if not isinstance(skill_name, str):
                raise RuntimeError(
                    f"❌ Route {route_name!r} "
                    "contains non-string Skill name."
                )

            skill_name = skill_name.strip()

            if not skill_name:
                continue

            if skill_name not in clean_skills:
                clean_skills.append(skill_name)

        if not clean_skills:
            raise RuntimeError(
                f"❌ Analysis route {route_name!r} "
                "contains no valid Skills."
            )

        result[route_name] = clean_skills

    if not result:
        raise RuntimeError(
            "❌ No analysis routes found in skill_routes.json."
        )

    return result


# ======================================================================
# SKILL CATALOG
# ======================================================================

def build_skill_catalog() -> dict[str, Any]:
    """
    加载 Skills Library。

    这里只加载一次。

    注意：

    不会把全部 Skill 内容发送给 AI。
    """

    skills = load_skills()

    if not isinstance(skills, dict):
        raise RuntimeError(
            "❌ load_skills() must return a dict."
        )

    return skills


# ======================================================================
# VALIDATE ROUTE SKILLS AGAINST LIBRARY
# ======================================================================

def validate_route_skill_library(
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
) -> None:

    for route_name, skill_names in analysis_routes.items():

        for skill_name in skill_names:

            if skill_name not in skill_catalog:
                raise RuntimeError(
                    "❌ Skill Router references missing Skill:\n"
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

        for skill_name in analysis_routes[route_name]:

            if skill_name not in candidates:
                candidates.append(skill_name)

    return candidates


# ======================================================================
# JSON EXTRACTION
# ======================================================================

def extract_json_object(text: str) -> dict[str, Any]:
    """
    从 AI 输出中尽量提取 JSON object。

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
        data = json.loads(text)

        if isinstance(data, dict):
            return data

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:

        candidate = text[start:end + 1]

        try:
            data = json.loads(candidate)

            if isinstance(data, dict):
                return data

        except json.JSONDecodeError:
            pass

    raise ValueError(
        "AI output does not contain a valid JSON object."
    )


# ======================================================================
# ROUTE SELECTION PROMPT
# ======================================================================

def build_skill_selection_prompt(
    event_id: str,
    event_title: str,
    event_text: str,
    analysis_routes: dict[str, list[str]],
    min_skills: int,
    max_skills: int,
) -> str:

    route_catalog = json.dumps(
        analysis_routes,
        ensure_ascii=False,
        indent=2,
    )

    return f"""
你是 748686 自生长知识系统的 Skill Router。

你的任务不是写分析。

你的任务只有两个：

1. 判断这个 EventUnit 最适合哪些“分析路线”
2. 从这些分析路线允许的 Skills 中选择 {min_skills}–{max_skills} 个最适合本事件的 Skill

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

下面是唯一允许使用的分析路线：

{route_catalog}

注意：

只允许使用上述 routes。

这些路线全部满足：

role == "analysis"

任何 output 类型 Skill 都禁止选择。

============================================================
SELECTION RULES
============================================================

你必须：

1. 选择 1–3 个最相关的 analysis routes
2. 从这些 routes 的 Skill 并集中选择 Skills
3. 最终必须选择 {min_skills}–{max_skills} 个 Skill
4. Skill 名称必须逐字匹配候选 Skill
5. 不得创造新的 Skill 名称
6. 不得选择 output route
7. 不要选择明显无关的 Skill
8. 优先选择能够真正解释这个 Event 的分析框架
9. 如果多个 Skill 功能重复，应优先选择互补的 Skill

============================================================
OUTPUT FORMAT
============================================================

只能输出 JSON。

格式：

{{
  "event_type": "新闻",
  "routes": [
    "新闻"
  ],
  "selected_skills": [
    "总结文章.md",
    "四维价值模型.md"
  ],
  "reason": "简短说明为什么选择这些分析路线和 Skills"
}}

不要输出 Markdown。
不要输出代码块。
不要输出 JSON 之外的内容。
""".strip()


# ======================================================================
# VALIDATE AI SELECTION
# ======================================================================

def validate_skill_selection(
    result: dict[str, Any],
    analysis_routes: dict[str, list[str]],
    skill_catalog: dict[str, Any],
    min_skills: int,
    max_skills: int,
) -> tuple[list[str], list[str]]:

    routes = result.get("routes")

    if not isinstance(routes, list):
        raise ValueError(
            "routes must be a list."
        )

    if not routes:
        raise ValueError(
            "routes cannot be empty."
        )

    for route_name in routes:

        if not isinstance(route_name, str):
            raise ValueError(
                "route name must be string."
            )

        if route_name not in analysis_routes:
            raise ValueError(
                f"Illegal analysis route: {route_name!r}"
            )

    selected_skills = result.get("selected_skills")

    if not isinstance(selected_skills, list):
        raise ValueError(
            "selected_skills must be a list."
        )

    # --------------------------------------------------------------
    # 数量验证
    # --------------------------------------------------------------

    if len(selected_skills) < min_skills:
        raise ValueError(
            f"Too few Skills: {len(selected_skills)}. "
            f"Minimum is {min_skills}."
        )

    if len(selected_skills) > max_skills:
        raise ValueError(
            f"Too many Skills: {len(selected_skills)}. "
            f"Maximum is {max_skills}."
        )

    # --------------------------------------------------------------
    # Duplicate
    # --------------------------------------------------------------

    if len(selected_skills) != len(set(selected_skills)):
        raise ValueError(
            "Duplicate Skills detected."
        )

    # --------------------------------------------------------------
    # Candidate
    # --------------------------------------------------------------

    candidates = build_candidate_skills(
        routes,
        analysis_routes,
    )

    for skill_name in selected_skills:

        if not isinstance(skill_name, str):
            raise ValueError(
                "Skill name must be string."
            )

        if skill_name not in skill_catalog:
            raise ValueError(
                f"Skill does not exist in Library: "
                f"{skill_name!r}"
            )

        if skill_name not in candidates:
            raise ValueError(
                f"Skill {skill_name!r} is not allowed "
                "by the selected analysis routes."
            )

    return routes, selected_skills


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
) -> tuple[list[str], list[str]]:

    prompt = build_skill_selection_prompt(
        event_id=event_id,
        event_title=event_title,
        event_text=event_text,
        analysis_routes=analysis_routes,
        min_skills=min_skills,
        max_skills=max_skills,
    )

    last_error: Exception | None = None

    for attempt in range(
        1,
        MAX_SKILL_SELECTION_RETRIES + 1,
    ):

        try:

            result_text = call_ai(
                prompt,
                temperature=0.1,
            )

            result = extract_json_object(
                result_text
            )

            routes, selected_skills = validate_skill_selection(
                result=result,
                analysis_routes=analysis_routes,
                skill_catalog=skill_catalog,
                min_skills=min_skills,
                max_skills=max_skills,
            )

            return routes, selected_skills

        except Exception as exc:

            last_error = exc

            print(
                f"   ⚠️ Skill Selection retry "
                f"{attempt}/{MAX_SKILL_SELECTION_RETRIES}: "
                f"{exc}"
            )

            if attempt < MAX_SKILL_SELECTION_RETRIES:
                time.sleep(2)

    raise RuntimeError(
        "❌ Skill selection failed after retries.\n"
        f"Event ID : {event_id}\n"
        f"Error    : {last_error}"
    )


# ======================================================================
# BUILD SELECTED SKILL CONTENT
# ======================================================================

def build_selected_skill_context(
    selected_skills: list[str],
    skill_catalog: dict[str, Any],
) -> str:

    blocks: list[str] = []

    for skill_name in selected_skills:

        data = skill_catalog.get(skill_name)

        if isinstance(data, dict):
            content = data.get("content", "")
        else:
            content = ""

        if not isinstance(content, str):
            content = str(content)

        content = content.strip()

        if not content:
            raise RuntimeError(
                f"❌ Selected Skill has empty content: "
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

    return "\n\n".join(blocks)


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

你现在负责对一个已经完成聚类和 EventUnit 构建的事件进行深度分析。

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
SKILL CONTENT
============================================================

{selected_skill_context}

============================================================
ORIGINAL EVENTUNIT
============================================================

{event_text}

============================================================
ANALYSIS REQUIREMENTS
============================================================

输出语言必须是：

{output_language}

你必须：

1. 只围绕当前 EventUnit 分析
2. 不编造事实
3. 明确区分：
   - 已知事实
   - 推断
   - 不确定信息
4. 使用 Selected Skills 的方法论
5. 不要机械地逐个介绍 Skill
6. 必须把多个 Skill 综合成一个完整分析
7. 分析应该服务于：
   - 理解事件
   - 判断影响
   - 理解机制
   - 发现风险
   - 发现机会
   - 支持后续决策
8. 不要生成内容创作类文章
9. 不要生成小红书文案
10. 不要生成故事
11. 不要生成日报或周报
12. 不要添加与事件无关的内容

============================================================
OUTPUT STRUCTURE
============================================================

必须严格使用以下结构：

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
SELECTED SKILLS
============================================================

在：

## Selected Skills

中列出本次实际使用的 Skills：

{skills_text}

不要列出其他 Skill。

============================================================
QUALITY
============================================================

分析应该：

- 事实准确
- 逻辑清晰
- 有因果关系
- 有影响分析
- 有战略或商业含义
- 有不确定性说明
- 避免空泛总结
- 避免重复 EventUnit 原文
- 避免为了使用 Skill 而强行套模型

直接输出 Markdown 正文。

不要输出：

```markdown
...
