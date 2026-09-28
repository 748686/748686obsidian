#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 ENGLISH EXAM PARSER V1.6

Purpose
-------
Parse the generated English exam and its answer/explanation file.

V1.6 is based on the real generated exam format.

Supported structures:
- Listening Part A / B / C
- Single choice
- Multiple choice
- Cloze passage + separate numbered options
- Reading comprehension
- Translation Part A / B
- Writing

IMPORTANT
---------
PARSER_VERSION remains "1.6" intentionally.

The JSON contract is unchanged.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PARSER_VERSION = "1.6"


# ----------------------------------------------------------------------
# Section definitions
# ----------------------------------------------------------------------

SECTION_MAP = {
    "一、听力": "listening",
    "一、听力原文": "listening",
    "一、听力理解": "listening",
    "一、听力部分": "listening",
    "一、听力测试": "listening",
    "一、听力题目": "listening",
    "一、听力试题": "listening",

    "二、单项选择": "single_choice",

    "三、多选题": "multiple_choice",
    "三、多项选择": "multiple_choice",

    "四、完形填空": "cloze",

    "五、阅读理解": "reading",

    "六、翻译": "translation",

    "七、写作": "writing",
}


ANSWER_SECTION_ALIASES = {
    "一、听力": "listening",
    "二、听力": "listening",
    "听力": "listening",

    "一、听力答案": "listening",
    "二、听力答案": "listening",
    "听力答案": "listening",

    "一、听力原文": "listening",
    "听力原文": "listening",

    "二、单项选择": "single_choice",
    "单项选择": "single_choice",
    "二、单项选择答案": "single_choice",
    "单项选择答案": "single_choice",

    "三、多选题": "multiple_choice",
    "多选题": "multiple_choice",
    "多项选择": "multiple_choice",
    "三、多选题答案": "multiple_choice",
    "多选题答案": "multiple_choice",
    "多项选择答案": "multiple_choice",

    "四、完形填空": "cloze",
    "完形填空": "cloze",
    "四、完形填空答案": "cloze",
    "完形填空答案": "cloze",

    "五、阅读理解": "reading",
    "阅读理解": "reading",
    "五、阅读理解答案": "reading",
    "阅读理解答案": "reading",

    "六、翻译": "translation",
    "翻译": "translation",
    "六、翻译答案": "translation",
    "翻译答案": "translation",

    "七、写作": "writing",
    "写作": "writing",
    "七、写作答案": "writing",
    "写作答案": "writing",
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


# ----------------------------------------------------------------------
# Generic helpers
# ----------------------------------------------------------------------

def normalize_text(text: Any) -> str:
    if text is None:
        return ""

    text = str(text)
    text = text.replace("\ufeff", "")
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()


def normalize_answer(answer: Any) -> str:
    """
    Normalize answer representation.

    Examples:
        A
        a
        A,C
        A、C
        A, C
        A,B,D
        [A, C]

    -> canonical representation.
    """

    if answer is None:
        return ""

    if isinstance(answer, (list, tuple, set)):
        values = []

        for item in answer:
            value = normalize_answer(item)

            if value:
                values.append(value)

        if not values:
            return ""

        flat = []

        for value in values:
            flat.extend(value.split(","))

        return ",".join(
            sorted(
                set(
                    x
                    for x in flat
                    if x
                )
            )
        )

    text = normalize_text(answer)

    if not text:
        return ""

    text = text.upper()

    text = text.replace("，", ",")
    text = text.replace("、", ",")
    text = text.replace("；", ",")
    text = text.replace(";", ",")
    text = text.replace("／", "/")
    text = text.replace(" ", "")
    text = text.replace("　", "")

    text = re.sub(
        r"^[\[\(（【]+",
        "",
        text,
    )

    text = re.sub(
        r"[\]\)）】]+$",
        "",
        text,
    )

    if "," in text:

        parts = [
            x.strip()
            for x in text.split(",")
            if x.strip()
        ]

        letters = []

        for part in parts:

            match = re.search(
                r"[A-D]",
                part,
            )

            if match:
                letters.append(
                    match.group(0)
                )
            else:
                letters.append(
                    part
                )

        return ",".join(
            sorted(
                set(letters)
            )
        )

    if re.fullmatch(
        r"[A-D]{2,}",
        text,
    ):

        return ",".join(
            sorted(
                set(text)
            )
        )

    match = re.fullmatch(
        r"[A-D]",
        text,
    )

    if match:
        return match.group(0)

    return text


def normalize_heading(
    text: str,
) -> str:

    text = normalize_text(
        text
    )

    text = re.sub(
        r"^#+\s*",
        "",
        text,
    )

    text = re.sub(
        r"^\d+[、.．]\s*",
        "",
        text,
    )

    return text.strip()


def normalize_section_text(
    text: str,
) -> str:

    text = normalize_heading(
        text
    )

    text = re.sub(
        r"\s+",
        "",
        text,
    )

    text = text.replace(
        "：",
        ":",
    )

    text = text.replace(
        "（",
        "(",
    )

    text = text.replace(
        "）",
        ")",
    )

    text = text.replace(
        "－",
        "-",
    )

    text = text.replace(
        "—",
        "-",
    )

    return text.strip()


def strip_section_number(
    text: str,
) -> str:

    text = normalize_section_text(
        text
    )

    text = re.sub(
        r"^[一二三四五六七八九十百千万]+[、.．:：]\s*",
        "",
        text,
    )

    text = re.sub(
        r"^\d+[、.．:：]\s*",
        "",
        text,
    )

    return text.strip()


def parse_question_number(
    text: str,
) -> Optional[int]:

    text = normalize_text(
        text
    )

    if not re.match(
        r"^#{1,6}\s*",
        text,
    ):
        return None

    match = re.match(
        r"^#{1,6}\s*(\d+)\s*[.．、)]\s*(.*)$",
        text,
    )

    if not match:
        return None

    try:
        return int(
            match.group(1)
        )

    except ValueError:
        return None


def parse_question_header(
    text: str,
) -> Optional[Tuple[int, str]]:

    text = normalize_text(
        text
    )

    if not re.match(
        r"^#{1,6}\s*",
        text,
    ):
        return None

    match = re.match(
        r"^#{1,6}\s*(\d+)\s*[.．、)]\s*(.*?)\s*$",
        text,
    )

    if not match:
        return None

    number = int(
        match.group(1)
    )

    question = normalize_text(
        match.group(2)
    )

    return number, question


def parse_options(
    lines: List[str],
) -> List[Dict[str, str]]:

    options: List[
        Dict[str, str]
    ] = []

    option_pattern = re.compile(
        r"^\s*(?:-\s*)?([A-D])\s*[.．、:：]\s*(.*?)\s*$",
        re.IGNORECASE,
    )

    for line in lines:

        match = option_pattern.match(
            normalize_text(line)
        )

        if not match:
            continue

        letter = match.group(1).upper()

        text = normalize_text(
            match.group(2)
        )

        options.append({
            "key": letter,
            "text": text,
        })

    return options


def make_question_id(
    section: str,
    number: int,
    listening_part: Optional[str] = None,
) -> str:

    if section == "listening":

        part = (
            listening_part
            or "A"
        )

        return (
            f"listening_{part}_{number}"
        )

    if section == "translation":

        part = (
            listening_part
            or "A"
        )

        return (
            f"translation_{part}_{number}"
        )

    return (
        f"{section}_{number}"
    )


# ----------------------------------------------------------------------
# Section detection
# ----------------------------------------------------------------------

def detect_exam_section(
    line: str,
) -> Optional[str]:

    raw = normalize_text(
        line
    )

    if not raw:
        return None

    text = normalize_section_text(
        raw
    )

    if not text:
        return None

    text = re.sub(
        r"^>\s*",
        "",
        text,
    ).strip()

    for title, section in SECTION_MAP.items():

        if text == normalize_section_text(
            title
        ):
            return section

    body = strip_section_number(
        text
    )

    body = body.replace(
        "：",
        ":",
    )

    body_base = re.split(
        r"[\(:\-]",
        body,
        maxsplit=1,
    )[0].strip()

    listening_prefixes = (
        "听力",
        "听力原文",
        "听力理解",
        "听力部分",
        "听力测试",
        "听力题目",
        "听力试题",
    )

    if (
        body_base == "听力"
        or body_base == "听力原文"
        or body_base.startswith("听力理解")
        or body_base.startswith("听力部分")
        or body_base.startswith("听力测试")
        or body_base.startswith("听力题目")
        or body_base.startswith("听力试题")
    ):
        return "listening"

    if any(
        body.startswith(prefix)
        for prefix in listening_prefixes
    ):
        return "listening"

    if (
        body_base == "单项选择"
        or body_base.startswith("单项选择题")
        or body_base.startswith("单项选择")
    ):
        return "single_choice"

    if (
        body_base == "多选题"
        or body_base == "多项选择"
        or body_base.startswith("多选题")
        or body_base.startswith("多项选择")
    ):
        return "multiple_choice"

    if (
        body_base == "完形填空"
        or body_base.startswith("完形填空")
    ):
        return "cloze"

    if (
        body_base == "阅读理解"
        or body_base.startswith("阅读理解")
    ):
        return "reading"

    if (
        body_base == "翻译"
        or body_base.startswith("翻译题")
        or body_base.startswith("翻译")
    ):
        return "translation"

    if (
        body_base == "写作"
        or body_base.startswith("写作题")
        or body_base.startswith("写作")
    ):
        return "writing"

    part_match = re.match(
        r"^第\s*([一二三四五六七八九十百千万\d]+)"
        r"\s*部分\s*[:：]?\s*(.*)$",
        text,
    )

    if part_match:

        part_body = normalize_text(
            part_match.group(2)
        )

        part_body = re.sub(
            r"\s+",
            "",
            part_body,
        )

        if part_body.startswith(
            "听力"
        ):
            return "listening"

        if part_body.startswith(
            "单项选择"
        ):
            return "single_choice"

        if (
            part_body.startswith("多选题")
            or part_body.startswith("多项选择")
        ):
            return "multiple_choice"

        if part_body.startswith(
            "完形填空"
        ):
            return "cloze"

        if part_body.startswith(
            "阅读理解"
        ):
            return "reading"

        if part_body.startswith(
            "翻译"
        ):
            return "translation"

        if part_body.startswith(
            "写作"
        ):
            return "writing"

    return None


def split_sections(
    text: str,
) -> Dict[str, str]:

    lines = normalize_text(
        text
    ).splitlines()

    sections: Dict[
        str,
        List[str]
    ] = {}

    current: Optional[str] = None

    for line in lines:

        detected = detect_exam_section(
            line
        )

        if detected:

            current = detected

            sections.setdefault(
                current,
                [],
            )

            continue

        if current:

            sections[current].append(
                line
            )

    return {
        key: "\n".join(value).strip()
        for key, value in sections.items()
    }


# ----------------------------------------------------------------------
# Listening section fallback recovery
# ----------------------------------------------------------------------

def contains_listening_markers(
    text: str,
) -> bool:

    lines = normalize_text(
        text
    ).splitlines()

    parts = set()

    for line in lines:

        part = detect_listening_part(
            line
        )

        if part:
            parts.add(part)

    return {
        "A",
        "B",
        "C",
    }.issubset(parts)


def recover_listening_section(
    text: str,
) -> str:

    lines = normalize_text(
        text
    ).splitlines()

    if not contains_listening_markers(
        text
    ):
        return ""

    first_part_index: Optional[int] = None

    for index, line in enumerate(lines):

        if detect_listening_part(
            line
        ):

            first_part_index = index

            break

    if first_part_index is None:
        return ""

    start_index = first_part_index

    for index in range(
        first_part_index - 1,
        -1,
        -1,
    ):

        detected = detect_exam_section(
            lines[index]
        )

        if detected == "listening":

            start_index = index

            break

        if detected in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
            "translation",
            "writing",
        }:
            break

        candidate = normalize_text(
            lines[index]
        )

        candidate = re.sub(
            r"^#+\s*",
            "",
            candidate,
        )

        candidate = re.sub(
            r"^[一二三四五六七八九十百千万]+[、.．]\s*",
            "",
            candidate,
        )

        if (
            candidate.startswith("听力")
            or candidate.startswith("第一部分")
            or candidate.startswith("第1部分")
        ):

            start_index = index

            break

    end_index = len(lines)

    for index in range(
        first_part_index,
        len(lines),
    ):

        detected = detect_exam_section(
            lines[index]
        )

        if detected in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
            "translation",
            "writing",
        }:

            end_index = index

            break

    return "\n".join(
        lines[
            start_index:end_index
        ]
    ).strip()


# ----------------------------------------------------------------------
# Question construction
# ----------------------------------------------------------------------

def base_question(
    section: str,
    number: int,
    question: str,
    options: Optional[
        List[Dict[str, str]]
    ] = None,
    listening_part: Optional[str] = None,
) -> Dict[str, Any]:

    question_data: Dict[str, Any] = {
        "id": make_question_id(
            section,
            number,
            listening_part,
        ),
        "section": section,
        "number": number,
        "question": normalize_text(
            question
        ),
        "options": options or [],
        "correct_answer": None,
        "explanation": "",
        "reference_answer": None,
        "graded": False,
        "review_required": False,
    }

    if listening_part:

        question_data["part"] = (
            listening_part
        )

    return question_data


def parse_choice_section(
    text: str,
    section: str,
) -> List[Dict[str, Any]]:

    lines = normalize_text(
        text
    ).splitlines()

    questions: List[
        Dict[str, Any]
    ] = []

    current: Optional[
        Dict[str, Any]
    ] = None

    option_buffer: List[str] = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        parsed = parse_question_header(
            clean
        )

        if parsed:

            if current is not None:

                current["options"] = (
                    parse_options(
                        option_buffer
                    )
                )

                questions.append(
                    current
                )

            number, question_text = parsed

            current = base_question(
                section=section,
                number=number,
                question=question_text,
            )

            option_buffer = []

            continue

        if current is None:
            continue

        option_buffer.append(
            clean
        )

    if current is not None:

        current["options"] = (
            parse_options(
                option_buffer
            )
        )

        questions.append(
            current
        )

    return questions


# ----------------------------------------------------------------------
# Listening exam
# ----------------------------------------------------------------------

def detect_listening_part(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    match = re.match(
        r"^#{0,6}\s*Part\s+([ABC])"
        r"(?:\s*[:：\-–—]\s*.*)?$",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).upper()

    return None


def parse_listening_question_line(
    line: str,
) -> Optional[Tuple[int, str]]:

    clean = normalize_text(
        line
    )

    if not clean:
        return None

    parsed = parse_question_header(
        clean
    )

    if parsed is not None:
        return parsed

    match = re.match(
        r"^(\d+)\s*[.．、)]\s*(.*?)\s*$",
        clean,
    )

    if match:

        try:
            number = int(
                match.group(1)
            )

        except ValueError:
            return None

        question_text = normalize_text(
            match.group(2)
        )

        return number, question_text

    return None


def parse_listening(
    text: str,
) -> List[Dict[str, Any]]:

    lines = normalize_text(
        text
    ).splitlines()

    questions: List[
        Dict[str, Any]
    ] = []

    current_part: Optional[str] = None

    current: Optional[
        Dict[str, Any]
    ] = None

    option_buffer: List[str] = []

    pending_number: Optional[int] = None
    pending_part: Optional[str] = None

    def flush_current() -> None:

        nonlocal current
        nonlocal option_buffer

        if current is None:
            return

        current["options"] = (
            parse_options(
                option_buffer
            )
        )

        questions.append(
            current
        )

        current = None
        option_buffer = []

    def flush_pending_as_empty() -> None:

        nonlocal pending_number
        nonlocal pending_part

        if (
            pending_number is None
            or pending_part is None
        ):
            return

        current_question = base_question(
            section="listening",
            number=pending_number,
            question="",
            listening_part=pending_part,
        )

        questions.append(
            current_question
        )

        pending_number = None
        pending_part = None

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        part = detect_listening_part(
            clean
        )

        if part:

            if pending_number is not None:

                flush_pending_as_empty()

            flush_current()

            current_part = part

            continue

        if pending_number is not None:

            nested_question = (
                parse_listening_question_line(
                    clean
                )
            )

            if nested_question is not None:

                flush_pending_as_empty()

                number, question_text = (
                    nested_question
                )

                current = base_question(
                    section="listening",
                    number=number,
                    question=question_text,
                    listening_part=current_part,
                )

                option_buffer = []

                continue

            option_candidate = re.match(
                r"^\s*(?:-\s*)?[A-D]\s*[.．、:：]\s*(.*?)\s*$",
                clean,
                re.IGNORECASE,
            )

            if not option_candidate:

                pending_part_value = (
                    pending_part
                    or current_part
                )

                current = base_question(
                    section="listening",
                    number=pending_number,
                    question=clean,
                    listening_part=pending_part_value,
                )

                pending_number = None
                pending_part = None

                option_buffer = []

                continue

            current = base_question(
                section="listening",
                number=pending_number,
                question="",
                listening_part=(
                    pending_part
                    or current_part
                ),
            )

            pending_number = None
            pending_part = None

            option_buffer = []

            option_buffer.append(
                clean
            )

            continue

        parsed = parse_listening_question_line(
            clean
        )

        if parsed is not None:

            flush_current()

            number, question_text = parsed

            if not question_text:

                pending_number = number
                pending_part = current_part

                continue

            current = base_question(
                section="listening",
                number=number,
                question=question_text,
                listening_part=current_part,
            )

            option_buffer = []

            continue

        if current is not None:

            option_buffer.append(
                clean
            )

    if pending_number is not None:

        flush_pending_as_empty()

    flush_current()

    return questions


# ----------------------------------------------------------------------
# Cloze
# ----------------------------------------------------------------------

def extract_cloze_blank_numbers(
    text: str,
) -> List[int]:

    numbers = []

    for match in re.finditer(
        r"\(\s*(\d+)\s*\)",
        text,
    ):

        number = int(
            match.group(1)
        )

        if number not in numbers:

            numbers.append(
                number
            )

    return numbers


def parse_inline_cloze_options(
    line: str,
) -> List[Dict[str, str]]:

    result: List[
        Dict[str, str]
    ] = []

    pattern = re.compile(
        r"([A-D])\s*[.．、:：]\s*(.*?)(?=\s+[A-D]\s*[.．、:：]|$)",
        re.IGNORECASE,
    )

    for match in pattern.finditer(
        line
    ):

        result.append({
            "key": match.group(1).upper(),
            "text": normalize_text(
                match.group(2)
            ),
        })

    return result


def parse_cloze(
    text: str,
) -> List[Dict[str, Any]]:

    lines = normalize_text(
        text
    ).splitlines()

    passage_lines: List[str] = []

    in_options = False

    option_section_lines: List[str] = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if clean == "选择题":

            in_options = True

            continue

        if not in_options:

            if clean:

                passage_lines.append(
                    clean
                )

        else:

            option_section_lines.append(
                clean
            )

    passage = "\n".join(
        passage_lines
    ).strip()

    blank_numbers = (
        extract_cloze_blank_numbers(
            passage
        )
    )

    if not blank_numbers:

        blank_numbers = list(
            range(1, 11)
        )

    question_options: Dict[
        int,
        List[Dict[str, str]]
    ] = {}

    current_number: Optional[int] = None

    current_option_lines: List[str] = []

    def flush_current() -> None:

        nonlocal current_number
        nonlocal current_option_lines

        if current_number is None:
            return

        parsed = parse_options(
            current_option_lines
        )

        if (
            not parsed
            and current_option_lines
        ):

            parsed = parse_inline_cloze_options(
                " ".join(
                    current_option_lines
                )
            )

        question_options[
            current_number
        ] = parsed

        current_number = None
        current_option_lines = []

    for line in option_section_lines:

        if not line:
            continue

        match = re.match(
            r"^#{1,6}\s*(\d+)\s*[.．、)]\s*(.*)$",
            line,
        )

        if match:

            flush_current()

            current_number = int(
                match.group(1)
            )

            inline_rest = normalize_text(
                match.group(2)
            )

            if inline_rest:

                inline_options = (
                    parse_inline_cloze_options(
                        f"{current_number}. {inline_rest}"
                    )
                )

                if inline_options:

                    question_options[
                        current_number
                    ] = inline_options

                    current_option_lines = []

                else:

                    current_option_lines = [
                        inline_rest
                    ]

            continue

        if current_number is not None:

            current_option_lines.append(
                line
            )

    flush_current()

    questions: List[
        Dict[str, Any]
    ] = []

    for number in blank_numbers:

        question_text = passage

        question_text = re.sub(
            rf"_{2,}\s*\(\s*{number}\s*\)\s*_{2,}",
            f"____ ({number}) ____",
            question_text,
        )

        options = question_options.get(
            number,
            [],
        )

        questions.append(
            base_question(
                section="cloze",
                number=number,
                question=question_text,
                options=options,
            )
        )

    return questions


# ----------------------------------------------------------------------
# Translation
# ----------------------------------------------------------------------

def detect_translation_part(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    if re.search(
        r"Part\s+A",
        text,
        re.IGNORECASE,
    ):
        return "A"

    if re.search(
        r"Part\s+B",
        text,
        re.IGNORECASE,
    ):
        return "B"

    return None


def is_translation_prompt(
    line: str,
) -> bool:

    text = normalize_text(
        line
    )

    return (
        text.startswith("翻译：")
        or text.startswith("翻译:")
    )


def parse_translation(
    text: str,
) -> List[Dict[str, Any]]:

    lines = normalize_text(
        text
    ).splitlines()

    questions: List[
        Dict[str, Any]
    ] = []

    current_part: Optional[str] = None

    current: Optional[
        Dict[str, Any]
    ] = None

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        part = detect_translation_part(
            clean
        )

        if part:

            current_part = part

            continue

        parsed = parse_question_header(
            clean
        )

        if parsed:

            if current is not None:

                questions.append(
                    current
                )

            number, prompt = parsed

            current = base_question(
                section="translation",
                number=number,
                question=prompt,
                listening_part=current_part,
            )

            current["part"] = (
                current_part
            )

            continue

        if current is None:
            continue

        if is_translation_prompt(
            clean
        ):
            continue

    if current is not None:

        questions.append(
            current
        )

    return questions


# ----------------------------------------------------------------------
# Writing
# ----------------------------------------------------------------------

def parse_writing(
    text: str,
) -> List[Dict[str, Any]]:

    lines = normalize_text(
        text
    ).splitlines()

    questions: List[
        Dict[str, Any]
    ] = []

    current: Optional[
        Dict[str, Any]
    ] = None

    body_lines: List[str] = []

    def flush_current() -> None:

        nonlocal current
        nonlocal body_lines

        if current is None:
            return

        question_text = normalize_text(
            current.get(
                "question",
                "",
            )
        )

        if not question_text:

            prompt_lines: List[str] = []

            for raw in body_lines:

                clean = normalize_text(
                    raw
                )

                if not clean:
                    continue

                if re.match(
                    r"^作文\s*[:：]",
                    clean,
                ):
                    break

                if re.fullmatch(
                    r"_+",
                    clean,
                ):
                    continue

                prompt_lines.append(
                    clean
                )

            question_text = " ".join(
                prompt_lines
            ).strip()

            current["question"] = (
                question_text
            )

        current["prompt"] = (
            question_text
        )

        current["question"] = (
            normalize_text(
                current["question"]
            )
        )

        questions.append(
            current
        )

        current = None
        body_lines = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        parsed = parse_question_header(
            clean
        )

        if parsed:

            flush_current()

            number, prompt = parsed

            current = base_question(
                section="writing",
                number=number,
                question=prompt,
            )

            body_lines = []

            continue

        if current is not None:

            body_lines.append(
                clean
            )

    flush_current()

    return questions


# ----------------------------------------------------------------------
# Full exam parser
# ----------------------------------------------------------------------

def parse_exam(
    exam_text: str,
) -> List[Dict[str, Any]]:

    sections = split_sections(
        exam_text
    )

    listening_questions: List[
        Dict[str, Any]
    ] = []

    if "listening" in sections:

        listening_questions = (
            parse_listening(
                sections["listening"]
            )
        )

    if len(listening_questions) < 15:

        recovered_listening = (
            recover_listening_section(
                exam_text
            )
        )

        if recovered_listening:

            recovered_questions = (
                parse_listening(
                    recovered_listening
                )
            )

            if len(recovered_questions) > len(
                listening_questions
            ):

                listening_questions = (
                    recovered_questions
                )

    questions: List[
        Dict[str, Any]
    ] = []

    questions.extend(
        listening_questions
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
            parse_cloze(
                sections["cloze"]
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


# ----------------------------------------------------------------------
# Answer parsing
# ----------------------------------------------------------------------

def clean_answer_line(
    line: str,
) -> str:

    text = normalize_text(
        line
    )

    text = re.sub(
        r"^[>\-\*\s]+",
        "",
        text,
    )

    return text.strip()


def extract_choice_answer(
    line: str,
) -> Optional[str]:

    text = clean_answer_line(
        line
    )

    text = text.replace(
        "**",
        "",
    )

    match = re.search(
        r"答案\s*[:：]\s*"
        r"([A-D](?:\s*[,、，]\s*[A-D])*)",
        text,
        re.IGNORECASE,
    )

    if match:

        return normalize_answer(
            match.group(1)
        )

    match = re.match(
        r"^(\d+)\s*[.．、)]\s*"
        r"([A-D](?:\s*[,、，]\s*[A-D])*)"
        r"\s*$",
        text,
        re.IGNORECASE,
    )

    if match:

        return normalize_answer(
            match.group(2)
        )

    match = re.match(
        r"^\*{0,2}\s*"
        r"(\d+)\s*[.．、)]\s*"
        r"\*{0,2}\s*"
        r"([A-D](?:\s*[,、，]\s*[A-D])*)"
        r"\s*$",
        text,
        re.IGNORECASE,
    )

    if match:

        return normalize_answer(
            match.group(2)
        )

    return None


def is_answer_heading(
    line: str,
) -> bool:

    text = normalize_text(
        line
    )

    if not text:
        return False

    normalized = normalize_heading(
        text
    )

    patterns = [
        "答案",
        "答案与解析",
        "参考答案",
        "标准答案",
        "听力答案",
        "单项选择答案",
        "多选题答案",
        "多项选择答案",
        "完形填空答案",
        "阅读理解答案",
        "翻译参考答案",
        "写作参考范文",
        "解析",
    ]

    return any(
        normalized == pattern
        or normalized.startswith(
            pattern + " "
        )
        or normalized.startswith(
            pattern + "："
        )
        or normalized.startswith(
            pattern + ":"
        )
        for pattern in patterns
    )


# ----------------------------------------------------------------------
# ANSWER SECTION DETECTION
# ----------------------------------------------------------------------

def normalize_answer_heading(
    line: str,
) -> str:
    """
    Normalize answer-file headings.

    Examples:

        ## 二、标准答案
        ### 听力
        #### Part A

    ->

        二、标准答案
        听力
        Part A
    """

    text = normalize_text(
        line
    )

    text = re.sub(
        r"^#+\s*",
        "",
        text,
    )

    text = text.strip()

    return text


def is_standard_answer_heading(
    line: str,
) -> bool:

    text = normalize_answer_heading(
        line
    )

    text_without_number = re.sub(
        r"^[一二三四五六七八九十百千万\d]+[、.．:：]\s*",
        "",
        text,
    )

    normalized = normalize_section_text(
        text_without_number
    )

    return normalized in {
        "答案",
        "答案与解析",
        "标准答案",
        "参考答案",
    }


def detect_answer_section(
    line: str,
) -> Optional[str]:

    text = normalize_heading(
        line
    )

    text_without_number = re.sub(
        r"^[一二三四五六七八九十百千万]+[、.．]\s*",
        "",
        text,
    )

    for title, section in (
        ANSWER_SECTION_ALIASES.items()
    ):

        if text == title:
            return section

        if text_without_number == title:
            return section

    for title, section in (
        ANSWER_SECTION_ALIASES.items()
    ):

        if text.startswith(title):
            return section

        if text_without_number.startswith(title):
            return section

    if (
        text_without_number.startswith(
            "听力答案"
        )
        or text_without_number == "听力"
    ):

        return "listening"

    return None


def detect_answer_part(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    match = re.search(
        r"Part\s+([ABC])",
        text,
        re.IGNORECASE,
    )

    if match:

        return match.group(1).upper()

    if re.search(
        r"汉译英",
        text,
    ):

        return "A"

    if re.search(
        r"英译汉",
        text,
    ):

        return "B"

    return None


def collect_numbered_answers(
    lines: List[str],
) -> Dict[int, str]:

    answers: Dict[
        int,
        str
    ] = {}

    for line in lines:

        answer = extract_choice_answer(
            line
        )

        if answer is None:
            continue

        text = (
            clean_answer_line(
                line
            ).replace(
                "**",
                "",
            )
        )

        match = re.match(
            r"^(\d+)\s*[.．、)]",
            text,
        )

        if match:

            number = int(
                match.group(1)
            )

            answers[number] = answer

    return answers


# ----------------------------------------------------------------------
# FIXED ANSWER BLOCK SPLITTER
# ----------------------------------------------------------------------

def split_answer_blocks(
    text: str,
) -> Dict[str, str]:
    """
    Split the real generated answer/explanation file.

    Important real structure:

        ## 一、听力原文
        ### Part A
        ...
        ### Part B
        ...
        ### Part C
        ...

        ## 二、标准答案
        ### 听力
        #### Part A
        1. B
        2. C
        ...

        ### 单项选择
        1. B
        ...

    The transcript section MUST NOT be treated as listening answers.

    The key rule is:

        "标准答案" starts the answer area.

    Inside the answer area, headings such as "听力",
    "单项选择", etc. start actual answer blocks.
    """

    lines = normalize_text(
        text
    ).splitlines()

    blocks: Dict[
        str,
        List[str]
    ] = {}

    in_standard_answer = False

    current: Optional[str] = None

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            if current:
                blocks.setdefault(
                    current,
                    [],
                ).append("")
            continue

        # ----------------------------------------------------------
        # First priority:
        # Detect the real answer area.
        #
        # Example:
        # ## 二、标准答案
        # ----------------------------------------------------------

        if is_standard_answer_heading(
            clean
        ):

            in_standard_answer = True
            current = None

            continue

        # ----------------------------------------------------------
        # Before "标准答案":
        #
        # Ignore everything completely.
        #
        # This prevents:
        #
        # ## 一、听力原文
        # ### Part A
        # 1. Hello...
        #
        # from becoming listening answers.
        # ----------------------------------------------------------

        if not in_standard_answer:

            continue

        # ----------------------------------------------------------
        # Inside standard answer area:
        # recognize answer subsection.
        #
        # Example:
        #
        # ### 听力
        # ### 单项选择
        # ### 多项选择
        # ...
        # ----------------------------------------------------------

        detected = detect_answer_section(
            clean
        )

        if detected:

            current = detected

            blocks.setdefault(
                current,
                [],
            )

            continue

        # ----------------------------------------------------------
        # Keep content belonging to current answer section.
        # ----------------------------------------------------------

        if current:

            blocks[current].append(
                clean
            )

    return {
        key: "\n".join(value).strip()
        for key, value in blocks.items()
    }


# ----------------------------------------------------------------------
# Listening answer parsing
# ----------------------------------------------------------------------

def is_listening_answer_boundary(
    line: str,
) -> bool:

    text = normalize_heading(
        line
    )

    if not text:
        return False

    patterns = [
        "标准答案",
        "参考答案",
        "答案与解析",
        "答案",
    ]

    for pattern in patterns:

        if text == pattern:
            return True

        if text.startswith(
            pattern + "："
        ):
            return True

        if text.startswith(
            pattern + ":"
        ):
            return True

        if text.startswith(
            pattern + " "
        ):
            return True

    return False


def is_standalone_listening_part(
    line: str,
) -> Optional[str]:

    clean = normalize_text(
        line
    )

    match = re.match(
        r"^#{0,6}\s*Part\s+([ABC])"
        r"(?:\s*[:：\-–—]\s*.*)?$",
        clean,
        re.IGNORECASE,
    )

    if match:

        return match.group(1).upper()

    return None


def is_numbered_answer_line(
    line: str,
) -> bool:

    return (
        extract_choice_answer(line)
        is not None
    )


def parse_listening_answers(
    text: str,
) -> Dict[Tuple[str, int], str]:
    """
    Parse listening answers from the actual answer block.

    Supported real structure:

        ### 听力

        #### Part A

        1. B
        2. C
        3. D
        4. D
        5. A

        #### Part B

        1. B
        2. A
        3. B
        4. B
        5. C

        #### Part C

        1. A
        2. B
        3. C
        4. C
        5. D

    Result:

        ("A", 1) -> "B"
        ("A", 2) -> "C"
        ...
        ("C", 5) -> "D"
    """

    lines = normalize_text(
        text
    ).splitlines()

    result: Dict[
        Tuple[str, int],
        str
    ] = {}

    current_part: Optional[str] = None

    explicit_part_mode = False

    flat_answers: List[str] = []

    # --------------------------------------------------------------
    # First pass:
    #
    # Determine whether the block contains explicit Part A/B/C.
    # --------------------------------------------------------------

    for line in lines:

        part = is_standalone_listening_part(
            line
        )

        if part:

            explicit_part_mode = True

            break

    # --------------------------------------------------------------
    # Second pass:
    # --------------------------------------------------------------

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        part = is_standalone_listening_part(
            clean
        )

        if part:

            current_part = part

            continue

        answer = extract_choice_answer(
            clean
        )

        if answer is None:
            continue

        text_clean = clean.replace(
            "**",
            "",
        )

        match = re.match(
            r"^(\d+)\s*[.．、)]",
            text_clean,
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        # ----------------------------------------------------------
        # Explicit Part A/B/C mode.
        # ----------------------------------------------------------

        if (
            explicit_part_mode
            and current_part
        ):

            result[
                (
                    current_part,
                    number,
                )
            ] = answer

        # ----------------------------------------------------------
        # Flat fallback mode.
        # ----------------------------------------------------------

        else:

            flat_answers.append(
                answer
            )

    # --------------------------------------------------------------
    # If explicit Part A/B/C answers were found, use them.
    # --------------------------------------------------------------

    if explicit_part_mode:

        # Normally this already contains all 15 answers.
        # Flat fallback is retained for unusual mixed formats.
        for index, answer in enumerate(
            flat_answers[:15]
        ):

            if index < 5:

                part = "A"
                number = index + 1

            elif index < 10:

                part = "B"
                number = index - 4

            else:

                part = "C"
                number = index - 9

            key = (
                part,
                number,
            )

            if key not in result:

                result[key] = answer

        return result

    # --------------------------------------------------------------
    # Flat 15-answer format.
    # --------------------------------------------------------------

    for index, answer in enumerate(
        flat_answers[:15]
    ):

        if index < 5:

            part = "A"
            number = index + 1

        elif index < 10:

            part = "B"
            number = index - 4

        else:

            part = "C"
            number = index - 9

        result[
            (
                part,
                number,
            )
        ] = answer

    return result


def parse_general_choice_answers(
    text: str,
) -> Dict[int, str]:

    lines = normalize_text(
        text
    ).splitlines()

    return collect_numbered_answers(
        lines
    )


def extract_reference_after_number(
    line: str,
) -> Optional[Tuple[int, str]]:

    text = clean_answer_line(
        line
    )

    text = text.replace(
        "**",
        "",
    )

    match = re.match(
        r"^(\d+)\s*[.．、)]\s*(.*?)\s*$",
        text,
    )

    if not match:
        return None

    number = int(
        match.group(1)
    )

    reference = normalize_text(
        match.group(2)
    )

    if not reference:
        return None

    return number, reference


def parse_translation_references(
    text: str,
) -> Dict[Tuple[str, int], str]:

    lines = normalize_text(
        text
    ).splitlines()

    result: Dict[
        Tuple[str, int],
        str
    ] = {}

    current_part: Optional[str] = None

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        part = detect_answer_part(
            clean
        )

        if part:

            current_part = part

            continue

        parsed = extract_reference_after_number(
            clean
        )

        if not parsed:
            continue

        number, reference = parsed

        if current_part in {
            "A",
            "B",
        }:

            result[
                (
                    current_part,
                    number,
                )
            ] = reference

    if not result:

        refs: List[str] = []

        for line in lines:

            parsed = (
                extract_reference_after_number(
                    line
                )
            )

            if parsed:

                refs.append(
                    parsed[1]
                )

        for index, reference in enumerate(
            refs[:10]
        ):

            if index < 5:

                part = "A"
                number = index + 1

            else:

                part = "B"
                number = index - 4

            result[
                (
                    part,
                    number,
                )
            ] = reference

    return result


def parse_writing_reference(
    text: str,
) -> Optional[str]:

    lines = normalize_text(
        text
    ).splitlines()

    collecting = False

    reference_lines: List[str] = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        heading = normalize_heading(
            clean
        )

        if "写作参考范文" in heading:

            collecting = True

            continue

        if not collecting:

            continue

        if re.match(
            r"^#{1,6}\s+",
            clean,
        ):

            if (
                "写作参考范文"
                not in heading
            ):

                break

        if re.fullmatch(
            r"\*{0,2}\s*1\s*[.．、)]\s*\*{0,2}",
            clean,
        ):

            continue

        reference_lines.append(
            clean.replace(
                "**",
                "",
            )
        )

    reference = " ".join(
        x
        for x in reference_lines
        if x
    ).strip()

    return reference or None


# ----------------------------------------------------------------------
# Explanation parsing
# ----------------------------------------------------------------------

def parse_explanations(
    text: str,
) -> Dict[
    Tuple[str, int],
    str
]:

    lines = normalize_text(
        text
    ).splitlines()

    result: Dict[
        Tuple[str, int],
        str
    ] = {}

    current_section: Optional[
        str
    ] = None

    current_number: Optional[
        int
    ] = None

    buffer: List[str] = []

    def flush() -> None:

        nonlocal current_section
        nonlocal current_number
        nonlocal buffer

        if (
            current_section is not None
            and current_number is not None
            and buffer
        ):

            value = " ".join(
                x.strip()
                for x in buffer
                if x.strip()
            ).strip()

            if value:

                result[
                    (
                        current_section,
                        current_number,
                    )
                ] = value

        current_number = None
        buffer = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        # ----------------------------------------------------------
        # IMPORTANT:
        # Do not let "一、听力原文" become an explanation section.
        #
        # Explanations are only meaningful after standard answer area.
        # ----------------------------------------------------------

        detected = detect_answer_section(
            clean
        )

        if detected:

            flush()

            current_section = detected

            continue

        if current_section == "listening":

            part = detect_answer_part(
                clean
            )

            if part:

                continue

        text_without_bold = (
            clean.replace(
                "**",
                "",
            )
        )

        match = re.match(
            r"^(\d+)\s*[.．、)]\s*(.*)$",
            text_without_bold,
        )

        if match:

            flush()

            try:

                current_number = int(
                    match.group(1)
                )

            except ValueError:

                current_number = None

            remainder = normalize_text(
                match.group(2)
            )

            if remainder:

                buffer.append(
                    remainder
                )

            continue

        if current_number is not None:

            buffer.append(
                clean
            )

    flush()

    return result


# ----------------------------------------------------------------------
# Reference answer aggregation
# ----------------------------------------------------------------------

def parse_reference_answers(
    answer_text: str,
) -> Dict[str, Any]:

    blocks = split_answer_blocks(
        answer_text
    )

    result: Dict[str, Any] = {
        "choice": {},
        "listening": {},
        "translation": {},
        "writing": None,
        "explanations": {},
    }

    listening_text = blocks.get(
        "listening",
        "",
    )

    if listening_text:

        result["listening"] = (
            parse_listening_answers(
                listening_text
            )
        )

    for section in [
        "single_choice",
        "multiple_choice",
        "cloze",
        "reading",
    ]:

        block = blocks.get(
            section,
            "",
        )

        if not block:
            continue

        result["choice"][section] = (
            parse_general_choice_answers(
                block
            )
        )

    translation_text = blocks.get(
        "translation",
        "",
    )

    if translation_text:

        result["translation"] = (
            parse_translation_references(
                translation_text
            )
        )

    writing_text = blocks.get(
        "writing",
        "",
    )

    if writing_text:

        result["writing"] = (
            parse_writing_reference(
                writing_text
            )
        )

    result["explanations"] = (
        parse_explanations(
            answer_text
        )
    )

    return result


# ----------------------------------------------------------------------
# Answer attachment
# ----------------------------------------------------------------------

def attach_answers(
    questions: List[Dict[str, Any]],
    answer_data: Dict[str, Any],
) -> List[Dict[str, Any]]:

    choice_answers = answer_data.get(
        "choice",
        {},
    )

    listening_answers = answer_data.get(
        "listening",
        {},
    )

    translation_answers = answer_data.get(
        "translation",
        {},
    )

    writing_reference = answer_data.get(
        "writing"
    )

    explanations = answer_data.get(
        "explanations",
        {},
    )

    listening_global_index = 0

    for question in questions:

        section = question["section"]

        number = question["number"]

        correct_answer: Optional[
            str
        ] = None

        reference_answer: Optional[
            str
        ] = None

        explanation = ""

        if section == "listening":

            part = question.get(
                "part",
                "A",
            )

            correct_answer = (
                listening_answers.get(
                    (
                        part,
                        number,
                    )
                )
            )

            if not correct_answer:

                global_number = (
                    listening_global_index
                    + 1
                )

                if global_number <= 5:

                    fallback_part = "A"
                    fallback_number = (
                        global_number
                    )

                elif global_number <= 10:

                    fallback_part = "B"
                    fallback_number = (
                        global_number - 5
                    )

                else:

                    fallback_part = "C"
                    fallback_number = (
                        global_number - 10
                    )

                correct_answer = (
                    listening_answers.get(
                        (
                            fallback_part,
                            fallback_number,
                        )
                    )
                )

            listening_global_index += 1

        elif section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
        }:

            section_answers = (
                choice_answers.get(
                    section,
                    {},
                )
            )

            correct_answer = (
                section_answers.get(
                    number
                )
            )

        elif section == "translation":

            part = question.get(
                "part"
            )

            if part:

                reference_answer = (
                    translation_answers.get(
                        (
                            part,
                            number,
                        )
                    )
                )

        elif section == "writing":

            reference_answer = (
                writing_reference
            )

        explanation = explanations.get(
            (
                section,
                number,
            ),
            "",
        )

        if (
            section == "listening"
            and not explanation
        ):

            current_global_number = (
                listening_global_index
            )

            explanation = explanations.get(
                (
                    "listening",
                    current_global_number,
                ),
                "",
            )

        question["correct_answer"] = (
            normalize_answer(
                correct_answer
            )
            if correct_answer is not None
            else None
        )

        question["reference_answer"] = (
            reference_answer
        )

        question["explanation"] = (
            explanation
        )

        if section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
            "listening",
        }:

            question["graded"] = (
                question[
                    "correct_answer"
                ]
                not in (
                    None,
                    "",
                )
            )

        elif section in {
            "translation",
            "writing",
        }:

            question["graded"] = False

            question[
                "review_required"
            ] = True

    return questions


# ----------------------------------------------------------------------
# Build complete exam
# ----------------------------------------------------------------------

def build_exam(
    exam_text: str,
    answer_text: Optional[str] = None,
) -> Dict[str, Any]:

    questions = parse_exam(
        exam_text
    )

    answer_data: Dict[str, Any] = {
        "choice": {},
        "listening": {},
        "translation": {},
        "writing": None,
        "explanations": {},
    }

    if answer_text:

        answer_data = (
            parse_reference_answers(
                answer_text
            )
        )

        questions = attach_answers(
            questions,
            answer_data,
        )

    return {
        "version": PARSER_VERSION,
        "parser": (
            "748686 ENGLISH EXAM PARSER V1.6"
        ),
        "total_questions": len(
            questions
        ),
        "questions": questions,
    }


# ----------------------------------------------------------------------
# Validation
# ----------------------------------------------------------------------

EXPECTED_COUNTS = {
    "listening": 15,
    "single_choice": 10,
    "multiple_choice": 10,
    "cloze": 10,
    "reading": 5,
    "translation": 10,
    "writing": 1,
}


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


def validate_exam(
    exam: Dict[str, Any],
) -> List[str]:

    errors: List[str] = []

    questions = exam.get(
        "questions",
        [],
    )

    if not questions:

        errors.append(
            "没有解析出任何题目"
        )

        return errors

    counts: Dict[str, int] = {}

    for question in questions:

        section = question.get(
            "section",
            "",
        )

        counts[section] = (
            counts.get(
                section,
                0,
            )
            + 1
        )

    for section, expected in (
        EXPECTED_COUNTS.items()
    ):

        actual = counts.get(
            section,
            0
        )

        if actual != expected:

            errors.append(
                f"{section}: 数量 {actual}, "
                f"预期 {expected}"
            )

    ids = [
        q.get("id")
        for q in questions
    ]

    if len(ids) != len(set(ids)):

        errors.append(
            "题目 ID 不唯一"
        )

    for question in questions:

        qid = question.get(
            "id",
            "<unknown>",
        )

        section = question.get(
            "section",
            "",
        )

        content = normalize_text(
            question.get(
                "question",
                "",
            )
        )

        if not content:

            errors.append(
                f"{qid}: 缺少题目内容"
            )

        if section in {
            "single_choice",
            "multiple_choice",
            "reading",
        }:

            options = question.get(
                "options",
                [],
            )

            if len(options) < 4:

                errors.append(
                    f"{qid}: 选项数量不足 "
                    f"({len(options)}/4)"
                )

        if section in AUTO_GRADED_TYPES:

            answer = normalize_answer(
                question.get(
                    "correct_answer"
                )
            )

            if not answer:

                errors.append(
                    f"{qid}: 缺少正确答案"
                )

    if len(questions) != 61:

        errors.append(
            f"题目总数错误: "
            f"{len(questions)} / 61"
        )

    return errors


# ----------------------------------------------------------------------
# Summary
# ----------------------------------------------------------------------

def build_summary(
    exam: Dict[str, Any],
) -> Dict[str, Any]:

    questions = exam.get(
        "questions",
        [],
    )

    counts: Dict[str, int] = {}

    auto_total = 0

    auto_answered = 0

    manual_total = 0

    for question in questions:

        section = question.get(
            "section",
            "",
        )

        counts[section] = (
            counts.get(
                section,
                0,
            )
            + 1
        )

        if section in AUTO_GRADED_TYPES:

            auto_total += 1

            if normalize_answer(
                question.get(
                    "correct_answer"
                )
            ):

                auto_answered += 1

        elif section in MANUAL_REVIEW_TYPES:

            manual_total += 1

    return {
        "total": len(questions),
        "counts": counts,
        "auto_graded": auto_total,
        "auto_with_answers": auto_answered,
        "manual_review": manual_total,
    }


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "748686 English Exam Parser V1.6"
        )
    )

    parser.add_argument(
        "--exam",
        required=True,
        help="考试试卷 Markdown 文件",
    )

    parser.add_argument(
        "--answers",
        required=False,
        default="",
        help="答案与解析 Markdown 文件",
    )

    parser.add_argument(
        "--output",
        required=False,
        default="",
        help="可选：输出 JSON 文件",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="执行结构验证",
    )

    args = parser.parse_args()

    exam_path = Path(
        args.exam
    )

    if not exam_path.exists():

        print(
            f"❌ 试卷不存在: {exam_path}",
            file=sys.stderr,
        )

        return 1

    exam_text = exam_path.read_text(
        encoding="utf-8"
    )

    answer_text = ""

    if args.answers:

        answer_path = Path(
            args.answers
        )

        if not answer_path.exists():

            print(
                f"❌ 答案文件不存在: {answer_path}",
                file=sys.stderr,
            )

            return 1

        answer_text = (
            answer_path.read_text(
                encoding="utf-8"
            )
        )

    exam = build_exam(
        exam_text,
        answer_text,
    )

    summary = build_summary(
        exam
    )

    print("=" * 70)

    print(
        "748686 ENGLISH EXAM PARSER V1.6"
    )

    print("=" * 70)

    print()

    print(
        f"题目总数: "
        f"{summary['total']}"
    )

    print()

    print("题型统计:")

    for section in SECTION_ORDER:

        print(
            f"  {section:18s} "
            f"{summary['counts'].get(section, 0)}"
        )

    print()

    print(
        f"自动评分题: "
        f"{summary['auto_graded']}"
    )

    print(
        f"其中已绑定标准答案: "
        f"{summary['auto_with_answers']}"
    )

    print(
        f"人工/语义评阅题: "
        f"{summary['manual_review']}"
    )

    if args.validate:

        errors = validate_exam(
            exam
        )

        print()

        if errors:

            print(
                "❌ VALIDATION FAILED"
            )

            print()

            for error in errors:

                print(
                    f"  ❌ {error}"
                )

            if args.output:

                Path(
                    args.output
                ).write_text(
                    json.dumps(
                        exam,
                        ensure_ascii=False,
                        indent=2,
                    ),
                    encoding="utf-8",
                )

            return 1

        print(
            "✅ VALIDATION PASSED"
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
            f"JSON 已输出: "
            f"{output_path}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
