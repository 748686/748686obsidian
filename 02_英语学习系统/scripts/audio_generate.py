#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.2.2

======================================================================
职责
======================================================================

读取：

    1. 配套试卷
    2. 答案与解析

使用：

    Kokoro TTS

生成：

    Listening_A
    Listening_B
    Listening_C
    Listening_总音频

======================================================================
重要设计
======================================================================

Part A
    题目 + 选项来自试卷
    音频内容按照试卷生成

Part B
    题目 + 选项来自试卷
    对话优先来自试卷
    如果试卷没有对话，则从答案与解析补充

Part C
    题目 + 选项 ONLY 来自试卷
    听力原文 ONLY 来自答案与解析

    不使用答案字母推导题目
    不从答案分析文字猜题目
    不修改试卷
    不修改答案与解析

======================================================================
Part C 标准结构
======================================================================

答案与解析：

### Part C

I think healthy habits are important.
...

试卷：

## Part C

### 1. What does the speaker think is important?

- A. Eating sweet food
- B. Healthy habits
- C. Watching TV all day
- D. Sleeping for only two hours

...

最终：

    passage × 1

    question 1 × 2
    A × 2
    B × 2
    C × 2
    D × 2

    question 2 × 2
    ...

======================================================================
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


# ======================================================================
# 基础数据结构
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
    options: List[str] = field(default_factory=list)
    dialogue: List[Tuple[str, str]] = field(default_factory=list)


# ======================================================================
# 日志
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    print()
    print("=" * 70)
    print("ERROR")
    print("=" * 70)
    print(message)
    print("=" * 70)
    sys.exit(1)


# ======================================================================
# Markdown 清理
# ======================================================================

def clean_line(line: str) -> str:
    """
    清理 Markdown 格式，但保留正文。
    """

    line = line.strip()

    if not line:
        return ""

    # Markdown checkbox
    line = re.sub(r"^[-*+]\s+\[[ xX]\]\s*", "", line)

    # Markdown bullet
    line = re.sub(r"^[-*+]\s+", "", line)

    # Markdown heading
    line = re.sub(r"^#{1,6}\s*", "", line)

    # Bold / italic
    line = line.replace("**", "")
    line = line.replace("__", "")
    line = line.replace("*", "")
    line = line.replace("_", "")

    # Markdown blockquote
    line = re.sub(r"^>\s*", "", line)

    return line.strip()


# ======================================================================
# 标题判断
# ======================================================================

def normalize_header(line: str) -> str:
    line = clean_line(line)
    return re.sub(r"\s+", " ", line).strip().upper()


def is_part_header(line: str, part: str) -> bool:
    """
    判断一行是否为指定 Part 标题。

    支持：

        Part A
        PART A
        Listening A
        LISTENING A

        第一部分
        第二部分
        第三部分

        第一部分：听句子
        第二部分：听对话
        第三部分：听原文
    """

    cleaned = clean_line(line)
    normalized = normalize_header(line)

    part = part.upper()

    if part == "A":
        chinese_patterns = [
            r"^第一部分(?:\s*[:：-].*)?$",
        ]
        english_patterns = [
            r"^PART\s+A(?:\s*[:：-].*)?$",
            r"^LISTENING\s+A(?:\s*[:：-].*)?$",
        ]

    elif part == "B":
        chinese_patterns = [
            r"^第二部分(?:\s*[:：-].*)?$",
        ]
        english_patterns = [
            r"^PART\s+B(?:\s*[:：-].*)?$",
            r"^LISTENING\s+B(?:\s*[:：-].*)?$",
        ]

    elif part == "C":
        chinese_patterns = [
            r"^第三部分(?:\s*[:：-].*)?$",
        ]
        english_patterns = [
            r"^PART\s+C(?:\s*[:：-].*)?$",
            r"^LISTENING\s+C(?:\s*[:：-].*)?$",
        ]

    else:
        return False

    for pattern in chinese_patterns:
        if re.match(pattern, cleaned, flags=re.IGNORECASE):
            return True

    for pattern in english_patterns:
        if re.match(pattern, normalized, flags=re.IGNORECASE):
            return True

    return False


def find_part_start(lines: List[str], part: str) -> Optional[int]:
    for index, line in enumerate(lines):
        if is_part_header(line, part):
            return index

    return None


