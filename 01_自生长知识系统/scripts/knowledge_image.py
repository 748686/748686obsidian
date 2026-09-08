#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V4.1
======================================================================

V4.1 核心：

1. 新闻锚定
2. 一图一个场景
3. 单一地点
4. 单一时刻
5. 单一镜头
6. 单一视觉中心
7. 禁止拼图 / 格子 / 分屏
8. 禁止中文 / 英文 / Logo / 水印 / 招牌等文字
9. 生成后进行本地视觉结构质检
10. 不合格自动删除并重新生成
11. 最多自动重试 MAX_GENERATION_ATTEMPTS 次
12. 合格后才原子写入正式文件
13. 原始 Markdown 永远不修改
14. *_带图.md 单独生成
15. 首图 + 插图穿插正文
16. UTC
17. 日报：前天 / 昨天 / 今天
18. 周报：对应 ISO Week，去重
19. 修复 daily_image_dir / weekly_image_dir
20. 增强完整运行日志
======================================================================
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"

DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# AGNES
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


# ======================================================================
# GENERATION CONTROL
# ======================================================================

MAX_GENERATION_ATTEMPTS = 5

RETRY_SLEEP_SECONDS = 2


# ======================================================================
# IMAGE CONTRACT
# ======================================================================

IMAGE_NAMES = [
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
]

MIN_IMAGE_COUNT = 3
MAX_IMAGE_COUNT = 4


# ======================================================================
# OPTIONAL IMAGE ANALYSIS
# ======================================================================

try:

    from PIL import Image

    PIL_AVAILABLE = True

except Exception:

    PIL_AVAILABLE = False


# ======================================================================
# LOG
# ======================================================================

def log(message):

    print(
        message,
        flush=True
    )


# ======================================================================
# UTC
# ======================================================================

def utc_today():

    return datetime.now(
        timezone.utc
    ).date()


# ======================================================================
# IMAGE DIRECTORY
# ======================================================================

