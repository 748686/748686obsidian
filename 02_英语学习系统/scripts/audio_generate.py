#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.3.0
======================================================================

职责
======================================================================

只负责：

    1. 读取已经存在的试卷 Markdown
    2. 读取已经存在的答案与解析 Markdown
    3. 从答案与解析中的「听力原文」恢复 Part A / B / C 原文
    4. 从试卷中的 Part A / B / C 恢复题目与选项
    5. 将「原文 + 对应题目 + 对应选项」组成完整听力
    6. 自动判断 Part B 是否是真正的 M/F 对话
    7. 使用本地 Kokoro ONNX 模型生成音频
    8. 输出：

           Listening_A.mp3
           Listening_B.mp3
           Listening_C.mp3
           Listening_总音频.mp3

严格禁止：

    ✗ 不调用 AI
    ✗ 不修改试卷
    ✗ 不修改答案与解析
    ✗ 不重新生成试卷
    ✗ 不重新生成答案

======================================================================
V2.3.0 核心修复
======================================================================

1. 答案与解析是 Listening Original 的唯一来源。

   Part A / Part B：

       答案与解析
           ↓
       听力原文
           ↓
       对应编号原文
           ↓
       对应试卷题目
           ↓
       对应 A/B/C/D 选项

   Part C：

       答案与解析
           ↓
       听力原文
           ↓
       Passage
           ↓
       试卷 5 道题
           ↓
       每题 4 个选项

2. Part B 不再要求必须存在 M/F 对话。

   以下情况都合法：

       M: Hello...
       M: Exercise is...
       M: Children need...

   如果只有一个 speaker：

       判定为非对话

       第一遍：女声
       第二遍：男声

3. 真正的 M/F 对话：

       第一遍：
           M → 男声
           F → 女声

       第二遍：
           M → 女声
           F → 男声

4. Part A / Part B：

       第一遍：
           原文
           题目
           选项
           原文
           题目
           选项
           ...

       第二遍：
           原文
           题目
           选项
           原文
           题目
           选项
           ...

5. Part C：

       第一遍：
           原文
           Q1 + 选项
           Q2 + 选项
           ...
           Q5 + 选项

       第二遍：
           原文
           Q1 + 选项
           ...
           Q5 + 选项

6. 中文选项：

       如果选项包含中文，
       不再丢弃。

       自动选择本地中文 Kokoro voice。

       例如：

           B. 强壮的

       会实际读出：

           强壮的

7. Part C 逻辑片段保持：

       1 passage
       + 5 questions
       + 20 options
       = 26 logical segments

======================================================================
Kokoro
======================================================================

默认英语 Voice：

       female = af_maple
       male   = bf_vale

中文 voice：

       从本地 voices 中自动检测：

           zf_*
           zm_*

       优先选择：

           zf_xiaobei
           zf_xiaoni
           zf_xiaoxiao
           zm_yunjian
           zm_yunxi
           zm_yunyang
           zm_yunxia

       如果具体 voice 不存在，
       自动使用本地检测到的第一个中文 voice。

======================================================================
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


# ======================================================================
# 数据结构
# ======================================================================

@dataclass
class Segment:
    text: str
    voice: str
    repeat: int = 1


@dataclass
class Question:
    number: int
    question: str
    options: List[str]


@dataclass
class SourceBlock:
    number: int
    lines: List[str]


@dataclass
class SpeakerLine:
    speaker: str
    text: str


# ======================================================================
# 基础工具
# ======================================================================

def clean_line(line: str) -> str:
    line = line.strip()

    if not line:
        return ""

    line = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        line,
    )

    line = re.sub(
        r"^\s*[-*+]\s+",
        "",
        line,
    )

    line = re.sub(
        r"^\*\*(.*?)\*\*$",
        r"\1",
        line,
    )

    line = re.sub(
        r"^\*(.*?)\*$",
        r"\1",
        line,
    )

    return line.strip()


def normalize_space(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text,
    ).strip()


def is_top_level_heading(line: str) -> bool:
    return bool(
        re.match(
            r"^\s*#\s+.+",
            line,
        )
    )


# ======================================================================
# Part Header
# ======================================================================

def is_part_header(
    line: str,
    part: str,
) -> bool:

    cleaned = clean_line(line)
    cleaned_upper = cleaned.upper()
    part = part.upper()

    english_patterns = [
        rf"^PART\s+{part}\s*$",
        rf"^LISTENING\s+{part}\s*$",
        rf"^LISTENING\s+PART\s+{part}\s*$",
    ]

    for pattern in english_patterns:

        if re.match(
            pattern,
            cleaned_upper,
        ):
            return True

    chinese_patterns = {
        "A": [
            r"^第一部分\s*$",
            r"^听力\s*A\s*$",
            r"^听力第一部分\s*$",
            r"^听句子\s*$",
        ],
        "B": [
            r"^第二部分\s*$",
            r"^听力\s*B\s*$",
            r"^听力第二部分\s*$",
            r"^听力第二部分\s*$",
            r"^听对话\s*$",
        ],
        "C": [
            r"^第三部分\s*$",
            r"^听力\s*C\s*$",
            r"^听力第三部分\s*$",
            r"^听原文\s*$",
        ],
    }

    for pattern in chinese_patterns.get(
        part,
        [],
    ):

        if re.match(
            pattern,
            cleaned,
        ):
            return True

    return False


def find_part_start(
    lines: List[str],
    part: str,
) -> Optional[int]:

    for i, line in enumerate(lines):

        if is_part_header(
            line,
            part,
        ):
            return i

    return None


def extract_part(
    text: str,
    part: str,
) -> str:

    lines = text.splitlines()

    start = find_part_start(
        lines,
        part,
    )

    if start is None:
        return ""

    end = len(lines)

    for i in range(
        start + 1,
        len(lines),
    ):

        if (
            is_part_header(lines[i], "A")
            and part.upper() != "A"
        ):
            end = i
            break

        if (
            is_part_header(lines[i], "B")
            and part.upper() != "B"
        ):
            end = i
            break

        if (
            is_part_header(lines[i], "C")
            and part.upper() != "C"
        ):
            end = i
            break

        if (
            i > start + 1
            and is_top_level_heading(lines[i])
        ):
            end = i
            break

    return "\n".join(
        lines[start + 1:end]
    ).strip()


# ======================================================================
# Question Header
# ======================================================================

QUESTION_PATTERN = re.compile(
    r"""
    ^\s*
    (?:
        第\s*(\d+)\s*题
        |
        Question\s*(\d+)
        |
        (\d+)
    )
    \s*
    (?:[\.．、:：\)）\-]\s*)?
    (.+?)
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


def parse_question_header(
    line: str,
) -> Optional[Tuple[int, str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None

    match = QUESTION_PATTERN.match(
        cleaned
    )

    if not match:
        return None

    number = (
        match.group(1)
        or match.group(2)
        or match.group(3)
    )

    question = match.group(4).strip()

    if not number or not question:
        return None

    return (
        int(number),
        question,
    )


# ======================================================================
# Option
# ======================================================================

OPTION_PATTERN = re.compile(
    r"""
    ^\s*
    ([A-Da-d])
    \s*
    (?:
        [\.．\)）:：、\-]\s*
        |
        \s+
    )
    (.+?)
    \s*$
    """,
    re.VERBOSE,
)


def parse_option(
    line: str,
) -> Optional[Tuple[str, str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None

    match = OPTION_PATTERN.match(
        cleaned
    )

    if not match:
        return None

    letter = match.group(1).upper()
    text = match.group(2).strip()

    if not text:
        return None

    return (
        letter,
        text,
    )


# ======================================================================
# Parse Questions
# ======================================================================

def parse_questions(
    text: str,
) -> List[Question]:

    lines = text.splitlines()

    questions: List[Question] = []

    current: Optional[Question] = None

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        question_header = parse_question_header(
            line
        )

        if question_header:

            if current is not None:
                questions.append(current)

            number, question_text = question_header

            current = Question(
                number=number,
                question=question_text,
                options=[],
            )

            continue

        option = parse_option(line)

        if (
            option
            and current is not None
        ):

            _, option_text = option

            current.options.append(
                option_text
            )

            continue

    if current is not None:
        questions.append(current)

    return questions


# ======================================================================
# Source Block Extraction
# ======================================================================

NUMBERED_SOURCE_PATTERN = re.compile(
    r"""
    ^\s*
    (?:\*\*)?
    (?:
        (\d+)
        |
        第\s*(\d+)\s*题
    )
    \s*
    (?:[\.．、:：\)）\-]\s*)?
    (?:\*\*)?
    (.*?)
    \s*$
    """,
    re.VERBOSE,
)


def parse_source_number(
    line: str,
) -> Optional[int]:

    cleaned = clean_line(line)

    if not cleaned:
        return None

    match = NUMBERED_SOURCE_PATTERN.match(
        cleaned
    )

    if not match:
        return None

    number = (
        match.group(1)
        or match.group(2)
    )

    if not number:
        return None

    return int(number)


def extract_numbered_source_blocks(
    part_text: str,
) -> List[SourceBlock]:

    lines = part_text.splitlines()

    blocks: List[SourceBlock] = []

    current_number: Optional[int] = None
    current_lines: List[str] = []

    def flush():

        nonlocal current_number
        nonlocal current_lines

        if (
            current_number is not None
            and current_lines
        ):

            cleaned_lines = []

            for item in current_lines:

                value = clean_line(item)

                if value:
                    cleaned_lines.append(value)

            if cleaned_lines:

                blocks.append(
                    SourceBlock(
                        number=current_number,
                        lines=cleaned_lines,
                    )
                )

        current_number = None
        current_lines = []

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        number = parse_source_number(line)

        if number is not None:

            flush()

            match = NUMBERED_SOURCE_PATTERN.match(
                line
            )

            first_text = ""

            if match:

                first_text = (
                    match.group(3)
                    or ""
                ).strip()

            current_number = number

            if first_text:
                current_lines = [
                    first_text
                ]

            continue

        if current_number is not None:

            if parse_option(line):
                continue

            if parse_question_header(line):
                continue

            if is_top_level_heading(raw_line):
                continue

            current_lines.append(line)

    flush()

    return blocks


# ======================================================================
# Speaker
# ======================================================================

def parse_speaker(
    line: str,
) -> Optional[Tuple[str, str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None

    cleaned = re.sub(
        r"^\s*\d+\s*[\.．、:：\)）\-]\s*",
        "",
        cleaned,
    )

    cleaned = re.sub(
        r"^\s*第\s*\d+\s*题\s*[\.．、:：\)）\-]?\s*",
        "",
        cleaned,
    )

    patterns = [
        (
            r"^(?:Male|Man)\s*[:：]\s*(?P<text>.+)$",
            "male",
        ),
        (
            r"^(?:Female|Woman)\s*[:：]\s*(?P<text>.+)$",
            "female",
        ),
        (
            r"^M\s*[:：]\s*(?P<text>.+)$",
            "male",
        ),
        (
            r"^F\s*[:：]\s*(?P<text>.+)$",
            "female",
        ),
        (
            r"^(?:男声|男士|男性|男)\s*[:：]\s*(?P<text>.+)$",
            "male",
        ),
        (
            r"^(?:女声|女士|女性|女)\s*[:：]\s*(?P<text>.+)$",
            "female",
        ),
    ]

    for pattern, voice_type in patterns:

        match = re.match(
            pattern,
            cleaned,
            flags=re.IGNORECASE,
        )

        if match:

            return (
                voice_type,
                match.group("text").strip(),
            )

    return None


# ======================================================================
# Dialogue Detection
# ======================================================================

def extract_speaker_lines(
    lines: List[str],
) -> List[SpeakerLine]:

    result: List[SpeakerLine] = []

    current_speaker: Optional[str] = None
    current_text: List[str] = []

    def flush():

        nonlocal current_speaker
        nonlocal current_text

        if (
            current_speaker
            and current_text
        ):

            text_value = normalize_space(
                " ".join(current_text)
            )

            if text_value:

                result.append(
                    SpeakerLine(
                        speaker=current_speaker,
                        text=text_value,
                    )
                )

        current_speaker = None
        current_text = []

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        speaker = parse_speaker(line)

        if speaker:

            flush()

            (
                current_speaker,
                speaker_text,
            ) = speaker

            current_text = [
                speaker_text
            ]

            continue

        if current_speaker:

            if parse_option(line):
                continue

            if parse_question_header(line):
                continue

            current_text.append(line)

    flush()

    return result


def is_real_dialogue(
    speaker_lines: List[SpeakerLine],
) -> bool:

    speakers = {
        item.speaker
        for item in speaker_lines
    }

    return (
        "male" in speakers
        and "female" in speakers
    )


# ======================================================================
# Source Block Text
# ======================================================================

def source_block_text(
    block: SourceBlock,
) -> str:

    return normalize_space(
        " ".join(block.lines)
    )


# ======================================================================
# Part C Passage
# ======================================================================

def is_answer_section(
    line: str,
) -> bool:

    cleaned = clean_line(line)

    patterns = [
        r"^标准答案\s*$",
        r"^答案\s*$",
        r"^答案与解析\s*$",
        r"^解析\s*$",
        r"^二、标准答案",
        r"^三、标准答案",
    ]

    for pattern in patterns:

        if re.match(
            pattern,
            cleaned,
            flags=re.IGNORECASE,
        ):
            return True

    return False


def extract_passage(
    text: str,
) -> str:

    lines = text.splitlines()

    passage_lines: List[str] = []

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        if parse_question_header(line):
            break

        if re.match(
            r"^(Questions?|问题|选择题)\s*:?\s*$",
            line,
            flags=re.IGNORECASE,
        ):
            break

        if is_answer_section(line):
            break

        if is_top_level_heading(raw_line):
            break

        passage_lines.append(line)

    return normalize_space(
        " ".join(passage_lines)
    )


def extract_part_c_passage_from_answer(
    answer_text: str,
) -> str:

    part_c = extract_part(
        answer_text,
        "C",
    )

    if not part_c:
        return ""

    return extract_passage(
        part_c
    )


# ======================================================================
# Validation
# ======================================================================

def validate_questions(
    questions: List[Question],
    part_name: str,
):

    if len(questions) != 5:

        raise RuntimeError(
            f"{part_name} 校验失败："
            f"期望 5 题，实际 {len(questions)} 题"
        )

    numbers = [
        q.number
        for q in questions
    ]

    if sorted(numbers) != [1, 2, 3, 4, 5]:

        raise RuntimeError(
            f"{part_name} 题号错误："
            f"期望 [1, 2, 3, 4, 5]，"
            f"实际 {numbers}"
        )

    for question in questions:

        if len(question.options) != 4:

            raise RuntimeError(
                f"{part_name} 第 {question.number} 题"
                f"选项数量错误："
                f"期望 4，"
                f"实际 {len(question.options)}"
            )


def validate_source_blocks(
    blocks: List[SourceBlock],
    part_name: str,
):

    if len(blocks) != 5:

        raise RuntimeError(
            f"{part_name} 听力原文恢复失败："
            f"期望 5 个编号原文，"
            f"实际 {len(blocks)} 个"
        )

    numbers = [
        block.number
        for block in blocks
    ]

    if sorted(numbers) != [1, 2, 3, 4, 5]:

        raise RuntimeError(
            f"{part_name} 听力原文题号错误："
            f"期望 [1, 2, 3, 4, 5]，"
            f"实际 {numbers}"
        )

    for block in blocks:

        if not source_block_text(block):

            raise RuntimeError(
                f"{part_name} 第 {block.number} 题"
                "听力原文为空"
            )


def validate_part_c(
    passage: str,
    questions: List[Question],
) -> List[str]:

    errors: List[str] = []

    if not passage.strip():

        errors.append(
            "Part C 原文为空：无法从答案与解析中恢复 Part C 原文"
        )

    if len(questions) != 5:

        errors.append(
            f"Part C 题目数量错误：期望 5，实际 {len(questions)}"
        )

    numbers = [
        q.number
        for q in questions
    ]

    if len(numbers) != len(set(numbers)):

        errors.append(
            "Part C 存在重复题号"
        )

    expected = [
        1,
        2,
        3,
        4,
        5,
    ]

    if sorted(numbers) != expected:

        errors.append(
            f"Part C 题号错误：期望 {expected}，实际 {numbers}"
        )

    for question in questions:

        if len(question.options) != 4:

            errors.append(
                f"Part C 第 {question.number} 题"
                f"选项数量错误："
                f"期望 4，实际 {len(question.options)}"
            )

    return errors


# ======================================================================
# Text Language Detection
# ======================================================================

def contains_chinese(
    text: str,
) -> bool:

    return bool(
        re.search(
            r"[\u3400-\u4dbf\u4e00-\u9fff\u3040-\u30ff]",
            text,
        )
    )


def contains_english(
    text: str,
) -> bool:

    return bool(
        re.search(
            r"[A-Za-z]",
            text,
        )
    )


# ======================================================================
# Voice Selection
# ======================================================================

def select_chinese_voice(
    available_voices: set[str],
) -> Optional[str]:

    preferred = [
        "zf_xiaobei",
        "zf_xiaoni",
        "zf_xiaoxiao",
        "zf_xiaoyi",
        "zm_yunjian",
        "zm_yunxi",
        "zm_yunyang",
        "zm_yunxia",
    ]

    for voice in preferred:

        if voice in available_voices:
            return voice

    chinese_voices = sorted(
        voice
        for voice in available_voices
        if (
            voice.startswith("zf_")
            or voice.startswith("zm_")
        )
    )

    if chinese_voices:

        return chinese_voices[0]

    return None


def validate_and_select_voices(
    kokoro,
    requested_male_voice: str,
    requested_female_voice: str,
) -> Tuple[str, str, Optional[str]]:

    print()
    print(
        "  → 正在读取本地 Kokoro voices"
    )

    available_voices = set(
        kokoro.get_voices()
    )

    if not available_voices:

        raise RuntimeError(
            "Kokoro voices-v1.1-zh.bin 中没有检测到任何 voice"
        )

    print(
        f"  ✓ Available voices: "
        f"{len(available_voices)}"
    )

    english_voices = sorted(
        voice
        for voice in available_voices
        if (
            voice.startswith("af_")
            or voice.startswith("am_")
            or voice.startswith("bf_")
            or voice.startswith("bm_")
        )
    )

    chinese_voices = sorted(
        voice
        for voice in available_voices
        if (
            voice.startswith("zf_")
            or voice.startswith("zm_")
        )
    )

    print(
        "  ✓ Local English voices:"
    )

    if english_voices:

        for voice in english_voices:

            print(
                f"      {voice}"
            )

    else:

        print(
            "      <none>"
        )

    print(
        "  ✓ Local Chinese voices:"
    )

    if chinese_voices:

        for voice in chinese_voices:

            print(
                f"      {voice}"
            )

    else:

        print(
            "      <none>"
        )

    female_voice = None

    if requested_female_voice in available_voices:

        female_voice = requested_female_voice

    else:

        female_fallbacks = [
            "af_maple",
            "af_sol",
        ]

        for voice in female_fallbacks:

            if voice in available_voices:

                female_voice = voice
                break

    if female_voice is None:

        raise RuntimeError(
            "没有可用的英语女性 Kokoro voice。"
            f"请求的 voice={requested_female_voice}。"
            f"本地可用英语 voice={english_voices}"
        )

    male_voice = None

    if requested_male_voice in available_voices:

        male_voice = requested_male_voice

    else:

        male_fallbacks = [
            "bf_vale",
        ]

        for voice in male_fallbacks:

            if voice in available_voices:

                male_voice = voice
                break

    if male_voice is None:

        raise RuntimeError(
            "没有可用的英语男性 Kokoro voice。"
            f"请求的 voice={requested_male_voice}。"
            f"本地可用英语 voice={english_voices}"
        )

    chinese_voice = select_chinese_voice(
        available_voices
    )

    print()
    print(
        f"  ✓ Selected female voice: "
        f"{female_voice}"
    )

    print(
        f"  ✓ Selected male voice: "
        f"{male_voice}"
    )

    if chinese_voice:

        print(
            f"  ✓ Selected Chinese voice: "
            f"{chinese_voice}"
        )

    else:

        print(
            "  ⚠️ 未检测到中文 Kokoro voice"
        )

        print(
            "  ⚠️ 中文选项将使用英语 voice 保底，"
            "但不会被删除"
        )

    return (
        male_voice,
        female_voice,
        chinese_voice,
    )


# ======================================================================
# Segment Voice
# ======================================================================

def choose_text_voice(
    text: str,
    default_voice: str,
    chinese_voice: Optional[str],
) -> str:

    if (
        chinese_voice
        and contains_chinese(text)
        and not contains_english(text)
    ):

        return chinese_voice

    return default_voice


# ======================================================================
# Source Rendering
# ======================================================================

def build_source_segments(
    block: SourceBlock,
    first_pass: bool,
    male_voice: str,
    female_voice: str,
    chinese_voice: Optional[str],
) -> List[Segment]:

    source_text = source_block_text(block)

    speaker_lines = extract_speaker_lines(
        block.lines
    )

    real_dialogue = is_real_dialogue(
        speaker_lines
    )

    segments: List[Segment] = []

    if not real_dialogue:

        voice = (
            female_voice
            if first_pass
            else male_voice
        )

        voice = choose_text_voice(
            source_text,
            voice,
            chinese_voice,
        )

        segments.append(
            Segment(
                text=source_text,
                voice=voice,
                repeat=1,
            )
        )

        return segments

    for item in speaker_lines:

        if first_pass:

            if item.speaker == "male":

                voice = male_voice

            else:

                voice = female_voice

        else:

            if item.speaker == "male":

                voice = female_voice

            else:

                voice = male_voice

        voice = choose_text_voice(
            item.text,
            voice,
            chinese_voice,
        )

        segments.append(
            Segment(
                text=item.text,
                voice=voice,
                repeat=1,
            )
        )

    return segments


# ======================================================================
# Question Segments
# ======================================================================

def build_question_segments(
    question: Question,
    voice: str,
    chinese_voice: Optional[str],
) -> List[Segment]:

    segments: List[Segment] = []

    question_voice = choose_text_voice(
        question.question,
        voice,
        chinese_voice,
    )

    segments.append(
        Segment(
            text=question.question,
            voice=question_voice,
            repeat=1,
        )
    )

    for option in question.options:

        option_voice = choose_text_voice(
            option,
            voice,
            chinese_voice,
        )

        segments.append(
            Segment(
                text=option,
                voice=option_voice,
                repeat=1,
            )
        )

    return segments


# ======================================================================
# Part A
# ======================================================================

def build_part_a(
    questions: List[Question],
    source_blocks: List[SourceBlock],
    male_voice: str,
    female_voice: str,
    chinese_voice: Optional[str],
) -> List[Segment]:

    segments: List[Segment] = []

    source_map = {
        block.number: block
        for block in source_blocks
    }

    for first_pass in [True, False]:

        for question in questions:

            block = source_map.get(
                question.number
            )

            if block is None:

                raise RuntimeError(
                    "Part A 无法找到对应原文："
                    f"第 {question.number} 题"
                )

            segments.extend(
                build_source_segments(
                    block=block,
                    first_pass=first_pass,
                    male_voice=male_voice,
                    female_voice=female_voice,
                    chinese_voice=chinese_voice,
                )
            )

            question_voice = (
                female_voice
                if first_pass
                else male_voice
            )

            segments.extend(
                build_question_segments(
                    question=question,
                    voice=question_voice,
                    chinese_voice=chinese_voice,
                )
            )

    return segments


# ======================================================================
# Part B
# ======================================================================

def build_part_b(
    questions: List[Question],
    source_blocks: List[SourceBlock],
    male_voice: str,
    female_voice: str,
    chinese_voice: Optional[str],
) -> List[Segment]:

    segments: List[Segment] = []

    source_map = {
        block.number: block
        for block in source_blocks
    }

    all_speaker_lines: List[SpeakerLine] = []

    for block in source_blocks:

        all_speaker_lines.extend(
            extract_speaker_lines(
                block.lines
            )
        )

    real_dialogue = is_real_dialogue(
        all_speaker_lines
    )

    print()

    if real_dialogue:

        print(
            "  ✓ Part B 检测结果：真实 M/F 对话"
        )

        print(
            "  ✓ 第一遍：M=男声 / F=女声"
        )

        print(
            "  ✓ 第二遍：M=女声 / F=男声"
        )

    else:

        print(
            "  ✓ Part B 检测结果：非对话"
        )

        print(
            "  ✓ 第一遍：统一女声"
        )

        print(
            "  ✓ 第二遍：统一男声"
        )

    for first_pass in [True, False]:

        for question in questions:

            block = source_map.get(
                question.number
            )

            if block is None:

                raise RuntimeError(
                    "Part B 无法找到对应原文："
                    f"第 {question.number} 题"
                )

            segments.extend(
                build_source_segments(
                    block=block,
                    first_pass=first_pass,
                    male_voice=male_voice,
                    female_voice=female_voice,
                    chinese_voice=chinese_voice,
                )
            )

            question_voice = (
                female_voice
                if first_pass
                else male_voice
            )

            segments.extend(
                build_question_segments(
                    question=question,
                    voice=question_voice,
                    chinese_voice=chinese_voice,
                )
            )

    return segments


# ======================================================================
# Part C
# ======================================================================

def build_part_c(
    passage: str,
    questions: List[Question],
    male_voice: str,
    female_voice: str,
    chinese_voice: Optional[str],
) -> List[Segment]:

    segments: List[Segment] = []

    for first_pass in [True, False]:

        voice = (
            female_voice
            if first_pass
            else male_voice
        )

        passage_voice = choose_text_voice(
            passage,
            voice,
            chinese_voice,
        )

        segments.append(
            Segment(
                text=passage,
                voice=passage_voice,
                repeat=1,
            )
        )

        for question in questions:

            segments.extend(
                build_question_segments(
                    question=question,
                    voice=voice,
                    chinese_voice=chinese_voice,
                )
            )

    return segments


# ======================================================================
# Audio / Kokoro
# ======================================================================

def load_kokoro():

    try:

        from kokoro_onnx import Kokoro

    except ImportError:

        print(
            "ERROR: 未找到 kokoro_onnx。",
            file=sys.stderr,
        )

        print(
            "请安装：pip install -U kokoro-onnx",
            file=sys.stderr,
        )

        raise

    return Kokoro


def get_file_size(path: Path) -> int:

    try:
        return path.stat().st_size
    except OSError:
        return 0


def validate_kokoro_files(
    model_path: Path,
    voices_path: Path,
) -> Tuple[int, int]:

    if not model_path.exists():

        raise FileNotFoundError(
            f"Kokoro ONNX 模型不存在：{model_path}"
        )

    if not voices_path.exists():

        raise FileNotFoundError(
            f"Kokoro voices 不存在：{voices_path}"
        )

    model_size = get_file_size(
        model_path
    )

    voices_size = get_file_size(
        voices_path
    )

    print()
    print(
        "  FILE CHECK"
    )

    print(
        f"  Model size  : "
        f"{model_size:,} bytes"
    )

    print(
        f"  Voices size : "
        f"{voices_size:,} bytes"
    )

    if model_size < 100_000_000:

        raise RuntimeError(
            "Kokoro ONNX 模型文件不是完整模型。"
            "\n"
            f"Model: {model_path}"
            "\n"
            f"Model size: {model_size:,} bytes"
            "\n"
            "\n"
            "正常模型约为 163 MB。"
            "\n"
            "当前文件很可能是 Git LFS pointer。"
            "\n"
            "请确认 GitHub Actions checkout 使用："
            "\n"
            "  actions/checkout@v4"
            "\n"
            "  with:"
            "\n"
            "    lfs: true"
        )

    if voices_size < 10_000_000:

        raise RuntimeError(
            "Kokoro voices 文件不是完整文件。"
            "\n"
            f"Voices: {voices_path}"
            "\n"
            f"Voices size: {voices_size:,} bytes"
            "\n"
            "\n"
            "正常 voices 文件约为 54 MB。"
            "\n"
            "当前文件很可能是 Git LFS pointer。"
            "\n"
            "请确认 GitHub Actions checkout 使用："
            "\n"
            "  actions/checkout@v4"
            "\n"
            "  with:"
            "\n"
            "    lfs: true"
        )

    print()
    print(
        "  ✓ Kokoro model files are real files"
    )

    return (
        model_size,
        voices_size,
    )


def load_kokoro_with_validation(
    model_path: Path,
    voices_path: Path,
):

    Kokoro = load_kokoro()

    validate_kokoro_files(
        model_path=model_path,
        voices_path=voices_path,
    )

    print()
    print(
        "  → Kokoro load"
    )

    try:

        kokoro = Kokoro(
            str(model_path),
            str(voices_path),
        )

    except Exception as exc:

        print()
        print(
            "  ✗ Kokoro 加载失败"
        )

        print(
            f"  Error type: "
            f"{type(exc).__name__}"
        )

        print(
            f"  Error: {exc}"
        )

        raise RuntimeError(
            "Kokoro ONNX 模型加载失败。"
            "\n"
            f"Model: {model_path}"
            "\n"
            f"Model size: "
            f"{get_file_size(model_path):,} bytes"
            "\n"
            "\n"
            f"Voices: {voices_path}"
            "\n"
            f"Voices size: "
            f"{get_file_size(voices_path):,} bytes"
        ) from exc

    print()
    print(
        "  ✓ Kokoro ONNX 模型加载完成"
    )

    return kokoro


def synthesize_to_wav(
    kokoro,
    text: str,
    voice: str,
    speed: float,
    language: str,
    output_wav: Path,
):

    if not text.strip():
        return

    samples, sample_rate = kokoro.create(
        text,
        voice=voice,
        speed=speed,
    )

    import soundfile as sf

    sf.write(
        str(output_wav),
        samples,
        sample_rate,
    )


def run_ffmpeg(
    input_wav: Path,
    output_audio: Path,
):

    if output_audio.suffix.lower() == ".wav":

        if (
            input_wav.resolve()
            != output_audio.resolve()
        ):

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(input_wav),
                    str(output_audio),
                ],
                check=True,
            )

        return

    if output_audio.suffix.lower() == ".mp3":

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_wav),
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output_audio),
        ]

    elif output_audio.suffix.lower() == ".m4a":

        command = [
            "ffmpeg",
            "-y",
            "-i",
            str(input_wav),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output_audio),
        ]

    else:

        raise ValueError(
            f"不支持的音频格式："
            f"{output_audio.suffix}"
        )

    subprocess.run(
        command,
        check=True,
    )


def create_silence_wav(
    output_wav: Path,
    duration: float,
):

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=24000:cl=mono",
            "-t",
            str(duration),
            "-ar",
            "24000",
            "-ac",
            "1",
            str(output_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def concat_wavs(
    wav_files: List[Path],
    output_wav: Path,
):

    concat_file = (
        output_wav.parent
        / f"{output_wav.stem}_concat.txt"
    )

    with concat_file.open(
        "w",
        encoding="utf-8",
    ) as f:

        for wav in wav_files:

            escaped = str(
                wav.resolve()
            ).replace(
                "'",
                "'\\''",
            )

            f.write(
                f"file '{escaped}'\n"
            )

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output_wav),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        concat_file.unlink()
    except FileNotFoundError:
        pass


# ======================================================================
# Segment Rendering
# ======================================================================

def render_segments(
    kokoro,
    segments: List[Segment],
    output_audio: Path,
    speed: float,
    language: str,
    temp_dir: Path,
):

    temp_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    wav_files: List[Path] = []

    segment_index = 0

    for segment in segments:

        if not segment.text.strip():
            continue

        for repeat_index in range(
            segment.repeat
        ):

            segment_index += 1

            wav_path = (
                temp_dir
                / f"{segment_index:04d}.wav"
            )

            synthesize_to_wav(
                kokoro=kokoro,
                text=segment.text,
                voice=segment.voice,
                speed=speed,
                language=language,
                output_wav=wav_path,
            )

            wav_files.append(
                wav_path
            )

            if (
                repeat_index
                < segment.repeat - 1
            ):

                silence_path = (
                    temp_dir
                    / (
                        f"{segment_index:04d}"
                        "_repeat_silence.wav"
                    )
                )

                create_silence_wav(
                    silence_path,
                    0.7,
                )

                wav_files.append(
                    silence_path
                )

        silence_path = (
            temp_dir
            / (
                f"{segment_index:04d}"
                "_segment_silence.wav"
            )
        )

        create_silence_wav(
            silence_path,
            0.3,
        )

        wav_files.append(
            silence_path
        )

    if not wav_files:

        raise RuntimeError(
            f"没有可生成的音频片段："
            f"{output_audio.name}"
        )

    merged_wav = (
        temp_dir
        / f"{output_audio.stem}_merged.wav"
    )

    concat_wavs(
        wav_files,
        merged_wav,
    )

    run_ffmpeg(
        input_wav=merged_wav,
        output_audio=output_audio,
    )


# ======================================================================
# Main
# ======================================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 英语学习系统 "
            "Audio Generator V2.3.0"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help="业务日期 YYYY-MM-DD",
    )

    parser.add_argument(
        "--exam-file",
        required=True,
        help="试卷 Markdown",
    )

    parser.add_argument(
        "--answer-file",
        required=True,
        help="答案与解析 Markdown",
    )

    parser.add_argument(
        "--audio-format",
        "--format",
        dest="audio_format",
        default="mp3",
        choices=[
            "mp3",
            "m4a",
            "wav",
        ],
        help="音频格式，默认 mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Kokoro 语速，默认 1.0",
    )

    parser.add_argument(
        "--male-voice",
        default="bf_vale",
        help="男性声音，默认 bf_vale",
    )

    parser.add_argument(
        "--female-voice",
        default="af_maple",
        help="女性声音，默认 af_maple",
    )

    parser.add_argument(
        "--language",
        default="en-us",
        help="CLI 兼容参数；不传给 kokoro.create()",
    )

    args = parser.parse_args()

    date = args.date

    exam_file = Path(
        args.exam_file
    ).resolve()

    answer_file = Path(
        args.answer_file
    ).resolve()

    # ==================================================================
    # CONFIG
    # ==================================================================

    print("=" * 70)
    print("748686 英语学习系统")
    print("Audio Generator V2.3.0")
    print("=" * 70)

    print()
    print("CONFIG")
    print(f"  Date          : {date}")
    print(f"  Exam          : {exam_file}")
    print(f"  Answer        : {answer_file}")
    print(f"  Format        : {args.audio_format}")
    print(f"  Speed         : {args.speed}")
    print(f"  Male voice    : {args.male_voice}")
    print(f"  Female voice  : {args.female_voice}")
    print(f"  Language      : {args.language}")

    # ==================================================================
    # File Validation
    # ==================================================================

    if not exam_file.exists():

        raise FileNotFoundError(
            f"试卷不存在：{exam_file}"
        )

    if not answer_file.exists():

        raise FileNotFoundError(
            f"答案与解析不存在：{answer_file}"
        )

    exam_text = exam_file.read_text(
        encoding="utf-8"
    )

    answer_text = answer_file.read_text(
        encoding="utf-8"
    )

    # ==================================================================
    # Recover Part A
    # ==================================================================

    print()
    print("=" * 70)
    print("PART A")
    print("=" * 70)

    exam_part_a = extract_part(
        exam_text,
        "A",
    )

    answer_part_a = extract_part(
        answer_text,
        "A",
    )

    part_a_questions = parse_questions(
        exam_part_a
    )

    part_a_sources = extract_numbered_source_blocks(
        answer_part_a
    )

    print(
        f"  Questions from exam: "
        f"{len(part_a_questions)}"
    )

    print(
        f"  Listening originals from answer: "
        f"{len(part_a_sources)}"
    )

    validate_questions(
        part_a_questions,
        "Part A",
    )

    validate_source_blocks(
        part_a_sources,
        "Part A",
    )

    print(
        "  ✓ Part A 题目来自试卷"
    )

    print(
        "  ✓ Part A 原文来自答案与解析"
    )

    print(
        "  ✓ Part A 5 题与 5 段原文一一对应"
    )

    # ==================================================================
    # Recover Part B
    # ==================================================================

    print()
    print("=" * 70)
    print("PART B")
    print("=" * 70)

    exam_part_b = extract_part(
        exam_text,
        "B",
    )

    answer_part_b = extract_part(
        answer_text,
        "B",
    )

    part_b_questions = parse_questions(
        exam_part_b
    )

    part_b_sources = extract_numbered_source_blocks(
        answer_part_b
    )

    print(
        f"  Questions from exam: "
        f"{len(part_b_questions)}"
    )

    print(
        f"  Listening originals from answer: "
        f"{len(part_b_sources)}"
    )

    validate_questions(
        part_b_questions,
        "Part B",
    )

    validate_source_blocks(
        part_b_sources,
        "Part B",
    )

    print(
        "  ✓ Part B 题目来自试卷"
    )

    print(
        "  ✓ Part B 原文来自答案与解析"
    )

    print(
        "  ✓ Part B 5 题与 5 段原文一一对应"
    )

    # ==================================================================
    # Detect Part B Dialogue
    # ==================================================================

    part_b_speaker_lines: List[SpeakerLine] = []

    for block in part_b_sources:

        part_b_speaker_lines.extend(
            extract_speaker_lines(
                block.lines
            )
        )

    part_b_is_dialogue = is_real_dialogue(
        part_b_speaker_lines
    )

    if part_b_is_dialogue:

        print()
        print(
            "  ✓ Part B = TRUE DIALOGUE"
        )

        print(
            "  ✓ 检测到 M + F"
        )

    else:

        print()
        print(
            "  ✓ Part B = MONOLOGUE"
        )

        print(
            "  ✓ 即使存在 M: 标记，"
            "只要没有 F:，仍按非对话处理"
        )

    # ==================================================================
    # Recover Part C
    # ==================================================================

    print()
    print("=" * 70)
    print("PART C")
    print("=" * 70)

    exam_part_c = extract_part(
        exam_text,
        "C",
    )

    part_c_questions = parse_questions(
        exam_part_c
    )

    print(
        f"  Questions from exam: "
        f"{len(part_c_questions)}"
    )

    for question in part_c_questions:

        print(
            f"  Q{question.number}: "
            f"{len(question.options)} options"
        )

    part_c_passage = (
        extract_part_c_passage_from_answer(
            answer_text
        )
    )

    print(
        f"  Passage from answer: "
        f"{len(part_c_passage)} chars"
    )

    part_c_errors = validate_part_c(
        passage=part_c_passage,
        questions=part_c_questions,
    )

    if part_c_errors:

        print()
        print("=" * 70)
        print("ERROR")
        print("=" * 70)

        print(
            "Part C 校验失败："
        )

        print()

        for error in part_c_errors:

            print(
                f"  ✗ {error}"
            )

        print()

        raise RuntimeError(
            "Part C 数据结构不完整，"
            "为避免生成错误听力，"
            "已停止音频生成。"
        )

    print()
    print(
        "  ✓ Part C 原文存在"
    )

    print(
        "  ✓ Part C = 5 questions"
    )

    print(
        "  ✓ 每题 = 4 options"
    )

    print(
        "  ✓ 题号 = 1 / 2 / 3 / 4 / 5"
    )

    # ==================================================================
    # Output
    # ==================================================================

    output_dir = exam_file.parent

    listening_dir = (
        output_dir / "听力"
    )

    listening_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix = f".{args.audio_format}"

    output_a = (
        listening_dir
        / f"Listening_A{suffix}"
    )

    output_b = (
        listening_dir
        / f"Listening_B{suffix}"
    )

    output_c = (
        listening_dir
        / f"Listening_C{suffix}"
    )

    output_all = (
        listening_dir
        / f"Listening_总音频{suffix}"
    )

    # ==================================================================
    # Load Kokoro
    # ==================================================================

    print()
    print("=" * 70)
    print("KOKORO")
    print("=" * 70)

    print(
        "  → 正在加载本地 Kokoro ONNX 模型"
    )

    project_root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    model_dir = (
        project_root
        / "models"
        / "kokoro"
    )

    model_path = (
        model_dir
        / "kokoro-v1.1-zh.fp16.onnx"
    )

    voices_path = (
        model_dir
        / "voices-v1.1-zh.bin"
    )

    print(
        f"  Model: {model_path}"
    )

    print(
        f"  Voices: {voices_path}"
    )

    kokoro = load_kokoro_with_validation(
        model_path=model_path,
        voices_path=voices_path,
    )

    (
        actual_male_voice,
        actual_female_voice,
        actual_chinese_voice,
    ) = validate_and_select_voices(
        kokoro=kokoro,
        requested_male_voice=args.male_voice,
        requested_female_voice=args.female_voice,
    )

    # ==================================================================
    # Build Segments
    # ==================================================================

    segments_a = build_part_a(
        questions=part_a_questions,
        source_blocks=part_a_sources,
        male_voice=actual_male_voice,
        female_voice=actual_female_voice,
        chinese_voice=actual_chinese_voice,
    )

    segments_b = build_part_b(
        questions=part_b_questions,
        source_blocks=part_b_sources,
        male_voice=actual_male_voice,
        female_voice=actual_female_voice,
        chinese_voice=actual_chinese_voice,
    )

    segments_c = build_part_c(
        passage=part_c_passage,
        questions=part_c_questions,
        male_voice=actual_male_voice,
        female_voice=actual_female_voice,
        chinese_voice=actual_chinese_voice,
    )

    print()
    print("=" * 70)
    print("AUDIO PLAN")
    print("=" * 70)

    print(
        f"  Listening A logical segments: "
        f"{len(segments_a)}"
    )

    print(
        f"  Listening B logical segments: "
        f"{len(segments_b)}"
    )

    print(
        f"  Listening C logical segments: "
        f"{len(segments_c)}"
    )

    # ==================================================================
    # Part C segment validation
    #
    # 每一遍：
    #
    #   1 passage
    #   + 5 questions
    #   + 20 options
    #
    # = 26
    #
    # 两遍：
    #
    # = 52
    # ==================================================================

    expected_part_c_segments = 52

    if (
        len(segments_c)
        != expected_part_c_segments
    ):

        raise RuntimeError(
            "Part C 音频逻辑片段数量错误："
            f"期望 {expected_part_c_segments}，"
            f"实际 {len(segments_c)}"
        )

    print(
        "  ✓ Part C = 26 logical segments × 2"
    )

    # ==================================================================
    # Part A / B expected logical segment count
    #
    # 每一题：
    #
    #   原文
    #   + question
    #   + 4 options
    #
    # = 6
    #
    # 5题 × 6 = 30
    #
    # 两遍 = 60
    #
    # 对话原文可能被拆成 M/F 多个音频 segment，
    # 因此 Part B 不强制要求物理 segment = 60。
    # ==================================================================

    expected_basic_segments = 60

    if not part_b_is_dialogue:

        if len(segments_a) != expected_basic_segments:

            raise RuntimeError(
                "Part A 音频逻辑片段数量错误："
                f"期望 {expected_basic_segments}，"
                f"实际 {len(segments_a)}"
            )

        if len(segments_b) != expected_basic_segments:

            raise RuntimeError(
                "Part B 音频逻辑片段数量错误："
                f"期望 {expected_basic_segments}，"
                f"实际 {len(segments_b)}"
            )

    print(
        f"  ✓ Part A = {len(segments_a)} segments"
    )

    print(
        f"  ✓ Part B = {len(segments_b)} segments"
    )

    print(
        f"  ✓ Part C = {len(segments_c)} segments"
    )

    # ==================================================================
    # Temporary directory
    # ==================================================================

    temp_root = (
        listening_dir
        / ".audio_tmp"
    )

    if temp_root.exists():

        import shutil

        shutil.rmtree(
            temp_root
        )

    temp_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==================================================================
    # Generate A
    # ==================================================================

    print()
    print("=" * 70)
    print("GENERATE LISTENING A")
    print("=" * 70)

    render_segments(
        kokoro=kokoro,
        segments=segments_a,
        output_audio=output_a,
        speed=args.speed,
        language=args.language,
        temp_dir=temp_root / "A",
    )

    print(
        f"  ✓ {output_a}"
    )

    # ==================================================================
    # Generate B
    # ==================================================================

    print()
    print("=" * 70)
    print("GENERATE LISTENING B")
    print("=" * 70)

    render_segments(
        kokoro=kokoro,
        segments=segments_b,
        output_audio=output_b,
        speed=args.speed,
        language=args.language,
        temp_dir=temp_root / "B",
    )

    print(
        f"  ✓ {output_b}"
    )

    # ==================================================================
    # Generate C
    # ==================================================================

    print()
    print("=" * 70)
    print("GENERATE LISTENING C")
    print("=" * 70)

    render_segments(
        kokoro=kokoro,
        segments=segments_c,
        output_audio=output_c,
        speed=args.speed,
        language=args.language,
        temp_dir=temp_root / "C",
    )

    print(
        f"  ✓ {output_c}"
    )

    # ==================================================================
    # Generate Combined Audio
    # ==================================================================

    print()
    print("=" * 70)
    print("GENERATE TOTAL LISTENING")
    print("=" * 70)

    combined_temp = (
        temp_root
        / "TOTAL"
    )

    combined_temp.mkdir(
        parents=True,
        exist_ok=True,
    )

    total_wavs: List[Path] = []

    for index, audio_file in enumerate(
        [
            output_a,
            output_b,
            output_c,
        ],
        start=1,
    ):

        wav_file = (
            combined_temp
            / f"{index:02d}.wav"
        )

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_file),
                "-ar",
                "24000",
                "-ac",
                "1",
                str(wav_file),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        total_wavs.append(
            wav_file
        )

        if index < 3:

            silence = (
                combined_temp
                / f"{index:02d}_silence.wav"
            )

            create_silence_wav(
                silence,
                0.5,
            )

            total_wavs.append(
                silence
            )

    merged_total_wav = (
        combined_temp
        / "Listening_总音频.wav"
    )

    concat_wavs(
        wav_files=total_wavs,
        output_wav=merged_total_wav,
    )

    run_ffmpeg(
        input_wav=merged_total_wav,
        output_audio=output_all,
    )

    print(
        f"  ✓ {output_all}"
    )

    # ==================================================================
    # Cleanup
    # ==================================================================

    import shutil

    try:

        shutil.rmtree(
            temp_root
        )

    except Exception as exc:

        print(
            f"  ⚠️ 临时目录清理失败：{exc}"
        )

    # ==================================================================
    # Final Validation
    # ==================================================================

    print()
    print("=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    outputs = [
        output_a,
        output_b,
        output_c,
        output_all,
    ]

    for output in outputs:

        if not output.exists():

            raise RuntimeError(
                f"音频生成失败："
                f"{output}"
            )

        size = output.stat().st_size

        if size <= 0:

            raise RuntimeError(
                f"音频文件为空："
                f"{output}"
            )

        print(
            f"  ✓ {output.name}"
            f"  ({size:,} bytes)"
        )

    print()
    print("=" * 70)
    print(
        "748686 英语学习系统 AUDIO COMPLETE"
    )
    print("=" * 70)

    print()
    print("Output directory:")
    print(f"  {listening_dir}")
    print()

    return 0


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    try:

        sys.exit(
            main()
        )

    except KeyboardInterrupt:

        print()
        print(
            "用户中断音频生成。"
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print("=" * 70)
        print("ERROR")
        print("=" * 70)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        sys.exit(1)
