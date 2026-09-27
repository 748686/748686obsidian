#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Parser V1.1 Full Test

目标：

1. 真实试卷必须解析为 61 题
2. 各题型数量必须完全正确
3. 所有 question_id 必须唯一
4. 所有 50 道自动评分题必须有正确答案
5. 10 道翻译必须有参考答案
6. 1 道写作必须有参考范文
7. 每一个自动评分答案逐题核对
8. 可选调用 Grader 进行 50/50 全对测试
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

SCRIPT_DIR = (
    ROOT
    / "02_英语学习系统"
    / "scripts"
)

sys.path.insert(
    0,
    str(SCRIPT_DIR),
)

from english_exam_parser import (
    build_exam,
    normalize_answer,
)


# ============================================================
# 根据当前这份真实试卷定义预期答案
# ============================================================

EXPECTED = {

    # --------------------------------------------------------
    # Listening A
    # --------------------------------------------------------

    "LISTENING_A_01": "A",
    "LISTENING_A_02": "C",
    "LISTENING_A_03": "B",
    "LISTENING_A_04": "C",
    "LISTENING_A_05": "B",

    # Listening B
    "LISTENING_B_01": "A",
    "LISTENING_B_02": "C",
    "LISTENING_B_03": "A",
    "LISTENING_B_04": "B",
    "LISTENING_B_05": "A",

    # Listening C
    "LISTENING_C_01": "B",
    "LISTENING_C_02": "B",
    "LISTENING_C_03": "C",
    "LISTENING_C_04": "A",
    "LISTENING_C_05": "B",

    # --------------------------------------------------------
    # Single choice
    # --------------------------------------------------------

    "SINGLE_CHOICE_01": "B",
    "SINGLE_CHOICE_02": "C",
    "SINGLE_CHOICE_03": "C",
    "SINGLE_CHOICE_04": "B",
    "SINGLE_CHOICE_05": "B",
    "SINGLE_CHOICE_06": "B",
    "SINGLE_CHOICE_07": "C",
    "SINGLE_CHOICE_08": "B",
    "SINGLE_CHOICE_09": "C",
    "SINGLE_CHOICE_10": "A",

    # --------------------------------------------------------
    # Multiple choice
    # --------------------------------------------------------

    "MULTIPLE_CHOICE_01": "A,C",
    "MULTIPLE_CHOICE_02": "A,B",
    "MULTIPLE_CHOICE_03": "A,B",
    "MULTIPLE_CHOICE_04": "A,C",
    "MULTIPLE_CHOICE_05": "A,B,D",
    "MULTIPLE_CHOICE_06": "A,B,C",
    "MULTIPLE_CHOICE_07": "A,B",
    "MULTIPLE_CHOICE_08": "A,B",
    "MULTIPLE_CHOICE_09": "A",
    "MULTIPLE_CHOICE_10": "A,B",

    # --------------------------------------------------------
    # Cloze
    # --------------------------------------------------------

    "CLOZE_01": "A",
    "CLOZE_02": "B",
    "CLOZE_03": "B",
    "CLOZE_04": "C",
    "CLOZE_05": "A",
    "CLOZE_06": "B",
    "CLOZE_07": "A",
    "CLOZE_08": "B",
    "CLOZE_09": "B",
    "CLOZE_10": "C",

    # --------------------------------------------------------
    # Reading
    # --------------------------------------------------------

    "READING_01": "B",
    "READING_02": "A",
    "READING_03": "B",
    "READING_04": "B",
    "READING_05": "C",
}


EXPECTED_COUNTS = {
    "listening": 15,
    "single_choice": 10,
    "multiple_choice": 10,
    "cloze": 10,
    "reading": 5,
    "translation": 10,
    "writing": 1,
}


def locate_files() -> tuple[Path, Path]:
    """
    自动寻找 TODAY 对应文件。

    测试默认使用：
    output/YYYY-MM-DD/配套试卷/

    如果仓库结构不同，可以通过环境变量：
    ENGLISH_TEST_DATE
    指定日期。
    """

    import os

    date = os.environ.get(
        "ENGLISH_TEST_DATE"
    )

    if date:
        output_dir = (
            ROOT
            / "02_英语学习系统"
            / "output"
            / date
        )
    else:
        candidates = sorted(
            (
                ROOT
                / "02_英语学习系统"
                / "output"
            ).glob("*")
        )

        candidates = [
            x
            for x in candidates
            if x.is_dir()
        ]

        if not candidates:
            raise FileNotFoundError(
                "找不到 02_英语学习系统/output/YYYY-MM-DD"
            )

        output_dir = candidates[-1]

    exam_dir = (
        output_dir
        / "配套试卷"
    )

    exam_files = sorted(
        exam_dir.glob(
            "*星_*_试卷.md"
        )
    )

    answer_files = sorted(
        exam_dir.glob(
            "*星_*_答案与解析.md"
        )
    )

    if not exam_files:
        raise FileNotFoundError(
            f"找不到试卷: {exam_dir}"
        )

    if not answer_files:
        raise FileNotFoundError(
            f"找不到答案解析: {exam_dir}"
        )

    return (
        exam_files[0],
        answer_files[0],
    )


def main():

    print("=" * 78)
    print(
        "748686 ENGLISH EXAM "
        "PARSER V1.1 FULL TEST"
    )
    print("=" * 78)

    exam_file, answer_file = (
        locate_files()
    )

    print()
    print(
        f"试卷: {exam_file}"
    )
    print(
        f"答案: {answer_file}"
    )

    exam = build_exam(
        exam_file,
        answer_file,
    )

    questions = exam[
        "questions"
    ]

    question_map = {
        q["question_id"]: q
        for q in questions
    }

    failures: list[str] = []

    # ========================================================
    # Test 1
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 1 | 总题数")
    print("-" * 78)

    actual_total = len(
        questions
    )

    print(
        f"实际: {actual_total}"
    )
    print(
        "期望: 61"
    )

    if actual_total != 61:
        failures.append(
            f"总题数错误: {actual_total} != 61"
        )

    else:
        print("PASS")

    # ========================================================
    # Test 2
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 2 | 题型数量")
    print("-" * 78)

    actual_counts: dict[str, int] = {}

    for q in questions:

        key = q["type"]

        actual_counts[key] = (
            actual_counts.get(
                key,
                0,
            ) + 1
        )

    for key, expected in (
        EXPECTED_COUNTS.items()
    ):

        actual = actual_counts.get(
            key,
            0,
        )

        status = (
            "PASS"
            if actual == expected
            else "FAIL"
        )

        print(
            f"{status:5} "
            f"{key:18} "
            f"{actual:2} / {expected:2}"
        )

        if actual != expected:
            failures.append(
                f"{key}: "
                f"{actual} != {expected}"
            )

    # ========================================================
    # Test 3
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 3 | question_id 唯一性")
    print("-" * 78)

    ids = [
        q["question_id"]
        for q in questions
    ]

    if len(ids) != len(set(ids)):

        print("FAIL")

        duplicates = [
            qid
            for qid in set(ids)
            if ids.count(qid) > 1
        ]

        for qid in duplicates:
            print(
                f"   duplicate: {qid}"
            )

        failures.append(
            "存在重复 question_id"
        )

    else:
        print("PASS")

    # ========================================================
    # Test 4
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 4 | 50 道自动评分题答案")
    print("-" * 78)

    for qid, expected in EXPECTED.items():

        question = question_map.get(
            qid
        )

        if not question:

            print(
                f"FAIL  {qid:24} "
                "题目不存在"
            )

            failures.append(
                f"{qid}: question 不存在"
            )

            continue

        actual = normalize_answer(
            question.get(
                "correct_answer",
                "",
            )
        )

        expected = normalize_answer(
            expected
        )

        if actual == expected:

            print(
                f"PASS  {qid:24} "
                f"{actual}"
            )

        else:

            print(
                f"FAIL  {qid:24} "
                f"实际={actual!r} "
                f"期望={expected!r}"
            )

            failures.append(
                f"{qid}: "
                f"{actual} != {expected}"
            )

    # ========================================================
    # Test 5
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 5 | 翻译参考答案")
    print("-" * 78)

    for part in ("A", "B"):

        for number in range(
            1,
            6,
        ):

            qid = (
                f"TRANSLATION_"
                f"{part}_"
                f"{number:02d}"
            )

            question = question_map.get(
                qid
            )

            if not question:

                print(
                    f"FAIL  {qid} "
                    "题目不存在"
                )

                failures.append(
                    f"{qid}: "
                    "题目不存在"
                )

                continue

            reference = (
                question.get(
                    "reference_answer",
                    "",
                ).strip()
            )

            if reference:

                print(
                    f"PASS  {qid} "
                    f"参考答案长度="
                    f"{len(reference)}"
                )

            else:

                print(
                    f"FAIL  {qid} "
                    "参考答案为空"
                )

                failures.append(
                    f"{qid}: "
                    "参考答案为空"
                )

    # ========================================================
    # Test 6
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 6 | 写作参考范文")
    print("-" * 78)

    writing = question_map.get(
        "WRITING_01"
    )

    if not writing:

        print(
            "FAIL WRITING_01 不存在"
        )

        failures.append(
            "WRITING_01 不存在"
        )

    else:

        reference = (
            writing.get(
                "reference_answer",
                "",
            ).strip()
        )

        if reference:

            print(
                "PASS "
                f"参考范文长度="
                f"{len(reference)}"
            )

        else:

            print(
                "FAIL "
                "参考范文为空"
            )

            failures.append(
                "WRITING_01 "
                "参考范文为空"
            )

    # ========================================================
    # Test 7
    # ========================================================

    print()
    print("-" * 78)
    print("TEST 7 | 自动评分结构")
    print("-" * 78)

    auto_types = {
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
        "listening",
    }

    manual_types = {
        "translation",
        "writing",
    }

    auto_questions = [
        q
        for q in questions
        if q["type"] in auto_types
    ]

    manual_questions = [
        q
        for q in questions
        if q["type"] in manual_types
    ]

    print(
        f"自动评分题: "
        f"{len(auto_questions)} / 50"
    )

    print(
        f"人工/语义题: "
        f"{len(manual_questions)} / 11"
    )

    if len(auto_questions) != 50:

        failures.append(
            "自动评分题数量不是 50"
        )

    if len(manual_questions) != 11:

        failures.append(
            "人工/语义题数量不是 11"
        )

    # ========================================================
    # Final
    # ========================================================

    print()
    print("=" * 78)

    if failures:

        print(
            "❌ PARSER V1.1 TEST FAILED"
        )

        print()
        print(
            f"失败项目: "
            f"{len(failures)}"
        )

        for failure in failures:
            print(
                f"   - {failure}"
            )

        print("=" * 78)

        raise SystemExit(1)

    print(
        "✅ PARSER V1.1 TEST PASSED"
    )

    print()
    print(
        "61 / 61 questions"
    )

    print(
        "50 / 50 auto-graded answers"
    )

    print(
        "10 / 10 translation references"
    )

    print(
        "1 / 1 writing reference"
    )

    print("=" * 78)


if __name__ == "__main__":
    main()
