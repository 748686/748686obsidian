#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Generator
======================================================================

用途
----------------------------------------------------------------------
为已经生成完成的：

    05_日报/
    06_周报/

自动生成配图，并创建独立的：

    *_带图.md

原始 Markdown 永远不修改。

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

报告：

    05_日报/.../2026-09-08.md
    05_日报/.../2026-09-08_带图.md

    06_周报/.../W36.md
    06_周报/.../W36_带图.md


核心原则
----------------------------------------------------------------------
1. YAML 只负责调用本程序。
2. 所有日期判断由本程序负责。
3. 所有图片生成由本程序负责。
4. 所有图片下载由本程序负责。
5. 所有图片保存由本程序负责。
6. 所有 _带图.md 生成由本程序负责。
7. 原始报告绝不覆盖。
8. 一份报告完成并落盘后，才处理下一份。
9. 缺哪张图片补哪张。
10. 图片数量最终必须为 3～4 张。
11. 图片名称固定：
       首图.png
       插图1.png
       插图2.png
       插图3.png
12. 时间统一使用 UTC。
13. AGNES 图片接口：
       https://api.agnes-ai.cn/v1/images/generations
14. 图片模型：
       agnes-image-2.5-flash
15. 图片参数：
       size = 2K
       ratio = 16:9
16. response_format 必须放在：
       extra_body.response_format
17. 不在 YAML 中实现三天逻辑。
18. 不在 YAML 中下载图片。
19. 不在 YAML 中生成带图 Markdown。

======================================================================
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ======================================================================
# 1. 基础路径
# ======================================================================

# 当前脚本：
#
# 01_自生长知识系统/scripts/knowledge_image.py
#
# ROOT：
#
# 01_自生长知识系统/

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_ROOT = SCRIPT_DIR.parent

REPORT_DIR = SYSTEM_ROOT / "05_日报"
WEEKLY_DIR = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"


# ======================================================================
# 2. AGNES 配置
# ======================================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"

AGNES_IMAGE_ENDPOINT = (
    f"{AGNES_BASE_URL}/images/generations"
)

AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

AGNES_IMAGE_SIZE = "2K"
AGNES_IMAGE_RATIO = "16:9"

AGNES_API_KEY_ENV = "AGNES_API_KEY"


# ======================================================================
# 3. 图片规则
# ======================================================================

IMAGE_NAMES = [
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
]

MIN_IMAGES = 3
MAX_IMAGES = 4


# ======================================================================
# 4. 网络配置
# ======================================================================

HTTP_TIMEOUT = 180

MAX_IMAGE_RETRIES = 5

RETRY_BASE_SECONDS = 5

RETRY_MAX_SECONDS = 60


# ======================================================================
# 5. 日志
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


def section(title: str) -> None:
    log()
    log("=" * 72)
    log(title)
    log("=" * 72)


# ======================================================================
# 6. UTC 日期
# ======================================================================

def utc_today() -> datetime:
    """
    获取当前 UTC 日期。
    """
    return datetime.now(timezone.utc)


def utc_date_string(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def get_processing_dates() -> list[str]:
    """
    返回：

        DAY_BEFORE
        YESTERDAY
        TODAY

    全部使用 UTC。
    """

    today = utc_today().date()

    day_before = today - timedelta(days=2)
    yesterday = today - timedelta(days=1)
    today_date = today

    return [
        day_before.strftime("%Y-%m-%d"),
        yesterday.strftime("%Y-%m-%d"),
        today_date.strftime("%Y-%m-%d"),
    ]


# ======================================================================
# 7. 环境检查
# ======================================================================

def get_api_key() -> str:
    api_key = os.getenv(AGNES_API_KEY_ENV, "").strip()

    if not api_key:
        raise RuntimeError(
            f"❌ 环境变量 {AGNES_API_KEY_ENV} 未配置"
        )

    return api_key


# ======================================================================
# 8. 安全文件写入
# ======================================================================

def atomic_write_text(path: Path, content: str) -> None:
    """
    原子写入 Markdown。

    先写临时文件，成功后再 replace。
    避免运行中断导致 Markdown 只写了一半。
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=".knowledge_image_",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )

    temp_path = Path(temp_name)

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())

        temp_path.replace(path)

    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


# ======================================================================
# 9. 安全图片保存
# ======================================================================

def atomic_write_bytes(path: Path, data: bytes) -> None:
    """
    原子保存图片。
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=".knowledge_image_",
        suffix=".tmp",
        dir=str(path.parent),
    )

    temp_path = Path(temp_name)

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        temp_path.replace(path)

    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


# ======================================================================
# 10. PNG 基础检查
# ======================================================================

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_valid_png(path: Path) -> bool:
    """
    判断文件是否至少是一个有效 PNG 文件。

    不依赖 Pillow。
    """

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
# 11. 图片目录
# ======================================================================

def daily_image_dir(date_string: str) -> Path:
    return IMAGE_ROOT / "日报" / date_string


def weekly_image_dir(week_key: str) -> Path:
    return IMAGE_ROOT / "周报" / week_key


# ======================================================================
# 12. 报告内容读取
# ======================================================================

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")


# ======================================================================
# 13. 查找日报
# ======================================================================

def find_daily_report(date_string: str) -> Path | None:
    """
    在 05_日报 下递归查找：

        YYYY-MM-DD.md

    排除：

        YYYY-MM-DD_带图.md
    """

    if not REPORT_DIR.exists():
        return None

    target_name = f"{date_string}.md"

    candidates = []

    for path in REPORT_DIR.rglob(target_name):
        if path.is_file():
            candidates.append(path)

    if not candidates:
        return None

    candidates.sort()

    return candidates[0]


# ======================================================================
# 14. 查找周报
# ======================================================================

WEEKLY_PATTERN = re.compile(
    r"^(?:W)?(\d{1,2})\.md$",
    re.IGNORECASE,
)


def iso_week_key(dt: datetime) -> str:
    iso_year, iso_week, _ = dt.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def get_week_keys_for_processing_dates(
    dates: list[str],
) -> list[str]:

    keys = []

    for date_string in dates:
        dt = datetime.strptime(
            date_string,
            "%Y-%m-%d",
        )

        key = iso_week_key(
            dt.replace(tzinfo=timezone.utc)
        )

        if key not in keys:
            keys.append(key)

    return keys


def find_weekly_report(week_key: str) -> Path | None:
    """
    根据 ISO week 查找周报。

    支持类似：

        06_周报/2026/W36/W36.md

    以及：

        06_周报/2026/W36.md
    """

    if not WEEKLY_DIR.exists():
        return None

    match = re.match(
        r"^(\d{4})-W(\d{2})$",
        week_key,
    )

    if not match:
        return None

    year = match.group(1)
    week = match.group(2)

    candidates = []

    possible_names = [
        f"W{week}.md",
        f"{week}.md",
    ]

    for name in possible_names:
        for path in WEEKLY_DIR.rglob(name):
            if not path.is_file():
                continue

            text = str(path)

            if year in text and f"W{week}" in text:
                candidates.append(path)

    if not candidates:
        return None

    candidates.sort()

    return candidates[0]


# ======================================================================
# 15. 图片状态检查
# ======================================================================

def existing_images(image_dir: Path) -> list[str]:
    result = []

    for name in IMAGE_NAMES:
        path = image_dir / name

        if is_valid_png(path):
            result.append(name)

    return result


def missing_required_images(image_dir: Path) -> list[str]:
    """
    最低要求：

        首图
        插图1
        插图2

    如果缺其中任何一张，就补。

    插图3属于第四张，可有可无。
    """

    required = IMAGE_NAMES[:MIN_IMAGES]

    missing = []

    for name in required:
        path = image_dir / name

        if not is_valid_png(path):
            missing.append(name)

    return missing


