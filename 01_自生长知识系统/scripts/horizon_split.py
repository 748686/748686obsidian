#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Digest Splitter V5

功能：
1. 读取 Horizon summary Markdown
2. 自动识别编号新闻条目
3. 提取标题、评分、正文
4. 清理 HTML entities
5. 生成合法 YAML Front Matter
6. 每条新闻生成独立 MD
7. 根据语言写入 zh / en 子目录
8. 不依赖 Horizon 固定的“从 X 条内容中筛选出 Y 条重要资讯”文字
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path


# ============================================================
# 基础工具
# ============================================================

def clean_text(text: str) -> str:
    """清理 HTML entity、异常空白以及 Horizon 常见转义。"""

    if not text:
        return ""

    # HTML entity，例如:
    # &#x27; -> '
    # &amp;   -> &
    # &quot;  -> "
    text = html.unescape(text)

    # 某些情况下可能出现双重编码
    for _ in range(2):
        decoded = html.unescape(text)
        if decoded == text:
            break
        text = decoded

    # 清理零宽字符
    text = text.replace("\u200b", "")
    text = text.replace("\ufeff", "")

    # 统一换行
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # 压缩连续空格，但保留换行
    text = re.sub(r"[ \t]+", " ", text)

    # 清理多余空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def yaml_quote(value: str) -> str:
    """安全生成 YAML 双引号字符串。"""

    value = clean_text(value)

    value = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )

    return f'"{value}"'


def safe_filename(title: str, index: int) -> str:
    """生成安全的 Markdown 文件名。"""

    title = clean_text(title)

    # 删除 Markdown / HTML 标记
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", title)

    # Windows / Linux / GitHub 都比较安全的文件名
    title = re.sub(r'[\\/:*?"<>|]', "-", title)

    # 清理多余空格
    title = re.sub(r"\s+", " ", title).strip()

    # 防止文件名过长
    if len(title) > 100:
        title = title[:100].rstrip()

    if not title:
        title = f"atomic-news-{index:03d}"

    return f"{index:03d}-{title}.md"


# ============================================================
# 评分识别
# ============================================================

SCORE_RE = re.compile(
    r"""
    (?:
        (?P<int>\d{1,2})
        (?:\s*/\s*10)
    )
    """,
    re.VERBOSE,
)


def extract_score(text: str) -> float | None:
    """从文本中提取 0-10 评分。"""

    if not text:
        return None

    match = SCORE_RE.search(text)

    if not match:
        return None

    try:
        value = float(match.group("int"))
        if 0 <= value <= 10:
            return value
    except ValueError:
        pass

    return None


# ============================================================
# 新闻条目识别
# ============================================================

ITEM_RE = re.compile(
    r"""
    ^\s*
    (?P<number>\d{1,3})
    [\.\、\)]
    \s*
    (?P<title>.+?)
    \s*
    (?:
        (?P<score>\d{1,2}(?:\.\d+)?)
        \s*/\s*10
    )?
    \s*$
    """,
    re.VERBOSE,
)


def looks_like_noise(line: str) -> bool:
    """判断一行是不是明显不是新闻标题。"""

    line = clean_text(line)

    if not line:
        return True

    # Horizon 页面结构 / UI
    noise_patterns = [
        r"^Horizon Summary:",
        r"^Horizon 摘要",
        r"^AI 创作者雷达$",
        r"^AI Creator Radar$",
        r"^科技新闻$",
        r"^Technology News$",
        r"^新闻$",
        r"^摘要$",
        r"^核心观点$",
        r"^为什么重要$",
        r"^深度分析$",
        r"^结论$",
        r"^参考链接$",
        r"^社区讨论$",
        r"^背景$",
        r"^影响$",
    ]

    for pattern in noise_patterns:
        if re.search(pattern, line, re.IGNORECASE):
            return True

    return False


def parse_items(lines: list[str]) -> list[dict]:
    """
    自动识别：

    1. 标题
       8.0/10

    或：

    1. 标题 8.0/10

    或：

    1. 标题
    8/10

    并把后续内容归入该新闻。
    """

    items: list[dict] = []

    current: dict | None = None

    for raw_line in lines:
        line = clean_text(raw_line)

        if not line:
            if current is not None:
                current["body"].append("")
            continue

        match = ITEM_RE.match(line)

        # ----------------------------------------------------
        # 发现新的编号新闻
        # ----------------------------------------------------
        if match:
            number = int(match.group("number"))
            title = clean_text(match.group("title"))

            if looks_like_noise(title):
                continue

            score = None

            if match.group("score"):
                try:
                    score = float(match.group("score"))
                except ValueError:
                    score = None

            # 保存上一条
            if current is not None:
                items.append(current)

            current = {
                "number": number,
                "title": title,
                "score": score,
                "body": [],
            }

            continue

        # ----------------------------------------------------
        # 单独的评分行
        # ----------------------------------------------------
        score = extract_score(line)

        if (
            current is not None
            and score is not None
            and len(line) <= 12
        ):
            current["score"] = score
            continue

        # ----------------------------------------------------
        # 普通正文
        # ----------------------------------------------------
        if current is not None:
            current["body"].append(line)

    # 最后一条
    if current is not None:
        items.append(current)

    return items


# ============================================================
# 更强的标题 / 正文清理
# ============================================================

