#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V5.4.1

======================================================================
V5.4.1
======================================================================

仅修复报告目录路径：

日报：
    05_日报/YYYY/MM/YYYY-MM-DD.md

周报：
    06_周报/YYYY/YYYY-Wxx.md

同时修复 *_带图.md 中图片相对路径，使其适配新的报告目录层级。

其它逻辑保持 V5.4 不变。
======================================================================
"""

from __future__ import annotations

import os
import re
import sys
import base64
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import requests


# ======================================================================
# 基础配置
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]

REPORT_DIR = ROOT / "05_日报"
WEEKLY_DIR = ROOT / "06_周报"
IMAGE_DIR = ROOT / "04_图片"

AGNES_API_KEY = (
    os.environ.get("AGNES_API_KEY")
    or os.environ.get("AI_API_KEY")
    or ""
).strip()

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"
IMAGE_MODEL = "agnes-image-2.5-flash"

MIN_IMAGE_COUNT = 3
TARGET_IMAGE_COUNT = 4

REQUEST_TIMEOUT = 180
MAX_RETRY = 3

TIMEZONE = "Asia/Shanghai"


# ======================================================================
# 日志
# ======================================================================

def log(message: str = ""):
    print(message, flush=True)


# ======================================================================
# 时间
# ======================================================================

def get_today() -> str:
    from zoneinfo import ZoneInfo

    now = datetime.now(ZoneInfo(TIMEZONE))

    return now.strftime("%Y-%m-%d")


def get_report_dates() -> List[str]:
    today = get_today()

    dt = datetime.strptime(today, "%Y-%m-%d")

    yesterday = dt - timedelta(days=1)
    day_before = dt - timedelta(days=2)

    return [
        today,
        yesterday.strftime("%Y-%m-%d"),
        day_before.strftime("%Y-%m-%d"),
    ]


def get_current_week() -> str:
    from zoneinfo import ZoneInfo

    now = datetime.now(ZoneInfo(TIMEZONE))

    iso = now.isocalendar()

    return f"{iso.year}-W{iso.week:02d}"


# ======================================================================
# 路径
# ======================================================================

def get_daily_report_path(report_date: str) -> Path:
    """
    日报真实目录：

        05_日报/YYYY/MM/YYYY-MM-DD.md
    """

    year = report_date[:4]
    month = report_date[5:7]

    return (
        REPORT_DIR
        / year
        / month
        / f"{report_date}.md"
    )


def get_weekly_report_path(week: str) -> Path:
    """
    周报真实目录：

        06_周报/YYYY/YYYY-Wxx.md
    """

    year = week[:4]

    return (
        WEEKLY_DIR
        / year
        / f"{week}.md"
    )


def make_relative_image_ref(
    report_path: Path,
    image_path: Path,
) -> str:
    """
    根据报告实际所在目录生成图片相对路径。

    日报：
        05_日报/YYYY/MM/
              ↓
        ../../../04_图片/日报/YYYY-MM-DD/xxx.png

    周报：
        06_周报/YYYY/
              ↓
        ../../04_图片/周报/YYYY-Wxx/xxx.png
    """

    return Path(
        os.path.relpath(
            image_path,
            start=report_path.parent,
        )
    ).as_posix()


# ======================================================================
# 报告图片引用清理
# ======================================================================

def remove_old_image_refs(lines: List[str]) -> List[str]:
    new_lines = []

    skip_image_section = False

    for line in lines:

        stripped = line.strip()

        if stripped == "## 🖼️ 配图":
            skip_image_section = True
            continue

        if skip_image_section:
            continue

        # 删除旧版图片引用。
        #
        # 旧路径：
        #   ../04_图片/...
        #
        # 新路径：
        #   ../../04_图片/...
        #   ../../../04_图片/...
        #
        if re.match(
            r"!\[[^\]]*\]\((?:\.\./)+04_图片/.*\)",
            stripped,
        ):
            continue

        new_lines.append(line)

    return new_lines


# ======================================================================
# 新闻内容提取
# ======================================================================

def extract_news_from_report(
    report_path: Path,
) -> List[str]:

    text = report_path.read_text(
        encoding="utf-8"
    )

    lines = text.splitlines()

    news = []

    current = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            if current:
                news.append(
                    " ".join(current)
                )
                current = []

            continue

        current.append(stripped)

    if current:
        news.append(
            " ".join(current)
        )

    return news


# ======================================================================
# 图片 Prompt
# ======================================================================

def build_image_prompt(
    report_title: str,
    news_text: str,
    image_type: str,
) -> str:

    if image_type == "cover":
        role = """
Create a realistic editorial news photograph suitable as the
cover image of a high-quality international news report.
"""

    else:
        role = """
Create a realistic editorial news photograph illustrating the
specific news event described below.
"""

    prompt = f"""
{role}

Topic:
{report_title}

News context:
{news_text}

Requirements:

- realistic professional photojournalism
- one clear visual center
- cinematic but natural lighting
- realistic human subjects and environments when appropriate
- visually connected to the actual news event
- no text
- no letters
- no numbers
- no captions
- no logos
- no watermark
- no infographic
- no collage
- no split screen
- no UI
- no abstract symbols
- no ASCII
- no fake newspaper layout
- no duplicated subjects
- no distorted anatomy

The image must look like a real photograph taken by a professional
news photographer.
"""

    return prompt.strip()


# ======================================================================
# AGNES 图片生成
# ======================================================================

def generate_image(
    prompt: str,
    output_path: Path,
) -> bool:

    if not AGNES_API_KEY:
        log("❌ AGNES_API_KEY 未配置")
        return False

    url = (
        AGNES_BASE_URL.rstrip("/")
        + "/images/generations"
    )

    headers = {
        "Authorization": f"Bearer {AGNES_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
        "size": "2624x1472",
    }

    for attempt in range(
        1,
        MAX_RETRY + 1,
    ):

        try:

            log(
                f"   🎨 生成图片 "
                f"(attempt {attempt}/{MAX_RETRY})"
            )

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            )

            if response.status_code != 200:

                log(
                    f"   ⚠️ HTTP {response.status_code}: "
                    f"{response.text[:500]}"
                )

                continue

            data = response.json()

            image_url = None
            image_b64 = None

            if isinstance(data, dict):

                data_items = data.get(
                    "data",
                    [],
                )

                if data_items:

                    first = data_items[0]

                    image_url = first.get(
                        "url"
                    )

                    image_b64 = first.get(
                        "b64_json"
                    )

            if image_b64:

                output_path.write_bytes(
                    base64.b64decode(
                        image_b64
                    )
                )

                return True

            if image_url:

                image_response = requests.get(
                    image_url,
                    timeout=REQUEST_TIMEOUT,
                )

                if image_response.status_code == 200:

                    output_path.write_bytes(
                        image_response.content
                    )

                    return True

                log(
                    "   ⚠️ 图片下载失败: "
                    f"{image_response.status_code}"
                )

            else:

                log(
                    "   ⚠️ API 返回中没有图片数据"
                )

        except Exception as exc:

            log(
                f"   ⚠️ 图片生成异常: {exc}"
            )

    return False


# ======================================================================
# 图片验证
# ======================================================================

def validate_image(
    image_path: Path,
) -> bool:

    if not image_path.exists():
        return False

    try:

        from PIL import Image

        with Image.open(image_path) as img:

            img.verify()

        if image_path.stat().st_size < 10_000:
            return False

        return True

    except Exception as exc:

        log(
            f"   ⚠️ 图片验证失败: "
            f"{image_path.name}: {exc}"
        )

        return False


# ======================================================================
# 图片计划
# ======================================================================

def build_image_plan(
    report_title: str,
    news_items: List[str],
) -> List[Dict[str, str]]:

    plan = []

    if news_items:

        plan.append(
            {
                "name": "首图.png",
                "type": "cover",
                "content": news_items[0],
            }
        )

    for index, item in enumerate(
        news_items[1:4],
        start=1,
    ):

        plan.append(
            {
                "name": f"插图{index}.png",
                "type": "article",
                "content": item,
            }
        )

    return plan[:TARGET_IMAGE_COUNT]


# ======================================================================
# 生成带图 Markdown
# ======================================================================

def create_image_markdown(
    report_path: Path,
    image_dir: Path,
    image_paths: List[Path],
) -> Optional[Path]:

    try:

        text = report_path.read_text(
            encoding="utf-8"
        )

        lines = text.splitlines()

        lines = remove_old_image_refs(lines)

        output_lines = []

        inserted = False

        for line in lines:

            output_lines.append(line)

            if (
                not inserted
                and line.strip().startswith("#")
            ):

                if image_paths:

                    output_lines.append("")

                    cover_path = image_paths[0]

                    cover_ref = make_relative_image_ref(
                        report_path,
                        cover_path,
                    )

                    output_lines.append(
                        f"![首图]({cover_ref})"
                    )

                    inserted = True

        if not inserted and image_paths:

            output_lines.insert(
                0,
                f"![首图]({make_relative_image_ref(report_path, image_paths[0])})"
            )

        if len(image_paths) > 1:

            output_lines.append("")

            output_lines.append(
                "## 🖼️ 配图"
            )

            for image_path in image_paths[1:]:

                image_ref = make_relative_image_ref(
                    report_path,
                    image_path,
                )

                output_lines.append("")

                output_lines.append(
                    f"![{image_path.stem}]({image_ref})"
                )

        output_path = (
            report_path.parent
            / f"{report_path.stem}_带图.md"
        )

        output_path.write_text(
            "\n".join(output_lines)
            + "\n",
            encoding="utf-8",
        )

        return output_path

    except Exception as exc:

        log(
            f"❌ 创建带图 Markdown 失败: {exc}"
        )

        return None


# ======================================================================
# 核心图片处理
# ======================================================================

def generate_report_images(
    report_path: Path,
    report_date: str,
    report_type: str,
    force_regenerate: bool = False,
) -> bool:

    if not report_path.exists():

        log(
            f"⚠️ 报告不存在: {report_path}"
        )

        return False

    if report_type == "daily":

        image_dir = (
            IMAGE_DIR
            / "日报"
            / report_date
        )

    else:

        image_dir = (
            IMAGE_DIR
            / "周报"
            / report_date
        )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log(
        f"📄 报告: {report_path}"
    )

    log(
        f"🖼️ 图片目录: {image_dir}"
    )

    news_items = extract_news_from_report(
        report_path
    )

    if not news_items:

        log(
            "⚠️ 未提取到新闻内容"
        )

        return False

    log(
        f"   新闻内容: {len(news_items)} 条"
    )

    existing_images = []

    for name in [
        "首图.png",
        "插图1.png",
        "插图2.png",
        "插图3.png",
    ]:

        path = image_dir / name

        if validate_image(path):
            existing_images.append(path)

    if (
        not force_regenerate
        and len(existing_images) >= MIN_IMAGE_COUNT
    ):

        log(
            f"✅ 已存在有效图片 "
            f"{len(existing_images)} 张，跳过生成"
        )

        output_path = create_image_markdown(
            report_path,
            image_dir,
            existing_images,
        )

        return output_path is not None

    if force_regenerate:

        log(
            "🔄 FORCE_REGENERATE: 重新生成图片"
        )

        for path in image_dir.glob("*.png"):

            try:
                path.unlink()
            except Exception:
                pass

    report_title = report_path.stem

    image_plan = build_image_plan(
        report_title,
        news_items,
    )

    generated_images = []

    for item in image_plan:

        image_path = (
            image_dir
            / item["name"]
        )

        prompt = build_image_prompt(
            report_title,
            item["content"],
            item["type"],
        )

        log(
            f"   🎨 生成: {item['name']}"
        )

        success = generate_image(
            prompt,
            image_path,
        )

        if not success:

            log(
                f"   ❌ 生成失败: "
                f"{item['name']}"
            )

            continue

        if validate_image(image_path):

            generated_images.append(
                image_path
            )

            log(
                f"   ✅ 图片有效: "
                f"{item['name']}"
            )

        else:

            log(
                f"   ❌ 图片验证失败: "
                f"{item['name']}"
            )

    if len(generated_images) < MIN_IMAGE_COUNT:

        log(
            f"❌ 有效图片不足: "
            f"{len(generated_images)} / "
            f"{MIN_IMAGE_COUNT}"
        )

        return False

    output_path = create_image_markdown(
        report_path,
        image_dir,
        generated_images,
    )

    if output_path is None:

        return False

    log(
        f"✅ 带图报告已生成: "
        f"{output_path}"
    )

    return True


# ======================================================================
# 日报
# ======================================================================

def process_daily_report(
    report_date: str,
) -> bool:

    report_path = get_daily_report_path(
        report_date
    )

    log("")
    log(
        f"📰 日报图片处理: {report_date}"
    )

    return generate_report_images(
        report_path=report_path,
        report_date=report_date,
        report_type="daily",
        force_regenerate=False,
    )


# ======================================================================
# 周报
# ======================================================================

def process_weekly_report(
    week: str,
) -> bool:

    report_path = get_weekly_report_path(
        week
    )

    log("")
    log(
        f"📊 周报图片处理: {week}"
    )

    if not report_path.exists():

        log(
            f"⏭️ 当前周报不存在，SKIP: "
            f"{report_path}"
        )

        return True

    return generate_report_images(
        report_path=report_path,
        report_date=week,
        report_type="weekly",
        force_regenerate=True,
    )


# ======================================================================
# 主程序
# ======================================================================

def main() -> int:

    log("")
    log("=" * 70)
    log("748686 自生长知识系统")
    log("Knowledge Image Engine V5.4.1")
    log("=" * 70)
    log("")

    report_dates = get_report_dates()

    today = report_dates[0]

    # --------------------------------------------------------------
    # 日报
    # --------------------------------------------------------------

    today_success = False

    for index, report_date in enumerate(
        report_dates
    ):

        success = process_daily_report(
            report_date
        )

        if index == 0:

            today_success = success

            if not success:

                log(
                    "❌ TODAY 日报图片处理失败"
                )

        else:

            if not get_daily_report_path(
                report_date
            ).exists():

                log(
                    f"⏭️ 历史日报不存在，跳过: "
                    f"{report_date}"
                )

    # --------------------------------------------------------------
    # 周报
    # --------------------------------------------------------------

    current_week = get_current_week()

    weekly_report = get_weekly_report_path(
        current_week
    )

    if weekly_report.exists():

        process_weekly_report(
            current_week
        )

    else:

        log(
            f"⏭️ 当前周报不存在，SKIP: "
            f"{weekly_report}"
        )

    # --------------------------------------------------------------
    # TODAY 必须成功
    # --------------------------------------------------------------

    if not today_success:

        log("")
        log(
            "❌ TODAY 日报图片处理失败"
        )

        return 1

    log("")
    log("=" * 70)
    log("✅ Knowledge Image Engine 完成")
    log("=" * 70)

    return 0


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )
