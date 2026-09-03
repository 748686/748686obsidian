#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4
EventUnit → Skill Router → AI Analysis
V6.5.3

============================================================
TASK 4 新架构
============================================================

Task 3：

    EventUnit
        ↓
    一个事件 = 一个完整 Markdown

Task 4：

    EventUnit.md
        ↓
    Skill Router
        ↓
    AI判断事件类型
        ↓
    AI选择最适合的分析 Skills
        ↓
    一次综合分析
        ↓
    一个 Analysis.md

因此：

    一个 EventUnit
        =
    一个 Analysis.md

不再执行：

    Event × 27 Skills

不再产生：

    EVT-xxxx/
        SkillA.md
        SkillB.md
        SkillC.md
        ...

============================================================
语言契约
============================================================

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

禁止任何：

    lower()
    upper()
    casefold()

语言参数与磁盘目录完全一致。


============================================================
Task 3输入
============================================================

YYYY-MM-DD-EventUnit/
    en/
        event_units/
            EVT-YYYYMMDD-NNNNNN_Title.md

    zh/
        event_units/
            EVT-YYYYMMDD-NNNNNN_Title.md


============================================================
Task 4输出
============================================================

YYYY-MM-DD-EventUnit/
    en/
        event_units/
            EVT-YYYYMMDD-NNNNNN_Title.md
            EVT-YYYYMMDD-NNNNNN_analysis.md
        _SKILLS_COMPLETE

    zh/
        event_units/
            EVT-YYYYMMDD-NNNNNN_Title.md
            EVT-YYYYMMDD-NNNNNN_analysis.md
        _SKILLS_COMPLETE


============================================================
核心原则
============================================================

1. 不修改Task 3原始EventUnit。

2. EventUnit永远保持一个完整MD。

3. Skill MD是“方法库”，不是EventUnit的组成部分。

4. Router只负责提供候选方法。

5. AI根据EventUnit判断：
       - 事件类型
       - 分析需求
       - 最适合的Skills

6. 最终只生成一个Analysis.md。

7. 一个EventUnit原则上只调用一次AI。

8. AI必须输出结构化JSON。

9. Python负责把JSON转换为正式Analysis.md。

10. Analysis.md是后续日报、周报、专题报告、
    文章生成等任务的主要上游输入。


============================================================
断点续跑
============================================================

1. Analysis存在且非空：
       跳过。

2. Analysis不存在：
       生成。

3. Analysis为空：
       重新生成。

4. _SKILLS_COMPLETE存在：
       仍然检查全部EventUnit。

5. marker存在但Analysis缺失：
       删除marker。
       自动修复。

6. 所有EventUnit都有Analysis：
       才写入_SKILLS_COMPLETE。


============================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from knowledge_common import (
    ROOT,
    SKILLS_COMPLETE_FILE,
    load_saved_event_units,
    load_skills,
    load_routes,
    safe_name,
    call_ai,
    now,
    event_units_dir,
)


# ============================================================
# CONFIGURATION
# ============================================================

# EventUnit送入AI的最大字符数。
#
# 注意：
# 这是单个EventUnit的上限。
#
# 如果EventUnit本身超过这个长度，
# 会截断，而不会把多个EventUnit混在一起。
MAX_EVENT_CONTEXT = 30000

# 所有候选Skill规则送入AI的最大总字符数。
MAX_SKILL_CONTEXT = 50000

# AI最终最多选择多少个Skill。
DEFAULT_MIN_SKILLS = 2
DEFAULT_MAX_SKILLS = 6

# Analysis正式后缀。
ANALYSIS_SUFFIX = "_analysis.md"

# ============================================================
# FINAL LANGUAGE CONTRACT
# ============================================================

SUPPORTED_LANGUAGES = (
    "en",
    "zh",
)

# ============================================================
# EVENT ID CONTRACT
# ============================================================

EVENT_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

# ============================================================
# TIMEZONE
# ============================================================

TIMEZONE_NAME = "Asia/Shanghai"


# ============================================================
# LANGUAGE VALIDATION
# ============================================================

def validate_language(
    language: str
) -> str:
    """
    严格验证Task 4语言。

    只允许：

        en
        zh

    禁止任何大小写转换。
    """

    lang = str(
        language or ""
    ).strip()

    if lang not in SUPPORTED_LANGUAGES:

        raise RuntimeError(
            "❌ Task 4非法语言："
            f"{language!r}。"
            "只允许：en 或 zh"
        )

    return lang


# ============================================================
# DATE VALIDATION
# ============================================================

def validate_date(
    date: str
) -> str:
    """
    严格验证日期：

        YYYY-MM-DD
    """

    value = str(
        date or ""
    ).strip()

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        value
    ):

        raise RuntimeError(
            "❌ Task 4非法日期："
            f"{date!r}。"
            "必须为YYYY-MM-DD"
        )

    return value


# ============================================================
# EVENT ID VALIDATION
# ============================================================

def validate_event_id(
    event_id: str,
    date: str
) -> str:
    """
    验证Global Event ID。

    正式格式：

        EVT-YYYYMMDD-NNNNNN
    """

    eid = str(
        event_id or ""
    ).strip()

    if not eid:

        raise RuntimeError(
            f"❌ {date} Task 4发现空event_id"
        )

    if not EVENT_ID_PATTERN.fullmatch(
        eid
    ):

        raise RuntimeError(
            "❌ "
            f"{date} Task 4发现非法Global Event ID："
            f"{eid}"
        )

    expected_prefix = (
        f"EVT-{date.replace('-', '')}-"
    )

    if not eid.startswith(
        expected_prefix
    ):

        raise RuntimeError(
            "❌ "
            f"{date} Task 4 Event ID日期不匹配："
            f"{eid}"
        )

    return eid


# ============================================================
# ANALYSIS FILE NAME
# ============================================================

def analysis_filename(
    event_id: str
) -> str:
    """
    Analysis正式文件名：

        EVT-YYYYMMDD-NNNNNN_analysis.md
    """

    eid = str(
        event_id or ""
    ).strip()

    if not eid:

        raise RuntimeError(
            "❌ Analysis文件缺少Event ID"
        )

    validate_event_id(
        eid,
        eid[4:8] + "-" + eid[8:10] + "-" + eid[10:12]
        if len(eid) >= 12
        else ""
    )

    return (
        f"{eid}{ANALYSIS_SUFFIX}"
    )


# ============================================================
# EVENT ANALYSIS OUTPUT PATH
# ============================================================

def event_analysis_output_path(
    date: str,
    language: str,
    event_id: str
) -> Path:
    """
    返回Event Analysis正式路径：

        YYYY-MM-DD-EventUnit/
            en/
                event_units/
                    EVT-xxxx_analysis.md
    """

    lang = validate_language(
        language
    )

    date = validate_date(
        date
    )

    eid = validate_event_id(
        event_id,
        date
    )

    root = event_units_dir(
        date,
        lang
    )

    if root.name != "event_units":

        raise RuntimeError(
            "❌ Task 4 EventUnit目录契约异常："
            f"实际={root.name} "
            "期望=event_units"
        )

    if root.parent.name != lang:

        raise RuntimeError(
            "❌ Task 4语言目录契约异常："
            f"实际={root.parent.name} "
            f"期望={lang}"
        )

    return (
        root
        / analysis_filename(eid)
    )


# ============================================================
# OUTPUT VALIDATION
# ============================================================

def analysis_output_valid(
    path: Path
) -> bool:
    """
    Analysis文件有效性：

        存在
        普通文件
        非空
    """

    try:

        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
        )

    except OSError:

        return False


# ============================================================
# READ EVENT UNIT
# ============================================================

def read_event_unit(
    event
):
    """
    读取完整EventUnit。

    EventUnit不会被拆分。

    返回：

        metadata
        path
        content
    """

    metadata = event[0]
    path = event[1]

    if not isinstance(
        metadata,
        dict
    ):

        raise RuntimeError(
            "❌ Task 4 EventUnit metadata不是dict："
            f"{path}"
        )

    if not path.exists():

        raise RuntimeError(
            "❌ Task 4 EventUnit文件不存在："
            f"{path}"
        )

    if not path.is_file():

        raise RuntimeError(
            "❌ Task 4 EventUnit不是普通文件："
            f"{path}"
        )

    if path.stat().st_size <= 0:

        raise RuntimeError(
            "❌ Task 4 EventUnit为空："
            f"{path}"
        )

    content = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    if not content.strip():

        raise RuntimeError(
            "❌ Task 4 EventUnit读取后为空："
            f"{path}"
        )

    return (
        metadata,
        path,
        content
    )


# ============================================================
# ROUTER CONFIG NORMALIZATION
# ============================================================

def normalize_routes(
    routes
):
    """
    兼容：

    旧版：

        {
            "新闻": [
                "总结文章.md",
                ...
            ]
        }

    新版：

        {
            "version": "2.0",
            "routes": {
                "新闻": {
                    "role": "analysis",
                    "skills": [...]
                }
            },
            "selection": {
                "min_skills": 2,
                "max_skills": 6
            }
        }

    最终统一返回：

        {
            "version": ...,
            "routes": {...},
            "selection": {...}
        }
    """

    if not isinstance(
        routes,
        dict
    ):

        raise RuntimeError(
            "❌ skill_routes.json格式异常：不是dict"
        )

    # --------------------------------------------------------
    # 新版
    # --------------------------------------------------------

    if "routes" in routes:

        raw_routes = routes.get(
            "routes"
        )

        if not isinstance(
            raw_routes,
            dict
        ):

            raise RuntimeError(
                "❌ skill_routes.json的routes必须是dict"
            )

        selection = routes.get(
            "selection",
            {}
        )

        if not isinstance(
            selection,
            dict
        ):

            raise RuntimeError(
                "❌ skill_routes.json的selection必须是dict"
            )

        min_skills = selection.get(
            "min_skills",
            DEFAULT_MIN_SKILLS
        )

        max_skills = selection.get(
            "max_skills",
            DEFAULT_MAX_SKILLS
        )

        try:

            min_skills = int(
                min_skills
            )

            max_skills = int(
                max_skills
            )

        except Exception as e:

            raise RuntimeError(
                "❌ skill_routes.json selection数值非法"
            ) from e

        if min_skills < 1:

            raise RuntimeError(
                "❌ selection.min_skills必须>=1"
            )

        if max_skills < min_skills:

            raise RuntimeError(
                "❌ selection.max_skills不能小于min_skills"
            )

        return {
            "version": str(
                routes.get(
                    "version",
                    "2.0"
                )
            ),
            "routes": raw_routes,
            "selection": {
                "min_skills": min_skills,
                "max_skills": max_skills,
            }
        }

    # --------------------------------------------------------
    # 旧版兼容
    # --------------------------------------------------------

    normalized = {}

    for route_name, route_names in routes.items():

        if not isinstance(
            route_names,
            list
        ):

            raise RuntimeError(
                "❌ 旧版skill_routes.json路由格式异常："
                f"{route_name}"
            )

        normalized[
            str(route_name)
        ] = {
            "role": "analysis",
            "skills": route_names,
        }

    return {
        "version": "1.0-compatible",
        "routes": normalized,
        "selection": {
            "min_skills": DEFAULT_MIN_SKILLS,
            "max_skills": DEFAULT_MAX_SKILLS,
        }
    }


# ============================================================
# SKILL NAME
# ============================================================

def skill_name_from_object(
    skill
) -> str:
    """
    获取Skill名称。
    """

    if not isinstance(
        skill,
        dict
    ):

        raise RuntimeError(
            "❌ Task 4 Skill对象不是dict"
        )

    name = str(
        skill.get(
            "name",
            ""
        )
    ).strip()

    if not name:

        raise RuntimeError(
            "❌ Task 4 Skill缺少name"
        )

    return name


# ============================================================
# VALIDATE ALL SKILLS
# ============================================================

def validate_all_skills(
    skills
):
    """
    验证load_skills()。

    预期：

        {
            "SWOT分析.md": {
                "name": "SWOT分析.md",
                "content": "..."
            }
        }
    """

    if not isinstance(
        skills,
        dict
    ):

        raise RuntimeError(
            "❌ Task 4 load_skills()返回格式异常"
        )

    if not skills:

        raise RuntimeError(
            "❌ Task 4 Skills配置为空"
        )

    names = set()

    for key, skill in skills.items():

        if not isinstance(
            skill,
            dict
        ):

            raise RuntimeError(
                "❌ Task 4 Skill对象异常："
                f"{key}"
            )

        name = skill_name_from_object(
            skill
        )

        if name in names:

            raise RuntimeError(
                "❌ Task 4存在重复Skill："
                f"{name}"
            )

        names.add(
            name
        )

        content = str(
            skill.get(
                "content",
                ""
            )
        )

        if not content.strip():

            raise RuntimeError(
                "❌ Task 4 Skill规则为空："
                f"{name}"
            )

    return True


# ============================================================
# VALIDATE ROUTES
# ============================================================

def validate_routes(
    skills,
    route_config
):
    """
    验证Router中的Skill全部真实存在。

    注意：

    output型Skill也允许存在于Router。

    但Task 4只读取：

        role == analysis

    的Skill。
    """

    normalized = normalize_routes(
        route_config
    )

    routes = normalized[
        "routes"
    ]

    for route_name, route_data in routes.items():

        if not isinstance(
            route_data,
            dict
        ):

            raise RuntimeError(
                "❌ Route配置必须是dict："
                f"{route_name}"
            )

        role = str(
            route_data.get(
                "role",
                "analysis"
            )
        ).strip()

        if role not in (
            "analysis",
            "output",
        ):

            raise RuntimeError(
                "❌ Route role非法："
                f"{route_name} / {role}"
            )

        route_skills = route_data.get(
            "skills",
            []
        )

        if not isinstance(
            route_skills,
            list
        ):

            raise RuntimeError(
                "❌ Route skills必须是list："
                f"{route_name}"
            )

        for name in route_skills:

            skill_name = str(
                name
            ).strip()

            if not skill_name:
                continue

            if skill_name not in skills:

                raise RuntimeError(
                    "❌ skill_routes.json引用不存在Skill："
                    f"{skill_name}"
                    f" / route={route_name}"
                )

    return normalized


# ============================================================
# BUILD ANALYSIS SKILL POOL
# ============================================================

def build_analysis_skill_pool(
    skills,
    route_config
):
    """
    构建Task 4真正使用的分析Skill候选池。

    规则：

        role == analysis
            ↓
        可以进入Task 4

        role == output
            ↓
        Task 4不使用
    """

    normalized = normalize_routes(
        route_config
    )

    routes = normalized[
        "routes"
    ]

    pool_names = []
    seen = set()

    for route_name, route_data in routes.items():

        role = str(
            route_data.get(
                "role",
                "analysis"
            )
        ).strip()

        if role != "analysis":
            continue

        route_skills = route_data.get(
            "skills",
            []
        )

        for name in route_skills:

            skill_name = str(
                name
            ).strip()

            if not skill_name:
                continue

            if skill_name not in skills:

                raise RuntimeError(
                    "❌ Analysis Skill不存在："
                    f"{skill_name}"
                )

            if skill_name in seen:
                continue

            pool_names.append(
                skill_name
            )

            seen.add(
                skill_name
            )

    if not pool_names:

        raise RuntimeError(
            "❌ Task 4没有任何analysis型Skill"
        )

    pool = []

    for name in pool_names:

        skill = skills[name]

        pool.append(
            skill
        )

    return (
        pool,
        normalized
    )


# ============================================================
# BUILD ROUTER SUMMARY FOR AI
# ============================================================

def build_router_summary(
    route_config
) -> str:
    """
    把Router转换成AI容易理解的候选关系。

    不把output型Skill送给Task 4。
    """

    routes = route_config[
        "routes"
    ]

    lines = []

    for route_name, route_data in routes.items():

        role = str(
            route_data.get(
                "role",
                "analysis"
            )
        ).strip()

        if role != "analysis":
            continue

        route_skills = route_data.get(
            "skills",
            []
        )

        names = []

        for name in route_skills:

            skill_name = str(
                name
            ).strip()

            if skill_name:
                names.append(
                    skill_name
                )

        if not names:
            continue

        lines.append(
            f"- {route_name}: "
            + "、".join(names)
        )

    return "\n".join(
        lines
    )


# ============================================================
# BUILD SKILL CONTEXT
# ============================================================

def build_skill_context(
    skill_pool
) -> str:
    """
    把所有候选分析Skill的规则提供给AI。

    为防止Prompt无限增长，
    使用总字符上限。
    """

    blocks = []
    total = 0

    for skill in skill_pool:

        name = skill_name_from_object(
            skill
        )

        content = str(
            skill.get(
                "content",
                ""
            )
        ).strip()

        block = (
            "\n"
            "==================================================\n"
            f"SKILL: {name}\n"
            "==================================================\n"
            f"{content}\n"
        )

        remaining = (
            MAX_SKILL_CONTEXT
            - total
        )

        if remaining <= 0:
            break

        if len(block) > remaining:

            block = block[
                :remaining
            ]

        blocks.append(
            block
        )

        total += len(
            block
        )

    if not blocks:

        raise RuntimeError(
            "❌ Task 4无法建立Skill上下文"
        )

    return "".join(
        blocks
    )


# ============================================================
# SAFE JSON EXTRACTION
# ============================================================

