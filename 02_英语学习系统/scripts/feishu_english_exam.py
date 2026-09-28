#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
Feishu English Exam Adapter V1.0

职责：
- 接收 English Exam Parser V1.6 输出的 JSON
- 转换成飞书答题所需的数据结构
- 严格隐藏 correct_answer
- 不负责评分
- 不修改试卷
- 不修改答案解析
- 不修改 Grader
- 不调用 AI

数据流：

English Exam Parser V1.6
        ↓
feishu_english_exam.py
        ↓
安全答题 JSON
        ↓
飞书答题界面
        ↓
用户提交 answers
        ↓
English Exam Grader V1.0
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


VERSION = "1.0"


# ============================================================
# 允许自动作答的题型
# ============================================================

CHOICE_TYPES = {
    "single_choice",
    "multiple_choice",
    "cloze",
    "reading",
    "listening",
}


MANUAL_TYPES = {
    "translation",
    "writing",
}


# ============================================================
# 基础工具
# ============================================================

def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise RuntimeError(
            f"❌ JSON文件不存在：{path}"
        )

    try:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except Exception as exc:
        raise RuntimeError(
            f"❌ JSON读取失败：{path}\n{exc}"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError(
            "❌ Parser JSON根节点必须是对象"
        )

    return data


def write_json(
    path: Path,
    data: dict[str, Any],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# ============================================================
# 安全字段
# ============================================================

def build_safe_question(
    question: dict[str, Any],
) -> dict[str, Any]:

    qtype = str(
        question.get(
            "type",
            ""
        )
    )

    question_id = str(
        question.get(
            "question_id",
            ""
        )
    )

    if not question_id:
        raise RuntimeError(
            "❌ 题目缺少 question_id"
        )

    if not qtype:
        raise RuntimeError(
            f"❌ 题目 {question_id} 缺少 type"
        )

    # --------------------------------------------------------
    # 飞书答题端只允许拿到这些字段
    # --------------------------------------------------------

    safe = {
        "question_id": question_id,
        "type": qtype,
        "id": question.get("id"),
        "section": question.get("section"),
        "number": question.get("number"),
        "part": question.get("part"),
        "question": question.get(
            "question",
            ""
        ),
        "options": question.get(
            "options",
            []
        ),
    }

    # --------------------------------------------------------
    # 自动评分题
    # --------------------------------------------------------

    if qtype in CHOICE_TYPES:

        safe["answer_mode"] = (
            "multiple"
            if qtype == "multiple_choice"
            else "single"
        )

        safe["input_type"] = "choice"

    # --------------------------------------------------------
    # 翻译
    # --------------------------------------------------------

    elif qtype == "translation":

        safe["answer_mode"] = "text"
        safe["input_type"] = "textarea"

    # --------------------------------------------------------
    # 作文
    # --------------------------------------------------------

    elif qtype == "writing":

        safe["answer_mode"] = "text"
        safe["input_type"] = "textarea"

    else:

        raise RuntimeError(
            f"❌ 未知题型："
            f"{question_id} / {qtype}"
        )

    return safe


# ============================================================
# 构建飞书安全答题数据
# ============================================================

def build_feishu_exam(
    parser_data: dict[str, Any],
) -> dict[str, Any]:

    questions = parser_data.get(
        "questions",
        []
    )

    if not isinstance(
        questions,
        list
    ):
        raise RuntimeError(
            "❌ Parser JSON 中 questions 不是数组"
        )

    safe_questions = []

    for question in questions:

        if not isinstance(
            question,
            dict
        ):
            raise RuntimeError(
                "❌ questions 中存在非法题目对象"
            )

        safe_questions.append(
            build_safe_question(
                question
            )
        )

    # --------------------------------------------------------
    # 统计
    # --------------------------------------------------------

    type_counts: dict[str, int] = {}

    for question in safe_questions:

        qtype = question["type"]

        type_counts[qtype] = (
            type_counts.get(
                qtype,
                0
            )
            + 1
        )

    result = {
        "version": VERSION,

        "source": {
            "parser_version":
                parser_data.get(
                    "version",
                    ""
                ),

            "parser":
                parser_data.get(
                    "parser",
                    ""
                ),
        },

        "exam": {
            "total_questions":
                len(safe_questions),

            "type_counts":
                type_counts,

            "questions":
                safe_questions,
        },

        "submission": {
            "status": "waiting",

            "answers": {},

            "submitted_at": None,
        },

        "security": {
            "correct_answers_removed": True,

            "answer_explanations_removed": True,

            "reference_answers_removed": True,

            "grading_hidden": True,
        },
    }

    return result


# ============================================================
# 安全检查
# ============================================================

def validate_no_answer_leak(
    data: dict[str, Any],
) -> None:

    forbidden_fields = {
        "correct_answer",
        "explanation",
        "reference_answer",
    }

    questions = (
        data
        .get("exam", {})
        .get("questions", [])
    )

    for question in questions:

        leaked = (
            forbidden_fields
            & set(question.keys())
        )

        if leaked:

            raise RuntimeError(
                "❌ SECURITY CHECK FAILED\n"
                f"题目："
                f"{question.get('question_id')}\n"
                f"泄露字段："
                f"{sorted(leaked)}"
            )

    print(
        "✓ 正确答案未进入飞书答题数据"
    )

    print(
        "✓ 答案解析未进入飞书答题数据"
    )

    print(
        "✓ 参考答案未进入飞书答题数据"
    )


# ============================================================
# 结构检查
# ============================================================

def validate_exam_structure(
    data: dict[str, Any],
) -> None:

    exam = data.get(
        "exam",
        {}
    )

    questions = exam.get(
        "questions",
        []
    )

    if not questions:
        raise RuntimeError(
            "❌ 飞书答题数据没有题目"
        )

    question_ids = []

    for question in questions:

        question_id = question.get(
            "question_id"
        )

        if not question_id:
            raise RuntimeError(
                "❌ 存在没有 question_id 的题目"
            )

        question_ids.append(
            question_id
        )

    duplicates = {
        qid
        for qid in question_ids
        if question_ids.count(qid) > 1
    }

    if duplicates:

        raise RuntimeError(
            "❌ 发现重复 question_id："
            f"{sorted(duplicates)}"
        )

    print(
        f"✓ 题目结构正常："
        f"{len(questions)} 题"
    )


# ============================================================
# CLI
# ============================================================

def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "748686 "
            "Feishu English Exam Adapter V1.0"
        )
    )

    parser.add_argument(
        "--exam-json",
        required=True,
        help=(
            "English Exam Parser V1.6 "
            "输出的JSON"
        ),
    )

    parser.add_argument(
        "--output",
        required=True,
        help="输出安全飞书答题JSON",
    )

    args = parser.parse_args()

    exam_json = Path(
        args.exam_json
    )

    output = Path(
        args.output
    )

    print("=" * 70)
    print(
        "748686 FEISHU ENGLISH EXAM "
        "ADAPTER V1.0"
    )
    print("=" * 70)

    print()
    print(
        f"输入：{exam_json}"
    )

    print(
        f"输出：{output}"
    )

    # --------------------------------------------------------
    # 读取 Parser
    # --------------------------------------------------------

    parser_data = load_json(
        exam_json
    )

    print()
    print(
        "Parser version:",
        parser_data.get(
            "version",
            ""
        )
    )

    # --------------------------------------------------------
    # 构建安全答题数据
    # --------------------------------------------------------

    feishu_exam = build_feishu_exam(
        parser_data
    )

    # --------------------------------------------------------
    # 安全检查
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        "SECURITY CHECK"
    )

    print(
        "=" * 70
    )

    validate_no_answer_leak(
        feishu_exam
    )

    # --------------------------------------------------------
    # 结构检查
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        "STRUCTURE CHECK"
    )

    print(
        "=" * 70
    )

    validate_exam_structure(
        feishu_exam
    )

    # --------------------------------------------------------
    # 写文件
    # --------------------------------------------------------

    write_json(
        output,
        feishu_exam
    )

    # --------------------------------------------------------
    # 最终检查
    # --------------------------------------------------------

    if not output.exists():

        raise RuntimeError(
            "❌ 输出文件没有成功生成"
        )

    size = output.stat().st_size

    if size <= 0:

        raise RuntimeError(
            "❌ 输出文件为空"
        )

    print()
    print(
        "=" * 70
    )

    print(
        "FEISHU EXAM DATA READY"
    )

    print(
        "=" * 70
    )

    print(
        f"总题数："
        f"{feishu_exam['exam']['total_questions']}"
    )

    print(
        "题型："
    )

    for qtype, count in (
        feishu_exam[
            "exam"
        ][
            "type_counts"
        ].items()
    ):

        print(
            f"  {qtype}: {count}"
        )

    print()
    print(
        f"✅ 安全答题 JSON 已生成："
        f"{output}"
    )


if __name__ == "__main__":
    main()
