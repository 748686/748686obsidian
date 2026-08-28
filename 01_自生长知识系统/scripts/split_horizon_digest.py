from pathlib import Path
import re
from datetime import datetime


# ============================================================
# Horizon 日报 → 原子新闻拆解器
#
# 输入：
# 01_自生长知识系统/Raw News/YYYY-MM-DD/
#     YYYY-MM-DD-summary-zh.md
#
# 输出：
# 01_自生长知识系统/Raw News/YYYY-MM-DD_原子新闻/
#     001-新闻标题.md
#     002-新闻标题.md
#     ...
#
# 注意：
# 这里只负责拆解 Horizon 已经生成的日报。
# 不调用 AI。
# 不修改 Horizon。
# ============================================================


BASE_DIR = Path("01_自生长知识系统")
RAW_DIR = BASE_DIR / "Raw News"


def get_today():
    """
    GitHub Actions 使用 UTC 日期。
    """
    return datetime.utcnow().strftime("%Y-%m-%d")


def find_latest_raw_directory():
    """
    找到 Raw News 中最新的日期目录。
    """
    if not RAW_DIR.exists():
        raise FileNotFoundError(
            f"找不到 Raw News 目录：{RAW_DIR}"
        )

    date_dirs = []

    for item in RAW_DIR.iterdir():
        if not item.is_dir():
            continue

        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", item.name):
            date_dirs.append(item)

    if not date_dirs:
        raise FileNotFoundError(
            "Raw News 中没有找到 YYYY-MM-DD 日期目录。"
        )

    return sorted(date_dirs)[-1]


def find_chinese_digest(date_dir):
    """
    找当天的中文 Horizon 日报。
    """
    files = list(date_dir.glob("*summary-zh.md"))

    if not files:
        raise FileNotFoundError(
            f"{date_dir} 中没有找到中文 Horizon 日报。"
        )

    return sorted(files)[-1]


def clean_filename(title):
    """
    清理标题，使其可以作为 Markdown 文件名。
    """
    title = re.sub(r'[\\/:*?"<>|]', "-", title)
    title = re.sub(r"\s+", " ", title)
    title = title.strip()

    # 防止文件名过长
    if len(title) > 100:
        title = title[:100].rstrip()

    return title


def extract_title(line):
    """
    从 Horizon 日报列表中提取新闻标题。

    例如：
    1. 《复杂系统如何失败》经典文章引发韧性工程过
    8.0/10

    返回：
    《复杂系统如何失败》经典文章引发韧性工程过
    """

    line = line.strip()

    match = re.match(
        r"^\d+\.\s*(.+?)\s*$",
        line
    )

    if not match:
        return None

    title = match.group(1).strip()

    if not title:
        return None

    return title


def split_digest(text):
    """
    将 Horizon 中文日报拆成若干新闻。

    Horizon 的结构通常类似：

    科技新闻

    1. 新闻标题
    8.0/10

    2. 新闻标题
    7.0/10

    科技新闻

    新闻标题
    8.0/10

    正文……

    新闻标题
    7.0/10

    正文……
    """

    lines = text.splitlines()

    # --------------------------------------------------------
    # 第一阶段：
    # 找到 Horizon 的编号新闻列表
    # --------------------------------------------------------

    candidates = []

    for i, line in enumerate(lines):

        title = extract_title(line)

        if not title:
            continue

        # 下一行通常是评分
        score = None

        if i + 1 < len(lines):
            score_match = re.search(
                r"(\d+(?:\.\d+)?)\s*/\s*10",
                lines[i + 1]
            )

            if score_match:
                score = score_match.group(1)

        candidates.append(
            {
                "title": title,
                "score": score,
                "index": i,
            }
        )

    if not candidates:
        return []

    # --------------------------------------------------------
    # 第二阶段：
    # 去重
    # --------------------------------------------------------

    unique = []

    seen = set()

    for item in candidates:

        key = re.sub(
            r"\s+",
            "",
            item["title"]
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    # --------------------------------------------------------
    # 第三阶段：
    # 对每个标题寻找正文
    #
    # Horizon 后面通常会再次出现完整标题，
    # 然后才开始真正的新闻正文。
    # --------------------------------------------------------

    articles = []

    for n, item in enumerate(unique):

        title = item["title"]
        score = item["score"]

        start_search = item["index"] + 1

        if n + 1 < len(unique):
            end_search = unique[n + 1]["index"]
        else:
            end_search = len(lines)

        section = lines[start_search:end_search]

        # 找到第二次出现的标题
        title_index = None

        normalized_title = re.sub(
            r"\s+",
            "",
            title
        )

        for j, section_line in enumerate(section):

            normalized_line = re.sub(
                r"\s+",
                "",
                section_line.strip()
            )

            if (
                normalized_title
                and normalized_title in normalized_line
                and j > 0
            ):
                title_index = j
                break

        if title_index is not None:
            body_lines = section[title_index + 1:]
        else:
            body_lines = section

        # 删除评分
        cleaned_body = []

        for line in body_lines:

            if re.fullmatch(
                r"\s*\d+(?:\.\d+)?\s*/\s*10\s*",
                line
            ):
                continue

            cleaned_body.append(line)

        body = "\n".join(cleaned_body).strip()

        # 清理连续空行
        body = re.sub(
            r"\n{3,}",
            "\n\n",
            body
        )

        articles.append(
            {
                "title": title,
                "score": score,
                "body": body,
            }
        )

    return articles


def build_atomic_markdown(article, date):
    """
    创建单条原子新闻 Markdown。
    """

    title = article["title"]
    score = article["score"] or ""

    return f"""---
title: "{title.replace('"', '\\"')}"
date: {date}
type: "原子新闻"
source: "Horizon"
horizon_score: "{score}"
status: "待AI处理"
---

# {title}

## Horizon 摘要

{article["body"]}

## AI 二次处理

> 待 27 Skills 处理

## 知识关联

> 待 AI 建立

## 最终分类

> 待 AI 分类

"""


def main():

    print("=" * 60)
    print("Horizon → 原子新闻拆解器")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. 找日期目录
    # --------------------------------------------------------

    date_dir = find_latest_raw_directory()

    date = date_dir.name

    print(f"\n📅 日期：{date}")
    print(f"📂 Raw News：{date_dir}")

    # --------------------------------------------------------
    # 2. 找中文日报
    # --------------------------------------------------------

    digest_file = find_chinese_digest(date_dir)

    print(f"📰 Horizon 中文日报：{digest_file}")

    # --------------------------------------------------------
    # 3. 读取日报
    # --------------------------------------------------------

    text = digest_file.read_text(
        encoding="utf-8"
    )

    print(f"📄 日报大小：{len(text):,} 字符")

    # --------------------------------------------------------
    # 4. 拆解
    # --------------------------------------------------------

    articles = split_digest(text)

    print(f"\n🔎 识别到：{len(articles)} 条新闻")

    if not articles:
        raise RuntimeError(
            "没有识别到新闻，请检查 Horizon 日报格式。"
        )

    # --------------------------------------------------------
    # 5. 创建原子新闻目录
    # --------------------------------------------------------

    output_dir = RAW_DIR / f"{date}_原子新闻"

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    print(f"📁 输出目录：{output_dir}")

    # --------------------------------------------------------
    # 6. 写入 Markdown
    # --------------------------------------------------------

    created = 0

    for index, article in enumerate(
        articles,
        start=1
    ):

        title = clean_filename(
            article["title"]
        )

        filename = (
            f"{index:03d}-{title}.md"
        )

        output_file = output_dir / filename

        markdown = build_atomic_markdown(
            article,
            date
        )

        output_file.write_text(
            markdown,
            encoding="utf-8"
        )

        created += 1

        print(
            f"  ✓ {index:03d} "
            f"{article['title']}"
        )

    # --------------------------------------------------------
    # 7. 完成
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("✅ 原子新闻拆解完成")
    print("=" * 60)
    print(f"日期：{date}")
    print(f"原始日报：{digest_file}")
    print(f"生成数量：{created}")
    print(f"输出目录：{output_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
