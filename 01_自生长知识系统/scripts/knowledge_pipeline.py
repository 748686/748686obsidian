#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V5

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
STAGE 1：第二层 AI 事件聚合
   ↓
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
Raw News/YYYY-MM-DD-EventUnits/
   ├── _event_index.json
   ├── EVT-xxxx_事件名称.md
   └── _EVENT_UNITS_COMPLETE

   ↓ Git commit + push（由外层 Workflow 负责）
   ↓ git pull
   ↓
STAGE 2：27 Skills 深度处理

核心规则
============================================================

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
21. 发现重复ARTICLE ID时记录清晰冲突日志，并自动要求AI重新修复本批聚类。
22. 修复后仍不满足“一篇文章一个归属”则立即失败。
23. EventUnits目录存在则优先断点检查。
24. 有效Event Index存在时，不重新执行事件聚类，只补缺失EventUnit。
25. Index无效时重新建立完整Event Index。
26. 只有所有EventUnit实际文件都存在并通过验证，才生成_EVENT_UNITS_COMPLETE。
27. Stage 1完成后立即退出，不进入Stage 2。
28. Stage 2只读取已经保存的EventUnits。
29. Stage 2不重新读取原始Enriched News。
30. 三天由外层Workflow分别调用，日期彼此独立。
31. Source Enrichment不在本程序内处理。
32. Git commit/push/pull不在本程序内处理。
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
# 聚合参数
# ============================================================

AGGREGATION_BATCH_SIZE = 40

CLUSTER_MERGE_BATCH_SIZE = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

# AI聚类冲突自动修复次数。
# 第一次正常聚类失败后，会再次把本批输入和冲突信息交给AI修复。
# 修复仍失败，则整个批次失败，绝不生成错误EventUnit。
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
    写入清晰的事件聚类冲突日志。

    注意：
    这里不会把API Key写入日志。
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
            if isinstance(details, str):
                detail_text = details
            else:
                detail_text = json.dumps(
                    details,
                    ensure_ascii=False,
                    indent=2
                )
        except Exception:
            detail_text = str(details)

        lines.append("DETAILS:")
        lines.append(detail_text)

    lines.append("=" * 80)
    lines.append("")

    with path.open(
        "a",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(lines))

    print()
    print("⚠️ EVENT AGGREGATION CONFLICT")
    print(f"   Stage : {stage}")
    print(f"   Message: {message}")

    if details is not None:
        print("   Details:")
        print(str(details)[:5000])

    print(f"   Conflict log: {path}")


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

def parse_ai_json(
    result: str,
    context: str
):

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

def parse_front_matter(
    content: str
):

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
                "748686-Knowledge-Pipeline/5.0",
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

    # Horizon Score只负责排序，不负责截断
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
    """
    返回聚类结果的结构化覆盖问题：

    duplicate:
        同一ARTICLE出现在多个cluster中。

    missing:
        输入ARTICLE没有被任何cluster覆盖。

    extra:
        AI创造了输入之外的ARTICLE编号。

    malformed:
        cluster/article_indexes结构错误。
    """

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
        article_index: positions
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
        "duplicate": duplicate,
        "missing": missing,
        "extra": extra,
        "malformed": malformed,
    }


def cluster_assignment_is_valid(
    issues
):
    return not any(
        [
            issues["duplicate"],
            issues["missing"],
            issues["extra"],
            issues["malformed"],
        ]
    )


# ============================================================
# 聚类结果规范化
# ============================================================

def normalize_cluster_indexes(
    clusters
):
    """
    只做类型转换，不做任何“自动抢归属”。

    这是故意的：
    如果AI把ARTICLE 153放进两个cluster，
    我们不能武断地替AI决定它应该属于哪个事件。

    正确做法是：
    记录冲突 → AI修复 → 再验证。

    """

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
绝对覆盖要求
============================================================

本批输入ARTICLE编号为：

{json.dumps(
    expected_indexes,
    ensure_ascii=False
)}

输入中的每一篇ARTICLE：

必须且只能属于一个cluster。

例如：

ARTICLE 153不能同时出现在：

cluster C001
和
cluster C004

如果ARTICLE 153与ARTICLE 200属于同一事件，
应该把它们放入同一个cluster，
而不是让ARTICLE 153重复出现。

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

在输出JSON之前，请你自己检查：

1. ARTICLE总覆盖数是否等于输入ARTICLE数量。
2. 每个ARTICLE是否只出现一次。
3. 是否出现重复ARTICLE ID。
4. 是否出现输入之外的ARTICLE ID。
5. 是否遗漏ARTICLE。
6. 每个cluster是否至少包含一个ARTICLE。
7. cluster_id是否唯一。

