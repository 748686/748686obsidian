#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.1

======================================================================
核心职责
======================================================================

读取已经最终落盘的：

    1. 配套试卷
    2. 答案与解析

从中提取：

    Listening A
    Listening B
    Listening C

然后按照听力三大部分的真实规则生成音频。

======================================================================
LISTENING A
======================================================================

听句子。

规则：

    女声 af_sarah

    每道题：
        题目句子播放 2 遍
        A/B/C/D 选项正常播报

======================================================================
LISTENING B
======================================================================

听对话。

规则：

    Male   -> am_adam
    Female -> af_sarah

    对话完整播放 2 遍

    然后：
        A
        B
        C
        D

    选项使用女声播报。

======================================================================
LISTENING C
======================================================================

听原文。

规则：

    女声 af_sarah

    原文完整播放 1 遍

    然后每一道题：

        A × 2
        B × 2
        C × 2
        D × 2

======================================================================
重要原则
======================================================================

1. 本模块不调用 AI。

2. 本模块不修改试卷。

3. 本模块不修改答案与解析。

4. 音频文本来自最终落盘文件。

5. Part A / Part C 使用女声。

6. Part B 根据明确的 Male / Female 标签切换声音。

7. 不猜测 Speaker 1 / Speaker 2 的性别。

8. Part A 每题句子播放两遍。

9. Part B 每段对话播放两遍。

10. Part C 原文只播放一遍。

11. Part C 选项各播放两遍。

12. A/B/C 必须全部成功后，才生成总音频。

13. 不允许只生成部分总音频。

14. 总音频严格按照：

        A → B → C

    顺序合并。

======================================================================
默认 Kokoro
======================================================================

models/kokoro/kokoro-v1.1-zh.fp16.onnx
models/kokoro/voices-v1.1-zh.bin

======================================================================
默认声音
======================================================================

Male:
    am_adam

Female:
    af_sarah

======================================================================
输出
======================================================================

output/YYYY-MM-DD/配套试卷/听力/

    Listening_A.mp3
    Listening_B.mp3
    Listening_C.mp3
    Listening_总音频.mp3
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ======================================================================
# Paths
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = SCRIPT_DIR.parent

REPO_ROOT = PROJECT_ROOT.parent

DEFAULT_MODEL = (
    REPO_ROOT
    / "02_英语学习系统"
    / "models"
    / "kokoro"
    / "kokoro-v1.1-zh.fp16.onnx"
)

DEFAULT_VOICES = (
    REPO_ROOT
    / "02_英语学习系统"
    / "models"
    / "kokoro"
    / "voices-v1.1-zh.bin"
)


# ======================================================================
# Voice configuration
# ======================================================================

LANGUAGE = "en-us"

DEFAULT_MALE_VOICE = "am_adam"

DEFAULT_FEMALE_VOICE = "af_sarah"


# ======================================================================
# Utility
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    log("")
    log("=" * 70)
    log("❌ AUDIO GENERATION FAILED")
    log("=" * 70)
    log(message)
    log("=" * 70)
    raise RuntimeError(message)


def normalize_text(text: str) -> str:
    """
    清理 Markdown 格式，但尽量保持正文内容。
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"__(.*?)__",
        r"\1",
        text,
    )

    text = re.sub(
        r"`(.*?)`",
        r"\1",
        text,
    )

    text = re.sub(
        r"^\s*[-*+]\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def clean_line(line: str) -> str:
    return normalize_text(line).strip()


# ======================================================================
# Speaker recognition
# ======================================================================

MALE_LABELS = {
    "male",
    "man",
    "boy",
    "gentleman",
    "male speaker",
    "man speaker",
    "speaker male",
    "speaker man",
}

FEMALE_LABELS = {
    "female",
    "woman",
    "girl",
    "lady",
    "female speaker",
    "woman speaker",
    "speaker female",
    "speaker woman",
}


def clean_speaker_label(label: str) -> str:

    value = label.strip().lower()

    value = value.rstrip(":：")

    value = re.sub(
        r"[*_`#]",
        "",
        value,
    )

    return value.strip()


def speaker_from_label(
    label: str,
) -> Optional[str]:

    value = clean_speaker_label(label)

    if value in MALE_LABELS:
        return "male"

    if value in FEMALE_LABELS:
        return "female"

    return None


SPEAKER_LINE_PATTERN = re.compile(
    r"^\s*"
    r"(?:\*\*|__|`)?"
    r"(?P<label>"
    r"Male|Man|Boy|Gentleman|"
    r"Female|Woman|Girl|Lady"
    r")"
    r"(?:\*\*|__|`)?"
    r"\s*[:：]\s*"
    r"(?P<text>.*?)"
    r"\s*$",
    re.IGNORECASE,
)


# ======================================================================
# Section extraction
# ======================================================================

SECTION_PATTERNS = {
    "A": [
        r"(?im)^\s{0,3}#{0,6}\s*(?:listening\s*)?(?:part\s*)?a\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*听力\s*(?:部分\s*)?A\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Section\s*A\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Part\s*A\s*:?\s*$",
    ],
    "B": [
        r"(?im)^\s{0,3}#{0,6}\s*(?:listening\s*)?(?:part\s*)?b\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*听力\s*(?:部分\s*)?B\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Section\s*B\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Part\s*B\s*:?\s*$",
    ],
    "C": [
        r"(?im)^\s{0,3}#{0,6}\s*(?:listening\s*)?(?:part\s*)?c\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*听力\s*(?:部分\s*)?C\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Section\s*C\s*:?\s*$",
        r"(?im)^\s{0,3}#{0,6}\s*Part\s*C\s*:?\s*$",
    ],
}


def find_section(
    text: str,
    section: str,
) -> Optional[Tuple[int, int]]:

    matches = []

    for pattern in SECTION_PATTERNS[section]:

        match = re.search(
            pattern,
            text,
        )

        if match:
            matches.append(match)

    if not matches:
        return None

    start_match = min(
        matches,
        key=lambda x: x.start(),
    )

    start = start_match.end()

    next_positions = []

    for other in ("A", "B", "C"):

        if other == section:
            continue

        for pattern in SECTION_PATTERNS[other]:

            match = re.search(
                pattern,
                text[start:],
            )

            if match:

                next_positions.append(
                    start + match.start()
                )

    if next_positions:
        end = min(next_positions)
    else:
        end = len(text)

    return start, end


def extract_sections(
    text: str,
) -> Dict[str, str]:

    result: Dict[str, str] = {}

    for section in ("A", "B", "C"):

        location = find_section(
            text,
            section,
        )

        if location is None:
            continue

        start, end = location

        content = normalize_text(
            text[start:end]
        )

        if content:
            result[section] = content

    return result


# ======================================================================
# Source loading
# ======================================================================

TRANSCRIPT_HEADING_PATTERNS = [
    r"(?im)^\s{0,3}#{0,6}\s*(?:听力原文|听力原稿|听力文本)\s*:?\s*$",
    r"(?im)^\s{0,3}#{0,6}\s*(?:transcript|audio\s*script|listening\s*script)\s*:?\s*$",
]


def extract_transcript_block(
    text: str,
) -> Optional[str]:

    for pattern in TRANSCRIPT_HEADING_PATTERNS:

        match = re.search(
            pattern,
            text,
        )

        if not match:
            continue

        start = match.end()

        next_heading = re.search(
            r"(?im)^\s{0,3}#{1,6}\s+.+$",
            text[start:],
        )

        if next_heading:

            end = (
                start
                + next_heading.start()
            )

        else:

            end = len(text)

        block = normalize_text(
            text[start:end]
        )

        if block:
            return block

    return None


def load_source_text(
    exam_file: Path,
    answer_file: Optional[Path],
) -> Tuple[
    Dict[str, str],
    Dict[str, str],
    str,
]:

    exam_text = exam_file.read_text(
        encoding="utf-8"
    )

    exam_sections = extract_sections(
        exam_text
    )

    answer_sections: Dict[str, str] = {}

    if answer_file and answer_file.exists():

        answer_text = answer_file.read_text(
            encoding="utf-8"
        )

        answer_sections = extract_sections(
            answer_text
        )

        transcript = extract_transcript_block(
            answer_text
        )

        if transcript:

            transcript_sections = extract_sections(
                transcript
            )

            for section, content in transcript_sections.items():

                if section not in answer_sections:
                    answer_sections[section] = content

    if not exam_sections and not answer_sections:

        fail(
            "最终试卷和答案与解析中都没有找到 "
            "Listening A / B / C。"
        )

    return (
        exam_sections,
        answer_sections,
        "exam+answer",
    )


# ======================================================================
# Question / option parsing
# ======================================================================

QUESTION_PATTERN = re.compile(
    r"^\s*"
    r"(?:"
    r"(?:Question|Q)\s*)?"
    r"(?P<number>\d+)"
    r"\s*"
    r"[.)、:：-]"
    r"\s*"
    r"(?P<text>.*)"
    r"$",
    re.IGNORECASE,
)


OPTION_PATTERN = re.compile(
    r"^\s*"
    r"(?P<label>[A-Da-d])"
    r"\s*"
    r"[.)、:：]\s*"
    r"(?P<text>.+?)"
    r"\s*$",
)


def strip_question_number(
    line: str,
) -> str:

    match = QUESTION_PATTERN.match(line)

    if match:

        return (
            match.group("text")
            or ""
        ).strip()

    return line.strip()


def parse_questions_and_options(
    text: str,
) -> List[Tuple[str, List[str]]]:
    """
    从一个 Part 中提取：

        question
        A
        B
        C
        D

    返回：

        [
            (
                "question text",
                ["A text", "B text", "C text", "D text"]
            )
        ]
    """

    lines = [
        clean_line(line)
        for line in text.splitlines()
    ]

    lines = [
        line
        for line in lines
        if line
    ]

    questions: List[
        Tuple[str, List[str]]
    ] = []

    current_question: Optional[str] = None

    current_options: Dict[
        str,
        str,
    ] = {}

    current_option: Optional[str] = None

    def flush() -> None:

        nonlocal current_question
        nonlocal current_options
        nonlocal current_option

        if (
            current_question
            and all(
                label in current_options
                for label in ("A", "B", "C", "D")
            )
        ):

            questions.append(
                (
                    current_question,
                    [
                        current_options["A"],
                        current_options["B"],
                        current_options["C"],
                        current_options["D"],
                    ],
                )
            )

        current_question = None
        current_options = {}
        current_option = None

    for line in lines:

        question_match = QUESTION_PATTERN.match(
            line
        )

        if question_match:

            flush()

            current_question = (
                question_match.group("text")
                or ""
            ).strip()

            continue

        option_match = OPTION_PATTERN.match(
            line
        )

        if option_match and current_question:

            label = (
                option_match.group("label")
                .upper()
            )

            current_options[label] = (
                option_match.group("text").strip()
            )

            current_option = label

            continue

        if current_option:

            current_options[current_option] += (
                " " + line
            )

        elif current_question:

            current_question += (
                " " + line
            )

    flush()

    return questions


# ======================================================================
# Dialogue parsing
# ======================================================================

def parse_dialogue(
    text: str,
) -> List[Tuple[str, str]]:

    lines = text.splitlines()

    dialogue: List[
        Tuple[str, str]
    ] = []

    current_speaker: Optional[str] = None

    current_text: List[str] = []

    def flush_current() -> None:

        nonlocal current_speaker
        nonlocal current_text

        if current_speaker is None:
            return

        body = " ".join(
            part.strip()
            for part in current_text
            if part.strip()
        ).strip()

        if body:

            dialogue.append(
                (
                    current_speaker,
                    body,
                )
            )

        current_speaker = None

        current_text = []

    for raw_line in lines:

        line = clean_line(raw_line)

        if not line:
            continue

        match = SPEAKER_LINE_PATTERN.match(
            line
        )

        if match:

            flush_current()

            label = match.group("label")

            speaker = speaker_from_label(
                label
            )

            if speaker is None:

                fail(
                    f"无法识别角色：{label}"
                )

            current_speaker = speaker

            current_text = [
                match.group("text").strip()
            ]

            continue

        if current_speaker is not None:

            # 遇到明显选项后结束对话
            if OPTION_PATTERN.match(line):
                flush_current()
                continue

            # 遇到下一道题也结束
            if QUESTION_PATTERN.match(line):
                flush_current()
                continue

            current_text.append(line)

    flush_current()

    return dialogue


# ======================================================================
# Audio segment
# ======================================================================

AudioSegment = Tuple[
    str,
    str,
    int,
]


# ======================================================================
# Part A builder
# ======================================================================

def build_part_a_segments(
    text: str,
) -> List[AudioSegment]:

    questions = parse_questions_and_options(
        text
    )

    if not questions:

        fail(
            "Listening A 无法解析题目。"
            "没有找到完整的 Question + A/B/C/D。"
        )

    segments: List[AudioSegment] = []

    log("")
    log(
        f"Part A 解析到 {len(questions)} 题"
    )

    for index, (
        question,
        options,
    ) in enumerate(
        questions,
        start=1,
    ):

        log(
            f"  A-{index:02d}: "
            f"句子 × 2"
        )

        segments.append(
            (
                "female",
                question,
                2,
            )
        )

        for option_index, option in enumerate(
            options,
            start=0,
        ):

            label = chr(
                ord("A") + option_index
            )

            segments.append(
                (
                    "female",
                    f"{label}. {option}",
                    1,
                )
            )

    return segments


# ======================================================================
# Part B builder
# ======================================================================

def split_part_b_questions(
    text: str,
) -> List[str]:

    lines = [
        clean_line(line)
        for line in text.splitlines()
    ]

    questions: List[str] = []

    current: List[str] = []

    for line in lines:

        if not line:
            continue

        if QUESTION_PATTERN.match(line):

            if current:

                questions.append(
                    "\n".join(current)
                )

            current = [line]

        else:

            current.append(line)

    if current:

        questions.append(
            "\n".join(current)
        )

    return questions


def build_part_b_segments(
    text: str,
) -> List[AudioSegment]:

    blocks = split_part_b_questions(
        text
    )

    if not blocks:

        fail(
            "Listening B 无法解析题目。"
        )

    segments: List[AudioSegment] = []

    valid_question_count = 0

    for block_index, block in enumerate(
        blocks,
        start=1,
    ):

        dialogue = parse_dialogue(
            block
        )

        if not dialogue:
            continue

        options_questions = (
            parse_questions_and_options(
                block
            )
        )

        if not options_questions:
            continue

        question, options = (
            options_questions[0]
        )

        valid_question_count += 1

        log("")
        log(
            f"  B-{valid_question_count:02d}: "
            f"对话 × 2"
        )

        # --------------------------------------------------------------
        # Dialogue first pass
        # --------------------------------------------------------------

        for speaker, speech in dialogue:

            segments.append(
                (
                    speaker,
                    speech,
                    2,
                )
            )

        # --------------------------------------------------------------
        # Options
        # --------------------------------------------------------------

        for option_index, option in enumerate(
            options,
            start=0,
        ):

            label = chr(
                ord("A") + option_index
            )

            segments.append(
                (
                    "female",
                    f"{label}. {option}",
                    1,
                )
            )

    if valid_question_count == 0:

        fail(
            "Listening B 没有识别到有效的 "
            "Male/Female 对话题目。"
        )

    return segments


# ======================================================================
# Part C builder
# ======================================================================

def extract_part_c_passage(
    text: str,
) -> Optional[str]:

    lines = [
        clean_line(line)
        for line in text.splitlines()
    ]

    passage_lines: List[str] = []

    for line in lines:

        if not line:
            continue

        if QUESTION_PATTERN.match(line):
            break

        if OPTION_PATTERN.match(line):
            break

        # 去掉明显说明性文字
        if re.match(
            r"^(?:questions?|请听|听下面|根据短文)",
            line,
            re.IGNORECASE,
        ):
            continue

        passage_lines.append(line)

    if not passage_lines:
        return None

    return " ".join(
        passage_lines
    ).strip()


def build_part_c_segments(
    text: str,
) -> List[AudioSegment]:

    passage = extract_part_c_passage(
        text
    )

    questions = parse_questions_and_options(
        text
    )

    if not passage:

        fail(
            "Listening C 无法找到听力原文。"
        )

    if not questions:

        fail(
            "Listening C 无法找到完整题目。"
        )

    segments: List[AudioSegment] = []

    log("")
    log(
        f"Part C 文章：1 遍"
    )

    segments.append(
        (
            "female",
            passage,
            1,
        )
    )

    log(
        f"Part C 解析到 {len(questions)} 题"
    )

    for index, (
        question,
        options,
    ) in enumerate(
        questions,
        start=1,
    ):

        # --------------------------------------------------------------
        # Part C 题目本身不作为文章朗读。
        # 用户要求的是选项各读两遍。
        # --------------------------------------------------------------

        log(
            f"  C-{index:02d}: "
            f"选项 A/B/C/D 各 × 2"
        )

        for option_index, option in enumerate(
            options,
            start=0,
        ):

            label = chr(
                ord("A") + option_index
            )

            segments.append(
                (
                    "female",
                    f"{label}. {option}",
                    2,
                )
            )

    return segments


# ======================================================================
# Build complete section
# ======================================================================

def build_audio_segments(
    section: str,
    text: str,
) -> List[AudioSegment]:

    if section == "A":

        return build_part_a_segments(
            text
        )

    if section == "B":

        return build_part_b_segments(
            text
        )

    if section == "C":

        return build_part_c_segments(
            text
        )

    fail(
        f"未知 Listening Section：{section}"
    )

    return []


# ======================================================================
# Kokoro
# ======================================================================

def load_kokoro(
    model_path: Path,
    voices_path: Path,
):

    if not model_path.exists():

        fail(
            f"Kokoro 模型不存在：\n{model_path}"
        )

    if not voices_path.exists():

        fail(
            f"Kokoro voices 不存在：\n{voices_path}"
        )

    try:

        from kokoro_onnx import Kokoro

    except ImportError as exc:

        fail(
            "无法导入 kokoro_onnx。\n"
            "请确认 requirements.txt 已安装 kokoro-onnx。"
        )

        raise exc

    log("")
    log("加载 Kokoro：")
    log(
        f"  model  : {model_path}"
    )
    log(
        f"  voices : {voices_path}"
    )

    return Kokoro(
        str(model_path),
        str(voices_path),
    )


# ======================================================================
# Synthesis
# ======================================================================

def synthesize_segments(
    kokoro,
    segments: List[AudioSegment],
    output_wav: Path,
    speed: float,
    male_voice: str,
    female_voice: str,
) -> None:

    try:

        import numpy as np
        import soundfile as sf

    except ImportError as exc:

        fail(
            "缺少 numpy 或 soundfile。\n"
            "请确认 requirements.txt 已安装。"
        )

        raise exc

    if not segments:

        fail(
            f"没有可生成的音频片段：{output_wav}"
        )

    audio_chunks = []

    sample_rate: Optional[int] = None

    log("")
    log(
        f"开始生成：{output_wav.name}"
    )

    segment_number = 0

    for speaker, text, repeat_count in segments:

        if speaker == "male":

            voice = male_voice

        elif speaker == "female":

            voice = female_voice

        else:

            fail(
                f"未知 speaker：{speaker}"
            )

        for repeat_index in range(
            repeat_count
        ):

            segment_number += 1

            log(
                f"  [{segment_number:03d}] "
                f"{speaker} / {voice} "
                f"第 {repeat_index + 1}/{repeat_count} 遍"
            )

            log(
                f"        {text}"
            )

            try:

                samples, rate = kokoro.create(
                    text,
                    voice=voice,
                    speed=speed,
                    lang=LANGUAGE,
                )

            except Exception as exc:

                fail(
                    "Kokoro 生成失败。\n"
                    f"speaker={speaker}\n"
                    f"voice={voice}\n"
                    f"text={text}\n"
                    f"error={exc}"
                )

            if samples is None:

                fail(
                    f"Kokoro 返回空音频：{text}"
                )

            samples = np.asarray(
                samples,
                dtype=np.float32,
            )

            if samples.size == 0:

                fail(
                    f"Kokoro 返回空音频：{text}"
                )

            if sample_rate is None:

                sample_rate = int(rate)

            elif int(rate) != sample_rate:

                fail(
                    "不同句子的采样率不一致："
                    f"{sample_rate} vs {rate}"
                )

            audio_chunks.append(
                samples
            )

            # ----------------------------------------------------------
            # 同一题不同句子之间短暂停顿
            # ----------------------------------------------------------

            pause_seconds = 0.22

            pause = np.zeros(
                int(
                    sample_rate
                    * pause_seconds
                ),
                dtype=np.float32,
            )

            audio_chunks.append(
                pause
            )

    if not audio_chunks:

        fail(
            f"没有生成任何音频：{output_wav}"
        )

    combined = np.concatenate(
        audio_chunks
    )

    output_wav.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sf.write(
        str(output_wav),
        combined,
        sample_rate,
        subtype="PCM_16",
    )

    if not output_wav.exists():

        fail(
            f"WAV 输出失败：{output_wav}"
        )

    if output_wav.stat().st_size <= 0:

        fail(
            f"WAV 文件为空：{output_wav}"
        )

    log(
        f"✓ 生成完成：{output_wav}"
    )


# ======================================================================
# FFmpeg
# ======================================================================

def require_ffmpeg() -> str:

    ffmpeg = shutil.which(
        "ffmpeg"
    )

    if not ffmpeg:

        fail(
            "系统中没有找到 ffmpeg。\n"
            "mp3 / m4a 输出需要 FFmpeg。"
        )

    return ffmpeg


def convert_wav(
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

    ffmpeg = require_ffmpeg()

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if audio_format == "mp3":

        command = [
            ffmpeg,
            "-y",
            "-i",
            str(wav_file),
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
            str(output_file),
        ]

    elif audio_format == "m4a":

        command = [
            ffmpeg,
            "-y",
            "-i",
            str(wav_file),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output_file),
        ]

    else:

        fail(
            f"不支持的音频格式：{audio_format}"
        )

    log("")
    log(
        "FFmpeg："
        + " ".join(command)
    )

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if result.returncode != 0:

        log(result.stdout)

        fail(
            f"FFmpeg 转换失败：{output_file}"
        )

    if not output_file.exists():

        fail(
            f"音频输出不存在：{output_file}"
        )

    if output_file.stat().st_size <= 0:

        fail(
            f"音频文件为空：{output_file}"
        )

    log(
        f"✓ 输出：{output_file}"
    )


# ======================================================================
# Merge A / B / C
# ======================================================================

def merge_audio_files(
    audio_files: List[Path],
    output_file: Path,
    audio_format: str,
) -> None:

    if len(audio_files) != 3:

        fail(
            "总音频必须由 A / B / C 三个部分组成。"
        )

    for file in audio_files:

        if not file.exists():

            fail(
                f"无法合并，文件不存在：{file}"
            )

        if file.stat().st_size <= 0:

            fail(
                f"无法合并，文件为空：{file}"
            )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    log("")
    log("=" * 70)
    log("合并 Listening 总音频")
    log("=" * 70)

    log("严格顺序：")

    for file in audio_files:

        log(
            f"  {file.name}"
        )

    if audio_format == "wav":

        try:

            import numpy as np
            import soundfile as sf

        except ImportError as exc:

            fail(
                "缺少 numpy / soundfile。"
            )

            raise exc

        arrays = []

        sample_rate: Optional[int] = None

        for file in audio_files:

            data, rate = sf.read(
                str(file),
                dtype="float32",
            )

            if sample_rate is None:

                sample_rate = rate

            elif rate != sample_rate:

                fail(
                    "A/B/C WAV 采样率不一致。"
                )

            arrays.append(data)

        merged = np.concatenate(
            arrays,
            axis=0,
        )

        sf.write(
            str(output_file),
            merged,
            sample_rate,
            subtype="PCM_16",
        )

    else:

        ffmpeg = require_ffmpeg()

        with tempfile.TemporaryDirectory() as temp_dir:

            concat_file = (
                Path(temp_dir)
                / "concat.txt"
            )

            lines = []

            for file in audio_files:

                absolute_path = (
                    file.resolve()
                    .as_posix()
                )

                escaped = (
                    absolute_path
                    .replace(
                        "'",
                        "'\\''",
                    )
                )

                lines.append(
                    f"file '{escaped}'"
                )

            concat_file.write_text(
                "\n".join(lines)
                + "\n",
                encoding="utf-8",
            )

            command = [
                ffmpeg,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_file),
            ]

            log(
                "执行："
                + " ".join(command)
            )

            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            if result.returncode != 0:

                log(result.stdout)

                fail(
                    "Listening 总音频合并失败。"
                )

    if not output_file.exists():

        fail(
            f"总音频不存在：{output_file}"
        )

    if output_file.stat().st_size <= 0:

        fail(
            f"总音频为空：{output_file}"
        )

    log(
        f"✓ 总音频完成：{output_file}"
    )


# ======================================================================
# Main
# ======================================================================

def main() -> int:

    parser = argparse.ArgumentParser(
        description=(
            "748686 英语学习系统 "
            "Listening Audio Generator V2.1"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--exam-file",
        required=True,
    )

    parser.add_argument(
        "--answer-file",
        required=False,
        default="",
    )

    parser.add_argument(
        "--audio-format",
        choices=[
            "mp3",
            "m4a",
            "wav",
        ],
        default="mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        choices=[
            0.75,
            0.9,
            1.0,
            1.1,
            1.25,
        ],
        default=1.0,
    )

    parser.add_argument(
        "--voice-male",
        default=DEFAULT_MALE_VOICE,
    )

    parser.add_argument(
        "--voice-female",
        default=DEFAULT_FEMALE_VOICE,
    )

    parser.add_argument(
        "--model",
        default=str(DEFAULT_MODEL),
    )

    parser.add_argument(
        "--voices",
        default=str(DEFAULT_VOICES),
    )

    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    exam_file = Path(
        args.exam_file
    ).resolve()

    answer_file = (
        Path(
            args.answer_file
        ).resolve()
        if args.answer_file
        else None
    )

    model_path = Path(
        args.model
    ).resolve()

    voices_path = Path(
        args.voices
    ).resolve()

    output_dir = (
        PROJECT_ROOT
        / "output"
        / args.date
        / "配套试卷"
        / "听力"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    log("")
    log("=" * 70)
    log("748686 英语学习系统")
    log("Audio Generator V2.1")
    log("=" * 70)

    log(
        f"DATE        : {args.date}"
    )

    log(
        f"FORMAT      : {args.audio_format}"
    )

    log(
        f"SPEED       : {args.speed}"
    )

    log(
        f"LANGUAGE    : {LANGUAGE}"
    )

    log(
        f"MALE VOICE  : {args.voice_male}"
    )

    log(
        f"FEMALE VOICE: {args.voice_female}"
    )

    log(
        f"EXAM        : {exam_file}"
    )

    log(
        f"ANSWER      : {answer_file}"
    )

    log(
        f"OUTPUT      : {output_dir}"
    )

    # ------------------------------------------------------------------
    # Validate source
    # ------------------------------------------------------------------

    if not exam_file.exists():

        fail(
            f"试卷不存在：\n{exam_file}"
        )

    if exam_file.stat().st_size <= 0:

        fail(
            f"试卷为空：\n{exam_file}"
        )

    if answer_file:

        if not answer_file.exists():

            log(
                "⚠️ 答案与解析不存在，"
                "将只使用试卷。"
            )

    # ------------------------------------------------------------------
    # Load sections
    # ------------------------------------------------------------------

    (
        exam_sections,
        answer_sections,
        _,
    ) = load_source_text(
        exam_file,
        answer_file,
    )

    # ------------------------------------------------------------------
    # Select source for each section
    #
    # Exam is preferred for question/options.
    # Answer is used when it contains a richer final transcript.
    # ------------------------------------------------------------------

    sections: Dict[str, str] = {}

    for section in ("A", "B", "C"):

        if section in exam_sections:

            sections[section] = (
                exam_sections[section]
            )

        elif section in answer_sections:

            sections[section] = (
                answer_sections[section]
            )

    for section in ("A", "B", "C"):

        if section not in sections:

            fail(
                f"Listening {section} 缺失。"
            )

        if not sections[section].strip():

            fail(
                f"Listening {section} 内容为空。"
            )

        log("")
        log(
            f"✓ Listening {section}"
            f"  文本长度："
            f"{len(sections[section])}"
        )

    # ------------------------------------------------------------------
    # Load Kokoro
    # ------------------------------------------------------------------

    kokoro = load_kokoro(
        model_path,
        voices_path,
    )

    # ------------------------------------------------------------------
    # Generate A / B / C
    # ------------------------------------------------------------------

    generated_files: List[Path] = []

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_root = Path(
            temp_dir
        )

        for section in (
            "A",
            "B",
            "C",
        ):

            log("")
            log("=" * 70)
            log(
                f"LISTENING {section}"
            )
            log("=" * 70)

            segments = build_audio_segments(
                section,
                sections[section],
            )

            if not segments:

                fail(
                    f"Listening {section} "
                    "没有生成有效音频结构。"
                )

            temp_wav = (
                temp_root
                / f"Listening_{section}.wav"
            )

            final_file = (
                output_dir
                / (
                    f"Listening_{section}."
                    f"{args.audio_format}"
                )
            )

            synthesize_segments(
                kokoro=kokoro,
                segments=segments,
                output_wav=temp_wav,
                speed=args.speed,
                male_voice=args.voice_male,
                female_voice=args.voice_female,
            )

            convert_wav(
                wav_file=temp_wav,
                output_file=final_file,
                audio_format=args.audio_format,
            )

            generated_files.append(
                final_file
            )

    # ------------------------------------------------------------------
    # IMPORTANT
    #
    # Only after A/B/C all succeed,
    # generate total audio.
    # ------------------------------------------------------------------

    log("")
    log("=" * 70)
    log("A / B / C 全部生成成功")
    log("=" * 70)

    total_file = (
        output_dir
        / (
            "Listening_总音频."
            f"{args.audio_format}"
        )
    )

    merge_audio_files(
        audio_files=generated_files,
        output_file=total_file,
        audio_format=args.audio_format,
    )

    # ------------------------------------------------------------------
    # Final validation
    # ------------------------------------------------------------------

    log("")
    log("=" * 70)
    log("AUDIO FINAL VALIDATION")
    log("=" * 70)

    expected_files = [
        output_dir
        / (
            f"Listening_A."
            f"{args.audio_format}"
        ),

        output_dir
        / (
            f"Listening_B."
            f"{args.audio_format}"
        ),

        output_dir
        / (
            f"Listening_C."
            f"{args.audio_format}"
        ),

        output_dir
        / (
            "Listening_总音频."
            f"{args.audio_format}"
        ),
    ]

    for file in expected_files:

        if not file.exists():

            fail(
                f"音频文件缺失：{file}"
            )

        if file.stat().st_size <= 0:

            fail(
                f"音频文件为空：{file}"
            )

        log(
            f"✓ {file.name}"
            f"  ({file.stat().st_size:,} bytes)"
        )

    log("")
    log("=" * 70)
    log("✓ Listening A 完成")
    log("✓ Listening B 完成")
    log("✓ Listening C 完成")
    log("✓ Listening 总音频完成")
    log("=" * 70)

    return 0


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    try:

        raise SystemExit(
            main()
        )

    except KeyboardInterrupt:

        log("")
        log("❌ 用户中断")

        raise SystemExit(130)

    except Exception as exc:

        log("")
        log(
            f"❌ {exc}"
        )

        raise SystemExit(1)
