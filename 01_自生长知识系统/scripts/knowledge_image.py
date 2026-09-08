#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Generator V4.1
======================================================================

核心原则：

    ONE IMAGE
        =
    ONE SCENE
        =
    ONE VISUAL STORY

即：

    一张图
    一个连续场景
    一个主要视觉中心
    一个时间点
    一个摄影机位
    一个视觉故事


图片保存：

01_自生长知识系统/
└── 04_图片/
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


报告：

原始报告保持不变：

    YYYY-MM-DD.md
    Wxx.md

带图版本：

    YYYY-MM-DD_带图.md
    Wxx_带图.md


V4.1 修复：

1. 修复 Markdown 清洗正则错误
2. 不再使用容易造成括号错误的 Markdown 图片正则
3. 强化 ONE IMAGE = ONE SCENE
4. 强化 ONE CAMERA
5. 强化 ONE LOCATION
6. 强化 ONE MOMENT
7. 强化 ONE VISUAL CENTER
8. 插图尽量只使用一个核心正文块
9. 禁止 collage / grid / split-screen / multiple mini-scenes
10. 每张图片生成后立即落盘
11. 每个报告完成后立即生成并落盘 _带图.md
12. UTC 日期
13. 原始 Markdown 永不修改
14. 不存在的日报/周报自动跳过
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


# ======================================================================
# 2. AGNES
# ======================================================================

AGNES_API_URL = (
    "https://api.agnes-ai.cn/v1/images/generations"
)

AGNES_IMAGE_MODEL = (
    "agnes-image-2.5-flash"
)

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

REQUEST_TIMEOUT = 180

REQUEST_INTERVAL_SECONDS = 3


# ======================================================================
# 3. 日志
# ======================================================================

def log(message):
    now = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    print(
        f"[{now}] {message}",
        flush=True
    )


# ======================================================================
# 4. UTC
# ======================================================================

def utc_today():
    return datetime.now(
        timezone.utc
    ).date()


def iso_week_string(day):
    year, week, _ = day.isocalendar()

    return (
        f"{year}-W{week:02d}"
    )


# ======================================================================
# 5. 报告路径
# ======================================================================

def daily_report_path(day):

    return (
        REPORT_DAILY_ROOT
        / f"{day.year:04d}"
        / f"{day.month:02d}"
        / f"{day.isoformat()}.md"
    )


def weekly_report_path(week_string):

    year = int(
        week_string[:4]
    )

    week = week_string[5:]

    return (
        REPORT_WEEKLY_ROOT
        / str(year)
        / f"{week}.md"
    )


def daily_image_dir(day):

    return (
        IMAGE_DAILY_ROOT
        / day.isoformat()
    )


def weekly_image_dir(week_string):

    return (
        IMAGE_WEEKLY_ROOT
        / week_string
    )


# ======================================================================
# 6. 文件读取
# ======================================================================

def read_text(path):

    return path.read_text(
        encoding="utf-8"
    )


# ======================================================================
# 7. Markdown 清洗
# ======================================================================

def clean_markdown(text):
    """
    V4.1：

    不再使用之前容易出现括号错误的 Markdown 图片正则。

    使用更安全的逐行清洗方式。
    """

    lines = text.splitlines()

    output = []

    inside_code_block = False

    for line in lines:

        stripped = line.strip()

        # --------------------------------------------------------------
        # Code block
        # --------------------------------------------------------------

        if stripped.startswith("```"):

            inside_code_block = (
                not inside_code_block
            )

            continue

        if inside_code_block:
            continue

        # --------------------------------------------------------------
        # Markdown 图片：
        #
        # ![alt](url)
        #
        # 只删除整行中图片链接的视觉干扰。
        # --------------------------------------------------------------

        line = re.sub(
            r"!$begin:math:display$\[\^$end:math:display$]*\]$begin:math:text$\[\^\)\]\*$end:math:text$",
            " ",
            line
        )

        # --------------------------------------------------------------
        # Markdown 链接：
        #
        # [文字](url)
        #
        # 保留文字。
        # --------------------------------------------------------------

        line = re.sub(
            r"$begin:math:display$\(\[\^$end:math:display$]+)\]$begin:math:text$\[\^\)\]\*$end:math:text$",
            r"\1",
            line
        )

        # --------------------------------------------------------------
        # HTML
        # --------------------------------------------------------------

        line = re.sub(
            r"<[^>]*>",
            " ",
            line
        )

        # --------------------------------------------------------------
        # Markdown 标题
        # --------------------------------------------------------------

        line = re.sub(
            r"^\s*#{1,6}\s*",
            "",
            line
        )

        # --------------------------------------------------------------
        # Markdown emphasis
        # --------------------------------------------------------------

        line = line.replace(
            "**",
            ""
        )

        line = line.replace(
            "__",
            ""
        )

        line = line.replace(
            "*",
            ""
        )

        line = line.replace(
            "_",
            " "
        )

        # --------------------------------------------------------------
        # Markdown 引用
        # --------------------------------------------------------------

        line = re.sub(
            r"^\s*>\s*",
            "",
            line
        )

        # --------------------------------------------------------------
        # Markdown 列表
        # --------------------------------------------------------------

        line = re.sub(
            r"^\s*[-+]\s+",
            "",
            line
        )

        line = re.sub(
            r"^\s*\d+[.)]\s+",
            "",
            line
        )

        # --------------------------------------------------------------
        # 空白
        # --------------------------------------------------------------

        line = re.sub(
            r"\s+",
            " ",
            line
        )

        line = line.strip()

        if line:
            output.append(line)

    return "\n".join(output).strip()


# ======================================================================
# 8. Markdown 正文分块
# ======================================================================

def split_markdown_blocks(text):
    """
    将 Markdown 按空行分成独立内容块。

    插图不会直接读取整篇报告。

    而是优先寻找：

        一个完整正文块
        +
        极少量上下文

    这样可以避免一张图片同时表现多个新闻。
    """

    raw_blocks = re.split(
        r"\n\s*\n",
        text
    )

    blocks = []

    for raw in raw_blocks:

        raw = raw.strip()

        if not raw:
            continue

        cleaned = clean_markdown(
            raw
        )

        if len(cleaned) < 20:
            continue

        blocks.append(cleaned)

    return blocks


# ======================================================================
# 9. 文本截断
# ======================================================================

def truncate_text(
    text,
    max_chars
):

    text = text.strip()

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        .rstrip()
        + "……"
    )


# ======================================================================
# 10. 提取标题
# ======================================================================

def extract_report_title(text):

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        match = re.match(
            r"^#{1,6}\s+(.+)$",
            line
        )

        if match:

            title = clean_markdown(
                match.group(1)
            )

            if title:
                return truncate_text(
                    title,
                    180
                )

    return ""


# ======================================================================
# 11. 首图视觉上下文
# ======================================================================

def get_cover_visual_context(
    report_text
):
    """
    首图：

    不把整篇报告全部交给模型。

    只提供：

        标题
        +
        前几个重要正文块

    然后强制模型：

        只选择一个最高优先级视觉故事。
    """

    title = extract_report_title(
        report_text
    )

    blocks = split_markdown_blocks(
        report_text
    )

    parts = []

    if title:
        parts.append(
            "报告标题："
            + title
        )

    # 首图最多读取前 4 个内容块。
    for block in blocks[:4]:

        parts.append(
            "正文信息："
            + truncate_text(
                block,
                260
            )
        )

    return truncate_text(
        "\n".join(parts),
        1200
    )


# ======================================================================
# 12. 插图核心内容
# ======================================================================

def get_visual_context_for_position(
    blocks,
    image_number,
    total_interior_images
):
    """
    V4.1：

    插图尽可能只取一个主要正文块。

    不把整个日报交给模型。

    image_number：

        1 = 插图1
        2 = 插图2
        3 = 插图3
    """

    if not blocks:
        return ""

    if len(blocks) == 1:
        selected_index = 0

    elif total_interior_images <= 1:

        selected_index = (
            len(blocks) // 2
        )

    else:

        ratio = (
            image_number - 1
        ) / max(
            1,
            total_interior_images - 1
        )

        selected_index = int(
            round(
                ratio
                * (len(blocks) - 1)
            )
        )

    selected_index = max(
        0,
        min(
            selected_index,
            len(blocks) - 1
        )
    )

    main_block = blocks[
        selected_index
    ]

    # --------------------------------------------------------------
    # 核心原则：
    #
    # 这里不再拼接前后多个新闻块。
    #
    # 只提供一个主要正文块。
    # --------------------------------------------------------------

    return truncate_text(
        main_block,
        850
    )


