#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Source Enrichment V2

处理逻辑：

第一层：
    1. Atomic News 中寻找已有 URL
    2. 有 URL -> 直接抓取
    3. 无 URL -> 使用公开新闻搜索/RSS候选来源
    4. 根据标题进行候选匹配
    5. 匹配成功 -> 抓取原文

第二层：
    如果第一层无法找到可靠来源：
        -> 调用 Agnes API
        -> 使用标题 + 日期 + Horizon 摘要
        -> 请求 Agnes 判断候选来源
        -> 返回候选 URL
        -> 再抓取候选网页

最终：

fetched
partial
pending_search
fetch_failed

重要原则：

1. 永远不把 Horizon 当真实新闻来源
2. 永远不伪造 source_url
3. Agnes 找不到时宁可 pending_search
4. 不修改 Atomic 原始文件
5. 输出到：
   Raw News/YYYY-MM-DD-Enriched/zh
   Raw News/YYYY-MM-DD-Enriched/en

Agnes：

环境变量：
    AGNES_API_KEY

可选：
    AGNES_BASE_URL

默认：
    https://apihub.agnes-ai.com/v1

模型：
    agnes-2.5-flash
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse

import requests


# ============================================================
# 配置
# ============================================================

DEFAULT_AGNES_BASE_URL = (
    "https://apihub.agnes-ai.com/v1"
)

AGNES_MODEL = "agnes-2.5-flash"

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/2.0; "
    "+https://github.com/748686/748686obsidian)"
)

TIMEOUT = 20

MAX_ARTICLE_CHARS = 30000

REQUEST_RETRIES = 2


# ============================================================
# 基础文本
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

    data = {}

    for line in raw_yaml.splitlines():

        if ":" not in line:
            continue

        key, value = line.split(
            ":",
            1,
        )

        key = key.strip()

        value = value.strip()

        value = value.strip(
            '"'
        ).strip(
            "'"
        )

        data[key] = value

    return data, body


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

            parsed = urlparse(
                url
            )

            if parsed.scheme in (
                "http",
                "https",
            ):

                if url not in result:
                    result.append(url)

        except Exception:
            pass

    return result


# ============================================================
# HTML
# ============================================================

def extract_html_title(content: str):

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


def extract_meta_content(
    content: str,
    name: str,
):

    patterns = [

        rf'<meta[^>]+(?:name|property)=["\']'
        rf'{re.escape(name)}["\'][^>]+'
        rf'content=["\'](.*?)["\']',

        rf'<meta[^>]+content=["\'](.*?)["\']'
        rf'[^>]+(?:name|property)=["\']'
        rf'{re.escape(name)}["\']',
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


def extract_article_text(content: str):

    # article 优先
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
        "",
        article,
        flags=re.I | re.S,
    )

    article = re.sub(
        r"<style.*?</style>",
        "",
        article,
        flags=re.I | re.S,
    )

    article = re.sub(
        r"<noscript.*?</noscript>",
        "",
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

        if len(line) < 2:
            continue

        lines.append(line)

    cleaned = []

    previous = None

    for line in lines:

        if line == previous:
            continue

        cleaned.append(line)

        previous = line

    text = "\n\n".join(
        cleaned
    )

    return text[:MAX_ARTICLE_CHARS]


# ============================================================
# URL 抓取
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

    last_error = ""

    for attempt in range(
        REQUEST_RETRIES + 1
    ):

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

            title = extract_html_title(
                content
            )

            description = extract_meta_content(
                content,
                "description",
            )

            article = extract_article_text(
                content
            )

            return {
                "ok": True,
                "url": response.url,
                "title": title,
                "description": description,
                "article": article,
                "status_code": response.status_code,
            }

        except Exception as exc:

            last_error = str(
                exc
            )

            print(
                f"⚠️ Fetch attempt "
                f"{attempt + 1} failed: "
                f"{exc}"
            )

            if attempt < REQUEST_RETRIES:

                time.sleep(
                    2 ** attempt
                )

    return {
        "ok": False,
        "error": last_error,
        "url": url,
    }


# ============================================================
# 标题匹配
# ============================================================

def normalize_title(title: str):

    title = clean_text(
        title
    ).lower()

    title = re.sub(
        r"[^\w\u4e00-\u9fff ]+",
        " ",
        title,
    )

    title = re.sub(
        r"\s+",
        " ",
        title,
    )

    return title.strip()


def title_similarity(
    target: str,
    candidate: str,
):

    a = normalize_title(
        target
    )

    b = normalize_title(
        candidate
    )

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    if a in b or b in a:
        return 0.90

    a_words = set(
        a.split()
    )

    b_words = set(
        b.split()
    )

    if not a_words or not b_words:
        return 0.0

    intersection = (
        a_words & b_words
    )

    union = (
        a_words | b_words
    )

    return len(
        intersection
    ) / len(
        union
    )


# ============================================================
# 搜索候选来源
# ============================================================

def search_candidates(
    title: str,
    date: str,
):

    print()
    print(
        "Searching candidate sources..."
    )

    query = f'"{title}" {date}'

    candidates = []

    # --------------------------------------------------------
    # Google/Bing 风格 RSS 新闻搜索
    # 使用 Google News RSS
    # --------------------------------------------------------

    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
    )

    try:

        response = requests.get(
            rss_url,
            headers={
                "User-Agent": USER_AGENT
            },
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        xml = response.text

        items = re.findall(
            r"<item>(.*?)</item>",
            xml,
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

            source_match = re.search(
                r"<source[^>]*>(.*?)</source>",
                item,
                flags=re.I | re.S,
            )

            if not title_match or not link_match:
                continue

            candidate_title = clean_text(
                html.unescape(
                    title_match.group(1)
                )
            )

            candidate_url = clean_text(
                html.unescape(
                    link_match.group(1)
                )
            )

            source = (
                clean_text(
                    source_match.group(1)
                )
                if source_match
                else ""
            )

            score = title_similarity(
                title,
                candidate_title,
            )

            candidates.append({
                "title": candidate_title,
                "url": candidate_url,
                "source": source,
                "score": score,
            })

    except Exception as exc:

        print(
            f"⚠️ RSS search failed: {exc}"
        )

    candidates.sort(
        key=lambda x: x["score"],
        reverse=True,
    )

    print(
        f"Candidates found: "
        f"{len(candidates)}"
    )

    for candidate in candidates[:5]:

        print(
            f"  {candidate['score']:.2f} "
            f"{candidate['title']}"
        )

    return candidates[:10]


# ============================================================
# Agnes API
# ============================================================

def get_agnes_config():

    api_key = os.getenv(
        "AGNES_API_KEY"
    )

    base_url = os.getenv(
        "AGNES_BASE_URL",
        DEFAULT_AGNES_BASE_URL,
    ).rstrip("/")

    return api_key, base_url


def call_agnes(
    title: str,
    date: str,
    horizon_summary: str,
    candidates: list,
):

    api_key, base_url = (
        get_agnes_config()
    )

    if not api_key:

        print(
            "ℹ️ AGNES_API_KEY not configured."
        )

        return None

    print()
    print(
        "Calling Agnes API..."
    )

    candidate_text = "\n".join(
        [
            f"{i + 1}. "
            f"{c['title']} | "
            f"{c['url']} | "
            f"{c.get('source', '')}"
            for i, c in enumerate(
                candidates[:10]
            )
        ]
    )

    if not candidate_text:

        candidate_text = (
            "No candidate source was "
            "found by RSS search."
        )

    system_prompt = """
你是新闻来源验证专家。

任务：
根据新闻标题、日期、Horizon摘要和候选来源，
判断最可能的真实原始新闻来源。

严格规则：

1. 不允许把 Horizon 当新闻媒体。
2. 不允许凭空制造 URL。
3. 只能从候选 URL 中选择，或者明确返回 null。
4. 如果候选来源与标题明显不匹配，返回 null。
5. 优先选择 Reuters、AP、BBC、CNN、ABC、NBC、
   CBS、NPR、NYT、WSJ、Bloomberg、Guardian、
   FT、NHK、新华社等真实新闻媒体。
6. source 必须是真实媒体名称。
7. confidence 必须在 0 到 1 之间。
8. 只返回 JSON。
"""

    user_prompt = f"""
新闻标题：
{title}

日期：
{date}

Horizon摘要：
{horizon_summary[:8000]}

候选来源：
{candidate_text}

请返回：

{{
  "source": "真实媒体名称或 null",
  "url": "候选 URL 或 null",
  "original_title": "候选来源标题或 null",
  "confidence": 0.0,
  "reason": "简短判断理由"
}}

只有 confidence >= 0.80 才认为匹配成功。
"""

    payload = {
        "model": AGNES_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt.strip(),
            },
            {
                "role": "user",
                "content": user_prompt.strip(),
            },
        ],
        "temperature": 0.0,
    }

    headers = {
        "Authorization": (
            f"Bearer {api_key}"
        ),
        "Content-Type": (
            "application/json"
        ),
    }

    endpoint = (
        f"{base_url}/chat/completions"
    )

    try:

        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=60,
        )

        response.raise_for_status()

        data = response.json()

        content = (
            data["choices"][0]
            ["message"]
            ["content"]
        )

        # 清理 markdown JSON
        content = re.sub(
            r"^```json\s*",
            "",
            content.strip(),
            flags=re.I,
        )

        content = re.sub(
            r"\s*```$",
            "",
            content.strip(),
        )

        result = json.loads(
            content
        )

        confidence = float(
            result.get(
                "confidence",
                0,
            )
        )

        if confidence < 0.80:

            print(
                f"⚠️ Agnes confidence too low: "
                f"{confidence}"
            )

            return None

        url = result.get(
            "url"
        )

        if not url:
            return None

        # 必须是 http/https
        parsed = urlparse(
            url
        )

        if parsed.scheme not in (
            "http",
            "https",
        ):
            return None

        print(
            "✅ Agnes source candidate:"
        )

        print(
            f"Source: "
            f"{result.get('source')}"
        )

        print(
            f"URL: {url}"
        )

        print(
            f"Confidence: "
            f"{confidence}"
        )

        return result

    except Exception as exc:

        print(
            f"⚠️ Agnes API failed: "
            f"{exc}"
        )

        return None


