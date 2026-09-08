#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
knowledge_image.py V2
======================================================================

核心目标
----------------------------------------------------------------------

为：

    05_日报
    06_周报

自动生成：

    首图.png
    插图1.png
    插图2.png
    插图3.png

并创建：

    *_带图.md

======================================================================
核心视觉规则
----------------------------------------------------------------------

一篇报告：

    一个核心主题
    一个核心视觉方向

但：

    每一张图片必须是独立、完整、真实的单一场景。

每一张图片严格遵守：

    一个场景
    一个地点
    一个时刻
    一个镜头
    一个视觉中心

禁止：

    格子
    拼图
    分屏
    四宫格
    多画面
    多小场景
    蒙太奇
    storyboard
    diptych
    triptych
    信息图
    PPT
    新闻拼贴
    多个地点同时出现
    多个时间同时出现
    多个视觉中心

======================================================================
图片关系
----------------------------------------------------------------------

一篇报告可以有：

    首图
    插图1
    插图2
    插图3

四张图片可以是不同场景。

但是必须属于：

    同一篇报告
    同一个核心主题
    同一个视觉叙事方向

不是：

    四张随机相关图片。

======================================================================
Markdown 规则
----------------------------------------------------------------------

原始 Markdown：

    永远不修改。

只生成：

    *_带图.md

结构：

    首图
        ↓
    原始正文
        ↓
    插图1
        ↓
    原始正文
        ↓
    插图2
        ↓
    原始正文
        ↓
    插图3
        ↓
    原始正文

首图：

    永远位于报告最前面。

插图：

    必须穿插正文。

禁止：

    所有图片集中在文章开头。

======================================================================
图片数量
----------------------------------------------------------------------

最少：

    3 张

最多：

    4 张

优先生成：

    首图
    插图1
    插图2

如果已经存在合法的：

    插图3.png

则保留。

缺什么补什么。

======================================================================
时间
----------------------------------------------------------------------

所有日期：

    UTC

日报：

    前天
    昨天
    今天

周报：

    ISO Week

======================================================================
AGNES
----------------------------------------------------------------------

API：

    https://api.agnes-ai.cn/v1/images/generations

Model：

    agnes-image-2.5-flash

Size：

    2K

Ratio：

    16:9

Response：

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

def is_valid_png(
    path: Path,
) -> bool:

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
# 13. 准备视觉上下文
# ======================================================================

def prepare_visual_context(
    content: str,
) -> str:
    """
    只用于让 AI 理解报告。

    不把这些文字绘制到图片中。
    """

    lines = []

    for line in content.splitlines():

        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith(
            "![]("
        ):
            continue

        if stripped.startswith(
            "<!--"
        ):
            continue

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

        lines.append(
            cleaned
        )

    text = "\n".join(lines)

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
    重点：

    一篇报告保持统一主题。

    但每张图片必须是一个完整独立场景。
    """

    if image_name == "首图.png":

        role = """
【首图】

这是整篇报告的视觉开场。

请从整篇报告中识别：

    一个最核心的主题。

然后用：

    一个地点
    一个时间状态
    一个主要主体
    一个镜头
    一个视觉中心

建立这篇报告的视觉世界。

首图不是新闻拼贴。

不是多个事件集合。

不是把文章所有内容都塞进一张图片。

只选择最能代表整篇报告核心主题的：

    一个场景。

这个场景必须具有：

    强烈主体
    明确环境
    清晰空间关系
    明确视觉焦点
    新闻纪录片感
    电影级摄影语言
"""

    elif image_name == "插图1.png":

        role = """
【插图1】

这是正文中的第一张插图。

它必须与整篇报告的核心主题保持一致。

但是必须是：

    一个全新的完整场景。

不要复制首图。

不要把首图拆成多个小画面。

可以从核心主题的另一个重要角度观察。

例如：

    现场细节
    核心设备
    关键人物行动
    生产现场
    关键空间

但最终只能选择：

    一个地点
    一个时刻
    一个镜头
    一个视觉中心。

不要加入第二个场景。
"""

    elif image_name == "插图2.png":

        role = """
【插图2】

这是正文中的第二张插图。

继续服务于整篇报告的核心主题。

选择核心主题中的另一个重要视觉关系。

例如：

    人与环境
    人与设备
    产业与基础设施
    城市与事件
    自然与事件
    生产与影响

但是：

    只能表现一个完整场景。

必须：

    一个地点
    一个时刻
    一个镜头
    一个视觉中心。

不能在一张图里表现多个地点或多个时间。
"""

    else:

        role = """
