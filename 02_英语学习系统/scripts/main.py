#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
Main Pipeline V2.4

职责：

1. 读取指定日期的学习输入
2. 提取学习词汇
3. 生成 / 恢复英语短文
4. 生成 / 恢复配套试卷
5. 生成答案与详细解析
6. 保存系统缓存
7. Git commit + push
8. 支持中断后继续运行

恢复原则：

- 已存在且有效的文件优先恢复
- 能从 Markdown 恢复就不重复调用 AI
- 只有无法恢复时才调用 AI
- 每个阶段完成后立即落盘
- 每个阶段完成后立即 Git 保存
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


# ============================================================
# 路径
# ============================================================

SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))


# ============================================================
# 本地模块
# ============================================================

from common import ROOT, CONFIG
from input_parser import parse
from vision_extract import extract

from agnes_generate import (
    generate as gen_article,
    ARTICLE_TYPES,
)

from validate import article
from render_markdown import render

from exam_generate import (
    generate as gen_exam,
    render as render_exam,
)

from exam_answers import (
    generate as gen_answers,
    render as render_answers,
)


# ============================================================
# Git
# ============================================================

def run_git(
    args: list[str],
    check: bool = True,
) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def ensure_git_identity() -> None:
    name = run_git(
        ["config", "--get", "user.name"],
        check=False,
    )

    email = run_git(
        ["config", "--get", "user.email"],
        check=False,
    )

    if not name.stdout.strip():
        run_git(
            ["config", "user.name", "github-actions[bot]"]
        )

    if not email.stdout.strip():
        run_git(
            [
                "config",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
            ]
        )


def git_save_stage(
    paths: list[Path],
    message: str,
    label: str,
) -> None:

    print()
    print("=" * 60)
    print(f"Git 保存：{label}")
    print("=" * 60)

    ensure_git_identity()

    valid_paths: list[Path] = []

    for path in paths:

        if not path.exists():
            raise FileNotFoundError(
                f"Git 保存前文件不存在：{path}"
            )

        if path.is_file() and path.stat().st_size == 0:
            raise ValueError(
                f"Git 保存前发现空文件：{path}"
            )

        valid_paths.append(path)

    relative_paths = [
        str(path.relative_to(ROOT))
        for path in valid_paths
    ]

    run_git(
        ["add", "--", *relative_paths]
    )

    status = run_git(
        ["status", "--short"],
        check=False,
    )

    if not status.stdout.strip():
        print("✓ 没有新的 Git 变更")
        return

    commit = run_git(
        ["commit", "-m", message],
        check=False,
    )

    if commit.returncode != 0:
        combined = (
            (commit.stdout or "")
            + "\n"
            + (commit.stderr or "")
        )

        if "nothing to commit" in combined.lower():
            print("✓ 没有需要提交的内容")
            return

        raise RuntimeError(
            f"Git commit 失败：\n{combined}"
        )

    print("✓ Git commit 完成")

    push = run_git(
        ["push"],
        check=False,
    )

    if push.returncode != 0:
        combined = (
            (push.stdout or "")
            + "\n"
            + (push.stderr or "")
        )

        raise RuntimeError(
            f"Git push 失败：\n{combined}"
        )

    print("✓ Git push 完成")


# ============================================================
# 文件工具
# ============================================================

def is_nonempty(path: Path) -> bool:
    return (
        path.exists()
        and path.is_file()
        and path.stat().st_size > 0
    )


def write_and_confirm(
    path: Path,
    text: str,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        text,
        encoding="utf-8",
    )

    if not is_nonempty(path):
        raise RuntimeError(
            f"文件写入失败或为空：{path}"
        )

    print(f"✓ 已保存：{path}")


