#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
knowledge_image.py
======================================================================

职责
----------------------------------------------------------------------

本脚本负责：

1. 自动计算 UTC 日期
2. 处理日报：
       前天
       昨天
       今天
3. 处理周报：
       根据上述日期对应的 ISO Week 查找周报
4. 检查报告是否存在
5. 检查已有图片是否有效
6. 仅生成缺失图片
7. 调用 AGNES Image API
8. 下载图片
9. 将图片立即保存到磁盘
10. 生成 *_带图.md
11. 对生成结果进行验证
12. 一个报告完成后才处理下一个报告

严格目录契约
----------------------------------------------------------------------

日报：

01_自生长知识系统/
├── 04_图片/
│   └── 日报/
│       └── YYYY-MM-DD/
│           ├── 首图.png
│           ├── 插图1.png
│           ├── 插图2.png
│           └── 插图3.png
│
└── 05_日报/
    └── YYYY/
        └── MM/
            ├── YYYY-MM-DD.md
            └── YYYY-MM-DD_带图.md


周报：

01_自生长知识系统/
├── 04_图片/
│   └── 周报/
│       └── YYYY-Wxx/
│           ├── 首图.png
│           ├── 插图1.png
│           ├── 插图2.png
│           └── 插图3.png
│
└── 06_周报/
    └── YYYY/
        ├── Wxx.md
        └── Wxx_带图.md


核心规则
----------------------------------------------------------------------

图片数量：

    最少 3 张
    最多 4 张

固定文件名：

    首图.png
    插图1.png
    插图2.png
    插图3.png

如果已经存在有效的 3 张：

    不强制生成第 4 张

如果已有第 4 张：

    保留

如果缺少图片：

    只生成缺少的图片

原始报告：

    永远不修改

带图报告：

    YYYY-MM-DD_带图.md
    Wxx_带图.md

语言目录契约
----------------------------------------------------------------------

整个系统语言目录只允许：

    en
    zh

本脚本不创建、不转换、不使用：

    EN
    ZH

时间契约
----------------------------------------------------------------------

所有日期逻辑使用 UTC。

AGNES Image API
----------------------------------------------------------------------

Endpoint:

    https://api.agnes-ai.cn/v1/images/generations

Model:

    agnes-image-2.5-flash

Project:

    size = 2K
    ratio = 16:9

response_format 必须：

    extra_body:
        response_format: url

API Key：

    环境变量：

        AGNES_API_KEY

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

# 01_自生长知识系统
SYSTEM_ROOT = SCRIPT_DIR.parent

# 报告目录
DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

# 图片总目录
IMAGE_ROOT = SYSTEM_ROOT / "04_图片"

# 图片目录
DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# 2. AGNES API
# ======================================================================

AGNES_API_URL = "https://api.agnes-ai.cn/v1/images/generations"
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

# 每篇报告至少三张
MIN_IMAGE_COUNT = 3

# 最多四张
MAX_IMAGE_COUNT = 4


# ======================================================================
# 4. 日志
# ======================================================================

def log(message: str) -> None:
    print(f"[knowledge_image] {message}", flush=True)


def log_error(message: str) -> None:
    print(f"[knowledge_image][ERROR] {message}", file=sys.stderr, flush=True)


# ======================================================================
# 5. UTC 日期
# ======================================================================

def utc_today() -> datetime.date:
    """
    返回当前 UTC 日期。
    """
    return datetime.now(timezone.utc).date()


# ======================================================================
# 6. 文件有效性
# ======================================================================

def is_valid_png(path: Path) -> bool:
    """
    检查文件是否至少具备 PNG 文件签名。
    """
    try:
        if not path.is_file():
            return False

        if path.stat().st_size < 8:
            return False

        with path.open("rb") as f:
            signature = f.read(8)

        return signature == b"\x89PNG\r\n\x1a\n"

    except Exception:
        return False


# ======================================================================
# 7. 原子写文件
# ======================================================================

def atomic_write_bytes(path: Path, data: bytes) -> None:
    """
    将二进制内容安全写入磁盘。

    先写临时文件，再 replace。
    避免 GitHub Actions 中出现半截文件。
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_name, path)

    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def atomic_write_text(
    path: Path,
    text: str,
    encoding: str = "utf-8",
) -> None:
    """
    原子写入文本文件。
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )

    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())

        os.replace(temp_name, path)

    except Exception:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


# ======================================================================
# 8. 报告发现
# ======================================================================

def find_daily_report(report_date) -> Path | None:
    """
    严格按照真实生产目录寻找日报：

        05_日报/YYYY/MM/YYYY-MM-DD.md
    """

    path = (
        DAILY_ROOT
        / f"{report_date.year:04d}"
        / f"{report_date.month:02d}"
        / f"{report_date.isoformat()}.md"
    )

    if path.is_file():
        return path

    return None


def find_weekly_report(year: int, week: int) -> Path | None:
    """
    严格按照真实生产目录寻找周报：

        06_周报/YYYY/Wxx.md
    """

    path = WEEKLY_ROOT / f"{year:04d}" / f"W{week:02d}.md"

    if path.is_file():
        return path

    return None


# ======================================================================
# 9. 周报 Key
# ======================================================================

def get_week_key(report_date) -> str:
    """
    根据 ISO Week 计算周报目录名称。

    例如：

        2026-09-08
        -> ISO year 2026
        -> ISO week 37

        返回：

        2026-W37
    """

    iso_year, iso_week, _ = report_date.isocalendar()

    return f"{iso_year:04d}-W{iso_week:02d}"


# ======================================================================
# 10. 图片目录
# ======================================================================

def get_daily_image_dir(report_date) -> Path:
    """
    日报图片：

        04_图片/日报/YYYY-MM-DD/
    """

    return DAILY_IMAGE_ROOT / report_date.isoformat()


def get_weekly_image_dir(year: int, week: int) -> Path:
    """
    周报图片：

        04_图片/周报/YYYY-Wxx/
    """

    return WEEKLY_IMAGE_ROOT / f"{year:04d}-W{week:02d}"


# ======================================================================
# 11. 读取报告
# ======================================================================

def read_report(path: Path) -> str:
    """
    读取 Markdown。
    """

    return path.read_text(encoding="utf-8")


# ======================================================================
# 12. AGNES Image API
# ======================================================================

def generate_image(prompt: str) -> bytes:
    """
    调用 AGNES Image API。

    返回：
        PNG 二进制数据
    """

    api_key = os.getenv("AGNES_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "环境变量 AGNES_API_KEY 未设置。"
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
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    log("调用 AGNES Image API")

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
            f"AGNES Image API HTTP {exc.code}: "
            f"{error_body[:2000]}"
        ) from exc

    except urllib.error.URLError as exc:

        raise RuntimeError(
            f"AGNES Image API 网络错误: {exc}"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            f"AGNES Image API 请求失败: {exc}"
        ) from exc

    try:
        result = json.loads(
            raw_response.decode("utf-8")
        )
    except Exception as exc:
        raise RuntimeError(
            "AGNES Image API 返回内容不是合法 JSON"
        ) from exc

    data = result.get("data")

    if not isinstance(data, list) or not data:
        raise RuntimeError(
            f"AGNES Image API 返回缺少 data: "
            f"{result}"
        )

    first = data[0]

    if not isinstance(first, dict):
        raise RuntimeError(
            f"AGNES Image API data[0] 格式异常: "
            f"{first}"
        )

    image_url = first.get("url")

    if not image_url:
        raise RuntimeError(
            f"AGNES Image API 未返回图片 URL: "
            f"{first}"
        )

    return download_image(image_url)


# ======================================================================
# 13. 下载图片
# ======================================================================

def download_image(url: str) -> bytes:
    """
    下载 AGNES 返回的图片 URL。
    """

    log(f"下载图片: {url}")

    request = urllib.request.Request(
        url,
        method="GET",
        headers={
            "User-Agent": (
                "748686-Knowledge-System/"
                "knowledge_image.py"
            )
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
            f"图片下载网络错误: {exc}: {url}"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            f"图片下载失败: {exc}: {url}"
        ) from exc

    if not data:
        raise RuntimeError(
            f"图片下载结果为空: {url}"
        )

    # PNG signature
    if not data.startswith(
        b"\x89PNG\r\n\x1a\n"
    ):
        raise RuntimeError(
            f"下载内容不是 PNG 文件: {url}"
        )

    return data


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
    根据报告内容生成图片 Prompt。

    report_type:
        日报
        周报
    """

    if image_name == "首图.png":

        role = (
            "你是一名专业新闻视觉设计师，"
            "为知识系统日报或周报制作高质量新闻主题首图。"
        )

        composition = (
            "画面具有明确的新闻与知识分析感，"
            "构图简洁、现代、专业，"
            "适合作为 Markdown 报告的横版首图。"
        )

    else:

        role = (
            "你是一名专业信息可视化与新闻插画设计师，"
            "为知识系统报告制作内容配图。"
        )

        composition = (
            "画面应直接对应报告核心主题，"
            "具有信息表达能力，"
            "避免纯装饰性图片。"
        )

    prompt = f"""
{role}

任务：
为「{report_type}」生成一张 16:9 横版知识报告图片。

报告标题：
{report_title}

当前图片：
{image_name}

设计要求：
- 16:9 横版构图
- 2K 高清
- 专业新闻媒体视觉风格
- 现代、克制、清晰
- 适合知识管理系统
- 有明确视觉主体
- 具有新闻信息与知识分析感
- 不要出现水印
- 不要出现 Logo
- 不要出现无意义的文字
- 不要生成乱码文字
- 不要使用卡通幼稚风格
- 不要过度赛博朋克
- 不要过度复杂
- 保持高级、专业、可信

{composition}

报告核心内容：

{report_content[:12000]}
"""

    return prompt.strip()


# ======================================================================
# 15. 获取报告标题
# ======================================================================

def extract_report_title(
    content: str,
    fallback: str,
) -> str:
    """
    尝试从 Markdown 第一层标题获取报告标题。
    """

    for line in content.splitlines():

        stripped = line.strip()

        if stripped.startswith("# "):

            title = stripped[2:].strip()

            if title:
                return title

    return fallback


# ======================================================================
# 16. 判断已有图片
# ======================================================================

def get_existing_images(
    image_dir: Path,
) -> list[str]:
    """
    返回已经存在且有效的图片。
    """

    valid_images = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):
            valid_images.append(image_name)

    return valid_images


# ======================================================================
# 17. 决定需要生成哪些图片
# ======================================================================

def determine_missing_images(
    image_dir: Path,
) -> list[str]:
    """
    核心规则：

    最少三张。

    如果首图、插图1、插图2全部存在：
        不强制生成插图3。

    如果其中任意一张缺失：
        只生成缺失项。

    如果已经存在插图3：
        保留。

    因此最终允许：

        3 张
        或
        4 张
    """

    required_names = IMAGE_NAMES[:MIN_IMAGE_COUNT]

    missing = []

    for image_name in required_names:

        path = image_dir / image_name

        if not is_valid_png(path):
            missing.append(image_name)

    return missing


# ======================================================================
# 18. 生成图片
# ======================================================================

def generate_missing_images(
    report_type: str,
    report_path: Path,
    image_dir: Path,
) -> None:
    """
    一个图片一个图片生成并立即落盘。
    """

    image_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    content = read_report(report_path)

    fallback_title = report_path.stem

    report_title = extract_report_title(
        content,
        fallback_title,
    )

    missing_images = determine_missing_images(
        image_dir
    )

    existing_images = get_existing_images(
        image_dir
    )

    log(
        f"{report_type}：{report_path.name}"
    )

    log(
        f"已有有效图片："
        f"{len(existing_images)} 张"
    )

    if not missing_images:

        log(
            "必需的 3 张图片均已存在，"
            "无需生成新图片。"
        )

        return

    log(
        "需要生成："
        + ", ".join(missing_images)
    )

    for image_name in missing_images:

        log(
            f"开始生成：{image_name}"
        )

        prompt = build_image_prompt(
            report_type=report_type,
            report_title=report_title,
            report_content=content,
            image_name=image_name,
        )

        image_data = generate_image(prompt)

        target_path = image_dir / image_name

        # 立即写入磁盘
        atomic_write_bytes(
            target_path,
            image_data,
        )

        # 立即验证
        if not is_valid_png(target_path):

            raise RuntimeError(
                f"图片写入后验证失败："
                f"{target_path}"
            )

        log(
            f"图片已落盘："
            f"{target_path}"
        )

    log(
        f"{report_type}图片生成阶段完成："
        f"{report_path.name}"
    )


# ======================================================================
# 19. 获取最终有效图片
# ======================================================================

def get_final_images(
    image_dir: Path,
) -> list[str]:
    """
    按固定顺序返回最终有效图片。
    """

    result = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):
            result.append(image_name)

    return result


# ======================================================================
# 20. Markdown 图片路径
# ======================================================================

def make_relative_image_path(
    report_path: Path,
    image_path: Path,
) -> str:
    """
    使用 os.path.relpath 计算 Markdown 图片路径。

    不硬编码 ../../../../ 等路径。
    """

    relative_path = os.path.relpath(
        image_path,
        start=report_path.parent,
    )

    # Markdown 使用 /
    return relative_path.replace(
        os.sep,
        "/",
    )


# ======================================================================
# 21. 插入图片 Markdown
# ======================================================================

def build_image_markdown(
    report_type: str,
    original_content: str,
    report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> str:
    """
    基于原始 Markdown 生成带图版本。

    永远从原始 .md 生成，
    不读取 *_带图.md 作为输入。

    因此不会发生图片块重复插入。
    """

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}有效图片数量不足："
            f"{len(image_names)} 张，"
            f"至少需要 {MIN_IMAGE_COUNT} 张。"
        )

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}图片数量超过上限："
            f"{len(image_names)} 张。"
        )

    image_lines = []

    for image_name in image_names:

        image_path = image_dir / image_name

        relative_path = make_relative_image_path(
            report_path,
            image_path,
        )

        image_lines.append(
            f"![]({relative_path})"
        )

    image_block = (
        "\n\n"
        "<!-- 748686_IMAGE_START -->\n"
        + "\n\n".join(image_lines)
        + "\n"
        "<!-- 748686_IMAGE_END -->\n\n"
    )

    content = original_content.strip()

    return (
        image_block
        + content
        + "\n"
    )


# ======================================================================
# 22. 验证带图 Markdown
# ======================================================================

def validate_image_report(
    report_type: str,
    image_report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> None:
    """
    对 *_带图.md 做完整验证：

    1. 文件存在
    2. 图片数量正确
    3. 图片实际存在
    4. 图片是有效 PNG
    5. Markdown 中包含图片引用
    """

    if not image_report_path.is_file():

        raise RuntimeError(
            f"{report_type}带图报告不存在："
            f"{image_report_path}"
        )

    content = image_report_path.read_text(
        encoding="utf-8"
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

    for image_name in image_names:

        image_path = image_dir / image_name

        if not is_valid_png(image_path):

            raise RuntimeError(
                f"{report_type}图片验证失败："
                f"{image_path}"
            )

        relative_path = make_relative_image_path(
            image_report_path,
            image_path,
        )

        expected_markdown = (
            f"![]({relative_path})"
        )

        if expected_markdown not in content:

            raise RuntimeError(
                f"{report_type}带图 Markdown "
                f"缺少图片引用："
                f"{expected_markdown}"
            )

    log(
        f"{report_type}带图报告验证成功："
        f"{image_report_path}"
    )


# ======================================================================
# 23. 生成带图报告
# ======================================================================

def build_image_report_path(
    report_path: Path,
) -> Path:
    """
    原始：

        xxx.md

    带图：

        xxx_带图.md
    """

    return report_path.with_name(
        f"{report_path.stem}_带图{report_path.suffix}"
    )


def create_image_report(
    report_type: str,
    report_path: Path,
    image_dir: Path,
) -> Path:
    """
    生成并立即保存 *_带图.md。
    """

    original_content = read_report(
        report_path
    )

    image_names = get_final_images(
        image_dir
    )

    if len(image_names) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}图片不足，"
            f"无法生成带图报告："
            f"{report_path}"
        )

    image_report_path = build_image_report_path(
        report_path
    )

    image_markdown = build_image_markdown(
        report_type=report_type,
        original_content=original_content,
        report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    # 立即落盘
    atomic_write_text(
        image_report_path,
        image_markdown,
    )

    log(
        f"{report_type}带图报告已落盘："
        f"{image_report_path}"
    )

    # 立即验证
    validate_image_report(
        report_type=report_type,
        image_report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    return image_report_path


# ======================================================================
# 24. 处理单篇日报
# ======================================================================

def process_daily_report(report_date) -> bool:
    """
    处理一篇日报。

    顺序：

    找报告
    ↓
    创建图片目录
    ↓
    检查图片
    ↓
    生成缺失图片
    ↓
    图片全部落盘
    ↓
    生成带图 Markdown
    ↓
    验证
    ↓
    完成
    """

    log("=" * 72)

    log(
        f"处理日报：{report_date.isoformat()}"
    )

    report_path = find_daily_report(
        report_date
    )

    if report_path is None:

        log(
            f"日报不存在，跳过："
            f"{report_date.isoformat()}"
        )

        return False

    image_dir = get_daily_image_dir(
        report_date
    )

    log(
        f"日报原始文件：{report_path}"
    )

    log(
        f"日报图片目录：{image_dir}"
    )

    # --------------------------------------------------------------
    # 1. 图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="日报",
        report_path=report_path,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 2. 最终图片检查
    # --------------------------------------------------------------

    final_images = get_final_images(
        image_dir
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"日报最终图片不足："
            f"{report_path}"
        )

    # --------------------------------------------------------------
    # 3. 生成带图 Markdown
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
# 25. 处理单篇周报
# ======================================================================

def process_weekly_report(
    iso_year: int,
    iso_week: int,
) -> bool:
    """
    处理一篇周报。
    """

    log("=" * 72)

    week_key = (
        f"{iso_year:04d}-W{iso_week:02d}"
    )

    log(
        f"处理周报：{week_key}"
    )

    report_path = find_weekly_report(
        iso_year,
        iso_week,
    )

    if report_path is None:

        log(
            f"周报不存在，跳过："
            f"{week_key}"
        )

        return False

    image_dir = get_weekly_image_dir(
        iso_year,
        iso_week,
    )

    log(
        f"周报原始文件：{report_path}"
    )

    log(
        f"周报图片目录：{image_dir}"
    )

    # --------------------------------------------------------------
    # 1. 图片
    # --------------------------------------------------------------

    generate_missing_images(
        report_type="周报",
        report_path=report_path,
        image_dir=image_dir,
    )

    # --------------------------------------------------------------
    # 2. 最终图片检查
    # --------------------------------------------------------------

    final_images = get_final_images(
        image_dir
    )

    if len(final_images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"周报最终图片不足："
            f"{report_path}"
        )

    # --------------------------------------------------------------
    # 3. 生成带图 Markdown
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
# 26. 主流程
# ======================================================================

def main() -> int:

    log("=" * 72)
    log("748686 自生长知识系统")
    log("knowledge_image.py")
    log("=" * 72)

    # --------------------------------------------------------------
    # API Key 检查
    # --------------------------------------------------------------

    if not os.getenv("AGNES_API_KEY", "").strip():

        log_error(
            "AGNES_API_KEY 未设置。"
        )

        return 1

    # --------------------------------------------------------------
    # UTC 日期
    # --------------------------------------------------------------

    today = utc_today()

    day_before = today - timedelta(days=2)
    yesterday = today - timedelta(days=1)

    log(
        f"DAY_BEFORE : {day_before.isoformat()}"
    )

    log(
        f"YESTERDAY  : {yesterday.isoformat()}"
    )

    log(
        f"TODAY      : {today.isoformat()}"
    )

    log(
        "Timezone   : UTC"
    )

    # ==============================================================
    # A. 日报
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

            processed = process_daily_report(
                report_date
            )

            if processed:
                daily_success += 1

        except Exception as exc:

            log_error(
                f"日报处理失败："
                f"{report_date.isoformat()}"
            )

            log_error(
                f"{type(exc).__name__}: {exc}"
            )

            # 单篇日报失败，不影响后续日报
            continue

    # ==============================================================
    # B. 周报
    # ==============================================================

    log("=" * 72)
    log("WEEKLY REPORT IMAGE GENERATION")
    log("=" * 72)

    # --------------------------------------------------------------
    # 根据三个日期得到对应 ISO Week
    # --------------------------------------------------------------

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
            weekly_keys.append(key)

    weekly_success = 0

    # --------------------------------------------------------------
    # 按顺序逐篇处理
    # --------------------------------------------------------------

    for iso_year, iso_week in weekly_keys:

        try:

            processed = process_weekly_report(
                iso_year,
                iso_week,
            )

            if processed:
                weekly_success += 1

        except Exception as exc:

            log_error(
                f"周报处理失败："
                f"{iso_year}-W{iso_week:02d}"
            )

            log_error(
                f"{type(exc).__name__}: {exc}"
            )

            # 单篇周报失败，不影响后续周报
            continue

    # ==============================================================
    # C. 最终统计
    # ==============================================================

    log("=" * 72)
    log("IMAGE GENERATION SUMMARY")
    log("=" * 72)

    log(
        f"日报完成：{daily_success}"
        f"/{len(daily_dates)}"
    )

    log(
        f"周报完成：{weekly_success}"
        f"/{len(weekly_keys)}"
    )

    log("=" * 72)
    log("knowledge_image.py 完成")
    log("=" * 72)

    # --------------------------------------------------------------
    # 注意：
    #
    # 单篇报告失败不会导致整个任务失败。
    #
    # 只有：
    #     初始化级别错误
    #     API Key 缺失
    #
    # 才会返回非 0。
    # --------------------------------------------------------------

    return 0


# ======================================================================
# 27. Entry Point
# ======================================================================

if __name__ == "__main__":
    sys.exit(main())
