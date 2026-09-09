#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V5.2
======================================================================

核心目标
----------------------------------------------------------------------

为：

    05_日报
    06_周报

自动生成新闻插图。

图片输出：

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

然后生成：

    原始日报.md
    原始日报_带图.md

    原始周报.md
    原始周报_带图.md

重要原则
----------------------------------------------------------------------

1. 原始 Markdown 永远不修改
2. 只生成新的 _带图.md
3. 首图 = 最新新闻
4. 插图1 = 最新新闻的第二视角
5. 插图2 = 第二条新闻
6. 插图3 = 第三条新闻
7. 所有图片均必须是：

       无文字信息图 / 新闻插图

8. 图片必须：

       一个场景
       一个地点
       一个时间
       一个瞬间
       一个摄影机位
       一个视觉中心

9. 严禁：

       汉字
       英文
       数字
       标题
       标签
       注释
       Logo
       水印
       标牌文字
       屏幕文字
       报纸文字
       书中文字
       文件文字
       包装文字
       衣服文字
       汽车文字

10. 严禁：

       拼图
       网格
       分屏
       多画面
       蒙太奇
       信息面板
       新闻版面
       海报
       图表
       流程图
       时间轴
       地图
       数据可视化
       用户界面

11. 如果 OCR 检测失败：

       删除图片
       重新生成
       最多 5 次

======================================================================
"""

import io
import os
import re
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# 1. Optional dependencies
# ======================================================================

try:
    from PIL import Image, ImageFilter, ImageOps
except ImportError:
    Image = None
    ImageFilter = None
    ImageOps = None


try:
    import pytesseract
except ImportError:
    pytesseract = None


# ======================================================================
# 2. AGNES configuration
# ======================================================================

AGNES_API_KEY = os.getenv("AGNES_API_KEY", "").strip()

AGNES_BASE_URL = (
    os.getenv(
        "AGNES_BASE_URL",
        "https://api.agnes-ai.cn/v1"
    ).rstrip("/")
)

AGNES_IMAGE_URL = (
    f"{AGNES_BASE_URL}/images/generations"
)

AGNES_IMAGE_MODEL = (
    os.getenv(
        "AGNES_IMAGE_MODEL",
        "agnes-image-2.5-flash"
    ).strip()
)

IMAGE_SIZE = (
    os.getenv(
        "IMAGE_SIZE",
        "2K"
    ).strip()
)

IMAGE_RATIO = (
    os.getenv(
        "IMAGE_RATIO",
        "16:9"
    ).strip()
)

IMAGE_TIMEOUT = int(
    os.getenv(
        "IMAGE_TIMEOUT",
        "180"
    )
)

FORCE_REGENERATE = (
    os.getenv(
        "FORCE_REGENERATE",
        "false"
    ).lower()
    in {"1", "true", "yes", "y"}
)

MAX_IMAGE_RETRIES = int(
    os.getenv(
        "MAX_IMAGE_RETRIES",
        "5"
    )
)

MIN_IMAGE_COUNT = 3
TARGET_IMAGE_COUNT = 4


IMAGE_NAMES = (
    "首图.png",
    "插图1.png",
    "插图2.png",
    "插图3.png",
)


# ======================================================================
# 3. Path configuration
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent

SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = (
    SYSTEM_ROOT / "05_日报"
)

WEEKLY_ROOT = (
    SYSTEM_ROOT / "06_周报"
)

IMAGE_ROOT = (
    SYSTEM_ROOT / "04_图片"
)

DAILY_IMAGE_ROOT = (
    IMAGE_ROOT / "日报"
)

WEEKLY_IMAGE_ROOT = (
    IMAGE_ROOT / "周报"
)


# ======================================================================
# 4. Global visual contract
# ======================================================================

VISUAL_CONTRACT = """
【最终视觉类型】

这是一张“无文字信息图 / 新闻插图”。

它不是新闻海报。
它不是信息图表。
它不是数据可视化。
它不是新闻网页截图。
它不是报纸版面。
它不是宣传海报。

它应该看起来像：

一名专业新闻摄影记者，
在真实世界中，
亲自拍摄的一张真实新闻现场照片。

【最重要的画面结构】

整张图片只能有：

一个完整场景。
一个地点。
一个时间。
一个瞬间。
一个摄影机位。
一个视觉中心。
一个连续的现实空间。

必须让所有视觉元素自然存在于同一个真实场景中。

禁止把多个新闻事件放在同一张图片中。

禁止把多个地点放在同一张图片中。

禁止把多个时间阶段放在同一张图片中。

禁止制造多个独立的小画面。

禁止拼图。

禁止网格。

禁止分屏。

禁止多窗口。

禁止蒙太奇。

禁止多个独立场景并列。

【绝对禁止文字】

图片中不得出现任何可识别文字。

绝对不要出现：

汉字。
中文。
英文。
英文字母。
数字。
单词。
句子。
标题。
副标题。
标签。
说明文字。
注释。
图例。
坐标。
数据。
日期文字。
时间文字。
Logo。
品牌名称。
水印。
签名。
网页文字。
新闻标题。
报纸文字。
书中文字。
文件文字。
合同文字。
包装文字。
广告文字。
衣服上的文字。
帽子上的文字。
车辆上的文字。
建筑物上的文字。
路牌文字。
交通标志文字。
商店招牌文字。
屏幕文字。
电脑文字。
手机文字。
电视字幕。
投影文字。

不要生成任何随机字符。

不要生成任何乱码。

不要生成任何类似文字的伪文字。

不要生成看起来像文字的装饰符号。

【含文字物体的处理】

如果真实新闻场景中自然存在：

路牌。
广告牌。
电脑屏幕。
手机屏幕。
电视。
报纸。
书籍。
文件。
包装。
商店招牌。
车辆标识。
制服。
证件。
墙面标语。

必须主动避免显示文字。

可以：

从背面拍摄。
从侧面拍摄。
让文字区域朝向摄影机之外。
让表面保持空白。
使用浅景深让背景自然虚化。
使用合理构图遮挡文字区域。
使用没有文字的普通物体代替。

但是不能制造乱码来代替文字。

【真实世界表现】

使用真实新闻摄影的视觉语言。

人物必须自然。
动作必须自然。
建筑必须真实。
车辆必须真实。
环境必须真实。
光线必须自然。
天气必须自然。
空间关系必须合理。

通过：

人物。
动作。
物体。
建筑。
车辆。
环境。
天气。
光线。
空间关系。

来表达新闻事件。

不要通过文字表达新闻事件。

【摄影风格】

专业新闻摄影。
纪实摄影。
真实现场摄影。
自然光。
真实空间。
真实比例。
自然景深。
合理透视。
真实材质。
自然人物姿态。

不要过度艺术化。

不要海报化。

不要宣传画风。

不要游戏概念图风格。

不要科幻界面。

不要信息面板。

不要人工排版。

【无文字信息图定义】

这里的“无文字信息图”只表示：

用一张完整、清晰、具有新闻叙事能力的真实场景图片，
让观众不需要阅读文字，
也能理解新闻事件的大致内容。

它绝对不是：

传统信息图。
图表。
统计图。
流程图。
关系图。
时间轴。
地图。
新闻网页。
新闻海报。
数据面板。

【最终要求】

只生成一张完整的新闻现场视觉。

一个场景。

一个地点。

一个时间。

一个瞬间。

一个摄影机位。

一个视觉中心。

零文字。

零乱码。

零Logo。

零水印。

零拼图。

零分屏。

零网格。

零信息面板。

零新闻版面。
"""


# ======================================================================
# 5. Utility
# ======================================================================

def log(message=""):
    print(message, flush=True)


def utc_now():
    return datetime.now(timezone.utc)


def utc_today():
    return utc_now().date()


def sha1_text(text):
    return hashlib.sha1(
        text.encode("utf-8")
    ).hexdigest()


def safe_text(value):
    if value is None:
        return ""

    return str(value).strip()


# ======================================================================
# 6. Date handling
# ======================================================================

def target_dates():
    """
    处理：

        前天
        昨天
        今天

    使用 UTC。
    """

    today = utc_today()

    return [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]


# ======================================================================
# 7. Report discovery
# ======================================================================

def find_daily_report(target_date):
    date_text = target_date.isoformat()

    candidates = [
        DAILY_ROOT / f"{date_text}.md",
        DAILY_ROOT / f"{date_text}日报.md",
        DAILY_ROOT / date_text / f"{date_text}.md",
    ]

    for path in candidates:
        if path.exists() and path.is_file():
            return path

    if DAILY_ROOT.exists():
        for path in DAILY_ROOT.rglob("*.md"):
            name = path.name

            if date_text in name:
                return path

    return None


def find_weekly_report(week_key):
    candidates = [
        WEEKLY_ROOT / f"{week_key}.md",
        WEEKLY_ROOT / f"{week_key}周报.md",
        WEEKLY_ROOT / week_key / f"{week_key}.md",
    ]

    for path in candidates:
        if path.exists() and path.is_file():
            return path

    if WEEKLY_ROOT.exists():
        for path in WEEKLY_ROOT.rglob("*.md"):
            if week_key in path.name:
                return path

    return None


# ======================================================================
# 8. Markdown cleanup
# ======================================================================

NOISE_HEADINGS = {
    "日报",
    "周报",
    "今日总结",
    "本周总结",
    "核心发现",
    "核心观点",
    "建议",
    "风险",
    "数据源",
    "参考资料",
    "参考来源",
    "总结",
    "结论",
}


def normalize_line(line):
    line = re.sub(
        r"\s+",
        " ",
        line
    ).strip()

    return line


def is_noise_heading(text):
    cleaned = re.sub(
        r"^[#\-\*\d\.\、\s]+",
        "",
        text
    ).strip()

    return cleaned in NOISE_HEADINGS


# ======================================================================
# 9. Extract news items
# ======================================================================

def extract_news_items(markdown):
    """
    从日报 / 周报中提取新闻内容。

    这里不要求固定 Markdown 格式，
    尽量兼容不同版本日报。
    """

    lines = markdown.splitlines()

    items = []

    current = []

    def flush():
        nonlocal current

        if not current:
            return

        text = "\n".join(current).strip()

        if len(text) >= 40:
            items.append(text)

        current = []

    for raw in lines:

        line = normalize_line(raw)

        if not line:
            continue

        # 跳过图片
        if re.match(
            r"!\[.*?\]\(.*?\)",
            line
        ):
            continue

        # 跳过 YAML
        if line.startswith("---"):
            continue

        # 明显标题
        if line.startswith("#"):
            flush()

            if is_noise_heading(line):
                continue

            current.append(line)
            continue

        # 编号新闻
        if re.match(
            r"^\d+[\.\、\)]\s+",
            line
        ):
            flush()
            current.append(line)
            continue

        # 项目符号新闻
        if re.match(
            r"^[-*•]\s+",
            line
        ):
            flush()
            current.append(line)
            continue

        current.append(line)

    flush()

    # 如果结构化提取不足，进行段落兜底
    if len(items) < 3:

        paragraphs = re.split(
            r"\n\s*\n",
            markdown
        )

        fallback = []

        for paragraph in paragraphs:

            text = normalize_line(
                paragraph
            )

            if len(text) < 60:
                continue

            if is_noise_heading(text):
                continue

            if text not in fallback:
                fallback.append(text)

        for text in fallback:

            if text not in items:
                items.append(text)

            if len(items) >= 20:
                break

    return items


# ======================================================================
# 10. Extract title/body semantic context
# ======================================================================

def extract_semantic_title_body(item):
    """
    新闻文本只作为语义参考。

    绝对不要求图片生成模型把文字本身画出来。
    """

    text = safe_text(item)

    lines = [
        normalize_line(x)
        for x in text.splitlines()
        if normalize_line(x)
    ]

    if not lines:
        return "", ""

    title = lines[0]

    body = " ".join(lines[1:])

    if not body:
        body = title

    # 防止 prompt 无限增长
    body = body[:3500]

    return title, body


# ======================================================================
# 11. Build visual prompt
# ======================================================================

def build_visual_prompt(item, view="primary"):
    """
    完全中文提示词。

    不再使用英文视觉提示词。
    """

    title, body = (
        extract_semantic_title_body(item)
    )

    if view == "secondary":

        view_instruction = """
