#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
02_英语学习系统
knowledge_image.py
======================================================================

功能：
根据英语学习文章生成 ONE 张配套知识图片。

核心规则：
1. 一篇文章只生成一张图片
2. 根据文章标题 + 正文决定画面内容
3. 图片中加入文章原始英文标题
4. 视觉风格：
   - 1970s–1990s 日本复古动画电影感
   - 手绘赛璐珞动画质感
   - 手绘复古宫崎骏和新海诚动画质感
   - 复古背景绘画
   - 电影感构图
   - 温暖、诗意、怀旧
   - 细腻胶片颗粒
5. 不直接模仿具体艺术家的名字
6. 图片中除了文章英文标题，不允许出现其他文字
7. 使用 Agnes Image API
8. 模型：
   agnes-image-2.5-flash
9. 输出：
   2K / 16:9
10. Agnes 返回 URL 后立即下载并落盘
11. 单张图片失败自动重试
12. 图片生成由主程序独立调用
13. API Key 从 settings.json 指定的环境变量获取
14. 默认环境变量：
   AGNES_API_KEY

======================================================================
"""

import argparse
import base64
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# ======================================================================
# 路径
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_DIR = SCRIPT_DIR.parent

CONFIG_PATH = SYSTEM_DIR / "config" / "settings.json"
OUTPUT_DIR = SYSTEM_DIR / "output"


# ======================================================================
# Agnes 图片参数
# ======================================================================

DEFAULT_AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

DEFAULT_IMAGE_SIZE = "2K"
DEFAULT_IMAGE_RATIO = "16:9"

MAX_RETRIES = 5
RETRY_BASE_SECONDS = 5

IMAGE_FILENAME = "文章配图.png"


# ======================================================================
# 日志
# ======================================================================

def log(message: str):
    print(message, flush=True)


# ======================================================================
# 配置
# ======================================================================

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"找不到配置文件：{CONFIG_PATH}"
        )

    with CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as f:
        return json.load(f)


def get_required_env(name: str) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise RuntimeError(
            f"环境变量 {name} 未设置或为空。"
        )

    return value


# ======================================================================
# Markdown 清理
# ======================================================================

def clean_text(text: str) -> str:
    if not text:
        return ""

    # 删除代码块
    text = re.sub(
        r"```.*?```",
        "",
        text,
        flags=re.DOTALL,
    )

    # 删除 Markdown 图片
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    # Markdown 链接只保留文字
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    # 删除 Markdown 标题符号
    text = re.sub(
        r"^\s*#+\s*",
        "",
        text,
        flags=re.MULTILINE,
    )

    # 删除 HTML
    text = re.sub(
        r"<[^>]+>",
        "",
        text,
    )

    # 压缩空白
    text = re.sub(
        r"\s+",
        " ",
        text,
    )

    return text.strip()


# ======================================================================
# 提取标题和正文
# ======================================================================

def extract_title_and_body(markdown_text: str):
    lines = markdown_text.splitlines()

    title = ""

    # ------------------------------------------------------------------
    # 1. Markdown 标题
    # ------------------------------------------------------------------

    for line in lines:
        stripped = line.strip()

        match = re.match(
            r"^#{1,6}\s+(.+?)\s*$",
            stripped,
        )

        if match:
            title = clean_text(
                match.group(1)
            )
            break

    # ------------------------------------------------------------------
    # 2. Title:
    # ------------------------------------------------------------------

    if not title:
        for line in lines:
            stripped = line.strip()

            match = re.match(
                r"^(?:Title|TITLE|title)\s*[:：]\s*(.+)$",
                stripped,
            )

            if match:
                title = clean_text(
                    match.group(1)
                )
                break

    # ------------------------------------------------------------------
    # 3. 中文标题：
    # ------------------------------------------------------------------

    if not title:
        for line in lines:
            stripped = line.strip()

            match = re.match(
                r"^标题\s*[:：]\s*(.+)$",
                stripped,
            )

            if match:
                title = clean_text(
                    match.group(1)
                )
                break

    # ------------------------------------------------------------------
    # 4. 第一行非空文本
    # ------------------------------------------------------------------

    if not title:
        for line in lines:
            stripped = clean_text(line)

            if stripped:
                title = stripped
                break

    # ------------------------------------------------------------------
    # 正文
    # ------------------------------------------------------------------

    body_lines = []

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        cleaned = clean_text(stripped)

        if not cleaned:
            continue

        # 跳过标题
        if title and cleaned == title:
            continue

        # 跳过 Title:
        if re.match(
            r"^(?:Title|TITLE|title|标题)\s*[:：]",
            cleaned,
        ):
            continue

        body_lines.append(cleaned)

    body = clean_text(
        "\n".join(body_lines)
    )

    return title, body


# ======================================================================
# 自动寻找文章
# ======================================================================

def find_article_file(run_date: str) -> Path:
    date_dir = OUTPUT_DIR / run_date

    if not date_dir.exists():
        raise FileNotFoundError(
            f"找不到当天输出目录：{date_dir}"
        )

    candidates = []

    # ------------------------------------------------------------------
    # 优先搜索文章目录
    # ------------------------------------------------------------------

    article_dirs = [
        date_dir / "文章",
        date_dir / "英语文章",
        date_dir / "article",
        date_dir / "articles",
    ]

    for directory in article_dirs:
        if directory.exists():
            candidates.extend(
                sorted(
                    directory.glob("*.md")
                )
            )

    # ------------------------------------------------------------------
    # 如果没找到，则搜索当天所有 Markdown
    # ------------------------------------------------------------------

    if not candidates:
        candidates = sorted(
            p
            for p in date_dir.rglob("*.md")
            if "配图" not in str(p)
        )

    if not candidates:
        raise FileNotFoundError(
            f"在 {date_dir} 中没有找到 Markdown 文章。"
        )

    # ------------------------------------------------------------------
    # 优先文章类文件
    # ------------------------------------------------------------------

    priority = []

    for path in candidates:
        name = path.stem.lower()

        if (
            "article" in name
            or "english" in name
            or "文章" in name
        ):
            priority.append(path)

    if priority:
        return priority[0]

    return candidates[0]


# ======================================================================
# 图片 Prompt
# ======================================================================

def build_image_prompt(
    title: str,
    body: str,
) -> str:

    # 防止正文过长
    body_for_prompt = body[:12000]

    prompt = f"""
Create ONE cinematic editorial illustration based on the
following English learning article.

============================================================
ARTICLE TITLE
============================================================

{title}

============================================================
ARTICLE CONTENT
============================================================

{body_for_prompt}

============================================================
MAIN REQUIREMENT
============================================================

First understand the article.

Then create ONE specific, meaningful visual scene that
communicates the central subject, situation, people,
environment, action, and emotional atmosphere of the article.

The image must NOT be a generic stock illustration.

The visual scene must clearly feel connected to the article.

If the article describes people, show appropriate people
and natural interaction.

If it describes a place, make the environment important.

If it describes education, work, technology, nature, travel,
society, family, relationships, history, daily life, or another
topic, visually communicate that topic through a coherent
cinematic scene.

============================================================
VISUAL STYLE
============================================================

Japanese retro animated feature-film aesthetic inspired by
the visual language of the 1970s, 1980s, and early 1990s.

Traditional hand-drawn cel animation feeling.

Hand-painted backgrounds.

Classic painted animation backgrounds.

Subtle analog film grain.

Slightly softened edges.

Natural hand-drawn line quality.

Warm atmospheric lighting.

Poetic cinematic composition.

Nostalgic late-Showa and early-Heisei mood.

Beautiful environmental storytelling.

Natural human expressions.

Believable anatomy.

Detailed environments.

Quiet emotional atmosphere.

A sense of wonder, warmth, youth, memory, and everyday life.

Use slightly muted vintage colors.

Avoid modern glossy digital-art appearance.

Avoid photorealism.

Avoid 3D-rendered appearance.

The final image should feel like a carefully painted frame
from a classic Japanese animated feature film.

============================================================
COMPOSITION
============================================================

16:9 widescreen cinematic composition.

Strong foreground, middleground, and background.

Clear focal subject.

Natural depth.

Elegant visual balance.

Leave sufficient clean negative space for the English
article title.

The article title should feel like part of a beautiful
vintage animated-film poster.

The artwork remains the primary visual element.

============================================================
ARTICLE TITLE IN IMAGE
============================================================

The ONLY intentional readable text in the image must be:

"{title}"

Render the title EXACTLY as provided.

Do NOT:

- translate it
- rewrite it
- shorten it
- abbreviate it
- replace it
- paraphrase it
- misspell it
- invent another title

Use elegant vintage cinematic English typography.

The title should be highly readable.

Place it naturally in the negative space of the composition.

Use restrained, tasteful typography.

============================================================
TEXT RESTRICTIONS
============================================================

Absolutely NO other readable text.

No subtitles.

No captions.

No dialogue.

No speech bubbles.

No additional English words.

No Chinese text.

No Japanese text.

No logos.

No brand names.

No watermarks.

No signatures.

No random letters.

No fake newspaper text.

No fake signs with readable writing.

The ONLY readable text is:

"{title}"

============================================================
FINAL IMAGE
============================================================

One finished image.

Cinematic.

Hand-painted.

Nostalgic.

Elegant.

Emotionally meaningful.

Visually connected to the article.

16:9 widescreen.

High detail.

Retro Japanese animation atmosphere.
"""

    return prompt.strip()


# ======================================================================
# Agnes API 请求
# ======================================================================

def agnes_generate_image(
    api_key: str,
    base_url: str,
    model: str,
    prompt: str,
):
    """
    调用 Agnes Image API。

    请求：

    POST /images/generations

    参数：

    model
    prompt
    n
    size=2K
    ratio=16:9
    extra_body.response_format=url
    """

    url = (
        base_url.rstrip("/")
        + "/images/generations"
    )

    payload = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": DEFAULT_IMAGE_SIZE,
        "ratio": DEFAULT_IMAGE_RATIO,
        "extra_body": {
            "response_format": "url",
        },
    }

    data = json.dumps(
        payload,
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        url,
        data=data,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    log("")
    log("Calling Agnes Image API...")
    log(f"Endpoint: {url}")
    log(f"Model: {model}")
    log(f"Size: {DEFAULT_IMAGE_SIZE}")
    log(f"Ratio: {DEFAULT_IMAGE_RATIO}")

    with urlopen(
        request,
        timeout=600,
    ) as response:

        raw = response.read()

        result = json.loads(
            raw.decode("utf-8")
        )

    # ------------------------------------------------------------------
    # API 基本检查
    # ------------------------------------------------------------------

    if not isinstance(result, dict):
        raise RuntimeError(
            f"Agnes 返回格式异常：{result}"
        )

    data_list = result.get("data")

    if not data_list:
        raise RuntimeError(
            f"Agnes 没有返回图片：{result}"
        )

    item = data_list[0]

    # ------------------------------------------------------------------
    # URL
    # ------------------------------------------------------------------

    image_url = item.get("url")

    if image_url:
        return {
            "type": "url",
            "value": image_url,
        }

    # ------------------------------------------------------------------
    # Base64 备用
    # ------------------------------------------------------------------

    b64_json = item.get("b64_json")

    if b64_json:
        return {
            "type": "base64",
            "value": b64_json,
        }

    raise RuntimeError(
        f"Agnes 返回中没有 url 或 b64_json：{result}"
    )


# ======================================================================
# 下载图片
# ======================================================================

def download_image(
    image_url: str,
) -> bytes:

    log("")
    log("Downloading generated image...")

    request = Request(
        image_url,
        headers={
            "User-Agent":
                "748686-English-Learning-System",
        },
    )

    with urlopen(
        request,
        timeout=600,
    ) as response:

        image_bytes = response.read()

    if not image_bytes:
        raise RuntimeError(
            "下载到的图片为空。"
        )

    return image_bytes


# ======================================================================
# Base64 解码
# ======================================================================

def decode_base64_image(
    b64_data: str,
) -> bytes:

    image_bytes = base64.b64decode(
        b64_data
    )

    if not image_bytes:
        raise RuntimeError(
            "Base64 图片为空。"
        )

    return image_bytes


# ======================================================================
# 安全保存
# ======================================================================

def save_image(
    image_bytes: bytes,
    output_path: Path,
):
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------------------
    # 临时文件
    # ------------------------------------------------------------------

    temp_path = output_path.with_suffix(
        ".tmp"
    )

    with temp_path.open(
        "wb"
    ) as f:

        f.write(image_bytes)

        f.flush()

        os.fsync(
            f.fileno()
        )

    # ------------------------------------------------------------------
    # 原子替换
    # ------------------------------------------------------------------

    temp_path.replace(
        output_path
    )


# ======================================================================
# 生成图片
# ======================================================================

def generate_image(
    date: str = "",
    run_date: str = "",
    article_path: Path | None = None,
    config: dict | None = None,
):
    """
    生成一张英语文章配图。

    兼容 main.py 当前调用：

        generate_image(date=date)

    也兼容直接调用：

        generate_image(
            run_date="2026-09-26",
            article_path=Path(...),
            config=config,
        )
    """

    # ------------------------------------------------------------------
    # 兼容 date / run_date
    # ------------------------------------------------------------------

    if date and not run_date:
        run_date = date

    run_date = str(run_date).strip()

    if not run_date:
        raise ValueError(
            "缺少文章日期：date / run_date"
        )

    # ------------------------------------------------------------------
    # 日期格式
    # ------------------------------------------------------------------

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        run_date,
    ):
        raise ValueError(
            f"日期格式错误：{run_date}"
        )

    # ------------------------------------------------------------------
    # 读取配置
    # ------------------------------------------------------------------

    if config is None:
        config = load_config()

    # ------------------------------------------------------------------
    # 找文章
    # ------------------------------------------------------------------

    if article_path is None:

        article_path = find_article_file(
            run_date
        )

    else:

        article_path = Path(
            article_path
        )

        if not article_path.is_absolute():
            article_path = (
                SYSTEM_DIR / article_path
            )

        article_path = article_path.resolve()

        if not article_path.exists():
            raise FileNotFoundError(
                f"指定文章不存在：{article_path}"
            )

    # ------------------------------------------------------------------
    # 读取文章
    # ------------------------------------------------------------------

    markdown = article_path.read_text(
        encoding="utf-8"
    )

    title, body = extract_title_and_body(
        markdown
    )

    if not title:
        raise RuntimeError(
            "无法从文章中提取英文标题。"
        )

    if not body:
        raise RuntimeError(
            "文章正文为空。"
        )

    # ------------------------------------------------------------------
    # 日志
    # ------------------------------------------------------------------

    log("")
    log("=" * 72)
    log("748686 · 02_英语学习系统")
    log("KNOWLEDGE IMAGE")
    log("=" * 72)

    log(f"DATE: {run_date}")
    log(f"ARTICLE: {article_path}")
    log(f"TITLE: {title}")

    log("=" * 72)

    # ------------------------------------------------------------------
    # Agnes 配置
    # ------------------------------------------------------------------

    agnes_config = config.get(
        "agnes",
        {},
    )

    base_url = (
        agnes_config
        .get(
            "base_url",
            "https://api.agnes-ai.cn/v1",
        )
        .strip()
    )

    # ------------------------------------------------------------------
    # 图片模型
    #
    # 明确使用：
    # agnes-image-2.5-flash
    #
    # 不使用文字模型。
    # ------------------------------------------------------------------

    model = (
        agnes_config
        .get(
            "image_model",
            DEFAULT_AGNES_IMAGE_MODEL,
        )
        .strip()
    )

    if not model:
        model = DEFAULT_AGNES_IMAGE_MODEL

    # ------------------------------------------------------------------
    # API Key 环境变量名称
    # ------------------------------------------------------------------

    api_key_env = (
        agnes_config
        .get(
            "api_key_env",
            "AGNES_API_KEY",
        )
        .strip()
    )

    api_key = get_required_env(
        api_key_env
    )

    # ------------------------------------------------------------------
    # 输出
    # ------------------------------------------------------------------

    image_dir = (
        OUTPUT_DIR
        / run_date
        / "配图"
    )

    output_path = (
        image_dir
        / IMAGE_FILENAME
    )

    # ------------------------------------------------------------------
    # 如果已经生成过
    # ------------------------------------------------------------------

    if (
        output_path.exists()
        and output_path.stat().st_size > 0
    ):

        log("")
        log("✓ 配图已经存在")
        log(f"✓ {output_path}")

        return output_path

    # ------------------------------------------------------------------
    # Prompt
    # ------------------------------------------------------------------

    prompt = build_image_prompt(
        title,
        body,
    )

    log("")
    log("IMAGE PROMPT")
    log("-" * 72)
    log(prompt)
    log("-" * 72)

    # ------------------------------------------------------------------
    # 重试
    # ------------------------------------------------------------------

    last_error = None

    for attempt in range(
        1,
        MAX_RETRIES + 1,
    ):

        log("")
        log(
            f"🖼️ Agnes 图片生成 "
            f"{attempt}/{MAX_RETRIES}"
        )

        try:

            result = agnes_generate_image(
                api_key=api_key,
                base_url=base_url,
                model=model,
                prompt=prompt,
            )

            # ----------------------------------------------------------
            # URL
            # ----------------------------------------------------------

            if result["type"] == "url":

                image_bytes = download_image(
                    result["value"]
                )

            # ----------------------------------------------------------
            # Base64
            # ----------------------------------------------------------

            elif result["type"] == "base64":

                image_bytes = decode_base64_image(
                    result["value"]
                )

            else:

                raise RuntimeError(
                    f"未知图片返回类型："
                    f"{result['type']}"
                )

            # ----------------------------------------------------------
            # 基本图片检查
            # ----------------------------------------------------------

            if not image_bytes:
                raise RuntimeError(
                    "图片数据为空。"
                )

            # ----------------------------------------------------------
            # 立即保存
            # ----------------------------------------------------------

            save_image(
                image_bytes,
                output_path,
            )

            # ----------------------------------------------------------
            # 落盘后检查
            # ----------------------------------------------------------

            if (
                not output_path.exists()
                or output_path.stat().st_size == 0
            ):
                raise RuntimeError(
                    "图片保存后文件不存在或为空。"
                )

            log("")
            log("✓ 图片生成成功")
            log("✓ 图片已经立即落盘")
            log(f"✓ {output_path}")

            log("")
            log("=" * 72)
            log("KNOWLEDGE IMAGE SUCCESS")
            log("=" * 72)

            return output_path

        except HTTPError as e:

            error_body = ""

            try:
                error_body = (
                    e.read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )
            except Exception:
                pass

            last_error = (
                f"HTTP {e.code}: "
                f"{error_body}"
            )

            log("")
            log("❌ Agnes API 请求失败")
            log(last_error)

        except URLError as e:

            last_error = (
                f"网络错误：{e}"
            )

            log("")
            log("❌ 图片下载/网络错误")
            log(last_error)

        except Exception as e:

            last_error = (
                f"{type(e).__name__}: {e}"
            )

            log("")
            log("❌ 图片生成失败")
            log(last_error)

        # --------------------------------------------------------------
        # 重试
        # --------------------------------------------------------------

        if attempt < MAX_RETRIES:

            wait_seconds = (
                RETRY_BASE_SECONDS
                * attempt
            )

            log(
                f"⏳ {wait_seconds} 秒后重试..."
            )

            time.sleep(
                wait_seconds
            )

    # ------------------------------------------------------------------
    # 全部失败
    # ------------------------------------------------------------------

    raise RuntimeError(
        "Agnes 图片生成最终失败。\n"
        f"最后错误：{last_error}"
    )


# ======================================================================
# MAIN
# ======================================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "02_英语学习系统："
            "使用 Agnes Image 2.5 Flash "
            "生成一张英语文章配图"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help=(
            "文章日期，例如：2026-09-09"
        ),
    )

    parser.add_argument(
        "--article",
        required=False,
        default="",
        help=(
            "可选：直接指定文章 Markdown 文件"
        ),
    )

    args = parser.parse_args()

    run_date = args.date.strip()

    # ------------------------------------------------------------------
    # 日期格式
    # ------------------------------------------------------------------

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        run_date,
    ):
        raise ValueError(
            f"日期格式错误：{run_date}"
        )

    # ------------------------------------------------------------------
    # 读取配置
    # ------------------------------------------------------------------

    config = load_config()

    # ------------------------------------------------------------------
    # 找文章
    # ------------------------------------------------------------------

    if args.article:

        article_path = Path(
            args.article
        )

        if not article_path.is_absolute():
            article_path = (
                SYSTEM_DIR
                / article_path
            )

        article_path = (
            article_path.resolve()
        )

        if not article_path.exists():
            raise FileNotFoundError(
                f"指定文章不存在："
                f"{article_path}"
            )

    else:

        article_path = find_article_file(
            run_date
        )

    # ------------------------------------------------------------------
    # 生成
    # ------------------------------------------------------------------

    output_path = generate_image(
        date=run_date,
        article_path=article_path,
        config=config,
    )

    # ------------------------------------------------------------------
    # 最终
    # ------------------------------------------------------------------

    log("")
    log("=" * 72)
    log("IMAGE GENERATION FINISHED")
    log("=" * 72)
    log(f"ARTICLE: {article_path}")
    log(f"IMAGE: {output_path}")
    log("=" * 72)

    return 0


# ======================================================================
# 程序入口
# ======================================================================

if __name__ == "__main__":

    try:

        sys.exit(
            main()
        )

    except KeyboardInterrupt:

        log("")
        log("❌ 用户中断。")

        sys.exit(130)

    except Exception as e:

        log("")
        log("=" * 72)
        log("KNOWLEDGE IMAGE FAILED")
        log("=" * 72)
        log(
            f"❌ {type(e).__name__}: {e}"
        )
        log("=" * 72)

        # --------------------------------------------------------------
        # 这里保持与你当前 main.py 的独立图片设计一致：
        #
        # 如果直接执行 knowledge_image.py，
        # 图片失败不会把整个系统判定为文章系统失败。
        #
        # 但 main.py 直接调用 generate_image() 时，
        # generate_image() 本身会抛出异常，
        # 因此 main.py 可以正确判断图片生成失败。
        # --------------------------------------------------------------

        sys.exit(0)
