#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.2.1

======================================================================
职责
======================================================================

独立生成英语听力：

    Listening_A
    Listening_B
    Listening_C
    Listening_总音频

不调用 AI。

不修改：

    试卷
    答案与解析

======================================================================
Kokoro
======================================================================

模型：

    02_英语学习系统/models/kokoro/
        kokoro-v1.1-zh.fp16.onnx
        voices-v1.1-zh.bin

男声：

    am_adam

女声：

    af_sarah

语言：

    en-us

======================================================================
听力规则
======================================================================

PART A
----------------------------------------------------------------------

女声。

每一道题：

    题目
    A
    B
    C
    D

整题播放两遍。

======================================================================

PART B
----------------------------------------------------------------------

明确 Male / Female。

例如：

    Male: ...
    Female: ...
    Male: ...

整段对话完整播放两遍。

不是每一句重复两遍。

然后播放：

    A
    B
    C
    D

======================================================================

PART C
----------------------------------------------------------------------

文章：

    女声
    播放一次

然后：

    题目 × 2
    A × 2
    B × 2
    C × 2
    D × 2

全部使用女声。

======================================================================
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

MODELS_DIR = PROJECT_ROOT / "models" / "kokoro"

MODEL_PATH = MODELS_DIR / "kokoro-v1.1-zh.fp16.onnx"
VOICES_PATH = MODELS_DIR / "voices-v1.1-zh.bin"


# ======================================================================
# DEFAULT
# ======================================================================

DEFAULT_MALE_VOICE = "am_adam"
DEFAULT_FEMALE_VOICE = "af_sarah"
DEFAULT_LANGUAGE = "en-us"
DEFAULT_SPEED = 1.0

SUPPORTED_FORMATS = {
    "mp3",
    "m4a",
    "wav",
}


# ======================================================================
# DATA
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
    options: list[str]
    dialogue: list[tuple[str, str]]


# ======================================================================
# LOG
# ======================================================================

def log(text: str = "") -> None:
    print(text, flush=True)


# ======================================================================
# TEXT
# ======================================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 图片
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    # Markdown link
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    # 粗体
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

    # 斜体
    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
    )

    text = re.sub(
        r"_(.*?)_",
        r"\1",
    )

    # 行内代码
    text = re.sub(
        r"`([^`]*)`",
        r"\1",
        text,
    )

    # HTML
    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
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
    line = line.strip()

    if not line:
        return ""

    line = re.sub(
        r"^#{1,6}\s*",
        "",
        line,
    )

    line = re.sub(
        r"^>\s*",
        "",
        line,
    )

    line = re.sub(
        r"^[-*+]\s+",
        "",
        line,
    )

    return clean_text(line)


# ======================================================================
# FILE
# ======================================================================

