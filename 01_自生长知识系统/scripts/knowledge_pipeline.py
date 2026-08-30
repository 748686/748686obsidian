#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V3

============================================================
核心数据流
============================================================

Horizon
   ↓
Atomic News
   ↓
Source Enrichment
   ↓
Enriched News
   ↓
============================================================
第二层 AI：跨来源 / 跨语言 / 同事件聚合
============================================================
400篇
   ↓
AI 第一轮批量事件聚类
   ↓
初步事件 Cluster
   ↓
AI 第二轮跨批次合并
   ↓
最终 Event Units
   ↓
可能：
400篇 → 50~150个 Event Units
   ↓
============================================================
第三层：事件知识提炼
============================================================
每个 Event Unit
   ↓
AI 综合所有来源
   ↓
形成一个高质量聚合知识单元
   ↓
============================================================
第四层：Knowledge Skills
============================================================
事件分类
   ↓
skill_routes.json
   ↓
动态选择 Skills
   ↓
深度知识分析
   ↓
============================================================
第五层：知识输出
============================================================
知识卡片
专题候选
后续追踪
日报


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
11. 不限制当天 Enriched News 数量。
12. 所有有效 Enriched News 都进入聚合层。
13. 聚合层允许跨来源。
14. 聚合层允许跨语言。
15. 同一现实世界事件应尽量归并。
16. 不同事件不得因为关键词相似而强行合并。
17. 同一事件的不同国家、媒体、语言报道必须保留来源关系。
18. 聚合后才进入 Skills。
19. Skills 不再逐篇处理原始新闻。
20. 每个聚合事件只进入一次深度分析。
21. 不要求每个事件调用全部 Skills。
22. Skills 根据 skill_routes.json 动态选择。
23. 自动提取长期知识实体。
24. 自动生成专题候选。
25. 自动生成后续追踪事项。
26. 任意关键 AI 步骤失败，程序立即失败。
27. 不允许半成品被标记为 SUCCESS。
28. 每次运行检查前天、昨天、今天。
29. 三个日期分别独立处理。
30. 某日期已经 SUCCESS，则跳过。
31. 某日期没有 SUCCESS，则只处理该日期。
32. 固定顺序：前天 → 昨天 → 今天。


============================================================
聚合架构
============================================================

第一阶段：

400篇 Enriched
   ↓
每批最多 40 篇
   ↓
AI 判断同一事件
   ↓
Cluster

第二阶段：

所有 Cluster
   ↓
AI 跨批次合并
   ↓
Final Event Units

第三阶段：

Final Event Unit
   ↓
AI 综合全部来源
   ↓
Aggregated Knowledge

第四阶段：

Aggregated Knowledge
   ↓
分类
   ↓
Skills
   ↓
深度分析


============================================================
重要说明
============================================================

这里的“聚合”不是简单删除重复新闻。

例如：

美国媒体：
某公司发布新AI芯片

英国媒体：
某公司AI芯片获得监管批准

日本媒体：
该芯片进入日本市场

韩国媒体：
韩国企业与该公司合作

中国媒体：
该公司发布新一代AI芯片

如果 AI 判断这些属于同一个现实世界事件，

最终形成：

EVENT-001
某公司新一代AI芯片发布及全球市场布局

并保留：

- 美国来源
- 英国来源
- 日本来源
- 韩国来源
- 中国来源

以及各来源独有信息。

因此：

400篇
不等于
400个知识单元。

最终可能：

400篇
→ 180 Cluster
→ 100 Event Units

然后：

100 Event Units
→ Skills

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
# 聚合结果目录
# ============================================================

AGGREGATED_ROOT = RAW_NEWS


# ============================================================
# AGNES AI
# ============================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"

AGNES_MODEL = "agnes-2.5-flash"

AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180


# ============================================================
# 聚合参数
# ============================================================

# 每次第一轮聚合最多处理多少篇新闻。
#
# 400篇：
#
# 400 / 40 = 10批
#
# 不会一次性把400篇全部塞给模型。
#
AGGREGATION_BATCH_SIZE = 40


# 第二轮跨批次合并时，
# 每次最多处理多少 Cluster。
CLUSTER_MERGE_BATCH_SIZE = 30


# 单篇新闻用于“聚类判断”的最大字符数。
ARTICLE_CLUSTER_CONTENT_LIMIT = 3500


# 最终事件生成聚合内容时，
# 每篇来源最多提供多少字符。
ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000


# 防止一次事件因为异常来源过多而无限膨胀。
MAX_ARTICLES_PER_EVENT_CONTEXT = 30


# ============================================================
# 北京时间
# ============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def now() -> datetime:
    return datetime.now(BEIJING_TZ)


def today_str() -> str:
    return now().strftime("%Y-%m-%d")


# ============================================================
# JSON
# ============================================================

def read_json(path: Path, default=None):

    if default is None:
        default = {}

    if not path.exists():

        print(f"⚠️ JSON文件不存在：{path}")

        return default

    try:

        return json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

    except Exception as exc:

        raise RuntimeError(
            f"❌ JSON读取失败：{path}\n{exc}"
        ) from exc


def parse_ai_json(result: str, context: str):

    """
    严格解析 AI JSON。

    与旧版本不同：

    不再 silently fallback。

    因为：

        AI步骤失败
            ↓
        必须让整个Pipeline失败

    防止半成品被标记SUCCESS。
    """

    text = str(result).strip()

    # 去除可能出现的 Markdown JSON fence
    if text.startswith("```"):

        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.IGNORECASE
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        )

        text = text.strip()

    try:

        return json.loads(text)

    except Exception as exc:

        raise RuntimeError(
            f"❌ AI JSON解析失败：{context}\n\n"
            f"AI原始返回：\n{text[:5000]}"
        ) from exc


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

        value = value.strip('"').strip("'")

        data[key] = value

    return data, body


