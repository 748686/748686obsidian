#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Rolling Orchestrator V6.5.3.

严格按 DATE + language 顺序执行：
en -> zh -> next date en -> zh。

每个 Unit 独立完成、验证并在返回后由本程序执行 Git push/pull。

============================================================
LANGUAGE CONTRACT
============================================================

整个系统语言命名永久统一为：

    en
    zh

严格禁止：

    EN
    ZH

本程序不进行任何语言大小写转换。

也就是说：

    不使用 .upper()
    不使用 .lower()
    不使用任何大小写转换逻辑

调用方必须直接传入：

    en
    zh

如果收到其他值，直接失败。

目录、CLI 参数、Task 之间的 language
全部使用完全相同的：

    en / zh

============================================================
PROCESSING UNIT
============================================================

每个 Processing Unit = DATE + language

严格顺序：

1. day-before en
2. day-before zh
3. yesterday  en
4. yesterday  zh
5. today      en
6. today      zh

同一天：

    en
      ↓
    zh

zh 必须等待同一天 en 的 _COMPLETE。

============================================================
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_NEWS = ROOT / "Raw News"
SCRIPTS = ROOT / "scripts"


# ============================================================
# LANGUAGE CONTRACT
# ============================================================

SUPPORTED_LANGUAGES = ("en", "zh")


def validate_language(lang):
    """严格验证 language。

    注意：
    这里绝不进行 upper/lower 转换。

    只允许：
        en
        zh

    任何：
        EN
        ZH
        En
        Zh
        其他值

    都直接失败。
    """

    if lang not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ Invalid language: {lang!r}\n"
            f"Language contract requires exactly: en or zh\n"
            f"No language case conversion is performed."
        )

    return lang


# ============================================================
# COMMAND RUNNER
# ============================================================

def run(cmd):
    """执行子进程命令。"""

    print("\n▶️ " + " ".join(map(str, cmd)))

    subprocess.run(
        cmd,
        check=True,
        cwd=ROOT,
    )


# ============================================================
# COMPLETE MARKER
# ============================================================

def marker(date, lang):
    """返回指定 DATE + language 的 COMPLETE marker。

    language 必须已经是：
        en
        zh

    本函数不做任何大小写转换。
    """

    validate_language(lang)

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / lang
        / "_COMPLETE"
    )


# ============================================================
# SKILLS COMPLETE MARKER
# ============================================================

def skills_marker(date, lang):
    """返回指定 DATE + language 的 SKILLS_COMPLETE marker。

    正确目录结构：

        Raw News/
        YYYY-MM-DD-EventUnit/
            en/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/
                    EVT-....md
                    EVT-...._analysis.md

    或：

        Raw News/
        YYYY-MM-DD-EventUnit/
            zh/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/
                    EVT-....md
                    EVT-...._analysis.md

    注意：

        _SKILLS_COMPLETE 位于 language 根目录。

    不是：

        event_units/_SKILLS_COMPLETE
    """

    validate_language(lang)

    return (
        RAW_NEWS
        / f"{date}-EventUnit"
        / lang
        / "_SKILLS_COMPLETE"
    )


# ============================================================
# INPUT VALIDATION
# ============================================================

def validate_inputs(date, lang):
    """验证 Atomic / Enriched 输入。

    目录严格使用：

        Raw News/
        DATE-Atomic/
            en/
            zh/

        Raw News/
        DATE-Enriched/
            en/
            zh/
    """

    validate_language(lang)

    for root_name in ("Atomic", "Enriched"):

        p = (
            RAW_NEWS
            / f"{date}-{root_name}"
            / lang
        )

        if not p.is_dir():
            raise RuntimeError(
                f"❌ {lang} {root_name} input missing: {p}"
            )

        count = len(
            list(
                p.glob("*.md")
            )
        )

        if count <= 0:
            raise RuntimeError(
                f"❌ {lang} {root_name} input empty: {p}"
            )

        print(
            f"{root_name} {lang}: {count}"
        )


# ============================================================
# GIT SYNC
# ============================================================

def git_sync(date, lang):
    """完成当前 DATE + language 的 Git Push / Pull。

    language 永远保持原值：

        en
        zh

    不进行任何大小写转换。
    """

    validate_language(lang)

    event_root = (
        f"01_自生长知识系统/Raw News/"
        f"{date}-EventUnit"
    )

    subprocess.run(
        [
            "git",
            "config",
            "user.name",
            "748686 Knowledge Bot",
        ],
        check=True,
        cwd=ROOT,
    )

    subprocess.run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        check=True,
        cwd=ROOT,
    )

    # --------------------------------------------------------
    # Git Add
    # --------------------------------------------------------

    run(
        [
            "git",
            "add",
            event_root,
        ]
    )

    # --------------------------------------------------------
    # 判断是否存在变化
    # --------------------------------------------------------

    staged = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet",
        ],
        cwd=ROOT,
    )

    # --------------------------------------------------------
    # Commit + Push
    # --------------------------------------------------------

    if staged.returncode != 0:

        run(
            [
                "git",
                "commit",
                "-m",
                f"data: complete EventUnit {date} {lang}",
            ]
        )

        run(
            [
                "git",
                "push",
                "origin",
                "HEAD:main",
            ]
        )

    else:

        print(
            "ℹ️ No changes detected"
        )

    # --------------------------------------------------------
    # Pull
    # --------------------------------------------------------

    run(
        [
            "git",
            "pull",
            "--ff-only",
            "origin",
            "main",
        ]
    )

    # --------------------------------------------------------
    # Post-sync validation
    # --------------------------------------------------------

    complete_marker = marker(
        date,
        lang,
    )

    if not complete_marker.exists():

        raise RuntimeError(
            f"❌ COMPLETE marker missing after pull: "
            f"{complete_marker}"
        )


# ============================================================
# UNIT COMPLETE
# ============================================================

def unit_complete(date, lang):
    """判断 DATE + language 是否已经完成。"""

    validate_language(lang)

    return marker(
        date,
        lang,
    ).exists()


# ============================================================
# EVENTUNIT PROCESSING
# ============================================================

def process_eventunit_unit(date, lang):
    """执行单个 EventUnit Processing Unit。

    顺序：

        Task 1 — Cluster
        ↓
        Task 2 — Merge
        ↓
        Task 3 — EventUnit
        ↓
        _COMPLETE
        ↓
        Git Push
        ↓
        Git Pull

    language 永远是：
        en
        zh
    """

    validate_language(lang)

    print(
        "\n" + "#" * 70
    )

    print(
        f"EVENTUNIT PROCESSING UNIT | "
        f"{date} | {lang}"
    )

    print(
        "#" * 70
    )

    # --------------------------------------------------------
    # Recovery
    # --------------------------------------------------------

    if unit_complete(
        date,
        lang,
    ):

        print(
            "✅ EventUnit Unit already COMPLETE — skip"
        )

        return

    # --------------------------------------------------------
    # 同一天必须先完成 en，再处理 zh
    # --------------------------------------------------------

    if lang == "zh":

        en_marker = marker(
            date,
            "en",
        )

        if not en_marker.exists():

            raise RuntimeError(
                f"❌ en Unit is not complete: "
                f"{en_marker}"
            )

    # --------------------------------------------------------
    # Input validation
    # --------------------------------------------------------

    validate_inputs(
        date,
        lang,
    )

    # --------------------------------------------------------
    # EventUnit Processing Tasks
    #
    # 所有 Task 直接接收：
    #
    #     en
    #     zh
    #
    # 不进行任何转换。
    # --------------------------------------------------------

    for task in (
        "knowledge_task_1_cluster.py",
        "knowledge_task_2_merge.py",
        "knowledge_task_3_eventunit.py",
    ):

        run(
            [
                sys.executable,
                str(
                    SCRIPTS / task
                ),
                "--date",
                date,
                "--language",
                lang,
            ]
        )

    # --------------------------------------------------------
    # COMPLETE validation
    # --------------------------------------------------------

    complete_marker = marker(
        date,
        lang,
    )

    if not complete_marker.exists():

        raise RuntimeError(
            f"❌ EventUnit未生成_COMPLETE："
            f"{complete_marker}"
        )

    # --------------------------------------------------------
    # Git Push / Pull
    # --------------------------------------------------------

    git_sync(
        date,
        lang,
    )

    print(
        f"✅ EVENTUNIT COMPLETE + PUSHED + PULLED | "
        f"{date}/{lang}"
    )


# ============================================================
# SKILLS PROCESSING
# ============================================================

