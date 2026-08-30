#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Source Enrichment V4

============================================================
核心逻辑
============================================================

每次运行固定处理：

    前天
    昨天
    今天

目录：

    YYYY-MM-DD-Atomic/
        ├── zh/
        └── en/

        ↓

    YYYY-MM-DD-Enriched/
        ├── zh/
        └── en/

重要原则：

1. 先创建日期 Enriched 文件夹
2. 再创建 zh / en
3. 分别检查 Atomic
4. 分别检查 Enriched
5. 已经存在的文件跳过
6. 缺失文件重新寻找真实原文
7. Atomic 永远不修改
8. Horizon 摘要永远不能冒充原文
9. 三天全部完成后才成功
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import (
    quote_plus,
    urlparse,
)

import requests


# ============================================================
# 配置
# ============================================================

AGNES_BASE_URL = (
    "https://apihub.agnes-ai.com/v1"
)

AGNES_MODEL = (
    "agnes-2.5-flash"
)

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/4.0; "
    "+https://github.com/748686/748686obsidian)"
)

RSS_TIMEOUT = 10

FETCH_TIMEOUT = 15

AGNES_TIMEOUT = 30

MAX_ARTICLE_LENGTH = 50000

MIN_MATCH_SCORE = 0.72


# ============================================================
# 通用
# ============================================================

def clean_text(
    text: str,
):

    if not text:
        return ""

    text = html.unescape(
        text
    )

    text = re.sub(
        r"<script.*?</script>",
        " ",
        text,
        flags=re.I | re.S,
    )

    text = re.sub(
        r"<style.*?</style>",
        " ",
        text,
        flags=re.I | re.S,
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def yaml_escape(
    text: str,
):

    text = clean_text(
        text
    )

    text = text.replace(
        "\\",
        "\\\\",
    )

    text = text.replace(
        '"',
        '\\"',
    )

    text = text.replace(
        "\n",
        " ",
    )

    return text


def normalize_title(
    title: str,
):

    if not title:
        return ""

    title = html.unescape(
        title
    )

    title = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        title,
    )

    title = re.sub(
        r"\(#item-[^)]+\)",
        "",
        title,
        flags=re.I,
    )

    title = re.sub(
        r"[⭐️🌟🔥🚨⚡️]+",
        "",
        title,
    )

    title = re.sub(
        r"\s+",
        " ",
        title,
    )

    return title.strip()


def tokenize(
    title: str,
):

    title = normalize_title(
        title
    )

    title = title.lower()

    words = re.findall(
        r"[a-z0-9]+",
        title,
    )

    return set(words)


# ============================================================
# Front Matter
# ============================================================

def parse_front_matter(
    content: str,
):

    if not content.startswith("---"):

        return {}, content

    parts = content.split(
        "---",
        2,
    )

    if len(parts) < 3:

        return {}, content

    raw = parts[1].strip()

    body = parts[2].lstrip()

    data = {}

    for line in raw.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1,
        )

        key = key.strip()

        value = value.strip()

        value = (
            value
            .strip('"')
            .strip("'")
        )

        data[key] = value

    return data, body


# ============================================================
# URL
# ============================================================

def extract_urls(
    text: str,
):

    urls = re.findall(
        r"https?://[^\s<>\"\]\)]+",
        text,
    )

    result = []

    for url in urls:

        url = url.rstrip(
            ".,;"
        )

        if url not in result:

            result.append(
                url
            )

    return result


# ============================================================
# RSS
# ============================================================

RSS_SOURCES = [

    (
        "https://news.google.com/rss/search"
        "?q={query}"
        "&hl=en-US"
        "&gl=US"
        "&ceid=US:en"
    ),

    (
        "https://www.google.com/alerts/feeds"
        "?q={query}"
    ),

]


def fetch_rss_candidates(
    title: str,
    date: str,
):

    clean_title = normalize_title(
        title
    )

    query = quote_plus(
        clean_title
    )

    candidates = []

    for template in RSS_SOURCES:

        url = template.format(
            query=query
        )

        try:

            response = requests.get(
                url,
                headers={
                    "User-Agent":
                        USER_AGENT
                },
                timeout=RSS_TIMEOUT,
            )

            if response.status_code != 200:
                continue

            text = response.text

            items = re.findall(
                r"<item>(.*?)</item>",
                text,
                flags=re.I | re.S,
            )

            for item in items[:20]:

                title_match = re.search(
                    r"<title>(.*?)</title>",
                    item,
                    flags=re.I | re.S,
                )

                link_match = re.search(
                    r"<link>(.*?)</link>",
                    item,
                    flags=re.I | re.S,
                )

                if (
                    not title_match
                    or not link_match
                ):
                    continue

                candidate_title = clean_text(
                    title_match.group(1)
                )

                candidate_url = clean_text(
                    link_match.group(1)
                )

                if not candidate_url.startswith(
                    "http"
                ):
                    continue

                candidates.append(
                    {
                        "title":
                            candidate_title,

                        "url":
                            candidate_url,

                        "source":
                            urlparse(
                                candidate_url
                            ).netloc,
                    }
                )

        except Exception as exc:

            print(
                f"RSS failed: {exc}"
            )

    unique = {}

    for candidate in candidates:

        unique[
            candidate["url"]
        ] = candidate

    return list(
        unique.values()
    )


# ============================================================
# 标题匹配
# ============================================================

def title_similarity(
    original: str,
    candidate: str,
):

    a = tokenize(
        original
    )

    b = tokenize(
        candidate
    )

    if not a or not b:
        return 0.0

    intersection = len(
        a & b
    )

    union = len(
        a | b
    )

    if union == 0:
        return 0.0

    return (
        intersection
        / union
    )


def rank_candidates(
    title: str,
    candidates: list,
):

    ranked = []

    for candidate in candidates:

        score = title_similarity(
            title,
            candidate["title"],
        )

        candidate = dict(
            candidate
        )

        candidate[
            "match_score"
        ] = round(
            score,
            4,
        )

        ranked.append(
            candidate
        )

    ranked.sort(
        key=lambda x:
            x["match_score"],
        reverse=True,
    )

    return ranked


# ============================================================
# Agnes
# ============================================================

def call_agnes(
    title: str,
    date: str,
    candidates: list,
):

    api_key = os.environ.get(
        "AGNES_API_KEY",
        "",
    )

    if not api_key:

        print(
            "⚠️ AGNES_API_KEY not configured"
        )

        return None

    if not candidates:

        print(
            "ℹ️ No candidates for Agnes."
        )

        return None

    candidate_text = ""

    for index, candidate in enumerate(
        candidates[:15],
        start=1,
    ):

        candidate_text += (
            f"\n[{index}]\n"
            f"title: "
            f"{candidate.get('title','')}\n"
            f"url: "
            f"{candidate.get('url','')}\n"
            f"source: "
            f"{candidate.get('source','')}\n"
            f"match_score: "
            f"{candidate.get('match_score',0)}\n"
        )

    prompt = f"""
你是新闻来源验证器。

任务：
从候选新闻来源中判断，哪个最可能是下面 Horizon 新闻对应的真实原始报道。

原始标题：
{normalize_title(title)}

日期：
{date}

候选来源：
{candidate_text}

严格要求：

1. 不允许把 Horizon 摘要当成原文。
2. 必须根据标题、事件、日期和来源判断。
3. 如果没有可信来源，必须返回 found=false。
4. 不要猜 URL。
5. 只能选择候选列表中的 URL。
6. confidence 必须是 0 到 1。
7. 可信度低于 0.75 时 found 必须为 false。

只返回 JSON：

{{
  "found": true,
  "candidate_index": 1,
  "confidence": 0.91,
  "reason": "标题和事件高度一致"
}}

或者：

{{
  "found": false,
  "candidate_index": 0,
  "confidence": 0.0,
  "reason": "没有可信原始来源"
}}
"""

    payload = {

        "model":
            AGNES_MODEL,

        "messages": [

            {
                "role":
                    "system",

                "content":
                    "你是严格的新闻来源验证器。"
            },

            {
                "role":
                    "user",

                "content":
                    prompt
            },
        ],

        "temperature":
            0.0,

        "max_tokens":
            300,

        "stream":
            False,
    }

    try:

        response = requests.post(

            AGNES_BASE_URL
            + "/chat/completions",

            headers={
                "Authorization":
                    "Bearer "
                    + api_key,

                "Content-Type":
                    "application/json",

                "User-Agent":
                    USER_AGENT,
            },

            json=payload,

            timeout=AGNES_TIMEOUT,
        )

        if response.status_code != 200:

            print(
                "⚠️ Agnes HTTP:",
                response.status_code,
            )

            print(
                response.text[:500]
            )

            return None

        data = response.json()

        text = (
            data
            .get(
                "choices",
                [{}],
            )[0]
            .get(
                "message",
                {},
            )
            .get(
                "content",
                "",
            )
        )

        text = text.strip()

        text = re.sub(
            r"^```json",
            "",
            text,
            flags=re.I,
        )

        text = re.sub(
            r"```$",
            "",
            text,
        )

        text = text.strip()

        return json.loads(
            text
        )

    except Exception as exc:

        print(
            f"⚠️ Agnes failed: {exc}"
        )

        return None


