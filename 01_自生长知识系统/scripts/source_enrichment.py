#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Source Enrichment V1

作用：
1. 读取 Horizon Atomic News
2. 尝试提取原文 URL
3. 如果有 URL：
   - 抓取网页
   - 提取网页标题
   - 保存原始网页内容
4. 如果没有 URL：
   - 保留 Horizon 内容
   - 标记 source_status = pending_search
5. 永远不覆盖 Atomic 原始文件
6. 输出到：
   Raw News/YYYY-MM-DD-Enriched/zh
   Raw News/YYYY-MM-DD-Enriched/en
"""

from __future__ import annotations

import argparse
import html
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


# ============================================================
# 基础设置
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/1.0; "
    "+https://github.com/748686/748686obsidian)"
)

TIMEOUT = 20


# ============================================================
# 文本处理
# ============================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    replacements = {
        "&#x27;": "'",
        "&#X27;": "'",
        "&apos;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = html.unescape(text)

    text = re.sub(r"<script.*?</script>", "", text,
                  flags=re.I | re.S)

    text = re.sub(r"<style.*?</style>", "", text,
                  flags=re.I | re.S)

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(r"[ \t]+", " ", text)

    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)

    return text.strip()


def yaml_escape(text: str) -> str:
    text = clean_text(text)
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", " ")
    return text


# ============================================================
# YAML Front Matter
# ============================================================

def parse_front_matter(content: str):
    """
    读取：

    ---
    title: "..."
    date: ...
    ...
    ---

    返回 dict
    """

    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)

    if len(parts) < 3:
        return {}, content

    raw_yaml = parts[1].strip()
    body = parts[2].lstrip()

    data = {}

    for line in raw_yaml.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip()

        value = value.strip('"').strip("'")

        data[key] = value

    return data, body


# ============================================================
# URL 提取
# ============================================================

def extract_urls(text: str):

    urls = re.findall(
        r'https?://[^\s<>"\]\)]+',
        text
    )

    result = []

    for url in urls:

        url = url.rstrip(".,;")

        try:
            parsed = urlparse(url)

            if parsed.scheme in ("http", "https"):
                result.append(url)

        except Exception:
            pass

    # 去重
    unique = []

    for url in result:
        if url not in unique:
            unique.append(url)

    return unique


# ============================================================
# 网页正文提取
# ============================================================

def extract_html_title(content: str):

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        content,
        flags=re.I | re.S
    )

    if match:
        return clean_text(match.group(1))

    return ""


def extract_meta_content(content: str, name: str):

    patterns = [
        rf'<meta[^>]+(?:name|property)=["\']{re.escape(name)}["\'][^>]+content=["\'](.*?)["\']',
        rf'<meta[^>]+content=["\'](.*?)["\'][^>]+(?:name|property)=["\']{re.escape(name)}["\']',
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            content,
            flags=re.I | re.S
        )

        if match:
            return clean_text(match.group(1))

    return ""


def extract_article_text(content: str):

    # 优先 article
    match = re.search(
        r"<article[^>]*>(.*?)</article>",
        content,
        flags=re.I | re.S
    )

    if match:
        article = match.group(1)
    else:
        article = content

    article = re.sub(
        r"<script.*?</script>",
        "",
        article,
        flags=re.I | re.S
    )

    article = re.sub(
        r"<style.*?</style>",
        "",
        article,
        flags=re.I | re.S
    )

    article = re.sub(
        r"<noscript.*?</noscript>",
        "",
        article,
        flags=re.I | re.S
    )

    article = re.sub(
        r"<[^>]+>",
        "\n",
        article
    )

    article = html.unescape(article)

    lines = []

    for line in article.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if not line:
            continue

        lines.append(line)

    # 去除重复连续行
    cleaned = []

    previous = None

    for line in lines:

        if line == previous:
            continue

        cleaned.append(line)
        previous = line

    return "\n\n".join(cleaned)


# ============================================================
# 获取网页
# ============================================================

def fetch_url(url: str):

    print()
    print("Fetching:")
    print(url)

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        response.encoding = (
            response.apparent_encoding
            or response.encoding
        )

        content = response.text

        title = extract_html_title(content)

        description = extract_meta_content(
            content,
            "description"
        )

        article = extract_article_text(content)

        return {
            "ok": True,
            "url": response.url,
            "title": title,
            "description": description,
            "article": article,
            "status_code": response.status_code,
        }

    except Exception as exc:

        print(
            f"⚠️ Fetch failed: {exc}"
        )

        return {
            "ok": False,
            "error": str(exc),
            "url": url,
        }


# ============================================================
# 生成 Enriched Markdown
# ============================================================

def build_enriched_markdown(
    original_content: str,
    metadata: dict,
    source_data: dict,
):

    title = metadata.get(
        "title",
        "Untitled"
    )

    date = metadata.get(
        "date",
        ""
    )

    language = metadata.get(
        "language",
        ""
    )

    horizon_score = metadata.get(
        "horizon_score",
        "null"
    )

    urls = extract_urls(
        original_content
    )

    # --------------------------------------------------------
    # 有 URL，并且成功抓取
    # --------------------------------------------------------

    if source_data.get("ok"):

        source_url = source_data.get(
            "url",
            ""
        )

        original_title = source_data.get(
            "title",
            ""
        )

        description = source_data.get(
            "description",
            ""
        )

        article = source_data.get(
            "article",
            ""
        )

        source_status = "fetched"

        content_status = (
            "full"
            if len(article) >= 500
            else "partial"
        )

    # --------------------------------------------------------
    # 没有 URL
    # --------------------------------------------------------

    else:

        source_url = (
            urls[0]
            if urls
            else ""
        )

        original_title = ""

        description = ""

        article = ""

        if urls:

            source_status = "fetch_failed"

            content_status = (
                "horizon_summary_only"
            )

        else:

            source_status = "pending_search"

            content_status = (
                "horizon_summary_only"
            )

    # --------------------------------------------------------
    # 来源
    # --------------------------------------------------------

    source = metadata.get(
        "source",
        ""
    )

    # Horizon 不作为真实媒体来源
    if not source or source.lower() == "horizon":

        source = "Unknown"

    # --------------------------------------------------------
    # Front Matter
    # --------------------------------------------------------

    front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "news"
source: "{yaml_escape(source)}"
source_url: "{yaml_escape(source_url)}"
language: "{yaml_escape(language)}"
horizon_score: {horizon_score}
source_status: "{source_status}"
content_status: "{content_status}"
ai_status: "pending"
original_title: "{yaml_escape(original_title)}"
---

"""

    # --------------------------------------------------------
    # 内容
    # --------------------------------------------------------

    body = f"""# {title}

## Horizon 摘要

"""

    # 提取原始 Atomic 正文
    _, original_body = parse_front_matter(
        original_content
    )

    body += original_body.strip()

    # --------------------------------------------------------
    # 原文
    # --------------------------------------------------------

    if source_status == "fetched":

        body += """

## 原文信息

"""

        if original_title:

            body += (
                f"- 原文标题：{original_title}\n"
            )

        if source_url:

            body += (
                f"- 原文链接：{source_url}\n"
            )

        if description:

            body += (
                f"- 页面摘要：{description}\n"
            )

        body += """

## 原文正文

"""

        body += article.strip()

    elif source_status == "pending_search":

        body += """

## 原文获取状态

当前 Atomic News 中没有检测到原始文章链接。

本条新闻将进入下一阶段的原文搜索：

标题 + 日期 + Horizon 信息

目前禁止将 Horizon 摘要误认为原文。

"""

    else:

        body += """

## 原文获取状态

原文链接存在，但本次自动抓取失败。

暂时保留 Horizon 摘要，等待后续重试。

"""

        if source_url:

            body += (
                f"\n原文链接：{source_url}\n"
            )

    body += """

## AI 处理状态

等待 27 Skills 进行后续处理。
"""

    return front + body.strip() + "\n"


# ============================================================
# 处理单个文件
# ============================================================

def process_file(
    input_file: Path,
    output_file: Path,
):

    print()
    print("=" * 70)
    print("Processing")
    print("=" * 70)

    print(
        f"Input : {input_file}"
    )

    print(
        f"Output: {output_file}"
    )

    content = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    metadata, _ = parse_front_matter(
        content
    )

    urls = extract_urls(content)

    print(
        f"Detected URLs: {len(urls)}"
    )

    source_data = {
        "ok": False
    }

    # 有 URL → 尝试获取
    if urls:

        source_data = fetch_url(
            urls[0]
        )

    else:

        print(
            "ℹ️ No source URL found."
        )

    enriched = build_enriched_markdown(
        original_content=content,
        metadata=metadata,
        source_data=source_data,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        enriched,
        encoding="utf-8",
    )

    print(
        "✅ Enriched file created"
    )


# ============================================================
# 处理一个语言目录
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path,
):

    if not input_dir.exists():

        print(
            f"⚠️ Directory does not exist: {input_dir}"
        )

        return 0

    files = sorted(
        input_dir.glob("*.md")
    )

    print()
    print("=" * 70)
    print(
        f"Processing directory: {input_dir}"
    )
    print("=" * 70)

    print(
        f"Files: {len(files)}"
    )

    count = 0

    for file in files:

        output_file = (
            output_dir / file.name
        )

        process_file(
            input_file=file,
            output_file=output_file,
        )

        count += 1

        # 防止连续请求过快
        time.sleep(0.5)

    return count


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Horizon Source Enrichment V1"
    )

    parser.add_argument(
        "--zh",
        required=True,
        help="Chinese Atomic directory",
    )

    parser.add_argument(
        "--en",
        required=True,
        help="English Atomic directory",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Enriched root directory",
    )

    args = parser.parse_args()

    zh_input = Path(args.zh)
    en_input = Path(args.en)
    output_root = Path(args.output)

    print("=" * 70)
    print("HORIZON SOURCE ENRICHMENT V1")
    print("=" * 70)

    print(
        f"ZH input : {zh_input}"
    )

    print(
        f"EN input : {en_input}"
    )

    print(
        f"Output   : {output_root}"
    )

    zh_output = (
        output_root / "zh"
    )

    en_output = (
        output_root / "en"
    )

    zh_count = process_language(
        zh_input,
        zh_output,
    )

    en_count = process_language(
        en_input,
        en_output,
    )

    print()
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(
        f"Chinese enriched files : {zh_count}"
    )

    print(
        f"English enriched files : {en_count}"
    )

    if zh_count == 0 and en_count == 0:

        raise RuntimeError(
            "没有发现任何 Atomic News 文件。"
        )

    print()
    print(
        "✅ SOURCE ENRICHMENT COMPLETE"
    )


if __name__ == "__main__":
    main()