def find_next_part_start(
    lines: List[str],
    current_part: str,
    start_index: int,
) -> Optional[int]:
    """
    查找当前 Part 后面的下一个 Part。
    """

    order = ["A", "B", "C"]

    try:
        position = order.index(current_part.upper())
    except ValueError:
        return None

    next_parts = order[position + 1:]

    for index in range(start_index + 1, len(lines)):
        for next_part in next_parts:
            if is_part_header(lines[index], next_part):
                return index

    return None


def find_part_header(lines: List[str], part: str) -> Optional[int]:
    """
    V2.2.2：

    与 find_part_start() 使用完全一致的 Part 判断。

    修复旧版只识别：

        PART B
        PART C

    却无法识别：

        第二部分
        第三部分
    """

    return find_part_start(lines, part)


# ======================================================================
# Part 提取
# ======================================================================

def extract_part(
    text: str,
    part: str,
) -> str:
    """
    从一个 Markdown 文件中提取指定 Part。

    例如：

        extract_part(text, "C")

    只返回 Part C 内容，不包含 Part D / 其他大章节。
    """

    lines = text.splitlines()

    start = find_part_start(lines, part)

    if start is None:
        return ""

    end = find_next_part_start(
        lines,
        part,
        start,
    )

    if end is None:
        selected = lines[start + 1:]
    else:
        selected = lines[start + 1:end]

    return "\n".join(selected).strip()


# ======================================================================
# 题目解析
# ======================================================================

QUESTION_PATTERNS = [
    # 1. Question
    re.compile(
        r"^\s*(\d+)\s*[\.．、:：\-]\s*(.+?)\s*$"
    ),

    # 1) Question
    re.compile(
        r"^\s*(\d+)\s*\)\s*(.+?)\s*$"
    ),

    # 第1题 Question
    re.compile(
        r"^\s*第\s*(\d+)\s*题\s*[:：.\-]?\s*(.+?)\s*$"
    ),

    # Question 1: Question
    re.compile(
        r"^\s*Question\s+(\d+)\s*[:：.\-]\s*(.+?)\s*$",
        flags=re.IGNORECASE,
    ),
]


def parse_question_header(
    line: str,
) -> Tuple[Optional[int], Optional[str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None, None

    for pattern in QUESTION_PATTERNS:
        match = pattern.match(cleaned)

        if match:
            try:
                number = int(match.group(1))
            except ValueError:
                return None, None

            question = match.group(2).strip()

            if question:
                return number, question

    return None, None


# ======================================================================
# 选项解析
# ======================================================================

OPTION_PATTERN = re.compile(
    r"^\s*([A-Da-d])\s*(?:[\.．\)）:：、\-]\s*|\s+)(.+?)\s*$"
)


def parse_option(
    line: str,
) -> Tuple[Optional[str], Optional[str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None, None

    match = OPTION_PATTERN.match(cleaned)

    if not match:
        return None, None

    letter = match.group(1).upper()
    text = match.group(2).strip()

    if not text:
        return None, None

    return letter, text


# ======================================================================
# Speaker 解析
# ======================================================================

def parse_speaker(
    line: str,
) -> Tuple[Optional[str], Optional[str]]:

    cleaned = clean_line(line)

    if not cleaned:
        return None, None

    patterns = [
        # English
        (r"^(Male|Man)\s*[:：]\s*(.+)$", "male"),
        (r"^(Female|Woman)\s*[:：]\s*(.+)$", "female"),

        # Chinese
        (r"^(男声|男士|男)\s*[:：]\s*(.+)$", "male"),
        (r"^(女声|女士|女)\s*[:：]\s*(.+)$", "female"),

        # M: / F:
        (r"^M\s*[:：]\s*(.+)$", "male"),
        (r"^F\s*[:：]\s*(.+)$", "female"),
    ]

    for pattern, voice in patterns:
        match = re.match(
            pattern,
            cleaned,
            flags=re.IGNORECASE,
        )

        if match:

            if voice in ("male", "female"):
                text = match.group(2).strip()
            else:
                text = match.group(1).strip()

            if text:
                return voice, text

    return None, None


# ======================================================================
# Questions 解析
# ======================================================================

def parse_questions(
    text: str,
) -> List[Question]:

    lines = text.splitlines()

    questions: List[Question] = []

    current: Optional[Question] = None

    for raw in lines:

        line = clean_line(raw)

        if not line:
            continue

        # --------------------------------------------------------------
        # Question header
        # --------------------------------------------------------------

        number, question_text = parse_question_header(line)

        if number is not None:

            if current is not None:
                questions.append(current)

            current = Question(
                number=number,
                question=question_text or "",
            )

            continue

        # --------------------------------------------------------------
        # Option
        # --------------------------------------------------------------

        if current is not None:

            letter, option_text = parse_option(line)

            if letter is not None:

                # 防止同一个选项重复写入
                existing_letters = {
                    re.match(
                        r"^([A-D])\.",
                        option,
                    ).group(1)
                    for option in current.options
                    if re.match(
                        r"^([A-D])\.",
                        option,
                    )
                }

                if letter not in existing_letters:
                    current.options.append(
                        f"{letter}. {option_text}"
                    )

                continue

        # --------------------------------------------------------------
        # Speaker
        # --------------------------------------------------------------

        if current is not None:

            speaker, speech = parse_speaker(line)

            if speaker is not None:

                current.dialogue.append(
                    (speaker, speech)
                )

                continue

        # --------------------------------------------------------------
        # Continuation
        # --------------------------------------------------------------

        if current is not None:

            if current.dialogue:

                speaker, _ = current.dialogue[-1]

                current.dialogue.append(
                    (
                        speaker,
                        line,
                    )
                )

    if current is not None:
        questions.append(current)

    return questions


# ======================================================================
# 对话提取
# ======================================================================

def extract_dialogue(
    text: str,
) -> List[Tuple[str, str]]:

    lines = text.splitlines()

    dialogue: List[Tuple[str, str]] = []

    current_speaker: Optional[str] = None

    for raw in lines:

        line = clean_line(raw)

        if not line:
            continue

        speaker, speech = parse_speaker(line)

        if speaker is not None:

            current_speaker = speaker

            dialogue.append(
                (
                    speaker,
                    speech,
                )
            )

            continue

        if current_speaker is not None:

            dialogue.append(
                (
                    current_speaker,
                    line,
                )
            )

    return dialogue


# ======================================================================
# Dialogue 附着
# ======================================================================

def attach_dialogue(
    questions: List[Question],
    dialogue: List[Tuple[str, str]],
) -> None:

    if not questions or not dialogue:
        return

    # 如果只有一道题，则整段对话属于该题
    if len(questions) == 1:
        questions[0].dialogue = dialogue
        return

    # 如果题目已经存在 dialogue，则不覆盖
    if any(question.dialogue for question in questions):
        return

    # 保留旧版兼容逻辑：
    # 如果没有任何题目拥有 dialogue，
    # 则整段 dialogue 放到第一题。
    questions[0].dialogue = dialogue


# ======================================================================
# 听力原文提取
# ======================================================================

def extract_passage(
    text: str,
) -> str:

    lines = text.splitlines()

    passage: List[str] = []

    started = False

    for raw in lines:

        line = clean_line(raw)

        if not line:
            continue

        # --------------------------------------------------------------
        # Part C header
        # --------------------------------------------------------------

        if is_part_header(raw, "C"):

            started = True
            continue

        if not started:
            continue

        # --------------------------------------------------------------
        # 遇到下一个 Part
        # --------------------------------------------------------------

        if is_part_header(raw, "A") or is_part_header(raw, "B"):
            break

        # --------------------------------------------------------------
        # 遇到大章节
        #
        # 答案文件中的：
        #
        # ## 二、标准答案
        #
        # 不能继续被当成听力原文。
        # --------------------------------------------------------------

        if re.match(
            r"^(一|二|三|四|五|六|七)[、.．]",
            line,
        ):
            break

        if re.match(
            r"^(标准答案|答案与解析|答案|解析)$",
            line,
            flags=re.IGNORECASE,
        ):
            break

        # --------------------------------------------------------------
        # 遇到题目
        # --------------------------------------------------------------

        number, _ = parse_question_header(line)

        if number is not None:
            break

        # --------------------------------------------------------------
        # 遇到 Questions / 问题 / 选择题
        # --------------------------------------------------------------

        if re.match(
            r"^(QUESTIONS?|问题|选择题)\b",
            line,
            flags=re.IGNORECASE,
        ):
            break

        passage.append(line)

    return " ".join(passage).strip()


# ======================================================================
# Part C 专用原文提取
# ======================================================================

def extract_part_c_passage_from_answer(
    answer_text: str,
) -> str:
    """
    Part C 原文专用解析。

    重要：

        Part C 题目不从答案文件解析。

    这里只负责：

        答案与解析 → Part C passage
    """

    part_c = extract_part(
        answer_text,
        "C",
    )

    if not part_c:
        return ""

    return extract_passage(
        "Part C\n" + part_c
    )


# ======================================================================
# Part C 严格验证
# ======================================================================

def validate_part_c(
    passage: str,
    questions: List[Question],
) -> None:

    errors: List[str] = []

    # --------------------------------------------------------------
    # 原文
    # --------------------------------------------------------------

    if not passage.strip():
        errors.append(
            "Part C 听力原文为空"
        )

    # --------------------------------------------------------------
    # 题目数量
    # --------------------------------------------------------------

    if len(questions) != 5:

        errors.append(
            f"Part C 题目数量错误："
            f"期望 5，实际 {len(questions)}"
        )

    # --------------------------------------------------------------
    # 每题
    # --------------------------------------------------------------

    for expected_number in range(1, 6):

        matched = [
            question
            for question in questions
            if question.number == expected_number
        ]

        if not matched:

            errors.append(
                f"Part C 缺少第 {expected_number} 题"
            )

            continue

        question = matched[0]

        if not question.question.strip():

            errors.append(
                f"Part C 第 {expected_number} 题题干为空"
            )

        if len(question.options) != 4:

            errors.append(
                f"Part C 第 {expected_number} 题选项数量错误："
                f"期望 4，实际 {len(question.options)}"
            )

    # --------------------------------------------------------------
    # 重复题号
    # --------------------------------------------------------------

    numbers = [
        question.number
        for question in questions
    ]

    if len(numbers) != len(set(numbers)):

        errors.append(
            "Part C 存在重复题号"
        )

    # --------------------------------------------------------------
    # 报错
    # --------------------------------------------------------------

    if errors:

        message = (
            "Part C 校验失败：\n\n"
            + "\n".join(
                f"  ✗ {error}"
                for error in errors
            )
        )

        fail(message)


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
            text_parts.append(option)

        full_text = " ".join(text_parts).strip()

        if not full_text:
            continue

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
    female_voice: str,
    male_voice: str,
) -> List[Segment]:

    segments: List[Segment] = []

    # --------------------------------------------------------------
    # Dialogue
    # --------------------------------------------------------------

    dialogue: List[Tuple[str, str]] = []

    for question in questions:

        if question.dialogue:
            dialogue.extend(
                question.dialogue
            )

    # --------------------------------------------------------------
    # 第一遍 + 第二遍
    # --------------------------------------------------------------

    for _ in range(2):

        for speaker, text in dialogue:

            voice = (
                male_voice
                if speaker == "male"
                else female_voice
            )

            if text.strip():

                segments.append(
                    Segment(
                        text=text,
                        voice=voice,
                        repeat=1,
                    )
                )

    # --------------------------------------------------------------
    # Questions + options
    # --------------------------------------------------------------

    for question in questions:

        if question.question.strip():

            segments.append(
                Segment(
                    text=question.question,
                    voice=female_voice,
                    repeat=2,
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

    """
    Part C V2.2.2

    passage ×1

    每题：
        question ×2
        A ×2
        B ×2
        C ×2
        D ×2
    """

    segments: List[Segment] = []

    # --------------------------------------------------------------
    # Passage
    # --------------------------------------------------------------

    if passage.strip():

        segments.append(
            Segment(
                text=passage,
                voice=female_voice,
                repeat=1,
            )
        )

    # --------------------------------------------------------------
    # Questions
    # --------------------------------------------------------------

    for question in sorted(
        questions,
        key=lambda item: item.number,
    ):

        if question.question.strip():

            segments.append(
                Segment(
                    text=question.question,
                    voice=female_voice,
                    repeat=2,
                )
            )

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
# TTS 文本清理
# ======================================================================

def clean_text(text: str) -> str:

    text = text.strip()

    # Markdown
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")

    # 下划线
    text = text.replace("_", " ")

    # 多余空格
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ======================================================================
# Kokoro
# ======================================================================

def load_kokoro(
    model_path: Path,
    voices_path: Path,
):

    try:
        from kokoro_onnx import KModel
        from kokoro_onnx import KPipeline
    except Exception as exc:
        fail(
            "无法导入 kokoro_onnx：\n"
            f"{exc}"
        )

    try:

        model = KModel(
            str(model_path),
            str(voices_path),
        )

        pipeline = KPipeline(
            model=model,
            lang_code="a",
        )

        return pipeline

    except Exception as exc:

        fail(
            "Kokoro 初始化失败：\n"
            f"{exc}"
        )


# ======================================================================
# 音频生成
# ======================================================================

def synthesize_segment(
    pipeline,
    segment: Segment,
    speed: float,
    language: str,
    output_wav: Path,
) -> None:

    import soundfile as sf
    import numpy as np

    text = clean_text(
        segment.text
    )

    if not text:
        return

    audio_parts = []

    for repeat_index in range(
        segment.repeat
    ):

        try:

            samples = []

            for audio, sample_rate in pipeline.create(
                text,
                voice=segment.voice,
                speed=speed,
                lang=language,
            ):

                samples.append(
                    audio
                )

            if not samples:
                raise RuntimeError(
                    "Kokoro 没有返回音频数据"
                )

            audio_data = np.concatenate(
                samples
            )

            audio_parts.append(
                audio_data
            )

            # ----------------------------------------------------------
            # 两次重复之间 0.7 秒静音
            # ----------------------------------------------------------

            if (
                repeat_index
                < segment.repeat - 1
            ):

                silence = np.zeros(
                    int(
                        sample_rate
                        * 0.7
                    ),
                    dtype=np.float32,
                )

                audio_parts.append(
                    silence
                )

        except Exception as exc:

            fail(
                "Kokoro 生成失败：\n"
                f"文本：{text}\n"
                f"voice：{segment.voice}\n"
                f"错误：{exc}"
            )

    final_audio = np.concatenate(
        audio_parts
    )

    sf.write(
        str(output_wav),
        final_audio,
        sample_rate,
    )


# ======================================================================
# Part 音频生成
# ======================================================================

def render_segments(
    pipeline,
    segments: List[Segment],
    speed: float,
    language: str,
    output_wav: Path,
) -> None:

    if not segments:

        fail(
            f"没有可生成的音频内容：{output_wav}"
        )

    with tempfile.TemporaryDirectory(
        prefix="kokoro_segments_"
    ) as temp_dir:

        temp_path = Path(
            temp_dir
        )

        files: List[Path] = []

        for index, segment in enumerate(
            segments,
            start=1,
        ):

            clean_segment_text = clean_text(
                segment.text
            )

            if not clean_segment_text:
                continue

            segment_file = (
                temp_path
                / f"{index:04d}.wav"
            )

            log(
                f"      Segment "
                f"{index:04d} | "
                f"{segment.voice} | "
                f"repeat={segment.repeat}"
            )

            synthesize_segment(
                pipeline=pipeline,
                segment=segment,
                speed=speed,
                language=language,
                output_wav=segment_file,
            )

            files.append(
                segment_file
            )

        if not files:

            fail(
                f"没有生成任何音频片段：{output_wav}"
            )

        # --------------------------------------------------------------
        # ffmpeg concat
        # --------------------------------------------------------------

        concat_file = (
            temp_path
            / "concat.txt"
        )

        with concat_file.open(
            "w",
            encoding="utf-8",
        ) as handle:

            for file in files:

                handle.write(
                    f"file '{file.as_posix()}'\n"
                )

        try:

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
                    "-c:a",
                    "pcm_s16le",
                    str(output_wav),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        except subprocess.CalledProcessError as exc:

            fail(
                "ffmpeg 合并音频失败：\n"
                f"{exc.stderr}"
            )


# ======================================================================
# WAV → MP3 / M4A
# ======================================================================

def convert_audio(
    wav_file: Path,
    output_file: Path,
    audio_format: str,
) -> None:

    if audio_format == "wav":

        shutil.copy2(
            wav_file,
            output_file,
        )

        return

    if audio_format == "mp3":

        codec_args = [
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
        ]

    elif audio_format == "m4a":

        codec_args = [
            "-codec:a",
            "aac",
            "-b:a",
            "192k",
        ]

    else:

        fail(
            f"不支持的音频格式：{audio_format}"
        )

    try:

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(wav_file),
                *codec_args,
                str(output_file),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    except subprocess.CalledProcessError as exc:

        fail(
            "音频格式转换失败：\n"
            f"{exc.stderr}"
        )


# ======================================================================
# Part 文件生成
# ======================================================================

def generate_part_audio(
    pipeline,
    part_name: str,
    segments: List[Segment],
    output_dir: Path,
    audio_format: str,
    speed: float,
    language: str,
) -> Path:

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    final_file = (
        output_dir
        / f"Listening_{part_name}.{audio_format}"
    )

    with tempfile.TemporaryDirectory(
        prefix=f"audio_{part_name}_"
    ) as temp_dir:

        temp_wav = (
            Path(temp_dir)
            / f"Listening_{part_name}.wav"
        )

        log()
        log(
            f"▶️ 正在生成 Listening {part_name}"
        )

        render_segments(
            pipeline=pipeline,
            segments=segments,
            speed=speed,
            language=language,
            output_wav=temp_wav,
        )

        convert_audio(
            wav_file=temp_wav,
            output_file=final_file,
            audio_format=audio_format,
        )

    if not final_file.exists():
        fail(
            f"音频生成失败，文件不存在：{final_file}"
        )

    if final_file.stat().st_size <= 0:
        fail(
            f"音频文件为空：{final_file}"
        )

    log(
        f"✓ Listening {part_name}："
        f"{final_file}"
    )

    return final_file


# ======================================================================
# 总音频
# ======================================================================

def generate_total_audio(
    part_files: List[Path],
    output_file: Path,
) -> None:

    if not part_files:
        fail(
            "没有 Part 音频，无法生成总音频。"
        )

    with tempfile.TemporaryDirectory(
        prefix="total_audio_"
    ) as temp_dir:

        temp_path = Path(
            temp_dir
        )

        wav_files: List[Path] = []

        # --------------------------------------------------------------
        # 所有 Part 转 WAV
        # --------------------------------------------------------------

        for index, part_file in enumerate(
            part_files,
            start=1,
        ):

            wav_file = (
                temp_path
                / f"part_{index}.wav"
            )

            try:

                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        str(part_file),
                        "-codec:a",
                        "pcm_s16le",
                        str(wav_file),
                    ],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )

            except subprocess.CalledProcessError as exc:

                fail(
                    "总音频转换 WAV 失败：\n"
                    f"{exc.stderr}"
                )

            wav_files.append(
                wav_file
            )

        # --------------------------------------------------------------
        # concat
        # --------------------------------------------------------------

        concat_file = (
            temp_path
            / "concat.txt"
        )

        with concat_file.open(
            "w",
            encoding="utf-8",
        ) as handle:

            for wav_file in wav_files:

                handle.write(
                    f"file '{wav_file.as_posix()}'\n"
                )

        # --------------------------------------------------------------
        # 根据输出格式选择 codec
        # --------------------------------------------------------------

        suffix = output_file.suffix.lower()

        if suffix == ".mp3":

            codec_args = [
                "-codec:a",
                "libmp3lame",
                "-q:a",
                "2",
            ]

        elif suffix == ".m4a":

            codec_args = [
                "-codec:a",
                "aac",
                "-b:a",
                "192k",
            ]

        elif suffix == ".wav":

            codec_args = [
                "-codec:a",
                "pcm_s16le",
            ]

        else:

            fail(
                f"不支持的总音频格式：{suffix}"
            )

        try:

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
                    *codec_args,
                    str(output_file),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

        except subprocess.CalledProcessError as exc:

            fail(
                "总音频生成失败：\n"
                f"{exc.stderr}"
            )

    if not output_file.exists():
        fail(
            f"总音频文件不存在：{output_file}"
        )

    if output_file.stat().st_size <= 0:
        fail(
            f"总音频文件为空：{output_file}"
        )

    log(
        f"✓ Listening 总音频："
        f"{output_file}"
    )


# ======================================================================
# 参数
# ======================================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="748686 English Learning System - Audio Generator V2.2.2"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="业务日期 YYYY-MM-DD",
    )

    parser.add_argument(
        "--exam-file",
        required=True,
        help="配套试卷 Markdown 文件",
    )

    parser.add_argument(
        "--answer-file",
        required=True,
        help="答案与解析 Markdown 文件",
    )

    parser.add_argument(
        "--format",
        default="mp3",
        choices=[
            "mp3",
            "m4a",
            "wav",
        ],
        help="输出音频格式",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Kokoro 语速",
    )

    parser.add_argument(
        "--male-voice",
        default="am_adam",
        help="Kokoro 男声",
    )

    parser.add_argument(
        "--female-voice",
        default="af_sarah",
        help="Kokoro 女声",
    )

    parser.add_argument(
        "--language",
        default="en-us",
        help="Kokoro language",
    )

    return parser


# ======================================================================
# Main
# ======================================================================

def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    # ==================================================================
    # 路径
    # ==================================================================

    script_path = Path(__file__).resolve()

    # 脚本位于：
    #
    # 02_英语学习系统/...
    #
    # project_root：
    #
    # 02_英语学习系统
    #

    project_root = script_path.parents[1]

    model_path = (
        project_root
        / "models"
        / "kokoro"
        / "kokoro-v1.1-zh.fp16.onnx"
    )

    voices_path = (
        project_root
        / "models"
        / "kokoro"
        / "voices-v1.1-zh.bin"
    )

    exam_file = Path(
        args.exam_file
    ).resolve()

    answer_file = Path(
        args.answer_file
    ).resolve()

    # ==================================================================
    # 输出目录
    # ==================================================================

    output_dir = (
        project_root
        / "output"
        / args.date
        / "配套试卷"
        / "听力"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ==================================================================
    # 基础验证
    # ==================================================================

    log("=" * 70)
    log("748686 英语学习系统")
    log("Audio Generator V2.2.2")
    log("=" * 70)

    log()
    log("CONFIG")
    log(f"  Date          : {args.date}")
    log(f"  Exam          : {exam_file}")
    log(f"  Answer        : {answer_file}")
    log(f"  Format        : {args.format}")
    log(f"  Speed         : {args.speed}")
    log(f"  Male voice    : {args.male_voice}")
    log(f"  Female voice  : {args.female_voice}")
    log(f"  Language      : {args.language}")

    if not exam_file.exists():
        fail(
            f"试卷文件不存在：{exam_file}"
        )

    if not answer_file.exists():
        fail(
            f"答案与解析文件不存在：{answer_file}"
        )

    if not model_path.exists():
        fail(
            f"Kokoro model 不存在：{model_path}"
        )

    if not voices_path.exists():
        fail(
            f"Kokoro voices 不存在：{voices_path}"
        )

    # ==================================================================
    # 读取文件
    # ==================================================================

    try:

        exam_text = exam_file.read_text(
            encoding="utf-8"
        )

    except Exception as exc:

        fail(
            "读取试卷失败：\n"
            f"{exc}"
        )

    try:

        answer_text = answer_file.read_text(
            encoding="utf-8"
        )

    except Exception as exc:

        fail(
            "读取答案与解析失败：\n"
            f"{exc}"
        )

    # ==================================================================
    # Part A
    # ==================================================================

    log()
    log("=" * 70)
    log("PART A")
    log("=" * 70)

    exam_part_a = extract_part(
        exam_text,
        "A",
    )

    if not exam_part_a:

        fail(
            "试卷中没有找到 Part A。"
        )

    questions_a = parse_questions(
        exam_part_a
    )

    log(
        f"  Questions: {len(questions_a)}"
    )

    if not questions_a:

        fail(
            "Part A 没有解析到任何题目。"
        )

    for question in questions_a:

        log(
            f"  Q{question.number}: "
            f"{len(question.options)} options"
        )

    # ==================================================================
    # Part B
    # ==================================================================

    log()
    log("=" * 70)
    log("PART B")
    log("=" * 70)

    exam_part_b = extract_part(
        exam_text,
        "B",
    )

    if not exam_part_b:

        fail(
            "试卷中没有找到 Part B。"
        )

    questions_b = parse_questions(
        exam_part_b
    )

    log(
        f"  Questions: {len(questions_b)}"
    )

    # --------------------------------------------------------------
    # B dialogue
    # --------------------------------------------------------------

    dialogue_b = extract_dialogue(
        exam_part_b
    )

    if not dialogue_b:

        log(
            "  ⚠️ 试卷 Part B 没有找到对话"
        )

        answer_part_b = extract_part(
            answer_text,
            "B",
        )

        dialogue_b = extract_dialogue(
            answer_part_b
        )

        if dialogue_b:

            log(
                "  ✓ 已从答案与解析补充 Part B 对话"
            )

    attach_dialogue(
        questions_b,
        dialogue_b,
    )

    # ==================================================================
    # Part C
    # ==================================================================

    log()
    log("=" * 70)
    log("PART C")
    log("=" * 70)

    # ------------------------------------------------------------------
    # 1. 题目 + 选项
    #
    # ONLY 从 exam_file 读取
    # ------------------------------------------------------------------

    exam_part_c = extract_part(
        exam_text,
        "C",
    )

    if not exam_part_c:

        fail(
            "试卷中没有找到 Part C。"
        )

    questions_c = parse_questions(
        exam_part_c
    )

    log(
        f"  Questions from exam: "
        f"{len(questions_c)}"
    )

    # ------------------------------------------------------------------
    # 2. 原文
    #
    # ONLY 从 answer_file 读取
    # ------------------------------------------------------------------

    passage_c = extract_part_c_passage_from_answer(
        answer_text
    )

    log(
        f"  Passage from answer: "
        f"{len(passage_c)} chars"
    )

    # ------------------------------------------------------------------
    # 3. 严格验证
    # ------------------------------------------------------------------

    validate_part_c(
        passage=passage_c,
        questions=questions_c,
    )

    log(
        "  ✓ Part C validation passed"
    )

    for question in sorted(
        questions_c,
        key=lambda item: item.number,
    ):

        log(
            f"  Q{question.number}: "
            f"{len(question.options)} options"
        )

    # ==================================================================
    # 构建音频 Segment
    # ==================================================================

    log()
    log("=" * 70)
    log("BUILD AUDIO SEGMENTS")
    log("=" * 70)

    segments_a = build_part_a(
        questions=questions_a,
        female_voice=args.female_voice,
    )

    segments_b = build_part_b(
        questions=questions_b,
        female_voice=args.female_voice,
        male_voice=args.male_voice,
    )

    segments_c = build_part_c(
        passage=passage_c,
        questions=questions_c,
        female_voice=args.female_voice,
    )

    log(
        f"  Part A segments: {len(segments_a)}"
    )

    log(
        f"  Part B segments: {len(segments_b)}"
    )

    log(
        f"  Part C segments: {len(segments_c)}"
    )

    # ==================================================================
    # Kokoro
    # ==================================================================

    log()
    log("=" * 70)
    log("INITIALIZE KOKORO")
    log("=" * 70)

    pipeline = load_kokoro(
        model_path=model_path,
        voices_path=voices_path,
    )

    log(
        "✓ Kokoro initialized"
    )

    # ==================================================================
    # 生成 A
    # ==================================================================

    part_files: List[Path] = []

    part_a_file = generate_part_audio(
        pipeline=pipeline,
        part_name="A",
        segments=segments_a,
        output_dir=output_dir,
        audio_format=args.format,
        speed=args.speed,
        language=args.language,
    )

    part_files.append(
        part_a_file
    )

    # ==================================================================
    # 生成 B
    # ==================================================================

    part_b_file = generate_part_audio(
        pipeline=pipeline,
        part_name="B",
        segments=segments_b,
        output_dir=output_dir,
        audio_format=args.format,
        speed=args.speed,
        language=args.language,
    )

    part_files.append(
        part_b_file
    )

    # ==================================================================
    # 生成 C
    # ==================================================================

    part_c_file = generate_part_audio(
        pipeline=pipeline,
        part_name="C",
        segments=segments_c,
        output_dir=output_dir,
        audio_format=args.format,
        speed=args.speed,
        language=args.language,
    )

    part_files.append(
        part_c_file
    )

    # ==================================================================
    # 总音频
    # ==================================================================

    log()
    log("=" * 70)
    log("GENERATE TOTAL AUDIO")
    log("=" * 70)

    total_file = (
        output_dir
        / f"Listening_总音频.{args.format}"
    )

    generate_total_audio(
        part_files=part_files,
        output_file=total_file,
    )

    # ==================================================================
    # 最终验证
    # ==================================================================

    log()
    log("=" * 70)
    log("FINAL VALIDATION")
    log("=" * 70)

    expected_files = [
        part_a_file,
        part_b_file,
        part_c_file,
        total_file,
    ]

    for file in expected_files:

        if not file.exists():

            fail(
                f"缺少输出文件：{file}"
            )

        size = file.stat().st_size

        if size <= 0:

            fail(
                f"输出文件为空：{file}"
            )

        log(
            f"  ✓ {file.name} "
            f"({size:,} bytes)"
        )

    # ==================================================================
    # 完成
    # ==================================================================

    log()
    log("=" * 70)
    log("AUDIO GENERATION COMPLETE")
    log("=" * 70)

    log(
        f"Output directory:\n"
        f"  {output_dir}"
    )

    log()
    log("Generated:")

    for file in expected_files:
        log(
            f"  ✓ {file.name}"
        )

    log()


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":
    main()
