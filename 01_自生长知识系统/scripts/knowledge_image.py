#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
knowledge_image.py
======================================================================

用途
----------------------------------------------------------------------

为日报和周报自动生成高质量纯视觉配图。

日报：

    05_日报/YYYY/MM/YYYY-MM-DD.md

周报：

    06_周报/YYYY/Wxx.md

图片：

    04_图片/日报/YYYY-MM-DD/
        首图.png
        插图1.png
        插图2.png
        插图3.png

    04_图片/周报/YYYY-Wxx/
        首图.png
        插图1.png
        插图2.png
        插图3.png

带图报告：

    YYYY-MM-DD_带图.md
    Wxx_带图.md


核心规则
----------------------------------------------------------------------

一、图片数量

    最少 3 张
    最多 4 张

    首图.png
    插图1.png
    插图2.png
    插图3.png

插图3是可选的。

已有有效的三张图片时：

    不强制生成第四张。

已有第四张：

    保留。


二、图片位置

    首图：
        永远位于报告最前面。

    插图1：
        穿插在正文中。

    插图2：
        穿插在正文中。

    插图3：
        如果存在，继续穿插在正文中。

禁止：

    所有图片全部放在文章开头。


三、一图一主题

每一张图片只能表达：

    一个核心主题
    一个主要视觉主体
    一个统一场景

禁止：

    四宫格
    六宫格
    九宫格
    多窗口
    分屏
    拼贴
    照片墙
    多张小图片组合
    信息图
    PPT式排版
    多新闻事件拼在一张图中
    多个互不相关场景同时出现


四、纯视觉

图片禁止出现：

    中文汉字
    中文字符
    英文字母
    英文单词
    标题
    标签
    注释
    图例
    Logo
    水印
    字幕
    海报文字
    UI文字
    屏幕文字
    报纸文字
    路牌文字
    包装文字

允许自然出现：

    阿拉伯数字 0-9

但不主动添加数字。


五、内容关联

首图：

    根据整篇报告提炼一个核心主题。

插图：

    根据对应正文区域提炼一个核心主题。

每张图片都必须和报告内容有明确关系。


六、时间

所有日期逻辑使用 UTC。


七、原始报告

永远不修改：

    YYYY-MM-DD.md
    Wxx.md

只生成：

    YYYY-MM-DD_带图.md
    Wxx_带图.md


八、API

AGNES Image API：

    https://api.agnes-ai.cn/v1/images/generations

Model：

    agnes-image-2.5-flash

Size：

    2K

Ratio：

    16:9

response_format：

    extra_body.response_format = url


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
# 1. 路径
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
# 3. 图片
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
# 6. PNG 验证
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
# 7. 原子写入
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
# 8. 日报查找
# ======================================================================

def find_daily_report(
    report_date,
) -> Path | None:

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
# 9. 周报查找
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
# 11. 读取报告
# ======================================================================

def read_report(
    path: Path,
) -> str:

    return path.read_text(
        encoding="utf-8"
    )


# ======================================================================
# 12. 标题
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
# 13. 清理报告内容
# ======================================================================

def clean_report_content(
    content: str,
) -> str:
    """
    提取纯正文内容。

    目的：

        帮助模型理解文章。

    注意：

        这些文字只是给模型理解。
        不允许模型把这些文字画进图片。
    """

    lines = []

    for line in content.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        # 删除已有图片引用
        if stripped.startswith("![]("):
            continue

        # 删除 HTML 注释
        if stripped.startswith("<!--"):
            continue

        cleaned = stripped

        # Markdown 标题标记
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

        # Markdown 粗体
        cleaned = cleaned.replace(
            "**",
            "",
        )

        # Markdown 斜体
        cleaned = cleaned.replace(
            "__",
            "",
        )

        lines.append(cleaned)

    return "\n".join(lines)[:16000]


# ======================================================================
# 14. 正文块
# ======================================================================

def split_markdown_blocks(
    content: str,
) -> list[str]:
    """
    按 Markdown 段落拆分。

    保持原文，不修改原文。
    """

    lines = content.splitlines()

    blocks = []

    current = []

    for line in lines:

        if not line.strip():

            if current:

                blocks.append(
                    "\n".join(current)
                )

                current = []

        else:

            current.append(line)

    if current:

        blocks.append(
            "\n".join(current)
        )

    return [
        block
        for block in blocks
        if block.strip()
    ]


# ======================================================================
# 15. 根据正文位置提取主题上下文
# ======================================================================

def get_visual_context_for_position(
    blocks: list[str],
    position: int,
    total_images: int,
) -> str:
    """
    根据插图所在正文位置，
    选取附近内容作为图片主题依据。

    不把整个报告所有主题同时塞给模型。

    这样可以减少：

        多主题
        多场景
        多窗口
        拼贴

    的概率。
    """

    if not blocks:
        return ""

    total_blocks = len(blocks)

    # --------------------------------------------------------------
    # position 从 1 开始
    # --------------------------------------------------------------

    center = max(
        0,
        min(
            position - 1,
            total_blocks - 1,
        ),
    )

    # --------------------------------------------------------------
    # 以当前位置为中心，只取附近少量正文
    # --------------------------------------------------------------

    start = max(
        0,
        center - 1,
    )

    end = min(
        total_blocks,
        center + 2,
    )

    selected = blocks[
        start:end
    ]

    context = "\n\n".join(
        selected
    )

    return context[:7000]


# ======================================================================
# 16. 图片 Prompt
# ======================================================================

def build_image_prompt(
    report_type: str,
    report_title: str,
    visual_context: str,
    image_name: str,
) -> str:
    """
    一图一主题 Prompt。
    """

    if image_name == "首图.png":

        role = """
这是整篇报告的首图。

请从报告中提炼一个最核心的主题。

只选择一个主题。

只建立一个统一场景。

只设置一个主要视觉主体。

不要尝试把整篇报告的所有内容都塞进图片。
"""

    else:

        role = f"""
这是报告正文中的 {image_name}。

请根据它所在正文区域的内容，
选择其中最重要的一个视觉主题。

只选择一个主题。

只表现一个主要事件、对象、人物或场景。

不要把正文附近的多个主题同时塞进一张图片。
"""

    prompt = f"""
You are a world-class documentary photographer
and cinematic editorial visual artist.

Create ONE coherent 16:9 landscape image in 2K resolution.

Report type:
{report_type}

Report title:
{report_title}

Image role:
{role}

================================================================
ABSOLUTE COMPOSITION RULE
================================================================

ONE IMAGE = ONE CORE SUBJECT.

The image must communicate ONE core visual idea only.

Use:

    one main subject
    one unified scene
    one coherent composition

Do NOT create:

    collage
    grid
    multi-panel image
    four-panel layout
    six-panel layout
    nine-panel layout
    split screen
    multiple windows
    photo wall
    thumbnail collection
    montage
    multiple mini-scenes
    infographic
    presentation slide
    dashboard
    magazine collage

Do NOT place several unrelated events into the same image.

Do NOT show:

    one country on one side
    another country on another side
    a factory in another box
    a stock market in another box
    a map in another box

Instead, choose the single most important idea
and express it through ONE unified visual scene.

================================================================
NO TEXT
================================================================

The image must contain NO readable text.

Absolutely forbid:

    Chinese characters
    Chinese writing
    Chinese words
    English letters
    English words
    titles
    captions
    labels
    subtitles
    annotations
    logos
    watermarks
    UI text
    screen text
    newspaper text
    book text
    packaging text
    road-sign text
    advertising text

Do NOT generate Chinese.

Do NOT generate English.

Do NOT add a title.

Do NOT add explanatory text.

Do NOT turn the image into an infographic.

If a natural scene contains a screen,
newspaper, sign, document, billboard,
package or phone:

    make the writing absent,
    blurred,
    abstract,
    or unreadable.

Arabic numerals 0-9 may appear naturally,
but do not add numbers unless visually necessary.

================================================================
VISUAL STORYTELLING
================================================================

Express the topic ONLY through visual elements:

    people
    objects
    buildings
    landscapes
    industrial environments
    technology
    transportation
    economic environments
    financial environments
    political environments
    social environments
    natural environments
    documentary scenes
    cinematic lighting
    visual symbolism
    composition
    depth
    atmosphere

The image should feel like:

    premium documentary photography
    serious editorial photography
    cinematic realism
    high-end journalism
    sophisticated knowledge-report imagery

Avoid:

    cartoon
    childish illustration
    cheap commercial art
    excessive cyberpunk
    fantasy overload
    decorative abstract art
    PPT style
    infographic style
    poster style
    collage style

================================================================
REPORT CONTEXT
================================================================

The following text is ONLY context for understanding the topic.

Do not reproduce any of this text inside the image.

Do not visualize the text as written words.

Extract ONE core visual subject from it.

{visual_context}

================================================================
FINAL INSTRUCTION
================================================================

Generate one single coherent visual scene.

One main subject.

One core theme.

One unified composition.

No collage.

No grid.

No split screen.

No multiple mini-scenes.

No Chinese text.

No English text.

No readable words.

16:9 landscape.

2K quality.
"""

    return prompt.strip()


# ======================================================================
# 17. 下载图片
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
            f"图片下载 HTTP {exc.code}"
        ) from exc

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"图片下载网络错误：{exc}"
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
# 18. AGNES
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
            "AGNES_API_KEY 未设置"
        )

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

    try:

        result = json.loads(
            raw_response.decode(
                "utf-8"
            )
        )

    except Exception as exc:

        raise RuntimeError(
            "AGNES Image API 返回不是合法 JSON"
        ) from exc

    data = result.get(
        "data"
    )

    if not isinstance(
        data,
        list,
    ) or not data:

        raise RuntimeError(
            f"AGNES Image API 缺少 data："
            f"{result}"
        )

    first = data[0]

    if not isinstance(
        first,
        dict,
    ):

        raise RuntimeError(
            "AGNES data[0] 格式异常"
        )

    image_url = first.get(
        "url"
    )

    if not image_url:

        raise RuntimeError(
            "AGNES 没有返回图片 URL"
        )

    return download_image(
        image_url
    )


# ======================================================================
# 19. 已有图片
# ======================================================================

def get_existing_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = (
            image_dir / image_name
        )

        if is_valid_png(path):

            result.append(
                image_name
            )

    return result


# ======================================================================
# 20. 缺失图片
# ======================================================================

def determine_missing_images(
    image_dir: Path,
) -> list[str]:

    required = IMAGE_NAMES[
        :MIN_IMAGE_COUNT
    ]

    missing = []

    for image_name in required:

        path = (
            image_dir / image_name
        )

        if not is_valid_png(
            path
        ):

            missing.append(
                image_name
            )

    return missing


# ======================================================================
# 21. 正文插图位置
# ======================================================================

def get_insertion_positions(
    block_count: int,
    interior_image_count: int,
) -> list[int]:
    """
    将正文插图均匀分布。

    例如：

        文章 12 个正文块
        3 张正文插图

    大致：

        3
        6
        9

    即：

        正文
        插图1
        正文
        插图2
        正文
        插图3
        正文
    """

    if interior_image_count <= 0:
        return []

    if block_count <= 1:

        return [
            1
            for _ in range(
                interior_image_count
            )
        ]

    positions = []

    for i in range(
        1,
        interior_image_count + 1,
    ):

        position = round(
            block_count
            * i
            / (
                interior_image_count
                + 1
            )
        )

        position = max(
            1,
            min(
                position,
                block_count,
            ),
        )

        positions.append(
            position
        )

    # 防止重复
    fixed = []

    for position in positions:

        if not fixed:

            fixed.append(position)
            continue

        if position <= fixed[-1]:

            position = (
                fixed[-1] + 1
            )

        position = min(
            position,
            block_count,
        )

        fixed.append(
            position
        )

    return fixed


# ======================================================================
# 22. 生成缺失图片
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

    clean_content = clean_report_content(
        content
    )

    blocks = split_markdown_blocks(
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
            "首图、插图1、插图2 已存在。"
        )

        if is_valid_png(
            image_dir / "插图3.png"
        ):

            log(
                "已有插图3.png，保留。"
            )

        return

    # --------------------------------------------------------------
    # 图片总数
    # --------------------------------------------------------------

    current_count = len(existing)

    final_target_count = max(
        MIN_IMAGE_COUNT,
        current_count,
    )

    final_target_count = min(
        final_target_count,
        MAX_IMAGE_COUNT,
    )

    log(
        f"目标图片数量："
        f"{final_target_count}"
    )

    # --------------------------------------------------------------
    # 计算正文插图位置
    # --------------------------------------------------------------

    interior_count = (
        final_target_count - 1
    )

    positions = get_insertion_positions(
        len(blocks),
        interior_count,
    )

    # --------------------------------------------------------------
    # 逐张生成
    # --------------------------------------------------------------

    for image_name in missing:

        if image_name == "首图.png":

            visual_context = clean_content

        else:

            try:

                number = int(
                    image_name
                    .replace(
                        "插图",
                        ""
                    )
                    .replace(
                        ".png",
                        ""
                    )
                )

            except ValueError:

                number = 1

            interior_index = (
                number - 1
            )

            if (
                interior_index
                < len(positions)
            ):

                position = (
                    positions[
                        interior_index
                    ]
                )

            else:

                position = max(
                    1,
                    len(blocks) // 2,
                )

            visual_context = (
                get_visual_context_for_position(
                    blocks,
                    position,
                    final_target_count,
                )
            )

            if not visual_context:

                visual_context = (
                    clean_content
                )

        log(
            f"开始生成："
            f"{image_name}"
        )

        prompt = build_image_prompt(
            report_type=report_type,
            report_title=title,
            visual_context=visual_context,
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
                f"图片验证失败："
                f"{target_path}"
            )

        log(
            f"图片已落盘："
            f"{target_path}"
        )


# ======================================================================
# 23. 最终图片
# ======================================================================

def get_final_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = (
            image_dir / image_name
        )

        if is_valid_png(path):

            result.append(
                image_name
            )

    return result


# ======================================================================
# 24. 相对路径
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
# 25. 生成带图 Markdown
# ======================================================================

def build_image_markdown(
    original_content: str,
    report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> str:

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "图片数量不足"
        )

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            "图片数量超过上限"
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

    blocks = split_markdown_blocks(
        original_content.strip()
    )

    # --------------------------------------------------------------
    # 正文插图
    # --------------------------------------------------------------

    interior_images = [
        name
        for name in image_names
        if name != "首图.png"
    ]

    interior_images = (
        interior_images[:3]
    )

    positions = get_insertion_positions(
        len(blocks),
        len(interior_images),
    )

    # --------------------------------------------------------------
    # 建立位置映射
    # --------------------------------------------------------------

    position_to_image = {}

    for index, position in enumerate(
        positions
    ):

        if index >= len(
            interior_images
        ):
            break

        position_to_image[
            position
        ] = interior_images[index]

    # --------------------------------------------------------------
    # 组装正文
    # --------------------------------------------------------------

    output = []

    for index, block in enumerate(
        blocks,
        start=1,
    ):

        output.append(
            block
        )

        if index in position_to_image:

            image_name = (
                position_to_image[
                    index
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

            output.append(
                f"![]({relative_path})"
            )

    # --------------------------------------------------------------
    # 防止正文过少导致图片没有插入
    # --------------------------------------------------------------

    already_inserted = set(
        position_to_image.values()
    )

    for image_name in interior_images:

        if image_name in already_inserted:
            continue

        image_path = (
            image_dir / image_name
        )

        relative_path = (
            make_relative_image_path(
                report_path,
                image_path,
            )
        )

        output.append(
            f"![]({relative_path})"
        )

    body = "\n\n".join(
        output
    )

    return (
        cover_markdown
        + "\n\n"
        + body
        + "\n"
    )


# ======================================================================
# 26. 带图文件名
# ======================================================================

def build_image_report_path(
    report_path: Path,
) -> Path:

    return report_path.with_name(
        f"{report_path.stem}_带图"
        f"{report_path.suffix}"
    )


# ======================================================================
# 27. 验证
# ======================================================================

def validate_image_report(
    report_type: str,
    image_report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> None:

    if not image_report_path.is_file():

        raise RuntimeError(
            f"带图报告不存在："
            f"{image_report_path}"
        )

    content = (
        image_report_path.read_text(
            encoding="utf-8"
        )
    )

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "最终图片数量不足"
        )

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            "最终图片数量超过上限"
        )

    # --------------------------------------------------------------
    # 图片必须存在
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

        marker = (
            f"![]({relative_path})"
        )

        if marker not in content:

            raise RuntimeError(
                f"Markdown 缺少图片："
                f"{image_name}"
            )

    # --------------------------------------------------------------
    # 首图必须是第一个内容
    # --------------------------------------------------------------

    cover_path = (
        image_dir / "首图.png"
    )

    cover_relative = (
        make_relative_image_path(
            image_report_path,
            cover_path,
        )
    )

    cover_marker = (
        f"![]({cover_relative})"
    )

    if not content.startswith(
        cover_marker
    ):

        raise RuntimeError(
            "首图没有位于报告最前面"
        )

    # --------------------------------------------------------------
    # 图片顺序
    # --------------------------------------------------------------

    previous_position = -1

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

        if position <= previous_position:

            raise RuntimeError(
                f"图片顺序错误："
                f"{image_name}"
            )

        previous_position = position

    log(
        f"{report_type}验证成功："
        f"{image_report_path}"
    )


# ======================================================================
# 28. 创建带图报告
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
            f"{report_type}图片不足"
        )

    image_report_path = (
        build_image_report_path(
            report_path
        )
    )

    final_content = (
        build_image_markdown(
            original_content=
                original_content,

            report_path=
                image_report_path,

            image_dir=
                image_dir,

            image_names=
                image_names,
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
        report_type=
            report_type,

        image_report_path=
            image_report_path,

        image_dir=
            image_dir,

        image_names=
            image_names,
    )

    return image_report_path


# ======================================================================
# 29. 日报
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
        f"原始报告："
        f"{report_path}"
    )

    log(
        f"图片目录："
        f"{image_dir}"
    )

    generate_missing_images(
        report_type="日报",
        report_path=report_path,
        image_dir=image_dir,
    )

    final_images = (
        get_final_images(
            image_dir
        )
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "日报图片不足"
        )

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
# 30. 周报
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
        f"处理周报："
        f"{week_key}"
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
        f"原始报告："
        f"{report_path}"
    )

    log(
        f"图片目录："
        f"{image_dir}"
    )

    generate_missing_images(
        report_type="周报",
        report_path=report_path,
        image_dir=image_dir,
    )

    final_images = (
        get_final_images(
            image_dir
        )
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "周报图片不足"
        )

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
# 31. 主程序
# ======================================================================

def main() -> int:

    log("=" * 72)
    log(
        "748686 自生长知识系统"
    )
    log(
        "knowledge_image.py"
    )
    log(
        "一图一主题 + 正文穿插 + 纯视觉无文字"
    )
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
    # UTC 日期
    # --------------------------------------------------------------

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
    log(
        "DAILY REPORT IMAGE GENERATION"
    )
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
    log(
        "WEEKLY REPORT IMAGE GENERATION"
    )
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
    log(
        "IMAGE GENERATION SUMMARY"
    )
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
