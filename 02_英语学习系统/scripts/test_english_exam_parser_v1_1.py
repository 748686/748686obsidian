#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 ENGLISH EXAM PARSER V1.4

Purpose
-------
Parse the generated English exam and its answer/explanation file.

V1.4 is based on the real generated exam format:

### 1. Question text
- A. ...
- B. ...
- C. ...
- D. ...

Special structures:
- Listening Part A / B / C
- Single choice
- Multiple choice
- Cloze passage + separate numbered options
- Reading comprehension
- Translation Part A / B
- Writing

V1.4 fixes:
1. Support answer section alias "多项选择".
2. Correctly separate listening transcript Part A/B/C from
   the later standard-answer area.
3. Namespace translation Part A/B question IDs.
4. Support writing prompts placed on the line after "### 1.".

Important:
- This parser ONLY parses existing files.
- It does NOT modify exam generation.
- It does NOT modify answer generation.
- It does NOT perform semantic grading.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


PARSER_VERSION = "1.4"


# ----------------------------------------------------------------------
# Section definitions
# ----------------------------------------------------------------------

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
    "一、听力": "listening",
    "二、听力": "listening",
    "听力": "listening",

    "二、单项选择": "single_choice",
    "单项选择": "single_choice",

    "三、多选题": "multiple_choice",
    "多选题": "multiple_choice",
    "多项选择": "multiple_choice",

    "四、完形填空": "cloze",
    "完形填空": "cloze",

    "五、阅读理解": "reading",
    "阅读理解": "reading",

    "六、翻译": "translation",
    "翻译": "translation",

    "七、写作": "writing",
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

    # Common answer wrappers.
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

    # A,C
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
            sorted(
                set(letters)
            )
        )

    # AC -> A,C
    if re.fullmatch(
        r"[A-D]{2,}",
        text,
    ):
        return ",".join(
            sorted(
                set(text)
            )
        )

    # A
    match = re.fullmatch(
        r"[A-D]",
        text,
    )

    if match:
        return match.group(0)

    return text


def normalize_heading(text: str) -> str:
    text = normalize_text(text)

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


def parse_question_number(
    text: str,
) -> Optional[int]:
    """
    Extract question number ONLY when the beginning of the line is a
    Markdown question heading.

    Valid:
        ### 1. What...
        ### 10. What...
        ### 1、...
        ### 1．...

    Invalid:
        (1)
        **1.**
        1. A. ...
        - A. ...
    """

    text = normalize_text(text)

    if not re.match(
        r"^#{1,6}\s+",
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
    """
    Parse a question heading.

    Example:
        ### 1. What does sleep help our body do?

    returns:
        (1, "What does sleep help our body do?")
    """

    text = normalize_text(text)

    if not re.match(
        r"^#{1,6}\s+",
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
    """
    Parse:
        - A. Grow
        - B. Run

    Also supports:
        A. Grow
        B. Run

    Does not treat inline cloze options such as:
        ### 1. A. happy B. sad C. tired D. angry
    as normal question options here.
    """

    options: List[Dict[str, str]] = []

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
    """
    Build a unique question ID.

    Listening:
        listening_A_1
        listening_B_1
        listening_C_1

    Translation:
        translation_A_1
        translation_B_1

    Other sections:
        single_choice_1
        multiple_choice_1
        ...
    """

    if section == "listening":
        part = listening_part or "A"

        return (
            f"listening_{part}_{number}"
        )

    # V1.4 FIX:
    # Translation Part A / B both restart numbering at 1,
    # so the part MUST be included in the ID.
    if section == "translation":
        part = listening_part or "A"

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
    text = normalize_heading(line)

    # Exact known section names.
    for title, section in SECTION_MAP.items():
        if text == title:
            return section

    # Fallback by content.
    for title, section in SECTION_MAP.items():
        clean_title = re.sub(
            r"^[一二三四五六七八九十]+[、.．]\s*",
            "",
            title,
        )

        clean_line = re.sub(
            r"^[一二三四五六七八九十]+[、.．]\s*",
            "",
            text,
        )

        if clean_line == clean_title:
            return section

    return None


def split_sections(
    text: str,
) -> Dict[str, str]:
    """
    Split exam into the seven top-level sections.

    Only headings beginning with # are considered section boundaries.
    """

    lines = normalize_text(
        text
    ).splitlines()

    sections: Dict[str, List[str]] = {}

    current: Optional[str] = None

    for line in lines:
        detected = detect_exam_section(line)

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
    """
    Parse standard numbered choice questions.

    Example:

    ### 1. What does...
    - A. ...
    - B. ...
    - C. ...
    - D. ...

    The question text comes directly from the heading.
    """

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
        clean = normalize_text(line)

        if not clean:
            continue

        parsed = parse_question_header(
            clean
        )

        if parsed:
            # Flush previous.
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
# Listening
# ----------------------------------------------------------------------

def detect_listening_part(
    line: str,
) -> Optional[str]:
    text = normalize_text(line)

    match = re.match(
        r"^#{1,6}\s*Part\s+([ABC])\b",
        text,
        re.IGNORECASE,
    )

    if match:
        return match.group(1).upper()

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

    for line in lines:
        clean = normalize_text(line)

        if not clean:
            continue

        part = detect_listening_part(
            clean
        )

        if part:
            if current is not None:
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

            current_part = part

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
# Cloze
# ----------------------------------------------------------------------

def extract_cloze_blank_numbers(
    text: str,
) -> List[int]:
    """
    Extract:
        ____ (1) ____
        ____ (10) ____

    from the cloze passage.
    """

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
    """
    Parse a cloze heading such as:

    ### 1. A. happy B. sad C. tired D. angry

    Returns four options.
    """

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
    """
    Parse the special cloze structure.

    Passage:
        Hello... ____ (1) ____ ...

    Then:

        ### 1. A. happy B. sad C. tired D. angry

        - A. happy
        - B. sad
        - C. tired
        - D. angry
    """

    lines = normalize_text(
        text
    ).splitlines()

    passage_lines: List[str] = []

    # First collect the passage until "选择题".
    in_options = False

    option_section_lines: List[str] = []

    for line in lines:
        clean = normalize_text(line)

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

    # Fallback if the passage extraction somehow missed numbers.
    if not blank_numbers:
        blank_numbers = list(
            range(1, 11)
        )

    # Parse the question headings in the option section.
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

        # Cloze question heading can be:
        # ### 1. A. happy B. sad C. tired D. angry
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

    # The question itself is the sentence containing the corresponding blank.
    questions: List[
        Dict[str, Any]
    ] = []

    for number in blank_numbers:
        question_text = passage

        # Replace the whole blank marker with an explicit placeholder
        # while retaining the original passage.
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
    text = normalize_text(line)

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
    text = normalize_text(line)

    return (
        text.startswith("翻译：")
        or text.startswith("翻译:")
    )


def clean_translation_prompt(
    line: str,
) -> str:
    text = normalize_text(line)

    text = re.sub(
        r"^翻译\s*[:：]\s*",
        "",
        text,
    )

    return text.strip()


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
        clean = normalize_text(line)

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

            # V1.4 FIX:
            # Translation Part A and Part B both restart numbering.
            # Pass current_part into base_question so IDs become:
            # translation_A_1 ... translation_A_5
            # translation_B_1 ... translation_B_5
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

        # Do not use the blank answer field as the question.
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
    """
    Parse writing questions.

    Supports both:

        ### 1. Write a short paragraph...

    and the actual generated format:

        ### 1.

        Write a short paragraph...

        作文：

        ______

    V1.4 FIX:
    When the heading itself contains no prompt text, collect the
    following body lines and use the first meaningful lines before
    "作文：" / answer blanks as the question content.
    """

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

        # V1.4 FIX:
        # If "### 1." has an empty prompt, recover the prompt from
        # the following lines.
        if not question_text:
            prompt_lines: List[str] = []

            for raw in body_lines:
                clean = normalize_text(
                    raw
                )

                if not clean:
                    continue

                # The actual answer area starts here.
                if re.match(
                    r"^作文\s*[:：]",
                    clean,
                ):
                    break

                # Ignore pure answer lines.
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
        clean = normalize_text(line)

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
    text: str,
) -> List[Dict[str, Any]]:
    sections = split_sections(
        text
    )

    questions: List[
        Dict[str, Any]
    ] = []

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
    text = normalize_text(line)

    text = re.sub(
        r"^[>\-\*\s]+",
        "",
        text,
    )

    return text.strip()


def extract_choice_answer(
    line: str,
) -> Optional[str]:
    """
    Supports:
        答案：A
        答案: A
        1. A
        1、A
        1. A,C
        1. A、C
        **1.** A
    """

    text = clean_answer_line(
        line
    )

    # Remove Markdown bold around number.
    text = text.replace(
        "**",
        "",
    )

    # Explicit answer marker.
    match = re.search(
        r"答案\s*[:：]\s*([A-D](?:\s*[,、，]\s*[A-D])*)",
        text,
        re.IGNORECASE,
    )

    if match:
        return normalize_answer(
            match.group(1)
        )

    # Numbered answer.
    match = re.match(
        r"^(\d+)\s*[.．、)]\s*([A-D](?:\s*[,、，]\s*[A-D])?)\s*$",
        text,
        re.IGNORECASE,
    )

    if match:
        return normalize_answer(
            match.group(2)
        )

    # **1.** A
    match = re.match(
        r"^\*{0,2}\s*(\d+)\s*[.．、)]\s*\*{0,2}\s*([A-D](?:\s*[,、，]\s*[A-D])?)\s*$",
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
    text = normalize_text(line)

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


def detect_answer_section(
    line: str,
) -> Optional[str]:
    text = normalize_heading(
        line
    )

    for title, section in ANSWER_SECTION_ALIASES.items():
        if text == title:
            return section

    # More flexible matching.
    for title, section in ANSWER_SECTION_ALIASES.items():
        if text.startswith(title):
            return section

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
    answers: Dict[int, str] = {}

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


def split_answer_blocks(
    text: str,
) -> Dict[str, str]:
    """
    Split answer file by major answer sections.

    This is intentionally tolerant because answer files may contain
    headings such as:
        一、听力答案
        Part A
        二、单项选择答案
        多项选择答案
    """

    lines = normalize_text(
        text
    ).splitlines()

    blocks: Dict[
        str,
        List[str]
    ] = {}

    current: Optional[str] = None

    for line in lines:
        detected = detect_answer_section(
            line
        )

        if detected:
            current = detected

            blocks.setdefault(
                current,
                [],
            )

            continue

        if current:
            blocks[current].append(
                line
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
    """
    Detect the transition from listening transcript to actual answers.

    Examples:
        标准答案
        参考答案
        答案
        答案与解析
        标准答案：
    """

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


def parse_listening_answers(
    text: str,
) -> Dict[Tuple[str, int], str]:
    """
    Parse Listening A/B/C.

    The real generated answer file can contain:

        Part A
        [listening transcript...]

        Part B
        [listening transcript...]

        Part C
        [listening transcript...]

        标准答案

        1. A
        2. B
        ...
        15. C

    The Part A/B/C headings appearing BEFORE the standard-answer
    boundary belong to the transcript and must NOT control answer
    assignment.

    V1.4 therefore:

    1. Wait for an explicit answer boundary.
    2. Reset current_part at that boundary.
    3. Collect numbered answers after the boundary.
    4. If no explicit Part headings occur after the boundary,
       map 1-5 -> A, 6-10 -> B, 11-15 -> C.
    5. If Part headings DO occur after the boundary, use them.
    """

    lines = normalize_text(
        text
    ).splitlines()

    result: Dict[
        Tuple[str, int],
        str
    ] = {}

    current_part: Optional[str] = None

    collecting_answers = False

    all_answers: List[str] = []

    explicit_part_answers = False

    for line in lines:
        clean = normalize_text(
            line
        )

        if not clean:
            continue

        # --------------------------------------------------------------
        # Enter actual standard-answer area.
        # --------------------------------------------------------------

        if is_listening_answer_boundary(
            clean
        ):
            collecting_answers = True

            # Critical:
            # Do NOT carry transcript Part C into the answer area.
            current_part = None

            continue

        # Ignore all transcript content before the answer boundary.
        if not collecting_answers:
            continue

        # --------------------------------------------------------------
        # Part headings AFTER answer boundary are valid.
        # --------------------------------------------------------------

        part = detect_answer_part(
            clean
        )

        if part:
            current_part = part
            explicit_part_answers = True
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

        # Only numbered answer lines.
        match = re.match(
            r"^(\d+)\s*[.．、)]",
            text_clean,
        )

        if not match:
            continue

        number = int(
            match.group(1)
        )

        if current_part:
            result[
                (
                    current_part,
                    number,
                )
            ] = answer

        else:
            all_answers.append(
                answer
            )

    # --------------------------------------------------------------
    # If there were no Part headings after the answer boundary,
    # the generated 15 answers are treated as a flat list.
    # --------------------------------------------------------------

    if (
        all_answers
        and not explicit_part_answers
    ):
        for index, answer in enumerate(
            all_answers[:15]
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

    # --------------------------------------------------------------
    # Additional compatibility fallback:
    #
    # If no explicit answer boundary exists in an older answer file,
    # preserve the original V1.3 Part-based behavior.
    # --------------------------------------------------------------

    if (
        not collecting_answers
        and not result
    ):
        current_part = None

        fallback_answers: List[
            Tuple[
                Optional[str],
                int,
                str,
            ]
        ] = []

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

            fallback_answers.append(
                (
                    current_part,
                    number,
                    answer,
                )
            )

        for part, number, answer in (
            fallback_answers
        ):
            if part:
                result[
                    (
                        part,
                        number,
                    )
                ] = answer

        # If still no Part mapping, use flat 1-15 mapping.
        if not result:
            flat = [
                item[2]
                for item in fallback_answers
            ]

            for index, answer in enumerate(
                flat[:15]
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
    """
    Supports:
        **1.** It is very important...
        1. It is...
        1、It is...
    """

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

    # Fallback: if no Part headings were detected,
    # assign first five references to A and next five to B.
    if not result:
        refs: List[str] = []

        for line in lines:
            parsed = extract_reference_after_number(
                line
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

        # Stop at a new obvious section heading.
        if re.match(
            r"^#{1,6}\s+",
            clean,
        ):
            if (
                "写作参考范文"
                not in heading
            ):
                break

        # Ignore numbered labels such as **1.**
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
    """
    Best-effort extraction of explanations.

    We intentionally keep this tolerant because explanation files may
    vary in Markdown formatting.
    """

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

        detected = detect_answer_section(
            clean
        )

        if detected:
            flush()

            current_section = detected

            continue

        # Part headings within listening.
        if current_section == "listening":
            part = detect_answer_part(
                clean
            )

            if part:
                # We represent listening explanations by section plus
                # global question number later if needed.
                continue

        # Numbered explanation.
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

    # --------------------------------------------------------------
    # Listening
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # Standard choice sections
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # Translation
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # Writing
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # Explanations
    # --------------------------------------------------------------

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

    # Listening fallback numbering.
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

            # Fallback in case answer parser receives a flat
            # 1-15 representation.
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

        # Explanation lookup.
        explanation = explanations.get(
            (
                section,
                number,
            ),
            "",
        )

        # Listening explanations sometimes use global numbering.
        if (
            section == "listening"
            and not explanation
        ):
            global_number = (
                listening_global_index
            )

            explanation = (
                explanations.get(
                    (
                        "listening",
                        global_number,
                    ),
                    "",
                )
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
            "748686 ENGLISH EXAM PARSER V1.4"
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

    # --------------------------------------------------------------
    # Count by type
    # --------------------------------------------------------------

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
            0,
        )

        if actual != expected:
            errors.append(
                f"{section}: 数量 {actual}, "
                f"预期 {expected}"
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

        # Choice types require four options.
        if section in {
            "listening",
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

        # Auto graded types require answer.
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

    # --------------------------------------------------------------
    # Final count
    # --------------------------------------------------------------

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
            "748686 English Exam Parser V1.4"
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
        "748686 ENGLISH EXAM PARSER V1.4"
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
