#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Horizon Bilingual Digest Splitter V9

============================================================
核心目标
============================================================

Horizon 每天生成：

    Raw News/YYYY-MM-DD/
        ├── 中文 Horizon 日报
        └── 英文 Horizon 日报

本程序负责：

    Horizon 中文日报
            ↓
    拆解成 Atomic News

    Horizon 英文日报
            ↓
    拆解成 Atomic News


============================================================
最重要的完成判断
============================================================

绝对不能：

    Atomic 文件夹存在
        ↓
    就认为已经完成

也不能：

    Atomic 文件夹里存在 MD
        ↓
    就认为已经完成


真正的完成条件：

    1. Horizon 中文日报存在
    2. Horizon 英文日报存在
    3. 实际解析中文新闻数量 N
    4. 实际解析英文新闻数量 N
    5. 检查 Atomic/zh/ 中真正有效的 Atomic 文件
    6. 检查 Atomic/en/ 中真正有效的 Atomic 文件
    7. 数量必须与 Horizon 日报一致
    8. 文件名必须一一对应
    9. 最终再次验证

只有全部满足：

    Horizon 新闻数量
        ==
    Atomic 有效文件数量

并且：

    Horizon 新闻集合
        ==
    Atomic 文件集合

才允许：

    COMPLETE


============================================================
V9 修复的问题
============================================================

修复：

1. Atomic 文件夹不存在
   → 创建

2. Atomic 文件夹存在
   → 绝不直接判定完成

3. Atomic 文件夹里面只有 1 个或几个 MD
   → 与 Horizon 实际新闻数量比较

4. Horizon 原始日报被复制到 Atomic
   → 不能作为有效 Atomic

5. Atomic 数量不足
   → 自动补建

6. Atomic 数量超过理论数量
   → 判定异常

7. Atomic 文件名不对应
   → 判定异常

8. 生成完成后
   → 再次严格验证

9. 前天 / 昨天 / 今天
   → 逐日处理

============================================================
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

    return candidates[0]


# ============================================================
# 读取并解析 Horizon 日报
# ============================================================

def read_digest_items(
    input_file: Path,
):

    if not input_file.exists():

        raise FileNotFoundError(
            f"找不到 Horizon 日报："
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
            f"无法从 Horizon 日报解析出新闻："
            f"{input_file}"
        )

    return items


# ============================================================
# 判断是否是我们自己生成的 Atomic
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

    # 必须包含 Atomic 自己的结构
    if 'original_source: "Horizon"' not in content:
        return False

    if "## AI处理状态" not in content:
        return False

    # 防止 Horizon 原始日报冒充 Atomic
    if content.count("---") < 2:
        return False

    if "# Horizon 摘要" in content:
        return False

    if "# Horizon Summary" in content:
        return False

    return True


# ============================================================
# 理论 Atomic 文件集合
# ============================================================

def expected_atomic_filenames(
    items,
):

    expected = []

    for index, item in enumerate(
        items,
        start=1,
    ):

        filename = safe_filename(
            item["title"],
            index,
        )

        expected.append(
            filename
        )

    return expected


# ============================================================
# Atomic 完整性检查
# ============================================================

def validate_atomic_directory(
    output_dir: Path,
    items,
):

    expected = expected_atomic_filenames(
        items
    )

    expected_set = set(
        expected
    )

    actual_files = sorted(
        output_dir.glob("*.md")
    )

    valid_actual = []

    invalid_actual = []

    for file in actual_files:

        if valid_atomic_file(file):

            valid_actual.append(
                file
            )

        else:

            invalid_actual.append(
                file
            )

    actual_set = {
        file.name
        for file in valid_actual
    }

    missing = sorted(
        expected_set - actual_set
    )

    unexpected = sorted(
        actual_set - expected_set
    )

    duplicate_problem = (
        len(expected)
        != len(expected_set)
    )

    count_match = (
        len(valid_actual)
        == len(expected)
    )

    complete = (
        not duplicate_problem
        and count_match
        and not missing
        and not unexpected
    )

    return {
        "complete": complete,
        "expected_count": len(expected),
        "actual_md_count": len(actual_files),
        "valid_count": len(valid_actual),
        "invalid_count": len(invalid_actual),
        "missing": missing,
        "unexpected": unexpected,
        "invalid_files": [
            file.name
            for file in invalid_actual
        ],
        "expected": expected,
    }


# ============================================================
# 打印验证结果
# ============================================================

def print_validation(
    language: str,
    validation: dict,
):

    print()
    print(
        f"----- {language.upper()} ATOMIC VALIDATION -----"
    )

    print(
        f"Horizon expected : "
        f"{validation['expected_count']}"
    )

    print(
        f"Atomic MD total  : "
        f"{validation['actual_md_count']}"
    )

    print(
        f"Atomic valid     : "
        f"{validation['valid_count']}"
    )

    print(
        f"Invalid files    : "
        f"{validation['invalid_count']}"
    )

    print(
        f"Missing files    : "
        f"{len(validation['missing'])}"
    )

    print(
        f"Unexpected files : "
        f"{len(validation['unexpected'])}"
    )

    print(
        f"Complete         : "
        f"{validation['complete']}"
    )


# ============================================================
# 拆解单日报
# ============================================================

def split_one(
    input_file: Path,
    output_dir: Path,
    date: str,
    language: str,
    items=None,
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

    if items is None:

        items = read_digest_items(
            input_file
        )

    print(
        f"Expected Horizon items: "
        f"{len(items)}"
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

        # ====================================================
        # 已经是真正有效的 Atomic
        # ====================================================

        if valid_atomic_file(path):

            print(
                f"⏭️ Already valid: "
                f"{filename}"
            )

            count += 1

            continue

        # ====================================================
        # 不存在 / 无效
        # → 创建或重建
        # ====================================================

        if path.exists():

            print(
                f"♻️ Rebuilding invalid: "
                f"{filename}"
            )

        else:

            print(
                f"🆕 Creating: "
                f"{filename}"
            )

        markdown = make_atomic_markdown(
            item=item,
            language=language,
            date=date,
        )

        if len(markdown) < 250:

            raise RuntimeError(
                f"生成文件异常过短："
                f"{path}"
            )

        path.write_text(
            markdown,
            encoding="utf-8",
        )

        if not valid_atomic_file(path):

            raise RuntimeError(
                f"生成后的 Atomic 文件验证失败："
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
        f"HORIZON ATOMIC PROCESSING: {date}"
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

    # ========================================================
    # STEP 1
    # 检查 Horizon 原始日报
    # ========================================================

    print()
    print(
        "STEP 1: CHECK HORIZON RAW DIGEST"
    )

    if not raw_dir.exists():

        raise FileNotFoundError(
            f"{date} Horizon 原始日报目录不存在："
            f"{raw_dir}"
        )

    print(
        f"✅ Raw directory exists: "
        f"{raw_dir}"
    )

    zh_input = find_daily_digest(
        raw_dir,
        "zh",
    )

    en_input = find_daily_digest(
        raw_dir,
        "en",
    )

    print(
        f"ZH Horizon: "
        f"{zh_input if zh_input else 'MISSING'}"
    )

    print(
        f"EN Horizon: "
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

    # ========================================================
    # STEP 2
    # Atomic 目录
    # ========================================================

    print()
    print(
        "STEP 2: CHECK / CREATE ATOMIC DIRECTORIES"
    )

    if atomic_dir.exists():

        print(
            f"ℹ️ Atomic directory already exists: "
            f"{atomic_dir}"
        )

    else:

        print(
            f"🆕 Atomic directory does not exist."
        )

        print(
            f"🆕 Creating: "
            f"{atomic_dir}"
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
        f"✅ Atomic : {atomic_dir}"
    )

    print(
        f"✅ ZH     : {zh_dir}"
    )

    print(
        f"✅ EN     : {en_dir}"
    )

    # ========================================================
    # STEP 3
    # 先解析 Horizon 日报
    # ========================================================

    print()
    print(
        "STEP 3: PARSE HORIZON DIGEST"
    )

    zh_items = read_digest_items(
        zh_input
    )

    en_items = read_digest_items(
        en_input
    )

    print(
        f"ZH Horizon actual items: "
        f"{len(zh_items)}"
    )

    print(
        f"EN Horizon actual items: "
        f"{len(en_items)}"
    )

    # ========================================================
    # STEP 4
    # 无论文件夹是否存在，都必须检查里面
    # ========================================================

    print()
    print(
        "STEP 4: VALIDATE EXISTING ATOMIC CONTENT"
    )

    zh_validation = validate_atomic_directory(
        zh_dir,
        zh_items,
    )

    en_validation = validate_atomic_directory(
        en_dir,
        en_items,
    )

    print_validation(
        "zh",
        zh_validation,
    )

    print_validation(
        "en",
        en_validation,
    )

    # ========================================================
    # STEP 5
    # 不完整 → 拆解
    # ========================================================

    print()
    print(
        "STEP 5: BUILD / REBUILD ATOMIC"
    )

    # --------------------------------------------------------
    # 中文
    # --------------------------------------------------------

    if zh_validation["complete"]:

        print()
        print(
            "✅ ZH Atomic already matches "
            "the Horizon digest exactly."
        )

        print(
            f"   {zh_validation['valid_count']} "
            f"/ {zh_validation['expected_count']}"
        )

        print(
            "⏭️ Skip ZH rebuild."
        )

        zh_count = (
            zh_validation["valid_count"]
        )

    else:

        print()
        print(
            "⚠️ ZH Atomic is NOT complete."
        )

        print(
            f"   Horizon : "
            f"{zh_validation['expected_count']}"
        )

        print(
            f"   Valid   : "
            f"{zh_validation['valid_count']}"
        )

        print(
            f"   Missing : "
            f"{len(zh_validation['missing'])}"
        )

        print(
            f"   Invalid : "
            f"{len(zh_validation['invalid_files'])}"
        )

        print(
            "♻️ Starting ZH Atomic split."
        )

        zh_count = split_one(
            zh_input,
            zh_dir,
            date,
            "zh",
            items=zh_items,
        )

    # --------------------------------------------------------
    # 英文
    # --------------------------------------------------------

    if en_validation["complete"]:

        print()
        print(
            "✅ EN Atomic already matches "
            "the Horizon digest exactly."
        )

        print(
            f"   {en_validation['valid_count']} "
            f"/ {en_validation['expected_count']}"
        )

        print(
            "⏭️ Skip EN rebuild."
        )

        en_count = (
            en_validation["valid_count"]
        )

    else:

        print()
        print(
            "⚠️ EN Atomic is NOT complete."
        )

        print(
            f"   Horizon : "
            f"{en_validation['expected_count']}"
        )

        print(
            f"   Valid   : "
            f"{en_validation['valid_count']}"
        )

        print(
            f"   Missing : "
            f"{len(en_validation['missing'])}"
        )

        print(
            f"   Invalid : "
            f"{len(en_validation['invalid_files'])}"
        )

        print(
            "♻️ Starting EN Atomic split."
        )

        en_count = split_one(
            en_input,
            en_dir,
            date,
            "en",
            items=en_items,
        )

    # ========================================================
    # STEP 6
    # 最终严格验证
    # ========================================================

    print()
    print(
        "STEP 6: FINAL ATOMIC VALIDATION"
    )

    zh_final = validate_atomic_directory(
        zh_dir,
        zh_items,
    )

    en_final = validate_atomic_directory(
        en_dir,
        en_items,
    )

    print_validation(
        "zh",
        zh_final,
    )

    print_validation(
        "en",
        en_final,
    )

    # ========================================================
    # 最终硬门槛
    # ========================================================

    if not zh_final["complete"]:

        print()
        print(
            "❌ ZH FINAL VALIDATION FAILED"
        )

        raise RuntimeError(
            f"{date} ZH Atomic 最终验证失败。"
            f" Horizon={len(zh_items)}, "
            f"Valid={zh_final['valid_count']}, "
            f"Missing={len(zh_final['missing'])}, "
            f"Unexpected={len(zh_final['unexpected'])}"
        )

    if not en_final["complete"]:

        print()
        print(
            "❌ EN FINAL VALIDATION FAILED"
        )

        raise RuntimeError(
            f"{date} EN Atomic 最终验证失败。"
            f" Horizon={len(en_items)}, "
            f"Valid={en_final['valid_count']}, "
            f"Missing={len(en_final['missing'])}, "
            f"Unexpected={len(en_final['unexpected'])}"
        )

    # ========================================================
    # 成功
    # ========================================================

    print()
    print(
        "=" * 70
    )

    print(
        f"✅ {date} ATOMIC PROCESSING COMPLETE"
    )

    print(
        f"ZH: {zh_final['valid_count']}/"
        f"{len(zh_items)}"
    )

    print(
        f"EN: {en_final['valid_count']}/"
        f"{len(en_items)}"
    )

    print(
        "=" * 70
    )

    return {
        "date": date,
        "zh": zh_final["valid_count"],
        "en": en_final["valid_count"],
        "zh_expected": len(zh_items),
        "en_expected": len(en_items),
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
        "DIGEST SPLITTER V9"
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
    # 前天 → 昨天 → 今天
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
    # 三天最终硬验证
    # ========================================================

    print()
    print("=" * 80)

    print(
        "THREE-DAY ATOMIC FINAL RESULT"
    )

    print("=" * 80)

    for result in results:

        print(
            f"{result['date']} | "
            f"ZH "
            f"{result['zh']}/"
            f"{result['zh_expected']} | "
            f"EN "
            f"{result['en']}/"
            f"{result['en_expected']}"
        )

        if (
            result["zh"]
            != result["zh_expected"]
        ):

            raise RuntimeError(
                f"{result['date']} "
                f"ZH final verification failed."
            )

        if (
            result["en"]
            != result["en_expected"]
        ):

            raise RuntimeError(
                f"{result['date']} "
                f"EN final verification failed."
            )

    print()
    print(
        "✅ THREE-DAY ATOMIC PROCESSING COMPLETE"
    )


if __name__ == "__main__":
    main()
