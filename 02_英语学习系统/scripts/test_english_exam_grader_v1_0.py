#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Grader V1.0
FULL AUTOMATIC TEST

测试目标：

1. 真实 Parser V1.5 JSON
2. 61 道题结构
3. 50 道自动评分题
4. 11 道人工/语义处理题
5. 全部正确 => 50/50
6. 故意错误 => 正确识别
7. 多选集合匹配
8. 翻译/写作进入 manual_review
9. 错题回顾数据完整
10. 提交结果卡数据完整
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

EXPECTED_PARSER_VERSION = "1.5"


SCRIPT_DIR = Path(__file__).resolve().parent

sys.path.insert(
    0,
    str(SCRIPT_DIR),
)


from english_exam_grader import (
    AUTO_GRADED_TYPES,
    MANUAL_REVIEW_TYPES,
    grade_exam,
    make_review_data,
    build_submission_card_data,
    normalize_answer,
    validate_submission,
)


# ============================================================
# BASIC TEST HELPERS
# ============================================================

def fail(message: str):
    print(f"\n❌ {message}")
    raise SystemExit(1)


def check(condition: bool, message: str):
    if not condition:
        fail(message)

    print(f"   ✅ {message}")


# ============================================================
# JSON
# ============================================================

def load_json(path: str) -> dict:
    file = Path(path)

    if not file.exists():
        fail(
            f"JSON 文件不存在: {file}"
        )

    try:
        return json.loads(
            file.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:
        fail(
            f"JSON 读取失败: {file}\n"
            f"错误: {exc}"
        )


# ============================================================
# BUILD CORRECT ANSWERS
# ============================================================

def build_all_correct_answers(exam: dict) -> dict:
    """
    使用 Parser V1.5 已附着的 correct_answer
    构造完整 61 题答案。
    """

    answers = {}

    for question in exam.get(
        "questions",
        [],
    ):

        qid = question["question_id"]
        qtype = question["type"]

        if qtype in AUTO_GRADED_TYPES:

            correct = question.get(
                "correct_answer",
                "",
            )

            if not correct:
                fail(
                    f"自动评分题缺少 correct_answer: "
                    f"{qid}"
                )

            answers[qid] = correct

        elif qtype in MANUAL_REVIEW_TYPES:

            # 翻译 / 写作：
            # 不参与自动正确率，
            # 但必须允许提交。
            answers[qid] = (
                "TEST MANUAL ANSWER"
            )

        else:

            fail(
                f"未知题型: "
                f"{qid} / {qtype}"
            )

    return answers


# ============================================================
# TEST 1
# ============================================================

def test_structure(exam: dict):
    print("\n" + "-" * 70)
    print("TEST 1 | EXAM STRUCTURE")
    print("-" * 70)

    questions = exam.get(
        "questions",
        []
    )

    check(
        len(questions) == 61,
        f"总题数 = 61（实际 {len(questions)}）",
    )

    counts = {}

    for q in questions:

        qtype = q.get("type")

        counts[qtype] = (
            counts.get(qtype, 0) + 1
        )

    expected = {
        "listening": 15,
        "single_choice": 10,
        "multiple_choice": 10,
        "cloze": 10,
        "reading": 5,
        "translation": 10,
        "writing": 1,
    }

    for qtype, expected_count in expected.items():

        actual = counts.get(
            qtype,
            0,
        )

        check(
            actual == expected_count,
            f"{qtype}: {actual}/{expected_count}",
        )

    auto_total = sum(
        counts.get(
            qtype,
            0,
        )
        for qtype in AUTO_GRADED_TYPES
    )

    manual_total = sum(
        counts.get(
            qtype,
            0,
        )
        for qtype in MANUAL_REVIEW_TYPES
    )

    check(
        auto_total == 50,
        "自动评分题 = 50",
    )

    check(
        manual_total == 11,
        "人工/语义处理题 = 11",
    )


# ============================================================
# TEST 2
# ============================================================

def test_normalization():
    print("\n" + "-" * 70)
    print("TEST 2 | ANSWER NORMALIZATION")
    print("-" * 70)

    cases = [
        ("A", "A"),
        ("a", "A"),
        ("A,C", "A,C"),
        ("C,A", "A,C"),
        ("AC", "A,C"),
        ("A、C", "A,C"),
        ("A，C", "A,C"),
        (" A , C ", "A,C"),
    ]

    for source, expected in cases:

        actual = normalize_answer(
            source
        )

        check(
            actual == expected,
            f"{source!r} -> {actual!r}",
        )


# ============================================================
# TEST 3
# ============================================================

def test_all_correct(exam: dict):
    print("\n" + "-" * 70)
    print("TEST 3 | FULL 50/50 CORRECT")
    print("-" * 70)

    answers = build_all_correct_answers(
        exam
    )

    errors = validate_submission(
        exam,
        answers,
    )

    check(
        not errors,
        "提交答案 ID 全部合法",
    )

    result = grade_exam(
        exam,
        answers,
    )

    check(
        result["total_questions"] == 61,
        "总题数 = 61",
    )

    check(
        result["auto_graded_questions"] == 50,
        "自动评分题 = 50",
    )

    check(
        result["auto_correct"] == 50,
        "自动评分正确 = 50",
    )

    check(
        result["auto_wrong"] == 0,
        "自动评分错误 = 0",
    )

    check(
        result["accuracy"] == 100.0,
        "自动评分正确率 = 100.0%",
    )

    check(
        result["manual_review_questions"] == 11,
        "人工/语义处理 = 11",
    )

    for item in result["results"]:

        qtype = item["type"]

        if qtype in AUTO_GRADED_TYPES:

            check(
                item.get("graded") is True,
                f"{item['question_id']} 已自动评分",
            )

            check(
                item.get("correct") is True,
                f"{item['question_id']} 判定正确",
            )

        elif qtype in MANUAL_REVIEW_TYPES:

            check(
                item.get("graded") is False,
                f"{item['question_id']} 未机械评分",
            )

            check(
                item.get("review_required") is True,
                f"{item['question_id']} 进入人工/语义处理",
            )


# ============================================================
# TEST 4
# ============================================================

def test_multiple_choice():
    print("\n" + "-" * 70)
    print("TEST 4 | MULTIPLE CHOICE SET MATCHING")
    print("-" * 70)

    from english_exam_grader import grade_choice

    check(
        grade_choice(
            "A,C",
            "A,C",
            multiple=True,
        ),
        "A,C == A,C",
    )

    check(
        grade_choice(
            "A,C",
            "C,A",
            multiple=True,
        ),
        "A,C == C,A",
    )

    check(
        grade_choice(
            "A,C",
            "AC",
            multiple=True,
        ),
        "A,C == AC",
    )

    check(
        not grade_choice(
            "A,C",
            "A",
            multiple=True,
        ),
        "A,C != A",
    )

    check(
        not grade_choice(
            "A,C",
            "A,B,C",
            multiple=True,
        ),
        "A,C != A,B,C",
    )

    check(
        not grade_choice(
            "A,C",
            "B,C",
            multiple=True,
        ),
        "A,C != B,C",
    )


# ============================================================
# TEST 5
# ============================================================

def test_wrong_answers(exam: dict):
    print("\n" + "-" * 70)
    print("TEST 5 | INTENTIONAL WRONG ANSWERS")
    print("-" * 70)

    answers = build_all_correct_answers(
        exam
    )

    auto_questions = [
        q
        for q in exam["questions"]
        if q["type"] in AUTO_GRADED_TYPES
    ]

    check(
        len(auto_questions) == 50,
        "找到 50 道自动评分题",
    )

    # 分别挑选不同题型制造错误
    selected = {}

    for q in auto_questions:

        if q["type"] not in selected:
            selected[q["type"]] = q

    for qtype in [
        "listening",
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
    ]:

        check(
            qtype in selected,
            f"找到 {qtype} 测试题",
        )

    # 制造错误
    for qtype, question in selected.items():

        qid = question["question_id"]

        correct = str(
            question.get(
                "correct_answer",
                "",
            )
        )

        if qtype == "multiple_choice":

            # 与正确答案不同的完整集合
            answers[qid] = "Z"

        else:

            # A/B/C/D 中选择一个明确不同的答案
            answers[qid] = (
                "A"
                if correct != "A"
                else "B"
            )

    result = grade_exam(
        exam,
        answers,
    )

    check(
        result["auto_correct"] == 45,
        "故意制造 5 个错误后，正确 = 45",
    )

    check(
        result["auto_wrong"] == 5,
        "故意制造 5 个错误后，错误 = 5",
    )

    check(
        result["accuracy"] == 90.0,
        "故意制造 5 个错误后，正确率 = 90.0%",
    )

    review = make_review_data(
        result
    )

    wrong_items = [
        item
        for item in review
        if item.get("status") == "wrong"
    ]

    check(
        len(wrong_items) == 5,
        "错题回顾 = 5 道",
    )

    wrong_ids = {
        item["question_id"]
        for item in wrong_items
    }

    for qtype, question in selected.items():

        check(
            question["question_id"]
            in wrong_ids,
            f"{qtype} 错题进入回顾",
        )


# ============================================================
# TEST 6
# ============================================================

def test_manual_review(exam: dict):
    print("\n" + "-" * 70)
    print("TEST 6 | TRANSLATION / WRITING REVIEW")
    print("-" * 70)

    answers = build_all_correct_answers(
        exam
    )

    result = grade_exam(
        exam,
        answers,
    )

    review = make_review_data(
        result
    )

    manual_items = [
        item
        for item in review
        if item.get(
            "status"
        ) == "manual_review"
    ]

    check(
        len(manual_items) == 11,
        "翻译 + 写作人工/语义复核 = 11",
    )

    translation_count = sum(
        1
        for item in manual_items
        if item["section"]
        == "翻译"
    )

    writing_count = sum(
        1
        for item in manual_items
        if item["section"]
        == "写作"
    )

    check(
        translation_count == 10,
        "翻译人工复核 = 10",
    )

    check(
        writing_count == 1,
        "写作人工复核 = 1",
    )


# ============================================================
# TEST 7
# ============================================================

def test_submission_card(exam: dict):
    print("\n" + "-" * 70)
    print("TEST 7 | SUBMISSION CARD DATA")
    print("-" * 70)

    answers = build_all_correct_answers(
        exam
    )

    result = grade_exam(
        exam,
        answers,
    )

    card = build_submission_card_data(
        result
    )

    check(
        card["status"] == "graded",
        "状态 = graded",
    )

    check(
        card["title"] == "📊 已评分",
        "标题 = 📊 已评分",
    )

    check(
        card["total_questions"] == 61,
        "卡片总题数 = 61",
    )

    check(
        card["auto_graded_questions"] == 50,
        "卡片自动评分题 = 50",
    )

    check(
        card["correct"] == 50,
        "卡片正确 = 50",
    )

    check(
        card["wrong"] == 0,
        "卡片错误 = 0",
    )

    check(
        card["accuracy"] == 100.0,
        "卡片正确率 = 100.0%",
    )

    check(
        card["manual_review"] == 11,
        "卡片人工复核 = 11",
    )

    check(
        len(card["review"]) == 11,
        "全答对时回顾区只包含 11 道人工/语义题",
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--exam-json",
        required=True,
        help=(
            f"Parser V{EXPECTED_PARSER_VERSION} "
            "输出的 exam JSON"
        ),
    )

    args = parser.parse_args()

    print("=" * 70)
    print("748686 ENGLISH EXAM GRADER V1.0")
    print("FULL AUTOMATIC TEST")
    print("=" * 70)

    print(
        f"\n考试 JSON:\n  {args.exam_json}"
    )

    exam = load_json(
        args.exam_json
    )

    # ========================================================
    # PARSER VERSION CHECK
    # ========================================================

    actual_version = str(
        exam.get(
            "version",
            ""
        )
    )

    check(
        actual_version
        == EXPECTED_PARSER_VERSION,
        (
            f"Parser JSON version = "
            f"{EXPECTED_PARSER_VERSION}"
            f"（实际 {actual_version or '缺失'}）"
        ),
    )

    # ========================================================
    # TESTS
    # ========================================================

    test_structure(exam)

    test_normalization()

    test_all_correct(exam)

    test_multiple_choice()

    test_wrong_answers(exam)

    test_manual_review(exam)

    test_submission_card(exam)

    # ========================================================
    # SUCCESS
    # ========================================================

    print("\n" + "=" * 70)
    print("🎉 ALL GRADER V1.0 TESTS PASSED")
    print("=" * 70)

    print(
        "\n最终确认："
    )

    print(
        "  Parser V1.5 JSON 正常"
    )

    print(
        "  61 道题结构正常"
    )

    print(
        "  50 道自动评分题正常"
    )

    print(
        "  50/50 全部答对测试通过"
    )

    print(
        "  单选/多选/完形/阅读/听力错误识别通过"
    )

    print(
        "  多选集合匹配通过"
    )

    print(
        "  翻译 10 + 写作 1 人工/语义复核通过"
    )

    print(
        "  错题回顾通过"
    )

    print(
        "  提交结果卡数据通过"
    )


if __name__ == "__main__":
    main()