如果发现冲突，必须先在内部修正，再输出最终JSON。

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
    """
    当AI第一次聚类出现重复/遗漏/越界时，
    不直接人工猜测归属。

    重新把本批真实文章 + 错误聚类结果 + 冲突信息
    交给AI进行修复。

    修复结果仍必须经过严格覆盖检查。
    """

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
你正在修复748686自生长知识系统第二层事件聚合中的一个严重覆盖冲突。

日期：
{date}

修复次数：
第 {attempt} 次

============================================================
本批真实ARTICLE
============================================================

{joined_articles}

============================================================
AI上一次错误的聚类结果
============================================================

{broken_json}

============================================================
检测到的冲突
============================================================

{issue_json}

============================================================
修复任务
============================================================

请重新检查全部ARTICLE。

你必须同时满足：

1. 同一个现实世界事件尽量归入同一个cluster。
2. 不同现实世界事件不能强行合并。
3. 一篇ARTICLE只能属于一个cluster。
4. 一篇ARTICLE不能出现在两个cluster。
5. 不允许遗漏任何ARTICLE。
6. 不允许创造任何ARTICLE编号。
7. 不允许修改ARTICLE编号。
8. 如果一个ARTICLE无法与其他文章合并，让它单独成为cluster。
9. 不确定时宁可分开。
10. 必须依据文章内容判断，不依据cluster原结果盲目修复。

============================================================
本批完整ARTICLE编号
============================================================

{json.dumps(
    expected_indexes,
    ensure_ascii=False
)}

============================================================
输出前强制检查
============================================================

在输出之前逐项检查：

- 输入ARTICLE数量 = 输出ARTICLE归属总数
- 每个ARTICLE出现次数 = 1
- Missing = 0
- Duplicate = 0
- Extra = 0

