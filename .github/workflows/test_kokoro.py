#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Kokoro 独立加载测试
TEST ONLY

职责：
    1. 检查 Kokoro ONNX 模型文件
    2. 检查 voices 文件
    3. 尝试加载 Kokoro
    4. 随机生成一段英文测试音频
    5. 不读取试卷
    6. 不读取答案
    7. 不调用任何 AI API
    8. 不修改英语学习系统其它文件

测试输出：
    02_英语学习系统/output/kokoro_test/kokoro_test.mp3
"""

from __future__ import annotations

import random
import sys
import time
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_DIR = PROJECT_ROOT / "models" / "kokoro"

MODEL_PATH = MODEL_DIR / "kokoro-v1.1-zh.fp16.onnx"
VOICES_PATH = MODEL_DIR / "voices-v1.1-zh.bin"

OUTPUT_DIR = PROJECT_ROOT / "output" / "kokoro_test"
OUTPUT_PATH = OUTPUT_DIR / "kokoro_test.mp3"


# ============================================================
# TEST CONFIG
# ============================================================

LANGUAGE = "en-us"
VOICE = "af_sarah"
SPEED = 1.0

TEST_SENTENCES = [
    "This is a test of the Kokoro text to speech system.",
    "The local Kokoro model is being loaded successfully.",
    "If you can hear this sentence, the audio generation test has passed.",
    "Today is a good day to learn something new.",
    "This is a completely local audio generation test.",
]


# ============================================================
# PRINT HELPERS
# ============================================================

def line():
    print("=" * 70)


def section(title: str):
    print()
    line()
    print(title)
    line()


def fail(message: str):
    print()
    print("❌ TEST FAILED")
    print()
    print(message)
    print()
    sys.exit(1)


# ============================================================
# FILE CHECK
# ============================================================

def check_file(path: Path, name: str):
    print(f"  {name}")
    print(f"    Path : {path}")

    if not path.exists():
        fail(
            f"{name} 不存在：\n"
            f"{path}"
        )

    if not path.is_file():
        fail(
            f"{name} 不是普通文件：\n"
            f"{path}"
        )

    size = path.stat().st_size

    print(f"    Size : {size:,} bytes")

    if size == 0:
        fail(
            f"{name} 是空文件：\n"
            f"{path}"
        )

    return size


# ============================================================
# LFS / FILE HEADER CHECK
# ============================================================

def check_model_content():
    section("MODEL FILE CONTENT CHECK")

    try:
        with MODEL_PATH.open("rb") as f:
            header = f.read(512)
    except Exception as exc:
        fail(f"无法读取 ONNX 文件：{exc}")

    # Git LFS pointer is plain text.
    header_text = header.decode("utf-8", errors="ignore")

    if "version https://git-lfs.github.com/spec/v1" in header_text:
        print("  ❌ 检测到 Git LFS pointer 文件")
        print()
        print("  当前 ONNX 文件不是实际模型，而是 Git LFS 指针。")
        print()
        print("  文件开头：")
        print(header_text[:300])
        fail(
            "请先确保 GitHub Actions checkout 时真正下载了 Git LFS 文件。"
        )

    # ONNX files are binary protobuf files.
    # A text file beginning with obvious markdown / HTML is suspicious.
    suspicious_prefixes = [
        "<html",
        "<!doctype",
        "404:",
        "error",
        "version https://",
    ]

    lower_text = header_text.lower().strip()

    for prefix in suspicious_prefixes:
        if lower_text.startswith(prefix):
            print("  ❌ ONNX 文件看起来不是二进制模型文件")
            print()
            print(header_text[:300])
            fail(
                "ONNX 文件内容异常，可能是下载错误、Git LFS 指针或错误文件。"
            )

    print("  ✓ ONNX 文件不是 Git LFS pointer")
    print("  ✓ ONNX 文件头可以读取")
    print()
    print("  前 32 bytes:")

    print("   ", header[:32].hex(" "))


# ============================================================
# IMPORT KOKORO
# ============================================================

def import_kokoro():
    section("IMPORT KOKORO")

    try:
        from kokoro_onnx import Kokoro
    except Exception as exc:
        print("  ❌ 无法导入 kokoro_onnx")
        print()
        print(f"  Error: {type(exc).__name__}: {exc}")
        fail(
            "请确认 GitHub Actions / 当前 Python 环境已经安装 kokoro-onnx。"
        )

    print("  ✓ kokoro_onnx import 成功")

    return Kokoro


# ============================================================
# LOAD MODEL
# ============================================================

def load_model(Kokoro):
    section("LOAD KOKORO MODEL")

    print("  Model :")
    print(f"    {MODEL_PATH}")

    print()
    print("  Voices :")
    print(f"    {VOICES_PATH}")

    print()
    print("  Language :", LANGUAGE)
    print("  Voice    :", VOICE)
    print("  Speed    :", SPEED)

    print()
    print("  → 正在加载 Kokoro ...")

    started = time.time()

    try:
        kokoro = Kokoro(
            str(MODEL_PATH),
            str(VOICES_PATH),
        )
    except Exception as exc:
        elapsed = time.time() - started

        print()
        print(f"  加载耗时: {elapsed:.2f}s")
        print()
        print("  ❌ Kokoro 模型加载失败")
        print()
        print(f"  Error Type:")
        print(f"    {type(exc).__name__}")
        print()
        print(f"  Error:")
        print(f"    {exc}")
        print()

        fail(
            "模型文件存在，但 Kokoro 无法加载它。\n\n"
            "如果这里出现 INVALID_PROTOBUF，重点检查 ONNX 文件本身，"
            "而不是 audio_generate.py。"
        )

    elapsed = time.time() - started

    print()
    print(f"  ✓ Kokoro 模型加载成功")
    print(f"  ✓ Loading time: {elapsed:.2f}s")

    return kokoro


# ============================================================
# GENERATE AUDIO
# ============================================================

def generate_audio(kokoro):
    section("GENERATE RANDOM TEST AUDIO")

    text = random.choice(TEST_SENTENCES)

    print("  Random test sentence:")
    print()
    print(f"    {text}")
    print()

    print("  → 正在生成音频 ...")

    started = time.time()

    try:
        samples, sample_rate = kokoro.create(
            text,
            voice=VOICE,
            speed=SPEED,
            lang=LANGUAGE,
        )
    except TypeError:
        # 某些 kokoro-onnx 版本参数名可能不同。
        # 第二种调用方式作为兼容测试。
        try:
            samples, sample_rate = kokoro.create(
                text,
                voice=VOICE,
                speed=SPEED,
                lang=LANGUAGE,
            )
        except Exception as exc:
            elapsed = time.time() - started

            print()
            print(f"  Generation time: {elapsed:.2f}s")
            print()
            print("  ❌ 音频生成失败")
            print()
            print(f"  Error Type:")
            print(f"    {type(exc).__name__}")
            print()
            print(f"  Error:")
            print(f"    {exc}")

            fail(
                "Kokoro 可以加载，但 create() 音频推理失败。"
            )
    except Exception as exc:
        elapsed = time.time() - started

        print()
        print(f"  Generation time: {elapsed:.2f}s")
        print()
        print("  ❌ 音频生成失败")
        print()
        print(f"  Error Type:")
        print(f"    {type(exc).__name__}")
        print()
        print(f"  Error:")
        print(f"    {exc}")

        fail(
            "Kokoro 模型加载成功，但实际 TTS 推理失败。"
        )

    elapsed = time.time() - started

    print(f"  ✓ Audio generation succeeded")
    print(f"  ✓ Generation time: {elapsed:.2f}s")

    if samples is None:
        fail("Kokoro 返回的 samples 是 None。")

    if sample_rate is None:
        fail("Kokoro 返回的 sample_rate 是 None。")

    try:
        sample_count = len(samples)
    except Exception:
        sample_count = 0

    if sample_count <= 0:
        fail("Kokoro 返回了空音频。")

    print(f"  ✓ Sample rate : {sample_rate}")
    print(f"  ✓ Samples     : {sample_count}")

    duration = sample_count / float(sample_rate)

    print(f"  ✓ Duration    : {duration:.2f}s")

    return samples, sample_rate


# ============================================================
# SAVE MP3
# ============================================================

def save_audio(samples, sample_rate):
    section("SAVE TEST AUDIO")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("  Output:")
    print(f"    {OUTPUT_PATH}")

    print()
    print("  → 正在写入 MP3 ...")

    try:
        import soundfile as sf
    except Exception as exc:
        fail(
            "无法导入 soundfile。\n"
            f"Error: {exc}"
        )

    try:
        import numpy as np
    except Exception as exc:
        fail(
            "无法导入 numpy。\n"
            f"Error: {exc}"
        )

    try:
        audio = np.asarray(samples)

        sf.write(
            str(OUTPUT_PATH),
            audio,
            sample_rate,
            format="MP3",
        )
    except Exception as exc:
        print()
        print("  ❌ MP3 写入失败")
        print()
        print(f"  Error Type:")
        print(f"    {type(exc).__name__}")
        print()
        print(f"  Error:")
        print(f"    {exc}")

        fail(
            "Kokoro 推理成功，但 MP3 文件写入失败。"
        )

    if not OUTPUT_PATH.exists():
        fail(
            "MP3 写入操作完成，但找不到输出文件：\n"
            f"{OUTPUT_PATH}"
        )

    size = OUTPUT_PATH.stat().st_size

    if size <= 0:
        fail(
            "MP3 文件生成了，但是文件大小为 0。"
        )

    print()
    print("  ✓ MP3 写入成功")
    print(f"  ✓ File size: {size:,} bytes")


# ============================================================
# MAIN
# ============================================================

def main():
    section("748686 英语学习系统")
    print("Kokoro Standalone Test")
    print()
    print("This test does NOT:")
    print("  - read exam files")
    print("  - read answer files")
    print("  - call AI")
    print("  - modify exam files")
    print("  - modify answer files")
    print("  - run the English learning pipeline")

    section("PATH CHECK")

    print("  Project root:")
    print(f"    {PROJECT_ROOT}")

    print()
    print("  Kokoro directory:")
    print(f"    {MODEL_DIR}")

    check_file(
        MODEL_PATH,
        "ONNX Model",
    )

    check_file(
        VOICES_PATH,
        "Voices",
    )

    check_model_content()

    Kokoro = import_kokoro()

    kokoro = load_model(Kokoro)

    samples, sample_rate = generate_audio(kokoro)

    save_audio(
        samples,
        sample_rate,
    )

    section("TEST COMPLETE")

    print("  ✓ Model files exist")
    print("  ✓ ONNX file is not an LFS pointer")
    print("  ✓ kokoro_onnx import succeeded")
    print("  ✓ Kokoro model loaded successfully")
    print("  ✓ TTS inference succeeded")
    print("  ✓ MP3 file generated successfully")

    print()
    print("  TEST RESULT: PASS")
    print()
    print(f"  Audio:")
    print(f"    {OUTPUT_PATH}")
    print()

    line()


if __name__ == "__main__":
    main()
