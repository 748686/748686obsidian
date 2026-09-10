#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Main Pipeline

======================================================================
职责
======================================================================

Stage 1：文章
    1. 读取输入
    2. 解析学习词汇
    3. 如果文章已存在，则直接恢复
    4. 如果不存在，则调用 Agnes 生成文章
    5. 渲染为 Obsidian Markdown
    6. 保存文章及结构化缓存

Stage 2：配套试卷
    1. 如果试卷已存在，则恢复试卷结构
    2. 如果不存在，则调用 exam_generate
    3. 渲染并保存试卷

Stage 3：答案与详细解析
    1. 如果答案解析已存在，则恢复
    2. 如果不存在，则调用 exam_answers
    3. 生成答案、详细解析、听力原文、总体学习分析
    4. 保存结果

======================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ======================================================================
# 路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = SCRIPT_DIR.parent
REPO_ROOT = SYSTEM_DIR.parent

# 确保 scripts 目录可以直接导入模块
sys.path.insert(0, str(SCRIPT_DIR))


# ======================================================================
# 项目模块
# ======================================================================

from common import CONFIG
from input_parser import parse

# 文章生成：真实文件是 agnes_generate.py
from agnes_generate import ARTICLE_TYPES
from agnes_generate import generate as gen_article

# 文章 Markdown 渲染：真实文件是 render_markdown.py
from render_markdown import render as render_article

# 试卷
from exam_generate import generate as gen_exam
from exam_generate import render as render_exam

# 答案与详细解析
from exam_answers import generate as gen_answers
from exam_answers import render as render_answers


# ======================================================================
# 通用工具
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ======================================================================
# 输入
# ======================================================================

def find_input_file(date: str) -> Path | None:
    """
    在英语学习系统中查找指定日期的输入文件。

    保留原有搜索策略，不创建不存在的目录。
    """

    candidates = [
        SYSTEM_DIR / "input" / f"{date}.md",
        SYSTEM_DIR / "input" / f"{date}.txt",
        SYSTEM_DIR / "输入" / f"{date}.md",
        SYSTEM_DIR / "输入" / f"{date}.txt",
    ]

    for path in candidates:
        if path.exists():
            return path

    return None


# ======================================================================
# Stage 1：文章
# ======================================================================

def recover_article_structure(
    article_path: Path,
) -> dict[str, Any] | None:
    """
    从已经存在的文章 Markdown 中恢复文章结构。

    这里只做基础恢复。
    """

    if not article_path.exists():
        return None

    text = read_text(article_path)

    if not text.strip():
        return None

    # 优先查找已有结构化缓存
    cache_candidates = [
        article_path.with_suffix(".json"),
        article_path.parent / f"{article_path.stem}_structure.json",
        article_path.parent / f"{article_path.stem}_cache.json",
    ]

    for cache_path in cache_candidates:
        if cache_path.exists():
            try:
                data = load_json(cache_path)
                if isinstance(data, dict):
                    return data
            except Exception:
                pass

    # 如果没有缓存，构造最基础的文章结构
    return {
        "title": article_path.stem,
        "title_zh": article_path.stem,
        "content": text,
        "article": text,
        "raw_markdown": text,
    }


def get_article_path(
    date: str,
    difficulty: int,
    article_type: str,
) -> Path:
    """
    获取文章输出路径。

    保留当前系统原有目录约定。
    """

    difficulty_name = f"{difficulty}星"
    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    article_dir = (
        SYSTEM_DIR
        / "output"
        / date
        / "文章"
    )

    return article_dir / f"{difficulty_name}_{article_type_name}_文章.md"


def get_article_cache_path(article_path: Path) -> Path:
    return article_path.with_name(
        f"{article_path.stem}_结构化缓存.json"
    )


def stage1_article(
    date: str,
    words: list,
    difficulty: int,
    article_type: str,
    length: int,
) -> tuple[dict[str, Any], Path]:

    log("=" * 60)
    log("STAGE 1 / 3：英语文章")
    log("=" * 60)

    log(f"→ 学习词汇数量：{len(words)}")
    log(
        f"→ 难度：{difficulty}星"
    )
    log(
        f"→ 文章类型："
        f"{ARTICLE_TYPES.get(article_type, article_type)}"
        f" / {article_type}"
    )
    log(f"→ 目标长度：{length}")

    article_path = get_article_path(
        date,
        difficulty,
        article_type,
    )

    cache_path = get_article_cache_path(article_path)

    # --------------------------------------------------------------
    # 已存在结构化缓存
    # --------------------------------------------------------------

    if cache_path.exists():
        log("✓ 已找到文章结构化缓存")
        log(f"→ {cache_path}")

        try:
            article_data = load_json(cache_path)

            if isinstance(article_data, dict):
                log("✓ 直接使用现有文章结构")
                return article_data, article_path

        except Exception as exc:
            log(f"⚠️ 结构化缓存读取失败：{exc}")

    # --------------------------------------------------------------
    # 已存在文章
    # --------------------------------------------------------------

    if article_path.exists():
        log(f"✓ 已存在文章：{article_path}")
        log("→ 不调用文章 AI")
        log("→ 正在从现有 Markdown 恢复结构")

        article_data = recover_article_structure(
            article_path
        )

        if article_data is None:
            raise RuntimeError(
                f"无法恢复现有文章：{article_path}"
            )

        save_json(
            cache_path,
            article_data,
        )

        log(
            f"✓ 文章结构化缓存已落盘："
            f"{cache_path}"
        )

        return article_data, article_path

    # --------------------------------------------------------------
    # 不存在文章 → 调用 Agnes
    # --------------------------------------------------------------

    log("→ 未找到文章")
    log("→ 正在调用文章 AI")

    article_data = gen_article(
        words,
        difficulty,
        article_type,
        length,
    )

    if not isinstance(article_data, dict):
        raise RuntimeError(
            "文章 AI 返回结果不是 dict"
        )

    # --------------------------------------------------------------
    # 渲染 Markdown
    # --------------------------------------------------------------

    markdown = render_article(
        article_data,
        words,
        difficulty,
        article_type,
        date,
        length,
    )

    write_text(
        article_path,
        markdown,
    )

    log(f"✓ 文章已保存：{article_path}")

    # --------------------------------------------------------------
    # 保存结构化缓存
    # --------------------------------------------------------------

    save_json(
        cache_path,
        article_data,
    )

    log(
        f"✓ 文章结构化缓存已保存："
        f"{cache_path}"
    )

    return article_data, article_path


# ======================================================================
# Stage 2：试卷
# ======================================================================

def get_exam_path(
    date: str,
    difficulty: int,
    article_type: str,
) -> Path:

    difficulty_name = f"{difficulty}星"

    return (
        SYSTEM_DIR
        / "output"
        / date
        / "配套试卷"
        / f"{difficulty_name}_{article_type}_试卷.md"
    )


def recover_exam(
    exam_path: Path,
) -> dict[str, Any] | None:
    """
    从已有试卷 Markdown 中恢复考试结构。

    保留现有恢复逻辑，特别是 Listening Part A/B/C
    的边界必须以 Part 标题或第二大题为结束条件。
    """

    if not exam_path.exists():
        return None

    text = read_text(exam_path)

    if not text.strip():
        return None

    exam: dict[str, Any] = {
        "raw_markdown": text,
        "title": "",
        "listening": {},
        "single_choice": {},
        "multiple_choice": {},
        "cloze": {},
        "reading": {},
        "translation": {},
        "writing": {},
    }

    # --------------------------------------------------------------
    # Listening
    # --------------------------------------------------------------

    for part in ["A", "B", "C"]:

        match = re.search(
            rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[ABC]|#\s*二、单项选择|\Z)",
            text,
            flags=re.I | re.S,
        )

        if match:
            content = match.group(1).strip()

            questions = re.findall(
                r"(?m)^\s*(\d+)[\.\、]\s*(.+)$",
                content,
            )

            exam["listening"][part] = {
                "content": content,
                "questions": [
                    {
                        "number": int(number),
                        "question": question.strip(),
                    }
                    for number, question in questions
                ],
            }

    # --------------------------------------------------------------
    # 基础标题
    # --------------------------------------------------------------

    title_match = re.search(
        r"^#\s+(.+)$",
        text,
        flags=re.M,
    )

    if title_match:
        exam["title"] = title_match.group(1).strip()

    return exam


def stage2_exam(
    article_data: dict[str, Any],
    article_path: Path,
    words: list,
    difficulty: int,
    article_type: str,
    date: str,
) -> tuple[dict[str, Any], Path]:

    log("")
    log("=" * 60)
    log("STAGE 2 / 3：配套试卷")
    log("=" * 60)

    exam_path = get_exam_path(
        date,
        difficulty,
        article_type,
    )

    # --------------------------------------------------------------
    # 已存在试卷
    # --------------------------------------------------------------

    if exam_path.exists():
        log(f"✓ 已存在试卷：{exam_path}")
        log("→ 不调用试卷 AI")
        log("→ 正在恢复试卷结构")

        exam_data = recover_exam(
            exam_path
        )

        if exam_data is not None:
            return exam_data, exam_path

        log("⚠️ 现有试卷无法恢复，将重新生成")

    # --------------------------------------------------------------
    # 调用试卷 AI
    # --------------------------------------------------------------

    log("→ 未找到可用试卷")
    log("→ 正在调用试卷 AI")

    generated = gen_exam(
        article_data,
        difficulty,
        article_type,
        words,
    )

    if not isinstance(generated, dict):
        raise RuntimeError(
            "试卷 AI 返回结果不是 dict"
        )

    # --------------------------------------------------------------
    # 渲染
    # --------------------------------------------------------------

    markdown = render_exam(
        generated,
        article_data.get("title", ""),
        difficulty,
        ARTICLE_TYPES.get(
            article_type,
            article_type,
        ),
    )

    write_text(
        exam_path,
        markdown,
    )

    log(f"✓ 已保存：{exam_path}")

    return generated, exam_path


# ======================================================================
# Stage 3：答案与详细解析
# ======================================================================

def get_answers_path(
    exam_path: Path,
) -> Path:

    return exam_path.with_name(
        exam_path.stem.replace(
            "_试卷",
            "_答案与解析",
        )
        + ".md"
    )


def recover_answers(
    answers_path: Path,
) -> dict[str, Any] | None:

    if not answers_path.exists():
        return None

    text = read_text(answers_path)

    if not text.strip():
        return None

    return {
        "raw_markdown": text,
    }


def stage3_answers(
    exam_data: dict[str, Any],
    article_data: dict[str, Any],
    article_path: Path,
    exam_path: Path,
    words: list,
    difficulty: int,
    article_type: str,
) -> Path:

    log("")
    log("=" * 60)
    log("STAGE 3 / 3：答案与详细解析")
    log("=" * 60)

    answers_path = get_answers_path(
        exam_path
    )

    # --------------------------------------------------------------
    # 已存在答案解析
    # --------------------------------------------------------------

    if answers_path.exists():
        log(f"✓ 已存在答案解析：{answers_path}")
        log("→ 不调用答案解析 AI")
        return answers_path

    log("→ 未找到答案解析")
    log("→ 正在调用答案解析 AI")

    # --------------------------------------------------------------
    # 调用答案解析 AI
    # --------------------------------------------------------------

    generated = gen_answers(
        exam_data,
        article_data,
        difficulty,
        article_type,
        words,
    )

    if not isinstance(generated, dict):
        raise RuntimeError(
            "答案解析 AI 返回结果不是 dict"
        )

    # --------------------------------------------------------------
    # 渲染
    # --------------------------------------------------------------

    article_title = article_data.get(
        "title",
        "",
    )

    article_type_name = ARTICLE_TYPES.get(
        article_type,
        article_type,
    )

    markdown = render_answers(
        generated,
        article_title,
        difficulty,
        article_type_name,
    )

    write_text(
        answers_path,
        markdown,
    )

    log(
        f"✓ 答案与详细解析已保存："
        f"{answers_path}"
    )

    return answers_path


# ======================================================================
# Git
# ======================================================================

def git_save(
    paths: list[Path],
    message: str,
) -> None:

    import subprocess

    existing = [
        p
        for p in paths
        if p.exists()
    ]

    if not existing:
        log("→ 没有需要 Git 保存的文件")
        return

    log("")
    log("=" * 60)
    log(f"Git 保存：{message}")
    log("=" * 60)

    relative_paths = [
        str(p.relative_to(REPO_ROOT))
        for p in existing
    ]

    subprocess.run(
        [
            "git",
            "add",
            *relative_paths,
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    status = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet",
        ],
        cwd=REPO_ROOT,
    )

    if status.returncode == 0:
        log("→ 没有新的 Git 变更")
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

    log("✓ Git commit 完成")

    subprocess.run(
        [
            "git",
            "push",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    log("✓ Git push 完成")


# ======================================================================
# CLI
# ======================================================================

def build_parser() -> argparse.ArgumentParser:

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
        type=int,
    )

    parser.add_argument(
        "--article-type",
        required=True,
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

    parser = build_parser()
    args = parser.parse_args()

    date = args.date
    difficulty = args.difficulty
    article_type = args.article_type
    length = args.length

    log("")
    log("=" * 60)
    log("748686 英语学习系统")
    log("=" * 60)

    log(f"日期：{date}")
    log(f"难度：{difficulty}星")
    log(
        f"文章类型："
        f"{ARTICLE_TYPES.get(article_type, article_type)}"
        f" / {article_type}"
    )
    log(f"目标长度：{length}")
    log(f"试卷：{args.exam}")
    log(f"图片：{args.image}")
    log(f"音频：{args.audio}")
    log(f"音频格式：{args.audio_format}")
    log(f"语速：{args.speed}")

    # --------------------------------------------------------------
    # 输入文件
    # --------------------------------------------------------------

    input_file = find_input_file(date)

    if input_file is None:
        raise FileNotFoundError(
            f"未找到 {date} 的输入文件"
        )

    log("")
    log(f"输入文件：{input_file}")

    # --------------------------------------------------------------
    # 解析输入
    # --------------------------------------------------------------

    words, images = parse(
        input_file
    )

    words = list(words)

    log(f"✓ 学习词汇数量：{len(words)}")

    # --------------------------------------------------------------
    # Stage 1
    # --------------------------------------------------------------

    article_data, article_path = stage1_article(
        date=date,
        words=words,
        difficulty=difficulty,
        article_type=article_type,
        length=length,
    )

    git_save(
        [article_path],
        "文章恢复缓存",
    )

    # --------------------------------------------------------------
    # Stage 2
    # --------------------------------------------------------------

    if args.exam == "yes":

        exam_data, exam_path = stage2_exam(
            article_data=article_data,
            article_path=article_path,
            words=words,
            difficulty=difficulty,
            article_type=article_type,
            date=date,
        )

        git_save(
            [exam_path],
            "配套试卷",
        )

        # ----------------------------------------------------------
        # Stage 3
        # ----------------------------------------------------------

        answers_path = stage3_answers(
            exam_data=exam_data,
            article_data=article_data,
            article_path=article_path,
            exam_path=exam_path,
            words=words,
            difficulty=difficulty,
            article_type=article_type,
        )

        git_save(
            [answers_path],
            "答案与详细解析",
        )

    else:
        log("")
        log("→ --exam=no，跳过 Stage 2 / Stage 3")

    # --------------------------------------------------------------
    # 结束
    # --------------------------------------------------------------

    log("")
    log("=" * 60)
    log("748686 英语学习系统 COMPLETE")
    log("=" * 60)


if __name__ == "__main__":
    main()
