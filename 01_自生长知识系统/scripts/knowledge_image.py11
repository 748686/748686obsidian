#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image V5.3

======================================================================
核心职责
======================================================================

1. 为 05_日报 生成日报配图
2. 为 06_周报 生成周报配图
3. 使用 AGNES Image API
4. 每份报告生成：
      首图.png
      插图1.png
      插图2.png
      插图3.png
5. 生成：
      原始日报_带图.md
      原始周报_带图.md

======================================================================
V5.3 核心变化
======================================================================

【1】周报严格绑定当前 ISO 周

例如：

2026-09-21 ～ 2026-09-27
        ↓
06_周报/2026/W39.md

这一整周每天运行：

09-21 → W39
09-22 → W39
09-23 → W39
09-24 → W39
...
09-27 → W39

每天读取最新的 W39.md，并重新生成 W39 的图片。

进入：

2026-09-28
        ↓
W40

自动切换到：

06_周报/2026/W40.md

不会继续修改 W39。

【2】FORCE_REGENERATE=true 时强制重新生成图片

因此：

W39.md 内容变化
        ↓
重新读取 W39.md
        ↓
重新生成首图/插图1/插图2/插图3
        ↓
重新生成 W39_带图.md

【3】不再因为文件已经存在而跳过

图片目录存在 ≠ 图片有效
旧图片存在 ≠ 当前周报图片仍然正确

当 FORCE_REGENERATE=true 时，直接重新生成。

【4】日报仍保持原来的三日期容错

TODAY
YESTERDAY
DAY_BEFORE

任何一天缺失，都不会阻塞其他日期。

【5】不修改 weekly_report.py
【6】不修改 Task 1～4
【7】不修改日报/周报内容生成逻辑
【8】不修改 Feishu image_key 链路

======================================================================
"""

from __future__ import annotations

import base64
import io
import os
import re
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from zoneinfo import ZoneInfo

import requests
from PIL import Image


# ======================================================================
# 基础路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"
DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# 时间
# ======================================================================

TIMEZONE = ZoneInfo("Asia/Shanghai")


def now_local() -> datetime:
    return datetime.now(TIMEZONE)


# ======================================================================
# 环境变量
# ======================================================================

AGNES_API_KEY = os.getenv("AGNES_API_KEY") or os.getenv("AI_API_KEY")

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1",
).rstrip("/")

AGNES_IMAGE_MODEL = os.getenv(
    "AGNES_IMAGE_MODEL",
    "agnes-image-2.5-flash",
)

IMAGE_SIZE = os.getenv(
    "IMAGE_SIZE",
    "2K",
)

IMAGE_RATIO = os.getenv(
    "IMAGE_RATIO",
    "16:9",
)

IMAGE_TIMEOUT = int(
    os.getenv(
        "IMAGE_TIMEOUT",
        "180",
    )
)

IMAGE_RETRIES = int(
    os.getenv(
        "IMAGE_RETRIES",
        "5",
    )
)

IMAGE_THROTTLE = float(
    os.getenv(
        "IMAGE_THROTTLE",
        "2.0",
    )
)

FORCE_REGENERATE = os.getenv(
    "FORCE_REGENERATE",
    "false",
).lower() in {
    "1",
    "true",
    "yes",
    "y",
}

MIN_IMAGE_COUNT = int(
    os.getenv(
        "MIN_IMAGE_COUNT",
        "3",
    )
)

TARGET_IMAGE_COUNT = int(
    os.getenv(
        "TARGET_IMAGE_COUNT",
        "4",
    )
)


# ======================================================================
# 日志
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


# ======================================================================
# 日期 / ISO 周
# ======================================================================

def iso_week_key(target_date: date) -> str:
    """
    返回 ISO 周，例如：

    2026-09-21 → W39
    2026-09-28 → W40
    """

    iso = target_date.isocalendar()

    return f"W{iso.week:02d}"


def iso_year_week_key(target_date: date) -> Tuple[int, int, str]:
    iso = target_date.isocalendar()

    return (
        iso.year,
        iso.week,
        f"W{iso.week:02d}",
    )


def current_iso_week() -> Tuple[int, int, str]:
    """
    当前 ISO 周。

    注意：
    ISO 年和自然年可能不同，因此不能简单使用
    datetime.now().year + week。
    """

    today = now_local().date()

    return iso_year_week_key(today)


# ======================================================================
# 周报路径
# ======================================================================

def weekly_report_path(year: int, week: int) -> Path:
    return (
        WEEKLY_ROOT
        / str(year)
        / f"W{week:02d}.md"
    )


def find_weekly_report(week_key: str, year: Optional[int] = None) -> Optional[Path]:
    """
    严格优先寻找当前 ISO 周的周报。

    例如：
        year = 2026
        week_key = W39

    优先：
        06_周报/2026/W39.md

    同时兼容旧目录结构。
    """

    if year is not None:
        candidates = [
            WEEKLY_ROOT / str(year) / f"{week_key}.md",
            WEEKLY_ROOT / str(year) / f"{week_key}周报.md",
            WEEKLY_ROOT / str(year) / week_key / f"{week_key}.md",
        ]
    else:
        candidates = [
            WEEKLY_ROOT / f"{week_key}.md",
            WEEKLY_ROOT / f"{week_key}周报.md",
            WEEKLY_ROOT / week_key / f"{week_key}.md",
        ]

    for path in candidates:
        if path.exists() and path.is_file() and path.stat().st_size > 0:
            return path

    # 兼容历史文件结构。
    if year is not None:
        search_root = WEEKLY_ROOT / str(year)
    else:
        search_root = WEEKLY_ROOT

    if search_root.exists():
        matches = sorted(
            [
                p
                for p in search_root.rglob("*.md")
                if p.is_file()
                and week_key in p.name
                and p.stat().st_size > 0
            ]
        )

        if matches:
            return matches[-1]

    return None


# ======================================================================
# 日报路径
# ======================================================================

def find_daily_report(target_date: date) -> Optional[Path]:
    date_key = target_date.isoformat()

    candidates = [
        DAILY_ROOT / f"{date_key}.md",
        DAILY_ROOT / f"{date_key}日报.md",
        DAILY_ROOT / date_key / f"{date_key}.md",
    ]

    for path in candidates:
        if path.exists() and path.is_file() and path.stat().st_size > 0:
            return path

    if DAILY_ROOT.exists():
        matches = sorted(
            [
                p
                for p in DAILY_ROOT.rglob("*.md")
                if p.is_file()
                and date_key in p.name
                and "_带图" not in p.name
                and p.stat().st_size > 0
            ]
        )

        if matches:
            return matches[-1]

    return None


# ======================================================================
# Markdown 清理
# ======================================================================

def strip_markdown(text: str) -> str:
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
        r"`{1,3}([^`]+)`{1,3}",
        r"\1",
        text,
    )

    text = re.sub(
        r"[*_~#]+",
        "",
        text,
    )

    return text


# ======================================================================
# 新闻内容提取
# ======================================================================

def extract_news_items(markdown: str) -> List[str]:
    """
    从日报/周报 Markdown 中提取可用于配图的主题内容。

    兼容：
        ## 标题
        ### 标题
        1. xxx
        - xxx
        * xxx

    如果结构无法识别，则使用正文段落。
    """

    text = markdown.replace("\r\n", "\n").replace("\r", "\n")

    lines = text.split("\n")

    items: List[str] = []

    current_heading = ""

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            continue

        # 跳过 Front Matter
        if line == "---":
            continue

        # 标题
        heading_match = re.match(
            r"^#{1,6}\s+(.+?)\s*$",
            line,
        )

        if heading_match:
            heading = strip_markdown(
                heading_match.group(1)
            ).strip()

            if heading:
                current_heading = heading

            continue

        # 编号列表
        numbered_match = re.match(
            r"^\d+[.)]\s+(.+)$",
            line,
        )

        if numbered_match:
            content = strip_markdown(
                numbered_match.group(1)
            ).strip()

            if content:
                if current_heading:
                    content = (
                        f"{current_heading}：{content}"
                    )

                items.append(content)

            continue

        # 无序列表
        bullet_match = re.match(
            r"^[-*+]\s+(.+)$",
            line,
        )

        if bullet_match:
            content = strip_markdown(
                bullet_match.group(1)
            ).strip()

            if content:
                if current_heading:
                    content = (
                        f"{current_heading}：{content}"
                    )

                items.append(content)

            continue

    # 如果没有结构化项目，则提取正文段落
    if not items:
        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        for paragraph in paragraphs:
            paragraph = strip_markdown(
                paragraph
            ).strip()

            if not paragraph:
                continue

            if len(paragraph) < 20:
                continue

            items.append(paragraph)

    # 去重，同时限制数量
    result: List[str] = []
    seen = set()

    for item in items:
        item = re.sub(
            r"\s+",
            " ",
            item,
        ).strip()

        if not item:
            continue

        if item in seen:
            continue

        seen.add(item)
        result.append(item)

    return result


# ======================================================================
# Visual Contract
# ======================================================================

VISUAL_CONTRACT = """
必须严格遵守以下视觉约束：

1. 横向 16:9 构图。
2. 画面必须是完整单幅场景。
3. 禁止漫画分格。
4. 禁止多宫格。
5. 禁止左右/上下分屏。
6. 禁止拼贴。
7. 禁止照片墙。
8. 禁止 UI 截图。
9. 禁止信息图表。
10. 禁止大段文字。
11. 禁止生成新闻网站页面。
12. 禁止生成新闻标题卡片。
13. 画面主体必须清晰。
14. 画面必须能够直接对应新闻主题。
15. 视觉上具有新闻专题插图的感觉。
16. 不要添加无法验证的具体人物姓名、公司 Logo 或品牌文字。
17. 如果涉及科学、医学、技术主题，应使用准确、合理的视觉隐喻。
18. 整体画面保持专业、清晰、现代。
"""


# ======================================================================
# Prompt
# ======================================================================

def build_visual_prompt(
    item: str,
    report_type: str,
    position: str,
) -> str:

    return f"""
你是一名专业新闻视觉设计师。

请根据下面的新闻内容生成一张新闻专题插图。

报告类型：
{report_type}

图片位置：
{position}

新闻主题：
{item}

{VISUAL_CONTRACT}

额外要求：

- 画面必须是一张完整的单幅 16:9 图片。
- 不要把新闻内容直接写成海报。
- 不要出现大段文字。
- 不要出现多个画面拼在一起。
- 让视觉主体直接表达新闻主题。
- 如果是科技、医学、物理、化学、生物等科学主题，应使用科学合理的视觉表现。
- 如果是政策、经济、社会或国际新闻，应使用具有新闻纪实感的场景。
- 如果新闻内容涉及抽象概念，可以使用专业、克制的视觉隐喻。
- 不要虚构具体人物身份。
- 不要生成品牌 Logo。
"""


# ======================================================================
# AGNES 图片 API
# ======================================================================

def generate_image_from_agnes(
    prompt: str,
) -> Optional[bytes]:

    if not AGNES_API_KEY:
        log("❌ AGNES_API_KEY 未设置")
        return None

    url = (
        f"{AGNES_BASE_URL}"
        "/images/generations"
    )

    headers = {
        "Authorization": (
            f"Bearer {AGNES_API_KEY}"
        ),
        "Content-Type": "application/json",
    }

    payload = {
        "model": AGNES_IMAGE_MODEL,
        "prompt": prompt,
        "size": IMAGE_SIZE,
        "aspect_ratio": IMAGE_RATIO,
        "n": 1,
    }

    for attempt in range(
        1,
        IMAGE_RETRIES + 1,
    ):

        log(
            f"    🎨 AGNES 生图 "
            f"{attempt}/{IMAGE_RETRIES}"
        )

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=IMAGE_TIMEOUT,
            )

            if response.status_code != 200:
                log(
                    f"    ⚠️ HTTP "
                    f"{response.status_code}: "
                    f"{response.text[:500]}"
                )

            response.raise_for_status()

            data = response.json()

            # 常见 OpenAI 风格返回
            items = data.get("data") or []

            if not items:
                log("    ⚠️ API 返回 data 为空")
                raise RuntimeError(
                    "AGNES image API data empty"
                )

            item = items[0]

            # URL
            image_url = item.get("url")

            if image_url:
                image_response = requests.get(
                    image_url,
                    timeout=IMAGE_TIMEOUT,
                )

                image_response.raise_for_status()

                return image_response.content

            # base64
            b64 = (
                item.get("b64_json")
                or item.get("base64")
            )

            if b64:
                return base64.b64decode(b64)

            raise RuntimeError(
                "AGNES response contains neither url nor b64_json"
            )

        except Exception as exc:
            log(
                f"    ⚠️ 生图失败：{exc}"
            )

            if attempt < IMAGE_RETRIES:
                time.sleep(
                    IMAGE_THROTTLE
                )

    return None


# ======================================================================
# 图片基础验证
# ======================================================================

def validate_image_bytes(
    image_bytes: bytes,
) -> Tuple[bool, str]:

    if not image_bytes:
        return False, "empty"

    try:
        image = Image.open(
            io.BytesIO(image_bytes)
        )

        width, height = image.size

        image_format = (
            image.format or ""
        ).upper()

        if width < 1000:
            return (
                False,
                f"width too small: {width}",
            )

        if height < 500:
            return (
                False,
                f"height too small: {height}",
            )

        if image_format not in {
            "PNG",
            "JPEG",
            "WEBP",
        }:
            return (
                False,
                f"unsupported format: {image_format}",
            )

        return (
            True,
            f"{width}x{height} {image_format}",
        )

    except Exception as exc:
        return (
            False,
            f"invalid image: {exc}",
        )


# ======================================================================
# 检测明显错误的分格结构
# ======================================================================

def detect_grid_structure(
    image_bytes: bytes,
) -> bool:

    try:
        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        width, height = image.size

        # 这里只做非常保守的检测。
        # 不进行复杂 AI 判断，避免误杀正常图片。

        if width < 2 or height < 2:
            return True

        # 检查中央横/竖区域是否出现极端一致的亮度分隔线。
        # 仅用于捕获非常明显的拼接图。
        pixels = image.load()

        center_x = width // 2
        center_y = height // 2

        vertical_samples = []

        for y in range(
            0,
            height,
            max(1, height // 50),
        ):
            r, g, b = pixels[
                center_x,
                y,
            ]

            vertical_samples.append(
                (r + g + b) / 3
            )

        horizontal_samples = []

        for x in range(
            0,
            width,
            max(1, width // 50),
        ):
            r, g, b = pixels[
                x,
                center_y,
            ]

            horizontal_samples.append(
                (r + g + b) / 3
            )

        def extreme_ratio(values):
            if not values:
                return 0

            mean = sum(values) / len(values)

            if mean <= 1:
                return 1

            extreme = sum(
                1
                for value in values
                if abs(value - mean)
                > 100
            )

            return extreme / len(values)

        # 只在非常明显时判定
        if extreme_ratio(
            vertical_samples
        ) > 0.85:
            return True

        if extreme_ratio(
            horizontal_samples
        ) > 0.85:
            return True

        return False

    except Exception:
        return False


# ======================================================================
# OCR 检查
# ======================================================================

def ocr_text_quality_check(
    image_bytes: bytes,
) -> bool:
    """
    当前版本继续关闭 OCR。

    原因：
    新闻图片允许出现自然场景中的少量文字，
    强行 OCR 容易误杀正常图片。

    保留函数接口，后续可以独立升级。
    """

    log("    OCR CHECK: DISABLED")

    return True


# ======================================================================
# 综合视觉质量检查
# ======================================================================

def visual_quality_check(
    image_bytes: bytes,
) -> Tuple[bool, str]:

    valid, detail = validate_image_bytes(
        image_bytes
    )

    if not valid:
        return False, detail

    if detect_grid_structure(
        image_bytes
    ):
        return (
            False,
            "possible grid/split layout",
        )

    if not ocr_text_quality_check(
        image_bytes
    ):
        return (
            False,
            "OCR text quality failed",
        )

    return True, detail


# ======================================================================
# 生成并验证图片
# ======================================================================

def generate_validated_image(
    prompt: str,
    output_path: Path,
) -> bool:

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    correction_prompt = ""

    for attempt in range(
        1,
        IMAGE_RETRIES + 1,
    ):

        current_prompt = prompt

        if correction_prompt:
            current_prompt += (
                "\n\n请修正上一张图片的问题：\n"
                + correction_prompt
            )

        log(
            f"  🖼️ 生成图片 "
            f"{attempt}/{IMAGE_RETRIES}"
        )

        image_bytes = (
            generate_image_from_agnes(
                current_prompt
            )
        )

        if not image_bytes:
            correction_prompt = (
                "上一轮没有得到有效图片。"
                "请重新生成完整的单幅16:9新闻专题插图。"
            )
            continue

        valid, detail = (
            visual_quality_check(
                image_bytes
            )
        )

        if valid:
            output_path.write_bytes(
                image_bytes
            )

            log(
                f"  ✅ 图片通过验证："
                f"{output_path}"
                f" ({detail})"
            )

            return True

        log(
            f"  ⚠️ 图片验证失败："
            f"{detail}"
        )

        correction_prompt = (
            "上一轮图片未通过质量检查："
            f"{detail}。"
            "请生成一张完整、单幅、"
            "无分格、无拼贴、16:9 的新闻专题插图。"
        )

        # 删除无效文件，避免留下坏图
        try:
            if output_path.exists():
                output_path.unlink()
        except Exception:
            pass

    log(
        f"  ❌ 图片最终生成失败："
        f"{output_path}"
    )

    return False


# ======================================================================
# 已存在图片验证
# ======================================================================

def validate_existing_image(
    image_path: Path,
) -> bool:

    if not image_path.exists():
        return False

    try:
        image_bytes = (
            image_path.read_bytes()
        )

        valid, detail = (
            visual_quality_check(
                image_bytes
            )
        )

        if valid:
            log(
                f"  ✅ 已有图片有效："
                f"{image_path.name} "
                f"({detail})"
            )

            return True

        log(
            f"  ⚠️ 已有图片无效："
            f"{image_path.name} "
            f"({detail})"
        )

        return False

    except Exception as exc:
        log(
            f"  ⚠️ 读取已有图片失败："
            f"{image_path} | {exc}"
        )

        return False


# ======================================================================
# 图片规划
# ======================================================================

def build_image_plan(
    news: List[str],
) -> List[Tuple[str, str, str]]:

    """
    返回：
        [
            (文件名, 新闻内容, 图片位置),
            ...
        ]

    优先使用最新新闻作为首图。
    """

    if not news:
        return []

    latest = news[-1]

    plan: List[
        Tuple[str, str, str]
    ] = []

    plan.append(
        (
            "首图.png",
            latest,
            "首图",
        )
    )

    plan.append(
        (
            "插图1.png",
            latest,
            "主题插图",
        )
    )

    if len(news) >= 2:
        plan.append(
            (
                "插图2.png",
                news[-2],
                "第二重点新闻插图",
            )
        )
    else:
        plan.append(
            (
                "插图2.png",
                latest,
                "第二主题插图",
            )
        )

    if len(news) >= 3:
        plan.append(
            (
                "插图3.png",
                news[-3],
                "第三重点新闻插图",
            )
        )
    else:
        plan.append(
            (
                "插图3.png",
                latest,
                "第三主题插图",
            )
        )

    return plan[:TARGET_IMAGE_COUNT]


# ======================================================================
# Markdown 中清除旧图片引用
# ======================================================================

def remove_old_image_refs(
    markdown: str,
) -> str:

    # Markdown 图片
    markdown = re.sub(
        r"!$begin:math:display$\[\^$end:math:display$]*\]$begin:math:text$\[\^\)\]\+$end:math:text$\s*",
        "",
        markdown,
    )

    # HTML img
    markdown = re.sub(
        r"<img[^>]*>\s*",
        "",
        markdown,
        flags=re.IGNORECASE,
    )

    return markdown


# ======================================================================
# 创建带图 Markdown
# ======================================================================

def create_image_markdown(
    report_path: Path,
    image_dir: Path,
    image_paths: List[Path],
    output_path: Path,
) -> bool:

    try:
        markdown = report_path.read_text(
            encoding="utf-8"
        )

        markdown = remove_old_image_refs(
            markdown
        ).rstrip()

        if not image_paths:
            log(
                "  ⚠️ 没有可写入的图片"
            )
            return False

        lines = [
            "",
            "",
            "---",
            "",
            "## 🖼️ 配图",
            "",
        ]

        for image_path in image_paths:

            try:
                relative = image_path.relative_to(
                    report_path.parent
                )

                image_ref = (
                    relative.as_posix()
                )

            except ValueError:
                # 如果图片不在报告目录下，
                # 使用从系统根目录计算的相对路径。
                relative = os.path.relpath(
                    image_path,
                    report_path.parent,
                )

                image_ref = Path(
                    relative
                ).as_posix()

            lines.extend(
                [
                    f"![{image_path.stem}]"
                    f"({image_ref})",
                    "",
                ]
            )

        final_text = (
            markdown
            + "\n".join(lines)
            + "\n"
        )

        output_path.write_text(
            final_text,
            encoding="utf-8",
        )

        log(
            f"  ✅ 带图 Markdown："
            f"{output_path}"
        )

        return True

    except Exception as exc:
        log(
            f"  ❌ 写入带图 Markdown 失败："
            f"{exc}"
        )

        return False


# ======================================================================
# 生成单份报告图片
# ======================================================================

def generate_report_images(
    report_path: Path,
    image_dir: Path,
    report_type: str,
    output_markdown: Path,
) -> bool:

    log("")
    log("=" * 70)
    log(
        f"🖼️ {report_type}图片生成"
    )
    log("=" * 70)

    log(
        f"报告：{report_path}"
    )

    try:
        markdown = report_path.read_text(
            encoding="utf-8"
        )
    except Exception as exc:
        log(
            f"❌ 读取报告失败：{exc}"
        )
        return False

    news = extract_news_items(
        markdown
    )

    if not news:
        log(
            "⚠️ 报告没有提取到可用新闻内容"
        )
        return False

    log(
        f"新闻主题数量：{len(news)}"
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    plan = build_image_plan(
        news
    )

    generated_paths: List[Path] = []

    for filename, item, position in plan:

        output_path = (
            image_dir / filename
        )

        log("")
        log(
            f"📌 {filename}"
        )
        log(
            f"   主题：{item[:300]}"
        )

        # ==============================================================
        # V5.3：
        # FORCE_REGENERATE=true 时，不使用已有图片。
        # 每天重新根据当前报告生成。
        # ==============================================================

        if (
            output_path.exists()
            and not FORCE_REGENERATE
        ):
            if validate_existing_image(
                output_path
            ):
                generated_paths.append(
                    output_path
                )
                continue

        if FORCE_REGENERATE:
            log(
                "  🔄 FORCE_REGENERATE=true"
                " → 强制重新生成"
            )

            try:
                if output_path.exists():
                    output_path.unlink()
            except Exception as exc:
                log(
                    f"  ⚠️ 删除旧图片失败：{exc}"
                )

        prompt = build_visual_prompt(
            item=item,
            report_type=report_type,
            position=position,
        )

        success = (
            generate_validated_image(
                prompt=prompt,
                output_path=output_path,
            )
        )

        if success:
            generated_paths.append(
                output_path
            )

        # 控制 API 请求速度
        if IMAGE_THROTTLE > 0:
            time.sleep(
                IMAGE_THROTTLE
            )

    # ==================================================================
    # 图片数量检查
    # ==================================================================

    if len(generated_paths) < MIN_IMAGE_COUNT:
        log(
            f"❌ 图片数量不足："
            f"{len(generated_paths)}"
            f"/{MIN_IMAGE_COUNT}"
        )

        return False

    # ==================================================================
    # 生成 _带图.md
    # ==================================================================

    return create_image_markdown(
        report_path=report_path,
        image_dir=image_dir,
        image_paths=generated_paths,
        output_path=output_markdown,
    )


# ======================================================================
# 日报
# ======================================================================

def process_daily_report(
    target_date: date,
) -> bool:

    date_key = target_date.isoformat()

    log("")
    log(
        f"📅 处理日报：{date_key}"
    )

    report_path = find_daily_report(
        target_date
    )

    if not report_path:
        log(
            f"⏭️ 日报不存在，SKIP："
            f"{date_key}"
        )

        return False

    image_dir = (
        DAILY_IMAGE_ROOT
        / date_key
    )

    output_markdown = (
        report_path.parent
        / f"{report_path.stem}_带图.md"
    )

    return generate_report_images(
        report_path=report_path,
        image_dir=image_dir,
        report_type="日报",
        output_markdown=output_markdown,
    )


# ======================================================================
# 周报
# ======================================================================

def process_weekly_report(
    year: int,
    week: int,
) -> bool:

    week_key = f"W{week:02d}"

    log("")
    log(
        "=" * 70
    )
    log(
        f"📅 处理当前周报："
        f"{year}-{week_key}"
    )
    log(
        "🔄 V5.3：每次运行重新读取当前周报"
    )
    log(
        "🔄 同一 ISO 周始终使用同一个 Wxx 文件"
    )
    log(
        "=" * 70
    )

    report_path = find_weekly_report(
        week_key=week_key,
        year=year,
    )

    if not report_path:
        log(
            f"⏭️ 当前周报不存在，SKIP："
            f"{year}/{week_key}.md"
        )

        return False

    log(
        f"✅ 当前周报："
        f"{report_path}"
    )

    # ==============================================================
    # 关键：
    # 周报图片目录严格绑定：
    #
    # 04_图片/周报/2026-W39/
    #
    # 不根据报告文件修改日期判断。
    # ==============================================================
    image_dir = (
        WEEKLY_IMAGE_ROOT
        / f"{year}-{week_key}"
    )

    output_markdown = (
        report_path.parent
        / f"{report_path.stem}_带图.md"
    )

    return generate_report_images(
        report_path=report_path,
        image_dir=image_dir,
        report_type="周报",
        output_markdown=output_markdown,
    )


# ======================================================================
# 当前日期
# ======================================================================

def target_dates() -> List[date]:

    today = now_local().date()

    return [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]


# ======================================================================
# 主程序
# ======================================================================

def main() -> int:

    log("=" * 70)
    log(
        "748686 自生长知识系统"
    )
    log(
        "Knowledge Image V5.3"
    )
    log("=" * 70)

    log(
        f"运行时间：{now_local().isoformat()}"
    )

    log(
        f"AGNES Base URL："
        f"{AGNES_BASE_URL}"
    )

    log(
        f"AGNES Image Model："
        f"{AGNES_IMAGE_MODEL}"
    )

    log(
        f"Image Size：{IMAGE_SIZE}"
    )

    log(
        f"Image Ratio：{IMAGE_RATIO}"
    )

    log(
        f"FORCE_REGENERATE："
        f"{FORCE_REGENERATE}"
    )

    # ==================================================================
    # API Key
    # ==================================================================

    if not AGNES_API_KEY:
        log(
            "❌ AGNES_API_KEY / AI_API_KEY 未设置"
        )
        return 1

    # ==================================================================
    # 统计
    # ==================================================================

    success_count = 0
    failure_count = 0
    actual_task_count = 0

    # ==================================================================
    # 日报
    # ==================================================================

    dates = target_dates()

    log("")
    log(
        "📋 日报处理日期："
        + ", ".join(
            d.isoformat()
            for d in dates
        )
    )

    for target_date in dates:

        report_path = find_daily_report(
            target_date
        )

        if not report_path:
            log(
                f"⏭️ 日报不存在："
                f"{target_date.isoformat()}"
            )
            continue

        actual_task_count += 1

        try:
            success = (
                process_daily_report(
                    target_date
                )
            )

            if success:
                success_count += 1
            else:
                failure_count += 1

        except Exception as exc:
            failure_count += 1

            log(
                f"❌ 日报处理异常："
                f"{target_date} | {exc}"
            )

    # ==================================================================
    # V5.3：
    # 周报只处理“当前 ISO 周”
    #
    # 不再从：
    # TODAY / YESTERDAY / DAY_BEFORE
    # 推导多个 week。
    #
    # 这样可以确保：
    #
    # 09-21 → W39
    # 09-22 → W39
    # 09-23 → W39
    # ...
    # 09-27 → W39
    #
    # 09-28 → W40
    #
    # ==================================================================

    current_year, current_week, current_week_key = (
        current_iso_week()
    )

    log("")
    log("=" * 70)
    log(
        "📘 当前 ISO 周："
        f"{current_year}-{current_week_key}"
    )
    log(
        "📘 本次只处理这一周的周报"
    )
    log("=" * 70)

    weekly_report = find_weekly_report(
        week_key=current_week_key,
        year=current_year,
    )

    if not weekly_report:
        log(
            "⏭️ 当前 ISO 周没有周报，SKIP："
            f"{current_year}/{current_week_key}.md"
        )

    else:
        actual_task_count += 1

        try:
            success = process_weekly_report(
                year=current_year,
                week=current_week,
            )

            if success:
                success_count += 1
            else:
                failure_count += 1

        except Exception as exc:
            failure_count += 1

            log(
                f"❌ 周报处理异常："
                f"{current_year}-{current_week_key} | "
                f"{exc}"
            )

    # ==================================================================
    # 最终结果
    # ==================================================================

    log("")
    log("=" * 70)
    log(
        "📊 Knowledge Image V5.3 完成"
    )
    log("=" * 70)

    log(
        f"成功：{success_count}"
    )

    log(
        f"失败：{failure_count}"
    )

    log(
        f"实际任务：{actual_task_count}"
    )

    # ==================================================================
    # 没有任何报告
    # ==================================================================

    if actual_task_count == 0:
        log(
            "ℹ️ 当前没有任何可处理的日报/周报"
        )

        return 0

    # ==================================================================
    # 有成功
    # ==================================================================

    if success_count > 0:
        log(
            "✅ 至少一个报告处理成功"
        )

        return 0

    # ==================================================================
    # 全部失败
    # ==================================================================

    if failure_count > 0:
        log(
            "❌ 所有实际任务均处理失败"
        )

        return 1

    return 0


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":
    sys.exit(
        main()
    )
