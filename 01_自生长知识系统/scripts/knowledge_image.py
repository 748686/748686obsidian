#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Generator V4.0
======================================================================

核心目标
----------------------------------------------------------------------

为日报 / 周报生成配套图片，并生成：

    原始报告.md
    原始报告_带图.md

图片统一保存到：

    01_自生长知识系统/04_图片/

目录结构：

    04_图片/
    ├── 日报/
    │   └── YYYY-MM-DD/
    │       ├── 首图.png
    │       ├── 插图1.png
    │       ├── 插图2.png
    │       └── 插图3.png
    │
    └── 周报/
        └── YYYY-Wxx/
            ├── 首图.png
            ├── 插图1.png
            ├── 插图2.png
            └── 插图3.png


V4.0 核心视觉规则
----------------------------------------------------------------------

    ONE IMAGE
        =
    ONE SCENE
        =
    ONE VISUAL STORY

即：

    一张图片
    一个连续空间
    一个主要视觉主体
    一个明确动作 / 状态
    一个视觉中心

严禁：

    四宫格
    六宫格
    九宫格
    分屏
    多窗口
    拼图
    蒙太奇
    图片墙
    缩略图集合
    多个独立场景
    多个地点
    多个时间点
    新闻事件拼接
    信息图
    PPT
    Dashboard
    杂志拼版
    概念元素堆叠


图片要求
----------------------------------------------------------------------

    - 不出现中文文字
    - 不出现英文文字
    - 不出现可读文字
    - 不出现标题
    - 不出现字幕
    - 不出现说明文字
    - 不出现新闻标题
    - 不出现报纸版面
    - 不出现网页 UI
    - 不出现 Logo
    - 不出现水印
    - 不出现图表文字
    - 不出现信息图文字

数字：
    只有当真实场景自然需要时才允许出现。
    不主动加入数字、图表或文字。

视觉风格：

    serious
    documentary
    editorial
    cinematic
    realistic
    coherent
    premium

重要：

    不要求图片解释新闻的全部信息。

    如果一个新闻包含很多信息，
    只选择一个最有代表性的视觉故事。

    宁可少表现信息，
    也不要把多个场景塞进一张图。


API
----------------------------------------------------------------------

POST:
    https://api.agnes-ai.cn/v1/images/generations

Model:
    agnes-image-2.5-flash

size:
    2K

ratio:
    16:9

response_format 必须位于：

    extra_body.response_format

并使用：

    data[0].url


运行环境
----------------------------------------------------------------------

    Python 3.11+
    GitHub Actions
    UTC
