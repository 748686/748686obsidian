#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V2

数据流：

Horizon
   ↓
Atomic News
   ↓
Source Enrichment
   ↓
Enriched News
   ↓
新闻分类
   ↓
skill_routes.json
   ↓
动态调用 Skills
   ↓
知识分析
   ↓
日报 / 知识卡片 / 专题候选 / 追踪事项


============================================================
核心原则
============================================================

1. Horizon 完全由 Horizon 自己的配置管理。
2. 本程序不读取 Horizon Config。
3. 本程序不负责启动 Horizon。
4. 本程序只处理已经进入本系统的 Enriched News。
5. AI 使用 AGNES.ai。
6. AGNES API Key 从环境变量 AGNES_API_KEY 读取。
7. AGNES 模型固定为 agnes-2.5-flash。
8. AGNES Base URL 固定为 https://api.agnes-ai.cn/v1。
9. 不人为设置 max_tokens。
10. 日期统一使用北京时间 Asia/Shanghai。
11. Enriched 优先于 Horizon Summary。
12. source_status=fetched 时可以使用真实抓取内容。
13. pending_search / fetch_failed 不得伪装成原文。
14. Skills 根据 skill_routes.json 动态选择。
15. 不要求每条新闻调用全部 Skills。
16. 自动提取长期知识实体。
17. 自动生成专题候选。
18. 自动生成后续追踪事项。
19. 任意关键 AI 步骤失败，程序立即失败。
20. 不允许半成品被标记为成功。
21. 不限制当天新闻处理数量，所有有效 Enriched News 全部处理。
22. 每次运行检查前天、昨天、今天三个日期。
23. 三个日期必须分别独立处理，不合并成一个批次。
24. 某日期已经 SUCCESS，则跳过该日期。
25. 某日期没有 SUCCESS，则只处理该日期。
26. 处理顺序固定为：前天 → 昨天 → 今天。
"""

from __future__ import annotations

import json
import os
import re
import sys

from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ============================================================
# 基础路径
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

SYSTEM = ROOT / "00_System"
SKILLS = ROOT / "Skills"

RAW_NEWS = ROOT / "Raw News"

REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"
TOPICS = ROOT / "07_专题报告"
KNOWLEDGE = ROOT / "08_知识库"

LOGS = SYSTEM / "运行日志"

ROUTES_FILE = SYSTEM / "skill_routes.json"


# ============================================================
# AGNES AI
# ============================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"
AGNES_MODEL = "agnes-2.5-flash"

AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180


# ============================================================
# 北京时间
# ============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def now() -> datetime:
    """
    获取当前北京时间。
    """

    return datetime.now(BEIJING_TZ)


def today_str() -> str:
    """
    获取当前北京时间日期。
    """

    return now().strftime("%Y-%m-%d")


# ============================================================
# JSON
# ============================================================

def read_json(path: Path, default=None):

    if default is None:
        default = {}

    if not path.exists():

        print(
            f"⚠️ JSON文件不存在：{path}"
        )

        return default

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:

        print(
            f"⚠️ JSON读取失败：{path}"
        )

        print(exc)

        return default


# ============================================================
# 文件名安全处理
# ============================================================

def safe_name(text: str):

    text = str(text or "")

    text = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    text = text.strip()

    return text[:120] or "未命名"


# ============================================================
# Markdown Front Matter
# ============================================================

def parse_front_matter(content: str):

    if not content.startswith("---"):

        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:

        return {}, content

    raw = parts[1].strip()

    body = parts[2].lstrip()

    data = {}

    for line in raw.splitlines():

        if ":" not in line:

            continue

        key, value = line.split(
            ":",
            1
        )

        key = key.strip()

        value = value.strip()

        value = value.strip(
            '"'
        ).strip(
            "'"
        )

        data[key] = value

    return data, body


# ============================================================
# AI
# ============================================================

def call_ai(
    prompt: str,
    system_prompt: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
):
    """
    调用 AGNES.ai。

    不读取 system_config.json。

    AGNES 配置固定为：

        API KEY:
            AGNES_API_KEY

        Base URL:
            https://api.agnes-ai.cn/v1

        Model:
            agnes-2.5-flash

    不设置 max_tokens。
    """

    api_key = os.getenv(
        AGNES_API_KEY_ENV,
        ""
    ).strip()

    if not api_key:

        raise RuntimeError(
            "❌ 缺少 AGNES_API_KEY。"
            "请在 GitHub Actions Secrets 中配置 AGNES_API_KEY。"
        )

    if not system_prompt:

        system_prompt = (
            "你是748686自生长知识系统的知识工程师。"
            "严格依据输入内容。"
            "不得编造事实。"
            "如果资料不足，明确说明资料不足。"
            "输出标准Markdown。"
        )

    payload_data = {
        "model": AGNES_MODEL,

        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        "temperature": temperature,
    }

    payload = json.dumps(
        payload_data,
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        AGNES_BASE_URL + "/chat/completions",

        data=payload,

        headers={
            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json",

            "Accept":
                "application/json",

            "User-Agent":
                "748686-Knowledge-Pipeline/2.0",
        },

        method="POST",
    )

    print()
    print(
        "🤖 Calling AGNES.ai"
    )

    print(
        f"   Model: {AGNES_MODEL}"
    )

    print(
        f"   Base URL: {AGNES_BASE_URL}"
    )

    try:

        with urlopen(
            request,
            timeout=AI_TIMEOUT,
        ) as response:

            raw_response = (
                response
                .read()
                .decode("utf-8")
            )

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
            "❌ AGNES.ai HTTP错误\n"
            f"HTTP Status: {exc.code}\n"
            f"URL: {AGNES_BASE_URL}/chat/completions\n"
            f"Response: {error_body[:3000]}"
        ) from exc

    except URLError as exc:

        raise RuntimeError(
            "❌ AGNES.ai 网络连接失败\n"
            f"URL: {AGNES_BASE_URL}/chat/completions\n"
            f"Reason: {exc.reason}"
        ) from exc

    except TimeoutError as exc:

        raise RuntimeError(
            "❌ AGNES.ai 请求超时"
        ) from exc

    except Exception as exc:

        raise RuntimeError(
            "❌ AGNES.ai 请求失败\n"
            f"{type(exc).__name__}: {exc}"
        ) from exc

    try:

        data = json.loads(
            raw_response
        )

    except Exception as exc:

        raise RuntimeError(
            "❌ AGNES.ai 返回的不是合法JSON\n"
            f"Response: {raw_response[:3000]}"
        ) from exc

    try:

        result = data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    except Exception as exc:

        raise RuntimeError(
            "❌ AGNES.ai 返回格式异常\n"
            + json.dumps(
                data,
                ensure_ascii=False
            )[:5000]
        ) from exc

    if not result or not str(result).strip():

        raise RuntimeError(
            "❌ AGNES.ai 返回空内容"
        )

    return str(result).strip()


# ============================================================
# Skills
# ============================================================

def load_skills():

    skills = {}

    if not SKILLS.exists():

        raise RuntimeError(
            f"Skills目录不存在：{SKILLS}"
        )

    for path in sorted(
        SKILLS.rglob("*.md")
    ):

        try:

            content = path.read_text(
                encoding="utf-8"
            )

            skills[path.name] = {
                "name": path.name,
                "path": str(path),
                "content": content,
            }

        except Exception as exc:

            print(
                f"⚠️ Skill读取失败：{path}"
            )

            print(exc)

    return skills


# ============================================================
# Skill Routes
# ============================================================

def load_routes():

    routes = read_json(
        ROUTES_FILE,
        {}
    )

    if not routes:

        raise RuntimeError(
            "skill_routes.json为空或不存在"
        )

    return routes


# ============================================================
# 根据类别选择 Skills
# ============================================================

def route_skills(
    category: str,
    routes: dict,
    skills: dict,
):

    selected_names = routes.get(
        category,
        []
    )

    selected = []

    for name in selected_names:

        if name in skills:

            selected.append(
                skills[name]
            )

        else:

            print(
                f"⚠️ 路由中的Skill不存在：{name}"
            )

    return selected


# ============================================================
# 获取指定日期 Enriched
# ============================================================

def get_enriched_files(date: str):

    root = (
        RAW_NEWS
        / f"{date}-Enriched"
    )

    if not root.exists():

        raise FileNotFoundError(
            f"没有找到 Enriched目录：{root}"
        )

    files = sorted(
        root.rglob("*.md")
    )

    return files


# ============================================================
# 新闻记录
# ============================================================

def load_news_file(path: Path):

    content = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    metadata, body = parse_front_matter(
        content
    )

    return {
        "path": path,
        "metadata": metadata,
        "body": body,
        "content": content,
    }


# ============================================================
# 判断是否为有效新闻
# ============================================================

def is_news(item):

    metadata = item["metadata"]

    title = metadata.get(
        "title",
        ""
    ).strip()

    if not title:

        return False

    return True


# ============================================================
# AI：新闻分类
# ============================================================

def classify_news(
    item,
    categories,
):

    metadata = item["metadata"]

    title = metadata.get(
        "title",
        ""
    )

    source = metadata.get(
        "source",
        "Unknown"
    )

    body = item["body"]

    prompt = f"""
请判断下面这条新闻最适合进入哪个知识分析类别。

可选类别：

{json.dumps(
    categories,
    ensure_ascii=False
)}

新闻标题：
{title}

来源：
{source}

新闻内容：
{body[:12000]}

只输出JSON：

{{
  "category": "类别名称",
  "confidence": 0.0,
  "reason": "一句话原因"
}}

要求：

1. category必须来自给出的类别。
2. confidence范围0到1。
3. 不得创造新的类别。
4. 不要输出JSON之外的内容。
"""

    result = call_ai(
        prompt,

        system_prompt=(
            "你是748686知识系统的新闻分类器。"
            "只依据输入判断。"
            "必须返回合法JSON。"
            "不要输出JSON之外的解释。"
        ),

        temperature=0,
    )

    try:

        data = json.loads(
            result
        )

        category = data.get(
            "category",
            "新闻"
        )

        if category not in categories:

            category = (
                "新闻"
                if "新闻" in categories
                else categories[0]
            )

        return {
            "category": category,

            "confidence": data.get(
                "confidence",
                0
            ),

            "reason": data.get(
                "reason",
                ""
            ),
        }

    except Exception:

        print(
            "⚠️ 分类JSON解析失败"
        )

        print(
            "AI原始返回："
        )

        print(
            result[:2000]
        )

        fallback_category = (
            "新闻"
            if "新闻" in categories
            else categories[0]
        )

        return {
            "category": fallback_category,
            "confidence": 0,
            "reason": "AI分类结果解析失败",
        }


# ============================================================
# AI：动态 Skills 分析
# ============================================================

def analyze_with_skills(
    item,
    category,
    selected_skills,
):

    metadata = item["metadata"]

    title = metadata.get(
        "title",
        ""
    )

    source = metadata.get(
        "source",
        "Unknown"
    )

    source_url = metadata.get(
        "source_url",
        ""
    )

    source_status = metadata.get(
        "source_status",
        ""
    )

    content_status = metadata.get(
        "content_status",
        ""
    )

    body = item["body"]

    skill_text = []

    for skill in selected_skills:

        skill_text.append(
            f"""
## SKILL: {skill["name"]}

{skill["content"][:12000]}
"""
        )

    joined_skills = "\n\n".join(
        skill_text
    )

    prompt = f"""
# 新闻分析任务

日期：
{metadata.get("date", "")}

标题：
{title}

来源：
{source}

原文链接：
{source_url}

来源状态：
{source_status}

内容状态：
{content_status}

知识类别：
{category}

---

## 新闻内容

{body[:30000]}

---

## 本次使用的 Skills

{joined_skills[:40000]}

---

请根据以上资料进行深度知识分析。

必须严格遵守：

1. 不得把 Horizon 摘要写成原文。
2. source_status 不是 fetched 时，不得声称已经阅读完整原文。
3. 不得编造人物、公司、数字、事件。
4. 不确定的信息必须明确标记。
5. 如果资料不足，直接说明资料不足。
6. 所有结论必须能够在输入资料中找到依据。
7. 不要因为使用了 Skill 就自行增加输入资料中不存在的事实。

请输出以下结构：

# 事件分析

## 1. 核心事实

## 2. 事件背景

## 3. 为什么重要

## 4. 影响

### 短期影响

### 中期影响

### 长期影响

## 5. 趋势判断

## 6. 机会

## 7. 风险

## 8. 关键实体

使用表格：

| 类型 | 名称 | 说明 |
|---|---|---|
| 人物 | | |
| 公司 | | |
| 产品 | | |
| 技术 | | |
| 行业 | | |
| 概念 | | |

## 9. 值得长期保存的知识

## 10. 后续追踪

## 11. 可生成专题
"""

    return call_ai(
        prompt,

        system_prompt=(
            "你是748686自生长知识系统的高级知识工程师。"
            "必须严格依据资料。"
            "绝不把摘要冒充原文。"
            "不得编造事实。"
            "必须输出结构化Markdown。"
        ),

        temperature=0.3,
    )


# ============================================================
# 生成知识卡片
# ============================================================

def generate_knowledge_cards(
    date,
    analyses,
):

    if not analyses:

        return ""

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

下面是今天已经完成的新闻知识分析：

{joined[:60000]}

请提取真正值得进入长期知识库的知识实体。

重点提取：

- 人物
- 公司
- 产品
- 技术
- 行业
- 概念
- 方法
- 战略
- 长期趋势

不要把普通新闻事件全部做成知识卡片。

只保留具有长期价值的实体。

不要编造不存在的实体。

输出：

# 今日知识卡片

## 人物

### 名称
- 身份：
- 核心信息：
- 与今日事件关系：
- 长期价值：

## 公司

### 名称
- 公司：
- 核心业务：
- 今日事件：
- 长期价值：

## 技术

### 名称
- 定义：
- 当前进展：
- 应用：
- 长期价值：

## 行业

### 名称
- 当前变化：
- 驱动因素：
- 风险：
- 长期趋势：

## 概念

### 名称
- 定义：
- 关键特征：
- 实际案例：
- 长期意义：
"""

    return call_ai(
        prompt,

        system_prompt=(
            "你是长期知识库构建专家。"
            "只提取真正具有长期价值的知识。"
            "不要编造实体。"
            "输出中文Markdown。"
        ),

        temperature=0.3,
    )


# ============================================================
# 生成专题候选
# ============================================================

def generate_topics(
    date,
    analyses,
):

    if not analyses:

        return ""

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

以下是今天新闻分析：

{joined[:60000]}

请寻找值得进一步研究的专题。

要求：

1. 不要简单重复新闻标题。
2. 必须存在跨新闻的共同主题。
3. 优先选择未来仍然具有研究价值的主题。
4. 给出研究问题。
5. 给出为什么值得研究。
6. 给出需要继续寻找的数据或资料。
7. 不得编造事实。
8. 如果今天资料不足以形成3个高质量专题，可以少于3个。
9. 不要为了凑数量而创造不存在的主题。

输出：

# 专题研究候选

## 1. 专题名称

### 核心问题

### 为什么值得研究

### 当前证据

### 需要继续寻找

### 可能涉及人物

### 可能涉及公司

### 可能涉及行业

