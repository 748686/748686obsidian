#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Parser V1.2

职责：
1. 解析实际试卷 Markdown
2. 解析答案与解析 Markdown
3. 建立稳定 question_id
4. 保留题目、选项、题型、正确答案、参考答案、解析
5. 不修改任何英语学习生成文件

V1.2 重点修复：
- 不再要求章节必须是 # 一级标题
- 支持 # / ## / ### 等 Markdown 标题层级
- 章节标题按“中文章节编号 + 标题”识别
- Listening Part A/B/C 独立解析
- Listening A/B/C 标准答案严格按 1~5 分组
- 普通选择题按章节严格绑定答案
- Multiple Choice 独立绑定
- Reading 不再混入 Single Choice
- Translation / Writing 保留 V1.1 已通过逻辑
- question_id 稳定化
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


# ============================================================
# SECTION
# ============================================================

SECTION_MAP = {
    "一、听力": "listening",
    "二、单项选择": "single_choice",
    "三、多选题": "multiple_choice",
    "四、完形填空": "cloze",
    "五、阅读理解": "reading",
    "六、翻译": "translation",
    "七、写作": "writing",
}


ANSWER_SECTION_ALIASES = {
    "听力": "listening",
    "单项选择": "single_choice",
    "多选题": "multiple_choice",
    "完形填空": "cloze",
    "阅读理解": "reading",
    "翻译": "translation",
    "写作": "writing",
}


SECTION_ORDER = [
    "listening",
    "single_choice",
    "multiple_choice",
    "cloze",
    "reading",
    "translation",
    "writing",
]


# ============================================================
# TEXT
# ============================================================

def normalize_text(text: str) -> str:
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def normalize_answer(value: str | None) -> str:
    """
    A,C
    A，C
    A、C
    AC
    C,A

    -> A,C
    """

    if value is None:
        return ""

    value = value.strip().upper()

    value = value.replace("，", ",")
    value = value.replace("、", ",")
    value = value.replace("；", ",")
    value = value.replace(";", ",")

    value = re.sub(r"\s+", "", value)

    if re.fullmatch(r"[A-Z]+", value):
        letters = sorted(set(value))
        return ",".join(letters)

    letters = re.findall(r"[A-Z]", value)

    if not letters:
        return value

    return ",".join(sorted(set(letters)))


# ============================================================
# QUESTION NUMBER
# ============================================================

def parse_question_number(line: str) -> int | None:
    """
    支持：

    ### 1.
    ## 1.
    1.
    1、
    1)
    **1.**
    **第5题**
    """

    cleaned = line.strip()

    cleaned = re.sub(
        r"^#+\s*",
        "",
        cleaned,
    )

    cleaned = re.sub(
        r"^\*\*\s*",
        "",
        cleaned,
    )

    cleaned = re.sub(
        r"\s*\*\*$",
        "",
        cleaned,
    )

    match = re.match(
        r"^\s*(?:第\s*)?(\d+)\s*[.、．)]",
        cleaned,
    )

    if match:
        return int(match.group(1))

    match = re.match(
        r"^\s*第\s*(\d+)\s*题",
        cleaned,
    )

    if match:
        return int(match.group(1))

    return None


def parse_question_header(line: str) -> int | None:
    return parse_question_number(line)


# ============================================================
# OPTIONS
# ============================================================

def parse_options(
    lines: list[str],
) -> list[dict[str, str]]:

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


# ============================================================
# SECTION HEADING
# ============================================================

def normalize_heading(line: str) -> str:
    """
    去除 Markdown 标题符号：

    # 一、听力
    ## 一、听力
    ### 一、听力

    -> 一、听力
    """

    value = line.strip()

    value = re.sub(
        r"^#+\s*",
        "",
        value,
    )

    value = value.strip()

    return value


def detect_exam_section(
    line: str,
) -> str | None:

    heading = normalize_heading(line)

    for alias, section in SECTION_MAP.items():

        if heading.startswith(alias):

            return section

    return None


