#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.2.3
======================================================================

职责
======================================================================

只负责：

    1. 读取已经存在的试卷 Markdown
    2. 读取已经存在的答案与解析 Markdown
    3. 恢复 Listening A / B / C
    4. 使用本地 Kokoro ONNX 模型生成音频
    5. 输出：

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
V2.2.3 修复
======================================================================

1. 修复 Part B：

   支持：

       M: ...
       F: ...

   以及答案解析常见格式：

       **1.** M: ...
       **2.** F: ...

2. 修复 Part C：

   Part C 题目/选项：

       只来自试卷 Markdown

   Part C 原文：

       只来自答案与解析 Markdown

   Part C 不再吞掉：

       二、单项选择
       三、多项选择
       四、完形填空
       五、阅读理解
       六、翻译
       七、写作

3. Part C 严格校验：

       5 道题
       每题 4 个选项
       题号必须唯一
       题号必须为 1~5

4. 支持中英文 Part Header：

       PART A
       PART B
       PART C

       Listening A
       Listening B
       Listening C

       第一部分
       第二部分
       第三部分

5. 保持 A / B 原有音频逻辑。

6. Kokoro 修复：

       使用官方 kokoro-onnx API

       Kokoro(
           model_path,
           voices_path,
       )

       kokoro.get_voices()

       kokoro.create(
           text,
           voice=voice,
           speed=speed,
       )

   不再向 create() 传入 lang 参数。

7. 本地 Voice 修复：

   当前 voices-v1.1-zh.bin 实际验证存在：

       af_maple
       af_sol
       bf_vale

   默认：

       female = af_maple
       male   = bf_vale

   同时在运行时检查指定 voice 是否真实存在。
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
    dialogue: str = ""


# ======================================================================
# 基础工具
# ======================================================================

def clean_line(line: str) -> str:
    """
    清理 Markdown 常见格式，但不破坏正文。
    """

    line = line.strip()

    if not line:
        return ""

    # Markdown heading
    line = re.sub(r"^\s*#{1,6}\s*", "", line)

    # Markdown bullet
    line = re.sub(r"^\s*[-*+]\s+", "", line)

    # Markdown bold
    line = re.sub(r"^\*\*(.*?)\*\*$", r"\1", line)

    # Markdown italic
    line = re.sub(r"^\*(.*?)\*$", r"\1", line)

    return line.strip()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_top_level_heading(line: str) -> bool:
    """
    判断是否为 Markdown 一级标题。

    例如：

        # 一、听力
        # 二、单项选择
        # 三、多项选择

    Part C 到达：

        # 二、单项选择

    时必须停止。
    """

    return bool(re.match(r"^\s*#\s+.+", line))


# ======================================================================
# Part Header
# ======================================================================

def is_part_header(line: str, part: str) -> bool:
    """
    统一识别 Listening Part A/B/C。
    """

    cleaned = clean_line(line)
    cleaned_upper = cleaned.upper()

    part = part.upper()

    english_patterns = [
        rf"^PART\s+{part}\s*$",
        rf"^LISTENING\s+{part}\s*$",
        rf"^LISTENING\s+PART\s+{part}\s*$",
    ]

    for pattern in english_patterns:

        if re.match(pattern, cleaned_upper):
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
            r"^听对话\s*$",
        ],
        "C": [
            r"^第三部分\s*$",
            r"^听力\s*C\s*$",
            r"^听力第三部分\s*$",
            r"^听原文\s*$",
        ],
    }

    for pattern in chinese_patterns.get(part, []):

        if re.match(pattern, cleaned):
            return True

    return False


def find_part_start(
    lines: List[str],
    part: str,
) -> Optional[int]:
    """
    找到 Part A/B/C 的起始行。
    """

    for i, line in enumerate(lines):

        if is_part_header(line, part):
            return i

    return None


def find_part_header(
    lines: List[str],
    part: str,
) -> Optional[int]:
    """
    与 find_part_start 保持一致。
    """

    return find_part_start(
        lines,
        part,
    )


def extract_part(
    text: str,
    part: str,
) -> str:
    """
    提取一个 Listening Part。

    关键规则：

        1. 从目标 Part Header 开始
        2. 遇到下一个 Listening Part 时停止
        3. 如果当前是最后一个 Part（尤其 Part C），
           遇到下一个一级 Markdown 标题时停止
    """

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

        # --------------------------------------------------------------
        # 下一个 Listening Part
        # --------------------------------------------------------------

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

        # --------------------------------------------------------------
        # 一级 Markdown 标题
        # --------------------------------------------------------------

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
    """
    支持：

        1. Question
        1) Question
        1、Question
        1．Question
        1: Question
        1- Question

        第1题 Question

        Question 1:
    """

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
    """
    支持：

        A. xxx
        B) xxx
        C: xxx
        D、xxx
        A- xxx
        A xxx

    同时兼容 Markdown bullet：

        - A. xxx
    """

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
# Speaker
# ======================================================================