def report_image_status(image_dir: Path) -> None:
    existing = existing_images(image_dir)

    log(f"图片目录：{image_dir}")

    for name in IMAGE_NAMES:
        path = image_dir / name

        if is_valid_png(path):
            log(f"  ✅ {name}")
        elif path.exists():
            log(f"  ⚠️ {name} 存在但 PNG 无效")
        else:
            log(f"  ❌ {name} 不存在")

    log(
        f"当前有效图片：{len(existing)} / {MAX_IMAGES}"
    )


# ======================================================================
# 16. 报告内容摘要
# ======================================================================

def clean_report_for_prompt(text: str) -> str:
    """
    给 AI 的报告内容做轻量清理。

    不修改原始文件。
    """

    text = text.replace("\x00", "")

    # 去掉过大的连续空白
    text = re.sub(r"\n{4,}", "\n\n", text)

    # 防止 prompt 无限膨胀
    max_chars = 12000

    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[报告内容已截断]"

    return text


# ======================================================================
# 17. 图片 Prompt
# ======================================================================

def build_image_prompt(
    report_type: str,
    report_date: str,
    image_name: str,
    report_text: str,
) -> str:

    if image_name == "首图.png":
        role = """
这是整份报告的【首图 / Cover Image】。

要求：
- 概括整份报告最重要的主题
- 具有新闻知识报告封面的感觉
- 信息密度适中
- 有明确视觉中心
- 专业、现代、真实
- 不要出现文字
- 不要出现 Logo
- 不要出现水印
"""

    elif image_name == "插图1.png":
        role = """
这是整份报告的第一张【内容插图】。

要求：
- 表达报告中的第一个重要主题或核心事件
- 具有新闻信息图视觉逻辑
- 真实、专业
- 不要出现文字
- 不要出现 Logo
- 不要出现水印
"""

    elif image_name == "插图2.png":
        role = """
这是整份报告的第二张【内容插图】。

要求：
- 表达报告中的另一个重要主题、趋势或关键事件
- 与首图明显不同
- 具有新闻、知识、分析报告的视觉感觉
- 真实、专业
- 不要出现文字
- 不要出现 Logo
- 不要出现水印
"""

    else:
        role = """
这是整份报告的第三张【内容插图】。

要求：
- 表达报告中的第三个重要主题、趋势或知识点
- 与前面图片明显不同
- 具有新闻、知识、分析报告的视觉感觉
- 真实、专业
- 不要出现文字
- 不要出现 Logo
- 不要出现水印
"""

    return f"""
你是 748686 自生长知识系统的专业视觉编辑。

现在需要为一份{report_type}生成图片。

报告日期：
{report_date}

图片名称：
{image_name}

{role}

统一视觉要求：
- 横向 16:9
- 新闻杂志级视觉
- 知识系统 / 深度报道风格
- 构图清晰
- 主体明确
- 光影自然
- 具有现实感
- 不使用卡通风
- 不使用儿童插画风
- 不使用夸张游戏风
- 不要在图片中生成标题
- 不要生成任何可读文字
- 不要生成 Logo
- 不要生成水印
- 图片必须能够直接用于 Markdown 知识报告。

以下是报告内容：

---------------- REPORT START ----------------

{report_text}

---------------- REPORT END ----------------

请根据报告内容生成最具有代表性的图片。
"""


# ======================================================================
# 18. 调用 AGNES 图片 API
# ======================================================================