【插图3】

这是正文中的第三张插图。

它仍然属于整篇报告的同一个核心主题。

可以选择：

    更宏观的现场
    事件结果
    产业影响
    社会环境
    基础设施
    长期变化的视觉表现

但是仍然只能：

    一个地点
    一个时刻
    一个镜头
    一个视觉中心。

不要制作总结型信息图。

不要把多个场景拼在一起。
"""

    prompt = f"""
你是一名顶级新闻摄影师、纪录片摄影师和电影摄影指导。

你的任务是：

    为一篇知识日报或周报生成真实、
    专业、统一的新闻视觉图片。

================================================================
第一原则：一个报告，一个核心主题
================================================================

整篇报告只有一个：

    CORE VISUAL THEME

当前图片必须服务于这个核心主题。

不要因为文章中存在多个新闻事件，
就把多个新闻事件放入当前图片。

必须找到整篇报告最核心的视觉方向。

================================================================
第二原则：一图一场景
================================================================

这是绝对规则。

当前图片必须只有：

    一个场景
    一个地点
    一个时刻
    一个镜头
    一个视觉中心

画面应该像：

    一张真实新闻照片
    或
    一帧高质量纪录片电影画面。

================================================================
绝对禁止多场景
================================================================

禁止：

    collage
    grid
    split screen
    multi-panel
    four-panel
    diptych
    triptych
    montage
    storyboard
    infographic
    visual timeline
    multiple scenes
    multiple locations
    multiple time periods

禁止：

    左边一个场景，右边另一个场景。

禁止：

    上面一个场景，下面另一个场景。

禁止：

    四宫格。

禁止：

    把多个新闻事件拼在一起。

禁止：

    多个小场景组成一个大画面。

================================================================
第三原则：一个视觉中心
================================================================

画面必须存在一个最重要的视觉主体。

例如：

    一个人
    一台设备
    一座建筑
    一辆车辆
    一处设施
    一个工业现场
    一个自然现象
    一个核心物体

其他元素只能服务于这个主体。

不要出现：

    多个同等重要的主体。

================================================================
第四原则：地点和时间统一
================================================================

一张图只能发生在：

    一个地点。

一张图只能表现：

    一个时间状态。

不能把：

    白天 + 夜晚

或者：

    城市 + 工厂

或者：

    两个国家

或者：

    两个不同地点

同时塞进一张图片。

================================================================
第五原则：摄影语言
================================================================

采用：

    新闻摄影
    纪录片摄影
    电影级摄影

要求：

    真实
    克制
    专业
    高级
    可信
    有空间层次
    有景深
    有自然光影
    有明确构图

不要：

    卡通
    儿童插画
    廉价商业广告
    PPT
    游戏概念图
    过度赛博朋克
    过度科幻
    海报
    信息图

================================================================
文字绝对禁止
================================================================

图片中绝对不能出现任何可读文字。

禁止：

    中文
    汉字
    英文字母
    英文单词
    标题
    标签
    注释
    图例
    UI文字
    Logo
    品牌名称
    品牌文字
    水印
    字幕
    路牌文字
    屏幕文字
    报纸文字
    书本文字
    包装文字
    广告文字

如果场景中自然存在：

    手机
    电脑
    屏幕
    报纸
    文件
    书籍
    广告牌
    路牌
    包装
    建筑招牌

必须让这些物体：

    没有文字
    不可读
    模糊
    抽象化

不要主动生成任何文字。

不要生成 Logo。

不要生成水印。

阿拉伯数字 0-9 只有在真实场景确实需要时才允许出现。

不要为了装饰主动添加数字。

================================================================
当前报告
================================================================

报告类型：

{report_type}

报告标题：

{report_title}

================================================================
当前图片角色
================================================================

{role}

================================================================
报告内容
================================================================

下面内容只用于理解主题。

绝对不要把其中的文字直接绘制进图片。

{report_content}

================================================================
最终生成要求
================================================================

生成：

    一张
    16:9
    横版
    2K
    高清
    新闻纪录片级
    纯视觉图片。

最终检查：

    是否只有一个场景？
    是否只有一个地点？
    是否只有一个时刻？
    是否只有一个镜头？
    是否只有一个视觉中心？
    是否与整篇报告核心主题一致？
    是否没有拼图？
    是否没有分屏？
    是否没有格子？
    是否没有多场景？
    是否没有中文？
    是否没有英文？
    是否没有 Logo？
    是否没有水印？
    是否没有标题？
    是否没有标签？
    是否没有信息图文字？

如果画面中存在多个场景，
请重新构图为：

    一个场景。

