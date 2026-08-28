#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon 双语日报拆解器

功能：
1. 同时处理 Horizon summary-zh.md 和 summary-en.md
2. 自动识别日报中的重要资讯条目
3. 每条资讯生成一个独立 Markdown
4. 中文、英文分别存放
5. 自动生成标准 YAML Front Matter
6. 不依赖固定的「从 X 条内容中筛选出 Y 条」文字
7. 支持 Horizon 中英文日报格式略有变化的情况
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


# ============================================================
# 工具函数
# ============================================================

def clean_text(text: str) -> str:
    """清理 Horizon 文本中的常见 HTML/编码残留。"""

    replacements = {
        "&#x27;": "'",
        "&#X27;": "'",
        "&apos;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        "[&-x27;": "'",
        "[&-×27;": "'",
        "&#×27;": "'",
        "&#x2": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # 清除明显的 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)

    # 清除连续空格
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def yaml_escape(text: str) -> str:
    """安全生成 YAML 双引号字符串。"""
    text = clean_text(text)
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", " ")
    return text


def detect_language(path: Path, content: str) -> str:
    """优先根据文件名判断语言，否则根据内容判断。"""

    name = path.name.lower()

    if "-zh" in name or "_zh" in name or "zh" in name:
        return "zh"

    if "-en" in name or "_en" in name or "en" in name:
        return "en"

    chinese = len(re.findall(r"[\u4e00-\u9fff]", content))
    english = len(re.findall(r"[A-Za-z]", content))

    return "zh" if chinese >= english else "en"


# ============================================================
# 提取 Horizon 资讯条目
# ============================================================

def extract_ranked_items(content: str):
    """
    提取类似：

    1. 标题
    8.0/10

    或：

    1. 标题  8.0/10

    或：

    01版-xxxx
    7.0/10

    的 Horizon 条目。
    """

    content = clean_text(content)

    lines = content.splitlines()

    items = []

    current = None

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # ----------------------------------------------------
        # 普通数字排行：
        # 1. 标题
        # 2. 标题
        # ----------------------------------------------------

        m = re.match(
            r"^(\d{1,3})\s*[\.\、\)]\s*(.+?)\s*$",
            line
        )

        if m:
            if current:
                items.append(current)

            current = {
                "rank": int(m.group(1)),
                "title": clean_text(m.group(2)),
                "score": None,
                "body": [],
            }

            continue

        # ----------------------------------------------------
        # 中文版面标题：
        #
        # 01版-xxx
        # 02版-xxx
        #
        # 或：
        # ［01版-xxx］
        # ----------------------------------------------------

        m = re.match(
            r"^[\[［]?\s*(\d{1,2})\s*版\s*[-—–:：]?\s*(.+?)[\]］]?\s*$",
            line
        )

        if m:

            if current:
                items.append(current)

            current = {
                "rank": len(items) + 1,
                "title": clean_text(m.group(2)),
                "score": None,
                "body": [],
            }

            continue

        # ----------------------------------------------------
        # 评分
        # ----------------------------------------------------

        score_match = re.search(
            r"(\d+(?:\.\d+)?)\s*/\s*10",
            line
        )

        if score_match and current:

            current["score"] = float(score_match.group(1))

            # 如果评分后还有文字，保留下来
            remaining = re.sub(
                r"(\d+(?:\.\d+)?)\s*/\s*10",
                "",
                line
            ).strip()

            if remaining:
                current["body"].append(remaining)

            continue

        # ----------------------------------------------------
        # 过滤明显不是正文的 Horizon UI 字段
        # ----------------------------------------------------

        skip_patterns = [
            r"^Horizon\s*$",
            r"^Horizon 摘要$",
            r"^AI Creator Radar$",
            r"^AI创作者雷达$",
            r"^科技新闻$",
            r"^财经新闻$",
            r"^国际新闻$",
            r"^核心资讯$",
            r"^重要资讯$",
            r"^从 .* 条内容中筛选",
            r"^参考链接$",
            r"^Tags?$",
        ]

        if any(re.search(p, line, re.I) for p in skip_patterns):
            continue

        # ----------------------------------------------------
        # 当前条目的正文
        # ----------------------------------------------------

        if current:
            current["body"].append(line)

    if current:
        items.append(current)

    return items


# ============================================================
# 二次清理
# ============================================================

def normalize_items(items):

    result = []

    seen = set()

    for item in items:

        title = clean_text(item["title"])

        if not title:
            continue

        # 清理标题中的评分
        title = re.sub(
            r"\s*\d+(?:\.\d+)?\s*/\s*10\s*$",
            "",
            title
        ).strip()

        # 清理重复标题
        key = title.lower()

        if key in seen:
            continue

        seen.add(key)

        body = []

        for line in item["body"]:

            line = clean_text(line)

            if not line:
                continue

            # 排除一些明显的重复标题
            if line == title:
                continue

            body.append(line)

        item["title"] = title
        item["body"] = body

        result.append(item)

    return result


# ============================================================
# 生成 Atomic Markdown
# ============================================================

def make_atomic_markdown(
    item,
    language: str,
    date: str,
    rank: int,
) -> str:

    title = item["title"]
    score = item.get("score")

    score_text = (
        f"{score:.1f}"
        if isinstance(score, (int, float))
        else ""
    )

    if language == "zh":

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "原子新闻"
source: "Horizon"
language: "zh"
horizon_score: {score_text if score_text else "null"}
status: "待AI处理"
---

# {title}

## Horizon 摘要

"""

    else:

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "Atomic News"
source: "Horizon"
language: "en"
horizon_score: {score_text if score_text else "null"}
status: "待AI处理"
---

# {title}

## Horizon Summary

"""

    body = "\n\n".join(item["body"])

    if not body:
        body = (
            "本文来自 Horizon 日报拆解，"
            "等待后续 AI 二次处理。"
            if language == "zh"
            else
            "This item was extracted from the Horizon digest "
            "and is waiting for further AI processing."
        )

    return front + body.strip() + "\n"


# ============================================================
# 安全文件名
# ============================================================

def safe_filename(title: str, rank: int) -> str:

    title = clean_text(title)

    # 删除 Linux/Windows 不适合文件名的字符
    title = re.sub(
        r'[\\/:*?"<>|]',
        "",
        title
    )

    # 删除 Markdown/HTML 噪声
    title = re.sub(
        r"[#\[\]{}]",
        "",
        title
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    ).strip()

    if not title:
        title = "untitled"

    # 防止文件名过长
    title = title[:100]

    return f"{rank:03d}-{title}.md"


# ============================================================
# 单语言拆解
# ============================================================

def split_one(
    input_file: Path,
    output_dir: Path,
    date: str,
    language: str,
):

    print()
    print("=" * 70)
    print(f"Processing {language.upper()} Horizon digest")
    print("=" * 70)

    print(f"Input : {input_file}")
    print(f"Output: {output_dir}")

    if not input_file.exists():
        raise FileNotFoundError(
            f"找不到 Horizon 日报：{input_file}"
        )

    content = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    items = extract_ranked_items(content)

    items = normalize_items(items)

    if not items:
        raise RuntimeError(
            f"无法从 {input_file} 提取 Horizon 资讯。"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    for index, item in enumerate(items, start=1):

        filename = safe_filename(
            item["title"],
            index,
        )

        path = output_dir / filename

        markdown = make_atomic_markdown(
            item=item,
            language=language,
            date=date,
            rank=index,
        )

        path.write_text(
            markdown,
            encoding="utf-8",
        )

        count += 1

        print(
            f"[{language}] {index:03d} "
            f"{item['title']}"
        )

    print()
    print(
        f"✅ {language.upper()} generated: {count}"
    )

    return count


# ============================================================
# 主程序
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Horizon bilingual digest splitter"
    )

    parser.add_argument(
        "--zh",
        required=True,
        help="中文 Horizon summary",
    )

    parser.add_argument(
        "--en",
        required=True,
        help="英文 Horizon summary",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Atomic 输出根目录",
    )

    parser.add_argument(
        "--date",
        required=True,
        help="日期，例如 2026-08-28",
    )

    args = parser.parse_args()

    zh_input = Path(args.zh)
    en_input = Path(args.en)
    output_root = Path(args.output)

    print("=" * 70)
    print("Horizon Bilingual Digest Splitter")
    print("=" * 70)

    print(f"ZH : {zh_input}")
    print(f"EN : {en_input}")
    print(f"OUT: {output_root}")
    print(f"DATE: {args.date}")

    # --------------------------------------------------------
    # 中文
    # --------------------------------------------------------

    zh_count = split_one(
        input_file=zh_input,
        output_dir=output_root / "zh",
        date=args.date,
        language="zh",
    )

    # --------------------------------------------------------
    # 英文
    # --------------------------------------------------------

    en_count = split_one(
        input_file=en_input,
        output_dir=output_root / "en",
        date=args.date,
        language="en",
    )

    # --------------------------------------------------------
    # 最终验证
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    print(f"Chinese Atomic News : {zh_count}")
    print(f"English Atomic News : {en_count}")

    if zh_count <= 0:
        raise RuntimeError(
            "❌ 中文日报没有生成任何 Atomic News。"
        )

    if en_count <= 0:
        raise RuntimeError(
            "❌ 英文日报没有生成任何 Atomic News。"
        )

    print()
    print("✅ 中文拆解成功")
    print("✅ 英文拆解成功")
    print("✅ Horizon 双语日报拆解全部完成")


if __name__ == "__main__":
    main()
