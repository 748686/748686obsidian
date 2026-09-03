#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4
27 Skills Processing
V6.5.3

============================================================
目录 / 语言大小写最终契约
============================================================

一、语言协议
------------------------------------------------------------

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
    eN
    zH

禁止：

    lower()
    upper()
    casefold()

禁止任何语言大小写自动转换。


二、磁盘语言目录
------------------------------------------------------------

磁盘目录永久锁死为：

    en
    zh

程序参数与磁盘目录完全一致。

因此不存在：

    EN -> en
    ZH -> zh

这种映射。


三、EventUnit根目录
------------------------------------------------------------

固定：

    YYYY-MM-DD-EventUnit/

注意：

    EventUnit 是正式目录协议。
    E / U 保持大写。

例如：

    2026-08-31-EventUnit/


四、语言目录
------------------------------------------------------------

固定：

    2026-08-31-EventUnit/en/
    2026-08-31-EventUnit/zh/


五、Task 3输出
------------------------------------------------------------

    YYYY-MM-DD-EventUnit/
        en/
            articles/
            event_units/
                EVT-YYYYMMDD-NNNNNN_Title.md
            _event_index.json
            _COMPLETE

        zh/
            articles/
            event_units/
                EVT-YYYYMMDD-NNNNNN_Title.md
            _event_index.json
            _COMPLETE


六、Task 4输出
------------------------------------------------------------

    YYYY-MM-DD-EventUnit/
        en/
            event_units/
                EVT-YYYYMMDD-NNNNNN/
                    SkillA.md
                    SkillB.md
                    ...
                _SKILLS_COMPLETE

        zh/
            event_units/
                EVT-YYYYMMDD-NNNNNN/
                    SkillA.md
                    SkillB.md
                    ...
                _SKILLS_COMPLETE


七、Event ID
------------------------------------------------------------

正式格式：

    EVT-YYYYMMDD-NNNNNN

例如：

    EVT-20260831-000001

EVT 必须保持大写。

Event ID 大小写属于 Global Event ID 正式协议，
不属于语言目录大小写协议。


八、断点续跑
------------------------------------------------------------

1. 已存在且非空 Skill 文件：
       直接跳过。

2. 不存在 Skill 文件：
       自动生成。

3. 空 Skill 文件：
       自动重新生成。

4. _SKILLS_COMPLETE 存在：
       仍然重新检查所有 Event × Skill。

5. marker 存在但有缺失：
       删除 marker。
       自动进入修复。

6. 只有全部 Event × Skill 完整：
       才允许写入 _SKILLS_COMPLETE。


九、严格原则
------------------------------------------------------------

Task 4 不负责修复 Task 3。

Task 4 只读取 Task 3 已完成 EventUnit。

如果 Task 3：

    _COMPLETE

不存在，

Task 4 直接失败。

============================================================
"""

from __future__ import annotations

import argparse
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

MAX_SKILL_CONTEXT = 30000

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

    不使用：

        lower()
        upper()
        casefold()
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
# SKILL FILE NAME
# ============================================================

def skill_output_filename(
    skill_name: str
) -> str:
    """
    将Skill名称转换成稳定Markdown文件名。

    不修改Skill名称大小写。

    safe_name()只负责文件系统安全字符处理。

    正式扩展名：

        .md
    """

    name = str(
        skill_name or ""
    ).strip()

    if not name:

        raise RuntimeError(
            "❌ Skill名称为空"
        )

    filename = safe_name(
        name
    ).strip()

    if not filename:

        raise RuntimeError(
            "❌ Skill名称无法生成安全文件名："
            f"{name}"
        )

    # --------------------------------------------------------
    # 只处理正式的小写 .md
    #
    # 不接受：
    #
    # .MD
    # .Md
    # .mD
    #
    # 因为系统禁止大小写自动归一化。
    # --------------------------------------------------------

    while filename.endswith(
        ".md"
    ):

        filename = filename[:-3]

    filename = filename.rstrip(".")

    if not filename:

        raise RuntimeError(
            "❌ Skill文件名无效："
            f"{name}"
        )

    return (
        f"{filename}.md"
    )


# ============================================================
# SKILL OUTPUT PATH
# ============================================================

def skill_event_dir(
    date: str,
    language: str,
    event_id: str
) -> Path:
    """
    Task 4单个Event的Skill输出目录。

    标准：

        YYYY-MM-DD-EventUnit/
            en/
                event_units/
                    EVT-YYYYMMDD-NNNNNN/

    或：

        YYYY-MM-DD-EventUnit/
            zh/
                event_units/
                    EVT-YYYYMMDD-NNNNNN/
    """

    lang = validate_language(
        language
    )

    eid = validate_event_id(
        event_id,
        date
    )

    root = event_units_dir(
        date,
        lang
    )

    # --------------------------------------------------------
    # 语言目录必须直接等于：
    #
    # en
    # zh
    # --------------------------------------------------------

    if root.parent.name != lang:

        raise RuntimeError(
            "❌ Task 4语言目录契约异常："
            f"实际={root.parent.name} "
            f"期望={lang}"
        )

    # --------------------------------------------------------
    # event_units必须固定小写
    # --------------------------------------------------------

    if root.name != "event_units":

        raise RuntimeError(
            "❌ Task 4 EventUnit目录契约异常："
            f"实际={root.name} "
            "期望=event_units"
        )

    return (
        root
        / eid
    )


# ============================================================
# SKILL OUTPUT VALIDATION
# ============================================================

def skill_output_valid(
    path: Path
) -> bool:
    """
    Skill输出文件有效性检查。

    必须满足：

        文件存在
        普通文件
        大小 > 0
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
# EVENT × SKILL OUTPUT PATH
# ============================================================