def daily_image_dir(
    target_date
):
    """
    日报图片目录：

    04_图片/日报/YYYY-MM-DD/
    """

    path = (
        DAILY_IMAGE_ROOT
        / target_date.strftime("%Y-%m-%d")
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


def weekly_image_dir(
    year,
    week
):
    """
    周报图片目录：

    04_图片/周报/YYYY-Wxx/
    """

    path = (
        WEEKLY_IMAGE_ROOT
        / f"{year}-W{week:02d}"
    )

    path.mkdir(
        parents=True,
        exist_ok=True
    )

    return path


# ======================================================================
# MARKDOWN CLEAN
# ======================================================================

def clean_markdown_text(
    text
):

    if not text:

        return ""

    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        " ",
        text
    )

    text = re.sub(
        r"\[[^\]]+\]\([^)]+\)",
        " ",
        text
    )

    text = re.sub(
        r"<[^>]+>",
        " ",
        text
    )

    text = re.sub(
        r"`{1,3}.*?`{1,3}",
        " ",
        text,
        flags=re.S
    )

    text = re.sub(
        r"[*_~]+",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ======================================================================
# REPORT
# ======================================================================

def find_daily_report(
    target_date
):

    path = (
        DAILY_ROOT
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / f"{target_date:%Y-%m-%d}.md"
    )

    log(
        f"Daily report path: {path}"
    )

    if path.exists():

        log(
            "Daily report: FOUND"
        )

        return path

    log(
        "Daily report: NOT FOUND"
    )

    return None


def find_weekly_report(
    year,
    week
):

    path = (
        WEEKLY_ROOT
        / str(year)
        / f"W{week:02d}.md"
    )

    log(
        f"Weekly report path: {path}"
    )

    if path.exists():

        log(
            "Weekly report: FOUND"
        )

        return path

    log(
        "Weekly report: NOT FOUND"
    )

    return None


def read_report(
    path
):

    content = path.read_text(
        encoding="utf-8"
    )

    log(
        f"Report size: "
        f"{len(content)} characters"
    )

    return content


def extract_report_title(
    content
):

    for line in content.splitlines():

        s = line.strip()

        if not s:

            continue

        match = re.match(
            r"^\s*#{1,6}\s+(.+?)\s*$",
            s
        )

        if match:

            return clean_markdown_text(
                match.group(1)
            )

    return "Knowledge Report"


# ======================================================================
# NEWS EXTRACTION
# ======================================================================

def is_noise_heading(
    text
):

    t = clean_markdown_text(
        text
    )

    if not t:

        return True

    noise = [
        "日报",
        "周报",
        "摘要",
        "总结",
        "分析",
        "趋势",
        "目录",
        "概览",
        "说明",
        "来源",
        "参考",
        "核心观点",
        "免责声明",
        "运行信息",
        "系统信息",
    ]

    for keyword in noise:

        if t == keyword:

            return True

        if t.startswith(
            keyword + ":"
        ):

            return True

        if t.startswith(
            keyword + "："
        ):

            return True

    return False


def split_sections_by_headings(
    content
):

    sections = []

    current_title = None
    current_lines = []

    for line in content.splitlines():

        match = re.match(
            r"^\s*#{1,6}\s+(.+?)\s*$",
            line
        )

        if match:

            if current_title is not None:

                sections.append({
                    "title":
                        clean_markdown_text(
                            current_title
                        ),
                    "content":
                        "\n".join(
                            current_lines
                        ).strip(),
                })

            current_title = match.group(1)

            current_lines = []

        else:

            if current_title is not None:

                current_lines.append(
                    line
                )

    if current_title is not None:

        sections.append({
            "title":
                clean_markdown_text(
                    current_title
                ),
            "content":
                "\n".join(
                    current_lines
                ).strip(),
        })

    return sections


def extract_news_items(
    content
):

    items = []

    sections = (
        split_sections_by_headings(
            content
        )
    )

    for section in sections:

        title = section["title"]

        if is_noise_heading(
            title
        ):

            continue

        body = clean_markdown_text(
            section["content"]
        )

        if len(title) < 4:

            continue

        if not body:

            continue

        body = body[:5000]

        items.append({
            "title": title,
            "body": body,
            "text":
                title
                + "\n"
                + body,
        })

    # --------------------------------------------------------------
    # 编号新闻兜底
    # --------------------------------------------------------------

    if len(items) < 2:

        current = None

        for line in content.splitlines():

            match = re.match(
                r"^\s*(?:\d+[\.\、\)]|[-•])\s+(.+?)\s*$",
                line
            )

            if match:

                title = clean_markdown_text(
                    match.group(1)
                )

                if len(title) >= 8:

                    current = {
                        "title": title,
                        "body": "",
                        "text": title,
                    }

                    items.append(
                        current
                    )

            elif current:

                text = clean_markdown_text(
                    line
                )

                if text:

                    current["body"] += (
                        " " + text
                    )

                    current["text"] = (
                        current["title"]
                        + "\n"
                        + current["body"]
                    )

    return items


# ======================================================================
# NEWS PLAN
# ======================================================================

def normalize_news_text(
    text,
    limit=2600
):

    text = clean_markdown_text(
        text
    )

    text = re.sub(
        r"https?://\S+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()[:limit]


def build_image_plan(
    report_content
):

    news_items = extract_news_items(
        report_content
    )

    log(
        f"Detected news items: "
        f"{len(news_items)}"
    )

    for i, item in enumerate(
        news_items[-10:],
        start=max(
            1,
            len(news_items) - 9
        )
    ):

        log(
            f"NEWS {i}: "
            f"{item['title'][:120]}"
        )

    if not news_items:

        raise RuntimeError(
            "No news items detected."
        )

    latest_index = (
        len(news_items) - 1
    )

    latest = news_items[
        latest_index
    ]

    previous = []

    for i in range(
        latest_index - 1,
        -1,
        -1
    ):

        previous.append(
            news_items[i]
        )

        if len(previous) >= 2:

            break

    plan = []

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    plan.append({
        "image_name":
            "首图.png",
        "news":
            latest,
        "role":
            "latest",
        "news_index":
            latest_index + 1,
    })

    # --------------------------------------------------------------
    # 插图1
    # --------------------------------------------------------------

    plan.append({
        "image_name":
            "插图1.png",
        "news":
            latest,
        "role":
            "latest_second_view",
        "news_index":
            latest_index + 1,
    })

    # --------------------------------------------------------------
    # 插图2
    # --------------------------------------------------------------

    if len(previous) >= 1:

        plan.append({
            "image_name":
                "插图2.png",
            "news":
                previous[0],
            "role":
                "second_news",
            "news_index":
                latest_index,
        })

    # --------------------------------------------------------------
    # 插图3
    # --------------------------------------------------------------

    if len(previous) >= 2:

        plan.append({
            "image_name":
                "插图3.png",
            "news":
                previous[1],
            "role":
                "third_news",
            "news_index":
                latest_index - 1,
        })

    return plan


# ======================================================================
# PROMPT
# ======================================================================

def build_image_prompt(
    image_name,
    plan_item,
    attempt
):

    news = plan_item["news"]

    title = normalize_news_text(
        news.get("title", ""),
        500
    )

    body = normalize_news_text(
        news.get("body", ""),
        1800
    )

    role = plan_item["role"]

    retry_instruction = ""

    if attempt >= 2:

        retry_instruction = """
THIS IS A RETRY.

The previous candidate was rejected.

Make the composition dramatically simpler.

Use fewer visible objects.
Use one dominant subject.
Use a plain natural background.
Use one physical location.
Use one photographic moment.

Do NOT attempt to show the whole news story.
"""

    if attempt >= 3:

        retry_instruction += """
SECOND RETRY WARNING.

Do not create any editorial graphic composition.

Think like a photojournalist who has only ONE
camera frame available.

Take ONE photograph.
Nothing else.
"""

    if attempt >= 4:

        retry_instruction += """
FINAL RETRY MODE.

Use an extremely simple documentary photograph.

ONE subject.
ONE action.
ONE location.
ONE moment.

Avoid every object that can contain writing.
Avoid every visual structure that can become
a panel, grid, poster, collage, or infographic.
"""

    if role == "latest":

        role_instruction = """
This is the COVER IMAGE.

It MUST represent the latest news item below.

Choose the clearest single physical scene
that a professional photojournalist could
actually photograph while covering this event.
"""

    elif role == "latest_second_view":

        role_instruction = """
This is the SECOND IMAGE for the SAME latest news.

It MUST remain about exactly the same news event.

Use a different single camera position or
different physical moment within that same event.

Do not introduce another event.
Do not introduce another location.
"""

    else:

        role_instruction = """
This image MUST represent the specific news item below.

Do not use the whole report as visual inspiration.

Do not combine this news item with other news.
"""

    prompt = f"""
IMPORTANT: GENERATE ONE NORMAL PHOTOGRAPH.

{role_instruction}

NEWS TITLE:
{title}

NEWS FACTS:
{body}

The text above is the ONLY factual source for the scene.

The image must visibly correspond to this news.

Do not generate an unrelated generic image.

============================================================
SINGLE SCENE CONTRACT
============================================================

ONE photograph.

ONE physical location.

ONE moment in time.

ONE camera.

ONE camera viewpoint.

ONE continuous environment.

ONE dominant subject.

ONE main action.

ONE visual center.

The viewer must immediately perceive this as
ONE ordinary documentary photograph.

============================================================
ABSOLUTELY FORBIDDEN
============================================================

NO collage.

NO grid.

NO tiled image.

NO split screen.

NO multiple panels.

NO four panels.

NO triptych.

NO diptych.

NO montage.

NO storyboard.

NO infographic.

NO poster.

NO newspaper-style layout.

NO news board.

NO multiple photographs.

NO multiple frames.

NO multiple scenes.

NO multiple locations.

NO separate mini-scenes.

NO before-and-after.

NO timeline.

NO visual summary.

NO symbolic collection of objects.

============================================================
TEXT-FREE PHOTOGRAPH
============================================================

The photograph must contain ZERO readable writing.

Do not show:

Chinese characters.

Hanzi.

Chinese text.

English letters.

English words.

Numbers used as labels.

Headlines.

Titles.

Captions.

Subtitles.

Logos.

Watermarks.

Brand names.

Signs.

Road signs.

Shop signs.

Building signs.

Billboards.

Posters.

Newspapers.

Books.

Documents.

Printed papers.

Packaging.

Labels.

Badges.

Banners.

Screens.

Phones.

Computer monitors.

Televisions.

Digital displays.

Charts.

Graphs.

Diagrams.

Maps containing labels.

UI.

Interfaces.

Menus.

Advertisements.

If an object could naturally contain writing,
DO NOT include that object.

============================================================
COMPOSITION
============================================================

Use a simple natural photographic composition.

Keep the background quiet.

Keep secondary objects subordinate.

Do not create repeated rectangular shapes.

Do not create rows of panels.

Do not create windows that look like separate photographs.

Do not create screens.

Do not create picture frames.

Do not create posters.

Do not create newspaper pages.

Do not create multiple visible displays.

============================================================
PHOTOGRAPHIC STYLE
============================================================

Realistic documentary news photography.

Professional photojournalism.

Photorealistic.

Natural lighting.

Natural perspective.

Real physical environment.

Credible human anatomy.

Restrained cinematic quality.

No illustration.

No cartoon.

No fantasy.

No surrealism.

No graphic design.

No infographic aesthetic.

{retry_instruction}

============================================================
FINAL CHECK
============================================================

Before generating the photograph, internally verify:

ONE scene.
ONE location.
ONE moment.
ONE camera.
ONE visual center.
ZERO readable text.
ZERO panels.
ZERO grids.
ZERO collage.

If any condition fails,
simplify the photograph.

Generate ONLY the photograph.
"""

    return prompt


# ======================================================================
# AGNES API
# ======================================================================

def get_api_key():

    key = os.getenv(
        "AGNES_API_KEY",
        ""
    ).strip()

    if not key:

        raise RuntimeError(
            "AGNES_API_KEY is not configured."
        )

    return key


def download_image(
    url
):

    log(
        "Downloading generated image..."
    )

    request = Request(
        url,
        headers={
            "User-Agent":
                "748686-Knowledge-Image-V4.1"
        }
    )

    with urlopen(
        request,
        timeout=REQUEST_TIMEOUT
    ) as response:

        data = response.read()

    log(
        f"Downloaded bytes: "
        f"{len(data)}"
    )

    if not data.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):

        raise RuntimeError(
            "Downloaded file is not PNG."
        )

    return data


def generate_image(
    prompt
):

    api_key = get_api_key()

    payload = {
        "model":
            AGNES_IMAGE_MODEL,
        "prompt":
            prompt,
        "size":
            IMAGE_SIZE,
        "ratio":
            IMAGE_RATIO,
        "extra_body": {
            "response_format":
                "url"
        },
    }

    body = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    log(
        "Calling AGNES image API..."
    )

    log(
        f"AGNES MODEL: "
        f"{AGNES_IMAGE_MODEL}"
    )

    log(
        f"IMAGE SIZE: "
        f"{IMAGE_SIZE}"
    )

    log(
        f"IMAGE RATIO: "
        f"{IMAGE_RATIO}"
    )

    request = Request(
        AGNES_API_URL,
        data=body,
        headers={
            "Authorization":
                f"Bearer {api_key}",
            "Content-Type":
                "application/json",
            "Accept":
                "application/json",
        },
        method="POST",
    )

    try:

        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw = response.read()

    except HTTPError as exc:

        detail = exc.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            f"AGNES HTTP {exc.code}: "
            f"{detail[:2000]}"
        )

    except URLError as exc:

        raise RuntimeError(
            f"AGNES network error: {exc}"
        )

    log(
        f"AGNES response bytes: "
        f"{len(raw)}"
    )

    data = json.loads(
        raw.decode("utf-8")
    )

    image_url = None

    if isinstance(
        data,
        dict
    ):

        items = data.get(
            "data"
        )

        if (
            isinstance(items, list)
            and items
            and isinstance(
                items[0],
                dict
            )
        ):

            image_url = items[0].get(
                "url"
            )

    if not image_url:

        raise RuntimeError(
            "No data[0].url in AGNES response."
        )

    log(
        "AGNES image URL received."
    )

    return download_image(
        image_url
    )


# ======================================================================
# ATOMIC WRITE
# ======================================================================

def atomic_write_bytes(
    path,
    data
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        "." + path.name + ".tmp"
    )

    with open(
        tmp,
        "wb"
    ) as f:

        f.write(data)

        f.flush()

        os.fsync(
            f.fileno()
        )

    os.replace(
        tmp,
        path
    )


# ======================================================================
# PNG VALIDATION
# ======================================================================

def is_valid_png(
    path
):

    try:

        if not path.exists():

            return False

        if path.stat().st_size < 100:

            return False

        with open(
            path,
            "rb"
        ) as f:

            signature = f.read(8)

        return (
            signature
            == b"\x89PNG\r\n\x1a\n"
        )

    except Exception:

        return False


# ======================================================================
# VISUAL QUALITY CHECK
# ======================================================================

def image_dimensions(
    image_path
):

    if not PIL_AVAILABLE:

        return None

    try:

        with Image.open(
            image_path
        ) as img:

            return img.size

    except Exception:

        return None


def detect_extreme_grid_structure(
    image_path
):

    if not PIL_AVAILABLE:

        return False, (
            "Pillow unavailable; "
            "grid detector skipped"
        )

    try:

        with Image.open(
            image_path
        ) as img:

            img = img.convert(
                "L"
            )

            width, height = img.size

            if width < 100 or height < 100:

                return True, (
                    "image too small"
                )

            img.thumbnail(
                (240, 240)
            )

            pixels = img.load()

            w, h = img.size

            vertical_scores = []

            for x in range(w):

                dark = 0

                for y in range(h):

                    if pixels[x, y] < 35:

                        dark += 1

                vertical_scores.append(
                    dark / max(h, 1)
                )

            horizontal_scores = []

            for y in range(h):

                dark = 0

                for x in range(w):

                    if pixels[x, y] < 35:

                        dark += 1

                horizontal_scores.append(
                    dark / max(w, 1)
                )

            strong_vertical = sum(
                1
                for score
                in vertical_scores
                if score > 0.72
            )

            strong_horizontal = sum(
                1
                for score
                in horizontal_scores
                if score > 0.72
            )

            if strong_vertical >= 2:

                return True, (
                    "possible multi-panel "
                    "vertical separators"
                )

            if strong_horizontal >= 2:

                return True, (
                    "possible multi-panel "
                    "horizontal separators"
                )

            return False, (
                "grid structure not obvious"
            )

    except Exception as exc:

        return False, (
            f"grid detector error: {exc}"
        )


def detect_text_like_structure(
    image_path
):

    if not PIL_AVAILABLE:

        return False, (
            "Pillow unavailable; "
            "text detector skipped"
        )

    try:

        with Image.open(
            image_path
        ) as img:

            img = img.convert(
                "L"
            )

            img.thumbnail(
                (500, 500)
            )

            w, h = img.size

            if w < 50 or h < 50:

                return False, (
                    "image too small"
                )

            small_regions = 0

            step_x = max(
                8,
                w // 50
            )

            step_y = max(
                8,
                h // 50
            )

            for y in range(
                0,
                h - step_y,
                step_y
            ):

                for x in range(
                    0,
                    w - step_x,
                    step_x
                ):

                    values = []

                    for yy in range(
                        y,
                        min(
                            y + step_y,
                            h
                        )
                    ):

                        for xx in range(
                            x,
                            min(
                                x + step_x,
                                w
                            )
                        ):

                            values.append(
                                img.getpixel(
                                    (xx, yy)
                                )
                            )

                    if not values:

                        continue

                    mean = (
                        sum(values)
                        /
                        len(values)
                    )

                    variance = (
                        sum(
                            (
                                v - mean
                            ) ** 2
                            for v in values
                        )
                        /
                        len(values)
                    )

                    if variance > 5000:

                        small_regions += 1

            total_regions = max(
                1,
                (
                    w // step_x
                )
                *
                (
                    h // step_y
                )
            )

            ratio = (
                small_regions
                /
                total_regions
            )

            if ratio > 0.62:

                return True, (
                    "unusually dense "
                    "text-like texture"
                )

            return False, (
                "text-like structure "
                "not obvious"
            )

    except Exception as exc:

        return False, (
            f"text detector error: {exc}"
        )


def visual_quality_check(
    image_path
):

    reasons = []

    if not is_valid_png(
        image_path
    ):

        return False, [
            "invalid PNG"
        ]

    dimensions = image_dimensions(
        image_path
    )

    if dimensions:

        width, height = dimensions

        log(
            f"Image dimensions: "
            f"{width}x{height}"
        )

        if width < 512 or height < 512:

            reasons.append(
                "image resolution too small"
            )

    grid_bad, grid_reason = (
        detect_extreme_grid_structure(
            image_path
        )
    )

    log(
        f"Grid check: "
        f"{grid_reason}"
    )

    if grid_bad:

        reasons.append(
            grid_reason
        )

    text_bad, text_reason = (
        detect_text_like_structure(
            image_path
        )
    )

    log(
        f"Text-like check: "
        f"{text_reason}"
    )

    if text_bad:

        reasons.append(
            text_reason
        )

    if reasons:

        return False, reasons

    return True, [
        "basic visual structure check passed"
    ]


# ======================================================================
# GENERATE VERIFIED IMAGE
# ======================================================================

def generate_verified_image(
    image_path,
    image_name,
    plan_item
):

    for attempt in range(
        1,
        MAX_GENERATION_ATTEMPTS + 1
    ):

        log("")
        log(
            "=" * 60
        )

        log(
            f"GENERATE "
            f"{image_name} "
            f"ATTEMPT "
            f"{attempt}/"
            f"{MAX_GENERATION_ATTEMPTS}"
        )

        log(
            f"Target: {image_path}"
        )

        prompt = build_image_prompt(
            image_name,
            plan_item,
            attempt
        )

        try:

            image_bytes = generate_image(
                prompt
            )

            candidate_path = (
                image_path.with_name(
                    "."
                    + image_path.stem
                    + ".candidate.png"
                )
            )

            atomic_write_bytes(
                candidate_path,
                image_bytes
            )

            log(
                f"Candidate saved: "
                f"{candidate_path}"
            )

            passed, reasons = (
                visual_quality_check(
                    candidate_path
                )
            )

            if passed:

                log(
                    "VISUAL CHECK: PASS"
                )

                atomic_write_bytes(
                    image_path,
                    image_bytes
                )

                try:

                    candidate_path.unlink()

                except Exception:

                    pass

                if not is_valid_png(
                    image_path
                ):

                    raise RuntimeError(
                        "Final PNG validation failed."
                    )

                log(
                    f"ACCEPTED: "
                    f"{image_path}"
                )

                return True

            log(
                "VISUAL CHECK: FAIL"
            )

            for reason in reasons:

                log(
                    f"  REJECT: {reason}"
                )

            try:

                candidate_path.unlink()

            except Exception:

                pass

            if attempt < MAX_GENERATION_ATTEMPTS:

                log(
                    f"Retrying in "
                    f"{RETRY_SLEEP_SECONDS} seconds..."
                )

                time.sleep(
                    RETRY_SLEEP_SECONDS
                )

        except Exception as exc:

            log(
                f"Generation attempt failed: "
                f"{exc}"
            )

            if attempt < MAX_GENERATION_ATTEMPTS:

                log(
                    f"Retrying in "
                    f"{RETRY_SLEEP_SECONDS} seconds..."
                )

                time.sleep(
                    RETRY_SLEEP_SECONDS
                )

    raise RuntimeError(
        f"Unable to generate a verified "
        f"single-scene image after "
        f"{MAX_GENERATION_ATTEMPTS} attempts: "
        f"{image_name}"
    )


# ======================================================================
# EXISTING IMAGES
# ======================================================================

def get_existing_images(
    image_dir
):

    result = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if is_valid_png(path):

            result.append(name)

    return result


def determine_missing_images(
    image_dir
):

    existing = (
        get_existing_images(
            image_dir
        )
    )

    missing = []

    for name in IMAGE_NAMES[
        :MIN_IMAGE_COUNT
    ]:

        if name not in existing:

            missing.append(name)

    return existing, missing


# ======================================================================
# GENERATE MISSING
# ======================================================================

def generate_missing_images(
    image_dir,
    report_content
):

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    log(
        f"Image directory: "
        f"{image_dir}"
    )

    existing, missing = (
        determine_missing_images(
            image_dir
        )
    )

    log("")
    log("=" * 70)
    log("VERIFIED IMAGE GENERATION")
    log("=" * 70)

    log(
        f"Existing valid: "
        f"{len(existing)}"
    )

    if existing:

        for name in existing:

            log(
                f"  EXISTING: {name}"
            )

    log(
        f"Missing: "
        f"{len(missing)}"
    )

    if missing:

        for name in missing:

            log(
                f"  MISSING: {name}"
            )

    if not missing:

        log(
            "No image generation required."
        )

        return

    plan = build_image_plan(
        report_content
    )

    plan_map = {
        item["image_name"]:
            item
        for item in plan
    }

    for image_name in missing:

        plan_item = plan_map.get(
            image_name
        )

        if not plan_item:

            raise RuntimeError(
                f"No image plan for "
                f"{image_name}"
            )

        news = plan_item["news"]

        log("")
        log("-" * 70)

        log(
            f"IMAGE: {image_name}"
        )

        log(
            f"NEWS INDEX: "
            f"{plan_item['news_index']}"
        )

        log(
            f"NEWS ROLE: "
            f"{plan_item['role']}"
        )

        log(
            f"NEWS TITLE: "
            f"{news['title'][:200]}"
        )

        target = (
            image_dir
            / image_name
        )

        generate_verified_image(
            target,
            image_name,
            plan_item
        )


# ======================================================================
# MARKDOWN INSERTION
# ======================================================================

def split_markdown_blocks(
    content
):

    return re.split(
        r"\n\s*\n",
        content.strip()
    )


def is_good_insertion_block(
    block
):

    s = block.strip()

    if not s:

        return False

    if re.match(
        r"^\s*#{1,6}\s+",
        s
    ):

        return False

    if re.fullmatch(
        r"!\[[^\]]*\]\([^)]+\)",
        s
    ):

        return False

    if s.startswith("<"):

        return False

    if "|" in s:

        return False

    return True


def get_insertion_positions(
    blocks,
    image_count
):

    good = [
        i
        for i, block
        in enumerate(blocks)
        if is_good_insertion_block(
            block
        )
    ]

    interior_count = (
        image_count - 1
    )

    if not good:

        return []

    if len(good) <= interior_count:

        return good

    positions = []

    for i in range(
        interior_count
    ):

        ratio = (
            i + 1
        ) / (
            interior_count + 1
        )

        index = int(
            ratio
            *
            (
                len(good) - 1
            )
        )

        p = good[index]

        if p not in positions:

            positions.append(p)

    return positions


