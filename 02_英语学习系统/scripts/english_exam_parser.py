#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Parser V1.0

职责：
1. 解析实际试卷 Markdown
2. 解析答案与解析 Markdown
3. 建立稳定的 question_id
4. 保留题目、选项、题型、正确答案、解析
5. 不修改任何英语学习生成文件

支持：
- 听力 Part A / B / C
- 单项选择
- 多选题
- 完形填空
- 阅读理解
- 汉译英
- 英译汉
- 写作
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SECTION_MAP = {
    "一、听力": "listening",
    "二、单项选择": "single_choice",
    "三、多选题": "multiple_choice",
    "四、完形填空": "cloze",
    "五、阅读理解": "reading",
    "六、翻译": "translation",
    "七、写作": "writing",
}


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def normalize_answer(value: str) -> str:
    """
    标准化答案。

    A,C
    A，C
    AC
    C,A

    最终统一为：
    A,C
    """
    if value is None:
        return ""

    value = value.strip().upper()
    value = value.replace("，", ",")
    value = value.replace("、", ",")
    value = value.replace("；", ",")
    value = value.replace(";", ",")
    value = re.sub(r"\s+", "", value)

    # 处理类似 AC / CA
    if re.fullmatch(r"[A-Z]+", value):
        letters = sorted(set(value))
        return ",".join(letters)

    letters = re.findall(r"[A-Z]", value)

    if not letters:
        return value

    return ",".join(sorted(set(letters)))


def extract_answer_from_line(line: str) -> str:
    """
    从答案行提取答案。

    支持：
    1. A
    1. B
    1 B
    1. A,C
    1. A、C
    """
    line = line.strip()

    match = re.match(
        r"^\s*\d+\s*[.、．)]?\s*([A-Za-z](?:\s*[,，、]\s*[A-Za-z])*)\s*$",
        line,
    )

    if not match:
        return ""

    return normalize_answer(match.group(1))


def parse_question_header(line: str) -> int | None:
    match = re.match(r"^\s*###\s*(\d+)[.、．)]", line)
    if match:
        return int(match.group(1))
    return None


def parse_options(lines: list[str]) -> list[dict[str, str]]:
    options: list[dict[str, str]] = []

    for line in lines:
        match = re.match(
            r"^\s*-\s*([A-Z])[.、．)]\s*(.+?)\s*$",
            line,
        )

        if match:
            options.append(
                {
                    "key": match.group(1).upper(),
                    "text": match.group(2).strip(),
                }
            )

    return options


def split_sections(markdown: str) -> dict[str, str]:
    """
    根据一级标题切分试卷。
    """
    lines = markdown.splitlines()

    sections: dict[str, list[str]] = {}
    current = None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# ") and stripped[2:].strip() in SECTION_MAP:
            current = SECTION_MAP[stripped[2:].strip()]
            sections[current] = []
            continue

        if current:
            sections[current].append(line)

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }


def parse_choice_section(
    text: str,
    section: str,
) -> list[dict[str, Any]]:
    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    i = 0

    while i < len(lines):
        number = parse_question_header(lines[i])

        if number is None:
            i += 1
            continue

        question_lines: list[str] = []
        option_lines: list[str] = []

        i += 1

        while i < len(lines):
            if parse_question_header(lines[i]) is not None:
                break

            line = lines[i]

            if re.match(r"^\s*-\s*[A-Z][.、．)]\s*", line):
                option_lines.append(line)
            elif line.strip():
                question_lines.append(line.strip())

            i += 1

        question_text = "\n".join(question_lines).strip()

        # 去掉答题提示
        question_text = re.sub(
            r"\*\*作答：.*?\*\*",
            "",
            question_text,
        ).strip()

        question_text = question_text.replace(
            "Choose all correct answers.",
            "",
        ).strip()

        options = parse_options(option_lines)

        if section == "multiple_choice":
            question_type = "multiple_choice"
        else:
            question_type = "single_choice"

        questions.append(
            {
                "question_id": f"{section.upper()}_{number}",
                "section": section,
                "number": number,
                "type": question_type,
                "question": question_text,
                "options": options,
                "correct_answer": "",
                "explanation": "",
            }
        )

    return questions


