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
动态调用 27 Skills
   ↓
知识分析
   ↓
日报 / 知识卡片 / 专题候选 / 追踪事项

核心原则：

1. Enriched 优先于 Horizon Summary
2. source_status=fetched 时优先使用真实原文
3. pending_search / fetch_failed 不得伪装成原文
4. 不再固定只使用 5 个 Skills
5. 根据 skill_routes.json 动态选择 Skills
6. 不要求每条新闻调用全部 27 Skills
7. 自动提取人物、公司、产品、技术、行业、概念
8. 自动生成长期知识卡片
9. 自动生成专题候选
10. 自动生成后续追踪事项
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen


# ============================================================
# 路径
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

CONFIG_FILE = SYSTEM / "system_config.json"
ROUTES_FILE = SYSTEM / "skill_routes.json"


# ============================================================
# 时间
# ============================================================

def now():
    return datetime.now(
        timezone(timedelta(hours=8))
    )


# ============================================================
# JSON
# ============================================================

def read_json(path: Path, default=None):

    if default is None:
        default = {}

    try:
        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:

        print(
            f"⚠️ JSON读取失败: {path}"
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
    temperature: float = 0.2,
):

    api_key = os.getenv(
        "AI_API_KEY",
        ""
    )

    base_url = os.getenv(
        "AI_BASE_URL",
        "https://api.openai.com/v1"
    ).rstrip("/")

    model = os.getenv(
        "AI_MODEL",
        ""
    )

    if not api_key:

        raise RuntimeError(
            "缺少 AI_API_KEY"
        )

    if not model:

        raise RuntimeError(
            "缺少 AI_MODEL"
        )

    if not system_prompt:

        system_prompt = (
            "你是748686自生长知识系统的知识工程师。"
            "严格依据输入内容。"
            "不得编造事实。"
            "如果资料不足，明确说明资料不足。"
            "输出标准Markdown。"
        )

    payload = json.dumps(
        {
            "model": model,
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
        },
        ensure_ascii=False,
    ).encode("utf-8")

    request = Request(
        base_url + "/chat/completions",
        data=payload,
        headers={
            "Authorization":
                f"Bearer {api_key}",
            "Content-Type":
                "application/json",
        },
    )

    with urlopen(
        request,
        timeout=180,
    ) as response:

        data = json.loads(
            response.read().decode(
                "utf-8"
            )
        )

    try:

        return data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    except Exception:

        raise RuntimeError(
            "AI返回格式异常："
            + json.dumps(
                data,
                ensure_ascii=False
            )[:2000]
        )


# ============================================================
# Skills
# ============================================================

def load_skills():

    skills = {}

    if not SKILLS.exists():

        raise RuntimeError(
            f"Skills目录不存在：{SKILLS}"
        )

    for path in SKILLS.rglob("*.md"):

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
# 获取当天 Enriched
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

{json.dumps(categories, ensure_ascii=False)}

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
"""

    result = call_ai(
        prompt,
        system_prompt=(
            "你是748686知识系统的新闻分类器。"
            "只依据输入判断。"
            "必须返回合法JSON。"
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

            category = "新闻"

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
            "⚠️ 分类JSON解析失败，默认使用新闻"
        )

        return {
            "category": "新闻",
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
2. source_status不是fetched时，不得声称已经阅读完整原文。
3. 不得编造人物、公司、数字、事件。
4. 不确定的信息必须明确标记。
5. 如果资料不足，直接说明。

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
            "必须输出结构化Markdown。"
        ),
        temperature=0.2,
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
        temperature=0.2,
    )


# ============================================================
# 生成专题候选
# ============================================================

def generate_topics(
    date,
    analyses,
):

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

---

至少生成3个，最多10个。
"""

    return call_ai(
        prompt,
        system_prompt=(
            "你是战略研究员。"
            "从新闻之间寻找长期主题。"
            "不得编造事实。"
        ),
        temperature=0.2,
    )


# ============================================================
# 生成追踪事项
# ============================================================

def generate_watchlist(
    date,
    analyses,
):

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
"""

    return call_ai(
        prompt,
        system_prompt=(
            "你是新闻趋势追踪分析师。"
            "只根据已有资料判断。"
        ),
        temperature=0.2,
    )


# ============================================================
# 写入知识卡片
# ============================================================

def save_entity_knowledge(
    date,
    knowledge,
):

    target = (
        KNOWLEDGE
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%Y")
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%m")
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
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%Y")
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%m")
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
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%Y")
        / datetime.strptime(
            date,
            "%Y-%m-%d"
        ).strftime("%m")
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

    sections.append(
        knowledge
    )

    sections.append(
        topics
    )

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
# 主流程
# ============================================================

def main():

    current = now()

    date = current.strftime(
        "%Y-%m-%d"
    )

    print("=" * 70)

    print(
        "748686 KNOWLEDGE PIPELINE V2"
    )

    print("=" * 70)

    print(
        f"Date: {date}"
    )

    print()

    # --------------------------------------------------------
    # 创建目录
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 加载配置
    # --------------------------------------------------------

    config = read_json(
        CONFIG_FILE,
        {}
    )

    routes = load_routes()

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

    # --------------------------------------------------------
    # 获取 Enriched
    # --------------------------------------------------------

    files = get_enriched_files(
        date
    )

    print(
        f"Enriched files: {len(files)}"
    )

    if not files:

        raise RuntimeError(
            "当天没有Enriched新闻"
        )

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

        except Exception as exc:

            print(
                f"⚠️ 新闻读取失败：{path}"
            )

            print(exc)

    print(
        f"Valid news: {len(news_items)}"
    )

    # --------------------------------------------------------
    # 限制 AI 新闻数量
    # --------------------------------------------------------

    max_items = int(
        config.get(
            "max_items_for_ai",
            30
        )
    )

    # Horizon score优先
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

    news_items = news_items[
        :max_items
    ]

    print(
        f"AI items: {len(news_items)}"
    )

    # --------------------------------------------------------
    # 分类 + Skills分析
    # --------------------------------------------------------

    categories = list(
        routes.keys()
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
        # 路由 Skills
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

            continue

        # ----------------------------------------------------
        # 分析
        # ----------------------------------------------------

        analysis = analyze_with_skills(
            item,
            category,
            selected_skills
        )

        # ----------------------------------------------------
        # 保存来源信息
        # ----------------------------------------------------

        header = f"""
---

# {title}

> 分类：{category}
>
> 来源：{metadata.get("source", "Unknown")}
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

    if not analyses:

        raise RuntimeError(
            "没有生成任何新闻分析"
        )

    # --------------------------------------------------------
    # 知识卡片
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        "Generating knowledge cards..."
    )

    knowledge = generate_knowledge_cards(
        date,
        analyses
    )

    knowledge_path = save_entity_knowledge(
        date,
        knowledge
    )

    # --------------------------------------------------------
    # 专题
    # --------------------------------------------------------

    print(
        "Generating topic candidates..."
    )

    topics = generate_topics(
        date,
        analyses
    )

    topic_path = save_topics(
        date,
        topics
    )

    # --------------------------------------------------------
    # 追踪
    # --------------------------------------------------------

    print(
        "Generating watchlist..."
    )

    watchlist = generate_watchlist(
        date,
        analyses
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

    # --------------------------------------------------------
    # 日志
    # --------------------------------------------------------

    log_path = (
        LOGS
        / f"{date}_knowledge_pipeline.md"
    )

    log = f"""# {date} Knowledge Pipeline V2

- 时间：{current.isoformat()}
- Enriched 新闻：{len(files)}
- AI处理新闻：{len(news_items)}
- 实际分析新闻：{len(analyses)}
- Skills数量：{len(skills)}
- 路由类别：{len(routes)}

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
"""

    log_path.write_text(
        log,
        encoding="utf-8"
    )

    print()
    print("=" * 70)

    print(
        "✅ KNOWLEDGE PIPELINE V2 COMPLETE"
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

    print()

    print(
        "DAILY_REPORT="
        + str(report_path)
    )


if __name__ == "__main__":

    main()
