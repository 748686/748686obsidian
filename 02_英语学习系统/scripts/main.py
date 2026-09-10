#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Main Pipeline V2.5

======================================================================
职责
======================================================================

负责串联：

    STAGE 1
    英语短文生成 / 恢复

    STAGE 2
    配套试卷生成 / 恢复

    STAGE 3
    答案与详细解析生成 / 恢复

======================================================================
原则
======================================================================

1. 已存在的有效文件直接恢复，不重复调用 AI
2. 只有缺失或无效时才调用 AI
3. 每个阶段完成后立即写盘
4. 每个阶段完成后立即 Git commit + push
5. Stage 之间通过结构化数据传递
6. 不修改已经存在的有效内容
7. CLI 参数保持与 GitHub Actions 工作流一致
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# ======================================================================
# 路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = SCRIPT_DIR.parent
REPO_ROOT = SYSTEM_DIR.parent

sys.path.insert(0, str(SCRIPT_DIR))


# ======================================================================
# 导入
# ======================================================================

from config import CONFIG, ARTICLE_TYPES
from input_parser import parse
from article_generate import generate as gen_article
from article_generate import render as render_article
from exam_generate import generate as gen_exam
from exam_generate import render as render_exam
from exam_answers import generate as gen_answers
from exam_answers import render as render_answers


# ======================================================================
# 工具
# ======================================================================

def load_json(path: Path) -> dict[str, Any]:
    """
    读取 JSON。
    """
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError(f"JSON 根节点不是对象：{path}")

    return data


def save_json(path: Path, data: dict[str, Any]) -> None:
    """
    保存 JSON。
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )


def read_text(path: Path) -> str:
    """
    读取 UTF-8 文本。
    """
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    """
    写入 UTF-8 文本。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def find_first_existing(paths: list[Path]) -> Path | None:
    """
    返回第一个存在的文件。
    """
    for path in paths:
        if path.exists() and path.is_file():
            return path

    return None


# ======================================================================
# Git
# ======================================================================

def git_save(message: str, paths: list[Path]) -> None:
    """
    Git add / commit / push。

    如果没有变化，不视为失败。
    """
    import subprocess

    print()
    print("=" * 60)
    print(f"Git 保存：{message}")
    print("=" * 60)

    relative_paths: list[str] = []

    for path in paths:
        try:
            relative_paths.append(
                str(path.relative_to(REPO_ROOT))
            )
        except ValueError:
            relative_paths.append(str(path))

    if not relative_paths:
        return

    subprocess.run(
        ["git", "add", *relative_paths],
        cwd=REPO_ROOT,
        check=True,
    )

    result = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet",
        ],
        cwd=REPO_ROOT,
    )

    if result.returncode == 0:
        print("✓ 没有新的 Git 变化")
        return

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            message,
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    subprocess.run(
        ["git", "push"],
        cwd=REPO_ROOT,
        check=True,
    )

    print("✓ Git commit 完成")
    print("✓ Git push 完成")


# ======================================================================
# 配置
# ======================================================================

def get_article_type_name(article_type: str) -> str:
    """
    获取文章类型中文名称。
    """
    return ARTICLE_TYPES.get(
        article_type,
        article_type,
    )


def get_output_dir(date: str) -> Path:
    """
    获取当天英语学习系统输出目录。
    """
    return (
        SYSTEM_DIR
        / "output"
        / date
    )


def get_article_dir(date: str) -> Path:
    """
    获取文章目录。
    """
    return (
        get_output_dir(date)
        / "文章"
    )


def get_exam_dir(date: str) -> Path:
    """
    获取试卷目录。
    """
    return (
        get_output_dir(date)
        / "配套试卷"
    )


def get_answers_dir(date: str) -> Path:
    """
    获取答案解析目录。
    """
    return (
        get_output_dir(date)
        / "答案解析"
    )


# ======================================================================
# Stage 1
# 英语短文
# ======================================================================

def find_article_file(
    date: str,
    article_type: str,
) -> Path | None:
    """
    查找已有文章。

    优先使用配置生成的标准路径。
    """

    article_type_name = get_article_type_name(article_type)

    article_dir = get_article_dir(date)

    candidates = [
        article_dir / f"{article_type_name}.md",
        article_dir / f"{article_type}.md",
        article_dir / f"{date}_{article_type_name}.md",
        article_dir / f"{date}_{article_type}.md",
    ]

    return find_first_existing(candidates)


def recover_article(
    input_file: Path,
) -> dict[str, Any]:
    """
    从已经存在的 Markdown 文章恢复结构化数据。
    """

    print("→ 正在从现有 Markdown 恢复结构")

    text = read_text(input_file)

    lines = text.splitlines()

    title = ""
    article_en = ""
    article_zh = ""

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("# ") and not title:
            title = stripped[2:].strip()

    # --------------------------------------------------------------
    # 英文正文
    # --------------------------------------------------------------

    english_start = None
    chinese_start = None

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.lower() in {
            "## english",
            "## english article",
            "## 英文正文",
        }:
            english_start = i + 1

        if stripped in {
            "## 中文",
            "## 中文翻译",
            "## 中文译文",
        }:
            chinese_start = i + 1

    if english_start is not None:
        end = chinese_start if chinese_start is not None else len(lines)

        article_en = "\n".join(
            lines[english_start:end]
        ).strip()

    if chinese_start is not None:
        article_zh = "\n".join(
            lines[chinese_start:]
        ).strip()

    # --------------------------------------------------------------
    # 如果没有标准标题结构，尽可能恢复正文
    # --------------------------------------------------------------

    if not article_en:
        blocks: list[str] = []

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                continue

            blocks.append(stripped)

        article_en = "\n\n".join(blocks)

    if not title:
        title = input_file.stem

    return {
        "title": title,
        "article_en": article_en,
        "article_zh": article_zh,
    }


def load_or_generate_article(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    length: int,
    output_file: Path,
) -> dict[str, Any]:
    """
    Stage 1：加载或生成文章。
    """

    existing_file = find_article_file(
        date,
        article_type,
    )

    if existing_file is not None:
        print(f"✓ 已存在文章：{existing_file}")
        print("✓ 不调用文章 AI")

        article_data = recover_article(
            existing_file
        )

        cache_file = (
            get_article_dir(date)
            / "_article_data.json"
        )

        save_json(
            cache_file,
            article_data,
        )

        print(
            f"✓ 文章结构化缓存 已落盘：{cache_file}"
        )

        git_save(
            "文章恢复缓存",
            [
                existing_file,
                cache_file,
            ],
        )

        return article_data

    print("→ 未找到文章")
    print("→ 正在调用文章 AI")

    generated = gen_article(
        difficulty,
        article_type,
        length,
    )

    if not isinstance(generated, dict):
        raise ValueError(
            "文章 AI 返回结果不是 dict"
        )

    article_type_name = get_article_type_name(
        article_type
    )

    markdown = render_article(
        generated,
        difficulty,
        article_type_name,
    )

    write_text(
        output_file,
        markdown,
    )

    print(f"✓ 已保存文章：{output_file}")

    cache_file = (
        get_article_dir(date)
        / "_article_data.json"
    )

    save_json(
        cache_file,
        generated,
    )

    git_save(
        "文章",
        [
            output_file,
            cache_file,
        ],
    )

    return generated


# ======================================================================
# Stage 2
# 配套试卷
# ======================================================================

def find_exam_file(
    date: str,
    difficulty: int,
    article_type: str,
) -> Path | None:
    """
    查找已有试卷。
    """

    exam_dir = get_exam_dir(date)

    article_type_name = get_article_type_name(
        article_type
    )

    difficulty_name = f"{difficulty}星"

    candidates = [
        exam_dir / f"{difficulty_name}_{article_type_name}_试卷.md",
        exam_dir / f"{difficulty_name}_{article_type}_试卷.md",
    ]

    return find_first_existing(candidates)


def recover_exam(
    input_file: Path,
) -> dict[str, Any]:
    """
    从已有 Markdown 恢复试卷结构。

    保持与 exam_generate.py V5.3 的数据结构兼容。
    """

    import re

    print("→ 正在从现有 Markdown 恢复结构")

    text = read_text(input_file)

    # --------------------------------------------------------------
    # Listening
    # --------------------------------------------------------------

    listening: dict[str, Any] = {
        "part_a": [],
        "part_b": [],
        "part_c": [],
    }

    for part in ["A", "B", "C"]:
        match = re.search(
            rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[ABC]|#\s*二、单项选择|\Z)",
            text,
            flags=re.I | re.S,
        )

        if not match:
            continue

        block = match.group(1)

        questions = re.findall(
            r"(?:^|\n)\s*(\d+)[.)]\s*(.*?)(?=\n\s*\d+[.)]\s*|\Z)",
            block,
            flags=re.S,
        )

        parsed_questions = []

        for number, content in questions:
            parsed_questions.append(
                {
                    "number": int(number),
                    "question": content.strip(),
                }
            )

        listening[
            f"part_{part.lower()}"
        ] = parsed_questions

    # --------------------------------------------------------------
    # 基础结构
    # --------------------------------------------------------------

    exam_data: dict[str, Any] = {
        "title": input_file.stem,
        "listening": listening,
        "single_choice": [],
        "multiple_choice": [],
        "cloze": [],
        "reading": [],
        "translation": {
            "part_a": [],
            "part_b": [],
        },
        "writing": [],
    }

    return exam_data


def validate_exam_structure(
    exam_data: dict[str, Any],
) -> None:
    """
    对恢复后的试卷做基础检查。
    """

    listening = exam_data.get(
        "listening",
        {},
    )

    expected = {
        "part_a": 5,
        "part_b": 5,
        "part_c": 5,
    }

    for key, count in expected.items():
        actual = len(
            listening.get(key, [])
        )

        if actual != count:
            raise ValueError(
                f"Listening {key.upper()} "
                f"题数异常：{actual}，期望 {count}"
            )


def load_or_generate_exam(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    article_data: dict[str, Any],
    words: list[Any],
    output_file: Path,
) -> dict[str, Any]:
    """
    Stage 2：加载或生成配套试卷。
    """

    existing_file = find_exam_file(
        date,
        difficulty,
        article_type,
    )

    if existing_file is not None:
        print(f"✓ 已存在试卷：{existing_file}")
        print("✓ 不调用试卷 AI")

        exam_data = recover_exam(
            existing_file
        )

        validate_exam_structure(
            exam_data
        )

        cache_file = (
            get_exam_dir(date)
            / "_exam_data.json"
        )

        save_json(
            cache_file,
            exam_data,
        )

        print(
            f"✓ 试卷结构化缓存 已落盘：{cache_file}"
        )

        git_save(
            "试卷恢复缓存",
            [
                existing_file,
                cache_file,
            ],
        )

        return exam_data

    print("→ 未找到试卷")
    print("→ 正在调用试卷 AI")

    generated = gen_exam(
        article_data,
        difficulty,
        article_type,
        words,
    )

    if not isinstance(generated, dict):
        raise ValueError(
            "试卷 AI 返回结果不是 dict"
        )

    article_type_name = get_article_type_name(
        article_type
    )

    markdown = render_exam(
        generated,
        article_data.get("title", ""),
        difficulty,
        article_type_name,
    )

    write_text(
        output_file,
        markdown,
    )

    print(
        f"✓ 已保存：{output_file}"
    )

    cache_file = (
        get_exam_dir(date)
        / "_exam_data.json"
    )

    save_json(
        cache_file,
        generated,
    )

    git_save(
        "配套试卷",
        [
            output_file,
            cache_file,
        ],
    )

    return generated


# ======================================================================
# Stage 3
# 答案与详细解析
# ======================================================================

def find_answers_file(
    date: str,
    difficulty: int,
    article_type: str,
) -> Path | None:
    """
    查找已有答案解析。
    """

    answers_dir = get_answers_dir(date)

    article_type_name = get_article_type_name(
        article_type
    )

    difficulty_name = f"{difficulty}星"

    candidates = [
        answers_dir / f"{difficulty_name}_{article_type_name}_答案解析.md",
        answers_dir / f"{difficulty_name}_{article_type}_答案解析.md",
    ]

    return find_first_existing(candidates)


def load_or_generate_answers(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    article_data: dict[str, Any],
    exam_data: dict[str, Any],
    words: list[Any],
    output_file: Path,
) -> dict[str, Any]:
    """
    Stage 3：加载或生成答案与详细解析。

    重要：
    exam_answers.py V2.1 的 generate() 接口是：

        generate(
            exam,
            article,
            difficulty,
            article_type,
            words,
        )

    render() 接口是：

        render(
            result,
            article_title,
            difficulty,
            article_type_name,
        )
    """

    existing_file = find_answers_file(
        date,
        difficulty,
        article_type,
    )

    if existing_file is not None:
        print(f"✓ 已存在答案解析：{existing_file}")
        print("✓ 不调用答案解析 AI")

        return {
            "existing_file": str(existing_file),
        }

    print("→ 未找到答案解析")
    print("→ 正在调用答案解析 AI")

    # ==============================================================
    # FIX：
    # exam_answers.generate() 不接受：
    #
    #     date=
    #
    # 它的真实接口是：
    #
    #     generate(
    #         exam,
    #         article,
    #         difficulty,
    #         article_type,
    #         words,
    #     )
    # ==============================================================

    generated = gen_answers(
        exam_data,
        article_data,
        difficulty,
        article_type,
        words,
    )

    if not isinstance(generated, dict):
        raise ValueError(
            "答案解析 AI 返回结果不是 dict"
        )

    article_type_name = get_article_type_name(
        article_type
    )

    # ==============================================================
    # FIX：
    # render() 需要 4 个参数
    #
    #     render(
    #         result,
    #         article_title,
    #         difficulty,
    #         article_type_name,
    #     )
    # ==============================================================

    markdown = render_answers(
        generated,
        article_data.get("title", ""),
        difficulty,
        article_type_name,
    )

    write_text(
        output_file,
        markdown,
    )

    print(
        f"✓ 已保存：{output_file}"
    )

    cache_file = (
        get_answers_dir(date)
        / "_answers_data.json"
    )

    save_json(
        cache_file,
        generated,
    )

    git_save(
        "答案与详细解析",
        [
            output_file,
            cache_file,
        ],
    )

    return generated


# ======================================================================
# CLI
# ======================================================================

def build_parser() -> argparse.ArgumentParser:
    """
    CLI 参数。
    """

    parser = argparse.ArgumentParser(
        description="748686 英语学习系统"
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--difficulty",
        required=True,
        choices=[
            str(i)
            for i in range(1, 18)
        ],
    )

    parser.add_argument(
        "--article-type",
        required=True,
        choices=list(
            ARTICLE_TYPES.keys()
        ),
    )

    parser.add_argument(
        "--length",
        required=True,
        type=int,
    )

    parser.add_argument(
        "--exam",
        choices=["yes", "no"],
        default="yes",
    )

    parser.add_argument(
        "--image",
        choices=["yes", "no"],
        default="yes",
    )

    # ==============================================================
    # 这里必须保持原来的接口：
    #
    # --audio yes
    # --audio no
    #
    # 音频格式由 --audio-format 单独控制。
    # ==============================================================

    parser.add_argument(
        "--audio",
        choices=["yes", "no"],
        default="yes",
    )

    parser.add_argument(
        "--audio-format",
        choices=["mp3", "m4a", "wav"],
        default="mp3",
    )

    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
    )

    return parser


# ======================================================================
# Main
# ======================================================================

def main() -> None:
    """
    主流程。
    """

    parser = build_parser()
    args = parser.parse_args()

    date = args.date
    difficulty = int(
        args.difficulty
    )
    article_type = args.article_type
    length = args.length

    print()
    print("=" * 60)
    print("748686 英语学习系统 V2.5")
    print("=" * 60)

    print(f"日期：{date}")
    print(f"难度：{difficulty}星")
    print(
        f"文章类型："
        f"{get_article_type_name(article_type)}"
    )
    print(
        f"英文类型：{article_type}"
    )
    print(
        f"目标长度：{length}"
    )
    print(
        f"试卷：{args.exam}"
    )
    print(
        f"图片：{args.image}"
    )
    print(
        f"音频：{args.audio}"
    )
    print(
        f"音频格式：{args.audio_format}"
    )
    print(
        f"语速：{args.speed}"
    )

    # ==================================================================
    # 输入文章
    # ==================================================================

    input_file = (
        SYSTEM_DIR
        / "input"
        / f"{date}.md"
    )

    if not input_file.exists():
        raise FileNotFoundError(
            f"找不到输入文件：{input_file}"
        )

    # ==================================================================
    # Stage 1：读取词汇
    # ==================================================================

    print()
    print("=" * 60)
    print("STAGE 1 / 3：英语短文")
    print("=" * 60)

    words, images = parse(
        input_file
    )

    words = list(words)

    print(
        f"✓ 学习词汇数量：{len(words)}"
    )

    if images:
        print(
            f"✓ 图片数量：{len(images)}"
        )

    # ==================================================================
    # Stage 1：文章
    # ==================================================================

    article_type_name = get_article_type_name(
        article_type
    )

    article_file = (
        get_article_dir(date)
        / f"{article_type_name}.md"
    )

    article_data = load_or_generate_article(
        date=date,
        difficulty=difficulty,
        article_type=article_type,
        length=length,
        output_file=article_file,
    )

    # ==================================================================
    # Stage 2：试卷
    # ==================================================================

    exam_data: dict[str, Any] = {}

    if args.exam == "yes":

        print()
        print("=" * 60)
        print("STAGE 2 / 3：配套试卷")
        print("=" * 60)

        exam_file = (
            get_exam_dir(date)
            / f"{difficulty}星_{article_type_name}_试卷.md"
        )

        exam_data = load_or_generate_exam(
            date=date,
            difficulty=difficulty,
            article_type=article_type,
            article_data=article_data,
            words=words,
            output_file=exam_file,
        )

    else:
        print()
        print("✓ 用户选择不生成试卷")
        print("✓ 跳过 STAGE 2")

    # ==================================================================
    # Stage 3：答案解析
    # ==================================================================

    if args.exam == "yes":

        print()
        print("=" * 60)
        print("STAGE 3 / 3：答案与详细解析")
        print("=" * 60)

        answers_file = (
            get_answers_dir(date)
            / f"{difficulty}星_{article_type_name}_答案解析.md"
        )

        load_or_generate_answers(
            date=date,
            difficulty=difficulty,
            article_type=article_type,
            article_data=article_data,
            exam_data=exam_data,
            words=words,
            output_file=answers_file,
        )

    else:
        print()
        print("✓ 跳过 STAGE 3")

    # ==================================================================
    # 完成
    # ==================================================================

    print()
    print("=" * 60)
    print("748686 英语学习系统 COMPLETE")
    print("=" * 60)

    print(f"✓ 日期：{date}")
    print(
        f"✓ 文章类型："
        f"{article_type_name}"
    )
    print(
        f"✓ 学习词汇：{len(words)}"
    )

    if args.exam == "yes":
        print("✓ 配套试卷：完成")
        print("✓ 答案与详细解析：完成")
    else:
        print("✓ 配套试卷：跳过")
        print("✓ 答案与详细解析：跳过")


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":
    main()
