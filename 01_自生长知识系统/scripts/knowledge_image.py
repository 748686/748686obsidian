#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V5.4

======================================================================
核心职责
======================================================================

1. 读取已经生成的日报 / 周报 Markdown
2. 根据报告内容生成：
       首图.png
       插图1.png
       插图2.png
       插图3.png
3. 使用 AGNES Image Model
4. 图片质量检查
5. 日报：
       已存在完整有效图片 → SKIP
6. 周报：
       当前 ISO 周每次重新生成
7. 生成 *_带图.md
8. 首图放在文章最顶部
9. 插图插入对应正文主题附近
10. 日报与周报使用完全相同的图片排版逻辑

======================================================================
"""

from __future__ import annotations

import base64
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from PIL import Image


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

def log(message: str) -> None:
    print(message, flush=True)


# ======================================================================
# 日期
# ======================================================================

def get_today() -> str:
    """
    使用 Asia/Shanghai 作为业务日期。
    """
    try:
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo(TIMEZONE))
    except Exception:
        now = datetime.utcnow() + timedelta(hours=8)

    return now.strftime("%Y-%m-%d")


def get_report_dates() -> List[str]:
    """
    TODAY → YESTERDAY → DAY-BEFORE
    """
    today = get_today()
    dt = datetime.strptime(today, "%Y-%m-%d")

    return [
        today,
        (dt - timedelta(days=1)).strftime("%Y-%m-%d"),
        (dt - timedelta(days=2)).strftime("%Y-%m-%d"),
    ]


# ======================================================================
# 周
# ======================================================================

def get_current_week() -> str:
    """
    当前 ISO Week。
    """
    try:
        from zoneinfo import ZoneInfo

        now = datetime.now(ZoneInfo(TIMEZONE))
    except Exception:
        now = datetime.utcnow() + timedelta(hours=8)

    iso = now.isocalendar()

    return f"{iso.year}-W{iso.week:02d}"


# ======================================================================
# Markdown 工具
# ======================================================================

def remove_old_image_refs(markdown: str) -> str:
    """
    删除旧版本生成的图片引用以及旧配图区。

    注意：
    不删除普通正文，只清理本引擎曾经产生的图片引用。
    """

    lines = markdown.splitlines()

    cleaned: List[str] = []

    skip_image_section = False

    for line in lines:

        stripped = line.strip()

        # 旧版本的配图区
        if stripped == "## 🖼️ 配图":
            skip_image_section = True
            continue

        if skip_image_section:
            # 配图区直到正文结束，因此直接跳过
            continue

        # 删除本引擎生成的图片 Markdown
        if re.match(
            r"!\[[^\]]*\]\(\.\./04_图片/.*\)",
            stripped,
        ):
            continue

        cleaned.append(line)

    return "\n".join(cleaned).strip()


# ======================================================================
# 新闻提取
# ======================================================================

def extract_news_from_report(markdown: str) -> List[Dict]:
    """
    从日报 / 周报中提取基础新闻信息。

    当前版本只用于生成图片主题。
    """

    news: List[Dict] = []

    lines = markdown.splitlines()

    current_title = ""
    current_content: List[str] = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        # 标题
        if stripped.startswith("#"):
            if current_title:
                content = " ".join(current_content).strip()

                if content:
                    news.append(
                        {
                            "title": current_title,
                            "content": content,
                        }
                    )

            current_title = re.sub(
                r"^#+\s*",
                "",
                stripped,
            ).strip()

            current_content = []

        else:
            current_content.append(stripped)

    if current_title:
        content = " ".join(current_content).strip()

        if content:
            news.append(
                {
                    "title": current_title,
                    "content": content,
                }
            )

    return news


# ======================================================================
# 图片 Prompt
# ======================================================================

def build_image_prompt(
    news_item: Dict,
    image_type: str,
    report_type: str,
) -> str:

    title = str(
        news_item.get("title", "")
    ).strip()

    content = str(
        news_item.get("content", "")
    ).strip()

    if len(content) > 1200:
        content = content[:1200]

    if image_type == "首图":
        style = (
            "Create a cinematic editorial cover image representing "
            "the overall themes and major developments of this report."
        )

    elif image_type == "主题插图":
        style = (
            "Create a realistic editorial news photograph representing "
            "the main theme of this report section."
        )

    elif image_type == "第二重点新闻插图":
        style = (
            "Create a realistic editorial news photograph representing "
            "the second major news development."
        )

    else:
        style = (
            "Create a realistic editorial news photograph representing "
            "another important development in this report."
        )

    prompt = f"""
{style}

Report type:
{report_type}

News title:
{title}

News context:
{content}

Requirements:
- realistic editorial news photography
- one clear visual center
- natural photographic composition
- visually meaningful scene
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
- no chart
- no artificial typography
"""

    return prompt.strip()


# ======================================================================
# AGNES Image API
# ======================================================================

def generate_image(
    prompt: str,
    output_path: Path,
) -> bool:

    if not AGNES_API_KEY:
        log("❌ AGNES_API_KEY / AI_API_KEY 未设置")
        return False

    url = f"{AGNES_BASE_URL}/images/generations"

    headers = {
        "Authorization": f"Bearer {AGNES_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": IMAGE_MODEL,
        "prompt": prompt,
    }

    for attempt in range(1, MAX_RETRY + 1):

        try:
            log(
                f"      🎨 AGNES 图片生成 "
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
                    f"      ⚠️ AGNES HTTP "
                    f"{response.status_code}: "
                    f"{response.text[:500]}"
                )

                if attempt < MAX_RETRY:
                    time.sleep(2 * attempt)

                continue

            data = response.json()

            image_data = None

            if isinstance(data, dict):

                result = data.get("data")

                if isinstance(result, list) and result:
                    first = result[0]

                    if isinstance(first, dict):

                        if first.get("b64_json"):
                            image_data = base64.b64decode(
                                first["b64_json"]
                            )

                        elif first.get("url"):
                            image_response = requests.get(
                                first["url"],
                                timeout=REQUEST_TIMEOUT,
                            )

                            if image_response.status_code == 200:
                                image_data = (
                                    image_response.content
                                )

            if not image_data:
                log("      ❌ AGNES 返回中没有图片数据")

                if attempt < MAX_RETRY:
                    time.sleep(2 * attempt)

                continue

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            output_path.write_bytes(image_data)

            log(
                f"      ✅ 图片已保存: "
                f"{output_path}"
            )

            return True

        except Exception as exc:

            log(
                f"      ⚠️ 图片生成异常: "
                f"{type(exc).__name__}: {exc}"
            )

            if attempt < MAX_RETRY:
                time.sleep(2 * attempt)

    return False


# ======================================================================
# 图片质量检查
# ======================================================================

def validate_image(
    image_path: Path,
) -> bool:

    if not image_path.exists():
        return False

    try:

        if image_path.stat().st_size < 10 * 1024:
            return False

        with Image.open(image_path) as image:

            image.verify()

        with Image.open(image_path) as image:

            width, height = image.size

            if width < 500 or height < 300:
                return False

        return True

    except Exception:
        return False


# ======================================================================
# 图片计划
# ======================================================================

def build_image_plan(
    news: List[Dict],
) -> List[Tuple[str, Dict, str]]:

    if not news:
        return []

    latest = news[-1]

    plan = [
        (
            "首图.png",
            latest,
            "首图",
        ),
        (
            "插图1.png",
            latest,
            "主题插图",
        ),
    ]

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
# 图片 Markdown
# ======================================================================

def create_image_markdown(
    report_path: Path,
    image_dir: Path,
    image_paths: List[Path],
    output_path: Path,
) -> bool:
    """
    创建带图 Markdown。

    排版规则：

    1. 首图.png 永远放在正文最顶部
    2. 插图1 / 插图2 / 插图3 不再统一放到文末
    3. 插图根据 Markdown 的主要主题结构插入正文对应位置
    4. 日报 / 周报完全使用同一套逻辑
    5. 不增加“配图”标题
    6. 不增加“配图1/2/3”等文字标签
    7. 不改变原始正文内容结构
    """

    try:

        markdown = report_path.read_text(
            encoding="utf-8"
        )

        markdown = remove_old_image_refs(
            markdown
        ).strip()

        if not image_paths:

            log(
                "      ⚠️ 没有可用图片，"
                "不生成带图 Markdown"
            )

            return False

        # --------------------------------------------------------------
        # 图片分类
        # --------------------------------------------------------------

        cover_path: Optional[Path] = None

        illustration_paths: List[Path] = []

        for image_path in image_paths:

            if image_path.name == "首图.png":
                cover_path = image_path

            elif image_path.name in {
                "插图1.png",
                "插图2.png",
                "插图3.png",
            }:
                illustration_paths.append(
                    image_path
                )

        # --------------------------------------------------------------
        # 过滤无效图片
        # --------------------------------------------------------------

        valid_illustrations: List[Path] = []

        for image_path in illustration_paths:

            if validate_image(image_path):
                valid_illustrations.append(
                    image_path
                )

        # --------------------------------------------------------------
        # 首图
        # --------------------------------------------------------------

        result: List[str] = []

        if (
            cover_path is not None
            and validate_image(cover_path)
        ):

            cover_ref = (
                f"../04_图片/"
                f"{image_dir.name}/"
                f"{cover_path.name}"
            )

            result.extend(
                [
                    f"![首图]({cover_ref})",
                    "",
                ]
            )

        # --------------------------------------------------------------
        # 没有插图时
        # --------------------------------------------------------------

        if not valid_illustrations:

            final_text = (
                "\n".join(result)
                + markdown
                + "\n"
            )

            output_path.write_text(
                final_text,
                encoding="utf-8",
            )

            return True

        # --------------------------------------------------------------
        # 正文拆分
        # --------------------------------------------------------------
        #
        # 保留每一行，而不是重新生成正文。
        #
        # 这样能够最大限度保持：
        # - 原 Markdown
        # - 表格
        # - 列表
        # - 引用
        # - 粗体
        # - 链接
        # - 空行
        #
        # 完全不被破坏。
        # --------------------------------------------------------------

        body_lines = markdown.splitlines()

        # --------------------------------------------------------------
        # 找主要主题
        # --------------------------------------------------------------
        #
        # 主要主题使用 ###。
        #
        # 排除：
        # 基本信息
        # 数据统计
        # 关键数据
        # 数据源
        # 参考资料
        # 参考来源
        # 明日计划
        # 本周计划
        # 总结
        # 结论
        # 目录
        #
        # 这些区域不是主要新闻主题，不用于插图定位。
        # --------------------------------------------------------------

        excluded_keywords = (
            "基本信息",
            "数据统计",
            "关键数据",
            "数据源",
            "参考资料",
            "参考来源",
            "明日计划",
            "本周计划",
            "总结",
            "结论",
            "目录",
        )

        major_sections: List[Tuple[int, str]] = []

        for index, line in enumerate(body_lines):

            stripped = line.strip()

            if not stripped.startswith("### "):
                continue

            title = stripped[4:].strip()

            if any(
                keyword in title
                for keyword in excluded_keywords
            ):
                continue

            major_sections.append(
                (
                    index,
                    title,
                )
            )

        # --------------------------------------------------------------
        # 为每一个主要主题寻找正文结束 / 子主题位置
        # --------------------------------------------------------------

        section_ranges: List[
            Tuple[int, int, str]
        ] = []

        for section_index, (
            start_index,
            title,
        ) in enumerate(major_sections):

            if section_index + 1 < len(
                major_sections
            ):

                end_index = (
                    major_sections[
                        section_index + 1
                    ][0]
                )

            else:

                end_index = len(body_lines)

            section_ranges.append(
                (
                    start_index,
                    end_index,
                    title,
                )
            )

        # --------------------------------------------------------------
        # 每个主要主题内部寻找 #### 子主题
        # --------------------------------------------------------------

        section_targets: List[int] = []

        for (
            start_index,
            end_index,
            _title,
        ) in section_ranges:

            subsection_indices: List[int] = []

            for index in range(
                start_index + 1,
                end_index,
            ):

                stripped = body_lines[
                    index
                ].strip()

                if stripped.startswith(
                    "#### "
                ):

                    subsection_indices.append(
                        index
                    )

            if subsection_indices:

                # ------------------------------------------------------
                # 位置规则
                #
                # 4 个以上子主题：
                # 插图放在中间偏后的位置。
                #
                # 2～3 个：
                # 插图放在第二个主题前。
                #
                # 1 个：
                # 插图放在唯一主题前。
                #
                # 这样视觉上不会把图片集中到标题区，
                # 而是进入正文内容区域。
                # ------------------------------------------------------

                if len(subsection_indices) >= 4:

                    target = subsection_indices[
                        len(subsection_indices) // 2
                    ]

                elif len(subsection_indices) >= 2:

                    target = subsection_indices[1]

                else:

                    target = subsection_indices[0]

            else:

                # 没有 #### 时，
                # 放在 ### 标题之后、正文开始位置。
                target = start_index + 1

            section_targets.append(
                target
            )

        # --------------------------------------------------------------
        # 图片与主要主题对应
        # --------------------------------------------------------------

        insertion_map: Dict[int, List[Path]] = {}

        if section_targets:

            for image_index, image_path in enumerate(
                valid_illustrations
            ):

                target_index = section_targets[
                    min(
                        image_index,
                        len(section_targets) - 1,
                    )
                ]

                insertion_map.setdefault(
                    target_index,
                    [],
                ).append(
                    image_path
                )

        # --------------------------------------------------------------
        # 如果没有识别到 ### 主要主题
        #
        # 采用正文等距插入。
        #
        # 这是兜底逻辑，不影响正常日报 / 周报。
        # --------------------------------------------------------------

        else:

            paragraph_indices: List[int] = []

            for index, line in enumerate(
                body_lines
            ):

                if line.strip():
                    paragraph_indices.append(
                        index
                    )

            if paragraph_indices:

                interval = max(
                    1,
                    len(paragraph_indices)
                    // (
                        len(valid_illustrations)
                        + 1
                    ),
                )

                for image_index, image_path in enumerate(
                    valid_illustrations
                ):

                    target_position = min(
                        (
                            image_index + 1
                        )
                        * interval,
                        len(paragraph_indices) - 1,
                    )

                    target_index = paragraph_indices[
                        target_position
                    ]

                    insertion_map.setdefault(
                        target_index,
                        [],
                    ).append(
                        image_path
                    )

        # --------------------------------------------------------------
        # 插入正文
        # --------------------------------------------------------------

        for index, line in enumerate(
            body_lines
        ):

            if index in insertion_map:

                for image_path in insertion_map[
                    index
                ]:

                    image_ref = (
                        f"../04_图片/"
                        f"{image_dir.name}/"
                        f"{image_path.name}"
                    )

                    result.extend(
                        [
                            "",
                            f"![{image_path.stem}]"
                            f"({image_ref})",
                            "",
                        ]
                    )

            result.append(line)

        # --------------------------------------------------------------
        # 写出最终文件
        # --------------------------------------------------------------

        final_text = (
            "\n".join(result).strip()
            + "\n"
        )

        output_path.write_text(
            final_text,
            encoding="utf-8",
        )

        log(
            f"      ✅ 带图 Markdown 已生成: "
            f"{output_path}"
        )

        return True

    except Exception as exc:

        log(
            f"      ❌ 创建带图 Markdown 失败: "
            f"{type(exc).__name__}: {exc}"
        )

        return False


# ======================================================================
# 生成日报 / 周报图片
# ======================================================================

def generate_report_images(
    report_path: Path,
    report_type: str,
    report_date: str,
    force_regenerate: bool = False,
) -> bool:

    if not report_path.exists():

        log(
            f"   ⚠️ 报告不存在: {report_path}"
        )

        return False

    # --------------------------------------------------------------
    # 图片目录
    # --------------------------------------------------------------

    if report_type == "日报":

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

    output_path = (
        report_path.parent
        / f"{report_path.stem}_带图.md"
    )

    # --------------------------------------------------------------
    # 日报已有完整图片 → SKIP
    # --------------------------------------------------------------

    if not force_regenerate:

        required_images = [
            image_dir / "首图.png",
            image_dir / "插图1.png",
            image_dir / "插图2.png",
            image_dir / "插图3.png",
        ]

        if all(
            validate_image(path)
            for path in required_images
        ):

            log(
                f"   ⏭️ {report_type} 图片已经完整，"
                f"SKIP 重新生成"
            )

            if output_path.exists():

                log(
                    f"      已存在带图 Markdown，"
                    f"保持原文件"
                )

            else:

                create_image_markdown(
                    report_path,
                    image_dir,
                    required_images,
                    output_path,
                )

            return True

    # --------------------------------------------------------------
    # 周报强制重新生成
    # --------------------------------------------------------------

    if force_regenerate:

        log(
            f"   🔄 {report_type} 当前周期强制重新生成图片"
        )

        for image_name in [
            "首图.png",
            "插图1.png",
            "插图2.png",
            "插图3.png",
        ]:

            image_path = (
                image_dir
                / image_name
            )

            if image_path.exists():

                try:
                    image_path.unlink()

                except Exception as exc:

                    log(
                        f"      ⚠️ 删除旧图片失败: "
                        f"{image_path} "
                        f"{exc}"
                    )

    # --------------------------------------------------------------
    # 读取报告
    # --------------------------------------------------------------

    markdown = report_path.read_text(
        encoding="utf-8"
    )

    news = extract_news_from_report(
        markdown
    )

    if not news:

        log(
            f"   ⚠️ 无法从 {report_type} "
            f"提取新闻内容"
        )

        return False

    # --------------------------------------------------------------
    # 图片计划
    # --------------------------------------------------------------

    image_plan = build_image_plan(
        news
    )

    if not image_plan:

        log(
            f"   ⚠️ 没有图片生成计划"
        )

        return False

    # --------------------------------------------------------------
    # 生成图片
    # --------------------------------------------------------------

    generated_images: List[Path] = []

    for (
        image_name,
        news_item,
        image_type,
    ) in image_plan:

        output_image = (
            image_dir
            / image_name
        )

        # ----------------------------------------------------------
        # 日报单张图片已有且有效 → 保留
        # ----------------------------------------------------------

        if (
            not force_regenerate
            and validate_image(output_image)
        ):

            log(
                f"   ⏭️ 已存在有效图片: "
                f"{image_name}"
            )

            generated_images.append(
                output_image
            )

            continue

        # ----------------------------------------------------------
        # Prompt
        # ----------------------------------------------------------

        prompt = build_image_prompt(
            news_item,
            image_type,
            report_type,
        )

        log(
            f"   🎨 生成 {image_name}"
        )

        success = generate_image(
            prompt,
            output_image,
        )

        if success and validate_image(
            output_image
        ):

            generated_images.append(
                output_image
            )

        else:

            log(
                f"      ❌ {image_name} "
                f"生成或质量检查失败"
            )

    # --------------------------------------------------------------
    # 最低图片数量
    # --------------------------------------------------------------

    valid_images = [
        path
        for path in generated_images
        if validate_image(path)
    ]

    if len(valid_images) < MIN_IMAGE_COUNT:

        log(
            f"   ❌ 有效图片数量不足: "
            f"{len(valid_images)} "
            f"/ {MIN_IMAGE_COUNT}"
        )

        return False

    # --------------------------------------------------------------
    # 创建带图 Markdown
    # --------------------------------------------------------------

    return create_image_markdown(
        report_path,
        image_dir,
        valid_images,
        output_path,
    )


# ======================================================================
# 日报
# ======================================================================

def process_daily_report(
    report_date: str,
) -> bool:

    report_path = (
        REPORT_DIR
        / f"{report_date}.md"
    )

    log("")
    log("=" * 70)
    log(
        f"📰 日报图片处理: {report_date}"
    )
    log("=" * 70)

    return generate_report_images(
        report_path=report_path,
        report_type="日报",
        report_date=report_date,
        force_regenerate=False,
    )


# ======================================================================
# 周报
# ======================================================================

def process_weekly_report(
    week: str,
) -> bool:

    report_path = (
        WEEKLY_DIR
        / f"{week}.md"
    )

    log("")
    log("=" * 70)
    log(
        f"📊 周报图片处理: {week}"
    )
    log("=" * 70)

    return generate_report_images(
        report_path=report_path,
        report_type="周报",
        report_date=week,
        force_regenerate=True,
    )


# ======================================================================
# Main
# ======================================================================

def main() -> int:

    log("")
    log("=" * 70)
    log("748686 自生长知识系统")
    log("Knowledge Image Engine V5.4")
    log("=" * 70)

    if not AGNES_API_KEY:

        log(
            "⚠️ 未检测到 AGNES_API_KEY "
            "或 AI_API_KEY"
        )

    # --------------------------------------------------------------
    # 日报
    # --------------------------------------------------------------

    report_dates = get_report_dates()

    daily_success = True

    for index, report_date in enumerate(
        report_dates
    ):

        success = process_daily_report(
            report_date
        )

        # TODAY 必须成功
        if index == 0 and not success:

            daily_success = False

            log(
                "❌ TODAY 日报图片处理失败"
            )

        # 历史日期允许不存在
        elif (
            index > 0
            and not (
                REPORT_DIR
                / f"{report_date}.md"
            ).exists()
        ):

            log(
                f"⏭️ 历史日报不存在，跳过: "
                f"{report_date}"
            )

    # --------------------------------------------------------------
    # 周报
    # --------------------------------------------------------------

    current_week = get_current_week()

    weekly_report = (
        WEEKLY_DIR
        / f"{current_week}.md"
    )

    if weekly_report.exists():

        weekly_success = process_weekly_report(
            current_week
        )

        if not weekly_success:

            log(
                "⚠️ 周报图片处理失败"
            )

    else:

        log(
            f"⏭️ 当前周报不存在，SKIP: "
            f"{weekly_report}"
        )

    # --------------------------------------------------------------
    # 结果
    # --------------------------------------------------------------

    log("")
    log("=" * 70)

    if daily_success:

        log(
            "✅ Knowledge Image Engine 完成"
        )

        return 0

    log(
        "❌ TODAY 日报图片处理失败"
    )

    return 1


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":
    sys.exit(main())
