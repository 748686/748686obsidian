#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Bilingual Digest Splitter V6

功能：
1. 同时处理中文 / 英文 Horizon 日报
2. 自动识别排行资讯
3. 每条资讯生成独立 Markdown
4. zh / en 分开保存
5. 保留 Horizon 的完整上下文
6. 尽可能提取真实新闻来源
7. 尽可能提取原文 URL
8. YAML Front Matter 标准化
9. 不使用“原子新闻”作为新闻类型
10. Horizon 只作为 original_source
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


# ============================================================
# 基础清理
# ============================================================

def clean_text(text: str) -> str:
    """清理 Horizon 常见 HTML / 编码残留。"""

    if not text:
        return ""

    # HTML entity
    text = html.unescape(text)

    replacements = {
        "&#x27;": "'",
        "&#X27;": "'",
        "&#39;": "'",
        "&apos;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        "[&-x27;": "'",
        "[&-×27;": "'",
        "&#×27;": "'",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # HTML 标签
    text = re.sub(r"<[^>]+>", "", text)

    # Markdown 图片
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)

    # 多余空格
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def yaml_escape(text: str) -> str:
    text = clean_text(text)
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", " ")
    return text


# ============================================================
# 语言判断
# ============================================================

def detect_language(path: Path, content: str) -> str:

    name = path.name.lower()

    if "-zh" in name or "_zh" in name:
        return "zh"

    if "-en" in name or "_en" in name:
        return "en"

    chinese = len(re.findall(r"[\u4e00-\u9fff]", content))
    english = len(re.findall(r"[A-Za-z]", content))

    return "zh" if chinese >= english else "en"


# ============================================================
# 来源识别
# ============================================================

KNOWN_SOURCES = [
    "Reuters",
    "BBC",
    "CNN",
    "ABC News",
    "NBC News",
    "CBS News",
    "NPR",
    "The New York Times",
    "The Washington Post",
    "The Guardian",
    "The Economist",
    "Financial Times",
    "Fox News",
    "Associated Press",
    "AP",
    "Bloomberg",
    "The Atlantic",
    "France 24",
    "Le Monde",
    "Le Figaro",
    "Der Spiegel",
    "Frankfurter Allgemeine Zeitung",
    "Japan Times",
    "NHK",
    "KBS",
    "MBC",
    "SBS",
    "YTN",
    "人民日报",
    "新华社",
    "央视",
    "中国新闻网",
    "中国日报",
    "环球时报",
    "澎湃新闻",
    "财新",
    "第一财经",
    "证券时报",
    "界面新闻",
    "36氪",
    "虎嗅",
]


def detect_source(text: str) -> str:

    text_clean = clean_text(text)

    for source in KNOWN_SOURCES:
        if source.lower() in text_clean.lower():
            return source

    # URL 域名识别
    domains = {
        "reuters.com": "Reuters",
        "bbc.com": "BBC",
        "bbc.co.uk": "BBC",
        "cnn.com": "CNN",
        "nytimes.com": "The New York Times",
        "washingtonpost.com": "The Washington Post",
        "theguardian.com": "The Guardian",
        "ft.com": "Financial Times",
        "bloomberg.com": "Bloomberg",
        "npr.org": "NPR",
        "apnews.com": "Associated Press",
        "abcnews.go.com": "ABC News",
        "nbcnews.com": "NBC News",
        "cbsnews.com": "CBS News",
        "foxnews.com": "Fox News",
        "france24.com": "France 24",
        "lemonde.fr": "Le Monde",
        "lefigaro.fr": "Le Figaro",
        "spiegel.de": "Der Spiegel",
        "faz.net": "Frankfurter Allgemeine Zeitung",
        "japantimes.co.jp": "Japan Times",
        "nhk.or.jp": "NHK",
        "kbs.co.kr": "KBS",
    }

    for domain, source in domains.items():
        if domain in text_clean.lower():
            return source

    return "Unknown"


# ============================================================
# URL 提取
# ============================================================

def extract_urls(text: str) -> list[str]:

    urls = re.findall(
        r"https?://[^\s<>\]\)]+",
        text
    )

    cleaned = []

    for url in urls:

        url = url.rstrip(
            ".,;:!?)]}>'\""
        )

        if url not in cleaned:
            cleaned.append(url)

    return cleaned


# ============================================================
# Horizon 条目识别
# ============================================================

def is_rank_line(line: str):

    return re.match(
        r"^\s*(\d{1,3})\s*[\.\、\)]\s*(.+?)\s*$",
        line
    )


def is_score_line(line: str):

    return re.search(
        r"(\d+(?:\.\d+)?)\s*/\s*10",
        line
    )


def is_section_heading(line: str):

    patterns = [
        r"^科技新闻$",
        r"^财经新闻$",
        r"^国际新闻$",
        r"^国内新闻$",
        r"^AI新闻$",
        r"^重要资讯$",
        r"^核心资讯$",
        r"^Horizon$",
        r"^Horizon 摘要$",
        r"^AI Creator Radar$",
        r"^AI创作者雷达$",
        r"^参考链接$",
        r"^Tags?$",
    ]

    return any(
        re.search(pattern, line, re.I)
        for pattern in patterns
    )


def extract_ranked_items(content: str):

    lines = content.splitlines()

    items = []
    current = None

    for raw in lines:

        line = clean_text(raw)

        if not line:
            continue

        # --------------------------------------------
        # 数字排行
        # --------------------------------------------

        match = is_rank_line(line)

        if match:

            if current:
                items.append(current)

            rank = int(match.group(1))
            title = clean_text(match.group(2))

            # 去掉标题尾部评分
            score_match = re.search(
                r"(\d+(?:\.\d+)?)\s*/\s*10",
                title
            )

            score = None

            if score_match:

                score = float(
                    score_match.group(1)
                )

                title = re.sub(
                    r"\s*\d+(?:\.\d+)?\s*/\s*10",
                    "",
                    title
                ).strip()

            current = {
                "rank": rank,
                "title": title,
                "score": score,
                "body": [],
            }

            continue

        # --------------------------------------------
        # 中文版面标题
        # --------------------------------------------

        match = re.match(
            r"^[\[［]?\s*(\d{1,2})\s*版\s*[-—–:：]?\s*(.+?)[\]］]?\s*$",
            line
        )

        if match:

            if current:
                items.append(current)

            current = {
                "rank": len(items) + 1,
                "title": clean_text(match.group(2)),
                "score": None,
                "body": [],
            }

            continue

        # --------------------------------------------
        # 评分
        # --------------------------------------------

        score_match = is_score_line(line)

        if score_match and current:

            current["score"] = float(
                score_match.group(1)
            )

            remaining = re.sub(
                r"\d+(?:\.\d+)?\s*/\s*10",
                "",
                line
            ).strip()

            if remaining:
                current["body"].append(
                    remaining
                )

            continue

        # --------------------------------------------
        # UI 噪声
        # --------------------------------------------

        if is_section_heading(line):
            continue

        # --------------------------------------------
        # 当前新闻正文
        # --------------------------------------------

        if current:
            current["body"].append(line)

    if current:
        items.append(current)

    return items


# ============================================================
# 新闻清理
# ============================================================

def normalize_items(items):

    result = []
    seen = set()

    for item in items:

        title = clean_text(
            item.get("title", "")
        )

        if not title:
            continue

        # 删除评分
        title = re.sub(
            r"\s*\d+(?:\.\d+)?\s*/\s*10\s*$",
            "",
            title
        ).strip()

        # 删除重复
        key = re.sub(
            r"\W+",
            "",
            title.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        body = []

        for line in item.get("body", []):

            line = clean_text(line)

            if not line:
                continue

            # 重复标题
            if line == title:
                continue

            body.append(line)

        item["title"] = title
        item["body"] = body

        result.append(item)

    return result


# ============================================================
# 生成 Markdown
# ============================================================

def make_atomic_markdown(
    item,
    language,
    date,
):

    title = clean_text(
        item["title"]
    )

    body = item.get("body", [])

    combined = "\n".join(body)

    urls = extract_urls(combined)

    source = detect_source(
        title + "\n" + combined
    )

    score = item.get("score")

    score_text = (
        f"{score:.1f}"
        if isinstance(score, (int, float))
        else "null"
    )

    original_url = (
        urls[0]
        if urls
        else ""
    )

    if language == "zh":

        type_name = "新闻"

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "{type_name}"
source: "{yaml_escape(source)}"
language: "zh"
horizon_score: {score_text}
original_source: "Horizon"
original_url: "{yaml_escape(original_url)}"
status: "待AI处理"
---

# {title}

## Horizon 摘要

"""

    else:

        type_name = "新闻"

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "{type_name}"
source: "{yaml_escape(source)}"
language: "en"
horizon_score: {score_text}
original_source: "Horizon"
original_url: "{yaml_escape(original_url)}"
status: "待AI处理"
---

# {title}

## Horizon Summary

"""

    # 保留完整正文
    content = "\n\n".join(body).strip()

    if content:

        front += content
        front += "\n\n"

    else:

        front += (
            "Horizon 日报中未提供该条目的完整正文。"
            "\n\n"
            if language == "zh"
            else
            "The Horizon digest did not provide "
            "a full body for this item.\n\n"
        )

    # 原文
    front += "## 原文信息\n\n"

    front += f"- Source: {source}\n"

    if original_url:

        front += (
            f"- Original URL: {original_url}\n"
        )

    else:

        front += (
            "- Original URL: 未从 Horizon 日报中找到\n"
        )

    front += (
        "\n## AI处理状态\n\n"
        "等待后续 AI 二次处理及 27 Skills 分析。\n"
    )

    return front


# ============================================================
# 文件名
# ============================================================

def safe_filename(title, rank):

    title = clean_text(title)

    title = re.sub(
        r'[\\/:*?"<>|]',
        "",
        title
    )

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

    title = title[:100]

    return f"{rank:03d}-{title}.md"


# ============================================================
# 单语言
# ============================================================

def split_one(
    input_file,
    output_dir,
    date,
    language,
):

    print()
    print("=" * 70)
    print(f"Processing {language.upper()}")
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

    items = extract_ranked_items(
        content
    )

    items = normalize_items(
        items
    )

    if not items:

        raise RuntimeError(
            f"无法从 {input_file} 提取新闻。"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    for index, item in enumerate(
        items,
        start=1
    ):

        filename = safe_filename(
            item["title"],
            index,
        )

        path = output_dir / filename

        markdown = make_atomic_markdown(
            item=item,
            language=language,
            date=date,
        )

        path.write_text(
            markdown,
            encoding="utf-8",
        )

        # 内容长度保护
        if len(markdown) < 250:

            raise RuntimeError(
                f"生成文件异常过短：{path}"
            )

        print(
            f"[{language}] "
            f"{index:03d} "
            f"{item['title']}"
        )

        count += 1

    print()
    print(
        f"✅ {language.upper()} generated: {count}"
    )

    return count


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--zh",
        required=True,
    )

    parser.add_argument(
        "--en",
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

    zh_input = Path(args.zh)
    en_input = Path(args.en)

    output_root = Path(
        args.output
    )

    print("=" * 70)
    print(
        "Horizon Bilingual Digest Splitter V6"
    )
    print("=" * 70)

    zh_count = split_one(
        zh_input,
        output_root / "zh",
        args.date,
        "zh",
    )

    en_count = split_one(
        en_input,
        output_root / "en",
        args.date,
        "en",
    )

    print()
    print("=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    print(
        f"Chinese Atomic News : {zh_count}"
    )

    print(
        f"English Atomic News : {en_count}"
    )

    if zh_count <= 0:
        raise RuntimeError(
            "中文拆解失败"
        )

    if en_count <= 0:
        raise RuntimeError(
            "英文拆解失败"
        )

    print()
    print(
        "✅ 中文拆解成功"
    )

    print(
        "✅ 英文拆解成功"
    )

    print(
        "✅ Horizon 双语拆解完成"
    )


if __name__ == "__main__":
    main()
