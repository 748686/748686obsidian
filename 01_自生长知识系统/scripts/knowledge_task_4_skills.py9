#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4 — Event Analysis / Skill Router
V6.5.7

======================================================================
TASK 4职责
======================================================================

    1. 读取 Task 3 EventUnit
    2. 验证 Task 3 _COMPLETE
    3. 根据 EventUnit 内容进行 Event Type / Route 判断
    4. 根据 skill_routes.json 的 selection 配置选择 2–6 个 Analysis Skills
    5. Python 严格验证 Skill Selection
    6. 只加载 Router 选择出的 Skills
    7. AI 生成 Event Analysis
    8. Python 严格验证 Analysis
    9. Analysis 验证失败最多重试 3 次
       每次重试必须携带上一轮 Validator 的具体错误反馈
   10. 保存 {event_stem}_analysis.md
   11. 所有 EventUnit 完成后写入 _SKILLS_COMPLETE

======================================================================
V6.5.7 修复
======================================================================

核心修复：

V6.5.6 原问题：

    Analysis 第一次生成失败
        ↓
    Validator 返回：
        Analysis missing selected skills: 总结文章.md
        ↓
    Retry 2
        ↓
    使用完全相同 Prompt 再次生成
        ↓
    Retry 3
        ↓
    仍然使用相同 Prompt
        ↓
    失败

V6.5.7：

    Analysis 第一次生成失败
        ↓
    Validator 返回具体错误
        ↓
    将错误反馈注入下一轮 Analysis Prompt
        ↓
    AI 根据具体错误修正
        ↓
    再次严格验证

Router Selection 永远固定。

Validation Retry 只重新生成 Analysis。

======================================================================
目录 / 语言大小写最终契约
======================================================================

语言参数永久锁死为：

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

禁止任何大小写自动转换。

======================================================================
TASK 3 输入
======================================================================

Raw News/
└── YYYY-MM-DD-EventUnit/
    └── en/
        ├── _COMPLETE
        └── event_units/
            ├── EVT-xxxxxx.md
            └── ...

zh 同理。

======================================================================
TASK 4 输出
======================================================================

Raw News/
└── YYYY-MM-DD-EventUnit/
    └── en/
        ├── _COMPLETE
        └── event_units/
            ├── EVT-xxxxxx.md
            ├── EVT-xxxxxx_analysis.md
            └── _SKILLS_COMPLETE

zh 同理。

======================================================================
SKILL CONTRACT
======================================================================

Router 只能选择：

    role == "analysis"

禁止：

    role == "output"

Skill 数量必须来自：

    skill_routes.json
        selection.min_skills
        selection.max_skills

DEFAULT_MIN_SKILLS / DEFAULT_MAX_SKILLS
仅作为配置缺失时的 fallback，
不是业务规则。

======================================================================
ANALYSIS CONTRACT
======================================================================

Analysis 中：

    ## Selected Skills

必须严格包含 Router 最终选择的 Skills。

要求：

    1. 所有 selected skills 必须存在
    2. 不允许遗漏
    3. 不允许增加
    4. Skill 名称不得修改
    5. 不重新运行 Router
    6. Retry 时必须保留原始 EventUnit
    7. Retry 时必须保留原始 selected_skills
    8. Retry 时必须把 Validator 错误反馈给 AI

======================================================================
VERSION
======================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ======================================================================
# KNOWLEDGE COMMON
# ======================================================================

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


# ======================================================================
# VERSION
# ======================================================================

VERSION = "V6.5.7"


# ======================================================================
# LANGUAGE CONTRACT
# ======================================================================

SUPPORTED_LANGUAGES = {"en", "zh"}


def validate_language(
    language: str,
) -> str:

    if language not in SUPPORTED_LANGUAGES:

        raise ValueError(
            f"Invalid language: {language!r}. "
            f"Only exact lowercase 'en' or 'zh' are allowed."
        )

    return language


# ======================================================================
# GLOBAL EVENT ID
# ======================================================================

GLOBAL_EVENT_ID_RE = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)


# ======================================================================
# RETRY CONFIG
# ======================================================================

MAX_SKILL_SELECTION_RETRIES = 3

