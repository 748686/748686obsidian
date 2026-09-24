#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V5.4.1

======================================================================
核心原则
======================================================================

本版本以 V5.4.1 为主体，只进行两类学习合并：

【一】周报日期逻辑
学习 V5.3：

    当前 UTC 日期
        ↓
    当前 ISO Year / Week
        ↓
    例如：
        2026-09-21 ～ 2026-09-27
                ↓
             2026/W39
                ↓
        06_周报/2026/W39.md

同一个 ISO 周内：

    09-21 → W39
    09-22 → W39
    09-23 → W39
    ...
    09-27 → W39

进入：

    09-28
        ↓
       W40

自动切换到：

    06_周报/2026/W40.md

同一周内每次运行都重新读取当前 Wxx.md。
因此当本周日报不断增加、周报重新生成以后，
图片也可以重新根据最新周报生成。

【二】图片系统与排版
完全以 V5.2 为质量基准：

    - V5.2 Visual Contract
    - V5.2 新闻内容提取逻辑
    - V5.2 Prompt
    - V5.2 首图/插图1同新闻不同机位
    - V5.2 插图2/插图3重点新闻逻辑
    - V5.2 图片验证
    - V5.2 Grid 检查
    - V5.2 重试机制
    - V5.2 correction prompt
    - OCR 永久 DISABLED
    - V5.2 图片排版方式

日报与周报使用同一套 create_image_markdown() 排版算法。

======================================================================
报告路径
======================================================================

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

======================================================================
重要约束
======================================================================