# ============================================================
# AGNES AI
# ============================================================

def call_ai(
    prompt: str,
    system_prompt: str | None = None,
    temperature: float = DEFAULT_TEMPERATURE,
):
    """
    调用 AGNES.ai。

    固定：

        Base URL:
            https://api.agnes-ai.cn/v1

        Model:
            agnes-2.5-flash

        API Key:
            AGNES_API_KEY

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
                "748686-Knowledge-Pipeline/3.0",
        },

        method="POST",
    )

    print()
    print("🤖 Calling AGNES.ai")
    print(f"   Model: {AGNES_MODEL}")
    print(f"   Base URL: {AGNES_BASE_URL}")

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

            raise RuntimeError(
                f"❌ Skill读取失败：{path}\n{exc}"
            ) from exc

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
# 动态选择 Skills
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

            raise RuntimeError(
                f"❌ skill_routes.json引用了不存在的Skill：{name}"
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
# 判断有效新闻
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
# 聚合：构造新闻简表
# ============================================================

def build_article_digest(
    item,
    index,
):

    metadata = item["metadata"]

    title = metadata.get(
        "title",
        "Untitled"
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

    return f"""
[ARTICLE {index}]

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

内容：
{body[:ARTICLE_CLUSTER_CONTENT_LIMIT]}
"""


# ============================================================
# 第一层 AI：批量事件聚类
# ============================================================

def cluster_news_batch(
    date,
    batch_items,
    batch_start_index,
):

    articles = []

    for offset, item in enumerate(
        batch_items
    ):

        global_index = (
            batch_start_index
            + offset
        )

        articles.append(
            build_article_digest(
                item,
                global_index
            )
        )

    joined = "\n\n".join(
        articles
    )

    prompt = f"""
你现在正在执行748686自生长知识系统的“第二层事件聚合”。

日期：
{date}

下面是本批新闻。

这些新闻已经经过：
Horizon
→ Atomic News
→ Source Enrichment

现在不要做最终深度知识分析。

你的任务只有一个：

============================================================
识别哪些新闻实际上属于同一个现实世界事件 / 情况
============================================================

必须考虑：

1. 不同国家媒体报道同一个事件。
2. 中文、英文、日文、韩文等不同语言报道同一个事件。
3. 标题完全不同但实际上是同一事件。
4. 同一个政策变化产生的不同报道。
5. 同一个公司动作产生的不同报道。
6. 同一个技术发布产生的不同报道。
7. 同一个市场变化产生的不同报道。
8. 同一个人物事件产生的不同报道。

不要仅仅因为：

- 关键词相同
- 公司名字相同
- 行业相同
- 国家相同

就强行合并。

例如：

“某公司发布新芯片”
和
“某公司三个月前的财报”

即使都是同一家公司，也不一定是同一个事件。

============================================================
聚合原则
============================================================

如果多个文章明显描述同一个现实世界事件：

放进同一个 cluster。

如果只是同一个行业、公司或主题，但不是同一事件：

必须分开。

如果无法确定：

宁可分开，不要错误合并。

============================================================
重要
============================================================

必须覆盖输入中的所有 ARTICLE。

每一篇 ARTICLE 都必须且只能属于一个 cluster。

如果某篇新闻无法与其他新闻合并：

它自己成为一个 cluster。

============================================================
输出
============================================================

只输出合法JSON。

格式：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1, 7, 13],
      "event_title": "简洁的事件名称",
      "event_reason": "为什么这些文章属于同一个现实世界事件"
    }},
    {{
      "cluster_id": "C002",
      "article_indexes": [2],
      "event_title": "独立事件",
      "event_reason": "该新闻与其他新闻不是同一事件"
    }}
  ]
}}

要求：

1. article_indexes必须来自输入。
2. 不得遗漏文章。
3. 不得重复文章。
4. 不得创造输入中不存在的ARTICLE编号。
5. cluster_id必须唯一。
6. event_title不要写成新闻标题堆砌。
7. event_reason简洁说明判断依据。
8. 只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是全球新闻事件聚类专家。"
            "你的任务是识别不同媒体、国家和语言报道的同一现实世界事件。"
            "不要进行深度知识分析。"
            "必须返回合法JSON。"
            "必须覆盖全部输入文章。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        f"{date} 第一轮新闻聚类"
    )

    clusters = data.get(
        "clusters"
    )

    if not isinstance(
        clusters,
        list
    ):

        raise RuntimeError(
            f"❌ {date} 第一轮聚类结果缺少clusters"
        )

    return clusters


# ============================================================
# 验证 Cluster 覆盖情况
# ============================================================

def validate_cluster_coverage(
    clusters,
    expected_indexes,
    context,
):

    expected = set(
        expected_indexes
    )

    actual = []

    for cluster in clusters:

        indexes = cluster.get(
            "article_indexes",
            []
        )

        if not isinstance(
            indexes,
            list
        ):

            raise RuntimeError(
                f"❌ {context} article_indexes不是数组"
            )

        actual.extend(
            indexes
        )

    actual_set = set(actual)

    duplicates = [
        index
        for index in actual
        if actual.count(index) > 1
    ]

    missing = sorted(
        expected - actual_set
    )

    extra = sorted(
        actual_set - expected
    )

    if duplicates:

        raise RuntimeError(
            f"❌ {context} 存在重复文章归属："
            f"{sorted(set(duplicates))}"
        )

    if missing:

        raise RuntimeError(
            f"❌ {context} 存在未被聚类的文章："
            f"{missing}"
        )

    if extra:

        raise RuntimeError(
            f"❌ {context} 出现不存在的文章编号："
            f"{extra}"
        )


# ============================================================
# 第二层：跨批次 Cluster 合并
# ============================================================

def merge_cluster_batch(
    date,
    clusters,
    merge_round,
    batch_index,
):

    descriptors = []

    for index, cluster in enumerate(
        clusters,
        start=1
    ):

        descriptors.append(
            f"""
[CLUSTER {index}]

cluster_id：
{cluster["cluster_id"]}

事件名称：
{cluster["event_title"]}

事件判断：
{cluster["event_reason"]}

包含文章：
{json.dumps(
    cluster.get("article_indexes", []),
    ensure_ascii=False
)}
"""
        )

    joined = "\n\n".join(
        descriptors
    )

    prompt = f"""
你现在执行748686自生长知识系统的“跨批次事件合并”。

日期：
{date}

这是第 {merge_round} 轮，第 {batch_index} 批。

下面不是原始新闻，而是已经完成第一轮AI聚类的事件Cluster。

你的任务：

判断这些Cluster中，哪些其实还是同一个现实世界事件。

例如：

Cluster A：
“某公司宣布推出新AI芯片”

Cluster B：
“该公司新AI芯片获得日本批准”

Cluster C：
“韩国企业与该公司新AI芯片合作”

如果这些事情明显属于同一连续事件 / 同一新闻主线：

可以合并。

但是：

Cluster A：
“某公司发布新芯片”

Cluster B：
“某公司去年第四季度财报”

虽然都是同一家公司：

不能因为公司相同就合并。

============================================================
原则
============================================================

1. 同事件 → 合并。
2. 同主题但不同事件 → 不合并。
3. 同公司但不同事件 → 不合并。
4. 同行业但不同事件 → 不合并。
5. 不确定 → 不合并。
6. 尽量避免错误合并。
7. 所有Cluster必须被覆盖。
8. 一个Cluster只能属于一个最终合并组。

============================================================
输出
============================================================

只输出合法JSON：

{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1, 4, 8],
      "event_title": "统一事件名称",
      "reason": "为什么这些Cluster属于同一个事件"
    }},
    {{
      "group_id": "G002",
      "cluster_indexes": [2],
      "event_title": "独立事件",
      "reason": "为什么不能与其他Cluster合并"
    }}
  ]
}}

必须：

- 覆盖全部CLUSTER。
- 不重复CLUSTER。
- 不遗漏CLUSTER。
- 不创造不存在的CLUSTER编号。
- 只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是跨来源新闻事件归并专家。"
            "重点识别同一个现实世界事件。"
            "宁可少合并，也不要错误合并。"
            "必须返回合法JSON。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        f"{date} 第{merge_round}轮跨批次聚合"
    )

    groups = data.get(
        "groups"
    )

    if not isinstance(
        groups,
        list
    ):

        raise RuntimeError(
            f"❌ {date} 跨批次合并缺少groups"
        )

    expected = set(
        range(
            1,
            len(clusters) + 1
        )
    )

    actual = []

    for group in groups:

        indexes = group.get(
            "cluster_indexes",
            []
        )

        actual.extend(
            indexes
        )

    if len(actual) != len(
        set(actual)
    ):

        raise RuntimeError(
            f"❌ {date} 跨批次合并存在重复Cluster"
        )

    if set(actual) != expected:

        missing = sorted(
            expected - set(actual)
        )

        extra = sorted(
            set(actual) - expected
        )

        raise RuntimeError(
            f"❌ {date} 跨批次合并覆盖异常\n"
            f"missing={missing}\n"
            f"extra={extra}"
        )

    return groups


# ============================================================
# 构建初步 Cluster
# ============================================================

def build_initial_clusters(
    date,
    news_items,
):

    all_clusters = []

    total = len(
        news_items
    )

    print()
    print("=" * 70)
    print("🧠 STAGE 1 — AI EVENT CLUSTERING")
    print("=" * 70)

    print(
        f"Input Enriched News: {total}"
    )

    print(
        f"Batch Size: {AGGREGATION_BATCH_SIZE}"
    )

    batch_number = 0

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE
    ):

        batch_number += 1

        end = min(
            start + AGGREGATION_BATCH_SIZE,
            total
        )

        batch_items = news_items[
            start:end
        ]

        print()
        print(
            f"🔹 Cluster Batch "
            f"{batch_number}: "
            f"{start + 1}-{end}/{total}"
        )

        clusters = cluster_news_batch(

            date,

            batch_items,

            start + 1
        )

        expected_indexes = list(
            range(
                start + 1,
                end + 1
            )
        )

        validate_cluster_coverage(

            clusters,

            expected_indexes,

            f"{date} 第一轮Batch {batch_number}"
        )

        for cluster in clusters:

            article_indexes = [
                int(index)
                for index in cluster[
                    "article_indexes"
                ]
            ]

            all_clusters.append({

                "cluster_id":
                    f"B{batch_number:03d}-"
                    f"{cluster['cluster_id']}",

                "event_title":
                    cluster.get(
                        "event_title",
                        "未命名事件"
                    ),

                "event_reason":
                    cluster.get(
                        "event_reason",
                        ""
                    ),

                "article_indexes":
                    article_indexes,
            })

        print(
            f"   Clusters generated: "
            f"{len(clusters)}"
        )

    print()
    print(
        f"✅ Initial Clusters: "
        f"{len(all_clusters)}"
    )

    return all_clusters


# ============================================================
# 跨批次合并所有 Cluster
# ============================================================

def merge_all_clusters(
    date,
    clusters,
):

    current = clusters

    merge_round = 1

    print()
    print("=" * 70)
    print("🧠 STAGE 2 — CROSS-BATCH EVENT MERGING")
    print("=" * 70)

    print(
        f"Initial Clusters: {len(current)}"
    )

    while len(current) > CLUSTER_MERGE_BATCH_SIZE:

        print()
        print(
            f"🔄 Merge Round {merge_round}"
        )

        next_level = []

        batch_number = 0

        for start in range(
            0,
            len(current),
            CLUSTER_MERGE_BATCH_SIZE
        ):

            batch_number += 1

            batch = current[
                start:
                start + CLUSTER_MERGE_BATCH_SIZE
            ]

            print(
                f"   Merge Batch "
                f"{batch_number}: "
                f"{start + 1}-"
                f"{start + len(batch)}"
            )

            groups = merge_cluster_batch(

                date,

                batch,

                merge_round,

                batch_number
            )

            for group in groups:

                merged_clusters = []

                for cluster_index in group[
                    "cluster_indexes"
                ]:

                    source_cluster = batch[
                        cluster_index - 1
                    ]

                    merged_clusters.append(
                        source_cluster
                    )

                article_indexes = []

                for cluster in merged_clusters:

                    article_indexes.extend(
                        cluster[
                            "article_indexes"
                        ]
                    )

                article_indexes = sorted(
                    set(
                        article_indexes
                    )
                )

                next_level.append({

                    "cluster_id":
                        f"R{merge_round:02d}-"
                        f"G{len(next_level) + 1:04d}",

                    "event_title":
                        group.get(
                            "event_title",
                            "未命名事件"
                        ),

                    "event_reason":
                        group.get(
                            "reason",
                            ""
                        ),

                    "article_indexes":
                        article_indexes,
                })

        print(
            f"   Result after round "
            f"{merge_round}: "
            f"{len(next_level)}"
        )

        current = next_level

        merge_round += 1

    # --------------------------------------------------------
    # 最后一次全局合并
    #
    # 此时通常已经 <= 30个Cluster。
    #
    # 直接进行一次完整跨Cluster判断。
    # --------------------------------------------------------

    if len(current) > 1:

        print()
        print(
            "🔄 Final Global Merge"
        )

        groups = merge_cluster_batch(

            date,

            current,

            merge_round,

            1
        )

        final_clusters = []

        for group_index, group in enumerate(
            groups,
            start=1
        ):

            article_indexes = []

            for cluster_index in group[
                "cluster_indexes"
            ]:

                article_indexes.extend(
                    current[
                        cluster_index - 1
                    ][
                        "article_indexes"
                    ]
                )

            final_clusters.append({

                "event_id":
                    f"EVT-{date}-"
                    f"{group_index:04d}",

                "event_title":
                    group.get(
                        "event_title",
                        "未命名事件"
                    ),

                "event_reason":
                    group.get(
                        "reason",
                        ""
                    ),

                "article_indexes":
                    sorted(
                        set(
                            article_indexes
                        )
                    ),
            })

    else:

        final_clusters = [

            {

                "event_id":
                    f"EVT-{date}-0001",

                "event_title":
                    current[0][
                        "event_title"
                    ],

                "event_reason":
                    current[0][
                        "event_reason"
                    ],

                "article_indexes":
                    sorted(
                        set(
                            current[0][
                                "article_indexes"
                            ]
                        )
                    ),
            }

        ]

    print()
    print(
        "=" * 70
    )

    print(
        f"✅ FINAL EVENT UNITS: "
        f"{len(final_clusters)}"
    )

    print(
        f"Original News: "
        f"{sum(len(c['article_indexes']) for c in final_clusters)}"
    )

    return final_clusters


# ============================================================
# 构建 Event Unit
# ============================================================

def build_event_units(
    date,
    final_clusters,
    news_items,
):

    events = []

    for cluster in final_clusters:

        article_indexes = cluster[
            "article_indexes"
        ]

        articles = []

        for index in article_indexes:

            if index < 1 or index > len(
                news_items
            ):

                raise RuntimeError(
                    f"❌ Event {cluster['event_id']} "
                    f"引用了不存在的文章：{index}"
                )

            item = news_items[
                index - 1
            ]

            metadata = item[
                "metadata"
            ]

            articles.append({

                "index": index,

                "path": str(
                    item["path"]
                ),

                "title":
                    metadata.get(
                        "title",
                        "Untitled"
                    ),

                "source":
                    metadata.get(
                        "source",
                        "Unknown"
                    ),

                "source_url":
                    metadata.get(
                        "source_url",
                        ""
                    ),

                "source_status":
                    metadata.get(
                        "source_status",
                        ""
                    ),

                "content_status":
                    metadata.get(
                        "content_status",
                        ""
                    ),

                "body":
                    item["body"],
            })

        events.append({

            "event_id":
                cluster["event_id"],

            "date":
                date,

            "event_title":
                cluster[
                    "event_title"
                ],

            "event_reason":
                cluster[
                    "event_reason"
                ],

            "articles":
                articles,
        })

    return events


# ============================================================
# 保存聚合结果
# ============================================================

def save_aggregation_index(
    date,
    events,
):

    target = (
        AGGREGATED_ROOT
        / f"{date}-Aggregated"
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    index_path = (
        target
        / "_event_index.json"
    )

    serializable = []

    for event in events:

        serializable.append({

            "event_id":
                event["event_id"],

            "date":
                event["date"],

            "event_title":
                event["event_title"],

            "event_reason":
                event["event_reason"],

            "article_count":
                len(
                    event["articles"]
                ),

            "articles": [

                {

                    "index":
                        article["index"],

                    "title":
                        article["title"],

                    "source":
                        article["source"],

                    "source_url":
                        article["source_url"],

                    "path":
                        article["path"],
                }

                for article in event[
                    "articles"
                ]

            ],
        })

    index_path.write_text(

        json.dumps(
            serializable,
            ensure_ascii=False,
            indent=2
        ),

        encoding="utf-8"
    )

    return index_path


# ============================================================
# 第三层：AI 综合同事件所有来源
# ============================================================

def synthesize_event(
    event,
):

    date = event["date"]

    event_id = event[
        "event_id"
    ]

    event_title = event[
        "event_title"
    ]

    articles = event[
        "articles"
    ]

    # 为防止极端情况输入无限膨胀，
    # 默认最多取30个来源。
    context_articles = articles[
        :MAX_ARTICLES_PER_EVENT_CONTEXT
    ]

    article_blocks = []

    for article in context_articles:

        article_blocks.append(
            f"""
============================================================
来源文章 #{article["index"]}
============================================================

标题：
{article["title"]}

来源：
{article["source"]}

原文链接：
{article["source_url"]}

source_status：
{article["source_status"]}

content_status：
{article["content_status"]}

内容：

{article["body"][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}
"""
        )

    joined = "\n".join(
        article_blocks
    )

    prompt = f"""
你现在正在执行748686自生长知识系统的“事件知识提炼”。

日期：
{date}

事件ID：
{event_id}

AI第一阶段识别出的事件名称：
{event_title}

AI第一阶段判断：
{event["event_reason"]}

这个事件下面包含：

{len(articles)} 篇独立来源报道。

============================================================
任务
============================================================

请把这些不同来源的报道综合成一个“事件知识单元”。

注意：

这不是简单摘要。

你需要：

1. 识别不同来源共同确认的核心事实。
2. 合并重复信息。
3. 保留不同来源独有的重要信息。
4. 保留不同国家 / 地区的观察角度。
5. 区分事实和推测。
6. 不得因为多个媒体重复报道，就把它当成多个独立事实。
7. 不得把摘要冒充原文。
8. source_status不是fetched时，不得声称已经阅读完整原文。
9. 不得创造输入资料中没有的人物、公司、数字、时间、地点或因果关系。
10. 如果不同来源存在冲突，明确指出。
11. 如果资料不足，明确写“资料不足”。
12. 最终结果必须代表“一个事件”，而不是多篇新闻简单拼接。

============================================================
来源保留
============================================================

必须保留来源信息。

最终输出中明确列出：

- 来源数量
- 涉及国家/地区
- 涉及语言（如果能判断）
- 各来源独有的重要信息
- 来源之间是否存在明显差异

============================================================
输出结构
============================================================

# 事件名称

## 事件概述

## 核心事实

## 多来源交叉验证

## 不同来源提供的独有信息

## 不同国家 / 地区视角

## 信息差异与冲突

## 当前已知影响

## 目前不能确定的事情

## 来源

| # | 来源 | 标题 | 原文链接 | 状态 |
|---|---|---|---|---|

## 事件结论

用一段话总结：

“综合这些来源，目前最可靠的判断是什么？”

"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是748686自生长知识系统的跨来源新闻综合专家。"
            "必须把同一事件的多来源报道综合成一个高质量知识单元。"
            "不得编造事实。"
            "不得把摘要冒充原文。"
            "必须输出标准中文Markdown。"
        ),

        temperature=0.2,
    )

    if not result.strip():

        raise RuntimeError(
            f"❌ Event {event_id} 综合结果为空"
        )

    return result


# ============================================================
# 保存 Event Unit
# ============================================================

def save_event_unit(
    date,
    event,
    aggregated_content,
):

    target = (
        AGGREGATED_ROOT
        / f"{date}-Aggregated"
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{event['event_id']}_"
        f"{safe_name(event['event_title'])}.md"
    )

    path = (
        target
        / filename
    )

    source_lines = []

    for article in event[
        "articles"
    ]:

        source_lines.append(
            f"""- {article["source"]} | {article["title"]} | {article["source_url"]}"""
        )

    content = f"""---
date: {date}
event_id: {event["event_id"]}
type: aggregated_event
status: generated
source_count: {len(event["articles"])}
timezone: Asia/Shanghai
---

# {event["event_title"]}

> Event ID：{event["event_id"]}
>
> 原始新闻数量：{len(event["articles"])}

{aggregated_content}

## 原始来源映射

{chr(10).join(source_lines)}
"""

    path.write_text(
        content,
        encoding="utf-8"
    )

    return path


# ============================================================
# 处理全部 Event Units
# ============================================================

def process_event_aggregation(
    date,
    news_items,
):

    # --------------------------------------------------------
    # 第一轮聚类
    # --------------------------------------------------------

    initial_clusters = build_initial_clusters(
        date,
        news_items
    )

    # --------------------------------------------------------
    # 第二轮跨批次合并
    # --------------------------------------------------------

    final_clusters = merge_all_clusters(
        date,
        initial_clusters
    )

    # --------------------------------------------------------
    # Event Units
    # --------------------------------------------------------

    events = build_event_units(
        date,
        final_clusters,
        news_items
    )

    # --------------------------------------------------------
    # 覆盖率检查
    # --------------------------------------------------------

    all_indexes = []

    for event in events:

        all_indexes.extend(
            article["index"]
            for article in event[
                "articles"
            ]
        )

    expected_indexes = set(
        range(
            1,
            len(news_items) + 1
        )
    )

    actual_indexes = set(
        all_indexes
    )

    if (
        expected_indexes
        != actual_indexes
    ):

        missing = sorted(
            expected_indexes
            - actual_indexes
        )

        extra = sorted(
            actual_indexes
            - expected_indexes
        )

        raise RuntimeError(
            "❌ 最终Event覆盖率检查失败\n"
            f"Missing: {missing}\n"
            f"Extra: {extra}"
        )

    if len(all_indexes) != len(
        set(all_indexes)
    ):

        raise RuntimeError(
            "❌ 最终Event存在新闻重复归属"
        )

    # --------------------------------------------------------
    # 保存聚合索引
    # --------------------------------------------------------

    index_path = save_aggregation_index(
        date,
        events
    )

    print(
        f"✅ Aggregation Index: "
        f"{index_path}"
    )

    # --------------------------------------------------------
    # 第三层：逐事件综合
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("🧠 STAGE 3 — EVENT SYNTHESIS")
    print("=" * 70)

    aggregated_events = []

    for index, event in enumerate(
        events,
        start=1
    ):

        print()
        print(
            f"[{index}/{len(events)}] "
            f"{event['event_id']}"
        )

        print(
            f"   {event['event_title']}"
        )

        print(
            f"   Sources: "
            f"{len(event['articles'])}"
        )

        aggregated_content = synthesize_event(
            event
        )

        path = save_event_unit(
            date,
            event,
            aggregated_content
        )

        print(
            f"   ✅ Aggregated: {path}"
        )

        aggregated_events.append({

            **event,

            "aggregated_content":
                aggregated_content,

            "aggregated_path":
                path,
        })

    print()
    print("=" * 70)

    print(
        f"✅ EVENT SYNTHESIS COMPLETE: "
        f"{len(aggregated_events)}"
    )

    print("=" * 70)

    return aggregated_events


# ============================================================
# AI：新闻 / 事件分类
# ============================================================

def classify_event(
    event,
    categories,
):

    title = event[
        "event_title"
    ]

    aggregated_content = event[
        "aggregated_content"
    ]

    prompt = f"""
请判断下面这个“聚合事件知识单元”最适合进入哪个知识分析类别。

可选类别：

{json.dumps(
    categories,
    ensure_ascii=False
)}

事件：

{title}

聚合内容：

{aggregated_content[:30000]}

只输出合法JSON：

{{
  "category": "类别名称",
  "confidence": 0.0,
  "reason": "一句话原因"
}}

要求：

1. category必须来自给出的类别。
2. confidence范围0到1。
3. 不得创造新的类别。
4. 只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是748686知识系统的事件分类器。"
            "只依据聚合事件内容判断。"
            "必须返回合法JSON。"
            "不要输出JSON之外的解释。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        f"{event['event_id']} 分类"
    )

    category = data.get(
        "category"
    )

    if category not in categories:

        raise RuntimeError(
            f"❌ {event['event_id']} AI返回不存在的类别："
            f"{category}"
        )

    return {

        "category":
            category,

        "confidence":
            data.get(
                "confidence",
                0
            ),

        "reason":
            data.get(
                "reason",
                ""
            ),
    }


# ============================================================
# AI：聚合事件进入 Skills
# ============================================================

def analyze_event_with_skills(
    event,
    category,
    selected_skills,
):

    title = event[
        "event_title"
    ]

    aggregated_content = event[
        "aggregated_content"
    ]

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
# 聚合事件深度知识分析

事件ID：
{event["event_id"]}

日期：
{event["date"]}

事件名称：
{title}

知识类别：
{category}

============================================================
已经完成的多来源聚合
============================================================

{aggregated_content[:50000]}

============================================================
本次使用的 Skills
============================================================

{joined_skills[:50000]}

============================================================
分析要求
============================================================

现在开始进行最终知识分析。

非常重要：

1. 输入已经是经过跨来源、跨语言聚合后的事件。
2. 不要重新把每个来源当成独立新闻。
3. 不要重新制造重复事件。
4. 不得把摘要冒充原文。
5. source_status不是fetched时，不得声称已经阅读完整原文。
6. 不得编造人物、公司、数字、事件。
7. 不确定的信息必须明确标记。
8. 所有结论必须能够在输入资料中找到依据。
9. 如果资料不足，明确说明。
10. 重点分析“这个事件本身意味着什么”。

============================================================
输出结构
============================================================

# 事件分析

## 1. 核心事实

## 2. 事件背景

## 3. 为什么重要

## 4. 多来源综合判断

## 5. 影响

### 短期影响

### 中期影响

### 长期影响

## 6. 趋势判断

## 7. 机会

## 8. 风险

## 9. 关键实体

使用表格：

| 类型 | 名称 | 说明 |
|---|---|---|
| 人物 | | |
| 公司 | | |
| 产品 | | |
| 技术 | | |
| 行业 | | |
| 概念 | | |

## 10. 值得长期保存的知识

## 11. 后续追踪

## 12. 可生成专题
"""

    return call_ai(

        prompt,

        system_prompt=(
            "你是748686自生长知识系统的高级知识工程师。"
            "输入已经是多来源聚合后的事件。"
            "必须在此基础上进行深度知识分析。"
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

        raise RuntimeError(
            f"❌ {date} 没有分析结果，无法生成知识卡片"
        )

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

下面是已经完成“事件聚合 + Skills深度分析”的知识单元：

{joined[:60000]}

请提取真正值得进入长期知识库的知识实体。

重点：

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

只保留具有长期价值的知识。

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

        raise RuntimeError(
            f"❌ {date} 没有分析结果，无法生成专题"
        )

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

以下是今天完成的事件级知识分析：

{joined[:60000]}

请寻找值得进一步研究的专题。

要求：

1. 不要简单重复新闻标题。
2. 必须存在跨事件的共同主题。
3. 优先选择未来仍具有研究价值的主题。
4. 给出研究问题。
5. 给出为什么值得研究。
6. 给出需要继续寻找的数据或资料。
7. 不得编造事实。
8. 如果资料不足，可以少于3个。
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
            "从多个事件之间寻找长期主题。"
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

        raise RuntimeError(
            f"❌ {date} 没有分析结果，无法生成追踪事项"
        )

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

下面是今天的事件级知识分析：

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
            "只根据已有事件资料判断。"
            "不得编造未来事件。"
        ),

        temperature=0.3,
    )


# ============================================================
# 判断指定日期是否已经完整处理
# ============================================================

def is_date_completed(
    date: str
):

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
        f"""
## 今日知识处理概览

- 原始有效 Enriched News：{len(analyses)}
- 最终事件级知识单元：{len(analyses)}
- 处理方式：跨来源 / 跨语言事件聚合后深度分析
"""
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

    print()
    print("=" * 70)
    print(f"📅 CHECK DATE: {date}")
    print("=" * 70)

    # --------------------------------------------------------
    # 已完成 → 跳过
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
    # 获取 Enriched
    # --------------------------------------------------------

    try:

        files = get_enriched_files(
            date
        )

    except FileNotFoundError as exc:

        print(
            f"⚠️ {date} 暂无 Enriched：{exc}"
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
    # 加载全部新闻
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

            raise RuntimeError(
                f"❌ 新闻读取失败：{path}\n{exc}"
            ) from exc

    print(
        f"Valid news: {len(news_items)}"
    )

    if not news_items:

        raise RuntimeError(
            f"❌ {date} 没有有效新闻"
        )

    # --------------------------------------------------------
    # Horizon Score
    #
    # 只用于顺序。
    # 不用于截断。
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

    print(
        f"AI Input News: {len(news_items)}"
    )

    print(
        "News processing limit: NONE"
    )

    # ========================================================
    # 第二层：
    #
    # 400篇
    # ↓
    # AI聚类
    # ↓
    # Event Units
    # ========================================================

    aggregated_events = process_event_aggregation(
        date,
        news_items
    )

    if not aggregated_events:

        raise RuntimeError(
            f"❌ {date} 没有生成任何Event Unit"
        )

    original_count = len(
        news_items
    )

    event_count = len(
        aggregated_events
    )

    reduction_ratio = (
        event_count / original_count
        if original_count
        else 1
    )

    print()
    print("=" * 70)
    print("📊 AGGREGATION RESULT")
    print("=" * 70)

    print(
        f"Original Enriched News : {original_count}"
    )

    print(
        f"Final Event Units      : {event_count}"
    )

    print(
        f"Compression Ratio      : "
        f"{reduction_ratio:.2%}"
    )

    print(
        f"Reduced By             : "
        f"{original_count - event_count}"
    )

    # ========================================================
    # 第四层：
    #
    # Event Unit
    # ↓
    # 分类
    # ↓
    # Skills
    # ========================================================

    categories = list(
        routes.keys()
    )

    if not categories:

        raise RuntimeError(
            "skill_routes.json没有任何类别"
        )

    analyses = []

    category_count = {}

    total_events = len(
        aggregated_events
    )

    print()
    print("=" * 70)
    print("🧠 STAGE 4 — CLASSIFICATION + SKILLS")
    print("=" * 70)

    print(
        f"Event Units entering Skills: "
        f"{total_events}"
    )

    for index, event in enumerate(
        aggregated_events,
        start=1
    ):

        print()
        print(
            "=" * 70
        )

        print(
            f"[{index}/{total_events}] "
            f"{event['event_id']}"
        )

        print(
            f"Event: {event['event_title']}"
        )

        print(
            f"Sources: "
            f"{len(event['articles'])}"
        )

        # ----------------------------------------------------
        # 分类
        # ----------------------------------------------------

        classification = classify_event(

            event,

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

            raise RuntimeError(
                f"❌ {event['event_id']} "
                f"没有匹配到任何Skill："
                f"category={category}"
            )

        # ----------------------------------------------------
        # 深度分析
        # ----------------------------------------------------

        analysis = analyze_event_with_skills(

            event,

            category,

            selected_skills
        )

        if not analysis.strip():

            raise RuntimeError(
                f"❌ {event['event_id']} "
                f"Skills分析返回空内容"
            )

        header = f"""
---

# {event['event_title']}

> Event ID：{event['event_id']}
>
> 日期：{date}
>
> 分类：{category}
>
> 聚合来源数：{len(event['articles'])}
>
> 聚合原始新闻数：{len(event['articles'])}
>
> 聚合文件：{event['aggregated_path']}

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
    # 验证
    # --------------------------------------------------------

    print()
    print(
        "=" * 70
    )

    print(
        f"Successful event analyses: "
        f"{len(analyses)}"
    )

    if len(analyses) != len(
        aggregated_events
    ):

        raise RuntimeError(
            f"❌ {date} Event分析数量不一致。\n"
            f"Events={len(aggregated_events)}\n"
            f"Analyses={len(analyses)}"
        )

    # ========================================================
    # 知识卡片
    # ========================================================

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
        f"✅ Knowledge Cards: "
        f"{knowledge_path}"
    )

    # ========================================================
    # 专题
    # ========================================================

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

    # ========================================================
    # 追踪
    # ========================================================

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

    # ========================================================
    # 日报
    # ========================================================

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
        f"✅ Daily Report: "
        f"{report_path}"
    )

    # ========================================================
    # 日志
    # ========================================================

    log_path = (
        LOGS
        / f"{date}_knowledge_pipeline.md"
    )

    current = now()

    log = f"""# {date} Knowledge Pipeline V3

- 时间：{current.isoformat()}
- 时区：Asia/Shanghai
- Enriched 新闻：{original_count}
- 初始 AI Cluster：{len(build_initial_cluster_log_placeholder(initial_count=None)) if False else "见聚合过程日志"}
- 最终 Event Units：{event_count}
- AI处理事件：{len(analyses)}
- Skills数量：{len(skills)}
- 路由类别：{len(routes)}
- AI Provider：AGNES.ai
- AI Model：{AGNES_MODEL}

## 新版处理架构

Enriched News
→ AI 第一轮批量事件聚类
→ 跨批次事件合并
→ Event Units
→ 多来源事件综合
→ 事件分类
→ 动态 Skills
→ 知识卡片
→ 专题候选
→ 后续追踪
→ 日报

## 新闻处理模式

- 当日有效 Enriched News：全部进入聚合层
- 新闻数量上限：无
- Horizon Score：仅用于处理顺序
- 多日处理方式：逐日独立处理
- 当前日期单元：{date}

## 聚合结果

- 原始 Enriched News：{original_count}
- 最终 Event Units：{event_count}
- 减少新闻单元：{original_count - event_count}
- 压缩比例：{reduction_ratio:.2%}

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

- 聚合索引：Raw News/{date}-Aggregated/_event_index.json
- 聚合事件目录：Raw News/{date}-Aggregated/
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

    # ========================================================
    # 完成
    # ========================================================

    print()
    print("=" * 70)

    print(
        f"✅ {date} KNOWLEDGE PIPELINE COMPLETE"
    )

    print("=" * 70)

    print(
        f"Original News : {original_count}"
    )

    print(
        f"Event Units   : {event_count}"
    )

    print(
        f"Daily Report  : {report_path}"
    )

    print(
        f"Knowledge     : {knowledge_path}"
    )

    print(
        f"Topics        : {topic_path}"
    )

    print(
        f"Log           : {log_path}"
    )

    return True


# ============================================================
# 占位函数
#
# 仅用于保持日志结构简单。
# ============================================================

def build_initial_cluster_log_placeholder(
    initial_count=None
):

    return []


# ============================================================
# 主流程
# ============================================================

def main():

    current = now()

    today = current.date()

    # ========================================================
    # 三天窗口
    # ========================================================

    target_dates = [

        (
            today
            - timedelta(days=2)
        ).strftime("%Y-%m-%d"),

        (
            today
            - timedelta(days=1)
        ).strftime("%Y-%m-%d"),

        today.strftime("%Y-%m-%d"),
    ]

    print("=" * 70)

    print(
        "748686 KNOWLEDGE PIPELINE V3"
    )

    print("=" * 70)

    print(
        f"Current Date: "
        f"{today.strftime('%Y-%m-%d')}"
    )

    print(
        f"Timezone: "
        f"{current.tzinfo}"
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
        "Architecture:"
    )

    print(
        "  Enriched News"
    )

    print(
        "      ↓"
    )

    print(
        "  AI Event Clustering"
    )

    print(
        "      ↓"
    )

    print(
        "  Cross-Batch Merging"
    )

    print(
        "      ↓"
    )

    print(
        "  Event Units"
    )

    print(
        "      ↓"
    )

    print(
        "  Multi-Source Synthesis"
    )

    print(
        "      ↓"
    )

    print(
        "  Classification"
    )

    print(
        "      ↓"
    )

    print(
        "  Dynamic Skills"
    )

    print(
        "      ↓"
    )

    print(
        "  Knowledge / Topics / Watchlist / Daily Report"
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
    # 创建目录
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
    # Routes
    # ========================================================

    routes = load_routes()

    # ========================================================
    # Skills
    # ========================================================

    skills = load_skills()

    print(
        f"Loaded Skills: "
        f"{len(skills)}"
    )

    print(
        f"Loaded Routes: "
        f"{len(routes)}"
    )

    if len(skills) < 27:

        print(
            "⚠️ 警告：当前Skills数量少于27"
        )

    # ========================================================
    # AGNES Key
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
    # 三日逐日处理
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
            print("=" * 70)

            print(
                f"❌ {date} PROCESSING FAILED"
            )

            print("=" * 70)

            print(
                f"{type(exc).__name__}: "
                f"{exc}"
            )

            print()

            # ------------------------------------------------
            # 非常重要
            #
            # 任意需要处理的日期失败：
            #
            # 整个GitHub Actions必须失败。
            #
            # 不允许继续伪装SUCCESS。
            # ------------------------------------------------

            raise

    # ========================================================
    # 完成
    # ========================================================

    print()
    print("=" * 70)

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
        "最终架构："
    )

    print(
        "  全量 Enriched News"
    )

    print(
        "        ↓"
    )

    print(
        "  AI 跨来源 / 跨语言聚类"
    )

    print(
        "        ↓"
    )

    print(
        "  跨批次事件合并"
    )

    print(
        "        ↓"
    )

    print(
        "  Event Units"
    )

    print(
        "        ↓"
    )

    print(
        "  多来源综合提炼"
    )

    print(
        "        ↓"
    )

    print(
        "  分类"
    )

    print(
        "        ↓"
    )

    print(
        "  动态 Skills"
    )

    print(
        "        ↓"
    )

    print(
        "  知识卡片 / 专题 / 追踪 / 日报"
    )

    print()

    print(
        "三天不合并。"
    )

    print(
        "当天新闻不截断。"
    )

    print(
        "聚合后才进入Skills。"
    )

    print()

    print(
        "✅ KNOWLEDGE PIPELINE V3 COMPLETE"
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
        print("=" * 70)

        print(
            "❌ KNOWLEDGE PIPELINE V3 FAILED"
        )

        print("=" * 70)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print()

        sys.exit(1)
