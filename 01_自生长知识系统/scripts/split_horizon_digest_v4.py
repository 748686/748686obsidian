#!/usr/bin/env python3

import argparse
import html
import re
from pathlib import Path


# ============================================================
# Horizon Digest → Atomic News V4
#
# 目标：
# 1. 从 Horizon Summary 中识别真正的精选新闻
# 2. 不把 Radar / 导读 / 其他栏目当成新闻正文
# 3. 每条新闻生成一个独立 MD
# 4. 清理 HTML entity，例如 &#x27;
# 5. 生成合法 YAML Front Matter
# ============================================================


def clean_text(text: str) -> str:
    """清理 Horizon/HTML 中常见的编码问题。"""

    if not text:
        return ""

    text = html.unescape(text)

    # 处理一些异常编码
    text = text.replace("&#×27;", "'")
    text = text.replace("&×27;", "'")
    text = text.replace("&-x27;", "'")
    text = text.replace("&-×27;", "'")
    text = text.replace("\\&", "&")

    # 再次处理可能嵌套的 HTML entity
    text = html.unescape(text)

    # 全角引号转换
    text = text.replace("＂", '"')
    text = text.replace("＇", "'")

    # 清理多余空白
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def yaml_quote(text: str) -> str:
    """安全生成 YAML 双引号字符串。"""

    text = clean_text(text)
    text = text.replace("\\", "\\\\")
    text = text.replace('"', '\\"')
    return f'"{text}"'


def normalize_for_match(text: str) -> str:
    """用于标题匹配的标准化文本。"""

    text = clean_text(text)

    text = text.lower()

    # 去 Markdown / HTML 噪音
    text = re.sub(r"[*_`>#]", "", text)

    # 去掉 Horizon 可能附加的 item ID
    text = re.sub(r"$begin:math:text$\#item\-\[\^\)\]\+$end:math:text$", "", text)

    # 去掉评分
    text = re.sub(r"\s*[—–-]?\s*\d+(?:\.\d+)?\s*/\s*10\s*$", "", text)

    # 中文标点和英文标点统一成空格
    text = re.sub(r"[“”‘’\"'「」『』《》〈〉]", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def slugify(text: str, max_len: int = 90) -> str:
    """生成安全的 Markdown 文件名。"""

    text = clean_text(text)

    # 去掉 Windows / GitHub 文件名危险字符
    text = re.sub(r'[\\/:*?"<>|]', "-", text)

    # 去掉 Markdown / Horizon item 标记
    text = re.sub(r"$begin:math:text$\#item\-\[\^\)\]\+$end:math:text$", "", text)

    # 连续空格
    text = re.sub(r"\s+", " ", text).strip()

    # 不让文件名太长
    if len(text) > max_len:
        text = text[:max_len].rstrip()

    return text


def extract_score(line: str):
    """从一行中提取 x/10。"""

    match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*10", line)

    if not match:
        return None

    return float(match.group(1))


def find_summary_block(text: str):
    """
    找到类似：

    从 26 条内容中筛选出11 条重要资讯。

    1. xxx
    8.0/10
    2. xxx
    7.0/10

    的区域。
    """

    lines = text.splitlines()

    start = None

    for i, line in enumerate(lines):
        if re.search(
            r"从\s*\d+\s*条内容中筛选出\s*\d+\s*条重要资讯",
            clean_text(line),
        ):
            start = i
            break

    if start is None:
        return None, None

    # 从这里往后找真正详细正文开始的位置。
    #
    # Horizon 常见结构：
    #
    # 1. 新闻标题
    # 8.0/10
    # 2. 新闻标题
    # 7.0/10
    #
    # 后面再次出现：
    #
    # 科技新闻
    #
    # 新闻标题
    # 8.0/10
    #
    # Hacker News 用户……

    return lines, start


def extract_selected_items(lines, start):
    """
    提取 Horizon 顶部精选列表。

    返回：

    [
        {
            "index": 1,
            "title": "...",
            "score": 8.0
        }
    ]
    """

    items = []

    i = start + 1

    current = None

    while i < len(lines):

        raw = lines[i]
        line = clean_text(raw)

        if not line:
            i += 1
            continue

        # 匹配：
        # 1. 标题
        # 2. 标题
        # 10. 标题
        m = re.match(r"^(\d+)[\.\、]\s*(.+?)\s*$", line)

        if m:
            number = int(m.group(1))
            title = clean_text(m.group(2))

            # 避免把普通正文里的数字列表继续识别进去
            if number >= 1:
                current = {
                    "index": number,
                    "title": title,
                    "score": None,
                }

                items.append(current)

            i += 1
            continue

        # 紧跟标题的评分
        score = extract_score(line)

        if score is not None and current is not None:
            current["score"] = score
            i += 1
            continue

        # 一旦进入明显的详细正文区域，并且已经有足够的精选项目，
        # 就停止继续扫描。
        if current is not None and items:
            # 出现明显章节标题
            if (
                line in {
                    "科技新闻",
                    "财经新闻",
                    "国际新闻",
                    "AI 创作者雷达",
                    "AI创作者雷达",
                    "Horizon 摘要",
                }
            ):
                break

        i += 1

    # 只保留确实拿到评分的项目
    result = [
        item
        for item in items
        if item["title"] and item["score"] is not None
    ]

    return result


def find_detail_start(lines, item, summary_start):
    """
    找到某条精选新闻在正文中的第二次出现。

    第一次通常出现在顶部精选列表。
    第二次才是完整正文。
    """

    target = normalize_for_match(item["title"])

    if not target:
        return None

    occurrences = []

    for i, line in enumerate(lines):
        normalized = normalize_for_match(line)

        if not normalized:
            continue

        # 完整标题
        if normalized == target:
            occurrences.append(i)
            continue

        # 某些 Horizon 标题会因为换行导致文本不完全一致
        if len(target) >= 20:
            if target in normalized or normalized in target:
                occurrences.append(i)

    # 找 summary 区域之后的标题。
    # 第一处往往是顶部精选列表。
    candidates = [x for x in occurrences if x > summary_start + 3]

    if not candidates:
        return None

    # 优先寻找第二次出现
    if len(candidates) >= 2:
        return candidates[1]

    return candidates[0]


def is_noise_line(line: str) -> bool:
    """判断是否为 Horizon 页面噪音。"""

    text = clean_text(line)

    if not text:
        return True

    noise_exact = {
        "Horizon 摘要",
        "AI 创作者雷达",
        "AI创作者雷达",
        "科技新闻",
        "财经新闻",
        "国际新闻",
        "参考链接",
        "核心观点",
        "结论",
    }

    if text in noise_exact:
        return True

    return False


def clean_article_body(body_lines):
    """
    清理单条新闻正文。

    特别避免：
    - AI 创作者雷达
    - 顶部精选列表
    - 下一条新闻
    """

    cleaned = []

    for line in body_lines:
        line = clean_text(line)

        if not line:
            if cleaned and cleaned[-1] != "":
                cleaned.append("")
            continue

        if is_noise_line(line):
            continue

        cleaned.append(line)

    # 删除尾部空行
    while cleaned and cleaned[-1] == "":
        cleaned.pop()

    return cleaned


def detect_language(text: str) -> str:
    """粗略判断中文/英文。"""

    chinese = len(re.findall(r"[\u4e00-\u9fff]", text))
    english = len(re.findall(r"[A-Za-z]", text))

    if chinese >= english:
        return "zh"

    return "en"


def build_markdown(item, body_lines, date):
    """生成最终 Atomic Markdown。"""

    title = clean_text(item["title"])

    body = "\n".join(body_lines).strip()

    language = detect_language(title + "\n" + body)

    score = item["score"]

    front_matter = f"""---
title: {yaml_quote(title)}
date: {date}
type: "原子新闻"
source: "Horizon"
language: "{language}"
horizon_score: {score}
status: "待AI处理"
---

# {title}

## Horizon 摘要

{body}

---

## AI 二次处理

待 27 Skills 处理

## 知识关联

待 AI 建立

## 最终分类

待 AI 分类
"""

    return front_matter


def split_digest(input_file: Path, output_dir: Path, date: str):

    print("=" * 70)
    print("Horizon Digest Splitter V4")
    print("=" * 70)

    print(f"Input : {input_file}")
    print(f"Output: {output_dir}")
    print(f"Date  : {date}")
    print()

    text = input_file.read_text(encoding="utf-8")

    # 清理全文 HTML entity
    text = html.unescape(text)

    lines, summary_start = find_summary_block(text)

    if lines is None:
        raise RuntimeError(
            "找不到 Horizon 的「从 X 条内容中筛选出 Y 条重要资讯」区域。"
        )

    print(f"Summary start line: {summary_start + 1}")

    items = extract_selected_items(lines, summary_start)

    if not items:
        raise RuntimeError(
            "没有识别出任何带评分的 Horizon 精选新闻。"
        )

    print()
    print(f"Detected {len(items)} selected articles:")
    print()

    for item in items:
        print(
            f"{item['index']:>3}. "
            f"{item['title']} "
            f"({item['score']}/10)"
        )

    print()

    output_dir.mkdir(parents=True, exist_ok=True)

    generated = 0

    # 为了确定正文范围：
    # 找到所有精选新闻正文的起点
    detail_positions = []

    for item in items:
        pos = find_detail_start(
            lines,
            item,
            summary_start,
        )

        if pos is not None:
            detail_positions.append(
                (pos, item)
            )

    detail_positions.sort(key=lambda x: x[0])

    print("Detected detail sections:")
    for pos, item in detail_positions:
        print(
            f"  line {pos + 1}: "
            f"{item['title']}"
        )

    print()

    if not detail_positions:
        raise RuntimeError(
            "找不到任何精选新闻对应的详细正文。"
        )

    for idx, (start_pos, item) in enumerate(detail_positions):

        # 下一篇正文开始的位置
        if idx + 1 < len(detail_positions):
            end_pos = detail_positions[idx + 1][0]
        else:
            end_pos = len(lines)

        raw_body = lines[start_pos + 1:end_pos]

        body = clean_article_body(raw_body)

        # 防止正文把顶部其他列表/内容吞进去
        if not body:
            body = [
                "Horizon 已识别该条新闻，但暂未提取到详细正文。"
            ]

        markdown = build_markdown(
            item,
            body,
            date,
        )

        filename = (
            f"{item['index']:03d}-"
            f"{slugify(item['title'])}.md"
        )

        output_file = output_dir / filename

        output_file.write_text(
            markdown,
            encoding="utf-8",
        )

        generated += 1

        print(
            f"✓ {output_file.name}"
        )

    print()
    print("=" * 70)
    print(f"Detected : {len(items)}")
    print(f"Generated: {generated}")
    print("=" * 70)

    if generated == 0:
        raise RuntimeError(
            "V4 没有生成任何 Atomic News 文件。"
        )

    print()
    print("✅ Horizon Digest Split V4 COMPLETE")


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
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

    split_digest(
        Path(args.input),
        Path(args.output),
        args.date,
    )


if __name__ == "__main__":
    main()