MAX_ANALYSIS_RETRIES = 3

MAX_ANALYSIS_VALIDATION_RETRIES = 3


# ======================================================================
# FALLBACK ONLY
# ======================================================================

DEFAULT_MIN_SKILLS = 2
DEFAULT_MAX_SKILLS = 6


# ======================================================================
# TASK 3 COMPLETE MARKER
# ======================================================================

def task3_complete_marker(
    date: str,
    language: str,
) -> Path:

    validate_language(language)

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / language
        / EVENT_UNITS_COMPLETE_FILE
    )


# ======================================================================
# TASK 4 COMPLETE MARKER
# ======================================================================

def skills_complete_marker(
    date: str,
    language: str,
) -> Path:

    validate_language(language)

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / language
        / "event_units"
        / SKILLS_COMPLETE_FILE
    )


# ======================================================================
# EVENTUNIT DISCOVERY
# ======================================================================

def discover_event_units(
    date: str,
    language: str,
) -> list[Path]:

    validate_language(language)

    directory = event_units_dir(
        date,
        language,
    )

    if not directory.exists():

        raise FileNotFoundError(
            f"EventUnit directory does not exist:\n{directory}"
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

def analysis_path(
    event_path: Path,
) -> Path:

    return event_path.with_name(
        event_path.stem + "_analysis.md"
    )


# ======================================================================
# READ TEXT
# ======================================================================

def read_text(
    path: Path,
) -> str:

    return path.read_text(
        encoding="utf-8"
    )


# ======================================================================
# EXTRACT EVENT ID
# ======================================================================

def extract_event_id(
    text: str,
    path: Path,
) -> str:

    match = re.search(
        r"(?m)^event_id\s*:\s*([^\s]+)\s*$",
        text,
    )

    if match:

        event_id = match.group(1).strip()

        if GLOBAL_EVENT_ID_RE.fullmatch(event_id):

            return event_id

    match = re.search(
        r"\bEVT-\d{8}-\d{6}\b",
        text,
    )

    if match:

        event_id = match.group(0)

        if GLOBAL_EVENT_ID_RE.fullmatch(event_id):

            return event_id

    match = GLOBAL_EVENT_ID_RE.search(
        path.stem
    )

    if match:

        return match.group(0)

    raise ValueError(
        f"Unable to determine valid Event ID: {path}"
    )


# ======================================================================
# ROUTE NAME
# ======================================================================

def extract_route_name(
    route: Any,
) -> str:

    if isinstance(route, str):

        return route.strip()

    if isinstance(route, dict):

        for key in (
            "name",
            "route",
            "type",
            "event_type",
            "id",
        ):

            value = route.get(key)

            if isinstance(value, str) and value.strip():

                return value.strip()

    return ""


# ======================================================================
# SKILL NAME
# ======================================================================

def extract_skill_name(
    skill: Any,
) -> str:

    if isinstance(skill, str):

        return skill.strip()

    if isinstance(skill, dict):

        for key in (
            "name",
            "skill",
            "id",
            "file",
        ):

            value = skill.get(key)

            if isinstance(value, str) and value.strip():

                return value.strip()

    return ""


# ======================================================================
# ANALYSIS SKILL CATALOG
# ======================================================================

def analysis_skill_catalog(
    skills: Any,
) -> dict[str, Any]:

    catalog: dict[str, Any] = {}

    if isinstance(skills, dict):

        for key, value in skills.items():

            if not isinstance(key, str):

                continue

            name = key.strip()

            if not name:

                continue

            catalog[name] = value

    elif isinstance(skills, list):

        for item in skills:

            if not isinstance(item, dict):

                continue

            name = extract_skill_name(item)

            if not name:

                continue

            catalog[name] = item

    return catalog


# ======================================================================
# SELECTION CONFIG
# ======================================================================

def get_selection_config(
    routes: Any,
) -> tuple[int, int]:

    minimum = DEFAULT_MIN_SKILLS
    maximum = DEFAULT_MAX_SKILLS

    if isinstance(routes, dict):

        selection = routes.get(
            "selection"
        )

        if isinstance(selection, dict):

            raw_min = selection.get(
                "min_skills"
            )

            raw_max = selection.get(
                "max_skills"
            )

            if isinstance(raw_min, int):

                minimum = raw_min

            if isinstance(raw_max, int):

                maximum = raw_max

    if minimum < 1:

        raise ValueError(
            f"Invalid min_skills: {minimum}"
        )

    if maximum < minimum:

        raise ValueError(
            f"Invalid skill range: "
            f"{minimum}–{maximum}"
        )

    return minimum, maximum


# ======================================================================
# ROUTE LOOKUP
# ======================================================================

def find_event_route(
    routes: Any,
    event_text: str,
) -> Any:

    if not isinstance(routes, dict):

        raise ValueError(
            "skill_routes.json must be a JSON object."
        )

    route_names: list[str] = []

    for key in (
        "routes",
        "event_types",
        "types",
    ):

        values = routes.get(key)

        if isinstance(values, dict):

            for name in values:

                if isinstance(name, str):

                    route_names.append(name)

        elif isinstance(values, list):

            for item in values:

                name = extract_route_name(item)

                if name:

                    route_names.append(name)

    if not route_names:

        raise ValueError(
            "No routes found in skill_routes.json."
        )

    prompt = f"""
你是 748686 自生长知识系统的 Event Type Router。

请根据下面 EventUnit 判断它最适合的 Route。

允许的 Route：

{json.dumps(
    route_names,
    ensure_ascii=False,
    indent=2,
)}

EventUnit：

{event_text}

只返回一个 Route 名称。
不要解释。
"""

    result = call_ai(prompt)

    route_text = result.strip()

    for name in route_names:

        if route_text == name:

            return name

    raise ValueError(
        f"AI returned invalid route: {route_text!r}"
    )


# ======================================================================
# GET ROUTE CONFIG
# ======================================================================

def get_route_config(
    routes: Any,
    route_name: str,
) -> Any:

    if not isinstance(routes, dict):

        raise ValueError(
            "Routes configuration must be dict."
        )

    for container_key in (
        "routes",
        "event_types",
        "types",
    ):

        container = routes.get(
            container_key
        )

        if isinstance(container, dict):

            if route_name in container:

                return container[route_name]

        elif isinstance(container, list):

            for item in container:

                if not isinstance(item, dict):

                    continue

                name = extract_route_name(item)

                if name == route_name:

                    return item

    raise ValueError(
        f"Route not found: {route_name}"
    )


# ======================================================================
# ROUTE SKILLS
# ======================================================================

def route_skill_candidates(
    route_config: Any,
) -> list[str]:

    candidates: list[str] = []

    if isinstance(route_config, dict):

        for key in (
            "skills",
            "analysis_skills",
            "candidate_skills",
        ):

            values = route_config.get(key)

            if isinstance(values, list):

                for item in values:

                    name = extract_skill_name(item)

                    if name:

                        candidates.append(name)

            elif isinstance(values, dict):

                for key_name in values:

                    if isinstance(key_name, str):

                        candidates.append(
                            key_name
                        )

    elif isinstance(route_config, list):

        for item in route_config:

            name = extract_skill_name(item)

            if name:

                candidates.append(name)

    unique: list[str] = []

    seen: set[str] = set()

    for name in candidates:

        if name in seen:

            continue

        seen.add(name)

        unique.append(name)

    return unique


# ======================================================================
# ROUTER SKILL SELECTION
# ======================================================================

def select_skills(
    event_text: str,
    route_name: str,
    route_config: Any,
    skill_catalog: dict[str, Any],
    minimum: int,
    maximum: int,
) -> list[str]:

    candidates = route_skill_candidates(
        route_config
    )

    if not candidates:

        candidates = list(
            skill_catalog.keys()
        )

    candidates = [
        name
        for name in candidates
        if name in skill_catalog
    ]

    if len(candidates) < minimum:

        raise ValueError(
            f"Route {route_name!r} has only "
            f"{len(candidates)} analysis skills, "
            f"but minimum is {minimum}."
        )

    prompt = f"""
你是 748686 自生长知识系统的 Skill Router。

Event Type / Route：

{route_name}

EventUnit：

{event_text}

候选 Analysis Skills：

{json.dumps(
    candidates,
    ensure_ascii=False,
    indent=2,
)}

请选择 {minimum}–{maximum} 个最适合的 Analysis Skills。

硬性要求：

1. 只能从候选 Skills 中选择。
2. 只能选择 role == analysis 的 Skills。
3. 不得创建新 Skill。
4. 不得修改 Skill 名称。
5. 数量必须在 {minimum}–{maximum} 范围内。
6. 必须至少选择 {minimum} 个 Skill。
7. 绝对不能只返回 1 个 Skill。
8. 即使只有一个 Skill 最相关，也必须从候选列表中继续选择其他相关 Skill，
   直到达到最少 {minimum} 个。
9. 只返回 JSON 数组。
10. 不要解释。

例如：

["总结文章.md", "金字塔原理.md"]
"""

    last_error: Exception | None = None

    for attempt in range(
        1,
        MAX_SKILL_SELECTION_RETRIES + 1,
    ):

        try:

            current_prompt = prompt

            if (
                attempt > 1
                and last_error is not None
            ):

                current_prompt += f"""

============================================================
上一次 Skill Selection 无效
============================================================

上一次 Python 验证失败：

{last_error}

本次必须修正。

再次强调：

- 必须选择至少 {minimum} 个 Skills。
- 最多只能选择 {maximum} 个 Skills。
- 不能返回 1 个 Skill。
- 只能从候选 Skills 中选择。
- 必须返回 JSON 数组。
- 不要解释。
"""

            result = call_ai(
                current_prompt
            )

            parsed = json.loads(
                result
            )

            if not isinstance(
                parsed,
                list,
            ):

                raise ValueError(
                    "Skill selection must be a JSON array."
                )

            selected: list[str] = []

            for item in parsed:

                if not isinstance(
                    item,
                    str,
                ):

                    raise ValueError(
                        "Skill names must be strings."
                    )

                name = item.strip()

                if not name:

                    raise ValueError(
                        "Empty skill name."
                    )

                if name not in candidates:

                    raise ValueError(
                        f"Skill not allowed: {name}"
                    )

                if name not in skill_catalog:

                    raise ValueError(
                        f"Skill not found in catalog: {name}"
                    )

                if name not in selected:

                    selected.append(name)

            if not (
                minimum
                <= len(selected)
                <= maximum
            ):

                raise ValueError(
                    f"Invalid skill count: "
                    f"{len(selected)} "
                    f"(expected {minimum}–{maximum})"
                )

            return selected

        except Exception as exc:

            last_error = exc

            print(
                f"   ⚠️ SKILL ROUTER RETRY "
                f"{attempt}/"
                f"{MAX_SKILL_SELECTION_RETRIES} | "
                f"{exc}"
            )

    raise RuntimeError(
        f"Skill selection failed after "
        f"{MAX_SKILL_SELECTION_RETRIES} attempts: "
        f"{last_error}"
    )


# ======================================================================
# LOAD SELECTED SKILLS
# ======================================================================

def load_selected_skills(
    selected: list[str],
    skill_catalog: dict[str, Any],
) -> dict[str, Any]:

    loaded: dict[str, Any] = {}

    for name in selected:

        if name not in skill_catalog:

            raise ValueError(
                f"Selected skill missing: {name}"
            )

        loaded[name] = skill_catalog[name]

    return loaded


# ======================================================================
# EXISTING ANALYSIS VALIDATION
# ======================================================================

def validate_existing_analysis(
    event_path: Path,
    analysis_file: Path,
    selected_skills: list[str],
    skill_catalog: dict[str, Any],
) -> bool:

    if not analysis_file.exists():

        return False

    try:

        text = read_text(
            analysis_file
        )

        event_id = extract_event_id(
            read_text(event_path),
            event_path,
        )

        validate_generated_analysis_strict(
            text,
            event_id,
            selected_skills,
            skill_catalog,
        )

        return True

    except Exception:

        return False


# ======================================================================
# STRICT ANALYSIS VALIDATION
# ======================================================================

def validate_generated_analysis_strict(
    analysis_text: str,
    event_id: str,
    selected_skills: list[str],
    skill_catalog: dict[str, Any],
) -> None:

    if not analysis_text.strip():

        raise ValueError(
            "Analysis output is empty."
        )

    # --------------------------------------------------------------
    # Event ID
    # --------------------------------------------------------------

    if event_id not in analysis_text:

        raise ValueError(
            f"Analysis missing Event ID: {event_id}"
        )

    # --------------------------------------------------------------
    # Required sections
    # --------------------------------------------------------------

    required_sections = (
        "## Event ID",
        "## Selected Skills",
    )

    for section in required_sections:

        if section not in analysis_text:

            raise ValueError(
                f"Analysis missing required section: {section}"
            )

    # --------------------------------------------------------------
    # Selected Skills section
    # --------------------------------------------------------------

    marker = "## Selected Skills"

    start = analysis_text.find(
        marker
    )

    if start < 0:

        raise ValueError(
            "Analysis missing Selected Skills section."
        )

    content = analysis_text[
        start + len(marker):
    ]

    next_section = content.find(
        "\n## "
    )

    if next_section >= 0:

        content = content[
            :next_section
        ]

    # --------------------------------------------------------------
    # Required selected skills
    # --------------------------------------------------------------

    missing = [
        skill
        for skill in selected_skills
        if skill not in content
    ]

    if missing:

        raise ValueError(
            "Analysis missing selected skills: "
            + ", ".join(missing)
        )

    # --------------------------------------------------------------
    # Extra known skills
    # --------------------------------------------------------------

    extras = [
        skill
        for skill in skill_catalog
        if skill not in selected_skills
        and skill in content
    ]

    if extras:

        raise ValueError(
            "Analysis contains unselected skills: "
            + ", ".join(extras)
        )


# ======================================================================
# GENERATE ANALYSIS
# ======================================================================

def generate_analysis(
    event_text: str,
    event_id: str,
    route_name: str,
    selected_skills: list[str],
    loaded_skills: dict[str, Any],
    validation_feedback: str | None = None,
) -> str:

    skill_payload: dict[str, Any] = {}

    for name in selected_skills:

        skill_payload[name] = loaded_skills[
            name
        ]

    prompt = f"""
你是 748686 自生长知识系统的 Event Analysis Engine。

请根据 EventUnit 生成最终 Event Analysis。

Event ID：

{event_id}

Event Route：

{route_name}

============================================================
Router 已经固定选择的 Skills
============================================================

{json.dumps(
    selected_skills,
    ensure_ascii=False,
    indent=2,
)}

注意：

这些 Skills 已经由 Router 固定。

你不得：

- 重新选择 Skills
- 增加 Skills
- 删除 Skills
- 修改 Skill 名称

============================================================
实际加载的 Skills
============================================================

{json.dumps(
    skill_payload,
    ensure_ascii=False,
    indent=2,
)}

============================================================
EventUnit
============================================================

{event_text}

============================================================
输出要求
============================================================

必须严格按照以下结构输出：

## Event ID

{event_id}

## Selected Skills

- {selected_skills[0]}
"""

    if len(selected_skills) > 1:

        for skill in selected_skills[1:]:

            prompt += f"""
- {skill}
"""

    prompt += """

随后根据所选 Skills 完成 Event Analysis。

============================================================
Selected Skills 严格契约
============================================================

以下是 Router 已经固定选择的 Skills：

"""

    prompt += json.dumps(
        selected_skills,
        ensure_ascii=False,
        indent=2,
    )

    prompt += """

你必须在：

## Selected Skills

下面逐字、完整、原样列出所有这些 Skill 文件名。

特别注意：

- 必须保留 `.md`
- 不得翻译
- 不得改名
- 不得删除
- 不得增加
- 不得使用 Skill 标题代替文件名
- 不得把文件名改成不带 `.md` 的形式
- 不得把一个 Skill 的标题当成另一个 Skill 的文件名

例如：

总结文章.md

必须写成：

- 总结文章.md

而不是：

- 总结文章
- 总结
- Article Summary
- 其他名称

必须全部出现。

只输出最终 Markdown。
不要输出解释。
"""

    # --------------------------------------------------------------
    # V6.5.7
    # Validation Feedback
    # --------------------------------------------------------------

    if validation_feedback:

        prompt += f"""

============================================================
⚠️ 上一次 Analysis 验证失败
============================================================

这是上一轮 Analysis 的 Python Validator 错误：

{validation_feedback}

本次不是重新选择 Skills。

Router Selection 已经固定。

你必须：

1. 保留 Event ID：
   {event_id}

2. 保留 Route：
   {route_name}

3. 保留全部 Router 选择的 Skills。

4. 修复上面 Validator 指出的具体问题。

5. 重新输出完整 Markdown。

特别重要：

如果错误是：

Analysis missing selected skills: 某个Skill.md

那么必须确认：

## Selected Skills

下面存在这个 Skill 的完整文件名，
包括 `.md` 后缀。

不要只输出 Skill 的自然语言标题。

不要解释修复过程。

只输出修复后的完整 Markdown。
"""

    return call_ai(
        prompt
    ).strip()


# ======================================================================
# WRITE ANALYSIS
# ======================================================================

def write_analysis(
    path: Path,
    text: str,
) -> None:

    write_text_atomic(
        path,
        text.rstrip() + "\n",
    )


# ======================================================================
# PROCESS SINGLE EVENTUNIT
# ======================================================================

def process_event(
    event_path: Path,
    routes: Any,
    skill_catalog: dict[str, Any],
    minimum: int,
    maximum: int,
) -> tuple[bool, bool]:

    event_text = read_text(
        event_path
    )

    event_id = extract_event_id(
        event_text,
        event_path,
    )

    print(
        f"   🧭 ROUTING | {event_id}"
    )

    route_name = find_event_route(
        routes,
        event_text,
    )

    print(
        f"   🧠 ROUTES  | {route_name}"
    )

    route_config = get_route_config(
        routes,
        route_name,
    )

    selected_skills = select_skills(
        event_text,
        route_name,
        route_config,
        skill_catalog,
        minimum,
        maximum,
    )

    print(
        f"   🧩 SKILLS  | "
        f"{', '.join(selected_skills)}"
    )

    analysis_file = analysis_path(
        event_path
    )

    # --------------------------------------------------------------
    # Preserve valid existing analysis
    # --------------------------------------------------------------

    if validate_existing_analysis(
        event_path,
        analysis_file,
        selected_skills,
        skill_catalog,
    ):

        print(
            f"   ⏭️ EXISTS | {analysis_file}"
        )

        return False, True

    loaded_skills = load_selected_skills(
        selected_skills,
        skill_catalog,
    )

    print(
        f"   🔨 ANALYSIS | {event_id}"
    )

    last_error: Exception | None = None

    for attempt in range(
        1,
        MAX_ANALYSIS_VALIDATION_RETRIES + 1,
    ):

        try:

            validation_feedback = (
                str(last_error)
                if last_error is not None
                else None
            )

            # ----------------------------------------------------------
            # 每次 retry：
            #
            # 1. Router 不重新执行
            # 2. selected_skills 不改变
            # 3. EventUnit 不改变
            # 4. 原 Validator 错误加入 Prompt
            # ----------------------------------------------------------

            if validation_feedback:

                print(
                    f"   🔁 ANALYSIS CORRECTION "
                    f"{attempt}/"
                    f"{MAX_ANALYSIS_VALIDATION_RETRIES} | "
                    f"{event_id}"
                )

                print(
                    f"   🛠️ VALIDATION FEEDBACK | "
                    f"{validation_feedback}"
                )

            analysis_text = generate_analysis(
                event_text,
                event_id,
                route_name,
                selected_skills,
                loaded_skills,
                validation_feedback,
            )

            validate_generated_analysis_strict(
                analysis_text,
                event_id,
                selected_skills,
                skill_catalog,
            )

            print(
                f"   ✅ ANALYSIS VALIDATED | "
                f"{event_id}"
            )

            write_analysis(
                analysis_file,
                analysis_text,
            )

            print(
                f"   ✅ SAVED | {analysis_file}"
            )

            return True, False

        except Exception as exc:

            last_error = exc

            print(
                f"   ⚠️ ANALYSIS VALIDATION RETRY "
                f"{attempt}/"
                f"{MAX_ANALYSIS_VALIDATION_RETRIES} | "
                f"{event_id} | {exc}"
            )

    raise RuntimeError(
        f"Analysis failed after "
        f"{MAX_ANALYSIS_VALIDATION_RETRIES} "
        f"validation attempts for {event_id}: "
        f"{last_error}"
    )


# ======================================================================
# REMOVE STALE COMPLETE MARKER
# ======================================================================

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
            f"   🧹 Removed stale marker | {marker}"
        )


