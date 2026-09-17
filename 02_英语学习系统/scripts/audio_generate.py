#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Listening Audio Generator V1.0

======================================================================
职责
======================================================================

从已经生成并最终落盘的英语试卷中读取 Listening A / B / C
听力原文，然后使用本地 Kokoro 模型生成音频。

核心原则：

1. 不调用 AI
2. 不重新生成听力文本
3. 不修改原始试卷
4. 音频内容严格来自最终听力原文
5. Listening A / B / C 分别生成独立音频
6. 支持 mp3 / m4a / wav
7. 支持 speed
8. 使用本地 Kokoro 模型

======================================================================
目录
======================================================================

02_英语学习系统/
│
├── models/
│   └── kokoro/
│       ├── kokoro-v1.1-zh.fp16.onnx
│       └── voices-v1.1-zh.bin
│
├── output/
│   └── YYYY-MM-DD/
│       └── 配套试卷/
│           ├── xxx_试卷.md
│           ├── xxx_答案与解析.md
│           └── 听力/
│               ├── Listening_A.mp3
│               ├── Listening_B.mp3
│               └── Listening_C.mp3
│
└── scripts/
    └── audio_generate.py

======================================================================
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf


# ======================================================================
# 基础路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent

MODELS_DIR = PROJECT_ROOT / "models" / "kokoro"

DEFAULT_MODEL = MODELS_DIR / "kokoro-v1.1-zh.fp16.onnx"
DEFAULT_VOICES = MODELS_DIR / "voices-v1.1-zh.bin"

DEFAULT_VOICE = "af_sarah"
DEFAULT_SPEED = 1.0

SAMPLE_RATE = 24000


# ======================================================================
# 日志
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    print()
    print("=" * 70)
    print("❌ AUDIO GENERATION ERROR")
    print("=" * 70)
    print(message)
    print("=" * 70)
    raise SystemExit(1)


# ======================================================================
# 文件读取
# ======================================================================

def read_text(path: Path) -> str:

    if not path.exists():
        fail(f"文件不存在：{path}")

    try:
        return path.read_text(encoding="utf-8")

    except UnicodeDecodeError:
        fail(f"文件不是 UTF-8 编码：{path}")

    except Exception as exc:
        fail(f"读取文件失败：{path}\n{exc}")


# ======================================================================
# 清理 Markdown
# ======================================================================

def clean_markdown(text: str) -> str:

    # 图片
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)

    # 链接
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # 粗体 / 斜体
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # Markdown 标题
    text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)

    # 引用
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)

    # 列表符号
    text = re.sub(
        r"^\s*(?:[-*+]|\d+[.)])\s+",
        "",
        text,
        flags=re.MULTILINE,
    )

    # 多余空白
    text = re.sub(r"[ \t]+", " ", text)

    # 多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ======================================================================
# 查找 Listening A / B / C
# ======================================================================

LISTENING_PATTERNS = {
    "A": [
        re.compile(
            r"(?is)"
            r"(?:^|\n)"
            r"\s*(?:#{1,6}\s*)?"
            r"(?:Listening\s*A|听力\s*A|Part\s*A|Section\s*A)"
            r"\s*(?:\n|:|：)"
            r"(.*?)(?="
            r"\n\s*(?:#{1,6}\s*)?"
            r"(?:Listening\s*B|听力\s*B|Part\s*B|Section\s*B)"
            r"\s*(?:\n|:|：)"
            r"|$)"
        )
    ],
    "B": [
        re.compile(
            r"(?is)"
            r"(?:^|\n)"
            r"\s*(?:#{1,6}\s*)?"
            r"(?:Listening\s*B|听力\s*B|Part\s*B|Section\s*B)"
            r"\s*(?:\n|:|：)"
            r"(.*?)(?="
            r"\n\s*(?:#{1,6}\s*)?"
            r"(?:Listening\s*C|听力\s*C|Part\s*C|Section\s*C)"
            r"\s*(?:\n|:|：)"
            r"|$)"
        )
    ],
    "C": [
        re.compile(
            r"(?is)"
            r"(?:^|\n)"
            r"\s*(?:#{1,6}\s*)?"
            r"(?:Listening\s*C|听力\s*C|Part\s*C|Section\s*C)"
            r"\s*(?:\n|:|：)"
            r"(.*)$"
        )
    ],
}


def extract_part(text: str, part: str) -> str | None:

    for pattern in LISTENING_PATTERNS[part]:

        match = pattern.search(text)

        if match:
            content = match.group(1).strip()

            if content:
                return clean_markdown(content)

    return None


# ======================================================================
# 从试卷读取 Listening A/B/C
# ======================================================================

def extract_listening_parts(exam_text: str) -> dict[str, str]:

    parts: dict[str, str] = {}

    for part in ("A", "B", "C"):

        content = extract_part(exam_text, part)

        if content:
            parts[part] = content

    return parts


# ======================================================================
# 从答案与解析中读取听力原文
#
# 作为严格的最终听力原文来源。
#
# 如果试卷中已经包含听力原文，则优先使用试卷。
# 如果试卷只有题目而答案文件包含 Transcript，
# 则从答案文件补充。
# ======================================================================

TRANSCRIPT_PATTERNS = [

    re.compile(
        r"(?is)"
        r"(?:^|\n)"
        r"\s*(?:#{1,6}\s*)?"
        r"(?:Listening\s*A|听力\s*A|Part\s*A|Section\s*A)"
        r".*?"
        r"(?:听力原文|原文|Transcript|Audio\s*Script)"
        r"\s*(?:\n|:|：)"
        r"(.*?)(?="
        r"\n\s*(?:#{1,6}\s*)?"
        r"(?:Listening\s*B|听力\s*B|Part\s*B|Section\s*B)"
        r"|$)"
    ),

    re.compile(
        r"(?is)"
        r"(?:^|\n)"
        r"\s*(?:#{1,6}\s*)?"
        r"(?:Listening\s*B|听力\s*B|Part\s*B|Section\s*B)"
        r".*?"
        r"(?:听力原文|原文|Transcript|Audio\s*Script)"
        r"\s*(?:\n|:|：)"
        r"(.*?)(?="
        r"\n\s*(?:#{1,6}\s*)?"
        r"(?:Listening\s*C|听力\s*C|Part\s*C|Section\s*C)"
        r"|$)"
    ),

    re.compile(
        r"(?is)"
        r"(?:^|\n)"
        r"\s*(?:#{1,6}\s*)?"
        r"(?:Listening\s*C|听力\s*C|Part\s*C|Section\s*C)"
        r".*?"
        r"(?:听力原文|原文|Transcript|Audio\s*Script)"
        r"\s*(?:\n|:|：)"
        r"(.*)$"
    ),
]


def extract_transcripts(answer_text: str) -> dict[str, str]:

    parts: dict[str, str] = {}

    matches = []

    for pattern in TRANSCRIPT_PATTERNS:

        match = pattern.search(answer_text)

        if match:
            matches.append(match.group(1).strip())

    # 如果有明确的三个分区，重新按分区处理
    for part in ("A", "B", "C"):

        pattern = re.compile(
            rf"(?is)"
            rf"(?:Listening\s*{part}|听力\s*{part}|Part\s*{part}|Section\s*{part})"
            rf".*?"
            rf"(?:听力原文|原文|Transcript|Audio\s*Script)"
            rf"\s*(?:\n|:|：)"
            rf"(.*?)"
            rf"(?="
            rf"\n\s*(?:#{1,6}\s*)?"
            rf"(?:Listening\s*[ABC]|听力\s*[ABC]|Part\s*[ABC]|Section\s*[ABC])"
            rf"|$)"
        )

        match = pattern.search(answer_text)

        if match:

            content = clean_markdown(match.group(1))

            if content:
                parts[part] = content

    return parts


# ======================================================================
# 合并题目 / 原文
# ======================================================================

def resolve_listening_text(
    exam_file: Path,
    answer_file: Path | None,
) -> dict[str, str]:

    exam_text = read_text(exam_file)

    log()
    log("正在读取最终试卷听力内容...")
    log(f"试卷：{exam_file}")

    parts = extract_listening_parts(exam_text)

    # --------------------------------------------------------------
    # 如果试卷本身已经包含完整听力原文
    # --------------------------------------------------------------

    if len(parts) == 3:

        log("✓ 从最终试卷读取 Listening A/B/C")

        return parts

    # --------------------------------------------------------------
    # 如果试卷没有完整原文，则从答案与解析读取 Transcript
    # --------------------------------------------------------------

    if answer_file is not None and answer_file.exists():

        log("试卷未包含完整听力原文")
        log("→ 检查答案与解析中的最终 Transcript")

        answer_text = read_text(answer_file)

        transcript_parts = extract_transcripts(answer_text)

        for part, content in transcript_parts.items():

            if content:
                parts[part] = content

    # --------------------------------------------------------------
    # 最终验证
    # --------------------------------------------------------------

    missing = [
        part
        for part in ("A", "B", "C")
        if not parts.get(part)
    ]

    if missing:

        fail(
            "无法找到完整的 Listening 原文。\n"
            f"缺少：{', '.join(missing)}\n\n"
            "为了防止 TTS 生成错误内容，程序不会猜测或自行生成听力文本。"
        )

    log("✓ Listening A 原文已确认")
    log("✓ Listening B 原文已确认")
    log("✓ Listening C 原文已确认")

    return parts


# ======================================================================
# 检查 Kokoro
# ======================================================================

def load_kokoro(
    model_path: Path,
    voices_path: Path,
):

    if not model_path.exists():
        fail(
            "Kokoro 模型不存在：\n"
            f"{model_path}"
        )

    if not voices_path.exists():
        fail(
            "Kokoro voices 文件不存在：\n"
            f"{voices_path}"
        )

    try:
        from kokoro_onnx import Kokoro

    except ImportError:
        fail(
            "没有安装 kokoro-onnx。\n"
            "请检查 requirements.txt。"
        )

    log()
    log("============================================================")
    log("加载 Kokoro")
    log("============================================================")
    log(f"Model : {model_path}")
    log(f"Voices: {voices_path}")

    try:
        kokoro = Kokoro(
            str(model_path),
            str(voices_path),
        )

    except Exception as exc:
        fail(f"Kokoro 模型加载失败：\n{exc}")

    log("✓ Kokoro 加载成功")

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

    if not text.strip():
        fail("听力原文为空，拒绝生成音频。")

    log()
    log("开始 TTS...")
    log(f"Voice : {voice}")
    log(f"Speed : {speed}")
    log(f"Chars : {len(text)}")

    try:

        samples, sample_rate = kokoro.create(
            text,
            voice=voice,
            speed=speed,
            lang="en-us",
        )

    except Exception as exc:
        fail(f"Kokoro TTS 生成失败：\n{exc}")

    samples = np.asarray(samples)

    if samples.size == 0:
        fail("Kokoro 返回空音频。")

    if samples.dtype != np.float32:
        samples = samples.astype(np.float32)

    return samples, sample_rate


# ======================================================================
# WAV
# ======================================================================

def save_wav(
    samples,
    sample_rate: int,
    output_file: Path,
) -> None:

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    sf.write(
        str(output_file),
        samples,
        sample_rate,
        subtype="PCM_16",
    )

    if not output_file.exists() or output_file.stat().st_size == 0:
        fail(f"WAV 写入失败：{output_file}")

    log(f"✓ WAV：{output_file}")


# ======================================================================
# FFmpeg
# ======================================================================

def require_ffmpeg() -> str:

    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:

        fail(
            "当前音频格式需要 FFmpeg，但系统中没有找到 ffmpeg。\n"
            "请先安装 FFmpeg。"
        )

    return ffmpeg


def convert_audio(
    wav_file: Path,
    output_file: Path,
    audio_format: str,
) -> None:

    if audio_format == "wav":

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
            "-b:a",
            "128k",
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
            "128k",
            str(output_file),
        ]

    else:

        fail(
            f"不支持的音频格式：{audio_format}"
        )

    log()
    log(f"转换音频：{output_file.name}")

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:

        fail(
            f"FFmpeg 转换失败：\n"
            f"{result.stderr}"
        )

    if not output_file.exists() or output_file.stat().st_size == 0:

        fail(
            f"音频文件生成失败：{output_file}"
        )

    log(f"✓ 音频：{output_file}")


# ======================================================================
# 单个 Part
# ======================================================================

def generate_part(
    kokoro,
    part: str,
    text: str,
    output_dir: Path,
    audio_format: str,
    voice: str,
    speed: float,
) -> Path:

    log()
    log("============================================================")
    log(f"Listening {part}")
    log("============================================================")

    log()
    log("听力原文：")
    log("-" * 60)
    log(text)
    log("-" * 60)

    samples, sample_rate = synthesize(
        kokoro=kokoro,
        text=text,
        voice=voice,
        speed=speed,
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_wav = Path(temp_dir) / f"Listening_{part}.wav"

        save_wav(
            samples=samples,
            sample_rate=sample_rate,
            output_file=temp_wav,
        )

        final_file = (
            output_dir
            / f"Listening_{part}.{audio_format}"
        )

        convert_audio(
            wav_file=temp_wav,
            output_file=final_file,
            audio_format=audio_format,
        )

    return final_file


# ======================================================================
# 主流程
# ======================================================================

def generate_audio(
    date: str,
    exam_file: Path,
    answer_file: Path | None,
    audio_format: str,
    speed: float,
    voice: str,
    model_path: Path,
    voices_path: Path,
) -> None:

    log()
    log("============================================================")
    log("748686 英语学习系统")
    log("Listening Audio Generator V1.0")
    log("============================================================")
    log(f"DATE       : {date}")
    log(f"FORMAT     : {audio_format}")
    log(f"SPEED      : {speed}")
    log(f"VOICE      : {voice}")
    log("============================================================")

    # --------------------------------------------------------------
    # 1. 读取最终听力原文
    # --------------------------------------------------------------

    listening_parts = resolve_listening_text(
        exam_file=exam_file,
        answer_file=answer_file,
    )

    # --------------------------------------------------------------
    # 2. 加载 Kokoro
    # --------------------------------------------------------------

    kokoro = load_kokoro(
        model_path=model_path,
        voices_path=voices_path,
    )

    # --------------------------------------------------------------
    # 3. 输出目录
    # --------------------------------------------------------------

    output_dir = (
        PROJECT_ROOT
        / "output"
        / date
        / "配套试卷"
        / "听力"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------------
    # 4. A / B / C
    # --------------------------------------------------------------

    generated = {}

    for part in ("A", "B", "C"):

        generated[part] = generate_part(
            kokoro=kokoro,
            part=part,
            text=listening_parts[part],
            output_dir=output_dir,
            audio_format=audio_format,
            voice=voice,
            speed=speed,
        )

    # --------------------------------------------------------------
    # 5. 最终验证
    # --------------------------------------------------------------

    log()
    log("============================================================")
    log("音频最终验证")
    log("============================================================")

    for part, path in generated.items():

        if not path.exists():

            fail(
                f"Listening {part} 音频不存在：{path}"
            )

        if path.stat().st_size == 0:

            fail(
                f"Listening {part} 音频为空：{path}"
            )

        log(
            f"✓ Listening {part}: "
            f"{path.name} "
            f"({path.stat().st_size} bytes)"
        )

    log()
    log("============================================================")
    log("✓ Listening A / B / C 音频全部生成")
    log("============================================================")

    for part in ("A", "B", "C"):
        log(str(generated[part]))

    log("============================================================")


# ======================================================================
# CLI
# ======================================================================

def build_parser():

    parser = argparse.ArgumentParser(
        description="748686 英语学习系统 Listening 音频生成器"
    )

    parser.add_argument(
        "--date",
        required=True,
        help="日期，例如 2026-09-17",
    )

    parser.add_argument(
        "--exam-file",
        required=True,
        help="最终英语试卷 Markdown 文件",
    )

    parser.add_argument(
        "--answer-file",
        required=False,
        default="",
        help="答案与解析 Markdown 文件，可选",
    )

    parser.add_argument(
        "--audio-format",
        choices=["mp3", "m4a", "wav"],
        default="mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
    )

    parser.add_argument(
        "--voice",
        default=DEFAULT_VOICE,
    )

    parser.add_argument(
        "--model",
        default=str(DEFAULT_MODEL),
    )

    parser.add_argument(
        "--voices",
        default=str(DEFAULT_VOICES),
    )

    return parser


# ======================================================================
# Entry
# ======================================================================

def main():

    parser = build_parser()
    args = parser.parse_args()

    exam_file = Path(args.exam_file)

    answer_file = (
        Path(args.answer_file)
        if args.answer_file
        else None
    )

    model_path = Path(args.model)
    voices_path = Path(args.voices)

    generate_audio(
        date=args.date,
        exam_file=exam_file,
        answer_file=answer_file,
        audio_format=args.audio_format,
        speed=args.speed,
        voice=args.voice,
        model_path=model_path,
        voices_path=voices_path,
    )


if __name__ == "__main__":
    main()
