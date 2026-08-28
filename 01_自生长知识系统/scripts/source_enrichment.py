#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Source Enrichment V2

功能：

1. 读取 Horizon Atomic News
2. 有原文 URL：
   - 直接抓取
   - 不进行搜索
3. 没有原文 URL：
   - 使用标题 + 日期进行新闻搜索
   - 自动寻找候选原文
4. 自动识别真实媒体来源
5. 保存原文标题、URL、正文
6. 中文 / 英文并行处理
7. 单篇失败不会影响其他新闻
8. 支持本地缓存
9. Horizon 与真实新闻来源彻底分离
10. 永远不修改 Atomic 原始文件

输出：

Raw News/YYYY-MM-DD-Enriched/
├── zh/
└── en/

Front Matter：

source: "真实媒体"
source_url: "https://..."
source_type: "original"
source_status: "found"
content_status: "full"
horizon_source: "Horizon"

如果找不到：

source: "Unknown"
source_url: ""
source_type: "digest"
source_status: "not_found"
content_status: "horizon_summary_only"
horizon_source: "Horizon"
"""

from __future__ import annotations

import argparse
import concurrent.futures
import html
import json
import re
import time

from pathlib import Path
from urllib.parse import (
    urlparse,
    quote_plus,
)

import requests
import xml.etree.ElementTree as ET


# ============================================================
# 基础设置
# ============================================================

USER_AGENT = (
    "Mozilla/5.0 "
    "(compatible; 748686-Knowledge-Bot/2.0; "
    "+https://github.com/748686/748686obsidian)"
)

TIMEOUT = 15

MAX_WORKERS = 8

MIN_ARTICLE_LENGTH = 500

CACHE_DIR_NAME = ".source_cache"


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
        "&#39;": "'",
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
        r"<noscript.*?</noscript>",
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
# YAML Front Matter
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
# URL 提取
# ============================================================

def extract_urls(text: str):

    urls = re.findall(
        r'https?://[^\s<>"\]\)]+',
        text,
    )

    result = []

    for url in urls:

        url = url.rstrip(
            ".,;，。；））"
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
# HTML 标题
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


# ============================================================
# Meta
# ============================================================

def extract_meta_content(
    content: str,
    name: str,
):

    patterns = [

        rf'<meta[^>]+'
        rf'(?:name|property)=["\']'
        rf'{re.escape(name)}'
        rf'["\'][^>]+'
        rf'content=["\'](.*?)["\']',

        rf'<meta[^>]+'
        rf'content=["\'](.*?)["\'][^>]+'
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


# ============================================================
# 网页正文
# ============================================================

def extract_article_text(
    content: str,
):

    # --------------------------------------------------------
    # 优先 article
    # --------------------------------------------------------

    match = re.search(
        r"<article[^>]*>(.*?)</article>",
        content,
        flags=re.I | re.S,
    )

    if match:

        article = match.group(1)

    else:

        # ----------------------------------------------------
        # 尝试 main
        # ----------------------------------------------------

        match = re.search(
            r"<main[^>]*>(.*?)</main>",
            content,
            flags=re.I | re.S,
        )

        if match:
            article = match.group(1)

        else:
            article = content

    # --------------------------------------------------------
    # 删除无关标签
    # --------------------------------------------------------

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
        r"<svg.*?</svg>",
        "",
        article,
        flags=re.I | re.S,
    )

    # --------------------------------------------------------
    # 保留段落结构
    # --------------------------------------------------------

    article = re.sub(
        r"</?(p|div|section|article|h1|h2|h3|h4|li|br)[^>]*>",
        "\n",
        article,
        flags=re.I,
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

        # 太短的导航/按钮文字过滤
        if len(line) <= 2:
            continue

        lines.append(line)

    # --------------------------------------------------------
    # 去除连续重复
    # --------------------------------------------------------

    cleaned = []

    previous = None

    for line in lines:

        if line == previous:
            continue

        cleaned.append(line)

        previous = line

    return "\n\n".join(
        cleaned
    ).strip()


# ============================================================
# URL 抓取
# ============================================================

def fetch_url(
    url: str,
):

    print(
        f"🌐 Fetch: {url}"
    )

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,*/*;q=0.8"
        ),
        "Accept-Language": (
            "zh-CN,zh;q=0.9,en;q=0.8"
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

        print(
            f"⚠️ Fetch failed: {url}"
        )

        print(
            f"   {exc}"
        )

        return {
            "ok": False,
            "url": url,
            "error": str(exc),
        }


# ============================================================
# 从 URL 推测来源
# ============================================================

def source_from_url(
    url: str,
):

    try:

        host = urlparse(
            url
        ).netloc.lower()

        host = host.replace(
            "www.",
            "",
        )

        mapping = {

            "cnn.com": "CNN",

            "nytimes.com":
                "The New York Times",

            "washingtonpost.com":
                "The Washington Post",

            "wsj.com":
                "The Wall Street Journal",

            "reuters.com":
                "Reuters",

            "apnews.com":
                "Associated Press",

            "bbc.com":
                "BBC",

            "bbc.co.uk":
                "BBC",

            "theguardian.com":
                "The Guardian",

            "bloomberg.com":
                "Bloomberg",

            "npr.org":
                "NPR",

            "cnbc.com":
                "CNBC",

            "abcnews.go.com":
                "ABC News",

            "nbcnews.com":
                "NBC News",

            "cbsnews.com":
                "CBS News",

            "foxnews.com":
                "Fox News",

            "economist.com":
                "The Economist",

            "ft.com":
                "Financial Times",

            "scmp.com":
                "South China Morning Post",

            "rthk.hk":
                "RTHK",

            "nhk.or.jp":
                "NHK",

            "yonhapnews.co.kr":
                "Yonhap",

            "xinhuanet.com":
                "新华社",

            "people.com.cn":
                "人民日报",

            "cctv.com":
                "央视",

            "chinanews.com.cn":
                "中国新闻网",

            "chinadaily.com.cn":
                "中国日报",

            "huanqiu.com":
                "环球时报",

            "thepaper.cn":
                "澎湃新闻",

            "caixin.com":
                "财新",

            "yicai.com":
                "第一财经",

            "stcn.com":
                "证券时报",

            "jiemian.com":
                "界面新闻",

        }

        if host in mapping:

            return mapping[host]

        # 子域名匹配
        for domain, name in mapping.items():

            if host.endswith(
                "." + domain
            ):

                return name

        return host

    except Exception:

        return "Unknown"


# ============================================================
# Google News RSS 搜索
# ============================================================

def google_news_search(
    title: str,
    date: str,
    language: str,
):

    print()
    print(
        "🔎 Search:"
    )

    print(
        f"   {title}"
    )

    # --------------------------------------------------------
    # 查询
    # --------------------------------------------------------

    query = (
        f'"{title}"'
    )

    if date:
        query += (
            f" {date}"
        )

    encoded = quote_plus(
        query
    )

    if language == "zh":

        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={encoded}"
            "&hl=zh-CN"
            "&gl=CN"
            "&ceid=CN:zh-Hans"
        )

    else:

        rss_url = (
            "https://news.google.com/rss/search?"
            f"q={encoded}"
            "&hl=en-US"
            "&gl=US"
            "&ceid=US:en"
        )

    headers = {
        "User-Agent": USER_AGENT
    }

    try:

        response = requests.get(
            rss_url,
            headers=headers,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        root = ET.fromstring(
            response.content
        )

    except Exception as exc:

        print(
            f"⚠️ Search failed: {exc}"
        )

        return None

    candidates = []

    # --------------------------------------------------------
    # 解析 RSS
    # --------------------------------------------------------

    for item in root.findall(
        ".//item"
    ):

        title_node = item.find(
            "title"
        )

        link_node = item.find(
            "link"
        )

        source_node = item.find(
            "source"
        )

        if (
            title_node is None
            or link_node is None
        ):
            continue

        result_title = clean_text(
            title_node.text or ""
        )

        link = (
            link_node.text or ""
        ).strip()

        publisher = ""

        if source_node is not None:

            publisher = clean_text(
                source_node.text or ""
            )

        if not link:
            continue

        # ----------------------------------------------------
        # 过滤明显不是新闻正文的结果
        # ----------------------------------------------------

        lower = link.lower()

        bad_domains = (
            "facebook.com",
            "twitter.com",
            "x.com",
            "youtube.com",
            "youtu.be",
            "instagram.com",
            "reddit.com",
        )

        if any(
            domain in lower
            for domain in bad_domains
        ):
            continue

        candidates.append(
            {
                "title": result_title,
                "url": link,
                "publisher": publisher,
            }
        )

    if not candidates:

        print(
            "   ❌ No candidates"
        )

        return None

    # --------------------------------------------------------
    # 选择第一个候选
    # --------------------------------------------------------

    best = candidates[0]

    print(
        "   ✅ Candidate:"
    )

    print(
        f"   {best['title']}"
    )

    print(
        f"   {best['url']}"
    )

    return best


# ============================================================
# 搜索缓存
# ============================================================

def cache_key(
    title: str,
    language: str,
):

    value = (
        f"{language}|{title}"
    )

    return str(
        abs(
            hash(value)
        )
    )


def load_cache(
    cache_dir: Path,
    title: str,
    language: str,
):

    path = (
        cache_dir
        / f"{cache_key(title, language)}.json"
    )

    if not path.exists():
        return None

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception:

        return None


def save_cache(
    cache_dir: Path,
    title: str,
    language: str,
    data: dict,
):

    cache_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        cache_dir
        / f"{cache_key(title, language)}.json"
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


# ============================================================
# 寻找原文
# ============================================================

def find_original_source(
    title: str,
    date: str,
    language: str,
    cache_dir: Path,
):

    # --------------------------------------------------------
    # 先读缓存
    # --------------------------------------------------------

    cached = load_cache(
        cache_dir,
        title,
        language,
    )

    if cached:

        print(
            f"💾 Cache hit: {title}"
        )

        return cached

    # --------------------------------------------------------
    # 搜索
    # --------------------------------------------------------

    candidate = google_news_search(
        title,
        date,
        language,
    )

    if not candidate:

        result = {
            "found": False,
            "reason": "not_found",
        }

        save_cache(
            cache_dir,
            title,
            language,
            result,
        )

        return result

    # --------------------------------------------------------
    # 获取候选原文
    # --------------------------------------------------------

    source_data = fetch_url(
        candidate["url"]
    )

    if not source_data.get(
        "ok"
    ):

        result = {
            "found": False,
            "reason": "fetch_failed",
            "candidate_url":
                candidate["url"],
            "candidate_title":
                candidate["title"],
            "publisher":
                candidate.get(
                    "publisher",
                    "",
                ),
        }

        save_cache(
            cache_dir,
            title,
            language,
            result,
        )

        return result

    article = source_data.get(
        "article",
        "",
    )

    # --------------------------------------------------------
    # 正文太短
    # --------------------------------------------------------

    if len(article) < MIN_ARTICLE_LENGTH:

        result = {
            "found": False,
            "reason": "article_too_short",
            "candidate_url":
                source_data.get(
                    "url",
                    candidate["url"],
                ),
            "candidate_title":
                source_data.get(
                    "title",
                    candidate["title"],
                ),
            "publisher":
                candidate.get(
                    "publisher",
                    "",
                ),
        }

        save_cache(
            cache_dir,
            title,
            language,
            result,
        )

        return result

    # --------------------------------------------------------
    # 识别来源
    # --------------------------------------------------------

    final_url = source_data.get(
        "url",
        candidate["url"],
    )

    publisher = (
        candidate.get(
            "publisher",
            "",
        )
        or source_from_url(
            final_url
        )
    )

    result = {
        "found": True,
        "source": publisher,
        "url": final_url,
        "title":
            source_data.get(
                "title",
                candidate["title"],
            ),
        "description":
            source_data.get(
                "description",
                "",
            ),
        "article": article,
    }

    save_cache(
        cache_dir,
        title,
        language,
        result,
    )

    return result


# ============================================================
# 处理单条新闻
# ============================================================

def process_file(
    input_file: Path,
    output_file: Path,
    language: str,
    date: str,
    cache_dir: Path,
):

    print()
    print(
        "=" * 70
    )

    print(
        f"[{language.upper()}] {input_file.name}"
    )

    content = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    metadata, original_body = (
        parse_front_matter(
            content
        )
    )

    title = metadata.get(
        "title",
        input_file.stem,
    )

    urls = extract_urls(
        content
    )

    # --------------------------------------------------------
    # Horizon 里本来就有 URL
    # --------------------------------------------------------

    if urls:

        print(
            "🔗 Existing URL detected"
        )

        source_data = fetch_url(
            urls[0]
        )

        if source_data.get(
            "ok"
        ):

            source_url = (
                source_data.get(
                    "url",
                    urls[0],
                )
            )

            source = source_from_url(
                source_url
            )

            original_title = (
                source_data.get(
                    "title",
                    "",
                )
            )

            description = (
                source_data.get(
                    "description",
                    "",
                )
            )

            article = (
                source_data.get(
                    "article",
                    "",
                )
            )

            source_status = "found"

            source_type = "original"

            content_status = (
                "full"
                if len(article)
                >= MIN_ARTICLE_LENGTH
                else "partial"
            )

        else:

            source_url = urls[0]

            source = source_from_url(
                source_url
            )

            original_title = ""

            description = ""

            article = ""

            source_status = (
                "fetch_failed"
            )

            source_type = "original"

            content_status = (
                "horizon_summary_only"
            )

    # --------------------------------------------------------
    # 没有 URL → 搜索
    # --------------------------------------------------------

    else:

        print(
            "🔍 No URL → searching original source"
        )

        source_data = (
            find_original_source(
                title=title,
                date=date,
                language=language,
                cache_dir=cache_dir,
            )
        )

        if source_data.get(
            "found"
        ):

            source_url = (
                source_data.get(
                    "url",
                    "",
                )
            )

            source = (
                source_data.get(
                    "source",
                    "Unknown",
                )
            )

            original_title = (
                source_data.get(
                    "title",
                    "",
                )
            )

            description = (
                source_data.get(
                    "description",
                    "",
                )
            )

            article = (
                source_data.get(
                    "article",
                    "",
                )
            )

            source_status = "found"

            source_type = "original"

            content_status = (
                "full"
                if len(article)
                >= MIN_ARTICLE_LENGTH
                else "partial"
            )

        else:

            source_url = (
                source_data.get(
                    "candidate_url",
                    "",
                )
            )

            source = "Unknown"

            original_title = (
                source_data.get(
                    "candidate_title",
                    "",
                )
            )

            description = ""

            article = ""

            source_status = "not_found"

            source_type = "digest"

            content_status = (
                "horizon_summary_only"
            )

    # --------------------------------------------------------
    # Front Matter
    # --------------------------------------------------------

    horizon_score = metadata.get(
        "horizon_score",
        "null",
    )

    front = f"""---
title: "{yaml_escape(title)}"
date: {yaml_escape(date)}
type: "news"
source: "{yaml_escape(source)}"
source_url: "{yaml_escape(source_url)}"
source_type: "{source_type}"
language: "{yaml_escape(language)}"
horizon_score: {horizon_score}
source_status: "{source_status}"
content_status: "{content_status}"
ai_status: "pending"
horizon_source: "Horizon"
original_title: "{yaml_escape(original_title)}"
---

"""

    # --------------------------------------------------------
    # 正文
    # --------------------------------------------------------

    body = (
        f"# {title}\n\n"
        "## Horizon 摘要\n\n"
    )

    body += (
        original_body.strip()
    )

    # --------------------------------------------------------
    # 原文信息
    # --------------------------------------------------------

    if source_status == "found":

        body += (
            "\n\n"
            "## 原文信息\n\n"
        )

        if source:

            body += (
                f"- 原始来源：{source}\n"
            )

        if original_title:

            body += (
                f"- 原文标题："
                f"{original_title}\n"
            )

        if source_url:

            body += (
                f"- 原文链接："
                f"{source_url}\n"
            )

        if description:

            body += (
                f"- 页面摘要："
                f"{description}\n"
            )

        body += (
            "\n"
            "## 原文正文\n\n"
        )

        body += (
            article.strip()
        )

    elif source_status == "fetch_failed":

        body += (
            "\n\n"
            "## 原文获取状态\n\n"
            "已检测到原始文章链接，"
            "但本次抓取失败。\n\n"
            "后续运行可以继续重试。\n\n"
        )

        body += (
            f"- 原文链接："
            f"{source_url}\n"
        )

    else:

        body += (
            "\n\n"
            "## 原文获取状态\n\n"
            "本条新闻在 Horizon 日报中"
            "没有提供原始文章链接。\n\n"
            "系统已经执行标题搜索，但"
            "目前没有获得可确认的原文。\n\n"
            "因此本文件不会把 Horizon 摘要"
            "误认为新闻原文。\n"
        )

        if source_url:

            body += (
                "\n"
                "候选链接："
                f"{source_url}\n"
            )

    # --------------------------------------------------------
    # AI 状态
    # --------------------------------------------------------

    body += (
        "\n\n"
        "## AI 处理状态\n\n"
        "等待 27 Skills 进行后续分析。\n"
    )

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file.write_text(
        front + body,
        encoding="utf-8",
    )

    print(
        f"✅ {output_file.name}"
    )

    print(
        f"   source_status = {source_status}"
    )

    print(
        f"   source = {source}"
    )

    return {
        "status": source_status,
        "source": source,
    }


# ============================================================
# 并行处理目录
# ============================================================

def process_language(
    input_dir: Path,
    output_dir: Path,
    language: str,
    date: str,
    cache_dir: Path,
):

    if not input_dir.exists():

        print(
            f"⚠️ Directory not found: {input_dir}"
        )

        return []

    files = sorted(
        input_dir.glob("*.md")
    )

    print()
    print(
        "=" * 70
    )

    print(
        f"{language.upper()} SOURCE ENRICHMENT"
    )

    print(
        "=" * 70
    )

    print(
        f"Files: {len(files)}"
    )

    results = []

    # --------------------------------------------------------
    # 并行
    # --------------------------------------------------------

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:

        futures = []

        for file in files:

            output_file = (
                output_dir
                / file.name
            )

            future = executor.submit(
                process_file,
                file,
                output_file,
                language,
                date,
                cache_dir,
            )

            futures.append(
                future
            )

        for future in concurrent.futures.as_completed(
            futures
        ):

            try:

                results.append(
                    future.result()
                )

            except Exception as exc:

                print(
                    f"⚠️ Worker failed: {exc}"
                )

    return results


# ============================================================
# 主程序
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

    parser.add_argument(
        "--date",
        required=True,
        help="Date YYYY-MM-DD",
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

    cache_dir = (
        output_root
        / CACHE_DIR_NAME
    )

    print(
        "=" * 70
    )

    print(
        "HORIZON SOURCE ENRICHMENT V2"
    )

    print(
        "=" * 70
    )

    print(
        f"ZH input : {zh_input}"
    )

    print(
        f"EN input : {en_input}"
    )

    print(
        f"Output   : {output_root}"
    )

    print(
        f"Workers  : {MAX_WORKERS}"
    )

    print(
        f"Date     : {args.date}"
    )

    # --------------------------------------------------------
    # 中文
    # --------------------------------------------------------

    zh_results = process_language(
        input_dir=zh_input,
        output_dir=(
            output_root / "zh"
        ),
        language="zh",
        date=args.date,
        cache_dir=cache_dir,
    )

    # --------------------------------------------------------
    # 英文
    # --------------------------------------------------------

    en_results = process_language(
        input_dir=en_input,
        output_dir=(
            output_root / "en"
        ),
        language="en",
        date=args.date,
        cache_dir=cache_dir,
    )

    # --------------------------------------------------------
    # 统计
    # --------------------------------------------------------

    all_results = (
        zh_results
        + en_results
    )

    found = sum(
        1
        for item in all_results
        if item.get("status")
        == "found"
    )

    not_found = sum(
        1
        for item in all_results
        if item.get("status")
        == "not_found"
    )

    fetch_failed = sum(
        1
        for item in all_results
        if item.get("status")
        == "fetch_failed"
    )

    print()
    print(
        "=" * 70
    )

    print(
        "SOURCE STATUS REPORT"
    )

    print(
        "=" * 70
    )

    print(
        f"Total processed : {len(all_results)}"
    )

    print(
        f"Original found  : {found}"
    )

    print(
        f"Not found       : {not_found}"
    )

    print(
        f"Fetch failed    : {fetch_failed}"
    )

    print()

    if not all_results:

        raise RuntimeError(
            "没有发现任何 Atomic News 文件。"
        )

    print(
        "✅ SOURCE ENRICHMENT V2 COMPLETE"
    )


if __name__ == "__main__":
    main()
