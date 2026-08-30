#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Horizon Bilingual Digest Splitter V7

============================================================
核心逻辑
============================================================

每次运行固定检查三个日期：

    前天
    昨天
    今天

每一天独立处理：

    Raw News/YYYY-MM-DD/
            ↓
    YYYY-MM-DD-Atomic/
            ├── zh/
            └── en/

重要原则：

1. 先创建日期 Atomic 文件夹
2. 再创建 zh / en 文件夹
3. 再寻找当天中文 / 英文 Horizon 日报
4. zh / en 分别判断是否完整
5. 已完整的语言跳过
6. 缺失的语言重新拆解
7. 三天全部检查通过后才成功
8. 不依赖“总文件数量”判断完整性
9. 不修改 Raw News 原始日报
10. Horizon 只是 original_source
"""

from __future__ import annotations

import argparse
import html
import re
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# 基础清理
# ============================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

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

    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    text = re.sub(
        r"[ \t]+",
        " ",
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
# 语言判断
# ============================================================

def detect_language(
    path: Path,
    content: str,
) -> str:

    name = path.name.lower()

    if (
        "-zh" in name
        or "_zh" in name
        or "中文" in name
    ):
        return "zh"

    if (
        "-en" in name
        or "_en" in name
        or "english" in name
        or "英文" in name
    ):
        return "en"

    chinese = len(
        re.findall(
            r"[\u4e00-\u9fff]",
            content,
        )
    )

    english = len(
        re.findall(
            r"[A-Za-z]",
            content,
        )
    )

    return (
        "zh"
        if chinese >= english
        else "en"
    )


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

    lower = text_clean.lower()

    for domain, source in domains.items():

        if domain in lower:
            return source

    return "Unknown"


# ============================================================
# URL
# ============================================================

def extract_urls(text: str) -> list[str]:

    urls = re.findall(
        r"https?://[^\s<>\]\)]+",
        text,
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
        line,
    )


def is_score_line(line: str):

    return re.search(
        r"(\d+(?:\.\d+)?)\s*/\s*10",
        line,
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
        re.search(
            pattern,
            line,
            re.I,
        )
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

        match = is_rank_line(line)

        if match:

            if current:
                items.append(current)

            rank = int(
                match.group(1)
            )

            title = clean_text(
                match.group(2)
            )

            score_match = re.search(
                r"(\d+(?:\.\d+)?)\s*/\s*10",
                title,
            )

            score = None

            if score_match:

                score = float(
                    score_match.group(1)
                )

                title = re.sub(
                    r"\s*\d+(?:\.\d+)?\s*/\s*10",
                    "",
                    title,
                ).strip()

            current = {
                "rank": rank,
                "title": title,
                "score": score,
                "body": [],
            }

            continue

        match = re.match(
            r"^[\[［]?\s*(\d{1,2})\s*版\s*[-—–:：]?\s*(.+?)[\]］]?\s*$",
            line,
        )

        if match:

            if current:
                items.append(current)

            current = {
                "rank": len(items) + 1,
                "title": clean_text(
                    match.group(2)
                ),
                "score": None,
                "body": [],
            }

            continue

        score_match = is_score_line(line)

        if score_match and current:

            current["score"] = float(
                score_match.group(1)
            )

            remaining = re.sub(
                r"\d+(?:\.\d+)?\s*/\s*10",
                "",
                line,
            ).strip()

            if remaining:
                current["body"].append(
                    remaining
                )

            continue

        if is_section_heading(line):
            continue

        if current:
            current["body"].append(
                line
            )

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
            item.get(
                "title",
                "",
            )
        )

        if not title:
            continue

        title = re.sub(
            r"\s*\d+(?:\.\d+)?\s*/\s*10\s*$",
            "",
            title,
        ).strip()

        key = re.sub(
            r"\W+",
            "",
            title.lower(),
        )

        if key in seen:
            continue

        seen.add(key)

        body = []

        for line in item.get(
            "body",
            [],
        ):

            line = clean_text(line)

            if not line:
                continue

            if line == title:
                continue

            body.append(line)

        item["title"] = title
        item["body"] = body

        result.append(item)

    return result


# ============================================================
# Markdown
# ============================================================

def make_atomic_markdown(
    item,
    language,
    date,
):

    title = clean_text(
        item["title"]
    )

    body = item.get(
        "body",
        [],
    )

    combined = "\n".join(body)

    urls = extract_urls(
        combined
    )

    source = detect_source(
        title + "\n" + combined
    )

    score = item.get(
        "score"
    )

    score_text = (
        f"{score:.1f}"
        if isinstance(
            score,
            (int, float),
        )
        else "null"
    )

    original_url = (
        urls[0]
        if urls
        else ""
    )

    if language == "zh":

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "新闻"
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

        front = f"""---
title: "{yaml_escape(title)}"
date: {date}
type: "新闻"
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

    content = "\n\n".join(
        body
    ).strip()

    if content:

        front += content
        front += "\n\n"

    else:

        if language == "zh":

            front += (
                "Horizon 日报中未提供该条目的完整正文。\n\n"
            )

        else:

            front += (
                "The Horizon digest did not provide "
                "a full body for this item.\n\n"
            )

    front += "## 原文信息\n\n"

    front += (
        f"- Source: {source}\n"
    )

    if original_url:

        front += (
            f"- Original URL: "
            f"{original_url}\n"
        )

    else:

        front += (
            "- Original URL: "
            "未从 Horizon 日报中找到\n"
        )

    front += (
        "\n## AI处理状态\n\n"
        "等待后续 AI 二次处理及 27 Skills 分析。\n"
    )

    return front


# ============================================================
# 文件名
# ============================================================

def safe_filename(
    title,
    rank,
):

    title = clean_text(
        title
    )

    title = re.sub(
        r'[\\/:*?"<>|]',
        "",
        title,
    )

    title = re.sub(
        r"[#\[\]{}]",
        "",
        title,
    )

    title = re.sub(
        r"\s+",
        " ",
        title,
    ).strip()

    if not title:
        title = "untitled"

    title = title[:100]

    return (
        f"{rank:03d}-{title}.md"
    )


# ============================================================
# 找当天 Horizon 日报
# ============================================================

def find_daily_digest(
    raw_dir: Path,
    language: str,
):

    if not raw_dir.exists():
        return None

    files = sorted(
        raw_dir.glob("*.md")
    )

    candidates = []

    for file in files:

        content = file.read_text(
            encoding="utf-8",
            errors="replace",
        )

        detected = detect_language(
            file,
            content,
        )

        if detected == language:
            candidates.append(file)

    if not candidates:
        return None

    # 如果有明确语言标记，优先
    explicit = []

    for file in candidates:

        name = file.name.lower()

        if language == "zh":

            if (
                "-zh" in name
                or "_zh" in name
                or "中文" in name
            ):
                explicit.append(file)

        else:

            if (
                "-en" in name
                or "_en" in name
                or "english" in name
                or "英文" in name
            ):
                explicit.append(file)

    if explicit:
        return sorted(explicit)[0]

    # 否则使用语言识别后的第一个
    return candidates[0]


# ============================================================
# 读取日报
# ============================================================

