#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Rolling Orchestrator V6.5.3.

严格按 DATE + language 顺序执行：
en -> zh -> next date en -> zh。

每个 Unit 独立完成、验证并在返回后由本程序执行 Git push/pull。

语言目录契约：
    en
    zh

整个程序统一使用小写 language。
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_NEWS = ROOT / "Raw News"
SCRIPTS = ROOT / "scripts"


def run(cmd):
    print("\n▶️ " + " ".join(map(str, cmd)))
    subprocess.run(cmd, check=True, cwd=ROOT)


def marker(date, lang):
    lang = lang.lower()
    return RAW_NEWS / f"{date}-EventUnit" / lang / "_COMPLETE"


def validate_inputs(date, lang):
    lang = lang.lower()

    for root_name in ("Atomic", "Enriched"):
        p = RAW_NEWS / f"{date}-{root_name}" / lang

        if not p.is_dir():
            raise RuntimeError(
                f"❌ {lang} {root_name} input missing: {p}"
            )

        count = len(list(p.glob("*.md")))

        if count <= 0:
            raise RuntimeError(
                f"❌ {lang} {root_name} input empty: {p}"
            )

        print(f"{root_name} {lang}: {count}")


def git_sync(date, lang):
    lang = lang.lower()

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

    run(["git", "add", event_root])

    staged = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet",
        ],
        cwd=ROOT,
    )

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
        print("ℹ️ No changes detected")

    run(
        [
            "git",
            "pull",
            "--ff-only",
            "origin",
            "main",
        ]
    )

    if not marker(date, lang).exists():
        raise RuntimeError(
            f"❌ COMPLETE marker missing after pull: "
            f"{marker(date, lang)}"
        )


def unit_complete(date, lang):
    lang = lang.lower()
    return marker(date, lang).exists()


def process_eventunit_unit(date, lang):
    # ------------------------------------------------------
    # 语言统一标准：全部小写
    # ------------------------------------------------------

    lang = lang.lower()

    print("\n" + "#" * 70)
    print(
        f"EVENTUNIT PROCESSING UNIT | {date} | {lang}"
    )
    print("#" * 70)

    if unit_complete(date, lang):
        print(
            "✅ EventUnit Unit already COMPLETE — skip"
        )
        return

    # ------------------------------------------------------
    # 同一天必须先完成 en，再处理 zh
    # ------------------------------------------------------

    if lang == "zh":
        en = marker(date, "en")

        if not en.exists():
            raise RuntimeError(
                f"❌ en Unit is not complete: {en}"
            )

    validate_inputs(date, lang)

    # ------------------------------------------------------
    # EventUnit Processing Tasks
    #
    # Task 1 — Cluster
    # Task 2 — Merge
    # Task 3 — EventUnit
    # ------------------------------------------------------

    for task in (
        "knowledge_task_1_cluster.py",
        "knowledge_task_2_merge.py",
        "knowledge_task_3_eventunit.py",
    ):
        run(
            [
                sys.executable,
                str(SCRIPTS / task),
                "--date",
                date,
                "--language",
                lang,
            ]
        )

    # ------------------------------------------------------
    # COMPLETE validation
    # ------------------------------------------------------

    if not marker(date, lang).exists():
        raise RuntimeError(
            f"❌ EventUnit未生成_COMPLETE："
            f"{marker(date, lang)}"
        )

    # ------------------------------------------------------
    # Git Push / Pull
    # ------------------------------------------------------

    git_sync(date, lang)

    print(
        f"✅ EVENTUNIT COMPLETE + PUSHED + PULLED | "
        f"{date}/{lang}"
    )


def process_skills_unit(date, lang):
    # ------------------------------------------------------
    # 语言统一标准：全部小写
    # ------------------------------------------------------

    lang = lang.lower()

    print("\n" + "#" * 70)
    print(
        f"SKILLS PROCESSING UNIT | {date} | {lang}"
    )
    print("#" * 70)

    # ------------------------------------------------------
    # EventUnit 必须已经完成
    # ------------------------------------------------------

    if not unit_complete(date, lang):
        raise RuntimeError(
            f"❌ EventUnit尚未完成，禁止执行Skills："
            f"{date}/{lang}"
        )

    # ------------------------------------------------------
    # Task 4 — Skills
    # ------------------------------------------------------

    run(
        [
            sys.executable,
            str(SCRIPTS / "knowledge_task_4_skills.py"),
            "--date",
            date,
            "--language",
            lang,
        ]
    )

    # ------------------------------------------------------
    # Git Push / Pull
    # ------------------------------------------------------

    git_sync(date, lang)

    print(
        f"✅ SKILLS COMPLETE + PUSHED + PULLED | "
        f"{date}/{lang}"
    )


def main():
    ap = argparse.ArgumentParser(
        description="748686 Knowledge Rolling V6.5.3"
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

    # ------------------------------------------------------
    # 六个 Processing Units
    #
    # 严格使用小写 language：
    #
    # 1. day-before en
    # 2. day-before zh
    # 3. yesterday  en
    # 4. yesterday  zh
    # 5. today      en
    # 6. today      zh
    # ------------------------------------------------------

    units = [
        (args.day_before, "en"),
        (args.day_before, "zh"),
        (args.yesterday, "en"),
        (args.yesterday, "zh"),
        (args.today, "en"),
        (args.today, "zh"),
    ]

    try:

        # ==================================================
        # PHASE 1
        # EventUnit
        # ==================================================

        print("\n" + "=" * 70)
        print(
            "PHASE 1 — EVENTUNIT | "
            "每个 DATE + language 完成后立即 PUSH/PULL"
        )
        print("=" * 70)

        for date, lang in units:
            process_eventunit_unit(date, lang)

        # ==================================================
        # PHASE 2
        # 27 Skills
        # ==================================================

        print("\n" + "=" * 70)
        print(
            "PHASE 2 — 27 SKILLS | "
            "每个 DATE + language 完成后立即 PUSH/PULL"
        )
        print("=" * 70)

        for date, lang in units:
            process_skills_unit(date, lang)

    except KeyboardInterrupt:
        print("\n❌ 用户中断")
        return 130

    except Exception as e:
        print(
            f"\n❌ Knowledge Rolling V6.5.3 FAILED: {e}",
            file=sys.stderr,
        )
        return 1

    print("\n" + "#" * 70)
    print("ALL SIX PROCESSING UNITS COMPLETE")
    print("#" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