如果画面存在多个视觉中心，
请重新构图为：

    一个视觉中心。

只输出纯视觉图片。
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
            f"图片下载 HTTP {exc.code}: "
            f"{url}"
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
            "AGNES Image API 返回缺少 data："
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
# 17. 获取已有图片
# ======================================================================

def get_existing_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):

            result.append(
                image_name
            )

    return result


# ======================================================================
# 18. 确定缺失图片
# ======================================================================

def determine_missing_images(
    image_dir: Path,
) -> list[str]:
    """
    核心图片：

        首图
        插图1
        插图2

    必须存在。

    插图3：

        可选。

    因此最终：

        3 张 = 合法
        4 张 = 合法
    """

    required = IMAGE_NAMES[
        :MIN_IMAGE_COUNT
    ]

    missing = []

    for image_name in required:

        path = image_dir / image_name

        if not is_valid_png(path):

            missing.append(
                image_name
            )

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

    visual_context = (
        prepare_visual_context(
            content
        )
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
            "首图、插图1、插图2 "
            "均已存在。"
        )

        if is_valid_png(
            image_dir / "插图3.png"
        ):

            log(
                "发现有效插图3.png，保留。"
            )

        return

    log(
        "需要生成："
        + ", ".join(missing)
    )

    # --------------------------------------------------------------
    # 严格按照：
    #
    # 首图
    # 插图1
    # 插图2
    #
    # 顺序生成
    # --------------------------------------------------------------

    for image_name in missing:

        log(
            "=" * 60
        )

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
        # 每张图片立即落盘
        # ----------------------------------------------------------

        atomic_write_bytes(
            target_path,
            image_data,
        )

        log(
            f"图片已落盘："
            f"{target_path}"
        )

        # ----------------------------------------------------------
        # 每张图片立即验证
        # ----------------------------------------------------------

        if not is_valid_png(
            target_path
        ):

            raise RuntimeError(
                f"图片落盘后验证失败："
                f"{target_path}"
            )

        log(
            f"图片验证成功："
            f"{image_name}"
        )


# ======================================================================
# 20. 获取最终图片
# ======================================================================

def get_final_images(
    image_dir: Path,
) -> list[str]:

    result = []

    for image_name in IMAGE_NAMES:

        path = image_dir / image_name

        if is_valid_png(path):

            result.append(
                image_name
            )

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
# 22. Markdown 结构分析
# ======================================================================

def split_markdown_blocks(
    content: str,
) -> list[str]:
    """
    将 Markdown 按自然空行拆成 block。

    不修改 block 内容。

    目的只是：

        找到适合插图的位置。

    原始文字不会被重写。
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

    return blocks


# ======================================================================
# 23. 判断是否适合插图
# ======================================================================

def is_good_insertion_block(
    block: str,
) -> bool:
    """
    优先选择正文段落。

    不优先在：

        标题
        YAML
        HTML
        图片
        表格

    后面立即插入。

    """

    stripped = block.strip()

    if not stripped:

        return False

    # 标题
    if stripped.startswith("#"):

        return False

    # 图片
    if stripped.startswith("![]("):

        return False

    # HTML
    if stripped.startswith("<"):

        return False

    # Markdown 表格
    if "|" in stripped:

        lines = stripped.splitlines()

        if len(lines) >= 2:

            if all(
                "|" in line
                for line in lines[:2]
            ):

                return False

    return True


# ======================================================================
# 24. 找正文插图位置
# ======================================================================

def get_insertion_positions(
    blocks: list[str],
    image_count: int,
) -> list[int]:
    """
    image_count：

        只计算正文插图数量。

    例如：

        3 张总图
        =
        首图 + 插图1 + 插图2

    那么：

        image_count = 2

    4 张总图：

        image_count = 3

    返回：

        插入图片之后的 block 位置。

    例如：

        [3, 7, 11]

    表示：

        第3个正文 block 后
        第7个正文 block 后
        第11个正文 block 后

    """

    if image_count <= 0:

        return []

    good_positions = []

    for index, block in enumerate(
        blocks,
        start=1,
    ):

        if is_good_insertion_block(
            block
        ):

            good_positions.append(
                index
            )

    if not good_positions:

        return []

    # --------------------------------------------------------------
    # 如果正文太少
    # --------------------------------------------------------------

    if len(good_positions) <= image_count:

        return good_positions[
            :image_count
        ]

    # --------------------------------------------------------------
    # 均匀分布
    # --------------------------------------------------------------

    positions = []

    total = len(good_positions)

    for i in range(
        1,
        image_count + 1,
    ):

        target = round(
            total
            * i
            / (image_count + 1)
        )

        target = max(
            1,
            min(
                target,
                total,
            ),
        )

        positions.append(
            good_positions[
                target - 1
            ]
        )

    # --------------------------------------------------------------
    # 去重
    # --------------------------------------------------------------

    unique = []

    for position in positions:

        if position not in unique:

            unique.append(
                position
            )

    return unique


# ======================================================================
# 25. 构建带图 Markdown
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

    # ==============================================================
    # 1. 首图
    # ==============================================================

    cover_path = (
        image_dir / "首图.png"
    )

    if not is_valid_png(
        cover_path
    ):

        raise RuntimeError(
            "首图.png 不存在或无效"
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

    # ==============================================================
    # 2. 原始正文
    # ==============================================================

    original_body = (
        original_content.strip()
    )

    if not original_body:

        raise RuntimeError(
            f"{report_type}原始 Markdown 为空："
            f"{report_path}"
        )

    # ==============================================================
    # 3. 正文 block
    # ==============================================================

    blocks = split_markdown_blocks(
        original_body
    )

    if not blocks:

        raise RuntimeError(
            f"{report_type}没有可处理的 Markdown 正文"
        )

    # ==============================================================
    # 4. 正文插图
    # ==============================================================

    interior_images = [
        name
        for name in image_names
        if name != "首图.png"
    ]

    interior_images = (
        interior_images[:3]
    )

    insertion_positions = (
        get_insertion_positions(
            blocks=blocks,
            image_count=len(
                interior_images
            ),
        )
    )

    # ==============================================================
    # 5. 如果正文结构太短
    # ==============================================================
    #
    # 例如只有几个 block。
    #
    # 仍然必须让图片穿插，而不是全部放开头。
    #
    # 因此允许：
    #
    # 正文 block
    # ↓
    # 图片
    # ↓
    # 正文 block
    #
    # 如果实在没有足够位置，则最后才追加。
    # ==============================================================

    output_blocks = []

    image_index = 0

    for index, block in enumerate(
        blocks,
        start=1,
    ):

        # ----------------------------------------------------------
        # 原始 block 原封不动加入
        # ----------------------------------------------------------

        output_blocks.append(
            block
        )

        # ----------------------------------------------------------
        # 到达插图位置
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

            if not is_valid_png(
                image_path
            ):

                raise RuntimeError(
                    f"插图文件无效："
                    f"{image_path}"
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

    # ==============================================================
    # 6. 如果仍有未插入图片
    # ==============================================================

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

        if not is_valid_png(
            image_path
        ):

            raise RuntimeError(
                f"插图文件无效："
                f"{image_path}"
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

    # ==============================================================
    # 7. 首图 + 正文
    # ==============================================================

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
# 26. 带图报告路径
# ======================================================================

def build_image_report_path(
    report_path: Path,
) -> Path:

    return report_path.with_name(
        f"{report_path.stem}_带图"
        f"{report_path.suffix}"
    )


# ======================================================================
# 27. 验证图片顺序
# ======================================================================

def validate_image_order(
    content: str,
    report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> None:

    positions = []

    for image_name in image_names:

        image_path = (
            image_dir / image_name
        )

        relative_path = (
            make_relative_image_path(
                report_path,
                image_path,
            )
        )

        marker = (
            f"![]({relative_path})"
        )

        position = content.find(
            marker
        )

        if position < 0:

            raise RuntimeError(
                f"Markdown 缺少图片引用："
                f"{image_name}"
            )

        positions.append(
            (
                image_name,
                position,
            )
        )

    # --------------------------------------------------------------
    # 首图 → 插图1 → 插图2 → 插图3
    # --------------------------------------------------------------

    for index in range(
        1,
        len(positions),
    ):

        previous_name, previous_pos = (
            positions[index - 1]
        )

        current_name, current_pos = (
            positions[index]
        )

        if current_pos <= previous_pos:

            raise RuntimeError(
                f"图片顺序错误："
                f"{previous_name} → "
                f"{current_name}"
            )


# ======================================================================
# 28. 验证正文穿插
# ======================================================================

def validate_body_interleaving(
    content: str,
    report_path: Path,
    image_dir: Path,
    image_names: list[str],
) -> None:
    """
    验证：

        首图
        ↓
        正文
        ↓
        插图1
        ↓
        正文
        ↓
        插图2
        ↓
        正文
        ↓
        插图3

    禁止：

        首图
        插图1
        插图2
        插图3
        正文
    """

    markers = []

    for image_name in image_names:

        image_path = (
            image_dir / image_name
        )

        relative_path = (
            make_relative_image_path(
                report_path,
                image_path,
            )
        )

        marker = (
            f"![]({relative_path})"
        )

        position = content.find(
            marker
        )

        if position < 0:

            raise RuntimeError(
                f"找不到图片引用："
                f"{image_name}"
            )

        markers.append(
            (
                image_name,
                position,
                marker,
            )
        )

    # --------------------------------------------------------------
    # 首图必须从文件开头开始
    # --------------------------------------------------------------

    first_name, first_pos, first_marker = (
        markers[0]
    )

    if not content.startswith(
        first_marker
    ):

        raise RuntimeError(
            "首图没有位于报告最前面"
        )

    # --------------------------------------------------------------
    # 每两张图片之间必须存在正文
    #
    # 这里不要求每张图之间必须是很多文字，
    # 但绝不能直接连续：
    #
    # 图片
    # 图片
    # --------------------------------------------------------------

    for index in range(
        1,
        len(markers),
    ):

        previous_name, previous_pos, previous_marker = (
            markers[index - 1]
        )

        current_name, current_pos, current_marker = (
            markers[index]
        )

        between = content[
            previous_pos
            + len(previous_marker):
            current_pos
        ]

        # 去掉空白
        between_clean = between.strip()

        if not between_clean:

            raise RuntimeError(
                f"{previous_name} 与 "
                f"{current_name} 之间没有正文内容，"
                f"图片没有真正穿插正文。"
            )

        # ----------------------------------------------------------
        # 如果中间只有另一张图片引用，
        # 同样认为是连续图片堆叠。
        # ----------------------------------------------------------

        non_image_lines = []

        for line in between_clean.splitlines():

            stripped = line.strip()

            if not stripped:

                continue

            if stripped.startswith(
                "![]("
            ):

                continue

            non_image_lines.append(
                stripped
            )

        if not non_image_lines:

            raise RuntimeError(
                f"{previous_name} 与 "
                f"{current_name} 之间只有图片，"
                f"禁止图片连续堆叠。"
            )


# ======================================================================
# 29. 验证带图 Markdown
# ======================================================================

def validate_image_report(
    report_type: str,
    original_content: str,
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

    # --------------------------------------------------------------
    # 图片数量
    # --------------------------------------------------------------

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
    # 每张图片必须有效
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
                f"{report_type}带图报告缺少图片引用："
                f"{expected}"
            )

    # --------------------------------------------------------------
    # 首图最前
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
    # 图片顺序
    # --------------------------------------------------------------

    validate_image_order(
        content=content,
        report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    # --------------------------------------------------------------
    # 正文穿插
    # --------------------------------------------------------------

    validate_body_interleaving(
        content=content,
        report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    # --------------------------------------------------------------
    # 原始正文必须仍然存在
    #
    # 注意：
    #
    # 原始 Markdown 没有被修改。
    #
    # 这里通过去掉图片引用后，
    # 检查原始内容是否仍然存在。
    # --------------------------------------------------------------

    content_without_images = content

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

        content_without_images = (
            content_without_images.replace(
                marker,
                "",
            )
        )

    normalized_original = (
        original_content.strip()
    )

    normalized_output = (
        content_without_images.strip()
    )

    if normalized_original not in normalized_output:

        raise RuntimeError(
            f"{report_type}带图报告未完整保留原始 Markdown 正文"
        )

    log(
        f"{report_type}带图报告验证成功："
        f"{image_report_path}"
    )


# ======================================================================
# 30. 创建带图报告
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

    if len(image_names) > MAX_IMAGE_COUNT:

        raise RuntimeError(
            f"{report_type}图片超过上限："
            f"{len(image_names)}"
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
        original_content=original_content,
        image_report_path=image_report_path,
        image_dir=image_dir,
        image_names=image_names,
    )

    return image_report_path


# ======================================================================
# 31. 处理日报
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
    # 创建带图报告
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
# 32. 处理周报
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
    # 创建带图报告
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
# 33. 主程序
# ======================================================================

def main() -> int:

    log("=" * 72)

    log(
        "748686 自生长知识系统"
    )

    log(
        "knowledge_image.py V2"
    )

    log(
        "单报告统一主题 + 一图一场景 + "
        "首图置顶 + 插图穿插正文"
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
    # UTC
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
        "knowledge_image.py V2 完成"
    )

    log("=" * 72)

    return 0


# ======================================================================
# Entry Point
# ======================================================================

if __name__ == "__main__":

    sys.exit(
        main()
    )
