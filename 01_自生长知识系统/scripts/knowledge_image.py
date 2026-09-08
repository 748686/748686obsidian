#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Generator
======================================================================

用途
----------------------------------------------------------------------
为已经生成完成的：

    05_日报
    06_周报

自动生成配套图片，并将图片引用写回 Markdown。

核心规则
----------------------------------------------------------------------
1. 日报最多 4 张图片
2. 周报最多 4 张图片
3. 第一张必须是封面图
4. 其余 2~3 张为内容图
5. 图片根据对应 Markdown 实际内容生成
6. 使用 AGNES Image API
7. 模型固定：

       agnes-image-2.5-flash

8. 图片规格固定：

       size  = 2K
       ratio = 16:9

9. response_format 必须放在：

       extra_body.response_format

10. 图片 API 返回 URL 后，下载到本地 PNG
11. 所有图片成功生成并下载后，才修改 Markdown
12. 使用 _IMAGE_COMPLETE 防止重复生成
13. 不成功不创建 _IMAGE_COMPLETE
14. 不删除原 Markdown
15. 不覆盖已经存在的图片
16. 可重复运行
17. 只处理已经存在的日报/周报
18. 不负责日报、周报内容本身的生成

环境变量
----------------------------------------------------------------------
必须：

    AGNES_API_KEY

可选：

    AGNES_BASE_URL

默认：

    https://api.agnes-ai.cn/v1

使用方式
----------------------------------------------------------------------
python knowledge_image.py

也可以指定日期：

    python knowledge_image.py 2026-09-08

也可以处理三个日期：

    python knowledge_image.py 2026-09-06 2026-09-07 2026-09-08
"""

from __future__ import annotations

import os
import re
import sys
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# 基础配置
# ======================================================================

ROOT = Path("01_自生长知识系统")

DAILY_ROOT = ROOT / "05_日报"
WEEKLY_ROOT = ROOT / "06_周报"

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1"
).rstrip("/")

AGNES_API_KEY = os.getenv("AGNES_API_KEY", "").strip()

IMAGE_MODEL = "agnes-image-2.5-flash"

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

MAX_IMAGES_PER_REPORT = 4

IMAGE_DIR_NAME = "images"
IMAGE_COMPLETE_MARKER = "_IMAGE_COMPLETE"

REQUEST_TIMEOUT = 180

# 防止连续图片请求过于集中
IMAGE_REQUEST_INTERVAL = 2.0


# ======================================================================
# 工具函数
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


def fail(message: str) -> None:
    log("")
    log("=" * 70)
    log("❌ KNOWLEDGE IMAGE FAILED")
    log(message)
    log("=" * 70)
    raise RuntimeError(message)


def ensure_api_key() -> None:
    if not AGNES_API_KEY:
        fail(
            "环境变量 AGNES_API_KEY 未配置。\n"
            "请在 GitHub Actions 中使用 secrets.AGnes API Key。"
        )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def safe_filename(text: str) -> str:
    """
    将标题转换成适合作为文件名的形式。
    """

    text = text.strip()

    text = re.sub(
        r'[\\/:*?"<>|]+',
        "_",
        text
    )

    text = re.sub(
        r"\s+",
        "_",
        text
    )

    return text[:80] or "image"


def extract_title(markdown: str, fallback: str) -> str:
    """
    获取 Markdown 第一层标题。
    """

    match = re.search(
        r"(?m)^#\s+(.+?)\s*$",
        markdown
    )

    if match:
        return match.group(1).strip()

    return fallback


def strip_existing_image_lines(markdown: str) -> str:
    """
    删除之前由本脚本插入的 Markdown 图片引用。

    只删除：
        ![日报首图](images/xxx.png)
        ![重点主题](images/xxx.png)

    不碰其它 Markdown 图片。
    """

    pattern = re.compile(
        r"(?m)^\s*!\[[^\]]*\]\(images/[^)\n]+\)\s*\n?"
    )

    return pattern.sub("", markdown)


def truncate_for_prompt(text: str, limit: int = 18000) -> str:
    """
    防止超长 Markdown 直接进入图片 Prompt。
    """

    text = text.strip()

    if len(text) <= limit:
        return text

    return text[:limit] + "\n\n[后续内容省略]"


# ======================================================================
# 报告发现
# ======================================================================

def find_daily_reports(dates: list[str]) -> list[Path]:
    """
    查找指定日期的日报。

    兼容当前目录结构：

        05_日报/YYYY/MM/YYYY-MM-DD.md
    """

    reports: list[Path] = []

    for date in dates:

        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
            continue

        year = date[:4]
        month = date[5:7]

        path = DAILY_ROOT / year / month / f"{date}.md"

        if path.is_file():
            reports.append(path)
            continue

        # 备用搜索，防止目录结构未来稍有变化
        candidates = list(
            DAILY_ROOT.rglob(f"{date}.md")
        )

        if candidates:
            reports.append(candidates[0])

    return unique_paths(reports)


def find_weekly_reports(dates: list[str]) -> list[Path]:
    """
    根据日报日期所在周，寻找对应周报。

    当前周报结构兼容：

        06_周报/YYYY/Wxx/Wxx.md

    同时也会进行递归搜索。
    """

    reports: list[Path] = []

    for date in dates:

        try:
            year, month, day = map(int, date.split("-"))
            import datetime

            dt = datetime.date(year, month, day)
            iso = dt.isocalendar()

            iso_year = iso.year
            week = iso.week

            week_name = f"W{week:02d}"

            candidates = [
                WEEKLY_ROOT
                / str(iso_year)
                / week_name
                / f"{week_name}.md",

                WEEKLY_ROOT
                / str(iso_year)
                / week_name
                / f"{week_name}.MD",
            ]

            found = False

            for path in candidates:
                if path.is_file():
                    reports.append(path)
                    found = True
                    break

            if found:
                continue

            recursive = list(
                WEEKLY_ROOT.rglob(f"{week_name}.md")
            )

            if recursive:
                reports.append(recursive[0])

        except Exception as exc:
            log(
                f"⚠️ 无法根据日期 {date} 查找周报：{exc}"
            )

    return unique_paths(reports)


def unique_paths(paths: list[Path]) -> list[Path]:

    result: list[Path] = []
    seen: set[str] = set()

    for path in paths:

        key = str(path.resolve())

        if key in seen:
            continue

        seen.add(key)
        result.append(path)

    return result


# ======================================================================
# 图片数量判断
# ======================================================================

def determine_image_count(markdown: str) -> int:
    """
    根据报告内容决定生成 2~4 张。

    规则：

    内容很短：
        2 张

    正常报告：
        3 张

    内容丰富：
        4 张

    第一张永远是封面。
    """

    text_length = len(markdown)

    headings = re.findall(
        r"(?m)^#{2,4}\s+.+$",
        markdown
    )

    heading_count = len(headings)

    if text_length < 5000 and heading_count < 4:
        return 2

    if text_length < 12000 and heading_count < 8:
        return 3

    return 4


# ======================================================================
# 内容主题提取
# ======================================================================

def extract_sections(markdown: str) -> list[tuple[str, str]]:
    """
    从 Markdown 中提取主要章节。

    返回：

        [
            ("AI 与科技", "..."),
            ("国际与经济", "..."),
        ]
    """

    pattern = re.compile(
        r"(?ms)^#{2,4}\s+(.+?)\s*$"
        r"(.*?)(?=^#{2,4}\s+|\Z)"
    )

    sections = []

    for match in pattern.finditer(markdown):

        title = match.group(1).strip()
        content = match.group(2).strip()

        if not content:
            continue

        sections.append(
            (
                title,
                content[:5000]
            )
        )

    return sections


def choose_content_sections(
    markdown: str,
    count: int
) -> list[tuple[str, str]]:
    """
    选择最适合生成图片的章节。

    count 包含封面。

    例如：

        count = 4

    则最多选择 3 个内容主题。
    """

    wanted = max(0, count - 1)

    sections = extract_sections(markdown)

    if not sections:
        return []

    # 优先选择内容较丰富的章节
    sections.sort(
        key=lambda item: len(item[1]),
        reverse=True
    )

    return sections[:wanted]


# ======================================================================
# Prompt 生成
# ======================================================================

def build_cover_prompt(
    report_type: str,
    report_title: str,
    markdown: str
) -> str:

    content = truncate_for_prompt(
        markdown,
        12000
    )

    return f"""
Create a premium editorial cover image for a knowledge report.

Report type:
{report_type}

Report title:
{report_title}

The image must visually represent the real themes of this report.

Report content:
{content}

Visual requirements:

- cinematic editorial illustration
- sophisticated professional knowledge-report aesthetic
- realistic but slightly conceptual
- strong visual hierarchy
- clean composition
- high information density without clutter
- suitable as a report cover
- no readable text
- no logos
- no watermark
- no UI screenshot
- no fake charts
- no random unrelated objects
- 16:9 landscape composition
- polished magazine-quality visual
""".strip()


def build_content_prompt(
    report_type: str,
    report_title: str,
    section_title: str,
    section_content: str
) -> str:

    content = truncate_for_prompt(
        section_content,
        7000
    )

    return f"""
Create a premium editorial illustration for one section of a knowledge report.

Report type:
{report_type}

Report title:
{report_title}

Section:
{section_title}

Section content:
{content}

Visual requirements:

- directly visualize the actual meaning of the section
- cinematic editorial illustration
- sophisticated professional style
- realistic and conceptually clear
- strong composition
- visually memorable
- suitable for a high-quality knowledge report
- no readable text
- no logos
- no watermark
- no UI screenshot
- no random decorative objects
- 16:9 landscape composition
""".strip()


# ======================================================================
# AGNES 图片 API
# ======================================================================

def call_image_api(prompt: str) -> str:
    """
    调用：

        POST /v1/images/generations

    使用：

        model = agnes-image-2.5-flash
        size  = 2K
        ratio = 16:9

    注意：

        response_format 必须放在 extra_body。
    """

    url = (
        f"{AGNES_BASE_URL}"
        "/images/generations"
    )

    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
        "size": IMAGE_SIZE,
        "ratio": IMAGE_RATIO,
        "extra_body": {
            "response_format": "url"
        }
    }

    data = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    request = Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": (
                f"Bearer {AGNES_API_KEY}"
            ),
            "Content-Type": "application/json",
        },
    )

    last_error = None

    for attempt in range(1, 4):

        try:

            log(
                f"    🎨 图片 API 请求 "
                f"(第 {attempt}/3 次)"
            )

            with urlopen(
                request,
                timeout=REQUEST_TIMEOUT
            ) as response:

                raw = response.read()

            result = json.loads(
                raw.decode("utf-8")
            )

            image_url = (
                result
                .get("data", [{}])[0]
                .get("url")
            )

            if not image_url:
                raise RuntimeError(
                    "AGNES 图片 API 没有返回 data[0].url"
                )

            return image_url

        except HTTPError as exc:

            body = ""

            try:
                body = exc.read().decode(
                    "utf-8",
                    errors="replace"
                )
            except Exception:
                pass

            last_error = (
                f"HTTP {exc.code}: {body[:2000]}"
            )

            log(
                f"    ⚠️ 图片 API 错误："
                f"{last_error}"
            )

        except URLError as exc:

            last_error = (
                f"网络错误：{exc}"
            )

            log(
                f"    ⚠️ {last_error}"
            )

        except Exception as exc:

            last_error = str(exc)

            log(
                f"    ⚠️ {last_error}"
            )

        if attempt < 3:

            wait_seconds = attempt * 5

            log(
                f"    ⏳ {wait_seconds} 秒后重试..."
            )

            time.sleep(wait_seconds)

    raise RuntimeError(
        f"AGNES 图片生成失败：{last_error}"
    )


# ======================================================================
# 图片下载
# ======================================================================

def download_image(
    image_url: str,
    output_path: Path
) -> None:

    log(
        f"    ⬇️ 下载图片：{output_path.name}"
    )

    request = Request(
        image_url,
        headers={
            "User-Agent":
                "Mozilla/5.0 "
                "748686-Knowledge-System"
        }
    )

    with urlopen(
        request,
        timeout=REQUEST_TIMEOUT
    ) as response:

        image_data = response.read()

    if not image_data:
        raise RuntimeError(
            "下载到的图片为空"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_bytes(
        image_data
    )

    # 基础文件完整性检查
    size = output_path.stat().st_size

    if size < 1024:
        raise RuntimeError(
            f"图片文件异常，大小只有 {size} bytes"
        )

    log(
        f"    ✅ 图片保存成功："
        f"{output_path} "
        f"({size:,} bytes)"
    )


# ======================================================================
# Markdown 图片引用
# ======================================================================

def build_image_markdown(
    image_filename: str,
    alt_text: str
) -> str:

    return (
        f"![{alt_text}]"
        f"(images/{image_filename})"
    )


def insert_images_into_markdown(
    markdown: str,
    image_entries: list[tuple[str, str]]
) -> str:
    """
    image_entries：

        [
            ("cover.png", "日报首图"),
            ("image-01.png", "AI 与科技"),
        ]

    插入原则：

    第一张：
        放在第一个标题之后。

    后续图片：
        尽可能插入对应章节标题之前。
    """

    # --------------------------------------------------------------
    # 先清理本脚本以前生成的图片引用
    # --------------------------------------------------------------

    cleaned = strip_existing_image_lines(
        markdown
    )

    if not image_entries:
        return cleaned

    cover_filename, cover_alt = image_entries[0]

    cover_md = build_image_markdown(
        cover_filename,
        cover_alt
    )

    # --------------------------------------------------------------
    # 封面插入第一个一级标题之后
    # --------------------------------------------------------------

    heading_match = re.search(
        r"(?m)^#\s+.+?$",
        cleaned
    )

    if heading_match:

        insert_pos = heading_match.end()

        cleaned = (
            cleaned[:insert_pos]
            + "\n\n"
            + cover_md
            + "\n"
            + cleaned[insert_pos:]
        )

    else:

        cleaned = (
            cover_md
            + "\n\n"
            + cleaned
        )

    # --------------------------------------------------------------
    # 内容图片
    # --------------------------------------------------------------

    content_entries = image_entries[1:]

    if not content_entries:
        return cleaned

    # 找所有二级及以下章节
    section_matches = list(
        re.finditer(
            r"(?m)^#{2,4}\s+(.+?)\s*$",
            cleaned
        )
    )

    if not section_matches:
        return cleaned

    # 从后往前插入，避免位置偏移
    insertions = []

    for index, (filename, alt_text) in enumerate(
        content_entries
    ):

        if index >= len(section_matches):
            break

        match = section_matches[index]

        image_md = build_image_markdown(
            filename,
            alt_text
        )

        insertions.append(
            (
                match.start(),
                "\n"
                + image_md
                + "\n"
            )
        )

    for position, text in reversed(insertions):

        cleaned = (
            cleaned[:position]
            + text
            + cleaned[position:]
        )

    return cleaned


# ======================================================================
# 完整性检查
# ======================================================================

def validate_images(
    image_dir: Path,
    filenames: list[str]
) -> bool:

    for filename in filenames:

        path = image_dir / filename

        if not path.is_file():
            log(
                f"    ❌ 图片不存在：{path}"
            )
            return False

        size = path.stat().st_size

        if size < 1024:
            log(
                f"    ❌ 图片文件异常："
                f"{path} ({size} bytes)"
            )
            return False

    return True


def validate_markdown_references(
    markdown: str,
    image_dir: Path,
    filenames: list[str]
) -> bool:

    for filename in filenames:

        reference = (
            f"images/{filename}"
        )

        if reference not in markdown:
            log(
                f"    ❌ Markdown 缺少图片引用："
                f"{reference}"
            )
            return False

        if not (
            image_dir / filename
        ).is_file():
            log(
                f"    ❌ 引用图片不存在："
                f"{image_dir / filename}"
            )
            return False

    return True


# ======================================================================
# 单份报告处理
# ======================================================================

def process_report(
    report_path: Path,
    report_type: str
) -> bool:

    log("")
    log("=" * 70)
    log(
        f"📄 {report_type}："
        f"{report_path}"
    )
    log("=" * 70)

    markdown = read_text(
        report_path
    )

    if not markdown.strip():
        log("⚠️ Markdown 为空，跳过")
        return False

    image_dir = (
        report_path.parent
        / IMAGE_DIR_NAME
    )

    marker = (
        report_path.parent
        / IMAGE_COMPLETE_MARKER
    )

    # --------------------------------------------------------------
    # 已完成
    # --------------------------------------------------------------

    if marker.is_file():

        log(
            "⏭️ 检测到 _IMAGE_COMPLETE"
        )

        log(
            "   已完成图片生成，跳过 API 请求。"
        )

        return False

    # --------------------------------------------------------------
    # 报告标题
    # --------------------------------------------------------------

    fallback_title = (
        report_path.stem
    )

    report_title = extract_title(
        markdown,
        fallback_title
    )

    # --------------------------------------------------------------
    # 图片数量
    # --------------------------------------------------------------

    image_count = determine_image_count(
        markdown
    )

    image_count = min(
        MAX_IMAGES_PER_REPORT,
        max(2, image_count)
    )

    log(
        f"🖼️ 计划生成："
        f"{image_count} 张图片"
    )

    log(
        f"   封面：1"
    )

    log(
        f"   内容图："
        f"{image_count - 1}"
    )

    # --------------------------------------------------------------
    # 选择内容章节
    # --------------------------------------------------------------

    sections = choose_content_sections(
        markdown,
        image_count
    )

    # 如果章节太少，则降低实际图片数量
    actual_count = 1 + len(sections)

    if actual_count < 2:
        log(
            "⚠️ 报告缺少足够内容章节，"
            "至少生成 1 张封面。"
        )

    # --------------------------------------------------------------
    # 准备目录
    # --------------------------------------------------------------

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    generated: list[
        tuple[str, str]
    ] = []

    downloaded_files: list[str] = []

    # --------------------------------------------------------------
    # 1. 生成封面
    # --------------------------------------------------------------

    cover_filename = (
        f"{report_path.stem}-cover.png"
    )

    cover_path = (
        image_dir
        / cover_filename
    )

    log("")
    log("🎬 生成封面图")

    cover_prompt = build_cover_prompt(
        report_type,
        report_title,
        markdown
    )

    image_url = call_image_api(
        cover_prompt
    )

    download_image(
        image_url,
        cover_path
    )

    generated.append(
        (
            cover_filename,
            f"{report_type}首图"
        )
    )

    downloaded_files.append(
        cover_filename
    )

    time.sleep(
        IMAGE_REQUEST_INTERVAL
    )

    # --------------------------------------------------------------
    # 2. 生成内容图片
    # --------------------------------------------------------------

    for index, (
        section_title,
        section_content
    ) in enumerate(
        sections,
        start=1
    ):

        filename = (
            f"{report_path.stem}"
            f"-image-{index:02d}.png"
        )

        output_path = (
            image_dir
            / filename
        )

        log("")
        log(
            f"🖼️ 生成内容图 "
            f"{index}/{len(sections)}："
            f"{section_title}"
        )

        prompt = build_content_prompt(
            report_type,
            report_title,
            section_title,
            section_content
        )

        image_url = call_image_api(
            prompt
        )

        download_image(
            image_url,
            output_path
        )

        generated.append(
            (
                filename,
                section_title
            )
        )

        downloaded_files.append(
            filename
        )

        if index < len(sections):
            time.sleep(
                IMAGE_REQUEST_INTERVAL
            )

    # --------------------------------------------------------------
    # 3. 验证所有图片
    # --------------------------------------------------------------

    log("")
    log("🔍 验证生成图片")

    if not validate_images(
        image_dir,
        downloaded_files
    ):
        fail(
            f"{report_path} 图片完整性验证失败"
        )

    log(
        "✅ 所有图片文件验证通过"
    )

    # --------------------------------------------------------------
    # 4. 生成新的 Markdown
    # --------------------------------------------------------------

    log("")
    log("📝 写入 Markdown 图片引用")

    new_markdown = insert_images_into_markdown(
        markdown,
        generated
    )

    # --------------------------------------------------------------
    # 5. 验证 Markdown
    # --------------------------------------------------------------

    if not validate_markdown_references(
        new_markdown,
        image_dir,
        downloaded_files
    ):
        fail(
            f"{report_path} Markdown 图片引用验证失败"
        )

    log(
        "✅ Markdown 图片引用验证通过"
    )

    # --------------------------------------------------------------
    # 6. 最后才覆盖原 Markdown
    # --------------------------------------------------------------

    write_text(
        report_path,
        new_markdown
    )

    log(
        f"✅ Markdown 已更新："
        f"{report_path}"
    )

    # --------------------------------------------------------------
    # 7. 最后才创建完成标记
    # --------------------------------------------------------------

    marker.write_text(
        "IMAGE_GENERATION_COMPLETE\n",
        encoding="utf-8"
    )

    log(
        f"✅ 已创建：{marker}"
    )

    log("")
    log(
        f"🎉 {report_type} 图片处理完成"
    )

    return True


# ======================================================================
# 日期参数
# ======================================================================

def get_dates_from_args() -> list[str]:
    """
    如果命令行提供日期：

        python knowledge_image.py 2026-09-06 2026-09-07

    则只处理这些日期。

    如果没有参数：

        自动使用今天 UTC 日期及前两天。
    """

    if len(sys.argv) > 1:

        dates = []

        for value in sys.argv[1:]:

            value = value.strip()

            if re.fullmatch(
                r"\d{4}-\d{2}-\d{2}",
                value
            ):
                dates.append(value)
            else:
                log(
                    f"⚠️ 忽略非法日期：{value}"
                )

        if dates:
            return dates

    import datetime

    today = datetime.datetime.now(
        datetime.timezone.utc
    ).date()

    return [
        str(today - datetime.timedelta(days=2)),
        str(today - datetime.timedelta(days=1)),
        str(today),
    ]


# ======================================================================
# 主程序
# ======================================================================

def main() -> None:

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE IMAGE GENERATOR")
    log("=" * 70)
    log(
        f"Model : {IMAGE_MODEL}"
    )
    log(
        f"Size  : {IMAGE_SIZE}"
    )
    log(
        f"Ratio : {IMAGE_RATIO}"
    )
    log(
        f"Base  : {AGNES_BASE_URL}"
    )
    log("=" * 70)

    ensure_api_key()

    dates = get_dates_from_args()

    log("")
    log(
        "📅 处理日期："
        + ", ".join(dates)
    )

    # --------------------------------------------------------------
    # 查找日报
    # --------------------------------------------------------------

    daily_reports = find_daily_reports(
        dates
    )

    # --------------------------------------------------------------
    # 查找周报
    # --------------------------------------------------------------

    weekly_reports = find_weekly_reports(
        dates
    )

    log("")
    log(
        f"📊 找到日报："
        f"{len(daily_reports)}"
    )

    for path in daily_reports:
        log(f"   • {path}")

    log("")
    log(
        f"📊 找到周报："
        f"{len(weekly_reports)}"
    )

    for path in weekly_reports:
        log(f"   • {path}")

    processed = 0
    skipped = 0

    # --------------------------------------------------------------
    # 日报
    # --------------------------------------------------------------

    for report in daily_reports:

        result = process_report(
            report,
            "知识日报"
        )

        if result:
            processed += 1
        else:
            skipped += 1

    # --------------------------------------------------------------
    # 周报
    # --------------------------------------------------------------

    for report in weekly_reports:

        result = process_report(
            report,
            "知识周报"
        )

        if result:
            processed += 1
        else:
            skipped += 1

    # --------------------------------------------------------------
    # 最终结果
    # --------------------------------------------------------------

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE IMAGE GENERATOR COMPLETE")
    log("=" * 70)
    log(
        f"处理完成：{processed}"
    )
    log(
        f"跳过：{skipped}"
    )
    log("=" * 70)


if __name__ == "__main__":
    main()
