#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Rolling Orchestrator V7.1

======================================================================
核心职责
======================================================================

本程序只负责：

    1. 单个 DATE 的任务顺序控制
    2. language 顺序控制
    3. EventUnit → Skills 顺序控制
    4. DATE 级事务隔离
    5. Recovery / COMPLETE / SKILLS_COMPLETE 判断
    6. 每个 DATE + language 完成后的 Git checkpoint

本程序不负责：

    三日期调度
    TODAY / YESTERDAY / DAY-BEFORE 计算
    TODAY / 历史日期判断
    Task 1 Cluster 业务逻辑
    Task 2 Merge 业务逻辑
    Task 3 EventUnit 业务逻辑
    Task 4 Skills 业务逻辑
    Raw News 获取
    Atomic 生成
    Enriched 生成

这些职责保持在外层 Workflow 或现有程序中。

======================================================================
DATE CONTRACT
======================================================================

重要：

    外层 GitHub Actions Workflow
    是整个系统唯一的业务日期来源。

本程序一次只处理一个 DATE。

Workflow 调用：

    python knowledge_rolling.py \
        --date "$DATE"

例如：

    python knowledge_rolling.py \
        --date 2026-09-11

本程序：

    不计算 TODAY
    不计算 YESTERDAY
    不计算 DAY-BEFORE

禁止：

    datetime.now() 决定业务处理日期
    系统当前日期决定业务处理日期
    Asia/Shanghai 决定业务处理日期
    在本程序内部生成三日期

======================================================================
DATE TRANSACTION CONTRACT
======================================================================

一次运行 = 一个 DATE。

例如：

    DATE = 2026-09-11

处理严格按照：

    2026-09-11
        en EventUnit
        ↓
        en Skills
        ↓
        zh EventUnit
        ↓
        zh Skills
        ↓
        DATE COMPLETE

外层 Workflow 再负责：

    TODAY
      ↓
    YESTERDAY
      ↓
    DAY-BEFORE

因此：

    knowledge_rolling.py
        = 单日期内部 Orchestrator

    GitHub Actions Workflow
        = 三日期外部 Orchestrator

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

单个 DATE 内严格执行：

    en
        EventUnit
        ↓
        Skills

    ↓

    zh
        EventUnit
        ↓
        Skills

即：

    DATE
      ↓
    en EventUnit
      ↓
    en Skills
      ↓
    zh EventUnit
      ↓
    zh Skills

同一天：

    zh EventUnit

必须等待：

    en EventUnit COMPLETE

======================================================================
TASK CONTRACT
======================================================================

本程序只负责调用现有 Task：

    Task 1
        knowledge_task_1_cluster.py

    Task 2
        knowledge_task_2_merge.py

    Task 3
        knowledge_task_3_eventunit.py

    Task 4
        knowledge_task_4_skills.py

本程序不修改这些 Task 的业务逻辑。

Task 1 → Task 2 → Task 3：

    --date DATE
    --language en/zh

Task 4：

    --date DATE
    --language en/zh
    --max-new 30

======================================================================
COMPLETE CONTRACT
======================================================================

EventUnit 完成标记：

    Raw News/
    YYYY-MM-DD-EventUnit/
        en/
            _COMPLETE

        zh/
            _COMPLETE

Skills 完成标记：

    Raw News/
    YYYY-MM-DD-EventUnit/
        en/
            _SKILLS_COMPLETE

        zh/
            _SKILLS_COMPLETE

Recovery：

    _COMPLETE 存在
        → EventUnit 跳过

    _SKILLS_COMPLETE 存在
        → Skills 跳过

======================================================================
GIT CHECKPOINT CONTRACT
======================================================================

每个 DATE + language 都是独立 checkpoint。

例如：

    DATE
      en EventUnit
        ↓
      Git checkpoint

      en Skills
        ↓
      Git checkpoint

      zh EventUnit
        ↓
      Git checkpoint

      zh Skills
        ↓
      Git checkpoint

不允许等待所有日期全部完成后才统一 push。

======================================================================
错误处理 CONTRACT
======================================================================

本程序现在只处理一个 DATE。

因此：

    任意阶段失败
        ↓
    当前 knowledge_rolling.py 失败
        ↓
    exit 1

是否：

    TODAY = 必须成功

或者：

    历史日期 = 可以 SKIP

不再由本程序判断。

这些判断由外层 Workflow：

    process_date "$TODAY" "true"
    process_date "$YESTERDAY" "false"
    process_date "$DAY_BEFORE" "false"

负责。

因此本程序不再存在：

    required
    today
    yesterday
    day-before
    date_specs
    三日期循环

======================================================================
IMPORTANT
======================================================================

本版本解决：

    Workflow：

        python knowledge_rolling.py --date "$DATE"

与旧 V7.0：

        --today
        --yesterday
        --day-before

之间的接口冲突。

V7.1 的唯一 CLI：

    --date YYYY-MM-DD
"""


from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


# ============================================================
# VERSION
# ============================================================

VERSION = "V7.1"


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


def validate_language(lang: str) -> str:
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
# DATE CONTRACT
# ============================================================

DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}$"
)


def validate_date(date: str) -> str:
    """
    严格验证 Workflow 传入的单个业务日期。

    注意：

        这里只验证日期格式和日历合法性。

        不计算业务日期。

        不生成 TODAY / YESTERDAY / DAY-BEFORE。
    """

    if not isinstance(
        date,
        str,
    ):

        raise RuntimeError(
            f"❌ Invalid date type: "
            f"{type(date).__name__}"
        )

    if not DATE_RE.fullmatch(
        date
    ):

        raise RuntimeError(
            f"❌ Invalid date format: {date!r}\n"
            f"Expected YYYY-MM-DD."
        )

    try:

        datetime.strptime(
            date,
            "%Y-%m-%d",
        )

    except ValueError as exc:

        raise RuntimeError(
            f"❌ Invalid calendar date: {date!r}"
        ) from exc

    return date


# ============================================================
# COMMAND RUNNER
# ============================================================

def run(cmd: list[str]) -> None:
    """
    执行子进程命令。

    任意非零退出码都会抛出异常。

    外层 Workflow 决定：

        TODAY      → FAILED
        历史日期   → SKIPPED
    """

    print(
        "\n▶️ " + " ".join(
            map(str, cmd)
        )
    )

    subprocess.run(
        cmd,
        check=True,
        cwd=ROOT,
    )


# ============================================================
# COMPLETE MARKER
# ============================================================

def marker(
    date: str,
    lang: str,
) -> Path:
    """
    返回指定 DATE + language 的 EventUnit COMPLETE marker。
    """

    validate_date(date)

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

def skills_marker(
    date: str,
    lang: str,
) -> Path:
    """
    返回指定 DATE + language 的 SKILLS_COMPLETE marker。

    正确结构：

        Raw News/
        YYYY-MM-DD-EventUnit/
            en/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/

            zh/
                _COMPLETE
                _SKILLS_COMPLETE
                event_units/
    """

    validate_date(date)

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

def validate_inputs(
    date: str,
    lang: str,
) -> None:
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

    每个 DATE + language 目录：

        必须存在
        必须至少有一个 Markdown 文件
    """

    validate_date(date)

    validate_language(lang)

    for root_name in (
        "Atomic",
        "Enriched",
    ):

        path = (
            RAW_NEWS
            / f"{date}-{root_name}"
            / lang
        )

        if not path.is_dir():

            raise RuntimeError(
                f"❌ {lang} {root_name} input missing:\n"
                f"{path}"
            )

        count = len(
            list(
                path.glob("*.md")
            )
        )

        if count <= 0:

            raise RuntimeError(
                f"❌ {lang} {root_name} input empty:\n"
                f"{path}"
            )

        print(
            f"   {root_name} {lang}: {count}"
        )


# ============================================================
# GIT SYNC
# ============================================================