def extract_json_object(
    text: str
):
    """
    从AI返回结果中提取JSON对象。

    优先：

        ```json
        {...}
        ```

    其次直接寻找：

        {...}
    """

    raw = str(
        text or ""
    ).strip()

    if not raw:

        raise RuntimeError(
            "❌ Task 4 AI返回为空"
        )

    # --------------------------------------------------------
    # 1. Markdown code block
    # --------------------------------------------------------

    match = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        raw,
        re.DOTALL
    )

    if match:

        candidate = match.group(
            1
        ).strip()

        try:

            value = json.loads(
                candidate
            )

            if isinstance(
                value,
                dict
            ):

                return value

        except json.JSONDecodeError:
            pass

    # --------------------------------------------------------
    # 2. 直接寻找第一个完整JSON对象
    # --------------------------------------------------------

    start = raw.find(
        "{"
    )

    if start >= 0:

        depth = 0
        in_string = False
        escaped = False

        for index in range(
            start,
            len(raw)
        ):

            char = raw[index]

            if in_string:

                if escaped:

                    escaped = False

                elif char == "\\":
                    escaped = True

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

                    candidate = raw[
                        start:index + 1
                    ]

                    try:

                        value = json.loads(
                            candidate
                        )

                        if isinstance(
                            value,
                            dict
                        ):

                            return value

                    except json.JSONDecodeError:
                        break

    raise RuntimeError(
        "❌ Task 4无法解析AI返回的JSON："
        f"{raw[:1000]}"
    )


# ============================================================
# VALIDATE AI ROUTING RESULT
# ============================================================

def validate_ai_routing(
    data,
    available_names,
    min_skills,
    max_skills
):
    """
    验证AI选择的Skills。

    要求：

        selected_skills
            必须存在于候选池

        数量：
            min <= n <= max
    """

    if not isinstance(
        data,
        dict
    ):

        raise RuntimeError(
            "❌ Task 4 AI routing结果不是dict"
        )

    event_types = data.get(
        "event_types",
        []
    )

    if not isinstance(
        event_types,
        list
    ):

        event_types = []

    event_types = [
        str(x).strip()
        for x in event_types
        if str(x).strip()
    ]

    selected = data.get(
        "selected_skills",
        []
    )

    if not isinstance(
        selected,
        list
    ):

        raise RuntimeError(
            "❌ Task 4 AI没有返回selected_skills数组"
        )

    cleaned = []

    seen = set()

    for item in selected:

        name = str(
            item
        ).strip()

        if not name:
            continue

        if name not in available_names:

            raise RuntimeError(
                "❌ Task 4 AI选择了不存在或非候选Skill："
                f"{name}"
            )

        if name in seen:
            continue

        cleaned.append(
            name
        )

        seen.add(
            name
        )

    if not (
        min_skills
        <= len(cleaned)
        <= max_skills
    ):

        raise RuntimeError(
            "❌ Task 4 AI选择Skill数量异常："
            f"{len(cleaned)} "
            f"期望范围={min_skills}-{max_skills} "
            f"selected={cleaned}"
        )

    analysis = data.get(
        "analysis",
        {}
    )

    if not isinstance(
        analysis,
        dict
    ):

        raise RuntimeError(
            "❌ Task 4 AI的analysis必须是dict"
        )

    return {
        "event_types": event_types,
        "analysis_needs": data.get(
            "analysis_needs",
            []
        ),
        "selected_skills": cleaned,
        "analysis": analysis,
    }


# ============================================================
# NORMALIZE ANALYSIS VALUE
# ============================================================

def normalize_analysis_value(
    value
) -> str:
    """
    将AI JSON中的字段安全转换为Markdown文本。
    """

    if value is None:

        return "暂无"

    if isinstance(
        value,
        str
    ):

        text = value.strip()

        return text if text else "暂无"

    if isinstance(
        value,
        list
    ):

        items = []

        for item in value:

            text = normalize_analysis_value(
                item
            )

            if text != "暂无":

                items.append(
                    text
                )

        if not items:
            return "暂无"

        return "\n".join(
            f"- {item}"
            for item in items
        )

    if isinstance(
        value,
        dict
    ):

        lines = []

        for key, item in value.items():

            text = normalize_analysis_value(
                item
            )

            lines.append(
                f"### {key}\n{text}"
            )

        if not lines:
            return "暂无"

        return "\n\n".join(
            lines
        )

    return str(
        value
    )


# ============================================================
# BUILD ANALYSIS MARKDOWN
# ============================================================