# ======================================================================
# WRITE SKILLS COMPLETE
# ======================================================================

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
# FINAL VALIDATE UNIT
# ======================================================================

def final_validate_unit(
    date: str,
    language: str,
    event_paths: list[Path],
    skill_catalog: dict[str, Any],
) -> int:

    analysis_count = 0

    for event_path in event_paths:

        event_text = read_text(
            event_path
        )

        event_id = extract_event_id(
            event_text,
            event_path,
        )

        analysis_file = analysis_path(
            event_path
        )

        if not analysis_file.exists():

            raise RuntimeError(
                f"Missing analysis file for "
                f"{event_id}: {analysis_file}"
            )

        analysis_text = read_text(
            analysis_file
        )

        if event_id not in analysis_text:

            raise RuntimeError(
                f"Analysis Event ID mismatch: "
                f"{event_id}"
            )

        if "## Selected Skills" not in analysis_text:

            raise RuntimeError(
                f"Analysis missing Selected Skills: "
                f"{event_id}"
            )

        analysis_count += 1

    if analysis_count != len(event_paths):

        raise RuntimeError(
            f"Analysis count mismatch: "
            f"{analysis_count} / {len(event_paths)}"
        )

    return analysis_count


# ======================================================================
# PROCESS UNIT
# ======================================================================

def process_unit(
    date: str,
    language: str,
) -> None:

    validate_language(
        language
    )

    print()
    print("=" * 70)
    print(
        "TASK 4 — EVENT ANALYSIS / SKILL ROUTER"
    )
    print("=" * 70)
    print(
        f"DATE              : {date}"
    )
    print(
        f"LANGUAGE          : {language}"
    )
    print(
        f"VERSION           : {VERSION}"
    )
    print("=" * 70)

    # --------------------------------------------------------------
    # Verify Task 3
    # --------------------------------------------------------------

    task3_marker = task3_complete_marker(
        date,
        language,
    )

    if not task3_marker.exists():

        raise RuntimeError(
            "Task 3 is not complete.\n"
            f"Expected:\n{task3_marker}"
        )

    print(
        f"✅ TASK 3 COMPLETE | {task3_marker}"
    )

    # --------------------------------------------------------------
    # Load routes
    # --------------------------------------------------------------

    routes = load_routes()

    minimum, maximum = get_selection_config(
        routes
    )

    print(
        f"SKILL RANGE        : "
        f"{minimum}–{maximum}"
    )

    # --------------------------------------------------------------
    # Load skills
    # --------------------------------------------------------------

    all_skills = load_skills()

    skill_catalog = analysis_skill_catalog(
        all_skills
    )

    if not skill_catalog:

        raise RuntimeError(
            "No analysis skills found."
        )

    print(
        f"ANALYSIS SKILLS    : "
        f"{len(skill_catalog)}"
    )

    # --------------------------------------------------------------
    # Discover EventUnits
    # --------------------------------------------------------------

    event_paths = discover_event_units(
        date,
        language,
    )

    if not event_paths:

        raise RuntimeError(
            f"No EventUnits found for "
            f"{date} {language}"
        )

    expected_count = len(
        event_paths
    )

    print(
        f"EVENTUNITS         : "
        f"{expected_count}"
    )

    # --------------------------------------------------------------
    # Remove stale Task 4 marker
    # --------------------------------------------------------------

    remove_stale_complete_marker(
        date,
        language,
    )

    generated = 0
    preserved = 0

    # --------------------------------------------------------------
    # Process sequentially
    # --------------------------------------------------------------

    for index, event_path in enumerate(
        event_paths,
        start=1,
    ):

        print()

        print(
            f"[{index}/{expected_count}] "
            f"PROCESSING EVENTUNIT"
        )

        created, existing = process_event(
            event_path,
            routes,
            skill_catalog,
            minimum,
            maximum,
        )

        if created:

            generated += 1

        if existing:

            preserved += 1

    # --------------------------------------------------------------
    # Final validation
    # --------------------------------------------------------------

    analysis_count = final_validate_unit(
        date,
        language,
        event_paths,
        skill_catalog,
    )

    if analysis_count != expected_count:

        raise RuntimeError(
            f"Final analysis count mismatch: "
            f"{analysis_count} / {expected_count}"
        )

    # --------------------------------------------------------------
    # Write COMPLETE marker
    # --------------------------------------------------------------

    write_skills_complete(
        date,
        language,
        expected_count,
        analysis_count,
    )

    # --------------------------------------------------------------
    # Complete
    # --------------------------------------------------------------

    print()

    print(
        "=" * 70
    )

    print(
        "TASK 4 COMPLETE"
    )

    print(
        "=" * 70
    )

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
        f"ANALYSIS          : {analysis_count}"
    )

    print(
        f"SKILL RANGE       : "
        f"{minimum}–{maximum}"
    )

    print(
        f"COMPLETE MARKER   : "
        f"{skills_complete_marker(date, language)}"
    )

    print(
        "=" * 70
    )

    print(
        f"✅ Task 4 Skills finished: "
        f"{date} {language}"
    )