def request_image_url(
    prompt: str,
    api_key: str,
) -> str:

    payload = {
        "model": AGNES_IMAGE_MODEL,
        "prompt": prompt,
        "size": AGNES_IMAGE_SIZE,
        "ratio": AGNES_IMAGE_RATIO,
        "extra_body": {
            "response_format": "url"
        },
    }

    body = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        AGNES_IMAGE_ENDPOINT,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    last_error = None

    for attempt in range(1, MAX_IMAGE_RETRIES + 1):

        try:
            log(
                f"      AGNES 图片请求 "
                f"{attempt}/{MAX_IMAGE_RETRIES}"
            )

            with urlopen(
                request,
                timeout=HTTP_TIMEOUT,
            ) as response:

                raw = response.read()

            result = json.loads(
                raw.decode("utf-8")
            )

            data = result.get("data")

            if not isinstance(data, list) or not data:
                raise RuntimeError(
                    f"AGNES 返回中没有 data：{result}"
                )

            first = data[0]

            if not isinstance(first, dict):
                raise RuntimeError(
                    f"AGNES data[0] 异常：{first}"
                )

            image_url = first.get("url")

            if not image_url:
                raise RuntimeError(
                    f"AGNES 未返回图片 URL：{result}"
                )

            return str(image_url)

        except HTTPError as e:
            last_error = e

            try:
                error_body = e.read().decode(
                    "utf-8",
                    errors="replace",
                )
            except Exception:
                error_body = ""

            log(
                f"      ⚠️ HTTP Error {e.code}: "
                f"{error_body[:1000]}"
            )

        except (
            URLError,
            TimeoutError,
            json.JSONDecodeError,
            RuntimeError,
            OSError,
        ) as e:

            last_error = e

            log(
                f"      ⚠️ 图片 API 异常：{e}"
            )

        if attempt < MAX_IMAGE_RETRIES:

            wait_seconds = min(
                RETRY_BASE_SECONDS * (2 ** (attempt - 1)),
                RETRY_MAX_SECONDS,
            )

            log(
                f"      等待 {wait_seconds} 秒后重试..."
            )

            time.sleep(wait_seconds)

    raise RuntimeError(
        f"❌ AGNES 图片生成失败：{last_error}"
    )


# ======================================================================
# 19. 下载图片
# ======================================================================

def download_image(
    image_url: str,
    output_path: Path,
) -> None:

    log(
        f"      下载图片：{image_url}"
    )

    request = Request(
        image_url,
        method="GET",
        headers={
            "User-Agent": (
                "748686-Knowledge-System/1.0"
            )
        },
    )

    last_error = None

    for attempt in range(1, MAX_IMAGE_RETRIES + 1):

        try:
            with urlopen(
                request,
                timeout=HTTP_TIMEOUT,
            ) as response:

                data = response.read()

            if not data:
                raise RuntimeError(
                    "下载得到空文件"
                )

            if not data.startswith(PNG_SIGNATURE):
                raise RuntimeError(
                    "下载内容不是 PNG"
                )

            atomic_write_bytes(
                output_path,
                data,
            )

            if not is_valid_png(output_path):
                raise RuntimeError(
                    "保存后 PNG 检查失败"
                )

            return

        except (
            HTTPError,
            URLError,
            TimeoutError,
            RuntimeError,
            OSError,
        ) as e:

            last_error = e

            log(
                f"      ⚠️ 图片下载失败 "
                f"{attempt}/{MAX_IMAGE_RETRIES}: {e}"
            )

            if attempt < MAX_IMAGE_RETRIES:

                wait_seconds = min(
                    RETRY_BASE_SECONDS * (2 ** (attempt - 1)),
                    RETRY_MAX_SECONDS,
                )

                time.sleep(wait_seconds)

    raise RuntimeError(
        f"❌ 图片下载失败：{last_error}"
    )


# ======================================================================
# 20. 生成单张图片
# ======================================================================

def generate_one_image(
    report_type: str,
    report_date: str,
    image_name: str,
    report_text: str,
    image_dir: Path,
    api_key: str,
) -> None:

    output_path = image_dir / image_name

    log()
    log(
        f"    ▶ 开始生成：{image_name}"
    )

    prompt = build_image_prompt(
        report_type=report_type,
        report_date=report_date,
        image_name=image_name,
        report_text=report_text,
    )

    image_url = request_image_url(
        prompt=prompt,
        api_key=api_key,
    )

    download_image(
        image_url=image_url,
        output_path=output_path,
    )

    log(
        f"    ✅ 图片落盘：{output_path}"
    )


# ======================================================================
# 21. Markdown 图片路径
# ======================================================================

def relative_image_path(
    report_path: Path,
    image_path: Path,
) -> str:
    """
    自动计算 Markdown 相对路径。

    不硬编码 ../../../../ 等路径。
    """

    relative = os.path.relpath(
        image_path,
        start=report_path.parent,
    )

    # Markdown 统一使用 /
    return relative.replace(
        os.sep,
        "/",
    )


# ======================================================================
# 22. 生成带图 Markdown
# ======================================================================

def build_image_markdown(
    original_report_path: Path,
    image_dir: Path,
    report_type: str,
) -> str:

    original_text = read_text(
        original_report_path
    )

    lines = original_text.splitlines()

    output_lines = []

    inserted = False

    for line in lines:

        output_lines.append(line)

        # 在 YAML frontmatter 后插入首图
        if not inserted:

            # 如果没有 frontmatter，
            # 则在文件最前面插入。
            pass

    # ==============================================================
    # 更稳定的插入策略：
    #
    # 1. 如果存在 YAML frontmatter：
    #       --- ... ---
    #       后插入首图
    #
    # 2. 没有 frontmatter：
    #       文件开头直接插入
    # ==============================================================

    if (
        len(lines) >= 1
        and lines[0].strip() == "---"
    ):

        closing_index = None

        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                closing_index = i
                break

        if closing_index is not None:

            prefix = lines[
                : closing_index + 1
            ]

            suffix = lines[
                closing_index + 1 :
            ]

            output_lines = (
                prefix
                + [""]
                + build_image_block(
                    original_report_path,
                    image_dir,
                    report_type,
                )
                + [""]
                + suffix
            )

        else:

            output_lines = (
                build_image_block(
                    original_report_path,
                    image_dir,
                    report_type,
                )
                + [""]
                + lines
            )

    else:

        output_lines = (
            build_image_block(
                original_report_path,
                image_dir,
                report_type,
            )
            + [""]
            + lines
        )

    return "\n".join(output_lines).rstrip() + "\n"


# ======================================================================
# 23. 图片 Markdown Block
# ======================================================================

def build_image_block(
    report_path: Path,
    image_dir: Path,
    report_type: str,
) -> list[str]:

    block = []

    if report_type == "日报":
        block.append(
            "<!-- 748686_KNOWLEDGE_IMAGE_DAILY -->"
        )
    else:
        block.append(
            "<!-- 748686_KNOWLEDGE_IMAGE_WEEKLY -->"
        )

    block.append("")

    # 首图
    cover_path = image_dir / "首图.png"

    if is_valid_png(cover_path):

        relative = relative_image_path(
            report_path,
            cover_path,
        )

        block.append(
            f"![首图]({relative})"
        )

        block.append("")

    # 内容图
    for index in range(1, 4):

        image_name = f"插图{index}.png"

        image_path = image_dir / image_name

        if not is_valid_png(image_path):
            continue

        relative = relative_image_path(
            report_path,
            image_path,
        )

        block.append(
            f"![插图{index}]({relative})"
        )

        block.append("")

    return block


# ======================================================================
# 24. 带图报告路径
# ======================================================================

def image_report_path(
    original_path: Path,
) -> Path:

    if original_path.name.endswith(
        "_带图.md"
    ):
        return original_path

    return original_path.with_name(
        original_path.stem + "_带图.md"
    )


# ======================================================================
# 25. 检查带图报告
# ======================================================================

def validate_image_report(
    report_path: Path,
    image_dir: Path,
) -> bool:

    if not report_path.exists():
        return False

    try:
        text = read_text(
            report_path
        )

        if not text.strip():
            return False

        # 必须存在首图
        cover_path = image_dir / "首图.png"

        if not is_valid_png(cover_path):
            return False

        # 至少三张
        valid_count = len(
            existing_images(image_dir)
        )

        if valid_count < MIN_IMAGES:
            return False

        # 必须引用首图
        if "首图.png" not in text:
            return False

        # 至少两个插图
        if (
            "插图1.png" not in text
            or "插图2.png" not in text
        ):
            return False

        return True

    except Exception:
        return False


# ======================================================================
# 26. 处理日报
# ======================================================================

def process_daily_report(
    date_string: str,
    api_key: str,
) -> bool:

    section(
        f"日报配图：{date_string}"
    )

    report_path = find_daily_report(
        date_string
    )

    if report_path is None:

        log(
            f"⚠️ 未找到日报：{date_string}.md"
        )

        log(
            "跳过该日期，继续下一个日期。"
        )

        return True

    log(
        f"原始日报：{report_path}"
    )

    image_dir = daily_image_dir(
        date_string
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_image_status(
        image_dir
    )

    missing = missing_required_images(
        image_dir
    )

    if missing:

        log()
        log(
            "需要补生成的图片："
        )

        for name in missing:
            log(f"  → {name}")

        report_text = clean_report_for_prompt(
            read_text(report_path)
        )

        for image_name in missing:

            generate_one_image(
                report_type="日报",
                report_date=date_string,
                image_name=image_name,
                report_text=report_text,
                image_dir=image_dir,
                api_key=api_key,
            )

            # 每张图片生成后立即检查
            if not is_valid_png(
                image_dir / image_name
            ):
                raise RuntimeError(
                    f"❌ 图片生成后验证失败："
                    f"{image_name}"
                )

    else:

        log()
        log(
            "✅ 最低 3 张图片已经完整。"
        )

    # ==============================================================
    # 生成 _带图.md
    # ==============================================================

    image_report = image_report_path(
        report_path
    )

    log()
    log(
        f"生成带图日报：{image_report}"
    )

    image_markdown = build_image_markdown(
        original_report_path=report_path,
        image_dir=image_dir,
        report_type="日报",
    )

    atomic_write_text(
        image_report,
        image_markdown,
    )

    # ==============================================================
    # 最终验证
    # ==============================================================

    if not validate_image_report(
        image_report,
        image_dir,
    ):
        raise RuntimeError(
            f"❌ 日报带图版本验证失败："
            f"{image_report}"
        )

    log()
    log(
        f"✅ 日报完成并落盘：{date_string}"
    )

    log(
        f"   图片目录：{image_dir}"
    )

    log(
        f"   带图报告：{image_report}"
    )

    # ==============================================================
    # 再次输出图片状态
    # ==============================================================

    report_image_status(
        image_dir
    )

    return True


# ======================================================================
# 27. 处理周报
# ======================================================================

def process_weekly_report(
    week_key: str,
    api_key: str,
) -> bool:

    section(
        f"周报配图：{week_key}"
    )

    report_path = find_weekly_report(
        week_key
    )

    if report_path is None:

        log(
            f"⚠️ 未找到周报：{week_key}"
        )

        log(
            "跳过该周，继续下一个周报。"
        )

        return True

    log(
        f"原始周报：{report_path}"
    )

    image_dir = weekly_image_dir(
        week_key
    )

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_image_status(
        image_dir
    )

    missing = missing_required_images(
        image_dir
    )

    if missing:

        log()
        log(
            "需要补生成的图片："
        )

        for name in missing:
            log(f"  → {name}")

        report_text = clean_report_for_prompt(
            read_text(report_path)
        )

        for image_name in missing:

            generate_one_image(
                report_type="周报",
                report_date=week_key,
                image_name=image_name,
                report_text=report_text,
                image_dir=image_dir,
                api_key=api_key,
            )

            if not is_valid_png(
                image_dir / image_name
            ):
                raise RuntimeError(
                    f"❌ 图片生成后验证失败："
                    f"{image_name}"
                )

    else:

        log()
        log(
            "✅ 最低 3 张图片已经完整。"
        )

    # ==============================================================
    # 生成 _带图.md
    # ==============================================================

    image_report = image_report_path(
        report_path
    )

    log()
    log(
        f"生成带图周报：{image_report}"
    )

    image_markdown = build_image_markdown(
        original_report_path=report_path,
        image_dir=image_dir,
        report_type="周报",
    )

    atomic_write_text(
        image_report,
        image_markdown,
    )

    # ==============================================================
    # 最终验证
    # ==============================================================

    if not validate_image_report(
        image_report,
        image_dir,
    ):
        raise RuntimeError(
            f"❌ 周报带图版本验证失败："
            f"{image_report}"
        )

    log()
    log(
        f"✅ 周报完成并落盘：{week_key}"
    )

    log(
        f"   图片目录：{image_dir}"
    )

    log(
        f"   带图报告：{image_report}"
    )

    report_image_status(
        image_dir
    )

    return True


# ======================================================================
# 28. 主程序
# ======================================================================

def main() -> int:

    section(
        "748686 KNOWLEDGE IMAGE GENERATOR"
    )

    log(
        "系统：748686 自生长知识系统"
    )

    log(
        "任务：日报 / 周报配图与带图 Markdown"
    )

    log(
        "时间：UTC"
    )

    log(
        f"图片模型：{AGNES_IMAGE_MODEL}"
    )

    log(
        f"图片尺寸：{AGNES_IMAGE_SIZE}"
    )

    log(
        f"图片比例：{AGNES_IMAGE_RATIO}"
    )

    log(
        f"图片根目录：{IMAGE_ROOT}"
    )

    # ==============================================================
    # API Key
    # ==============================================================

    try:
        api_key = get_api_key()

    except Exception as e:

        log()
        log(str(e))

        return 1

    # ==============================================================
    # 日期
    # ==============================================================

    processing_dates = get_processing_dates()

    day_before = processing_dates[0]
    yesterday = processing_dates[1]
    today = processing_dates[2]

    log()
    log(
        "处理日期："
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

    # ==============================================================
    # 日报：严格按顺序逐个处理
    # ==============================================================

    section(
        "DAILY REPORTS"
    )

    for index, date_string in enumerate(
        processing_dates,
        start=1,
    ):

        log()
        log(
            f"日报处理 {index}/"
            f"{len(processing_dates)}"
        )

        process_daily_report(
            date_string=date_string,
            api_key=api_key,
        )

        log()
        log(
            f"✅ 第 {index} 份日报已经完成并落盘。"
        )

    # ==============================================================
    # 周报
    #
    # 三天可能属于同一个 ISO 周。
    # 去重，只处理一次。
    # ==============================================================

    section(
        "WEEKLY REPORTS"
    )

    weekly_keys = (
        get_week_keys_for_processing_dates(
            processing_dates
        )
    )

    log(
        f"需要检查的周报数量："
        f"{len(weekly_keys)}"
    )

    for index, week_key in enumerate(
        weekly_keys,
        start=1,
    ):

        log()
        log(
            f"周报处理 {index}/"
            f"{len(weekly_keys)}"
        )

        process_weekly_report(
            week_key=week_key,
            api_key=api_key,
        )

        log()
        log(
            f"✅ 第 {index} 份周报已经完成并落盘。"
        )

    # ==============================================================
    # 全部完成
    # ==============================================================

    section(
        "KNOWLEDGE IMAGE GENERATOR COMPLETE"
    )

    log(
        "✅ 所有日报 / 周报图片任务完成。"
    )

    log(
        "✅ 图片已经保存到 04_图片。"
    )

    log(
        "✅ 原始 Markdown 未修改。"
    )

    log(
        "✅ _带图.md 已独立生成。"
    )

    log(
        "✅ 每份报告均逐份处理并落盘。"
    )

    return 0


# ======================================================================
# 29. Entry Point
# ======================================================================

if __name__ == "__main__":

    try:
        sys.exit(
            main()
        )

    except KeyboardInterrupt:

        log()
        log(
            "⚠️ 用户中断任务。"
        )

        sys.exit(130)

    except Exception as e:

        log()
        log("=" * 72)
        log(
            "❌ KNOWLEDGE IMAGE GENERATOR FAILED"
        )
        log("=" * 72)
        log(
            f"{type(e).__name__}: {e}"
        )

        sys.exit(1)
