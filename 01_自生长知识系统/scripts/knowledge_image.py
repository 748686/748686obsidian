#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V5.2
======================================================================

核心目标
----------------------------------------------------------------------

1. UTC 日期
2. 日报处理：前天 / 昨天 / 今天
3. 周报处理：上述日期对应 ISO Week，自动去重

4. 图片目录：

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

5. 原始 Markdown 永远不修改

6. 只生成：

   YYYY-MM-DD_带图.md
   Wxx_带图.md

7. 新闻锚定：

   首图 = 最新真实新闻
   插图1 = 同一新闻的第二视角
   插图2 = 第二条真实新闻
   插图3 = 第三条真实新闻

8. V5.2 无文字新闻插图视觉合同：

   一图
   一场景
   一地点
   一时刻
   一镜头
   一个视觉中心

   图片类型：

   - 真实新闻摄影
   - 纪录片式新闻插图
   - 写实编辑部新闻视觉
   - photorealistic editorial news illustration

   禁止：

   - 拼图
   - 九宫格
   - 分屏
   - 多小场景
   - 蒙太奇
   - 信息图
   - 图表
   - UI
   - Dashboard
   - 新闻版面
   - 报纸版面
   - PPT
   - 海报
   - Logo
   - 水印
   - 标题
   - 标签
   - 注释
   - 图例

   画面不得承载文字信息。

   禁止生成可读：

   - 中文
   - 英文
   - 数字文本
   - 标题
   - 字幕
   - 标签
   - 路牌文字
   - 屏幕文字
   - 报纸文字
   - 书本文字
   - 文件文字
   - 包装文字
   - 横幅文字
   - 制服文字
   - 徽章文字
   - Logo
   - 水印

   注意：

   OCR 不再采用：

       “发现任意一个中文字符 = FAIL”

   而采用：

       “检测到明显、连续、高置信度、具有可读文字特征的文本区域 = FAIL”

9. 图片质量检查：

   Pillow
   +
   Tesseract OCR

10. OCR 主要用于检测“明显可读文字”，
    不把随机纹理、建筑细节、噪声、单个误识别字符当成失败。

11. FORCE_REGENERATE=true：

    强制重新生成本次测试所需图片

======================================================================
"""

from __future__ import annotations

import io
import os
import re
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# Optional dependencies
# ======================================================================

try:
    from PIL import Image, ImageOps, ImageFilter
    PIL_AVAILABLE = True
except Exception:
    Image = None
    ImageOps = None
    ImageFilter = None
    PIL_AVAILABLE = False


try:
    import pytesseract
    from pytesseract import Output
    PYTESSERACT_AVAILABLE = True
except Exception:
    pytesseract = None
    Output = None
    PYTESSERACT_AVAILABLE = False


# ======================================================================
# Environment
# ======================================================================

AGNES_API_KEY = os.getenv("AGNES_API_KEY", "").strip()

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"
AGNES_IMAGE_URL = f"{AGNES_BASE_URL}/images/generations"
AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

IMAGE_TIMEOUT = 180

FORCE_REGENERATE = (
    os.getenv("FORCE_REGENERATE", "false").lower()
    in ("1", "true", "yes", "on")
)

MAX_IMAGE_RETRIES = 5

MIN_IMAGE_COUNT = 3
TARGET_IMAGE_COUNT = 4

IMAGE_NAMES = (
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
)


# ======================================================================
# V5.2 Visual Contract
# ======================================================================

VISUAL_CONTRACT = """
ABSOLUTE VISUAL CONTRACT
========================

Create ONE realistic news photograph / editorial news illustration.

This is NOT an infographic.

This is NOT a chart.

This is NOT a diagram.

This is NOT a presentation.

This is NOT a poster.

This is NOT a newspaper page.

The final result must look like a professional,
realistic documentary photograph suitable for a serious news report.

ONE IMAGE
ONE SCENE
ONE LOCATION
ONE MOMENT
ONE CAMERA SHOT
ONE VISUAL CENTER

The image communicates the event through physical reality only:

- people
- buildings
- vehicles
- infrastructure
- objects
- weather
- landscape
- physical action
- realistic lighting
- realistic spatial relationships
- historically / geographically plausible surroundings

DO NOT communicate the event through written information.

ABSOLUTELY NO READABLE TEXT.

The image must contain no readable:

- Chinese characters
- Hanzi
- English words
- English sentences
- numbers used as text
- titles
- captions
- subtitles
- labels
- annotations
- legends
- watermarks
- logos
- brand names
- road signs
- street signs
- billboards
- screens
- newspapers
- books
- documents
- menus
- packaging
- banners
- badges
- uniforms containing text

Avoid objects whose main purpose is displaying text.

If a real-world object normally contains text,
make its surface blank, blurred, turned away,
out of focus, cropped, or otherwise unreadable.

The image must NOT contain fake gibberish text either.

Do not create pseudo-writing.
Do not create random letters.
Do not create fake Chinese characters.
Do not create fake newspaper typography.

The source text supplied to the model is SEMANTIC CONTEXT ONLY.

NEVER copy the source text.
NEVER typeset the source text.
NEVER translate the source text into visible text.
NEVER visualize the source document itself.

Do not create a document containing the source text.

Do not create:
- infographic
- chart
- diagram
- timeline
- map with labels
- flowchart
- dashboard
- UI
- slide
- poster
- collage
- grid
- contact sheet
- split screen
- diptych
- triptych
- montage
- multiple panels
- multiple mini-scenes

STYLE

Professional documentary photography.

Photorealistic.

Realistic physical materials.

Natural human proportions.

Natural lighting.

Credible journalistic composition.

Restrained cinematic quality.

Serious editorial tone.

No sensationalism.

No fantasy.

No surrealism.

No decorative typography.

No text-based visual storytelling.

The final image should look like a photograph captured by
a professional news photographer at the actual event.
"""


# ======================================================================
# Utility
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def clean_text(text: str) -> str:

    if not text:
        return ""

    text = str(text)

    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    text = re.sub(
        r"`+",
        "",
        text,
    )

    text = re.sub(
        r"[*_~]+",
        "",
        text,
    )

    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    text = text.replace(
        "\u200b",
        "",
    )

    text = text.replace(
        "\ufeff",
        "",
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def strip_heading_prefix(text: str) -> str:

    text = clean_text(text)

    text = re.sub(
        r"^\s{0,3}#{1,6}\s*",
        "",
        text,
    )

    text = re.sub(
        r"^\s*(?:[-*+]\s+)",
        "",
        text,
    )

    text = re.sub(
        r"^\s*\d+\s*[\.\、\)]\s*",
        "",
        text,
    )

    return text.strip()


def normalize_title(text: str) -> str:

    text = strip_heading_prefix(text)

    for emoji in (
        "📚",
        "📊",
        "🗓️",
        "⚠️",
        "🔴",
        "🟡",
        "🟢",
    ):
        text = text.replace(
            emoji,
            "",
        )

    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


def short_hash(text: str) -> str:

    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()[:12]


# ======================================================================
# Date
# ======================================================================

def utc_today() -> datetime:

    return datetime.now(
        timezone.utc
    )


def target_dates() -> list:

    today = utc_today().date()

    return [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]


# ======================================================================
# Report directories
# ======================================================================

def daily_image_dir(target_date) -> Path:

    return (
        DAILY_IMAGE_ROOT
        / target_date.strftime("%Y-%m-%d")
    )


def weekly_image_dir(
    year: int,
    week: int,
) -> Path:

    return (
        WEEKLY_IMAGE_ROOT
        / f"{year}-W{week:02d}"
    )


# ======================================================================
# Paths
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"

DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# Report discovery
# ======================================================================

def find_daily_report(
    target_date,
) -> Path | None:

    path = (
        DAILY_ROOT
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / f"{target_date:%Y-%m-%d}.md"
    )

    if path.exists():
        return path

    candidates = list(
        DAILY_ROOT.rglob(
            f"{target_date:%Y-%m-%d}.md"
        )
    )

    if candidates:
        return sorted(candidates)[0]

    return None


def find_weekly_report(
    year: int,
    week: int,
) -> Path | None:

    filename_candidates = [
        f"W{week:02d}.md",
        f"{year}-W{week:02d}.md",
    ]

    for filename in filename_candidates:

        direct = (
            WEEKLY_ROOT
            / str(year)
            / filename
        )

        if direct.exists():
            return direct

    for filename in filename_candidates:

        candidates = list(
            WEEKLY_ROOT.rglob(filename)
        )

        if candidates:
            return sorted(candidates)[0]

    return None


# ======================================================================
# Noise detection
# ======================================================================

NOISE_EXACT = {
    "日报",
    "周报",
    "今日总结",
    "今日概况",
    "本周总结",
    "本周概况",
    "基本信息",
    "资源分享",
    "科技与产业",
    "人事变动",
    "其他重要动态",
    "风险与预警",
    "风险预警",
    "核心发现",
    "专题研究候选沉淀",
    "数据源完整性危机",
    "新闻源内部一致性风险",
    "免责声明",
    "目录",
    "参考资料",
    "来源",
}


NOISE_PREFIXES = (
    "今日总结",
    "今日概况",
    "本日总结",
    "本周总结",
    "本周概况",
    "核心发现",
    "专题研究",
    "建议",
    "数据源完整性",
    "新闻源内部一致性",
    "继续监控",
    "针对本周",
    "针对高价值",
    "结合本周新增",
    "基于本周新增",
    "基于8月",
    "基于9月",
    "风险与预警",
    "风险预警",
    "基本信息",
    "资源分享",
    "科技与产业",
    "人事变动",
    "其他重要动态",
)


def is_noise_heading(
    title: str,
) -> bool:

    title = normalize_title(title)

    if not title:
        return True

    if title in NOISE_EXACT:
        return True

    for prefix in NOISE_PREFIXES:

        if title.startswith(prefix):
            return True

    analysis_patterns = (
        "建议优化",
        "建议加强",
        "建议关注",
        "建议继续",
        "建议建立",
        "值得关注",
        "需要关注",
        "应当关注",
        "后续建议",
        "监控建议",
        "风险提示",
        "分析结论",
        "研究方向",
        "研究候选",
        "数据质量",
        "数据源",
        "新闻源",
        "完整性危机",
        "内部一致性",
    )

    if any(
        x in title
        for x in analysis_patterns
    ):
        return True

    if len(title) <= 5:

        generic_short = (
            "概况",
            "总结",
            "建议",
            "分析",
            "风险",
            "预警",
            "动态",
            "其他",
            "来源",
        )

        if title in generic_short:
            return True

    return False


# ======================================================================
# News extraction
# ======================================================================

def heading_level(
    line: str,
) -> int:

    m = re.match(
        r"^\s*(#{1,6})\s+",
        line,
    )

    if not m:
        return 0

    return len(
        m.group(1)
    )


def is_heading(
    line: str,
) -> bool:

    return heading_level(line) > 0


def is_numbered_item(
    line: str,
) -> bool:

    return bool(
        re.match(
            r"^\s*(?:[-*+]\s*)?"
            r"\d+\s*[\.\、\)]\s+.+",
            line,
        )
    )


def extract_title_from_line(
    line: str,
) -> str:

    title = clean_text(line)

    title = re.sub(
        r"^\s*#{1,6}\s*",
        "",
        title,
    )

    title = re.sub(
        r"^\s*[-*+]\s*",
        "",
        title,
    )

    title = re.sub(
        r"^\s*\d+\s*[\.\、\)]\s*",
        "",
        title,
    )

    return normalize_title(title)


def likely_news_title(
    title: str,
    body: str = "",
) -> bool:

    title = normalize_title(title)

    if not title:
        return False

    if is_noise_heading(title):
        return False

    if len(title) < 8:
        return False

    bad_phrases = (
        "建议",
        "需要",
        "应继续",
        "应当",
        "值得关注",
        "继续监控",
        "结合本周",
        "基于本周",
        "数据源",
        "新闻源",
        "完整性",
        "一致性",
        "专题研究",
        "核心发现",
    )

    if any(
        x in title
        for x in bad_phrases
    ):
        return False

    if title.endswith(
        ("：", ":")
    ) and len(title) < 18:

        return False

    body_clean = clean_text(body)

    if len(body_clean) < 20:

        generic = (
            "政治",
            "经济",
            "科技",
            "国际",
            "其他",
            "动态",
            "概况",
            "总结",
        )

        if title in generic:
            return False

    return True


def extract_news_items(
    markdown: str,
) -> list[dict]:

    lines = markdown.splitlines()

    candidates = []

    current_title = None
    current_body = []

    def flush():

        nonlocal current_title
        nonlocal current_body

        if current_title:

            body = "\n".join(
                current_body
            ).strip()

            title = normalize_title(
                current_title
            )

            if likely_news_title(
                title,
                body,
            ):

                candidates.append(
                    {
                        "title": title,
                        "body": clean_text(body),
                    }
                )

        current_title = None
        current_body = []

    for line in lines:

        if is_heading(line):

            flush()

            current_title = (
                extract_title_from_line(
                    line
                )
            )

            continue

        if is_numbered_item(line):

            flush()

            current_title = (
                extract_title_from_line(
                    line
                )
            )

            continue

        if current_title:

            current_body.append(line)

    flush()

    unique = []
    seen = set()

    for item in candidates:

        key = normalize_title(
            item["title"]
        )

        if key in seen:
            continue

        seen.add(key)
        unique.append(item)

    return unique


def extract_news_items_fallback(
    markdown: str,
) -> list[dict]:

    paragraphs = re.split(
        r"\n\s*\n+",
        markdown,
    )

    candidates = []

    for paragraph in paragraphs:

        text = clean_text(
            paragraph
        )

        if len(text) < 25:
            continue

        first_sentence = re.split(
            r"[。！？!?\n]",
            text,
            maxsplit=1,
        )[0].strip()

        if not likely_news_title(
            first_sentence,
            text,
        ):
            continue

        candidates.append(
            {
                "title": first_sentence[:120],
                "body": text[:2000],
            }
        )

    return candidates


def extract_news(
    markdown: str,
) -> list[dict]:

    items = extract_news_items(
        markdown
    )

    if not items:

        items = (
            extract_news_items_fallback(
                markdown
            )
        )

    return items


# ======================================================================
# Report loading
# ======================================================================

def read_report(
    path: Path,
) -> str:

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


# ======================================================================
# Image planning
# ======================================================================

def build_image_plan(
    report_text: str,
    report_type: str,
) -> list[dict]:

    news = extract_news(
        report_text
    )

    log(
        f"Detected candidate news: "
        f"{len(news)}"
    )

    for idx, item in enumerate(
        news,
        start=1,
    ):

        log(
            f"NEWS {idx}: "
            f"{item['title']}"
        )

    if not news:

        log(
            "WARNING: no valid news candidates found"
        )

        return []

    plan = []

    latest = news[-1]

    plan.append(
        {
            "name": "首图.png",
            "role": "latest_news",
            "title": latest["title"],
            "body": latest["body"],
            "view": "primary",
        }
    )

    plan.append(
        {
            "name": "插图1.png",
            "role": "latest_news_second_view",
            "title": latest["title"],
            "body": latest["body"],
            "view": "secondary",
        }
    )

    if len(news) >= 2:

        second = news[-2]

        plan.append(
            {
                "name": "插图2.png",
                "role": "second_news",
                "title": second["title"],
                "body": second["body"],
                "view": "primary",
            }
        )

    if len(news) >= 3:

        third = news[-3]

        plan.append(
            {
                "name": "插图3.png",
                "role": "third_news",
                "title": third["title"],
                "body": third["body"],
                "view": "primary",
            }
        )

    return plan[:TARGET_IMAGE_COUNT]


# ======================================================================
# Prompt
# ======================================================================

def build_visual_prompt(
    item: dict,
) -> str:

    title = item.get(
        "title",
        "",
    )

    body = item.get(
        "body",
        "",
    )

    view = item.get(
        "view",
        "primary",
    )

    if view == "secondary":

        view_instruction = """
Show the SAME real-world news event
from a different physical camera position.

This is a second photographic perspective,
not a second scene.

Keep:

one location,
one moment,
one physical event,
one camera shot,
one visual center.

Do not introduce another location.
Do not create a collage.
Do not create multiple panels.
"""

    else:

        view_instruction = """
Show the physical reality of this news event
as one professional documentary photograph.

Choose the single most visually representative
physical moment.
"""

    semantic_context = f"""
SEMANTIC EVENT CONTEXT
======================

Event:
{title}

Relevant factual context:
{body[:3000]}

IMPORTANT:

The text above is semantic context only.

It must NEVER appear in the image.

Do not copy the wording.

Do not translate the wording.

Do not typeset the wording.

Do not display the wording.

Do not create a newspaper page.

Do not create a document.

Do not create a screen containing the wording.

Do not create signs containing the wording.
"""

    prompt = f"""
Generate ONE professional realistic documentary
news photograph / editorial news illustration.

This is a NEWS IMAGE, not an infographic.

{semantic_context}

{view_instruction}

Communicate the event only through physical visual reality:

people,
objects,
architecture,
vehicles,
infrastructure,
environment,
weather,
physical action,
lighting,
spatial relationships.

No written information is needed.

The viewer should understand the general event
from the physical scene itself.

{VISUAL_CONTRACT}

FINAL PRIORITY:

No readable text anywhere in the image.

If any object would normally contain text,
make the text area blank, obscured,
out of focus, turned away,
cropped, or otherwise unreadable.

Do not generate fake text or gibberish.

Do not generate letters.

Do not generate Chinese characters.

Do not generate readable numbers.

The final result must look like a clean,
professional,
photorealistic news photograph.
"""

    return prompt.strip()


# ======================================================================
# AGNES image generation
# ======================================================================

def generate_image_bytes(
    prompt: str,
) -> bytes:

    if not AGNES_API_KEY:

        raise RuntimeError(
            "AGNES_API_KEY is not configured."
        )

    payload = {
        "model": AGNES_IMAGE_MODEL,
        "prompt": prompt,
        "size": IMAGE_SIZE,
        "aspect_ratio": IMAGE_RATIO,
        "extra_body": {
            "response_format": "url",
        },
    }

    data = json.dumps(
        payload
    ).encode("utf-8")

    request = Request(
        AGNES_IMAGE_URL,
        data=data,
        headers={
            "Authorization":
                f"Bearer {AGNES_API_KEY}",
            "Content-Type":
                "application/json",
        },
        method="POST",
    )

    log(
        "Calling AGNES image API..."
    )

    with urlopen(
        request,
        timeout=IMAGE_TIMEOUT,
    ) as response:

        raw = response.read()

    response_data = json.loads(
        raw.decode("utf-8")
    )

    image_url = None

    if isinstance(
        response_data,
        dict,
    ):

        data_field = (
            response_data.get(
                "data"
            )
        )

        if (
            isinstance(
                data_field,
                list,
            )
            and data_field
        ):

            first = data_field[0]

            if isinstance(
                first,
                dict,
            ):

                image_url = first.get(
                    "url"
                )

        if not image_url:

            image_url = (
                response_data.get(
                    "url"
                )
            )

    if not image_url:

        raise RuntimeError(
            "AGNES image API returned no image URL.\n"
            f"Response: "
            f"{str(response_data)[:2000]}"
        )

    log(
        "Downloading generated image..."
    )

    image_request = Request(
        image_url,
        headers={
            "User-Agent":
                "748686-Knowledge-Image-Engine/5.2",
        },
    )

    with urlopen(
        image_request,
        timeout=IMAGE_TIMEOUT,
    ) as image_response:

        return image_response.read()


# ======================================================================
# Image basic validation
# ======================================================================

def validate_image_basic(
    image_bytes: bytes,
) -> tuple[bool, str]:

    if not PIL_AVAILABLE:

        return (
            False,
            "Pillow unavailable",
        )

    try:

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        image.load()

        width, height = image.size

        if (
            width < 1000
            or height < 500
        ):

            return (
                False,
                f"Image resolution too small: "
                f"{width}x{height}",
            )

        if image.format not in (
            "PNG",
            "JPEG",
            "WEBP",
        ):

            return (
                False,
                f"Unsupported image format: "
                f"{image.format}",
            )

        return (
            True,
            f"{image.format} "
            f"{width}x{height}",
        )

    except Exception as exc:

        return (
            False,
            f"Pillow validation failed: {exc}",
        )


# ======================================================================
# Grid / collage detection
# ======================================================================

def detect_extreme_grid_structure(
    image_bytes: bytes,
) -> tuple[bool, str]:

    if not PIL_AVAILABLE:

        return (
            False,
            "Pillow unavailable; "
            "grid detector skipped",
        )

    try:

        image = (
            Image.open(
                io.BytesIO(image_bytes)
            )
            .convert("L")
        )

        image.thumbnail(
            (900, 600)
        )

        width, height = image.size

        if (
            width < 100
            or height < 100
        ):

            return (
                False,
                "Image too small for grid analysis",
            )

        edges = ImageOps.autocontrast(
            image
        )

        edges = edges.filter(
            ImageFilter.FIND_EDGES
        )

        px = edges.load()

        vertical_hits = 0
        horizontal_hits = 0

        x_start = int(
            width * 0.10
        )

        x_end = int(
            width * 0.90
        )

        y_start = int(
            height * 0.10
        )

        y_end = int(
            height * 0.90
        )

        threshold = 150

        for x in range(
            x_start,
            x_end,
        ):

            hits = 0

            for y in range(
                y_start,
                y_end,
                3,
            ):

                if px[x, y] >= threshold:
                    hits += 1

            if hits > height * 0.22:
                vertical_hits += 1

        for y in range(
            y_start,
            y_end,
        ):

            hits = 0

            for x in range(
                x_start,
                x_end,
                3,
            ):

                if px[x, y] >= threshold:
                    hits += 1

            if hits > width * 0.22:
                horizontal_hits += 1

        if vertical_hits >= 4:

            return (
                True,
                f"Strong vertical separator pattern: "
                f"{vertical_hits}",
            )

        if horizontal_hits >= 4:

            return (
                True,
                f"Strong horizontal separator pattern: "
                f"{horizontal_hits}",
            )

        return (
            False,
            "No extreme grid structure detected",
        )

    except Exception as exc:

        return (
            False,
            f"Grid detector error: {exc}",
        )


# ======================================================================
# OCR helpers
# ======================================================================

def contains_chinese(
    text: str,
) -> bool:

    if not text:
        return False

    return bool(
        re.search(
            r"[\u3400-\u4DBF"
            r"\u4E00-\u9FFF"
            r"\uF900-\uFAFF]",
            text,
        )
    )


def chinese_char_count(
    text: str,
) -> int:

    if not text:
        return 0

    return len(
        re.findall(
            r"[\u3400-\u4DBF"
            r"\u4E00-\u9FFF"
            r"\uF900-\uFAFF]",
            text,
        )
    )


def latin_word_count(
    text: str,
) -> int:

    if not text:
        return 0

    return len(
        re.findall(
            r"\b[A-Za-z]{3,}\b",
            text,
        )
    )


def safe_float(
    value,
    default: float = 0.0,
) -> float:

    try:
        return float(value)
    except Exception:
        return default


# ======================================================================
# OCR readable-text detector
# ======================================================================

def detect_readable_text_region(
    image: Image.Image,
) -> tuple[bool, str]:

    if not PYTESSERACT_AVAILABLE:

        return (
            False,
            "OCR unavailable",
        )

    try:

        data = pytesseract.image_to_data(
            image,
            lang="eng+chi_sim+chi_tra",
            config="--psm 11",
            output_type=Output.DICT,
        )

    except Exception as exc:

        log(
            f"OCR data warning: {exc}"
        )

        return (
            False,
            "",
        )

    n = len(
        data.get(
            "text",
            [],
        )
    )

    high_conf_chinese = []
    high_conf_latin = []

    for i in range(n):

        raw_text = (
            data["text"][i] or ""
        ).strip()

        if not raw_text:
            continue

        confidence = safe_float(
            data["conf"][i],
            0.0,
        )

        if confidence < 55:
            continue

        left = int(
            data["left"][i]
        )

        top = int(
            data["top"][i]
        )

        width = int(
            data["width"][i]
        )

        height = int(
            data["height"][i]
        )

        cjk_count = (
            chinese_char_count(
                raw_text
            )
        )

        latin_count = (
            latin_word_count(
                raw_text
            )
        )

        if cjk_count > 0:

            high_conf_chinese.append(
                {
                    "text": raw_text,
                    "confidence": confidence,
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                    "count": cjk_count,
                }
            )

        if latin_count > 0:

            high_conf_latin.append(
                {
                    "text": raw_text,
                    "confidence": confidence,
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height,
                    "count": latin_count,
                }
            )

    # --------------------------------------------------------------
    # 中文：只有明显的连续文字区域才 FAIL
    # --------------------------------------------------------------

    if high_conf_chinese:

        total_chars = sum(
            item["count"]
            for item in high_conf_chinese
        )

        # 一个孤立汉字、两个随机汉字不算真正文字。
        if total_chars >= 8:

            avg_conf = (
                sum(
                    item["confidence"]
                    for item in high_conf_chinese
                )
                / len(high_conf_chinese)
            )

            if avg_conf >= 60:

                preview = " ".join(
                    item["text"]
                    for item in high_conf_chinese[:8]
                )

                return (
                    True,
                    "Readable Chinese text region "
                    f"detected: {preview[:200]} "
                    f"(chars={total_chars}, "
                    f"avg_conf={avg_conf:.1f})",
                )

        # 同一水平区域出现多个中文 token
        # 才进一步认为可能是实际文字。
        sorted_items = sorted(
            high_conf_chinese,
            key=lambda x: (
                x["top"],
                x["left"],
            ),
        )

        for i, current in enumerate(
            sorted_items
        ):

            nearby_count = (
                current["count"]
            )

            confidence_values = [
                current["confidence"]
            ]

            for j in range(
                i + 1,
                len(sorted_items),
            ):

                other = sorted_items[j]

                y_distance = abs(
                    other["top"]
                    - current["top"]
                )

                x_distance = abs(
                    other["left"]
                    - (
                        current["left"]
                        + current["width"]
                    )
                )

                if (
                    y_distance
                    <= max(
                        current["height"],
                        other["height"],
                    ) * 1.5
                    and x_distance
                    < 250
                ):

                    nearby_count += (
                        other["count"]
                    )

                    confidence_values.append(
                        other["confidence"]
                    )

            if (
                nearby_count >= 4
                and (
                    sum(confidence_values)
                    / len(confidence_values)
                ) >= 65
            ):

                preview = " ".join(
                    item["text"]
                    for item in sorted_items[:8]
                )

                return (
                    True,
                    "Continuous Chinese-like text "
                    f"region detected: {preview[:200]}",
                )

    # --------------------------------------------------------------
    # 英文：
    # 只有真正像英文单词/句子的 OCR 才 FAIL
    # --------------------------------------------------------------

    if high_conf_latin:

        meaningful_words = [
            item
            for item in high_conf_latin
            if item["count"] >= 3
            and item["confidence"] >= 65
        ]

        # 单个随机英文 token 不立即 FAIL。
        #
        # 需要：
        #   两个以上明显英文单词
        # 或
        #   一个很高置信度的较长英文词
        if len(meaningful_words) >= 2:

            preview = " ".join(
                item["text"]
                for item in meaningful_words[:8]
            )

            return (
                True,
                "Readable English text region "
                f"detected: {preview[:200]}",
            )

        for item in meaningful_words:

            token = re.sub(
                r"[^A-Za-z]",
                "",
                item["text"],
            )

            if (
                len(token) >= 7
                and item["confidence"] >= 78
            ):

                return (
                    True,
                    "High-confidence readable "
                    f"English text detected: "
                    f"{token}",
                )

    return (
        False,
        "",
    )


# ======================================================================
# OCR quality check
# ======================================================================

def ocr_text_quality_check(
    image_bytes: bytes,
) -> tuple[bool, str]:

    if not PIL_AVAILABLE:

        return (
            False,
            "Pillow unavailable; OCR cannot run",
        )

    if not PYTESSERACT_AVAILABLE:

        return (
            False,
            "pytesseract unavailable; OCR cannot run",
        )

    try:

        original = (
            Image.open(
                io.BytesIO(image_bytes)
            )
            .convert("RGB")
        )

        width, height = original.size

        # ----------------------------------------------------------
        # V5.2：
        # 不再做 4 次 OCR。
        #
        # 过度增强会把纹理增强成“伪文字”，
        # 从而造成大量 OCR 假阳性。
        #
        # 只做：
        #   1. 原图
        #   2. 适度放大图
        # ----------------------------------------------------------

        images = [
            (
                "original",
                original,
            )
        ]

        enlarged_width = min(
            width * 2,
            3000,
        )

        enlarged_height = min(
            height * 2,
            3000,
        )

        enlarged = original.resize(
            (
                enlarged_width,
                enlarged_height,
            ),
            Image.Resampling.LANCZOS,
        )

        images.append(
            (
                "enlarged",
                enlarged,
            )
        )

        detections = []

        for name, image in images:

            found, reason = (
                detect_readable_text_region(
                    image
                )
            )

            if found:

                detections.append(
                    (
                        name,
                        reason,
                    )
                )

        if detections:

            name, reason = (
                detections[0]
            )

            return (
                False,
                f"Readable text detected by OCR "
                f"({name}): {reason}",
            )

        return (
            True,
            "OCR PASS: no clearly readable "
            "text region detected",
        )

    except Exception as exc:

        return (
            False,
            f"OCR validation error: {exc}",
        )


# ======================================================================
# Composite visual QA
# ======================================================================

def visual_quality_check(
    image_bytes: bytes,
) -> tuple[bool, list[str]]:

    reasons = []

    # --------------------------------------------------------------
    # Pillow
    # --------------------------------------------------------------

    ok, reason = validate_image_basic(
        image_bytes
    )

    if not ok:

        reasons.append(
            reason
        )

    else:

        log(
            f"Basic image check: {reason}"
        )

    # --------------------------------------------------------------
    # Grid
    # --------------------------------------------------------------

    grid_found, grid_reason = (
        detect_extreme_grid_structure(
            image_bytes
        )
    )

    log(
        f"Grid check: {grid_reason}"
    )

    if grid_found:

        reasons.append(
            grid_reason
        )

    # --------------------------------------------------------------
    # OCR
    # --------------------------------------------------------------

    ocr_ok, ocr_reason = (
        ocr_text_quality_check(
            image_bytes
        )
    )

    log(
        f"Text check: {ocr_reason}"
    )

    if not ocr_ok:

        reasons.append(
            ocr_reason
        )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    if reasons:

        return (
            False,
            reasons,
        )

    return (
        True,
        [],
    )


# ======================================================================
# Atomic image save
# ======================================================================

def save_png_atomic(
    image_bytes: bytes,
    destination: Path,
) -> None:

    if not PIL_AVAILABLE:

        raise RuntimeError(
            "Pillow is required for PNG normalization."
        )

    image = (
        Image.open(
            io.BytesIO(image_bytes)
        )
        .convert("RGB")
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temp_path = destination.with_suffix(
        ".tmp.png"
    )

    image.save(
        temp_path,
        format="PNG",
        optimize=True,
    )

    temp_path.replace(
        destination
    )


# ======================================================================
# Generate one validated image
# ======================================================================

def generate_validated_image(
    item: dict,
    destination: Path,
) -> bool:

    title = item.get(
        "title",
        "",
    )

    log()

    log(
        "------------------------------------------------------------"
    )

    log(
        f"GENERATE IMAGE: "
        f"{destination.name}"
    )

    log(
        f"NEWS TITLE: "
        f"{title}"
    )

    log(
        "------------------------------------------------------------"
    )

    prompt = build_visual_prompt(
        item
    )

    for attempt in range(
        1,
        MAX_IMAGE_RETRIES + 1,
    ):

        log()

        log(
            f"Image attempt "
            f"{attempt}/{MAX_IMAGE_RETRIES}"
        )

        try:

            image_bytes = (
                generate_image_bytes(
                    prompt
                )
            )

            log(
                f"Downloaded image bytes: "
                f"{len(image_bytes):,}"
            )

            valid, reasons = (
                visual_quality_check(
                    image_bytes
                )
            )

            if valid:

                log(
                    "VISUAL CHECK: PASS"
                )

                save_png_atomic(
                    image_bytes,
                    destination,
                )

                log(
                    f"IMAGE SAVED: "
                    f"{destination}"
                )

                return True

            log(
                "VISUAL CHECK: FAIL"
            )

            for reason in reasons:

                log(
                    f"  - {reason}"
                )

            if destination.exists():

                destination.unlink()

            # ------------------------------------------------------
            # V5.2 regeneration instruction
            # ------------------------------------------------------

            prompt = (
                build_visual_prompt(item)
                + "\n\n"
                + """
IMPORTANT REGENERATION CORRECTION

The previous image failed visual quality control.

Generate a cleaner photographic composition.

The next image MUST be:

ONE real-world scene.
ONE location.
ONE moment.
ONE camera shot.
ONE visual center.

Do not create an infographic.

Do not create a collage.

Do not create multiple panels.

Do not create a split screen.

Do not create a grid.

Do not create a newspaper.

Do not create a poster.

Do not create a presentation.

Do not create a diagram.

Do not create a chart.

Most importantly:

REMOVE ALL READABLE TEXT.

Remove:
Chinese characters,
English words,
letters,
numbers used as text,
signs,
billboards,
screens,
papers,
documents,
newspapers,
books,
labels,
logos,
watermarks,
captions,
titles,
banners,
badges.

Do not replace them with gibberish.

Do not generate fake writing.

If a real-world object would normally contain text,
make that surface blank, blurred, turned away,
out of focus, cropped, or otherwise unreadable.

The image should communicate only through
physical visual reality.

Make it look like a professional documentary
news photograph.
"""
            )

            time.sleep(
                min(
                    8 * attempt,
                    30,
                )
            )

        except (
            HTTPError,
            URLError,
            TimeoutError,
            OSError,
            json.JSONDecodeError,
        ) as exc:

            log(
                f"Generation attempt failed: "
                f"{exc}"
            )

            if attempt < MAX_IMAGE_RETRIES:

                time.sleep(
                    min(
                        10 * attempt,
                        40,
                    )
                )

        except Exception as exc:

            log(
                f"Unexpected generation error: "
                f"{exc}"
            )

            if attempt < MAX_IMAGE_RETRIES:

                time.sleep(
                    min(
                        10 * attempt,
                        40,
                    )
                )

    log(
        f"FAILED: "
        f"{destination.name}"
    )

    return False


# ======================================================================
# Existing image validation
# ======================================================================

def validate_existing_image(
    path: Path,
) -> bool:

    if not path.exists():

        return False

    try:

        data = path.read_bytes()

        valid, reasons = (
            visual_quality_check(
                data
            )
        )

        if valid:

            log(
                f"Existing image valid: "
                f"{path.name}"
            )

            return True

        log(
            f"Existing image invalid: "
            f"{path.name}"
        )

        for reason in reasons:

            log(
                f"  - {reason}"
            )

        return False

    except Exception as exc:

        log(
            f"Existing image validation error: "
            f"{path}: {exc}"
        )

        return False


# ======================================================================
# Image generation for report
# ======================================================================

def generate_report_images(
    report_path: Path,
    image_dir: Path,
    report_type: str,
) -> list[Path]:

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_text = read_report(
        report_path
    )

    log()

    log(
        "============================================================"
    )

    log(
        f"IMAGE PLAN: "
        f"{report_path.name}"
    )

    log(
        "============================================================"
    )

    plan = build_image_plan(
        report_text,
        report_type,
    )

    if not plan:

        log(
            "No valid news found. "
            "Skipping image generation."
        )

        return []

    # --------------------------------------------------------------
    # FORCE_REGENERATE
    # --------------------------------------------------------------

    if FORCE_REGENERATE:

        log(
            "FORCE_REGENERATE=true"
        )

        for name in IMAGE_NAMES:

            old = image_dir / name

            if old.exists():

                log(
                    f"Removing old image: "
                    f"{old}"
                )

                old.unlink()

    generated = []

    for item in plan:

        destination = (
            image_dir
            / item["name"]
        )

        if (
            not FORCE_REGENERATE
            and validate_existing_image(
                destination
            )
        ):

            generated.append(
                destination
            )

            continue

        success = (
            generate_validated_image(
                item,
                destination,
            )
        )

        if success:

            generated.append(
                destination
            )

    # --------------------------------------------------------------
    # Final image count
    # --------------------------------------------------------------

    valid_images = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if path.exists():

            if validate_existing_image(
                path
            ):

                valid_images.append(
                    path
                )

    log()

    log(
        f"VALID IMAGE COUNT: "
        f"{len(valid_images)}"
    )

    if len(valid_images) < MIN_IMAGE_COUNT:

        log(
            f"WARNING: only "
            f"{len(valid_images)} "
            f"valid images available; "
            f"minimum is "
            f"{MIN_IMAGE_COUNT}"
        )

    return valid_images


# ======================================================================
# Markdown image path
# ======================================================================

def make_relative_image_path(
    report_path: Path,
    image_path: Path,
) -> str:

    relative = os.path.relpath(
        image_path,
        start=report_path.parent,
    )

    return Path(
        relative
    ).as_posix()


# ======================================================================
# Create image report
# ======================================================================

def create_image_report(
    report_path: Path,
    image_paths: list[Path],
) -> Path | None:

    if not image_paths:

        return None

    original = read_report(
        report_path
    )

    output_path = (
        report_path.parent
        / f"{report_path.stem}_带图.md"
    )

    lines = original.splitlines()

    if not lines:

        return None

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover = image_paths[0]

    cover_relative = (
        make_relative_image_path(
            report_path,
            cover,
        )
    )

    result = []

    result.append(
        f"![首图]({cover_relative})"
    )

    result.append("")

    # --------------------------------------------------------------
    # 正文插图
    # --------------------------------------------------------------

    body_lines = list(lines)

    if len(image_paths) == 1:

        result.extend(
            body_lines
        )

    else:

        insertion_points = []

        total = len(
            body_lines
        )

        start = 0

        if (
            body_lines
            and body_lines[0].strip()
            == "---"
        ):

            try:

                end = body_lines.index(
                    "---",
                    1,
                )

                start = end + 1

            except ValueError:

                start = 0

        usable = max(
            total - start,
            1,
        )

        for index in range(
            1,
            len(image_paths),
        ):

            point = (
                start
                + int(
                    usable
                    * index
                    / len(image_paths)
                )
            )

            point = min(
                max(
                    point,
                    start,
                ),
                total,
            )

            insertion_points.append(
                point
            )

        insertion_map = {}

        for image_index, point in enumerate(
            insertion_points,
            start=1,
        ):

            insertion_map.setdefault(
                point,
                [],
            ).append(
                image_index
            )

        for index, line in enumerate(
            body_lines
        ):

            if index in insertion_map:

                for image_index in (
                    insertion_map[index]
                ):

                    image_path = (
                        image_paths[
                            image_index
                        ]
                    )

                    relative = (
                        make_relative_image_path(
                            report_path,
                            image_path,
                        )
                    )

                    result.append("")

                    result.append(
                        f"![插图{image_index}]"
                        f"({relative})"
                    )

                    result.append("")

            result.append(
                line
            )

        inserted = sum(
            len(v)
            for v in insertion_map.values()
        )

        if (
            inserted
            < len(image_paths) - 1
        ):

            for image_index in range(
                inserted + 1,
                len(image_paths),
            ):

                image_path = (
                    image_paths[
                        image_index
                    ]
                )

                relative = (
                    make_relative_image_path(
                        report_path,
                        image_path,
                    )
                )

                result.append("")

                result.append(
                    f"![插图{image_index}]"
                    f"({relative})"
                )

    output_path.write_text(
        "\n".join(
            result
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )

    log(
        f"IMAGE REPORT CREATED: "
        f"{output_path}"
    )

    return output_path


# ======================================================================
# Daily
# ======================================================================

def process_daily_report(
    target_date,
) -> bool:

    log()

    log(
        "######################################################################"
    )

    log(
        f"DAILY IMAGE REPORT: "
        f"{target_date}"
    )

    log(
        "######################################################################"
    )

    report_path = find_daily_report(
        target_date
    )

    if not report_path:

        log(
            f"Daily report not found: "
            f"{target_date}"
        )

        return False

    log(
        f"Daily report: "
        f"{report_path}"
    )

    image_dir = daily_image_dir(
        target_date
    )

    images = generate_report_images(
        report_path,
        image_dir,
        "daily",
    )

    if len(images) < MIN_IMAGE_COUNT:

        log(
            "Daily image generation incomplete."
        )

        return False

    output = create_image_report(
        report_path,
        images,
    )

    return output is not None


# ======================================================================
# Weekly
# ======================================================================

def process_weekly_report(
    year: int,
    week: int,
) -> bool:

    log()

    log(
        "######################################################################"
    )

    log(
        f"WEEKLY IMAGE REPORT: "
        f"{year}-W{week:02d}"
    )

    log(
        "######################################################################"
    )

    report_path = find_weekly_report(
        year,
        week,
    )

    if not report_path:

        log(
            f"Weekly report not found: "
            f"{year}-W{week:02d}"
        )

        return False

    log(
        f"Weekly report: "
        f"{report_path}"
    )

    image_dir = weekly_image_dir(
        year,
        week,
    )

    images = generate_report_images(
        report_path,
        image_dir,
        "weekly",
    )

    if len(images) < MIN_IMAGE_COUNT:

        log(
            "Weekly image generation incomplete."
        )

        return False

    output = create_image_report(
        report_path,
        images,
    )

    return output is not None


# ======================================================================
# Dependency diagnostics
# ======================================================================

def dependency_check() -> None:

    log()

    log(
        "============================================================"
    )

    log(
        "IMAGE ENGINE DEPENDENCIES"
    )

    log(
        "============================================================"
    )

    log(
        f"Pillow available      : "
        f"{PIL_AVAILABLE}"
    )

    log(
        f"pytesseract available : "
        f"{PYTESSERACT_AVAILABLE}"
    )

    if PIL_AVAILABLE:

        try:

            log(
                f"Pillow version        : "
                f"{Image.__version__}"
            )

        except Exception:
            pass

    if PYTESSERACT_AVAILABLE:

        try:

            version = (
                pytesseract.get_tesseract_version()
            )

            log(
                f"Tesseract version     : "
                f"{version}"
            )

            languages = (
                pytesseract.get_languages(
                    config=""
                )
            )

            log(
                f"OCR languages         : "
                f"{languages}"
            )

        except Exception as exc:

            log(
                f"Tesseract check failed: "
                f"{exc}"
            )

    log(
        f"FORCE_REGENERATE      : "
        f"{FORCE_REGENERATE}"
    )

    log()

    log(
        "Visual mode            : "
        "TEXT-FREE NEWS IMAGE"
    )

    log(
        "Image style            : "
        "Photorealistic Documentary"
    )

    log(
        "OCR policy             : "
        "Readable Text Only"
    )

    log()


# ======================================================================
# Main
# ======================================================================

def main() -> int:

    log()

    log(
        "======================================================================"
    )

    log(
        "748686 KNOWLEDGE IMAGE ENGINE V5.2"
    )

    log(
        "TEXT-FREE NEWS IMAGE + PILLOW + OCR QUALITY CHECK"
    )

    log(
        "======================================================================"
    )

    log(
        f"UTC now               : "
        f"{utc_today().isoformat()}"
    )

    log(
        f"AGNES model            : "
        f"{AGNES_IMAGE_MODEL}"
    )

    log(
        f"Image size             : "
        f"{IMAGE_SIZE}"
    )

    log(
        f"Image ratio            : "
        f"{IMAGE_RATIO}"
    )

    dependency_check()

    if not AGNES_API_KEY:

        log(
            "ERROR: AGNES_API_KEY is missing."
        )

        return 1

    if not PIL_AVAILABLE:

        log(
            "ERROR: Pillow is required."
        )

        return 1

    if not PYTESSERACT_AVAILABLE:

        log(
            "ERROR: pytesseract is required."
        )

        return 1

    # --------------------------------------------------------------
    # Daily
    # --------------------------------------------------------------

    dates = target_dates()

    daily_success = 0
    daily_failed = 0

    for target_date in dates:

        try:

            if process_daily_report(
                target_date
            ):

                daily_success += 1

            else:

                daily_failed += 1

        except Exception as exc:

            daily_failed += 1

            log(
                f"DAILY ERROR "
                f"{target_date}: "
                f"{exc}"
            )

    # --------------------------------------------------------------
    # Weekly
    # --------------------------------------------------------------

    weekly_targets = []

    seen_weeks = set()

    for target_date in dates:

        iso = target_date.isocalendar()

        key = (
            iso.year,
            iso.week,
        )

        if key in seen_weeks:
            continue

        seen_weeks.add(key)

        weekly_targets.append(
            key
        )

    weekly_success = 0
    weekly_failed = 0

    for year, week in weekly_targets:

        try:

            if process_weekly_report(
                year,
                week,
            ):

                weekly_success += 1

            else:

                weekly_failed += 1

        except Exception as exc:

            weekly_failed += 1

            log(
                f"WEEKLY ERROR "
                f"{year}-W{week:02d}: "
                f"{exc}"
            )

    # --------------------------------------------------------------
    # Final
    # --------------------------------------------------------------

    log()

    log(
        "======================================================================"
    )

    log(
        "748686 KNOWLEDGE IMAGE ENGINE V5.2 COMPLETE"
    )

    log(
        "======================================================================"
    )

    log(
        f"Daily success : "
        f"{daily_success}"
    )

    log(
        f"Daily failed  : "
        f"{daily_failed}"
    )

    log(
        f"Weekly success: "
        f"{weekly_success}"
    )

    log(
        f"Weekly failed : "
        f"{weekly_failed}"
    )

    log()

    if (
        daily_failed > 0
        or weekly_failed > 0
    ):

        log(
            "RESULT: PARTIAL FAILURE"
        )

        return 1

    log(
        "RESULT: SUCCESS"
    )

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )
