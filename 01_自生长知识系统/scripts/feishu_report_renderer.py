#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Feishu Report Renderer V1.1

======================================================================
职责
======================================================================

将：

    日报 *_带图.md
    周报 *_带图.md

转换为：

    飞书 Interactive Card

支持：

    1. Markdown 图片
       -> 本地 PNG
       -> 上传飞书
       -> image_key
       -> 飞书原生图片

    2. Markdown 表格
       -> 数据表格

    3. 关键数字
       -> KPI 卡片

    4. 分类数值
       -> 柱状图

    5. 构成比例
       -> 饼图

    6. 时间序列
       -> 折线图

    7. 标题

    8. 普通 Markdown

    9. 长报告自动拆分多个 Card

======================================================================
重要原则
======================================================================

本程序：

    不修改原始 Markdown
    不修改日报
    不修改周报
    不修改图片

只负责：

    Markdown
        ↓
    Renderer
        ↓
    Feishu Card
        ↓
    Webhook

======================================================================
V1.1 修复
======================================================================

修复：

    ErrCode: 11310
    ErrMsg: margin invalid

原因：

    Card 2.0 markdown element 不接受之前使用的
    margin 字段。

因此 V1.1：

    所有 markdown element
    删除 margin 字段。

同时尽量减少非必要 Card Schema 字段，
优先保证飞书实际发送稳定性。
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

import requests


# ======================================================================
# Feishu
# ======================================================================

FEISHU_HOST = "https://open.feishu.cn"

TOKEN_URL = (
    f"{FEISHU_HOST}"
    "/open-apis/auth/v3/tenant_access_token/internal"
)

UPLOAD_URL = (
    f"{FEISHU_HOST}"
    "/open-apis/im/v1/images"
)

REQUEST_TIMEOUT = 30


# ======================================================================
# Renderer
# ======================================================================

MAX_CARD_ELEMENTS = 16

MAX_TABLE_ROWS = 30

MAX_CHART_ROWS = 12


# ======================================================================
# 通用工具
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


def clean_text(value: Any) -> str:

    if value is None:
        return ""

    text = str(value)

    text = text.replace("\r", "")
    text = text.replace("\n", " ")

    return text.strip()


def strip_markdown(value: str) -> str:

    value = clean_text(value)

    value = re.sub(
        r"\*\*(.*?)\*\*",
        r"\1",
        value,
    )

    value = re.sub(
        r"__(.*?)__",
        r"\1",
        value,
    )

    value = re.sub(
        r"`(.*?)`",
        r"\1",
        value,
    )

    value = re.sub(
        r"~~(.*?)~~",
        r"\1",
        value,
    )

    return value.strip()


def safe_filename(value: str) -> str:

    value = re.sub(
        r"[^\w\u4e00-\u9fff.-]+",
        "_",
        value,
    )

    return value[:100]


# ======================================================================
# 数字
# ======================================================================

def numeric_value(
    value: str,
) -> float | None:

    value = clean_text(value)

    if not value:
        return None

    multiplier = 1.0

    if "亿" in value:
        multiplier = 100000000

    elif "万" in value:
        multiplier = 10000

    value = (
        value
        .replace(",", "")
        .replace("，", "")
        .replace("%", "")
        .replace("％", "")
        .replace("¥", "")
        .replace("$", "")
        .replace("€", "")
        .replace("£", "")
        .replace("万", "")
        .replace("亿", "")
    )

    try:

        return float(value) * multiplier

    except Exception:

        return None


def is_number(
    value: str,
) -> bool:

    return (
        numeric_value(value)
        is not None
    )


def is_percentage(
    value: str,
) -> bool:

    value = clean_text(value)

    return (
        "%" in value
        or "％" in value
    )


def percentage_value(
    value: str,
) -> float | None:

    if not is_percentage(value):
        return None

    return numeric_value(value)


def looks_like_date(
    value: str,
) -> bool:

    value = clean_text(value)

    patterns = [
        r"\d{4}[-/]\d{1,2}[-/]\d{1,2}",
        r"\d{1,2}[-/]\d{1,2}",
        r"\d{4}年\d{1,2}月",
        r"\d{1,2}月\d{1,2}日",
        r"\d{4}",
    ]

    return any(
        re.search(
            pattern,
            value,
        )
        for pattern in patterns
    )


# ======================================================================
# Feishu Client
# ======================================================================

class FeishuClient:

    def __init__(
        self,
        app_id: str,
        app_secret: str,
        webhook: str,
    ):

        self.app_id = app_id
        self.app_secret = app_secret
        self.webhook = webhook

        self.token: str | None = None

    # ------------------------------------------------------------------
    # Token
    # ------------------------------------------------------------------

    def get_token(self) -> str:

        response = requests.post(
            TOKEN_URL,
            json={
                "app_id": self.app_id,
                "app_secret": self.app_secret,
            },
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            raise RuntimeError(
                "获取 tenant_access_token 失败："
                f"{data}"
            )

        token = (
            data.get(
                "tenant_access_token"
            )
        )

        if not token:

            raise RuntimeError(
                "tenant_access_token 缺失："
                f"{data}"
            )

        self.token = token

        return token

    # ------------------------------------------------------------------
    # Upload image
    # ------------------------------------------------------------------

    def upload_image(
        self,
        image_path: Path,
    ) -> str:

        if not self.token:

            self.get_token()

        if not image_path.exists():

            raise FileNotFoundError(
                f"图片不存在：{image_path}"
            )

        with image_path.open(
            "rb"
        ) as file:

            response = requests.post(
                UPLOAD_URL,
                headers={
                    "Authorization":
                        f"Bearer {self.token}",
                },
                files={
                    "image": (
                        image_path.name,
                        file,
                        "image/png",
                    )
                },
                data={
                    "image_type": "message",
                },
                timeout=REQUEST_TIMEOUT,
            )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            raise RuntimeError(
                "飞书图片上传失败："
                f"{data}"
            )

        image_key = (
            data
            .get("data", {})
            .get("image_key")
        )

        if not image_key:

            raise RuntimeError(
                "飞书没有返回 image_key："
                f"{data}"
            )

        log(
            "      ✓ 图片上传成功："
            f"{image_path.name}"
            f" -> {image_key}"
        )

        return image_key

    # ------------------------------------------------------------------
    # Send Card
    # ------------------------------------------------------------------

    def send_card(
        self,
        card: dict,
        label: str,
    ) -> None:

        payload = {
            "msg_type": "interactive",
            "card": card,
        }

        response = requests.post(
            self.webhook,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        data = response.json()

        if data.get("code") != 0:

            raise RuntimeError(
                f"飞书发送失败 [{label}]："
                f"{data}"
            )

        log(
            f"      ✓ 飞书卡片发送成功：{label}"
        )


# ======================================================================
# Markdown Block
# ======================================================================

class MarkdownBlock:

    def __init__(
        self,
        block_type: str,
        content: Any = None,
    ):

        self.type = block_type

        self.content = content


# ======================================================================
# Markdown Parser
# ======================================================================

class MarkdownParser:

    IMAGE_RE = re.compile(
        r"!\[([^\]]*)\]\(([^)]+)\)"
    )

    HEADING_RE = re.compile(
        r"^(#{1,6})\s+(.*)$"
    )

    TABLE_SEPARATOR_RE = re.compile(
        r"^\s*\|?\s*:?-+:?\s*"
        r"(\|\s*:?-+:?\s*)+"
        r"\|?\s*$"
    )

    # ------------------------------------------------------------------
    # Parse
    # ------------------------------------------------------------------

    def __init__(
        self,
        markdown_path: Path,
    ):

        self.markdown_path = markdown_path

    def parse(
        self,
    ) -> list[MarkdownBlock]:

        text = (
            self.markdown_path
            .read_text(
                encoding="utf-8"
            )
        )

        lines = text.splitlines()

        blocks: list[
            MarkdownBlock
        ] = []

        paragraph: list[str] = []

        def flush_paragraph():

            if not paragraph:
                return

            content = "\n".join(
                paragraph
            ).strip()

            if content:

                blocks.append(
                    MarkdownBlock(
                        "paragraph",
                        content,
                    )
                )

            paragraph.clear()

        i = 0

        while i < len(lines):

            line = lines[i]

            # ==========================================================
            # Empty
            # ==========================================================

            if not line.strip():

                flush_paragraph()

                i += 1

                continue

            # ==========================================================
            # Heading
            # ==========================================================

            heading_match = (
                self.HEADING_RE.match(
                    line
                )
            )

            if heading_match:

                flush_paragraph()

                level = len(
                    heading_match.group(1)
                )

                title = (
                    heading_match
                    .group(2)
                    .strip()
                )

                blocks.append(
                    MarkdownBlock(
                        "heading",
                        {
                            "level": level,
                            "title": title,
                        },
                    )
                )

                i += 1

                continue

            # ==========================================================
            # Standalone image
            # ==========================================================

            image_match = (
                self.IMAGE_RE.fullmatch(
                    line.strip()
                )
            )

            if image_match:

                flush_paragraph()

                blocks.append(
                    MarkdownBlock(
                        "image",
                        {
                            "alt":
                                image_match.group(1),
                            "path":
                                image_match.group(2),
                        },
                    )
                )

                i += 1

                continue

            # ==========================================================
            # Table
            # ==========================================================

            if (
                i + 1 < len(lines)
                and "|" in line
                and self.TABLE_SEPARATOR_RE.match(
                    lines[i + 1]
                )
            ):

                flush_paragraph()

                headers = (
                    self.parse_table_row(
                        line
                    )
                )

                i += 2

                rows = []

                while i < len(lines):

                    row_line = lines[i]

                    if (
                        not row_line.strip()
                        or "|" not in row_line
                    ):
                        break

                    rows.append(
                        self.parse_table_row(
                            row_line
                        )
                    )

                    i += 1

                blocks.append(
                    MarkdownBlock(
                        "table",
                        {
                            "headers": headers,
                            "rows": rows,
                        },
                    )
                )

                continue

            # ==========================================================
            # Horizontal rule
            # ==========================================================

            if re.match(
                r"^\s*(---+|\*\*\*+|___+)\s*$",
                line,
            ):

                flush_paragraph()

                blocks.append(
                    MarkdownBlock(
                        "hr"
                    )
                )

                i += 1

                continue

            # ==========================================================
            # Paragraph
            # ==========================================================

            paragraph.append(line)

            i += 1

        flush_paragraph()

        return blocks

    # ------------------------------------------------------------------
    # Table row
    # ------------------------------------------------------------------

    @staticmethod
    def parse_table_row(
        line: str,
    ) -> list[str]:

        line = line.strip()

        if line.startswith("|"):
            line = line[1:]

        if line.endswith("|"):
            line = line[:-1]

        parts = line.split("|")

        return [
            clean_text(part)
            for part in parts
        ]


# ======================================================================
# Image Resolver
# ======================================================================

def resolve_image_path(
    markdown_path: Path,
    image_ref: str,
    repo_root: Path,
    report_type: str,
    report_date: str,
) -> Path:

    image_ref = image_ref.strip()

    # --------------------------------------------------------------
    # External URL
    # --------------------------------------------------------------

    if image_ref.startswith(
        (
            "http://",
            "https://",
        )
    ):

        raise RuntimeError(
            "报告引用了外部图片 URL，"
            "当前 Renderer 要求本地图片："
            f"{image_ref}"
        )

    # --------------------------------------------------------------
    # Remove query
    # --------------------------------------------------------------

    image_ref = image_ref.split("?")[0]

    # --------------------------------------------------------------
    # Relative to Markdown
    # --------------------------------------------------------------

    candidate_1 = (
        markdown_path.parent
        / image_ref
    ).resolve()

    if candidate_1.exists():

        return candidate_1

    # --------------------------------------------------------------
    # Actual repository image structure
    #
    # 日报：
    #
    # 04_图片/日报/YYYY-MM-DD/
    #
    # 周报：
    #
    # 04_图片/周报/YYYY-MM-DD/
    # --------------------------------------------------------------

    image_root = (
        repo_root
        / "01_自生长知识系统"
        / "04_图片"
        / report_type
        / report_date
    )

    filename = Path(
        image_ref
    ).name

    candidate_2 = (
        image_root
        / filename
    ).resolve()

    if candidate_2.exists():

        return candidate_2

    # --------------------------------------------------------------
    # Recursive fallback
    # --------------------------------------------------------------

    if image_root.exists():

        matches = list(
            image_root.rglob(
                filename
            )
        )

        if matches:

            return matches[0].resolve()

    raise RuntimeError(
        "\n"
        "Markdown 引用的图片不存在：\n"
        f"  Markdown：{markdown_path}\n"
        f"  引用：{image_ref}\n"
        f"  尝试路径：{candidate_1}\n"
        f"  尝试路径：{candidate_2}\n"
    )


# ======================================================================
# Chart Generator
# ======================================================================

class ChartGenerator:

    def __init__(self):

        import matplotlib

        matplotlib.use("Agg")

        import matplotlib.pyplot as plt

        self.plt = plt

    # ------------------------------------------------------------------
    # Create chart
    # ------------------------------------------------------------------

    def create_chart(
        self,
        table: dict,
        title: str,
        output_dir: Path,
    ) -> Path | None:

        headers = table["headers"]

        rows = table["rows"]

        if len(rows) < 2:
            return None

        if len(rows) > MAX_CHART_ROWS:
            return None

        if len(headers) < 2:
            return None

        # --------------------------------------------------------------
        # Find numeric column
        # --------------------------------------------------------------

        numeric_index = None

        for index in range(
            1,
            len(headers),
        ):

            numeric_count = 0

            for row in rows:

                if index >= len(row):
                    continue

                if is_number(
                    row[index]
                ):

                    numeric_count += 1

            if numeric_count >= max(
                2,
                len(rows) // 2,
            ):

                numeric_index = index

                break

        if numeric_index is None:
            return None

        labels = []

        values = []

        raw_values = []

        for row in rows:

            if (
                len(row) <= numeric_index
            ):
                continue

            value = numeric_value(
                row[numeric_index]
            )

            if value is None:
                continue

            labels.append(
                strip_markdown(
                    row[0]
                )
            )

            values.append(value)

            raw_values.append(
                row[numeric_index]
            )

        if len(values) < 2:
            return None

        # --------------------------------------------------------------
        # Determine chart type
        # --------------------------------------------------------------

        percentage_values = [
            percentage_value(
                value
            )
            for value in raw_values
        ]

        all_percentage = all(
            value is not None
            for value in percentage_values
        )

        percentage_sum = (
            sum(
                percentage_values
            )
            if all_percentage
            else None
        )

        is_pie = (
            all_percentage
            and percentage_sum is not None
            and 95 <= percentage_sum <= 105
            and len(values) <= 8
        )

        is_line = all(
            looks_like_date(label)
            for label in labels
        )

        if is_pie:

            chart_type = "pie"

        elif is_line:

            chart_type = "line"

        else:

            chart_type = "bar"

        # --------------------------------------------------------------
        # Output
        # --------------------------------------------------------------

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            safe_filename(title)
            or "chart"
        )

        output_path = (
            output_dir
            / f"{filename}_{chart_type}.png"
        )

        plt = self.plt

        plt.figure(
            figsize=(
                10,
                5.6,
            )
        )

        # ==============================================================
        # Pie
        # ==============================================================

        if chart_type == "pie":

            plt.pie(
                values,
                labels=labels,
                autopct="%1.1f%%",
                startangle=90,
            )

            plt.axis("equal")

        # ==============================================================
        # Line
        # ==============================================================

        elif chart_type == "line":

            x = list(
                range(
                    len(labels)
                )
            )

            plt.plot(
                x,
                values,
                marker="o",
            )

            plt.xticks(
                x,
                labels,
                rotation=30,
                ha="right",
            )

            plt.grid(
                axis="y",
                alpha=0.25,
            )

            plt.ylabel(
                headers[
                    numeric_index
                ]
            )

        # ==============================================================
        # Bar
        # ==============================================================

        else:

            y_positions = list(
                range(
                    len(labels)
                )
            )

            plt.barh(
                y_positions,
                values,
            )

            plt.yticks(
                y_positions,
                labels,
            )

            plt.xlabel(
                headers[
                    numeric_index
                ]
            )

            plt.grid(
                axis="x",
                alpha=0.25,
            )

        plt.title(
            strip_markdown(
                title
            )
        )

        plt.tight_layout()

        plt.savefig(
            output_path,
            dpi=180,
            bbox_inches="tight",
        )

        plt.close()

        log(
            "      ✓ 图表生成："
            f"{output_path.name}"
        )

        return output_path


# ======================================================================
# Feishu Report Renderer
# ======================================================================

class FeishuReportRenderer:

    def __init__(
        self,
        client: FeishuClient,
        repo_root: Path,
        report_type: str,
        report_date: str,
        markdown_path: Path,
    ):

        self.client = client

        self.repo_root = repo_root

        self.report_type = (
            report_type
        )

        self.report_date = (
            report_date
        )

        self.markdown_path = (
            markdown_path
        )

        self.parser = (
            MarkdownParser(
                markdown_path
            )
        )

        self.chart_generator = (
            ChartGenerator()
        )

        self.temp_dir = Path(
            tempfile.mkdtemp(
                prefix="feishu-report-"
            )
        )

        self.upload_cache: dict[
            str,
            str,
        ] = {}

    # ==================================================================
    # Upload cache
    # ==================================================================

    def upload_cached(
        self,
        path: Path,
    ) -> str:

        cache_key = str(
            path.resolve()
        )

        if cache_key in (
            self.upload_cache
        ):

            return (
                self.upload_cache[
                    cache_key
                ]
            )

        image_key = (
            self.client.upload_image(
                path
            )
        )

        self.upload_cache[
            cache_key
        ] = image_key

        return image_key

    # ==================================================================
    # Image element
    # ==================================================================

    def image_element(
        self,
        image_key: str,
        alt: str,
    ) -> dict:

        return {
            "tag": "img",
            "img_key": image_key,
            "alt": {
                "tag": "plain_text",
                "content": (
                    alt or ""
                ),
            },
            "mode": "fit_horizontal",
            "preview": True,
        }

    # ==================================================================
    # Heading
    #
    # 重要：
    # 不再使用 margin。
    # ==================================================================

    def heading_element(
        self,
        level: int,
        title: str,
    ) -> dict:

        title = strip_markdown(
            title
        )

        # --------------------------------------------------------------
        # H1
        # --------------------------------------------------------------

        if level == 1:

            return {
                "tag": "markdown",
                "content":
                    f"## {title}",
            }

        # --------------------------------------------------------------
        # H2
        # --------------------------------------------------------------

        if level == 2:

            return {
                "tag": "markdown",
                "content":
                    f"### {title}",
            }

        # --------------------------------------------------------------
        # H3
        # --------------------------------------------------------------

        if level == 3:

            return {
                "tag": "markdown",
                "content":
                    f"**{title}**",
            }

        # --------------------------------------------------------------
        # H4/H5/H6
        # --------------------------------------------------------------

        return {
            "tag": "markdown",
            "content":
                f"**{title}**",
        }

    # ==================================================================
    # KPI detection
    # ==================================================================

    def is_kpi_table(
        self,
        table: dict,
        previous_heading: str,
    ) -> bool:

        headers = table["headers"]

        rows = table["rows"]

        if not rows:
            return False

        if len(rows) > 6:
            return False

        heading = (
            previous_heading
            or ""
        ).lower()

        kpi_words = [
            "关键数字",
            "核心数字",
            "核心指标",
            "关键指标",
            "数字摘要",
            "指标概览",
            "metrics",
            "kpi",
            "key numbers",
        ]

        if any(
            word.lower()
            in heading
            for word in kpi_words
        ):

            return True

        # --------------------------------------------------------------
        # 2~3 列数字表
        # --------------------------------------------------------------

        if len(headers) in (
            2,
            3,
        ):

            numeric_count = 0

            for row in rows:

                if len(row) < 2:
                    continue

                if is_number(
                    row[1]
                ):

                    numeric_count += 1

            if numeric_count >= max(
                2,
                len(rows) // 2,
            ):

                return True

        return False

    # ==================================================================
    # KPI
    # ==================================================================

    def build_kpi_element(
        self,
        table: dict,
    ) -> dict:

        columns = []

        for row in table[
            "rows"
        ][
            :4
        ]:

            if len(row) < 2:
                continue

            label = strip_markdown(
                row[0]
            )

            value = strip_markdown(
                row[1]
            )

            columns.append(
                {
                    "tag": "column",
                    "width": "weighted",
                    "weight": 1,
                    "elements": [
                        {
                            "tag": "markdown",
                            "content": (
                                f"**{label}**\n\n"
                                f"## {value}"
                            ),
                        }
                    ],
                }
            )

        if not columns:

            return {
                "tag": "markdown",
                "content":
                    "暂无关键指标。",
            }

        # --------------------------------------------------------------
        # 根据数量决定布局
        # --------------------------------------------------------------

        if len(columns) == 1:

            flex_mode = "none"

        elif len(columns) == 2:

            flex_mode = "bisect"

        elif len(columns) == 3:

            flex_mode = "trisect"

        else:

            flex_mode = "flow"

        return {
            "tag": "column_set",
            "flex_mode": flex_mode,
            "columns": columns,
        }

    # ==================================================================
    # Table
    # ==================================================================

    def build_table_element(
        self,
        table: dict,
    ) -> dict:

        headers = table[
            "headers"
        ]

        rows = table[
            "rows"
        ]

        # --------------------------------------------------------------
        # 不使用过多高级字段
        # --------------------------------------------------------------

        columns = []

        column_names = []

        for index, header in enumerate(
            headers
        ):

            name = (
                f"col_{index}"
            )

            column_names.append(
                name
            )

            values = []

            for row in rows:

                if index < len(row):

                    values.append(
                        row[index]
                    )

            numeric_count = sum(
                1
                for value in values
                if is_number(value)
            )

            data_type = (
                "number"
                if (
                    values
                    and numeric_count
                    == len(
                        [
                            value
                            for value
                            in values
                            if value
                        ]
                    )
                )
                else "text"
            )

            columns.append(
                {
                    "name": name,
                    "display_name":
                        strip_markdown(
                            header
                        ),
                    "data_type":
                        data_type,
                    "width": "auto",
                }
            )

        output_rows = []

        for row in rows[
            :MAX_TABLE_ROWS
        ]:

            item = {}

            for index, name in enumerate(
                column_names
            ):

                value = (
                    row[index]
                    if index < len(row)
                    else ""
                )

                column_type = (
                    columns[index]
                    ["data_type"]
                )

                if (
                    column_type
                    == "number"
                ):

                    number = numeric_value(
                        value
                    )

                    item[name] = (
                        number
                        if number is not None
                        else 0
                    )

                else:

                    item[name] = (
                        strip_markdown(
                            value
                        )
                    )

            output_rows.append(
                item
            )

        # --------------------------------------------------------------
        # Table
        # --------------------------------------------------------------

        return {
            "tag": "table",
            "page_size": min(
                10,
                max(
                    5,
                    len(output_rows),
                ),
            ),
            "columns": columns,
            "rows": output_rows,
        }

    # ==================================================================
    # Markdown Image
    # ==================================================================

    def build_image(
        self,
        image_data: dict,
    ) -> dict:

        image_path = (
            resolve_image_path(
                self.markdown_path,
                image_data["path"],
                self.repo_root,
                self.report_type,
                self.report_date,
            )
        )

        image_key = (
            self.upload_cached(
                image_path
            )
        )

        return self.image_element(
            image_key,
            image_data.get(
                "alt",
                "",
            ),
        )

    # ==================================================================
    # Render
    # ==================================================================

    def render(
        self,
    ) -> list[dict]:

        blocks = (
            self.parser.parse()
        )

        elements = []

        previous_heading = ""

        table_counter = 0

        for block in blocks:

            # ==========================================================
            # Heading
            # ==========================================================

            if block.type == "heading":

                previous_heading = (
                    block.content[
                        "title"
                    ]
                )

                elements.append(
                    self.heading_element(
                        block.content[
                            "level"
                        ],
                        block.content[
                            "title"
                        ],
                    )
                )

                continue

            # ==========================================================
            # Image
            # ==========================================================

            if block.type == "image":

                elements.append(
                    self.build_image(
                        block.content
                    )
                )

                continue

            # ==========================================================
            # Table
            # ==========================================================

            if block.type == "table":

                table_counter += 1

                table = block.content

                # ------------------------------------------------------
                # KPI
                # ------------------------------------------------------

                if self.is_kpi_table(
                    table,
                    previous_heading,
                ):

                    elements.append(
                        self.build_kpi_element(
                            table
                        )
                    )

                # ------------------------------------------------------
                # Table
                # ------------------------------------------------------

                elements.append(
                    self.build_table_element(
                        table
                    )
                )

                # ------------------------------------------------------
                # Chart
                # ------------------------------------------------------

                try:

                    chart_path = (
                        self
                        .chart_generator
                        .create_chart(
                            table,
                            previous_heading
                            or (
                                f"数据图表 "
                                f"{table_counter}"
                            ),
                            self.temp_dir,
                        )
                    )

                    if chart_path:

                        chart_key = (
                            self
                            .upload_cached(
                                chart_path
                            )
                        )

                        elements.append(
                            self.image_element(
                                chart_key,
                                (
                                    f"{previous_heading}"
                                    " 数据图表"
                                ),
                            )
                        )

                except Exception as exc:

                    log(
                        "      ⚠ 图表生成跳过："
                        f"{exc}"
                    )

                continue

            # ==========================================================
            # HR
            # ==========================================================

            if block.type == "hr":

                elements.append(
                    {
                        "tag": "hr"
                    }
                )

                continue

            # ==========================================================
            # Paragraph
            # ==========================================================

            if block.type == "paragraph":

                content = (
                    block.content
                    .strip()
                )

                if not content:
                    continue

                cursor = 0

                found_image = False

                for match in (
                    MarkdownParser
                    .IMAGE_RE
                    .finditer(
                        content
                    )
                ):

                    found_image = True

                    before = (
                        content[
                            cursor:
                            match.start()
                        ].strip()
                    )

                    if before:

                        elements.append(
                            {
                                "tag":
                                    "markdown",
                                "content":
                                    before,
                            }
                        )

                    image_data = {
                        "alt":
                            match.group(1),
                        "path":
                            match.group(2),
                    }

                    elements.append(
                        self.build_image(
                            image_data
                        )
                    )

                    cursor = (
                        match.end()
                    )

                remaining = (
                    content[
                        cursor:
                    ].strip()
                )

                if remaining:

                    elements.append(
                        {
                            "tag":
                                "markdown",
                            "content":
                                remaining,
                        }
                    )

                continue

        return elements

    # ==================================================================
    # Build cards
    # ==================================================================

    def build_cards(
        self,
        elements: list[dict],
        title: str,
    ) -> list[dict]:

        cards = []

        current = []

        for element in elements:

            current.append(
                element
            )

            if (
                len(current)
                >= MAX_CARD_ELEMENTS
            ):

                cards.append(
                    self.make_card(
                        current,
                        title,
                        len(cards) + 1,
                    )
                )

                current = []

        if current:

            cards.append(
                self.make_card(
                    current,
                    title,
                    len(cards) + 1,
                )
            )

        return cards

    # ==================================================================
    # Make card
    # ==================================================================

    def make_card(
        self,
        elements: list[dict],
        title: str,
        index: int,
    ) -> dict:

        # --------------------------------------------------------------
        # Card header
        # --------------------------------------------------------------

        header = {
            "title": {
                "tag": "plain_text",
                "content": title,
            },
            "template": (
                "blue"
                if self.report_type
                == "日报"
                else "green"
            ),
        }

        # --------------------------------------------------------------
        # 第 2 / 3 ... 卡
        # --------------------------------------------------------------

        if index > 1:

            header[
                "subtitle"
            ] = {
                "tag":
                    "plain_text",
                "content":
                    f"第 {index} 部分",
            }

        # --------------------------------------------------------------
        # Card 2.0
        # --------------------------------------------------------------

        return {
            "schema": "2.0",

            "config": {
                "width_mode": "fill",
                "enable_forward": True,
            },

            "header": header,

            "body": {
                "direction":
                    "vertical",
                "padding":
                    "12px",
                "vertical_spacing":
                    "8px",
                "elements":
                    elements,
            },
        }

    # ==================================================================
    # Send
    # ==================================================================

    def send(
        self,
        title: str,
    ) -> None:

        elements = (
            self.render()
        )

        if not elements:

            raise RuntimeError(
                "报告渲染后没有任何内容。"
            )

        cards = (
            self.build_cards(
                elements,
                title,
            )
        )

        log("")

        log(
            "======================================================================"
        )

        log(
            f"RENDER RESULT | "
            f"{self.report_type}"
        )

        log(
            "======================================================================"
        )

        log(
            f"   Elements : "
            f"{len(elements)}"
        )

        log(
            f"   Cards    : "
            f"{len(cards)}"
        )

        # --------------------------------------------------------------
        # Send
        # --------------------------------------------------------------

        for index, card in enumerate(
            cards,
            start=1,
        ):

            self.client.send_card(
                card,
                (
                    f"{self.report_type} "
                    f"#{index}"
                ),
            )


# ======================================================================
# CLI
# ======================================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Feishu "
            "Report Renderer"
        )
    )

    parser.add_argument(
        "--markdown",
        required=True,
    )

    parser.add_argument(
        "--repo-root",
        required=True,
    )

    parser.add_argument(
        "--report-type",
        required=True,
        choices=[
            "日报",
            "周报",
        ],
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--title",
        required=True,
    )

    args = parser.parse_args()

    # ==================================================================
    # Secrets
    # ==================================================================

    app_id = os.environ.get(
        "APP_ID"
    )

    app_secret = os.environ.get(
        "APP_SECRET"
    )

    webhook = os.environ.get(
        "FEISHU_WEBHOOK"
    )

    if not app_id:

        raise RuntimeError(
            "缺少 APP_ID"
        )

    if not app_secret:

        raise RuntimeError(
            "缺少 APP_SECRET"
        )

    if not webhook:

        raise RuntimeError(
            "缺少 FEISHU_WEBHOOK"
        )

    # ==================================================================
    # Paths
    # ==================================================================

    markdown_path = (
        Path(
            args.markdown
        ).resolve()
    )

    repo_root = (
        Path(
            args.repo_root
        ).resolve()
    )

    if not markdown_path.exists():

        raise FileNotFoundError(
            "Markdown 不存在："
            f"{markdown_path}"
        )

    # ==================================================================
    # Client
    # ==================================================================

    client = FeishuClient(
        app_id=app_id,
        app_secret=app_secret,
        webhook=webhook,
    )

    # ==================================================================
    # Renderer
    # ==================================================================

    renderer = (
        FeishuReportRenderer(
            client=client,
            repo_root=repo_root,
            report_type=
                args.report_type,
            report_date=
                args.date,
            markdown_path=
                markdown_path,
        )
    )

    # ==================================================================
    # Send
    # ==================================================================

    renderer.send(
        args.title
    )


# ======================================================================
# Main
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n❌ 用户中断"
        )

        sys.exit(130)

    except Exception as exc:

        print(
            "\n❌ Feishu Report Renderer "
            "失败："
        )

        print(
            str(exc)
        )

        sys.exit(1)