如果发现任何问题，必须在内部重新修正。

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
    }}
  ]
}}
"""

    result = call_ai(

        prompt,

        system_prompt=(
            "你是新闻事件聚类冲突修复专家。"
            "你必须修复ARTICLE覆盖冲突。"
            "一篇ARTICLE绝对不能属于多个cluster。"
            "绝对不能遗漏ARTICLE。"
            "绝对不能创造ARTICLE编号。"
            "必须返回合法JSON。"
        ),

        temperature=0,
    )

    data = parse_ai_json(
        result,
        f"{date} 第一轮新闻聚类冲突修复 #{attempt}"
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
# 带自动冲突修复的第一轮聚类
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

    # --------------------------------------------------------
    # 第一次发现冲突：
    # 必须记录完整日志。
    # --------------------------------------------------------

    log_conflict(
        date,
        f"STAGE 1A / BATCH {batch_number}",
        "AI第一次聚类返回了非法ARTICLE归属，启动自动修复。",
        {
            "batch_number": batch_number,
            "expected_indexes": expected_indexes,
            "issues": issues,
            "broken_clusters": clusters,
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

            log_conflict(
                date,
                f"STAGE 1A / BATCH {batch_number}",
                "AI聚类冲突已成功修复。",
                {
                    "repair_attempt": attempt,
                    "final_cluster_count":
                        len(repaired_clusters),
                }
            )

            return repaired_clusters

        log_conflict(
            date,
            f"STAGE 1A / BATCH {batch_number}",
            f"第{attempt}次聚类冲突修复仍然失败。",
            {
                "repair_attempt": attempt,
                "issues": repaired_issues,
                "clusters": repaired_clusters,
            }
        )

    # --------------------------------------------------------
    # 修复次数用尽：
    # 绝不继续生成EventUnits。
    # --------------------------------------------------------

    raise RuntimeError(
        f"❌ {date} Batch {batch_number} "
        f"ARTICLE聚类覆盖冲突无法自动修复。\n"
        f"Duplicate={repaired_issues['duplicate']}\n"
        f"Missing={repaired_issues['missing']}\n"
        f"Extra={repaired_issues['extra']}\n"
        f"Malformed={repaired_issues['malformed']}\n"
        f"详细冲突日志：{conflict_log_path(date)}"
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

如果两个Cluster属于同一事件：
可以放入同一个group。

如果不属于同一事件：
各自成为独立group。

============================================================
输出前强制检查
============================================================

输入Cluster编号为：

{json.dumps(
    list(range(1, len(clusters) + 1)),
    ensure_ascii=False
)}

检查：

1. 每个Cluster编号恰好出现一次。
2. 不得重复Cluster。
3. 不得遗漏Cluster。
4. 不得创造Cluster编号。

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
            "每个Cluster必须且只能属于一个group。"
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

        if not isinstance(
            indexes,
            list
        ):

            raise RuntimeError(
                f"❌ {date} 跨批次合并存在非法cluster_indexes"
            )

        actual.extend(
            indexes
        )

    duplicate = [
        x
        for x in set(actual)
        if actual.count(x) > 1
    ]

    if duplicate:

        log_conflict(
            date,
            f"STAGE 1B / ROUND {merge_round} / BATCH {batch_index}",
            "AI跨批次合并返回重复Cluster。",
            {
                "duplicate_cluster_indexes":
                    duplicate,
                "expected":
                    sorted(expected),
                "actual":
                    actual,
                "groups":
                    groups,
            }
        )

        raise RuntimeError(
            f"❌ {date} 跨批次合并存在重复Cluster："
            f"{duplicate}"
        )

    actual_set = set(actual)

    missing = sorted(
        expected - actual_set
    )

    extra = sorted(
        actual_set - expected
    )

    if missing or extra:

        log_conflict(
            date,
            f"STAGE 1B / ROUND {merge_round} / BATCH {batch_index}",
            "AI跨批次合并覆盖异常。",
            {
                "missing":
                    missing,
                "extra":
                    extra,
                "expected":
                    sorted(expected),
                "actual":
                    actual,
                "groups":
                    groups,
            }
        )

        raise RuntimeError(
            f"❌ {date} 跨批次覆盖异常\n"
            f"Missing={missing}\n"
            f"Extra={extra}"
        )

    return groups


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

        clusters = cluster_news_batch_with_repair(

            date,

            batch_items,

            start + 1,

            batch_number
        )

        # ----------------------------------------------------
        # 修复后的最终强制检查
        # ----------------------------------------------------

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

    # --------------------------------------------------------
    # 整个Stage 1A再次做一次总覆盖检查
    # --------------------------------------------------------

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
# Stage 1B
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

        # ----------------------------------------------------
        # 每一轮完成后，检查文章是否仍然一篇只属于一个Cluster
        # ----------------------------------------------------

        previous_indexes = []

        for cluster in current:

            previous_indexes.extend(
                cluster.get(
                    "article_indexes",
                    []
                )
            )

        next_indexes = []

        for cluster in next_level:

            next_indexes.extend(
                cluster.get(
                    "article_indexes",
                    []
                )
            )

        if (
            len(previous_indexes)
            != len(set(previous_indexes))
        ):

            raise RuntimeError(
                f"❌ {date} Merge Round "
                f"{merge_round} 输入Cluster本身存在重复文章"
            )

        if (
            len(next_indexes)
            != len(set(next_indexes))
        ):

            log_conflict(
                date,
                f"STAGE 1B / ROUND {merge_round}",
                "跨批次合并后发现同一ARTICLE进入多个Cluster。",
                {
                    "duplicate_articles": sorted(
                        {
                            x
                            for x in next_indexes
                            if next_indexes.count(x) > 1
                        }
                    )
                }
            )

            raise RuntimeError(
                f"❌ {date} Merge Round "
                f"{merge_round} 产生重复文章归属"
            )

        if set(previous_indexes) != set(
            next_indexes
        ):

            missing = sorted(
                set(previous_indexes)
                - set(next_indexes)
            )

            extra = sorted(
                set(next_indexes)
                - set(previous_indexes)
            )

            log_conflict(
                date,
                f"STAGE 1B / ROUND {merge_round}",
                "跨批次合并后文章覆盖发生变化。",
                {
                    "missing":
                        missing,
                    "extra":
                        extra,
                }
            )

            raise RuntimeError(
                f"❌ {date} Merge Round "
                f"{merge_round} 文章覆盖异常\n"
                f"Missing={missing}\n"
                f"Extra={extra}"
            )

        print(
            f"   Result after round "
            f"{merge_round}: "
            f"{len(next_level)}"
        )

        current = next_level

        merge_round += 1

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

    # --------------------------------------------------------
    # 最终Event Cluster生成后再次做全量唯一性检查
    # --------------------------------------------------------

    final_indexes = []

    for event in final_clusters:

        final_indexes.extend(
            event.get(
                "article_indexes",
                []
            )
        )

    if len(final_indexes) != len(
        set(final_indexes)
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
            "最终Event Units出现重复ARTICLE归属。",
            {
                "duplicate_articles":
                    duplicates
            }
        )

        raise RuntimeError(
            f"❌ {date} 最终Event Units存在重复文章："
            f"{duplicates}"
        )

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
    print("=" * 70)
    print(
        f"EVENT UNITS PREFLIGHT: {date}"
    )
    print("=" * 70)

    if not target.exists():

        print(
            "📁 EventUnits目录：不存在"
        )

        print(
            "➡️ 需要创建并完整生成。"
        )

        return {

            "exists": False,

            "complete": False,

            "index": None,

            "missing": [],

            "invalid": [],

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

            "exists": True,

            "complete": False,

            "index": None,

            "missing": [],

            "invalid": [],

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

    # --------------------------------------------------------
    # 检查是否有重复Event文件
    # --------------------------------------------------------

    existing_event_files = sorted(
        target.glob(
            "EVT-*.md"
        )
    )

    existing_ids = set()

    for path in existing_event_files:

        match = re.match(
            r"^(EVT-[^_]+)",
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
        and len(invalid) == 0
        and len(expected_ids) > 0
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

        "exists": True,

        "complete": complete,

        "index": index,

        "missing": missing,

        "invalid": invalid,

        "unexpected": unexpected,

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
# 删除错误的完成标记
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
                f"❌ Event Index存在空event_id"
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

        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败\n"
            f"Missing={sorted(expected - actual)}\n"
            f"Extra={sorted(actual - expected)}"
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
    print("=" * 70)
    print("EVENT UNIT RESUME / REPAIR")
    print("=" * 70)

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

    # --------------------------------------------------------
    # 再次实际检查磁盘
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # 完成标记
    # --------------------------------------------------------

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
        f"Existing skipped : {completed - generated}"
    )

    print(
        f"Newly generated  : {generated}"
    )

    print(
        f"Total EventUnits  : {len(events)}"
    )

    print(
        f"Directory         : {target}"
    )

    print(
        f"Marker            : {marker}"
    )

    return True


# ============================================================
# Stage 1完整执行
# ============================================================

def run_stage_1(
    date
):

    print()
    print("=" * 70)
    print(
        f"STAGE 1 — EVENT UNIT GENERATION: {date}"
    )
    print("=" * 70)

    # --------------------------------------------------------
    # 第一关：先检查EventUnits
    # --------------------------------------------------------

    inspection = inspect_event_units(
        date
    )

    # --------------------------------------------------------
    # 如果已经完整：
    # 直接结束，不重新调用AI
    # --------------------------------------------------------

    if inspection["complete"]:

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
    # 只有需要检查/生成时，才读取Enriched
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
    # → 不重新聚类
    # → 根据Index恢复Event
    # → 只补缺失EventUnit
    # ========================================================

    if inspection["index"] is not None:

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

            inspection["index"],

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
    # → 完整执行AI事件聚类
    # ========================================================

    print()
    print(
        "🆕 未找到有效Event Index。"
    )

    print(
        "➡️ 执行完整Stage 1聚合。"
    )

    remove_event_units_complete(
        date
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
    # EventUnits：
    # 新建后逐个生成
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
            r"(?m)^#\s+(.+)$",
            body
        )

        if heading_match:

            title = (
                heading_match
                .group(1)
                .strip()
            )

        try:

            source_count = int(
                metadata.get(
                    "source_count",
                    "0"
                )
            )

        except Exception:

            source_count = 0

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

def skills_complete(
    date
):

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
    print(
        f"STAGE 2 — 27 SKILLS DEEP PROCESSING: {date}"
    )
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

        f"""# {date} Knowledge Pipeline V5

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
# 日期格式检查
# ============================================================