1. 不修改原始日报/周报 Markdown。
2. 只生成 *_带图.md。
3. 日报 TODAY 必须成功。
4. YESTERDAY / DAY_BEFORE 缺失可以 SKIP。
5. 周报不存在可以 SKIP。
6. 周报图片每次运行重新根据当前 Wxx.md 生成。
7. OCR 永久关闭。
8. 不改变 Feishu image_key 链路。
9. 不修改 weekly_report.py。
10. 不修改 Task 1～4。
======================================================================
"""

from __future__ import annotations

import base64
import io
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Tuple
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

# 自生长知识系统的业务日期以 GitHub Actions / UTC 为准。
# 不使用本地运行机器时区决定 TODAY。
UTC = timezone.utc


def utc_now() -> datetime:
    return datetime.now(UTC)


def utc_today() -> date:
    return utc_now().date()


# ======================================================================
# 环境变量
# ======================================================================

AGNES_API_KEY = (
    os.getenv("AGNES_API_KEY")
    or os.getenv("AI_API_KEY")
    or ""
).strip()

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1",
).rstrip("/")

AGNES_IMAGE_URL = (
    f"{AGNES_BASE_URL}/images/generations"
)

AGNES_IMAGE_MODEL = os.getenv(
    "AGNES_IMAGE_MODEL",
    "agnes-image-2.5-flash",
).strip()

IMAGE_SIZE = os.getenv(
    "IMAGE_SIZE",
    "2K",
).strip()

IMAGE_RATIO = os.getenv(
    "IMAGE_RATIO",
    "16:9",
).strip()

IMAGE_TIMEOUT = int(
    os.getenv(
        "IMAGE_TIMEOUT",
        "180",
    )
)

MAX_IMAGE_RETRIES = int(
    os.getenv(
        "MAX_IMAGE_RETRIES",
        "5",
    )
)

IMAGE_THROTTLE = float(
    os.getenv(
        "IMAGE_THROTTLE",
        "2",
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

IMAGE_NAMES = (
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
)


# ======================================================================
# 日志
# ======================================================================

def log(message: str = "") -> None:
    print(message, flush=True)


# ======================================================================
# ISO 周
# ======================================================================

def iso_year_week(
    target_date: date,
) -> Tuple[int, int, str]:

    iso = target_date.isocalendar()

    return (
        iso.year,
        iso.week,
        f"W{iso.week:02d}",
    )


def current_iso_week() -> Tuple[int, int, str]:
    """
    当前 UTC 日期对应的 ISO 年 / ISO 周。
    """

    return iso_year_week(
        utc_today()
    )


# ======================================================================
# 日报日期
# ======================================================================

def target_dates() -> List[date]:
    """
    保持 V5.2：

        DAY_BEFORE
        YESTERDAY
        TODAY

    使用 UTC。
    """

    today = utc_today()

    return [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]


# ======================================================================
# 日报路径
# ======================================================================

def get_daily_report_path(
    target_date: date,
) -> Path:

    date_text = target_date.isoformat()

    return (
        DAILY_ROOT
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / f"{date_text}.md"
    )


def find_daily_report(
    target_date: date,
) -> Optional[Path]:

    date_text = target_date.isoformat()

    # ==============================================================
    # 当前真实结构
    # ==============================================================

    candidates = [
        get_daily_report_path(
            target_date
        ),

        # 兼容历史结构
        DAILY_ROOT / f"{date_text}.md",

        DAILY_ROOT / f"{date_text}日报.md",

        DAILY_ROOT
        / date_text
        / f"{date_text}.md",
    ]

    for path in candidates:

        if (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
            and "_带图" not in path.name
        ):
            return path

    # ==============================================================
    # 最后兼容搜索
    # ==============================================================

    if DAILY_ROOT.exists():

        matches = sorted(
            [
                path
                for path in DAILY_ROOT.rglob("*.md")
                if path.is_file()
                and date_text in path.name
                and "_带图" not in path.name
                and path.stat().st_size > 0
            ]
        )

        if matches:
            return matches[-1]

    return None


# ======================================================================
# 周报路径
# ======================================================================

def get_weekly_report_path(
    year: int,
    week: int,
) -> Path:

    return (
        WEEKLY_ROOT
        / str(year)
        / f"W{week:02d}.md"
    )


def find_weekly_report(
    year: int,
    week: int,
) -> Optional[Path]:

    week_key = f"W{week:02d}"

    # ==============================================================
    # 当前真实结构
    #
    # 06_周报/2026/W39.md
    # ==============================================================

    candidates = [
        WEEKLY_ROOT
        / str(year)
        / f"{week_key}.md",

        WEEKLY_ROOT
        / str(year)
        / f"{week_key}周报.md",

        WEEKLY_ROOT
        / str(year)
        / week_key
        / f"{week_key}.md",
    ]

    for path in candidates:

        if (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
            and "_带图" not in path.name
        ):
            return path

    # ==============================================================
    # 兼容旧结构
    # ==============================================================

    legacy_candidates = [
        WEEKLY_ROOT / f"{week_key}.md",
        WEEKLY_ROOT / f"{week_key}周报.md",
        WEEKLY_ROOT / week_key / f"{week_key}.md",
    ]

    for path in legacy_candidates:

        if (
            path.exists()
            and path.is_file()
            and path.stat().st_size > 0
            and "_带图" not in path.name
        ):
            return path

    # ==============================================================
    # 当前年份目录下兼容搜索
    # ==============================================================

    search_root = WEEKLY_ROOT / str(year)

    if search_root.exists():

        matches = sorted(
            [
                path
                for path in search_root.rglob("*.md")
                if path.is_file()
                and week_key in path.name
                and "_带图" not in path.name
                and path.stat().st_size > 0
            ]
        )

        if matches:
            return matches[-1]

    return None


# ======================================================================
# 图片相对路径
# ======================================================================

def make_relative_image_ref(
    report_path: Path,
    image_path: Path,
) -> str:
    """
    根据真实报告目录计算图片相对路径。

    日报：

        05_日报/2026/09/
            ↓
        ../../../04_图片/日报/2026-09-24/首图.png

    周报：

        06_周报/2026/
            ↓
        ../../04_图片/周报/2026-W39/首图.png
    """

    return Path(
        os.path.relpath(
            image_path,
            start=report_path.parent,
        )
    ).as_posix()


# ======================================================================
# Markdown 基础清理
# ======================================================================

def strip_markdown(
    text: str,
) -> str:

    # 图片
    text = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        text,
    )

    # 链接
    text = re.sub(
        r"\[([^\]]+)\]\([^)]+\)",
        r"\1",
        text,
    )

    # 行内代码
    text = re.sub(
        r"`{1,3}([^`]+)`{1,3}",
        r"\1",
        text,
    )

    # Markdown 强调符号
    text = re.sub(
        r"[*_~]+",
        "",
        text,
    )

    return text


# ======================================================================
# 新闻内容提取
# ======================================================================

NOISE_HEADINGS = {
    "目录",
    "contents",
    "参考资料",
    "参考来源",
    "来源",
    "sources",
    "source",
    "总结",
    "结语",
    "免责声明",
}


def is_noise_heading(
    heading: str,
) -> bool:

    normalized = (
        heading
        .strip()
        .lower()
    )

    return normalized in {
        item.lower()
        for item in NOISE_HEADINGS
    }


def normalize_line(
    line: str,
) -> str:

    return re.sub(
        r"\s+",
        " ",
        strip_markdown(line),
    ).strip()


def extract_news_items(
    markdown: str,
) -> List[str]:
    """
    V5.2 新闻提取逻辑。

    支持：

        ## 标题
        ### 标题
        1. 新闻
        - 新闻
        * 新闻

    如果没有结构化列表，
    再使用正文段落作为 fallback。
    """

    text = (
        markdown
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    lines = text.split("\n")

    items: List[str] = []

    current_heading = ""

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # Front Matter
        if line == "---":
            continue

        # --------------------------------------------------------------
        # 标题
        # --------------------------------------------------------------

        heading_match = re.match(
            r"^#{1,6}\s+(.+?)\s*$",
            line,
        )

        if heading_match:

            heading = normalize_line(
                heading_match.group(1)
            )

            if (
                heading
                and not is_noise_heading(
                    heading
                )
            ):
                current_heading = heading

            continue

        # --------------------------------------------------------------
        # 编号列表
        # --------------------------------------------------------------

        numbered_match = re.match(
            r"^\d+[.)]\s+(.+)$",
            line,
        )

        if numbered_match:

            content = normalize_line(
                numbered_match.group(1)
            )

            if content:

                if current_heading:
                    content = (
                        f"{current_heading}："
                        f"{content}"
                    )

                items.append(content)

            continue

        # --------------------------------------------------------------
        # 无序列表
        # --------------------------------------------------------------

        bullet_match = re.match(
            r"^[-*+]\s+(.+)$",
            line,
        )

        if bullet_match:

            content = normalize_line(
                bullet_match.group(1)
            )

            if content:

                if current_heading:
                    content = (
                        f"{current_heading}："
                        f"{content}"
                    )

                items.append(content)

            continue

    # ==============================================================
    # fallback：没有结构化新闻时使用正文段落
    # ==============================================================

    if not items:

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        for paragraph in paragraphs:

            paragraph = normalize_line(
                paragraph
            )

            if not paragraph:
                continue

            if len(paragraph) < 20:
                continue

            items.append(paragraph)

    # ==============================================================
    # 去重
    # ==============================================================

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
# V5.2 Visual Contract
# ======================================================================

VISUAL_CONTRACT = """
必须严格遵守以下视觉约束：