def git_sync(
    date: str,
    lang: str,
) -> None:
    """
    完成当前 DATE + language 的 Git Push / Pull。

    这是独立 checkpoint。

    language 永远保持：

        en
        zh
    """

    validate_date(date)

    validate_language(lang)

    event_root = (
        f"01_自生长知识系统/Raw News/"
        f"{date}-EventUnit"
    )

    print()
    print(
        "------------------------------------------------------------"
    )
    print(
        f"GIT CHECKPOINT | {date} | {lang}"
    )
    print(
        "------------------------------------------------------------"
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

        print(
            f"✅ Git push complete | "
            f"{date}/{lang}"
        )

    else:

        print(
            "ℹ️ No staged changes detected"
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
            f"❌ COMPLETE marker missing after pull:\n"
            f"{complete_marker}"
        )

    print(
        f"✅ Git checkpoint verified | "
        f"{date}/{lang}"
    )


# ============================================================
# UNIT COMPLETE
# ============================================================

def unit_complete(
    date: str,
    lang: str,
) -> bool:
    """
    判断 DATE + language 的 EventUnit 是否已经完成。
    """

    validate_date(date)

    validate_language(lang)

    return marker(
        date,
        lang,
    ).exists()


# ============================================================
# SKILLS COMPLETE
# ============================================================

def skills_complete(
    date: str,
    lang: str,
) -> bool:
    """
    判断 DATE + language 的 Skills 是否已经完成。
    """

    validate_date(date)

    validate_language(lang)

    return skills_marker(
        date,
        lang,
    ).exists()


# ============================================================
# EVENTUNIT PROCESSING
# ============================================================

def process_eventunit_unit(
    date: str,
    lang: str,
) -> None:
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

    validate_date(date)

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
                f"❌ en Unit is not complete:\n"
                f"{en_marker}"
            )

        print(
            f"✅ en EventUnit COMPLETE verified "
            f"before zh | {date}"
        )

    # --------------------------------------------------------
    # Input validation
    # --------------------------------------------------------

    print()
    print(
        "INPUT VALIDATION"
    )

    validate_inputs(
        date,
        lang,
    )

    # --------------------------------------------------------
    # Task 1 → Task 2 → Task 3
    # --------------------------------------------------------

    tasks = (
        "knowledge_task_1_cluster.py",
        "knowledge_task_2_merge.py",
        "knowledge_task_3_eventunit.py",
    )

    for task_number, task in enumerate(
        tasks,
        start=1,
    ):

        print()
        print(
            "-" * 70
        )

        print(
            f"TASK {task_number} | "
            f"{task} | "
            f"{date}/{lang}"
        )

        print(
            "-" * 70
        )

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
            f"❌ EventUnit 未生成 _COMPLETE:\n"
            f"{complete_marker}"
        )

    print(
        f"✅ _COMPLETE verified | "
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
        f"✅ EVENTUNIT COMPLETE + "
        f"PUSHED + PULLED | "
        f"{date}/{lang}"
    )


# ============================================================
# SKILLS PROCESSING
# ============================================================

def process_skills_unit(
    date: str,
    lang: str,
) -> None:
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

    validate_date(date)

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
            f"❌ EventUnit 尚未完成，禁止执行 Skills："
            f"{date}/{lang}"
        )

    print(
        f"✅ EventUnit COMPLETE verified | "
        f"{date}/{lang}"
    )

    # --------------------------------------------------------
    # Skills Recovery
    # --------------------------------------------------------

    if skills_complete(
        date,
        lang,
    ):

        print(
            "✅ Skills Unit already "
            "_SKILLS_COMPLETE — skip"
        )

        return

    # --------------------------------------------------------
    # Task 4
    #
    # 每次最多生成 30 个新的 Analysis。
    #
    # 注意：
    #
    # 本程序只负责调用 Task 4。
    #
    # Task 4 是否已经全部完成，
    # 由 Task 4 自己生成：
    #
    #     _SKILLS_COMPLETE
    #
    # 本程序验证这个 marker。
    # --------------------------------------------------------

    print()
    print(
        "-" * 70
    )

    print(
        f"TASK 4 | knowledge_task_4_skills.py | "
        f"{date}/{lang}"
    )

    print(
        "-" * 70
    )

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
            "❌ Task 4 did not create "
            "_SKILLS_COMPLETE\n"
            f"Expected:\n"
            f"{skills_complete_marker}"
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
        f"✅ SKILLS COMPLETE + "
        f"PUSHED + PULLED | "
        f"{date}/{lang}"
    )


# ============================================================
# DATE TRANSACTION
# ============================================================

def process_date(
    date: str,
) -> bool:
    """
    执行一个完整的单 DATE 事务。

    注意：

        这里的 date 只能来自外层 Workflow。

    严格顺序：

        en EventUnit
        ↓
        en Skills
        ↓
        zh EventUnit
        ↓
        zh Skills

    返回：

        True

    任意阶段失败：

        抛出异常。

    外层 Workflow 决定：

        TODAY       → fatal
        历史日期    → skipped
    """

    validate_date(date)

    print()
    print(
        "=" * 80
    )

    print(
        "KNOWLEDGE ROLLING — SINGLE DATE TRANSACTION"
    )

    print(
        "=" * 80
    )

    print(
        f"VERSION   : {VERSION}"
    )

    print(
        f"DATE      : {date}"
    )

    print(
        "DATE SOURCE: GitHub Actions Workflow"
    )

    print(
        "=" * 80
    )

    # ========================================================
    # EN
    # ========================================================

    print()
    print(
        "-" * 70
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

    print()
    print(
        "-" * 70
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

    # ========================================================
    # ZH
    # ========================================================

    print()
    print(
        "-" * 70
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

    print()
    print(
        "-" * 70
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

    # ========================================================
    # DATE COMPLETE
    # ========================================================

    print()
    print(
        "=" * 80
    )

    print(
        f"✅ DATE TRANSACTION COMPLETE | "
        f"{date}"
    )

    print(
        "=" * 80
    )

    return True


# ============================================================
# CLI
# ============================================================

def parse_args() -> argparse.Namespace:
    """
    V7.1 CLI。

    唯一业务日期参数：

        --date YYYY-MM-DD

    不接受：

        --today
        --yesterday
        --day-before
    """

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Rolling V7.1 — "
            "Single Date Transaction Orchestrator"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help=(
            "Business date supplied by the outer "
            "GitHub Actions Workflow: YYYY-MM-DD"
        ),
    )

    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main() -> int:
    """
    单日期入口。

    外层 Workflow 已经负责：

        TODAY
        YESTERDAY
        DAY-BEFORE

    本程序只负责：

        DATE
          ↓
        en EventUnit
          ↓
        en Skills
          ↓
        zh EventUnit
          ↓
        zh Skills
    """

    args = parse_args()

    date = validate_date(
        args.date
    )

    print()
    print(
        "#" * 80
    )

    print(
        "748686 KNOWLEDGE ROLLING V7.1"
    )

    print(
        "SINGLE DATE MODE"
    )

    print(
        "#" * 80
    )

    print(
        f"DATE       : {date}"
    )

    print(
        "DATE SOURCE: OUTER WORKFLOW"
    )

    print(
        "LANGUAGES  : en → zh"
    )

    print(
        "PIPELINE   : "
        "Task1 → Task2 → Task3 → Task4"
    )

    print(
        "#" * 80
    )

    try:

        success = process_date(
            date
        )

        if not success:

            raise RuntimeError(
                f"Unexpected process result: "
                f"{date}"
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
            "❌ Knowledge Rolling V7.1 FAILED",
            file=sys.stderr,
        )

        print(
            f"DATE  : {date}",
            file=sys.stderr,
        )

        print(
            f"Reason: "
            f"{type(exc).__name__}: {exc}",
            file=sys.stderr,
        )

        print(
            "#" * 80,
            file=sys.stderr,
        )

        return 1

    # ========================================================
    # FINAL
    # ========================================================

    print()
    print(
        "#" * 80
    )

    print(
        "ROLLING ORCHESTRATOR V7.1 COMPLETE"
    )

    print(
        f"DATE: {date}"
    )

    print(
        "STATUS: SUCCESS"
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