# ============================================================
# HTML
# ============================================================

def extract_html_title(
    content: str,
):

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        content,
        flags=re.I | re.S,
    )

    if match:

        return clean_text(
            match.group(1)
        )

    return ""


def extract_meta(
    content: str,
    name: str,
):

    patterns = [

        rf'<meta[^>]+(?:name|property)=["\']'
        rf'{re.escape(name)}'
        rf'["\'][^>]+content=["\'](.*?)["\']',

        rf'<meta[^>]+content=["\'](.*?)["\'][^>]+'
        rf'(?:name|property)=["\']'
        rf'{re.escape(name)}'
        rf'["\']',

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            content,
            flags=re.I | re.S,
        )

        if match:

            return clean_text(
                match.group(1)
            )

    return ""


def extract_author(
    content: str,
):

    patterns = [

        r'<meta[^>]+name=["\']author["\'][^>]+content=["\'](.*?)["\']',

        r'<meta[^>]+property=["\']article:author["\'][^>]+content=["\'](.*?)["\']',

        r'<meta[^>]+name=["\']byl["\'][^>]+content=["\'](.*?)["\']',

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            content,
            flags=re.I | re.S,
        )

        if match:

            return clean_text(
                match.group(1)
            )

    return ""


def extract_article_text(
    content: str,
):

    match = re.search(
        r"<article[^>]*>(.*?)</article>",
        content,
        flags=re.I | re.S,
    )

    if match:

        article = match.group(1)

    else:

        article = content

    article = re.sub(
        r"<script.*?</script>",
        " ",
        article,
        flags=re.I | re.S,
    )

    article = re.sub(
        r"<style.*?</style>",
        " ",
        article,
        flags=re.I | re.S,
    )

    article = re.sub(
        r"<noscript.*?</noscript>",
        " ",
        article,
        flags=re.I | re.S,
    )

    article = re.sub(
        r"<[^>]+>",
        "\n",
        article,
    )

    article = html.unescape(
        article
    )

    lines = []

    for line in article.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line,
        ).strip()

        if not line:
            continue

        lines.append(line)

    cleaned = []

    previous = ""

    for line in lines:

        if line == previous:
            continue

        cleaned.append(line)

        previous = line

    text = "\n\n".join(
        cleaned
    )

    return text[
        :MAX_ARTICLE_LENGTH
    ]


# ============================================================
# 抓取
# ============================================================

def fetch_url(
    url: str,
):

    print(
        "Fetching:",
        url,
    )

    try:

        response = requests.get(

            url,

            headers={
                "User-Agent":
                    USER_AGENT,

                "Accept":
                    "text/html,"
                    "application/xhtml+xml,"
                    "application/xml;q=0.9,"
                    "*/*;q=0.8",
            },

            timeout=FETCH_TIMEOUT,

            allow_redirects=True,
        )

        response.raise_for_status()

        response.encoding = (
            response.apparent_encoding
            or response.encoding
        )

        content = response.text

        article = extract_article_text(
            content
        )

        return {

            "ok":
                True,

            "url":
                response.url,

            "title":
                extract_html_title(
                    content
                ),

            "description":
                extract_meta(
                    content,
                    "description",
                ),

            "author":
                extract_author(
                    content
                ),

            "article":
                article,

            "status_code":
                response.status_code,
        }

    except Exception as exc:

        print(
            f"⚠️ Fetch failed: {exc}"
        )

        return {

            "ok":
                False,

            "error":
                str(exc),

            "url":
                url,
        }


# ============================================================
# Markdown
# ============================================================

def build_markdown(
    original_content: str,
    metadata: dict,
    source_data: dict,
):

    title = metadata.get(
        "title",
        "Untitled",
    )

    date = metadata.get(
        "date",
        "",
    )

    language = metadata.get(
        "language",
        "",
    )

    horizon_score = metadata.get(
        "horizon_score",
        "null",
    )

    source = metadata.get(
        "source",
        "Unknown",
    )

    if not source:
        source = "Unknown"

    source_url = source_data.get(
        "url",
        "",
    )

    original_title = source_data.get(
        "title",
        "",
    )

    author = source_data.get(
        "author",
        "",
    )

    description = source_data.get(
        "description",
        "",
    )

    article = source_data.get(
        "article",
        "",
    )

    source_status = source_data.get(
        "source_status",
        "unresolved",
    )

    search_method = source_data.get(
        "search_method",
        "unresolved",
    )

    match_score = source_data.get(
        "match_score",
        0.0,
    )

    if source_url:

        parsed = urlparse(
            source_url
        )

        source = (
            parsed.netloc
            or source
        )

    if source_status == "fetched":

        content_status = (
            "full"
            if len(article) >= 500
            else "partial"
        )

    else:

        content_status = (
            "horizon_summary_only"
        )

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
search_method: "{yaml_escape(search_method)}"
match_score: {match_score}
ai_status: "pending"
original_title: "{yaml_escape(original_title)}"
author: "{yaml_escape(author)}"
---

"""

    _, original_body = parse_front_matter(
        original_content
    )

    body = (
        f"# {title}\n\n"
        "## Horizon 摘要\n\n"
    )

    body += original_body.strip()

    body += (
        "\n\n## 原文信息\n\n"
    )

    if source_url:

        body += (
            f"- Source: {source}\n"
            f"- Original URL: "
            f"{source_url}\n"
        )

        if original_title:

            body += (
                f"- Original Title: "
                f"{original_title}\n"
            )

        if author:

            body += (
                f"- Author: "
                f"{author}\n"
            )

        if description:

            body += (
                f"- Description: "
                f"{description}\n"
            )

    else:

        body += (
            "- Source: Unknown\n"
            "- Original URL: "
            "未找到可信原文\n"
        )

    if article:

        body += (
            "\n## 原文正文\n\n"
            + article
        )

    else:

        body += (
            "\n## 原文获取状态\n\n"
            "当前没有找到可信的原始文章。\n\n"
            "Horizon 摘要不会被视为原文。\n"
        )

    body += (
        "\n\n## AI 处理状态\n\n"
        "等待 27 Skills 进行后续处理。\n"
    )

    return front + body


# ============================================================
# 单文件
# ============================================================

def process_file(
    input_file: Path,
    output_file: Path,
):

    print()
    print("=" * 70)

    print(
        f"Processing: "
        f"{input_file.name}"
    )

    print("=" * 70)

    content = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    metadata, _ = parse_front_matter(
        content
    )

    title = normalize_title(
        metadata.get(
            "title",
            input_file.stem,
        )
    )

    date = metadata.get(
        "date",
        "",
    )

    print(
        "Title:",
        title,
    )

    # --------------------------------------------------------
    # 1. Atomic 自带 URL
    # --------------------------------------------------------

    urls = extract_urls(
        content
    )

    if urls:

        print(
            "Direct URL detected."
        )

        result = fetch_url(
            urls[0]
        )

        if result.get("ok"):

            result[
                "source_status"
            ] = "fetched"

            result[
                "search_method"
            ] = "direct_url"

            result[
                "match_score"
            ] = 1.0

            enriched = build_markdown(
                content,
                metadata,
                result,
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
                "✅ Direct source fetched"
            )

            return "fetched"

    # --------------------------------------------------------
    # 2. RSS
    # --------------------------------------------------------

    print(
        "Searching RSS candidates..."
    )

    candidates = fetch_rss_candidates(
        title,
        date,
    )

    ranked = rank_candidates(
        title,
        candidates,
    )

    best = (
        ranked[0]
        if ranked
        else None
    )

    if best:

        print(
            "Best RSS candidate:",
            best["title"],
        )

        print(
            "RSS match:",
            best["match_score"],
        )

    # --------------------------------------------------------
    # 3. RSS 高置信度
    # --------------------------------------------------------

    if (
        best
        and best["match_score"]
        >= MIN_MATCH_SCORE
    ):

        result = fetch_url(
            best["url"]
        )

        if result.get("ok"):

            result[
                "source_status"
            ] = "fetched"

            result[
                "search_method"
            ] = "rss"

            result[
                "match_score"
            ] = best[
                "match_score"
            ]

            enriched = build_markdown(
                content,
                metadata,
                result,
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
                "✅ RSS source fetched"
            )

            return "fetched"

    # --------------------------------------------------------
    # 4. Agnes
    # --------------------------------------------------------

    print(
        "RSS not confident."
    )

    print(
        "→ Calling Agnes fallback..."
    )

    agnes_result = call_agnes(
        title,
        date,
        ranked,
    )

    if agnes_result:

        print(
            "Agnes result:",
            agnes_result,
        )

        if agnes_result.get(
            "found"
        ):

            index = int(
                agnes_result.get(
                    "candidate_index",
                    0,
                )
            )

            confidence = float(
                agnes_result.get(
                    "confidence",
                    0,
                )
            )

            if (
                1
                <= index
                <= len(ranked)
                and confidence
                >= MIN_MATCH_SCORE
            ):

                selected = ranked[
                    index - 1
                ]

                result = fetch_url(
                    selected["url"]
                )

                if result.get("ok"):

                    result[
                        "source_status"
                    ] = "fetched"

                    result[
                        "search_method"
                    ] = "rss+agnes_api"

                    result[
                        "match_score"
                    ] = round(
                        confidence,
                        4,
                    )

                    enriched = build_markdown(
                        content,
                        metadata,
                        result,
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
                        "✅ Agnes verified "
                        "source fetched"
                    )

                    return "fetched"

    # --------------------------------------------------------
    # 5. unresolved
    # --------------------------------------------------------

    print(
        "⚠️ No trustworthy source found."
    )

    result = {

        "source_status":
            "unresolved",

        "search_method":
            "rss+agnes_api",

        "match_score":
            0.0,
    }

    enriched = build_markdown(
        content,
        metadata,
        result,
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        enriched,
        encoding="utf-8",
    )

    return "unresolved"


# ============================================================
# 判断 Enriched 文件是否已经真正生成
# ============================================================

def valid_enriched_file(
    path: Path,
):

    if not path.exists():
        return False

    try:

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

    except Exception:

        return False

    if len(content) < 250:
        return False

    if not content.startswith("---"):
        return False

    return True


# ============================================================
# 单语言
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path,
):

    # --------------------------------------------------------
    # 先建目录
    # --------------------------------------------------------

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    files = sorted(
        input_dir.glob("*.md")
    )

    if not files:

        raise RuntimeError(
            f"Atomic directory empty: "
            f"{input_dir}"
        )

    stats = {

        "total":
            len(files),

        "already":
            0,

        "fetched":
            0,

        "unresolved":
            0,

    }

    for index, file in enumerate(
        files,
        start=1,
    ):

        output_file = (
            output_dir
            / file.name
        )

        print()
        print(
            f"[{index}/{len(files)}] "
            f"{file.name}"
        )

        # ----------------------------------------------------
        # 已存在 → 跳过
        # ----------------------------------------------------

        if valid_enriched_file(
            output_file
        ):

            print(
                "⏭️ Already enriched"
            )

            stats[
                "already"
            ] += 1

            continue

        # ----------------------------------------------------
        # 缺失 → 重新生成
        # ----------------------------------------------------

        status = process_file(
            file,
            output_file,
        )

        if status == "fetched":

            stats[
                "fetched"
            ] += 1

        else:

            stats[
                "unresolved"
            ] += 1

    return stats


# ============================================================
# 单日期
# ============================================================

def process_date(
    raw_root: Path,
    date: str,
):

    print()
    print("#" * 80)

    print(
        f"SOURCE ENRICHMENT: {date}"
    )

    print("#" * 80)

    atomic_root = (
        raw_root
        / f"{date}-Atomic"
    )

    enriched_root = (
        raw_root
        / f"{date}-Enriched"
    )

    atomic_zh = (
        atomic_root / "zh"
    )

    atomic_en = (
        atomic_root / "en"
    )

    enriched_zh = (
        enriched_root / "zh"
    )

    enriched_en = (
        enriched_root / "en"
    )

    # --------------------------------------------------------
    # STEP 1
    # 先建立所有目录
    # --------------------------------------------------------

    print()
    print(
        "STEP 1: CREATE DIRECTORIES"
    )

    atomic_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    atomic_zh.mkdir(
        parents=True,
        exist_ok=True,
    )

    atomic_en.mkdir(
        parents=True,
        exist_ok=True,
    )

    enriched_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    enriched_zh.mkdir(
        parents=True,
        exist_ok=True,
    )

    enriched_en.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"✅ Atomic : {atomic_root}"
    )

    print(
        f"✅ Atomic ZH : {atomic_zh}"
    )

    print(
        f"✅ Atomic EN : {atomic_en}"
    )

    print(
        f"✅ Enriched : {enriched_root}"
    )

    print(
        f"✅ Enriched ZH : {enriched_zh}"
    )

    print(
        f"✅ Enriched EN : {enriched_en}"
    )

    # --------------------------------------------------------
    # STEP 2
    # 检查 Atomic
    # --------------------------------------------------------

    print()
    print(
        "STEP 2: CHECK ATOMIC"
    )

    zh_atomic = sorted(
        atomic_zh.glob("*.md")
    )

    en_atomic = sorted(
        atomic_en.glob("*.md")
    )

    print(
        f"Atomic ZH: "
        f"{len(zh_atomic)}"
    )

    print(
        f"Atomic EN: "
        f"{len(en_atomic)}"
    )

    if not zh_atomic:

        raise RuntimeError(
            f"{date} Atomic ZH missing."
        )

    if not en_atomic:

        raise RuntimeError(
            f"{date} Atomic EN missing."
        )

    # --------------------------------------------------------
    # STEP 3
    # 分别处理 ZH / EN
    # --------------------------------------------------------

    print()
    print(
        "STEP 3: ENRICH ZH"
    )

    zh_stats = process_language(
        atomic_zh,
        enriched_zh,
    )

    print()
    print(
        "ZH RESULT:",
        zh_stats,
    )

    print()
    print(
        "STEP 4: ENRICH EN"
    )

    en_stats = process_language(
        atomic_en,
        enriched_en,
    )

    print()
    print(
        "EN RESULT:",
        en_stats,
    )

    # --------------------------------------------------------
    # STEP 5
    # 分别验证
    # --------------------------------------------------------

    print()
    print(
        "STEP 5: FINAL VALIDATION"
    )

    zh_valid = [
        file
        for file in enriched_zh.glob(
            "*.md"
        )
        if valid_enriched_file(file)
    ]

    en_valid = [
        file
        for file in enriched_en.glob(
            "*.md"
        )
        if valid_enriched_file(file)
    ]

    print(
        f"{date} ZH Atomic   : "
        f"{len(zh_atomic)}"
    )

    print(
        f"{date} ZH Enriched : "
        f"{len(zh_valid)}"
    )

    print(
        f"{date} EN Atomic   : "
        f"{len(en_atomic)}"
    )

    print(
        f"{date} EN Enriched : "
        f"{len(en_valid)}"
    )

    # --------------------------------------------------------
    # 数量必须一一对应
    # --------------------------------------------------------

    if len(zh_valid) < len(
        zh_atomic
    ):

        raise RuntimeError(
            f"{date} ZH Enrichment "
            f"incomplete: "
            f"{len(zh_valid)} / "
            f"{len(zh_atomic)}"
        )

    if len(en_valid) < len(
        en_atomic
    ):

        raise RuntimeError(
            f"{date} EN Enrichment "
            f"incomplete: "
            f"{len(en_valid)} / "
            f"{len(en_atomic)}"
        )

    print()
    print(
        f"✅ {date} SOURCE ENRICHMENT COMPLETE"
    )

    return {

        "date":
            date,

        "zh_atomic":
            len(zh_atomic),

        "zh_enriched":
            len(zh_valid),

        "en_atomic":
            len(en_atomic),

        "en_enriched":
            len(en_valid),

    }


# ============================================================
# 三天
# ============================================================

def calculate_three_dates():

    today = datetime.now().date()

    return [

        (
            today
            - timedelta(days=2)
        ).isoformat(),

        (
            today
            - timedelta(days=1)
        ).isoformat(),

        today.isoformat(),

    ]


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--raw-root",
        default=(
            "01_自生长知识系统/Raw News"
        ),
    )

    parser.add_argument(
        "--date",
        default=None,
        help=(
            "兼容单日期测试。"
            "不提供则运行前天、昨天、今天。"
        ),
    )

    args = parser.parse_args()

    raw_root = Path(
        args.raw_root
    )

    print("=" * 80)

    print(
        "748686 HORIZON "
        "SOURCE ENRICHMENT V4"
    )

    print("=" * 80)

    if args.date:

        dates = [
            args.date
        ]

        print(
            "MODE: SINGLE DATE"
        )

    else:

        dates = calculate_three_dates()

        print(
            "MODE: THREE DAYS"
        )

    print()
    print(
        "Processing dates:"
    )

    for date in dates:

        print(
            f"  - {date}"
        )

    results = []

    for date in dates:

        result = process_date(
            raw_root,
            date,
        )

        results.append(
            result
        )

    # ========================================================
    # 三天最终验证
    # ========================================================

    print()
    print("=" * 80)

    print(
        "THREE-DAY ENRICHMENT FINAL RESULT"
    )

    print("=" * 80)

    for result in results:

        print(
            f"{result['date']} | "
            f"ZH "
            f"{result['zh_enriched']}/"
            f"{result['zh_atomic']} | "
            f"EN "
            f"{result['en_enriched']}/"
            f"{result['en_atomic']}"
        )

        if (
            result["zh_enriched"]
            < result["zh_atomic"]
        ):

            raise RuntimeError(
                f"{result['date']} ZH "
                "enrichment failed"
            )

        if (
            result["en_enriched"]
            < result["en_atomic"]
        ):

            raise RuntimeError(
                f"{result['date']} EN "
                "enrichment failed"
            )

    print()
    print(
        "✅ THREE-DAY SOURCE "
        "ENRICHMENT COMPLETE"
    )


if __name__ == "__main__":
    main()