# ======================================================================
# 13. Prompt
# ======================================================================

def build_image_prompt(
    report_type,
    report_identifier,
    image_name,
    visual_context
):

    is_cover = (
        image_name == "首图.png"
    )

    if is_cover:

        role_instruction = """
This is the COVER IMAGE.

The report may contain many subjects.

Do NOT visualize all subjects.

Choose ONE dominant visual story that best represents the overall report.

Turn that single idea into ONE complete documentary scene.

The image must look like ONE real photograph taken by ONE camera in ONE physical location at ONE moment.
"""

    else:

        role_instruction = f"""
This is interior illustration {image_name}.

The supplied source context is only ONE selected section of the report.

Choose ONE dominant visual story from this section.

Do not visualize secondary information.

Turn the selected idea into ONE complete documentary scene.

The image must look like ONE real photograph taken by ONE camera in ONE physical location at ONE moment.
"""

    prompt = f"""
Create a premium editorial documentary image.

Report type:
{report_type}

Report:
{report_identifier}

Image:
{image_name}


============================================================
ABSOLUTE COMPOSITION RULE
============================================================

ONE IMAGE
=
ONE SCENE
=
ONE VISUAL STORY

This is the most important instruction.

The final image must represent ONE single continuous scene.

It must feel like:

    ONE photographer
    ONE camera
    ONE location
    ONE moment
    ONE scene
    ONE visual story


============================================================
ONE CAMERA
============================================================

Imagine that a real photographer is physically standing in the scene.

The entire image must be captured from ONE camera position.

Do not combine photographs.

Do not simulate multiple camera angles.

Do not show several different viewpoints.

Do not show separate photographs.


============================================================
ONE LOCATION
============================================================

Everything in the image must exist naturally in the same physical location.

No second location.

No distant location.

No map of another location.

No symbolic representation of another location.

No transition between locations.


============================================================
ONE MOMENT
============================================================

Everything must happen at the same moment in time.

Do not combine:

    past + present

or:

    before + after

or:

    different stages of an event.

Show ONE specific moment.


============================================================
ONE VISUAL CENTER
============================================================

Create ONE dominant visual center.

The viewer should immediately know:

    "This is what the image is about."

The primary subject should clearly dominate.

Other objects may appear only when they naturally belong to the same scene.

Do not give equal importance to several independent subjects.


============================================================
DO NOT OVER-EXPLAIN THE NEWS
============================================================

The source material may contain many facts.

Do NOT illustrate every fact.

Do NOT illustrate every named person.

Do NOT illustrate every organization.

Do NOT illustrate every location.

Do NOT illustrate every consequence.

Do NOT create a visual encyclopedia.

Instead:

Choose ONE representative visual moment.

Less information is better.

One strong scene is better than many weak scenes.


============================================================
ABSOLUTELY FORBIDDEN
============================================================

NEVER create:

- collage
- photo collage
- grid
- four-panel
- six-panel
- nine-panel
- split screen
- multiple windows
- multiple frames
- multiple photographs
- picture wall
- photo wall
- thumbnail collection
- montage
- scrapbook
- contact sheet
- miniature scenes
- multiple mini-scenes
- floating scene fragments
- picture-in-picture
- magazine layout
- newspaper layout
- presentation slide
- PowerPoint layout
- dashboard
- infographic
- timeline graphic
- concept board
- mood board
- comparison board
- visual summary made from multiple scenes
- multiple unrelated events
- multiple locations
- multiple time periods
- separate visual boxes
- cards
- tiles
- compartments
- panels

There must be NO boxes.

There must be NO grids.

There must be NO separated mini-images.

There must be NO split composition.


============================================================
NO CONCEPTUAL OBJECT COLLECTION
============================================================

Do not place several symbolic objects around the frame just to represent different ideas.

For example:

Do NOT combine:

    building
    map
    aircraft
    stock chart
    politician
    crowd

just because they are related to the same news topic.

Instead choose ONE.

Build ONE coherent physical scene around that ONE choice.


============================================================
TEXT PROHIBITION
============================================================

NO Chinese characters.

NO English words.

NO readable text.

NO headlines.

NO captions.

NO subtitles.

NO labels.

NO newspaper text.

NO magazine text.

NO website text.

NO UI text.

NO logos.

NO watermarks.

NO brand marks.

NO infographic text.

NO chart labels.

Avoid signs, screens, documents, posters, packages, monitors, newspapers, and displays containing readable text.

Do not intentionally generate typography.


============================================================
NUMBERS
============================================================

Arabic numerals 0-9 are allowed ONLY if naturally unavoidable in a realistic environment.

Do not add decorative numbers.

Do not add charts.

Do not add statistics.

Do not add percentages.

Do not add data visualizations.


============================================================
VISUAL STYLE
============================================================

Serious documentary editorial photography.

Realistic.

Cinematic but credible.

Premium.

Natural lighting.

Natural depth.

Real physical environment.

Professional photographic composition.

Strong atmosphere.

Consistent perspective.

Consistent lighting.

Physically coherent objects.

No surreal fragmentation.

No abstract collage.

No information graphic.

No fantasy composition.

The final result should look like ONE powerful editorial photograph.


============================================================
DECISION PROCESS
============================================================

Before generating the image:

STEP 1:
Identify the strongest visual idea.

STEP 2:
Discard all secondary ideas.

STEP 3:
Choose ONE physical location.

STEP 4:
Choose ONE moment.

STEP 5:
Choose ONE dominant subject.

STEP 6:
Choose ONE camera viewpoint.

STEP 7:
Create ONE uninterrupted scene.

Do NOT merge multiple ideas.


============================================================
FINAL SELF-CHECK
============================================================

Before output:

Is there exactly ONE scene?

Is there exactly ONE location?

Is there exactly ONE moment?

Is there exactly ONE camera viewpoint?

Is there ONE dominant visual center?

Does everything belong naturally to the same physical environment?

If not:

Simplify the image.

Remove secondary scenes.

Remove secondary locations.

Remove symbolic fragments.

Remove unnecessary objects.

Return to ONE scene.


============================================================
SOURCE CONTEXT
============================================================

{role_instruction}

Source context:

{visual_context}


============================================================
FINAL COMMAND
============================================================

Generate ONE uninterrupted 16:9 editorial photograph.

ONE SCENE.

ONE MOMENT.

ONE CAMERA.

ONE LOCATION.

ONE VISUAL STORY.

No collage.

No grid.

No split screen.

No multiple mini-scenes.

No text.

No Chinese.

No English.

No watermark.
"""

    return prompt.strip()


# ======================================================================
# 14. AGNES API
# ======================================================================

def generate_image(prompt):

    api_key = os.getenv(
        "AGNES_API_KEY",
        ""
    ).strip()

    if not api_key:

        raise RuntimeError(
            "AGNES_API_KEY environment variable is missing."
        )

    payload = {

        "model": AGNES_IMAGE_MODEL,

        "prompt": prompt,

        "size": IMAGE_SIZE,

        "ratio": IMAGE_RATIO,

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
            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json",
        },
        method="POST",
    )

    log(
        "Calling AGNES image API..."
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw = response.read().decode(
                "utf-8"
            )

    except urllib.error.HTTPError as exc:

        error_body = ""

        try:

            error_body = (
                exc.read()
                .decode(
                    "utf-8",
                    errors="replace"
                )
            )

        except Exception:
            pass

        raise RuntimeError(
            f"AGNES HTTP {exc.code}: "
            f"{error_body[:2000]}"
        )

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"AGNES network error: {exc}"
        )

    try:

        data = json.loads(
            raw
        )

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            "Invalid AGNES JSON response: "
            f"{exc}\n"
            f"Raw response: {raw[:2000]}"
        )

    items = data.get(
        "data"
    )

    if not isinstance(
        items,
        list
    ) or not items:

        raise RuntimeError(
            "AGNES response does not contain data[0]."
        )

    first = items[0]

    image_url = first.get(
        "url"
    )

    if not image_url:

        raise RuntimeError(
            "AGNES response data[0].url is missing."
        )

    log(
        "AGNES image URL received."
    )

    return image_url


# ======================================================================
# 15. 下载图片
# ======================================================================

def download_image(url):

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent":
                "748686-Knowledge-System/4.1"
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
# 16. PNG 验证
# ======================================================================

PNG_SIGNATURE = (
    b"\x89PNG\r\n\x1a\n"
)


def is_valid_png(path):

    if not path.exists():
        return False

    if not path.is_file():
        return False

    try:

        if path.stat().st_size < 100:
            return False

        with path.open(
            "rb"
        ) as f:

            signature = f.read(8)

        return (
            signature
            == PNG_SIGNATURE
        )

    except Exception:

        return False


# ======================================================================
# 17. 原子写入 PNG
# ======================================================================

def atomic_write_bytes(
    path,
    data
):

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

        with os.fdopen(
            fd,
            "wb"
        ) as f:

            f.write(data)

            f.flush()

            os.fsync(
                f.fileno()
            )

        os.replace(
            temp_name,
            path
        )

    finally:

        if os.path.exists(
            temp_name
        ):

            try:
                os.remove(
                    temp_name
                )

            except OSError:
                pass


# ======================================================================
# 18. 原子写入 Markdown
# ======================================================================

def atomic_write_text(
    path,
    text
):

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

            os.fsync(
                f.fileno()
            )

        os.replace(
            temp_name,
            path
        )

    finally:

        if os.path.exists(
            temp_name
        ):

            try:
                os.remove(
                    temp_name
                )

            except OSError:
                pass


# ======================================================================
# 19. 已存在图片
# ======================================================================

def existing_valid_images(
    image_dir
):

    result = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if is_valid_png(path):

            result.append(
                name
            )

    return result


# ======================================================================
# 20. 缺失图片
# ======================================================================

def determine_missing_images(
    image_dir
):

    required = [
        "首图.png",
        "插图1.png",
        "插图2.png",
    ]

    missing = []

    for name in required:

        path = image_dir / name

        if not is_valid_png(
            path
        ):

            missing.append(
                name
            )

    return missing


# ======================================================================
# 21. 图片数量
# ======================================================================

def image_count(
    image_dir
):

    return len(
        existing_valid_images(
            image_dir
        )
    )


# ======================================================================
# 22. Markdown 图片相对路径
# ======================================================================

def markdown_image_path(
    report_path,
    image_path
):

    relative = os.path.relpath(
        image_path,
        start=report_path.parent
    )

    return relative.replace(
        os.sep,
        "/"
    )


# ======================================================================
# 23. 正文图片插入位置
# ======================================================================

def get_insertion_positions(
    block_count,
    interior_count
):

    if interior_count <= 0:
        return []

    if block_count <= 1:

        return [
            1
            for _ in range(
                interior_count
            )
        ]

    positions = []

    for i in range(
        interior_count
    ):

        ratio = (
            (i + 1)
            /
            (interior_count + 1)
        )

        position = int(
            round(
                ratio
                * block_count
            )
        )

        position = max(
            1,
            min(
                block_count,
                position
            )
        )

        positions.append(
            position
        )

    return positions


# ======================================================================
# 24. 构建带图 Markdown
# ======================================================================

def build_image_markdown(
    report_path,
    original_text,
    image_dir
):

    blocks = split_markdown_blocks(
        original_text
    )

    valid_images = existing_valid_images(
        image_dir
    )

    ordered_images = [
        name
        for name in IMAGE_NAMES
        if name in valid_images
    ]

    if len(ordered_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "Not enough valid images: "
            f"{ordered_images}"
        )

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover_path = (
        image_dir
        / "首图.png"
    )

    if not is_valid_png(
        cover_path
    ):

        raise RuntimeError(
            "Cover image is missing."
        )

    cover_relative = (
        markdown_image_path(
            report_path,
            cover_path
        )
    )

    output_parts = []

    output_parts.append(
        f"![首图]({cover_relative})"
    )

    output_parts.append("")

    # --------------------------------------------------------------
    # 没有正文
    # --------------------------------------------------------------

    if not blocks:

        output_parts.append(
            original_text.strip()
        )

        return (
            "\n".join(
                output_parts
            ).strip()
            + "\n"
        )

    # --------------------------------------------------------------
    # 插图
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
        ).append(
            name
        )

    # --------------------------------------------------------------
    # 正文
    # --------------------------------------------------------------

    for index, block in enumerate(
        blocks,
        start=1
    ):

        output_parts.append(
            block
        )

        images_here = (
            insert_map.get(
                index,
                []
            )
        )

        for image_name in images_here:

            image_path = (
                image_dir
                / image_name
            )

            if not is_valid_png(
                image_path
            ):
                continue

            relative = (
                markdown_image_path(
                    report_path,
                    image_path
                )
            )

            output_parts.append("")

            output_parts.append(
                f"![{image_name}]({relative})"
            )

            output_parts.append("")

    return (
        "\n\n".join(
            output_parts
        ).strip()
        + "\n"
    )


# ======================================================================
# 25. 验证带图报告
# ======================================================================

def validate_image_report(
    report_path,
    image_dir,
    image_report_path
):

    if not image_report_path.exists():

        raise RuntimeError(
            "Image report was not created."
        )

    text = read_text(
        image_report_path
    )

    valid_images = (
        existing_valid_images(
            image_dir
        )
    )

    count = len(
        valid_images
    )

    if count < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"Image count {count} "
            f"< {MIN_IMAGE_COUNT}"
        )

    if count > MAX_IMAGE_COUNT:

        raise RuntimeError(
            f"Image count {count} "
            f"> {MAX_IMAGE_COUNT}"
        )

    # --------------------------------------------------------------
    # 图片有效性
    # --------------------------------------------------------------

    for name in valid_images:

        path = (
            image_dir / name
        )

        if not is_valid_png(
            path
        ):

            raise RuntimeError(
                f"Invalid image: {path}"
            )

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover_path = (
        image_dir
        / "首图.png"
    )

    cover_relative = (
        markdown_image_path(
            image_report_path,
            cover_path
        )
    )

    expected_cover = (
        f"![首图]({cover_relative})"
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

        image_path = (
            image_dir / name
        )

        relative = (
            markdown_image_path(
                image_report_path,
                image_path
            )
        )

        marker = (
            f"]({relative})"
        )

        index = text.find(
            marker
        )

        if index == -1:

            raise RuntimeError(
                "Image link missing: "
                f"{name}"
            )

        if index < previous_index:

            raise RuntimeError(
                f"Image order invalid: "
                f"{name}"
            )

        previous_index = index

    log(
        "Validation passed: "
        f"{image_report_path}"
    )

    return True


# ======================================================================
# 26. 生成缺失图片
# ======================================================================

def generate_missing_images(
    report_type,
    report_identifier,
    report_text,
    image_dir
):

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    existing = (
        existing_valid_images(
            image_dir
        )
    )

    log(
        "Existing valid images: "
        f"{existing}"
    )

    missing = (
        determine_missing_images(
            image_dir
        )
    )

    if not missing:

        log(
            "Required images already exist."
        )

        log(
            "No AGNES generation needed."
        )

        return

    log(
        "Missing required images: "
        f"{missing}"
    )

    blocks = split_markdown_blocks(
        report_text
    )

    total_interior_images = (
        max(
            1,
            len(
                [
                    x
                    for x in missing
                    if x != "首图.png"
                ]
            )
        )
    )

    for image_name in missing:

        log("-" * 70)

        log(
            f"Preparing visual story: "
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

                image_number = int(
                    match.group(1)
                )

            else:

                image_number = 1

            visual_context = (
                get_visual_context_for_position(
                    blocks,
                    image_number,
                    total_interior_images
                )
            )

        # ----------------------------------------------------------
        # 日志：让 GitHub Actions 明确显示
        # 当前到底选了什么视觉上下文。
        # ----------------------------------------------------------

        log(
            "VISUAL STORY SELECTED"
        )

        log(
            truncate_text(
                visual_context,
                500
            )
        )

        prompt = build_image_prompt(
            report_type=report_type,
            report_identifier=report_identifier,
            image_name=image_name,
            visual_context=visual_context,
        )

        log(
            "Prompt prepared."
        )

        # ----------------------------------------------------------
        # AGNES
        # ----------------------------------------------------------

        image_url = generate_image(
            prompt
        )

        # ----------------------------------------------------------
        # 下载
        # ----------------------------------------------------------

        log(
            "Downloading generated image..."
        )

        image_data = download_image(
            image_url
        )

        # ----------------------------------------------------------
        # 保存
        # ----------------------------------------------------------

        target_path = (
            image_dir
            / image_name
        )

        atomic_write_bytes(
            target_path,
            image_data
        )

        # ----------------------------------------------------------
        # 立即验证
        # ----------------------------------------------------------

        if not is_valid_png(
            target_path
        ):

            raise RuntimeError(
                "Generated image failed PNG validation: "
                f"{target_path}"
            )

        log(
            "IMAGE SAVED SUCCESSFULLY"
        )

        log(
            f"Path: {target_path}"
        )

        log(
            f"Size: "
            f"{target_path.stat().st_size} bytes"
        )

        # ----------------------------------------------------------
        # 每张图片完成后立即落盘。
        # ----------------------------------------------------------

        time.sleep(
            REQUEST_INTERVAL_SECONDS
        )


# ======================================================================
# 27. 处理日报
# ======================================================================

def process_daily_report(
    day
):

    report_path = (
        daily_report_path(
            day
        )
    )

    log("=" * 70)

    log(
        f"DAILY REPORT: "
        f"{day.isoformat()}"
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

    image_dir = (
        daily_image_dir(
            day
        )
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
    # 带图报告
    # --------------------------------------------------------------

    image_report_path = (
        report_path.with_name(
            report_path.stem
            + "_带图.md"
        )
    )

    image_markdown = (
        build_image_markdown(
            report_path=report_path,
            original_text=original_text,
            image_dir=image_dir,
        )
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
        "DAILY IMAGE REPORT READY"
    )

    log(
        f"Path: {image_report_path}"
    )

    return True


# ======================================================================
# 28. 处理周报
# ======================================================================

def process_weekly_report(
    week_string
):

    report_path = (
        weekly_report_path(
            week_string
        )
    )

    log("=" * 70)

    log(
        f"WEEKLY REPORT: "
        f"{week_string}"
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

    image_dir = (
        weekly_image_dir(
            week_string
        )
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # 图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="WEEKLY REPORT",
        report_identifier=week_string,
        report_text=original_text,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 带图报告
    # --------------------------------------------------------------

    image_report_path = (
        report_path.with_name(
            report_path.stem
            + "_带图.md"
        )
    )

    image_markdown = (
        build_image_markdown(
            report_path=report_path,
            original_text=original_text,
            image_dir=image_dir,
        )
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
        "WEEKLY IMAGE REPORT READY"
    )

    log(
        f"Path: {image_report_path}"
    )

    return True


# ======================================================================
# 29. Main
# ======================================================================

def main():

    log("=" * 70)

    log(
        "748686 KNOWLEDGE IMAGE GENERATOR V4.1"
    )

    log(
        "ONE IMAGE = ONE SCENE = ONE VISUAL STORY"
    )

    log("=" * 70)

    today = utc_today()

    day_before = (
        today
        - timedelta(days=2)
    )

    yesterday = (
        today
        - timedelta(days=1)
    )

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
    # 日报
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
    # ==============================================================

    weekly_weeks = []

    for day in [
        day_before,
        yesterday,
        today,
    ]:

        week_string = (
            iso_week_string(
                day
            )
        )

        if (
            week_string
            not in weekly_weeks
        ):

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
    # 最终
    # ==============================================================

    log("=" * 70)

    log(
        "IMAGE GENERATION FINISHED"
    )

    log(
        f"Daily processed  : "
        f"{processed_daily}"
    )

    log(
        f"Weekly processed : "
        f"{processed_weekly}"
    )

    log(
        f"Failed           : "
        f"{failed}"
    )

    log("=" * 70)

    # --------------------------------------------------------------
    # 保持 0：
    #
    # 单个日报/周报失败不阻断其他报告。
    # 已成功落盘的结果仍然可以被 YAML 提交。
    # --------------------------------------------------------------

    return 0


# ======================================================================
# 30. Entry
# ======================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )
