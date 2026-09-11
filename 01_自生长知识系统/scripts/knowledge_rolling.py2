#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Rolling Orchestrator V7.0

======================================================================
核心职责
======================================================================

本程序只负责：

    1. DATE 顺序控制
    2. language 顺序控制
    3. EventUnit → Skills 顺序控制
    4. DATE 级事务隔离
    5. TODAY 必须成功
    6. 历史日期失败后跳过并继续
    7. 每个 DATE + language 完成后 Git checkpoint
    8. Recovery / COMPLETE / SKILLS_COMPLETE 判断

本程序不负责：

    Task 1 Cluster 业务逻辑
    Task 2 Merge 业务逻辑
    Task 3 EventUnit 业务逻辑
    Task 4 Skills 业务逻辑
    Raw News 获取
    Atomic 生成
    Enriched 生成

这些职责全部保持在现有程序中。

======================================================================
DATE TRANSACTION CONTRACT
======================================================================

严格按照：

    TODAY
      ↓
    YESTERDAY
      ↓
    DAY-BEFORE

每一个 DATE 都是独立事务。

例如：

    TODAY
      en EventUnit
      en Skills
      zh EventUnit
      zh Skills
      ↓
    DATE COMPLETE

    YESTERDAY
      en EventUnit
      en Skills
      zh EventUnit
      zh Skills
      ↓
    DATE COMPLETE

    DAY-BEFORE
      ...

======================================================================
TODAY CONTRACT
======================================================================

TODAY 是强制日期。

如果 TODAY 任意阶段失败：

    → 立即 FAILED
    → Workflow exit 1
    → 不继续历史日期

======================================================================
HISTORICAL DATE CONTRACT
======================================================================

YESTERDAY / DAY-BEFORE 是历史补偿日期。

如果历史日期任意阶段失败：

    → 记录 SKIPPED
    → 不回滚已经成功 push 的内容
    → 继续下一个 DATE

例如：

    YESTERDAY en EventUnit       SUCCESS
    YESTERDAY en Skills          SUCCESS
    YESTERDAY zh EventUnit       FAILED

那么：

    YESTERDAY = SKIPPED

已经成功 push 的 en 内容保留。

随后：

    DAY-BEFORE

继续执行。

======================================================================
LANGUAGE CONTRACT
======================================================================

整个系统语言命名永久统一为：

    en
    zh

严格禁止：

    EN
    ZH

本程序不进行任何语言大小写转换。

不使用：

    .upper()
    .lower()
    .casefold()

调用方必须直接传入：

    en
    zh

======================================================================
PROCESSING ORDER
======================================================================

严格执行：

    TODAY
        en EventUnit
        en Skills
        zh EventUnit
        zh Skills

    YESTERDAY
        en EventUnit
        en Skills
        zh EventUnit
        zh Skills

    DAY-BEFORE
        en EventUnit
        en Skills
        zh EventUnit
        zh Skills

同一天：

    en
      ↓
    zh

同一天 zh 必须等待 en EventUnit COMPLETE。

======================================================================
GIT CHECKPOINT CONTRACT
======================================================================

每个 DATE + language 都是独立 checkpoint。

即：

    EventUnit en
        ↓
    git push/pull

    Skills en
        ↓
    git push/pull

    EventUnit zh
        ↓
    git push/pull

    Skills zh
        ↓
    git push/pull

不允许把所有日期全部完成后才统一 push。

======================================================================
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


# ============================================================
# PATH
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

SCRIPTS = ROOT / "scripts"


# ============================================================
# LANGUAGE CONTRACT
# ============================================================

SUPPORTED_LANGUAGES = (
    "en",
    "zh",
)


def validate_language(lang):
    """
    严格验证 language。

    只允许：

        en
        zh

    不进行任何大小写转换。
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
    """
    执行子进程命令。

    任意非零退出码都会抛出异常，
    由 DATE 事务层决定：

        TODAY  → FAILED
        历史   → SKIPPED
    """

    print(
        "\n▶️ " + " ".join(map(str, cmd))
    )

    subprocess.run(
        cmd,
        check=True,
        cwd=ROOT,
    )


# ============================================================
# COMPLETE MARKER
# ============================================================

def marker(date, lang):
    """
    返回指定 DATE + language 的 COMPLETE marker。
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
    """
    返回指定 DATE + language 的 SKILLS_COMPLETE marker。

    正确结构：

        Raw News/
        YYYY-MM-DD-EventUnit/
            en/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/
                    EVT-....md
                    EVT-...._analysis.md

            zh/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/
                    EVT-....md
                    EVT-...._analysis.md
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
    """
    验证 Atomic / Enriched 输入。

    要求：

        Raw News/
        DATE-Atomic/
            en/
            zh/

        Raw News/
        DATE-Enriched/
            en/
            zh/

    每个目录必须至少有一个 Markdown 文件。
    """

    validate_language(lang)

    for root_name in (
        "Atomic",
        "Enriched",
    ):

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
    """
    完成当前 DATE + language 的 Git Push / Pull。

    这是独立 checkpoint。

    language 永远保持：

        en
        zh
    """

    validate_language(lang)

    event_root = (
        f"01_自生长知识系统/Raw News/"
        f"{date}-EventUnit"
    )

    # --------------------------------------------------------
    # Git identity
    # --------------------------------------------------------

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
    # 判断 staged 是否存在变化
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
    """
    判断 DATE + language 的 EventUnit 是否已经完成。
    """

    validate_language(lang)

    return marker(
        date,
        lang,
    ).exists()


# ============================================================
# EVENTUNIT PROCESSING
# ============================================================

def process_eventunit_unit(date, lang):
    """
    执行单个 DATE + language 的 EventUnit。

    顺序：

        Task 1
          ↓
        Task 2
          ↓
        Task 3
          ↓
        _COMPLETE
          ↓
        Git Push
          ↓
        Git Pull
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
    # Task 1 → Task 2 → Task 3
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
    # Git checkpoint
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
    """
    执行单个 DATE + language 的 Task 4 Skills。

    EventUnit 必须已经完成。

    Task 4：

        knowledge_task_4_skills.py

    使用：

        --date
        --language
        --max-new 30
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
    # Task 4
    #
    # Batch Persistence:
    #
    # 每次最多生成 30 个新的 Analysis。
    #
    # 如果本批次达到 30：
    #
    #     Task 4 正常返回
    #     不生成 _SKILLS_COMPLETE
    #     本程序 checkpoint
    #     下一次 Workflow 可 Recovery
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
            "--max-new",
            "30",
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
    # Git checkpoint
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
# DATE TRANSACTION
# ============================================================

def process_date(
    label,
    date,
    required,
):
    """
    执行一个完整 DATE 事务。

    顺序：

        en EventUnit
        ↓
        en Skills
        ↓
        zh EventUnit
        ↓
        zh Skills

    参数：

        label:
            today / yesterday / day-before

        date:
            Workflow 传入的具体日期

        required:
            TODAY = True
            历史日期 = False

    返回：

        True  → SUCCESS
        False → SKIPPED
    """

    print(
        "\n" + "=" * 80
    )

    print(
        f"DATE TRANSACTION START | "
        f"{label.upper()} | {date}"
    )

    print(
        f"Required: {required}"
    )

    print(
        "=" * 80
    )

    try:

        # ====================================================
        # EN
        # ====================================================

        print(
            "\n" + "-" * 70
        )

        print(
            f"{date} | en | EventUnit"
        )

        print(
            "-" * 70
        )

        process_eventunit_unit(
            date,
            "en",
        )

        print(
            "\n" + "-" * 70
        )

        print(
            f"{date} | en | Skills"
        )

        print(
            "-" * 70
        )

        process_skills_unit(
            date,
            "en",
        )

        # ====================================================
        # ZH
        # ====================================================

        print(
            "\n" + "-" * 70
        )

        print(
            f"{date} | zh | EventUnit"
        )

        print(
            "-" * 70
        )

        process_eventunit_unit(
            date,
            "zh",
        )

        print(
            "\n" + "-" * 70
        )

        print(
            f"{date} | zh | Skills"
        )

        print(
            "-" * 70
        )

        process_skills_unit(
            date,
            "zh",
        )

        # ====================================================
        # DATE COMPLETE
        # ====================================================

        print(
            "\n" + "=" * 80
        )

        print(
            f"✅ DATE TRANSACTION SUCCESS | "
            f"{date}"
        )

        print(
            "=" * 80
        )

        return True

    except KeyboardInterrupt:

        raise

    except Exception as exc:

        # ====================================================
        # TODAY = FATAL
        # ====================================================

        if required:

            print(
                "\n" + "!" * 80,
                file=sys.stderr,
            )

            print(
                f"❌ REQUIRED DATE FAILED | "
                f"{label} | {date}",
                file=sys.stderr,
            )

            print(
                f"Reason: {exc}",
                file=sys.stderr,
            )

            print(
                "TODAY failed — workflow must terminate.",
                file=sys.stderr,
            )

            print(
                "!" * 80,
                file=sys.stderr,
            )

            raise

        # ====================================================
        # HISTORICAL DATE = SKIPPED
        # ====================================================

        print(
            "\n" + "!" * 80
        )

        print(
            f"⚠️ HISTORICAL DATE SKIPPED | "
            f"{label} | {date}"
        )

        print(
            f"Reason: {exc}"
        )

        print(
            "Already pushed checkpoints are preserved."
        )

        print(
            "Workflow will continue to next date."
        )

        print(
            "!" * 80
        )

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Rolling V7.0 — "
            "Date Transaction Orchestrator"
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
    # DATE ORDER
    #
    # 永久固定：
    #
    #     TODAY
    #     ↓
    #     YESTERDAY
    #     ↓
    #     DAY-BEFORE
    #
    # ========================================================

    date_specs = [
        (
            "today",
            args.today,
            True,
        ),
        (
            "yesterday",
            args.yesterday,
            False,
        ),
        (
            "day-before",
            args.day_before,
            False,
        ),
    ]

    results = []

    try:

        # ====================================================
        # DATE TRANSACTION LOOP
        # ====================================================

        for label, date, required in date_specs:

            success = process_date(
                label=label,
                date=date,
                required=required,
            )

            if success:

                results.append(
                    (
                        date,
                        "SUCCESS",
                    )
                )

            else:

                results.append(
                    (
                        date,
                        "SKIPPED",
                    )
                )

    except KeyboardInterrupt:

        print(
            "\n❌ 用户中断",
            file=sys.stderr,
        )

        return 130

    except Exception as exc:

        print(
            "\n" + "#" * 80,
            file=sys.stderr,
        )

        print(
            "❌ Knowledge Rolling V7.0 FAILED",
            file=sys.stderr,
        )

        print(
            f"Reason: {exc}",
            file=sys.stderr,
        )

        print(
            "#" * 80,
            file=sys.stderr,
        )

        return 1

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print(
        "\n" + "=" * 80
    )

    print(
        "ROLLING PROCESS RESULT"
    )

    print(
        "=" * 80
    )

    for date, status in results:

        if status == "SUCCESS":

            print(
                f"✅ {date} → SUCCESS"
            )

        else:

            print(
                f"⚠️ {date} → SKIPPED"
            )

    print(
        "=" * 80
    )

    # ========================================================
    # TODAY 必须成功
    #
    # 理论上 TODAY 失败已经在 process_date()
    # 中抛出异常并退出。
    #
    # 这里再次保护。
    # ========================================================

    today_result = None

    for date, status in results:

        if date == args.today:

            today_result = status

            break

    if today_result != "SUCCESS":

        print(
            "\n❌ TODAY did not complete successfully.",
            file=sys.stderr,
        )

        return 1

    # ========================================================
    # FINAL
    # ========================================================

    print(
        "\n" + "#" * 80
    )

    print(
        "ROLLING ORCHESTRATOR COMPLETE"
    )

    print(
        "#" * 80
    )

    return 0


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )
