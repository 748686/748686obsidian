#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Source Enrichment V2

目标：

1. 同时处理 zh / en
2. 有原文 URL：
   → 直接抓取

3. 没有 URL：
   → 第一阶段：
      Google News RSS 批量搜索候选来源
      → 标题匹配
      → 验证 URL
      → 抓取原文

4. 第一阶段仍然失败：
   → 第二阶段：
      Agnes API 批量识别候选来源
      → 验证 URL
      → 抓取原文

5. 永远不修改 Atomic News
6. 输出：
   Raw News/YYYY-MM-DD-Enriched/zh
   Raw News/YYYY-MM-DD-Enriched/en

7. 不把 Horizon 当成真实新闻来源
8. 记录：
   source
   source_url
   source_status
   content_status
   search_method
   original_title

9. 尽量并发执行，避免逐条慢速等待
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import (
    quote_plus,
    urlparse,
)

import requests
from bs4 import BeautifulSoup


# ============================================================
# 配置
# ============================================================

DEFAULT_AGNES_BASE_URL = (
    "https://apihub.agnes-ai.com/v1"
)

DEFAULT_AGNES_MODEL = (
    "agnes-2.5-flash"
)

REQUEST_TIMEOUT = 10

RSS_TIMEOUT = 8

MAX_WORKERS = 8

AGNES_BATCH_SIZE = 12

MAX_ARTICLE_LENGTH = 30000

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/2.0; "
    "+https://github.com/748686/748686obsidian)"
)


# ============================================================
# Session
# ============================================================

def create_session():

    session = requests.Session()

    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": (
            "zh-CN,zh;q=0.9,en;q=0.8"
        ),
    })

    return session


SESSION = create_session()


# ============================================================
# 文本
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = html.unescape(text)

    text = re.sub(
        r"<script.*?</script>",
        "",
        text,
        flags=re.I | re.S,
    )

    text = re.sub(
        r"<style.*?</style>",
        "",
        text,
        flags=re.I | re.S,
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text,
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n\s*\n\s*\n+",
        "\n\n",
        text,
    )

    return text.strip()


def yaml_escape(text: str) -> str:

    text = clean_text(text)

    text = (
        text
        .replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )

    return text


def normalize_title(title: str) -> str:

    title = clean_text(title).lower()

    title = re.sub(
        r"[^a-z0-9\u4e00-\u9fff]+",
        " ",
        title,
    )

    title = re.sub(
        r"\s+",
        " ",
        title,
    )

    return title.strip()


def title_tokens(title: str):

    normalized = normalize_title(title)

    return set(
        normalized.split()
    )


def title_similarity(a: str, b: str):

    a_norm = normalize_title(a)
    b_norm = normalize_title(b)

    if not a_norm or not b_norm:
        return 0.0

    if a_norm == b_norm:
        return 1.0

    if (
        a_norm in b_norm
        or b_norm in a_norm
    ):
        return 0.92

    a_tokens = title_tokens(a)
    b_tokens = title_tokens(b)

    if not a_tokens or not b_tokens:
        return 0.0

    intersection = (
        len(a_tokens & b_tokens)
    )

    union = (
        len(a_tokens | b_tokens)
    )

    jaccard = (
        intersection / union
        if union
        else 0
    )

    coverage = (
        intersection / len(a_tokens)
        if a_tokens
        else 0
    )

    return max(
        jaccard,
        coverage * 0.85,
    )


# ============================================================
# Front Matter
# ============================================================

def parse_front_matter(content: str):

    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2,
    )

    if len(parts) < 3:
        return {}, content

    raw_yaml = parts[1].strip()

    body = parts[2].lstrip()

    metadata = {}

    for line in raw_yaml.splitlines():

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

        metadata[key] = value

    return metadata, body


# ============================================================
# URL
# ============================================================

def extract_urls(text: str):

    urls = re.findall(
        r'https?://[^\s<>"\]\)]+',
        text,
    )

    result = []

    for url in urls:

        url = url.rstrip(
            ".,;。；）)"
        )

        try:

            parsed = urlparse(url)

            if parsed.scheme in (
                "http",
                "https",
            ):
                if url not in result:
                    result.append(url)

        except Exception:
            continue

    return result


# ============================================================
# 来源名称
# ============================================================

DOMAIN_SOURCE_MAP = {

    "cnn.com": "CNN",
    "reuters.com": "Reuters",
    "apnews.com": "AP",
    "bbc.com": "BBC",
    "bbc.co.uk": "BBC",
    "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post",
    "wsj.com": "The Wall Street Journal",
    "bloomberg.com": "Bloomberg",
    "npr.org": "NPR",
    "abcnews.go.com": "ABC News",
    "nbcnews.com": "NBC News",
    "cbsnews.com": "CBS News",
    "theguardian.com": "The Guardian",
    "ft.com": "Financial Times",
    "economist.com": "The Economist",
    "scmp.com": "SCMP",
    "nhk.or.jp": "NHK",
    "kyodonews.net": "Kyodo News",
    "nikkei.com": "Nikkei",
    "lemonde.fr": "Le Monde",
    "lefigaro.fr": "Le Figaro",
}


def source_from_url(url: str):

    try:

        hostname = (
            urlparse(url)
            .hostname
            or ""
        )

        hostname = hostname.lower()

        if hostname.startswith("www."):
            hostname = hostname[4:]

        if hostname in DOMAIN_SOURCE_MAP:
            return DOMAIN_SOURCE_MAP[
                hostname
            ]

        for domain, name in DOMAIN_SOURCE_MAP.items():

            if hostname.endswith(
                "." + domain
            ):
                return name

        parts = hostname.split(".")

        if len(parts) >= 2:
            return parts[-2].capitalize()

    except Exception:
        pass

    return "Unknown"


# ============================================================
# 网页抓取
# ============================================================

def extract_jsonld_article(
    soup: BeautifulSoup,
):

    scripts = soup.find_all(
        "script",
        type=re.compile(
            r"application/ld\+json",
            re.I,
        ),
    )

    for script in scripts:

        raw = script.string

        if not raw:
            continue

        try:

            data = json.loads(
                raw.strip()
            )

        except Exception:
            continue

        objects = []

        if isinstance(data, dict):

            objects.append(data)

            graph = data.get(
                "@graph"
            )

            if isinstance(
                graph,
                list,
            ):
                objects.extend(graph)

        elif isinstance(data, list):

            objects.extend(data)

        for obj in objects:

            if not isinstance(
                obj,
                dict,
            ):
                continue

            obj_type = obj.get(
                "@type",
                "",
            )

            if isinstance(
                obj_type,
                list,
            ):
                obj_type = " ".join(
                    str(x)
                    for x in obj_type
                )

            if "article" not in str(
                obj_type
            ).lower():
                continue

            article_body = obj.get(
                "articleBody",
                "",
            )

            headline = obj.get(
                "headline",
                "",
            )

            if article_body:

                return (
                    clean_text(
                        str(headline)
                    ),
                    clean_text(
                        str(article_body)
                    ),
                )

    return "", ""


def extract_page(url: str):

    try:

        response = SESSION.get(
            url,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response.raise_for_status()

        content_type = (
            response.headers
            .get(
                "content-type",
                "",
            )
            .lower()
        )

        if (
            "html" not in content_type
            and "xhtml" not in content_type
        ):
            return {
                "ok": False,
                "error": "not_html",
                "url": response.url,
            }

        soup = BeautifulSoup(
            response.text,
            "html.parser",
        )

        # ----------------------------------------------------
        # 标题
        # ----------------------------------------------------

        title = ""

        if soup.title:
            title = clean_text(
                soup.title.get_text(
                    " ",
                    strip=True,
                )
            )

        og_title = soup.find(
            "meta",
            property="og:title",
        )

        if og_title:

            candidate = clean_text(
                og_title.get(
                    "content",
                    "",
                )
            )

            if candidate:
                title = candidate

        # ----------------------------------------------------
        # description
        # ----------------------------------------------------

        description = ""

        meta_description = soup.find(
            "meta",
            attrs={
                "name": "description"
            },
        )

        if meta_description:

            description = clean_text(
                meta_description.get(
                    "content",
                    "",
                )
            )

        # ----------------------------------------------------
        # JSON-LD
        # ----------------------------------------------------

        json_title, json_article = (
            extract_jsonld_article(
                soup
            )
        )

        if json_title:
            title = json_title

        article = json_article

        # ----------------------------------------------------
        # article HTML
        # ----------------------------------------------------

        if len(article) < 500:

            article_node = soup.find(
                "article"
            )

            if article_node:

                article = clean_text(
                    article_node.get_text(
                        "\n",
                        strip=True,
                    )
                )

        # ----------------------------------------------------
        # fallback paragraphs
        # ----------------------------------------------------

        if len(article) < 500:

            paragraphs = []

            for p in soup.find_all(
                "p"
            ):

                text = clean_text(
                    p.get_text(
                        " ",
                        strip=True,
                    )
                )

                if len(text) >= 40:
                    paragraphs.append(
                        text
                    )

            article = "\n\n".join(
                paragraphs
            )

        article = article[
            :MAX_ARTICLE_LENGTH
        ]

        return {
            "ok": True,
            "url": response.url,
            "title": title,
            "description": description,
            "article": article,
            "status_code": response.status_code,
        }

    except Exception as exc:

        return {
            "ok": False,
            "error": str(exc),
            "url": url,
        }


# ============================================================
# Google News RSS
# ============================================================

def google_news_search(
    title: str,
    language: str,
):

    query = title

    if language == "zh":

        url = (
            "https://news.google.com/rss/search?"
            f"q={quote_plus(query)}"
            "&hl=zh-CN"
            "&gl=CN"
            "&ceid=CN:zh-Hans"
        )

    else:

        url = (
            "https://news.google.com/rss/search?"
            f"q={quote_plus(query)}"
            "&hl=en-US"
            "&gl=US"
            "&ceid=US:en"
        )

    try:

        response = SESSION.get(
            url,
            timeout=RSS_TIMEOUT,
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "xml",
        )

        candidates = []

        for item in soup.find_all(
            "item"
        )[:10]:

            item_title = clean_text(
                item.title.get_text()
                if item.title
                else ""
            )

            link = ""

            if item.link:

                link = clean_text(
                    item.link.get_text(
                        strip=True
                    )
                )

            description = ""

            if item.description:

                description = clean_text(
                    item.description.get_text()
                )

            published = ""

            if item.pubDate:

                published = clean_text(
                    item.pubDate.get_text()
                )

            if not link:
                continue

            score = title_similarity(
                title,
                item_title,
            )

            candidates.append({
                "title": item_title,
                "url": link,
                "description": description,
                "published": published,
                "score": score,
            })

        candidates.sort(
            key=lambda x: x["score"],
            reverse=True,
        )

        return candidates

    except Exception as exc:

        print(
            f"RSS search failed: {title} "
            f"→ {exc}"
        )

        return []


# ============================================================
# RSS 批量搜索
# ============================================================

def search_rss_batch(items):

    results = {}

    print()
    print("=" * 70)
    print("PHASE 1 — GOOGLE NEWS RSS")
    print("=" * 70)

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = {}

        for item in items:

            future = executor.submit(
                google_news_search,
                item["title"],
                item["language"],
            )

            futures[future] = item

        for future in concurrent.futures.as_completed(
            futures
        ):

            item = futures[future]

            try:

                candidates = future.result()

            except Exception:

                candidates = []

            results[
                item["path"]
            ] = candidates

            best = (
                candidates[0]
                if candidates
                else None
            )

            if best:

                print(
                    f"RSS ✓ "
                    f"{item['language']} "
                    f"{item['title'][:55]} "
                    f"→ "
                    f"{best['score']:.2f}"
                )

            else:

                print(
                    f"RSS ? "
                    f"{item['title'][:55]}"
                )

    return results


# ============================================================
# RSS 候选验证
# ============================================================

def validate_rss_candidates(
    items,
    rss_results,
):

    unresolved = []

    resolved = {}

    print()
    print("=" * 70)
    print("VALIDATING RSS CANDIDATES")
    print("=" * 70)

    for item in items:

        candidates = rss_results.get(
            item["path"],
            [],
        )

        accepted = None

        for candidate in candidates[:5]:

            score = candidate[
                "score"
            ]

            # 标题必须达到较高相似度
            if score < 0.58:
                continue

            page = extract_page(
                candidate["url"]
            )

            if not page.get("ok"):
                continue

            page_title = page.get(
                "title",
                "",
            )

            final_score = max(
                score,
                title_similarity(
                    item["title"],
                    page_title,
                ),
            )

            if final_score < 0.58:
                continue

            if len(
                page.get(
                    "article",
                    "",
                )
            ) < 300:

                continue

            accepted = {
                "source": source_from_url(
                    page["url"]
                ),
                "source_url": page["url"],
                "original_title": (
                    page.get("title")
                    or candidate["title"]
                ),
                "description": page.get(
                    "description",
                    "",
                ),
                "article": page[
                    "article"
                ],
                "search_method": (
                    "google_news_rss"
                ),
                "match_score": final_score,
                "source_status": "fetched",
                "content_status": "full",
            }

            break

        if accepted:

            resolved[
                item["path"]
            ] = accepted

            print(
                f"✓ RSS MATCH "
                f"{item['title'][:55]}"
            )

        else:

            unresolved.append(item)

            print(
                f"→ API FALLBACK "
                f"{item['title'][:55]}"
            )

    return resolved, unresolved


# ============================================================
# Agnes API
# ============================================================

def agnes_chat(
    prompt: str,
):

    api_key = os.getenv(
        "AGNES_API_KEY"
    )

    if not api_key:
        return None

    base_url = os.getenv(
        "AGNES_BASE_URL",
        DEFAULT_AGNES_BASE_URL,
    )

    model = os.getenv(
        "AGNES_MODEL",
        DEFAULT_AGNES_MODEL,
    )

    url = (
        base_url.rstrip("/")
        + "/chat/completions"
    )

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a news source "
                    "identification assistant. "
                    "Never invent URLs. "
                    "Only return a URL when "
                    "you are reasonably confident "
                    "it is the original article. "
                    "Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0,
        "max_tokens": 3000,
    }

    headers = {
        "Authorization":
            f"Bearer {api_key}",
        "Content-Type":
            "application/json",
    }

    try:

        response = SESSION.post(
            url,
            headers=headers,
            json=payload,
            timeout=25,
        )

        response.raise_for_status()

        data = response.json()

        return (
            data["choices"][0]
            ["message"]
            ["content"]
        )

    except Exception as exc:

        print(
            f"Agnes API error: {exc}"
        )

        return None


def parse_json_response(text: str):

    if not text:
        return []

    text = text.strip()

    # Markdown JSON fence
    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.I,
    )

    text = re.sub(
        r"^```\s*",
        "",
        text,
    )

    text = re.sub(
        r"\s*```$",
        "",
        text,
    )

    try:

        data = json.loads(
            text
        )

        if isinstance(
            data,
            list,
        ):
            return data

        if isinstance(
            data,
            dict,
        ):

            if isinstance(
                data.get("items"),
                list,
            ):
                return data["items"]

    except Exception:
        pass

    # 尝试从文本中找 JSON array
    match = re.search(
        r"$begin:math:display$\[\\s\\S\]\*$end:math:display$",
        text,
    )

    if match:

        try:

            data = json.loads(
                match.group(0)
            )

            if isinstance(
                data,
                list,
            ):
                return data

        except Exception:
            pass

    return []


# ============================================================
# Agnes 批量搜索
# ============================================================

def agnes_batch(
    items,
):

    if not items:
        return {}

    if not os.getenv(
        "AGNES_API_KEY"
    ):

        print()
        print(
            "⚠️ AGNES_API_KEY not configured."
        )

        return {}

    results = {}

    print()
    print("=" * 70)
    print("PHASE 2 — AGNES API BATCH")
    print("=" * 70)

    for start in range(
        0,
        len(items),
        AGNES_BATCH_SIZE,
    ):

        batch = items[
            start:
            start + AGNES_BATCH_SIZE
        ]

        print(
            f"Agnes batch "
            f"{start + 1}-"
            f"{start + len(batch)} "
            f"/ {len(items)}"
        )

        news_lines = []

        for index, item in enumerate(
            batch,
            start=1,
        ):

            news_lines.append(
                f"""
ITEM {index}
language: {item['language']}
date: {item['date']}
title: {item['title']}
Horizon summary:
{item['summary'][:1500]}
""".strip()
            )

        prompt = f"""
Identify the original news source for
each news item below.

This is a source-identification task.

Rules:

1. Prefer the actual original publisher.
2. Do not return Horizon as a source.
3. Do not invent a URL.
4. If uncertain, return an empty URL.
5. Prefer Reuters, AP, CNN, BBC,
   Bloomberg, NYT, WSJ, Guardian,
   official government sources, etc.
6. Return ONE JSON array.
7. Preserve ITEM numbers.
8. Return:

[
  {{
    "item": 1,
    "source": "CNN",
    "url": "https://...",
    "title": "original article title",
    "confidence": 0.92
  }}
]

News items:

{chr(10).join(news_lines)}
"""

        response = agnes_chat(
            prompt
        )

        parsed = parse_json_response(
            response
        )

        for obj in parsed:

            if not isinstance(
                obj,
                dict,
            ):
                continue

            try:

                item_index = int(
                    obj.get(
                        "item",
                        0,
                    )
                )

            except Exception:
                continue

            if not (
                1 <= item_index
                <= len(batch)
            ):
                continue

            url = clean_text(
                str(
                    obj.get(
                        "url",
                        "",
                    )
                )
            )

            if not url.startswith(
                "http"
            ):
                continue

            batch_item = batch[
                item_index - 1
            ]

            results[
                batch_item["path"]
            ] = {
                "candidate_url": url,
                "candidate_source": clean_text(
                    str(
                        obj.get(
                            "source",
                            "",
                        )
                    )
                ),
                "candidate_title": clean_text(
                    str(
                        obj.get(
                            "title",
                            "",
                        )
                    )
                ),
                "confidence": obj.get(
                    "confidence",
                    0,
                ),
            }

    return results


# ============================================================
# 验证 Agnes URL
# ============================================================

def validate_agnes_results(
    items,
    agnes_results,
):

    resolved = {}

    print()
    print("=" * 70)
    print("VALIDATING AGNES RESULTS")
    print("=" * 70)

    for item in items:

        candidate = agnes_results.get(
            item["path"]
        )

        if not candidate:

            continue

        url = candidate[
            "candidate_url"
        ]

        page = extract_page(
            url
        )

        if not page.get("ok"):

            print(
                f"✗ API URL failed "
                f"{item['title'][:55]}"
            )

            continue

        page_title = page.get(
            "title",
            "",
        )

        score = title_similarity(
            item["title"],
            page_title,
        )

        api_confidence = candidate.get(
            "confidence",
            0,
        )

        try:
            api_confidence = float(
                api_confidence
            )
        except Exception:
            api_confidence = 0

        final_score = max(
            score,
            api_confidence,
        )

        if final_score < 0.55:

            print(
                f"✗ API title mismatch "
                f"{item['title'][:55]}"
            )

            continue

        article = page.get(
            "article",
            "",
        )

        if len(article) < 300:

            print(
                f"✗ API page too short "
                f"{item['title'][:55]}"
            )

            continue

        resolved[
            item["path"]
        ] = {
            "source": source_from_url(
                page["url"]
            ),
            "source_url": page[
                "url"
            ],
            "original_title": (
                page.get("title")
                or candidate.get(
                    "candidate_title",
                    "",
                )
            ),
            "description": page.get(
                "description",
                "",
            ),
            "article": article,
            "search_method": (
                "agnes_api"
            ),
            "match_score": final_score,
            "source_status": "fetched",
            "content_status": "full",
        }

        print(
            f"✓ API MATCH "
            f"{item['title'][:55]}"
        )

    return resolved


# ============================================================
# 生成 Enriched
# ============================================================

def build_enriched(
    original_content,
    metadata,
    source_data,
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

    source = source_data.get(
        "source",
        "Unknown",
    )

    source_url = source_data.get(
        "source_url",
        "",
    )

    original_title = source_data.get(
        "original_title",
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
        "pending_search",
    )

    content_status = source_data.get(
        "content_status",
        "horizon_summary_only",
    )

    search_method = source_data.get(
        "search_method",
        "none",
    )

    match_score = source_data.get(
        "match_score",
        0,
    )

    _, original_body = (
        parse_front_matter(
            original_content
        )
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
search_method: "{search_method}"
match_score: {match_score:.2f}
ai_status: "pending"
original_title: "{yaml_escape(original_title)}"
---

"""

    body = f"""# {title}

## Horizon 摘要

{original_body.strip()}
"""

    if source_status == "fetched":

        body += f"""

## 原文信息

- 来源：{source}
- 原文标题：{original_title}
- 原文链接：{source_url}
- 来源获取方式：{search_method}
- 标题匹配度：{match_score:.2f}
"""

        if description:

            body += (
                f"- 页面摘要："
                f"{description}\n"
            )

        body += """

## 原文正文

"""

        body += article.strip()

    else:

        body += """

## 原文获取状态

当前自动搜索仍未找到可信的原始文章。

本条新闻不会把 Horizon 摘要
错误地当作原文。

下一阶段可继续进行原文搜索。

"""

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
# 读取 Atomic
# ============================================================

def load_items(
    input_dir,
    language,
):

    files = sorted(
        input_dir.glob("*.md")
    )

    items = []

    for path in files:

        content = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        metadata, body = (
            parse_front_matter(
                content
            )
        )

        title = metadata.get(
            "title",
            path.stem,
        )

        urls = extract_urls(
            content
        )

        items.append({
            "path": str(path),
            "file": path,
            "content": content,
            "metadata": metadata,
            "body": body,
            "title": title,
            "language": language,
            "date": metadata.get(
                "date",
                "",
            ),
            "summary": body,
            "urls": urls,
        })

    return items


# ============================================================
# 主处理
# ============================================================

def process_language(
    input_dir,
    output_dir,
    language,
):

    items = load_items(
        input_dir,
        language,
    )

    if not items:

        return 0

    print()
    print("=" * 70)
    print(
        f"LANGUAGE: {language.upper()}"
    )
    print(
        f"Atomic files: {len(items)}"
    )
    print("=" * 70)

    resolved = {}

    # --------------------------------------------------------
    # 第一层：已有 URL
    # --------------------------------------------------------

    url_items = [
        item
        for item in items
        if item["urls"]
    ]

    no_url_items = [
        item
        for item in items
        if not item["urls"]
    ]

    print()
    print(
        f"Existing URL: {len(url_items)}"
    )

    print(
        f"No URL: {len(no_url_items)}"
    )

    # 已有 URL 也并发抓取
    if url_items:

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            futures = {}

            for item in url_items:

                futures[
                    executor.submit(
                        extract_page,
                        item["urls"][0],
                    )
                ] = item

            for future in concurrent.futures.as_completed(
                futures
            ):

                item = futures[
                    future
                ]

                try:

                    page = future.result()

                except Exception:

                    page = {
                        "ok": False
                    }

                if page.get("ok"):

                    article = page.get(
                        "article",
                        "",
                    )

                    if len(article) >= 300:

                        resolved[
                            item["path"]
                        ] = {
                            "source": source_from_url(
                                page["url"]
                            ),
                            "source_url": page[
                                "url"
                            ],
                            "original_title": page.get(
                                "title",
                                "",
                            ),
                            "description": page.get(
                                "description",
                                "",
                            ),
                            "article": article,
                            "search_method": (
                                "atomic_url"
                            ),
                            "match_score": 1.0,
                            "source_status": "fetched",
                            "content_status": "full",
                        }

    # --------------------------------------------------------
    # 第二层：RSS
    # --------------------------------------------------------

    unresolved = [
        item
        for item in items
        if item["path"]
        not in resolved
    ]

    rss_results = search_rss_batch(
        unresolved
    )

    rss_resolved, rss_unresolved = (
        validate_rss_candidates(
            unresolved,
            rss_results,
        )
    )

    resolved.update(
        rss_resolved
    )

    # --------------------------------------------------------
    # 第三层：Agnes
    # --------------------------------------------------------

    final_unresolved = [
        item
        for item in items
        if item["path"]
        not in resolved
    ]

    print()
    print(
        f"Need Agnes fallback: "
        f"{len(final_unresolved)}"
    )

    agnes_candidates = agnes_batch(
        final_unresolved
    )

    agnes_resolved = (
        validate_agnes_results(
            final_unresolved,
            agnes_candidates,
        )
    )

    resolved.update(
        agnes_resolved
    )

    # --------------------------------------------------------
    # 输出
    # --------------------------------------------------------

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    fetched = 0
    pending = 0

    for item in items:

        if item["path"] in resolved:

            source_data = resolved[
                item["path"]
            ]

            fetched += 1

        else:

            source_data = {
                "source": "Unknown",
                "source_url": "",
                "original_title": "",
                "description": "",
                "article": "",
                "search_method": (
                    "unresolved"
                ),
                "match_score": 0,
                "source_status": (
                    "pending_search"
                ),
                "content_status": (
                    "horizon_summary_only"
                ),
            }

            pending += 1

        enriched = build_enriched(
            item["content"],
            item["metadata"],
            source_data,
        )

        output_file = (
            output_dir
            / item["file"].name
        )

        output_file.write_text(
            enriched,
            encoding="utf-8",
        )

    print()
    print(
        f"✓ {language.upper()} "
        f"fetched: {fetched}"
    )

    print(
        f"→ {language.upper()} "
        f"pending: {pending}"
    )

    return len(items)


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Horizon Source Enrichment V2"
        )
    )

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
        "HORIZON SOURCE ENRICHMENT V2"
    )
    print("=" * 70)

    print(
        f"Date: {args.date}"
    )

    print(
        f"ZH: {zh_input}"
    )

    print(
        f"EN: {en_input}"
    )

    print(
        f"Output: {output_root}"
    )

    print()
    print(
        "Strategy:"
    )
    print(
        "1. Existing URL"
    )
    print(
        "2. Google News RSS"
    )
    print(
        "3. Agnes API batch fallback"
    )
    print(
        "4. URL validation"
    )
    print(
        "5. Article extraction"
    )

    zh_count = process_language(
        zh_input,
        output_root / "zh",
        "zh",
    )

    en_count = process_language(
        en_input,
        output_root / "en",
        "en",
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

    if (
        zh_count == 0
        and en_count == 0
    ):

        raise RuntimeError(
            "没有发现 Atomic News。"
        )

    print()
    print(
        "✅ HORIZON SOURCE ENRICHMENT V2 COMPLETE"
    )


if __name__ == "__main__":
    main()