def parse_speaker(
    line: str,
) -> Optional[Tuple[str, str]]:
    """
    解析说话人。

    支持：

        M: Hello
        F: Hello

        Male: Hello
        Female: Hello

        Man: Hello
        Woman: Hello

        男：你好
        女：你好

    同时支持答案解析中的：

        **1.** M: Hello
        **2.** F: Hi
    """

    cleaned = clean_line(line)

    if not cleaned:
        return None

    # --------------------------------------------------------------
    # 去掉前置题号
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # Speaker patterns
    # --------------------------------------------------------------

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
# Parse Questions
# ======================================================================

def parse_questions(
    text: str,
) -> List[Question]:
    """
    从 Listening Part 中恢复题目。

    只解析：

        Question Header
        +
        Options

    其他正文会忽略。
    """

    lines = text.splitlines()

    questions: List[Question] = []

    current: Optional[Question] = None

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        # --------------------------------------------------------------
        # Question
        # --------------------------------------------------------------

        question_header = parse_question_header(
            line
        )

        if question_header:

            if current is not None:
                questions.append(
                    current
                )

            number, question_text = (
                question_header
            )

            current = Question(
                number=number,
                question=question_text,
                options=[],
            )

            continue

        # --------------------------------------------------------------
        # Option
        # --------------------------------------------------------------

        option = parse_option(
            line
        )

        if (
            option
            and current is not None
        ):

            letter, option_text = option

            current.options.append(
                option_text
            )

            continue

    if current is not None:

        questions.append(
            current
        )

    return questions


# ======================================================================
# Dialogue
# ======================================================================

def extract_dialogue(
    text: str,
) -> List[Tuple[str, str]]:
    """
    提取 Part B 对话。

    返回：

        [
            ("male", "Hello ..."),
            ("female", "Hi ..."),
        ]

    支持答案解析中：

        **1.** M: ...
        **2.** F: ...
    """

    lines = text.splitlines()

    dialogue: List[Tuple[str, str]] = []

    current_voice: Optional[str] = None
    current_text: List[str] = []

    def flush():

        nonlocal current_voice
        nonlocal current_text

        if (
            current_voice
            and current_text
        ):

            text_value = normalize_space(
                " ".join(current_text)
            )

            if text_value:

                dialogue.append(
                    (
                        current_voice,
                        text_value,
                    )
                )

        current_voice = None
        current_text = []

    for raw_line in lines:

        line = clean_line(
            raw_line
        )

        if not line:
            continue

        speaker = parse_speaker(
            line
        )

        if speaker:

            flush()

            (
                current_voice,
                speaker_text,
            ) = speaker

            current_text = [
                speaker_text
            ]

            continue

        # --------------------------------------------------------------
        # 如果正在收集某个 speaker，
        # 普通行视为该 speaker 的续句。
        # --------------------------------------------------------------

        if current_voice:

            if parse_option(line):
                continue

            if parse_question_header(line):
                continue

            current_text.append(
                line
            )

    flush()

    return dialogue


def attach_dialogue(
    questions: List[Question],
    dialogue: List[Tuple[str, str]],
) -> List[Question]:
    """
    将对话按题目切分。

    当前系统的答案解析通常是：

        1. M...
           F...

        2. M...
           F...

    如果无法可靠切分，则将全部对话作为整体保留。
    """

    if (
        not questions
        or not dialogue
    ):
        return questions

    full_dialogue = " ".join(
        text
        for _, text in dialogue
    )

    for question in questions:

        question.dialogue = (
            full_dialogue
        )

    return questions


# ======================================================================
# Passage
# ======================================================================

def is_answer_section(
    line: str,
) -> bool:
    """
    判断答案解析中的结束区域。
    """

    cleaned = clean_line(
        line
    )

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
    """
    从 Part C 中提取原文。

    停止条件：

        1. 遇到题目
        2. 遇到 Questions / 问题 / 选择题
        3. 遇到答案区域
        4. 遇到下一个一级标题
    """

    lines = text.splitlines()

    passage_lines: List[str] = []

    for raw_line in lines:

        line = clean_line(
            raw_line
        )

        if not line:
            continue

        # --------------------------------------------------------------
        # Question
        # --------------------------------------------------------------

        if parse_question_header(line):
            break

        # --------------------------------------------------------------
        # 明确的题目区域
        # --------------------------------------------------------------

        if re.match(
            r"^(Questions?|问题|选择题)\s*:?\s*$",
            line,
            flags=re.IGNORECASE,
        ):
            break

        # --------------------------------------------------------------
        # 答案区域
        # --------------------------------------------------------------

        if is_answer_section(line):
            break

        # --------------------------------------------------------------
        # 一级标题
        # --------------------------------------------------------------

        if is_top_level_heading(
            raw_line
        ):
            break

        passage_lines.append(
            line
        )

    passage = normalize_space(
        " ".join(
            passage_lines
        )
    )

    return passage


def extract_part_c_passage_from_answer(
    answer_text: str,
) -> str:
    """
    Part C 原文：

        只允许从答案与解析中获取。
    """

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
# Part C Validation
# ======================================================================

def validate_part_c(
    passage: str,
    questions: List[Question],
) -> List[str]:
    """
    严格验证 Part C。

    要求：

        passage != empty

        exactly 5 questions

        numbers = 1,2,3,4,5

        every question has exactly 4 options
    """

    errors: List[str] = []

    # --------------------------------------------------------------
    # Passage
    # --------------------------------------------------------------

    if not passage.strip():

        errors.append(
            "Part C 原文为空："
            "无法从答案与解析中恢复 Part C 原文"
        )

    # --------------------------------------------------------------
    # Question count
    # --------------------------------------------------------------

    if len(questions) != 5:

        errors.append(
            f"Part C 题目数量错误："
            f"期望 5，实际 {len(questions)}"
        )

    # --------------------------------------------------------------
    # Duplicate number
    # --------------------------------------------------------------

    numbers = [
        q.number
        for q in questions
    ]

    if (
        len(numbers)
        != len(set(numbers))
    ):

        errors.append(
            "Part C 存在重复题号"
        )

    # --------------------------------------------------------------
    # Expected numbers
    # --------------------------------------------------------------

    expected = [
        1,
        2,
        3,
        4,
        5,
    ]

    if sorted(numbers) != expected:

        errors.append(
            f"Part C 题号错误："
            f"期望 {expected}，实际 {numbers}"
        )

    # --------------------------------------------------------------
    # Options
    # --------------------------------------------------------------

    for question in questions:

        if len(question.options) != 4:

            errors.append(
                f"Part C 第 "
                f"{question.number} 题"
                f"选项数量错误："
                f"期望 4，实际 "
                f"{len(question.options)}"
            )

    return errors


# ======================================================================
# Part A
# ======================================================================

def build_part_a(
    questions: List[Question],
    female_voice: str,
) -> List[Segment]:

    segments: List[Segment] = []

    for question in questions:

        text_parts = [
            question.question
        ]

        for option in question.options:

            text_parts.append(
                option
            )

        full_text = " ".join(
            text_parts
        )

        segments.append(
            Segment(
                text=full_text,
                voice=female_voice,
                repeat=2,
            )
        )

    return segments


# ======================================================================
# Part B
# ======================================================================

def build_part_b(
    questions: List[Question],
    dialogue: List[Tuple[str, str]],
    male_voice: str,
    female_voice: str,
) -> List[Segment]:

    segments: List[Segment] = []

    # --------------------------------------------------------------
    # Dialogue
    # --------------------------------------------------------------

    if dialogue:

        for voice_type, text in dialogue:

            voice = (
                male_voice
                if voice_type == "male"
                else female_voice
            )

            segments.append(
                Segment(
                    text=text,
                    voice=voice,
                    repeat=1,
                )
            )

    else:

        # ----------------------------------------------------------
        # 没有 speaker 时，
        # 使用 question dialogue fallback。
        # ----------------------------------------------------------

        for question in questions:

            if question.dialogue:

                segments.append(
                    Segment(
                        text=question.dialogue,
                        voice=female_voice,
                        repeat=1,
                    )
                )

    # --------------------------------------------------------------
    # Questions + options
    # --------------------------------------------------------------

    for question in questions:

        segments.append(
            Segment(
                text=question.question,
                voice=female_voice,
                repeat=1,
            )
        )

        for option in question.options:

            segments.append(
                Segment(
                    text=option,
                    voice=female_voice,
                    repeat=1,
                )
            )

    return segments


# ======================================================================
# Part C
# ======================================================================

def build_part_c(
    passage: str,
    questions: List[Question],
    female_voice: str,
) -> List[Segment]:

    segments: List[Segment] = []

    # --------------------------------------------------------------
    # 1. Passage
    # --------------------------------------------------------------

    segments.append(
        Segment(
            text=passage,
            voice=female_voice,
            repeat=1,
        )
    )

    # --------------------------------------------------------------
    # 2. Questions
    #
    # 每题重复 2 次。
    # --------------------------------------------------------------

    for question in questions:

        segments.append(
            Segment(
                text=question.question,
                voice=female_voice,
                repeat=2,
            )
        )

        # ----------------------------------------------------------
        # 3. Options
        #
        # 每个选项重复 2 次。
        # ----------------------------------------------------------

        for option in question.options:

            segments.append(
                Segment(
                    text=option,
                    voice=female_voice,
                    repeat=2,
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

        raise

    return Kokoro


def synthesize_to_wav(
    kokoro,
    text: str,
    voice: str,
    speed: float,
    language: str,
    output_wav: Path,
):
    """
    使用官方 kokoro-onnx API 生成 WAV。

    注意：

        language 参数保留，用于兼容现有 Workflow。

        当前 kokoro-onnx 的稳定调用：

            kokoro.create(
                text,
                voice=voice,
                speed=speed,
            )

        不向 create() 传 lang 参数。
    """

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
    """
    WAV -> mp3/m4a/wav
    """

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
    """
    使用 ffmpeg 创建静音 WAV。
    """

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
    """
    使用 ffmpeg concat demuxer 合并 WAV。
    """

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
    """
    将 Segment 列表生成一个完整音频。
    """

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

            # ------------------------------------------------------
            # 同一句重复之间：
            #
            # 0.7 秒静音
            # ------------------------------------------------------

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

        # ----------------------------------------------------------
        # Segment 之间：
        #
        # 0.3 秒静音
        # ----------------------------------------------------------

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
            "Audio Generator V2.2.3"
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
        help="兼容现有 Workflow 的 language 参数",
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

    print(
        "=" * 70
    )

    print(
        "748686 英语学习系统"
    )

    print(
        "Audio Generator V2.2.3"
    )

    print(
        "=" * 70
    )

    print()

    print("CONFIG")

    print(
        f"  Date          : {date}"
    )

    print(
        f"  Exam          : {exam_file}"
    )

    print(
        f"  Answer        : {answer_file}"
    )

    print(
        f"  Format        : {args.audio_format}"
    )

    print(
        f"  Speed         : {args.speed}"
    )

    print(
        f"  Male voice    : {args.male_voice}"
    )

    print(
        f"  Female voice  : {args.female_voice}"
    )

    print(
        f"  Language      : {args.language}"
    )

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

    part_a_questions = parse_questions(
        exam_part_a
    )

    print(
        f"  Questions: "
        f"{len(part_a_questions)}"
    )

    for question in part_a_questions:

        print(
            f"  Q{question.number}: "
            f"{len(question.options)} options"
        )

    if len(part_a_questions) != 5:

        raise RuntimeError(
            "Part A 校验失败："
            f"期望 5 题，实际 "
            f"{len(part_a_questions)} 题"
        )

    for question in part_a_questions:

        if len(question.options) != 4:

            raise RuntimeError(
                f"Part A 第 "
                f"{question.number} 题"
                f"选项数量错误："
                f"{len(question.options)}"
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

    print(
        f"  Questions: "
        f"{len(part_b_questions)}"
    )

    # --------------------------------------------------------------
    # 首先尝试从试卷获取对话
    # --------------------------------------------------------------

    dialogue = extract_dialogue(
        exam_part_b
    )

    # --------------------------------------------------------------
    # 如果试卷没有对话：
    #
    # 从答案与解析 Part B 获取。
    # --------------------------------------------------------------

    if not dialogue:

        print(
            "  ⚠️ 试卷 Part B 没有找到对话"
        )

        dialogue = extract_dialogue(
            answer_part_b
        )

        if dialogue:

            print(
                "  ✓ 已从答案与解析补充 "
                "Part B 对话"
            )

            print(
                f"  ✓ Dialogue segments: "
                f"{len(dialogue)}"
            )

        else:

            print(
                "  ⚠️ 答案与解析 Part B "
                "也没有找到对话"
            )

    else:

        print(
            f"  ✓ Dialogue segments: "
            f"{len(dialogue)}"
        )

    if len(part_b_questions) != 5:

        raise RuntimeError(
            "Part B 校验失败："
            f"期望 5 题，实际 "
            f"{len(part_b_questions)} 题"
        )

    for question in part_b_questions:

        if len(question.options) != 4:

            raise RuntimeError(
                f"Part B 第 "
                f"{question.number} 题"
                f"选项数量错误："
                f"{len(question.options)}"
            )

    # ==================================================================
    # Recover Part C
    # ==================================================================

    print()
    print("=" * 70)
    print("PART C")
    print("=" * 70)

    # --------------------------------------------------------------
    # 题目和选项：
    #
    # 只从试卷获取
    # --------------------------------------------------------------

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

    # --------------------------------------------------------------
    # 原文：
    #
    # 只从答案与解析获取
    # --------------------------------------------------------------

    part_c_passage = (
        extract_part_c_passage_from_answer(
            answer_text
        )
    )

    print(
        f"  Passage from answer: "
        f"{len(part_c_passage)} chars"
    )

    # --------------------------------------------------------------
    # Part C 严格校验
    # --------------------------------------------------------------

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
    # Build Segments
    # ==================================================================

    segments_a = build_part_a(
        questions=part_a_questions,
        female_voice=args.female_voice,
    )

    segments_b = build_part_b(
        questions=part_b_questions,
        dialogue=dialogue,
        male_voice=args.male_voice,
        female_voice=args.female_voice,
    )

    segments_c = build_part_c(
        passage=part_c_passage,
        questions=part_c_questions,
        female_voice=args.female_voice,
    )

    print()
    print("=" * 70)
    print("AUDIO PLAN")
    print("=" * 70)

    print(
        f"  Listening A segments: "
        f"{len(segments_a)}"
    )

    print(
        f"  Listening B segments: "
        f"{len(segments_b)}"
    )

    print(
        f"  Listening C segments: "
        f"{len(segments_c)}"
    )

    # --------------------------------------------------------------
    # Part C：
    #
    # 1 passage
    # + 5 questions
    # + 20 options
    #
    # = 26 segments
    # --------------------------------------------------------------

    expected_part_c_segments = 26

    if (
        len(segments_c)
        != expected_part_c_segments
    ):

        raise RuntimeError(
            "Part C 音频片段数量错误："
            f"期望 "
            f"{expected_part_c_segments}，"
            f"实际 "
            f"{len(segments_c)}"
        )

    print(
        "  ✓ Part C segments = 26"
    )

    # ==================================================================
    # Output
    # ==================================================================

    output_dir = (
        exam_file.parent
    )

    listening_dir = (
        output_dir / "听力"
    )

    listening_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    suffix = (
        f".{args.audio_format}"
    )

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

    if not model_path.exists():

        raise FileNotFoundError(
            f"Kokoro 模型不存在："
            f"{model_path}"
        )

    if not voices_path.exists():

        raise FileNotFoundError(
            f"Kokoro voices 不存在："
            f"{voices_path}"
        )

    Kokoro = load_kokoro()

    kokoro = Kokoro(
        str(model_path),
        str(voices_path),
    )

    print(
        "  ✓ Kokoro 模型加载完成"
    )

    # ==================================================================
    # Voice Validation
    # ==================================================================

    print()
    print(
        "  → 正在检查本地 Kokoro voices"
    )

    available_voices = set(
        kokoro.get_voices()
    )

    print(
        f"  ✓ Available voices: "
        f"{len(available_voices)}"
    )

    print(
        f"  → Requested male voice: "
        f"{args.male_voice}"
    )

    print(
        f"  → Requested female voice: "
        f"{args.female_voice}"
    )

    if args.male_voice not in available_voices:

        raise RuntimeError(
            "Kokoro 男性 voice 不存在："
            f"{args.male_voice}\n"
            "当前本地 voices 中没有该 voice。"
        )

    if args.female_voice not in available_voices:

        raise RuntimeError(
            "Kokoro 女性 voice 不存在："
            f"{args.female_voice}\n"
            "当前本地 voices 中没有该 voice。"
        )

    print(
        f"  ✓ Male voice available: "
        f"{args.male_voice}"
    )

    print(
        f"  ✓ Female voice available: "
        f"{args.female_voice}"
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

    # --------------------------------------------------------------
    # 为保证不同格式都可以正确合并：
    #
    # 如果 A/B/C 是 mp3/m4a，
    # 这里重新从已有文件转换为 WAV。
    # --------------------------------------------------------------

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

        # ----------------------------------------------------------
        # A / B / C 之间增加 0.5 秒静音
        # ----------------------------------------------------------

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
            f"  ⚠️ 临时目录清理失败："
            f"{exc}"
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
    print(
        "Output directory:"
    )

    print(
        f"  {listening_dir}"
    )

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