def split_sections(
    markdown: str,
) -> dict[str, str]:
    """
    V1.2：

    不再要求必须是 # 一级标题。

    支持：

    # 一、听力
    ## 一、听力
    ### 一、听力

    并且允许标题后存在附加说明。
    """

    lines = markdown.splitlines()

    sections: dict[str, list[str]] = {}

    current: str | None = None

    for line in lines:

        detected = detect_exam_section(line)

        if detected:

            current = detected

            if current not in sections:
                sections[current] = []

            continue

        if current:
            sections[current].append(line)

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }


# ============================================================
# CHOICE QUESTIONS
# ============================================================

def parse_choice_section(
    text: str,
    section: str,
) -> list[dict[str, Any]]:

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    i = 0

    while i < len(lines):

        number = parse_question_header(
            lines[i]
        )

        if number is None:
            i += 1
            continue

        question_lines: list[str] = []
        option_lines: list[str] = []

        i += 1

        while i < len(lines):

            if (
                parse_question_header(
                    lines[i]
                )
                is not None
            ):
                break

            line = lines[i]

            if re.match(
                r"^\s*-\s*[A-Z][.、．)]\s*",
                line,
            ):

                option_lines.append(line)

            elif line.strip():

                question_lines.append(
                    line.strip()
                )

            i += 1

        question_text = "\n".join(
            question_lines
        ).strip()

        question_text = re.sub(
            r"\*\*作答：.*?\*\*",
            "",
            question_text,
            flags=re.DOTALL,
        ).strip()

        question_text = question_text.replace(
            "Choose all correct answers.",
            "",
        ).strip()

        if section == "multiple_choice":

            question_type = "multiple_choice"

        elif section == "cloze":

            question_type = "cloze"

        else:

            question_type = "single_choice"

        questions.append(
            {
                "question_id": (
                    f"{section.upper()}_"
                    f"{number:02d}"
                ),
                "section": section,
                "number": number,
                "type": question_type,
                "question": question_text,
                "options": parse_options(
                    option_lines
                ),
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            }
        )

    return questions


# ============================================================
# LISTENING
# ============================================================

def detect_listening_part(
    line: str,
) -> str | None:

    match = re.search(
        r"\bPart\s+([ABC])\b",
        line,
        re.IGNORECASE,
    )

    if match:

        return match.group(1).upper()

    return None


def parse_listening(
    text: str,
) -> list[dict[str, Any]]:

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part: str | None = None

    i = 0

    while i < len(lines):

        part = detect_listening_part(
            lines[i]
        )

        if part:

            current_part = part
            i += 1
            continue

        if current_part is None:

            i += 1
            continue

        number = parse_question_header(
            lines[i]
        )

        if number is None:

            i += 1
            continue

        question_lines: list[str] = []
        option_lines: list[str] = []

        i += 1

        while i < len(lines):

            next_part = detect_listening_part(
                lines[i]
            )

            if next_part:

                break

            if (
                parse_question_header(
                    lines[i]
                )
                is not None
            ):

                break

            line = lines[i]

            if re.match(
                r"^\s*-\s*[A-Z][.、．)]\s*",
                line,
            ):

                option_lines.append(line)

            elif line.strip():

                question_lines.append(
                    line.strip()
                )

            i += 1

        questions.append(
            {
                "question_id": (
                    f"LISTENING_"
                    f"{current_part}_"
                    f"{number:02d}"
                ),
                "section": "listening",
                "part": current_part,
                "number": number,
                "type": "single_choice",
                "question": "\n".join(
                    question_lines
                ).strip(),
                "options": parse_options(
                    option_lines
                ),
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            }
        )

    return questions


# ============================================================
# TRANSLATION
# ============================================================

