#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 4
27 Skills Processing
V6.5.3

目录大小写契约：
------------------------------------------------------------
语言参数：
    EN / ZH

磁盘语言目录：
    en / zh

EventUnit目录：
    Raw News/
        YYYY-MM-DD-EventUnit/
            en/
                articles/
                event_units/
            zh/
                articles/
                event_units/

Task 4输出：
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

重要：
------------------------------------------------------------
1. EN / ZH 是程序接口标准值。
2. 磁盘目录永远使用小写 en / zh。
3. Event ID 永远使用：
       EVT-YYYYMMDD-NNNNNN
4. 不允许因为大小写不同产生第二套目录。
5. Task 4 只读取 Task 3 已完成的 EventUnit。
6. 已存在且非空的 Skill 文件直接跳过。
7. 缺失 Skill 自动补生成。
8. 最终只有全部 Event × Skill 完成后，
   才写入 _SKILLS_COMPLETE。
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
    normalize_language,
    now,
    event_units_dir,
)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_SKILL_CONTEXT = 30000

SUPPORTED_LANGUAGES = ("EN", "ZH")

EVENT_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

TIMEZONE_NAME = "Asia/Shanghai"


# ============================================================
# LANGUAGE / PATH CONTRACT
# ============================================================

def normalize_task_language(language: str) -> str:
    """
    Task 4统一语言入口。

    外部：
        EN / ZH

    内部：
        EN / ZH

    磁盘目录：
        en / zh

    绝不直接把用户输入拼接到路径中。
    """
    lang = normalize_language(language)

    if lang not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ Task 4不支持的语言：{language}"
        )

    return lang


def language_disk_name(language: str) -> str:
    """
    获取磁盘目录语言名称。

    EN -> en
    ZH -> zh
    """
    lang = normalize_task_language(language)
    return lang.lower()


# ============================================================
# EVENT ID VALIDATION
# ============================================================

def validate_event_id(event_id: str, date: str) -> str:
    """
    验证 Event ID。

    正式格式：
        EVT-YYYYMMDD-NNNNNN

    注意：
        Event ID 是大小写敏感的正式 Global ID。
        EVT 必须保持大写。
    """
    eid = str(event_id or "").strip()

    if not eid:
        raise RuntimeError(
            f"❌ {date} Task 4发现空event_id"
        )

    if not EVENT_ID_PATTERN.fullmatch(eid):
        raise RuntimeError(
            f"❌ {date} Task 4发现非法Global Event ID：{eid}"
        )

    expected_prefix = (
        f"EVT-{date.replace('-', '')}-"
    )

    if not eid.startswith(expected_prefix):
        raise RuntimeError(
            f"❌ {date} Task 4 Event ID日期不匹配：{eid}"
        )

    return eid


# ============================================================
# SKILL FILE NAME
# ============================================================

def skill_output_filename(skill_name: str) -> str:
    """
    将Skill名称转换成稳定的Markdown文件名。

    注意：
        不修改Skill本身的业务名称。
        只负责文件系统安全化。

    最终：
        xxx -> xxx.md
        xxx.md -> xxx.md
    """
    name = str(skill_name or "").strip()

    if not name:
        raise RuntimeError(
            "❌ Skill名称为空"
        )

    filename = safe_name(name).strip()

    if not filename:
        raise RuntimeError(
            f"❌ Skill名称无法生成安全文件名：{name}"
        )

    # 只移除末尾重复的 .md，
    # 避免出现 xxx.md.md
    while filename.lower().endswith(".md"):
        filename = filename[:-3]

    filename = filename.rstrip(".")

    if not filename:
        raise RuntimeError(
            f"❌ Skill文件名无效：{name}"
        )

    return f"{filename}.md"


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

    统一通过 knowledge_common.event_units_dir()
    获取 event_units 根目录。

    语言目录最终必须是：
        en
        zh
    """
    lang = normalize_task_language(language)
    eid = validate_event_id(event_id, date)

    root = event_units_dir(
        date,
        lang
    )

    # 防止公共函数发生大小写契约漂移。
    expected_language_dir = (
        root.parent.name
    )

    expected = language_disk_name(lang)

    if expected_language_dir != expected:
        raise RuntimeError(
            "❌ Task 4语言目录大小写契约异常："
            f"实际={expected_language_dir} "
            f"期望={expected}"
        )

    if root.name != "event_units":
        raise RuntimeError(
            "❌ Task 4 EventUnit目录大小写契约异常："
            f"实际={root.name} "
            "期望=event_units"
        )

    return root / eid


# ============================================================
# SKILL OUTPUT VALIDATION
# ============================================================

def skill_output_valid(path: Path) -> bool:
    """
    Skill输出文件有效性检查。

    只接受：
        文件存在
        且文件大小 > 0
    """
    try:
        return (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
        )
    except OSError:
        return False


def event_skill_output_path(
    date: str,
    language: str,
    event_id: str,
    skill_name: str
) -> Path:
    """
    返回单个 Event × Skill 的标准输出路径。
    """
    edir = skill_event_dir(
        date,
        language,
        event_id
    )

    filename = skill_output_filename(
        skill_name
    )

    return edir / filename


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
            f"❌ EventUnit缺少event_id：{event_path}"
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

    return str(result)


# ============================================================
# SKILL SELECTION
# ============================================================

def select_skills(
    skills,
    routes
):
    """
    根据 skill_routes.json 选择Task 4需要执行的Skills。

    规则：
    1. route中引用的Skill必须存在。
    2. 重复Skill只执行一次。
    3. 如果routes没有选出任何Skill，
       则执行skills中的全部Skill。
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

    # 如果routes没有有效选择，
    # 使用全部Skill。
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
    检查最终Skill列表。

    同时检查：
    - Skill对象
    - name
    - content
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

        seen_names.add(name)

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

        filename_key = filename.casefold()

        if filename_key in seen_files:
            raise RuntimeError(
                "❌ Task 4存在Skill文件名冲突："
                f"{filename}"
            )

        seen_files.add(
            filename_key
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
    扫描所有 Event × Skill，
    返回缺失或空文件。

    返回：
        [
            "EVT-.../SkillA.md",
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
# COMPLETION MARKER VALIDATION
# ============================================================

def skills_marker_path(
    date: str,
    language: str
) -> Path:
    """
    Task 4完成标记。

    必须位于：
        event_units/_SKILLS_COMPLETE
    """
    lang = normalize_task_language(
        language
    )

    root = event_units_dir(
        date,
        lang
    )

    if root.name != "event_units":
        raise RuntimeError(
            f"❌ Task 4 event_units目录大小写错误：{root}"
        )

    return root / SKILLS_COMPLETE_FILE


def write_skills_complete_marker(
    date: str,
    language: str,
    event_count: int,
    skill_count: int
):
    """
    所有Event × Skill完成后写入完成标记。
    """

    lang = normalize_task_language(
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
        f"disk_language: {lang.lower()}\n"
        f"events: {event_count}\n"
        f"skills: {skill_count}\n"
        "directory_contract: "
        "language_lowercase_event_units_lowercase\n"
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

    Processing Unit：

        Date
          ↓
        Language
          ↓
        Task 3 EventUnits
          ↓
        读取 EventUnit
          ↓
        Skill Routes
          ↓
        27 Skills
          ↓
        Event × Skill
          ↓
        知识库Skill Markdown
          ↓
        完整性验证
          ↓
        _SKILLS_COMPLETE
    """

    # --------------------------------------------------------
    # 1. 标准化语言
    # --------------------------------------------------------

    lang = normalize_task_language(
        language
    )

    disk_lang = language_disk_name(
        lang
    )

    print("\n" + "=" * 70)
    print("TASK 4 — 27 SKILLS")
    print("=" * 70)
    print(
        f"DATE          : {date}"
    )
    print(
        f"LANGUAGE      : {lang}"
    )
    print(
        f"DISK LANGUAGE : {disk_lang}"
    )
    print("=" * 70)

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
            f"❌ TASK 4 EventUnit读取结果异常："
            f"{date}/{lang}"
        )

    if not files:
        raise RuntimeError(
            f"❌ TASK 4没有找到可处理EventUnit："
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
                f"❌ TASK 4发现重复Event ID："
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
                f"❌ TASK 4 EventUnit文件不存在："
                f"{event_path}"
            )

        if event_path.stat().st_size <= 0:
            raise RuntimeError(
                f"❌ TASK 4 EventUnit文件为空："
                f"{event_path}"
            )

    # --------------------------------------------------------
    # 4. 加载Skills与Routes
    # --------------------------------------------------------

    skills = load_skills()

    if not isinstance(
        skills,
        dict
    ):
        raise RuntimeError(
            "❌ TASK 4 load_skills()返回格式异常"
        )

    routes = load_routes()

    if not isinstance(
        routes,
        dict
    ):
        raise RuntimeError(
            "❌ TASK 4 load_routes()返回格式异常"
        )

    selected = select_skills(
        skills,
        routes
    )

    validate_selected_skills(
        selected
    )

    # --------------------------------------------------------
    # 5. 基本信息
    # --------------------------------------------------------

    print(
        f"\nTASK 4 — 27 SKILLS"
        f" | Events={len(files)}"
        f" | Skills={len(selected)}"
        f" | DATE={date}"
        f" | LANGUAGE={lang}"
        f" | DISK={disk_lang}"
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
    # 6. 创建标准目录
    # --------------------------------------------------------

    outroot = event_units_dir(
        date,
        lang
    )

    outroot.mkdir(
        parents=True,
        exist_ok=True
    )

    # 严格验证磁盘目录大小写。
    if outroot.name != "event_units":
        raise RuntimeError(
            "❌ TASK 4目录契约失败："
            f"event_units实际={outroot.name}"
        )

    if outroot.parent.name != disk_lang:
        raise RuntimeError(
            "❌ TASK 4语言目录契约失败："
            f"实际={outroot.parent.name} "
            f"期望={disk_lang}"
        )

    # --------------------------------------------------------
    # 7. 先检查完成标记
    #
    # 注意：
    # 不能因为marker存在就直接跳过。
    # 必须再次验证所有 Event × Skill。
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
            f"   Disk     : {disk_lang}"
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
    # 8. 如果marker存在但文件缺失，
    #    删除旧marker，进入修复。
    # --------------------------------------------------------

    if marker.exists() and existing_missing:

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
                f"❌ 无法删除旧完成标记："
                f"{marker}"
            ) from e

    # --------------------------------------------------------
    # 9. Event × Skill执行
    # --------------------------------------------------------

    generated = 0
    skipped = 0

    total_events = len(files)
    total_skills = len(selected)

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

        print("\n" + "-" * 70)
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
        print("-" * 70)

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
            # 已存在且非空：直接跳过
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
    # 10. 最终完整性检查
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("TASK 4 FINAL COMPLETENESS CHECK")
    print("=" * 70)

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
    # 11. 最终检查数量
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
    # 12. 写入最终完成标记
    # --------------------------------------------------------

    marker = write_skills_complete_marker(
        date,
        lang,
        total_events,
        total_skills
    )

    # --------------------------------------------------------
    # 13. 再次验证marker
    # --------------------------------------------------------

    if (
        not marker.exists()
        or marker.stat().st_size <= 0
    ):
        raise RuntimeError(
            f"❌ TASK 4完成标记写入失败："
            f"{marker}"
        )

    # --------------------------------------------------------
    # 14. 最终输出
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("✅ TASK 4 COMPLETE")
    print("=" * 70)

    print(
        f"DATE             : {date}"
    )

    print(
        f"LANGUAGE         : {lang}"
    )

    print(
        f"DISK LANGUAGE    : {disk_lang}"
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

    print("=" * 70)

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
        choices=["EN", "ZH"],
        help="语言：EN 或 ZH"
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