# ======================================================================
# PROCESSING DATES
# ======================================================================

def default_processing_dates() -> list[str]:

    from knowledge_common import processing_dates

    return processing_dates()


# ======================================================================
# SIX PROCESSING UNITS
# ======================================================================

def process_all_units() -> None:

    dates = default_processing_dates()

    if len(dates) < 3:

        raise RuntimeError(
            "At least 3 processing dates are required."
        )

    units = [
        (dates[0], "en"),
        (dates[0], "zh"),
        (dates[1], "en"),
        (dates[1], "zh"),
        (dates[2], "en"),
        (dates[2], "zh"),
    ]

    print()

    print(
        "#" * 70
    )

    print(
        "KNOWLEDGE TASK 4"
    )

    print(
        "SIX PROCESSING UNITS"
    )

    print(
        "#" * 70
    )

    for index, (
        date,
        language,
    ) in enumerate(
        units,
        start=1,
    ):

        print()

        print(
            "#" * 70
        )

        print(
            f"PROCESSING UNIT {index} / 6"
        )

        print(
            f"DATE     : {date}"
        )

        print(
            f"LANGUAGE : {language}"
        )

        print(
            "#" * 70
        )

        process_unit(
            date,
            language,
        )

    print()

    print(
        "#" * 70
    )

    print(
        "KNOWLEDGE TASK 4 ALL SIX UNITS COMPLETE"
    )

    print(
        "#" * 70
    )


# ======================================================================
# CLI
# ======================================================================

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 4 "
            "Event Analysis / Skill Router"
        )
    )

    parser.add_argument(
        "--date",
        required=False,
        help="Processing date YYYY-MM-DD",
    )

    parser.add_argument(
        "--language",
        required=False,
        choices=[
            "en",
            "zh",
        ],
        help="Exact lowercase language: en or zh",
    )

    return parser.parse_args()


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    args = parse_args()

    if (
        args.date is not None
        and args.language is not None
    ):

        validate_language(
            args.language
        )

        process_unit(
            args.date,
            args.language,
        )

        return

    if (
        args.date is None
        and args.language is None
    ):

        process_all_units()

        return

    raise ValueError(
        "--date and --language must be "
        "provided together."
    )


# ======================================================================
# ENTRYPOINT
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n❌ Interrupted by user."
        )

        sys.exit(130)

    except Exception as exc:

        print()

        print(
            "=" * 70
        )

        print(
            "❌ TASK 4 FAILED"
        )

        print(
            "=" * 70
        )

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print(
            "=" * 70
        )

        sys.exit(1)