def clean_item(item: dict) -> dict:
    title = clean_text(item["title"])

    body_lines = []

    for line in item["body"]:
        line = clean_text(line)

        if not line:
            if body_lines and body_lines[-1] != "":
                body_lines.append("")
            continue

        # 如果正文重复出现标题，去掉
        if line == title:
            continue

        body_lines.append(line)

    # 删除尾部空行
    while body_lines and body_lines[-1] == "":
        body_lines.pop()

    body = "\n\n".join(
        part.strip()
        for part in "\n".join(body_lines).split("\n\n")
        if part.strip()
    )

    return {
        "number": item["number"],
        "title": title,
        "score": item["score"],
        "body": body,
    }


# ============================================================
# 判断语言
# ============================================================

def detect_language(text: str, fallback: str = "en") -> str:
    """
    简单语言判断。

    中文字符达到一定比例 -> zh
    否则 -> en
    """

    text = clean_text(text)

    if not text:
        return fallback

    chinese = len(
        re.findall(r"[\u4e00-\u9fff]", text)
    )

    letters = len(
        re.findall(r"[A-Za-z]", text)
    )

    if chinese >= 3 and chinese >= letters * 0.05:
        return "zh"

    return fallback


# ============================================================
# 生成 Markdown
# ============================================================

def build_markdown(
    item: dict,
    date: str,
    language: str,
) -> str:

    title = clean_text(item["title"])
    body = clean_text(item["body"])

    score = item["score"]

    score_text = (
        str(score)
        if score is not None
        else "null"
    )

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date}",
        "type: \"原子新闻\"",
        'source: "Horizon"',
        f"language: {language}",
        f"horizon_score: {score_text}",
        'status: "待AI处理"',
        "---",
        "",
        f"# {title}",
        "",
    ]

    if score is not None:
        lines.extend(
            [
                f"> Horizon 评分：{score}/10",
                "",
            ]
        )

    lines.extend(
        [
            "## Horizon 摘要",
            "",
        ]
    )

    if body:
        lines.append(body)
    else:
        lines.append("暂无正文摘要。")

    lines.extend(
        [
            "",
            "## AI 二次处理",
            "",
            "待 27 Skills 处理。",
            "",
            "## 知识关联",
            "",
            "待 AI 建立。",
            "",
            "## 最终分类",
            "",
            "待 AI 分类。",
            "",
        ]
    )

    return "\n".join(lines)


# ============================================================
# 主拆解逻辑
# ============================================================

def split_digest(
    input_file: Path,
    output_dir: Path,
    date: str,
) -> int:

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    text = input_file.read_text(
        encoding="utf-8",
        errors="replace",
    )

    text = clean_text(text)

    lines = text.splitlines()

    print(
        f"Input lines: {len(lines)}"
    )

    items = parse_items(lines)

    if not items:
        raise RuntimeError(
            "没有识别到 Horizon 新闻条目。"
            "请检查日报格式。"
        )

    print(
        f"Detected items: {len(items)}"
    )

    # --------------------------------------------------------
    # 清理条目
    # --------------------------------------------------------

    cleaned_items = []

    for item in items:
        item = clean_item(item)

        if not item["title"]:
            continue

        cleaned_items.append(item)

    if not cleaned_items:
        raise RuntimeError(
            "识别到了条目，但清理后没有有效新闻。"
        )

    # --------------------------------------------------------
    # 创建目录
    # --------------------------------------------------------

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    zh_dir = output_dir / "zh"
    en_dir = output_dir / "en"

    zh_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    en_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # 判断输入语言
    # --------------------------------------------------------

    input_language = detect_language(
        text,
        fallback="en",
    )

    print(
        f"Detected digest language: {input_language}"
    )

    # --------------------------------------------------------
    # 生成文件
    # --------------------------------------------------------

    generated = 0

    for index, item in enumerate(
        cleaned_items,
        start=1,
    ):

        sample_text = (
            item["title"]
            + "\n"
            + item["body"][:1000]
        )

        language = detect_language(
            sample_text,
            fallback=input_language,
        )

        # 当前日报是中文 / 英文，则优先按照日报语言。
        if input_language in {"zh", "en"}:
            language = input_language

        target_dir = (
            zh_dir
            if language == "zh"
            else en_dir
        )

        filename = safe_filename(
            item["title"],
            index,
        )

        output_file = target_dir / filename

        markdown = build_markdown(
            item=item,
            date=date,
            language=language,
        )

        output_file.write_text(
            markdown,
            encoding="utf-8",
        )

        generated += 1

        print(
            f"[{generated:03d}] "
            f"{language.upper()} "
            f"{item['title']}"
        )

    print()
    print("=" * 70)
    print("Horizon Digest Splitter V5")
    print("=" * 70)
    print(f"Generated: {generated}")
    print(f"Output   : {output_dir}")
    print("=" * 70)

    return generated


# ============================================================
# CLI
# ============================================================

def main() -> None:

    parser = argparse.ArgumentParser(
        description="Horizon Digest Splitter V5"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Horizon summary Markdown",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Atomic News output directory",
    )

    parser.add_argument(
        "--date",
        required=True,
        help="Date YYYY-MM-DD",
    )

    args = parser.parse_args()

    input_file = Path(args.input)
    output_dir = Path(args.output)

    print("=" * 70)
    print("Horizon Digest Splitter V5")
    print("=" * 70)
    print(f"Input : {input_file}")
    print(f"Output: {output_dir}")
    print(f"Date  : {args.date}")
    print()

    try:
        count = split_digest(
            input_file=input_file,
            output_dir=output_dir,
            date=args.date,
        )

        if count <= 0:
            raise RuntimeError(
                "没有生成任何原子新闻。"
            )

    except Exception as exc:
        print(
            f"ERROR: {exc}",
            file=sys.stderr,
        )
        raise


if __name__ == "__main__":
    main()
