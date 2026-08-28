#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon 双语日报拆解器 V5

核心目标：
1. 同时处理 summary-zh.md 和 summary-en.md
2. 中文、英文分别拆解
3. 每条资讯生成独立 Markdown
4. source 使用真实新闻来源，而不是 Horizon
5. 尽可能保留 Horizon 对该新闻的完整摘要
6. 尝试提取作者、来源、原文链接
7. 不依赖固定的 Horizon UI 文案
8. 为后续 27 Skills AI 二次处理保留足够上下文
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from urllib.parse import urlparse


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
        "&apos;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        "[&-x27;": "'",
        "[&-×27;": "'",
        "&#×27;": "'",
        "&-x27;": "'",
        "&-×27;": "'",
        "&#x2": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # 清除 HTML 标签
    text = re.sub(r"<[^>]+>", "", text)

    # 清理多余空格
    text = re.sub(r"[ \t]+", " ", text)

    # 清理明显残留
    text = text.replace("?/10", "")
    text = text.replace("？/10", "")

    return text.strip()


def yaml_escape(text: str) -> str:
    """安全生成 YAML 双引号字符串。"""

    text = clean_text(text)
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    text = text.replace("\n", " ")

    return text


# ============================================================
# 语言识别
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

SOURCE_PATTERNS = [
    # 国际媒体
    (r"\bReuters\b", "Reuters"),
    (r"\bCNN\b", "CNN"),
    (r"\bBBC\b", "BBC"),
    (r"\bABC News\b", "ABC News"),
    (r"\bNBC\b", "NBC News"),
    (r"\bCBS\b", "CBS News"),
    (r"\bNPR\b", "NPR"),
    (r"\bThe New York Times\b", "The New York Times"),
    (r"\bNew York Times\b", "The New York Times"),
    (r"\bWashington Post\b", "The Washington Post"),
    (r"\bThe Washington Post\b", "The Washington Post"),
    (r"\bBloomberg\b", "Bloomberg"),
    (r"\bThe Guardian\b", "The Guardian"),
    (r"\bGuardian\b", "The Guardian"),
    (r"\bFinancial Times\b", "Financial Times"),
    (r"\bThe Economist\b", "The Economist"),
    (r"\bEconomist\b", "The Economist"),
    (r"\bThe Atlantic\b", "The Atlantic"),
    (r"\bAtlantic\b", "The Atlantic"),
    (r"\bFox News\b", "Fox News"),
    (r"\bFrance 24\b", "France 24"),
    (r"\bLe Monde\b", "Le Monde"),
    (r"\bLe Figaro\b", "Le Figaro"),
    (r"\bDer Spiegel\b", "Der Spiegel"),
    (r"\bFAZ\b", "Frankfurter Allgemeine Zeitung"),
    (r"\bFrankfurter Allgemeine Zeitung\b", "Frankfurter Allgemeine Zeitung"),
    (r"\bThe Observer\b", "The Observer"),
    (r"\bJapan Times\b", "The Japan Times"),
    (r"\bThe Japan Times\b", "The Japan Times"),

    # 中国大陆
    (r"人民日报", "人民日报"),
    (r"新华社", "新华社"),
    (r"央视", "央视"),
    (r"中国新闻网", "中国新闻网"),
    (r"中国日报", "中国日报"),
    (r"环球时报", "环球时报"),
    (r"澎湃", "澎湃新闻"),
    (r"财新", "财新"),
    (r"第一财经", "第一财经"),
    (r"证券时报", "证券时报"),
    (r"界面新闻", "界面新闻"),
    (r"36氪", "36氪"),
    (r"虎嗅", "虎嗅"),

    # 香港
    (r"\bSCMP\b", "South China Morning Post"),
    (r"South China Morning Post", "South China Morning Post"),
    (r"\bRTHK\b", "RTHK"),
    (r"\bHKFP\b", "Hong Kong Free Press"),
    (r"\bTVB\b", "TVB"),
    (r"\bNow\b", "Now TV"),

    # 台湾
    (r"中央社", "中央社"),
    (r"联合报", "联合报"),
    (r"自由时报", "自由时报"),
    (r"工商时报", "工商时报"),
    (r"经济日报", "经济日报"),
    (r"TVBS", "TVBS"),
    (r"三立", "三立新闻"),
    (r"东森", "东森新闻"),

    # 日本
    (r"\bNHK\b", "NHK"),
    (r"共同社", "共同社"),
    (r"日经", "日本经济新闻"),
    (r"朝日新闻", "朝日新闻"),
    (r"读卖新闻", "读卖新闻"),
    (r"每日新闻", "每日新闻"),

    # 韩国
    (r"韩联社", "韩联社"),
    (r"\bKBS\b", "KBS"),
    (r"\bMBC\b", "MBC"),
    (r"\bSBS\b", "SBS"),
    (r"\bYTN\b", "YTN"),
    (r"朝鲜日报", "朝鲜日报"),
    (r"中央日报", "中央日报"),

    # 科技 / 社区
    (r"\bHacker News\b", "Hacker News"),
    (r"\bOpenAI Blog\b", "OpenAI"),
    (r"\bOpenAI\b", "OpenAI"),
    (r"\bLessWrong\b", "LessWrong"),
    (r"\bReddit\b", "Reddit"),
]


def detect_source(text: str) -> str:
    """
    从标题、正文和来源信息中识别真实来源。

    注意：
    Horizon 本身永远不会作为 source。
    """

    text = clean_text(text)

    for pattern, source in SOURCE_PATTERNS:
        if re.search(pattern, text, re.I):
            return source

    # Hacker News 常见格式
    if re.search(
        r"hackernews|hacker news",
        text,
        re.I,
    ):
        return "Hacker News"

    # Reddit
    if re.search(r"\breddit\b", text, re.I):
        return "Reddit"

    # 如果没有识别到
    return "Unknown"


# ============================================================
# 作者 / 发布者识别
# ============================================================

def detect_author(text: str) -> str:

    text = clean_text(text)

    patterns = [
        r"(?:作者|作者为|撰稿人)[：:\s]+([^\n，。,；;]+)",
        r"(?:by|By)\s+([A-Z][A-Za-z0-9 ._-]{1,80})",
        r"提交者[：:\s]+([^\s，。,；;]+)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.I,
        )

        if match:
            author = clean_text(match.group(1))

            if 1 <= len(author) <= 100:
                return author

    return ""


# ============================================================
# URL 提取
# ============================================================

def extract_urls(text: str) -> list[str]:

    urls = re.findall(
        r"https?://[^\s<>\]\)]+",
        text,
    )

    result = []

    for url in urls:

        url = url.rstrip(".,;，。；）)】")

        try:
            parsed = urlparse(url)

            if parsed.scheme in {"http", "https"}:
                result.append(url)

        except Exception:
            continue

    # 去重
    seen = set()
    output = []

    for url in result:
        if url not in seen:
            seen.add(url)
            output.append(url)

    return output


# ============================================================
# Horizon 条目解析
# ============================================================

def extract_ranked_items(content: str):

    lines = content.splitlines()

    items = []

    current = None

    for raw_line in lines:

        original = raw_line.rstrip()
        line = clean_text(original)

        if not line:
            continue

        # ----------------------------------------------------
        # 数字排行
        #
        # 1. 标题
        # 2. 标题
        # ----------------------------------------------------

        match = re.match(
            r"^(\d{1,3})\s*[\.\、\)]\s*(.+?)\s*$",
            line,
        )

        if match:

            if current:
                items.append(current)

            current = {
                "rank": int(match.group(1)),
                "title": clean_text(match.group(2)),
                "score": None,
                "body": [],
            }

            continue

        # ----------------------------------------------------
        # 中文版面新闻
        #
        # 01版-xxx
        # ［01版-xxx］
        # ----------------------------------------------------

        match = re.match(
            r"^[\[［]?\s*(\d{1,2})\s*版\s*[-—–:：]?\s*(.+?)[\]］]?\s*$",
            line,
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

        # ----------------------------------------------------
        # 评分
        # ----------------------------------------------------

        score_match = re.search(
            r"(\d+(?:\.\d+)?)\s*/\s*10",
            line,
        )

        if score_match and current:

            current["score"] = float(
                score_match.group(1)
            )

            remaining = re.sub(
                r"(\d+(?:\.\d+)?)\s*/\s*10",
                "",
                line,
            ).strip()

            if remaining:
                current["body"].append(
                    remaining
                )

            continue

        # ----------------------------------------------------
        # Horizon UI 噪声
        # ----------------------------------------------------

        skip_patterns = [

            r"^Horizon$",
            r"^Horizon 摘要$",
            r"^Horizon Summary$",

            r"^AI Creator Radar$",
            r"^AI创作者雷达$",

            r"^科技新闻$",
            r"^财经新闻$",
            r"^国际新闻$",
            r"^国内新闻$",
            r"^社会新闻$",
            r"^体育新闻$",

            r"^核心资讯$",
            r"^重要资讯$",

            r"^参考链接$",
            r"^Tags?$",

            r"^背景$",
            r"^影响$",
            r"^社区讨论$",
            r"^深度分析$",

            r"^从 .* 条内容中筛选",

        ]

        if any(
            re.search(pattern, line, re.I)
            for pattern in skip_patterns
        ):
            continue

        # ----------------------------------------------------
        # 正文
        # ----------------------------------------------------

        if current:
            current["body"].append(line)

    if current:
        items.append(current)

    return items


# ============================================================
# 条目清理
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

        # 清除标题尾部评分
        title = re.sub(
            r"\s*\d+(?:\.\d+)?\s*/\s*10\s*$",
            "",
            title,
        ).strip()

        # 清除明显的 Horizon 残留
        title = re.sub(
            r"^Horizon\s*[:：]\s*",
            "",
            title,
            flags=re.I,
        )

        key = title.lower()

        if key in seen:
            continue

        seen.add(key)

        body = []

        for line in item.get("body", []):

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
# 生成 Markdown
# ============================================================

def make_atomic_markdown(
    item,
    language: str,
    date: str,
    rank: int,
):

    title = item["title"]

    score = item.get("score")

    score_text = (
        f"{score:.1f}"
        if isinstance(score, (int, float))
        else "null"
    )

    # --------------------------------------------------------
    # 尽可能从该条新闻自己的正文识别真实来源
    # --------------------------------------------------------

    source_text = " ".join(
        [title] + item.get("body", [])
    )

    source = detect_source(source_text)

    author = detect_author(source_text)

    urls = extract_urls(source_text)

    # --------------------------------------------------------
    # YAML
    # --------------------------------------------------------

    front = [
        "---",
        f'title: "{yaml_escape(title)}"',
        f"date: {date}",
        'type: "新闻"',
        f'source: "{yaml_escape(source)}"',
    ]

    if author:
        front.append(
            f'author: "{yaml_escape(author)}"'
        )

    front.extend([
        f"language: {language}",
        f"horizon_score: {score_text}",
        'status: "待AI处理"',
        "---",
        "",
    ])

    # --------------------------------------------------------
    # 正文
    # --------------------------------------------------------

    content = []

    content.append(f"# {title}")
    content.append("")

    content.append("## 新闻摘要")
    content.append("")

    body = item.get("body", [])

    # 删除明显的重复 Horizon UI 文案
    clean_body = []

    for line in body:

        lower = line.lower()

        if (
            "本文来自 horizon 日报拆解" in lower
            or
            "this item was extracted from the horizon digest" in lower
        ):
            continue

        clean_body.append(line)

    if clean_body:

        content.extend(
            clean_body
        )

    else:

        content.append(
            "当前日报中未提供该资讯的完整摘要，"
            "等待后续 AI 获取原文并补充。"
        )

    # --------------------------------------------------------
    # 原文链接
    # --------------------------------------------------------

    if urls:

        content.append("")
        content.append("## 原文链接")
        content.append("")

        for url in urls:
            content.append(
                f"- {url}"
            )

    # --------------------------------------------------------
    # 数据来源
    # --------------------------------------------------------

    content.append("")
    content.append("## 来源信息")
    content.append("")
    content.append(
        f"- 来源：{source}"
    )

    if author:
        content.append(
            f"- 作者：{author}"
        )

    content.append(
        "- Horizon：日报聚合与初步筛选"
    )

    content.append(
        "- 后续处理：27 Skills AI 深度处理"
    )

    content.append("")

    return (
        "\n".join(front)
        + "\n"
        + "\n".join(content)
        + "\n"
    )


# ============================================================
# 文件名
# ============================================================

def safe_filename(
    title: str,
    rank: int,
):

    title = clean_text(title)

    # 删除非法字符
    title = re.sub(
        r'[\\/:*?"<>|]',
        "",
        title,
    )

    # 删除 Markdown 噪声
    title = re.sub(
        r"[#\[\]{}]",
        "",
        title,
    )

    # HTML entity
    title = html.unescape(title)

    # 空白
    title = re.sub(
        r"\s+",
        " ",
        title,
    ).strip()

    if not title:
        title = "untitled"

    # 文件名长度限制
    title = title[:100]

    return f"{rank:03d}-{title}.md"


# ============================================================
# 单语言
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
        f"Processing {language.upper()} Horizon digest"
    )
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
            f"无法从 {input_file} 提取 Horizon 资讯。"
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

        path = output_dir / filename

        markdown = make_atomic_markdown(
            item=item,
            language=language,
            date=date,
            rank=index,
        )

        path.write_text(
            markdown,
            encoding="utf-8",
        )

        count += 1

        source = detect_source(
            item["title"]
            + " "
            + " ".join(item["body"])
        )

        print(
            f"[{language}] "
            f"{index:03d} "
            f"[{source}] "
            f"{item['title']}"
        )

    print()
    print(
        f"✅ {language.upper()} generated: {count}"
    )

    return count


# ============================================================
# 主程序
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Horizon bilingual digest splitter V5"
        )
    )

    parser.add_argument(
        "--zh",
        required=True,
        help="中文 Horizon summary",
    )

    parser.add_argument(
        "--en",
        required=True,
        help="英文 Horizon summary",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Atomic 输出根目录",
    )

    parser.add_argument(
        "--date",
        required=True,
        help="日期，例如 2026-08-28",
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
        "Horizon Bilingual Digest Splitter V5"
    )
    print("=" * 70)

    print(f"ZH : {zh_input}")
    print(f"EN : {en_input}")
    print(f"OUT: {output_root}")
    print(f"DATE: {args.date}")

    # ========================================================
    # 中文
    # ========================================================

    zh_count = split_one(
        input_file=zh_input,
        output_dir=output_root / "zh",
        date=args.date,
        language="zh",
    )

    # ========================================================
    # 英文
    # ========================================================

    en_count = split_one(
        input_file=en_input,
        output_dir=output_root / "en",
        date=args.date,
        language="en",
    )

    # ========================================================
    # 最终验证
    # ========================================================

    print()
    print("=" * 70)
    print("FINAL VALIDATION")
    print("=" * 70)

    print(
        f"Chinese News : {zh_count}"
    )

    print(
        f"English News : {en_count}"
    )

    if zh_count <= 0:

        raise RuntimeError(
            "❌ 中文日报没有生成任何新闻。"
        )

    if en_count <= 0:

        raise RuntimeError(
            "❌ 英文日报没有生成任何新闻。"
        )

    print()
    print("✅ 中文拆解成功")
    print("✅ 英文拆解成功")
    print("✅ 真实 source 字段已启用")
    print("✅ Horizon 不再作为新闻 source")
    print("✅ 双语日报拆解全部完成")


if __name__ == "__main__":
    main()
