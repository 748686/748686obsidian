#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
main.py V2.4

======================================================================
职责
======================================================================

本程序负责：

    1. 生成 / 恢复英语短文
    2. 生成 / 恢复配套试卷
    3. 生成 / 恢复答案与解析
    4. 每个阶段独立断点续跑
    5. 每个阶段成功后立即落盘、立即 Git 保存
    6. 为后续断点续跑保存结构化 JSON 缓存

======================================================================
核心原则
======================================================================

文章存在：
    不重新调用文章 AI

试卷存在：
    不重新调用试卷 AI

答案解析存在：
    不重新调用答案解析 AI

只有缺失阶段才执行 AI。

======================================================================
结构化缓存
======================================================================

output/YYYY-MM-DD/.system/article.json
output/YYYY-MM-DD/.system/exam.json

这两个文件不是完成标记。

它们只是：

    已成功生成的数据结构缓存

作用：

    当 Markdown 已经存在，但后续阶段需要原始结构时，
    可以直接恢复，而无需再次调用 AI。

======================================================================
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


# ======================================================================
# 项目导入
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import ROOT, CONFIG
from input_parser import parse
from vision_extract import extract
from agnes_generate import generate as gen_article, ARTICLE_TYPES
from validate import article
from render_markdown import render
from exam_generate import generate as gen_exam, render as render_exam
from exam_answers import generate as gen_answers, render as render_answers


# ======================================================================
# Git
# ======================================================================

def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=check,
    )


def ensure_git_identity() -> None:
    name = run_git(["config", "user.name"], check=False).stdout.strip()
    email = run_git(["config", "user.email"], check=False).stdout.strip()

    if not name:
        run_git(["config", "user.name", "github-actions[bot]"])

    if not email:
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
    """
    一个阶段完成后立即 commit + push。
    """

    print()
    print("=" * 68)
    print(f"Git 保存：{label}")
    print("=" * 68)

    valid_paths: list[Path] = []

    for path in paths:
        if not path.exists():
            raise RuntimeError(
                f"{label} Git 保存失败：文件不存在：{path}"
            )

        if path.is_file() and path.stat().st_size == 0:
            raise RuntimeError(
                f"{label} Git 保存失败：文件为空：{path}"
            )

        valid_paths.append(path)

    ensure_git_identity()

    relative_paths = [
        str(path.relative_to(ROOT))
        for path in valid_paths
    ]

    run_git(["add", "--", *relative_paths])

    staged = run_git(
        ["diff", "--cached", "--name-only"],
        check=False,
    ).stdout.strip()

    if not staged:
        print("✓ 没有新的 Git 变更")
        return

    print("已暂存：")
    print(staged)

    run_git(["commit", "-m", message])

    push = run_git(
        ["push"],
        check=False,
    )

    print(push.stdout)

    if push.returncode != 0:
        raise RuntimeError(
            f"{label} git push 失败。\n{push.stdout}"
        )

    print(f"✓ {label} 已 commit + push")


# ======================================================================
# 文件工具
# ======================================================================

def is_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.stat().st_size > 0


def write_and_confirm(
    file_path: Path,
    content: str,
    label: str,
) -> None:

    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(
        content,
        encoding="utf-8",
    )

    if not is_nonempty(file_path):
        raise RuntimeError(
            f"{label} 写入失败或文件为空：{file_path}"
        )

    print(f"✓ {label} 已落盘：{file_path}")


def save_json(
    path: Path,
    data: dict[str, Any],
    label: str,
) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )

    write_and_confirm(
        path,
        text + "\n",
        label,
    )


def load_json(
    path: Path,
) -> dict[str, Any] | None:

    if not is_nonempty(path):
        return None

    try:
        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        if not isinstance(data, dict):
            return None

        return data

    except Exception as exc:
        print(
            f"⚠ JSON 缓存读取失败：{path}: {exc}"
        )
        return None


# ======================================================================
# Markdown / HTML 工具
# ======================================================================

def strip_html(value: str) -> str:
    """
    将文章 Markdown 中的 HTML 转成纯文本。

    不依赖 BeautifulSoup。
    """

    value = html.unescape(value)

    value = re.sub(
        r"<br\s*/?>",
        "\n",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"</div\s*>",
        "\n",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"</p\s*>",
        "\n",
        value,
        flags=re.I,
    )

    value = re.sub(
        r"<[^>]+>",
        "",
        value,
    )

    value = re.sub(
        r"\n{3,}",
        "\n\n",
        value,
    )

    return value.strip()


def markdown_plain_text(value: str) -> str:
    value = html.unescape(value)

    value = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        value,
    )

    value = re.sub(
        r"`(.*?)`",
        r"\1",
        value,
    )

    value = re.sub(
        r"<[^>]+>",
        "",
        value,
    )

    return value.strip()


def extract_section(
    text: str,
    start_pattern: str,
    end_patterns: list[str],
) -> str:

    start = re.search(
        start_pattern,
        text,
        flags=re.I | re.S,
    )

    if not start:
        return ""

    start_pos = start.end()
    end_pos = len(text)

    for pattern in end_patterns:
        match = re.search(
            pattern,
            text[start_pos:],
            flags=re.I | re.S,
        )

        if match:
            candidate = start_pos + match.start()
            if candidate < end_pos:
                end_pos = candidate

    return text[start_pos:end_pos].strip()


# ======================================================================
# 文章 Markdown → article dict
# ======================================================================

def recover_article_from_markdown(
    path: Path,
) -> dict[str, Any]:
    """
    将 render_markdown.py V4 已生成的文章 Markdown
    恢复为 agnes_generate / exam_generate 所需的 article dict。

    只做确定性解析，不调用 AI。
    """

    if not is_nonempty(path):
        raise RuntimeError(
            f"无法恢复文章：文件不存在或为空：{path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------------
    # Frontmatter
    # --------------------------------------------------------------

    date_match = re.search(
        r"^date:\s*(.+?)\s*$",
        text,
        flags=re.M,
    )

    difficulty_match = re.search(
        r"^difficulty:\s*(.+?)\s*$",
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

    difficulty_text = (
        difficulty_match.group(1).strip()
        if difficulty_match
        else ""
    )

    article_type_name = (
        article_type_match.group(1).strip()
        if article_type_match
        else ""
    )

    difficulty_number_match = re.search(
        r"(\d+)",
        difficulty_text,
    )

    difficulty_number = (
        int(difficulty_number_match.group(1))
        if difficulty_number_match
        else 1
    )

    # --------------------------------------------------------------
    # English Article 区域
    # --------------------------------------------------------------

    english_marker = re.search(
        r"📖\s*English Article",
        text,
        flags=re.I,
    )

    if not english_marker:
        raise RuntimeError(
            f"无法在文章 Markdown 中找到 English Article：{path}"
        )

    english_start = english_marker.end()

    chinese_marker = re.search(
        r"中文翻译",
        text[english_start:],
        flags=re.I,
    )

    if not chinese_marker:
        raise RuntimeError(
            f"无法在文章 Markdown 中找到中文翻译：{path}"
        )

    english_section = text[
        english_start:
        english_start + chinese_marker.start()
    ]

    english_clean = strip_html(
        english_section
    )

    english_lines = [
        line.strip()
        for line in english_clean.splitlines()
        if line.strip()
    ]

    # 第一行通常为标题，后续为正文
    title = ""

    if english_lines:
        for line in english_lines:
            if line and not line.startswith("📖"):
                title = line
                break

    article_en = ""

    if title:
        title_index = english_lines.index(title)

        body_lines = english_lines[
            title_index + 1:
        ]

        article_en = " ".join(
            body_lines
        ).strip()

    if not title or not article_en:
        raise RuntimeError(
            f"无法恢复文章标题或英文正文：{path}"
        )

    # --------------------------------------------------------------
    # 中文翻译
    # --------------------------------------------------------------

    chinese_start = (
        english_start
        + chinese_marker.end()
    )

    chinese_end_match = re.search(
        r"</div>\s*</td>",
        text[chinese_start:],
        flags=re.I,
    )

    if chinese_end_match:
        chinese_section = text[
            chinese_start:
            chinese_start + chinese_end_match.start()
        ]
    else:
        chinese_section = text[
            chinese_start:
        ]

    article_zh = strip_html(
        chinese_section
    )

    # 清除标题类残留
    article_zh = re.sub(
        r"^\s*[:：]?\s*",
        "",
        article_zh,
    ).strip()

    # --------------------------------------------------------------
    # 学习解析
    # --------------------------------------------------------------

    learning_match = re.search(
        r"🎯\s*学习解析",
        text,
        flags=re.I,
    )

    learning_text = (
        text[learning_match.end():]
        if learning_match
        else ""
    )

    def extract_learning_block(
        heading: str,
        next_headings: list[str],
    ) -> str:

        if not learning_text:
            return ""

        pattern = (
            re.escape(heading)
        )

        start_match = re.search(
            pattern,
            learning_text,
            flags=re.I,
        )

        if not start_match:
            return ""

        block = learning_text[
            start_match.end():
        ]

        end_pos = len(block)

        for next_heading in next_headings:
            match = re.search(
                re.escape(next_heading),
                block,
                flags=re.I,
            )

            if match:
                end_pos = min(
                    end_pos,
                    match.start(),
                )

        return strip_html(
            block[:end_pos]
        ).strip()

    target_vocab_text = extract_learning_block(
        "目标词汇",
        [
            "新增词汇",
            "重点短语",
            "语法知识点",
            "重点句型",
            "文章结构",
        ],
    )

    added_vocab_text = extract_learning_block(
        "新增词汇",
        [
            "重点短语",
            "语法知识点",
            "重点句型",
            "文章结构",
        ],
    )

    phrases_text = extract_learning_block(
        "重点短语",
        [
            "语法知识点",
            "重点句型",
            "文章结构",
        ],
    )

    grammar_text = extract_learning_block(
        "语法知识点",
        [
            "重点句型",
            "文章结构",
        ],
    )

    sentence_text = extract_learning_block(
        "重点句型",
        [
            "文章结构",
        ],
    )

    structure_text = extract_learning_block(
        "文章结构",
        [],
    )

    def parse_word_list(
        block: str,
    ) -> list[str]:

        result: list[str] = []

        for match in re.finditer(
            r"<strong>(.*?)</strong>",
            block,
            flags=re.I | re.S,
        ):
            word = strip_html(
                match.group(1)
            ).strip()

            if word:
                result.append(word)

        return result

    target_vocabulary = parse_word_list(
        target_vocab_text
    )

    added_vocabulary = parse_word_list(
        added_vocab_text
    )

    phrases = parse_word_list(
        phrases_text
    )

    # --------------------------------------------------------------
    # 构造与 Agnes 输出兼容的 article
    # --------------------------------------------------------------

    article_data: dict[str, Any] = {
        "title": title,
        "article_en": article_en,
        "article_zh": article_zh,
        "target_vocabulary": target_vocabulary,
        "added_vocabulary": added_vocabulary,
        "phrases": phrases,
        "grammar_points": grammar_text,
        "sentence_patterns": sentence_text,
        "knowledge_structure": structure_text,
        "date": date,
        "difficulty": difficulty_number,
        "article_type": article_type_name,
    }

    if not article_data["article_en"]:
        raise RuntimeError(
            f"恢复文章失败：article_en 为空：{path}"
        )

    if not article_data["article_zh"]:
        print(
            "⚠ 警告：恢复文章时未找到完整中文正文"
        )

    return article_data


# ======================================================================
# 试卷 Markdown → exam dict
# ======================================================================

def recover_exam_from_markdown(
    path: Path,
) -> dict[str, Any]:
    """
    将 exam_generate.py V5.3 render() 输出的 Markdown
    恢复成 exam_generate / exam_answers 所需结构。

    完全本地解析，不调用 AI。
    """

    if not is_nonempty(path):
        raise RuntimeError(
            f"无法恢复试卷：文件不存在或为空：{path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

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

    if not title:
        raise RuntimeError(
            f"无法恢复试卷标题：{path}"
        )

    # --------------------------------------------------------------
    # 通用选项解析
    # --------------------------------------------------------------

    def parse_options(
        block: str,
    ) -> list[str]:

        options = []

        for match in re.finditer(
            r"^\s*-\s*([A-D]\.\s+.+?)\s*$",
            block,
            flags=re.M,
        ):
            options.append(
                match.group(1).strip()
            )

        return options

    def parse_questions(
        block: str,
        section_heading: str | None = None,
    ) -> list[dict[str, Any]]:

        results = []

        matches = list(
            re.finditer(
                r"^###\s+(\d+)\.\s+(.+?)\s*$",
                block,
                flags=re.M,
            )
        )

        for index, match in enumerate(matches):

            number = int(match.group(1))
            question = match.group(2).strip()

            start = match.end()
            end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(block)
            )

            question_block = block[
                start:end
            ]

            options = parse_options(
                question_block
            )

            # 删除作答提示
            question = re.sub(
                r"\s*作答：.*$",
                "",
                question,
                flags=re.S,
            ).strip()

            item: dict[str, Any] = {
                "number": number,
                "question": question,
                "options": options,
            }

            results.append(item)

        return results

    # --------------------------------------------------------------
    # 听力
    # --------------------------------------------------------------

    listening: list[dict[str, Any]] = []

    for part in ["A", "B", "C"]:

        match = re.search(
            rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[ABC]|\Z)",
            text,
            flags=re.I | re.S,
        )

        if not match:
            raise RuntimeError(
                f"试卷缺少 Listening Part {part}：{path}"
            )

        block = match.group(1).strip()

        instruction_match = re.search(
            r"^(.+?)(?=###\s+1\.)",
            block,
            flags=re.M | re.S,
        )

        instruction = (
            instruction_match.group(1).strip()
            if instruction_match
            else ""
        )

        questions = parse_questions(
            block
        )

        if len(questions) != 5:
            raise RuntimeError(
                f"Listening Part {part} 题数异常："
                f"{len(questions)}，期望 5"
            )

        listening.append(
            {
                "part": part,
                "instruction": instruction,
                "questions": questions,
            }
        )

    # --------------------------------------------------------------
    # 单选
    # --------------------------------------------------------------

    single_match = re.search(
        r"#\s*二、单项选择(.*?)(?=#\s*三、多选题)",
        text,
        flags=re.I | re.S,
    )

    if not single_match:
        raise RuntimeError(
            f"试卷缺少单项选择：{path}"
        )

    single_choice = parse_questions(
        single_match.group(1)
    )

    if len(single_choice) != 10:
        raise RuntimeError(
            f"单项选择题数异常："
            f"{len(single_choice)}，期望 10"
        )

    # --------------------------------------------------------------
    # 多选
    # --------------------------------------------------------------

    multiple_match = re.search(
        r"#\s*三、多选题(.*?)(?=#\s*四、完形填空)",
        text,
        flags=re.I | re.S,
    )

    if not multiple_match:
        raise RuntimeError(
            f"试卷缺少多选题：{path}"
        )

    multiple_choice = parse_questions(
        multiple_match.group(1)
    )

    if len(multiple_choice) != 10:
        raise RuntimeError(
            f"多选题数异常："
            f"{len(multiple_choice)}，期望 10"
        )

    # --------------------------------------------------------------
    # 完形
    # --------------------------------------------------------------

    cloze_match = re.search(
        r"#\s*四、完形填空(.*?)(?=#\s*五、阅读理解)",
        text,
        flags=re.I | re.S,
    )

    if not cloze_match:
        raise RuntimeError(
            f"试卷缺少完形填空：{path}"
        )

    cloze_block = cloze_match.group(1)

    passage_match = re.search(
        r"(?s)(.*?)##\s*选择题",
        cloze_block,
        flags=re.I,
    )

    passage = (
        passage_match.group(1).strip()
        if passage_match
        else ""
    )

    passage = re.sub(
        r"\s+",
        " ",
        passage,
    ).strip()

    cloze_question_block = (
        passage_match.group(1)
        if passage_match
        else cloze_block
    )

    if passage_match:
        cloze_question_block = cloze_block[
            passage_match.end():
        ]

    cloze_questions = parse_questions(
        cloze_question_block
    )

    if len(cloze_questions) != 10:
        raise RuntimeError(
            f"完形题数异常："
            f"{len(cloze_questions)}，期望 10"
        )

    cloze = [
        {
            "passage": passage,
            "questions": cloze_questions,
        }
    ]

    # --------------------------------------------------------------
    # 阅读
    # --------------------------------------------------------------

    reading_match = re.search(
        r"#\s*五、阅读理解(.*?)(?=#\s*六、翻译)",
        text,
        flags=re.I | re.S,
    )

    if not reading_match:
        raise RuntimeError(
            f"试卷缺少阅读理解：{path}"
        )

    reading = parse_questions(
        reading_match.group(1)
    )

    if len(reading) != 5:
        raise RuntimeError(
            f"阅读题数异常："
            f"{len(reading)}，期望 5"
        )

    # --------------------------------------------------------------
    # 翻译
    # --------------------------------------------------------------

    translation_match = re.search(
        r"#\s*六、翻译(.*?)(?=#\s*七、写作)",
        text,
        flags=re.I | re.S,
    )

    if not translation_match:
        raise RuntimeError(
            f"试卷缺少翻译：{path}"
        )

    translation_block = translation_match.group(1)

    def parse_translation(
        part: str,
    ) -> list[dict[str, Any]]:

        match = re.search(
            rf"##\s*Part\s+{part}\s*(.*?)(?=##\s*Part\s+[AB]|\Z)",
            translation_block,
            flags=re.I | re.S,
        )

        if not match:
            raise RuntimeError(
                f"试卷缺少翻译 Part {part}"
            )

        results = []

        questions = list(
            re.finditer(
                r"^###\s+(\d+)\.\s+(.+?)\s*$",
                match.group(1),
                flags=re.M,
            )
        )

        for q in questions:

            results.append(
                {
                    "number": int(q.group(1)),
                    "sentence": q.group(2).strip(),
                    "question": q.group(2).strip(),
                }
            )

        if len(results) != 5:
            raise RuntimeError(
                f"翻译 Part {part} 题数异常："
                f"{len(results)}，期望 5"
            )

        return results

    translation = {
        "part_a": parse_translation("A"),
        "part_b": parse_translation("B"),
    }

    # --------------------------------------------------------------
    # 写作
    # --------------------------------------------------------------

    writing_match = re.search(
        r"#\s*七、写作(.*)$",
        text,
        flags=re.I | re.S,
    )

    if not writing_match:
        raise RuntimeError(
            f"试卷缺少写作：{path}"
        )

    writing_questions = parse_questions(
        writing_match.group(1)
    )

    if not writing_questions:
        raise RuntimeError(
            f"无法恢复写作题：{path}"
        )

    writing = writing_questions[:1]

    exam = {
        "title": title,
        "listening": listening,
        "single_choice": single_choice,
        "multiple_choice": multiple_choice,
        "cloze": cloze,
        "reading": reading,
        "translation": translation,
        "writing": writing,
    }

    return exam


# ======================================================================
# 文章恢复 / 生成
# ======================================================================

def load_or_generate_article(
    *,
    article_path: Path,
    article_cache: Path,
    words: list[str],
    difficulty: int,
    article_type: str,
    article_type_name: str,
    length: int,
    date: str,
) -> dict[str, Any]:

    print()
    print("=" * 68)
    print("STAGE 1 / 3：英语短文")
    print("=" * 68)

    # --------------------------------------------------------------
    # 优先使用结构化缓存
    # --------------------------------------------------------------

    cached = load_json(
        article_cache
    )

    if cached and cached.get("article_en"):

        print("✓ 已存在结构化文章缓存")
        print("✓ 不调用文章 AI")

        return cached

    # --------------------------------------------------------------
    # Markdown 已存在 → 本地恢复
    # --------------------------------------------------------------

    if is_nonempty(article_path):

        print(
            f"✓ 已存在文章：{article_path}"
        )
        print("✓ 不调用文章 AI")
        print("→ 正在从现有 Markdown 恢复结构")

        art = recover_article_from_markdown(
            article_path
        )

        save_json(
            article_cache,
            art,
            "文章结构化缓存",
        )

        git_save_stage(
            [
                article_cache,
            ],
            (
                f"chore(english): "
                f"save article recovery cache {date}"
            ),
            "文章恢复缓存",
        )

        return art

    # --------------------------------------------------------------
    # 真正缺失 → AI 生成
    # --------------------------------------------------------------

    print("→ 文章不存在")
    print("→ 调用文章 AI")

    art = gen_article(
        words,
        difficulty,
        article_type,
        length,
    )

    article(
        art,
        words,
    )

    content = render(
        art,
        words,
        difficulty,
        article_type,
        date,
        length,
    )

    write_and_confirm(
        article_path,
        content,
        "英语短文",
    )

    save_json(
        article_cache,
        art,
        "文章结构化缓存",
    )

    git_save_stage(
        [
            article_path,
            article_cache,
        ],
        (
            f"feat(english): "
            f"generate article {date}"
        ),
        "英语短文",
    )

    return art


# ======================================================================
# 试卷恢复 / 生成
# ======================================================================

def load_or_generate_exam(
    *,
    exam_path: Path,
    exam_cache: Path,
    art: dict[str, Any],
    words: list[str],
    difficulty: int,
    article_type: str,
    article_type_name: str,
    date: str,
) -> dict[str, Any]:

    print()
    print("=" * 68)
    print("STAGE 2 / 3：配套试卷")
    print("=" * 68)

    # --------------------------------------------------------------
    # JSON 缓存
    # --------------------------------------------------------------

    cached = load_json(
        exam_cache
    )

    if cached and cached.get("listening"):

        print("✓ 已存在结构化试卷缓存")
        print("✓ 不调用试卷 AI")

        return cached

    # --------------------------------------------------------------
    # Markdown 恢复
    # --------------------------------------------------------------

    if is_nonempty(exam_path):

        print(
            f"✓ 已存在试卷：{exam_path}"
        )
        print("✓ 不调用试卷 AI")
        print("→ 正在从现有 Markdown 恢复结构")

        exam = recover_exam_from_markdown(
            exam_path
        )

        save_json(
            exam_cache,
            exam,
            "试卷结构化缓存",
        )

        git_save_stage(
            [
                exam_cache,
            ],
            (
                f"chore(english): "
                f"save exam recovery cache {date}"
            ),
            "试卷恢复缓存",
        )

        return exam

    # --------------------------------------------------------------
    # 真正缺失
    # --------------------------------------------------------------

    print("→ 试卷不存在")
    print("→ 调用试卷 AI")

    exam = gen_exam(
        art,
        difficulty,
        article_type,
        words,
    )

    content = render_exam(
        exam,
        art["title"],
        difficulty,
        article_type_name,
    )

    write_and_confirm(
        exam_path,
        content,
        "配套试卷",
    )

    save_json(
        exam_cache,
        exam,
        "试卷结构化缓存",
    )

    git_save_stage(
        [
            exam_path,
            exam_cache,
        ],
        (
            f"feat(english): "
            f"generate exam {date}"
        ),
        "配套试卷",
    )

    return exam


# ======================================================================
# 答案解析
# ======================================================================

def load_or_generate_answers(
    *,
    answer_path: Path,
    exam: dict[str, Any],
    art: dict[str, Any],
    words: list[str],
    difficulty: int,
    article_type: str,
    article_type_name: str,
    date: str,
) -> None:

    print()
    print("=" * 68)
    print("STAGE 3 / 3：答案与解析")
    print("=" * 68)

    if is_nonempty(answer_path):

        print(
            f"✓ 已存在答案解析：{answer_path}"
        )
        print("✓ 不调用答案解析 AI")
        return

    print("→ 答案解析不存在")
    print("→ 文章和试卷均已准备完成")
    print("→ 现在只调用 exam_answers AI")

    result = gen_answers(
        exam,
        art,
        difficulty,
        article_type,
        words,
    )

    content = render_answers(
        result,
        art["title"],
        difficulty,
        article_type_name,
    )

    write_and_confirm(
        answer_path,
        content,
        "答案与解析",
    )

    git_save_stage(
        [
            answer_path,
        ],
        (
            f"feat(english): "
            f"generate answers analysis {date}"
        ),
        "答案与解析",
    )


# ======================================================================
# Manifest
# ======================================================================

def write_manifest(
    *,
    manifest_path: Path,
    date: str,
    difficulty: int,
    article_type_name: str,
    article_path: Path,
    exam_path: Path,
    answer_path: Path,
    exam_enabled: bool,
) -> None:

    data = {
        "date": date,
        "difficulty": difficulty,
        "article_type": article_type_name,
        "exam": exam_enabled,
        "stages": {
            "article": {
                "path": str(
                    article_path.relative_to(ROOT)
                ),
                "status": (
                    "complete"
                    if is_nonempty(article_path)
                    else "missing"
                ),
            },
            "exam": {
                "path": str(
                    exam_path.relative_to(ROOT)
                ),
                "status": (
                    "complete"
                    if not exam_enabled
                    else (
                        "complete"
                        if is_nonempty(exam_path)
                        else "missing"
                    )
                ),
            },
            "answers_analysis": {
                "path": str(
                    answer_path.relative_to(ROOT)
                ),
                "status": (
                    "complete"
                    if not exam_enabled
                    else (
                        "complete"
                        if is_nonempty(answer_path)
                        else "missing"
                    )
                ),
            },
        },
    }

    save_json(
        manifest_path,
        data,
        "运行清单",
    )

    git_save_stage(
        [
            manifest_path,
        ],
        (
            f"chore(english): "
            f"update manifest {date}"
        ),
        "运行清单",
    )


# ======================================================================
# CLI
# ======================================================================

def build_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(
        description="748686 英语学习系统 V2.4"
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--difficulty",
        type=int,
        required=True,
        choices=range(1, 18),
    )

    parser.add_argument(
        "--article-type",
        required=True,
        choices=ARTICLE_TYPES,
    )

    parser.add_argument(
        "--length",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--exam",
        choices=["yes", "no"],
        default="no",
    )

    parser.add_argument(
        "--image",
        choices=["yes", "no"],
        default="no",
    )

    parser.add_argument(
        "--audio",
        choices=["yes", "no"],
        default="no",
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
# MAIN
# ======================================================================

def main() -> int:

    args = build_parser().parse_args()

    date = args.date
    difficulty = args.difficulty
    article_type = args.article_type
    length = args.length
    exam_enabled = args.exam == "yes"

    article_type_name = (
        ARTICLE_TYPES[article_type]
    )

    print()
    print("=" * 68)
    print("02_英语学习系统 V2.4")
    print("=" * 68)
    print(f"日期：{date}")
    print(f"难度：{difficulty}星")
    print(f"文章类型：{article_type_name}")
    print(f"English ID：{article_type}")
    print(f"目标长度：{length}")
    print(f"考试：{'是' if exam_enabled else '否'}")
    print("=" * 68)

    # ==================================================================
    # 输入
    # ==================================================================

    input_file = (
        ROOT
        / "input"
        / f"{date}.md"
    )

    if not input_file.exists():
        raise FileNotFoundError(
            f"找不到输入文件：{input_file}"
        )

    parsed = parse(
        input_file
    )

    words = list(
        parsed.get("words", [])
    )

    try:
        vision_words = extract(
            input_file
        )

        if vision_words:
            words.extend(
                vision_words
            )

    except Exception as exc:
        print(
            f"⚠ Vision 提取失败，继续使用已有词汇：{exc}"
        )

    # 去重，同时保持原顺序
    dedup_words = []

    for word in words:
        if word not in dedup_words:
            dedup_words.append(word)

    words = dedup_words

    print(
        f"✓ 学习词汇数量：{len(words)}"
    )

    # ==================================================================
    # 输出路径
    # ==================================================================

    output_dir = (
        ROOT
        / "output"
        / date
    )

    article_dir = (
        output_dir
        / "英语短文注记"
    )

    exam_dir = (
        output_dir
        / "配套试卷"
    )

    system_dir = (
        output_dir
        / ".system"
    )

    article_path = (
        article_dir
        / f"{difficulty}星_{article_type_name}.md"
    )

    exam_path = (
        exam_dir
        / f"{difficulty}星_{article_type_name}_试卷.md"
    )

    answer_path = (
        exam_dir
        / f"{difficulty}星_{article_type_name}_答案解析.md"
    )

    article_cache = (
        system_dir
        / "article.json"
    )

    exam_cache = (
        system_dir
        / "exam.json"
    )

    manifest_path = (
        system_dir
        / "manifest.json"
    )

    # ==================================================================
    # Stage 1
    # ==================================================================

    art = load_or_generate_article(
        article_path=article_path,
        article_cache=article_cache,
        words=words,
        difficulty=difficulty,
        article_type=article_type,
        article_type_name=article_type_name,
        length=length,
        date=date,
    )

    # ==================================================================
    # Stage 2 + 3
    # ==================================================================

    if exam_enabled:

        exam = load_or_generate_exam(
            exam_path=exam_path,
            exam_cache=exam_cache,
            art=art,
            words=words,
            difficulty=difficulty,
            article_type=article_type,
            article_type_name=article_type_name,
            date=date,
        )

        load_or_generate_answers(
            answer_path=answer_path,
            exam=exam,
            art=art,
            words=words,
            difficulty=difficulty,
            article_type=article_type,
            article_type_name=article_type_name,
            date=date,
        )

    else:

        print()
        print("✓ exam=no")
        print("✓ 跳过试卷和答案解析")

    # ==================================================================
    # 最终检查
    # ==================================================================

    print()
    print("=" * 68)
    print("最终阶段验证")
    print("=" * 68)

    required = [
        ("英语短文", article_path),
    ]

    if exam_enabled:
        required.extend(
            [
                ("配套试卷", exam_path),
                ("答案解析", answer_path),
            ]
        )

    for label, path in required:

        if not is_nonempty(path):
            raise RuntimeError(
                f"最终验证失败：{label}不存在或为空：{path}"
            )

        print(
            f"✓ {label}：{path}"
        )

    # ==================================================================
    # Manifest
    # ==================================================================

    write_manifest(
        manifest_path=manifest_path,
        date=date,
        difficulty=difficulty,
        article_type_name=article_type_name,
        article_path=article_path,
        exam_path=exam_path,
        answer_path=answer_path,
        exam_enabled=exam_enabled,
    )

    print()
    print("=" * 68)
    print("✓ 本日英语学习任务全部完成")
    print("=" * 68)

    return 0


if __name__ == "__main__":

    try:
        raise SystemExit(
            main()
        )

    except KeyboardInterrupt:

        print(
            "\n用户中断。"
        )

        raise SystemExit(130)

    except Exception as exc:

        print()
        print("=" * 68)
        print("❌ 英语学习系统执行失败")
        print("=" * 68)
        print(str(exc))

        raise SystemExit(1)
