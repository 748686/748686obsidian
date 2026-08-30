#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Source Enrichment V6

============================================================
核心逻辑
============================================================

每次运行：

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


============================================================
V6 核心改进
============================================================

在 V5 基础上增加：

    1. 检查 Enriched 文件夹是否存在
    2. 不存在 → 自动创建
    3. Atomic 是唯一上游标准
    4. 获取 Atomic 实际有效文章数量
    5. 获取 Enriched 实际文件数量
    6. 数量不一致 → 找出缺失文件
    7. 只重新生成缺失 / 无效文件
    8. 已经有效的 Enriched 不重复处理
    9. Enriched 多出来的文件不自动删除
   10. 最终检查 Atomic 与 Enriched 文件是否一一对应


============================================================
重要原则
============================================================

1. Atomic 是唯一上游标准
2. Horizon 原始日报不能冒充 Atomic
3. Enriched 不以“文件夹存在”判断完成
4. Enriched 必须与 Atomic 一一对应
5. 文件夹不存在 → 创建
6. 文件夹存在但文件少 → 补齐
7. 已经有效的 Enriched → 跳过
8. 缺失 / 异常文件 → 重新获取
9. Enriched 多出来的文件 → 不自动删除
10. Atomic 永远不修改
11. Horizon 摘要永远不能冒充原文
12. 原来的文章生成格式保持不变
13. 默认检查前天、昨天、今天
14. 三天全部完成后才成功
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus, urlparse

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
    "(compatible; 748686-Knowledge-Bot/6.0; "
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
# Enriched 有效文件
# ============================================================

def valid_enriched_file(
    path: Path,
):

    if not path.exists():
        return False

    if not path.is_file():
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

    required = [
        "source_status:",
        "content_status:",
        "ai_status:",
        "## Horizon 摘要",
        "## AI 处理状态",
    ]

    for marker in required:

        if marker not in content:
            return False

    return True


# ============================================================
# Atomic 是否为真正有效文件
# ============================================================

def valid_atomic_file(
    path: Path,
):

    if not path.exists():
        return False

    if not path.is_file():
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

    if 'original_source: "Horizon"' not in content:
        return False

    if "## AI处理状态" not in content:
        return False

    return True


# ============================================================
# V6 新增
# Enriched 目录结构检查
# ============================================================

def ensure_enriched_directories(
    enriched_root: Path,
    enriched_zh: Path,
    enriched_en: Path,
):

    print()
    print(
        "CHECK ENRICHED DIRECTORY STRUCTURE"
    )

    if not enriched_root.exists():

        print(
            f"🆕 Enriched root missing:"
        )

        print(
            f"   Creating: {enriched_root}"
        )

        enriched_root.mkdir(
            parents=True,
            exist_ok=True,
        )

    else:

        print(
            f"✓ Enriched root exists:"
        )

        print(
            f"  {enriched_root}"
        )

    if not enriched_zh.exists():

        print(
            f"🆕 ZH directory missing:"
        )

        print(
            f"   Creating: {enriched_zh}"
        )

        enriched_zh.mkdir(
            parents=True,
            exist_ok=True,
        )

    else:

        print(
            f"✓ ZH directory exists"
        )

    if not enriched_en.exists():

        print(
            f"🆕 EN directory missing:"
        )

        print(
            f"   Creating: {enriched_en}"
        )

        enriched_en.mkdir(
            parents=True,
            exist_ok=True,
        )

    else:

        print(
            f"✓ EN directory exists"
        )


# ============================================================
# V6 新增
# Atomic / Enriched 文件集合检查
# ============================================================

def compare_article_sets(
    atomic_dir: Path,
    enriched_dir: Path,
):

    atomic_files = sorted(
        atomic_dir.glob("*.md")
    )

    valid_atomic = [
        file
        for file in atomic_files
        if valid_atomic_file(file)
    ]

    enriched_files = sorted(
        enriched_dir.glob("*.md")
    )

    valid_enriched = [
        file
        for file in enriched_files
        if valid_enriched_file(file)
    ]

    atomic_names = {
        file.name
        for file in valid_atomic
    }

    enriched_names = {
        file.name
        for file in valid_enriched
    }

    missing = sorted(
        atomic_names
        - enriched_names
    )

    unexpected = sorted(
        enriched_names
        - atomic_names
    )

    return {

        "atomic_total":
            len(atomic_files),

        "atomic_valid":
            len(valid_atomic),

        "enriched_total":
            len(enriched_files),

        "enriched_valid":
            len(valid_enriched),

        "missing":
            missing,

        "unexpected":
            unexpected,

        "complete":
            (
                atomic_names
                == enriched_names
                and len(valid_atomic)
                > 0
            ),

    }


# ============================================================
# Enriched 与 Atomic 一一对应验证
# ============================================================

def validate_enriched_directory(
    atomic_dir: Path,
    enriched_dir: Path,
):

    atomic_files = sorted(
        atomic_dir.glob("*.md")
    )

    valid_atomic = []

    invalid_atomic = []

    for file in atomic_files:

        if valid_atomic_file(file):

            valid_atomic.append(
                file
            )

        else:

            invalid_atomic.append(
                file
            )

    expected_names = {
        file.name
        for file in valid_atomic
    }

    enriched_files = sorted(
        enriched_dir.glob("*.md")
    )

    valid_enriched = []

    invalid_enriched = []

    for file in enriched_files:

        if valid_enriched_file(file):

            valid_enriched.append(
                file
            )

        else:

            invalid_enriched.append(
                file
            )

    enriched_names = {
        file.name
        for file in valid_enriched
    }

    missing = sorted(
        expected_names
        - enriched_names
    )

    unexpected = sorted(
        enriched_names
        - expected_names
    )

    complete = (
        len(expected_names)
        == len(enriched_names)
        and not missing
        and not unexpected
        and len(valid_enriched)
        == len(valid_atomic)
    )

    return {

        "complete":
            complete,

        "atomic_total":
            len(atomic_files),

        "atomic_valid":
            len(valid_atomic),

        "atomic_invalid":
            len(invalid_atomic),

        "enriched_total":
            len(enriched_files),

        "enriched_valid":
            len(valid_enriched),

        "enriched_invalid":
            len(invalid_enriched),

        "missing":
            missing,

        "unexpected":
            unexpected,

        "invalid_enriched":
            [
                file.name
                for file in invalid_enriched
            ],

        "invalid_atomic":
            [
                file.name
                for file in invalid_atomic
            ],

    }


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
# 单语言
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path,
):

    # ========================================================
    # V6
    # 输出目录不存在 → 创建
    # ========================================================

    if not output_dir.exists():

        print()
        print(
            f"🆕 Enriched language directory "
            f"missing."
        )

        print(
            f"Creating: {output_dir}"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    else:

        print()
        print(
            f"✓ Enriched language directory "
            f"exists: {output_dir}"
        )

    # ========================================================
    # Atomic 是唯一输入标准
    # ========================================================

    all_atomic = sorted(
        input_dir.glob("*.md")
    )

    atomic_files = []

    for file in all_atomic:

        if valid_atomic_file(file):

            atomic_files.append(
                file
            )

        else:

            print(
                f"⚠️ Ignoring invalid Atomic: "
                f"{file.name}"
            )

    if not atomic_files:

        raise RuntimeError(
            f"Atomic directory contains "
            f"no valid Atomic files: "
            f"{input_dir}"
        )

    # ========================================================
    # V6
    # 先进行数量排查
    # ========================================================

    enriched_files = sorted(
        output_dir.glob("*.md")
    )

    valid_existing_enriched = [
        file
        for file in enriched_files
        if valid_enriched_file(file)
    ]

    atomic_names = {
        file.name
        for file in atomic_files
    }

    enriched_names = {
        file.name
        for file in valid_existing_enriched
    }

    missing_names = sorted(
        atomic_names
        - enriched_names
    )

    unexpected_names = sorted(
        enriched_names
        - atomic_names
    )

    print()
    print(
        "------------------------------------------------------------"
    )

    print(
        "ARTICLE COUNT CHECK"
    )

    print(
        "------------------------------------------------------------"
    )

    print(
        f"Atomic valid articles    : "
        f"{len(atomic_files)}"
    )

    print(
        f"Enriched valid articles  : "
        f"{len(valid_existing_enriched)}"
    )

    print(
        f"Missing Enriched articles: "
        f"{len(missing_names)}"
    )

    print(
        f"Extra Enriched articles  : "
        f"{len(unexpected_names)}"
    )

    if (
        len(atomic_files)
        == len(valid_existing_enriched)
        and not missing_names
    ):

        print(
            "✓ Article count matches."
        )

    else:

        print(
            "⚠️ Article count does not match."
        )

    # ========================================================
    # 显示缺失文件
    # ========================================================

    if missing_names:

        print()
        print(
            "MISSING ENRICHED ARTICLES:"
        )

        for name in missing_names:

            print(
                f"  → {name}"
            )

    # ========================================================
    # 显示多出来的文件
    # ========================================================

    if unexpected_names:

        print()
        print(
            "EXTRA ENRICHED ARTICLES:"
        )

        for name in unexpected_names:

            print(
                f"  ⚠️ {name}"
            )

        print(
            "ℹ️ Extra files will NOT be deleted."
        )

    # ========================================================
    # 统计
    # ========================================================

    stats = {

        "total":
            len(atomic_files),

        "already":
            0,

        "fetched":
            0,

        "unresolved":
            0,

        "rebuilt":
            0,

        "missing":
            len(missing_names),

    }

    # ========================================================
    # 逐篇处理
    # ========================================================

    for index, file in enumerate(
        atomic_files,
        start=1,
    ):

        output_file = (
            output_dir
            / file.name
        )

        print()
        print(
            f"[{index}/{len(atomic_files)}] "
            f"{file.name}"
        )

        # ----------------------------------------------------
        # 已存在且有效 → 跳过
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
        # 缺失 / 无效 → 重新处理
        # ----------------------------------------------------

        if output_file.exists():

            print(
                "♻️ Existing Enriched invalid. "
                "Rebuilding."
            )

            stats[
                "rebuilt"
            ] += 1

        else:

            print(
                "🆕 Enriched missing. "
                "Creating."
            )

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

    # ========================================================
    # STEP 1
    # Atomic 必须存在
    # ========================================================

    print()
    print(
        "STEP 1: CHECK ATOMIC"
    )

    if not atomic_root.exists():

        raise RuntimeError(
            f"{date} Atomic directory missing: "
            f"{atomic_root}"
        )

    atomic_zh.mkdir(
        parents=True,
        exist_ok=True,
    )

    atomic_en.mkdir(
        parents=True,
        exist_ok=True,
    )

    zh_atomic = sorted(
        atomic_zh.glob("*.md")
    )

    en_atomic = sorted(
        atomic_en.glob("*.md")
    )

    zh_valid_atomic = [
        file
        for file in zh_atomic
        if valid_atomic_file(file)
    ]

    en_valid_atomic = [
        file
        for file in en_atomic
        if valid_atomic_file(file)
    ]

    print(
        f"ZH Atomic MD: "
        f"{len(zh_atomic)}"
    )

    print(
        f"ZH Valid Atomic: "
        f"{len(zh_valid_atomic)}"
    )

    print(
        f"EN Atomic MD: "
        f"{len(en_atomic)}"
    )

    print(
        f"EN Valid Atomic: "
        f"{len(en_valid_atomic)}"
    )

    if not zh_valid_atomic:

        raise RuntimeError(
            f"{date} Atomic ZH missing "
            f"or invalid."
        )

    if not en_valid_atomic:

        raise RuntimeError(
            f"{date} Atomic EN missing "
            f"or invalid."
        )

    # ========================================================
    # STEP 2
    # 创建 / 检查 Enriched 文件夹
    # ========================================================

    print()
    print(
        "STEP 2: CHECK / CREATE ENRICHED DIRECTORIES"
    )

    ensure_enriched_directories(
        enriched_root,
        enriched_zh,
        enriched_en,
    )

    # ========================================================
    # STEP 3
    # 判断现有 Enriched 是否完整
    # ========================================================

    print()
    print(
        "STEP 3: VALIDATE EXISTING ENRICHED"
    )

    zh_before = validate_enriched_directory(
        atomic_zh,
        enriched_zh,
    )

    en_before = validate_enriched_directory(
        atomic_en,
        enriched_en,
    )

    print()
    print(
        "ZH Enriched validation:"
    )

    print(
        f"  Atomic valid : "
        f"{zh_before['atomic_valid']}"
    )

    print(
        f"  Enriched MD  : "
        f"{zh_before['enriched_total']}"
    )

    print(
        f"  Enriched valid: "
        f"{zh_before['enriched_valid']}"
    )

    print(
        f"  Missing      : "
        f"{len(zh_before['missing'])}"
    )

    print(
        f"  Unexpected   : "
        f"{len(zh_before['unexpected'])}"
    )

    print(
        f"  Invalid      : "
        f"{len(zh_before['invalid_enriched'])}"
    )

    print(
        f"  Complete     : "
        f"{zh_before['complete']}"
    )

    print()
    print(
        "EN Enriched validation:"
    )

    print(
        f"  Atomic valid : "
        f"{en_before['atomic_valid']}"
    )

    print(
        f"  Enriched MD  : "
        f"{en_before['enriched_total']}"
    )

    print(
        f"  Enriched valid: "
        f"{en_before['enriched_valid']}"
    )

    print(
        f"  Missing      : "
        f"{len(en_before['missing'])}"
    )

    print(
        f"  Unexpected   : "
        f"{len(en_before['unexpected'])}"
    )

    print(
        f"  Invalid      : "
        f"{len(en_before['invalid_enriched'])}"
    )

    print(
        f"  Complete     : "
        f"{en_before['complete']}"
    )

    # ========================================================
    # STEP 4
    # ZH
    # ========================================================

    print()
    print(
        "STEP 4: ENRICH ZH"
    )

    if zh_before["complete"]:

        print(
            "⏭️ ZH Enriched is already complete."
        )

        zh_stats = {

            "total":
                zh_before["atomic_valid"],

            "already":
                zh_before["enriched_valid"],

            "fetched":
                0,

            "unresolved":
                0,

            "rebuilt":
                0,

            "missing":
                0,
        }

    else:

        print(
            "♻️ ZH Enriched incomplete."
        )

        print(
            "→ Checking every Atomic article."
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

    # ========================================================
    # STEP 5
    # EN
    # ========================================================

    print()
    print(
        "STEP 5: ENRICH EN"
    )

    if en_before["complete"]:

        print(
            "⏭️ EN Enriched is already complete."
        )

        en_stats = {

            "total":
                en_before["atomic_valid"],

            "already":
                en_before["enriched_valid"],

            "fetched":
                0,

            "unresolved":
                0,

            "rebuilt":
                0,

            "missing":
                0,
        }

    else:

        print(
            "♻️ EN Enriched incomplete."
        )

        print(
            "→ Checking every Atomic article."
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

    # ========================================================
    # STEP 6
    # 最终严格验证
    # ========================================================

    print()
    print(
        "STEP 6: FINAL VALIDATION"
    )

    zh_final = validate_enriched_directory(
        atomic_zh,
        enriched_zh,
    )

    en_final = validate_enriched_directory(
        atomic_en,
        enriched_en,
    )

    print()
    print(
        f"{date} ZH:"
    )

    print(
        f"  Atomic valid   : "
        f"{zh_final['atomic_valid']}"
    )

    print(
        f"  Enriched valid : "
        f"{zh_final['enriched_valid']}"
    )

    print(
        f"  Missing        : "
        f"{len(zh_final['missing'])}"
    )

    print(
        f"  Unexpected     : "
        f"{len(zh_final['unexpected'])}"
    )

    print(
        f"  Complete       : "
        f"{zh_final['complete']}"
    )

    print()
    print(
        f"{date} EN:"
    )

    print(
        f"  Atomic valid   : "
        f"{en_final['atomic_valid']}"
    )

    print(
        f"  Enriched valid : "
        f"{en_final['enriched_valid']}"
    )

    print(
        f"  Missing        : "
        f"{len(en_final['missing'])}"
    )

    print(
        f"  Unexpected     : "
        f"{len(en_final['unexpected'])}"
    )

    print(
        f"  Complete       : "
        f"{en_final['complete']}"
    )

    if not zh_final["complete"]:

        raise RuntimeError(
            f"{date} ZH Enrichment incomplete: "
            f"Atomic={zh_final['atomic_valid']} "
            f"Enriched={zh_final['enriched_valid']} "
            f"Missing={len(zh_final['missing'])}"
        )

    if not en_final["complete"]:

        raise RuntimeError(
            f"{date} EN Enrichment incomplete: "
            f"Atomic={en_final['atomic_valid']} "
            f"Enriched={en_final['enriched_valid']} "
            f"Missing={len(en_final['missing'])}"
        )

    print()
    print(
        f"✅ {date} SOURCE ENRICHMENT COMPLETE"
    )

    return {

        "date":
            date,

        "zh_atomic":
            zh_final["atomic_valid"],

        "zh_enriched":
            zh_final["enriched_valid"],

        "en_atomic":
            en_final["atomic_valid"],

        "en_enriched":
            en_final["enriched_valid"],

    }


# ============================================================
# 最近三天
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
        "SOURCE ENRICHMENT V6"
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

    # ========================================================
    # 严格 前天 → 昨天 → 今天
    # ========================================================

    for date in dates:

        result = process_date(
            raw_root,
            date,
        )

        results.append(
            result
        )

        print()
        print(
            f"✅ DAY COMPLETE: {date}"
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
            != result["zh_atomic"]
        ):

            raise RuntimeError(
                f"{result['date']} "
                f"ZH enrichment failed"
            )

        if (
            result["en_enriched"]
            != result["en_atomic"]
        ):

            raise RuntimeError(
                f"{result['date']} "
                f"EN enrichment failed"
            )

    print()
    print(
        "✅ THREE-DAY SOURCE "
        "ENRICHMENT COMPLETE"
    )


if __name__ == "__main__":
    main()
