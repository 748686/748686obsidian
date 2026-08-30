#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V4

============================================================
正式架构
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
STAGE 1：第二层 AI 事件聚合
============================================================
全部 Enriched News
   ↓
AI 第一轮批量事件聚类
   ↓
跨批次事件合并
   ↓
Final Event Units
   ↓
AI 多来源事件综合
   ↓
保存：
Raw News/
    YYYY-MM-DD-EventUnits/
        ├── _event_index.json
        ├── EVT-xxxx.md
        └── ...
   ↓
EVENT_UNITS_COMPLETE

============================================================
此处断点
============================================================

Git commit
   ↓
Git push
   ↓
本地重新拉取
   ↓

============================================================
STAGE 2：27 Skills 深度处理
============================================================

读取已经保存的 EventUnits
   ↓
每天独立处理
   ↓
事件分类
   ↓
skill_routes.json
   ↓
动态选择 Skills
   ↓
深度分析
   ↓
知识卡片
   ↓
专题候选
   ↓
Watchlist
   ↓
日报
   ↓
============================================================
STAGE 3：自生长
============================================================
知识实体
   ↓
长期知识库
   ↓
专题
   ↓
追踪
   ↓
后续自生长

============================================================
核心原则
============================================================

1. Horizon 完全由 Horizon 管理。
2. 本程序不读取 Horizon Config。
3. 本程序不启动 Horizon。
4. 本程序只处理已经存在的 Enriched News。
5. AI 使用 AGNES.ai。
6. API Key 从 AGNES_API_KEY 读取。
7. 模型固定 agnes-2.5-flash。
8. Base URL 固定 https://api.agnes-ai.cn/v1。
9. 不设置 max_tokens。
10. 日期统一 Asia/Shanghai。
11. 不限制 Enriched News 数量。
12. 所有有效 Enriched News 都进入 Stage 1。
13. Stage 1 每批最多40篇。
14. Stage 1 必须覆盖全部新闻。
15. Stage 1 支持跨来源。
16. Stage 1 支持跨语言。
17. Stage 1 同事件尽量归并。
18. 不同事件不得强行合并。
19. Stage 1 完成后必须落盘。
20. Stage 2 不再读取原始 Enriched News。
21. Stage 2 只读取 EventUnits。
22. 三天完全独立。
23. 任意关键 AI 步骤失败立即失败。
24. 不允许半成品标记 SUCCESS。
25. Stage 1 和 Stage 2 必须可以断点续跑。
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
# Event Unit目录
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnits"

EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"

SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"


# ============================================================
# AGNES
# ============================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"

AGNES_MODEL = "agnes-2.5-flash"

AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180


# ============================================================
# 聚合参数
# ============================================================

AGGREGATION_BATCH_SIZE = 40

CLUSTER_MERGE_BATCH_SIZE = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

MAX_ARTICLES_PER_EVENT_CONTEXT = 30


# ============================================================
# 北京时间
# ============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def now() -> datetime:
    return datetime.now(BEIJING_TZ)


# ============================================================
# JSON
# ============================================================

def read_json(path: Path, default=None):

    if default is None:
        default = {}

    if not path.exists():
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


def write_json(path: Path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# ============================================================
# AI JSON解析
# ============================================================

def parse_ai_json(result: str, context: str):

    text = str(result).strip()

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
# 文件名
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
# Front Matter
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

    api_key = os.getenv(
        AGNES_API_KEY_ENV,
        ""
    ).strip()

    if not api_key:

        raise RuntimeError(
            "❌ 缺少 AGNES_API_KEY"
        )

    if not system_prompt:

        system_prompt = (
            "你是748686自生长知识系统的知识工程师。"
            "严格依据输入内容。"
            "不得编造事实。"
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
        ensure_ascii=False
    ).encode("utf-8")

    request = Request(

        AGNES_BASE_URL
        + "/chat/completions",

        data=payload,

        headers={

            "Authorization":
                f"Bearer {api_key}",

            "Content-Type":
                "application/json",

            "Accept":
                "application/json",

            "User-Agent":
                "748686-Knowledge-Pipeline/4.0",
        },

        method="POST",
    )

    print()
    print("🤖 Calling AGNES.ai")
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
            f"Response: {error_body[:3000]}"
        ) from exc

    except URLError as exc:

        raise RuntimeError(
            "❌ AGNES.ai 网络连接失败\n"
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
            f"{raw_response[:3000]}"
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

        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        skills[path.name] = {

            "name": path.name,

            "path": str(path),

            "content": content,
        }

    return skills


# ============================================================
# Routes
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


def route_skills(
    category,
    routes,
    skills,
):

    selected_names = routes.get(
        category,
        []
    )

    selected = []

    for name in selected_names:

        if name not in skills:

            raise RuntimeError(
                "❌ skill_routes.json引用了不存在的Skill："
                f"{name}"
            )

        selected.append(
            skills[name]
        )

    return selected


# ============================================================
# Enriched
# ============================================================

def get_enriched_files(date):

    root = (
        RAW_NEWS
        / f"{date}-Enriched"
    )

    if not root.exists():

        raise FileNotFoundError(
            f"没有找到 Enriched目录：{root}"
        )

    return sorted(
        root.rglob("*.md")
    )


def load_news_file(path):

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


def is_news(item):

    title = item[
        "metadata"
    ].get(
        "title",
        ""
    ).strip()

    return bool(title)


# ============================================================
# 第一轮文章Digest
# ============================================================

def build_article_digest(
    item,
    index,
):

    metadata = item[
        "metadata"
    ]

    return f"""
[ARTICLE {index}]

标题：
{metadata.get("title", "Untitled")}

来源：
{metadata.get("source", "Unknown")}

原文链接：
{metadata.get("source_url", "")}

来源状态：
{metadata.get("source_status", "")}

内容状态：
{metadata.get("content_status", "")}

内容：
{item["body"][:ARTICLE_CLUSTER_CONTENT_LIMIT]}
"""


# ============================================================
# 第一轮AI聚类
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

    # --------------------------------------------------------
    # 重要硬检查
    # --------------------------------------------------------

    if not joined.strip():

        raise RuntimeError(
            f"❌ {date} 第一轮聚类输入为空"
        )

    print(
        f"   Articles sent to AI: "
        f"{len(batch_items)}"
    )

    print(
        f"   Prompt article characters: "
        f"{len(joined)}"
    )

    # --------------------------------------------------------
    # 正式Prompt
    # --------------------------------------------------------

    prompt = f"""
你现在正在执行748686自生长知识系统的第二层事件聚合。

日期：
{date}

============================================================
本批真实新闻输入
============================================================

{joined}

============================================================
任务
============================================================

识别哪些新闻实际上属于同一个现实世界事件。

必须考虑：

1. 不同国家媒体报道同一个事件。
2. 不同语言报道同一个事件。
3. 标题完全不同但实际描述同一事件。
4. 同一个政策变化产生的不同报道。
5. 同一个公司动作产生的不同报道。
6. 同一个技术发布产生的不同报道。
7. 同一个市场变化产生的不同报道。
8. 同一个人物事件产生的不同报道。

不要仅因为：

- 关键词相同
- 公司名字相同
- 行业相同
- 国家相同

就强行合并。

============================================================
核心原则
============================================================

如果多个文章明显描述同一个现实世界事件：

放入同一个cluster。

如果只是同一个主题、行业、公司，但不是同一个现实世界事件：

必须分开。

如果无法确定：

宁可分开。

============================================================
覆盖要求
============================================================

输入中的每一篇ARTICLE：

必须且只能属于一个cluster。

无法与其他文章合并的：

自己成为一个cluster。

不得遗漏。

不得重复。

不得创造不存在的ARTICLE编号。

============================================================
输出
============================================================

只输出合法JSON：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1, 7, 13],
      "event_title": "统一事件名称",
      "event_reason": "为什么这些文章属于同一个现实世界事件"
    }},
    {{
      "cluster_id": "C002",
      "article_indexes": [2],
      "event_title": "独立事件",
      "event_reason": "为什么不能与其他文章合并"
    }}
  ]
}}

要求：

1. article_indexes必须来自输入。
2. 必须覆盖全部ARTICLE。
3. 不得重复ARTICLE。
4. 不得创造ARTICLE。
5. cluster_id必须唯一。
6. event_title必须是事件名称，不是标题堆砌。
7. event_reason简洁。
8. 只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是全球新闻事件聚类专家。"
            "你必须直接分析用户提供的ARTICLE。"
            "必须覆盖全部ARTICLE。"
            "必须返回合法JSON。"
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
# Cluster覆盖检查
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

    duplicates = [
        x for x in actual
        if actual.count(x) > 1
    ]

    actual_set = set(actual)

    missing = sorted(
        expected - actual_set
    )

    extra = sorted(
        actual_set - expected
    )

    if duplicates:

        raise RuntimeError(
            f"❌ {context} 存在重复文章："
            f"{sorted(set(duplicates))}"
        )

    if missing:

        raise RuntimeError(
            f"❌ {context} 存在未聚类文章："
            f"{missing}"
        )

    if extra:

        raise RuntimeError(
            f"❌ {context} 出现不存在文章："
            f"{extra}"
        )


# ============================================================
# 跨批次Cluster合并
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
    cluster.get(
        "article_indexes",
        []
    ),
    ensure_ascii=False
)}
"""
        )

    joined = "\n\n".join(
        descriptors
    )

    if not joined.strip():

        raise RuntimeError(
            f"❌ {date} 跨批次Cluster输入为空"
        )

    prompt = f"""
你正在执行748686自生长知识系统的跨批次事件合并。

日期：
{date}

第 {merge_round} 轮
第 {batch_index} 批

============================================================
Cluster输入
============================================================

{joined}

============================================================
任务
============================================================

判断哪些Cluster实际上属于同一个现实世界事件。

原则：

1. 同事件 → 合并。
2. 同主题不同事件 → 分开。
3. 同公司不同事件 → 分开。
4. 同行业不同事件 → 分开。
5. 不确定 → 不合并。
6. 宁可少合并，不要错误合并。

============================================================
覆盖
============================================================

每个输入CLUSTER必须且只能进入一个group。

不得遗漏。

不得重复。

不得创造不存在的CLUSTER编号。

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
      "reason": "为什么这些Cluster属于同一事件"
    }},
    {{
      "group_id": "G002",
      "cluster_indexes": [2],
      "event_title": "独立事件",
      "reason": "为什么独立"
    }}
  ]
}}
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是跨来源新闻事件归并专家。"
            "必须覆盖所有输入Cluster。"
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

        actual.extend(
            group.get(
                "cluster_indexes",
                []
            )
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
            f"❌ {date} 跨批次覆盖异常\n"
            f"Missing={missing}\n"
            f"Extra={extra}"
        )

    return groups


# ============================================================
# Stage 1：建立初始Clusters
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
    print("STAGE 1A — AI EVENT CLUSTERING")
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
            start
            + AGGREGATION_BATCH_SIZE,
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

        validate_cluster_coverage(

            clusters,

            list(
                range(
                    start + 1,
                    end + 1
                )
            ),

            f"{date} Batch {batch_number}"
        )

        for cluster in clusters:

            article_indexes = [
                int(x)
                for x in cluster[
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
# Stage 1B：跨批次合并
# ============================================================

def merge_all_clusters(
    date,
    clusters,
):

    current = clusters

    merge_round = 1

    print()
    print("=" * 70)
    print("STAGE 1B — CROSS-BATCH MERGING")
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
                start
                + CLUSTER_MERGE_BATCH_SIZE
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

                article_indexes = []

                for cluster_index in group[
                    "cluster_indexes"
                ]:

                    source_cluster = batch[
                        cluster_index - 1
                    ]

                    article_indexes.extend(
                        source_cluster[
                            "article_indexes"
                        ]
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
                        sorted(
                            set(
                                article_indexes
                            )
                        ),
                })

        print(
            f"   Result after round "
            f"{merge_round}: "
            f"{len(next_level)}"
        )

        current = next_level

        merge_round += 1

    # --------------------------------------------------------
    # 最终全局合并
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
        f"✅ FINAL EVENT UNITS: "
        f"{len(final_clusters)}"
    )

    return final_clusters


# ============================================================
# Event Unit
# ============================================================

def build_event_units(
    date,
    final_clusters,
    news_items,
):

    events = []

    for cluster in final_clusters:

        articles = []

        for index in cluster[
            "article_indexes"
        ]:

            if (
                index < 1
                or index > len(news_items)
            ):

                raise RuntimeError(
                    f"❌ Event "
                    f"{cluster['event_id']} "
                    f"引用不存在文章：{index}"
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
                cluster["event_title"],

            "event_reason":
                cluster["event_reason"],

            "articles":
                articles,
        })

    return events


# ============================================================
# Stage 1C：多来源事件综合
# ============================================================

def synthesize_event(event):

    articles = event[
        "articles"
    ]

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

    if not joined.strip():

        raise RuntimeError(
            f"❌ {event['event_id']} "
            "事件综合输入为空"
        )

    prompt = f"""
你现在执行748686自生长知识系统的第二层事件知识综合。

日期：
{event["date"]}

事件ID：
{event["event_id"]}

事件名称：
{event["event_title"]}

第一轮事件判断：
{event["event_reason"]}

============================================================
同一事件的多来源原始输入
============================================================

{joined}

============================================================
任务
============================================================

把这些来源综合成一个高质量事件知识单元。

要求：

1. 识别共同确认的核心事实。
2. 合并重复信息。
3. 保留来源独有的重要信息。
4. 保留不同国家/地区视角。
5. 区分事实和推测。
6. 不得因为多个媒体重复报道就制造多个事实。
7. 不得编造。
8. source_status不是fetched时，不得声称完整阅读原文。
9. 如果来源存在冲突，明确指出。
10. 如果资料不足，明确说明。

============================================================
输出
============================================================

# 事件名称

## 事件概述

## 核心事实

## 多来源交叉验证

## 不同来源独有信息

## 不同国家 / 地区视角

## 信息差异与冲突

## 当前已知影响

## 目前不能确定的事情

## 来源

| # | 来源 | 标题 | 原文链接 | 状态 |
|---|---|---|---|---|

## 事件结论

综合这些来源，目前最可靠的判断是什么？
"""

    return call_ai(

        prompt,

        system_prompt=(
            "你是跨来源新闻综合专家。"
            "必须严格依据输入。"
            "不得编造。"
            "输出标准中文Markdown。"
        ),

        temperature=0.2,
    )


# ============================================================
# 保存 Event Unit
# ============================================================

def event_units_dir(date):

    return (
        RAW_NEWS
        / f"{date}-{EVENT_UNITS_SUFFIX}"
    )


def save_event_unit(
    date,
    event,
    aggregated_content,
):

    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"{event['event_id']}_"
        f"{safe_name(event['event_title'])}.md"
    )

    path = target / filename

    source_lines = []

    for article in event[
        "articles"
    ]:

        source_lines.append(
            f"- {article['source']} | "
            f"{article['title']} | "
            f"{article['source_url']}"
        )

    content = f"""---
date: {date}
event_id: {event['event_id']}
type: event_unit
status: completed
source_count: {len(event['articles'])}
timezone: Asia/Shanghai
---

# {event['event_title']}

> Event ID：{event['event_id']}
>
> 原始新闻数量：{len(event['articles'])}

## 第二层AI事件判断

{event['event_reason']}

## 第二层AI多来源综合

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
# 保存 Event Unit Index
# ============================================================

def save_aggregation_index(
    date,
    events,
):

    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True
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

            "source_count":
                len(event["articles"]),

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

    index_path = (
        target
        / "_event_index.json"
    )

    write_json(
        index_path,
        serializable
    )

    return index_path


# ============================================================
# Stage 1完成标记
# ============================================================

def mark_event_units_complete(
    date,
    original_count,
    event_count,
):

    target = event_units_dir(
        date
    )

    marker = (
        target
        / EVENT_UNITS_COMPLETE_FILE
    )

    marker.write_text(

        f"""EVENT_UNITS_COMPLETE

date: {date}
original_enriched_news: {original_count}
final_event_units: {event_count}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
""",

        encoding="utf-8"
    )

    return marker


def event_units_complete(date):

    marker = (
        event_units_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    return marker.exists()


# ============================================================
# Stage 1
# ============================================================

def run_stage_1(date):

    print()
    print("=" * 70)
    print(f"STAGE 1 — EVENT UNIT GENERATION: {date}")
    print("=" * 70)

    target = event_units_dir(
        date
    )

    if event_units_complete(date):

        print(
            f"✅ {date} EventUnits 已经完成。"
        )

        print(
            f"📁 {target}"
        )

        return False

    files = get_enriched_files(
        date
    )

    print(
        f"Enriched files: {len(files)}"
    )

    if not files:

        raise RuntimeError(
            f"❌ {date} 没有Enriched新闻"
        )

    news_items = []

    for path in files:

        item = load_news_file(
            path
        )

        if is_news(item):

            news_items.append(
                item
            )

    print(
        f"Valid news: {len(news_items)}"
    )

    if not news_items:

        raise RuntimeError(
            f"❌ {date} 没有有效新闻"
        )

    # --------------------------------------------------------
    # Horizon Score仅排序，不截断
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

    # --------------------------------------------------------
    # 第一轮
    # --------------------------------------------------------

    initial_clusters = build_initial_clusters(
        date,
        news_items
    )

    # --------------------------------------------------------
    # 第二轮
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
    # 覆盖检查
    # --------------------------------------------------------

    all_indexes = []

    for event in events:

        all_indexes.extend(
            article["index"]
            for article in event[
                "articles"
            ]
        )

    expected = set(
        range(
            1,
            len(news_items) + 1
        )
    )

    actual = set(
        all_indexes
    )

    if expected != actual:

        raise RuntimeError(
            f"❌ {date} Event覆盖率失败\n"
            f"Missing={sorted(expected - actual)}\n"
            f"Extra={sorted(actual - expected)}"
        )

    if len(all_indexes) != len(
        set(all_indexes)
    ):

        raise RuntimeError(
            f"❌ {date} Event存在重复新闻归属"
        )

    # --------------------------------------------------------
    # 保存Index
    # --------------------------------------------------------

    index_path = save_aggregation_index(
        date,
        events
    )

    print(
        f"✅ Event Index: {index_path}"
    )

    # --------------------------------------------------------
    # 多来源综合
    # --------------------------------------------------------

    print()
    print("=" * 70)
    print("STAGE 1C — EVENT SYNTHESIS")
    print("=" * 70)

    saved_events = []

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

        if not aggregated_content.strip():

            raise RuntimeError(
                f"❌ {event['event_id']} "
                "综合结果为空"
            )

        path = save_event_unit(

            date,

            event,

            aggregated_content
        )

        print(
            f"   ✅ Saved: {path}"
        )

        saved_events.append(
            event
        )

    if len(saved_events) != len(events):

        raise RuntimeError(
            f"❌ {date} EventUnits保存数量异常"
        )

    # --------------------------------------------------------
    # 完成标记
    # --------------------------------------------------------

    marker = mark_event_units_complete(

        date,

        len(news_items),

        len(events)
    )

    print()
    print("=" * 70)
    print("✅ STAGE 1 COMPLETE")
    print("=" * 70)

    print(
        f"Original Enriched News : "
        f"{len(news_items)}"
    )

    print(
        f"Final Event Units      : "
        f"{len(events)}"
    )

    print(
        f"Event Units Directory  : "
        f"{target}"
    )

    print(
        f"Completion Marker      : "
        f"{marker}"
    )

    return True


# ============================================================
# Stage 2：读取Event Units
# ============================================================

def load_saved_event_units(date):

    target = event_units_dir(
        date
    )

    if not target.exists():

        raise FileNotFoundError(
            f"EventUnits目录不存在：{target}"
        )

    if not event_units_complete(date):

        raise RuntimeError(
            f"❌ {date} EventUnits尚未完成，"
            "禁止进入27 Skills阶段"
        )

    files = sorted(
        target.glob(
            "EVT-*.md"
        )
    )

    if not files:

        raise RuntimeError(
            f"❌ {date} EventUnits目录没有事件文件"
        )

    events = []

    for path in files:

        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        metadata, body = parse_front_matter(
            content
        )

        event_id = metadata.get(
            "event_id",
            ""
        )

        if not event_id:

            raise RuntimeError(
                f"❌ EventUnit缺少event_id：{path}"
            )

        title = ""

        heading_match = re.search(
            r"(?m)^#\s+(.+)$",
            body
        )

        if heading_match:

            title = (
                heading_match
                .group(1)
                .strip()
            )

        source_count = int(
            metadata.get(
                "source_count",
                "0"
            )
        )

        events.append({

            "event_id":
                event_id,

            "date":
                date,

            "event_title":
                title or event_id,

            "aggregated_content":
                body,

            "aggregated_path":
                path,

            "source_count":
                source_count,
        })

    return events


# ============================================================
# 分类
# ============================================================

def classify_event(
    event,
    categories,
):

    prompt = f"""
请判断下面这个已经完成第二层AI多来源事件聚合的Event Unit，
最适合进入哪个知识分析类别。

可选类别：

{json.dumps(
    categories,
    ensure_ascii=False
)}

事件：

{event["event_title"]}

聚合内容：

{event["aggregated_content"][:30000]}

只输出合法JSON：

{{
  "category": "类别名称",
  "confidence": 0.0,
  "reason": "一句话原因"
}}

要求：

1. category必须来自给出的类别。
2. confidence范围0到1。
3. 不得创造类别。
4. 只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是748686知识系统的事件分类器。"
            "输入已经是Event Unit。"
            "必须返回合法JSON。"
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
            f"❌ {event['event_id']} "
            f"AI返回不存在类别：{category}"
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
# 27 Skills
# ============================================================

def analyze_event_with_skills(
    event,
    category,
    selected_skills,
):

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
{event["event_title"]}

知识类别：
{category}

============================================================
第二层AI已经完成的Event Unit
============================================================

{event["aggregated_content"][:50000]}

============================================================
本次动态选择的Skills
============================================================

{joined_skills[:50000]}

============================================================
分析要求
============================================================

现在开始最终知识分析。

非常重要：

1. 输入已经经过跨来源、跨语言事件聚合。
2. 不要重新把来源当成独立新闻。
3. 不要重新制造重复事件。
4. 不得编造事实。
5. source_status不是fetched时，不得声称完整阅读原文。
6. 不确定信息必须明确标记。
7. 所有结论必须有输入依据。
8. 资料不足必须明确说明。
9. 重点分析这个事件本身意味着什么。

============================================================
输出
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
            "输入已经是第二层AI完成的Event Unit。"
            "现在进行27 Skills深度分析。"
            "不得编造事实。"
            "输出结构化中文Markdown。"
        ),

        temperature=0.3,
    )


# ============================================================
# 知识卡片
# ============================================================

def generate_knowledge_cards(
    date,
    analyses,
):

    if not analyses:

        raise RuntimeError(
            f"❌ {date} 没有分析结果"
        )

    joined = "\n\n".join(
        analyses
    )

    prompt = f"""
日期：{date}

下面是已经完成事件聚合和Skills深度分析的知识单元：

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

不要把普通新闻全部做成知识卡片。

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
            "不得编造。"
            "输出中文Markdown。"
        ),

        temperature=0.3,
    )


# ============================================================
# 专题
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

以下是今天完成的事件级知识分析：

{joined[:60000]}

寻找值得进一步研究的专题。

要求：

1. 不简单重复新闻标题。
2. 必须存在跨事件共同主题。
3. 优先选择未来仍具有研究价值的主题。
4. 给出研究问题。
5. 给出为什么值得研究。
6. 给出需要继续寻找的数据或资料。
7. 不得编造。
8. 资料不足时少生成。
"""

    return call_ai(

        prompt,

        system_prompt=(
            "你是战略研究员。"
            "从多个事件之间寻找长期主题。"
            "不得编造。"
        ),

        temperature=0.3,
    )


# ============================================================
# Watchlist
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

下面是今天的事件级知识分析：

{joined[:50000]}

请生成未来值得继续追踪的项目。

输出：

# 后续追踪

| 优先级 | 追踪事项 | 原因 | 下一步需要关注 |
|---|---|---|---|
| 高 | | | |
| 中 | | | |
| 低 | | | |

要求：

- 只选择真正可能继续发展的事件。
- 不编造未来事件。
- 下一步需要关注写成观察指标。
- 没有足够证据时不要强行生成。
"""

    return call_ai(

        prompt,

        system_prompt=(
            "你是新闻趋势追踪分析师。"
            "只根据已有事件资料判断。"
            "不得编造。"
        ),

        temperature=0.3,
    )


# ============================================================
# 保存知识卡片
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
# 保存专题
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
# 日报
# ============================================================

def save_daily_report(
    date,
    analyses,
    knowledge,
    topics,
    watchlist,
    event_count,
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

- Event Units：{event_count}
- Skills深度分析：{len(analyses)}
- 处理方式：第二层AI事件聚合后进入27 Skills
- 日期：{date}
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

    path.write_text(
        "\n\n".join(sections)
        + "\n",
        encoding="utf-8"
    )

    return path


# ============================================================
# Stage 2完成标记
# ============================================================

def skills_complete(date):

    marker = (
        event_units_dir(date)
        / SKILLS_COMPLETE_FILE
    )

    return marker.exists()


def mark_skills_complete(
    date,
    event_count,
):

    marker = (
        event_units_dir(date)
        / SKILLS_COMPLETE_FILE
    )

    marker.write_text(

        f"""SKILLS_COMPLETE

date: {date}
event_units: {event_count}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
""",

        encoding="utf-8"
    )

    return marker


# ============================================================
# Stage 2
# ============================================================

def run_stage_2(
    date,
    routes,
    skills,
):

    print()
    print("=" * 70)
    print(f"STAGE 2 — 27 SKILLS DEEP PROCESSING: {date}")
    print("=" * 70)

    if skills_complete(date):

        print(
            f"✅ {date} 27 Skills已经完成，跳过。"
        )

        return False

    events = load_saved_event_units(
        date
    )

    print(
        f"Event Units loaded: "
        f"{len(events)}"
    )

    categories = list(
        routes.keys()
    )

    if not categories:

        raise RuntimeError(
            "skill_routes.json没有类别"
        )

    analyses = []

    category_count = {}

    for index, event in enumerate(
        events,
        start=1
    ):

        print()
        print("=" * 70)

        print(
            f"[{index}/{len(events)}] "
            f"{event['event_id']}"
        )

        print(
            f"Event: "
            f"{event['event_title']}"
        )

        print(
            f"Sources: "
            f"{event['source_count']}"
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
        # Skills
        # ----------------------------------------------------

        selected_skills = route_skills(

            category,

            routes,

            skills
        )

        if not selected_skills:

            raise RuntimeError(
                f"❌ {event['event_id']} "
                f"没有匹配Skills"
            )

        print(
            "Skills:"
        )

        for skill in selected_skills:

            print(
                f"  - {skill['name']}"
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
                "Skills分析为空"
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
> 聚合来源数：{event['source_count']}
>
> Event Unit：{event['aggregated_path']}

"""

        analyses.append(
            header + analysis
        )

        category_count[
            category
        ] = (
            category_count.get(
                category,
                0
            )
            + 1
        )

    if len(analyses) != len(events):

        raise RuntimeError(
            f"❌ {date} Skills分析数量异常"
        )

    # ========================================================
    # 知识卡片
    # ========================================================

    print()
    print("=" * 70)
    print(
        f"Generating knowledge cards for {date}..."
    )

    knowledge = generate_knowledge_cards(
        date,
        analyses
    )

    if not knowledge.strip():

        raise RuntimeError(
            f"❌ {date} 知识卡片为空"
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
            f"❌ {date} 专题为空"
        )

    topic_path = save_topics(
        date,
        topics
    )

    print(
        f"✅ Topics: {topic_path}"
    )

    # ========================================================
    # Watchlist
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
            f"❌ {date} Watchlist为空"
        )

    # ========================================================
    # 日报
    # ========================================================

    report_path = save_daily_report(

        date,

        analyses,

        knowledge,

        topics,

        watchlist,

        len(events)
    )

    if not report_path.exists():

        raise RuntimeError(
            f"❌ {date} 日报没有生成"
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

    log_path.write_text(

        f"""# {date} Knowledge Pipeline V4

- 时间：{now().isoformat()}
- 时区：Asia/Shanghai
- Event Units：{len(events)}
- Skills分析：{len(analyses)}
- Skills总数：{len(skills)}
- 路由类别：{len(routes)}
- AI Provider：AGNES.ai
- AI Model：{AGNES_MODEL}

## 正式处理架构

Enriched News
→ AI事件聚类
→ 跨批次事件合并
→ Event Units
→ 多来源综合
→ 保存EventUnits
→ Git Push
→ 本地重新拉取
→ 27 Skills
→ 知识卡片
→ 专题
→ Watchlist
→ 日报
→ 自生长

## 日期隔离

本日期：
{date}

三天独立处理。
不会将三天新闻混合。

## Event Units

数量：{len(events)}

目录：

Raw News/{date}-EventUnits/

## 分类统计

{
chr(10).join(
    f"- {k}: {v}"
    for k, v
    in sorted(
        category_count.items()
    )
)
}

## 输出

- Event Units：Raw News/{date}-EventUnits/
- 日报：{report_path}
- 知识卡片：{knowledge_path}
- 专题：{topic_path}

## 状态

SUCCESS
""",

        encoding="utf-8"
    )

    marker = mark_skills_complete(
        date,
        len(events)
    )

    print(
        f"✅ Skills Complete Marker: "
        f"{marker}"
    )

    print()
    print("=" * 70)
    print(
        f"✅ STAGE 2 COMPLETE: {date}"
    )
    print("=" * 70)

    return True


# ============================================================
# 统一入口
# ============================================================

def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--date",
        required=True
    )

    parser.add_argument(
        "--stage",
        required=True,
        choices=[
            "aggregation",
            "skills"
        ]
    )

    args = parser.parse_args()

    date = args.date

    print("=" * 70)
    print("748686 KNOWLEDGE PIPELINE V4")
    print("=" * 70)

    print(
        f"Date: {date}"
    )

    print(
        f"Stage: {args.stage}"
    )

    print(
        "Timezone: Asia/Shanghai"
    )

    print(
        "AI Provider: AGNES.ai"
    )

    print(
        f"AI Model: {AGNES_MODEL}"
    )

    print()

    # --------------------------------------------------------
    # 目录
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
    # API
    # --------------------------------------------------------

    if not os.getenv(
        AGNES_API_KEY_ENV,
        ""
    ).strip():

        raise RuntimeError(
            "❌ 未检测到 AGNES_API_KEY"
        )

    print(
        "✅ AGNES_API_KEY detected"
    )

    # --------------------------------------------------------
    # Stage 1
    # --------------------------------------------------------

    if args.stage == "aggregation":

        run_stage_1(
            date
        )

        print()
        print(
            "============================================================"
        )

        print(
            "STAGE 1 ONLY"
        )

        print(
            "EventUnits已经落盘。"
        )

        print(
            "现在可以Git commit + push。"
        )

        print(
            "之后再进入Stage 2。"
        )

        print(
            "============================================================"
        )

        return

    # --------------------------------------------------------
    # Stage 2
    # --------------------------------------------------------

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

    run_stage_2(

        date,

        routes,

        skills
    )


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
            "❌ KNOWLEDGE PIPELINE V4 FAILED"
        )

        print("=" * 70)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print()

        sys.exit(1)