def event_skill_output_path(
    date: str,
    language: str,
    event_id: str,
    skill_name: str
) -> Path:
    """
    返回单个Event × Skill标准输出路径。
    """

    edir = skill_event_dir(
        date,
        language,
        event_id
    )

    filename = skill_output_filename(
        skill_name
    )

    return (
        edir
        / filename
    )


# ============================================================
# SINGLE SKILL AI PROCESSING
# ============================================================

def run_one_skill(
    event,
    skill
):
    """
    对单个EventUnit执行单个Skill。
    """

    event_metadata = event[0]
    event_path = event[1]

    content = event_path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    event_title = str(
        event_metadata.get(
            "event_title",
            ""
        )
    ).strip()

    event_id = str(
        event_metadata.get(
            "event_id",
            ""
        )
    ).strip()

    skill_name = str(
        skill.get(
            "name",
            ""
        )
    ).strip()

    skill_content = str(
        skill.get(
            "content",
            ""
        )
    )

    if not event_id:

        raise RuntimeError(
            "❌ EventUnit缺少event_id："
            f"{event_path}"
        )

    if not skill_name:

        raise RuntimeError(
            "❌ Skill缺少name"
        )

    if not skill_content.strip():

        raise RuntimeError(
            f"❌ Skill规则为空：{skill_name}"
        )

    prompt = f"""你正在执行748686自生长知识系统V6.5.3的27 Skills深度处理。

事件：
{event_title}

Event ID：
{event_id}

Skill名称：
{skill_name}

Skill规则：
{skill_content}

EventUnit原文：
{content[:MAX_SKILL_CONTEXT]}

请严格按照该Skill完成深度处理。

要求：
1. 严格执行Skill规则。
2. 不要编造。
3. 只使用EventUnit提供的信息。
4. 不得引入EventUnit之外未经提供的事实。
5. 如果资料不足，明确说明资料不足。
6. 输出可直接写入知识库的中文Markdown。
"""

    result = call_ai(
        prompt,
        (
            "你是748686知识系统Skill执行器。"
            "严格执行Skill规则。"
            "只依据EventUnit提供的信息。"
            "不得编造。"
        ),
        0.2
    )

    if result is None:

        return ""

    return str(
        result
    )


# ============================================================
# SKILL SELECTION
# ============================================================

def select_skills(
    skills,
    routes
):
    """
    根据skill_routes.json选择Task 4需要执行的Skills。

    规则：

    1. route引用的Skill必须存在。
    2. 重复Skill只执行一次。
    3. 如果routes没有选出Skill，
       则执行全部Skill。
    """

    if not isinstance(
        skills,
        dict
    ):

        raise RuntimeError(
            "❌ Skills配置格式异常：不是dict"
        )

    if not skills:

        raise RuntimeError(
            "❌ Skills配置为空"
        )

    if not isinstance(
        routes,
        dict
    ):

        raise RuntimeError(
            "❌ skill_routes.json格式异常：不是dict"
        )

    selected = []
    selected_names = set()

    for route_name, route_names in routes.items():

        if route_names is None:
            continue

        if not isinstance(
            route_names,
            list
        ):

            raise RuntimeError(
                "❌ skill_routes.json路由格式异常："
                f"{route_name}"
            )

        for name in route_names:

            skill_name = str(
                name
            ).strip()

            if not skill_name:
                continue

            if skill_name not in skills:

                raise RuntimeError(
                    "❌ skill_routes.json引用不存在Skill："
                    f"{skill_name}"
                )

            if skill_name in selected_names:
                continue

            selected.append(
                skills[skill_name]
            )

            selected_names.add(
                skill_name
            )

    # --------------------------------------------------------
    # 没有有效Route选择：
    # 执行全部Skill
    # --------------------------------------------------------

    if not selected:

        for name in sorted(
            skills.keys()
        ):

            selected.append(
                skills[name]
            )

    if not selected:

        raise RuntimeError(
            "❌ Task 4最终没有可执行Skill"
        )

    return selected


