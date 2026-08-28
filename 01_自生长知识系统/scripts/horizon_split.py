#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Digest Splitter V6

用途：
Horizon 每日 summary
        ↓
拆成独立原子新闻 MD
        ↓
Raw News/YYYY-MM-DD-Atomic/
    ├── zh/
    └── en/

特点：
- 不依赖固定的“从 X 条内容中筛选出 Y 条重要资讯”
- 兼容 1. / 1、 / 1) 等编号
- 兼容标题与评分分行
- 清理 HTML entities
- 生成合法 YAML
- 保留 Horizon 摘要
- 自动生成后续 AI 处理占位区域
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


# ============================================================
# 文本清理
# ============================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    text = html.unescape(text)

    # 处理可能存在的双重 HTML 编码
    for _ in range(3):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded

    text = (
        text
        .replace("\ufeff", "")
        .replace("\u200b", "")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def yaml_quote(value: str) -> str:
    value = clean_text(value)

    value = (
        value
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )

    return f'"{value}"'


# ============================================================
# 文件名
# ============================================================

def safe_filename(title: str, number: int) -> str:

    title = clean_text(title)

    title = re.sub(r"<[^>]+>", "", title)

    title = re.sub(
        r'[\\/:*?"<>|]',
        "-",
        title,
    )

    title = re.sub(
        r"\s+",
        " ",
        title,
    ).strip()

    if len(title) > 100:
        title = title[:100].rstrip()

    if not title:
        title = f"atomic-news-{number:03d}"

    return f"{number:03d}-{title}.md"


# ============================================================
# 评分
# ============================================================

SCORE_RE = re.compile(
    r"(?P<score>\d+(?:\.\d+)?)\s*/\s*10"
)


def extract_score(text: str):

    match = SCORE_RE.search(text)

    if not match:
        return None

    try:
        score = float(match.group("score"))

        if 0 <= score <= 10:
            return score

    except ValueError:
        pass

    return None


# ============================================================
# 编号新闻
# ============================================================

NUMBER_RE = re.compile(
    r"""
    ^\s*
    (?P<number>\d{1,3})
    \s*
    (?:[.、\)]) 
    \s*
    (?P<text>.+?)
    \s*$
    """,
    re.VERBOSE,
)


def is_numbered_line(line: str):
    return NUMBER_RE.match(
        clean_text(line)
    )


# ============================================================
# 判断明显不是新闻的编号
# ============================================================

def is_bad_title(title: str) -> bool:

    title = clean_text(title)

    if not title:
        return True

    bad = [
        "AI 创作者雷达",
        "AI Creator Radar",
        "科技新闻",
        "Technology News",
        "新闻",
        "摘要",
        "核心观点",
        "为什么重要",
        "深度分析",
        "结论",
        "参考链接",
        "背景",
        "影响",
        "社区讨论",
    ]

    return title in bad


# ============================================================
# 解析 Horizon
# ============================================================

def parse_digest(text: str):

    lines = text.splitlines()

    items = []

    current = None

    i = 0

    while i < len(lines):

        raw = lines[i]
        line = clean_text(raw)

        match = is_numbered_line(line)

        if match:

            number = int(
                match.group("number")
            )

            candidate = clean_text(
                match.group("text")
            )

            # ------------------------------------------------
            # 排除明显不是新闻的编号
            # ------------------------------------------------

            if not is_bad_title(candidate):

                # 如果标题本身带评分
                score = extract_score(candidate)

                if score is not None:
                    candidate = SCORE_RE.sub(
                        "",
                        candidate,
                    ).strip()

                # 保存上一条
                if current is not None:
                    items.append(current)

                current = {
                    "number": number,
                    "title": candidate,
                    "score": score,
                    "body": [],
                }

                # ------------------------------------------------
                # 下一行可能单独就是评分
                # ------------------------------------------------

                if i + 1 < len(lines):

                    next_line = clean_text(
                        lines[i + 1]
                    )

                    next_score = extract_score(
                        next_line
                    )

                    if (
                        next_score is not None
                        and len(next_line) <= 15
                    ):
                        current["score"] = next_score
                        i += 1

                i += 1
                continue

        # --------------------------------------------------------
        # 普通正文
        # --------------------------------------------------------

        if current is not None:

            if line:

                # 单独评分
                score = extract_score(line)

                if (
                    score is not None
                    and len(line) <= 15
                ):
                    current["score"] = score

                else:
                    current["body"].append(line)

        i += 1

    # 最后一条
    if current is not None:
        items.append(current)

    return items


# ============================================================
# 清理新闻
# ============================================================

def normalize_item(item):

    title = clean_text(
        item["title"]
    )

    body = "\n\n".join(
        clean_text(x)
        for x in item["body"]
        if clean_text(x)
    )

    # 去掉正文中重复标题
    body_parts = []

    for part in body.split("\n\n"):

        part = part.strip()

        if not part:
            continue

        if part == title:
            continue

        body_parts.append(part)

    body = "\n\n".join(body_parts)

    return {
        "number": item["number"],
        "title": title,
        "score": item["score"],
        "body": body,
    }


# ============================================================
# 语言
# ============================================================

def detect_language(text: str):

    chinese = len(
        re.findall(
            r"[\u4e00-\u9fff]",
            text,
        )
    )

    english = len(
        re.findall(
            r"[A-Za-z]",
            text,
        )
    )

    if chinese >= 3 and chinese >= english * 0.05:
        return "zh"

    return "en"


# ============================================================
# Markdown
# ============================================================

def build_markdown(
    item,
    date,
    language,
):

    title = item["title"]
    body = item["body"]
    score = item["score"]

    if score is None:
        score_yaml = "null"
        score_text = "暂无"
    else:
        score_yaml = str(score)
        score_text = f"{score}/10"

    result = f"""---
title: {yaml_quote(title)}
date: {date}
type: "原子新闻"
source: "Horizon"
language: "{language}"
horizon_score: {score_yaml}
status: "待AI处理"
---

# {title}

> Horizon 评分：{score_text}

## Horizon 摘要

{body if body else "暂无 Horizon 摘要。"}

## AI 二次处理

待 27 Skills 处理。

## 知识关联

待 AI 建立。

## 最终分类

待 AI 分类。
"""

    return result


# ============================================================
# 主程序
# ============================================================

def split_digest(
    input_file: Path,
    output_dir: Path,
    date: str,
):

    if not input_file.exists():

        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    text = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    text = clean_text(text)

    print(
        f"Input characters: {len(text)}"
    )

    items = parse_digest(text)

    print(
        f"Detected numbered blocks: {len(items)}"
    )

    if not items:

        # ----------------------------------------------------
        # 输出诊断信息
        # ----------------------------------------------------

        print()
        print(
            "========== DEBUG PREVIEW =========="
        )

        for line in text.splitlines()[:100]:

            if line.strip():

                print(
                    repr(line[:200])
                )

        print(
            "========== END DEBUG =============="
        )

        raise RuntimeError(
            "没有识别到 Horizon 新闻条目。"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    zh_dir = output_dir / "zh"
    en_dir = output_dir / "en"

    zh_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    en_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fallback_language = detect_language(
        text
    )

    generated = 0

    for index, raw_item in enumerate(
        items,
        start=1,
    ):

        item = normalize_item(
            raw_item
        )

        if not item["title"]:
            continue

        language = fallback_language

        # 重新根据标题判断
        if detect_language(
            item["title"]
        ) == "zh":

            language = "zh"

        target_dir = (
            zh_dir
            if language == "zh"
            else en_dir
        )

        filename = safe_filename(
            item["title"],
            index,
        )

        output_file = (
            target_dir / filename
        )

        markdown = build_markdown(
            item=item,
            date=date,
            language=language,
        )

        output_file.write_text(
            markdown,
            encoding="utf-8",
        )

        generated += 1

        print(
            f"[{generated:03d}] "
            f"{language.upper()} "
            f"{item['title']}"
        )

    print()
    print("=" * 70)
    print("Horizon Digest Splitter V6")
    print("=" * 70)
    print(
        f"Generated: {generated}"
    )
    print(
        f"Output: {output_dir}"
    )
    print("=" * 70)

    return generated


# ============================================================
# CLI
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
    )

    parser.add_argument(
        "--output",
        required=True,
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    args = parser.parse_args()

    print("=" * 70)
    print("Horizon Digest Splitter V6")
    print("=" * 70)

    print(
        f"Input : {args.input}"
    )

    print(
        f"Output: {args.output}"
    )

    print(
        f"Date  : {args.date}"
    )

    print()

    count = split_digest(
        Path(args.input),
        Path(args.output),
        args.date,
    )

    if count == 0:

        raise RuntimeError(
            "脚本运行完成，但没有生成文件。"
        )


if __name__ == "__main__":
    main()