【第二视角】

这是同一条新闻事件的第二张图片。

必须表现同一个新闻事件。

必须保持：

同一个地点。
同一个现实环境。
同一个时间段。
同一个核心事件。
同一个视觉中心。

但是摄影机位置必须发生真实变化。

例如：

从正面改为侧面。
从较远位置改为中距离。
从低机位改为正常视角。
从另一侧街道观察。
从人物侧后方观察。
从现场稍远的位置观察。

这是“换一个摄影机位”，
不是重新创造第二个新闻事件。

绝对不能加入第二个地点。

绝对不能加入第二个事件。

绝对不能把两个视角拼在一张图片里。

仍然只能是一张完整的新闻现场照片。
"""

    else:

        view_instruction = """
【首要视角】

选择这条新闻最具有代表性的一个真实瞬间。

只选择一个最重要的视觉中心。

让观众通过真实的人物、动作、环境、建筑、车辆和空间关系，
直接理解这条新闻的大致内容。

不要试图把新闻全文全部表现出来。

只表现一个最有新闻价值的现场瞬间。
"""

    prompt = f"""
你现在是一名专业新闻摄影记者。

请根据下面提供的新闻内容，
创作一张真实、自然、具有新闻现场感的：

“无文字信息图 / 新闻插图”。

【新闻语义参考】

新闻标题：
{title}

新闻正文：
{body}

注意：

上面的文字只用于帮助你理解新闻事件。

绝对不要把这些文字画进图片。

不要复制文字。

不要翻译文字。

不要排版文字。

不要生成标题。

不要生成说明。

不要生成标签。

不要生成任何文字。

{view_instruction}

【画面构成】

整张图片必须只有：

一个完整场景。
一个地点。
一个时间。
一个瞬间。
一个摄影机位。
一个视觉中心。

这是一个连续的真实空间。

所有人物、物体、建筑、车辆和环境，
都必须自然存在于这个同一个空间中。

不要拼接多个画面。

不要制造多个独立场景。

不要使用分屏。

不要使用网格。

不要使用拼图。

不要使用蒙太奇。

【新闻表达方式】

通过真实世界中的：

人物。
动作。
建筑。
车辆。
环境。
天气。
光线。
空间关系。

来表达新闻事件。

不要通过文字表达新闻事件。

不要通过信息面板表达新闻事件。

不要通过图表表达新闻事件。

不要通过新闻版面表达新闻事件。

【绝对无文字】

图片中必须完全没有可识别文字。

禁止：

汉字。
中文。
英文。
英文字母。
数字。
单词。
标题。
标签。
说明。
注释。
Logo。
水印。
品牌名称。
广告文字。
路牌文字。
商店招牌。
建筑文字。
车辆文字。
制服文字。
帽子文字。
手机屏幕文字。
电脑屏幕文字。
电视字幕。
报纸文字。
书中文字。
文件文字。
包装文字。

不要出现随机字符。

不要出现乱码。

不要出现伪文字。

不要出现类似文字的装饰。

如果现实场景中存在本来可能带文字的物体，
必须让文字区域不可见、朝向摄影机之外、保持空白，
或者通过自然景深和构图避免文字出现。

【摄影要求】

真实新闻摄影。

真实人物比例。

真实空间透视。

自然光线。

自然阴影。

真实材质。

真实环境。

自然人物动作。

专业摄影构图。

具有新闻纪录片感觉。

不要海报感。

不要宣传画。

不要游戏概念图。

不要科幻界面。

不要人工排版。

不要数据可视化。