def parse_translation(
    text: str,
) -> list[dict[str, Any]]:

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part: str | None = None

    i = 0

    while i < len(lines):

        part_match = re.search(
            r"Part\s+([AB])\b",
            lines[i],
            re.IGNORECASE,
        )

        if part_match:

            current_part = (
                part_match.group(1).upper()
            )

            i += 1
            continue

        number = parse_question_header(
            lines[i]
        )

        if number is None:

            i += 1
            continue

        question_lines: list[str] = []

        i += 1

        while i < len(lines):

            if re.search(
                r"Part\s+[AB]\b",
                lines[i],
                re.IGNORECASE,
            ):

                break

            if (
                parse_question_header(
                    lines[i]
                )
                is not None
            ):

                break

            line = lines[i].strip()

            if (
                line
                and not line.startswith("翻译：")
            ):

                question_lines.append(line)

            i += 1

        direction = (
            "zh_to_en"
            if current_part == "A"
            else "en_to_zh"
        )

        questions.append(
            {
                "question_id": (
                    f"TRANSLATION_"
                    f"{current_part}_"
                    f"{number:02d}"
                ),
                "section": "translation",
                "part": current_part,
                "number": number,
                "type": "translation",
                "direction": direction,
                "question": "\n".join(
                    question_lines
                ).strip(),
                "options": [],
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            }
        )

    return questions


# ============================================================
# WRITING
# ============================================================

def parse_writing(
    text: str,
) -> list[dict[str, Any]]:

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    i = 0

    while i < len(lines):

        number = parse_question_header(
            lines[i]
        )

        if number is None:

            i += 1
            continue

        prompt: list[str] = []

        i += 1

        while i < len(lines):

            if (
                parse_question_header(
                    lines[i]
                )
                is not None
            ):

                break

            line = lines[i].strip()

            if (
                line
                and not line.startswith("作文：")
            ):

                prompt.append(line)

            i += 1

        questions.append(
            {
                "question_id": (
                    f"WRITING_{number:02d}"
                ),
                "section": "writing",
                "number": number,
                "type": "writing",
                "question": "\n".join(
                    prompt
                ).strip(),
                "options": [],
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            }
        )

    return questions


# ============================================================
# EXAM
# ============================================================

def parse_exam(
    markdown: str,
) -> list[dict[str, Any]]:

    markdown = normalize_text(markdown)

    sections = split_sections(
        markdown
    )

    questions: list[dict[str, Any]] = []

    if "listening" in sections:

        questions.extend(
            parse_listening(
                sections["listening"]
            )
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
            parse_translation(
                sections["translation"]
            )
        )

    if "writing" in sections:

        questions.extend(
            parse_writing(
                sections["writing"]
            )
        )

    return questions


# ============================================================
# ANSWER PARSING
# ============================================================

def clean_answer_line(
    line: str,
) -> str:

    line = line.strip()

    line = re.sub(
        r"^\*\*\s*",
        "",
        line,
    )

    line = re.sub(
        r"\s*\*\*$",
        "",
        line,
    )

    return line.strip()


def extract_choice_answer(
    line: str,
) -> str:

    line = clean_answer_line(line)

    match = re.match(
        r"^\s*\d+\s*[.、．)]?\s*"
        r"([A-Za-z]"
        r"(?:\s*[,，、;；]\s*[A-Za-z])*"
        r")\s*$",
        line,
    )

    if not match:

        return ""

    return normalize_answer(
        match.group(1)
    )


def is_answer_heading(
    line: str,
) -> bool:

    heading = normalize_heading(
        line
    )

    return (
        "标准答案" in heading
        or "答案与解析" in heading
    )


def detect_answer_section(
    line: str,
) -> tuple[str | None, str | None]:

    heading = normalize_heading(
        line
    )

    # 去掉前面的中文章节编号
    heading = re.sub(
        r"^[一二三四五六七八九十]+、",
        "",
        heading,
    ).strip()

    for alias, section in ANSWER_SECTION_ALIASES.items():

        if heading.startswith(alias):

            part_match = re.search(
                r"Part\s+([ABC])",
                heading,
                re.IGNORECASE,
            )

            part = (
                part_match.group(1).upper()
                if part_match
                else None
            )

            return section, part

    return None, None


# ============================================================
# ANSWER BLOCK HELPERS
# ============================================================

def collect_numbered_answers(
    lines: list[str],
    start: int,
    end: int,
) -> list[tuple[int, str]]:

    """
    在一个明确的答案区块中提取：

    1. A
    2. C
    3. B
    ...

    不跨越区块。
    """

    results: list[
        tuple[int, str]
    ] = []

    i = start

    while i < end:

        line = lines[i].strip()

        answer = extract_choice_answer(
            line
        )

        if answer:

            match = re.match(
                r"^\**\s*(\d+)"
                r"\s*[.、．)]?",
                line,
            )

            if match:

                number = int(
                    match.group(1)
                )

                results.append(
                    (
                        number,
                        answer,
                    )
                )

        i += 1

    return results


def split_answer_blocks(
    markdown: str,
) -> list[dict[str, Any]]:

    """
    把答案文件拆成：

    {
        section,
        part,
        lines
    }

    只依据明确章节标题。
    """

    lines = markdown.splitlines()

    blocks: list[dict[str, Any]] = []

    current_section: str | None = None
    current_part: str | None = None
    current_start = 0

    def flush(end_index: int):

        nonlocal current_section
        nonlocal current_part
        nonlocal current_start

        if current_section is None:
            return

        blocks.append(
            {
                "section": current_section,
                "part": current_part,
                "start": current_start,
                "end": end_index,
            }
        )

    i = 0

    while i < len(lines):

        line = lines[i].strip()

        section, part = detect_answer_section(
            line
        )

        if section:

            if current_section is not None:

                flush(i)

            current_section = section
            current_part = part
            current_start = i + 1

        i += 1

    if current_section is not None:

        flush(len(lines))

    return blocks


# ============================================================
# LISTENING ANSWERS
# ============================================================