def validate_date(
    date
):

    if not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}",
        date
    ):

        raise RuntimeError(
            f"❌ 日期格式错误：{date}"
        )


# ============================================================
# 统一入口
# ============================================================

def main():

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

    validate_date(
        date
    )

    print("=" * 70)
    print("748686 KNOWLEDGE PIPELINE V5")
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
    # 基础目录
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
    # API Key
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

    # ========================================================
    # Stage 1
    # ========================================================

    if args.stage == "aggregation":

        run_stage_1(
            date
        )

        print()
        print(
            "=" * 70
        )

        print(
            "STAGE 1 ONLY"
        )

        print(
            f"{date} EventUnits检查/生成/补齐已经完成。"
        )

        print(
            "现在停止，不进入Stage 2。"
        )

        print(
            "外层Workflow确认三天全部完成后："
        )

        print(
            "Git commit + push"
        )

        print(
            "然后重新pull到本地"
        )

        print(
            "再进入Stage 2。"
        )

        print(
            "=" * 70
        )

        return

    # ========================================================
    # Stage 2
    # ========================================================

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
            "❌ KNOWLEDGE PIPELINE V5 FAILED"
        )

        print("=" * 70)

        print(
            f"{type(exc).__name__}: {exc}"
        )

        print()

        sys.exit(1)