def save_json(
    path: Path,
    data: dict[str, Any],
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    if not is_nonempty(path):
        raise RuntimeError(
            f"JSON 保存失败或为空：{path}"
        )


def load_json(
    path: Path,
) -> dict[str, Any] | None:

    if not is_nonempty(path):
        return None

    try:
        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if isinstance(data, dict):
            return data

    except Exception:
        return None

    return None


# ============================================================
# Markdown / HTML 工具
# ============================================================

def strip_html(text: str) -> str:
    text = re.sub(
        r"<br\s*/?>",
        "\n",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    return html.unescape(text).strip()


def markdown_plain_text(text: str) -> str:
    text = strip_html(text)

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"\*(.*?)\*",
        r"\1",
        text,
    )

    text = re.sub(
        r"`(.*?)`",
        r"\1",
        text,
    )

    return text.strip()


def extract_section(
    text: str,
    start_pattern: str,
    end_pattern: str | None = None,
) -> str:

    if end_pattern:
        match = re.search(
            start_pattern
            + r"(.*?)"
            + end_pattern,
            text,
            flags=re.I | re.S,
        )
    else:
        match = re.search(
            start_pattern + r"(.*)$",
            text,
            flags=re.I | re.S,
        )

    if not match:
        return ""

    return match.group(1).strip()


# ============================================================
# 文章 Markdown 恢复
# ============================================================

def parse_word_list(
    block: str,
) -> list[dict[str, str]]:

    words: list[dict[str, str]] = []

    for match in re.finditer(
        r"<strong>\s*(.*?)\s*</strong>",
        block,
        flags=re.I | re.S,
    ):

        word = markdown_plain_text(
            match.group(1)
        )

        if not word:
            continue

        after = block[
            match.end():
        ]

        meaning_match = re.match(
            r"\s*[:：—–-]?\s*(.*?)(?:<br\s*/?>|\n|$)",
            after,
            flags=re.I | re.S,
        )

        meaning = ""

        if meaning_match:
            meaning = markdown_plain_text(
                meaning_match.group(1)
            )

        words.append(
            {
                "word": word,
                "meaning": meaning,
            }
        )

    return words


def recover_article_from_markdown(
    path: Path,
) -> dict[str, Any]:

    text = path.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # Frontmatter
    # --------------------------------------------------------

    date_match = re.search(
        r"^date:\s*(.+?)\s*$",
        text,
        flags=re.M,
    )

    difficulty_match = re.search(
        r"^difficulty:\s*(\d+)\s*$",
        text,
        flags=re.M,
    )

    article_type_match = re.search(
        r"^article_type:\s*(.+?)\s*$",
        text,
        flags=re.M,
    )

    date = (
        date_match.group(1).strip()
        if date_match
        else ""
    )

    difficulty = (
        int(difficulty_match.group(1))
        if difficulty_match
        else 1
    )

    article_type_name = (
        article_type_match.group(1).strip()
        if article_type_match
        else ""
    )

    # --------------------------------------------------------
    # 英文文章
    # --------------------------------------------------------

    article_en = extract_section(
        text,
        r"##\s*📖\s*English Article",
        r"##\s*中文翻译",
    )

    # --------------------------------------------------------
    # 中文翻译
    # --------------------------------------------------------

    article_zh = extract_section(
        text,
        r"##\s*中文翻译",
        r"##\s*学习重点",
    )

    # --------------------------------------------------------
    # 标题
    # --------------------------------------------------------

    title = ""

    title_match = re.search(
        r"^#\s+(.+?)\s*$",
        text,
        flags=re.M,
    )

    if title_match:
        title = title_match.group(1).strip()

    # --------------------------------------------------------
    # 学习重点
    # --------------------------------------------------------

    learning_block = extract_section(
        text,
        r"##\s*学习重点",
        None,
    )

    target_vocabulary = extract_section(
        learning_block,
        r"###\s*目标词汇",
        r"###\s*新增词汇",
    )

    added_vocabulary = extract_section(
        learning_block,
        r"###\s*新增词汇",
        r"###\s*重点短语",
    )

    phrases = extract_section(
        learning_block,
        r"###\s*重点短语",
        r"###\s*语法知识点",
    )

    grammar_text = extract_section(
        learning_block,
        r"###\s*语法知识点",
        r"###\s*重点句型",
    )

    sentence_text = extract_section(
        learning_block,
        r"###\s*重点句型",
        r"###\s*文章结构",
    )

    structure_text = extract_section(
        learning_block,
        r"###\s*文章结构",
        None,
    )

    target_vocabulary_data = parse_word_list(
        target_vocabulary
    )

    added_vocabulary_data = parse_word_list(
        added_vocabulary
    )

    return {
        "title": title,
        "article_en": article_en,
        "article_zh": article_zh,
        "target_vocabulary": target_vocabulary_data,
        "added_vocabulary": added_vocabulary_data,
        "phrases": phrases,
        "grammar_points": grammar_text,
        "sentence_patterns": sentence_text,
        "knowledge_structure": structure_text,
        "date": date,
        "difficulty": difficulty,
        "article_type": article_type_name,
    }


# ============================================================
# 试卷 Markdown 恢复
# ============================================================

def parse_options(
    block: str,
) -> dict[str, str]:

    options: dict[str, str] = {}

    for letter in ["A", "B", "C", "D"]:

        match = re.search(
            rf"^\s*-\s*{letter}\.\s*(.+?)\s*$",
            block,
            flags=re.M,
        )

        if match:
            options[letter] = (
                markdown_plain_text(
                    match.group(1)
                )
            )

    return options


def parse_questions(
    block: str,
) -> list[dict[str, Any]]:

    questions: list[dict[str, Any]] = []

    matches = list(
        re.finditer(
            r"^###\s+(\d+)\.\s+(.+?)\s*$",
            block,
            flags=re.M,
        )
    )

    for index, match in enumerate(matches):

        number = int(
            match.group(1)
        )

        question_text = (
            markdown_plain_text(
                match.group(2)
            )
        )

        start = match.end()

        if index + 1 < len(matches):
            end = matches[index + 1].start()
        else:
            end = len(block)

        question_block = block[
            start:end
        ]

        options = parse_options(
            question_block
        )

        questions.append(
            {
                "number": number,
                "question": question_text,
                "options": options,
            }
        )

    return questions


def parse_translation(
    block: str,
    part: str,
) -> list[dict[str, Any]]:

    match = re.search(
        rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[AB]|\Z)",
        block,
        flags=re.I | re.S,
    )

    if not match:
        return []

    part_block = match.group(1)

    return parse_questions(
        part_block
    )


