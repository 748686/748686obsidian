#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.0

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

然后：

    Male   -> 美式男声
    Female -> 美式女声

使用本地 Kokoro 模型生成：

    Listening_A
    Listening_B
    Listening_C

最后将：

    A + B + C

严格按照顺序合并为：

    Listening_总音频

======================================================================
重要原则
======================================================================

1. 本模块不调用 AI 生成新的听力内容。

2. 本模块不修改试卷。

3. 本模块不修改答案与解析。

4. 音频文本必须来自最终落盘文件。

5. 男声 / 女声只负责声音，不负责生成内容。

6. A / B / C 必须全部成功后，才生成总音频。

7. 如果 A / B / C 任意一部分无法可靠提取，
   整个音频任务直接失败。

8. 使用美式英语。

======================================================================
默认 Kokoro 模型
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

# 美式英语
LANGUAGE = "en-us"

# 男声
MALE_VOICE = "am_adam"

# 女声
FEMALE_VOICE = "af_sarah"


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
    清理 Markdown / 空白，但不修改正文内容。
    """

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 去掉 Markdown 加粗
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)

    # 去掉 Markdown 斜体
    text = re.sub(r"(?<!\*)\*(.*?)\*(?!\*)", r"\1", text)

    # 去掉行首 Markdown bullet
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)

    # 去掉多余空格
    text = re.sub(r"[ \t]+", " ", text)

    # 连续空行压缩
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_speaker_label(text: str) -> str:
    """
    将角色标签统一成标准形式。
    """

    value = text.strip().lower()

    value = value.rstrip(":：")

    value = re.sub(r"[*_`#]", "", value)

    value = value.strip()

    return value


# ======================================================================
# Speaker recognition
# ======================================================================

def speaker_from_label(label: str) -> Optional[str]:
    """
    根据角色标签判断 male / female。

    支持：

        Male
        Man
        Boy
        Speaker 1

        Female
        Woman
        Girl
        Lady
        Speaker 2

    注意：

    Speaker 1 / Speaker 2 无法可靠判断性别，
    因此不会自动猜测。
    """

    value = clean_speaker_label(label)

    male_labels = {
        "male",
        "man",
        "boy",
        "gentleman",
        "male speaker",
        "man speaker",
        "speaker male",
        "speaker man",
    }

    female_labels = {
        "female",
        "woman",
        "girl",
        "lady",
        "female speaker",
        "woman speaker",
        "speaker female",
        "speaker woman",
    }

    if value in male_labels:
        return "male"

    if value in female_labels:
        return "female"

    return None


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


def find_section(text: str, section: str) -> Optional[Tuple[int, int]]:
    """
    找到 Listening A/B/C 的正文范围。
    """

    matches = []

    for pattern in SECTION_PATTERNS[section]:
        match = re.search(pattern, text)

        if match:
            matches.append(match)

    if not matches:
        return None

    start_match = min(matches, key=lambda x: x.start())

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


def extract_sections(text: str) -> Dict[str, str]:
    """
    从 Markdown 中提取 Listening A/B/C。
    """

    result: Dict[str, str] = {}

    for section in ("A", "B", "C"):

        location = find_section(text, section)

        if location is None:
            continue

        start, end = location

        content = text[start:end]

        content = normalize_text(content)

        if content:
            result[section] = content

    return result


# ======================================================================
# Transcript extraction
# ======================================================================

TRANSCRIPT_HEADING_PATTERNS = [
    r"(?im)^\s{0,3}#{0,6}\s*(?:听力原文|听力原稿|听力文本)\s*:?\s*$",
    r"(?im)^\s{0,3}#{0,6}\s*(?:transcript|audio\s*script|listening\s*script)\s*:?\s*$",
    r"(?im)^\s{0,3}#{0,6}\s*听力\s*原文\s*:?\s*$",
]


def extract_transcript_block(text: str) -> Optional[str]:
    """
    尝试从答案与解析中找到完整听力原文。
    """

    for pattern in TRANSCRIPT_HEADING_PATTERNS:

        match = re.search(pattern, text)

        if not match:
            continue

        start = match.end()

        # 找下一个明显一级标题
        next_heading = re.search(
            r"(?im)^\s{0,3}#{1,6}\s+.+$",
            text[start:],
        )

        if next_heading:
            end = start + next_heading.start()
        else:
            end = len(text)

        block = text[start:end]

        block = normalize_text(block)

        if block:
            return block

    return None


# ======================================================================
# Speaker dialogue parsing
# ======================================================================

SPEAKER_LINE_PATTERN = re.compile(
    r"^\s*(?:\*\*|__|`)?"
    r"(?P<label>"
    r"Male|Man|Boy|Gentleman|"
    r"Female|Woman|Girl|Lady"
    r")"
    r"(?:\*\*|__|`)?"
    r"\s*[:：]\s*"
    r"(?P<text>.+?)"
    r"\s*$",
    re.IGNORECASE,
)


def parse_dialogue(text: str) -> List[Tuple[str, str]]:
    """
    将听力原文解析为：

        [
            ("male", "..."),
            ("female", "..."),
            ...
        ]

    只有明确角色标签时才允许进入。

    不猜测 Speaker 1 / Speaker 2。
    """

    lines = text.splitlines()

    dialogue: List[Tuple[str, str]] = []

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

        line = raw_line.strip()

        if not line:
            continue

        # --------------------------------------------------------------
        # speaker label
        # --------------------------------------------------------------

        match = SPEAKER_LINE_PATTERN.match(line)

        if match:

            flush_current()

            label = match.group("label")

            speaker = speaker_from_label(label)

            if speaker is None:
                fail(
                    f"无法识别角色：{label}"
                )

            current_speaker = speaker

            current_text = [
                match.group("text").strip()
            ]

            continue

        # --------------------------------------------------------------
        # plain text
        # --------------------------------------------------------------

        if current_speaker is not None:

            current_text.append(line)

            continue

        # --------------------------------------------------------------
        # Ignore obvious question/options sections.
        # --------------------------------------------------------------

        if re.match(
            r"^(?:\d+[\.\)、)]|[A-D][\.\)、)])\s*",
            line,
        ):
            continue

    flush_current()

    return dialogue


# ======================================================================
# Extract dialogue from one section
# ======================================================================

def extract_dialogue_from_section(
    section_text: str,
) -> List[Tuple[str, str]]:

    dialogue = parse_dialogue(section_text)

    if not dialogue:
        return []

    return dialogue


# ======================================================================
# Fallback transcript source
# ======================================================================

def load_source_text(
    exam_file: Path,
    answer_file: Optional[Path],
) -> Tuple[Dict[str, str], str]:

    exam_text = exam_file.read_text(
        encoding="utf-8"
    )

    exam_sections = extract_sections(exam_text)

    if all(
        section in exam_sections
        for section in ("A", "B", "C")
    ):
        return exam_sections, "exam"

    # --------------------------------------------------------------
    # Answer / analysis fallback
    # --------------------------------------------------------------

    if answer_file and answer_file.exists():

        answer_text = answer_file.read_text(
            encoding="utf-8"
        )

        answer_sections = extract_sections(answer_text)

        if all(
            section in answer_sections
            for section in ("A", "B", "C")
        ):
            return answer_sections, "answer"

        transcript = extract_transcript_block(
            answer_text
        )

        if transcript:

            transcript_sections = extract_sections(
                transcript
            )

            if all(
                section in transcript_sections
                for section in ("A", "B", "C")
            ):
                return transcript_sections, "answer_transcript"

    return {}, "none"


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
    log(f"  model  : {model_path}")
    log(f"  voices : {voices_path}")

    return Kokoro(
        str(model_path),
        str(voices_path),
    )


# ======================================================================
# Render one dialogue line
# ======================================================================

def synthesize_dialogue(
    kokoro,
    dialogue: List[Tuple[str, str]],
    output_wav: Path,
    speed: float,
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

    audio_chunks = []

    sample_rate: Optional[int] = None

    log("")
    log(
        f"开始生成：{output_wav.name}"
    )

    for index, (speaker, text) in enumerate(
        dialogue,
        start=1,
    ):

        if speaker == "male":

            voice = MALE_VOICE
            display_name = "Male"

        elif speaker == "female":

            voice = FEMALE_VOICE
            display_name = "Female"

        else:

            fail(
                f"未知 speaker：{speaker}"
            )

        log(
            f"  [{index:02d}] "
            f"{display_name} / {voice}"
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
                f"Kokoro 生成失败。\n"
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

        # --------------------------------------------------------------
        # 每句话之间留一点自然停顿
        # --------------------------------------------------------------

        pause_seconds = 0.22

        pause = np.zeros(
            int(sample_rate * pause_seconds),
            dtype=np.float32,
        )

        audio_chunks.append(samples)
        audio_chunks.append(pause)

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
# FFmpeg conversion
# ======================================================================

def require_ffmpeg() -> str:

    ffmpeg = shutil.which("ffmpeg")

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

    log("顺序：")

    for file in audio_files:
        log(f"  {file.name}")

    # --------------------------------------------------------------
    # WAV
    #
    # 使用 Python soundfile + numpy 拼接。
    # --------------------------------------------------------------

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

        # ----------------------------------------------------------
        # MP3 / M4A
        #
        # 使用 FFmpeg concat demuxer。
        # ----------------------------------------------------------

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
                    .replace("'", "'\\''")
                )

                lines.append(
                    f"file '{escaped}'"
                )

            concat_file.write_text(
                "\n".join(lines)
                + "\n",
                encoding="utf-8",
            )

            if audio_format == "mp3":

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

            elif audio_format == "m4a":

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

            else:

                fail(
                    f"不支持的合并格式：{audio_format}"
                )

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
            "Listening Audio Generator V2.0"
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
        default=MALE_VOICE,
    )

    parser.add_argument(
        "--voice-female",
        default=FEMALE_VOICE,
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

    global MALE_VOICE
    global FEMALE_VOICE

    MALE_VOICE = args.voice_male
    FEMALE_VOICE = args.voice_female

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    exam_file = Path(
        args.exam_file
    ).resolve()

    answer_file = (
        Path(args.answer_file).resolve()
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
    log("Audio Generator V2.0")
    log("=" * 70)

    log(f"DATE        : {args.date}")
    log(f"FORMAT      : {args.audio_format}")
    log(f"SPEED       : {args.speed}")
    log(f"LANGUAGE    : {LANGUAGE}")
    log(f"MALE VOICE  : {MALE_VOICE}")
    log(f"FEMALE VOICE: {FEMALE_VOICE}")
    log(f"EXAM        : {exam_file}")
    log(f"ANSWER      : {answer_file}")
    log(f"OUTPUT      : {output_dir}")

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
                "⚠️ 答案与解析不存在。"
                "将只使用试卷。"
            )

    # ------------------------------------------------------------------
    # Extract A/B/C
    # ------------------------------------------------------------------

    sections, source = load_source_text(
        exam_file,
        answer_file,
    )

    if source == "none":

        fail(
            "无法从最终试卷 / 答案与解析中完整提取 "
            "Listening A / B / C。"
        )

    log("")
    log("听力文本来源：")

    if source == "exam":
        log("  ✓ 最终试卷")

    elif source == "answer":
        log("  ✓ 答案与解析")

    elif source == "answer_transcript":
        log("  ✓ 答案与解析中的听力原文")

    # ------------------------------------------------------------------
    # Validate all sections
    # ------------------------------------------------------------------

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
            f"✓ Listening {section} "
            f"文本长度：{len(sections[section])}"
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

        temp_root = Path(temp_dir)

        for section in ("A", "B", "C"):

            log("")
            log("=" * 70)
            log(f"LISTENING {section}")
            log("=" * 70)

            dialogue = extract_dialogue_from_section(
                sections[section]
            )

            if not dialogue:

                fail(
                    f"Listening {section} "
                    "没有识别到 Male / Female 对话。"
                )

            male_count = sum(
                1
                for speaker, _ in dialogue
                if speaker == "male"
            )

            female_count = sum(
                1
                for speaker, _ in dialogue
                if speaker == "female"
            )

            log("")
            log(
                f"角色统计："
                f"Male={male_count}, "
                f"Female={female_count}"
            )

            if male_count == 0:

                fail(
                    f"Listening {section} "
                    "没有男声内容。"
                )

            if female_count == 0:

                fail(
                    f"Listening {section} "
                    "没有女声内容。"
                )

            temp_wav = (
                temp_root
                / f"Listening_{section}.wav"
            )

            final_file = (
                output_dir
                / f"Listening_{section}.{args.audio_format}"
            )

            synthesize_dialogue(
                kokoro=kokoro,
                dialogue=dialogue,
                output_wav=temp_wav,
                speed=args.speed,
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
    # IMPORTANT:
    #
    # Only after A/B/C all succeeded,
    # generate the total audio.
    # ------------------------------------------------------------------

    log("")
    log("=" * 70)
    log("A / B / C 全部生成成功")
    log("=" * 70)

    total_file = (
        output_dir
        / f"Listening_总音频.{args.audio_format}"
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
        / f"Listening_A.{args.audio_format}",

        output_dir
        / f"Listening_B.{args.audio_format}",

        output_dir
        / f"Listening_C.{args.audio_format}",

        output_dir
        / f"Listening_总音频.{args.audio_format}",
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