不要信息面板。

不要网页界面。

不要新闻网页。

不要报纸版面。

不要流程图。

不要时间轴。

不要地图。

【最终结果】

只生成一张完整的真实新闻现场图片。

一个场景。

一个地点。

一个时间。

一个瞬间。

一个摄影机位。

一个视觉中心。

零文字。

零乱码。

零Logo。

零水印。

零拼图。

零分屏。

零网格。

零信息面板。

零新闻版面。

{VISUAL_CONTRACT}
"""

    return prompt.strip()


# ======================================================================
# 12. Chinese regeneration correction prompt
# ======================================================================

def build_correction_prompt(base_prompt, failure_reason):
    """
    图片第一次生成失败后的中文修正提示词。
    """

    correction = f"""
【重新生成图片】

上一张图片没有通过视觉质量检查。

失败原因：

{failure_reason}

现在必须重新生成。

这一次必须更加严格地遵守下面的要求：

1. 只允许一个完整真实场景。

2. 只允许一个地点。

3. 只允许一个时间。

4. 只允许一个瞬间。

5. 只允许一个摄影机位。

6. 只允许一个视觉中心。

7. 所有元素必须存在于同一个连续的现实空间。

8. 绝对不能出现：

汉字。
中文。
英文。
英文字母。
数字。
单词。
标题。
标签。
说明文字。
注释。
Logo。
水印。
品牌名称。
路牌文字。
广告文字。
商店招牌。
建筑文字。
车辆文字。
制服文字。
屏幕文字。
电视字幕。
手机文字。
电脑文字。
报纸文字。
书中文字。
文件文字。
包装文字。

9. 不允许出现随机字符。

10. 不允许出现乱码。

11. 不允许出现任何看起来像文字的伪文字。

12. 不允许出现：

拼图。
网格。
分屏。
多画面。
蒙太奇。
多个独立场景。
新闻网页。
新闻版面。
海报。
信息面板。
数据图表。
流程图。
时间轴。
地图。
用户界面。

13. 如果场景中自然存在可能带文字的物体：

让文字面朝向摄影机之外，
或者使用自然角度避开，
或者使用自然景深虚化，
或者使用没有文字的空白表面。

绝对不要用乱码替代文字。

14. 最终必须像：

专业新闻摄影记者在真实现场拍摄的一张照片。

不是海报。

不是信息图表。

不是新闻网页。

不是宣传图片。

不是人工设计版面。

请重新生成一张：

“无文字信息图 / 新闻插图”。

只保留一个真实新闻场景。
"""

    return (
        base_prompt
        + "\n\n"
        + correction
    )


# ======================================================================
# 13. Call AGNES image generation API
# ======================================================================

def generate_image_from_agnes(prompt):
    if not AGNES_API_KEY:
        raise RuntimeError(
            "缺少环境变量 AGNES_API_KEY"
        )

    payload = {
        "model": AGNES_IMAGE_MODEL,
        "prompt": prompt,
        "size": IMAGE_SIZE,
        "aspect_ratio": IMAGE_RATIO,
        "extra_body": {
            "response_format": "url"
        },
    }

    body = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    request = Request(
        AGNES_IMAGE_URL,
        data=body,
        method="POST",
        headers={
            "Authorization":
                f"Bearer {AGNES_API_KEY}",
            "Content-Type":
                "application/json",
        },
    )

    try:

        with urlopen(
            request,
            timeout=IMAGE_TIMEOUT
        ) as response:

            raw = response.read()

    except HTTPError as exc:

        error_body = ""

        try:
            error_body = (
                exc.read()
                .decode(
                    "utf-8",
                    errors="replace"
                )
            )
        except Exception:
            pass

        raise RuntimeError(
            f"AGNES HTTP {exc.code}: "
            f"{error_body[:1000]}"
        )

    except URLError as exc:

        raise RuntimeError(
            f"AGNES 网络错误: {exc}"
        )

    except Exception as exc:

        raise RuntimeError(
            f"AGNES 请求失败: {exc}"
        )

    try:
        result = json.loads(
            raw.decode(
                "utf-8",
                errors="replace"
            )
        )

    except Exception as exc:

        raise RuntimeError(
            f"AGNES 返回 JSON 解析失败: {exc}"
        )

    # --------------------------------------------------------------
    # 兼容常见响应结构
    # --------------------------------------------------------------

    image_url = None

    if isinstance(result, dict):

        data = result.get("data")

        if isinstance(data, list) and data:

            first = data[0]

            if isinstance(first, dict):

                image_url = (
                    first.get("url")
                    or first.get("image_url")
                )

        if not image_url:

            image_url = (
                result.get("url")
                or result.get("image_url")
            )

    if not image_url:

        raise RuntimeError(
            "AGNES 返回中没有找到图片 URL"
        )

    return download_image(
        image_url
    )


# ======================================================================
# 14. Download generated image
# ======================================================================

def download_image(url):
    request = Request(
        url,
        method="GET",
        headers={
            "User-Agent":
                "Mozilla/5.0"
        },
    )

    try:

        with urlopen(
            request,
            timeout=IMAGE_TIMEOUT
        ) as response:

            return response.read()

    except Exception as exc:

        raise RuntimeError(
            f"图片下载失败: {exc}"
        )


# ======================================================================
# 15. Basic image validation
# ======================================================================

def validate_image_bytes(data):
    if not data:
        return False, "图片为空"

    if Image is None:
        return True, "Pillow 未安装，跳过基础图片检查"

    try:

        image = Image.open(
            io.BytesIO(data)
        )

        width, height = image.size

        if width < 1000:
            return False, (
                f"图片宽度过小: {width}"
            )

        if height < 500:
            return False, (
                f"图片高度过小: {height}"
            )

        image_format = (
            image.format or ""
        ).upper()

        if image_format not in {
            "PNG",
            "JPEG",
            "WEBP",
        }:

            return False, (
                f"不支持的图片格式: "
                f"{image_format}"
            )

        return True, (
            f"图片基础检查通过: "
            f"{width}x{height} "
            f"{image_format}"
        )

    except Exception as exc:

        return False, (
            f"图片解析失败: {exc}"
        )


# ======================================================================
# 16. Grid / collage detection
# ======================================================================

def detect_grid_structure(data):
    """
    粗略检测：

        拼图
        网格
        分屏
        多画面

    不追求完美计算，
    只用于拦截明显的人工排版图片。
    """

    if Image is None:
        return False, "Pillow 不可用"

    try:

        image = Image.open(
            io.BytesIO(data)
        ).convert("L")

        # 缩小，减少计算量
        image.thumbnail(
            (1200, 1200)
        )

        edges = image.filter(
            ImageFilter.FIND_EDGES
        )

        width, height = edges.size

        pixels = edges.load()

        # ----------------------------------------------------------
        # 检查内部垂直线
        # ----------------------------------------------------------

        vertical_candidates = []

        for x in range(
            int(width * 0.15),
            int(width * 0.85)
        ):

            strong = 0

            for y in range(
                int(height * 0.10),
                int(height * 0.90)
            ):

                if pixels[x, y] > 220:
                    strong += 1

            ratio = (
                strong /
                max(
                    1,
                    int(height * 0.80)
                )
            )

            if ratio > 0.55:
                vertical_candidates.append(
                    x
                )

        # ----------------------------------------------------------
        # 检查内部水平线
        # ----------------------------------------------------------

        horizontal_candidates = []

        for y in range(
            int(height * 0.15),
            int(height * 0.85)
        ):

            strong = 0

            for x in range(
                int(width * 0.10),
                int(width * 0.90)
            ):

                if pixels[x, y] > 220:
                    strong += 1

            ratio = (
                strong /
                max(
                    1,
                    int(width * 0.80)
                )
            )

            if ratio > 0.55:
                horizontal_candidates.append(
                    y
                )

        if (
            len(vertical_candidates) >= 2
            or len(horizontal_candidates) >= 2
        ):

            return True, (
                "检测到疑似网格/分屏结构"
            )

        return False, "未检测到明显网格"

    except Exception as exc:

        return False, (
            f"网格检测异常: {exc}"
        )


# ======================================================================
# 17. OCR helpers
# ======================================================================

def ocr_text_quality_check(data):
    """
    OCR 临时关闭。

    原因：
    当前 Tesseract 对真实新闻照片中的建筑线条、
    人物轮廓、阴影、纹理等容易产生 OCR 误识别，
    导致正常图片被错误判定为包含中文或英文文字。

    当前版本：

        不执行 OCR
        不调用 pytesseract
        不进行文字识别
        不因为 OCR 拒绝图片

    保留这个函数，是为了不改变后面的视觉 QA 调用结构。
    """

    log(
        "      OCR CHECK: DISABLED"
    )

    return True, (
        "OCR 已关闭"
    )
# ======================================================================
# 18. Full visual QA
# ======================================================================

def visual_quality_check(data):
    """
    综合：

        图片基础检查
        网格检测
        OCR 检测
    """

    ok, reason = (
        validate_image_bytes(data)
    )

    if not ok:
        return False, reason

    grid, grid_reason = (
        detect_grid_structure(data)
    )

    if grid:
        return False, grid_reason

    ocr_ok, ocr_reason = (
        ocr_text_quality_check(data)
    )

    if not ocr_ok:
        return False, ocr_reason

    return True, (
        "视觉质量检查通过"
    )


# ======================================================================
# 19. Save image
# ======================================================================

def save_image_png(data, destination):
    destination = Path(
        destination
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if Image is None:

        destination.write_bytes(
            data
        )

        return

    try:

        image = Image.open(
            io.BytesIO(data)
        )

        image = image.convert(
            "RGB"
        )

        temp_path = destination.with_suffix(
            ".tmp.png"
        )

        image.save(
            temp_path,
            format="PNG",
            optimize=True
        )

        temp_path.replace(
            destination
        )

    except Exception:

        # Pillow 保存失败时，
        # 保留原始数据作为兜底
        destination.write_bytes(
            data
        )


# ======================================================================
# 20. Generate one validated image
# ======================================================================

def generate_validated_image(
    item,
    destination,
    view="primary",
):
    destination = Path(
        destination
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    base_prompt = build_visual_prompt(
        item,
        view=view
    )

    prompt = base_prompt

    for attempt in range(
        1,
        MAX_IMAGE_RETRIES + 1
    ):

        log(
            f"      图片生成尝试 "
            f"{attempt}/{MAX_IMAGE_RETRIES}"
        )

        try:

            data = generate_image_from_agnes(
                prompt
            )

            ok, reason = (
                visual_quality_check(
                    data
                )
            )

            if ok:

                save_image_png(
                    data,
                    destination
                )

                log(
                    f"      ✓ 图片通过视觉检查"
                )

                log(
                    f"      ✓ 已保存: "
                    f"{destination}"
                )

                return True

            log(
                f"      ✗ 图片未通过检查: "
                f"{reason}"
            )

            # 删除失败图片
            if destination.exists():

                try:
                    destination.unlink()
                except Exception:
                    pass

            # ------------------------------------------------------
            # 中文修正提示词
            # ------------------------------------------------------

            prompt = build_correction_prompt(
                base_prompt,
                reason
            )

            if attempt < MAX_IMAGE_RETRIES:

                time.sleep(2)

        except Exception as exc:

            log(
                f"      ✗ 图片生成失败: {exc}"
            )

            if destination.exists():

                try:
                    destination.unlink()
                except Exception:
                    pass

            prompt = build_correction_prompt(
                base_prompt,
                str(exc)
            )

            if attempt < MAX_IMAGE_RETRIES:

                time.sleep(2)

    log(
        f"      ✗ {MAX_IMAGE_RETRIES} 次尝试全部失败"
    )

    return False


# ======================================================================
# 21. Existing image validation
# ======================================================================

def validate_existing_image(path):
    path = Path(path)

    if not path.exists():
        return False

    try:

        data = path.read_bytes()

        ok, reason = (
            visual_quality_check(
                data
            )
        )

        if ok:

            log(
                f"      ✓ 已存在图片通过检查: "
                f"{path.name}"
            )

            return True

        log(
            f"      ✗ 已存在图片未通过检查: "
            f"{path.name}"
        )

        log(
            f"        原因: {reason}"
        )

        try:
            path.unlink()
        except Exception:
            pass

        return False

    except Exception as exc:

        log(
            f"      ✗ 已存在图片检查失败: "
            f"{exc}"
        )

        try:
            path.unlink()
        except Exception:
            pass

        return False


# ======================================================================
# 22. Image plan
# ======================================================================

def build_image_plan(news):
    """
    图片语义规划：

        首图   = 最新新闻
        插图1  = 最新新闻第二视角
        插图2  = 第二条新闻
        插图3  = 第三条新闻
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

    return plan


# ======================================================================
# 23. Generate images for report
# ======================================================================

def generate_report_images(
    report_path,
    image_dir,
):
    report_path = Path(
        report_path
    )

    image_dir = Path(
        image_dir
    )

    log("")
    log(
        "============================================================"
    )
    log(
        f"IMAGE GENERATION: "
        f"{report_path.name}"
    )
    log(
        "============================================================"
    )

    try:

        markdown = report_path.read_text(
            encoding="utf-8"
        )

    except Exception as exc:

        log(
            f"      ✗ Markdown 读取失败: {exc}"
        )

        return False

    news = extract_news_items(
        markdown
    )

    log(
        f"      NEWS ITEMS: {len(news)}"
    )

    if not news:

        log(
            "      ✗ 没有提取到有效新闻"
        )

        return False

    plan = build_image_plan(
        news
    )

    log(
        f"      IMAGE PLAN: {len(plan)}"
    )

    valid_count = 0

    for filename, item, view in plan:

        destination = (
            image_dir / filename
        )

        log("")
        log(
            f"      ------------------------------------------------"
        )
        log(
            f"      {filename}"
        )
        log(
            f"      VIEW: {view}"
        )
        log(
            f"      ------------------------------------------------"
        )

        if (
            destination.exists()
            and not FORCE_REGENERATE
        ):

            if validate_existing_image(
                destination
            ):

                valid_count += 1
                continue

        success = (
            generate_validated_image(
                item=item,
                destination=destination,
                view=view,
            )
        )

        if success:
            valid_count += 1

    log("")
    log(
        f"      VALID IMAGE COUNT: "
        f"{valid_count}"
    )

    if valid_count < MIN_IMAGE_COUNT:

        log(
            f"      ✗ 图片数量不足"
        )

        return False

    return True


# ======================================================================
# 24. Create _带图.md
# ======================================================================

def create_image_markdown(
    report_path,
    image_dir,
):
    """
    不修改原始 Markdown。

    只创建：

        xxx_带图.md
    """

    report_path = Path(
        report_path
    )

    image_dir = Path(
        image_dir
    )

    original = report_path.read_text(
        encoding="utf-8"
    )

    output_path = (
        report_path.parent
        /
        f"{report_path.stem}_带图.md"
    )

    # --------------------------------------------------------------
    # 删除旧图片引用，避免重复
    # --------------------------------------------------------------

    clean = re.sub(
        r"!\[[^\]]*\]\([^)]+\)\s*",
        "",
        original
    )

    clean = clean.strip()

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover = (
        image_dir / "首图.png"
    )

    sections = []

    if cover.exists():

        sections.append(
            f"![首图](../04_图片/{image_dir.name}/首图.png)"
        )

    # --------------------------------------------------------------
    # 插图
    # --------------------------------------------------------------

    body = clean

    # 按段落分割
    paragraphs = [
        p.strip()
        for p in re.split(
            r"\n\s*\n",
            body
        )
        if p.strip()
    ]

    insert_images = [
        image_dir / "插图1.png",
        image_dir / "插图2.png",
        image_dir / "插图3.png",
    ]

    valid_insert_images = [
        p for p in insert_images
        if p.exists()
    ]

    if paragraphs and valid_insert_images:

        interval = max(
            1,
            len(paragraphs)
            //
            (
                len(valid_insert_images)
                + 1
            )
        )

        result = []

        image_index = 0

        for index, paragraph in enumerate(
            paragraphs,
            start=1
        ):

            result.append(
                paragraph
            )

            if (
                image_index
                <
                len(valid_insert_images)
                and
                index
                % interval
                == 0
            ):

                image_path = (
                    valid_insert_images[
                        image_index
                    ]
                )

                relative_name = (
                    image_path.name
                )

                result.append(
                    f"\n![新闻插图]"
                    f"(../04_图片/"
                    f"{image_dir.name}/"
                    f"{relative_name})"
                )

                image_index += 1

        body = "\n\n".join(
            result
        )

    # --------------------------------------------------------------
    # 最终 Markdown
    # --------------------------------------------------------------

    if sections:

        final_markdown = (
            "\n\n".join(
                sections
            )
            + "\n\n"
            + body
            + "\n"
        )

    else:

        final_markdown = (
            body
            + "\n"
        )

    output_path.write_text(
        final_markdown,
        encoding="utf-8"
    )

    log(
        f"      ✓ 已生成: "
        f"{output_path}"
    )

    return output_path


# ======================================================================
# 25. Daily report
# ======================================================================

def process_daily_report(target_date):
    date_text = target_date.isoformat()

    log("")
    log(
        "######################################################################"
    )
    log(
        f"DAILY IMAGE: {date_text}"
    )
    log(
        "######################################################################"
    )

    report_path = find_daily_report(
        target_date
    )

    if report_path is None:

        log(
            f"      ✗ 未找到日报: "
            f"{date_text}"
        )

        return False

    image_dir = (
        DAILY_IMAGE_ROOT
        /
        date_text
    )

    success = (
        generate_report_images(
            report_path,
            image_dir
        )
    )

    if not success:
        return False

    create_image_markdown(
        report_path,
        image_dir
    )

    return True


# ======================================================================
# 26. ISO week
# ======================================================================

def iso_week_key(target_date):
    year, week, _ = (
        target_date.isocalendar()
    )

    return f"{year}-W{week:02d}"


# ======================================================================
# 27. Weekly report
# ======================================================================

def process_weekly_report(
    week_key
):
    log("")
    log(
        "######################################################################"
    )
    log(
        f"WEEKLY IMAGE: {week_key}"
    )
    log(
        "######################################################################"
    )

    report_path = find_weekly_report(
        week_key
    )

    if report_path is None:

        log(
            f"      ✗ 未找到周报: "
            f"{week_key}"
        )

        return False

    image_dir = (
        WEEKLY_IMAGE_ROOT
        /
        week_key
    )

    success = (
        generate_report_images(
            report_path,
            image_dir
        )
    )

    if not success:
        return False

    create_image_markdown(
        report_path,
        image_dir
    )

    return True

# ======================================================================
# 28. Main
# ======================================================================

def main():

    log("")
    log(
        "======================================================================"
    )
    log(
        "748686 KNOWLEDGE IMAGE ENGINE V5.2"
    )
    log(
        "======================================================================"
    )

    log(
        f"UTC TODAY: {utc_today()}"
    )

    log(
        f"IMAGE MODEL: {AGNES_IMAGE_MODEL}"
    )

    log(
        f"IMAGE SIZE: {IMAGE_SIZE}"
    )

    log(
        f"IMAGE RATIO: {IMAGE_RATIO}"
    )

    log(
        f"FORCE_REGENERATE: "
        f"{FORCE_REGENERATE}"
    )

    log(
        "VISUAL MODE: "
        "无文字信息图 / 新闻插图"
    )

    log(
        "LANGUAGE: 中文提示词"
    )

    log(
        "OCR: DISABLED"
    )

    # --------------------------------------------------------------
    # API key
    # --------------------------------------------------------------

    if not AGNES_API_KEY:

        log("")
        log(
            "✗ ERROR: "
            "环境变量 AGNES_API_KEY 未设置"
        )

        return 1

    # --------------------------------------------------------------
    # Create directories
    # --------------------------------------------------------------

    DAILY_IMAGE_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    WEEKLY_IMAGE_ROOT.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------------
    # Processing statistics
    # --------------------------------------------------------------

    daily_success_count = 0
    daily_missing_count = 0
    daily_failed_count = 0

    weekly_success_count = 0
    weekly_missing_count = 0
    weekly_failed_count = 0

    # --------------------------------------------------------------
    # Daily
    #
    # 非常重要：
    #
    # 每一天独立处理。
    #
    # 第一天成功以后已经立即落盘，
    # 第二天即使不存在或者失败，
    # 也绝对不能影响第一天。
    # --------------------------------------------------------------

    dates = target_dates()

    weekly_keys = []

    for target_date in dates:

        date_text = target_date.isoformat()

        log("")
        log(
            "######################################################################"
        )
        log(
            f"DAILY IMAGE: {date_text}"
        )
        log(
            "######################################################################"
        )

        report_path = find_daily_report(
            target_date
        )

        # ----------------------------------------------------------
        # 日报不存在
        #
        # 不是错误。
        # 只是跳过。
        # ----------------------------------------------------------

        if report_path is None:

            log(
                f"      ⏭ 未找到日报，跳过: "
                f"{date_text}"
            )

            daily_missing_count += 1

        else:

            image_dir = (
                DAILY_IMAGE_ROOT
                /
                date_text
            )

            try:

                success = (
                    generate_report_images(
                        report_path,
                        image_dir
                    )
                )

                if success:

                    create_image_markdown(
                        report_path,
                        image_dir
                    )

                    daily_success_count += 1

                    log(
                        f"      ✓ 日报处理完成: "
                        f"{date_text}"
                    )

                else:

                    daily_failed_count += 1

                    log(
                        f"      ✗ 日报图片处理失败，"
                        f"继续处理下一天: "
                        f"{date_text}"
                    )

            except Exception as exc:

                daily_failed_count += 1

                log(
                    f"      ✗ 日报处理异常: "
                    f"{exc}"
                )

                log(
                    "      ⏭ 不终止程序，继续处理下一天"
                )

        # ----------------------------------------------------------
        # 收集对应 ISO 周
        # ----------------------------------------------------------

        week_key = iso_week_key(
            target_date
        )

        if week_key not in weekly_keys:

            weekly_keys.append(
                week_key
            )

    # --------------------------------------------------------------
    # Weekly
    #
    # 每一个周报同样独立处理。
    # --------------------------------------------------------------

    for week_key in weekly_keys:

        log("")
        log(
            "######################################################################"
        )
        log(
            f"WEEKLY IMAGE: {week_key}"
        )
        log(
            "######################################################################"
        )

        report_path = find_weekly_report(
            week_key
        )

        # ----------------------------------------------------------
        # 周报不存在
        # ----------------------------------------------------------

        if report_path is None:

            log(
                f"      ⏭ 未找到周报，跳过: "
                f"{week_key}"
            )

            weekly_missing_count += 1

            continue

        image_dir = (
            WEEKLY_IMAGE_ROOT
            /
            week_key
        )

        try:

            success = (
                generate_report_images(
                    report_path,
                    image_dir
                )
            )

            if success:

                create_image_markdown(
                    report_path,
                    image_dir
                )

                weekly_success_count += 1

                log(
                    f"      ✓ 周报处理完成: "
                    f"{week_key}"
                )

            else:

                weekly_failed_count += 1

                log(
                    f"      ✗ 周报图片处理失败，"
                    f"继续处理后续任务: "
                    f"{week_key}"
                )

        except Exception as exc:

            weekly_failed_count += 1

            log(
                f"      ✗ 周报处理异常: "
                f"{exc}"
            )

            log(
                "      ⏭ 不终止程序"
            )

    # --------------------------------------------------------------
    # Final statistics
    # --------------------------------------------------------------

    log("")
    log(
        "======================================================================"
    )
    log(
        "IMAGE ENGINE FINISHED"
    )
    log(
        "======================================================================"
    )

    log("")
    log(
        "DAILY:"
    )

    log(
        f"  SUCCESS : {daily_success_count}"
    )

    log(
        f"  MISSING : {daily_missing_count}"
    )

    log(
        f"  FAILED  : {daily_failed_count}"
    )

    log("")
    log(
        "WEEKLY:"
    )

    log(
        f"  SUCCESS : {weekly_success_count}"
    )

    log(
        f"  MISSING : {weekly_missing_count}"
    )

    log(
        f"  FAILED  : {weekly_failed_count}"
    )

    log("")

    # --------------------------------------------------------------
    # 最重要的退出规则
    #
    # 只要至少成功处理了一个日报或周报，
    # 就正常退出。
    #
    # 因为已经成功生成的文件必须允许 GitHub Actions
    # 后续 commit / push。
    #
    # 缺失的日报/周报不算失败。
    # 某一个日报/周报失败，也不能抹掉其他已经成功的结果。
    # --------------------------------------------------------------

    total_success = (
        daily_success_count
        +
        weekly_success_count
    )

    total_failed = (
        daily_failed_count
        +
        weekly_failed_count
    )

    total_missing = (
        daily_missing_count
        +
        weekly_missing_count
    )

    log(
        f"TOTAL SUCCESS : {total_success}"
    )

    log(
        f"TOTAL MISSING : {total_missing}"
    )

    log(
        f"TOTAL FAILED  : {total_failed}"
    )

    # --------------------------------------------------------------
    # 有成功结果
    # --------------------------------------------------------------

    if total_success > 0:

        log("")
        log(
            "✓ 已有成功生成内容"
        )

        log(
            "✓ 已成功落盘"
        )

        log(
            "✓ 后续 GitHub Actions 可以继续执行提交/推送"
        )

        return 0

    # --------------------------------------------------------------
    # 一个输入都没有
    #
    # 这种情况也不应该让每日自动任务变红。
    # --------------------------------------------------------------

    if total_failed == 0:

        log("")
        log(
            "⏭ 当前没有可处理的日报或周报"
        )

        log(
            "✓ 没有可生成内容，正常结束"
        )

        return 0

    # --------------------------------------------------------------
    # 所有实际存在的任务全部失败
    # --------------------------------------------------------------

    log("")
    log(
        "✗ 所有实际存在的图片任务均失败"
    )

    return 1
# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":
    sys.exit(
        main()
    )