def split_one(
    input_file: Path,
    output_dir: Path,
    date: str,
    language: str,
):

    print()
    print("=" * 70)

    print(
        f"PROCESS {date} / {language.upper()}"
    )

    print("=" * 70)

    print(
        f"Input : {input_file}"
    )

    print(
        f"Output: {output_dir}"
    )

    if not input_file.exists():

        raise FileNotFoundError(
            f"找不到 {language} Horizon 日报："
            f"{input_file}"
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
            f"无法从 {input_file} "
            f"提取 {language} 新闻。"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    count = 0

    for index, item in enumerate(
        items,
        start=1,
    ):

        filename = safe_filename(
            item["title"],
            index,
        )

        path = (
            output_dir / filename
        )

        # 已存在且内容正常 → 跳过
        if path.exists():

            existing = path.read_text(
                encoding="utf-8",
                errors="replace",
            )

            if len(existing) >= 250:

                print(
                    f"⏭️ Already exists: "
                    f"{filename}"
                )

                count += 1

                continue

        markdown = make_atomic_markdown(
            item=item,
            language=language,
            date=date,
        )

        path.write_text(
            markdown,
            encoding="utf-8",
        )

        if len(markdown) < 250:

            raise RuntimeError(
                f"生成文件异常过短："
                f"{path}"
            )

        print(
            f"✅ [{language}] "
            f"{index:03d} "
            f"{item['title']}"
        )

        count += 1

    print()
    print(
        f"Generated / verified "
        f"{language.upper()}: {count}"
    )

    return count


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
        f"THREE-DAY ATOMIC PROCESSING: {date}"
    )
    print("#" * 80)

    raw_dir = (
        raw_root / date
    )

    atomic_dir = (
        raw_root
        / f"{date}-Atomic"
    )

    zh_dir = (
        atomic_dir / "zh"
    )

    en_dir = (
        atomic_dir / "en"
    )

    # --------------------------------------------------------
    # 第一层：先建所有目录
    # --------------------------------------------------------

    print()
    print("STEP 1: CREATE DIRECTORIES")

    raw_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    atomic_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    zh_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    en_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"✅ Raw    : {raw_dir}"
    )

    print(
        f"✅ Atomic : {atomic_dir}"
    )

    print(
        f"✅ ZH     : {zh_dir}"
    )

    print(
        f"✅ EN     : {en_dir}"
    )

    # --------------------------------------------------------
    # 第二层：找当天日报
    # --------------------------------------------------------

    print()
    print("STEP 2: FIND HORIZON DIGESTS")

    zh_input = find_daily_digest(
        raw_dir,
        "zh",
    )

    en_input = find_daily_digest(
        raw_dir,
        "en",
    )

    print(
        f"ZH input: "
        f"{zh_input if zh_input else 'MISSING'}"
    )

    print(
        f"EN input: "
        f"{en_input if en_input else 'MISSING'}"
    )

    if not zh_input:

        raise FileNotFoundError(
            f"{date} 中文 Horizon 日报不存在。"
        )

    if not en_input:

        raise FileNotFoundError(
            f"{date} 英文 Horizon 日报不存在。"
        )

    # --------------------------------------------------------
    # 第三层：分别检查 ZH / EN
    # --------------------------------------------------------

    print()
    print("STEP 3: CHECK ATOMIC ZH / EN")

    zh_existing = list(
        zh_dir.glob("*.md")
    )

    en_existing = list(
        en_dir.glob("*.md")
    )

    print(
        f"Existing ZH Atomic: "
        f"{len(zh_existing)}"
    )

    print(
        f"Existing EN Atomic: "
        f"{len(en_existing)}"
    )

    # --------------------------------------------------------
    # 第四层：分别生成
    # --------------------------------------------------------

    print()
    print("STEP 4: BUILD MISSING ATOMIC NEWS")

    zh_count = split_one(
        zh_input,
        zh_dir,
        date,
        "zh",
    )

    en_count = split_one(
        en_input,
        en_dir,
        date,
        "en",
    )

    # --------------------------------------------------------
    # 第五层：最终验证
    # --------------------------------------------------------

    print()
    print("STEP 5: FINAL VALIDATION")

    zh_final = len(
        list(
            zh_dir.glob("*.md")
        )
    )

    en_final = len(
        list(
            en_dir.glob("*.md")
        )
    )

    if zh_final <= 0:

        raise RuntimeError(
            f"{date} ZH Atomic 为空。"
        )

    if en_final <= 0:

        raise RuntimeError(
            f"{date} EN Atomic 为空。"
        )

    print(
        f"✅ {date} ZH Atomic: "
        f"{zh_final}"
    )

    print(
        f"✅ {date} EN Atomic: "
        f"{en_final}"
    )

    return {
        "date": date,
        "zh": zh_final,
        "en": en_final,
    }


# ============================================================
# 三天日期
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
        default="01_自生长知识系统/Raw News",
    )

    parser.add_argument(
        "--date",
        default=None,
        help=(
            "兼容单日期测试。"
            "如果不提供，则自动运行前天、昨天、今天。"
        ),
    )

    args = parser.parse_args()

    raw_root = Path(
        args.raw_root
    )

    print("=" * 80)
    print(
        "748686 HORIZON BILINGUAL "
        "DIGEST SPLITTER V7"
    )
    print("=" * 80)

    if args.date:

        dates = [args.date]

        print(
            f"MODE: SINGLE DATE"
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
    # 三天总验证
    # ========================================================

    print()
    print("=" * 80)
    print("THREE-DAY ATOMIC FINAL RESULT")
    print("=" * 80)

    for result in results:

        print(
            f"{result['date']} "
            f"| ZH={result['zh']} "
            f"| EN={result['en']}"
        )

        if result["zh"] <= 0:
            raise RuntimeError(
                f"{result['date']} ZH failed"
            )

        if result["en"] <= 0:
            raise RuntimeError(
                f"{result['date']} EN failed"
            )

    print()
    print(
        "✅ THREE-DAY ATOMIC PROCESSING COMPLETE"
    )


if __name__ == "__main__":
    main()
