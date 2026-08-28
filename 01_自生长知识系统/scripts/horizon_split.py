#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Horizon Digest -> Atomic News Splitter

功能：
1. 读取 Horizon 中文/英文日报
2. 自动识别编号新闻
3. 每条新闻生成一个独立 Markdown
4. 自动生成标准 YAML Front Matter
5. 输出到指定 Atomic 目录
6. 不依赖 Horizon 固定的“从 X 条内容中筛选出 Y 条”文字
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def clean_text(text: str) -> str:
    """清理 Horizon 导出过程中常见的 HTML/XML 转义。"""

    replacements = {
        "&#x27;": "'",
        "&#39;": "'",
        "&apos;": "'",
        "&quot;": '"',
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        "[&-x27;": "'",
        "[&-×27;": "'",
        "&-x27;": "'",
        "&-×27;": "'",
        "&#×27;": "'",
        "&#×2": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # 清理连续空格
    text = re.sub(r"[ \t]+", " ", text)

    # 清理过多空行
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def yaml_escape(value: str) -> str:
    """安全生成 YAML 双引号字符串。"""

    value = clean_text(value)
    value = value.replace("\\", "\\\\")
    value = value.replace('"', '\\"')
    value = value.replace("\n", " ")

    return f'"{value}"'


def detect_language(text: str) -> str:
    """判断日报语言。"""

    zh_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    en_count = len(re.findall(r"[A-Za-z]", text))

    if zh_count >= en_count:
        return "zh"

    return "en"


def extract_score(text: str) -> str | None:
    """尝试从标题附近提取 Horizon 分数。"""

    patterns = [
        r"(\d+(?:\.\d+)?)\s*/\s*10",
        r"评分[：:\s]*(\d+(?:\.\d+)?)",
        r"score[：:\s]*(\d+(?:\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1)

    return None


def is_numbered_item(line: str) -> bool:
    """
    判断是不是 Horizon 编号新闻。

    支持：

    1. 标题
    2. 标题
    10. 标题
    01. 标题
    """

    return bool(
        re.match(
            r"^\s*\d{1,3}\s*[\.\、]\s*\S+",
            line
        )
    )


def parse_numbered_items(lines: list[str]) -> list[dict]:
    """提取编号新闻。"""

    items = []

    current = None

    for raw_line in lines:

        line = clean_text(raw_line)

        if not line:
            if current:
                current["lines"].append("")
            continue

        match = re.match(
            r"^\s*(\d{1,3})\s*[\.\、]\s*(.+?)\s*$",
            line
        )

        if match:

            if current:
                items.append(current)

            number = int(match.group(1))
            title = match.group(2).strip()

            current = {
                "number": number,
                "title": title,
                "lines": []
            }

            continue

        if current:
            current["lines"].append(line)

    if current:
        items.append(current)

    return items


def remove_digest_noise(lines: list[str]) -> list[str]:
    """
    去掉日报中明显不是正文新闻的内容。
    """

    result = []

    noise_patterns = [
        r"^Horizon Summary",
        r"^Horizon 摘要",
        r"^日报",
        r"^科技新闻$",
        r"^AI 创作者雷达$",
        r"^AI Creator Radar$",
        r"^从 .* 条内容中筛选",
        r"^Fetched .* items",
        r"^Analyzing content",
    ]

    for line in lines:

        cleaned = clean_text(line)

        if not cleaned:
            result.append("")
            continue

        skip = False

        for pattern in noise_patterns:
            if re.search(pattern, cleaned, re.IGNORECASE):
                skip = True
                break

        if not skip:
            result.append(cleaned)

    return result


def safe_filename(title: str, number: int) -> str:
    """生成安全文件名。"""

    title = clean_text(title)

    # 去掉 Markdown / Horizon 常见符号
    title = re.sub(r"[#*_`]", "", title)

    # 替换 Windows / Linux 不适合的字符
    title = re.sub(
        r'[\\/:*?"<>|]',
        "-",
        title
    )

    # 压缩空格
    title = re.sub(r"\s+", " ", title).strip()

    # 避免文件名过长
    title = title[:100]

    if not title:
        title = "Untitled"

    return f"{number:02d}-{title}.md"


def build_atomic_markdown(
    item: dict,
    date: str,
    language: str,
    source_digest: str
) -> str:

    title = clean_text(item["title"])

    body_lines = [
        clean_text(x)
        for x in item["lines"]
        if clean_text(x)
    ]

    body = "\n\n".join(body_lines)

    score = extract_score(
        title + "\n" + body
    )

    frontmatter = [
        "---",
        f"title: {yaml_escape(title)}",
        f"date: {date}",
        'type: "原子新闻"',
        'source: "Horizon"',
        f"language: {yaml_escape(language)}",
    ]

    if score is None:
        frontmatter.append("horizon_score: null")
    else:
        frontmatter.append(
            f"horizon_score: {score}"
        )

    frontmatter.extend([
        'status: "待AI处理"',
        f"source_digest: {yaml_escape(source_digest)}",
        "---",
        "",
    ])

    content = "\n".join(frontmatter)

    content += f"# {title}\n\n"

    if score:
        content += f"**Horizon 评分：{score}/10**\n\n"

    if body:
        content += "## Horizon 摘要\n\n"
        content += body
        content += "\n\n"

    content += "## AI 二次处理\n\n"
    content += "待 27 Skills 处理。\n\n"

    content += "## 知识关联\n\n"
    content += "待 AI 建立。\n\n"

    content += "## 最终分类\n\n"
    content += "待 AI 分类。\n"

    return content


def split_digest(
    input_file: Path,
    output_dir: Path,
    date: str
) -> int:

    print("=" * 70)
    print("Horizon Digest Splitter")
    print("=" * 70)

    print(f"Input : {input_file}")
    print(f"Output: {output_dir}")
    print(f"Date  : {date}")
    print()

    if not input_file.exists():
        raise FileNotFoundError(
            f"找不到输入日报：{input_file}"
        )

    text = input_file.read_text(
        encoding="utf-8",
        errors="replace"
    )

    text = clean_text(text)

    lines = text.splitlines()

    language = detect_language(text)

    print(f"Detected language: {language}")

    # ---------------------------------------------------------
    # 第一步：尝试找正文编号新闻
    # ---------------------------------------------------------

    lines = remove_digest_noise(lines)

    items = parse_numbered_items(lines)

    print(f"Detected numbered items: {len(items)}")

    # ---------------------------------------------------------
    # 第二步：过滤明显不是新闻的项目
    # ---------------------------------------------------------

    filtered = []

    for item in items:

        title = clean_text(item["title"])

        if len(title) < 4:
            continue

        # 排除纯评分
        if re.fullmatch(
            r"\d+(?:\.\d+)?\s*/\s*10",
            title
        ):
            continue

        filtered.append(item)

    items = filtered

    print(f"Valid atomic items: {len(items)}")

    if not items:
        raise RuntimeError(
            "没有识别到任何编号新闻。"
            "请检查 Horizon 日报格式。"
        )

    # ---------------------------------------------------------
    # 创建输出目录
    # ---------------------------------------------------------

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ---------------------------------------------------------
    # 防止重复运行造成旧文件残留
    # ---------------------------------------------------------

    for old_file in output_dir.glob("*.md"):

        try:
            old_file.unlink()
        except Exception:
            pass

    # ---------------------------------------------------------
    # 生成 Atomic News
    # ---------------------------------------------------------

    generated = 0

    source_digest = input_file.name

    for item in items:

        number = item["number"]
        title = clean_text(item["title"])

        filename = safe_filename(
            title,
            number
        )

        target = output_dir / filename

        markdown = build_atomic_markdown(
            item=item,
            date=date,
            language=language,
            source_digest=source_digest
        )

        target.write_text(
            markdown,
            encoding="utf-8"
        )

        generated += 1

        print(
            f"[{generated:03d}] {target.name}"
        )

    # ---------------------------------------------------------
    # 生成索引
    # ---------------------------------------------------------

    index = [
        "---",
        f"title: {date} Horizon Atomic News Index",
        f"date: {date}",
        'type: "原子新闻索引"',
        'source: "Horizon"',
        "---",
        "",
        f"# {date} Horizon Atomic News",
        "",
        f"共生成 **{generated}** 条原子新闻。",
        "",
    ]

    for item in items:

        title = clean_text(item["title"])

        filename = safe_filename(
            title,
            item["number"]
        )

        index.append(
            f"- [[{filename[:-3]}]]"
        )

    index.append("")

    (output_dir / "_index.md").write_text(
        "\n".join(index),
        encoding="utf-8"
    )

    print()
    print("=" * 70)
    print("✅ Horizon Digest Split COMPLETE")
    print("=" * 70)
    print(f"Generated: {generated}")
    print(f"Directory: {output_dir}")

    return generated


def main():

    parser = argparse.ArgumentParser(
        description="Split Horizon digest into atomic news"
    )

    parser.add_argument(
        "--input",
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

    count = split_digest(
        input_file=Path(args.input),
        output_dir=Path(args.output),
        date=args.date
    )

    if count <= 0:
        raise RuntimeError(
            "没有生成任何 Atomic News。"
        )


if __name__ == "__main__":
    main()