def parse_listening(text: str) -> list[dict[str, Any]]:
    """
    听力特殊处理。

    Part A/B/C 都从 1 开始，因此 question_id 必须包含 Part。
    """

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part = None
    i = 0

    while i < len(lines):

        part_match = re.match(
            r"^\s*##\s*Part\s+([ABC])\s*$",
            lines[i],
            re.IGNORECASE,
        )

        if part_match:
            current_part = part_match.group(1).upper()
            i += 1
            continue

        if current_part is None:
            i += 1
            continue

        number = parse_question_header(lines[i])

        if number is None:
            i += 1
            continue

        question_lines: list[str] = []
        option_lines: list[str] = []

        i += 1

        while i < len(lines):

            if re.match(
                r"^\s*##\s*Part\s+[ABC]\s*$",
                lines[i],
                re.IGNORECASE,
            ):
                break

            if parse_question_header(lines[i]) is not None:
                break

            line = lines[i]

            if re.match(
                r"^\s*-\s*[A-Z][.、．)]\s*",
                line,
            ):
                option_lines.append(line)
            elif line.strip():
                question_lines.append(line.strip())

            i += 1

        questions.append(
            {
                "question_id": f"LISTENING_{current_part}_{number}",
                "section": "listening",
                "part": current_part,
                "number": number,
                "type": "single_choice",
                "question": "\n".join(question_lines).strip(),
                "options": parse_options(option_lines),
                "correct_answer": "",
                "explanation": "",
            }
        )

    return questions


def parse_translation(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part = None
    i = 0

    while i < len(lines):

        part_match = re.match(
            r"^\s*##\s*Part\s+([AB])\s+(.+)$",
            lines[i],
            re.IGNORECASE,
        )

        if part_match:
            current_part = part_match.group(1).upper()
            i += 1
            continue

        number = parse_question_header(lines[i])

        if number is None:
            i += 1
            continue

        question_lines: list[str] = []

        i += 1

        while i < len(lines):
            if re.match(
                r"^\s*##\s*Part\s+[AB]\s+",
                lines[i],
                re.IGNORECASE,
            ):
                break

            if parse_question_header(lines[i]) is not None:
                break

            line = lines[i].strip()

            if line and not line.startswith("翻译："):
                question_lines.append(line)

            i += 1

        direction = (
            "zh_to_en"
            if current_part == "A"
            else "en_to_zh"
        )

        questions.append(
            {
                "question_id": f"TRANSLATION_{current_part}_{number}",
                "section": "translation",
                "part": current_part,
                "number": number,
                "type": "translation",
                "direction": direction,
                "question": "\n".join(question_lines).strip(),
                "options": [],
                "correct_answer": "",
                "explanation": "",
            }
        )

    return questions


def parse_writing(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    i = 0

    while i < len(lines):
        number = parse_question_header(lines[i])

        if number is None:
            i += 1
            continue

        prompt: list[str] = []

        i += 1

        while i < len(lines):
            if parse_question_header(lines[i]) is not None:
                break

            line = lines[i].strip()

            if line and not line.startswith("作文："):
                prompt.append(line)

            i += 1

        questions.append(
            {
                "question_id": f"WRITING_{number}",
                "section": "writing",
                "number": number,
                "type": "writing",
                "question": "\n".join(prompt).strip(),
                "options": [],
                "correct_answer": "",
                "explanation": "",
            }
        )

    return questions


def parse_exam(markdown: str) -> list[dict[str, Any]]:
    markdown = normalize_text(markdown)

    sections = split_sections(markdown)

    questions: list[dict[str, Any]] = []

    if "listening" in sections:
        questions.extend(
            parse_listening(sections["listening"])
        )

    if "single_choice" in sections:
        questions.extend(
            parse_choice_section(
                sections["single_choice"],
                "single_choice",
            )
        )

    if "multiple_choice" in sections:
        questions.extend(
            parse_choice_section(
                sections["multiple_choice"],
                "multiple_choice",
            )
        )

    if "cloze" in sections:
        questions.extend(
            parse_choice_section(
                sections["cloze"],
                "cloze",
            )
        )

    if "reading" in sections:
        questions.extend(
            parse_choice_section(
                sections["reading"],
                "reading",
            )
        )

    if "translation" in sections:
        questions.extend(
            parse_translation(sections["translation"])
        )

    if "writing" in sections:
        questions.extend(
            parse_writing(sections["writing"])
        )

    return questions


def answer_key_candidates(section: str, number: int, part: str | None):
    if section == "listening":
        return [
            f"{part}_{number}",
            f"Part {part}_{number}",
            f"{part}{number}",
        ]

    if section == "translation":
        return [
            f"{part}_{number}",
            f"Part {part}_{number}",
        ]

    return [
        str(number),
        f"{number}",
    ]


def parse_answer_blocks(markdown: str) -> dict[tuple[str, str | None, int], str]:
    """
    解析答案解析文件中的：

    Part A:
    1. A
    2. C

    单项选择:
    1 B
    ...

    多项选择:
    1 A,C

    等内容。
    """

    lines = markdown.splitlines()

    current_section = None
    current_part = None

    result: dict[tuple[str, str | None, int], str] = {}

    section_aliases = {
        "听力": "listening",
        "单项选择": "single_choice",
        "多选题": "multiple_choice",
        "完形填空": "cloze",
        "阅读理解": "reading",
        "翻译": "translation",
        "写作": "writing",
    }

    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("#"):
            heading = re.sub(r"^#+\s*", "", line).strip()

            matched = None

            for alias, section in section_aliases.items():
                if alias in heading:
                    matched = section
                    break

            if matched:
                current_section = matched
                current_part = None

            part_match = re.search(
                r"Part\s+([ABC])",
                heading,
                re.IGNORECASE,
            )

            if part_match:
                current_part = part_match.group(1).upper()

        if current_section and current_part is None:
            part_match = re.search(
                r"Part\s+([ABC])",
                line,
                re.IGNORECASE,
            )

            if part_match:
                current_part = part_match.group(1).upper()

        answer = extract_answer_from_line(line)

        if answer:
            number_match = re.match(
                r"^\s*(\d+)\s*[.、．)]?\s*",
                line,
            )

            if number_match:
                number = int(number_match.group(1))

                result[
                    (
                        current_section or "",
                        current_part,
                        number,
                    )
                ] = answer

        i += 1

    return result


def parse_reference_answers(markdown: str) -> dict[str, dict[str, Any]]:
    """
    从答案解析文件中提取：
    - 正确答案
    - 参考答案
    - 解析

    对选择题使用正确答案。
    对翻译/写作使用参考答案。
    """

    lines = markdown.splitlines()

    result: dict[str, dict[str, Any]] = {}

    current_section = None
    current_part = None
    current_number = None

    section_aliases = {
        "听力": "listening",
        "单项选择": "single_choice",
        "多选题": "multiple_choice",
        "完形填空": "cloze",
        "阅读理解": "reading",
        "翻译": "translation",
        "写作": "writing",
    }

    for i, raw_line in enumerate(lines):
        line = raw_line.strip()

        if line.startswith("#"):
            heading = re.sub(r"^#+\s*", "", line).strip()

            for alias, section in section_aliases.items():
                if alias in heading:
                    current_section = section
                    current_number = None

            part_match = re.search(
                r"Part\s+([ABC])",
                heading,
                re.IGNORECASE,
            )

            if part_match:
                current_part = part_match.group(1).upper()

        number_match = re.match(
            r"^\s*(?:###\s*)?(\d+)[.、．)]\s*(.*)$",
            line,
        )

        if number_match and current_section:
            current_number = int(number_match.group(1))

            question_text = number_match.group(2).strip()

            key = (
                f"{current_section.upper()}_"
                f"{current_part + '_' if current_part else ''}"
                f"{current_number}"
            )

            result[key] = {
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
                "question_text": question_text,
            }

            # 查找紧随其后的内容
            for future in lines[i + 1:i + 8]:
                future = future.strip()

                if not future:
                    continue

                answer = extract_answer_from_line(future)

                if answer and not result[key]["correct_answer"]:
                    result[key]["correct_answer"] = answer
                    continue

                if future.startswith("答案："):
                    value = future.split("：", 1)[1].strip()
                    result[key]["correct_answer"] = normalize_answer(value)

                if future.startswith("参考答案："):
                    result[key]["reference_answer"] = (
                        future.split("：", 1)[1].strip()
                    )

                if future.startswith("解析："):
                    result[key]["explanation"] = (
                        future.split("：", 1)[1].strip()
                    )

    return result


def attach_answers(
    questions: list[dict[str, Any]],
    answer_markdown: str,
) -> list[dict[str, Any]]:

    answer_data = parse_reference_answers(answer_markdown)

    for question in questions:
        section = question["section"]
        number = question["number"]
        part = question.get("part")

        key = (
            f"{section.upper()}_"
            f"{part + '_' if part else ''}"
            f"{number}"
        )

        info = answer_data.get(key)

        if not info:
            continue

        question["correct_answer"] = info.get(
            "correct_answer",
            "",
        )

        question["reference_answer"] = info.get(
            "reference_answer",
            "",
        )

        question["explanation"] = info.get(
            "explanation",
            "",
        )

    return questions


def build_exam(
    exam_file: str | Path,
    answer_file: str | Path | None = None,
) -> dict[str, Any]:

    exam_path = Path(exam_file)

    if not exam_path.exists():
        raise FileNotFoundError(
            f"试卷不存在: {exam_path}"
        )

    exam_text = exam_path.read_text(
        encoding="utf-8"
    )

    questions = parse_exam(exam_text)

    if answer_file:
        answer_path = Path(answer_file)

        if not answer_path.exists():
            raise FileNotFoundError(
                f"答案解析不存在: {answer_path}"
            )

        answer_text = answer_path.read_text(
            encoding="utf-8"
        )

        questions = attach_answers(
            questions,
            answer_text,
        )

    return {
        "version": "1.0",
        "exam_file": str(exam_path),
        "answer_file": (
            str(answer_file)
            if answer_file
            else None
        ),
        "question_count": len(questions),
        "questions": questions,
    }


def validate_exam(exam: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    questions = exam.get("questions", [])

    if not questions:
        errors.append("没有解析到任何题目")
        return errors

    ids = set()

    for q in questions:
        qid = q.get("question_id")

        if not qid:
            errors.append("存在题目缺少 question_id")
            continue

        if qid in ids:
            errors.append(
                f"重复 question_id: {qid}"
            )

        ids.add(qid)

        if not q.get("question"):
            errors.append(
                f"{qid} 缺少题目内容"
            )

        if q["type"] in {
            "single_choice",
            "multiple_choice",
        }:
            if not q.get("options"):
                errors.append(
                    f"{qid} 没有选项"
                )

            if not q.get("correct_answer"):
                errors.append(
                    f"{qid} 缺少正确答案"
                )

    return errors


def main():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--exam",
        required=True,
    )

    parser.add_argument(
        "--answers",
        required=False,
    )

    parser.add_argument(
        "--output",
        required=False,
    )

    args = parser.parse_args()

    exam = build_exam(
        args.exam,
        args.answers,
    )

    errors = validate_exam(exam)

    print("=" * 70)
    print("748686 ENGLISH EXAM PARSER V1.0")
    print("=" * 70)

    print(
        f"题目总数: {exam['question_count']}"
    )

    if errors:
        print()
        print("❌ VALIDATION FAILED")

        for error in errors:
            print(f"   - {error}")

        raise SystemExit(1)

    print("✅ VALIDATION PASSED")

    counts: dict[str, int] = {}

    for q in exam["questions"]:
        key = q["type"]
        counts[key] = counts.get(key, 0) + 1

    print()
    for key, value in counts.items():
        print(f"   {key}: {value}")

    if args.output:
        output_path = Path(args.output)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            json.dumps(
                exam,
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

        print()
        print(
            f"✅ 已写入: {output_path}"
        )


if __name__ == "__main__":
    main()