def parse_listening_answers(
    lines: list[str],
    start: int,
    end: int,
) -> dict[str, str]:

    """
    Listening 标准答案：

    A:
    1~5

    B:
    1~5

    C:
    1~5

    如果答案文件没有写 Part A/B/C，
    则按照连续的三个 1~5 答案块自动分组。
    """

    result: dict[str, str] = {}

    # --------------------------------------------------------
    # 第一种情况：明确出现 Part A/B/C
    # --------------------------------------------------------

    explicit_parts: dict[
        str,
        list[tuple[int, str]],
    ] = {
        "A": [],
        "B": [],
        "C": [],
    }

    current_part: str | None = None

    for i in range(start, end):

        line = lines[i].strip()

        part = detect_listening_part(
            line
        )

        if part:

            current_part = part
            continue

        answer = extract_choice_answer(
            line
        )

        if (
            current_part
            and answer
        ):

            match = re.match(
                r"^\**\s*(\d+)"
                r"\s*[.、．)]?",
                line,
            )

            if match:

                number = int(
                    match.group(1)
                )

                if 1 <= number <= 5:

                    explicit_parts[
                        current_part
                    ].append(
                        (
                            number,
                            answer,
                        )
                    )

    explicit_count = sum(
        len(v)
        for v in explicit_parts.values()
    )

    if explicit_count >= 15:

        for part in ["A", "B", "C"]:

            for number, answer in (
                explicit_parts[part]
            ):

                result[
                    f"LISTENING_{part}_"
                    f"{number:02d}"
                ] = answer

        return result

    # --------------------------------------------------------
    # 第二种情况：没有 Part 标题
    #
    # 自动识别三个 1~5 连续答案组
    # --------------------------------------------------------

    answer_groups: list[
        list[tuple[int, str]]
    ] = []

    current_group: list[
        tuple[int, str]
    ] = []

    expected_number = 1

    for i in range(start, end):

        line = lines[i].strip()

        answer = extract_choice_answer(
            line
        )

        if not answer:
            continue

        match = re.match(
            r"^\**\s*(\d+)"
            r"\s*[.、．)]?",
            line,
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        if number == expected_number:

            current_group.append(
                (
                    number,
                    answer,
                )
            )

            expected_number += 1

            if expected_number == 6:

                answer_groups.append(
                    current_group
                )

                current_group = []
                expected_number = 1

        elif number == 1:

            current_group = [
                (
                    1,
                    answer,
                )
            ]

            expected_number = 2

    if current_group:

        answer_groups.append(
            current_group
        )

    parts = ["A", "B", "C"]

    for index, group in enumerate(
        answer_groups[:3]
    ):

        part = parts[index]

        for number, answer in group:

            result[
                f"LISTENING_{part}_"
                f"{number:02d}"
            ] = answer

    return result


# ============================================================
# GENERAL CHOICE ANSWERS
# ============================================================

def parse_general_choice_answers(
    lines: list[str],
    start: int,
    end: int,
    section: str,
) -> dict[str, str]:

    result: dict[str, str] = {}

    for i in range(start, end):

        line = lines[i].strip()

        answer = extract_choice_answer(
            line
        )

        if not answer:
            continue

        match = re.match(
            r"^\**\s*(\d+)"
            r"\s*[.、．)]?",
            line,
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        if number < 1:
            continue

        result[
            f"{section.upper()}_"
            f"{number:02d}"
        ] = answer

    return result


# ============================================================
# REFERENCE ANSWERS
# ============================================================

def extract_reference_after_number(
    lines: list[str],
    start_index: int,
) -> str:

    collected: list[str] = []

    i = start_index + 1

    while i < len(lines):

        line = lines[i].strip()

        if not line:

            if collected:
                break

            i += 1
            continue

        if (
            line.startswith("#")
            or parse_question_number(line)
            is not None
        ):

            break

        if line.startswith("解析："):

            break

        if line.startswith("答案："):

            value = line.split(
                "：",
                1,
            )[1].strip()

            if value:
                collected.append(value)

            break

        if line.startswith("参考答案："):

            value = line.split(
                "：",
                1,
            )[1].strip()

            if value:
                collected.append(value)

            break

        collected.append(
            re.sub(
                r"^\*\*|\*\*$",
                "",
                line,
            ).strip()
        )

        i += 1

    return "\n".join(
        x for x in collected if x
    ).strip()


def parse_translation_references(
    markdown: str,
) -> dict[str, dict[str, str]]:

    lines = markdown.splitlines()

    result: dict[
        str,
        dict[str, str],
    ] = {}

    current_part: str | None = None
    in_translation = False

    for i, raw in enumerate(lines):

        line = raw.strip()

        heading = normalize_heading(
            line
        )

        translation_match = re.match(
            r"翻译\s*([AB])",
            heading,
            re.IGNORECASE,
        )

        if translation_match:

            in_translation = True

            current_part = (
                translation_match
                .group(1)
                .upper()
            )

            continue

        if not in_translation:
            continue

        if (
            line.startswith("#")
            and "翻译" not in heading
            and "标准答案" not in heading
            and "答案与解析" not in heading
        ):

            current_part = None
            in_translation = False
            continue

        if current_part is None:
            continue

        number = parse_question_number(
            line
        )

        if number is None:
            continue

        answer = extract_reference_after_number(
            lines,
            i,
        )

        if not answer:
            continue

        key = (
            f"TRANSLATION_"
            f"{current_part}_"
            f"{number:02d}"
        )

        result[key] = {
            "reference_answer": answer,
        }

    return result


# ============================================================
# WRITING REFERENCE
# ============================================================

def parse_writing_reference(
    markdown: str,
) -> dict[str, dict[str, str]]:

    lines = markdown.splitlines()

    result: dict[
        str,
        dict[str, str],
    ] = {}

    in_reference = False

    collected: list[str] = []

    for raw in lines:

        line = raw.strip()

        heading = normalize_heading(
            line
        )

        if "写作参考范文" in heading:

            in_reference = True
            collected = []

            continue

        if not in_reference:
            continue

        if (
            line.startswith("#")
            and "写作参考范文" not in heading
        ):

            break

        if re.match(
            r"^\*\*\s*\d+\s*[.、．)]\s*\*\*$",
            line,
        ):

            continue

        if not line:

            if collected:
                collected.append("")

            continue

        cleaned = re.sub(
            r"^\*\*|\*\*$",
            "",
            line,
        ).strip()

        collected.append(
            cleaned
        )

    reference = "\n".join(
        collected
    ).strip()

    reference = re.sub(
        r"\n{3,}",
        "\n\n",
        reference,
    )

    if reference:

        result["WRITING_01"] = {
            "reference_answer": reference,
        }

    return result


# ============================================================
# EXPLANATIONS
# ============================================================

def parse_explanations(
    markdown: str,
) -> dict[str, str]:

    lines = markdown.splitlines()

    result: dict[str, str] = {}

    current_section: str | None = None
    current_part: str | None = None
    current_number: int | None = None

    for raw in lines:

        line = raw.strip()

        section, part = (
            detect_answer_section(line)
        )

        if section:

            current_section = section
            current_part = part
            current_number = None

            continue

        number = parse_question_number(
            line
        )

        if (
            number is not None
            and current_section
        ):

            current_number = number

            continue

        if (
            line.startswith("解析：")
            and current_section
            and current_number is not None
        ):

            explanation = line.split(
                "：",
                1,
            )[1].strip()

            if current_section == "listening":

                if current_part is None:
                    continue

                key = (
                    f"LISTENING_"
                    f"{current_part}_"
                    f"{current_number:02d}"
                )

            elif current_section == "translation":

                if current_part is None:
                    continue

                key = (
                    f"TRANSLATION_"
                    f"{current_part}_"
                    f"{current_number:02d}"
                )

            elif current_section == "writing":

                key = (
                    f"WRITING_"
                    f"{current_number:02d}"
                )

            else:

                key = (
                    f"{current_section.upper()}_"
                    f"{current_number:02d}"
                )

            result[key] = explanation

    return result


# ============================================================
# REFERENCE ANSWERS
# ============================================================

def parse_reference_answers(
    markdown: str,
) -> dict[str, dict[str, Any]]:

    lines = markdown.splitlines()

    result: dict[
        str,
        dict[str, Any],
    ] = {}

    blocks = split_answer_blocks(
        markdown
    )

    # --------------------------------------------------------
    # 选择题答案
    # --------------------------------------------------------

    for block in blocks:

        section = block["section"]
        part = block["part"]
        start = block["start"]
        end = block["end"]

        if section == "listening":

            answers = parse_listening_answers(
                lines,
                start,
                end,
            )

            for key, answer in answers.items():

                result[key] = {
                    "correct_answer": answer,
                    "reference_answer": "",
                    "explanation": "",
                }

        elif section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
        }:

            answers = (
                parse_general_choice_answers(
                    lines,
                    start,
                    end,
                    section,
                )
            )

            for key, answer in answers.items():

                result[key] = {
                    "correct_answer": answer,
                    "reference_answer": "",
                    "explanation": "",
                }

    # --------------------------------------------------------
    # 翻译
    # --------------------------------------------------------

    translation_answers = (
        parse_translation_references(
            markdown
        )
    )

    for key, info in (
        translation_answers.items()
    ):

        result.setdefault(
            key,
            {
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            },
        )

        result[key][
            "reference_answer"
        ] = info[
            "reference_answer"
        ]

    # --------------------------------------------------------
    # 写作
    # --------------------------------------------------------

    writing_answers = (
        parse_writing_reference(
            markdown
        )
    )

    for key, info in (
        writing_answers.items()
    ):

        result.setdefault(
            key,
            {
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            },
        )

        result[key][
            "reference_answer"
        ] = info[
            "reference_answer"
        ]

    # --------------------------------------------------------
    # 解析
    # --------------------------------------------------------

    explanations = parse_explanations(
        markdown
    )

    for key, explanation in (
        explanations.items()
    ):

        result.setdefault(
            key,
            {
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            },
        )

        result[key][
            "explanation"
        ] = explanation

    return result


# ============================================================
# ATTACH
# ============================================================

def attach_answers(
    questions: list[dict[str, Any]],
    answer_markdown: str,
) -> list[dict[str, Any]]:

    answer_data = (
        parse_reference_answers(
            answer_markdown
        )
    )

    for question in questions:

        qid = question[
            "question_id"
        ]

        info = answer_data.get(
            qid
        )

        if not info:
            continue

        question[
            "correct_answer"
        ] = info.get(
            "correct_answer",
            "",
        )

        question[
            "reference_answer"
        ] = info.get(
            "reference_answer",
            "",
        )

        question[
            "explanation"
        ] = info.get(
            "explanation",
            "",
        )

    return questions


# ============================================================
# BUILD
# ============================================================

def build_exam(
    exam_file: str | Path,
    answer_file: str | Path | None = None,
) -> dict[str, Any]:

    exam_path = Path(
        exam_file
    )

    if not exam_path.exists():

        raise FileNotFoundError(
            f"试卷不存在: {exam_path}"
        )

    exam_text = (
        exam_path.read_text(
            encoding="utf-8"
        )
    )

    questions = parse_exam(
        exam_text
    )

    if answer_file:

        answer_path = Path(
            answer_file
        )

        if not answer_path.exists():

            raise FileNotFoundError(
                f"答案解析不存在: {answer_path}"
            )

        answer_text = (
            answer_path.read_text(
                encoding="utf-8"
            )
        )

        questions = attach_answers(
            questions,
            answer_text,
        )

    return {
        "version": "1.2",
        "exam_file": str(
            exam_path
        ),
        "answer_file": (
            str(answer_file)
            if answer_file
            else None
        ),
        "question_count": len(
            questions
        ),
        "questions": questions,
    }


# ============================================================
# VALIDATE
# ============================================================

def validate_exam(
    exam: dict[str, Any],
) -> list[str]:

    errors: list[str] = []

    questions = exam.get(
        "questions",
        [],
    )

    if not questions:

        errors.append(
            "没有解析到任何题目"
        )

        return errors

    ids: set[str] = set()

    for q in questions:

        qid = q.get(
            "question_id"
        )

        if not qid:

            errors.append(
                "存在题目缺少 question_id"
            )

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

            if not q.get(
                "correct_answer"
            ):

                errors.append(
                    f"{qid} 缺少正确答案"
                )

    return errors


# ============================================================
# CLI
# ============================================================

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

    errors = validate_exam(
        exam
    )

    print("=" * 70)

    print(
        "748686 ENGLISH EXAM PARSER V1.2"
    )

    print("=" * 70)

    print(
        f"题目总数: "
        f"{exam['question_count']}"
    )

    if errors:

        print()
        print(
            "❌ VALIDATION FAILED"
        )

        for error in errors:

            print(
                f"   - {error}"
            )

        raise SystemExit(1)

    print(
        "✅ VALIDATION PASSED"
    )

    print()

    counts: dict[str, int] = {}

    for q in exam["questions"]:

        key = q["type"]

        counts[key] = (
            counts.get(
                key,
                0,
            )
            + 1
        )

    for key, value in counts.items():

        print(
            f"   {key}: {value}"
        )

    if args.output:

        output_path = Path(
            args.output
        )

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
            f"✅ 已写入: "
            f"{output_path}"
        )


if __name__ == "__main__":
    main()