def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(
            f"文件不存在：{path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    if not text.strip():
        raise RuntimeError(
            f"文件为空：{path}"
        )

    return text


# ======================================================================
# PART EXTRACTION
# ======================================================================

def find_part_start(
    lines: list[str],
    part: str,
) -> int | None:

    target = part.upper()

    for index, raw in enumerate(lines):
        line = clean_line(raw)

        if not line:
            continue

        upper = line.upper()

        # Part A / Part B / Part C
        if re.match(
            rf"^PART\s+{target}\b",
            upper,
        ):
            return index

        # Listening A
        if re.match(
            rf"^LISTENING\s+{target}\b",
            upper,
        ):
            return index

        # 中文
        if target == "A" and (
            "第一部分" in line
            or "听句子" in line
        ):
            return index

        if target == "B" and (
            "第二部分" in line
            or "听对话" in line
        ):
            return index

        if target == "C" and (
            "第三部分" in line
            or "听原文" in line
        ):
            return index

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

    next_parts = {
        "A": ["B"],
        "B": ["C"],
        "C": [],
    }

    for index in range(
        start + 1,
        len(lines),
    ):
        if find_part_header(
            lines[index],
            next_parts.get(part, []),
        ):
            end = index
            break

    return "\n".join(
        lines[start:end]
    ).strip()


def find_part_header(
    line: str,
    parts: list[str],
) -> bool:

    if not parts:
        return False

    clean = clean_line(line)

    if not clean:
        return False

    upper = clean.upper()

    for part in parts:

        if re.match(
            rf"^PART\s+{part}\b",
            upper,
        ):
            return True

        if re.match(
            rf"^LISTENING\s+{part}\b",
            upper,
        ):
            return True

    return False


# ======================================================================
# QUESTION / OPTION
# ======================================================================

def parse_question_header(
    line: str,
) -> tuple[int | None, str]:

    line = clean_line(line)

    # 1. xxx
    match = re.match(
        r"^(\d+)\s*[.)、．:：-]\s*(.*)$",
        line,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    # 第1题 xxx
    match = re.match(
        r"^第\s*(\d+)\s*题\s*(.*)$",
        line,
        flags=re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    # Question 1: xxx
    match = re.match(
        r"^Question\s+(\d+)\s*[:：.)、-]?\s*(.*)$",
        line,
        flags=re.IGNORECASE,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    return None, ""


def parse_option(
    line: str,
) -> tuple[str | None, str]:

    line = clean_line(line)

    # 最简单稳定的判断：
    # A. xxx
    # B) xxx
    # C: xxx
    # D、xxx
    #
    # 不使用复杂的嵌套正则。

    if len(line) < 2:
        return None, ""

    first = line[0].upper()

    if first not in "ABCD":
        return None, ""

    rest = line[1:]

    if not rest:
        return None, ""

    # A xxx
    if rest[0].isspace():
        return first, rest.strip()

    # A. xxx
    if rest[0] in ".):：、-—":
        return first, rest[1:].strip()

    return None, ""


# ======================================================================
# SPEAKER
# ======================================================================

def parse_speaker(
    line: str,
) -> tuple[str | None, str]:

    line = clean_line(line)

    # 英文
    match = re.match(
        r"^(Male|Female|Man|Woman)\s*[:：-]\s*(.+)$",
        line,
        flags=re.IGNORECASE,
    )

    if match:
        name = match.group(1).lower()
        text = match.group(2).strip()

        if name in {"male", "man"}:
            return "male", text

        return "female", text

    # 中文
    match = re.match(
        r"^(男声|女声|男|女|男士|女士)\s*[:：-]\s*(.+)$",
        line,
    )

    if match:
        name = match.group(1)
        text = match.group(2).strip()

        if name in {"男", "男声", "男士"}:
            return "male", text

        return "female", text

    return None, ""


# ======================================================================
# QUESTIONS
# ======================================================================

def parse_questions(
    text: str,
) -> list[Question]:

    questions: list[Question] = []

    current: Question | None = None
    current_option_index: int | None = None

    for raw in text.splitlines():

        line = clean_line(raw)

        if not line:
            continue

        # Part 标题
        upper = line.upper()

        if (
            upper.startswith("PART A")
            or upper.startswith("PART B")
            or upper.startswith("PART C")
            or upper.startswith("LISTENING A")
            or upper.startswith("LISTENING B")
            or upper.startswith("LISTENING C")
        ):
            continue

        # 题号
        number, body = parse_question_header(line)

        if number is not None:

            current = Question(
                number=number,
                question=body,
                options=[],
                dialogue=[],
            )

            questions.append(current)
            current_option_index = None
            continue

        # 选项
        letter, option_text = parse_option(line)

        if (
            current is not None
            and letter is not None
        ):
            current.options.append(
                f"{letter}. {option_text}"
            )

            current_option_index = (
                len(current.options) - 1
            )

            continue

        # 对话
        speaker, dialogue_text = parse_speaker(
            line
        )

        if (
            current is not None
            and speaker is not None
        ):
            current.dialogue.append(
                (
                    speaker,
                    dialogue_text,
                )
            )

            continue

        # 普通续行
        if current is None:
            continue

        if current_option_index is not None:
            current.options[
                current_option_index
            ] += " " + line
        else:
            if current.question:
                current.question += " " + line
            else:
                current.question = line

    return questions


# ======================================================================
# DIALOGUE
# ======================================================================

def extract_dialogue(
    text: str,
) -> list[tuple[str, str]]:

    result = []

    for raw in text.splitlines():

        line = clean_line(raw)

        if not line:
            continue

        speaker, body = parse_speaker(
            line
        )

        if speaker and body:
            result.append(
                (
                    speaker,
                    body,
                )
            )

    return result


def attach_dialogue(
    questions: list[Question],
    dialogue: list[tuple[str, str]],
) -> None:

    if not questions:
        return

    # 如果只有一道题，整段对话属于该题
    if len(questions) == 1:
        questions[0].dialogue = dialogue
        return

    # 如果多道题，且题目中已经明确带有 dialogue，
    # 不覆盖。
    if any(
        question.dialogue
        for question in questions
    ):
        return

    # 无法安全按题号切分时，
    # 不猜测归属。
    #
    # 这种情况下将整段对话归到第一题，
    # 同时打印提示。
    questions[0].dialogue = dialogue


# ======================================================================
# PASSAGE
# ======================================================================

def extract_passage(
    text: str,
) -> str:

    lines = text.splitlines()

    passage = []

    for raw in lines:

        line = clean_line(raw)

        if not line:
            continue

        upper = line.upper()

        # Part C 标题
        if upper.startswith("PART C"):
            continue

        if upper.startswith("LISTENING C"):
            continue

        # 遇到第一道题就结束
        number, _ = parse_question_header(
            line
        )

        if number is not None:
            break

        # 如果进入 Questions 区域
        if re.match(
            r"^(QUESTIONS?|问题|选择题)\b",
            line,
            flags=re.IGNORECASE,
        ):
            break

        passage.append(line)

    return " ".join(
        passage
    ).strip()


# ======================================================================
# BUILD PART A
# ======================================================================

def build_part_a(
    questions: list[Question],
    female_voice: str,
) -> list[Segment]:

    segments = []

    for question in questions:

        parts = []

        if question.question:
            parts.append(
                question.question
            )

        parts.extend(
            question.options[:4]
        )

        text = " ".join(
            x for x in parts if x
        ).strip()

        if not text:
            continue

        # 整题 ×2
        segments.append(
            Segment(
                text=text,
                voice=female_voice,
                repeat=2,
            )
        )

    return segments


# ======================================================================
# BUILD PART B
# ======================================================================

def build_part_b(
    questions: list[Question],
    female_voice: str,
    male_voice: str,
) -> list[Segment]:

    segments = []

    for question in questions:

        dialogue = question.dialogue

        # --------------------------------------------------------------
        # 对话第一遍
        # --------------------------------------------------------------

        for speaker, text in dialogue:

            voice = (
                male_voice
                if speaker == "male"
                else female_voice
            )

            segments.append(
                Segment(
                    text=text,
                    voice=voice,
                    repeat=1,
                )
            )

        # --------------------------------------------------------------
        # 对话第二遍
        # --------------------------------------------------------------

        for speaker, text in dialogue:

            voice = (
                male_voice
                if speaker == "male"
                else female_voice
            )

            segments.append(
                Segment(
                    text=text,
                    voice=voice,
                    repeat=1,
                )
            )

        # --------------------------------------------------------------
        # 选项
        # --------------------------------------------------------------

        for option in question.options[:4]:

            segments.append(
                Segment(
                    text=option,
                    voice=female_voice,
                    repeat=1,
                )
            )

    return segments


# ======================================================================
# BUILD PART C
# ======================================================================

def build_part_c(
    passage: str,
    questions: list[Question],
    female_voice: str,
) -> list[Segment]:

    segments = []

    # --------------------------------------------------------------
    # 原文 ×1
    # --------------------------------------------------------------

    if passage:

        segments.append(
            Segment(
                text=passage,
                voice=female_voice,
                repeat=1,
            )
        )

    # --------------------------------------------------------------
    # 每道题：
    #
    # 题目 ×2
    # A ×2
    # B ×2
    # C ×2
    # D ×2
    # --------------------------------------------------------------

    for question in questions:

        if question.question:

            segments.append(
                Segment(
                    text=question.question,
                    voice=female_voice,
                    repeat=2,
                )
            )

        for option in question.options[:4]:

            segments.append(
                Segment(
                    text=option,
                    voice=female_voice,
                    repeat=2,
                )
            )

    return segments


# ======================================================================
# KOKORO
# ======================================================================

def load_kokoro():

    try:
        from kokoro_onnx import Kokoro
    except ImportError as exc:

        raise RuntimeError(
            "无法导入 kokoro_onnx。\n"
            "请确认 requirements.txt 包含：\n"
            "    kokoro-onnx\n"
            "    numpy\n"
            "    soundfile\n"
            f"\n原始错误：{exc}"
        ) from exc

    if not MODEL_PATH.exists():

        raise FileNotFoundError(
            f"Kokoro 模型不存在：\n"
            f"{MODEL_PATH}"
        )

    if not VOICES_PATH.exists():

        raise FileNotFoundError(
            f"Kokoro voices 不存在：\n"
            f"{VOICES_PATH}"
        )

    log()
    log("加载 Kokoro 模型")
    log(f"MODEL  : {MODEL_PATH}")
    log(f"VOICES : {VOICES_PATH}")

    kokoro = Kokoro(
        str(MODEL_PATH),
        str(VOICES_PATH),
    )

    log("✓ Kokoro loaded")

    return kokoro


# ======================================================================
# TTS
# ======================================================================

def synthesize(
    kokoro,
    text: str,
    voice: str,
    speed: float,
):

    import numpy as np

    audio, sample_rate = kokoro.create(
        clean_text(text),
        voice=voice,
        speed=speed,
        lang=DEFAULT_LANGUAGE,
    )

    return (
        np.asarray(
            audio,
            dtype=np.float32,
        ),
        int(sample_rate),
    )


# ======================================================================
# SILENCE
# ======================================================================

def silence(
    sample_rate: int,
    seconds: float,
):

    import numpy as np

    length = int(
        sample_rate * seconds
    )

    return np.zeros(
        length,
        dtype=np.float32,
    )


# ======================================================================
# WRITE WAV
# ======================================================================

def write_wav(
    path: Path,
    audio,
    sample_rate: int,
) -> None:

    import soundfile as sf

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sf.write(
        str(path),
        audio,
        sample_rate,
        subtype="PCM_16",
    )


# ======================================================================
# FFMPEG
# ======================================================================

def get_ffmpeg() -> str:

    ffmpeg = shutil.which(
        "ffmpeg"
    )

    if not ffmpeg:

        raise RuntimeError(
            "找不到 ffmpeg。\n"
            "请在 GitHub Actions 中安装 ffmpeg。"
        )

    return ffmpeg


def convert_audio(
    source: Path,
    target: Path,
    audio_format: str,
) -> None:

    if audio_format == "wav":

        shutil.copy2(
            source,
            target,
        )

        return

    ffmpeg = get_ffmpeg()

    if audio_format == "mp3":

        codec = [
            "-codec:a",
            "libmp3lame",
            "-q:a",
            "2",
        ]

    elif audio_format == "m4a":

        codec = [
            "-codec:a",
            "aac",
            "-b:a",
            "192k",
        ]

    else:

        raise ValueError(
            f"不支持的音频格式："
            f"{audio_format}"
        )

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(source),
        *codec,
        str(target),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:

        raise RuntimeError(
            "FFmpeg 转码失败：\n"
            + result.stderr[-3000:]
        )


# ======================================================================
# GENERATE
# ======================================================================

def generate_audio(
    kokoro,
    segments: list[Segment],
    output: Path,
    speed: float,
    label: str,
) -> None:

    import numpy as np

    if not segments:

        raise RuntimeError(
            f"{label} 没有解析到有效内容。"
        )

    log()
    log("=" * 70)
    log(label)
    log("=" * 70)

    chunks = []

    sample_rate = None

    total = len(segments)

    for index, segment in enumerate(
        segments,
        start=1,
    ):

        text = clean_text(
            segment.text
        )

        if not text:
            continue

        log(
            f"[{index}/{total}] "
            f"{segment.voice} "
            f"repeat={segment.repeat} "
            f"chars={len(text)}"
        )

        for repeat_index in range(
            segment.repeat
        ):

            audio, sr = synthesize(
                kokoro,
                text,
                segment.voice,
                speed,
            )

            if sample_rate is None:
                sample_rate = sr

            if sr != sample_rate:

                raise RuntimeError(
                    f"{label} 采样率不一致："
                    f"{sample_rate} / {sr}"
                )

            chunks.append(audio)

            # 重复之间
            if repeat_index < segment.repeat - 1:

                chunks.append(
                    silence(
                        sample_rate,
                        0.7,
                    )
                )

        # 不同内容之间
        chunks.append(
            silence(
                sample_rate,
                0.3,
            )
        )

    if not chunks:

        raise RuntimeError(
            f"{label} 没有生成音频。"
        )

    audio = np.concatenate(
        chunks
    )

    with tempfile.TemporaryDirectory() as temp:

        temp_wav = (
            Path(temp)
            / f"{label}.wav"
        )

        write_wav(
            temp_wav,
            audio,
            sample_rate,
        )

        convert_audio(
            temp_wav,
            output,
            output.suffix.lstrip("."),
        )

    if (
        not output.exists()
        or output.stat().st_size <= 0
    ):

        raise RuntimeError(
            f"{label} 输出失败："
            f"{output}"
        )

    log(
        f"✓ {label} 完成："
        f"{output}"
    )


# ======================================================================
# CONCAT
# ======================================================================

def concat_audio(
    files: list[Path],
    output: Path,
) -> None:

    ffmpeg = get_ffmpeg()

    for file in files:

        if (
            not file.exists()
            or file.stat().st_size <= 0
        ):

            raise RuntimeError(
                f"无法合并音频："
                f"{file}"
            )

    with tempfile.TemporaryDirectory() as temp:

        concat_file = (
            Path(temp)
            / "concat.txt"
        )

        lines = []

        for file in files:

            escaped = str(
                file.resolve()
            ).replace(
                "'",
                "'\\''",
            )

            lines.append(
                f"file '{escaped}'"
            )

        concat_file.write_text(
            "\n".join(lines) + "\n",
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
            str(output),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:

            raise RuntimeError(
                "Listening 总音频合并失败：\n"
                + result.stderr[-3000:]
            )


# ======================================================================
# MAIN
# ======================================================================

def main():

    parser = argparse.ArgumentParser()

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
        required=True,
    )

    parser.add_argument(
        "--audio-format",
        choices=sorted(
            SUPPORTED_FORMATS
        ),
        default="mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
    )

    parser.add_argument(
        "--male-voice",
        default=DEFAULT_MALE_VOICE,
    )

    parser.add_argument(
        "--female-voice",
        default=DEFAULT_FEMALE_VOICE,
    )

    args = parser.parse_args()

    if args.speed <= 0:

        raise ValueError(
            f"speed 必须大于 0："
            f"{args.speed}"
        )

    exam_file = Path(
        args.exam_file
    ).resolve()

    answer_file = Path(
        args.answer_file
    ).resolve()

    if not exam_file.exists():

        raise FileNotFoundError(
            f"试卷不存在："
            f"{exam_file}"
        )

    if not answer_file.exists():

        raise FileNotFoundError(
            f"答案与解析不存在："
            f"{answer_file}"
        )

    output_dir = (
        exam_file.parent
        / "听力"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    extension = args.audio_format

    listening_a = (
        output_dir
        / f"Listening_A.{extension}"
    )

    listening_b = (
        output_dir
        / f"Listening_B.{extension}"
    )

    listening_c = (
        output_dir
        / f"Listening_C.{extension}"
    )

    listening_total = (
        output_dir
        / f"Listening_总音频.{extension}"
    )

    # --------------------------------------------------------------
    # HEADER
    # --------------------------------------------------------------

    log()
    log("=" * 70)
    log("748686 英语学习系统")
    log("Audio Generator V2.2.1")
    log("=" * 70)
    log(f"DATE        : {args.date}")
    log(f"FORMAT      : {args.audio_format}")
    log(f"SPEED       : {args.speed}")
    log(f"LANGUAGE    : {DEFAULT_LANGUAGE}")
    log(f"MALE VOICE  : {args.male_voice}")
    log(f"FEMALE VOICE: {args.female_voice}")
    log(f"EXAM        : {exam_file}")
    log(f"ANSWER      : {answer_file}")
    log(f"OUTPUT      : {output_dir}")

    # --------------------------------------------------------------
    # READ
    # --------------------------------------------------------------

    exam_text = read_text(
        exam_file
    )

    answer_text = read_text(
        answer_file
    )

    # --------------------------------------------------------------
    # EXTRACT
    # --------------------------------------------------------------

    log()
    log("-" * 70)
    log("解析 Listening A / B / C")
    log("-" * 70)

    part_a = extract_part(
        exam_text,
        "A",
    )

    part_b = extract_part(
        exam_text,
        "B",
    )

    part_c = extract_part(
        exam_text,
        "C",
    )

    # 如果试卷没有 Part，则尝试答案文件
    if not part_a:
        part_a = extract_part(
            answer_text,
            "A",
        )

    if not part_b:
        part_b = extract_part(
            answer_text,
            "B",
        )

    if not part_c:
        part_c = extract_part(
            answer_text,
            "C",
        )

    if not part_a:
        raise RuntimeError(
            "没有找到 Listening A。"
        )

    if not part_b:
        raise RuntimeError(
            "没有找到 Listening B。"
        )

    if not part_c:
        raise RuntimeError(
            "没有找到 Listening C。"
        )

    # --------------------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------------------

    questions_a = parse_questions(
        part_a
    )

    questions_b = parse_questions(
        part_b
    )

    questions_c = parse_questions(
        part_c
    )

    # --------------------------------------------------------------
    # B DIALOGUE
    # --------------------------------------------------------------

    dialogue_b = extract_dialogue(
        part_b
    )

    # 如果答案文件里有更明确的男女对话，
    # 而试卷没有，则使用答案文件。
    if not dialogue_b:

        answer_b = extract_part(
            answer_text,
            "B",
        )

        if not answer_b:

            answer_b = (
                find_answer_listening(
                    answer_text,
                    "B",
                )
            )

        dialogue_b = extract_dialogue(
            answer_b
        )

    attach_dialogue(
        questions_b,
        dialogue_b,
    )

    # --------------------------------------------------------------
    # C PASSAGE
    # --------------------------------------------------------------

    passage_c = extract_passage(
        part_c
    )

    if not passage_c:

        answer_c = extract_part(
            answer_text,
            "C",
        )

        if not answer_c:

            answer_c = (
                find_answer_listening(
                    answer_text,
                    "C",
                )
            )

        passage_c = extract_passage(
            answer_c
        )

        if not questions_c:

            questions_c = parse_questions(
                answer_c
            )

    # --------------------------------------------------------------
    # BUILD
    # --------------------------------------------------------------

    segments_a = build_part_a(
        questions_a,
        args.female_voice,
    )

    segments_b = build_part_b(
        questions_b,
        args.female_voice,
        args.male_voice,
    )

    segments_c = build_part_c(
        passage_c,
        questions_c,
        args.female_voice,
    )

    log(
        f"✓ Listening A："
        f"{len(segments_a)} segments"
    )

    log(
        f"✓ Listening B："
        f"{len(segments_b)} segments"
    )

    log(
        f"✓ Listening C："
        f"{len(segments_c)} segments"
    )

    if not segments_a:
        raise RuntimeError(
            "Listening A 没有解析出有效内容。"
        )

    if not segments_b:
        raise RuntimeError(
            "Listening B 没有解析出有效内容。"
        )

    if not segments_c:
        raise RuntimeError(
            "Listening C 没有解析出有效内容。"
        )

    # --------------------------------------------------------------
    # LOAD KOKORO
    # --------------------------------------------------------------

    kokoro = load_kokoro()

    # --------------------------------------------------------------
    # CLEAN OLD OUTPUT
    # --------------------------------------------------------------

    for file in [
        listening_a,
        listening_b,
        listening_c,
        listening_total,
    ]:

        if file.exists():
            file.unlink()

    # --------------------------------------------------------------
    # A
    # --------------------------------------------------------------

    generate_audio(
        kokoro,
        segments_a,
        listening_a,
        args.speed,
        "Listening A",
    )

    # --------------------------------------------------------------
    # B
    # --------------------------------------------------------------

    generate_audio(
        kokoro,
        segments_b,
        listening_b,
        args.speed,
        "Listening B",
    )

    # --------------------------------------------------------------
    # C
    # --------------------------------------------------------------

    generate_audio(
        kokoro,
        segments_c,
        listening_c,
        args.speed,
        "Listening C",
    )

    # --------------------------------------------------------------
    # VERIFY A/B/C
    # --------------------------------------------------------------

    for file in [
        listening_a,
        listening_b,
        listening_c,
    ]:

        if (
            not file.exists()
            or file.stat().st_size <= 0
        ):

            raise RuntimeError(
                f"音频文件验证失败："
                f"{file}"
            )

    log()
    log("=" * 70)
    log("Listening A / B / C 全部成功")
    log("=" * 70)

    # --------------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------------

    log()
    log("合并总音频：")
    log("    Listening A")
    log("        ↓")
    log("    Listening B")
    log("        ↓")
    log("    Listening C")
    log("        ↓")
    log("    Listening 总音频")

    concat_audio(
        [
            listening_a,
            listening_b,
            listening_c,
        ],
        listening_total,
    )

    if (
        not listening_total.exists()
        or listening_total.stat().st_size <= 0
    ):

        raise RuntimeError(
            f"总音频验证失败："
            f"{listening_total}"
        )

    # --------------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------------

    log()
    log("=" * 70)
    log("748686 英语学习系统")
    log("AUDIO GENERATION COMPLETE")
    log("=" * 70)

    log()
    log(f"✓ Listening A")
    log(f"  {listening_a}")

    log()
    log(f"✓ Listening B")
    log(f"  {listening_b}")

    log()
    log(f"✓ Listening C")
    log(f"  {listening_c}")

    log()
    log(f"✓ Listening 总音频")
    log(f"  {listening_total}")

    log()
    log("=" * 70)
    log("全部音频生成完成")
    log("=" * 70)


# ======================================================================
# ANSWER LISTENING FALLBACK
# ======================================================================

def find_answer_listening(
    text: str,
    part: str,
) -> str:

    lines = text.splitlines()

    start = None

    for index, raw in enumerate(lines):

        line = clean_line(raw)

        if not line:
            continue

        upper = line.upper()

        if (
            f"LISTENING {part}" in upper
            or f"PART {part}" in upper
            or f"听力 {part}" in line
        ):
            start = index
            break

    if start is None:
        return ""

    end = len(lines)

    for index in range(
        start + 1,
        len(lines),
    ):

        line = clean_line(
            lines[index]
        )

        upper = line.upper()

        if part == "A":

            if (
                "LISTENING B" in upper
                or "PART B" in upper
                or "听力 B" in line
            ):
                end = index
                break

        elif part == "B":

            if (
                "LISTENING C" in upper
                or "PART C" in upper
                or "听力 C" in line
            ):
                end = index
                break

    return "\n".join(
        lines[start:end]
    ).strip()


# ======================================================================
# ENTRY
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        log()
        log("❌ 用户中断音频生成。")
        sys.exit(130)

    except Exception as exc:

        log()
        log("=" * 70)
        log("❌ AUDIO GENERATION FAILED")
        log("=" * 70)
        log()
        log(str(exc))
        log()
        log("=" * 70)

        sys.exit(1)