# ============================================================
# SKILL CONFIG VALIDATION
# ============================================================

def validate_selected_skills(
    selected
):
    """
    验证最终Skill列表。

    检查：

    - Skill对象
    - name
    - content
    - Skill名称重复
    - 文件名冲突
    """

    seen_names = set()
    seen_files = set()

    for index, skill in enumerate(
        selected,
        1
    ):

        if not isinstance(
            skill,
            dict
        ):

            raise RuntimeError(
                f"❌ Task 4 Skill[{index}]不是对象"
            )

        name = str(
            skill.get(
                "name",
                ""
            )
        ).strip()

        if not name:

            raise RuntimeError(
                f"❌ Task 4 Skill[{index}]缺少name"
            )

        if name in seen_names:

            raise RuntimeError(
                f"❌ Task 4存在重复Skill：{name}"
            )

        seen_names.add(
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
                f"❌ Task 4 Skill规则为空：{name}"
            )

        filename = skill_output_filename(
            name
        )

        # ----------------------------------------------------
        # 精确文件名匹配。
        #
        # 不使用：
        #
        # lower()
        # upper()
        # casefold()
        # ----------------------------------------------------

        if filename in seen_files:

            raise RuntimeError(
                "❌ Task 4存在Skill文件名冲突："
                f"{filename}"
            )

        seen_files.add(
            filename
        )


# ============================================================
# EXISTING OUTPUT COMPLETENESS
# ============================================================

def find_missing_skill_outputs(
    date: str,
    language: str,
    files,
    selected
):
    """
    扫描所有Event × Skill。

    返回缺失或空文件：

        [
            EVT-.../SkillA.md,
            ...
        ]
    """

    missing = []

    for event_metadata, _ in files:

        event_id = validate_event_id(
            str(
                event_metadata.get(
                    "event_id",
                    ""
                )
            ).strip(),
            date
        )

        for skill in selected:

            skill_name = str(
                skill.get(
                    "name",
                    ""
                )
            ).strip()

            path = event_skill_output_path(
                date,
                language,
                event_id,
                skill_name
            )

            if not skill_output_valid(
                path
            ):

                missing.append(
                    f"{event_id}/{path.name}"
                )

    return missing


# ============================================================
# COMPLETION MARKER
# ============================================================

def skills_marker_path(
    date: str,
    language: str
) -> Path:
    """
    Task 4完成标记。

    固定：

        event_units/_SKILLS_COMPLETE
    """

    lang = validate_language(
        language
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
# WRITE COMPLETION MARKER
# ============================================================

def write_skills_complete_marker(
    date: str,
    language: str,
    event_count: int,
    skill_count: int
):
    """
    所有Event × Skill完成后写入完成标记。
    """

    lang = validate_language(
        language
    )

    path = skills_marker_path(
        date,
        lang
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    content = (
        "SKILLS_COMPLETE\n"
        f"date: {date}\n"
        f"language: {lang}\n"
        f"events: {event_count}\n"
        f"skills: {skill_count}\n"
        "directory_contract: "
        "language_lowercase_eventunit_EventUnit_event_units_lowercase\n"
        f"completed_at: {now().isoformat()}\n"
        f"timezone: {TIMEZONE_NAME}\n"
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

    return path


# ============================================================
# TASK 4 MAIN
# ============================================================

def run_task_4(
    date: str,
    language: str
):
    """
    Task 4主流程。

    Date
      ↓
    Language en / zh
      ↓
    Task 3 EventUnits
      ↓
    Skill Routes
      ↓
    Skills
      ↓
    Event × Skill
      ↓
    Skill Markdown
      ↓
    完整性验证
      ↓
    _SKILLS_COMPLETE
    """

    # --------------------------------------------------------
    # 1. 严格验证语言
    # --------------------------------------------------------

    lang = validate_language(
        language
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "TASK 4 — 27 SKILLS"
    )

    print(
        "=" * 70
    )

    print(
        f"DATE     : {date}"
    )

    print(
        f"LANGUAGE : {lang}"
    )

    print(
        "=" * 70
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
            "❌ TASK 4 EventUnit读取结果异常："
            f"{date}/{lang}"
        )

    if not files:

        raise RuntimeError(
            "❌ TASK 4没有找到可处理EventUnit："
            f"{date}/{lang}"
        )

    # --------------------------------------------------------
    # 3. 验证所有Event ID
    # --------------------------------------------------------

    event_ids = []
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
                "❌ TASK 4发现重复Event ID："
                f"{event_id}"
            )

        seen_event_ids.add(
            event_id
        )

        event_ids.append(
            event_id
        )

        if not event_path.exists():

            raise RuntimeError(
                "❌ TASK 4 EventUnit文件不存在："
                f"{event_path}"
            )

        if event_path.stat().st_size <= 0:

            raise RuntimeError(
                "❌ TASK 4 EventUnit文件为空："
                f"{event_path}"
            )

    # --------------------------------------------------------
    # 4. 加载Skills
    # --------------------------------------------------------

    skills = load_skills()

    if not isinstance(
        skills,
        dict
    ):

        raise RuntimeError(
            "❌ TASK 4 load_skills()返回格式异常"
        )

    # --------------------------------------------------------
    # 5. 加载Routes
    # --------------------------------------------------------

    routes = load_routes()

    if not isinstance(
        routes,
        dict
    ):

        raise RuntimeError(
            "❌ TASK 4 load_routes()返回格式异常"
        )

    # --------------------------------------------------------
    # 6. 选择Skills
    # --------------------------------------------------------

    selected = select_skills(
        skills,
        routes
    )

    validate_selected_skills(
        selected
    )

    # --------------------------------------------------------
    # 7. 基本信息
    # --------------------------------------------------------

    print(
        "\nTASK 4 — 27 SKILLS"
        f" | Events={len(files)}"
        f" | Skills={len(selected)}"
        f" | DATE={date}"
        f" | LANGUAGE={lang}"
    )

    print(
        f"📁 EventUnit root:"
        f" {event_units_dir(date, lang)}"
    )

    print(
        f"📁 Completion marker:"
        f" {skills_marker_path(date, lang)}"
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

    # --------------------------------------------------------
    # 严格验证目录契约
    # --------------------------------------------------------

    if outroot.name != "event_units":

        raise RuntimeError(
            "❌ TASK 4目录契约失败："
            f"event_units实际={outroot.name}"
        )

    if outroot.parent.name != lang:

        raise RuntimeError(
            "❌ TASK 4语言目录契约失败："
            f"实际={outroot.parent.name} "
            f"期望={lang}"
        )

    # --------------------------------------------------------
    # 9. 检查完成标记
    #
    # marker存在：
    # 仍然必须验证全部Event × Skill。
    # --------------------------------------------------------

    marker = skills_marker_path(
        date,
        lang
    )

    existing_missing = (
        find_missing_skill_outputs(
            date,
            lang,
            files,
            selected
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
            f"   Events   : {len(files)}"
        )

        print(
            f"   Skills   : {len(selected)}"
        )

        print(
            f"   Marker   : {marker}"
        )

        return True

    # --------------------------------------------------------
    # 10. marker存在但文件缺失
    # --------------------------------------------------------

    if (
        marker.exists()
        and existing_missing
    ):

        print(
            "\n⚠️ 检测到旧的"
            "_SKILLS_COMPLETE"
            "，但完整性检查失败。"
        )

        print(
            f"   缺失/空文件："
            f"{len(existing_missing)}"
        )

        print(
            "   🔧 删除旧完成标记，"
            "进入增量修复。"
        )

        try:

            marker.unlink()

        except OSError as e:

            raise RuntimeError(
                "❌ 无法删除旧完成标记："
                f"{marker}"
            ) from e

    # --------------------------------------------------------
    # 11. Event × Skill执行
    # --------------------------------------------------------

    generated = 0
    skipped = 0

    total_events = len(
        files
    )

    total_skills = len(
        selected
    )

    for event_index, event in enumerate(
        files,
        1
    ):

        event_metadata = event[0]
        event_path = event[1]

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

        edir = skill_event_dir(
            date,
            lang,
            event_id
        )

        edir.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            "\n" + "-" * 70
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
            f"OUTPUT   : {edir}"
        )

        print(
            "-" * 70
        )

        for skill_index, skill in enumerate(
            selected,
            1
        ):

            skill_name = str(
                skill.get(
                    "name",
                    ""
                )
            ).strip()

            outfile = (
                event_skill_output_path(
                    date,
                    lang,
                    event_id,
                    skill_name
                )
            )

            # ------------------------------------------------
            # 已存在且非空
            # ------------------------------------------------

            if skill_output_valid(
                outfile
            ):

                skipped += 1

                print(
                    f"[{event_index}/{total_events}]"
                    f"[{skill_index}/{total_skills}] "
                    f"⏭️ 已存在："
                    f"{outfile.name}"
                )

                continue

            # ------------------------------------------------
            # 缺失：AI生成
            # ------------------------------------------------

            print(
                f"[{event_index}/{total_events}]"
                f"[{skill_index}/{total_skills}] "
                f"🤖 生成："
                f"{skill_name}"
            )

            result = run_one_skill(
                event,
                skill
            )

            result = str(
                result or ""
            ).strip()

            if not result:

                raise RuntimeError(
                    "❌ Skill结果为空："
                    f"{event_id} / "
                    f"{skill_name}"
                )

            # ------------------------------------------------
            # 原子写入
            # ------------------------------------------------

            outfile.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            tmp = outfile.with_name(
                outfile.name + ".tmp"
            )

            try:

                tmp.write_text(
                    result + "\n",
                    encoding="utf-8"
                )

                tmp.replace(
                    outfile
                )

            except Exception:

                try:

                    if tmp.exists():
                        tmp.unlink()

                except Exception:
                    pass

                raise

            # ------------------------------------------------
            # 写入后立即验证
            # ------------------------------------------------

            if not skill_output_valid(
                outfile
            ):

                raise RuntimeError(
                    "❌ Skill文件保存验证失败："
                    f"{outfile}"
                )

            generated += 1

            print(
                f"   ✅ 已保存："
                f"{outfile}"
            )

    # --------------------------------------------------------
    # 12. 最终完整性检查
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "TASK 4 FINAL COMPLETENESS CHECK"
    )

    print(
        "=" * 70
    )

    missing = (
        find_missing_skill_outputs(
            date,
            lang,
            files,
            selected
        )
    )

    if missing:

        print(
            "❌ TASK 4完整性检查失败"
        )

        print(
            f"   Missing/Empty : "
            f"{len(missing)}"
        )

        for item in missing[:30]:

            print(
                f"   - {item}"
            )

        raise RuntimeError(
            "❌ TASK 4仍有缺失Skill文件："
            f"{missing[:30]}"
        )

    # --------------------------------------------------------
    # 13. 最终检查数量
    # --------------------------------------------------------

    expected_outputs = (
        total_events
        * total_skills
    )

    actual_outputs = 0

    for event_metadata, _ in files:

        event_id = validate_event_id(
            event_metadata.get(
                "event_id",
                ""
            ),
            date
        )

        for skill in selected:

            skill_name = str(
                skill.get(
                    "name",
                    ""
                )
            ).strip()

            path = (
                event_skill_output_path(
                    date,
                    lang,
                    event_id,
                    skill_name
                )
            )

            if skill_output_valid(
                path
            ):

                actual_outputs += 1

    if actual_outputs != expected_outputs:

        raise RuntimeError(
            "❌ TASK 4输出数量异常："
            f"actual={actual_outputs} "
            f"expected={expected_outputs}"
        )

    # --------------------------------------------------------
    # 14. 写入最终完成标记
    # --------------------------------------------------------

    marker = write_skills_complete_marker(
        date,
        lang,
        total_events,
        total_skills
    )

    # --------------------------------------------------------
    # 15. 再次验证marker
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
        "\n" + "=" * 70
    )

    print(
        "✅ TASK 4 COMPLETE"
    )

    print(
        "=" * 70
    )

    print(
        f"DATE             : {date}"
    )

    print(
        f"LANGUAGE         : {lang}"
    )

    print(
        f"EVENTS           : {total_events}"
    )

    print(
        f"SKILLS           : {total_skills}"
    )

    print(
        f"EXPECTED OUTPUTS : {expected_outputs}"
    )

    print(
        f"ACTUAL OUTPUTS   : {actual_outputs}"
    )

    print(
        f"GENERATED        : {generated}"
    )

    print(
        f"SKIPPED          : {skipped}"
    )

    print(
        f"MARKER           : {marker}"
    )

    print(
        "=" * 70
    )

    return True


# ============================================================
# CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 4 "
            "- 27 Skills V6.5.3"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help="处理日期，例如：2026-08-30"
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