def process_skills_unit(date, lang):
    """执行单个 DATE + language 的 Skills。

    EventUnit 完成后才能进入 Task 4。

    Task 4 直接接收：

        en
        zh

    不进行任何大小写转换。
    """

    validate_language(lang)

    print(
        "\n" + "#" * 70
    )

    print(
        f"SKILLS PROCESSING UNIT | "
        f"{date} | {lang}"
    )

    print(
        "#" * 70
    )

    # --------------------------------------------------------
    # EventUnit 必须已经完成
    # --------------------------------------------------------

    if not unit_complete(
        date,
        lang,
    ):

        raise RuntimeError(
            f"❌ EventUnit尚未完成，禁止执行Skills："
            f"{date}/{lang}"
        )

    # --------------------------------------------------------
    # Skills Recovery
    # --------------------------------------------------------

    if skills_marker(
        date,
        lang,
    ).exists():

        print(
            "✅ Skills Unit already _SKILLS_COMPLETE — skip"
        )

        return

    # --------------------------------------------------------
    # Task 4 — Skills
    #
    # 直接传：
    #
    #     en
    #     zh
    #
    # 不转换。
    # --------------------------------------------------------

    run(
        [
            sys.executable,
            str(
                SCRIPTS
                / "knowledge_task_4_skills.py"
            ),
            "--date",
            date,
            "--language",
            lang,
        ]
    )

    # --------------------------------------------------------
    # Task 4 validation
    # --------------------------------------------------------

    skills_complete_marker = skills_marker(
        date,
        lang,
    )

    if not skills_complete_marker.exists():

        raise RuntimeError(
            "❌ Task 4 did not create _SKILLS_COMPLETE\n"
            f"Expected:\n{skills_complete_marker}"
        )

    print(
        f"✅ Task 4 _SKILLS_COMPLETE verified: "
        f"{skills_complete_marker}"
    )

    # --------------------------------------------------------
    # Git Push / Pull
    # --------------------------------------------------------

    git_sync(
        date,
        lang,
    )

    print(
        f"✅ SKILLS COMPLETE + PUSHED + PULLED | "
        f"{date}/{lang}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Rolling V6.5.3"
        )
    )

    ap.add_argument(
        "--today",
        required=True,
    )

    ap.add_argument(
        "--yesterday",
        required=True,
    )

    ap.add_argument(
        "--day-before",
        required=True,
    )

    args = ap.parse_args()

    # ========================================================
    # SIX PROCESSING UNITS
    #
    # 严格使用小写 language。
    #
    # 1. day-before en
    # 2. day-before zh
    # 3. yesterday  en
    # 4. yesterday  zh
    # 5. today      en
    # 6. today      zh
    #
    # ========================================================

    units = [
        (
            args.day_before,
            "en",
        ),
        (
            args.day_before,
            "zh",
        ),
        (
            args.yesterday,
            "en",
        ),
        (
            args.yesterday,
            "zh",
        ),
        (
            args.today,
            "en",
        ),
        (
            args.today,
            "zh",
        ),
    ]

    try:

        # ====================================================
        # PHASE 1
        #
        # EventUnit
        # ====================================================

        print(
            "\n" + "=" * 70
        )

        print(
            "PHASE 1 — EVENTUNIT | "
            "每个 DATE + language 完成后立即 PUSH/PULL"
        )

        print(
            "=" * 70
        )

        for date, lang in units:

            process_eventunit_unit(
                date,
                lang,
            )

        # ====================================================
        # PHASE 2
        #
        # 27 Skills
        # ====================================================

        print(
            "\n" + "=" * 70
        )

        print(
            "PHASE 2 — 27 SKILLS | "
            "每个 DATE + language 完成后立即 PUSH/PULL"
        )

        print(
            "=" * 70
        )

        for date, lang in units:

            process_skills_unit(
                date,
                lang,
            )

    except KeyboardInterrupt:

        print(
            "\n❌ 用户中断"
        )

        return 130

    except Exception as e:

        print(
            f"\n❌ Knowledge Rolling V6.5.3 FAILED: {e}",
            file=sys.stderr,
        )

        return 1

    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n" + "#" * 70
    )

    print(
        "ALL SIX PROCESSING UNITS COMPLETE"
    )

    print(
        "#" * 70
    )

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )
