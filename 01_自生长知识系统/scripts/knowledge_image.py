#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Image Engine V3
======================================================================

核心目标
----------------------------------------------------------------------

1. 日报 / 周报自动生成配图
2. 一图一个场景
3. 图片必须与报告中的真实新闻内容对应
4. 首图严格锚定“最近一条新闻”
5. 插图1继续围绕最近新闻，但使用另一个单独镜头
6. 插图2锚定第二条新闻
7. 插图3锚定第三条新闻
8. 禁止拼图 / 分屏 / 多场景 / 多事件
9. 禁止图片中出现中文、英文、标题、标签、Logo、水印等文字
10. 图片生成后立即验证 PNG
11. 使用原子写入
12. 已存在且有效的图片不重复生成
13. 原 Markdown 永远不修改
14. 创建 *_带图.md
15. 首图放在正文最前面
16. 其余图片穿插正文
17. 全部日期使用 UTC
18. 日报处理：前天 → 昨天 → 今天
19. 周报处理：三个日期对应的 ISO 周，去重
======================================================================
"""

import os
import re
import sys
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
SYSTEM_ROOT = SCRIPT_DIR.parent

DAILY_ROOT = SYSTEM_ROOT / "05_日报"
WEEKLY_ROOT = SYSTEM_ROOT / "06_周报"

IMAGE_ROOT = SYSTEM_ROOT / "04_图片"
DAILY_IMAGE_ROOT = IMAGE_ROOT / "日报"
WEEKLY_IMAGE_ROOT = IMAGE_ROOT / "周报"


# ======================================================================
# AGNES
# ======================================================================

AGNES_API_URL = "https://api.agnes-ai.cn/v1/images/generations"

AGNES_IMAGE_MODEL = "agnes-image-2.5-flash"

IMAGE_SIZE = "2K"
IMAGE_RATIO = "16:9"

REQUEST_TIMEOUT = 180


# ======================================================================
# IMAGE CONTRACT
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
# NEWS EXTRACTION
# ======================================================================

# 新闻条目标题常见形式：
#
# ## 新闻标题
# ### 新闻标题
# 1. 新闻标题
# 1、新闻标题
# - 新闻标题
# **新闻标题**
#
# 我们不会强依赖某一种 Markdown 格式。
#

HEADING_RE = re.compile(
    r"^\s{0,3}#{1,6}\s+(.+?)\s*$"
)

NUMBERED_RE = re.compile(
    r"^\s*(?:\d+[\.\、\)]|[-•])\s+(.+?)\s*$"
)


# ======================================================================
# UTC
# ======================================================================

def utc_today():
    return datetime.now(timezone.utc).date()


# ======================================================================
# BASIC UTILITIES
# ======================================================================

def log(message):
    print(message, flush=True)


def clean_markdown_text(text):
    """
    把 Markdown 内容变成适合新闻识别的纯文本。
    """

    if not text:
        return ""

    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)

    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)

    text = re.sub(r"<[^>]+>", " ", text)

    text = re.sub(r"`{1,3}.*?`{1,3}", " ", text, flags=re.S)

    text = re.sub(r"[*_~]+", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def remove_report_metadata_lines(text):
    """
    删除明显属于报告元数据的行。
    """

    output = []

    for line in text.splitlines():

        s = line.strip()

        if not s:
            continue

        lower = s.lower()

        if lower.startswith("date:"):
            continue

        if lower.startswith("generated"):
            continue

        if lower.startswith("timezone"):
            continue

        if lower.startswith("source"):
            continue

        if lower.startswith("url:"):
            continue

        if lower.startswith("http://"):
            continue

        if lower.startswith("https://"):
            continue

        if s.startswith("---"):
            continue

        output.append(line)

    return "\n".join(output)


# ======================================================================
# REPORT LOCATION
# ======================================================================

def find_daily_report(target_date):

    path = (
        DAILY_ROOT
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / f"{target_date:%Y-%m-%d}.md"
    )

    if path.exists():
        return path

    return None


def find_weekly_report(year, week):

    path = (
        WEEKLY_ROOT
        / str(year)
        / f"W{week:02d}.md"
    )

    if path.exists():
        return path

    return None


# ======================================================================
# IMAGE DIRECTORY
# ======================================================================

def daily_image_dir(target_date):

    return (
        DAILY_IMAGE_ROOT
        / target_date.strftime("%Y-%m-%d")
    )


def weekly_image_dir(year, week):

    return (
        WEEKLY_IMAGE_ROOT
        / f"{year}-W{week:02d}"
    )


# ======================================================================
# REPORT
# ======================================================================

def read_report(path):

    return path.read_text(
        encoding="utf-8"
    )


def extract_report_title(content):

    for line in content.splitlines():

        s = line.strip()

        if not s:
            continue

        m = HEADING_RE.match(s)

        if m:
            return clean_markdown_text(
                m.group(1)
            )

        if len(s) >= 8:
            return clean_markdown_text(s)

    return "Knowledge Report"


# ======================================================================
# NEWS EXTRACTION
# ======================================================================

def is_noise_heading(text):
    """
    判断一个标题是不是报告结构标题，而不是新闻标题。
    """

    t = clean_markdown_text(text).strip()

    if not t:
        return True

    noise_keywords = [
        "日报",
        "周报",
        "摘要",
        "总结",
        "分析",
        "趋势",
        "目录",
        "概览",
        "说明",
        "数据统计",
        "来源",
        "参考",
        "核心观点",
        "今日知识",
        "本周知识",
        "知识图谱",
        "系统运行",
        "运行信息",
        "报告说明",
        "免责声明",
    ]

    for keyword in noise_keywords:

        if t == keyword:
            return True

        if t.startswith(keyword + "："):
            return True

        if t.startswith(keyword + ":"):
            return True

    return False


def extract_candidate_headings(content):

    candidates = []

    for line in content.splitlines():

        s = line.strip()

        if not s:
            continue

        match = HEADING_RE.match(s)

        if match:

            title = clean_markdown_text(
                match.group(1)
            )

            if not is_noise_heading(title):

                candidates.append({
                    "title": title,
                    "source_line": line,
                })

    return candidates


def split_sections_by_headings(content):

    """
    按 Markdown 标题切分报告。

    返回：

    [
        {
            "title": "...",
            "content": "..."
        }
    ]
    """

    lines = content.splitlines()

    sections = []

    current_title = None
    current_lines = []

    for line in lines:

        match = HEADING_RE.match(
            line.strip()
        )

        if match:

            if current_title is not None:

                sections.append({
                    "title": clean_markdown_text(
                        current_title
                    ),
                    "content": "\n".join(
                        current_lines
                    ).strip(),
                })

            current_title = match.group(1)
            current_lines = []

        else:

            if current_title is not None:
                current_lines.append(line)

    if current_title is not None:

        sections.append({
            "title": clean_markdown_text(
                current_title
            ),
            "content": "\n".join(
                current_lines
            ).strip(),
        })

    return sections


def extract_news_items(content):

    """
    从报告中提取新闻单元。

    不要求报告必须使用统一 Markdown 模板。

    优先：
        标题 + 标题下面的正文

    其次：
        编号新闻

    最后：
        正文段落作为候选新闻。
    """

    items = []

    sections = split_sections_by_headings(
        content
    )

    for section in sections:

        title = clean_markdown_text(
            section["title"]
        )

        body = clean_markdown_text(
            remove_report_metadata_lines(
                section["content"]
            )
        )

        if is_noise_heading(title):
            continue

        if len(title) < 4:
            continue

        # 避免把极大的报告章节当成单条新闻
        if len(body) > 6000:
            body = body[:6000]

        if body:

            items.append({
                "title": title,
                "body": body,
                "text": (
                    f"{title}\n"
                    f"{body}"
                ),
            })

    # --------------------------------------------------------------
    # 如果标题解析不足，再尝试编号条目
    # --------------------------------------------------------------

    if len(items) < 2:

        lines = content.splitlines()

        current = None

        for line in lines:

            m = NUMBERED_RE.match(line)

            if m:

                title = clean_markdown_text(
                    m.group(1)
                )

                if (
                    len(title) >= 8
                    and not is_noise_heading(title)
                ):

                    current = {
                        "title": title,
                        "body": "",
                        "text": title,
                    }

                    items.append(current)

            elif current:

                s = clean_markdown_text(line)

                if s:

                    current["body"] += (
                        " " + s
                    )

                    current["text"] = (
                        current["title"]
                        + "\n"
                        + current["body"]
                    )

    # --------------------------------------------------------------
    # 最后兜底：使用正文段落
    # --------------------------------------------------------------

    if not items:

        blocks = split_markdown_blocks(
            content
        )

        for block in blocks:

            text = clean_markdown_text(
                block
            )

            if len(text) < 40:
                continue

            if text.startswith("#"):
                continue

            items.append({
                "title": text[:120],
                "body": text,
                "text": text,
            })

            if len(items) >= 5:
                break

    return items


# ======================================================================
# NEWS NORMALIZATION
# ======================================================================

def normalize_news_text(text, max_chars=2600):

    text = clean_markdown_text(text)

    # 删除 URL
    text = re.sub(
        r"https?://\S+",
        " ",
        text
    )

    # 删除明显的图片路径
    text = re.sub(
        r"\S+\.(?:png|jpg|jpeg|webp)",
        " ",
        text,
        flags=re.I
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()[:max_chars]


# ======================================================================
# NEWS ANCHOR
# ======================================================================

def build_news_anchor(
    news_item,
    role,
    index
):
    """
    建立图片与新闻之间的明确绑定。

    role:
        cover
        related
        secondary
    """

    title = normalize_news_text(
        news_item.get("title", ""),
        500
    )

    body = normalize_news_text(
        news_item.get("body", ""),
        2000
    )

    text = normalize_news_text(
        news_item.get("text", ""),
        2600
    )

    return {
        "role": role,
        "index": index,
        "title": title,
        "body": body,
        "news_text": text,
    }


# ======================================================================
# IMAGE PLAN
# ======================================================================

def build_image_plan(report_content):

    news_items = extract_news_items(
        report_content
    )

    log(
        f"Detected news items: "
        f"{len(news_items)}"
    )

    for i, item in enumerate(
        news_items[:10],
        start=1
    ):

        log(
            f"  NEWS {i}: "
            f"{item.get('title', '')[:120]}"
        )

    if not news_items:

        raise RuntimeError(
            "Unable to extract any news item "
            "from report."
        )

    # --------------------------------------------------------------
    # 最近一条新闻
    #
    # 这里的“最近”定义为：
    # 报告中最后一个可识别新闻单元。
    #
    # 这正是用户当前要求的核心。
    # --------------------------------------------------------------

    latest_index = len(news_items) - 1

    latest_news = news_items[
        latest_index
    ]

    # --------------------------------------------------------------
    # 第二、第三条新闻
    #
    # 从最近新闻向前寻找。
    # --------------------------------------------------------------

    previous_news = []

    for i in range(
        latest_index - 1,
        -1,
        -1
    ):

        previous_news.append(
            news_items[i]
        )

        if len(previous_news) >= 2:
            break

    plan = []

    # ==============================================================
    # COVER
    # ==============================================================

    plan.append({
        "image_name": "首图.png",
        "anchor": build_news_anchor(
            latest_news,
            "cover",
            latest_index + 1
        ),
    })

    # ==============================================================
    # INSERT 1
    #
    # 同一条最近新闻
    # 但必须要求“不同镜头”
    # ==============================================================

    plan.append({
        "image_name": "插图1.png",
        "anchor": build_news_anchor(
            latest_news,
            "related",
            latest_index + 1
        ),
    })

    # ==============================================================
    # INSERT 2
    # ==============================================================

    if len(previous_news) >= 1:

        plan.append({
            "image_name": "插图2.png",
            "anchor": build_news_anchor(
                previous_news[0],
                "secondary",
                latest_index
            ),
        })

    else:

        plan.append({
            "image_name": "插图2.png",
            "anchor": build_news_anchor(
                latest_news,
                "related",
                latest_index + 1
            ),
        })

    # ==============================================================
    # INSERT 3
    # ==============================================================

    if len(previous_news) >= 2:

        plan.append({
            "image_name": "插图3.png",
            "anchor": build_news_anchor(
                previous_news[1],
                "secondary",
                latest_index - 1
            ),
        })

    return plan


# ======================================================================
# SCENE BRIEF
# ======================================================================

def build_scene_brief(
    image_name,
    anchor
):

    role = anchor["role"]
    title = anchor["title"]
    body = anchor["body"]

    if image_name == "首图.png":

        shot_instruction = """
Create the strongest single photographic scene
that directly represents the news event described below.

The image must function as the visual cover of this
specific news event.

Do not summarize the whole report.
Do not combine different facts.
Do not create a symbolic collage.

Choose ONE concrete physical moment from this news.
"""

    elif image_name == "插图1.png":

        shot_instruction = """
Create a second photographic view of the SAME news event.

It must remain clearly connected to the same event,
but it must be a DIFFERENT single camera shot.

Do not create a collage.
Do not combine multiple moments.
Do not summarize several aspects of the event.

Choose one concrete physical moment related to this event.
"""

    else:

        shot_instruction = """
Create one concrete documentary photograph representing
the specific news item below.

The image must correspond directly to this news item,
not to the whole report.

Choose ONE physical situation from this news.
"""

    return f"""
NEWS-ANCHORED VISUAL TASK

{shot_instruction}

NEWS TITLE:
{title}

NEWS CONTENT:
{body}

The news content above is the factual anchor.
The generated image MUST depict a visually plausible,
real-world scene that directly corresponds to this news.

Do not invent an unrelated subject.

If the article describes a person, institution, building,
location, event, meeting, protest, launch, accident,
technology, market event, natural event, or other concrete
occurrence, visually represent that same occurrence.

If exact visual details are not explicitly stated,
choose only conservative details that are compatible
with the news.

Do not add unrelated objects or unrelated events.

============================================================
ABSOLUTE SCENE RULE
============================================================

ONE IMAGE.
ONE SCENE.
ONE LOCATION.
ONE MOMENT.
ONE CAMERA.
ONE CAMERA ANGLE.
ONE CONTINUOUS PHYSICAL ENVIRONMENT.
ONE DOMINANT VISUAL SUBJECT.
ONE MAIN ACTION.
ONE VISUAL CENTER.

The background must remain subordinate.

============================================================
STRICTLY FORBIDDEN
============================================================

NO collage.
NO composite image.
NO grid.
NO panels.
NO split screen.
NO four-panel layout.
NO triptych.
NO diptych.
NO montage.
NO storyboard.
NO infographic.
NO news-summary board.
NO multiple photographs inside one image.
NO multiple separate locations.
NO multiple unrelated events.
NO different time periods.
NO visual timeline.

============================================================
TEXT PROHIBITION
============================================================

The final image must contain NO readable text.

Absolutely no:

Chinese characters.
Hanzi.
Chinese writing.
English words.
English letters.
Headlines.
Titles.
Captions.
Labels.
Subtitles.
Logos.
Watermarks.
Brand names.
Signs.
Road signs.
Shop signs.
Building signs.
Billboards.
Newspapers.
Books.
Documents.
Printed papers.
Posters.
Advertisements.
Screen text.
Phone screen text.
Computer screen text.
Television text.
UI text.
Charts.
Chart labels.
Legends.
Diagrams.
Packaging text.
Name badges.
Uniform logos.

Avoid text-bearing objects whenever possible.

============================================================
VISUAL STYLE
============================================================

Professional documentary news photography.

Realistic physical environment.

Natural human proportions.

Credible lighting.

Natural materials.

Realistic camera perspective.

Photorealistic.

Editorial photography quality.

Cinematic but restrained.

No fantasy.

No illustration.

No cartoon.

No surrealism.

No artificial infographic aesthetic.

============================================================
FINAL INSTRUCTION
============================================================

Before generating, internally verify:

1. Does this image depict the SAME NEWS EVENT?
2. Is there exactly ONE physical scene?
3. Is there exactly ONE location?
4. Is there exactly ONE moment?
5. Is there exactly ONE camera view?
6. Is there exactly ONE visual center?
7. Is there any readable text?

If any answer violates the rules,
simplify the image until all rules are satisfied.

Generate ONLY the final single photograph.
"""


# ======================================================================
# API
# ======================================================================

def get_api_key():

    api_key = os.getenv(
        "AGNES_API_KEY",
        ""
    ).strip()

    if not api_key:

        raise RuntimeError(
            "AGNES_API_KEY environment variable "
            "is not configured."
        )

    return api_key


def download_image(url):

    request = Request(
        url,
        headers={
            "User-Agent":
                "748686-Knowledge-Image-Engine/3.0"
        }
    )

    with urlopen(
        request,
        timeout=REQUEST_TIMEOUT
    ) as response:

        data = response.read()

    if not data.startswith(b"\x89PNG\r\n\x1a\n"):

        raise RuntimeError(
            "Downloaded image is not a valid PNG."
        )

    return data


def generate_image(prompt):

    api_key = get_api_key()

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
        ensure_ascii=False
    ).encode("utf-8")

    request = Request(
        AGNES_API_URL,
        data=body,
        headers={
            "Authorization":
                f"Bearer {api_key}",
            "Content-Type":
                "application/json",
            "Accept":
                "application/json",
        },
        method="POST",
    )

    try:

        with urlopen(
            request,
            timeout=REQUEST_TIMEOUT
        ) as response:

            raw = response.read()

    except HTTPError as exc:

        error_body = exc.read().decode(
            "utf-8",
            errors="replace"
        )

        raise RuntimeError(
            f"AGNES HTTP {exc.code}: "
            f"{error_body[:2000]}"
        )

    except URLError as exc:

        raise RuntimeError(
            f"AGNES network error: {exc}"
        )

    data = json.loads(
        raw.decode("utf-8")
    )

    image_url = None

    if isinstance(data, dict):

        data_items = data.get(
            "data"
        )

        if (
            isinstance(data_items, list)
            and data_items
            and isinstance(data_items[0], dict)
        ):

            image_url = data_items[0].get(
                "url"
            )

    if not image_url:

        raise RuntimeError(
            "AGNES response did not contain "
            "data[0].url."
        )

    return download_image(
        image_url
    )


# ======================================================================
# ATOMIC WRITE
# ======================================================================

def atomic_write_bytes(
    path,
    data
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = path.with_name(
        f".{path.name}.tmp"
    )

    with open(
        temp_path,
        "wb"
    ) as f:

        f.write(data)

        f.flush()

        os.fsync(
            f.fileno()
        )

    os.replace(
        temp_path,
        path
    )


def atomic_write_text(
    path,
    text
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = path.with_name(
        f".{path.name}.tmp"
    )

    with open(
        temp_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)

        f.flush()

        os.fsync(
            f.fileno()
        )

    os.replace(
        temp_path,
        path
    )


# ======================================================================
# IMAGE VALIDATION
# ======================================================================

def is_valid_png(path):

    try:

        if not path.exists():
            return False

        if path.stat().st_size < 100:

            return False

        with open(
            path,
            "rb"
        ) as f:

            signature = f.read(8)

        return (
            signature
            == b"\x89PNG\r\n\x1a\n"
        )

    except Exception:

        return False


def get_existing_images(
    image_dir
):

    existing = []

    for name in IMAGE_NAMES:

        path = image_dir / name

        if is_valid_png(path):

            existing.append(name)

    return existing


def determine_missing_images(
    image_dir
):

    existing = get_existing_images(
        image_dir
    )

    missing = []

    # --------------------------------------------------------------
    # 至少保证三张
    # --------------------------------------------------------------

    for name in IMAGE_NAMES[:MIN_IMAGE_COUNT]:

        if name not in existing:

            missing.append(name)

    # --------------------------------------------------------------
    # 如果第四张已经存在，就保留。
    # 如果第四张不存在，本次不强制生成。
    # --------------------------------------------------------------

    return existing, missing


# ======================================================================
# IMAGE GENERATION
# ======================================================================

def generate_missing_images(
    image_dir,
    report_content
):

    image_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    existing, missing = (
        determine_missing_images(
            image_dir
        )
    )

    log("")
    log("=" * 70)
    log("IMAGE GENERATION PLAN")
    log("=" * 70)

    log(
        f"Existing valid images: "
        f"{len(existing)}"
    )

    log(
        f"Missing required images: "
        f"{len(missing)}"
    )

    if not missing:

        log(
            "All required images already exist. "
            "No regeneration needed."
        )

        return

    # --------------------------------------------------------------
    # 新闻锚点计划
    # --------------------------------------------------------------

    image_plan = build_image_plan(
        report_content
    )

    plan_map = {
        item["image_name"]: item
        for item in image_plan
    }

    # --------------------------------------------------------------
    # 严格按照：
    #
    # 首图
    # 插图1
    # 插图2
    # 插图3
    #
    # 顺序生成。
    # --------------------------------------------------------------

    for image_name in missing:

        plan_item = plan_map.get(
            image_name
        )

        if not plan_item:

            log(
                f"WARNING: no news plan for "
                f"{image_name}"
            )

            continue

        anchor = plan_item["anchor"]

        log("")
        log("-" * 70)
        log(
            f"Generating: {image_name}"
        )

        log(
            f"News anchor: "
            f"{anchor['title'][:180]}"
        )

        log(
            f"News position: "
            f"{anchor['index']}"
        )

        log(
            f"Image role: "
            f"{anchor['role']}"
        )

        scene_brief = build_scene_brief(
            image_name,
            anchor
        )

        log(
            "Single-scene visual task "
            "created."
        )

        prompt = scene_brief

        image_path = (
            image_dir
            / image_name
        )

        # ----------------------------------------------------------
        # 调用 AGNES
        # ----------------------------------------------------------

        image_bytes = generate_image(
            prompt
        )

        # ----------------------------------------------------------
        # 立即原子写入
        # ----------------------------------------------------------

        atomic_write_bytes(
            image_path,
            image_bytes
        )

        # ----------------------------------------------------------
        # 立即验证
        # ----------------------------------------------------------

        if not is_valid_png(
            image_path
        ):

            raise RuntimeError(
                f"Image validation failed: "
                f"{image_path}"
            )

        log(
            f"VALID PNG: "
            f"{image_path}"
        )

        # ----------------------------------------------------------
        # 每张图之间稍微停顿
        # ----------------------------------------------------------

        time.sleep(1)


# ======================================================================
# MARKDOWN
# ======================================================================

def split_markdown_blocks(
    content
):

    return re.split(
        r"\n\s*\n",
        content.strip()
    )


def is_good_insertion_block(
    block
):

    s = block.strip()

    if not s:
        return False

    # 标题
    if re.match(
        r"^\s*#{1,6}\s+",
        s
    ):
        return False

    # 图片
    if re.fullmatch(
        r"!\[[^\]]*\]\([^)]+\)",
        s
    ):
        return False

    # HTML
    if s.startswith("<"):
        return False

    # 表格
    if "|" in s and "\n|" in s:
        return False

    return True


def get_insertion_positions(
    blocks,
    image_count
):

    good_positions = [
        i
        for i, block in enumerate(blocks)
        if is_good_insertion_block(
            block
        )
    ]

    if not good_positions:

        return []

    # 需要插入的正文图片：
    # 插图1、插图2、插图3
    interior_count = image_count - 1

    if interior_count <= 0:

        return []

    if len(good_positions) <= interior_count:

        return good_positions

    positions = []

    for i in range(
        interior_count
    ):

        ratio = (
            i + 1
        ) / (
            interior_count + 1
        )

        index = int(
            ratio
            * (
                len(good_positions) - 1
            )
        )

        positions.append(
            good_positions[index]
        )

    # 去重并保持顺序
    result = []

    for p in positions:

        if p not in result:

            result.append(p)

    return result


def make_relative_image_path(
    markdown_path,
    image_path
):

    relative = os.path.relpath(
        image_path,
        start=markdown_path.parent
    )

    return relative.replace(
        os.sep,
        "/"
    )


def build_image_markdown(
    markdown_path,
    original_content,
    image_dir
):

    images = [
        image_dir / name
        for name in IMAGE_NAMES
        if is_valid_png(
            image_dir / name
        )
    ]

    if len(images) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            f"Need at least "
            f"{MIN_IMAGE_COUNT} valid images, "
            f"found {len(images)}."
        )

    if len(images) > MAX_IMAGE_COUNT:

        images = images[
            :MAX_IMAGE_COUNT
        ]

    cover = image_dir / "首图.png"

    if not is_valid_png(cover):

        raise RuntimeError(
            "首图.png is missing or invalid."
        )

    # --------------------------------------------------------------
    # 原始正文
    # --------------------------------------------------------------

    blocks = split_markdown_blocks(
        original_content
    )

    # --------------------------------------------------------------
    # 首图
    # --------------------------------------------------------------

    cover_relative = (
        make_relative_image_path(
            markdown_path,
            cover
        )
    )

    output = []

    output.append(
        f"![首图]({cover_relative})"
    )

    output.append("")

    # --------------------------------------------------------------
    # 正文图片
    # --------------------------------------------------------------

    interior_images = []

    for image_path in images:

        if image_path.name == "首图.png":
            continue

        interior_images.append(
            image_path
        )

    positions = get_insertion_positions(
        blocks,
        len(images)
    )

    position_to_image = {}

    for position, image_path in zip(
        positions,
        interior_images
    ):

        position_to_image[
            position
        ] = image_path

    remaining_images = [
        image_path
        for image_path in interior_images
        if image_path not in
        position_to_image.values()
    ]

    for index, block in enumerate(
        blocks
    ):

        output.append(
            block
        )

        image_path = (
            position_to_image.get(index)
        )

        if image_path:

            relative = (
                make_relative_image_path(
                    markdown_path,
                    image_path
                )
            )

            output.append("")

            output.append(
                f"![{image_path.stem}]"
                f"({relative})"
            )

            output.append("")

    # --------------------------------------------------------------
    # 如果正文块太少，剩余图片放在最后
    # --------------------------------------------------------------

    for image_path in remaining_images:

        relative = (
            make_relative_image_path(
                markdown_path,
                image_path
            )
        )

        output.append("")

        output.append(
            f"![{image_path.stem}]"
            f"({relative})"
        )

        output.append("")

    return "\n\n".join(
        output
    ).strip() + "\n"


# ======================================================================
# IMAGE REPORT PATH
# ======================================================================

def build_image_report_path(
    report_path
):

    return report_path.with_name(
        report_path.stem
        + "_带图.md"
    )


# ======================================================================
# MARKDOWN VALIDATION
# ======================================================================

def validate_image_order(
    content
):

    expected = [
        "首图.png",
        "插图1.png",
        "插图2.png",
        "插图3.png",
    ]

    found = []

    for name in expected:

        if name in content:

            found.append(name)

    # 首图必须存在
    if not found:

        raise RuntimeError(
            "No image references found."
        )

    if found[0] != "首图.png":

        raise RuntimeError(
            "Cover image is not first."
        )

    # 顺序必须正确
    positions = [
        expected.index(name)
        for name in found
    ]

    if positions != sorted(positions):

        raise RuntimeError(
            "Image order validation failed."
        )


def validate_body_interleaving(
    content
):

    image_pattern = re.compile(
        r"!\[[^\]]*\]\([^)]+\.(?:png|jpg|jpeg|webp)\)",
        re.I
    )

    parts = image_pattern.split(
        content
    )

    # 图片少于两张时没有必要检查
    if len(parts) <= 2:

        return

    for part in parts[1:-1]:

        if part.strip():

            return

    # 如果所有图片连续出现
    raise RuntimeError(
        "Images are not interleaved with "
        "body content."
    )


def validate_image_report(
    markdown_path,
    original_content
):

    content = markdown_path.read_text(
        encoding="utf-8"
    )

    # --------------------------------------------------------------
    # 图片存在
    # --------------------------------------------------------------

    image_references = re.findall(
        r"!\[[^\]]*\]\(([^)]+)\)",
        content
    )

    if len(image_references) < MIN_IMAGE_COUNT:

        raise RuntimeError(
            "Image report contains fewer "
            "than 3 image references."
        )

    # --------------------------------------------------------------
    # 每个引用必须存在
    # --------------------------------------------------------------

    for relative in image_references:

        image_path = (
            markdown_path.parent
            / relative
        ).resolve()

        if not image_path.exists():

            raise RuntimeError(
                f"Referenced image missing: "
                f"{relative}"
            )

        if not is_valid_png(
            image_path
        ):

            raise RuntimeError(
                f"Referenced image invalid: "
                f"{relative}"
            )

    # --------------------------------------------------------------
    # 顺序
    # --------------------------------------------------------------

    validate_image_order(
        content
    )

    # --------------------------------------------------------------
    # 正文穿插
    # --------------------------------------------------------------

    validate_body_interleaving(
        content
    )

    # --------------------------------------------------------------
    # 首图必须是第一内容
    # --------------------------------------------------------------

    stripped = content.lstrip()

    if not stripped.startswith(
        "![首图]"
    ):

        raise RuntimeError(
            "Cover image is not the first "
            "content of the image report."
        )

    # --------------------------------------------------------------
    # 原始正文必须仍然存在
    # --------------------------------------------------------------

    normalized_original = (
        re.sub(
            r"\s+",
            " ",
            original_content
        ).strip()
    )

    content_without_images = re.sub(
        r"!\[[^\]]*\]\([^)]+\)",
        "",
        content
    )

    normalized_result = (
        re.sub(
            r"\s+",
            " ",
            content_without_images
        ).strip()
    )

    if normalized_original:

        if normalized_original not in normalized_result:

            raise RuntimeError(
                "Original report body was "
                "altered or lost."
            )


# ======================================================================
# CREATE IMAGE REPORT
# ======================================================================

def create_image_report(
    report_path,
    image_dir,
    original_content
):

    output_path = (
        build_image_report_path(
            report_path
        )
    )

    content = build_image_markdown(
        output_path,
        original_content,
        image_dir
    )

    atomic_write_text(
        output_path,
        content
    )

    validate_image_report(
        output_path,
        original_content
    )

    log(
        f"Image report created: "
        f"{output_path}"
    )

    return output_path


# ======================================================================
# DAILY
# ======================================================================

def process_daily_report(
    target_date
):

    log("")
    log("=" * 70)
    log(
        f"DAILY IMAGE REPORT: "
        f"{target_date}"
    )
    log("=" * 70)

    report_path = find_daily_report(
        target_date
    )

    if not report_path:

        log(
            "Daily report not found."
        )

        return False

    original_content = read_report(
        report_path
    )

    title = extract_report_title(
        original_content
    )

    log(
        f"Report: {report_path}"
    )

    log(
        f"Title: {title}"
    )

    image_dir = daily_image_dir(
        target_date
    )

    generate_missing_images(
        image_dir,
        original_content
    )

    output_path = create_image_report(
        report_path,
        image_dir,
        original_content
    )

    log(
        f"SUCCESS: {output_path}"
    )

    return True


# ======================================================================
# WEEKLY
# ======================================================================

def process_weekly_report(
    year,
    week
):

    log("")
    log("=" * 70)
    log(
        f"WEEKLY IMAGE REPORT: "
        f"{year}-W{week:02d}"
    )
    log("=" * 70)

    report_path = find_weekly_report(
        year,
        week
    )

    if not report_path:

        log(
            "Weekly report not found."
        )

        return False

    original_content = read_report(
        report_path
    )

    title = extract_report_title(
        original_content
    )

    log(
        f"Report: {report_path}"
    )

    log(
        f"Title: {title}"
    )

    image_dir = weekly_image_dir(
        year,
        week
    )

    generate_missing_images(
        image_dir,
        original_content
    )

    output_path = create_image_report(
        report_path,
        image_dir,
        original_content
    )

    log(
        f"SUCCESS: {output_path}"
    )

    return True


# ======================================================================
# MAIN
# ======================================================================

def main():

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE IMAGE ENGINE V3")
    log("=" * 70)

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
        f"UTC TODAY     : {today}"
    )

    log(
        f"DAY BEFORE    : {day_before}"
    )

    log(
        f"YESTERDAY     : {yesterday}"
    )

    log(
        f"TODAY         : {today}"
    )

    # ==============================================================
    # DAILY
    # ==============================================================

    daily_dates = [
        day_before,
        yesterday,
        today,
    ]

    for target_date in daily_dates:

        try:

            process_daily_report(
                target_date
            )

        except Exception as exc:

            log(
                f"DAILY FAILED "
                f"{target_date}: {exc}"
            )

    # ==============================================================
    # WEEKLY
    # ==============================================================

    weeks = []

    for target_date in daily_dates:

        iso = target_date.isocalendar()

        key = (
            iso.year,
            iso.week
        )

        if key not in weeks:

            weeks.append(key)

    for year, week in weeks:

        try:

            process_weekly_report(
                year,
                week
            )

        except Exception as exc:

            log(
                f"WEEKLY FAILED "
                f"{year}-W{week:02d}: "
                f"{exc}"
            )

    log("")
    log("=" * 70)
    log(
        "748686 KNOWLEDGE IMAGE ENGINE V3 FINISHED"
    )
    log("=" * 70)

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )
