#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Grader V1.0

职责：
- 单选评分
- 多选评分
- 完形评分
- 阅读评分
- 听力评分
- 翻译提交结果整理
- 写作提交结果整理
- 生成统一评分结果

原则：
1. 不修改试卷
2. 不修改答案解析
3. 不调用 AI
4. 不提前显示正确答案
5. 多选必须集合完全匹配
6. 翻译 / 写作不做机械精确匹配
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any


AUTO_GRADED_TYPES = {
    "single_choice",
    "multiple_choice",
    "cloze",
    "reading",
    "listening",
}

MANUAL_REVIEW_TYPES = {
    "translation",
    "writing",
}


def normalize_answer(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, list):
        value = ",".join(str(x) for x in value)

    value = str(value).strip().upper()

    value = value.replace("，", ",")
    value = value.replace("、", ",")
    value = value.replace(";", ",")
    value = value.replace("；", ",")

    value = value.replace(" ", "")

    # 多选：
    # A,C
    # C,A
    # AC
    if "," in value:
        parts = [
            x for x in value.split(",")
            if x
        ]

        parts = sorted(set(parts))

        return ",".join(parts)

    if len(value) > 1 and value.isalpha():
        return ",".join(
            sorted(set(value))
        )

    return value


def grade_choice(
    correct_answer: str,
    user_answer: str,
    multiple: bool = False,
) -> bool:

    correct = normalize_answer(
        correct_answer
    )

    user = normalize_answer(
        user_answer
    )

    if multiple:
        return correct == user

    return correct == user


def grade_question(
    question: dict[str, Any],
    user_answer: Any,
) -> dict[str, Any]:

    result = deepcopy(question)

    qtype = question.get("type")

    result["user_answer"] = user_answer

    # ---------------------------------------------------------
    # 自动评分
    # ---------------------------------------------------------

    if qtype in {
        "single_choice",
        "cloze",
        "reading",
        "listening",
    }:

        correct = grade_choice(
            question.get(
                "correct_answer",
                "",
            ),
            user_answer,
            multiple=False,
        )

        result["graded"] = True
        result["correct"] = correct

        return result

    # ---------------------------------------------------------
    # 多选
    # ---------------------------------------------------------

    if qtype == "multiple_choice":

        correct = grade_choice(
            question.get(
                "correct_answer",
                "",
            ),
            user_answer,
            multiple=True,
        )

        result["graded"] = True
        result["correct"] = correct

        return result

    # ---------------------------------------------------------
    # 翻译
    # ---------------------------------------------------------

    if qtype == "translation":

        result["graded"] = False
        result["correct"] = None
        result["review_required"] = True

        return result

    # ---------------------------------------------------------
    # 写作
    # ---------------------------------------------------------

    if qtype == "writing":

        result["graded"] = False
        result["correct"] = None
        result["review_required"] = True

        return result

    result["graded"] = False
    result["correct"] = None

    return result


def grade_exam(
    exam: dict[str, Any],
    answers: dict[str, Any],
) -> dict[str, Any]:

    questions = exam.get(
        "questions",
        [],
    )

    results: list[dict[str, Any]] = []

    auto_total = 0
    auto_correct = 0

    manual_total = 0

    for question in questions:

        qid = question["question_id"]

        user_answer = answers.get(
            qid,
            "",
        )

        result = grade_question(
            question,
            user_answer,
        )

        results.append(result)

        if question["type"] in AUTO_GRADED_TYPES:

            auto_total += 1

            if result.get("correct"):
                auto_correct += 1

        elif question["type"] in MANUAL_REVIEW_TYPES:

            manual_total += 1

    total = len(questions)

    wrong = (
        auto_total
        - auto_correct
    )

    accuracy = (
        auto_correct / auto_total * 100
        if auto_total
        else 0
    )

    return {
        "version": "1.0",
        "total_questions": total,
        "auto_graded_questions": auto_total,
        "auto_correct": auto_correct,
        "auto_wrong": wrong,
        "manual_review_questions": manual_total,
        "accuracy": round(
            accuracy,
            1,
        ),
        "results": results,
    }


def make_review_data(
    grading_result: dict[str, Any],
) -> list[dict[str, Any]]:

    review: list[dict[str, Any]] = []

    for result in grading_result["results"]:

        qtype = result.get("type")

        # 自动评分错误
        if (
            qtype in AUTO_GRADED_TYPES
            and result.get("correct") is False
        ):

            review.append(
                {
                    "question_id":
                        result["question_id"],

                    "section":
                        result["section"],

                    "question":
                        result["question"],

                    "user_answer":
                        result.get(
                            "user_answer",
                            "",
                        ),

                    "correct_answer":
                        result.get(
                            "correct_answer",
                            "",
                        ),

                    "explanation":
                        result.get(
                            "explanation",
                            "",
                        ),

                    "status": "wrong",
                }
            )

        # 翻译
        elif qtype == "translation":

            review.append(
                {
                    "question_id":
                        result["question_id"],

                    "section":
                        result["section"],

                    "question":
                        result["question"],

                    "user_answer":
                        result.get(
                            "user_answer",
                            "",
                        ),

                    "reference_answer":
                        result.get(
                            "reference_answer",
                            "",
                        ),

                    "explanation":
                        result.get(
                            "explanation",
                            "",
                        ),

                    "status":
                        "manual_review",
                }
            )

        # 写作
        elif qtype == "writing":

            review.append(
                {
                    "question_id":
                        result["question_id"],

                    "section":
                        result["section"],

                    "question":
                        result["question"],

                    "user_answer":
                        result.get(
                            "user_answer",
                            "",
                        ),

                    "reference_answer":
                        result.get(
                            "reference_answer",
                            "",
                        ),

                    "explanation":
                        result.get(
                            "explanation",
                            "",
                        ),

                    "status":
                        "manual_review",
                }
            )

    return review


def build_submission_card_data(
    grading_result: dict[str, Any],
) -> dict[str, Any]:

    return {
        "status": "graded",
        "title": "📊 已评分",
        "total_questions":
            grading_result[
                "total_questions"
            ],
        "auto_graded_questions":
            grading_result[
                "auto_graded_questions"
            ],
        "correct":
            grading_result[
                "auto_correct"
            ],
        "wrong":
            grading_result[
                "auto_wrong"
            ],
        "accuracy":
            grading_result[
                "accuracy"
            ],
        "manual_review":
            grading_result[
                "manual_review_questions"
            ],
        "review":
            make_review_data(
                grading_result
            ),
    }


def validate_submission(
    exam: dict[str, Any],
    answers: dict[str, Any],
) -> list[str]:

    errors: list[str] = []

    question_ids = {
        q["question_id"]
        for q in exam.get(
            "questions",
            [],
        )
    }

    for question_id in answers:

        if question_id not in question_ids:

            errors.append(
                f"未知题目 ID: {question_id}"
            )

    return errors


def main():
    import argparse
    import json

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--exam-json",
        required=True,
    )

    parser.add_argument(
        "--answers-json",
        required=True,
    )

    parser.add_argument(
        "--output",
        required=False,
    )

    args = parser.parse_args()

    exam = json.loads(
        open(
            args.exam_json,
            "r",
            encoding="utf-8",
        ).read()
    )

    answers = json.loads(
        open(
            args.answers_json,
            "r",
            encoding="utf-8",
        ).read()
    )

    errors = validate_submission(
        exam,
        answers,
    )

    if errors:

        print("❌ SUBMISSION VALIDATION FAILED")

        for error in errors:
            print(
                f"   - {error}"
            )

        raise SystemExit(1)

    result = grade_exam(
        exam,
        answers,
    )

    print("=" * 70)
    print("748686 ENGLISH EXAM GRADER V1.0")
    print("=" * 70)

    print(
        f"总题数: {result['total_questions']}"
    )

    print(
        f"自动评分题数: "
        f"{result['auto_graded_questions']}"
    )

    print(
        f"正确: "
        f"{result['auto_correct']}"
    )

    print(
        f"错误: "
        f"{result['auto_wrong']}"
    )

    print(
        f"正确率: "
        f"{result['accuracy']}%"
    )

    print(
        f"待人工/语义处理: "
        f"{result['manual_review_questions']}"
    )

    if args.output:

        with open(
            args.output,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                result,
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(
            f"\n✅ 评分结果已写入: "
            f"{args.output}"
        )


if __name__ == "__main__":
    main()
