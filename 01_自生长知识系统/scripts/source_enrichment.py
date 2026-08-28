#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Source Enrichment V2.1

目标：

1. 读取 Horizon Atomic News
2. 优先使用 Atomic 中已有 URL
3. 没有 URL 时：
   - Google News RSS 搜索
   - Bing News RSS 搜索
4. 多查询并行执行
5. 建立候选来源池
6. 标题标准化 + 模糊匹配
7. 高可信候选直接抓取
8. 匹配不确定时调用 AGNES API
9. AGNES API 负责从候选来源中选择最可信真实来源
10. 获取真实网页正文
11. 尽可能识别真实媒体与作者
12. 永远不修改 Atomic 原文件
13. 输出：
    Raw News/YYYY-MM-DD-Enriched/zh
    Raw News/YYYY-MM-DD-Enriched/en

环境变量：

AGNES_API_KEY
AGNES_API_BASE_URL   可选
AGNES_API_MODEL      可选

默认：

AGNES_API_BASE_URL=https://api.openai.com/v1
AGNES_API_MODEL=gpt-4o-mini

如果你的 Agnes 服务不是 OpenAI-compatible，
只需要修改 AGNES_API_BASE_URL / AGNES_API_MODEL。
"""

from __future__ import annotations

import argparse
import concurrent.futures
import difflib
import html
import json
import os
import re
import time
import unicodedata
import xml.etree.ElementTree as ET

from pathlib import Path
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen


# ============================================================
# 基础配置
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/2.1; "
    "+https://github.com/748686/748686obsidian)"
)

TIMEOUT = 15

MAX_WORKERS = 10

MAX_CANDIDATES_PER_ITEM = 12

MIN_DIRECT_MATCH = 0.90

MIN_API_MATCH = 0.60

MAX_ARTICLE_CHARS = 60000


# ============================================================
# 基础文本处理
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(
        r"<script.*?</script>",
        " ",
        text,
        flags=re.I | re.S
    )

    text = re.sub(
        r"<style.*?</style>",
        " ",
        text,
        flags=re.I | re.S
    )

    text = re.sub(
        r"<noscript.*?</noscript>",
        " ",
        text,
        flags=re.I | re.S
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text
    )

    return text.strip()


def yaml_escape(text: str) -> str:

    text = clean_text(text)

    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", " ")

    return text


# ============================================================
# 标题标准化
# ============================================================

def normalize_title(title: str) -> str:

    if not title:
        return ""

    title = html.unescape(title)

    title = unicodedata.normalize(
        "NFKC",
        title
    )

    title = title.lower()

    title = re.sub(
        r"\[[^\]]*\]",
        " ",
        title
    )

    title = re.sub(
        r"\([^)]*\)",
        " ",
        title
    )

    title = re.sub(
        r"[^\w\s]",
        " ",
        title,
        flags=re.UNICODE
    )

    title = re.sub(
        r"\s+",
        " ",
        title
    )

    return title.strip()


def title_similarity(a: str, b: str) -> float:

    a = normalize_title(a)
    b = normalize_title(b)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    if a in b or b in a:
        return 0.96

    return difflib.SequenceMatcher(
        None,
        a,
        b
    ).ratio()


# ============================================================
# Front Matter
# ============================================================

def parse_front_matter(content: str):

    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:
        return {}, content

    raw_yaml = parts[1].strip()
    body = parts[2].lstrip()

    data = {}

    for line in raw_yaml.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1
        )

        key = key.strip()
        value = value.strip()

        value = value.strip('"').strip("'")

        data[key] = value

    return data, body


# ============================================================
# URL
# ============================================================

def extract_urls(text: str):

    urls = re.findall(
        r'https?://[^\s<>"\]\)]+',
        text
    )

    result = []

    for url in urls:

        url = url.rstrip(
            ".,;!?）】"
        )

        try:

            parsed = urlparse(url)

            if parsed.scheme in (
                "http",
                "https"
            ):

                if url not in result:
                    result.append(url)

        except Exception:
            pass

    return result


# ============================================================
# HTTP
# ============================================================

def http_get(
    url: str,
    accept: str = "*/*"
):

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": accept,
    }

    req = Request(
        url,
        headers=headers
    )

    with urlopen(
        req,
        timeout=TIMEOUT
    ) as response:

        raw = response.read()

        content_type = response.headers.get(
            "Content-Type",
            ""
        )

        charset = "utf-8"

        match = re.search(
            r"charset=([^\s;]+)",
            content_type,
            flags=re.I
        )

        if match:
            charset = match.group(1)

        try:
            text = raw.decode(
                charset,
                errors="replace"
            )
        except Exception:
            text = raw.decode(
                "utf-8",
                errors="replace"
            )

        return response.geturl(), text


# ============================================================
# RSS 搜索
# ============================================================

def parse_rss(xml_text: str):

    candidates = []

    try:

        root = ET.fromstring(
            xml_text
        )

    except Exception:
        return candidates

    for item in root.iter():

        tag = item.tag.lower()

        if not tag.endswith("item"):
            continue

        data = {}

        for child in item:

            key = child.tag.split(
                "}"
            )[-1].lower()

            data[key] = (
                child.text or ""
            ).strip()

        title = data.get(
            "title",
            ""
        )

        link = data.get(
            "link",
            ""
        )

        description = data.get(
            "description",
            ""
        )

        pub_date = data.get(
            "pubdate",
            ""
        )

        if not title or not link:
            continue

        candidates.append({
            "title": clean_text(title),
            "url": link.strip(),
            "description": clean_text(
                description
            ),
            "published": pub_date,
        })

    return candidates


def google_news_search(
    title: str,
    date: str
):

    query = f'"{title}"'

    url = (
        "https://news.google.com/rss/search?"
        f"q={quote_plus(query)}"
        f"&hl=en-US"
        f"&gl=US"
        f"&ceid=US:en"
    )

    try:

        _, xml = http_get(
            url,
            accept="application/rss+xml,text/xml,*/*"
        )

        return parse_rss(xml)

    except Exception as exc:

        print(
            f"Google News failed: {exc}"
        )

        return []


def bing_news_search(
    title: str,
    date: str
):

    query = f'"{title}"'

    url = (
        "https://www.bing.com/news/search?"
        f"q={quote_plus(query)}"
        f"&format=rss"
    )

    try:

        _, xml = http_get(
            url,
            accept="application/rss+xml,text/xml,*/*"
        )

        return parse_rss(xml)

    except Exception as exc:

        print(
            f"Bing News failed: {exc}"
        )

        return []


def search_candidates(
    title: str,
    date: str
):

    candidates = []

    searches = [
        google_news_search,
        bing_news_search,
    ]

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=2
    ) as executor:

        futures = [
            executor.submit(
                fn,
                title,
                date
            )
            for fn in searches
        ]

        for future in futures:

            try:

                candidates.extend(
                    future.result()
                )

            except Exception:
                pass

    # 去重
    unique = {}
    for c in candidates:

        url = c.get(
            "url",
            ""
        )

        if url:
            unique[url] = c

    candidates = list(
        unique.values()
    )

    # 标题匹配评分
    for c in candidates:

        c["match_score"] = title_similarity(
            title,
            c.get("title", "")
        )

    candidates.sort(
        key=lambda x: x.get(
            "match_score",
            0
        ),
        reverse=True
    )

    return candidates[
        :MAX_CANDIDATES_PER_ITEM
    ]


# ============================================================
# 页面信息
# ============================================================

def extract_html_title(
    content: str
):

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        content,
        flags=re.I | re.S
    )

    if match:
        return clean_text(
            match.group(1)
        )

    return ""


def extract_meta(
    content: str,
    names: list[str]
):

    for name in names:

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

                return clean_text(
                    match.group(1)
                )

    return ""


def extract_author(
    content: str
):

    return extract_meta(
        content,
        [
            "author",
            "article:author",
            "byl"
        ]
    )


def extract_article_text(
    content: str
):

    match = re.search(
        r"<article[^>]*>(.*?)</article>",
        content,
        flags=re.I | re.S
    )

    if match:
        article = match.group(1)

    else:

        # 常见正文区域
        patterns = [
            r"<main[^>]*>(.*?)</main>",
            r"<body[^>]*>(.*?)</body>",
        ]

        article = content

        for pattern in patterns:

            m = re.search(
                pattern,
                content,
                flags=re.I | re.S
            )

            if m:

                article = m.group(1)

                break

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

    # 保留段落结构
    article = re.sub(
        r"</(p|div|h1|h2|h3|h4|li|br)>",
        "\n",
        article,
        flags=re.I
    )

    article = re.sub(
        r"<[^>]+>",
        " ",
        article
    )

    article = html.unescape(
        article
    )

    lines = []

    for line in article.splitlines():

        line = re.sub(
            r"[ \t]+",
            " ",
            line
        ).strip()

        if not line:
            continue

        if len(line) < 2:
            continue

        lines.append(line)

    cleaned = []

    previous = ""

    for line in lines:

        if line == previous:
            continue

        cleaned.append(line)

        previous = line

    result = "\n\n".join(
        cleaned
    )

    return result[
        :MAX_ARTICLE_CHARS
    ]


# ============================================================
# 抓取候选
# ============================================================

def fetch_candidate(
    candidate: dict
):

    url = candidate.get(
        "url",
        ""
    )

    try:

        final_url, content = http_get(
            url,
            accept=(
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,"
                "*/*;q=0.8"
            )
        )

        title = extract_html_title(
            content
        )

        description = extract_meta(
            content,
            [
                "description",
                "og:description"
            ]
        )

        author = extract_author(
            content
        )

        article = extract_article_text(
            content
        )

        return {
            **candidate,
            "ok": True,
            "url": final_url,
            "page_title": title,
            "description": description,
            "author": author,
            "article": article,
            "page_match_score": title_similarity(
                candidate.get("source_title", ""),
                title
            ),
        }

    except Exception as exc:

        return {
            **candidate,
            "ok": False,
            "error": str(exc),
        }


# ============================================================
# AGNES API
# ============================================================

def agnes_configured():

    return bool(
        os.getenv(
            "AGNES_API_KEY",
            ""
        ).strip()
    )


def call_agnes(
    original_title: str,
    candidates: list[dict]
):

    api_key = os.getenv(
        "AGNES_API_KEY",
        ""
    ).strip()

    if not api_key:
        return None

    base = os.getenv(
        "AGNES_API_BASE_URL",
        "https://api.openai.com/v1"
    ).rstrip("/")

    model = os.getenv(
        "AGNES_API_MODEL",
        "gpt-4o-mini"
    )

    compact = []

    for index, candidate in enumerate(
        candidates
    ):

        compact.append({
            "index": index,
            "title": candidate.get(
                "title",
                ""
            ),
            "url": candidate.get(
                "url",
                ""
            ),
            "description": candidate.get(
                "description",
                ""
            )[:1000],
            "source": candidate.get(
                "source",
                ""
            ),
            "author": candidate.get(
                "author",
                ""
            ),
        })

    prompt = f"""
你是新闻来源核验系统。

原始 Horizon 标题：
{original_title}

下面是新闻搜索得到的候选来源：

{json.dumps(
    compact,
    ensure_ascii=False,
    indent=2
)}

任务：

1. 判断哪个候选最可能是原始新闻。
2. 优先判断真实新闻媒体，而不是聚合网站。
3. 如果候选明确显示转载自某媒体，优先识别真正的原始媒体。
4. 如果标题高度一致但来源是转载网站，也要尽可能判断原始媒体。
5. 不允许凭空创造来源。
6. 如果没有可信候选，返回 null。

严格只返回 JSON：

{{
  "index": 0,
  "confidence": 0.95,
  "source": "The New York Times",
  "author": "Zach Montague",
  "reason": "标题完全匹配，候选明确标注为 New York Times"
}}

如果没有可信来源：

null
"""

    payload = json.dumps({
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是严格的新闻来源核验器。"
                    "不得编造来源。"
                    "只输出 JSON。"
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }).encode(
        "utf-8"
    )

    req = Request(
        base + "/chat/completions",
        data=payload,
        headers={
            "Authorization":
                "Bearer " + api_key,
            "Content-Type":
                "application/json"
        }
    )

    try:

        with urlopen(
            req,
            timeout=30
        ) as response:

            data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

        text = (
            data["choices"][0]["message"]
            ["content"]
        )

        text = text.strip()

        if text.startswith(
            "```"
        ):

            text = re.sub(
                r"^```(?:json)?",
                "",
                text
            )

            text = re.sub(
                r"```$",
                "",
                text
            ).strip()

        if text.lower() == "null":
            return None

        return json.loads(
            text
        )

    except Exception as exc:

        print(
            f"⚠️ AGNES API failed: {exc}"
        )

        return None


# ============================================================
# 单条新闻处理
# ============================================================

def resolve_source(
    input_file: Path,
    metadata: dict,
    body: str
):

    title = metadata.get(
        "title",
        ""
    )

    date = metadata.get(
        "date",
        ""
    )

    direct_urls = extract_urls(
        body
    )

    # --------------------------------------------------------
    # 1. 已有 URL
    # --------------------------------------------------------

    if direct_urls:

        return {
            "status": "direct_url",
            "search_method": "direct_url",
            "match_score": 1.0,
            "source_url": direct_urls[0],
            "source": metadata.get(
                "source",
                "Unknown"
            ),
            "original_title": "",
            "author": "",
            "article": "",
            "description": "",
        }

    # --------------------------------------------------------
    # 2. RSS 搜索
    # --------------------------------------------------------

    print()
    print(
        f"🔎 Searching: {title}"
    )

    candidates = search_candidates(
        title,
        date
    )

    print(
        f"Candidates: {len(candidates)}"
    )

    if not candidates:

        return {
            "status": "pending_search",
            "search_method": "rss_unresolved",
            "match_score": 0.0,
            "source_url": "",
            "source": "Unknown",
            "original_title": "",
            "author": "",
            "article": "",
            "description": "",
        }

    best = candidates[0]

    print(
        "Best candidate:"
    )

    print(
        best.get(
            "title",
            ""
        )
    )

    print(
        best.get(
            "url",
            ""
        )
    )

    print(
        "Match:",
        round(
            best.get(
                "match_score",
                0
            ),
            3
        )
    )

    # --------------------------------------------------------
    # 3. 高可信 → 不调用 API
    # --------------------------------------------------------

    if best.get(
        "match_score",
        0
    ) >= MIN_DIRECT_MATCH:

        return {
            "status": "search_match",
            "search_method": "rss_title_match",
            "match_score": best.get(
                "match_score",
                0
            ),
            "source_url": best.get(
                "url",
                ""
            ),
            "source": best.get(
                "source",
                "Unknown"
            ),
            "original_title": best.get(
                "title",
                ""
            ),
            "author": best.get(
                "author",
                ""
            ),
            "article": "",
            "description": best.get(
                "description",
                ""
            ),
        }

    # --------------------------------------------------------
    # 4. API fallback
    # --------------------------------------------------------

    if agnes_configured():

        print(
            "🤖 RSS match uncertain."
        )

        print(
            "Calling AGNES API..."
        )

        decision = call_agnes(
            title,
            candidates
        )

        if decision:

            index = decision.get(
                "index"
            )

            confidence = float(
                decision.get(
                    "confidence",
                    0
                )
            )

            if (
                isinstance(index, int)
                and
                0 <= index < len(
                    candidates
                )
                and
                confidence >= MIN_API_MATCH
            ):

                chosen = candidates[
                    index
                ]

                return {
                    "status":
                        "api_match",
                    "search_method":
                        "rss_then_agnes",
                    "match_score":
                        confidence,
                    "source_url":
                        chosen.get(
                            "url",
                            ""
                        ),
                    "source":
                        decision.get(
                            "source"
                        )
                        or chosen.get(
                            "source",
                            "Unknown"
                        ),
                    "original_title":
                        chosen.get(
                            "title",
                            ""
                        ),
                    "author":
                        decision.get(
                            "author",
                            ""
                        ),
                    "article": "",
                    "description":
                        chosen.get(
                            "description",
                            ""
                        ),
                }

    # --------------------------------------------------------
    # 5. 最终 unresolved
    # --------------------------------------------------------

    return {
        "status": "pending_search",
        "search_method": "unresolved",
        "match_score": best.get(
            "match_score",
            0
        ),
        "source_url": "",
        "source": "Unknown",
        "original_title": "",
        "author": "",
        "article": "",
        "description": "",
    }


# ============================================================
# 获取最终网页正文
# ============================================================

def fetch_final_source(
    result: dict
):

    url = result.get(
        "source_url",
        ""
    )

    if not url:
        return result

    try:

        final_url, content = http_get(
            url,
            accept=(
                "text/html,"
                "application/xhtml+xml,"
                "*/*"
            )
        )

        page_title = extract_html_title(
            content
        )

        description = extract_meta(
            content,
            [
                "description",
                "og:description"
            ]
        )

        author = extract_author(
            content
        )

        article = extract_article_text(
            content
        )

        result["source_url"] = final_url

        if page_title:
            result["original_title"] = (
                page_title
            )

        if author:
            result["author"] = author

        if description:
            result["description"] = (
                description
            )

        result["article"] = article

        if len(article) >= 500:

            result["content_status"] = (
                "full"
            )

        else:

            result["content_status"] = (
                "partial"
            )

        if (
            result.get("status")
            == "direct_url"
        ):

            result["source_status"] = (
                "fetched"
            )

        else:

            result["source_status"] = (
                "fetched"
            )

    except Exception as exc:

        print(
            f"⚠️ Final fetch failed: {exc}"
        )

        result["source_status"] = (
            "fetch_failed"
        )

        result["content_status"] = (
            "horizon_summary_only"
        )

    return result


# ============================================================
# Markdown
# ============================================================

def build_markdown(
    original_content: str,
    metadata: dict,
    result: dict
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

    score = metadata.get(
        "horizon_score",
        "0"
    )

    source = result.get(
        "source",
        "Unknown"
    )

    source_url = result.get(
        "source_url",
        ""
    )

    status = result.get(
        "source_status",
        "pending_search"
    )

    search_method = result.get(
        "search_method",
        "unresolved"
    )

    match_score = result.get(
        "match_score",
        0
    )

    content_status = result.get(
        "content_status",
        "horizon_summary_only"
    )

    original_title = result.get(
        "original_title",
        ""
    )

    author = result.get(
        "author",
        ""
    )

    description = result.get(
        "description",
        ""
    )

    article = result.get(
        "article",
        ""
    )

    _, original_body = parse_front_matter(
        original_content
    )

    front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "news"
source: "{yaml_escape(source)}"
source_url: "{yaml_escape(source_url)}"
language: "{yaml_escape(language)}"
horizon_score: {score}
source_status: "{status}"
content_status: "{content_status}"
search_method: "{search_method}"
match_score: {match_score:.3f}
ai_status: "pending"
original_title: "{yaml_escape(original_title)}"
author: "{yaml_escape(author)}"
---

"""

    body = f"""# {title}

## Horizon 摘要

{original_body.strip()}
"""

    if status == "fetched":

        body += """

## 原文信息

"""

        body += (
            f"- Source: {source}\n"
        )

        if author:

            body += (
                f"- Author: {author}\n"
            )

        if original_title:

            body += (
                f"- Original Title: "
                f"{original_title}\n"
            )

        if source_url:

            body += (
                f"- Original URL: "
                f"{source_url}\n"
            )

        if description:

            body += (
                f"- Description: "
                f"{description}\n"
            )

        if article:

            body += """

## 原文正文

"""

            body += article

        else:

            body += """

## 原文正文

本次已确认来源，但正文抓取不完整。
后续 AI 处理阶段可以继续通过原文链接获取。

"""

    elif status == "pending_search":

        body += """

## 原文获取状态

当前自动搜索暂未找到可信原始来源。

本条新闻不会将 Horizon 摘要误认为原文。

下一阶段可以继续进行：
标题 + 日期 + 新闻事件 + 候选媒体交叉验证。

"""

    else:

        body += """

## 原文获取状态

原文来源已识别，但网页正文获取失败。

保留当前 Horizon 摘要与来源链接，
等待后续重试。

"""

        if source_url:

            body += (
                f"\n原文链接：{source_url}\n"
            )

    body += """

## AI 处理状态

等待 27 Skills 进行后续处理。
"""

    return (
        front
        + body.strip()
        + "\n"
    )


# ============================================================
# 单文件
# ============================================================

def process_file(
    input_file: Path,
    output_file: Path
):

    content = input_file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    metadata, body = parse_front_matter(
        content
    )

    result = resolve_source(
        input_file,
        metadata,
        body
    )

    result = fetch_final_source(
        result
    )

    enriched = build_markdown(
        content,
        metadata,
        result
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_file.write_text(
        enriched,
        encoding="utf-8"
    )

    print(
        f"✅ {input_file.name}"
    )

    print(
        f"   status={result.get('source_status')}"
    )

    print(
        f"   method={result.get('search_method')}"
    )

    print(
        f"   score={result.get('match_score')}"
    )


# ============================================================
# 并行处理语言目录
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path
):

    files = sorted(
        input_dir.glob("*.md")
    )

    if not files:
        return 0

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print(
        f"Processing {len(files)} files:"
    )

    # 全部并行
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = []

        for file in files:

            output_file = (
                output_dir / file.name
            )

            futures.append(
                executor.submit(
                    process_file,
                    file,
                    output_file
                )
            )

        for future in concurrent.futures.as_completed(
            futures
        ):

            try:
                future.result()

            except Exception as exc:

                print(
                    f"❌ Worker failed: {exc}"
                )

    return len(files)


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Horizon Source Enrichment V2.1"
        )
    )

    parser.add_argument(
        "--zh",
        required=True
    )

    parser.add_argument(
        "--en",
        required=True
    )

    parser.add_argument(
        "--output",
        required=True
    )

    parser.add_argument(
        "--date",
        required=True
    )

    args = parser.parse_args()

    zh_input = Path(
        args.zh
    )

    en_input = Path(
        args.en
    )

    output_root = Path(
        args.output
    )

    print("=" * 70)
    print(
        "HORIZON SOURCE ENRICHMENT V2.1"
    )
    print("=" * 70)

    print(
        f"Date: {args.date}"
    )

    print(
        f"AGNES API: "
        f"{'configured' if agnes_configured() else 'not configured'}"
    )

    zh_count = process_language(
        zh_input,
        output_root / "zh"
    )

    en_count = process_language(
        en_input,
        output_root / "en"
    )

    print()
    print("=" * 70)
    print("FINAL RESULT")
    print("=" * 70)

    print(
        f"Chinese: {zh_count}"
    )

    print(
        f"English: {en_count}"
    )

    if zh_count == 0 and en_count == 0:

        raise RuntimeError(
            "没有发现 Atomic News 文件。"
        )

    print()
    print(
        "✅ SOURCE ENRICHMENT V2.1 COMPLETE"
    )


if __name__ == "__main__":
    main()