"""

import os
import re
import sys
import json
import time
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ======================================================================
# 1. 基础配置
# ======================================================================

ROOT = Path("01_自生长知识系统")

REPORT_DAILY_ROOT = ROOT / "05_日报"
REPORT_WEEKLY_ROOT = ROOT / "06_周报"

IMAGE_ROOT = ROOT / "04_图片"

IMAGE_DAILY_ROOT = IMAGE_ROOT / "日报"
IMAGE_WEEKLY_ROOT = IMAGE_ROOT / "周报"

IMAGE_NAMES = [
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
]

MIN_IMAGE_COUNT = 3
MAX_IMAGE_COUNT = 4

AGNES_API_URL = "https://api.agnes-ai.cn/v1/images/generations"
AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

REQUEST_TIMEOUT = 180

# 每张图之间稍微留一点间隔。
# 当前项目调用量很低，不需要复杂队列。
REQUEST_INTERVAL_SECONDS = 3


# ======================================================================
# 2. 日志
# ======================================================================

def log(message):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print(f"[{now}] {message}", flush=True)


# ======================================================================
# 3. UTC 时间
# ======================================================================

def utc_today():
    return datetime.now(timezone.utc).date()


def iso_week_string(day):
    year, week, _ = day.isocalendar()
    return f"{year}-W{week:02d}"


# ======================================================================
# 4. 报告路径
# ======================================================================

def daily_report_path(day):
    return (
        REPORT_DAILY_ROOT
        / f"{day.year:04d}"
        / f"{day.month:02d}"
        / f"{day.isoformat()}.md"
    )


def weekly_report_path(week_string):
    year = int(week_string[:4])
    return REPORT_WEEKLY_ROOT / str(year) / f"{week_string[5:]}.md"


def daily_image_dir(day):
    return IMAGE_DAILY_ROOT / day.isoformat()


def weekly_image_dir(week_string):
    return IMAGE_WEEKLY_ROOT / week_string


# ======================================================================
# 5. 安全读取 Markdown
# ======================================================================

def read_text(path):
    return path.read_text(encoding="utf-8")


def clean_markdown(text):
    """
    去除 Markdown 中对视觉生成没有帮助的结构。
    """

    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`]*`", " ", text)

    # Markdown 图片
    text = re.sub(r"!$begin:math:display$\[\^$end:math:display$]*\]$begin:math:text$\[\^\)\]\+$end:math:text$", " ", text)

    # Markdown 链接
    text = re.sub(r"$begin:math:display$\(\[\^$end:math:display$]+)\]$begin:math:text$\[\^\)\]\+$end:math:text$", r"\1", text)

    # HTML
    text = re.sub(r"<[^>]+>", " ", text)

    # Markdown 标记
    text = re.sub(r"[*_>#~-]+", " ", text)

    # 多余空白
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ======================================================================
# 6. Markdown 分块
# ======================================================================

def split_markdown_blocks(text):
    """
    按 Markdown 空行切分。

    目的：

        插图1 / 插图2 / 插图3
        不再读取整篇报告。

    而是尽量找到图片插入位置附近的一个局部内容块。
    """

    raw_blocks = re.split(r"\n\s*\n", text)

    blocks = []

    for block in raw_blocks:
        block = block.strip()

        if not block:
            continue

        cleaned = clean_markdown(block)

        if len(cleaned) < 15:
            continue

        blocks.append(cleaned)

    return blocks


# ======================================================================
# 7. 截断文本
# ======================================================================

def truncate_text(text, max_chars):
    text = text.strip()

    if len(text) <= max_chars:
        return text

    return text[:max_chars].rstrip() + "……"


# ======================================================================
# 8. 提取标题
# ======================================================================

def extract_report_title(text):
    """
    尽量提取第一条 Markdown 标题。
    """

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        m = re.match(r"^#{1,6}\s+(.+)$", line)

        if m:
            title = clean_markdown(m.group(1))
            if title:
                return truncate_text(title, 160)

    return ""


# ======================================================================
# 9. 获取局部视觉上下文
# ======================================================================

def get_visual_context_for_position(blocks, position, total_images):
    """
    V4.0：

    不再给模型一大段正文。

    插图只使用：

        一个主要正文块
        + 少量上下文

    目的：

        强迫模型形成一个单一视觉故事。
    """

    if not blocks:
        return ""

    if len(blocks) == 1:
        return truncate_text(blocks[0], 650)

    # 根据插图序号分配正文区域。
    usable_count = max(1, total_images - 1)

    if usable_count == 1:
        index = len(blocks) // 2

    else:
        ratio = (position - 1) / max(1, usable_count - 1)

        index = int(round(ratio * (len(blocks) - 1)))

    index = max(0, min(index, len(blocks) - 1))

    main_block = blocks[index]

    # 只允许极少量相邻上下文。
    previous_block = ""
    next_block = ""

    if index > 0:
        previous_block = blocks[index - 1]

    if index + 1 < len(blocks):
        next_block = blocks[index + 1]

    context_parts = []

    if previous_block:
        context_parts.append(
            "前文背景："
            + truncate_text(previous_block, 220)
        )

    context_parts.append(
        "当前核心内容："
        + truncate_text(main_block, 600)
    )

    if next_block:
        context_parts.append(
            "后文背景："
            + truncate_text(next_block, 180)
        )

    context = "\n".join(context_parts)

    return truncate_text(context, 1000)


# ======================================================================
# 10. 首图视觉上下文
# ======================================================================

def get_cover_visual_context(report_text):
    """
    首图不能直接把整篇报告无限量交给模型。

    否则模型很容易认为：

        每一个主题都必须画出来。

    V4.0：

        标题
        +
        少量最重要正文

    然后明确：

        只选择一个最高优先级视觉故事。
    """

    title = extract_report_title(report_text)

    blocks = split_markdown_blocks(report_text)

    selected = []

    if title:
        selected.append("报告标题：" + title)

    for block in blocks[:4]:
        selected.append(
            "正文：" + truncate_text(block, 260)
        )

    return truncate_text("\n".join(selected), 1200)


# ======================================================================
# 11. Prompt
# ======================================================================

def build_image_prompt(
    report_type,
    report_identifier,
    image_name,
    visual_context,
):
    """
    V4.0 最重要部分。

    核心：

        ONE IMAGE
        ONE SCENE
        ONE VISUAL STORY

    不只是禁止 collage。

    而是主动要求：

        单一场景
        单一视觉中心
        单一叙事
    """

    is_cover = image_name == "首图.png"

    if is_cover:

        role_instruction = """
This is the COVER IMAGE of a news knowledge report.

The report may contain many different subjects and events.

DO NOT attempt to visualize all of them.

Instead:

Choose ONLY ONE dominant visual idea that best represents the overall character of the report.

Turn that single idea into ONE complete, coherent documentary scene.

The image must feel like ONE real moment captured by ONE camera in ONE physical location.

Do not create a visual summary made from multiple scenes.
"""

    else:

        role_instruction = f"""
This is interior illustration {image_name} of a news knowledge report.

Use the supplied local text only as contextual guidance.

Choose ONE single visual event, subject, or situation from that local context.

Do not attempt to visualize all information.

Create ONE complete scene that communicates ONE visual story.

The image should feel like ONE real moment captured by ONE camera in ONE physical location.
"""

    prompt = f"""
Create a high-quality editorial documentary image for:

Report type:
{report_type}

Report:
{report_identifier}

Image:
{image_name}

============================================================
PRIMARY VISUAL RULE
============================================================

ONE IMAGE
=
ONE SCENE
=
ONE VISUAL STORY

This rule is absolute.

Create:

- ONE continuous physical environment
- ONE coherent composition
- ONE dominant visual center
- ONE primary subject or tightly unified subject group
- ONE clear situation
- ONE moment in time
- ONE camera viewpoint

The viewer should immediately understand that this is ONE photograph-like scene.

============================================================
SCENE UNITY
============================================================

The image must look as if a real photographer stood in ONE location and captured ONE moment.

Everything visible must belong naturally to the same physical scene.

Do not combine separate places.

Do not combine separate moments.

Do not combine separate events.

Do not create a visual summary of several news stories.

Do not place unrelated symbolic objects around the frame.

Do not construct a collection of concepts.

If the source material contains many ideas:

IGNORE the secondary ideas.

Choose ONLY ONE dominant visual story.

Less information is better than multiple scenes.

============================================================
STRICTLY FORBIDDEN COMPOSITIONS
============================================================

ABSOLUTELY NO:

- collage
- photo collage
- grid
- four-panel composition
- six-panel composition
- nine-panel composition
- split screen
- multiple windows
- multiple frames
- picture wall
- thumbnail collection
- montage
- scrapbook
- contact sheet
- multiple photographs inside one image
- several mini-scenes
- miniature scenes
- separate visual boxes
- floating scene fragments
- picture-in-picture
- magazine layout
- newspaper layout
- presentation slide
- PowerPoint style
- dashboard
- infographic
- visual timeline
- concept board
- mood board
- comparison board
- before-and-after composition
- multiple locations
- multiple time periods
- multiple unrelated events

Do not use boxes, panels, frames, tiles, cards, windows, or compartments.

The final result must be ONE uninterrupted visual field.

============================================================
VISUAL CENTER
============================================================

Establish ONE obvious visual center.

The main subject should dominate the composition.

Secondary objects are allowed only when they naturally exist inside the same scene and support the same visual story.

Do NOT give equal visual importance to several different subjects.

Do NOT arrange several subjects like a catalog.

Do NOT create a collection of symbolic objects.

============================================================
NEWS CONTENT
============================================================

The image should be related to the supplied report content.

However:

Do NOT illustrate every fact.

Do NOT illustrate every named entity.

Do NOT illustrate every location.

Do NOT illustrate every consequence.

Do NOT turn the report into a visual encyclopedia.

Select ONE representative moment.

============================================================
TEXT RESTRICTION
============================================================

NO Chinese text.

NO English text.

NO readable text.

NO headlines.

NO captions.

NO subtitles.

NO labels.

NO article text.

NO newspaper text.

NO magazine text.

NO UI text.

NO website text.

NO logos.

NO brand marks.

NO watermark.

Avoid signs, screens, documents, posters, packages, or displays containing readable text.

Do not intentionally generate typography.

Arabic numerals 0-9 are allowed ONLY when naturally unavoidable in a realistic physical environment.

Do not add decorative numbers.

============================================================
STYLE
============================================================

Serious documentary editorial photography.

Realistic.

Cinematic but credible.

Premium visual quality.

Natural lighting.

Natural depth.

Professional photographic composition.

Strong but realistic atmosphere.

Detailed environment.

Physically coherent objects.

Consistent perspective.

Consistent lighting.

No surreal visual fragmentation.

No abstract concept collage.

No artificial information graphic.

No fantasy composition.

The final image should feel like ONE powerful editorial photograph.

============================================================
MOST IMPORTANT FINAL INSTRUCTION
============================================================

Before generating, mentally reduce the source material to:

ONE SUBJECT.
ONE SCENE.
ONE MOMENT.
ONE CAMERA.
ONE VISUAL STORY.

If the prompt contains several possible ideas:

Choose only the single strongest one.

Ignore the rest.

Do not merge them.

============================================================
SOURCE CONTEXT
============================================================

{role_instruction}

Source context:

{visual_context}

============================================================
FINAL QUALITY CHECK
============================================================

The result must pass all of these:

[YES] one scene
[YES] one location
[YES] one moment
[YES] one visual story
[YES] one dominant visual center
[YES] coherent photographic composition
[YES] realistic documentary style

[NO] collage
[NO] grid
[NO] split screen
[NO] multiple windows
[NO] multiple mini-scenes
[NO] multiple unrelated subjects
[NO] multiple locations
[NO] infographic
[NO] presentation layout
[NO] readable text
[NO] Chinese characters
[NO] English words
[NO] logos
[NO] watermark
"""

    return prompt.strip()


# ======================================================================
# 12. 调用 AGNES 图片 API
# ======================================================================

def generate_image(prompt):
    api_key = os.getenv("AGNES_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "AGNES_API_KEY environment variable is missing."
        )

    payload = {
        "model": AGNES_IMAGE_MODEL,
        "prompt": prompt,
        "size": IMAGE_SIZE,
        "ratio": IMAGE_RATIO,

        # 关键：
        # response_format 必须放在 extra_body 内。
        "extra_body": {
            "response_format": "url"
        }
    }

    body = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    request = urllib.request.Request(
        AGNES_API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    log("Calling AGNES image API...")

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw = response.read().decode("utf-8")

    except urllib.error.HTTPError as exc:

        error_body = ""

        try:
            error_body = exc.read().decode(
                "utf-8",
                errors="replace"
            )
        except Exception:
            pass

        raise RuntimeError(
            f"AGNES HTTP {exc.code}: {error_body[:2000]}"
        )

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"AGNES network error: {exc}"
        )

    try:
        data = json.loads(raw)

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"Invalid AGNES JSON response: {exc}\n"
            f"Raw response: {raw[:2000]}"
        )

    items = data.get("data")

    if not isinstance(items, list) or not items:

        raise RuntimeError(
            "AGNES response does not contain data[0]."
        )

    first = items[0]

    image_url = first.get("url")

    if not image_url:
        raise RuntimeError(
            "AGNES response data[0].url is missing."
        )

    log("AGNES image URL received.")

    return image_url


# ======================================================================
# 13. 下载图片
# ======================================================================

def download_image(url):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "748686-Knowledge-System/4.0"
        }
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            data = response.read()

    except Exception as exc:

        raise RuntimeError(
            f"Image download failed: {exc}"
        )

    if not data:
        raise RuntimeError(
            "Downloaded image is empty."
        )

    return data


# ======================================================================
# 14. PNG 校验
# ======================================================================

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_valid_png(path):
    if not path.exists():
        return False

    if not path.is_file():
        return False

    try:

        if path.stat().st_size < 100:
            return False

        with path.open("rb") as f:
            signature = f.read(8)

        return signature == PNG_SIGNATURE

    except Exception:
        return False


# ======================================================================
# 15. 原子落盘
# ======================================================================

def atomic_write_bytes(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=".tmp_",
        suffix=".png",
        dir=str(path.parent)
    )

    try:

        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(
            temp_name,
            path
        )

    finally:

        if os.path.exists(temp_name):

            try:
                os.remove(temp_name)
            except OSError:
                pass


def atomic_write_text(path, text):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=".tmp_",
        suffix=".md",
        dir=str(path.parent)
    )

    try:

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(text)
            f.flush()
            os.fsync(f.fileno())

        os.replace(
            temp_name,
            path
        )

    finally:

        if os.path.exists(temp_name):

            try:
                os.remove(temp_name)
            except OSError:
                pass


# ======================================================================
# 16. 当前图片检查
# ======================================================================

def existing_valid_images(image_dir):
    result = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if is_valid_png(path):
            result.append(name)

    return result


def determine_missing_images(image_dir):
    """
    最少必须：

        首图
        插图1
        插图2

    插图3：

        如果已有并有效，保留。
        如果没有，不强制生成。

    因此默认最低 3 张。
    """

    required = [
        "首图.png",
        "插图1.png",
        "插图2.png",
    ]

    missing = []

    for name in required:

        path = image_dir / name

        if not is_valid_png(path):
            missing.append(name)

    return missing


# ======================================================================
# 17. 图片数量
# ======================================================================

def image_count(image_dir):
    return len(
        existing_valid_images(image_dir)
    )


# ======================================================================
# 18. 计算图片插入位置
# ======================================================================

def get_insertion_positions(block_count, interior_count):
    """
    将插图分散到正文不同区域。

    首图固定最前。

    插图均匀穿插正文。
    """

    if interior_count <= 0:
        return []

    if block_count <= 1:
        return [1] * interior_count

    positions = []

    for i in range(interior_count):

        ratio = (i + 1) / (interior_count + 1)

        pos = int(
            round(
                ratio * block_count
            )
        )

        pos = max(
            1,
            min(
                block_count,
                pos
            )
        )

        positions.append(pos)

    return positions


# ======================================================================
# 19. Markdown 图片路径
# ======================================================================

def markdown_image_path(report_path, image_path):
    """
    必须使用 os.path.relpath。

    不硬编码 ../../。
    """

    relative = os.path.relpath(
        image_path,
        start=report_path.parent
    )

    return relative.replace(
        os.sep,
        "/"
    )


# ======================================================================
# 20. 构造带图 Markdown
# ======================================================================

def build_image_markdown(
    report_path,
    original_text,
    image_dir,
):
    blocks = split_markdown_blocks(
        original_text
    )

    valid_images = existing_valid_images(
        image_dir
    )

    # 至少首图、插图1、插图2。
    ordered_images = [
        name
        for name in IMAGE_NAMES
        if name in valid_images
    ]

    if len(ordered_images) < MIN_IMAGE_COUNT:
        raise RuntimeError(
            f"Not enough valid images: "
            f"{ordered_images}"
        )

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    output_parts = []

    cover_path = image_dir / "首图.png"

    if not is_valid_png(cover_path):
        raise RuntimeError(
            "Cover image is missing."
        )

    cover_rel = markdown_image_path(
        report_path,
        cover_path
    )

    output_parts.append(
        f"![首图]({cover_rel})"
    )

    output_parts.append("")

    # --------------------------------------------------------------
    # 没有正文
    # --------------------------------------------------------------

    if not blocks:

        output_parts.append(
            original_text.strip()
        )

        return "\n".join(
            output_parts
        ).strip() + "\n"

    # --------------------------------------------------------------
    # 正文插图
    # --------------------------------------------------------------

    interior_images = [
        name
        for name in ordered_images
        if name != "首图.png"
    ]

    positions = get_insertion_positions(
        len(blocks),
        len(interior_images)
    )

    insert_map = {}

    for name, position in zip(
        interior_images,
        positions
    ):

        insert_map.setdefault(
            position,
            []
        ).append(name)

    for index, block in enumerate(
        blocks,
        start=1
    ):

        output_parts.append(
            block
        )

        # 当前正文块后插入图片
        images_here = insert_map.get(
            index,
            []
        )

        for image_name in images_here:

            image_path = (
                image_dir / image_name
            )

            if not is_valid_png(image_path):
                continue

            relative = markdown_image_path(
                report_path,
                image_path
            )

            output_parts.append("")

            output_parts.append(
                f"![{image_name}]({relative})"
            )

            output_parts.append("")

    return "\n\n".join(
        output_parts
    ).strip() + "\n"


# ======================================================================
# 21. 验证带图报告
# ======================================================================

def validate_image_report(
    report_path,
    image_dir,
    image_report_path,
):
    if not image_report_path.exists():
        raise RuntimeError(
            "Image report was not created."
        )

    text = read_text(
        image_report_path
    )

    valid_images = existing_valid_images(
        image_dir
    )

    count = len(valid_images)

    if count < MIN_IMAGE_COUNT:
        raise RuntimeError(
            f"Image count {count} < {MIN_IMAGE_COUNT}"
        )

    if count > MAX_IMAGE_COUNT:
        raise RuntimeError(
            f"Image count {count} > {MAX_IMAGE_COUNT}"
        )

    # --------------------------------------------------------------
    # 所有图片必须存在
    # --------------------------------------------------------------

    for name in valid_images:

        path = image_dir / name

        if not is_valid_png(path):
            raise RuntimeError(
                f"Invalid image: {path}"
            )

    # --------------------------------------------------------------
    # 首图必须最先出现
    # --------------------------------------------------------------

    cover_path = image_dir / "首图.png"

    cover_rel = markdown_image_path(
        image_report_path,
        cover_path
    )

    expected_cover = (
        f"![首图]({cover_rel})"
    )

    if not text.startswith(
        expected_cover
    ):
        raise RuntimeError(
            "Cover image is not at the beginning."
        )

    # --------------------------------------------------------------
    # 图片顺序
    # --------------------------------------------------------------

    previous_index = -1

    for name in valid_images:

        image_path = image_dir / name

        relative = markdown_image_path(
            image_report_path,
            image_path
        )

        marker = (
            f"]({relative})"
        )

        index = text.find(marker)

        if index == -1:
            raise RuntimeError(
                f"Image link missing in report: {name}"
            )

        if index < previous_index:

            raise RuntimeError(
                f"Image order invalid: {name}"
            )

        previous_index = index

    log(
        f"Validation passed: "
        f"{image_report_path}"
    )

    return True


# ======================================================================
# 22. 生成缺失图片
# ======================================================================

def generate_missing_images(
    report_type,
    report_identifier,
    report_text,
    image_dir,
):
    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    missing = determine_missing_images(
        image_dir
    )

    current_valid = existing_valid_images(
        image_dir
    )

    log(
        f"Existing valid images: "
        f"{current_valid}"
    )

    if not missing:

        log(
            "Required images already exist. "
            "No image generation needed."
        )

        return

    blocks = split_markdown_blocks(
        report_text
    )

    # 默认最低 3 张：
    # 首图 + 插图1 + 插图2
    total_visual_images = max(
        MIN_IMAGE_COUNT,
        len(current_valid) + len(missing)
    )

    total_visual_images = min(
        total_visual_images,
        MAX_IMAGE_COUNT
    )

    log(
        f"Missing required images: {missing}"
    )

    for image_name in missing:

        log(
            f"Generating {report_identifier} "
            f"{image_name}"
        )

        # ----------------------------------------------------------
        # 首图
        # ----------------------------------------------------------

        if image_name == "首图.png":

            visual_context = (
                get_cover_visual_context(
                    report_text
                )
            )

        # ----------------------------------------------------------
        # 插图
        # ----------------------------------------------------------

        else:

            match = re.search(
                r"插图(\d+)\.png",
                image_name
            )

            if match:

                position = int(
                    match.group(1)
                )

            else:

                position = 1

            visual_context = (
                get_visual_context_for_position(
                    blocks,
                    position,
                    total_visual_images
                )
            )

        prompt = build_image_prompt(
            report_type=report_type,
            report_identifier=report_identifier,
            image_name=image_name,
            visual_context=visual_context,
        )

        log(
            f"Prompt prepared for {image_name}"
        )

        image_url = generate_image(
            prompt
        )

        image_data = download_image(
            image_url
        )

        target_path = (
            image_dir / image_name
        )

        atomic_write_bytes(
            target_path,
            image_data
        )

        if not is_valid_png(
            target_path
        ):
            raise RuntimeError(
                f"Generated image failed "
                f"PNG validation: {target_path}"
            )

        log(
            f"Saved image: {target_path}"
        )

        # ----------------------------------------------------------
        # 每张图片立即落盘。
        # ----------------------------------------------------------

        time.sleep(
            REQUEST_INTERVAL_SECONDS
        )


# ======================================================================
# 23. 处理日报
# ======================================================================

def process_daily_report(day):
    report_path = daily_report_path(day)

    log("=" * 70)
    log(
        f"DAILY REPORT: {day.isoformat()}"
    )
    log(
        f"Path: {report_path}"
    )

    if not report_path.exists():

        log(
            "Daily report does not exist. Skip."
        )

        return False

    original_text = read_text(
        report_path
    )

    image_dir = daily_image_dir(
        day
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # 生成缺失图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="DAILY REPORT",
        report_identifier=day.isoformat(),
        report_text=original_text,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 每次重新从原始 Markdown 构建带图版本。
    # 原始报告绝不修改。
    # --------------------------------------------------------------

    image_report_path = report_path.with_name(
        report_path.stem + "_带图.md"
    )

    image_markdown = build_image_markdown(
        report_path=report_path,
        original_text=original_text,
        image_dir=image_dir,
    )

    atomic_write_text(
        image_report_path,
        image_markdown
    )

    # --------------------------------------------------------------
    # 验证
    # --------------------------------------------------------------

    validate_image_report(
        report_path=report_path,
        image_dir=image_dir,
        image_report_path=image_report_path,
    )

    log(
        f"Daily image report ready: "
        f"{image_report_path}"
    )

    return True


# ======================================================================
# 24. 处理周报
# ======================================================================

def process_weekly_report(week_string):
    report_path = weekly_report_path(
        week_string
    )

    log("=" * 70)
    log(
        f"WEEKLY REPORT: {week_string}"
    )
    log(
        f"Path: {report_path}"
    )

    if not report_path.exists():

        log(
            "Weekly report does not exist. Skip."
        )

        return False

    original_text = read_text(
        report_path
    )

    image_dir = weekly_image_dir(
        week_string
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # 生成缺失图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="WEEKLY REPORT",
        report_identifier=week_string,
        report_text=original_text,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 构建带图版本
    # --------------------------------------------------------------

    image_report_path = report_path.with_name(
        report_path.stem + "_带图.md"
    )

    image_markdown = build_image_markdown(
        report_path=report_path,
        original_text=original_text,
        image_dir=image_dir,
    )

    atomic_write_text(
        image_report_path,
        image_markdown
    )

    # --------------------------------------------------------------
    # 验证
    # --------------------------------------------------------------

    validate_image_report(
        report_path=report_path,
        image_dir=image_dir,
        image_report_path=image_report_path,
    )

    log(
        f"Weekly image report ready: "
        f"{image_report_path}"
    )

    return True


# ======================================================================
# 25. 主程序
# ======================================================================

def main():
    log("=" * 70)
    log("748686 KNOWLEDGE IMAGE GENERATOR V4.0")
    log("ONE IMAGE = ONE SCENE = ONE VISUAL STORY")
    log("=" * 70)

    today = utc_today()

    day_before = today - timedelta(days=2)
    yesterday = today - timedelta(days=1)

    log(
        f"DAY_BEFORE : {day_before}"
    )
    log(
        f"YESTERDAY  : {yesterday}"
    )
    log(
        f"TODAY      : {today}"
    )
    log(
        "Timezone   : UTC"
    )

    processed_daily = 0
    processed_weekly = 0
    failed = 0

    # ==============================================================
    # 日报：
    #
    # day before
    # yesterday
    # today
    #
    # 一个报告处理完、落盘、验证后，
    # 才进入下一个报告。
    # ==============================================================

    for day in [
        day_before,
        yesterday,
        today,
    ]:

        try:

            if process_daily_report(
                day
            ):
                processed_daily += 1

        except Exception as exc:

            failed += 1

            log(
                f"ERROR processing daily "
                f"{day}: {exc}"
            )

    # ==============================================================
    # 周报
    #
    # 只处理上述日期对应的 ISO 周。
    # 同一周只处理一次。
    # ==============================================================

    weekly_weeks = []

    for day in [
        day_before,
        yesterday,
        today,
    ]:

        week_string = iso_week_string(
            day
        )

        if week_string not in weekly_weeks:

            weekly_weeks.append(
                week_string
            )

    for week_string in weekly_weeks:

        try:

            if process_weekly_report(
                week_string
            ):
                processed_weekly += 1

        except Exception as exc:

            failed += 1

            log(
                f"ERROR processing weekly "
                f"{week_string}: {exc}"
            )

    # ==============================================================
    # 最终状态
    # ==============================================================

    log("=" * 70)
    log("IMAGE GENERATION FINISHED")
    log(
        f"Daily processed  : {processed_daily}"
    )
    log(
        f"Weekly processed : {processed_weekly}"
    )
    log(
        f"Failed           : {failed}"
    )
    log("=" * 70)

    # 即使某一个报告失败，
    # 其他报告也继续处理。
    #
    # 这里保持 0，
    # 避免一个报告的问题导致整个 GitHub Action
    # 把已经成功落盘的其他结果全部判定失败。
    return 0


# ======================================================================
# 26. Entry
# ======================================================================

if __name__ == "__main__":
    sys.exit(
        main()
    )