# ============================================================
# 来源推断
# ============================================================

def resolve_source(
    title: str,
    date: str,
    horizon_summary: str,
):

    # --------------------------------------------------------
    # 第一层：RSS
    # --------------------------------------------------------

    candidates = search_candidates(
        title,
        date,
    )

    # 高置信候选直接尝试
    for candidate in candidates:

        if candidate["score"] < 0.82:
            continue

        print(
            "Trying RSS candidate:"
        )

        print(
            candidate["url"]
        )

        fetched = fetch_url(
            candidate["url"]
        )

        if not fetched.get("ok"):
            continue

        fetched_title = (
            fetched.get("title")
            or candidate["title"]
        )

        similarity = title_similarity(
            title,
            fetched_title,
        )

        if similarity >= 0.75:

            fetched["source"] = (
                candidate.get(
                    "source"
                )
                or ""
            )

            fetched["match_score"] = (
                similarity
            )

            return fetched

    # --------------------------------------------------------
    # 第二层：Agnes
    # --------------------------------------------------------

    print()
    print(
        "RSS search did not produce "
        "a reliable source."
    )

    agnes_result = call_agnes(
        title=title,
        date=date,
        horizon_summary=horizon_summary,
        candidates=candidates,
    )

    if not agnes_result:
        return None

    url = agnes_result.get(
        "url"
    )

    fetched = fetch_url(
        url
    )

    if not fetched.get("ok"):

        return None

    fetched["source"] = (
        agnes_result.get(
            "source"
        )
        or ""
    )

    fetched["match_score"] = (
        title_similarity(
            title,
            fetched.get(
                "title",
                "",
            ),
        )
    )

    # 最终安全阈值
    if fetched["match_score"] < 0.70:

        print(
            "⚠️ Final title match too low."
        )

        return None

    return fetched


# ============================================================
# 生成 Enriched
# ============================================================

def build_enriched_markdown(
    original_content: str,
    metadata: dict,
    source_data: dict | None,
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

    # Atomic 正文
    _, original_body = (
        parse_front_matter(
            original_content
        )
    )

    source = ""

    source_url = ""

    original_title = ""

    description = ""

    article = ""

    if source_data and source_data.get(
        "ok"
    ):

        source = (
            source_data.get(
                "source"
            )
            or ""
        )

        source_url = (
            source_data.get(
                "url"
            )
            or ""
        )

        original_title = (
            source_data.get(
                "title"
            )
            or ""
        )

        description = (
            source_data.get(
                "description"
            )
            or ""
        )

        article = (
            source_data.get(
                "article"
            )
            or ""
        )

        source_status = "fetched"

        content_status = (
            "full"
            if len(article) >= 500
            else "partial"
        )

        if not source:

            source = "Unknown"

    else:

        source = "Unknown"

        source_status = (
            "pending_search"
        )

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
ai_status: "pending"
original_title: "{yaml_escape(original_title)}"
---

"""

    body = f"""# {title}

## Horizon 摘要

{original_body.strip()}
"""

    if source_status == "fetched":

        body += """

## 原文信息

"""

        body += (
            f"- Source: {source}\n"
        )

        body += (
            f"- 原文标题："
            f"{original_title}\n"
        )

        body += (
            f"- 原文链接："
            f"{source_url}\n"
        )

        if description:

            body += (
                f"- 页面摘要："
                f"{description}\n"
            )

        body += """

## 原文正文

"""

        body += (
            article.strip()
        )

    else:

        body += """

## 原文获取状态

当前自动流程没有找到足够可靠的真实原文。

已执行：

1. 新闻 RSS 候选搜索
2. 标题匹配
3. 网页抓取验证
4. Agnes API 二次来源判断

仍无法确认时，不生成虚假来源。

本条新闻保留为 Horizon 摘要，
等待后续搜索或人工确认。
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
# 单文件
# ============================================================

def process_file(
    input_file: Path,
    output_file: Path,
):

    print()
    print("=" * 70)

    print(
        f"Processing: {input_file.name}"
    )

    content = input_file.read_text(
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
        "",
    )

    date = metadata.get(
        "date",
        "",
    )

    urls = extract_urls(
        content
    )

    source_data = None

    # --------------------------------------------------------
    # 1. Atomic 已有 URL
    # --------------------------------------------------------

    if urls:

        print(
            f"Existing URL detected: "
            f"{urls[0]}"
        )

        fetched = fetch_url(
            urls[0]
        )

        if fetched.get("ok"):

            fetched["source"] = (
                metadata.get(
                    "source",
                    "",
                )
            )

            source_data = fetched

    # --------------------------------------------------------
    # 2. 没有 URL -> 搜索 + Agnes
    # --------------------------------------------------------

    if not source_data:

        print(
            "No reliable existing source."
        )

        source_data = resolve_source(
            title=title,
            date=date,
            horizon_summary=body,
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

    if source_data:

        print(
            "✅ SOURCE FOUND"
        )

    else:

        print(
            "⚠️ SOURCE NOT FOUND"
        )


# ============================================================
# 语言目录
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path,
):

    if not input_dir.exists():

        print(
            f"⚠️ Missing directory: "
            f"{input_dir}"
        )

        return 0

    files = sorted(
        input_dir.glob(
            "*.md"
        )
    )

    count = 0

    for file in files:

        output_file = (
            output_dir
            / file.name
        )

        process_file(
            file,
            output_file,
        )

        count += 1

        time.sleep(
            0.3
        )

    return count


# ============================================================
# Main
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Horizon Source "
            "Enrichment V2"
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

    api_key, base_url = (
        get_agnes_config()
    )

    if api_key:

        print(
            "Agnes API: ENABLED"
        )

        print(
            f"Agnes Base URL: "
            f"{base_url}"
        )

        print(
            f"Agnes Model: "
            f"{AGNES_MODEL}"
        )

    else:

        print(
            "Agnes API: DISABLED "
            "(AGNES_API_KEY missing)"
        )

    zh_count = process_language(
        zh_input,
        output_root / "zh",
    )

    en_count = process_language(
        en_input,
        output_root / "en",
    )

    print()
    print("=" * 70)

    print(
        "FINAL RESULT"
    )

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
            "没有发现 Atomic News 文件。"
        )

    print()
    print(
        "✅ SOURCE ENRICHMENT V2 COMPLETE"
    )


if __name__ == "__main__":
    main()