def make_relative_image_path(
    markdown_path,
    image_path
):

    relative = os.path.relpath(
        image_path,
        start=markdown_path.parent
    )

    return relative.replace(
        os.sep,
        "/"
    )


def build_image_markdown(
    markdown_path,
    original_content,
    image_dir
):

    images = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if is_valid_png(path):

            images.append(path)

    if len(images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "Less than 3 valid images."
        )

    if len(images) > MAX_IMAGE_COUNT:

        images = images[
            :MAX_IMAGE_COUNT
        ]

    cover = image_dir / "首图.png"

    if not is_valid_png(cover):

        raise RuntimeError(
            "首图.png invalid."
        )

    blocks = split_markdown_blocks(
        original_content
    )

    output = []

    cover_relative = (
        make_relative_image_path(
            markdown_path,
            cover
        )
    )

    output.append(
        f"![首图]({cover_relative})"
    )

    output.append("")

    interior = [
        image
        for image in images
        if image.name != "首图.png"
    ]

    positions = (
        get_insertion_positions(
            blocks,
            len(images)
        )
    )

    position_map = {}

    for p, image in zip(
        positions,
        interior
    ):

        position_map[p] = image

    used = set(
        position_map.values()
    )

    remaining = [
        image
        for image in interior
        if image not in used
    ]

    for index, block in enumerate(
        blocks
    ):

        output.append(block)

        image = position_map.get(
            index
        )

        if image:

            relative = (
                make_relative_image_path(
                    markdown_path,
                    image
                )
            )

            output.append("")

            output.append(
                f"![{image.stem}]"
                f"({relative})"
            )

            output.append("")

    for image in remaining:

        relative = (
            make_relative_image_path(
                markdown_path,
                image
            )
        )

        output.append("")

        output.append(
            f"![{image.stem}]"
            f"({relative})"
        )

        output.append("")

    return "\n\n".join(
        output
    ).strip() + "\n"


# ======================================================================
# IMAGE REPORT
# ======================================================================

def build_image_report_path(
    report_path
):

    return report_path.with_name(
        report_path.stem
        + "_带图.md"
    )


def validate_image_order(
    content
):

    expected = [
        "首图.png",
        "插图1.png",
        "插图2.png",
        "插图3.png",
    ]

    found = []

    for name in expected:

        if name in content:

            found.append(name)

    if not found:

        raise RuntimeError(
            "No image references."
        )

    if found[0] != "首图.png":

        raise RuntimeError(
            "Cover is not first."
        )

    positions = [
        expected.index(x)
        for x in found
    ]

    if positions != sorted(
        positions
    ):

        raise RuntimeError(
            "Image order invalid."
        )


def validate_body_interleaving(
    content
):

    pattern = re.compile(
        r"!\[[^\]]*\]\([^)]+"
        r"\.(?:png|jpg|jpeg|webp)"
        r"\)",
        re.I
    )

    parts = pattern.split(
        content
    )

    if len(parts) <= 2:

        return

    for part in parts[1:-1]:

        if part.strip():

            return

    raise RuntimeError(
        "Images are not interleaved."
    )


def validate_image_report(
    markdown_path,
    original_content
):

    content = markdown_path.read_text(
        encoding="utf-8"
    )

    refs = re.findall(
        r"!\[[^\]]*\]\(([^)]+)\)",
        content
    )

    if len(refs) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "Not enough image references."
        )

    for ref in refs:

        path = (
            markdown_path.parent
            / ref
        ).resolve()

        if not path.exists():

            raise RuntimeError(
                f"Missing image: {ref}"
            )

        if not is_valid_png(path):

            raise RuntimeError(
                f"Invalid image: {ref}"
            )

    validate_image_order(
        content
    )

    validate_body_interleaving(
        content
    )

    if not content.lstrip().startswith(
        "![首图]"
    ):

        raise RuntimeError(
            "Cover is not first."
        )


def atomic_write_text(
    path,
    text
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        "." + path.name + ".tmp"
    )

    with open(
        tmp,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

        f.flush()

        os.fsync(
            f.fileno()
        )

    os.replace(
        tmp,
        path
    )


def create_image_report(
    report_path,
    image_dir,
    original_content
):

    output_path = (
        build_image_report_path(
            report_path
        )
    )

    log("")
    log(
        "Creating image Markdown..."
    )

    content = build_image_markdown(
        output_path,
        original_content,
        image_dir
    )

    atomic_write_text(
        output_path,
        content
    )

    validate_image_report(
        output_path,
        original_content
    )

    log(
        f"IMAGE REPORT: "
        f"{output_path}"
    )

    return output_path


# ======================================================================
# DAILY
# ======================================================================

def process_daily_report(
    target_date
):

    log("")
    log("=" * 70)
    log(
        f"DAILY IMAGE: {target_date}"
    )
    log("=" * 70)

    report_path = find_daily_report(
        target_date
    )

    if not report_path:

        log(
            "Daily report not found."
        )

        return False

    log(
        f"Using daily report: "
        f"{report_path}"
    )

    content = read_report(
        report_path
    )

    image_dir = daily_image_dir(
        target_date
    )

    log(
        f"Daily image directory: "
        f"{image_dir}"
    )

    generate_missing_images(
        image_dir,
        content
    )

    create_image_report(
        report_path,
        image_dir,
        content
    )

    log(
        f"DAILY SUCCESS: "
        f"{target_date}"
    )

    return True


# ======================================================================
# WEEKLY
# ======================================================================

def process_weekly_report(
    year,
    week
):

    log("")
    log("=" * 70)
    log(
        f"WEEKLY IMAGE: "
        f"{year}-W{week:02d}"
    )
    log("=" * 70)

    report_path = find_weekly_report(
        year,
        week
    )

    if not report_path:

        log(
            "Weekly report not found."
        )

        return False

    log(
        f"Using weekly report: "
        f"{report_path}"
    )

    content = read_report(
        report_path
    )

    image_dir = weekly_image_dir(
        year,
        week
    )

    log(
        f"Weekly image directory: "
        f"{image_dir}"
    )

    generate_missing_images(
        image_dir,
        content
    )

    create_image_report(
        report_path,
        image_dir,
        content
    )

    log(
        f"WEEKLY SUCCESS: "
        f"{year}-W{week:02d}"
    )

    return True


# ======================================================================
# MAIN
# ======================================================================

def main():

    log("")
    log("=" * 70)
    log(
        "748686 KNOWLEDGE IMAGE ENGINE V4.1"
    )
    log(
        "NEWS ANCHOR + VISUAL QUALITY CHECK"
    )
    log("=" * 70)

    log(
        f"Script directory : {SCRIPT_DIR}"
    )

    log(
        f"System root      : {SYSTEM_ROOT}"
    )

    log(
        f"Daily root       : {DAILY_ROOT}"
    )

    log(
        f"Weekly root      : {WEEKLY_ROOT}"
    )

    log(
        f"Image root       : {IMAGE_ROOT}"
    )

    log(
        f"AGNES API        : {AGNES_API_URL}"
    )

    log(
        f"AGNES model      : {AGNES_IMAGE_MODEL}"
    )

    log(
        f"Pillow available : {PIL_AVAILABLE}"
    )

    today = utc_today()

    day_before = (
        today
        - timedelta(days=2)
    )

    yesterday = (
        today
        - timedelta(days=1)
    )

    daily_dates = [
        day_before,
        yesterday,
        today,
    ]

    log("")
    log(
        f"UTC TODAY  : {today}"
    )

    log(
        f"DAY BEFORE : {day_before}"
    )

    log(
        f"YESTERDAY  : {yesterday}"
    )

    log(
        f"TODAY      : {today}"
    )

    # ==============================================================
    # DAILY
    # ==============================================================

    daily_success = 0
    daily_failed = 0

    for target_date in daily_dates:

        try:

            success = process_daily_report(
                target_date
            )

            if success:

                daily_success += 1

            else:

                log(
                    f"DAILY SKIPPED: "
                    f"{target_date}"
                )

        except Exception as exc:

            daily_failed += 1

            log(
                f"DAILY FAILED "
                f"{target_date}: "
                f"{exc}"
            )

    # ==============================================================
    # WEEKLY
    # ==============================================================

    weeks = []

    for target_date in daily_dates:

        iso = target_date.isocalendar()

        key = (
            iso.year,
            iso.week
        )

        if key not in weeks:

            weeks.append(key)

    log("")
    log(
        f"Unique ISO weeks: "
        f"{len(weeks)}"
    )

    for year, week in weeks:

        try:

            process_weekly_report(
                year,
                week
            )

        except Exception as exc:

            log(
                f"WEEKLY FAILED "
                f"{year}-W{week:02d}: "
                f"{exc}"
            )

    # ==============================================================
    # SUMMARY
    # ==============================================================

    log("")
    log("=" * 70)
    log(
        "KNOWLEDGE IMAGE ENGINE V4.1 FINISHED"
    )
    log("=" * 70)

    log(
        f"Daily success : "
        f"{daily_success}"
    )

    log(
        f"Daily failed  : "
        f"{daily_failed}"
    )

    log(
        f"Weekly count  : "
        f"{len(weeks)}"
    )

    log("=" * 70)

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )
