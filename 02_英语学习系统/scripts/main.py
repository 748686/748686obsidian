#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 英语学习系统
Main Pipeline V2.4

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
V2.4 修复
======================================================================

修复 Stage 2 已存在 Markdown 试卷的结构恢复。

旧版本问题：

    1. Listening 只能识别非常简单的：
           1. xxx

       无法稳定识别：

           **1.** xxx
           **1、** xxx
           1、xxx
           ### 1. xxx

       以及带多行选项的题目。

    2. 旧版本实际上只恢复 Listening，
       Single Choice / Multiple Choice / Cloze /
       Reading / Translation / Writing 均为空结构。

    3. 导致 Stage 3 收到：

           exam["listening"]["A"]["questions"] = []

       最终：

           Listening A 必须正好有5题，实际 0

本版本：

    - 从现有 Markdown 恢复完整试卷结构
    - Listening A/B/C：5/5/5
    - Single Choice：10
    - Multiple Choice：10
    - Cloze：10
    - Reading：5
    - Translation A：5
    - Translation B：5
    - Writing：1

绝对规则：

    本文件不得重新生成或修改原试卷题目。
    现有试卷存在时只读取 Markdown。
"""


from __future__ import annotations

import argparse
import json
import re
import subprocess
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

# 文章生成
from agnes_generate import ARTICLE_TYPES
from agnes_generate import generate as gen_article

# 文章 Markdown 渲染
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
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def save_json(path: Path, data: Any) -> None:
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


# ======================================================================
# 输入
# ======================================================================

def find_input_file(date: str) -> Path | None:
    """
    查找指定日期的英语学习输入文件。
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
    """

    if not article_path.exists():
        return None

    text = read_text(article_path)

    if not text.strip():
        return None

    # 优先读取结构化缓存
    cache_candidates = [
        article_path.with_suffix(".json"),
        article_path.parent
        / f"{article_path.stem}_structure.json",
        article_path.parent
        / f"{article_path.stem}_cache.json",
    ]

    for cache_path in cache_candidates:
        if cache_path.exists():
            try:
                data = load_json(cache_path)

                if isinstance(data, dict):
                    return data

            except Exception:
                pass

    # 没有缓存时，构造基础结构
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

    return (
        article_dir
        / f"{difficulty_name}_{article_type_name}_文章.md"
    )


def get_article_cache_path(
    article_path: Path,
) -> Path:

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
    log(f"→ 难度：{difficulty}星")
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

    cache_path = get_article_cache_path(
        article_path
    )

    # --------------------------------------------------------------
    # 已存在结构化缓存
    # --------------------------------------------------------------

    if cache_path.exists():

        log("✓ 已找到文章结构化缓存")
        log(f"→ {cache_path}")

        try:
            article_data = load_json(
                cache_path
            )

            if isinstance(article_data, dict):

                log("✓ 直接使用现有文章结构")

                return (
                    article_data,
                    article_path,
                )

        except Exception as exc:

            log(
                f"⚠️ 结构化缓存读取失败：{exc}"
            )

    # --------------------------------------------------------------
    # 已存在文章
    # --------------------------------------------------------------

    if article_path.exists():

        log(
            f"✓ 已存在文章：{article_path}"
        )

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
            f"✓ 文章结构化缓存已保存："
            f"{cache_path}"
        )

        return (
            article_data,
            article_path,
        )

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

    log(
        f"✓ 文章已保存：{article_path}"
    )

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

    return (
        article_data,
        article_path,
    )


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


# ======================================================================
# Stage 2 Markdown 恢复工具
# ======================================================================

def _clean_markdown_question_line(
    line: str,
) -> tuple[int | None, str]:
    """
    识别 Markdown 中常见的题号。

    支持：

        1. xxx
        1、xxx
        1) xxx
        **1.** xxx
        **1、** xxx
        ### 1. xxx
        - 1. xxx

    返回：

        (question_number, remaining_text)

    无法识别时：

        (None, "")
    """

    if not isinstance(line, str):
        return None, ""

    text = line.strip()

    if not text:
        return None, ""

    # --------------------------------------------------------------
    # 去掉 Markdown 列表 / 标题前缀
    # --------------------------------------------------------------

    text = re.sub(
        r"^#{1,6}\s+",
        "",
        text,
    )

    text = re.sub(
        r"^[-*+]\s+",
        "",
        text,
    )

    # --------------------------------------------------------------
    # 处理 **1.** xxx
    # --------------------------------------------------------------

    match = re.match(
        r"^\*\*\s*(\d+)\s*[\.\、\)]\s*\*\*\s*(.*)$",
        text,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    # --------------------------------------------------------------
    # 处理 **1. xxx**
    # --------------------------------------------------------------

    match = re.match(
        r"^\*\*\s*(\d+)\s*[\.\、\)]\s*(.*?)\s*\*\*$",
        text,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    # --------------------------------------------------------------
    # 普通题号
    # --------------------------------------------------------------

    match = re.match(
        r"^(\d+)\s*[\.\、\)]\s*(.*)$",
        text,
    )

    if match:
        return (
            int(match.group(1)),
            match.group(2).strip(),
        )

    return None, ""


def _is_option_line(line: str) -> bool:
    """
    判断一行是否是选择题选项。

    支持：

        A. xxx
        B. xxx
        C. xxx
        D. xxx

        - A. xxx
        - B. xxx
    """

    if not isinstance(line, str):
        return False

    text = line.strip()

    text = re.sub(
        r"^[-*+]\s+",
        "",
        text,
    )

    text = re.sub(
        r"^\*\*",
        "",
        text,
    )

    text = re.sub(
        r"\*\*$",
        "",
        text,
    )

    return bool(
        re.match(
            r"^[A-D]\s*[\.\、\)]\s+",
            text,
            flags=re.I,
        )
    )


def _parse_question_blocks(
    content: str,
) -> list[dict[str, Any]]:
    """
    将一个 Markdown section 中的题目恢复为：

        [
            {
                "number": 1,
                "question": "题干\\nA. ...\\nB. ..."
            },
            ...
        ]

    这里不重新生成题目。

    只把 Markdown 原文按题号切成题目块。

    注意：

        exam_answers.py 的 _question_number()
        同时支持 number / question。

    为了最大兼容性，本函数同时保存：

        number
        question
    """

    if not isinstance(content, str):
        return []

    lines = content.splitlines()

    blocks: list[dict[str, Any]] = []

    current_number: int | None = None
    current_lines: list[str] = []

    def flush_current() -> None:

        nonlocal current_number
        nonlocal current_lines

        if current_number is None:
            current_lines = []
            return

        cleaned_lines = []

        for item in current_lines:

            item = item.rstrip()

            if item.strip():
                cleaned_lines.append(
                    item.strip()
                )

        question_text = "\n".join(
            cleaned_lines
        ).strip()

        if question_text:

            blocks.append(
                {
                    "number": current_number,
                    "question": question_text,
                }
            )

        current_number = None
        current_lines = []

    for line in lines:

        number, remaining = (
            _clean_markdown_question_line(
                line
            )
        )

        if number is not None:

            # ------------------------------------------------------
            # 如果已经有上一题，先保存
            # ------------------------------------------------------

            flush_current()

            current_number = number

            if remaining:
                current_lines.append(
                    remaining
                )

            continue

        # ----------------------------------------------------------
        # 当前正在题目块中
        # ----------------------------------------------------------

        if current_number is not None:

            stripped = line.strip()

            # 跳过纯分隔线
            if re.fullmatch(
                r"[-*_]{3,}",
                stripped,
            ):
                continue

            current_lines.append(
                line
            )

    flush_current()

    return blocks


def _extract_section_by_heading(
    text: str,
    heading_patterns: list[str],
    stop_patterns: list[str],
) -> str:
    """
    从 Markdown 中提取一个 section。

    heading_patterns：
        当前 section 标题。

    stop_patterns：
        下一个 section 的标题。

    使用 re.I 只用于 Markdown 标题恢复，
    不涉及语言目录或语言值转换。
    """

    if not isinstance(text, str):
        return ""

    for heading_pattern in heading_patterns:

        match = re.search(
            heading_pattern,
            text,
            flags=re.I | re.M,
        )

        if not match:
            continue

        start = match.end()

        remaining = text[start:]

        if stop_patterns:

            stop_regex = (
                "(?:"
                + "|".join(stop_patterns)
                + ")"
            )

            stop_match = re.search(
                stop_regex,
                remaining,
                flags=re.I | re.M,
            )

            if stop_match:

                return remaining[
                    :stop_match.start()
                ].strip()

        return remaining.strip()

    return ""


def _section_heading_patterns(
    names: list[str],
) -> list[str]:
    """
    根据标题名称构造 Markdown heading 正则。
    """

    result = []

    for name in names:

        escaped = re.escape(name)

        result.append(
            rf"^#{1,6}\s*{escaped}\s*$"
        )

    return result


def _parse_first_section(
    text: str,
    names: list[str],
    stop_names: list[str],
) -> str:

    return _extract_section_by_heading(
        text,
        _section_heading_patterns(
            names
        ),
        _section_heading_patterns(
            stop_names
        ),
    )


def _recover_question_section(
    text: str,
    names: list[str],
    stop_names: list[str],
    expected_count: int,
    section_name: str,
) -> list[dict[str, Any]]:
    """
    恢复一个普通题型 section。

    如果 section 不存在或数量错误，
    直接报错。

    绝不调用 AI 补题。
    """

    content = _parse_first_section(
        text,
        names,
        stop_names,
    )

    if not content:

        raise RuntimeError(
            f"无法从现有试卷 Markdown 恢复："
            f"{section_name}"
        )

    questions = _parse_question_blocks(
        content
    )

    if len(questions) != expected_count:

        raise RuntimeError(
            f"现有试卷 {section_name} "
            f"恢复题目数量错误："
            f"期望 {expected_count}，"
            f"实际 {len(questions)}"
        )

    return questions


def _recover_listening_part(
    text: str,
    part: str,
) -> dict[str, Any]:
    """
    恢复 Listening Part A/B/C。

    支持：

        ## Part A
        ### Part A
        # Part A

    Part 边界：

        下一 Part
        第二大题
        下一大题
        文件结束
    """

    heading_patterns = [
        rf"^#{1,6}\s*Part\s+{part}\s*$",
    ]

    stop_patterns = [
        rf"^#{1,6}\s*Part\s+[ABC]\s*$",
        r"^#{1,6}\s*二[、．\.]\s*单项选择.*$",
        r"^#{1,6}\s*二[、．\.].*$",
        r"^#{1,6}\s*三[、．\.].*$",
        r"^#{1,6}\s*四[、．\.].*$",
        r"^#{1,6}\s*五[、．\.].*$",
        r"^#{1,6}\s*六[、．\.].*$",
        r"^#{1,6}\s*七[、．\.].*$",
        r"^#{1,6}\s*八[、．\.].*$",
        r"^#{1,6}\s*九[、．\.].*$",
        r"^#{1,6}\s*十[、．\.].*$",
    ]

    match = re.search(
        heading_patterns[0],
        text,
        flags=re.I | re.M,
    )

    if not match:

        raise RuntimeError(
            f"现有试卷 Markdown 缺少 "
            f"Listening Part {part}"
        )

    start = match.end()

    remaining = text[start:]

    stop_regex = (
        "(?:"
        + "|".join(stop_patterns)
        + ")"
    )

    stop_match = re.search(
        stop_regex,
        remaining,
        flags=re.I | re.M,
    )

    if stop_match:
        content = remaining[
            :stop_match.start()
        ].strip()
    else:
        content = remaining.strip()

    questions = _parse_question_blocks(
        content
    )

    if len(questions) != 5:

        raise RuntimeError(
            f"现有试卷 Listening Part {part} "
            f"恢复题目数量错误："
            f"期望 5，"
            f"实际 {len(questions)}"
        )

    return {
        "content": content,
        "questions": questions,
    }


def _recover_cloze(
    text: str,
) -> list[dict[str, Any]]:
    """
    恢复完形填空。

    exam_answers.py 需要：

        exam["cloze"] = [
            {
                "questions": [...]
            }
        ]

    如果原 Markdown 中存在一个或多个完形 section，
    这里将所有题目汇总到一个 passage。

    不改变题目文字。
    """

    names = [
        "三、完形填空",
        "三、完形填空（10题）",
        "三、完形填空（共10题）",
        "完形填空",
    ]

    stop_names = [
        "四、阅读理解",
        "四、阅读",
        "阅读理解",
        "五、翻译",
        "六、翻译",
        "七、写作",
        "写作",
    ]

    content = _parse_first_section(
        text,
        names,
        stop_names,
    )

    if not content:

        # 尝试英文/数字型标题
        content = _parse_first_section(
            text,
            [
                "三、完形填空",
                "Cloze",
            ],
            [
                "阅读理解",
                "翻译",
                "写作",
            ],
        )

    if not content:

        raise RuntimeError(
            "无法从现有试卷 Markdown 恢复："
            "Cloze"
        )

    questions = _parse_question_blocks(
        content
    )

    if len(questions) != 10:

        raise RuntimeError(
            "现有试卷 Cloze "
            "恢复题目数量错误："
            f"期望 10，"
            f"实际 {len(questions)}"
        )

    return [
        {
            "questions": questions,
        }
    ]


def _recover_translation(
    text: str,
) -> dict[str, Any]:
    """
    恢复翻译 A/B。

    支持：

        翻译 A：中译英
        翻译 A
        Translation A

        翻译 B：英译中
        翻译 B
        Translation B
    """

    part_a_content = _parse_first_section(
        text,
        [
            "翻译 A：中译英",
            "翻译 A",
            "Translation A：中译英",
            "Translation A",
        ],
        [
            "翻译 B：英译中",
            "翻译 B",
            "Translation B：英译中",
            "Translation B",
            "写作",
            "Writing",
        ],
    )

    part_b_content = _parse_first_section(
        text,
        [
            "翻译 B：英译中",
            "翻译 B",
            "Translation B：英译中",
            "Translation B",
        ],
        [
            "写作",
            "Writing",
            "六、写作",
            "七、写作",
        ],
    )

    if not part_a_content:

        raise RuntimeError(
            "无法从现有试卷 Markdown 恢复："
            "Translation A"
        )

    if not part_b_content:

        raise RuntimeError(
            "无法从现有试卷 Markdown 恢复："
            "Translation B"
        )

    part_a = _parse_question_blocks(
        part_a_content
    )

    part_b = _parse_question_blocks(
        part_b_content
    )

    if len(part_a) != 5:

        raise RuntimeError(
            "现有试卷 Translation A "
            "恢复题目数量错误："
            f"期望 5，"
            f"实际 {len(part_a)}"
        )

    if len(part_b) != 5:

        raise RuntimeError(
            "现有试卷 Translation B "
            "恢复题目数量错误："
            f"期望 5，"
            f"实际 {len(part_b)}"
        )

    return {
        "part_a": part_a,
        "part_b": part_b,
    }


def _recover_writing(
    text: str,
) -> list[dict[str, Any]]:
    """
    恢复写作题。

    当前系统要求正好 1 题。
    """

    content = _parse_first_section(
        text,
        [
            "写作",
            "七、写作",
            "六、写作",
            "Writing",
        ],
        [],
    )

    if not content:

        raise RuntimeError(
            "无法从现有试卷 Markdown 恢复："
            "Writing"
        )

    questions = _parse_question_blocks(
        content
    )

    if len(questions) != 1:

        raise RuntimeError(
            "现有试卷 Writing "
            "恢复题目数量错误："
            f"期望 1，"
            f"实际 {len(questions)}"
        )

    return questions


def recover_exam(
    exam_path: Path,
) -> dict[str, Any] | None:
    """
    从已有试卷 Markdown 中恢复完整试卷结构。

    重要：

        本函数只读取现有 Markdown。
        不调用 AI。
        不重新生成题目。
        不修改原 Markdown。

    返回结构与 exam_generate.generate()
    兼容，至少满足 exam_answers.py 的读取要求。
    """

    if not exam_path.exists():
        return None

    text = read_text(exam_path)

    if not text.strip():
        return None

    log("")
    log(
        "  → 开始从 Markdown 恢复完整试卷结构"
    )

    # --------------------------------------------------------------
    # 基础结构
    # --------------------------------------------------------------

    exam: dict[str, Any] = {
        "raw_markdown": text,
        "title": "",
        "listening": {},
        "single_choice": [],
        "multiple_choice": [],
        "cloze": [],
        "reading": [],
        "translation": {},
        "writing": [],
    }

    # --------------------------------------------------------------
    # 标题
    # --------------------------------------------------------------

    title_match = re.search(
        r"^#\s+(.+)$",
        text,
        flags=re.M,
    )

    if title_match:
        exam["title"] = (
            title_match.group(1).strip()
        )

    # --------------------------------------------------------------
    # Listening A / B / C
    # --------------------------------------------------------------

    listening_a = _recover_listening_part(
        text,
        "A",
    )

    listening_b = _recover_listening_part(
        text,
        "B",
    )

    listening_c = _recover_listening_part(
        text,
        "C",
    )

    exam["listening"] = {
        "A": listening_a,
        "B": listening_b,
        "C": listening_c,
    }

    log(
        "  ✓ Listening 恢复："
        f"A={len(listening_a['questions'])} "
        f"B={len(listening_b['questions'])} "
        f"C={len(listening_c['questions'])}"
    )

    # --------------------------------------------------------------
    # Single Choice
    # --------------------------------------------------------------

    single = _recover_question_section(
        text,
        [
            "二、单项选择",
            "二、单项选择题",
            "单项选择",
            "单项选择题",
        ],
        [
            "三、完形填空",
            "完形填空",
            "四、阅读理解",
            "阅读理解",
            "翻译",
            "写作",
        ],
        10,
        "Single Choice",
    )

    exam["single_choice"] = single

    log(
        f"  ✓ Single Choice = {len(single)}"
    )

    # --------------------------------------------------------------
    # Multiple Choice
    # --------------------------------------------------------------

    multiple = _recover_question_section(
        text,
        [
            "多项选择",
            "多项选择题",
            "三、 多项选择",
            "三、多项选择",
            "四、多项选择",
        ],
        [
            "完形填空",
            "阅读理解",
            "翻译",
            "写作",
        ],
        10,
        "Multiple Choice",
    )

    exam["multiple_choice"] = multiple

    log(
        f"  ✓ Multiple Choice = {len(multiple)}"
    )

    # --------------------------------------------------------------
    # Cloze
    # --------------------------------------------------------------

    cloze = _recover_cloze(
        text
    )

    exam["cloze"] = cloze

    log(
        f"  ✓ Cloze = "
        f"{sum(len(x.get('questions', [])) for x in cloze)}"
    )

    # --------------------------------------------------------------
    # Reading
    # --------------------------------------------------------------

    reading = _recover_question_section(
        text,
        [
            "四、阅读理解",
            "阅读理解",
            "阅读",
        ],
        [
            "翻译",
            "写作",
            "Translation A",
            "Translation B",
            "Writing",
        ],
        5,
        "Reading",
    )

    exam["reading"] = reading

    log(
        f"  ✓ Reading = {len(reading)}"
    )

    # --------------------------------------------------------------
    # Translation
    # --------------------------------------------------------------

    translation = _recover_translation(
        text
    )

    exam["translation"] = translation

    log(
        "  ✓ Translation = "
        f"A={len(translation['part_a'])} "
        f"B={len(translation['part_b'])}"
    )

    # --------------------------------------------------------------
    # Writing
    # --------------------------------------------------------------

    writing = _recover_writing(
        text
    )

    exam["writing"] = writing

    log(
        f"  ✓ Writing = {len(writing)}"
    )

    # --------------------------------------------------------------
    # 最终恢复完整性检查
    # --------------------------------------------------------------

    expected = {
        "listening_a": 5,
        "listening_b": 5,
        "listening_c": 5,
        "single_choice": 10,
        "multiple_choice": 10,
        "cloze": 10,
        "reading": 5,
        "translation_a": 5,
        "translation_b": 5,
        "writing": 1,
    }

    actual = {
        "listening_a": len(
            exam["listening"]["A"]["questions"]
        ),
        "listening_b": len(
            exam["listening"]["B"]["questions"]
        ),
        "listening_c": len(
            exam["listening"]["C"]["questions"]
        ),
        "single_choice": len(
            exam["single_choice"]
        ),
        "multiple_choice": len(
            exam["multiple_choice"]
        ),
        "cloze": sum(
            len(x.get("questions", []))
            for x in exam["cloze"]
        ),
        "reading": len(
            exam["reading"]
        ),
        "translation_a": len(
            exam["translation"]["part_a"]
        ),
        "translation_b": len(
            exam["translation"]["part_b"]
        ),
        "writing": len(
            exam["writing"]
        ),
    }

    for key, expected_value in expected.items():

        actual_value = actual[key]

        if actual_value != expected_value:

            raise RuntimeError(
                "现有试卷恢复完整性检查失败："
                f"{key} "
                f"期望 {expected_value}，"
                f"实际 {actual_value}"
            )

    log("")
    log(
        "  ✓ 现有试卷 Markdown 已完整恢复"
    )

    log(
        "  ✓ Listening A/B/C = 5/5/5"
    )

    log(
        "  ✓ Single Choice = 10"
    )

    log(
        "  ✓ Multiple Choice = 10"
    )

    log(
        "  ✓ Cloze = 10"
    )

    log(
        "  ✓ Reading = 5"
    )

    log(
        "  ✓ Translation A/B = 5/5"
    )

    log(
        "  ✓ Writing = 1"
    )

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

        log(
            f"✓ 已存在试卷：{exam_path}"
        )

        log("→ 不调用试卷 AI")
        log("→ 正在恢复试卷结构")

        try:

            exam_data = recover_exam(
                exam_path
            )

            if exam_data is not None:

                return (
                    exam_data,
                    exam_path,
                )

        except Exception as exc:

            # ------------------------------------------------------
            # 重要：
            #
            # 现有试卷存在但无法可靠恢复时，
            # 不偷偷调用 AI 覆盖原试卷。
            #
            # 直接失败，让错误明确暴露。
            # ------------------------------------------------------

            raise RuntimeError(
                "现有试卷存在，但无法可靠恢复。"
                "为保护原试卷，本次不会重新生成试卷。\n"
                f"恢复错误：{exc}"
            ) from exc

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
        article_data.get(
            "title",
            "",
        ),
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

    log(
        f"✓ 已保存：{exam_path}"
    )

    return (
        generated,
        exam_path,
    )


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

    text = read_text(
        answers_path
    )

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

        log(
            f"✓ 已存在答案解析："
            f"{answers_path}"
        )

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

    existing = [
        p
        for p in paths
        if p.exists()
    ]

    if not existing:
        log(
            "→ 没有需要 Git 保存的文件"
        )
        return

    log("")
    log("=" * 60)
    log(f"Git 保存：{message}")
    log("=" * 60)

    # --------------------------------------------------------------
    # GitHub Actions Runner Git 身份
    # --------------------------------------------------------------

    subprocess.run(
        [
            "git",
            "config",
            "user.name",
            "github-actions[bot]",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    subprocess.run(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    # --------------------------------------------------------------
    # Git Add
    # --------------------------------------------------------------

    relative_paths = [
        str(
            p.relative_to(REPO_ROOT)
        )
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

    # --------------------------------------------------------------
    # 检查 staged 是否有变化
    # --------------------------------------------------------------

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

        log(
            "→ 没有新的 Git 变更"
        )

        return

    # --------------------------------------------------------------
    # Git Commit
    # --------------------------------------------------------------

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

    log(
        "✓ Git commit 完成"
    )

    # --------------------------------------------------------------
    # Git Push
    # --------------------------------------------------------------

    subprocess.run(
        [
            "git",
            "push",
        ],
        cwd=REPO_ROOT,
        check=True,
    )

    log(
        "✓ Git push 完成"
    )


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
        choices=["mp3", "m4a", "wav"],
        default="mp3",
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

    input_file = find_input_file(
        date
    )

    if input_file is None:
        raise FileNotFoundError(
            f"未找到 {date} 的输入文件"
        )

    log("")
    log(
        f"输入文件：{input_file}"
    )

    # --------------------------------------------------------------
    # 解析输入
    #
    # input_parser.parse() 的真实返回值：
    #     words, images
    # --------------------------------------------------------------

    words, images = parse(
        input_file
    )

    words = list(words)

    log(
        f"✓ 学习词汇数量：{len(words)}"
    )

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
        log(
            "→ --exam=no，"
            "跳过 Stage 2 / Stage 3"
        )

    # --------------------------------------------------------------
    # 完成
    # --------------------------------------------------------------

    log("")
    log("=" * 60)
    log("748686 英语学习系统 COMPLETE")
    log("=" * 60)


if __name__ == "__main__":
    main()
