#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 ENGLISH EXAM PARSER V1.6

Purpose
-------
Parse the generated English exam and its answer/explanation file.

V1.6
------
Listening answer binding repair.

Real standard-answer format:

## 二、标准答案

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

Important:
- Exam question parsing remains compatible with V1.6.
- JSON contract remains unchanged.
- Listening answers are parsed independently and deterministically.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PARSER_VERSION = "1.6"


# ======================================================================
# EXPECTED STRUCTURE
# ======================================================================

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
    "listening",
    "single_choice",
    "multiple_choice",
    "cloze",
    "reading",
}


MANUAL_REVIEW_TYPES = {
    "translation",
    "writing",
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


# ======================================================================
# BASIC TEXT HELPERS
# ======================================================================

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
    Normalize answer.

    Examples:
        B -> B
        b -> B
        A,C -> A,C
        A、C -> A,C
        [A, C] -> A,C
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

        letters = []

        for value in values:

            for part in value.split(","):

                part = part.strip()

                if part:
                    letters.append(part)

        return ",".join(
            sorted(set(letters))
        )

    text = normalize_text(answer)

    if not text:
        return ""

    text = text.upper()

    text = text.replace("，", ",")
    text = text.replace("、", ",")
    text = text.replace("；", ",")
    text = text.replace(";", ",")
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
                letters.append(part)

        return ",".join(
            sorted(set(letters))
        )

    if re.fullmatch(
        r"[A-D]{2,}",
        text,
    ):

        return ",".join(
            sorted(set(text))
        )

    if re.fullmatch(
        r"[A-D]",
        text,
    ):

        return text

    return text


# ======================================================================
# MARKDOWN / HEADING HELPERS
# ======================================================================

def remove_markdown_heading(
    text: str,
) -> str:

    text = normalize_text(text)

    text = re.sub(
        r"^#{1,6}\s*",
        "",
        text,
    )

    return text.strip()


def normalize_heading(
    text: str,
) -> str:

    text = remove_markdown_heading(
        text
    )

    text = re.sub(
        r"^\d+\s*[、.．:：]\s*",
        "",
        text,
    )

    text = re.sub(
        r"^[一二三四五六七八九十百千万]+\s*[、.．:：]\s*",
        "",
        text,
    )

    return text.strip()


def canonical_text(
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

    return text.strip()


# ======================================================================
# EXAM SECTION DETECTION
# ======================================================================

def detect_exam_section(
    line: str,
) -> Optional[str]:

    text = canonical_text(line)

    if not text:
        return None

    # Listening
    if (
        text == "听力"
        or text.startswith("听力原文")
        or text.startswith("听力理解")
        or text.startswith("听力部分")
        or text.startswith("听力测试")
        or text.startswith("听力题目")
        or text.startswith("听力试题")
    ):
        return "listening"

    # Single choice
    if (
        text == "单项选择"
        or text.startswith("单项选择题")
        or text.startswith("单项选择")
    ):
        return "single_choice"

    # Multiple choice
    if (
        text == "多选题"
        or text == "多项选择"
        or text.startswith("多选题")
        or text.startswith("多项选择")
    ):
        return "multiple_choice"

    # Cloze
    if (
        text == "完形填空"
        or text.startswith("完形填空")
    ):
        return "cloze"

    # Reading
    if (
        text == "阅读理解"
        or text.startswith("阅读理解")
    ):
        return "reading"

    # Translation
    if (
        text == "翻译"
        or text.startswith("翻译题")
    ):
        return "translation"

    # Writing
    if (
        text == "写作"
        or text.startswith("写作题")
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


# ======================================================================
# QUESTION HELPERS
# ======================================================================

def parse_question_header(
    text: str,
) -> Optional[Tuple[int, str]]:

    text = normalize_text(
        text
    )

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

    pattern = re.compile(
        r"^\s*(?:-\s*)?([A-D])\s*[.．、:：]\s*(.*?)\s*$",
        re.IGNORECASE,
    )

    for line in lines:

        match = pattern.match(
            normalize_text(line)
        )

        if not match:
            continue

        options.append({
            "key": match.group(1).upper(),
            "text": normalize_text(
                match.group(2)
            ),
        })

    return options


def make_question_id(
    section: str,
    number: int,
    part: Optional[str] = None,
) -> str:

    if section == "listening":

        return (
            f"listening_{part or 'A'}_{number}"
        )

    if section == "translation":

        return (
            f"translation_{part or 'A'}_{number}"
        )

    return (
        f"{section}_{number}"
    )


def base_question(
    section: str,
    number: int,
    question: str,
    options: Optional[
        List[Dict[str, str]]
    ] = None,
    part: Optional[str] = None,
) -> Dict[str, Any]:

    question_id = make_question_id(
        section,
        number,
        part,
    )

    data: Dict[str, Any] = {
        # ----------------------------------------------------------
        # JSON contract
        #
        # Grader V1.0 expects:
        #   question_id
        #   type
        #   correct_answer
        #
        # Keep the original fields too for backward compatibility.
        # ----------------------------------------------------------
        "question_id": question_id,
        "type": section,

        # ----------------------------------------------------------
        # Original parser fields
        # ----------------------------------------------------------
        "id": question_id,
        "section": section,
        "number": number,
        "question": normalize_text(
            question
        ),
        "options": options or [],

        # ----------------------------------------------------------
        # Answer / explanation
        # ----------------------------------------------------------
        "correct_answer": None,
        "explanation": "",
        "reference_answer": None,

        # ----------------------------------------------------------
        # Grading state
        # ----------------------------------------------------------
        "graded": False,
        "review_required": False,
    }

    if part is not None:

        data["part"] = part

    return data

    if part is not None:
        data["part"] = part

    return data


# ======================================================================
# LISTENING QUESTION PARSER
# ======================================================================

def detect_listening_part(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    text = remove_markdown_heading(
        text
    )

    match = re.match(
        r"^Part\s+([ABC])"
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

    text = normalize_text(
        line
    )

    parsed = parse_question_header(
        text
    )

    if parsed:
        return parsed

    match = re.match(
        r"^(\d+)\s*[.．、)]\s*(.*?)\s*$",
        text,
    )

    if not match:
        return None

    return (
        int(match.group(1)),
        normalize_text(
            match.group(2)
        ),
    )


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

    def flush():

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

            flush()

            current_part = part

            continue

        parsed = parse_listening_question_line(
            clean
        )

        if parsed:

            flush()

            number, question = parsed

            current = base_question(
                section="listening",
                number=number,
                question=question,
                part=current_part or "A",
            )

            continue

        if current is not None:

            option_buffer.append(
                clean
            )

    flush()

    return questions


# ======================================================================
# CHOICE QUESTION PARSER
# ======================================================================

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

    def flush():

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

            flush()

            number, question = parsed

            current = base_question(
                section=section,
                number=number,
                question=question,
            )

            continue

        if current is not None:

            option_buffer.append(
                clean
            )

    flush()

    return questions


# ======================================================================
# CLOZE PARSER
# ======================================================================

def extract_cloze_numbers(
    text: str,
) -> List[int]:

    result: List[int] = []

    for match in re.finditer(
        r"\(\s*(\d+)\s*\)",
        text,
    ):

        number = int(
            match.group(1)
        )

        if number not in result:

            result.append(
                number
            )

    return result


def parse_inline_cloze_options(
    line: str,
) -> List[Dict[str, str]]:

    result: List[
        Dict[str, str]
    ] = []

    pattern = re.compile(
        r"([A-D])\s*[.．、:：]\s*"
        r"(.*?)(?=\s+[A-D]\s*[.．、:：]|$)",
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

    option_lines: List[str] = []

    in_options = False

    for line in lines:

        clean = normalize_text(
            line
        )

        if clean == "选择题":

            in_options = True

            continue

        if in_options:

            option_lines.append(
                clean
            )

        elif clean:

            passage_lines.append(
                clean
            )

    passage = "\n".join(
        passage_lines
    ).strip()

    numbers = extract_cloze_numbers(
        passage
    )

    if not numbers:

        numbers = list(
            range(1, 11)
        )

    option_map: Dict[
        int,
        List[Dict[str, str]]
    ] = {}

    current_number: Optional[int] = None

    current_lines: List[str] = []

    def flush():

        nonlocal current_number
        nonlocal current_lines

        if current_number is None:
            return

        parsed = parse_options(
            current_lines
        )

        if not parsed:

            parsed = parse_inline_cloze_options(
                " ".join(
                    current_lines
                )
            )

        option_map[
            current_number
        ] = parsed

        current_number = None
        current_lines = []

    for line in option_lines:

        match = re.match(
            r"^#{1,6}\s*(\d+)\s*[.．、)]\s*(.*)$",
            line,
        )

        if match:

            flush()

            current_number = int(
                match.group(1)
            )

            rest = normalize_text(
                match.group(2)
            )

            if rest:

                current_lines.append(
                    rest
                )

            continue

        if current_number is not None:

            current_lines.append(
                line
            )

    flush()

    questions: List[
        Dict[str, Any]
    ] = []

    for number in numbers:

        questions.append(
            base_question(
                section="cloze",
                number=number,
                question=passage,
                options=option_map.get(
                    number,
                    [],
                ),
            )
        )

    return questions


# ======================================================================
# TRANSLATION PARSER
# ======================================================================

def detect_translation_part(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    if re.search(
        r"\bPart\s+A\b",
        text,
        re.IGNORECASE,
    ):
        return "A"

    if re.search(
        r"\bPart\s+B\b",
        text,
        re.IGNORECASE,
    ):
        return "B"

    return None


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

    def flush():

        nonlocal current

        if current is not None:

            questions.append(
                current
            )

            current = None

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

            flush()

            number, question = parsed

            current = base_question(
                section="translation",
                number=number,
                question=question,
                part=current_part or "A",
            )

    flush()

    return questions


# ======================================================================
# WRITING PARSER
# ======================================================================

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

    body: List[str] = []

    def flush():

        nonlocal current
        nonlocal body

        if current is None:
            return

        if not current.get(
            "question"
        ):

            current["question"] = (
                " ".join(
                    body
                ).strip()
            )

        current["prompt"] = (
            current["question"]
        )

        questions.append(
            current
        )

        current = None
        body = []

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

            flush()

            number, question = parsed

            current = base_question(
                section="writing",
                number=number,
                question=question,
            )

            continue

        if current is not None:

            body.append(
                clean
            )

    flush()

    return questions


# ======================================================================
# EXAM PARSER
# ======================================================================

def recover_listening_section(
    exam_text: str,
) -> str:

    lines = normalize_text(
        exam_text
    ).splitlines()

    start: Optional[int] = None

    for index, line in enumerate(lines):

        if detect_exam_section(
            line
        ) == "listening":

            start = index

            break

    if start is None:
        return ""

    end = len(lines)

    for index in range(
        start + 1,
        len(lines),
    ):

        section = detect_exam_section(
            lines[index]
        )

        if section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
            "translation",
            "writing",
        }:

            end = index

            break

    return "\n".join(
        lines[start:end]
    ).strip()


def parse_exam(
    exam_text: str,
) -> List[Dict[str, Any]]:

    sections = split_sections(
        exam_text
    )

    questions: List[
        Dict[str, Any]
    ] = []

    # Listening
    listening_text = sections.get(
        "listening",
        "",
    )

    listening_questions = (
        parse_listening(
            listening_text
        )
        if listening_text
        else []
    )

    if len(listening_questions) < 15:

        recovered = (
            recover_listening_section(
                exam_text
            )
        )

        if recovered:

            recovered_questions = (
                parse_listening(
                    recovered
                )
            )

            if len(recovered_questions) > len(
                listening_questions
            ):

                listening_questions = (
                    recovered_questions
                )

    questions.extend(
        listening_questions
    )

    # Single choice
    if "single_choice" in sections:

        questions.extend(
            parse_choice_section(
                sections["single_choice"],
                "single_choice",
            )
        )

    # Multiple choice
    if "multiple_choice" in sections:

        questions.extend(
            parse_choice_section(
                sections["multiple_choice"],
                "multiple_choice",
            )
        )

    # Cloze
    if "cloze" in sections:

        questions.extend(
            parse_cloze(
                sections["cloze"]
            )
        )

    # Reading
    if "reading" in sections:

        questions.extend(
            parse_choice_section(
                sections["reading"],
                "reading",
            )
        )

    # Translation
    if "translation" in sections:

        questions.extend(
            parse_translation(
                sections["translation"]
            )
        )

    # Writing
    if "writing" in sections:

        questions.extend(
            parse_writing(
                sections["writing"]
            )
        )

    return questions


# ======================================================================
# ANSWER ROOT DETECTION
# ======================================================================

def normalize_answer_heading(
    line: str,
) -> str:

    text = normalize_text(
        line
    )

    text = re.sub(
        r"^#{1,6}\s*",
        "",
        text,
    )

    return text.strip()


def remove_heading_number(
    text: str,
) -> str:

    text = normalize_text(
        text
    )

    text = re.sub(
        r"^[一二三四五六七八九十百千万]+\s*[、.．:：]\s*",
        "",
        text,
    )

    text = re.sub(
        r"^\d+\s*[、.．:：]\s*",
        "",
        text,
    )

    return text.strip()


def canonical_answer_heading(
    line: str,
) -> str:

    text = normalize_answer_heading(
        line
    )

    text = remove_heading_number(
        text
    )

    text = re.sub(
        r"\s+",
        "",
        text,
    )

    return text


def is_standard_answer_heading(
    line: str,
) -> bool:

    text = canonical_answer_heading(
        line
    )

    if not text:
        return False

    exact = {
        "答案",
        "答案与解析",
        "标准答案",
        "标准答案与解析",
        "标准答案及解析",
        "参考答案",
        "参考答案与解析",
    }

    if text in exact:
        return True

    if text.startswith(
        "标准答案"
    ):
        return True

    if text.startswith(
        "参考答案"
    ):
        return True

    if text.startswith(
        "答案与解析"
    ):
        return True

    return False


# ======================================================================
# ANSWER SECTION DETECTION
# ======================================================================

def detect_answer_section(
    line: str,
) -> Optional[str]:

    text = canonical_answer_heading(
        line
    )

    if not text:
        return None

    # Part A/B/C are not answer sections.
    if re.fullmatch(
        r"Part[ABC]",
        text,
        re.IGNORECASE,
    ):
        return None

    # Listening
    if (
        text == "听力"
        or text.startswith("听力答案")
        or text.startswith("听力标准答案")
        or text.startswith("听力参考答案")
    ):
        return "listening"

    # Single choice
    if text.startswith(
        "单项选择"
    ):
        return "single_choice"

    # Multiple choice
    if (
        text.startswith("多选题")
        or text.startswith("多项选择")
    ):
        return "multiple_choice"

    # Cloze
    if text.startswith(
        "完形填空"
    ):
        return "cloze"

    # Reading
    if text.startswith(
        "阅读理解"
    ):
        return "reading"

    # Translation
    if text.startswith(
        "翻译"
    ):
        return "translation"

    # Writing
    if text.startswith(
        "写作"
    ):
        return "writing"

    return None


# ======================================================================
# CHOICE ANSWER EXTRACTION
# ======================================================================

def extract_choice_answer(
    line: str,
) -> Optional[str]:

    text = normalize_text(
        line
    )

    text = text.replace(
        "**",
        "",
    )

    # --------------------------------------------------------------
    # 1. B
    # 1、B
    # 1) B
    # --------------------------------------------------------------

    match = re.match(
        r"^\s*(\d+)\s*[.．、)]\s*"
        r"([A-D](?:\s*[,、，]\s*[A-D])*)"
        r"\s*$",
        text,
        re.IGNORECASE,
    )

    if match:

        return normalize_answer(
            match.group(2)
        )

    # --------------------------------------------------------------
    # 答案：B
    # --------------------------------------------------------------

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

    return None


# ======================================================================
# V1.6.1 LISTENING ANSWER PARSER
# ======================================================================

def parse_listening_answers_v161(
    answer_text: str,
) -> Dict[Tuple[str, int], str]:
    """
    Dedicated V1.6.1 listening answer parser.

    It does NOT depend on split_answer_blocks().

    It scans the complete answer file and uses this state machine:

        BEFORE_STANDARD
            |
            v
        STANDARD_ANSWER
            |
            v
        LISTENING
            |
            +--> PART A
            |
            +--> PART B
            |
            +--> PART C
            |
            v
        NEXT_SECTION -> STOP

    Expected result:

        ("A", 1) -> "B"
        ("A", 2) -> "C"
        ...
        ("C", 5) -> "D"
    """

    lines = normalize_text(
        answer_text
    ).splitlines()

    result: Dict[
        Tuple[str, int],
        str
    ] = {}

    in_standard_answer = False
    in_listening = False

    current_part: Optional[str] = None

    for raw_line in lines:

        line = normalize_text(
            raw_line
        )

        if not line:
            continue

        # ----------------------------------------------------------
        # STEP 1
        # Find root:
        #
        # ## 二、标准答案
        # ----------------------------------------------------------

        if not in_standard_answer:

            if is_standard_answer_heading(
                line
            ):

                in_standard_answer = True

            continue

        # ----------------------------------------------------------
        # STEP 2
        # Find:
        #
        # ### 听力
        # ----------------------------------------------------------

        if not in_listening:

            section = detect_answer_section(
                line
            )

            if section == "listening":

                in_listening = True
                current_part = None

                continue

            # Another section appearing before
            # listening means this answer file does
            # not contain listening in the expected
            # location.
            continue

        # ----------------------------------------------------------
        # STEP 3
        # Stop at next answer section.
        # ----------------------------------------------------------

        section = detect_answer_section(
            line
        )

        if section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
            "translation",
            "writing",
        }:

            break

        # ----------------------------------------------------------
        # STEP 4
        # Detect Part A/B/C.
        # ----------------------------------------------------------

        part = detect_listening_part(
            line
        )

        if part:

            current_part = part

            continue

        # ----------------------------------------------------------
        # STEP 5
        # Parse:
        #
        # 1. B
        # 2. C
        # ----------------------------------------------------------

        answer = extract_choice_answer(
            line
        )

        if answer is None:
            continue

        match = re.match(
            r"^\s*(\d+)\s*[.．、)]",
            line.replace(
                "**",
                "",
            ),
        )

        if not match:
            continue

        if current_part not in {
            "A",
            "B",
            "C",
        }:
            continue

        number = int(
            match.group(1)
        )

        if not 1 <= number <= 5:
            continue

        result[
            (
                current_part,
                number,
            )
        ] = normalize_answer(
            answer
        )

    return result


# ======================================================================
# LISTENING DIAGNOSTIC
# ======================================================================

def listening_answer_diagnostic(
    answers: Dict[
        Tuple[str, int],
        str
    ],
) -> Dict[str, int]:

    return {
        "A": sum(
            1
            for number in range(1, 6)
            if answers.get(
                ("A", number)
            )
        ),
        "B": sum(
            1
            for number in range(1, 6)
            if answers.get(
                ("B", number)
            )
        ),
        "C": sum(
            1
            for number in range(1, 6)
            if answers.get(
                ("C", number)
            )
        ),
    }


# ======================================================================
# ANSWER BLOCK SPLITTER
# ======================================================================

def split_answer_blocks(
    text: str,
) -> Dict[str, str]:

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

        if is_standard_answer_heading(
            clean
        ):

            in_standard_answer = True
            current = None

            continue

        if not in_standard_answer:
            continue

        section = detect_answer_section(
            clean
        )

        if section:

            current = section

            blocks.setdefault(
                current,
                [],
            )

            continue

        if current:

            blocks[current].append(
                clean
            )

    return {
        key: "\n".join(
            value
        ).strip()
        for key, value in blocks.items()
    }


# ======================================================================
# GENERAL ANSWER PARSERS
# ======================================================================

def collect_numbered_answers(
    text: str,
) -> Dict[int, str]:

    answers: Dict[
        int,
        str
    ] = {}

    for line in normalize_text(
        text
    ).splitlines():

        answer = extract_choice_answer(
            line
        )

        if answer is None:
            continue

        match = re.match(
            r"^\s*(\d+)\s*[.．、)]",
            line.replace(
                "**",
                "",
            ),
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        answers[number] = normalize_answer(
            answer
        )

    return answers


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

        if re.search(
            r"\bPart\s+A\b",
            clean,
            re.IGNORECASE,
        ):

            current_part = "A"
            continue

        if re.search(
            r"\bPart\s+B\b",
            clean,
            re.IGNORECASE,
        ):

            current_part = "B"
            continue

        match = re.match(
            r"^(\d+)\s*[.．、)]\s*(.*?)\s*$",
            clean.replace(
                "**",
                "",
            ),
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        value = normalize_text(
            match.group(2)
        )

        if (
            current_part in {
                "A",
                "B",
            }
            and value
        ):

            result[
                (
                    current_part,
                    number,
                )
            ] = value

    return result


def parse_writing_reference(
    text: str,
) -> Optional[str]:

    lines = normalize_text(
        text
    ).splitlines()

    collecting = False

    result: List[str] = []

    for line in lines:

        clean = normalize_text(
            line
        )

        if not clean:
            continue

        if "写作参考范文" in clean:

            collecting = True

            continue

        if not collecting:
            continue

        if (
            clean.startswith("#")
            and "写作参考范文"
            not in clean
        ):

            break

        result.append(
            clean.replace(
                "**",
                "",
            )
        )

    value = " ".join(
        result
    ).strip()

    return value or None


# ======================================================================
# EXPLANATIONS
# ======================================================================

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

    current_section: Optional[str] = None
    current_part: Optional[str] = None
    current_number: Optional[int] = None
    buffer: List[str] = []

    def flush():

        nonlocal current_number
        nonlocal buffer

        if (
            current_section
            and current_number is not None
            and buffer
        ):

            value = " ".join(
                x
                for x in buffer
                if x
            ).strip()

            if value:

                if current_section == "listening":

                    if current_part:

                        result[
                            (
                                f"listening_{current_part}",
                                current_number,
                            )
                        ] = value

                else:

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

        section = detect_answer_section(
            clean
        )

        if section:

            flush()

            current_section = section
            current_part = None

            continue

        if current_section == "listening":

            part = detect_listening_part(
                clean
            )

            if part:

                flush()

                current_part = part

                continue

        match = re.match(
            r"^(\d+)\s*[.．、)]\s*(.*)$",
            clean.replace(
                "**",
                "",
            ),
        )

        if match:

            flush()

            current_number = int(
                match.group(1)
            )

            rest = normalize_text(
                match.group(2)
            )

            if rest:

                buffer.append(
                    rest
                )

            continue

        if current_number is not None:

            buffer.append(
                clean
            )

    flush()

    return result


# ======================================================================
# REFERENCE ANSWERS
# ======================================================================

def parse_reference_answers(
    answer_text: str,
) -> Dict[str, Any]:

    result: Dict[str, Any] = {
        "choice": {},
        "listening": {},
        "translation": {},
        "writing": None,
        "explanations": {},
    }

    # ==============================================================
    # LISTENING
    #
    # V1.6.1:
    # DO NOT depend on split_answer_blocks().
    # ==============================================================
    listening_answers = (
        parse_listening_answers_v161(
            answer_text
        )
    )

    result["listening"] = (
        listening_answers
    )

    # ==============================================================
    # Other answer blocks
    # ==============================================================

    blocks = split_answer_blocks(
        answer_text
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

        if block:

            result["choice"][section] = (
                collect_numbered_answers(
                    block
                )
            )

    # ==============================================================
    # Translation
    # ==============================================================

    translation_block = blocks.get(
        "translation",
        "",
    )

    if translation_block:

        result["translation"] = (
            parse_translation_references(
                translation_block
            )
        )

    # ==============================================================
    # Writing
    # ==============================================================

    writing_block = blocks.get(
        "writing",
        "",
    )

    if writing_block:

        result["writing"] = (
            parse_writing_reference(
                writing_block
            )
        )

    # ==============================================================
    # Explanations
    # ==============================================================

    result["explanations"] = (
        parse_explanations(
            answer_text
        )
    )

    return result


# ======================================================================
# ATTACH ANSWERS
# ======================================================================

def attach_answers(
    questions: List[Dict[str, Any]],
    answer_data: Dict[str, Any],
) -> List[Dict[str, Any]]:

    choice_answers = answer_data.get(
        "choice",
        {}
    )

    listening_answers = answer_data.get(
        "listening",
        {}
    )

    translation_answers = answer_data.get(
        "translation",
        {}
    )

    writing_reference = answer_data.get(
        "writing"
    )

    explanations = answer_data.get(
        "explanations",
        {}
    )

    for question in questions:

        section = question.get(
            "section"
        )

        number = question.get(
            "number"
        )

        correct_answer = None

        reference_answer = None

        explanation = ""

        # ==========================================================
        # LISTENING
        # ==========================================================

        if section == "listening":

            part = (
                question.get(
                    "part"
                )
                or "A"
            )

            # ------------------------------------------------------
            # PRIMARY:
            #
            # ("A", 1)
            # ------------------------------------------------------

            correct_answer = (
                listening_answers.get(
                    (
                        part,
                        number,
                    )
                )
            )

            # ------------------------------------------------------
            # SECONDARY:
            #
            # Derive directly from ID.
            #
            # listening_A_1
            # ------------------------------------------------------

            if not correct_answer:

                question_id = (
                    question.get(
                        "id",
                        ""
                    )
                )

                match = re.match(
                    r"^listening_([ABC])_(\d+)$",
                    question_id,
                )

                if match:

                    id_part = (
                        match.group(1)
                    )

                    id_number = int(
                        match.group(2)
                    )

                    correct_answer = (
                        listening_answers.get(
                            (
                                id_part,
                                id_number,
                            )
                        )
                    )

            # ------------------------------------------------------
            # Explanation.
            # ------------------------------------------------------

            explanation = (
                explanations.get(
                    (
                        f"listening_{part}",
                        number,
                    ),
                    ""
                )
            )

            if not explanation:

                explanation = (
                    explanations.get(
                        (
                            "listening",
                            number,
                        ),
                        ""
                    )
                )

        # ==========================================================
        # OTHER AUTO-GRADED TYPES
        # ==========================================================

        elif section in {
            "single_choice",
            "multiple_choice",
            "cloze",
            "reading",
        }:

            section_answers = (
                choice_answers.get(
                    section,
                    {}
                )
            )

            correct_answer = (
                section_answers.get(
                    number
                )
            )

            explanation = (
                explanations.get(
                    (
                        section,
                        number,
                    ),
                    ""
                )
            )

        # ==========================================================
        # TRANSLATION
        # ==========================================================

        elif section == "translation":

            part = (
                question.get(
                    "part"
                )
                or "A"
            )

            reference_answer = (
                translation_answers.get(
                    (
                        part,
                        number,
                    )
                )
            )

            explanation = (
                explanations.get(
                    (
                        section,
                        number,
                    ),
                    ""
                )
            )

        # ==========================================================
        # WRITING
        # ==========================================================

        elif section == "writing":

            reference_answer = (
                writing_reference
            )

            explanation = (
                explanations.get(
                    (
                        section,
                        number,
                    ),
                    ""
                )
            )

        # ==========================================================
        # WRITE BACK
        # ==========================================================

        if correct_answer is not None:

            question[
                "correct_answer"
            ] = normalize_answer(
                correct_answer
            )

        else:

            question[
                "correct_answer"
            ] = None

        question[
            "reference_answer"
        ] = reference_answer

        question[
            "explanation"
        ] = explanation

        # ----------------------------------------------------------
        # Grading status
        # ----------------------------------------------------------

        if section in AUTO_GRADED_TYPES:

            question[
                "graded"
            ] = bool(
                question.get(
                    "correct_answer"
                )
            )

        elif section in MANUAL_REVIEW_TYPES:

            question[
                "graded"
            ] = False

            question[
                "review_required"
            ] = True

    return questions


# ======================================================================
# BUILD
# ======================================================================

def build_exam(
    exam_text: str,
    answer_text: Optional[str] = None,
) -> Dict[str, Any]:

    questions = parse_exam(
        exam_text
    )

    if answer_text:

        answer_data = (
            parse_reference_answers(
                answer_text
            )
        )

        questions = attach_answers(
            questions,
            answer_data
        )

    return {
        "version": PARSER_VERSION,
        "parser": (
            "748686 ENGLISH EXAM PARSER V1.6.1"
        ),
        "total_questions": len(
            questions
        ),
        "questions": questions,
    }


# ======================================================================
# VALIDATION
# ======================================================================

def validate_exam(
    exam: Dict[str, Any],
) -> List[str]:

    errors: List[str] = []

    questions = exam.get(
        "questions",
        []
    )

    if not questions:

        errors.append(
            "没有解析出任何题目"
        )

        return errors

    counts: Dict[str, int] = {}

    for question in questions:

        section = question.get(
            "section"
        )

        counts[section] = (
            counts.get(
                section,
                0
            )
            + 1
        )

    # --------------------------------------------------------------
    # Section counts
    # --------------------------------------------------------------

    for section, expected in (
        EXPECTED_COUNTS.items()
    ):

        actual = counts.get(
            section,
            0
        )

        if actual != expected:

            errors.append(
                f"{section}: "
                f"{actual}/{expected}"
            )

    # --------------------------------------------------------------
    # IDs
    # --------------------------------------------------------------

    ids = [
        q.get("id")
        for q in questions
    ]

    if len(ids) != len(set(ids)):

        errors.append(
            "题目 ID 不唯一"
        )

    # --------------------------------------------------------------
    # Content
    # --------------------------------------------------------------

    for question in questions:

        qid = question.get(
            "id",
            "<unknown>"
        )

        if not normalize_text(
            question.get(
                "question"
            )
        ):

            errors.append(
                f"{qid}: 缺少题目内容"
            )

        section = question.get(
            "section"
        )

        if section in {
            "single_choice",
            "multiple_choice",
            "reading",
        }:

            if len(
                question.get(
                    "options",
                    []
                )
            ) < 4:

                errors.append(
                    f"{qid}: 选项不足"
                )

    # --------------------------------------------------------------
    # Total
    # --------------------------------------------------------------

    if len(questions) != 61:

        errors.append(
            f"总题数错误: "
            f"{len(questions)}/61"
        )

    # --------------------------------------------------------------
    # Listening answers
    # --------------------------------------------------------------

    listening = [
        q
        for q in questions
        if q.get(
            "section"
        ) == "listening"
    ]

    listening_answer_count = sum(
        1
        for q in listening
        if normalize_answer(
            q.get(
                "correct_answer"
            )
        )
    )

    if listening_answer_count != 15:

        errors.append(
            "listening 标准答案绑定失败: "
            f"{listening_answer_count}/15"
        )

    return errors


# ======================================================================
# SUMMARY
# ======================================================================

def build_summary(
    exam: Dict[str, Any],
) -> Dict[str, Any]:

    questions = exam.get(
        "questions",
        []
    )

    counts: Dict[str, int] = {}

    auto_total = 0

    auto_answered = 0

    for question in questions:

        section = question.get(
            "section"
        )

        counts[section] = (
            counts.get(
                section,
                0
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

    return {
        "total": len(questions),
        "counts": counts,
        "auto_graded": auto_total,
        "auto_with_answers": auto_answered,
    }


# ======================================================================
# CLI
# ======================================================================

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "748686 English Exam Parser V1.6.1"
        )
    )

    parser.add_argument(
        "--exam",
        required=True,
        help="考试试卷 Markdown",
    )

    parser.add_argument(
        "--answers",
        required=False,
        default="",
        help="答案与解析 Markdown",
    )

    parser.add_argument(
        "--output",
        required=False,
        default="",
        help="输出 JSON",
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="执行验证",
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

    exam_text = (
        exam_path.read_text(
            encoding="utf-8"
        )
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

    print()
    print(
        "======================================================================"
    )
    print(
        "748686 ENGLISH EXAM PARSER V1.6.1"
    )
    print(
        "======================================================================"
    )

    print()
    print(
        "JSON version:"
    )
    print(
        " ",
        exam.get("version")
    )

    print()
    print(
        "总题数:"
    )
    print(
        " ",
        summary["total"]
    )

    print()
    print(
        "各 section 数量:"
    )

    for section in SECTION_ORDER:

        print(
            f"  {section}: "
            f"{summary['counts'].get(section, 0)}"
        )

    # --------------------------------------------------------------
    # Listening binding diagnostic
    # --------------------------------------------------------------

    questions = exam.get(
        "questions",
        []
    )

    listening = [
        q
        for q in questions
        if q.get(
            "section"
        ) == "listening"
    ]

    print()
    print(
        "======================================================================"
    )
    print(
        "LISTENING ANSWER BINDING"
    )
    print(
        "======================================================================"
    )

    part_counts = {
        "A": 0,
        "B": 0,
        "C": 0,
    }

    for question in listening:

        part = question.get(
            "part"
        )

        answer = normalize_answer(
            question.get(
                "correct_answer"
            )
        )

        if (
            part in part_counts
            and answer
        ):

            part_counts[part] += 1

    print()
    print(
        f"Part A: "
        f"{part_counts['A']}/5"
    )

    print(
        f"Part B: "
        f"{part_counts['B']}/5"
    )

    print(
        f"Part C: "
        f"{part_counts['C']}/5"
    )

    print(
        f"TOTAL : "
        f"{sum(part_counts.values())}/15"
    )

    if listening:

        print()

        for question in listening:

            print(
                f"  {question.get('id')}: "
                f"{question.get('correct_answer')}"
            )

    # --------------------------------------------------------------
    # Validation
    # --------------------------------------------------------------

    if args.validate:

        errors = validate_exam(
            exam
        )

        print()

        if errors:

            print(
                "======================================================================"
            )

            print(
                "❌ VALIDATION FAILED"
            )

            print(
                "======================================================================"
            )

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

        print()
        print(
            "======================================================================"
        )

        print(
            "✅ VALIDATION PASSED"
        )

        print(
            "======================================================================"
        )

    # --------------------------------------------------------------
    # Output
    # --------------------------------------------------------------

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