def build_analysis_markdown(
    date: str,
    language: str,
    event_metadata,
    event_path: Path,
    routing
) -> str:
    """
    将AI结构化结果转换为正式Analysis.md。

    Analysis.md是Task 4的正式标准接口。
    """

    event_id = validate_event_id(
        event_metadata.get(
            "event_id",
            ""
        ),
        date
    )

    event_title = str(
        event_metadata.get(
            "event_title",
            ""
        )
    ).strip()

    if not event_title:

        event_title = event_id

    event_types = routing.get(
        "event_types",
        []
    )

    analysis_needs = routing.get(
        "analysis_needs",
        []
    )

    selected_skills = routing.get(
        "selected_skills",
        []
    )

    analysis = routing.get(
        "analysis",
        {}
    )

    if not isinstance(
        event_types,
        list
    ):

        event_types = []

    if not isinstance(
        analysis_needs,
        list
    ):

        analysis_needs = []

    if not isinstance(
        selected_skills,
        list
    ):

        selected_skills = []

    summary = normalize_analysis_value(
        analysis.get(
            "executive_summary",
            analysis.get(
                "summary",
                ""
            )
        )
    )

    key_facts = normalize_analysis_value(
        analysis.get(
            "key_facts",
            []
        )
    )

    causes = normalize_analysis_value(
        analysis.get(
            "causes",
            []
        )
    )

    impacts = normalize_analysis_value(
        analysis.get(
            "impacts",
            []
        )
    )

    risks = normalize_analysis_value(
        analysis.get(
            "risks",
            []
        )
    )

    opportunities = normalize_analysis_value(
        analysis.get(
            "opportunities",
            []
        )
    )

    short_term = normalize_analysis_value(
        analysis.get(
            "short_term_trends",
            []
        )
    )

    long_term = normalize_analysis_value(
        analysis.get(
            "long_term_trends",
            []
        )
    )

    strategic = normalize_analysis_value(
        analysis.get(
            "strategic_implications",
            []
        )
    )

    decision = normalize_analysis_value(
        analysis.get(
            "decision_implications",
            []
        )
    )

    entities = normalize_analysis_value(
        analysis.get(
            "key_entities",
            []
        )
    )

    uncertainty = normalize_analysis_value(
        analysis.get(
            "uncertainties",
            []
        )
    )

    follow_up = normalize_analysis_value(
        analysis.get(
            "follow_up",
            []
        )
    )

    lines = []

    lines.append(
        "---"
    )

    lines.append(
        f"date: {date}"
    )

    lines.append(
        f"language: {language}"
    )

    lines.append(
        f"event_id: {event_id}"
    )

    lines.append(
        "type: event_analysis"
    )

    lines.append(
        "status: completed"
    )

    lines.append(
        f"source_event_unit: {event_path.name}"
    )

    lines.append(
        f"created_at: {now().isoformat()}"
    )

    lines.append(
        f"timezone: {TIMEZONE_NAME}"
    )

    lines.append(
        "---"
    )

    lines.append(
        ""
    )

    lines.append(
        f"# {event_title} — Event Analysis"
    )

    lines.append(
        ""
    )

    lines.append(
        "## Event"
    )

    lines.append(
        ""
    )

    lines.append(
        f"- Event ID: `{event_id}`"
    )

    lines.append(
        f"- Date: `{date}`"
    )

    lines.append(
        f"- Language: `{language}`"
    )

    lines.append(
        ""
    )

    lines.append(
        "## Event Types"
    )

    lines.append(
        ""
    )

    if event_types:

        for item in event_types:

            lines.append(
                f"- {item}"
            )

    else:

        lines.append(
            "- 未明确分类"
        )

    lines.append(
        ""
    )

    lines.append(
        "## Analysis Needs"
    )

    lines.append(
        ""
    )

    if isinstance(
        analysis_needs,
        list
    ) and analysis_needs:

        for item in analysis_needs:

            lines.append(
                f"- {item}"
            )

    else:

        lines.append(
            "- 未明确"
        )

    lines.append(
        ""
    )

    lines.append(
        "## Applied Skills"
    )

    lines.append(
        ""
    )

    for skill in selected_skills:

        lines.append(
            f"- {skill}"
        )

    lines.append(
        ""
    )

    lines.append(
        "## Executive Summary"
    )

    lines.append(
        ""
    )

    lines.append(
        summary
    )

    lines.append(
        ""
    )

    lines.append(
        "## Key Facts"
    )

    lines.append(
        ""
    )

    lines.append(
        key_facts
    )

    lines.append(
        ""
    )

    lines.append(
        "## Causes"
    )

    lines.append(
        ""
    )

    lines.append(
        causes
    )

    lines.append(
        ""
    )

    lines.append(
        "## Impacts"
    )

    lines.append(
        ""
    )

    lines.append(
        impacts
    )

    lines.append(
        ""
    )

    lines.append(
        "## Risks"
    )

    lines.append(
        ""
    )

    lines.append(
        risks
    )

    lines.append(
        ""
    )

    lines.append(
        "## Opportunities"
    )

    lines.append(
        ""
    )

    lines.append(
        opportunities
    )

    lines.append(
        ""
    )

    lines.append(
        "## Short-Term Trends"
    )

    lines.append(
        ""
    )

    lines.append(
        short_term
    )

    lines.append(
        ""
    )

    lines.append(
        "## Long-Term Trends"
    )

    lines.append(
        ""
    )

    lines.append(
        long_term
    )

    lines.append(
        ""
    )

    lines.append(
        "## Strategic Implications"
    )

    lines.append(
        ""
    )

    lines.append(
        strategic
    )

    lines.append(
        ""
    )

    lines.append(
        "## Decision Implications"
    )

    lines.append(
        ""
    )

    lines.append(
        decision
    )

    lines.append(
        ""
    )

    lines.append(
        "## Key Entities"
    )

    lines.append(
        ""
    )

    lines.append(
        entities
    )

    lines.append(
        ""
    )

    lines.append(
        "## Uncertainties"
    )

    lines.append(
        ""
    )

    lines.append(
        uncertainty
    )

    lines.append(
        ""
    )

    lines.append(
        "## Follow-up"
    )

    lines.append(
        ""
    )

    lines.append(
        follow_up
    )

    lines.append(
        ""
    )

    lines.append(
        "## Source EventUnit"
    )

    lines.append(
        ""
    )

    lines.append(
        f"`{event_path.name}`"
    )

    lines.append(
        ""
    )

    return "\n".join(
        lines
    )


# ============================================================
# SINGLE EVENT AI PROCESSING
# ============================================================

def analyze_one_event(
    date: str,
    language: str,
    event,
    skill_pool,
    route_config
):
    """
    一个EventUnit只进行一次AI调用。

    AI同时完成：

        1. 事件分类
        2. 分析需求判断
        3. Skill选择
        4. 综合分析

    返回：

        routing result
    """

    event_metadata, event_path, content = (
        read_event_unit(event)
    )

    event_id = validate_event_id(
        event_metadata.get(
            "event_id",
            ""
        ),
        date
    )

    event_title = str(
        event_metadata.get(
            "event_title",
            ""
        )
    ).strip()

    if not event_title:

        event_title = event_id

    min_skills = route_config[
        "selection"
    ][
        "min_skills"
    ]

    max_skills = route_config[
        "selection"
    ][
        "max_skills"
    ]

    router_summary = build_router_summary(
        route_config
    )

    skill_context = build_skill_context(
        skill_pool
    )

    event_context = content[
        :MAX_EVENT_CONTEXT
    ]

    prompt = f"""
你是748686自生长知识系统V6.5.3的Event Analysis Engine。

你的任务不是单独执行27个Skill。

你的任务是：

    1. 阅读一个完整EventUnit。
    2. 判断这个事件属于哪些分析类型。
    3. 判断这个事件真正需要分析什么。
    4. 从Router提供的候选Skills中选择最适合的
       {min_skills}～{max_skills}个。
    5. 使用这些Skills的思想和方法，
       对整个EventUnit进行一次综合分析。
    6. 输出结构化JSON。

============================================================
事件
============================================================

Event ID：
{event_id}

事件标题：
{event_title}

============================================================
Skill Router
============================================================

下面是系统定义的分析路线。

{router_summary}

============================================================
候选分析Skills
============================================================

下面是候选Skill的方法规则。

{skill_context}

============================================================
完整 EventUnit
============================================================

{event_context}

============================================================
严格要求
============================================================

1. 只能依据EventUnit中的信息。
2. 不得编造EventUnit之外的事实。
3. 如果资料不足，明确写“资料不足”或“不确定”。
4. 可以进行逻辑推理，但必须区分：
       已知事实
       合理推断
       不确定事项
5. 不要为了凑数量而选择Skill。
6. selected_skills必须从候选Skill中选择。
7. 必须选择{min_skills}～{max_skills}个Skill。
8. 不要选择output型Skill。
9. 不需要逐个机械执行Skill。
10. 多个Skill应该综合起来形成一份统一分析。
11. 不要重复EventUnit全文。
12. 不要生成日报。
13. 不要生成周报。
14. 不要生成小红书文章。
15. 不要生成营销文案。
16. 当前任务只负责“事件理解与分析”。

============================================================
必须返回JSON
============================================================

{
  "event_types": [
    "新闻",
    "商业"
  ],

  "analysis_needs": [
    "影响分析",
    "风险分析",
    "趋势判断"
  ],

  "selected_skills": [
    "SWOT分析.md",
    "情景规划.md"
  ],

  "analysis": {
    "executive_summary": "",
    "key_facts": [],
    "causes": [],
    "impacts": [],
    "risks": [],
    "opportunities": [],
    "short_term_trends": [],
    "long_term_trends": [],
    "strategic_implications": [],
    "decision_implications": [],
    "key_entities": [],
    "uncertainties": [],
    "follow_up": []
  }
}

只返回JSON。
不要返回JSON之外的解释。
"""

    system_prompt = (
        "你是748686自生长知识系统V6.5.3 "
        "Event Analysis Engine。"
        "你必须严格依据EventUnit。"
        "不得编造事实。"
        "必须按照指定JSON结构输出。"
    )

    result = call_ai(
        prompt,
        system_prompt,
        0.2
    )

    if result is None:

        raise RuntimeError(
            "❌ Task 4 AI返回None："
            f"{event_id}"
        )

    raw_result = str(
        result
    ).strip()

    if not raw_result:

        raise RuntimeError(
            "❌ Task 4 AI返回空结果："
            f"{event_id}"
        )

    parsed = extract_json_object(
        raw_result
    )

    available_names = {
        skill_name_from_object(skill)
        for skill in skill_pool
    }

    return validate_ai_routing(
        parsed,
        available_names,
        min_skills,
        max_skills
    )


# ============================================================
# ATOMIC WRITE
# ============================================================

