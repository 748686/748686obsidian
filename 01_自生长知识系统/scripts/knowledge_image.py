#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
knowledge_image.py
======================================================================

功能
----------------------------------------------------------------------

负责为：

    05_日报
    06_周报

自动生成图片，并创建：

    *_带图.md

图片统一保存到：

    04_图片/日报/YYYY-MM-DD/
    04_图片/周报/YYYY-Wxx/

图片：

    首图.png
    插图1.png
    插图2.png
    插图3.png

核心规则
----------------------------------------------------------------------

1. 每篇报告至少 3 张图片
2. 最多 4 张图片
3. 首图永远位于报告最前面
4. 插图1、插图2、插图3 穿插在正文中
5. 不把所有图片堆在文章开头
6. 原始 Markdown 永远不修改
7. 生成独立的 *_带图.md
8. 已有有效图片不重复生成
9. 缺什么补什么
10. 每篇报告完成后立即落盘并验证
11. 日报处理：
        前天
        昨天
        今天
12. 周报按照 ISO Week 查找
13. 所有日期使用 UTC
14. 图片生成使用 AGNES Image API

图片视觉规则
----------------------------------------------------------------------

图片必须是：

    纯视觉图片

禁止：

    中文汉字
    英文字母
    英文单词
    中文标题
    英文标题
    标签
    注释
    图例文字
    水印
    Logo
    品牌文字
    UI文字
    海报文字
    信息图文字

允许：

    阿拉伯数字 0-9

但阿拉伯数字也只有在视觉上自然需要时才允许出现。

最终目标：

    不依赖图片中的文字表达信息。

图片必须通过：

    人物
    场景
    物体
    环境
    光线
    构图
    象征性视觉元素
    新闻现场感
    数据视觉形态

来表达文章内容。

======================================================================
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ======================================================================
# 1. 基础路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent

SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"

DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# 2. AGNES
# ======================================================================

AGNES_API_URL = (
    "https://api.agnes-ai.cn/v1/images/generations"
)

AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

REQUEST_TIMEOUT = 180


# ======================================================================
# 3. 图片配置
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
# 4. 日志
# ======================================================================

def log(message: str) -> None:
    print(
        f"[knowledge_image] {message}",
        flush=True,
    )


def log_error(message: str) -> None:
    print(
        f"[knowledge_image][ERROR] {message}",
        file=sys.stderr,
        flush=True,
    )


# ======================================================================
# 5. UTC
# ======================================================================

def utc_today():
    return datetime.now(
        timezone.utc
    ).date()


# ======================================================================
# 6. PNG 检查
# ======================================================================

def is_valid_png(path: Path) -> bool:

    try:

        if not path.is_file():
            return False

        if path.stat().st_size < 8:
            return False

        with path.open("rb") as f:
            signature = f.read(8)

        return signature == (
            b"\x89PNG\r\n\x1a\n"
        )

    except Exception:
        return False


# ======================================================================
# 7. 原子写文件
# ======================================================================

def atomic_write_bytes(
    path: Path,
    data: bytes,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:

        with os.fdopen(
            fd,
            "wb",
        ) as f:

            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(
            temp_name,
            path,
        )

    except Exception:

        try:
            os.unlink(temp_name)
        except OSError:
            pass

        raise


def atomic_write_text(
    path: Path,
    text: str,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:

        with os.fdopen(
            fd,
            "w",
            encoding="utf-8",
            newline="",
        ) as f:

            f.write(text)
            f.flush()
            os.fsync(f.fileno())

        os.replace(
            temp_name,
            path,
        )

    except Exception:

        try:
            os.unlink(temp_name)
        except OSError:
            pass

        raise


# ======================================================================
# 8. 日报路径
# ======================================================================

def find_daily_report(report_date) -> Path | None:

    path = (
        DAILY_ROOT
        / f"{report_date.year:04d}"
        / f"{report_date.month:02d}"
        / f"{report_date.isoformat()}.md"
    )

    if path.is_file():
        return path

    return None


# ======================================================================
# 9. 周报路径
# ======================================================================

def find_weekly_report(
    iso_year: int,
    iso_week: int,
) -> Path | None:

    path = (
        WEEKLY_ROOT
        / f"{iso_year:04d}"
        / f"W{iso_week:02d}.md"
    )

    if path.is_file():
        return path

    return None


# ======================================================================
# 10. 图片目录
# ======================================================================

def get_daily_image_dir(
    report_date,
) -> Path:

    return (
        DAILY_IMAGE_ROOT
        / report_date.isoformat()
    )


def get_weekly_image_dir(
    iso_year: int,
    iso_week: int,
) -> Path:

    return (
        WEEKLY_IMAGE_ROOT
        / f"{iso_year:04d}-W{iso_week:02d}"
    )


# ======================================================================
# 11. 读取 Markdown
# ======================================================================

def read_report(
    path: Path,
) -> str:

    return path.read_text(
        encoding="utf-8"
    )


# ======================================================================
# 12. 提取标题
# ======================================================================

def extract_report_title(
    content: str,
    fallback: str,
) -> str:

    for line in content.splitlines():

        stripped = line.strip()

        if stripped.startswith("# "):

            title = stripped[2:].strip()

            if title:
                return title

    return fallback


# ======================================================================
# 13. 清理文本，提供给图片模型
# ======================================================================

def prepare_visual_context(
    content: str,
) -> str:
    """
    给图片模型提供文章内容。

    注意：

    这里不是为了让模型把文字画进图片。

    只是让模型理解：

        文章讲什么
        有哪些人物
        有哪些事件
        有哪些场景
        有哪些对象
        有什么关系

    最终图片仍然必须无文字。
    """

    lines = []

    for line in content.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        # 去掉 Markdown 图片
        if stripped.startswith("![]("):
            continue

        # 去掉 HTML 注释
        if stripped.startswith("<!--"):
            continue

        # 去掉 Markdown 标记
        cleaned = stripped

        cleaned = cleaned.replace(
            "**",
            "",
        )

        cleaned = cleaned.replace(
            "__",
            "",
        )

        cleaned = cleaned.replace(
            "### ",
            "",
        )

        cleaned = cleaned.replace(
            "## ",
            "",
        )

        cleaned = cleaned.replace(
            "# ",
            "",
        )

        lines.append(cleaned)

    text = "\n".join(lines)

    # 控制 Prompt 长度
    return text[:14000]


# ======================================================================
# 14. 图片 Prompt
# ======================================================================

def build_image_prompt(
    report_type: str,
    report_title: str,
    report_content: str,
    image_name: str,
) -> str:
    """
    生成纯视觉图片 Prompt。

    特别重要：

    明确禁止中文和英文文字。
    """

    if image_name == "首图.png":

        image_role = """
这是报告的首图。

需要具有强烈的主题概括能力。

用一张高级、专业、具有新闻摄影和电影视觉语言的
横版画面，概括整篇报告的核心主题。

画面应该一眼让人理解：

    这篇报告主要在讨论什么。

不要依靠文字表达。
"""

    else:

        image_role = f"""
这是报告正文中的第 {image_name} 配图。

它不是封面。

应该从文章内容中选择一个重要主题、事件、人物、
产业、科技、经济、社会场景或因果关系，
制作一张能够解释正文内容的纯视觉图片。

不要制作装饰性空图。

要让图片与文章内容存在明确关系。
"""

    prompt = f"""
你是一名顶级新闻摄影师、纪录片摄影师和电影视觉设计师。

请根据下面的报告内容生成一张 16:9 横版 2K 高清图片。

报告类型：
{report_type}

报告标题：
{report_title}

{image_role}

================================================================
最重要的文字限制
================================================================

这是一张纯视觉图片。

禁止在图片中出现任何文字。

禁止：

- 中文汉字
- 中文字符
- 英文字母
- 英文单词
- 英文标题
- 中文标题
- 新闻标题
- 标签
- 注释
- 图例
- 说明文字
- UI文字
- 海报文字
- Logo
- 品牌名称
- 水印
- 字幕
- 路牌文字
- 屏幕文字
- 报纸文字
- 书本文字
- 包装文字
- 任何可读文本

特别注意：

不要尝试生成中文。

不要尝试生成英文。

不要在画面中放标题。

不要在画面中放说明。

不要在画面中放信息图文字。

不要通过文字表达主题。

如果场景中自然存在屏幕、报纸、招牌、广告牌、
文件、书籍、手机等带文字物体，
请将其处理成：

    无文字
    模糊
    不可读
    纯视觉纹理

允许自然出现阿拉伯数字 0-9，
但只有在视觉上确实需要时才出现。

不要为了装饰主动添加数字。

================================================================
视觉表达要求
================================================================

只通过视觉语言表达内容：

- 人物
- 场景
- 建筑
- 城市
- 工厂
- 企业环境
- 科技设备
- 交通
- 商品
- 金融市场视觉
- 数据曲线的抽象视觉形态
- 自然环境
- 地缘政治场景
- 社会场景
- 真实事件环境
- 象征性视觉元素
- 光影
- 色彩
- 空间
- 构图
- 景深
- 摄影语言

整体风格：

专业
真实
高级
克制
新闻纪录片
电影级摄影
现代
可信
具有知识报告视觉感

避免：

卡通
儿童插画
低幼风
廉价商业广告
过度赛博朋克
过度科幻
花哨海报
文字海报
信息图
PPT风格

================================================================
报告内容
================================================================

下面的内容只用于理解文章主题。

不要把这些文字直接绘制到图片中。

{report_content}

================================================================
最终要求
================================================================

输出：

一张纯视觉的 16:9 横版 2K 图片。

核心主题必须来自报告内容。

图片本身不要包含任何中文或英文文字。
"""

    return prompt.strip()


# ======================================================================
# 15. 下载图片
# ======================================================================

def download_image(
    url: str,
) -> bytes:

    log(
        f"下载图片：{url}"
    )

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent":
                "748686-Knowledge-System"
        },
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:

            data = response.read()

    except urllib.error.HTTPError as exc:

        raise RuntimeError(
            f"图片下载 HTTP {exc.code}: {url}"
        ) from exc

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"图片下载网络错误：{exc}"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            f"图片下载失败：{exc}"
        ) from exc

    if not data:

        raise RuntimeError(
            "图片下载结果为空"
        )

    if not data.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):

        raise RuntimeError(
            "下载内容不是 PNG 文件"
        )

    return data


# ======================================================================
# 16. AGNES Image API
# ======================================================================

def generate_image(
    prompt: str,
) -> bytes:

    api_key = os.getenv(
        "AGNES_API_KEY",
        "",
    ).strip()

    if not api_key:

        raise RuntimeError(
            "环境变量 AGNES_API_KEY 未设置"
        )

    payload = {
        "model": AGNES_IMAGE_MODEL,

        "prompt": prompt,

        "size": IMAGE_SIZE,

        "ratio": IMAGE_RATIO,

        "extra_body": {
            "response_format": "url"
        },
    }

    body = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = urllib.request.Request(
        AGNES_API_URL,
        data=body,
        method="POST",
        headers={
            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json",
        },
    )

    log(
        "调用 AGNES Image API"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=REQUEST_TIMEOUT,
        ) as response:

            raw_response = response.read()

    except urllib.error.HTTPError as exc:

        error_body = exc.read().decode(
            "utf-8",
            errors="replace",
        )

        raise RuntimeError(
            f"AGNES Image API HTTP "
            f"{exc.code}: "
            f"{error_body[:2000]}"
        ) from exc

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"AGNES Image API 网络错误："
            f"{exc}"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            f"AGNES Image API 请求失败："
            f"{exc}"
        ) from exc

    try:

        result = json.loads(
            raw_response.decode(
                "utf-8"
            )
        )

    except Exception as exc:

        raise RuntimeError(
            "AGNES Image API 返回内容不是合法 JSON"
        ) from exc

    data = result.get("data")

    if not isinstance(
        data,
        list,
    ) or not data:

        raise RuntimeError(
            f"AGNES Image API 返回缺少 data："
            f"{result}"
        )

    first = data[0]

    if not isinstance(
        first,
        dict,
    ):

        raise RuntimeError(
            "AGNES Image API data[0] 格式异常"
        )

    image_url = first.get(
        "url"
    )

    if not image_url:

        raise RuntimeError(
            "AGNES Image API 没有返回图片 URL"
        )

    return download_image(
        image_url
    )


# ======================================================================
# 17. 检查已有图片
# ======================================================================

def get_existing_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):
            result.append(image_name)

    return result


# ======================================================================
# 18. 确定缺失图片
# ======================================================================

def determine_missing_images(
    image_dir: Path,
) -> list[str]:

    required = IMAGE_NAMES[
        :MIN_IMAGE_COUNT
    ]

    missing = []

    for image_name in required:

        path = image_dir / image_name

        if not is_valid_png(path):

            missing.append(image_name)

    return missing


# ======================================================================
# 19. 生成缺失图片
# ======================================================================

def generate_missing_images(
    report_type: str,
    report_path: Path,
    image_dir: Path,
) -> None:

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    content = read_report(
        report_path
    )

    title = extract_report_title(
        content,
        report_path.stem,
    )

    visual_context = prepare_visual_context(
        content
    )

    existing = get_existing_images(
        image_dir
    )

    missing = determine_missing_images(
        image_dir
    )

    log(
        f"{report_type}："
        f"{report_path.name}"
    )

    log(
        f"已有有效图片："
        f"{len(existing)} 张"
    )

    if not missing:

        log(
            "首图、插图1、插图2 均已存在。"
        )

        if is_valid_png(
            image_dir / "插图3.png"
        ):

            log(
                "发现已有插图3.png，保留。"
            )

        return

    log(
        "需要生成："
        + ", ".join(missing)
    )

    # --------------------------------------------------------------
    # 严格顺序生成
    # --------------------------------------------------------------

    for image_name in missing:

        log(
            f"开始生成：{image_name}"
        )

        prompt = build_image_prompt(
            report_type=report_type,
            report_title=title,
            report_content=visual_context,
            image_name=image_name,
        )

        image_data = generate_image(
            prompt
        )

        target_path = (
            image_dir / image_name
        )

        # ----------------------------------------------------------
        # 立即落盘
        # ----------------------------------------------------------

        atomic_write_bytes(
            target_path,
            image_data,
        )

        # ----------------------------------------------------------
        # 立即验证
        # ----------------------------------------------------------

        if not is_valid_png(
            target_path
        ):

            raise RuntimeError(
                f"图片落盘后验证失败："
                f"{target_path}"
            )

        log(
            f"图片已落盘："
            f"{target_path}"
        )


# ======================================================================
# 20. 最终图片
# ======================================================================

def get_final_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):
            result.append(image_name)

    return result


# ======================================================================
# 21. 相对路径
# ======================================================================

def make_relative_image_path(
    report_path: Path,
    image_path: Path,
) -> str:

    relative = os.path.relpath(
        image_path,
        start=report_path.parent,
    )

    return relative.replace(
        os.sep,
        "/",
    )


# ======================================================================
# 22. Markdown 正文分段
# ======================================================================

def split_markdown_for_images(
    content: str,
) -> list[str]:
    """
    将 Markdown 正文拆成适合插图的几个区段。

    目标：

        首图
        ↓
        第一段正文
        ↓
        插图1
        ↓
        第二段正文
        ↓
        插图2
        ↓
        第三段正文
        ↓
        插图3
        ↓
        剩余正文

    不修改正文文字。

    这里尽量按 Markdown 段落切分，
    而不是简单按字符硬切。
    """

    lines = content.splitlines()

    blocks = []

    current = []

    for line in lines:

        # 空行代表段落边界
        if not line.strip():

            if current:

                blocks.append(
                    "\n".join(current)
                )

                current = []

            blocks.append("")

        else:

            current.append(line)

    if current:

        blocks.append(
            "\n".join(current)
        )

    # 合并连续空块
    normalized = []

    for block in blocks:

        if block == "":

            if normalized and normalized[-1] != "":
                normalized.append("")

        else:

            normalized.append(block)

    # 去掉头尾空块
    while normalized and normalized[0] == "":
        normalized.pop(0)

    while normalized and normalized[-1] == "":
        normalized.pop()

    return normalized


# ======================================================================
# 23. 找到合理插图位置
# ======================================================================

def get_insertion_positions(
    block_count: int,
    image_count: int,
) -> list[int]:
    """
    计算插图位置。

    首图不在这里处理。

    这里只计算：

        插图1
        插图2
        插图3

    的正文位置。

    位置尽量均匀分布。
    """

    interior_count = image_count - 1

    if interior_count <= 0:
        return []

    if block_count <= 1:
        return [1] * interior_count

    positions = []

    # --------------------------------------------------------------
    # 将正文大致分成 N+1 个区段
    # --------------------------------------------------------------

    for i in range(
        1,
        interior_count + 1,
    ):

        position = round(
            block_count
            * i
            / (interior_count + 1)
        )

        position = max(
            1,
            min(
                position,
                block_count,
            ),
        )

        positions.append(position)

    # --------------------------------------------------------------
    # 防止位置重复
    # --------------------------------------------------------------

    fixed = []

    for position in positions:

        if not fixed:

            fixed.append(position)
            continue

        if position <= fixed[-1]:

            position = fixed[-1] + 1

        if position > block_count:

            position = block_count

        fixed.append(position)

    return fixed


# ======================================================================
# 24. 构建图片 Markdown
# ======================================================================

def build_image_markdown(
    report_type: str,
    original_content: str,
    report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> str:

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}有效图片不足："
            f"{len(image_names)}"
        )

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}图片超过上限："
            f"{len(image_names)}"
        )

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover_path = (
        image_dir / "首图.png"
    )

    cover_relative = (
        make_relative_image_path(
            report_path,
            cover_path,
        )
    )

    cover_markdown = (
        f"![]({cover_relative})"
    )

    # --------------------------------------------------------------
    # 正文
    # --------------------------------------------------------------

    blocks = split_markdown_for_images(
        original_content.strip()
    )

    # --------------------------------------------------------------
    # 插图数量
    # --------------------------------------------------------------

    interior_images = [
        name
        for name in image_names
        if name != "首图.png"
    ]

    # 最多 3 张正文插图
    interior_images = interior_images[:3]

    insertion_positions = (
        get_insertion_positions(
            len(blocks),
            len(interior_images) + 1,
        )
    )

    # --------------------------------------------------------------
    # 生成正文
    # --------------------------------------------------------------

    output_blocks = []

    image_index = 0

    for index, block in enumerate(
        blocks,
        start=1,
    ):

        if block:
            output_blocks.append(
                block
            )

        # ----------------------------------------------------------
        # 插入正文图片
        # ----------------------------------------------------------

        if (
            image_index
            < len(interior_images)
            and index
            in insertion_positions
        ):

            image_name = (
                interior_images[
                    image_index
                ]
            )

            image_path = (
                image_dir / image_name
            )

            relative_path = (
                make_relative_image_path(
                    report_path,
                    image_path,
                )
            )

            output_blocks.append(
                f"![]({relative_path})"
            )

            image_index += 1

    # --------------------------------------------------------------
    # 如果正文块太少，确保剩余插图仍然进入正文
    # --------------------------------------------------------------

    while (
        image_index
        < len(interior_images)
    ):

        image_name = (
            interior_images[
                image_index
            ]
        )

        image_path = (
            image_dir / image_name
        )

        relative_path = (
            make_relative_image_path(
                report_path,
                image_path,
            )
        )

        output_blocks.append(
            f"![]({relative_path})"
        )

        image_index += 1

    # --------------------------------------------------------------
    # 最终 Markdown
    # --------------------------------------------------------------

    body = "\n\n".join(
        block
        for block in output_blocks
        if block.strip()
    )

    return (
        cover_markdown
        + "\n\n"
        + body
        + "\n"
    )


# ======================================================================
# 25. 带图报告路径
# ======================================================================

def build_image_report_path(
    report_path: Path,
) -> Path:

    return report_path.with_name(
        f"{report_path.stem}_带图"
        f"{report_path.suffix}"
    )


# ======================================================================
# 26. 验证带图 Markdown
# ======================================================================

def validate_image_report(
    report_type: str,
    image_report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> None:

    if not image_report_path.is_file():

        raise RuntimeError(
            f"{report_type}带图报告不存在："
            f"{image_report_path}"
        )

    content = (
        image_report_path.read_text(
            encoding="utf-8"
        )
    )

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}最终图片数量不足："
            f"{len(image_names)}"
        )

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}最终图片数量超过上限："
            f"{len(image_names)}"
        )

    # --------------------------------------------------------------
    # 每一张图片都必须存在于 Markdown
    # --------------------------------------------------------------

    for image_name in image_names:

        image_path = (
            image_dir / image_name
        )

        if not is_valid_png(
            image_path
        ):

            raise RuntimeError(
                f"图片文件无效："
                f"{image_path}"
            )

        relative_path = (
            make_relative_image_path(
                image_report_path,
                image_path,
            )
        )

        expected = (
            f"![]({relative_path})"
        )

        if expected not in content:

            raise RuntimeError(
                f"{report_type}带图报告"
                f"缺少图片引用："
                f"{expected}"
            )

    # --------------------------------------------------------------
    # 首图必须在文件开头
    # --------------------------------------------------------------

    first_image_path = (
        image_dir / "首图.png"
    )

    first_relative = (
        make_relative_image_path(
            image_report_path,
            first_image_path,
        )
    )

    first_markdown = (
        f"![]({first_relative})"
    )

    if not content.startswith(
        first_markdown
    ):

        raise RuntimeError(
            f"{report_type}首图没有位于报告最前面"
        )

    # --------------------------------------------------------------
    # 检查图片引用顺序
    # --------------------------------------------------------------

    positions = []

    for image_name in image_names:

        image_path = (
            image_dir / image_name
        )

        relative_path = (
            make_relative_image_path(
                image_report_path,
                image_path,
            )
        )

        marker = (
            f"![]({relative_path})"
        )

        position = content.find(
            marker
        )

        positions.append(
            (
                image_name,
                position,
            )
        )

    for i in range(
        1,
        len(positions),
    ):

        previous_name, previous_pos = (
            positions[i - 1]
        )

        current_name, current_pos = (
            positions[i]
        )

        if current_pos <= previous_pos:

            raise RuntimeError(
                f"{report_type}图片顺序错误："
                f"{previous_name} → "
                f"{current_name}"
            )

    log(
        f"{report_type}带图报告验证成功："
        f"{image_report_path}"
    )


# ======================================================================
# 27. 创建带图报告
# ======================================================================

def create_image_report(
    report_type: str,
    report_path: Path,
    image_dir: Path,
) -> Path:

    original_content = read_report(
        report_path
    )

    image_names = get_final_images(
        image_dir
    )

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}有效图片不足，"
            f"无法生成带图报告："
            f"{report_path}"
        )

    image_report_path = (
        build_image_report_path(
            report_path
        )
    )

    final_content = (
        build_image_markdown(
            report_type=report_type,
            original_content=original_content,
            report_path=image_report_path,
            image_dir=image_dir,
            image_names=image_names,
        )
    )

    # --------------------------------------------------------------
    # 立即落盘
    # --------------------------------------------------------------

    atomic_write_text(
        image_report_path,
        final_content,
    )

    log(
        f"{report_type}带图报告已落盘："
        f"{image_report_path}"
    )

    # --------------------------------------------------------------
    # 立即验证
    # --------------------------------------------------------------

    validate_image_report(
        report_type=report_type,
        image_report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    return image_report_path


# ======================================================================
# 28. 处理日报
# ======================================================================

def process_daily_report(
    report_date,
) -> bool:

    log("=" * 72)

    log(
        f"处理日报："
        f"{report_date.isoformat()}"
    )

    report_path = (
        find_daily_report(
            report_date
        )
    )

    if report_path is None:

        log(
            f"日报不存在，跳过："
            f"{report_date.isoformat()}"
        )

        return False

    image_dir = (
        get_daily_image_dir(
            report_date
        )
    )

    log(
        f"原始报告：{report_path}"
    )

    log(
        f"图片目录：{image_dir}"
    )

    # --------------------------------------------------------------
    # 图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="日报",
        report_path=report_path,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 最终图片
    # --------------------------------------------------------------

    final_images = (
        get_final_images(
            image_dir
        )
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"日报最终图片不足："
            f"{report_path}"
        )

    # --------------------------------------------------------------
    # 带图报告
    # --------------------------------------------------------------

    create_image_report(
        report_type="日报",
        report_path=report_path,
        image_dir=image_dir,
    )

    log(
        f"日报处理完成："
        f"{report_date.isoformat()}"
    )

    return True


# ======================================================================
# 29. 处理周报
# ======================================================================

def process_weekly_report(
    iso_year: int,
    iso_week: int,
) -> bool:

    log("=" * 72)

    week_key = (
        f"{iso_year:04d}-W{iso_week:02d}"
    )

    log(
        f"处理周报：{week_key}"
    )

    report_path = (
        find_weekly_report(
            iso_year,
            iso_week,
        )
    )

    if report_path is None:

        log(
            f"周报不存在，跳过："
            f"{week_key}"
        )

        return False

    image_dir = (
        get_weekly_image_dir(
            iso_year,
            iso_week,
        )
    )

    log(
        f"原始报告：{report_path}"
    )

    log(
        f"图片目录：{image_dir}"
    )

    # --------------------------------------------------------------
    # 图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="周报",
        report_path=report_path,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 最终图片
    # --------------------------------------------------------------

    final_images = (
        get_final_images(
            image_dir
        )
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"周报最终图片不足："
            f"{report_path}"
        )

    # --------------------------------------------------------------
    # 带图报告
    # --------------------------------------------------------------

    create_image_report(
        report_type="周报",
        report_path=report_path,
        image_dir=image_dir,
    )

    log(
        f"周报处理完成："
        f"{week_key}"
    )

    return True


# ======================================================================
# 30. 主程序
# ======================================================================

def main() -> int:

    log("=" * 72)
    log("748686 自生长知识系统")
    log("knowledge_image.py")
    log("正文穿插图片 + 纯视觉无文字模式")
    log("=" * 72)

    # --------------------------------------------------------------
    # API Key
    # --------------------------------------------------------------

    if not os.getenv(
        "AGNES_API_KEY",
        "",
    ).strip():

        log_error(
            "AGNES_API_KEY 未设置"
        )

        return 1

    # --------------------------------------------------------------
    # UTC
    # --------------------------------------------------------------

    today = utc_today()

    day_before = (
        today - timedelta(days=2)
    )

    yesterday = (
        today - timedelta(days=1)
    )

    log(
        f"DAY_BEFORE : "
        f"{day_before.isoformat()}"
    )

    log(
        f"YESTERDAY  : "
        f"{yesterday.isoformat()}"
    )

    log(
        f"TODAY      : "
        f"{today.isoformat()}"
    )

    log(
        "Timezone   : UTC"
    )

    # ==============================================================
    # 日报
    # ==============================================================

    log("=" * 72)
    log("DAILY REPORT IMAGE GENERATION")
    log("=" * 72)

    daily_dates = [
        day_before,
        yesterday,
        today,
    ]

    daily_success = 0

    for report_date in daily_dates:

        try:

            if process_daily_report(
                report_date
            ):

                daily_success += 1

        except Exception as exc:

            log_error(
                f"日报处理失败："
                f"{report_date.isoformat()}"
            )

            log_error(
                f"{type(exc).__name__}: "
                f"{exc}"
            )

            continue

    # ==============================================================
    # 周报
    # ==============================================================

    log("=" * 72)
    log("WEEKLY REPORT IMAGE GENERATION")
    log("=" * 72)

    weekly_keys = []

    for report_date in daily_dates:

        iso_year, iso_week, _ = (
            report_date.isocalendar()
        )

        key = (
            iso_year,
            iso_week,
        )

        if key not in weekly_keys:

            weekly_keys.append(
                key
            )

    weekly_success = 0

    for iso_year, iso_week in weekly_keys:

        try:

            if process_weekly_report(
                iso_year,
                iso_week,
            ):

                weekly_success += 1

        except Exception as exc:

            log_error(
                f"周报处理失败："
                f"{iso_year}-W{iso_week:02d}"
            )

            log_error(
                f"{type(exc).__name__}: "
                f"{exc}"
            )

            continue

    # ==============================================================
    # 汇总
    # ==============================================================

    log("=" * 72)
    log("IMAGE GENERATION SUMMARY")
    log("=" * 72)

    log(
        f"日报完成："
        f"{daily_success}/"
        f"{len(daily_dates)}"
    )

    log(
        f"周报完成："
        f"{weekly_success}/"
        f"{len(weekly_keys)}"
    )

    log("=" * 72)
    log(
        "knowledge_image.py 完成"
    )
    log("=" * 72)

    return 0


# ======================================================================
# Entry Point
# ======================================================================

if __name__ == "__main__":
    sys.exit(main())
