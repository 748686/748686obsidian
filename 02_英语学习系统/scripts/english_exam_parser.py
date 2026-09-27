#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 English Learning System
English Exam Parser V1.1

职责：
1. 解析实际试卷 Markdown
2. 解析答案与解析 Markdown
3. 建立稳定 question_id
4. 保留题目、选项、题型、正确答案、参考答案、解析
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

V1.1 重点修复：
- 支持 **1. / **1. / 1、 等题号格式
- 听力 A/B/C 独立映射
- 选择题答案精确映射
- 翻译参考答案提取
- 写作参考范文提取
- question_id 稳定化
- 答案不再依赖“向后扫描若干行”
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


ANSWER_SECTION_ALIASES = {
    "听力": "listening",
    "单项选择": "single_choice",
    "多选题": "multiple_choice",
    "完形填空": "cloze",
    "阅读理解": "reading",
    "翻译": "translation",
    "写作": "writing",
}


def normalize_text(text: str) -> str:
    return (
        text.replace("\r\n", "\n")
        .replace("\r", "\n")
        .strip()
    )


def normalize_answer(value: str | None) -> str:
    """
    统一选择题答案。

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

    # AC / CA
    if re.fullmatch(r"[A-Z]+", value):
        letters = sorted(set(value))
        return ",".join(letters)

    letters = re.findall(r"[A-Z]", value)

    if not letters:
        return value

    return ",".join(sorted(set(letters)))


def clean_markdown_number_prefix(line: str) -> str:
    """
    去除：
    1.
    1、
    1)
    **1.**
    ### 1.
    **第5题**
    """

    line = line.strip()

    line = re.sub(r"^#+\s*", "", line)
    line = re.sub(r"^\*\*\s*", "", line)
    line = re.sub(r"\s*\*\*$", "", line)

    line = re.sub(
        r"^\s*(?:第\s*)?\d+\s*[.、．)]\s*",
        "",
        line,
    )

    return line.strip()


def parse_question_number(line: str) -> int | None:
    """
    支持：

    ### 1.
    ### 1、
    ### 1)
    1.
    **1.**
    **第5题**
    """

    cleaned = line.strip()

    cleaned = re.sub(r"^#+\s*", "", cleaned)
    cleaned = re.sub(r"^\*\*\s*", "", cleaned)
    cleaned = re.sub(r"\s*\*\*$", "", cleaned)

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
    根据试卷一级标题切分。
    """

    lines = markdown.splitlines()

    sections: dict[str, list[str]] = {}
    current: str | None = None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# "):
            heading = stripped[2:].strip()

            if heading in SECTION_MAP:
                current = SECTION_MAP[heading]
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

            if re.match(
                r"^\s*-\s*[A-Z][.、．)]\s*",
                line,
            ):
                option_lines.append(line)

            elif line.strip():
                question_lines.append(line.strip())

            i += 1

        question_text = "\n".join(
            question_lines
        ).strip()

        # 删除作答提示
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
                    f"{section.upper()}_{number:02d}"
                ),
                "section": section,
                "number": number,
                "type": question_type,
                "question": question_text,
                "options": parse_options(option_lines),
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            }
        )

    return questions


def parse_listening(text: str) -> list[dict[str, Any]]:
    """
    听力：

    Part A -> 1~5
    Part B -> 1~5
    Part C -> 1~5

    question_id：

    LISTENING_A_01
    LISTENING_A_02
    ...
    LISTENING_C_05
    """

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part: str | None = None

    i = 0

    while i < len(lines):

        part_match = re.match(
            r"^\s*##\s*Part\s+([ABC])\s*$",
            lines[i],
            re.IGNORECASE,
        )

        if part_match:
            current_part = (
                part_match.group(1).upper()
            )
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


def parse_translation(
    text: str,
) -> list[dict[str, Any]]:

    lines = text.splitlines()

    questions: list[dict[str, Any]] = []

    current_part: str | None = None

    i = 0

    while i < len(lines):

        part_match = re.match(
            r"^\s*##\s*Part\s+([AB])\s+(.+)$",
            lines[i],
            re.IGNORECASE,
        )

        if part_match:
            current_part = (
                part_match.group(1).upper()
            )
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


def parse_writing(
    text: str,
) -> list[dict[str, Any]]:

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


def parse_exam(
    markdown: str,
) -> list[dict[str, Any]]:

    markdown = normalize_text(markdown)

    sections = split_sections(markdown)

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
# 答案文件解析
# ============================================================


def clean_answer_line(line: str) -> str:
    """
    清理答案行：

    **1. A**
    1. A
    **1.**
    **第5题**
    """

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


def is_section_heading(
    line: str,
) -> tuple[str | None, str | None]:

    heading = re.sub(
        r"^#+\s*",
        "",
        line.strip(),
    )

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


def parse_answer_choice_blocks(
    markdown: str,
) -> dict[tuple[str, str | None, int], str]:
    """
    专门解析标准答案中的选择题。

    不采用旧版“向后扫描”的方法。

    对普通选择题：

    单项选择
    1. B
    2. C

    多选题
    1. A,C

    对听力：

    Part A
    1. A
    ...
    5. B

    Part B
    ...

    Part C
    ...
    """

    lines = markdown.splitlines()

    result: dict[
        tuple[str, str | None, int],
        str,
    ] = {}

    current_section: str | None = None
    current_part: str | None = None

    in_standard_answer = False
    listening_part_index = 0

    listening_parts = ["A", "B", "C"]

    i = 0

    while i < len(lines):

        raw = lines[i]
        line = raw.strip()

        # 标准答案区域
        if (
            line.startswith("#")
            and "标准答案" in line
        ):
            in_standard_answer = True
            i += 1
            continue

        if not in_standard_answer:
            i += 1
            continue

        section, part = is_section_heading(line)

        if section:
            current_section = section

            if section == "listening":
                current_part = None
                listening_part_index = 0
            else:
                current_part = part

            i += 1
            continue

        # 听力可能没有明确 Part 标题，
        # 但连续出现三个 1~5 答案块。
        if (
            current_section == "listening"
            and current_part is None
        ):
            # 尝试从当前连续答案块开始。
            if (
                extract_choice_answer(line)
                and re.match(
                    r"^\**1[.、．)]?",
                    line,
                )
            ):
                if (
                    listening_part_index
                    < len(listening_parts)
                ):
                    current_part = (
                        listening_parts[
                            listening_part_index
                        ]
                    )

        answer = extract_choice_answer(line)

        if answer and current_section:

            number_match = re.match(
                r"^\**\s*(\d+)"
                r"\s*[.、．)]?",
                line,
            )

            if number_match:

                number = int(
                    number_match.group(1)
                )

                result[
                    (
                        current_section,
                        current_part,
                        number,
                    )
                ] = answer

                # 听力一个 1~5 块完成后，
                # 下一次 1 自动进入下一 Part。
                if (
                    current_section
                    == "listening"
                    and number == 5
                ):
                    listening_part_index += 1
                    current_part = None

        i += 1

    return result


def extract_reference_after_number(
    lines: list[str],
    start_index: int,
) -> str:

    """
    从编号后提取参考答案。

    支持：

    **1.** xxx

    1. xxx

    也允许答案跨多行。
    """

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

    """
    专门解析翻译参考答案。

    支持：

    ### 翻译 A：中译英

    **1.** It is very important...

    **2.** First, we need...

    ### 翻译 B：英译汉

    **1.** 睡眠有助于...
    """

    lines = markdown.splitlines()

    result: dict[str, dict[str, str]] = {}

    current_part: str | None = None

    in_translation = False

    for i, raw in enumerate(lines):

        line = raw.strip()

        heading = re.sub(
            r"^#+\s*",
            "",
            line,
        )

        translation_match = re.match(
            r"翻译\s*([AB])",
            heading,
            re.IGNORECASE,
        )

        if translation_match:
            in_translation = True
            current_part = (
                translation_match.group(1)
                .upper()
            )
            continue

        if not in_translation:
            continue

        # 进入其他大章节后停止
        if (
            line.startswith("#")
            and "翻译" not in heading
            and "标准答案" not in heading
        ):
            current_part = None
            in_translation = False
            continue

        if current_part is None:
            continue

        number = parse_question_number(line)

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


def parse_writing_reference(
    markdown: str,
) -> dict[str, dict[str, str]]:

    """
    专门提取写作参考范文。

    真实答案文件存在：

    ### 写作参考范文

    **5.**

    Dear friend, ...

    因此不依赖试卷题号必须为 5。
    """

    lines = markdown.splitlines()

    result: dict[str, dict[str, str]] = {}

    in_reference = False

    collected: list[str] = []

    for raw in lines:

        line = raw.strip()

        heading = re.sub(
            r"^#+\s*",
            "",
            line,
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

        # 跳过参考范文的题号
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

        collected.append(cleaned)

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


def parse_explanations(
    markdown: str,
) -> dict[str, str]:

    """
    尝试提取：

    解析：xxx

    绑定到当前题目。
    """

    lines = markdown.splitlines()

    result: dict[str, str] = {}

    current_section: str | None = None
    current_part: str | None = None
    current_number: int | None = None

    for raw in lines:

        line = raw.strip()

        section, part = is_section_heading(line)

        if section:
            current_section = section
            current_part = part
            current_number = None
            continue

        number = parse_question_number(line)

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
                key = (
                    f"LISTENING_"
                    f"{current_part}_"
                    f"{current_number:02d}"
                )

            elif current_section == "translation":
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


def parse_reference_answers(
    markdown: str,
) -> dict[str, dict[str, Any]]:

    result: dict[str, dict[str, Any]] = {}

    choice_answers = parse_answer_choice_blocks(
        markdown
    )

    translation_answers = (
        parse_translation_references(
            markdown
        )
    )

    writing_answers = (
        parse_writing_reference(
            markdown
        )
    )

    explanations = parse_explanations(
        markdown
    )

    # 选择题
    for (
        section,
        part,
        number,
    ), answer in choice_answers.items():

        if section == "listening":
            key = (
                f"LISTENING_"
                f"{part}_"
                f"{number:02d}"
            )
        else:
            key = (
                f"{section.upper()}_"
                f"{number:02d}"
            )

        result[key] = {
            "correct_answer": answer,
            "reference_answer": "",
            "explanation": "",
        }

    # 翻译
    for key, info in translation_answers.items():

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
        ] = info["reference_answer"]

    # 写作
    for key, info in writing_answers.items():

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
        ] = info["reference_answer"]

    # 解析
    for key, explanation in explanations.items():

        result.setdefault(
            key,
            {
                "correct_answer": "",
                "reference_answer": "",
                "explanation": "",
            },
        )

        result[key]["explanation"] = explanation

    return result


def attach_answers(
    questions: list[dict[str, Any]],
    answer_markdown: str,
) -> list[dict[str, Any]]:

    answer_data = parse_reference_answers(
        answer_markdown
    )

    for question in questions:

        qid = question["question_id"]

        info = answer_data.get(qid)

        if not info:
            continue

        question["correct_answer"] = (
            info.get(
                "correct_answer",
                "",
            )
        )

        question["reference_answer"] = (
            info.get(
                "reference_answer",
                "",
            )
        )

        question["explanation"] = (
            info.get(
                "explanation",
                "",
            )
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

    questions = parse_exam(
        exam_text
    )

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
        "version": "1.1",
        "exam_file": str(exam_path),
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

        qid = q.get("question_id")

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
        "748686 ENGLISH EXAM PARSER V1.1"
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

    counts: dict[str, int] = {}

    for q in exam["questions"]:

        key = q["type"]

        counts[key] = (
            counts.get(key, 0) + 1
        )

    print()

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
