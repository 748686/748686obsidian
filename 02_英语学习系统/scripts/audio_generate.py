#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Audio Generator V2.2

======================================================================
职责
======================================================================

独立于 main.py 的听力音频生成器。

读取已经生成并落盘的：

    1. 试卷
    2. 答案与解析

然后生成：

    output/YYYY-MM-DD/配套试卷/听力/
        ├── Listening_A.mp3
        ├── Listening_B.mp3
        ├── Listening_C.mp3
        └── Listening_总音频.mp3

支持：

    mp3
    m4a
    wav

======================================================================
核心原则
======================================================================

1. 不调用 AI
2. 不修改试卷
3. 不修改答案与解析
4. 不重新生成文章
5. 不重新生成试卷
6. 不重新生成答案
7. 直接读取最终已经落盘的 Markdown
8. 使用仓库内 Kokoro 模型
9. Listening A / B / C 独立生成
10. A / B / C 全部成功后才生成总音频

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
Listening 规则
======================================================================

PART A — 听句子
----------------------------------------------------------------------
女声。

每一道题：

    句子
    四个选项

作为完整的一道题，整题播放两遍。

即：

    Question 1
    Options A B C D

    再完整播放一次。

----------------------------------------------------------------------

PART B — 听对话
----------------------------------------------------------------------
明确区分 Male / Female。

例如：

    Male: ...
    Female: ...
    Male: ...

整段男女对话完整播放两遍。

然后播放四个选项。

注意：

不能把每一句男女对话分别重复两遍。

错误：

    Male ×2
    Female ×2
    Male ×2
    Female ×2

正确：

    Male
    Female
    Male
    Female

    ↓ 整段再重复一次 ↓

    Male
    Female
    Male
    Female

然后：

    A
    B
    C
    D

----------------------------------------------------------------------

PART C — 听原文
----------------------------------------------------------------------
文章：

    女声
    播放一次

然后每一道题：

    题目
    A
    B
    C
    D

其中：

    题目 ×2
    A ×2
    B ×2
    C ×2
    D ×2

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
from typing import Iterable


# ======================================================================
# 基础路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
REPO_ROOT = PROJECT_ROOT.parent

MODELS_DIR = PROJECT_ROOT / "models" / "kokoro"

MODEL_PATH = MODELS_DIR / "kokoro-v1.1-zh.fp16.onnx"
VOICES_PATH = MODELS_DIR / "voices-v1.1-zh.bin"

OUTPUT_ROOT = PROJECT_ROOT / "output"


# ======================================================================
# Kokoro 默认配置
# ======================================================================

DEFAULT_MALE_VOICE = "am_adam"
DEFAULT_FEMALE_VOICE = "af_sarah"
DEFAULT_LANGUAGE = "en-us"

DEFAULT_SPEED = 1.0

SUPPORTED_FORMATS = {"mp3", "m4a", "wav"}


# ======================================================================
# 数据结构
# ======================================================================

@dataclass
class Segment:
    """
    单个 TTS 片段。
    """

    text: str
    voice: str
    repeat: int = 1


@dataclass
class Question:
    """
    一道听力题。

    question:
        题目正文

    options:
        四个选项

    dialogue:
        Part B 使用的男女对话。
    """

    number: int
    question: str = ""
    options: list[str] | None = None
    dialogue: list[tuple[str, str]] | None = None

    def __post_init__(self) -> None:
        if self.options is None:
            self.options = []

        if self.dialogue is None:
            self.dialogue = []


# ======================================================================
# 文本清洗
# ======================================================================

def clean_text(text: str) -> str:
    """
    清理 Markdown 和明显不应该朗读的格式。
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Markdown 链接：
    # [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    # 图片
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)

    # 粗体 / 斜体
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)

    # 行内代码
    text = re.sub(r"`([^`]*)`", r"\1", text)

    # HTML
    text = re.sub(r"<[^>]+>", " ", text)

    # 多余空白
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_line(line: str) -> str:
    """
    清洗单行 Markdown。
    """

    line = line.strip()

    if not line:
        return ""

    # Markdown 标题
    line = re.sub(r"^#{1,6}\s*", "", line)

    # Markdown 引用
    line = re.sub(r"^>\s*", "", line)

    # Markdown 列表
    line = re.sub(r"^[-*+]\s+", "", line)

    return clean_text(line).strip()


def normalize_for_match(text: str) -> str:
    """
    用于判断标题 / 标签的归一化。
    """

    text = clean_text(text)
    text = text.lower()
    text = re.sub(r"[\s:：\-—–_]+", "", text)

    return text


# ======================================================================
# 文件读取
# ======================================================================

def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{path}")

    return path.read_text(encoding="utf-8")


# ======================================================================
# Part A / B / C 区域提取
# ======================================================================

PART_A_PATTERN = re.compile(
    r"(?ims)"
    r"^\s*(?:#{1,6}\s*)?"
    r"(?:part\s*a\b|听力\s*part\s*a\b|第一部分.*?听句子)"
    r".*?"
    r"(?=^\s*(?:#{1,6}\s*)?(?:part\s*b\b|听力\s*part\s*b\b|第二部分.*?听对话)|\Z)"
)

PART_B_PATTERN = re.compile(
    r"(?ims)"
    r"^\s*(?:#{1,6}\s*)?"
    r"(?:part\s*b\b|听力\s*part\s*b\b|第二部分.*?听对话)"
    r".*?"
    r"(?=^\s*(?:#{1,6}\s*)?(?:part\s*c\b|听力\s*part\s*c\b|第三部分.*?听原文)|\Z)"
)

PART_C_PATTERN = re.compile(
    r"(?ims)"
    r"^\s*(?:#{1,6}\s*)?"
    r"(?:part\s*c\b|听力\s*part\s*c\b|第三部分.*?听原文)"
    r".*?$"
)


def extract_part(text: str, part: str) -> str:
    """
    从 Markdown 中提取 Part A / B / C。
    """

    if part == "A":
        match = PART_A_PATTERN.search(text)
    elif part == "B":
        match = PART_B_PATTERN.search(text)
    elif part == "C":
        match = PART_C_PATTERN.search(text)
    else:
        raise ValueError(f"未知 Part：{part}")

    if not match:
        return ""

    return match.group(0).strip()


# ======================================================================
# 行解析
# ======================================================================

QUESTION_PATTERN = re.compile(
    r"^\s*(?:#{1,6}\s*)?"
    r"(?:"
    r"Q(?:uestion)?\.?\s*"
    r"|"
    r"第\s*(\d+)\s*题"
    r"|"
    r"(\d+)\s*[.)、．]"
    r")"
    r"(.*)$",
    re.IGNORECASE,
)

OPTION_PATTERN = re.compile(
    r"^\s*"
    r"(?:"
    r"$begin:math:text$\?\(\[ABCD\]\)$end:math:text$?"
    r"[\.\)、:：、\-—]\s*"
    r"|"
    r"([ABCD])\s+"
    r")"
    r"(.*)$",
    re.IGNORECASE,
)

SPEAKER_PATTERN = re.compile(
    r"^\s*(?:[-*]\s*)?"
    r"(male|female|man|woman|speaker\s*1|speaker\s*2|男|女|男声|女声)"
    r"\s*[:：\-—]\s*(.+)$",
    re.IGNORECASE,
)


def parse_question_header(line: str) -> tuple[int | None, str | None]:
    """
    识别题号。
    """

    match = QUESTION_PATTERN.match(line)

    if not match:
        return None, None

    number = match.group(1) or match.group(2)

    if number:
        try:
            number_int = int(number)
        except ValueError:
            number_int = None
    else:
        number_int = None

    body = match.group(3) or ""

    return number_int, clean_text(body)


def parse_option(line: str) -> tuple[str | None, str | None]:
    """
    识别 A/B/C/D 选项。
    """

    match = OPTION_PATTERN.match(line)

    if not match:
        return None, None

    letter = (match.group(1) or match.group(2) or "").upper()
    body = match.group(3) or ""

    return letter, clean_text(body)


def parse_speaker(line: str) -> tuple[str | None, str | None]:
    """
    识别 Male / Female。
    """

    match = SPEAKER_PATTERN.match(line)

    if not match:
        return None, None

    raw_speaker = match.group(1).lower()
    body = clean_text(match.group(2))

    if raw_speaker in {"male", "man", "speaker 1", "男", "男声"}:
        speaker = "male"
    elif raw_speaker in {"female", "woman", "speaker 2", "女", "女声"}:
        speaker = "female"
    else:
        speaker = None

    return speaker, body


# ======================================================================
# 通用题目解析
# ======================================================================

def parse_questions(text: str) -> list[Question]:
    """
    从一个 Part 中尽可能稳健地解析：

        题号
        题目
        A/B/C/D

    不依赖固定 Markdown 样式。
    """

    lines = text.splitlines()

    questions: list[Question] = []

    current: Question | None = None
    current_option: str | None = None

    generated_number = 0

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        # 忽略 Part 标题
        normalized = normalize_for_match(line)

        if normalized.startswith("parta"):
            continue

        if normalized.startswith("partb"):
            continue

        if normalized.startswith("partc"):
            continue

        # 题号
        q_number, q_body = parse_question_header(line)

        if q_number is not None:
            generated_number += 1

            current = Question(
                number=q_number,
                question=q_body,
                options=[],
                dialogue=[],
            )

            questions.append(current)
            current_option = None
            continue

        # 选项
        option_letter, option_body = parse_option(line)

        if option_letter and current is not None:
            current.options.append(
                f"{option_letter}. {option_body}"
            )
            current_option = option_letter
            continue

        # 普通文本
        if current is None:
            continue

        cleaned = clean_line(line)

        if not cleaned:
            continue

        # 如果当前正在读取选项，继续追加
        if current_option:
            for index, option in enumerate(current.options):
                prefix = option[:2].upper()

                if prefix == f"{current_option}.":
                    current.options[index] = (
                        option + " " + cleaned
                    )
                    break
        else:
            if current.question:
                current.question += " " + cleaned
            else:
                current.question = cleaned

    return questions


# ======================================================================
# Part B 专用：男女对话解析
# ======================================================================

def parse_dialogue_blocks(text: str) -> list[tuple[str, str]]:
    """
    解析：

        Male: ...
        Female: ...
        Male: ...

    返回：

        [
            ("male", "..."),
            ("female", "..."),
            ...
        ]

    只接受明确的 Male / Female / Man / Woman / 男 / 女。

    不猜测 Speaker 1 / Speaker 2 的性别。
    """

    dialogue: list[tuple[str, str]] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        speaker, body = parse_speaker(line)

        if speaker and body:
            dialogue.append((speaker, body))

    return dialogue


def attach_dialogues(
    questions: list[Question],
    text: str,
) -> list[Question]:
    """
    将文本中按题号分组的男女对话尽可能附加到题目。

    如果没有办法按题号精确分组，则把整段对话作为
    当前 Part B 的连续对话使用。
    """

    lines = text.splitlines()

    grouped: dict[int, list[tuple[str, str]]] = {}

    current_number: int | None = None

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        q_number, _ = parse_question_header(line)

        if q_number is not None:
            current_number = q_number
            grouped.setdefault(current_number, [])
            continue

        speaker, body = parse_speaker(line)

        if speaker and body and current_number is not None:
            grouped[current_number].append((speaker, body))

    if grouped:
        for question in questions:
            question.dialogue = grouped.get(question.number, [])

    return questions


# ======================================================================
# 答案文件中的听力原文
# ======================================================================

def find_listening_transcript(text: str, part: str) -> str:
    """
    尝试从答案与解析中找到对应 Listening Part。

    支持：

        Listening A
        Listening B
        Listening C
        Part A
        Part B
        Part C
        听力 A
        听力 B
        听力 C
    """

    patterns = {
        "A": re.compile(
            r"(?is)"
            r"^\s*(?:#{1,6}\s*)?"
            r"(?:"
            r"listening\s*a\b"
            r"|听力\s*a\b"
            r"|part\s*a\b"
            r")"
            r".*?"
            r"(?=^\s*(?:#{1,6}\s*)?(?:listening\s*b\b|听力\s*b\b|part\s*b\b)|\Z)"
            ,
            re.MULTILINE,
        ),
        "B": re.compile(
            r"(?is)"
            r"^\s*(?:#{1,6}\s*)?"
            r"(?:"
            r"listening\s*b\b"
            r"|听力\s*b\b"
            r"|part\s*b\b"
            r")"
            r".*?"
            r"(?=^\s*(?:#{1,6}\s*)?(?:listening\s*c\b|听力\s*c\b|part\s*c\b)|\Z)"
            ,
            re.MULTILINE,
        ),
        "C": re.compile(
            r"(?is)"
            r"^\s*(?:#{1,6}\s*)?"
            r"(?:"
            r"listening\s*c\b"
            r"|听力\s*c\b"
            r"|part\s*c\b"
            r")"
            r".*$"
            ,
            re.MULTILINE,
        ),
    }

    match = patterns[part].search(text)

    if not match:
        return ""

    return match.group(0).strip()


# ======================================================================
# 选项标准化
# ======================================================================

def ensure_four_options(question: Question) -> None:
    """
    对选项做轻量清理。

    不伪造缺失选项。
    """

    cleaned: list[str] = []

    for option in question.options:
        option = clean_text(option)

        if option:
            cleaned.append(option)

    question.options = cleaned[:4]


# ======================================================================
# Part A Segment 构造
# ======================================================================

def build_part_a_segments(
    questions: list[Question],
    female_voice: str,
) -> list[Segment]:
    """
    Part A：

        女声

        每道题：
            题目 + 四个选项

        整题播放两遍。
    """

    segments: list[Segment] = []

    for question in questions:
        ensure_four_options(question)

        if not question.question:
            continue

        question_parts = [
            question.question
        ]

        question_parts.extend(question.options)

        full_question = " ".join(
            x for x in question_parts if x
        ).strip()

        if not full_question:
            continue

        # 整道题播放两遍
        segments.append(
            Segment(
                text=full_question,
                voice=female_voice,
                repeat=2,
            )
        )

    return segments


# ======================================================================
# Part B Segment 构造
# ======================================================================

def build_part_b_segments(
    questions: list[Question],
    female_voice: str,
    male_voice: str,
) -> list[Segment]:
    """
    Part B：

        明确 Male / Female。

        整段对话完整播放两遍。

        然后播放选项。

    重要：

        不能把每一句单独 repeat=2。

    正确结构：

        Male 1
        Female 1
        Male 2
        Female 2

        Male 1
        Female 1
        Male 2
        Female 2

        A
        B
        C
        D
    """

    segments: list[Segment] = []

    for question in questions:
        ensure_four_options(question)

        dialogue = question.dialogue or []

        if dialogue:
            # 第一遍完整对话
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

            # 第二遍完整对话
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

        # 选项使用女声
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
# Part C Segment 构造
# ======================================================================

def extract_part_c_passage(text: str) -> str:
    """
    从 Part C 中尽量提取文章原文。

    规则：

        在第一道题之前的正文作为文章。

    不把题目和选项读进文章。
    """

    lines = text.splitlines()

    passage_lines: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        q_number, _ = parse_question_header(line)

        if q_number is not None:
            break

        # 跳过 Part C 标题
        normalized = normalize_for_match(line)

        if normalized.startswith("partc"):
            continue

        cleaned = clean_line(line)

        if cleaned:
            passage_lines.append(cleaned)

    return " ".join(passage_lines).strip()


def build_part_c_segments(
    passage: str,
    questions: list[Question],
    female_voice: str,
) -> list[Segment]:
    """
    Part C：

        文章：
            女声 ×1

        每道题：
            题目 ×2
            A ×2
            B ×2
            C ×2
            D ×2
    """

    segments: list[Segment] = []

    if passage:
        segments.append(
            Segment(
                text=passage,
                voice=female_voice,
                repeat=1,
            )
        )

    for question in questions:
        ensure_four_options(question)

        if question.question:
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
# Kokoro 加载
# ======================================================================

def load_kokoro():
    """
    加载仓库内 Kokoro 模型。
    """

    try:
        from kokoro_onnx import Kokoro
    except ImportError as exc:
        print()
        print("=" * 70)
        print("❌ AUDIO GENERATION FAILED")
        print("=" * 70)
        print()
        print("无法导入 kokoro_onnx。")
        print()
        print("请确认 requirements.txt 包含：")
        print()
        print("    kokoro-onnx")
        print("    numpy")
        print("    soundfile")
        print()
        print(f"Python 错误：{exc}")
        print("=" * 70)
        raise

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Kokoro 模型不存在：{MODEL_PATH}"
        )

    if not VOICES_PATH.exists():
        raise FileNotFoundError(
            f"Kokoro voices 不存在：{VOICES_PATH}"
        )

    print()
    print("Loading Kokoro...")
    print(f"MODEL  : {MODEL_PATH}")
    print(f"VOICES : {VOICES_PATH}")

    kokoro = Kokoro(
        str(MODEL_PATH),
        str(VOICES_PATH),
    )

    print("✓ Kokoro loaded")

    return kokoro


# ======================================================================
# 单段 TTS
# ======================================================================

def synthesize_segment(
    kokoro,
    segment: Segment,
    speed: float,
):
    """
    使用 Kokoro 生成一个 Segment。
    """

    import numpy as np

    text = clean_text(segment.text)

    if not text:
        return np.array([], dtype=np.float32), 24000

    audio, sample_rate = kokoro.create(
        text,
        voice=segment.voice,
        speed=speed,
        lang=DEFAULT_LANGUAGE,
    )

    audio = np.asarray(audio, dtype=np.float32)

    return audio, int(sample_rate)


# ======================================================================
# 音频拼接
# ======================================================================

def make_silence(
    sample_rate: int,
    seconds: float,
):
    import numpy as np

    count = max(
        0,
        int(sample_rate * seconds),
    )

    return np.zeros(
        count,
        dtype=np.float32,
    )


def concatenate_audio(
    chunks: Iterable,
    sample_rate: int,
):
    import numpy as np

    valid = [
        chunk
        for chunk in chunks
        if chunk is not None and len(chunk) > 0
    ]

    if not valid:
        return np.array([], dtype=np.float32)

    return np.concatenate(valid)


# ======================================================================
# 输出 WAV
# ======================================================================

def write_wav(
    audio,
    sample_rate: int,
    path: Path,
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
# FFmpeg 转码
# ======================================================================

def require_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")

    if not ffmpeg:
        raise RuntimeError(
            "找不到 ffmpeg。"
            "请在 GitHub Actions Workflow 中安装 ffmpeg。"
        )

    return ffmpeg


def convert_audio(
    source_wav: Path,
    output_path: Path,
    audio_format: str,
) -> None:
    """
    WAV -> mp3 / m4a / wav
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if audio_format == "wav":
        shutil.copy2(
            source_wav,
            output_path,
        )
        return

    ffmpeg = require_ffmpeg()

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
        raise ValueError(
            f"不支持的音频格式：{audio_format}"
        )

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(source_wav),
        *codec_args,
        str(output_path),
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)

        raise RuntimeError(
            f"FFmpeg 转码失败：{output_path.name}"
        )


# ======================================================================
# 生成单个 Listening
# ======================================================================

def generate_audio_file(
    kokoro,
    segments: list[Segment],
    output_path: Path,
    audio_format: str,
    speed: float,
    label: str,
) -> None:
    """
    根据 Segment 列表生成一个完整音频。
    """

    if not segments:
        raise RuntimeError(
            f"{label} 没有可生成的音频内容。"
        )

    import numpy as np

    print()
    print("=" * 70)
    print(f"生成 {label}")
    print("=" * 70)
    print(f"Segments : {len(segments)}")
    print(f"Output   : {output_path}")

    all_chunks = []

    sample_rate: int | None = None

    for index, segment in enumerate(segments, start=1):
        text = clean_text(segment.text)

        if not text:
            continue

        print(
            f"  [{index:03d}/{len(segments):03d}] "
            f"{segment.voice:<10} "
            f"repeat={segment.repeat} "
            f"chars={len(text)}"
        )

        for repeat_index in range(segment.repeat):
            audio, sr = synthesize_segment(
                kokoro,
                segment,
                speed,
            )

            if sample_rate is None:
                sample_rate = sr

            if sr != sample_rate:
                raise RuntimeError(
                    f"{label} 出现不一致的采样率："
                    f"{sample_rate} / {sr}"
                )

            if len(audio) == 0:
                continue

            all_chunks.append(audio)

            # 同一内容重复播放之间留一点停顿
            if repeat_index < segment.repeat - 1:
                all_chunks.append(
                    make_silence(
                        sample_rate,
                        0.65,
                    )
                )

        # 不同片段之间留一点停顿
        all_chunks.append(
            make_silence(
                sample_rate,
                0.30,
            )
        )

    if sample_rate is None:
        raise RuntimeError(
            f"{label} 没有生成有效音频。"
        )

    audio = concatenate_audio(
        all_chunks,
        sample_rate,
    )

    if len(audio) == 0:
        raise RuntimeError(
            f"{label} 最终音频为空。"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_wav = Path(temp_dir) / f"{label}.wav"

        write_wav(
            audio,
            sample_rate,
            temp_wav,
        )

        convert_audio(
            temp_wav,
            output_path,
            audio_format,
        )

    print(
        f"✓ {label} 完成："
        f"{output_path.name}"
    )


# ======================================================================
# 合并 A / B / C
# ======================================================================

def concat_with_ffmpeg(
    input_files: list[Path],
    output_path: Path,
    audio_format: str,
) -> None:
    """
    使用 FFmpeg 将已经生成好的：

        A
        B
        C

    严格按照顺序直接拼接。

    不重新 TTS。
    """

    if not input_files:
        raise RuntimeError(
            "没有可以合并的音频文件。"
        )

    for path in input_files:
        if not path.exists():
            raise FileNotFoundError(
                f"无法合并，文件不存在：{path}"
            )

    ffmpeg = require_ffmpeg()

    with tempfile.TemporaryDirectory() as temp_dir:
        concat_file = Path(temp_dir) / "concat.txt"

        lines = []

        for path in input_files:
            escaped = str(path.resolve()).replace(
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
            str(output_path),
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)

            raise RuntimeError(
                "Listening 总音频合并失败。"
            )


# ======================================================================
# 文件路径
# ======================================================================

def build_paths(
    date: str,
    difficulty: int,
    article_type: str,
):
    day_dir = OUTPUT_ROOT / date
    exam_dir = day_dir / "配套试卷"
    listening_dir = exam_dir / "听力"

    exam_file = (
        exam_dir
        / f"{difficulty}星_{article_type}_试卷.md"
    )

    answer_file = (
        exam_dir
        / f"{difficulty}星_{article_type}_答案与解析.md"
    )

    return (
        day_dir,
        exam_dir,
        listening_dir,
        exam_file,
        answer_file,
    )


# ======================================================================
# 解析整个听力
# ======================================================================

def build_listening_segments(
    exam_text: str,
    answer_text: str,
    female_voice: str,
    male_voice: str,
):
    """
    解析 A/B/C。

    优先使用试卷。

    如果 Part B 的试卷没有明确 Male/Female 对话，
    再从答案与解析中的听力原文寻找。
    """

    # ------------------------------------------------------------------
    # Part A
    # ------------------------------------------------------------------

    part_a_exam = extract_part(
        exam_text,
        "A",
    )

    part_a_questions = parse_questions(
        part_a_exam
    )

    part_a_segments = build_part_a_segments(
        part_a_questions,
        female_voice,
    )

    # ------------------------------------------------------------------
    # Part B
    # ------------------------------------------------------------------

    part_b_exam = extract_part(
        exam_text,
        "B",
    )

    part_b_questions = parse_questions(
        part_b_exam
    )

    part_b_questions = attach_dialogues(
        part_b_questions,
        part_b_exam,
    )

    # 如果试卷中没有明确的男女对话，
    # 从答案与解析中的 Listening B 寻找。
    if not any(
        question.dialogue
        for question in part_b_questions
    ):
        part_b_answer = find_listening_transcript(
            answer_text,
            "B",
        )

        part_b_questions = attach_dialogues(
            part_b_questions,
            part_b_answer,
        )

    part_b_segments = build_part_b_segments(
        part_b_questions,
        female_voice,
        male_voice,
    )

    # ------------------------------------------------------------------
    # Part C
    # ------------------------------------------------------------------

    part_c_exam = extract_part(
        exam_text,
        "C",
    )

    part_c_passage = extract_part_c_passage(
        part_c_exam
    )

    part_c_questions = parse_questions(
        part_c_exam
    )

    # 如果试卷中没有 C，则尝试答案文件。
    if not part_c_passage or not part_c_questions:
        part_c_answer = find_listening_transcript(
            answer_text,
            "C",
        )

        if not part_c_passage:
            part_c_passage = extract_part_c_passage(
                part_c_answer
            )

        if not part_c_questions:
            part_c_questions = parse_questions(
                part_c_answer
            )

    part_c_segments = build_part_c_segments(
        part_c_passage,
        part_c_questions,
        female_voice,
    )

    return (
        part_a_segments,
        part_b_segments,
        part_c_segments,
    )


# ======================================================================
# 验证
# ======================================================================

def validate_source_files(
    exam_file: Path,
    answer_file: Path,
) -> None:
    if not exam_file.exists():
        raise FileNotFoundError(
            f"试卷不存在：{exam_file}"
        )

    if not answer_file.exists():
        raise FileNotFoundError(
            f"答案与解析不存在：{answer_file}"
        )

    if exam_file.stat().st_size == 0:
        raise RuntimeError(
            f"试卷为空：{exam_file}"
        )

    if answer_file.stat().st_size == 0:
        raise RuntimeError(
            f"答案与解析为空：{answer_file}"
        )


def validate_generated_files(
    files: list[Path],
) -> None:
    for path in files:
        if not path.exists():
            raise RuntimeError(
                f"音频生成失败，文件不存在：{path}"
            )

        if path.stat().st_size <= 0:
            raise RuntimeError(
                f"音频生成失败，文件为空：{path}"
            )


# ======================================================================
# CLI
# ======================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "748686 英语学习系统 "
            "Audio Generator V2.2"
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
        help="试卷 Markdown 文件",
    )

    parser.add_argument(
        "--answer-file",
        required=True,
        help="答案与解析 Markdown 文件",
    )

    parser.add_argument(
        "--audio-format",
        choices=sorted(SUPPORTED_FORMATS),
        default="mp3",
        help="音频格式",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help="Kokoro 播放速度",
    )

    parser.add_argument(
        "--male-voice",
        default=DEFAULT_MALE_VOICE,
        help="男声",
    )

    parser.add_argument(
        "--female-voice",
        default=DEFAULT_FEMALE_VOICE,
        help="女声",
    )

    return parser.parse_args()


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:
    args = parse_args()

    if args.speed <= 0:
        raise ValueError(
            f"speed 必须大于 0：{args.speed}"
        )

    audio_format = args.audio_format.lower()

    exam_file = Path(args.exam_file).resolve()
    answer_file = Path(args.answer_file).resolve()

    output_dir = (
        exam_file.parent
        / "听力"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("=" * 70)
    print("748686 英语学习系统")
    print("Audio Generator V2.2")
    print("=" * 70)
    print(f"DATE        : {args.date}")
    print(f"FORMAT      : {audio_format}")
    print(f"SPEED       : {args.speed}")
    print(f"LANGUAGE    : {DEFAULT_LANGUAGE}")
    print(f"MALE VOICE  : {args.male_voice}")
    print(f"FEMALE VOICE: {args.female_voice}")
    print(f"EXAM        : {exam_file}")
    print(f"ANSWER      : {answer_file}")
    print(f"OUTPUT      : {output_dir}")

    # ------------------------------------------------------------------
    # Source validation
    # ------------------------------------------------------------------

    validate_source_files(
        exam_file,
        answer_file,
    )

    exam_text = read_text(exam_file)
    answer_text = read_text(answer_file)

    # ------------------------------------------------------------------
    # Build segments BEFORE loading model
    # ------------------------------------------------------------------

    print()
    print("-" * 70)
    print("解析 Listening A / B / C")
    print("-" * 70)

    (
        part_a_segments,
        part_b_segments,
        part_c_segments,
    ) = build_listening_segments(
        exam_text,
        answer_text,
        args.female_voice,
        args.male_voice,
    )

    print(
        f"✓ Listening A segments："
        f"{len(part_a_segments)}"
    )

    print(
        f"✓ Listening B segments："
        f"{len(part_b_segments)}"
    )

    print(
        f"✓ Listening C segments："
        f"{len(part_c_segments)}"
    )

    if not part_a_segments:
        raise RuntimeError(
            "Listening A 没有解析出有效内容。"
        )

    if not part_b_segments:
        raise RuntimeError(
            "Listening B 没有解析出有效内容。"
        )

    if not part_c_segments:
        raise RuntimeError(
            "Listening C 没有解析出有效内容。"
        )

    # ------------------------------------------------------------------
    # Load Kokoro
    # ------------------------------------------------------------------

    kokoro = load_kokoro()

    # ------------------------------------------------------------------
    # Output files
    # ------------------------------------------------------------------

    extension = audio_format

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

    # 删除旧的输出，避免旧文件被误认为本次成功
    for path in [
        listening_a,
        listening_b,
        listening_c,
        listening_total,
    ]:
        if path.exists():
            path.unlink()

    # ------------------------------------------------------------------
    # Generate A
    # ------------------------------------------------------------------

    generate_audio_file(
        kokoro=kokoro,
        segments=part_a_segments,
        output_path=listening_a,
        audio_format=audio_format,
        speed=args.speed,
        label="Listening A",
    )

    # ------------------------------------------------------------------
    # Generate B
    # ------------------------------------------------------------------

    generate_audio_file(
        kokoro=kokoro,
        segments=part_b_segments,
        output_path=listening_b,
        audio_format=audio_format,
        speed=args.speed,
        label="Listening B",
    )

    # ------------------------------------------------------------------
    # Generate C
    # ------------------------------------------------------------------

    generate_audio_file(
        kokoro=kokoro,
        segments=part_c_segments,
        output_path=listening_c,
        audio_format=audio_format,
        speed=args.speed,
        label="Listening C",
    )

    # ------------------------------------------------------------------
    # Verify A/B/C
    # ------------------------------------------------------------------

    validate_generated_files(
        [
            listening_a,
            listening_b,
            listening_c,
        ]
    )

    print()
    print("=" * 70)
    print("A / B / C 全部生成成功")
    print("=" * 70)

    # ------------------------------------------------------------------
    # Total audio
    # ------------------------------------------------------------------

    print()
    print("正在合并 Listening 总音频：")
    print()
    print("    Listening A")
    print("        ↓")
    print("    Listening B")
    print("        ↓")
    print("    Listening C")
    print("        ↓")
    print("    Listening 总音频")

    concat_with_ffmpeg(
        input_files=[
            listening_a,
            listening_b,
            listening_c,
        ],
        output_path=listening_total,
        audio_format=audio_format,
    )

    # ------------------------------------------------------------------
    # Final validation
    # ------------------------------------------------------------------

    validate_generated_files(
        [
            listening_a,
            listening_b,
            listening_c,
            listening_total,
        ]
    )

    print()
    print("=" * 70)
    print("748686 英语学习系统")
    print("AUDIO GENERATION COMPLETE")
    print("=" * 70)

    print()
    print("✓ Listening A")
    print(f"  {listening_a}")

    print()
    print("✓ Listening B")
    print(f"  {listening_b}")

    print()
    print("✓ Listening C")
    print(f"  {listening_c}")

    print()
    print("✓ Listening 总音频")
    print(f"  {listening_total}")

    print()
    print("=" * 70)
    print("全部音频生成完成")
    print("=" * 70)


# ======================================================================
# ENTRY
# ======================================================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print()
        print("❌ 用户中断音频生成。")
        sys.exit(130)

    except Exception as exc:
        print()
        print("=" * 70)
        print("❌ AUDIO GENERATION FAILED")
        print("=" * 70)
        print()
        print(str(exc))
        print()
        print("=" * 70)

        sys.exit(1)