### 可能涉及技术
"""

    return call_ai(
        prompt,

        system_prompt=(
            "你是战略研究员。"
            "从新闻之间寻找长期主题。"
            "不得编造事实。"
            "资料不足时明确说明。"
        ),

        temperature=0.3,
    )


# ============================================================
# 生成追踪事项
# ============================================================

def generate_watchlist(
    date,
    analyses,
):

    if not analyses:

        return ""

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

下面是今天的新闻分析：

{joined[:50000]}

请生成“未来值得继续追踪”的项目。

输出：

# 后续追踪

| 优先级 | 追踪事项 | 原因 | 下一步需要关注 |
|---|---|---|---|
| 高 | | | |
| 中 | | | |
| 低 | | | |

要求：

- 只选择真正可能继续发展的事件。
- 不要编造未来事件。
- “下一步需要关注”写成观察指标。
- 如果没有足够证据，不要强行生成。
"""

    return call_ai(
        prompt,

        system_prompt=(
            "你是新闻趋势追踪分析师。"
            "只根据已有资料判断。"
            "不得编造未来事件。"
        ),

        temperature=0.3,
    )


# ============================================================
# 判断指定日期是否已经完整处理
# ============================================================

def is_date_completed(date: str):

    log_path = (
        LOGS
        / f"{date}_knowledge_pipeline.md"
    )

    if not log_path.exists():

        return False

    try:

        content = log_path.read_text(
            encoding="utf-8",
            errors="replace"
        )

    except Exception:

        return False

    # 必须明确存在 SUCCESS
    # 才认为这一天已经完整处理。
    if re.search(
        r"(?m)^SUCCESS\s*$",
        content
    ):

        return True

    return False


# ============================================================
# 写入知识卡片
# ============================================================

def save_entity_knowledge(
    date,
    knowledge,
):

    target = (
        KNOWLEDGE
        / date[:4]
        / date[5:7]
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        target
        / f"{date}_知识卡片.md"
    )

    path.write_text(
        f"""---
date: {date}
type: knowledge_cards
status: generated
timezone: Asia/Shanghai
---

{knowledge}
""",
        encoding="utf-8"
    )

    return path


# ============================================================
# 写入专题候选
# ============================================================

def save_topics(
    date,
    topics,
):

    target = (
        TOPICS
        / date[:4]
        / date[5:7]
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        target
        / f"{date}_专题候选.md"
    )

    path.write_text(
        f"""---
date: {date}
type: topic_candidates
status: generated
timezone: Asia/Shanghai
---

{topics}
""",
        encoding="utf-8"
    )

    return path


# ============================================================
# 写入日报
# ============================================================

def save_daily_report(
    date,
    analyses,
    knowledge,
    topics,
    watchlist,
):

    target = (
        REPORTS
        / date[:4]
        / date[5:7]
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        target
        / f"{date}.md"
    )

    sections = []

    sections.append(
        f"# {date} 自生长知识日报"
    )

    sections.append(
        "\n\n---\n\n".join(
            analyses
        )
    )

    if knowledge:

        sections.append(
            knowledge
        )

    if topics:

        sections.append(
            topics
        )

    if watchlist:

        sections.append(
            watchlist
        )

    content = "\n\n".join(
        sections
    )

    path.write_text(
        content + "\n",
        encoding="utf-8"
    )

    return path


# ============================================================
# 处理单独一天
# ============================================================

def process_date(
    date,
    routes,
    skills,
):
    """
    独立处理某一天。

    注意：

    每个日期都是一个完全独立的处理单元。

    不会把多个日期的新闻合并。

    返回：

        True  = 本次实际完成处理
        False = 本次跳过
    """

    print()
    print("=" * 70)
    print(f"📅 CHECK DATE: {date}")
    print("=" * 70)

    # --------------------------------------------------------
    # 已经完成 → 跳过
    # --------------------------------------------------------

    if is_date_completed(date):

        print(
            f"✅ {date} 已经完整处理，跳过。"
        )

        return False

    print(
        f"🟡 {date} 尚未完成，需要处理。"
    )

    # --------------------------------------------------------
    # 获取当天 Enriched
    # --------------------------------------------------------

    try:

        files = get_enriched_files(
            date
        )

    except FileNotFoundError as exc:

        print(
            f"⚠️ {date} 暂无 Enriched："
            f"{exc}"
        )

        print(
            f"⏭️ 跳过 {date}，继续检查下一天。"
        )

        return False

    print(
        f"Enriched files: {len(files)}"
    )

    if not files:

        print(
            f"⚠️ {date} 没有 Enriched 新闻。"
        )

        print(
            f"⏭️ 跳过 {date}，继续检查下一天。"
        )

        return False

    # --------------------------------------------------------
    # 加载新闻
    # --------------------------------------------------------

    news_items = []

    for path in files:

        try:

            item = load_news_file(
                path
            )

            if is_news(item):

                news_items.append(
                    item
                )

            else:

                print(
                    f"⚠️ 跳过无标题文件：{path}"
                )

        except Exception as exc:

            print(
                f"⚠️ 新闻读取失败：{path}"
            )

            print(exc)

    print(
        f"Valid news: {len(news_items)}"
    )

    if not news_items:

        raise RuntimeError(
            f"{date} 没有有效新闻"
        )

    # --------------------------------------------------------
    # Horizon score
    #
    # 只负责排序。
    # 不负责限制新闻数量。
    # --------------------------------------------------------

    def score(item):

        try:

            return float(
                item["metadata"].get(
                    "horizon_score",
                    0
                )
            )

        except Exception:

            return 0

    news_items.sort(
        key=score,
        reverse=True
    )

    # --------------------------------------------------------
    # 所有有效新闻全部进入 AI
    # --------------------------------------------------------

    print(
        f"AI items: {len(news_items)}"
    )

    print(
        "News processing limit: NONE"
    )

    # --------------------------------------------------------
    # 分类 + Skills分析
    # --------------------------------------------------------

    categories = list(
        routes.keys()
    )

    if not categories:

        raise RuntimeError(
            "skill_routes.json没有任何类别"
        )

    analyses = []

    category_count = {}

    for index, item in enumerate(
        news_items,
        start=1
    ):

        metadata = item[
            "metadata"
        ]

        title = metadata.get(
            "title",
            "Untitled"
        )

        print()
        print(
            "=" * 70
        )

        print(
            f"[{index}/{len(news_items)}] {title}"
        )

        # ----------------------------------------------------
        # 分类
        # ----------------------------------------------------

        classification = classify_news(
            item,
            categories
        )

        category = classification[
            "category"
        ]

        print(
            f"Category: {category}"
        )

        # ----------------------------------------------------
        # 动态 Skills
        # ----------------------------------------------------

        selected_skills = route_skills(
            category,
            routes,
            skills
        )

        print(
            "Skills:"
        )

        for skill in selected_skills:

            print(
                f"  - {skill['name']}"
            )

        if not selected_skills:

            print(
                "⚠️ No Skills routed"
            )

            # 保持原逻辑：
            # 不把没有Skill路由的新闻伪装成分析成功。
            continue

        # ----------------------------------------------------
        # AI 深度分析
        # ----------------------------------------------------

        analysis = analyze_with_skills(
            item,
            category,
            selected_skills
        )

        if not analysis.strip():

            raise RuntimeError(
                f"新闻分析返回空内容：{title}"
            )

        # ----------------------------------------------------
        # 保存来源信息
        # ----------------------------------------------------

        header = f"""
---

# {title}

> 日期：{date}
>
> 分类：{category}
>
> 来源：{metadata.get("source", "Unknown")}
>
> 原文链接：{metadata.get("source_url", "")}
>
> 原文状态：{metadata.get("source_status", "")}
>
> 内容状态：{metadata.get("content_status", "")}

"""

        analyses.append(
            header + analysis
        )

        category_count[
            category
        ] = category_count.get(
            category,
            0
        ) + 1

    # --------------------------------------------------------
    # 验证分析结果
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        f"Successful analyses: {len(analyses)}"
    )

    if not analyses:

        raise RuntimeError(
            f"❌ {date} 没有生成任何新闻分析，停止该日期流程。"
        )

    # --------------------------------------------------------
    # 知识卡片
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        f"Generating knowledge cards for {date}..."
    )

    knowledge = generate_knowledge_cards(
        date,
        analyses
    )

    if not knowledge.strip():

        raise RuntimeError(
            f"❌ {date} 知识卡片生成失败：返回为空"
        )

    knowledge_path = save_entity_knowledge(
        date,
        knowledge
    )

    print(
        f"✅ Knowledge Cards: {knowledge_path}"
    )

    # --------------------------------------------------------
    # 专题候选
    # --------------------------------------------------------

    print(
        f"Generating topic candidates for {date}..."
    )

    topics = generate_topics(
        date,
        analyses
    )

    if not topics.strip():

        raise RuntimeError(
            f"❌ {date} 专题候选生成失败：返回为空"
        )

    topic_path = save_topics(
        date,
        topics
    )

    print(
        f"✅ Topics: {topic_path}"
    )

    # --------------------------------------------------------
    # 后续追踪
    # --------------------------------------------------------

    print(
        f"Generating watchlist for {date}..."
    )

    watchlist = generate_watchlist(
        date,
        analyses
    )

    if not watchlist.strip():

        raise RuntimeError(
            f"❌ {date} 后续追踪生成失败：返回为空"
        )

    # --------------------------------------------------------
    # 日报
    # --------------------------------------------------------

    report_path = save_daily_report(
        date,
        analyses,
        knowledge,
        topics,
        watchlist
    )

    if not report_path.exists():

        raise RuntimeError(
            f"❌ {date} 日报文件没有成功写入"
        )

    print(
        f"✅ Daily Report: {report_path}"
    )

    # --------------------------------------------------------
    # 日志
    # --------------------------------------------------------

    log_path = (
        LOGS
        / f"{date}_knowledge_pipeline.md"
    )

    current = now()

    log = f"""# {date} Knowledge Pipeline V2

- 时间：{current.isoformat()}
- 时区：Asia/Shanghai
- Enriched 新闻：{len(files)}
- AI处理新闻：{len(news_items)}
- 实际分析新闻：{len(analyses)}
- Skills数量：{len(skills)}
- 路由类别：{len(routes)}
- AI Provider：AGNES.ai
- AI Model：{AGNES_MODEL}

## 新闻处理模式

- 当日有效 Enriched News：全部处理
- 新闻数量上限：无
- Horizon Score：仅用于处理顺序，不用于截断
- 多日处理方式：逐日独立处理
- 当前日期单元：{date}

## 分类统计

"""

    for category, count in sorted(
        category_count.items()
    ):

        log += (
            f"- {category}: {count}\n"
        )

    log += f"""
## 输出

- 日报：{report_path}
- 知识卡片：{knowledge_path}
- 专题候选：{topic_path}

## 状态

SUCCESS

"""

    log_path.write_text(
        log,
        encoding="utf-8"
    )

    print(
        f"✅ Log: {log_path}"
    )

    # --------------------------------------------------------
    # 最终完成
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        f"✅ {date} KNOWLEDGE PIPELINE COMPLETE"
    )

    print("=" * 70)

    print(
        f"Daily Report : {report_path}"
    )

    print(
        f"Knowledge    : {knowledge_path}"
    )

    print(
        f"Topics       : {topic_path}"
    )

    print(
        f"Log          : {log_path}"
    )

    return True


# ============================================================
# 主流程
# ============================================================

def main():

    current = now()

    today = current.date()

    # ========================================================
    # 三天窗口
    #
    # 固定为：
    #
    # 前天
    # 昨天
    # 今天
    #
    # 并且严格按照：
    #
    # 前天 → 昨天 → 今天
    #
    # 每一天都是独立处理单元。
    # ========================================================

    target_dates = [
        (today - timedelta(days=2)).strftime("%Y-%m-%d"),
        (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        today.strftime("%Y-%m-%d"),
    ]

    print("=" * 70)

    print(
        "748686 KNOWLEDGE PIPELINE V2"
    )

    print("=" * 70)

    print(
        f"Current Date: {today.strftime('%Y-%m-%d')}"
    )

    print(
        f"Timezone: {current.tzinfo}"
    )

    print(
        "AI Provider: AGNES.ai"
    )

    print(
        f"AI Model: {AGNES_MODEL}"
    )

    print()

    print(
        "Three-Day Processing Window:"
    )

    for index, date in enumerate(
        target_dates,
        start=1
    ):

        label = {
            1: "前天",
            2: "昨天",
            3: "今天",
        }[index]

        print(
            f"  {label}: {date}"
        )

    print()

    print(
        "Processing Mode:"
    )

    print(
        "  每一天独立处理"
    )

    print(
        "  不合并三天新闻"
    )

    print(
        "  已 SUCCESS → 跳过"
    )

    print(
        "  未 SUCCESS → 完整处理"
    )

    print(
        "  顺序：前天 → 昨天 → 今天"
    )

    print()

    # ========================================================
    # 创建输出目录
    # ========================================================

    for directory in [
        REPORTS,
        WEEKLY,
        TOPICS,
        KNOWLEDGE,
        LOGS,
    ]:

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

    # ========================================================
    # 加载 Routes
    # ========================================================

    routes = load_routes()

    # ========================================================
    # 加载 Skills
    # ========================================================

    skills = load_skills()

    print(
        f"Loaded Skills: {len(skills)}"
    )

    print(
        f"Loaded Routes: {len(routes)}"
    )

    if len(skills) < 27:

        print(
            "⚠️ 警告：当前Skills数量少于27"
        )

    # ========================================================
    # 检查 AGNES API Key
    #
    # 在真正开始处理新闻之前检查。
    # ========================================================

    if not os.getenv(
        AGNES_API_KEY_ENV,
        ""
    ).strip():

        raise RuntimeError(
            "❌ 未检测到 AGNES_API_KEY。"
        )

    print(
        "✅ AGNES_API_KEY detected"
    )

    # ========================================================
    # 逐日处理
    #
    # 非常重要：
    #
    # 不是三天合并。
    #
    # 而是：
    #
    # 28号 → 完整处理 / 跳过
    # 29号 → 完整处理 / 跳过
    # 30号 → 完整处理 / 跳过
    # ========================================================

    processed_dates = []
    skipped_dates = []

    for date in target_dates:

        try:

            result = process_date(
                date,
                routes,
                skills
            )

            if result:

                processed_dates.append(
                    date
                )

            else:

                skipped_dates.append(
                    date
                )

        except Exception as exc:

            print()
            print(
                "=" * 70
            )

            print(
                f"❌ {date} PROCESSING FAILED"
            )

            print("=" * 70)

            print(
                f"{type(exc).__name__}: {exc}"
            )

            print()

            # 任意一个需要处理的日期失败，
            # 整个GitHub Actions运行失败。
            #
            # 不允许继续伪装成成功。

            raise

    # ========================================================
    # 三天检查完成
    # ========================================================

    print()
    print(
        "=" * 70
    )

    print(
        "THREE-DAY KNOWLEDGE PIPELINE CHECK COMPLETE"
    )

    print("=" * 70)

    print()

    print(
        "实际处理日期："
    )

    if processed_dates:

        for date in processed_dates:

            print(
                f"  ✅ {date}"
            )

    else:

        print(
            "  无"
        )

    print()

    print(
        "已经完成、跳过日期："
    )

    if skipped_dates:

        for date in skipped_dates:

            print(
                f"  ⏭️ {date}"
            )

    else:

        print(
            "  无"
        )

    print()

    print(
        "处理规则："
    )

    print(
        "  前天 → 检查"
    )

    print(
        "  昨天 → 检查"
    )

    print(
        "  今天 → 检查"
    )

    print(
        "  已完成 → 跳过"
    )

    print(
        "  未完成 → 补处理"
    )

    print(
        "  三天不合并"
    )

    print()

    print(
        "✅ KNOWLEDGE PIPELINE V2 COMPLETE"
    )

    print("=" * 70)


# ============================================================
# 程序入口
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print(
            "❌ 用户中断程序"
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print(
            "=" * 70
        )

        print(
            "❌ KNOWLEDGE PIPELINE V2 FAILED"
        )

        print("=" * 70)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print()

        # 非0退出码非常重要：
        # GitHub Actions 会因此判断本次运行失败，
        # 不会把半成品误报成成功。

        sys.exit(1)