def recover_exam_from_markdown(
    path: Path,
) -> dict[str, Any]:

    text = path.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------
    # 标题
    # --------------------------------------------------------

    title_match = re.search(
        r"^#\s+(.+?)\s*$",
        text,
        flags=re.M,
    )

    title = (
        title_match.group(1).strip()
        if title_match
        else ""
    )

    # --------------------------------------------------------
    # Listening
    #
    # Part C 后面没有 Part D。
    #
    # 因此 Part C 必须在：
    #
    #   # 二、单项选择
    #
    # 之前停止。
    #
    # 否则 Part C 会把后面的所有 ### 题目一起
    # 解析进去，导致：
    #
    #   Listening Part C 题数异常：40，期望 5
    # --------------------------------------------------------

    listening: dict[str, list[dict[str, Any]]] = {}

    for part in ["A", "B", "C"]:

        match = re.search(
            rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[ABC]|#\s*二、单项选择|\Z)",
            text,
            flags=re.I | re.S,
        )

        if not match:
            raise ValueError(
                f"Listening Part {part} 无法恢复"
            )

        part_block = match.group(1)

        questions = parse_questions(
            part_block
        )

        if len(questions) != 5:
            raise ValueError(
                f"Listening Part {part} 题数异常："
                f"{len(questions)}，期望 5"
            )

        listening[part] = questions

    # --------------------------------------------------------
    # 二、单项选择
    # --------------------------------------------------------

    single_match = re.search(
        r"#\s*二、单项选择(.*?)(?=#\s*三、多选题)",
        text,
        flags=re.I | re.S,
    )

    if not single_match:
        raise ValueError(
            "无法恢复：二、单项选择"
        )

    single_choice = parse_questions(
        single_match.group(1)
    )

    if len(single_choice) != 10:
        raise ValueError(
            f"单项选择题数异常："
            f"{len(single_choice)}，期望 10"
        )

    # --------------------------------------------------------
    # 三、多选题
    # --------------------------------------------------------

    multiple_match = re.search(
        r"#\s*三、多选题(.*?)(?=#\s*四、完形填空)",
        text,
        flags=re.I | re.S,
    )

    if not multiple_match:
        raise ValueError(
            "无法恢复：三、多选题"
        )

    multiple_choice = parse_questions(
        multiple_match.group(1)
    )

    if len(multiple_choice) != 10:
        raise ValueError(
            f"多选题数异常："
            f"{len(multiple_choice)}，期望 10"
        )

    # --------------------------------------------------------
    # 四、完形填空
    # --------------------------------------------------------

    cloze_match = re.search(
        r"#\s*四、完形填空(.*?)(?=#\s*五、阅读理解)",
        text,
        flags=re.I | re.S,
    )

    if not cloze_match:
        raise ValueError(
            "无法恢复：四、完形填空"
        )

    cloze_block = cloze_match.group(1)

    passage_match = re.search(
        r"(.*?)(?=##\s*选择题)",
        cloze_block,
        flags=re.I | re.S,
    )

    passage = ""

    if passage_match:
        passage = passage_match.group(1).strip()

    cloze_questions_match = re.search(
        r"##\s*选择题(.*)$",
        cloze_block,
        flags=re.I | re.S,
    )

    if not cloze_questions_match:
        raise ValueError(
            "无法恢复：完形填空选择题"
        )

    cloze_questions = parse_questions(
        cloze_questions_match.group(1)
    )

    if len(cloze_questions) != 10:
        raise ValueError(
            f"完形填空题数异常："
            f"{len(cloze_questions)}，期望 10"
        )

    cloze = {
        "passage": markdown_plain_text(
            passage
        ),
        "questions": cloze_questions,
    }

    # --------------------------------------------------------
    # 五、阅读理解
    # --------------------------------------------------------

    reading_match = re.search(
        r"#\s*五、阅读理解(.*?)(?=#\s*六、翻译)",
        text,
        flags=re.I | re.S,
    )

    if not reading_match:
        raise ValueError(
            "无法恢复：五、阅读理解"
        )

    reading_questions = parse_questions(
        reading_match.group(1)
    )

    if len(reading_questions) != 5:
        raise ValueError(
            f"阅读理解题数异常："
            f"{len(reading_questions)}，期望 5"
        )

    reading = {
        "questions": reading_questions
    }

    # --------------------------------------------------------
    # 六、翻译
    # --------------------------------------------------------

    translation_match = re.search(
        r"#\s*六、翻译(.*?)(?=#\s*七、写作)",
        text,
        flags=re.I | re.S,
    )

    if not translation_match:
        raise ValueError(
            "无法恢复：六、翻译"
        )

    translation_block = translation_match.group(1)

    translation: dict[str, list[dict[str, Any]]] = {}

    for part in ["A", "B"]:

        questions = parse_translation(
            translation_block,
            part,
        )

        if len(questions) != 5:
            raise ValueError(
                f"翻译 Part {part} 题数异常："
                f"{len(questions)}，期望 5"
            )

        translation[part] = questions

    # --------------------------------------------------------
    # 七、写作
    # --------------------------------------------------------

    writing_match = re.search(
        r"#\s*七、写作(.*)$",
        text,
        flags=re.I | re.S,
    )

    if not writing_match:
        raise ValueError(
            "无法恢复：七、写作"
        )

    writing_questions = parse_questions(
        writing_match.group(1)
    )

    if not writing_questions:
        raise ValueError(
            "写作题为空"
        )

    writing = writing_questions[0]

    # --------------------------------------------------------
    # 返回
    # --------------------------------------------------------

    return {
        "title": title,
        "listening": listening,
        "single_choice": single_choice,
        "multiple_choice": multiple_choice,
        "cloze": cloze,
        "reading": reading,
        "translation": translation,
        "writing": writing,
    }


# ============================================================
# Stage 1：文章
# ============================================================

def load_or_generate_article(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    length: int,
    words: list[Any],
    images: list[Path],
    output_file: Path,
    system_dir: Path,
) -> dict[str, Any]:

    print()
    print("=" * 60)
    print("STAGE 1 / 3：英语短文")
    print("=" * 60)

    cache_file = (
        system_dir / "article.json"
    )

    # --------------------------------------------------------
    # 优先使用缓存
    # --------------------------------------------------------

    cached = load_json(
        cache_file
    )

    if cached:
        print("✓ 已存在文章结构化缓存")
        return cached

    # --------------------------------------------------------
    # 从 Markdown 恢复
    # --------------------------------------------------------

    if is_nonempty(output_file):

        print(
            f"✓ 已存在文章：{output_file}"
        )

        print(
            "✓ 不调用文章 AI"
        )

        print(
            "→ 正在从现有 Markdown 恢复结构"
        )

        data = recover_article_from_markdown(
            output_file
        )

        save_json(
            cache_file,
            data,
        )

        print(
            f"✓ 文章结构化缓存 已落盘：{cache_file}"
        )

        git_save_stage(
            [
                output_file,
                cache_file,
            ],
            "英语学习系统：文章恢复缓存",
            "文章恢复缓存",
        )

        return data

    # --------------------------------------------------------
    # AI 生成
    # --------------------------------------------------------

    print("→ 未找到现有文章")
    print("→ 正在调用文章 AI")

    generated = gen_article(
        date=date,
        difficulty=difficulty,
        article_type=article_type,
        length=length,
        words=words,
        images=images,
    )

    if not isinstance(generated, dict):
        raise ValueError(
            "文章 AI 返回结果不是 dict"
        )

    valid = article(
        generated
    )

    if valid is not True:
        raise ValueError(
            f"文章验证失败：{valid}"
        )

    markdown = render(
        generated
    )

    write_and_confirm(
        output_file,
        markdown,
    )

    save_json(
        cache_file,
        generated,
    )

    git_save_stage(
        [
            output_file,
            cache_file,
        ],
        "英语学习系统：生成英语短文",
        "英语短文",
    )

    return generated


# ============================================================
# Stage 2：试卷
# ============================================================

def load_or_generate_exam(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    article_data: dict[str, Any],
    words: list[Any],
    output_file: Path,
    system_dir: Path,
) -> dict[str, Any]:

    print()
    print("=" * 60)
    print("STAGE 2 / 3：配套试卷")
    print("=" * 60)

    cache_file = (
        system_dir / "exam.json"
    )

    # --------------------------------------------------------
    # 优先使用缓存
    # --------------------------------------------------------

    cached = load_json(
        cache_file
    )

    if cached:
        print("✓ 已存在试卷结构化缓存")
        return cached

    # --------------------------------------------------------
    # 从 Markdown 恢复
    # --------------------------------------------------------

    if is_nonempty(output_file):

        print(
            f"✓ 已存在试卷：{output_file}"
        )

        print(
            "✓ 不调用试卷 AI"
        )

        print(
            "→ 正在从现有 Markdown 恢复结构"
        )

        data = recover_exam_from_markdown(
            output_file
        )

        save_json(
            cache_file,
            data,
        )

        print(
            f"✓ 试卷结构化缓存 已落盘：{cache_file}"
        )

        git_save_stage(
            [
                output_file,
                cache_file,
            ],
            "英语学习系统：试卷恢复缓存",
            "试卷恢复缓存",
        )

        return data

    # --------------------------------------------------------
    # AI 生成
    #
    # exam_generate.py V5.3 的真实接口是：
    #
    # generate(
    #     article,
    #     difficulty,
    #     article_type,
    #     words,
    # )
    #
    # 不接受 date=。
    # --------------------------------------------------------

    print("→ 未找到现有试卷")
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

    # --------------------------------------------------------
    # exam_generate.py V5.3 的真实 render 接口：
    #
    # render(
    #     exam,
    #     article_title,
    #     difficulty,
    #     article_type_name,
    # )
    # --------------------------------------------------------

    markdown = render_exam(
        generated,
        article_data.get("title", ""),
        difficulty,
        ARTICLE_TYPES.get(
            article_type,
            article_type,
        ),
    )

    write_and_confirm(
        output_file,
        markdown,
    )

    save_json(
        cache_file,
        generated,
    )

    git_save_stage(
        [
            output_file,
            cache_file,
        ],
        "英语学习系统：生成配套试卷",
        "配套试卷",
    )

    return generated


# ============================================================
# Stage 3：答案与解析
# ============================================================

def load_or_generate_answers(
    *,
    date: str,
    difficulty: int,
    article_type: str,
    article_data: dict[str, Any],
    exam_data: dict[str, Any],
    output_file: Path,
) -> dict[str, Any]:

    print()
    print("=" * 60)
    print("STAGE 3 / 3：答案与详细解析")
    print("=" * 60)

    # --------------------------------------------------------
    # 已存在则直接跳过
    # --------------------------------------------------------

    if is_nonempty(output_file):

        print(
            f"✓ 已存在答案解析：{output_file}"
        )

        print(
            "✓ 不调用答案解析 AI"
        )

        return {
            "reused": True
        }

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    print(
        "→ 未找到答案解析"
    )

    print(
        "→ 正在调用答案解析 AI"
    )

    generated = gen_answers(
        date=date,
        difficulty=difficulty,
        article_type=article_type,
        article=article_data,
        exam=exam_data,
    )

    if not isinstance(generated, dict):
        raise ValueError(
            "答案解析 AI 返回结果不是 dict"
        )

    markdown = render_answers(
        generated
    )

    write_and_confirm(
        output_file,
        markdown,
    )

    git_save_stage(
        [
            output_file,
        ],
        "英语学习系统：生成答案与详细解析",
        "答案与详细解析",
    )

    return generated


# ============================================================
# Manifest
# ============================================================

def write_manifest(
    *,
    system_dir: Path,
    date: str,
    difficulty: int,
    article_type: str,
    article_file: Path,
    exam_file: Path,
    answers_file: Path,
) -> Path:

    manifest_file = (
        system_dir / "manifest.json"
    )

    data = {
        "date": date,
        "difficulty": difficulty,
        "article_type": article_type,
        "article_file": str(
            article_file.relative_to(ROOT)
        ),
        "exam_file": str(
            exam_file.relative_to(ROOT)
        ),
        "answers_file": str(
            answers_file.relative_to(ROOT)
        ),
    }

    save_json(
        manifest_file,
        data,
    )

    print(
        f"✓ Manifest 已保存：{manifest_file}"
    )

    return manifest_file


# ============================================================
# CLI
# ============================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="02_英语学习系统"
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--difficulty",
        required=True,
        type=int,
        choices=range(1, 18),
    )

    parser.add_argument(
        "--article-type",
        required=True,
        choices=ARTICLE_TYPES,
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


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    parser = build_parser()

    args = parser.parse_args()

    date = args.date
    difficulty = args.difficulty
    article_type = args.article_type
    length = args.length

    # ========================================================
    # 基本信息
    # ========================================================

    print()
    print("=" * 60)
    print("02_英语学习系统 V2.4")
    print("=" * 60)

    print(f"日期：{date}")
    print(f"难度：{difficulty}星")
    print(f"文章类型：{article_type}")
    print(f"目标长度：{length}")
    print(f"试卷：{args.exam}")
    print(f"图片：{args.image}")
    print(f"音频：{args.audio}")
    print(f"音频格式：{args.audio_format}")
    print(f"语速：{args.speed}")

    # ========================================================
    # 输入文件
    # ========================================================

    input_file = (
        ROOT
        / "input"
        / f"{date}.md"
    )

    if not input_file.exists():
        raise FileNotFoundError(
            f"学习输入不存在：{input_file}"
        )

    # ========================================================
    # 读取学习词汇
    #
    # parse() 返回：
    #
    #     words, images
    #
    # 这里必须按照 tuple 解包。
    # ========================================================

    words, images = parse(
        input_file
    )

    words = list(words)

    print(
        f"✓ 学习词汇数量：{len(words)}"
    )

    # ========================================================
    # Vision 词汇
    # ========================================================

    if args.image == "yes":

        try:

            vision_words = extract(
                input_file
            )

            if vision_words:
                words.extend(
                    vision_words
                )

                print(
                    f"✓ Vision 提取词汇："
                    f"{len(vision_words)}"
                )

        except Exception as exc:

            print(
                "⚠ Vision 提取失败，"
                f"继续使用已有词汇：{exc}"
            )

    # ========================================================
    # 词汇去重
    # ========================================================

    dedup_words: list[Any] = []

    for word in words:

        if word not in dedup_words:
            dedup_words.append(word)

    words = dedup_words

    print(
        f"✓ 去重后学习词汇数量：{len(words)}"
    )

    # ========================================================
    # 输出路径
    # ========================================================

    date_dir = (
        ROOT
        / "output"
        / date
    )

    system_dir = (
        date_dir
        / ".system"
    )

    # --------------------------------------------------------
    # 文章类型中文名称
    # --------------------------------------------------------

    article_type_name = (
        CONFIG
        .get("article_types", {})
        .get(article_type, {})
        .get("name")
    )

    if not article_type_name:

        # 如果配置中没有中文名称，
        # 尝试直接使用 article_type。
        article_type_name = article_type

    # --------------------------------------------------------
    # 文件名
    # --------------------------------------------------------

    article_file = (
        date_dir
        / "英语短文注记"
        / f"{difficulty}星_{article_type_name}.md"
    )

    exam_file = (
        date_dir
        / "配套试卷"
        / f"{difficulty}星_{article_type_name}_试卷.md"
    )

    answers_file = (
        date_dir
        / "配套试卷"
        / f"{difficulty}星_{article_type_name}_答案解析.md"
    )

    # ========================================================
    # Stage 1
    # ========================================================

    article_data = load_or_generate_article(
        date=date,
        difficulty=difficulty,
        article_type=article_type,
        length=length,
        words=words,
        images=images,
        output_file=article_file,
        system_dir=system_dir,
    )

    # ========================================================
    # Stage 2
    # ========================================================

    exam_data: dict[str, Any] = {}

    if args.exam == "yes":

        exam_data = load_or_generate_exam(
            date=date,
            difficulty=difficulty,
            article_type=article_type,
            article_data=article_data,
            words=words,
            output_file=exam_file,
            system_dir=system_dir,
        )

    else:

        print()
        print("=" * 60)
        print("STAGE 2 / 3：配套试卷")
        print("=" * 60)

        print(
            "✓ --exam=no，跳过试卷"
        )

    # ========================================================
    # Stage 3
    # ========================================================

    answers_data: dict[str, Any] = {}

    if args.exam == "yes":

        answers_data = load_or_generate_answers(
            date=date,
            difficulty=difficulty,
            article_type=article_type,
            article_data=article_data,
            exam_data=exam_data,
            output_file=answers_file,
        )

    else:

        print()
        print("=" * 60)
        print("STAGE 3 / 3：答案与详细解析")
        print("=" * 60)

        print(
            "✓ --exam=no，跳过答案解析"
        )

    # ========================================================
    # Manifest
    # ========================================================

    manifest_file = write_manifest(
        system_dir=system_dir,
        date=date,
        difficulty=difficulty,
        article_type=article_type,
        article_file=article_file,
        exam_file=exam_file,
        answers_file=answers_file,
    )

    # ========================================================
    # Manifest Git 保存
    # ========================================================

    git_save_stage(
        [
            manifest_file,
        ],
        "英语学习系统：更新运行清单",
        "Manifest",
    )

    # ========================================================
    # 最终检查
    # ========================================================

    print()
    print("=" * 60)
    print("最终文件检查")
    print("=" * 60)

    required_files = [
        article_file,
    ]

    if args.exam == "yes":
        required_files.extend(
            [
                exam_file,
                answers_file,
            ]
        )

    required_files.append(
        manifest_file
    )

    for path in required_files:

        if not is_nonempty(path):
            raise RuntimeError(
                f"最终文件检查失败：{path}"
            )

        print(
            f"✓ {path.relative_to(ROOT)}"
        )

    print()
    print("=" * 60)
    print("02_英语学习系统执行完成")
    print("=" * 60)


# ============================================================
# ENTRY
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as exc:

        print()
        print("=" * 60)
        print("❌ 英语学习系统执行失败")
        print("=" * 60)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        raise
