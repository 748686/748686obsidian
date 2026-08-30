#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V6

================================================================
正式架构
================================================================

Horizon
   ↓
Atomic News
   ↓
Source Enrichment
   ↓
Enriched News
   ↓
STAGE 1：第二层 AI 事件聚合
   ↓
全部 Enriched News
   ↓
AI 第一轮批量事件聚类
   ↓
重叠窗口全局事件归并
   ↓
全局事件收敛
   ↓
Final Event Units
   ↓
AI 多来源事件综合
   ↓
Raw News/YYYY-MM-DD-EventUnits/
   ├── _event_index.json
   ├── EVT-xxxx_事件名称.md
   └── _EVENT_UNITS_COMPLETE

   ↓ Git commit + push（外层 Workflow）
   ↓ git pull
   ↓
STAGE 2：27 Skills 深度处理


================================================================
V6 核心改进
================================================================

V5存在的核心问题：

    Cluster Batch 1
    Cluster Batch 2
    Cluster Batch 3
         ↓
    同一事件如果落在不同Batch，
    在该轮AI中可能永远无法相遇。

V6改为：

    Stage 1A
         ↓
    初始Clusters
         ↓
    Stage 1B
         ↓
    重叠窗口全局归并
         ↓
    Window Size = 30
    Overlap = 15
         ↓
    同一事件即使跨原始Batch，
    也能够在相邻窗口中相遇。
         ↓
    每轮结束后重新构建Cluster
         ↓
    下一轮继续归并
         ↓
    直到Cluster数量不再下降
    或达到安全最大轮次。
         ↓
    最终全局Event Units


================================================================
核心规则
================================================================

1. Horizon完全由Horizon管理。
2. 本程序不读取Horizon Config。
3. 本程序不启动Horizon。
4. 本程序只处理已经存在的Enriched News。
5. AI使用AGNES.ai。
6. API Key从AGNES_API_KEY读取。
7. 模型固定agnes-2.5-flash。
8. Base URL固定https://api.agnes-ai.cn/v1。
9. 不设置max_tokens。
10. 日期统一Asia/Shanghai。
11. 不限制Enriched News数量。
12. 所有有效Enriched News都进入Stage 1。
13. Stage 1每批最多40篇。
14. Stage 1必须覆盖全部新闻。
15. Stage 1支持跨来源。
16. Stage 1支持跨语言。
17. Stage 1同事件尽量归并。
18. 不同事件不得强行合并。
19. 一篇文章最终只能属于一个EventUnit。
20. AI返回重复ARTICLE ID时，不静默吞掉。
21. 发现重复ARTICLE ID时记录冲突日志，并自动要求AI重新修复。
22. 修复后仍失败立即退出。
23. EventUnits目录存在则优先断点检查。
24. 有效Event Index存在时，不重新执行事件聚类。
25. Index无效时重新建立完整Event Index。
26. 所有EventUnit实际文件存在且有效后才生成完成标记。
27. Stage 1完成后立即退出。
28. Stage 2只读取已经保存的EventUnits。
29. Stage 2不重新读取原始Enriched News。
30. 三天由外层Workflow分别调用。
31. Source Enrichment不在本程序内处理。
32. Git commit/push/pull不在本程序内处理。
33. V6跨批次事件归并采用重叠窗口。
34. 每一轮归并后检查文章集合是否发生变化。
35. 绝不因为程序方便而自动抢文章归属。
36. 最终Event Index必须100%覆盖全部Enriched News。
"""


from __future__ import annotations

import argparse
import json
import os
import re
import sys

from pathlib import Path
from datetime import datetime
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
# Event Units
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnits"

EVENT_INDEX_FILE = "_event_index.json"

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
# Stage 1 参数
# ============================================================

# 第一层：新闻 → 初始Cluster
AGGREGATION_BATCH_SIZE = 40

# 第二层：Cluster → 全局事件
GLOBAL_MERGE_WINDOW_SIZE = 30

# V6关键：
# 相邻窗口之间重叠15个Cluster。
GLOBAL_MERGE_OVERLAP = 15

# 最大全局归并轮次，防止异常情况下无限循环。
MAX_GLOBAL_MERGE_ROUNDS = 12

# 单次Event最多给AI多少文章上下文。
MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000


# ============================================================
# AI聚类冲突自动修复
# ============================================================

CLUSTER_REPAIR_ATTEMPTS = 2


# ============================================================
# 北京时间
# ============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


def now() -> datetime:
    return datetime.now(BEIJING_TZ)


# ============================================================
# 冲突日志
# ============================================================

def conflict_log_path(date: str) -> Path:
    return LOGS / f"{date}_event_aggregation_conflicts.log"


def log_conflict(
    date: str,
    stage: str,
    message: str,
    details=None,
):
    """
    写入事件聚类冲突日志。

    不记录API Key。
    """

    LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

    path = conflict_log_path(date)

    lines = [
        "",
        "=" * 80,
        f"TIME: {now().isoformat()}",
        f"DATE: {date}",
        f"STAGE: {stage}",
        f"MESSAGE: {message}",
    ]

    if details is not None:

        try:

            if isinstance(
                details,
                str
            ):

                detail_text = details

            else:

                detail_text = json.dumps(
                    details,
                    ensure_ascii=False,
                    indent=2
                )

        except Exception:

            detail_text = str(details)

        lines.append(
            "DETAILS:"
        )

        lines.append(
            detail_text
        )

    lines.append(
        "=" * 80
    )

    lines.append("")

    with path.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print()
    print(
        "⚠️ EVENT AGGREGATION CONFLICT"
    )

    print(
        f"   Stage  : {stage}"
    )

    print(
        f"   Message: {message}"
    )

    if details is not None:

        print(
            "   Details:"
        )

        print(
            str(details)[:5000]
        )

    print(
        f"   Conflict log: {path}"
    )


# ============================================================
# JSON
# ============================================================

def read_json(
    path: Path,
    default=None
):

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


def write_json(
    path: Path,
    data
):

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

def parse_ai_json(
    result: str,
    context: str
):

    text = str(
        result
    ).strip()

    if text.startswith(
        "```"
    ):

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

        return json.loads(
            text
        )

    except Exception as exc:

        raise RuntimeError(
            f"❌ AI JSON解析失败：{context}\n\n"
            f"AI原始返回：\n{text[:5000]}"
        ) from exc


# ============================================================
# 文件名
# ============================================================

def safe_name(
    text: str
):

    text = str(
        text or ""
    )

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

    return (
        text[:120]
        or "未命名"
    )


# ============================================================
# Front Matter
# ============================================================

def parse_front_matter(
    content: str
):

    if not content.startswith(
        "---"
    ):

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

        value = (
            value
            .strip('"')
            .strip("'")
        )

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

        "model":
            AGNES_MODEL,

        "messages": [

            {
                "role":
                    "system",

                "content":
                    system_prompt,
            },

            {
                "role":
                    "user",

                "content":
                    prompt,
            },

        ],

        "temperature":
            temperature,
    }

    payload = json.dumps(
        payload_data,
        ensure_ascii=False
    ).encode(
        "utf-8"
    )

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
                "748686-Knowledge-Pipeline/6.0",
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
                .decode(
                    "utf-8"
                )
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

    if not result or not str(
        result
    ).strip():

        raise RuntimeError(
            "❌ AGNES.ai 返回空内容"
        )

    return str(
        result
    ).strip()


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

            "name":
                path.name,

            "path":
                str(path),

            "content":
                content,
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

def get_enriched_files(
    date
):

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


def load_news_file(
    path
):

    content = path.read_text(
        encoding="utf-8",
        errors="replace"
    )

    metadata, body = parse_front_matter(
        content
    )

    return {

        "path":
            path,

        "metadata":
            metadata,

        "body":
            body,

        "content":
            content,
    }


def is_news(
    item
):

    title = item[
        "metadata"
    ].get(
        "title",
        ""
    ).strip()

    return bool(
        title
    )


def load_all_enriched_news(
    date
):

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

        if is_news(
            item
        ):

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

    # Horizon Score只负责排序，不负责截断。
    def score(item):

        try:

            return float(
                item[
                    "metadata"
                ].get(
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

    return news_items


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
# 聚类结果冲突检测
# ============================================================

def inspect_cluster_assignment(
    clusters,
    expected_indexes,
):

    expected = set(
        int(x)
        for x in expected_indexes
    )

    occurrences = {}

    malformed = []

    for cluster_position, cluster in enumerate(
        clusters,
        start=1
    ):

        if not isinstance(
            cluster,
            dict
        ):

            malformed.append(
                f"cluster[{cluster_position}]不是对象"
            )

            continue

        indexes = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            indexes,
            list
        ):

            malformed.append(
                f"cluster[{cluster_position}] article_indexes不是数组"
            )

            continue

        if not indexes:

            malformed.append(
                f"cluster[{cluster_position}]为空Cluster"
            )

            continue

        for raw_index in indexes:

            try:

                article_index = int(
                    raw_index
                )

            except Exception:

                malformed.append(
                    f"cluster[{cluster_position}]存在无法转换的ARTICLE ID：{raw_index}"
                )

                continue

            occurrences.setdefault(
                article_index,
                []
            ).append(
                cluster_position
            )

    duplicate = {

        article_index:
            positions

        for article_index, positions
        in occurrences.items()

        if len(positions) > 1
    }

    actual = set(
        occurrences.keys()
    )

    missing = sorted(
        expected - actual
    )

    extra = sorted(
        actual - expected
    )

    return {

        "duplicate":
            duplicate,

        "missing":
            missing,

        "extra":
            extra,

        "malformed":
            malformed,
    }


def cluster_assignment_is_valid(
    issues
):

    return not any(
        [
            issues[
                "duplicate"
            ],

            issues[
                "missing"
            ],

            issues[
                "extra"
            ],

            issues[
                "malformed"
            ],
        ]
    )


# ============================================================
# 聚类结果规范化
# ============================================================

def normalize_cluster_indexes(
    clusters
):

    normalized = []

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict
        ):

            normalized.append(
                cluster
            )

            continue

        copied = dict(
            cluster
        )

        indexes = copied.get(
            "article_indexes",
            []
        )

        if isinstance(
            indexes,
            list
        ):

            converted = []

            for value in indexes:

                try:

                    converted.append(
                        int(value)
                    )

                except Exception:

                    converted.append(
                        value
                    )

            copied[
                "article_indexes"
            ] = converted

        normalized.append(
            copied
        )

    return normalized


# ============================================================
# 第一轮AI聚类
# ============================================================

def cluster_news_batch(
    date,
    batch_items,
    batch_start_index,
):

    articles = []

    expected_indexes = list(
        range(
            batch_start_index,
            batch_start_index
            + len(batch_items)
        )
    )

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

    prompt = f"""
你现在正在执行748686自生长知识系统V6第二层事件聚合。

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
绝对覆盖要求
============================================================

本批输入ARTICLE编号为：

{json.dumps(
    expected_indexes,
    ensure_ascii=False
)}

输入中的每一篇ARTICLE：

必须且只能属于一个cluster。

如果某ARTICLE无法与任何其他文章合并：

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

============================================================
输出前强制自检
============================================================

1. ARTICLE总覆盖数必须等于输入ARTICLE数量。
2. 每个ARTICLE必须只出现一次。
3. 不得出现重复ARTICLE ID。
4. 不得出现输入之外的ARTICLE ID。
5. 不得遗漏ARTICLE。
6. 每个cluster至少包含一个ARTICLE。
7. cluster_id必须唯一。

只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是全球新闻事件聚类专家。"
            "每篇ARTICLE必须且只能归属于一个cluster。"
            "绝对禁止重复ARTICLE ID。"
            "绝对禁止遗漏ARTICLE。"
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

    return normalize_cluster_indexes(
        clusters
    )


# ============================================================
# AI聚类冲突修复
# ============================================================

def repair_cluster_news_batch(
    date,
    batch_items,
    batch_start_index,
    broken_clusters,
    issues,
    attempt,
):

    articles = []

    expected_indexes = list(
        range(
            batch_start_index,
            batch_start_index
            + len(batch_items)
        )
    )

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

    joined_articles = "\n\n".join(
        articles
    )

    broken_json = json.dumps(
        broken_clusters,
        ensure_ascii=False,
        indent=2
    )

    issue_json = json.dumps(
        issues,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
你正在修复748686自生长知识系统V6中的ARTICLE覆盖冲突。

日期：
{date}

修复次数：
第 {attempt} 次

============================================================
本批真实ARTICLE
============================================================

{joined_articles}

============================================================
AI上一次错误聚类
============================================================

{broken_json}

============================================================
检测到的冲突
============================================================

{issue_json}

============================================================
修复要求
============================================================

重新检查全部ARTICLE。

必须满足：

1. 同一个现实世界事件尽量归入同一个cluster。
2. 不同现实世界事件不能强行合并。
3. 一篇ARTICLE只能属于一个cluster。
4. 一篇ARTICLE不能出现在两个cluster。
5. 不允许遗漏任何ARTICLE。
6. 不允许创造任何ARTICLE编号。
7. 不允许修改ARTICLE编号。
8. 无法合并的ARTICLE单独成为cluster。
9. 不确定时宁可分开。
10. 必须重新依据文章内容判断。

============================================================
本批ARTICLE编号
============================================================

{json.dumps(
    expected_indexes,
    ensure_ascii=False
)}

============================================================
最终强制检查
============================================================

Missing = 0
Duplicate = 0
Extra = 0

输入ARTICLE数量
必须等于
输出ARTICLE归属总数。

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
      "event_reason": "事件判断"
    }}
  ]
}}
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是新闻事件聚类冲突修复专家。"
            "一篇ARTICLE绝对不能属于多个cluster。"
            "绝对不能遗漏ARTICLE。"
            "绝对不能创造ARTICLE编号。"
            "必须返回合法JSON。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        f"{date} 聚类冲突修复 #{attempt}"
    )

    clusters = data.get(
        "clusters"
    )

    if not isinstance(
        clusters,
        list
    ):

        raise RuntimeError(
            f"❌ {date} 聚类修复结果缺少clusters"
        )

    return normalize_cluster_indexes(
        clusters
    )


# ============================================================
# 带自动修复的第一轮聚类
# ============================================================

def cluster_news_batch_with_repair(
    date,
    batch_items,
    batch_start_index,
    batch_number,
):

    expected_indexes = list(
        range(
            batch_start_index,
            batch_start_index
            + len(batch_items)
        )
    )

    clusters = cluster_news_batch(

        date,

        batch_items,

        batch_start_index
    )

    issues = inspect_cluster_assignment(

        clusters,

        expected_indexes
    )

    if cluster_assignment_is_valid(
        issues
    ):

        return clusters

    log_conflict(

        date,

        f"STAGE 1A / BATCH {batch_number}",

        "AI第一次聚类返回非法ARTICLE归属，启动自动修复。",

        {
            "batch_number":
                batch_number,

            "expected_indexes":
                expected_indexes,

            "issues":
                issues,

            "broken_clusters":
                clusters,
        }
    )

    repaired_clusters = clusters

    repaired_issues = issues

    for attempt in range(
        1,
        CLUSTER_REPAIR_ATTEMPTS + 1
    ):

        print()
        print(
            f"🔧 Cluster conflict repair "
            f"{attempt}/{CLUSTER_REPAIR_ATTEMPTS}"
        )

        repaired_clusters = repair_cluster_news_batch(

            date,

            batch_items,

            batch_start_index,

            repaired_clusters,

            repaired_issues,

            attempt
        )

        repaired_issues = inspect_cluster_assignment(

            repaired_clusters,

            expected_indexes
        )

        if cluster_assignment_is_valid(
            repaired_issues
        ):

            print(
                "   ✅ Cluster conflict repaired successfully."
            )

            return repaired_clusters

        log_conflict(

            date,

            f"STAGE 1A / BATCH {batch_number}",

            f"第{attempt}次聚类冲突修复仍然失败。",

            {
                "repair_attempt":
                    attempt,

                "issues":
                    repaired_issues,

                "clusters":
                    repaired_clusters,
            }
        )

    raise RuntimeError(

        f"❌ {date} Batch {batch_number} "
        f"ARTICLE聚类覆盖冲突无法自动修复。\n"
        f"Duplicate={repaired_issues['duplicate']}\n"
        f"Missing={repaired_issues['missing']}\n"
        f"Extra={repaired_issues['extra']}\n"
        f"Malformed={repaired_issues['malformed']}\n"
        f"详细日志：{conflict_log_path(date)}"
    )


# ============================================================
# Cluster覆盖检查
# ============================================================

def validate_cluster_coverage(
    clusters,
    expected_indexes,
    context,
    date=None,
):

    issues = inspect_cluster_assignment(

        clusters,

        expected_indexes
    )

    if cluster_assignment_is_valid(
        issues
    ):

        return

    if date:

        log_conflict(

            date,

            context,

            "聚类覆盖验证失败。",

            {
                "expected_indexes":
                    list(expected_indexes),

                "issues":
                    issues,

                "clusters":
                    clusters,
            }
        )

    raise RuntimeError(

        f"❌ {context} 聚类覆盖失败\n"
        f"Duplicate={issues['duplicate']}\n"
        f"Missing={issues['missing']}\n"
        f"Extra={issues['extra']}\n"
        f"Malformed={issues['malformed']}"
    )


# ============================================================
# Stage 1A
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
    print(
        "=" * 70
    )

    print(
        "STAGE 1A — AI EVENT CLUSTERING"
    )

    print(
        "=" * 70
    )

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

        clusters = cluster_news_batch_with_repair(

            date,

            batch_items,

            start + 1,

            batch_number
        )

        validate_cluster_coverage(

            clusters,

            list(
                range(
                    start + 1,
                    end + 1
                )
            ),

            f"{date} Batch {batch_number}",

            date=date
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

    validate_cluster_coverage(

        all_clusters,

        list(
            range(
                1,
                total + 1
            )
        ),

        f"{date} Stage 1A GLOBAL",

        date=date
    )

    print()
    print(
        f"✅ Initial Clusters: "
        f"{len(all_clusters)}"
    )

    print(
        f"✅ Stage 1A coverage: "
        f"{total}/{total}"
    )

    return all_clusters


# ============================================================
# V6 Cluster窗口
# ============================================================

def build_merge_windows(
    clusters
):

    total = len(
        clusters
    )

    if total <= GLOBAL_MERGE_WINDOW_SIZE:

        return [
            clusters
        ]

    step = (
        GLOBAL_MERGE_WINDOW_SIZE
        - GLOBAL_MERGE_OVERLAP
    )

    if step <= 0:

        raise RuntimeError(
            "❌ GLOBAL_MERGE_WINDOW_SIZE必须大于GLOBAL_MERGE_OVERLAP"
        )

    windows = []

    start = 0

    while start < total:

        end = min(
            start
            + GLOBAL_MERGE_WINDOW_SIZE,
            total
        )

        window = clusters[
            start:end
        ]

        windows.append(
            window
        )

        if end >= total:

            break

        start += step

    return windows


# ============================================================
# Cluster描述
# ============================================================

def build_cluster_descriptor(
    cluster,
    local_index
):

    return f"""
[CLUSTER {local_index}]

Cluster ID：
{cluster["cluster_id"]}

事件名称：
{cluster.get("event_title", "未命名事件")}

事件判断：
{cluster.get("event_reason", "")}

文章数量：
{len(cluster.get("article_indexes", []))}

文章编号：
{json.dumps(
    cluster.get(
        "article_indexes",
        []
    ),
    ensure_ascii=False
)}
"""


# ============================================================
# V6窗口AI归并
# ============================================================

def merge_cluster_window(
    date,
    window,
    merge_round,
    window_index,
):

    descriptors = []

    for index, cluster in enumerate(
        window,
        start=1
    ):

        descriptors.append(
            build_cluster_descriptor(
                cluster,
                index
            )
        )

    joined = "\n\n".join(
        descriptors
    )

    if not joined.strip():

        raise RuntimeError(
            f"❌ {date} Global Merge输入为空"
        )

    expected_indexes = list(
        range(
            1,
            len(window) + 1
        )
    )

    prompt = f"""
你正在执行748686自生长知识系统V6的全局事件归并。

日期：
{date}

全局归并轮次：
{merge_round}

当前窗口：
{window_index}

============================================================
重要说明
============================================================

这些Cluster来自前面的新闻事件聚类。

现在不是判断“主题是否相似”。

而是判断：

这些Cluster是否描述同一个现实世界事件。

必须区分：

同事件

和

同主题。

============================================================
Cluster输入
============================================================

{joined}

============================================================
合并原则
============================================================

可以合并：

- 同一个具体现实世界事件
- 同一次政策发布
- 同一次公司重大动作
- 同一次产品发布
- 同一次事故
- 同一次会议中的同一具体事件
- 同一个具体市场事件
- 同一个人物具体事件
- 不同国家/语言媒体对同一事件的报道

不得合并：

- 同一公司不同事件
- 同一人物不同事件
- 同一行业不同事件
- 同一政策领域不同政策
- 同一产品不同版本事件
- 同一个长期趋势中的不同具体事件
- 仅仅因为关键词相同而相关的事件

如果无法确认：

宁可分开。

============================================================
绝对覆盖要求
============================================================

输入Cluster编号：

{json.dumps(
    expected_indexes,
    ensure_ascii=False
)}

每个输入Cluster必须：

且只能：

进入一个group。

不得遗漏。

不得重复。

不得创造不存在的Cluster编号。

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
      "reason": "为什么这些Cluster属于同一个现实世界事件"
    }},
    {{
      "group_id": "G002",
      "cluster_indexes": [2],
      "event_title": "独立事件",
      "reason": "为什么独立"
    }}
  ]
}}

============================================================
输出前必须自检
============================================================

1. 输入Cluster数量 = 输出Cluster归属总数。
2. 每个Cluster出现恰好一次。
3. Duplicate = 0。
4. Missing = 0。
5. Extra = 0。
6. 每个group至少一个Cluster。
7. group_id唯一。

只输出JSON。
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是全球新闻事件归并专家。"
            "当前任务是判断Cluster是否属于同一个现实世界事件。"
            "必须覆盖全部输入Cluster。"
            "每个Cluster必须且只能进入一个group。"
            "不得强行合并。"
            "必须返回合法JSON。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        (
            f"{date} "
            f"Global Merge Round {merge_round} "
            f"Window {window_index}"
        )
    )

    groups = data.get(
        "groups"
    )

    if not isinstance(
        groups,
        list
    ):

        raise RuntimeError(
            f"❌ {date} Global Merge缺少groups"
        )

    actual = []

    malformed = []

    for group_position, group in enumerate(
        groups,
        start=1
    ):

        if not isinstance(
            group,
            dict
        ):

            malformed.append(
                f"group[{group_position}]不是对象"
            )

            continue

        indexes = group.get(
            "cluster_indexes"
        )

        if not isinstance(
            indexes,
            list
        ):

            malformed.append(
                f"group[{group_position}] cluster_indexes不是数组"
            )

            continue

        if not indexes:

            malformed.append(
                f"group[{group_position}]为空"
            )

            continue

        for value in indexes:

            try:

                actual.append(
                    int(value)
                )

            except Exception:

                malformed.append(
                    f"group[{group_position}]非法Cluster编号：{value}"
                )

    duplicate = sorted(
        {
            x
            for x in actual
            if actual.count(x) > 1
        }
    )

    expected = set(
        expected_indexes
    )

    actual_set = set(
        actual
    )

    missing = sorted(
        expected
        - actual_set
    )

    extra = sorted(
        actual_set
        - expected
    )

    if (
        duplicate
        or
        missing
        or
        extra
        or
        malformed
    ):

        log_conflict(

            date,

            (
                f"STAGE 1B / ROUND {merge_round} "
                f"/ WINDOW {window_index}"
            ),

            "V6 Global Merge窗口覆盖异常。",

            {
                "duplicate":
                    duplicate,

                "missing":
                    missing,

                "extra":
                    extra,

                "malformed":
                    malformed,

                "groups":
                    groups,
            }
        )

        raise RuntimeError(

            f"❌ {date} Global Merge覆盖异常\n"
            f"Duplicate={duplicate}\n"
            f"Missing={missing}\n"
            f"Extra={extra}\n"
            f"Malformed={malformed}"
        )

    return groups


# ============================================================
# 根据窗口结果生成局部归并Cluster
# ============================================================

def build_window_merged_clusters(
    window,
    groups,
    merge_round,
    window_index,
):

    result = []

    for group_position, group in enumerate(
        groups,
        start=1
    ):

        article_indexes = []

        titles = []

        reasons = []

        for cluster_index in group[
            "cluster_indexes"
        ]:

            source_cluster = window[
                int(cluster_index) - 1
            ]

            article_indexes.extend(
                source_cluster[
                    "article_indexes"
                ]
            )

            titles.append(
                source_cluster.get(
                    "event_title",
                    ""
                )
            )

            reasons.append(
                source_cluster.get(
                    "event_reason",
                    ""
                )
            )

        result.append({

            "cluster_id":
                (
                    f"R{merge_round:02d}"
                    f"W{window_index:03d}"
                    f"G{group_position:03d}"
                ),

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

    return result


# ============================================================
# Cluster唯一性辅助
# ============================================================

def article_signature(
    cluster
):

    return tuple(
        sorted(
            set(
                int(x)
                for x in cluster.get(
                    "article_indexes",
                    []
                )
            )
        )
    )


def cluster_signature(
    cluster
):

    return article_signature(
        cluster
    )


# ============================================================
# V6重叠窗口全局归并
# ============================================================

def merge_all_clusters(
    date,
    clusters,
    news_count,
):

    current = clusters

    print()
    print(
        "=" * 70
    )

    print(
        "STAGE 1B — V6 GLOBAL EVENT MERGING"
    )

    print(
        "=" * 70
    )

    print(
        f"Initial Clusters: {len(current)}"
    )

    print(
        f"Window Size: {GLOBAL_MERGE_WINDOW_SIZE}"
    )

    print(
        f"Window Overlap: {GLOBAL_MERGE_OVERLAP}"
    )

    print(
        f"Max Rounds: {MAX_GLOBAL_MERGE_ROUNDS}"
    )

    # --------------------------------------------------------
    # 如果初始Cluster已经很少，
    # 仍然进行一次全局判断。
    # --------------------------------------------------------

    for merge_round in range(
        1,
        MAX_GLOBAL_MERGE_ROUNDS + 1
    ):

        print()
        print(
            "=" * 70
        )

        print(
            f"GLOBAL MERGE ROUND {merge_round}"
        )

        print(
            "=" * 70
        )

        before_count = len(
            current
        )

        print(
            f"Input Clusters: {before_count}"
        )

        # ----------------------------------------------------
        # 如果只有一个Cluster，不需要AI合并。
        # ----------------------------------------------------

        if before_count == 1:

            print(
                "   Only one cluster remains."
            )

            break

        windows = build_merge_windows(
            current
        )

        print(
            f"Windows: {len(windows)}"
        )

        print(
            f"Overlap: {GLOBAL_MERGE_OVERLAP}"
        )

        # ----------------------------------------------------
        # V6核心：
        #
        # 每个窗口独立AI判断。
        #
        # 由于窗口重叠：
        #
        # Window 1:
        #   C1 ... C30
        #
        # Window 2:
        #   C16 ... C45
        #
        # Window 3:
        #   C31 ... C60
        #
        # 同一个事件即使跨原始边界，
        # 也有机会在Overlap窗口中相遇。
        # ----------------------------------------------------

        window_results = []

        for window_index, window in enumerate(
            windows,
            start=1
        ):

            start_cluster = (
                1
                + (
                    window_index - 1
                )
                * (
                    GLOBAL_MERGE_WINDOW_SIZE
                    - GLOBAL_MERGE_OVERLAP
                )
            )

            end_cluster = (
                start_cluster
                + len(window)
                - 1
            )

            print()
            print(
                f"🔹 Window {window_index}/"
                f"{len(windows)}"
                f" | clusters "
                f"{start_cluster}-"
                f"{end_cluster}"
                f" | size={len(window)}"
            )

            groups = merge_cluster_window(

                date,

                window,

                merge_round,

                window_index
            )

            merged = build_window_merged_clusters(

                window,

                groups,

                merge_round,

                window_index
            )

            print(
                f"   Input : {len(window)}"
            )

            print(
                f"   Output: {len(merged)}"
            )

            window_results.append(
                merged
            )

        # ----------------------------------------------------
        # 将重叠窗口结果重新统一。
        #
        # 同一Cluster可能在两个窗口中出现，
        # 因此不能简单append。
        #
        # 这里使用“文章集合签名”进行确定性去重。
        # 如果两个窗口产生完全相同文章集合，
        # 认为是同一个中间Cluster。
        # ----------------------------------------------------

        dedup = {}

        for merged_window in window_results:

            for cluster in merged_window:

                signature = cluster_signature(
                    cluster
                )

                if not signature:

                    raise RuntimeError(
                        f"❌ {date} "
                        "V6 Global Merge产生空Cluster"
                    )

                if signature not in dedup:

                    dedup[
                        signature
                    ] = cluster

                else:

                    # ------------------------------------------------
                    # 相同文章集合来自多个重叠窗口。
                    #
                    # 保留更完整的标题/判断。
                    # 不重新调用AI。
                    # ------------------------------------------------

                    existing = dedup[
                        signature
                    ]

                    if (
                        len(
                            cluster.get(
                                "event_reason",
                                ""
                            )
                        )
                        >
                        len(
                            existing.get(
                                "event_reason",
                                ""
                            )
                        )
                    ):

                        dedup[
                            signature
                        ] = cluster

        merged_unique = list(
            dedup.values()
        )

        # ----------------------------------------------------
        # 注意：
        #
        # 仅仅去重还不够。
        #
        # 如果：
        #
        # Window 1:
        #   [ARTICLE 1,2]
        #
        # Window 2:
        #   [ARTICLE 2,3]
        #
        # 那么它们不是同一签名。
        #
        # 需要继续下一轮，
        # 让这些跨窗口事件再次相遇。
        # ----------------------------------------------------

        merged_unique.sort(
            key=lambda x: (
                min(
                    x[
                        "article_indexes"
                    ]
                )
                if x[
                    "article_indexes"
                ]
                else 999999
            )
        )

        # ----------------------------------------------------
        # 全局覆盖检查
        # ----------------------------------------------------

        global_indexes = []

        for cluster in merged_unique:

            global_indexes.extend(
                cluster[
                    "article_indexes"
                ]
            )

        if (
            len(global_indexes)
            != len(
                set(global_indexes)
            )
        ):

            duplicates = sorted(
                {
                    x
                    for x in global_indexes
                    if global_indexes.count(x) > 1
                }
            )

            log_conflict(

                date,

                f"STAGE 1B / ROUND {merge_round}",

                "V6重叠窗口合并后发现ARTICLE重复归属。",

                {
                    "duplicates":
                        duplicates
                }
            )

            raise RuntimeError(

                f"❌ {date} "
                f"Global Merge Round {merge_round} "
                f"出现重复ARTICLE："
                f"{duplicates}"
            )

        actual = set(
            global_indexes
        )

        expected = set(
            range(
                1,
                news_count + 1
            )
        )

        missing = sorted(
            expected
            - actual
        )

        extra = sorted(
            actual
            - expected
        )

        if missing or extra:

            log_conflict(

                date,

                f"STAGE 1B / ROUND {merge_round}",

                "V6重叠窗口合并后文章覆盖发生变化。",

                {
                    "missing":
                        missing,

                    "extra":
                        extra,
                }
            )

            raise RuntimeError(

                f"❌ {date} "
                f"Global Merge Round {merge_round} "
                f"覆盖异常\n"
                f"Missing={missing}\n"
                f"Extra={extra}"
            )

        after_count = len(
            merged_unique
        )

        print()
        print(
            f"✅ Round {merge_round} result: "
            f"{after_count} clusters"
        )

        print(
            f"   Before: {before_count}"
        )

        print(
            f"   After : {after_count}"
        )

        # ----------------------------------------------------
        # 收敛判断
        #
        # 如果数量完全没有变化，
        # 说明这一轮没有进一步合并。
        #
        # 继续一轮没有意义，
        # 因为输入Cluster结构已经稳定。
        # ----------------------------------------------------

        if after_count >= before_count:

            print()
            print(
                "🟢 GLOBAL MERGE CONVERGED"
            )

            print(
                "   本轮没有继续减少Event Cluster。"
            )

            current = merged_unique

            break

        current = merged_unique

    else:

        # ----------------------------------------------------
        # 达到最大轮次。
        #
        # 不是静默失败。
        # 记录日志并使用当前已经验证覆盖完整的结果。
        # ----------------------------------------------------

        log_conflict(

            date,

            "STAGE 1B",

            (
                f"达到最大全局归并轮次 "
                f"{MAX_GLOBAL_MERGE_ROUNDS}。"
            ),

            {
                "final_cluster_count":
                    len(current)
            }
        )

        print()
        print(
            f"⚠️ 已达到最大Global Merge轮次："
            f"{MAX_GLOBAL_MERGE_ROUNDS}"
        )

    # ========================================================
    # 最终事件编号
    # ========================================================

    final_clusters = []

    for index, cluster in enumerate(
        current,
        start=1
    ):

        final_clusters.append({

            "event_id":
                f"EVT-{date}-"
                f"{index:04d}",

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
                sorted(
                    set(
                        int(x)
                        for x in cluster[
                            "article_indexes"
                        ]
                    )
                ),
        })

    # --------------------------------------------------------
    # 最终100%覆盖
    # --------------------------------------------------------

    final_indexes = []

    for event in final_clusters:

        final_indexes.extend(
            event[
                "article_indexes"
            ]
        )

    expected = set(
        range(
            1,
            news_count + 1
        )
    )

    actual = set(
        final_indexes
    )

    if (
        len(final_indexes)
        != len(
            set(final_indexes)
        )
    ):

        duplicates = sorted(
            {
                x
                for x in final_indexes
                if final_indexes.count(x) > 1
            }
        )

        log_conflict(

            date,

            "STAGE 1B / FINAL",

            "最终Event Units存在重复ARTICLE。",

            {
                "duplicates":
                    duplicates
            }
        )

        raise RuntimeError(

            f"❌ {date} 最终Event Units存在重复ARTICLE："
            f"{duplicates}"
        )

    if expected != actual:

        missing = sorted(
            expected
            - actual
        )

        extra = sorted(
            actual
            - expected
        )

        log_conflict(

            date,

            "STAGE 1B / FINAL",

            "最终Event Units没有100%覆盖全部新闻。",

            {
                "missing":
                    missing,

                "extra":
                    extra,
            }
        )

        raise RuntimeError(

            f"❌ {date} 最终Event Units覆盖失败\n"
            f"Missing={missing}\n"
            f"Extra={extra}"
        )

    print()
    print(
        "=" * 70
    )

    print(
        f"✅ FINAL EVENT UNITS: "
        f"{len(final_clusters)}"
    )

    print(
        f"✅ ARTICLE COVERAGE: "
        f"{len(final_indexes)}/{news_count}"
    )

    print(
        "=" * 70
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

                "index":
                    index,

                "path":
                    str(
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
# Stage 1C
# ============================================================

def synthesize_event(
    event
):

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
你现在执行748686自生长知识系统V6第二层事件知识综合。

日期：
{event["date"]}

事件ID：
{event["event_id"]}

事件名称：
{event["event_title"]}

第一轮事件判断：
{event["event_reason"]}

============================================================
同一事件的多来源输入
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
# EventUnits目录
# ============================================================

def event_units_dir(
    date
):

    return (
        RAW_NEWS
        / f"{date}-{EVENT_UNITS_SUFFIX}"
    )


# ============================================================
# EventUnit文件名
# ============================================================

def event_unit_filename(
    event
):

    return (
        f"{event['event_id']}_"
        f"{safe_name(event['event_title'])}.md"
    )


# ============================================================
# 保存EventUnit
# ============================================================

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

    filename = event_unit_filename(
        event
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
# 保存Index
# ============================================================

def save_aggregation_index(
    date,
    events
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
                event[
                    "event_id"
                ],

            "date":
                event[
                    "date"
                ],

            "event_title":
                event[
                    "event_title"
                ],

            "event_reason":
                event[
                    "event_reason"
                ],

            "source_count":
                len(
                    event[
                        "articles"
                    ]
                ),

            "articles": [

                {

                    "index":
                        article[
                            "index"
                        ],

                    "title":
                        article[
                            "title"
                        ],

                    "source":
                        article[
                            "source"
                        ],

                    "source_url":
                        article[
                            "source_url"
                        ],

                    "path":
                        article[
                            "path"
                        ],

                }

                for article in event[
                    "articles"
                ]

            ],
        })

    index_path = (
        target
        / EVENT_INDEX_FILE
    )

    write_json(
        index_path,
        serializable
    )

    return index_path


# ============================================================
# 读取Event Index
# ============================================================

def load_event_index(
    date
):

    target = event_units_dir(
        date
    )

    index_path = (
        target
        / EVENT_INDEX_FILE
    )

    if not index_path.exists():

        return None

    try:

        data = read_json(
            index_path,
            None
        )

    except Exception:

        return None

    if not isinstance(
        data,
        list
    ):

        return None

    if not data:

        return None

    return data


# ============================================================
# EventUnit文件有效性检查
# ============================================================

def event_unit_file_valid(
    path: Path,
    event_id: str
):

    if not path.exists():

        return False

    if path.stat().st_size <= 0:

        return False

    try:

        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        metadata, body = parse_front_matter(
            content
        )

    except Exception:

        return False

    if not body.strip():

        return False

    if metadata.get(
        "event_id",
        ""
    ) != event_id:

        return False

    if metadata.get(
        "status",
        ""
    ) != "completed":

        return False

    return True


# ============================================================
# 检查EventUnits完整性
# ============================================================

def inspect_event_units(
    date
):

    target = event_units_dir(
        date
    )

    print()
    print(
        "=" * 70
    )

    print(
        f"EVENT UNITS PREFLIGHT: {date}"
    )

    print(
        "=" * 70
    )

    if not target.exists():

        print(
            "📁 EventUnits目录：不存在"
        )

        print(
            "➡️ 需要创建并完整生成。"
        )

        return {

            "exists":
                False,

            "complete":
                False,

            "index":
                None,

            "missing":
                [],

            "invalid":
                [],

        }

    print(
        f"📁 EventUnits目录：{target}"
    )

    index = load_event_index(
        date
    )

    if index is None:

        print(
            "⚠️ _event_index.json不存在或无效。"
        )

        print(
            "➡️ 将重新建立完整EventUnits。"
        )

        return {

            "exists":
                True,

            "complete":
                False,

            "index":
                None,

            "missing":
                [],

            "invalid":
                [],

        }

    expected_ids = []

    missing = []

    invalid = []

    for event in index:

        event_id = str(
            event.get(
                "event_id",
                ""
            )
        ).strip()

        if not event_id:

            invalid.append(
                "missing_event_id"
            )

            continue

        expected_ids.append(
            event_id
        )

        matching = sorted(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        if not matching:

            missing.append(
                event_id
            )

            continue

        valid = any(

            event_unit_file_valid(
                path,
                event_id
            )

            for path in matching
        )

        if not valid:

            invalid.append(
                event_id
            )

    existing_event_files = sorted(
        target.glob(
            "EVT-*.md"
        )
    )

    existing_ids = set()

    for path in existing_event_files:

        match = re.match(
            r"^(EVT-\d{4}-\d{2}-\d{2}-\d+)",
            path.stem
        )

        if match:

            existing_ids.add(
                match.group(1)
            )

    expected_id_set = set(
        expected_ids
    )

    unexpected = sorted(
        existing_ids
        - expected_id_set
    )

    if unexpected:

        print(
            "⚠️ 发现Index中不存在的Event文件："
        )

        for item in unexpected:

            print(
                f"   - {item}"
            )

    complete = (
        len(missing) == 0
        and
        len(invalid) == 0
        and
        len(expected_ids) > 0
    )

    print()
    print(
        f"Index Event Units : "
        f"{len(expected_ids)}"
    )

    print(
        f"Missing           : "
        f"{len(missing)}"
    )

    print(
        f"Invalid           : "
        f"{len(invalid)}"
    )

    print(
        f"Unexpected files  : "
        f"{len(unexpected)}"
    )

    if complete:

        print(
            "✅ EventUnits内容完整。"
        )

    else:

        print(
            "⚠️ EventUnits尚未完整。"
        )

    return {

        "exists":
            True,

        "complete":
            complete,

        "index":
            index,

        "missing":
            missing,

        "invalid":
            invalid,

        "unexpected":
            unexpected,

    }


# ============================================================
# EventUnits完成标记
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


# ============================================================
# 删除错误完成标记
# ============================================================

def remove_event_units_complete(
    date
):

    marker = (
        event_units_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    if marker.exists():

        marker.unlink()

        print(
            f"🧹 已删除错误完成标记：{marker}"
        )


# ============================================================
# 根据Index重新建立Event对象
# ============================================================

def rebuild_events_from_index(
    date,
    index,
    news_items,
):

    events = []

    for record in index:

        event_id = str(
            record.get(
                "event_id",
                ""
            )
        ).strip()

        if not event_id:

            raise RuntimeError(
                "❌ Event Index存在空event_id"
            )

        articles = []

        for article_record in record.get(
            "articles",
            []
        ):

            try:

                article_index = int(
                    article_record[
                        "index"
                    ]
                )

            except Exception as exc:

                raise RuntimeError(
                    f"❌ {event_id} Index中的文章index无效"
                ) from exc

            if (
                article_index < 1
                or article_index > len(news_items)
            ):

                raise RuntimeError(
                    f"❌ {event_id} "
                    f"引用不存在文章："
                    f"{article_index}"
                )

            item = news_items[
                article_index - 1
            ]

            metadata = item[
                "metadata"
            ]

            articles.append({

                "index":
                    article_index,

                "path":
                    str(
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
                event_id,

            "date":
                date,

            "event_title":
                record.get(
                    "event_title",
                    "未命名事件"
                ),

            "event_reason":
                record.get(
                    "event_reason",
                    ""
                ),

            "articles":
                articles,
        })

    return events


# ============================================================
# 检查Index覆盖率
# ============================================================

def validate_event_index_coverage(
    date,
    events,
    news_count
):

    all_indexes = []

    event_ids = set()

    for event in events:

        event_id = event[
            "event_id"
        ]

        if event_id in event_ids:

            raise RuntimeError(
                f"❌ {date} Event Index存在重复event_id："
                f"{event_id}"
            )

        event_ids.add(
            event_id
        )

        all_indexes.extend(

            article["index"]

            for article in event[
                "articles"
            ]
        )

    expected = set(
        range(
            1,
            news_count + 1
        )
    )

    actual = set(
        all_indexes
    )

    if expected != actual:

        missing = sorted(
            expected
            - actual
        )

        extra = sorted(
            actual
            - expected
        )

        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败\n"
            f"Missing={missing}\n"
            f"Extra={extra}"
        )

    if len(all_indexes) != len(
        set(all_indexes)
    ):

        duplicates = sorted(
            {
                x
                for x in all_indexes
                if all_indexes.count(x) > 1
            }
        )

        log_conflict(

            date,

            "EVENT INDEX",

            "Event Index存在重复新闻归属。",

            {
                "duplicates":
                    duplicates
            }
        )

        raise RuntimeError(

            f"❌ {date} Event Index存在重复新闻归属："
            f"{duplicates}"
        )


# ============================================================
# 检查并补齐EventUnits
# ============================================================

def complete_existing_event_units(
    date,
    events,
    news_count
):

    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    print()
    print(
        "=" * 70
    )

    print(
        "EVENT UNIT RESUME / REPAIR"
    )

    print(
        "=" * 70
    )

    completed = 0

    generated = 0

    for index, event in enumerate(
        events,
        start=1
    ):

        event_id = event[
            "event_id"
        ]

        matches = sorted(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        valid_existing = None

        for path in matches:

            if event_unit_file_valid(
                path,
                event_id
            ):

                valid_existing = path

                break

        if valid_existing:

            print(
                f"[{index}/{len(events)}] "
                f"⏭️ 已存在："
                f"{event_id}"
            )

            completed += 1

            continue

        print()
        print(
            f"[{index}/{len(events)}] "
            f"🔨 补齐：{event_id}"
        )

        print(
            f"   Event: "
            f"{event['event_title']}"
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
                f"❌ {event_id} "
                "综合结果为空"
            )

        path = save_event_unit(

            date,

            event,

            aggregated_content
        )

        if not event_unit_file_valid(
            path,
            event_id
        ):

            raise RuntimeError(
                f"❌ {event_id} 文件保存后验证失败："
                f"{path}"
            )

        print(
            f"   ✅ Saved: {path}"
        )

        generated += 1

        completed += 1

    if completed != len(events):

        raise RuntimeError(
            f"❌ {date} EventUnit补齐数量异常："
            f"{completed}/{len(events)}"
        )

    missing_after = []

    for event in events:

        event_id = event[
            "event_id"
        ]

        matches = sorted(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        valid = any(

            event_unit_file_valid(
                path,
                event_id
            )

            for path in matches
        )

        if not valid:

            missing_after.append(
                event_id
            )

    if missing_after:

        raise RuntimeError(
            f"❌ {date} EventUnits补齐后仍缺失："
            f"{missing_after}"
        )

    marker = mark_event_units_complete(

        date,

        news_count,

        len(events)
    )

    print()
    print(
        "=" * 70
    )

    print(
        "✅ EVENT UNITS COMPLETE"
    )

    print(
        f"Existing skipped : "
        f"{completed - generated}"
    )

    print(
        f"Newly generated  : "
        f"{generated}"
    )

    print(
        f"Total EventUnits  : "
        f"{len(events)}"
    )

    print(
        f"Directory         : "
        f"{target}"
    )

    print(
        f"Marker            : "
        f"{marker}"
    )

    return True


# ============================================================
# Stage 1完整执行
# ============================================================

def run_stage_1(
    date
):

    print()
    print(
        "=" * 70
    )

    print(
        f"STAGE 1 — EVENT UNIT GENERATION V6: {date}"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # 第一关：先检查EventUnits
    # --------------------------------------------------------

    inspection = inspect_event_units(
        date
    )

    # --------------------------------------------------------
    # 已完整：
    # 不重新调用AI
    # --------------------------------------------------------

    if inspection[
        "complete"
    ]:

        print()
        print(
            f"✅ {date} EventUnits已经完整。"
        )

        print(
            "⏭️ 不重新执行AI聚合。"
        )

        print(
            f"📁 {event_units_dir(date)}"
        )

        return False

    # --------------------------------------------------------
    # 只有需要生成/检查时才读取Enriched
    # --------------------------------------------------------

    news_items = load_all_enriched_news(
        date
    )

    print(
        f"AI Input News: {len(news_items)}"
    )

    print(
        "News processing limit: NONE"
    )

    # ========================================================
    # 情况A：
    # 已经有有效Index
    #
    # 不重新聚类。
    # 直接补EventUnit。
    # ========================================================

    if inspection[
        "index"
    ] is not None:

        print()
        print(
            "♻️ 检测到已有有效Event Index。"
        )

        print(
            "➡️ 不重新执行事件聚类。"
        )

        print(
            "➡️ 直接检查并补齐缺失EventUnit。"
        )

        events = rebuild_events_from_index(

            date,

            inspection[
                "index"
            ],

            news_items
        )

        validate_event_index_coverage(

            date,

            events,

            len(news_items)
        )

        return complete_existing_event_units(

            date,

            events,

            len(news_items)
        )

    # ========================================================
    # 情况B：
    # 没有有效Index
    #
    # 完整执行V6 Stage 1。
    # ========================================================

    print()
    print(
        "🆕 未找到有效Event Index。"
    )

    print(
        "➡️ 执行完整V6 Stage 1聚合。"
    )

    remove_event_units_complete(
        date
    )

    # --------------------------------------------------------
    # Stage 1A
    # --------------------------------------------------------

    initial_clusters = build_initial_clusters(

        date,

        news_items
    )

    # --------------------------------------------------------
    # Stage 1B
    # --------------------------------------------------------

    final_clusters = merge_all_clusters(

        date,

        initial_clusters,

        len(news_items)
    )

    # --------------------------------------------------------
    # Stage 1C
    # --------------------------------------------------------

    events = build_event_units(

        date,

        final_clusters,

        news_items
    )

    # --------------------------------------------------------
    # 覆盖检查
    # --------------------------------------------------------

    validate_event_index_coverage(

        date,

        events,

        len(news_items)
    )

    # --------------------------------------------------------
    # Index必须先落盘
    # --------------------------------------------------------

    index_path = save_aggregation_index(

        date,

        events
    )

    print()
    print(
        f"✅ Event Index saved: "
        f"{index_path}"
    )

    # --------------------------------------------------------
    # EventUnits逐个生成
    # --------------------------------------------------------

    complete_existing_event_units(

        date,

        events,

        len(news_items)
    )

    return True


# ============================================================
# Stage 2：读取Event Units
# ============================================================

def load_saved_event_units(
    date
):

    target = event_units_dir(
        date
    )

    if not target.exists():

        raise FileNotFoundError(
            f"EventUnits目录不存在：{target}"
        )

    marker = (
        target
        / EVENT_UNITS_COMPLETE_FILE
    )

    if not marker.exists():

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
            r