最终视觉类型必须是：
“无文字信息图 / 新闻插图”。

但这里的“无文字信息图”绝对不是：
海报、信息图表、数据可视化、网页截图、
新闻标题卡片、报纸版式、宣传海报。

它必须是一张完整的、真实新闻摄影风格的单幅场景。

【场景结构】

- 只能有一个完整场景。
- 只能有一个地点。
- 只能有一个时间。
- 只能有一个瞬间。
- 只能有一个主要视觉中心。
- 所有元素必须存在于同一个真实连续空间中。
- 必须像专业新闻摄影记者现场拍摄的一张照片。

【严格禁止】

- 禁止多事件。
- 禁止多地点。
- 禁止多时间。
- 禁止多个独立场景。
- 禁止拼贴。
- 禁止照片墙。
- 禁止宫格。
- 禁止网格。
- 禁止左右分屏。
- 禁止上下分屏。
- 禁止 montage。
- 禁止多个独立画面。
- 禁止网页。
- 禁止新闻网站截图。
- 禁止新闻标题卡片。
- 禁止报纸版面。
- 禁止信息面板。
- 禁止数据图表。
- 禁止流程图。
- 禁止时间线。
- 禁止 UI。
- 禁止游戏界面。
- 禁止宣传海报。
- 禁止广告视觉。

【文字】

画面中绝对不能出现任何可识别文字。

禁止：

- 中文
- 英文
- 字母
- 数字
- 单词
- 标题
- 标签
- 注释
- 图例
- 坐标
- 日期
- 时间文字
- Logo
- 品牌名称
- 水印
- 签名
- 网页文字
- 新闻标题
- 报纸文字
- 书籍文字
- 文件文字
- 合同文字
- 包装文字
- 广告文字
- 衣服上的文字
- 车辆上的文字
- 建筑上的文字
- 招牌上的文字
- 商店文字
- 屏幕文字
- 手机文字
- 电脑文字
- 电视文字。

禁止随机字符。
禁止乱码。
禁止伪文字。
禁止文字装饰。

如果真实场景中存在可能出现文字的物体，
应通过以下自然方式避免文字：

- 背面
- 侧面
- 空白表面
- 浅景深
- 遮挡
- 合理裁切

绝对不要把文字替换成乱码。

【视觉风格】

- 真实人物。
- 真实动作。
- 真实建筑。
- 真实车辆。
- 真实环境。
- 真实天气。
- 真实光线。
- 真实空间关系。
- 自然透视。
- 真实材质。
- 新闻纪实摄影。
- 专业摄影。
- 自然光优先。
- 具有真实新闻现场感。

禁止：

- 游戏概念图。
- 科幻 UI。
- 人工信息布局。
- 虚假的视觉面板。

【核心原则】

图片应该让观众通过：

人物、
动作、
环境、
建筑、
车辆、
空间、
光线、

直接理解新闻主题。

不要依靠文字理解新闻。
"""


# ======================================================================
# V5.2 Prompt
# ======================================================================

def build_visual_prompt(
    item: str,
    view: str,
) -> str:

    if view == "secondary":

        camera_instruction = """
这是同一新闻事件的第二张视觉插图。

必须保持：

- 同一个新闻事件
- 同一个地点
- 同一个环境
- 同一个时间
- 同一个核心动作
- 同一个视觉中心

但是使用不同的真实摄影机位。

例如：

- 正面改成侧面
- 近景改成中景
- 正常高度改成略低机位
- 街道另一侧观察
- 后侧角度
- 稍远距离观察

注意：

这不是第二个事件。
不是第二个地点。
不是第二个时间。
不是拼贴。

仍然只是一张完整的真实新闻照片。
"""

    else:

        camera_instruction = """
请选择这个新闻最具有代表性的真实新闻摄影瞬间。

画面必须通过真实人物、真实动作、
真实环境和空间关系表达新闻主题。

只保留一个主要视觉中心。
"""

    prompt = f"""
你是一名专业新闻摄影师和新闻视觉设计师。

请根据下面的新闻内容，
生成一张专业新闻摄影风格的真实场景图片。

新闻内容：

{item}

{camera_instruction}

{VISUAL_CONTRACT}

额外要求：

- 横向 16:9。
- 单一完整场景。
- 单一地点。
- 单一时间。
- 单一瞬间。
- 单一视觉中心。
- 真实摄影机位。
- 真实透视。
- 真实光线。
- 真实材质。
- 新闻纪实摄影。
- 不要海报。
- 不要信息图。
- 不要图表。
- 不要网页。
- 不要新闻标题。
- 不要 UI。
- 不要拼贴。
- 不要分屏。
- 不要宫格。
- 不要照片墙。
- 不要 montage。
- 不要任何可识别文字。
- 不要英文伪文字。
- 不要中文伪文字。
- 不要随机字符。
- 不要乱码。
- 不要 Logo。
- 不要水印。

尤其注意：

不要把新闻内容排版到图片中。
不要把新闻标题写到图片中。
不要生成任何“新闻海报”。

这是一张真实新闻摄影照片，
不是新闻网页，
不是宣传海报，
不是信息图。

如果场景中存在招牌、屏幕、车辆、
建筑、衣服等可能带文字的物体，
请选择背面、侧面、空白表面、
浅景深或自然遮挡，
避免任何可识别文字。

绝对不要用乱码替代文字。

最终画面应该像专业新闻摄影记者
在现场使用真实相机拍摄的一张照片。
"""

    return prompt.strip()


# ======================================================================
# V5.2 Correction Prompt
# ======================================================================

def build_correction_prompt(
    base_prompt: str,
    failure_reason: str,
) -> str:

    return f"""
上一轮生成的图片没有通过视觉质量检查。

失败原因：

{failure_reason}

请重新生成。

必须严格遵守：

- 单一完整场景。
- 单一地点。
- 单一时间。
- 单一瞬间。
- 单一视觉中心。
- 真实新闻摄影。
- 真实摄影机位。
- 16:9。
- 禁止拼贴。
- 禁止宫格。
- 禁止分屏。
- 禁止 montage。
- 禁止多个独立场景。
- 禁止网页。
- 禁止新闻网站。
- 禁止新闻标题卡片。
- 禁止海报。
- 禁止信息图。
- 禁止图表。
- 禁止流程图。
- 禁止时间线。
- 禁止地图。
- 禁止 UI。

尤其必须避免：

- 英文伪文字。
- 中文伪文字。
- 随机字符。
- 乱码。
- Logo。
- 水印。
- 招牌文字。
- 屏幕文字。
- 文件文字。
- 报纸文字。
- 网页文字。

如果真实场景存在文字载体，
请使用背面、侧面、空白区域、
浅景深或自然遮挡避免文字。

绝对不要生成乱码。

重新生成一张完整、
自然、
真实、
专业新闻摄影风格的图片。

原始主题要求仍然是：

{base_prompt}
""".strip()


# ======================================================================
# AGNES 生图
# ======================================================================

def generate_image_from_agnes(
    prompt: str,
) -> Optional[bytes]:

    if not AGNES_API_KEY:

        log(
            "❌ AGNES_API_KEY / AI_API_KEY 未设置"
        )

        return None

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
        "extra_body": {
            "response_format": "url",
        },
    }

    for attempt in range(
        1,
        MAX_IMAGE_RETRIES + 1,
    ):

        log(
            f"    🎨 AGNES 生图 "
            f"{attempt}/{MAX_IMAGE_RETRIES}"
        )

        try:

            response = requests.post(
                AGNES_IMAGE_URL,
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

            items = data.get(
                "data"
            ) or []

            if not items:

                raise RuntimeError(
                    "AGNES image API data empty"
                )

            first = items[0]

            image_url = first.get(
                "url"
            )

            if image_url:

                image_response = requests.get(
                    image_url,
                    timeout=IMAGE_TIMEOUT,
                )

                image_response.raise_for_status()

                return image_response.content

            b64 = (
                first.get("b64_json")
                or first.get("base64")
            )

            if b64:

                return base64.b64decode(
                    b64
                )

            raise RuntimeError(
                "AGNES response contains "
                "neither url nor b64_json"
            )

        except Exception as exc:

            log(
                f"    ⚠️ 生图失败：{exc}"
            )

            if attempt < MAX_IMAGE_RETRIES:

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

        return (
            False,
            "empty",
        )

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
                f"unsupported format: "
                f"{image_format}",
            )

        return (
            True,
            f"{width}x{height} "
            f"{image_format}",
        )

    except Exception as exc:

        return (
            False,
            f"invalid image: {exc}",
        )


# ======================================================================
# Grid / Split 检查
# ======================================================================

def detect_grid_structure(
    image_bytes: bytes,
) -> bool:

    try:

        image = Image.open(
            io.BytesIO(image_bytes)
        ).convert("RGB")

        width, height = image.size

        if width < 2 or height < 2:

            return True

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

        def extreme_ratio(
            values,
        ):

            if not values:
                return 0

            mean = (
                sum(values)
                / len(values)
            )

            if mean <= 1:
                return 1

            extreme = sum(
                1
                for value in values
                if abs(value - mean) > 100
            )

            return (
                extreme
                / len(values)
            )

        # 非常保守。
        # 只拦截明显分格图。
        if (
            extreme_ratio(
                vertical_samples
            )
            > 0.85
        ):
            return True

        if (
            extreme_ratio(
                horizontal_samples
            )
            > 0.85
        ):
            return True

        return False

    except Exception:

        return False


# ======================================================================
# OCR
# ======================================================================

def ocr_text_quality_check(
    image_bytes: bytes,
) -> Tuple[bool, str]:

    # ==============================================================
    # V5.2 明确关闭 OCR。
    #
    # 不恢复。
    # 不使用 OCR 作为图片淘汰条件。
    # ==============================================================

    log(
        "      OCR CHECK: DISABLED"
    )

    return (
        True,
        "OCR 已关闭",
    )


# ======================================================================
# 综合视觉质量检查
# ======================================================================

def visual_quality_check(
    image_bytes: bytes,
) -> Tuple[bool, str]:

    valid, detail = (
        validate_image_bytes(
            image_bytes
        )
    )

    if not valid:

        return (
            False,
            detail,
        )

    if detect_grid_structure(
        image_bytes
    ):

        return (
            False,
            "possible grid/split layout",
        )

    ocr_valid, ocr_detail = (
        ocr_text_quality_check(
            image_bytes
        )
    )

    if not ocr_valid:

        return (
            False,
            f"OCR text quality failed: "
            f"{ocr_detail}",
        )

    return (
        True,
        detail,
    )


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
        MAX_IMAGE_RETRIES + 1,
    ):

        current_prompt = prompt

        if correction_prompt:

            current_prompt += (
                "\n\n"
                "请修正上一张图片的问题：\n"
                + correction_prompt
            )

        log(
            f"  🖼️ 生成图片 "
            f"{attempt}/{MAX_IMAGE_RETRIES}"
        )

        image_bytes = (
            generate_image_from_agnes(
                current_prompt
            )
        )

        if not image_bytes:

            correction_prompt = (
                "上一轮没有得到有效图片。"
                "请重新生成完整的单幅16:9"
                "新闻摄影风格图片。"
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
            build_correction_prompt(
                base_prompt=prompt,
                failure_reason=detail,
            )
        )

        try:

            if output_path.exists():

                output_path.unlink()

        except Exception:

            pass

        if attempt < MAX_IMAGE_RETRIES:

            time.sleep(
                2
            )

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
# 图片计划
# ======================================================================

def build_image_plan(
    news: List[str],
) -> List[Tuple[str, str, str]]:

    """
    完全采用 V5.2 图片规划。

    最新新闻：
        首图.png
        插图1.png（同一新闻，不同摄影机位）

    第二新闻：
        插图2.png

    第三新闻：
        插图3.png
    """

    if not news:

        return []

    latest = news[-1]

    plan = [
        (
            "首图.png",
            latest,
            "primary",
        ),
        (
            "插图1.png",
            latest,
            "secondary",
        ),
    ]

    if len(news) >= 2:

        plan.append(
            (
                "插图2.png",
                news[-2],
                "primary",
            )
        )

    if len(news) >= 3:

        plan.append(
            (
                "插图3.png",
                news[-3],
                "primary",
            )
        )

    return plan[:TARGET_IMAGE_COUNT]


# ======================================================================
# 删除旧图片引用
# ======================================================================

def remove_old_image_refs(
    markdown: str,
) -> str:

    # --------------------------------------------------------------
    # 删除完整“配图”章节
    # --------------------------------------------------------------

    markdown = re.sub(
        r"\n##\s*🖼️\s*配图\s*\n"
        r"(?:.*\n?)*?"
        r"(?=\n#{1,6}\s|\Z)",
        "\n",
        markdown,
        flags=re.DOTALL,
    )

    # --------------------------------------------------------------
    # 删除 Markdown 图片引用
    # --------------------------------------------------------------

    markdown = re.sub(
        r"!$begin:math:display$\[\^$end:math:display$]*\]$begin:math:text$\[\^\)\]\+$end:math:text$\s*",
        "",
        markdown,
    )

    # --------------------------------------------------------------
    # 删除 HTML img
    # --------------------------------------------------------------

    markdown = re.sub(
        r"<img[^>]*>\s*",
        "",
        markdown,
        flags=re.IGNORECASE,
    )

    return markdown


# ======================================================================
# 图片排版
# ======================================================================

def create_image_markdown(
    report_path: Path,
    image_dir: Path,
    image_paths: List[Path],
    output_path: Path,
) -> bool:

    """
    V5.2 排版算法。

    核心：

        首图放在正文顶部。

        插图1 / 插图2 / 插图3
        按正文段落间隔分布。

    日报和周报完全使用同一套排版逻辑。

    不在末尾单独建立“配图”图片区块。
    """

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

        # ==============================================================
        # 先取得正文段落
        # ==============================================================

        raw_paragraphs = re.split(
            r"\n\s*\n",
            markdown,
        )

        paragraphs = []

        for paragraph in raw_paragraphs:

            paragraph = paragraph.strip()

            if not paragraph:

                continue

            paragraphs.append(
                paragraph
            )

        if not paragraphs:

            return False

        # ==============================================================
        # V5.2：
        # 第一张图片 = 首图
        # 放在正文最顶部。
        # ==============================================================

        cover_path = image_paths[0]

        cover_ref = make_relative_image_ref(
            report_path,
            cover_path,
        )

        final_parts = []

        final_parts.append(
            f"![{cover_path.stem}]"
            f"({cover_ref})"
        )

        final_parts.append("")

        # ==============================================================
        # 插图
        # ==============================================================

        valid_insert_images = [
            path
            for path in image_paths[1:4]
            if path.exists()
        ]

        if valid_insert_images:

            interval = max(
                1,
                len(paragraphs)
                // (
                    len(valid_insert_images)
                    + 1
                ),
            )

        else:

            interval = 0

        inserted_count = 0

        # ==============================================================
        # V5.2 段落分布逻辑
        # ==============================================================

        for index, paragraph in enumerate(
            paragraphs,
            start=1,
        ):

            final_parts.append(
                paragraph
            )

            # ----------------------------------------------------------
            # 到达插图位置
            # ----------------------------------------------------------

            if (
                valid_insert_images
                and inserted_count
                < len(valid_insert_images)
                and (
                    index
                    >= (
                        interval
                        * (
                            inserted_count
                            + 1
                        )
                    )
                )
            ):

                image_path = (
                    valid_insert_images[
                        inserted_count
                    ]
                )

                image_ref = (
                    make_relative_image_ref(
                        report_path,
                        image_path,
                    )
                )

                final_parts.append("")

                final_parts.append(
                    f"![{image_path.stem}]"
                    f"({image_ref})"
                )

                final_parts.append("")

                inserted_count += 1

        # ==============================================================
        # 如果正文太短，剩余图片追加到最后。
        #
        # 仍然保持正文内排版，不创建单独配图区。
        # ==============================================================

        while (
            inserted_count
            < len(valid_insert_images)
        ):

            image_path = (
                valid_insert_images[
                    inserted_count
                ]
            )

            image_ref = (
                make_relative_image_ref(
                    report_path,
                    image_path,
                )
            )

            final_parts.append("")

            final_parts.append(
                f"![{image_path.stem}]"
                f"({image_ref})"
            )

            inserted_count += 1

        final_text = (
            "\n\n".join(
                final_parts
            ).rstrip()
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
# 单份报告图片处理
# ======================================================================

def generate_report_images(
    report_path: Path,
    image_dir: Path,
    report_type: str,
    output_markdown: Path,
    force_regenerate: bool = False,
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

    for filename, item, view in plan:

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
        # 已有图片
        # ==============================================================

        if (
            output_path.exists()
            and not force_regenerate
        ):

            if validate_existing_image(
                output_path
            ):

                generated_paths.append(
                    output_path
                )

                continue

        # ==============================================================
        # 强制重新生成
        # ==============================================================

        if force_regenerate:

            log(
                "  🔄 FORCE_REGENERATE=true"
                " → 强制重新生成"
            )

            try:

                if output_path.exists():

                    output_path.unlink()

            except Exception as exc:

                log(
                    f"  ⚠️ 删除旧图片失败："
                    f"{exc}"
                )

        # ==============================================================
        # V5.2 Prompt
        # ==============================================================

        prompt = build_visual_prompt(
            item=item,
            view=view,
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

        if IMAGE_THROTTLE > 0:

            time.sleep(
                IMAGE_THROTTLE
            )

    # ==============================================================
    # 图片数量检查
    # ==============================================================

    if (
        len(generated_paths)
        < MIN_IMAGE_COUNT
    ):

        log(
            f"❌ 图片数量不足："
            f"{len(generated_paths)}"
            f"/{MIN_IMAGE_COUNT}"
        )

        return False

    # ==============================================================
    # 带图 Markdown
    # ==============================================================

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

    date_text = target_date.isoformat()

    log("")
    log(
        f"📰 日报图片处理："
        f"{date_text}"
    )

    report_path = find_daily_report(
        target_date
    )

    if not report_path:

        log(
            f"⏭️ 日报不存在，SKIP："
            f"{date_text}"
        )

        return False

    image_dir = (
        DAILY_IMAGE_ROOT
        / date_text
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
        force_regenerate=FORCE_REGENERATE,
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
    log("=" * 70)
    log(
        f"📊 当前 ISO 周报："
        f"{year}-{week_key}"
    )
    log(
        "🔄 每次运行读取当前最新 Wxx.md"
    )
    log(
        "🔄 同一 ISO 周始终绑定同一个 Wxx"
    )
    log("=" * 70)

    report_path = find_weekly_report(
        year=year,
        week=week,
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
    # 周报图片目录
    #
    # 例如：
    #
    # 2026/W39.md
    #      ↓
    # 04_图片/周报/2026-W39/
    # ==============================================================

    image_dir = (
        WEEKLY_IMAGE_ROOT
        / f"{year}-{week_key}"
    )

    output_markdown = (
        report_path.parent
        / f"{report_path.stem}_带图.md"
    )

    # ==============================================================
    # 关键：
    #
    # 周报每次运行都强制重新生成图片。
    #
    # 原因：
    #
    # 09-21 → W39 第一次周报
    # 09-22 → W39 更新
    # 09-23 → W39 再更新
    #
    # 图片必须跟随最新 W39.md 更新。
    # ==============================================================

    return generate_report_images(
        report_path=report_path,
        image_dir=image_dir,
        report_type="周报",
        output_markdown=output_markdown,
        force_regenerate=True,
    )


# ======================================================================
# 主程序
# ======================================================================

def main() -> int:

    log("=" * 70)
    log(
        "748686 自生长知识系统"
    )
    log(
        "Knowledge Image Engine V5.4.1"
    )
    log("=" * 70)

    log(
        f"UTC 当前时间："
        f"{utc_now().isoformat()}"
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
        f"Image Size："
        f"{IMAGE_SIZE}"
    )

    log(
        f"Image Ratio："
        f"{IMAGE_RATIO}"
    )

    log(
        f"FORCE_REGENERATE："
        f"{FORCE_REGENERATE}"
    )

    log(
        "OCR：DISABLED"
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
            target.isoformat()
            for target in dates
        )
    )

    for target_date in dates:

        report_path = find_daily_report(
            target_date
        )

        if not report_path:

            log(
                f"⏭️ 日报不存在，SKIP："
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
                f"{target_date} | "
                f"{exc}"
            )

    # ==================================================================
    # 当前 ISO 周
    # ==================================================================

    current_year, current_week, current_week_key = (
        current_iso_week()
    )

    log("")
    log("=" * 70)
    log(
        "📘 当前 UTC ISO 周："
        f"{current_year}-{current_week_key}"
    )
    log(
        "📘 本次只处理当前 ISO 周"
    )
    log("=" * 70)

    weekly_report = find_weekly_report(
        year=current_year,
        week=current_week,
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
        "📊 Knowledge Image Engine V5.4.1 完成"
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
    # 没有任务
    # ==================================================================

    if actual_task_count == 0:

        log(
            "ℹ️ 当前没有任何可处理的日报/周报"
        )

        return 0

    # ==================================================================
    # 至少一个成功
    # ==================================================================

    if success_count > 0:

        log(
            "✅ 至少一个报告处理成功"
        )

        return 0

    # ==================================================================
    # 所有任务失败
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