def atomic_write_text(
    path: Path,
    content: str
):
    """
    原子写入。
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:

        tmp.write_text(
            content,
            encoding="utf-8"
        )

        tmp.replace(
            path
        )

    except Exception:

        try:

            if tmp.exists():
                tmp.unlink()

        except Exception:
            pass

        raise


# ============================================================
# COMPLETION MARKER
# ============================================================

def skills_marker_path(
    date: str,
    language: str
) -> Path:
    """
    Task 4完成标记：

        event_units/_SKILLS_COMPLETE
    """

    lang = validate_language(
        language
    )

    date = validate_date(
        date
    )

    root = event_units_dir(
        date,
        lang
    )

    if root.name != "event_units":

        raise RuntimeError(
            "❌ Task 4 event_units目录大小写错误："
            f"{root}"
        )

    if root.parent.name != lang:

        raise RuntimeError(
            "❌ Task 4语言目录大小写错误："
            f"{root.parent}"
        )

    return (
        root
        / SKILLS_COMPLETE_FILE
    )


# ============================================================
# FIND MISSING ANALYSIS
# ============================================================

def find_missing_analysis(
    date: str,
    language: str,
    files
):
    """
    检查：

        EventUnit数量
        =
        有效Analysis数量

    返回缺失Analysis的Event ID。
    """

    missing = []

    for event_metadata, event_path in files:

        event_id = validate_event_id(
            event_metadata.get(
                "event_id",
                ""
            ),
            date
        )

        output = event_analysis_output_path(
            date,
            language,
            event_id
        )

        if not analysis_output_valid(
            output
        ):

            missing.append(
                f"{event_id}/{output.name}"
            )

    return missing


# ============================================================
# WRITE COMPLETION MARKER
# ============================================================

def write_skills_complete_marker(
    date: str,
    language: str,
    event_count: int,
    analysis_count: int,
    skill_pool_count: int
):
    """
    所有EventUnit Analysis完成后，
    写入Task 4完成标记。
    """

    lang = validate_language(
        language
    )

    path = skills_marker_path(
        date,
        lang
    )

    content = (
        "SKILLS_COMPLETE\n"
        f"date: {date}\n"
        f"language: {lang}\n"
        f"events: {event_count}\n"
        f"analysis_files: {analysis_count}\n"
        f"analysis_skill_pool: {skill_pool_count}\n"
        "processing_model: "
        "one_eventunit_one_ai_analysis\n"
        "output_model: "
        "one_eventunit_one_analysis_markdown\n"
        "directory_contract: "
        "language_lowercase_eventunit_EventUnit_event_units_lowercase\n"
        f"completed_at: {now().isoformat()}\n"
        f"timezone: {TIMEZONE_NAME}\n"
    )

    atomic_write_text(
        path,
        content
    )

    return path


# ============================================================
# FINAL OUTPUT COUNT
# ============================================================

def count_valid_analysis(
    date: str,
    language: str,
    files
) -> int:
    """
    统计有效Analysis数量。
    """

    count = 0

    for event_metadata, _ in files:

        event_id = validate_event_id(
            event_metadata.get(
                "event_id",
                ""
            ),
            date
        )

        output = event_analysis_output_path(
            date,
            language,
            event_id
        )

        if analysis_output_valid(
            output
        ):

            count += 1

    return count


# ============================================================
# TASK 4 MAIN
# ============================================================

def run_task_4(
    date: str,
    language: str
):
    """
    Task 4主流程：

        Task 3 EventUnits
                ↓
        Skill Router
                ↓
        Analysis Skill Pool
                ↓
        EventUnit
                ↓
        一次AI
                ↓
        Analysis.md
                ↓
        完整性验证
                ↓
        _SKILLS_COMPLETE
    """

    # --------------------------------------------------------
    # 1. 严格验证
    # --------------------------------------------------------

    date = validate_date(
        date
    )

    lang = validate_language(
        language
    )

    print(
        "\n" + "=" * 76
    )

    print(
        "TASK 4 — EVENT ANALYSIS"
    )

    print(
        "=" * 76
    )

    print(
        f"DATE     : {date}"
    )

    print(
        f"LANGUAGE : {lang}"
    )

    print(
        "MODEL    : EventUnit → Router → "
        "Selected Skills → Analysis.md"
    )

    print(
        "=" * 76
    )

    # --------------------------------------------------------
    # 2. 加载Task 3 EventUnits
    # --------------------------------------------------------

    files = load_saved_event_units(
        date,
        lang
    )

    if not isinstance(
        files,
        list
    ):

        raise RuntimeError(
            "❌ Task 4 EventUnit读取结果异常："
            f"{date}/{lang}"
        )

    if not files:

        raise RuntimeError(
            "❌ Task 4没有找到可处理EventUnit："
            f"{date}/{lang}"
        )

    # --------------------------------------------------------
    # 3. 验证EventUnits
    # --------------------------------------------------------

    seen_event_ids = set()

    for event_metadata, event_path in files:

        event_id = validate_event_id(
            event_metadata.get(
                "event_id",
                ""
            ),
            date
        )

        if event_id in seen_event_ids:

            raise RuntimeError(
                "❌ Task 4发现重复Event ID："
                f"{event_id}"
            )

        seen_event_ids.add(
            event_id
        )

        if not event_path.exists():

            raise RuntimeError(
                "❌ Task 4 EventUnit文件不存在："
                f"{event_path}"
            )

        if not event_path.is_file():

            raise RuntimeError(
                "❌ Task 4 EventUnit不是普通文件："
                f"{event_path}"
            )

        if event_path.stat().st_size <= 0:

            raise RuntimeError(
                "❌ Task 4 EventUnit为空："
                f"{event_path}"
            )

    # --------------------------------------------------------
    # 4. 加载Skills
    # --------------------------------------------------------

    skills = load_skills()

    validate_all_skills(
        skills
    )

    # --------------------------------------------------------
    # 5. 加载Router
    # --------------------------------------------------------

    raw_routes = load_routes()

    route_config = validate_routes(
        skills,
        raw_routes
    )

    # --------------------------------------------------------
    # 6. 建立Analysis Skill Pool
    # --------------------------------------------------------

    skill_pool, route_config = (
        build_analysis_skill_pool(
            skills,
            route_config
        )
    )

    min_skills = route_config[
        "selection"
    ][
        "min_skills"
    ]

    max_skills = route_config[
        "selection"
    ][
        "max_skills"
    ]

    # --------------------------------------------------------
    # 7. 基本信息
    # --------------------------------------------------------

    total_events = len(
        files
    )

    print(
        "\nTASK 4 CONFIG"
    )

    print(
        f"Events              : {total_events}"
    )

    print(
        f"Analysis Skill Pool : {len(skill_pool)}"
    )

    print(
        f"AI Skill Selection  : "
        f"{min_skills} - {max_skills}"
    )

    print(
        f"EventUnit root      : "
        f"{event_units_dir(date, lang)}"
    )

    print(
        f"Completion marker   : "
        f"{skills_marker_path(date, lang)}"
    )

    print(
        "\nAnalysis Skill Pool:"
    )

    for index, skill in enumerate(
        skill_pool,
        1
    ):

        print(
            f"  {index:02d}. "
            f"{skill_name_from_object(skill)}"
        )

    # --------------------------------------------------------
    # 8. 创建标准目录
    # --------------------------------------------------------

    outroot = event_units_dir(
        date,
        lang
    )

    outroot.mkdir(
        parents=True,
        exist_ok=True
    )

    if outroot.name != "event_units":

        raise RuntimeError(
            "❌ Task 4目录契约失败："
            f"实际={outroot.name}"
        )

    if outroot.parent.name != lang:

        raise RuntimeError(
            "❌ Task 4语言目录契约失败："
            f"实际={outroot.parent.name} "
            f"期望={lang}"
        )

    # --------------------------------------------------------
    # 9. 检查完成Marker
    # --------------------------------------------------------

    marker = skills_marker_path(
        date,
        lang
    )

    existing_missing = (
        find_missing_analysis(
            date,
            lang,
            files
        )
    )

    if (
        marker.exists()
        and not existing_missing
    ):

        print(
            "\n♻️ TASK 4已经完整完成"
        )

        print(
            f"   Date     : {date}"
        )

        print(
            f"   Language : {lang}"
        )

        print(
            f"   Events   : {total_events}"
        )

        print(
            f"   Analysis : {total_events}"
        )

        print(
            f"   Marker   : {marker}"
        )

        return True

    # --------------------------------------------------------
    # 10. Marker存在但Analysis缺失
    # --------------------------------------------------------

    if (
        marker.exists()
        and existing_missing
    ):

        print(
            "\n⚠️ 检测到旧的"
            "_SKILLS_COMPLETE"
            "，但Analysis完整性检查失败。"
        )

        print(
            f"   缺失/空Analysis："
            f"{len(existing_missing)}"
        )

        print(
            "   🔧 删除旧完成标记，进入增量修复。"
        )

        try:

            marker.unlink()

        except OSError as e:

            raise RuntimeError(
                "❌ 无法删除旧完成标记："
                f"{marker}"
            ) from e

    # --------------------------------------------------------
    # 11. EventUnit逐个分析
    # --------------------------------------------------------

    generated = 0
    skipped = 0

    for event_index, event in enumerate(
        files,
        1
    ):

        event_metadata, event_path, _ = (
            read_event_unit(event)
        )

        event_id = validate_event_id(
            event_metadata.get(
                "event_id",
                ""
            ),
            date
        )

        event_title = str(
            event_metadata.get(
                "event_title",
                ""
            )
        ).strip()

        output = event_analysis_output_path(
            date,
            lang,
            event_id
        )

        print(
            "\n" + "-" * 76
        )

        print(
            f"EVENT {event_index}/{total_events}"
        )

        print(
            f"EVENT ID : {event_id}"
        )

        print(
            f"TITLE    : {event_title}"
        )

        print(
            f"INPUT    : {event_path}"
        )

        print(
            f"OUTPUT   : {output}"
        )

        print(
            "-" * 76
        )

        # ----------------------------------------------------
        # 已经完成
        # ----------------------------------------------------

        if analysis_output_valid(
            output
        ):

            skipped += 1

            print(
                "⏭️ Analysis已经存在，跳过AI："
                f"{output.name}"
            )

            continue

        # ----------------------------------------------------
        # AI一次综合处理
        # ----------------------------------------------------

        print(
            "🤖 AI正在执行："
            "事件分类 + Skill选择 + 综合分析"
        )

        routing = analyze_one_event(
            date,
            lang,
            event,
            skill_pool,
            route_config
        )

        selected_skills = routing[
            "selected_skills"
        ]

        print(
            "   Event Types:"
        )

        for item in routing[
            "event_types"
        ]:

            print(
                f"      - {item}"
            )

        print(
            "   Selected Skills:"
        )

        for item in selected_skills:

            print(
                f"      - {item}"
            )

        # ----------------------------------------------------
        # 生成正式Analysis Markdown
        # ----------------------------------------------------

        analysis_markdown = (
            build_analysis_markdown(
                date,
                lang,
                event_metadata,
                event_path,
                routing
            )
        )

        if not analysis_markdown.strip():

            raise RuntimeError(
                "❌ Task 4生成Analysis内容为空："
                f"{event_id}"
            )

        # ----------------------------------------------------
        # 原子写入
        # ----------------------------------------------------

        atomic_write_text(
            output,
            analysis_markdown
        )

        # ----------------------------------------------------
        # 写入后验证
        # ----------------------------------------------------

        if not analysis_output_valid(
            output
        ):

            raise RuntimeError(
                "❌ Task 4 Analysis保存验证失败："
                f"{output}"
            )

        generated += 1

        print(
            f"   ✅ Analysis已保存："
            f"{output}"
        )

    # --------------------------------------------------------
    # 12. 最终完整性检查
    # --------------------------------------------------------

    print(
        "\n" + "=" * 76
    )

    print(
        "TASK 4 FINAL COMPLETENESS CHECK"
    )

    print(
        "=" * 76
    )

    missing = (
        find_missing_analysis(
            date,
            lang,
            files
        )
    )

    if missing:

        print(
            "❌ TASK 4完整性检查失败"
        )

        print(
            f"   Missing/Empty Analysis : "
            f"{len(missing)}"
        )

        for item in missing[:30]:

            print(
                f"   - {item}"
            )

        raise RuntimeError(
            "❌ TASK 4仍有缺失Analysis："
            f"{missing[:30]}"
        )

    # --------------------------------------------------------
    # 13. 数量检查
    # --------------------------------------------------------

    expected_outputs = (
        total_events
    )

    actual_outputs = count_valid_analysis(
        date,
        lang,
        files
    )

    print(
        f"Expected Analysis : "
        f"{expected_outputs}"
    )

    print(
        f"Actual Analysis   : "
        f"{actual_outputs}"
    )

    if actual_outputs != expected_outputs:

        raise RuntimeError(
            "❌ TASK 4 Analysis数量异常："
            f"actual={actual_outputs} "
            f"expected={expected_outputs}"
        )

    # --------------------------------------------------------
    # 14. 写入最终完成Marker
    # --------------------------------------------------------

    marker = write_skills_complete_marker(
        date,
        lang,
        total_events,
        actual_outputs,
        len(skill_pool)
    )

    # --------------------------------------------------------
    # 15. Marker最终验证
    # --------------------------------------------------------

    if (
        not marker.exists()
        or marker.stat().st_size <= 0
    ):

        raise RuntimeError(
            "❌ TASK 4完成标记写入失败："
            f"{marker}"
        )

    # --------------------------------------------------------
    # 16. 最终输出
    # --------------------------------------------------------

    print(
        "\n" + "=" * 76
    )

    print(
        "✅ TASK 4 COMPLETE"
    )

    print(
        "=" * 76
    )

    print(
        f"DATE              : {date}"
    )

    print(
        f"LANGUAGE          : {lang}"
    )

    print(
        f"EVENTS            : {total_events}"
    )

    print(
        f"ANALYSIS SKILL POOL : "
        f"{len(skill_pool)}"
    )

    print(
        f"EXPECTED ANALYSIS : "
        f"{expected_outputs}"
    )

    print(
        f"ACTUAL ANALYSIS   : "
        f"{actual_outputs}"
    )

    print(
        f"GENERATED         : "
        f"{generated}"
    )

    print(
        f"SKIPPED           : "
        f"{skipped}"
    )

    print(
        f"MARKER            : "
        f"{marker}"
    )

    print(
        "=" * 76
    )

    return True


# ============================================================
# CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 4 "
            "- EventUnit Analysis V6.5.3"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help="处理日期，例如：2026-08-31"
    )

    parser.add_argument(
        "--language",
        required=True,
        choices=[
            "en",
            "zh",
        ],
        help="语言：en 或 zh"
    )

    args = parser.parse_args()

    try:

        run_task_4(
            args.date,
            args.language
        )

        return 0

    except KeyboardInterrupt:

        print(
            "\n❌ TASK 4被用户中断"
        )

        return 130

    except Exception as e:

        print(
            f"\n❌ TASK 4 FAILED: {e}"
        )

        return 1


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )
