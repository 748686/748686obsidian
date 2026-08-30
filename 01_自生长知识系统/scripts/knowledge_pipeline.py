#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V6.1

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
STAGE 1A：第二层 AI 事件聚类
   ↓
全部 Enriched News
   ↓
Batch Size 40
   ↓
AI 跨来源 / 跨语言事件识别
   ↓
ARTICLE 覆盖验证
   ↓
非法 ARTICLE 自动 Repair
   ↓
STAGE 1B：Global Event Merge
   ↓
30 Cluster Window / 15 Overlap
   ↓
多轮全局收敛
   ↓
一篇 ARTICLE 最终只能属于一个 EventUnit
   ↓
EventUnit Index
   ↓
EventUnit 完整性验证
   ↓
STAGE 2：27 Skills
   ↓
知识库

================================================================
V6.1 修复重点
================================================================

1. 修复：
   'list' object has no attribute 'get'

2. AI 顶层 JSON 可以是：
   - dict
   - list
   - ```json ... ```
   - 带额外文本的 JSON

3. 聚类 / Repair / Global Merge 全部统一结构解析。

4. AI 返回非法 ARTICLE：
   - missing
   - duplicate
   - extra
   - malformed
   自动 Repair。

5. Repair 自身返回非法 JSON 结构时：
   不再直接 data.get() 崩溃，
   而是进入结构标准化 / 重试。

6. 保留：
   - 1012 全量 Enriched News
   - Batch Size 40
   - 跨来源
   - 跨语言
   - Global Merge
   - 30 Cluster Window
   - 15 Overlap
   - 多轮收敛
   - Event Index resumable
   - EventUnit resumable
   - Stage 2 27 Skills
   - --stage aggregation
   - --stage skills
   - --stage all

7. 最终强保证：
   每一篇 ARTICLE 必须且只能进入一个 EventUnit。
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
# PATHS / CONSTANTS
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

EVENT_UNITS_SUFFIX = "EventUnits"
EVENT_INDEX_FILE = "_event_index.json"

EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"
SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"
AGNES_MODEL = "agnes-2.5-flash"
AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3
AI_TIMEOUT = 180

AGGREGATION_BATCH_SIZE = 40

GLOBAL_MERGE_WINDOW_SIZE = 30
GLOBAL_MERGE_OVERLAP = 15
MAX_GLOBAL_MERGE_ROUNDS = 12

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500
ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


# ============================================================
# BASIC HELPERS
# ============================================================

def now():
    return datetime.now(BEIJING_TZ)


def event_units_dir(date):
    return RAW_NEWS / f"{date}-{EVENT_UNITS_SUFFIX}"


def conflict_log_path(date):
    return LOGS / f"{date}_event_aggregation_conflicts.log"


def log_conflict(date, stage, message, details=None):
    LOGS.mkdir(parents=True, exist_ok=True)

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
            detail = (
                details
                if isinstance(details, str)
                else json.dumps(
                    details,
                    ensure_ascii=False,
                    indent=2
                )
            )
        except Exception:
            detail = str(details)

        lines += [
            "DETAILS:",
            detail
        ]

    lines += [
        "=" * 80,
        ""
    ]

    with conflict_log_path(date).open(
        "a",
        encoding="utf-8"
    ) as f:
        f.write("\n".join(lines))

    print(f"⚠️ {message}")
    print(f"   Conflict log: {conflict_log_path(date)}")


def read_json(path, default=None):
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
    except Exception as e:
        raise RuntimeError(
            f"❌ JSON读取失败：{path}\n{e}"
        ) from e


def write_json(path, data):
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


def safe_name(text):
    text = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        str(text or "")
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text[:120] or "未命名"


# ============================================================
# FRONT MATTER
# ============================================================

def parse_front_matter(content):
    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:
        return {}, content

    data = {}

    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue

        k, v = line.split(
            ":",
            1
        )

        data[k.strip()] = (
            v.strip()
            .strip('"')
            .strip("'")
        )

    return data, parts[2].lstrip()


# ============================================================
# AI JSON PARSING
# ============================================================

def strip_code_fence(text):
    text = str(text or "").strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.I
        )

        text = re.sub(
            r"\s*```$",
            "",
            text
        ).strip()

    return text


def extract_json_block(text):
    """
    从 AI 返回中尽可能提取 JSON。

    支持：

    1. 纯 JSON
    2. ```json ... ```
    3. JSON 前后带解释文字
    4. 顶层 object
    5. 顶层 array
    """

    text = strip_code_fence(text)

    # --------------------------------------------------------
    # First attempt: direct JSON
    # --------------------------------------------------------

    try:
        return json.loads(text)
    except Exception:
        pass

    # --------------------------------------------------------
    # Locate first { or [
    # --------------------------------------------------------

    candidates = []

    obj_pos = text.find("{")
    arr_pos = text.find("[")

    if obj_pos >= 0:
        candidates.append(obj_pos)

    if arr_pos >= 0:
        candidates.append(arr_pos)

    if not candidates:
        raise ValueError("未找到JSON起始符号")

    start = min(candidates)

    candidate = text[start:].strip()

    # --------------------------------------------------------
    # JSONDecoder raw_decode
    # --------------------------------------------------------

    decoder = json.JSONDecoder()

    try:
        value, _ = decoder.raw_decode(candidate)
        return value
    except Exception:
        pass

    # --------------------------------------------------------
    # Last fallback: scan possible JSON endings
    # --------------------------------------------------------

    for end in range(
        len(candidate),
        max(0, len(candidate) - 20000),
        -1
    ):
        fragment = candidate[:end].strip()

        if not (
            fragment.endswith("}")
            or fragment.endswith("]")
        ):
            continue

        try:
            return json.loads(fragment)
        except Exception:
            continue

    raise ValueError(
        "无法从AI返回内容中提取合法JSON"
    )


def parse_ai_json(result, context):
    text = str(result or "").strip()

    if not text:
        raise RuntimeError(
            f"❌ AI返回为空：{context}"
        )

    try:
        return extract_json_block(text)

    except Exception as e:
        raise RuntimeError(
            f"❌ AI JSON解析失败：{context}\n\n"
            f"{text[:5000]}"
        ) from e


# ============================================================
# AI STRUCTURE NORMALIZATION
# ============================================================

def extract_list_field(
    data,
    field_name,
    aliases=None
):
    """
    安全提取 AI JSON 中的 list。

    重点解决：

        data.get(...)

    在 data 为 list 时直接崩溃的问题。

    支持：

        {"clusters": [...]}

    或：

        [...]

    或：

        {"result": {"clusters": [...]}}

    """

    aliases = aliases or []

    # --------------------------------------------------------
    # dict
    # --------------------------------------------------------

    if isinstance(data, dict):

        possible_names = [
            field_name,
            *aliases
        ]

        for name in possible_names:
            value = data.get(name)

            if isinstance(value, list):
                return value

        # Nested common containers
        for key in (
            "result",
            "data",
            "output",
            "response",
            "answer"
        ):
            nested = data.get(key)

            if isinstance(nested, dict):
                for name in possible_names:
                    value = nested.get(name)

                    if isinstance(value, list):
                        return value

            elif isinstance(nested, list):
                # If nested itself is the desired list
                if nested and all(
                    isinstance(x, dict)
                    for x in nested
                ):
                    return nested

        return None

    # --------------------------------------------------------
    # top-level list
    # --------------------------------------------------------

    if isinstance(data, list):
        return data

    return None


def normalize_cluster_response(data):
    """
    将各种 AI 返回统一为：

    [
        {
            "cluster_id": "...",
            "article_indexes": [...],
            "event_title": "...",
            "event_reason": "..."
        }
    ]
    """

    clusters = extract_list_field(
        data,
        "clusters",
        aliases=[
            "cluster",
            "groups",
            "results",
            "items"
        ]
    )

    if not isinstance(clusters, list):
        raise RuntimeError(
            "❌ AI聚类结果无法识别为clusters数组"
        )

    normalized = []

    for pos, cluster in enumerate(
        clusters,
        1
    ):

        if not isinstance(cluster, dict):
            normalized.append(cluster)
            continue

        d = dict(cluster)

        # ----------------------------------------------------
        # article index aliases
        # ----------------------------------------------------

        ids = None

        for key in (
            "article_indexes",
            "article_index",
            "articles",
            "article_ids",
            "indexes"
        ):
            value = d.get(key)

            if isinstance(value, list):
                ids = value
                break

        if ids is None:
            ids = []

        d["article_indexes"] = ids

        # ----------------------------------------------------
        # Normalize ID
        # ----------------------------------------------------

        normalized_ids = []

        for x in ids:
            try:
                if isinstance(x, bool):
                    raise ValueError

                normalized_ids.append(
                    int(str(x).strip())
                )

            except Exception:
                normalized_ids.append(x)

        d["article_indexes"] = normalized_ids

        # ----------------------------------------------------
        # normalize titles
        # ----------------------------------------------------

        if not d.get("cluster_id"):
            d["cluster_id"] = (
                f"C{pos:03d}"
            )

        if not d.get("event_title"):
            d["event_title"] = (
                d.get("title")
                or d.get("event")
                or "未命名事件"
            )

        if not d.get("event_reason"):
            d["event_reason"] = (
                d.get("reason")
                or d.get("explanation")
                or ""
            )

        normalized.append(d)

    return normalized


def normalize_merge_response(data):
    """
    Global Merge AI 返回统一为：

    [
        {
            "group_id": "...",
            "cluster_indexes": [...],
            "event_title": "...",
            "reason": "..."
        }
    ]
    """

    groups = extract_list_field(
        data,
        "groups",
        aliases=[
            "clusters",
            "merge_groups",
            "results",
            "items"
        ]
    )

    if not isinstance(groups, list):
        raise RuntimeError(
            "❌ Global Merge结果无法识别为groups数组"
        )

    normalized = []

    for pos, group in enumerate(
        groups,
        1
    ):

        if not isinstance(group, dict):
            normalized.append(group)
            continue

        d = dict(group)

        ids = None

        for key in (
            "cluster_indexes",
            "cluster_index",
            "clusters",
            "cluster_ids",
            "indexes"
        ):
            value = d.get(key)

            if isinstance(value, list):
                ids = value
                break

        if ids is None:
            ids = []

        normalized_ids = []

        for x in ids:
            try:
                if isinstance(x, bool):
                    raise ValueError

                normalized_ids.append(
                    int(str(x).strip())
                )

            except Exception:
                normalized_ids.append(x)

        d["cluster_indexes"] = normalized_ids

        if not d.get("group_id"):
            d["group_id"] = (
                f"G{pos:03d}"
            )

        if not d.get("event_title"):
            d["event_title"] = (
                d.get("title")
                or d.get("event")
                or "未命名事件"
            )

        if not d.get("reason"):
            d["reason"] = (
                d.get("event_reason")
                or d.get("explanation")
                or ""
            )

        normalized.append(d)

    return normalized


# ============================================================
# AGNES API
# ============================================================

def call_ai(
    prompt,
    system_prompt=None,
    temperature=DEFAULT_TEMPERATURE
):

    key = os.getenv(
        AGNES_API_KEY_ENV,
        ""
    ).strip()

    if not key:
        raise RuntimeError(
            "❌ 缺少 AGNES_API_KEY"
        )

    if not system_prompt:
        system_prompt = (
            "你是748686自生长知识系统的知识工程师。"
            "严格依据输入内容，不得编造事实。"
        )

    payload = json.dumps(
        {
            "model": AGNES_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature
        },
        ensure_ascii=False
    ).encode()

    req = Request(
        AGNES_BASE_URL + "/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": (
                "748686-Knowledge-Pipeline/6.1"
            )
        },
        method="POST"
    )

    try:

        with urlopen(
            req,
            timeout=AI_TIMEOUT
        ) as r:

            raw = r.read().decode(
                "utf-8"
            )

    except HTTPError as e:

        body = (
            e.read().decode(
                "utf-8",
                errors="replace"
            )
            if hasattr(e, "read")
            else ""
        )

        raise RuntimeError(
            f"❌ AGNES.ai HTTP错误 {e.code}\n"
            f"{body[:3000]}"
        ) from e

    except URLError as e:

        raise RuntimeError(
            "❌ AGNES.ai 网络连接失败\n"
            f"{e.reason}"
        ) from e

    except TimeoutError as e:

        raise RuntimeError(
            "❌ AGNES.ai 请求超时"
        ) from e

    except Exception as e:

        raise RuntimeError(
            f"❌ AGNES.ai 请求失败：{e}"
        ) from e

    try:

        data = json.loads(raw)

    except Exception as e:

        raise RuntimeError(
            "❌ AGNES.ai 返回不是合法JSON\n"
            f"{raw[:3000]}"
        ) from e

    try:

        result = data[
            "choices"
        ][0][
            "message"
        ][
            "content"
        ]

    except Exception as e:

        raise RuntimeError(
            "❌ AGNES.ai 返回格式异常\n"
            + json.dumps(
                data,
                ensure_ascii=False
            )[:5000]
        ) from e

    if not str(result).strip():
        raise RuntimeError(
            "❌ AGNES.ai 返回空内容"
        )

    return str(result).strip()


# ============================================================
# SKILLS
# ============================================================

def load_skills():

    if not SKILLS.exists():
        raise RuntimeError(
            f"Skills目录不存在：{SKILLS}"
        )

    out = {}

    for p in sorted(
        SKILLS.rglob("*.md")
    ):

        out[p.name] = {
            "name": p.name,
            "path": str(p),
            "content": p.read_text(
                encoding="utf-8",
                errors="replace"
            )
        }

    return out


def load_routes():

    routes = read_json(
        ROUTES_FILE,
        {}
    )

    if not isinstance(
        routes,
        dict
    ) or not routes:

        raise RuntimeError(
            "skill_routes.json为空或不存在"
        )

    return routes


def route_skills(
    category,
    routes,
    skills
):

    selected = []

    values = routes.get(
        category,
        []
    )

    if not isinstance(
        values,
        list
    ):
        raise RuntimeError(
            f"❌ Skill route不是数组：{category}"
        )

    for name in values:

        if name not in skills:
            raise RuntimeError(
                "❌ skill_routes.json引用"
                f"不存在Skill：{name}"
            )

        selected.append(
            skills[name]
        )

    return selected


# ============================================================
# ENRICHED NEWS
# ============================================================

def get_enriched_files(date):

    root = RAW_NEWS / f"{date}-Enriched"

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

    meta, body = parse_front_matter(
        content
    )

    return {
        "path": path,
        "metadata": meta,
        "body": body,
        "content": content
    }


def load_all_enriched_news(date):

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

    items = [
        load_news_file(p)
        for p in files
    ]

    items = [
        x
        for x in items
        if isinstance(
            x.get("metadata"),
            dict
        )
        and x["metadata"].get(
            "title",
            ""
        ).strip()
    ]

    if not items:
        raise RuntimeError(
            f"❌ {date} 没有有效新闻"
        )

    def score(x):

        try:
            return float(
                x["metadata"].get(
                    "horizon_score",
                    0
                )
            )

        except Exception:
            return 0

    items.sort(
        key=score,
        reverse=True
    )

    print(
        f"Valid news: {len(items)}"
    )

    return items


# ============================================================
# ARTICLE DIGEST
# ============================================================

def build_article_digest(
    item,
    index
):

    m = item["metadata"]

    return f"""
[ARTICLE {index}]

标题：
{m.get("title", "Untitled")}

来源：
{m.get("source", "Unknown")}

原文链接：
{m.get("source_url", "")}

来源状态：
{m.get("source_status", "")}

内容状态：
{m.get("content_status", "")}

内容：
{item["body"][:ARTICLE_CLUSTER_CONTENT_LIMIT]}
""".strip()


# ============================================================
# ARTICLE COVERAGE VALIDATION
# ============================================================

def inspect_cluster_assignment(
    clusters,
    expected_indexes
):

    expected = set(
        map(
            int,
            expected_indexes
        )
    )

    occ = {}
    malformed = []

    if not isinstance(
        clusters,
        list
    ):

        return {
            "duplicate": {},
            "missing": sorted(expected),
            "extra": [],
            "malformed": [
                "clusters不是数组"
            ]
        }

    for pos, c in enumerate(
        clusters,
        1
    ):

        if not isinstance(
            c,
            dict
        ):
            malformed.append(
                f"cluster[{pos}]不是对象"
            )
            continue

        ids = c.get(
            "article_indexes"
        )

        if not isinstance(
            ids,
            list
        ):

            malformed.append(
                f"cluster[{pos}] "
                "article_indexes不是数组"
            )

            continue

        if not ids:

            malformed.append(
                f"cluster[{pos}]为空Cluster"
            )

            continue

        for v in ids:

            try:

                if isinstance(
                    v,
                    bool
                ):
                    raise ValueError

                i = int(
                    str(v).strip()
                )

            except Exception:

                malformed.append(
                    f"cluster[{pos}]"
                    f"非法ARTICLE ID：{v}"
                )

                continue

            occ.setdefault(
                i,
                []
            ).append(pos)

    duplicate = {
        i: positions
        for i, positions in occ.items()
        if len(positions) > 1
    }

    actual = set(occ)

    return {
        "duplicate": duplicate,
        "missing": sorted(
            expected - actual
        ),
        "extra": sorted(
            actual - expected
        ),
        "malformed": malformed
    }


def valid_issues(i):

    return not any(
        [
            i["duplicate"],
            i["missing"],
            i["extra"],
            i["malformed"]
        ]
    )


def normalize_clusters(cs):

    return normalize_cluster_response(
        cs
    )


# ============================================================
# STAGE 1A — FIRST AI CLUSTERING
# ============================================================

def cluster_news_batch(
    date,
    items,
    start
):

    expected = list(
        range(
            start,
            start + len(items)
        )
    )

    joined = "\n\n".join(
        build_article_digest(
            x,
            start + i
        )
        for i, x in enumerate(items)
    )

    prompt = f"""
你正在执行748686自生长知识系统V6第二层事件聚合。

日期：
{date}

{joined}

任务：

识别哪些新闻属于同一个现实世界事件。

支持：
- 跨来源
- 跨语言

不要因为：
- 关键词相同
- 公司相同
- 行业相同
- 国家相同
- 人物相同

就强行合并。

只有明确属于同一个具体现实世界事件时才合并。

无法确定时宁可分开。

============================================================
绝对覆盖要求
============================================================

ARTICLE编号：

{json.dumps(expected, ensure_ascii=False)}

每篇ARTICLE：
1. 必须出现一次
2. 只能出现一次
3. 不得遗漏
4. 不得重复
5. 不得创造不存在的编号

============================================================
输出格式
============================================================

只输出JSON。

推荐格式：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "统一事件名称",
      "event_reason": "事件判断"
    }}
  ]
}}

禁止输出JSON以外的解释。
""".strip()

    raw = call_ai(
        prompt,
        (
            "你是全球新闻事件聚类专家。"
            "每篇ARTICLE必须且只能属于一个cluster。"
            "只输出JSON。"
        ),
        0
    )

    data = parse_ai_json(
        raw,
        f"{date} 第一轮新闻聚类"
    )

    return normalize_clusters(
        data
    )


# ============================================================
# STAGE 1A — REPAIR
# ============================================================

def repair_cluster_news_batch(
    date,
    items,
    start,
    broken,
    issues,
    attempt
):

    expected = list(
        range(
            start,
            start + len(items)
        )
    )

    joined = "\n\n".join(
        build_article_digest(
            x,
            start + i
        )
        for i, x in enumerate(items)
    )

    prompt = f"""
修复748686 V6 ARTICLE覆盖冲突。

日期：
{date}

第 {attempt} 次修复。

============================================================
真实ARTICLE
============================================================

{json.dumps(expected, ensure_ascii=False)}

============================================================
文章
============================================================

{joined}

============================================================
上次AI结果
============================================================

{json.dumps(
    broken,
    ensure_ascii=False,
    indent=2
)}

============================================================
检测问题
============================================================

{json.dumps(
    issues,
    ensure_ascii=False,
    indent=2
)}

============================================================
修复要求
============================================================

重新判断全部文章。

同一具体现实世界事件：
→ 合并。

不同具体事件：
→ 分开。

每篇ARTICLE：
→ 恰好一次。

最终必须：

Missing = 0
Duplicate = 0
Extra = 0
Malformed = 0

============================================================
输出
============================================================

只输出JSON。

格式：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "事件",
      "event_reason": "原因"
    }}
  ]
}}

如果你的系统倾向直接返回数组，也允许：

[
  {{
    "cluster_id": "C001",
    "article_indexes": [1],
    "event_title": "事件",
    "event_reason": "原因"
  }}
]

禁止输出解释文字。
""".strip()

    raw = call_ai(
        prompt,
        (
            "你是新闻事件聚类冲突修复专家。"
            "必须修复ARTICLE覆盖问题。"
            "允许JSON对象或JSON数组。"
            "只输出JSON。"
        ),
        0
    )

    data = parse_ai_json(
        raw,
        f"{date} 聚类冲突修复 #{attempt}"
    )

    # ========================================================
    # IMPORTANT:
    # 这里绝不能直接：
    #
    #     data.get("clusters")
    #
    # 因为 data 可能是 list。
    #
    # 统一经过 normalize_clusters。
    # ========================================================

    return normalize_clusters(
        data
    )


def cluster_news_batch_with_repair(
    date,
    items,
    start,
    batch_no
):

    expected = list(
        range(
            start,
            start + len(items)
        )
    )

    # --------------------------------------------------------
    # First clustering
    # --------------------------------------------------------

    cs = cluster_news_batch(
        date,
        items,
        start
    )

    issues = inspect_cluster_assignment(
        cs,
        expected
    )

    if valid_issues(issues):
        return cs

    # --------------------------------------------------------
    # Repair
    # --------------------------------------------------------

    log_conflict(
        date,
        f"STAGE 1A / BATCH {batch_no}",
        "AI第一次聚类返回非法ARTICLE归属，启动自动修复。",
        {
            "issues": issues,
            "clusters": cs
        }
    )

    for attempt in range(
        1,
        CLUSTER_REPAIR_ATTEMPTS + 1
    ):

        try:

            cs = repair_cluster_news_batch(
                date,
                items,
                start,
                cs,
                issues,
                attempt
            )

        except Exception as e:

            log_conflict(
                date,
                f"STAGE 1A / BATCH {batch_no}",
                (
                    f"第{attempt}次Repair发生结构/API异常，"
                    "不会直接丢失原始冲突信息。"
                ),
                {
                    "error": str(e),
                    "previous_issues": issues
                }
            )

            if attempt >= CLUSTER_REPAIR_ATTEMPTS:
                raise

            continue

        issues = inspect_cluster_assignment(
            cs,
            expected
        )

        if valid_issues(issues):

            print(
                "   ✅ Cluster conflict "
                "repaired successfully."
            )

            return cs

        log_conflict(
            date,
            f"STAGE 1A / BATCH {batch_no}",
            (
                f"第{attempt}次聚类冲突修复仍然失败。"
            ),
            {
                "issues": issues,
                "clusters": cs
            }
        )

    raise RuntimeError(
        f"❌ {date} Batch {batch_no} "
        f"ARTICLE聚类覆盖冲突无法自动修复："
        f"{issues}"
    )


def validate_cluster_coverage(
    clusters,
    expected,
    context,
    date=None
):

    issues = inspect_cluster_assignment(
        clusters,
        expected
    )

    if valid_issues(issues):
        return

    if date:

        log_conflict(
            date,
            context,
            "聚类覆盖验证失败。",
            issues
        )

    raise RuntimeError(
        f"❌ {context} 聚类覆盖失败：{issues}"
    )


# ============================================================
# BUILD INITIAL CLUSTERS
# ============================================================

def build_initial_clusters(
    date,
    news
):

    allc = []

    total = len(news)

    print(
        "\n"
        + "=" * 70
        + "\nSTAGE 1A — AI EVENT CLUSTERING\n"
        + "=" * 70
    )

    print(
        f"Input Enriched News: {total}"
    )

    print(
        f"Batch Size: {AGGREGATION_BATCH_SIZE}"
    )

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE
    ):

        batch_no = (
            start // AGGREGATION_BATCH_SIZE
            + 1
        )

        end = min(
            start + AGGREGATION_BATCH_SIZE,
            total
        )

        print(
            f"\n🔹 Cluster Batch {batch_no}: "
            f"{start + 1}-{end}/{total}"
        )

        cs = cluster_news_batch_with_repair(
            date,
            news[start:end],
            start + 1,
            batch_no
        )

        validate_cluster_coverage(
            cs,
            range(
                start + 1,
                end + 1
            ),
            f"{date} Batch {batch_no}",
            date
        )

        for pos, c in enumerate(
            cs,
            1
        ):

            if not isinstance(
                c,
                dict
            ):
                raise RuntimeError(
                    f"❌ {date} Batch "
                    f"{batch_no} 存在非法Cluster对象："
                    f"{c}"
                )

            ids = c.get(
                "article_indexes",
                []
            )

            if not isinstance(
                ids,
                list
            ):
                raise RuntimeError(
                    f"❌ {date} Batch "
                    f"{batch_no} article_indexes非法"
                )

            try:
                normalized_ids = [
                    int(x)
                    for x in ids
                ]

            except Exception as e:

                raise RuntimeError(
                    f"❌ {date} Batch "
                    f"{batch_no} ARTICLE编号无法转换："
                    f"{ids}"
                ) from e

            allc.append(
                {
                    "cluster_id": (
                        f"B{batch_no:03d}-"
                        f"{c.get('cluster_id', f'C{pos:03d}')}"
                    ),
                    "event_title": c.get(
                        "event_title",
                        "未命名事件"
                    ),
                    "event_reason": c.get(
                        "event_reason",
                        ""
                    ),
                    "article_indexes": normalized_ids
                }
            )

        print(
            f"   Clusters generated: {len(cs)}"
        )

    validate_cluster_coverage(
        allc,
        range(
            1,
            total + 1
        ),
        f"{date} Stage 1A GLOBAL",
        date
    )

    print(
        f"\n✅ Initial Clusters: {len(allc)}"
    )

    return allc


# ============================================================
# GLOBAL MERGE WINDOWS
# ============================================================

def build_merge_windows(
    clusters
):

    total = len(clusters)

    if total <= GLOBAL_MERGE_WINDOW_SIZE:
        return [clusters]

    step = (
        GLOBAL_MERGE_WINDOW_SIZE
        - GLOBAL_MERGE_OVERLAP
    )

    if step <= 0:
        raise RuntimeError(
            "❌ Window Size必须大于Overlap"
        )

    return _windows(
        clusters,
        step
    )


def _windows(
    clusters,
    step
):

    out = []

    s = 0

    while s < len(clusters):

        e = min(
            s + GLOBAL_MERGE_WINDOW_SIZE,
            len(clusters)
        )

        out.append(
            clusters[s:e]
        )

        if e >= len(clusters):
            break

        s += step

    return out


# ============================================================
# GLOBAL MERGE AI
# ============================================================

def merge_cluster_window(
    date,
    window,
    round_no,
    window_no
):

    joined = "\n\n".join(
        f"""
[CLUSTER {i}]

Cluster ID：
{c.get("cluster_id", "")}

事件名称：
{c.get("event_title", "未命名事件")}

事件判断：
{c.get("event_reason", "")}

文章数量：
{len(c.get("article_indexes", []))}

文章编号：
{json.dumps(
    c.get("article_indexes", []),
    ensure_ascii=False
)}
""".strip()

        for i, c in enumerate(
            window,
            1
        )
    )

    expected = list(
        range(
            1,
            len(window) + 1
        )
    )

    prompt = f"""
你正在执行748686自生长知识系统V6全局事件归并。

日期：
{date}

轮次：
{round_no}

窗口：
{window_no}

============================================================
输入Cluster
============================================================

{joined}

============================================================
任务
============================================================

判断Cluster是否属于同一个具体现实世界事件。

可以合并：

- 同一政策发布
- 同一公司重大动作
- 同一事故
- 同一产品发布
- 同一军事行动
- 同一自然灾害
- 同一具体国际事件
- 同一具体司法事件

不得因为以下原因强行合并：

- 同公司
- 同人物
- 同国家
- 同行业
- 同政策方向
- 同关键词
- 同趋势

如果属于不同具体事件：
必须分开。

无法确认：
宁可分开。

============================================================
覆盖要求
============================================================

输入Cluster编号：

{json.dumps(expected)}

每个Cluster：
必须且只能进入一个group。

不得：
- 遗漏
- 重复
- 创造不存在编号

============================================================
输出
============================================================

只输出JSON：

{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1,4],
      "event_title": "统一事件名称",
      "reason": "原因"
    }}
  ]
}}

禁止输出解释文字。
""".strip()

    raw = call_ai(
        prompt,
        (
            "你是全球新闻事件归并专家。"
            "必须覆盖全部输入Cluster。"
            "每个Cluster恰好一次。"
            "只输出JSON。"
        ),
        0
    )

    data = parse_ai_json(
        raw,
        (
            f"{date} Global Merge "
            f"Round {round_no} "
            f"Window {window_no}"
        )
    )

    groups = normalize_merge_response(
        data
    )

    actual = []
    malformed = []

    for pos, g in enumerate(
        groups,
        1
    ):

        if not isinstance(
            g,
            dict
        ):

            malformed.append(
                f"group[{pos}]不是对象"
            )

            continue

        ids = g.get(
            "cluster_indexes"
        )

        if not isinstance(
            ids,
            list
        ) or not ids:

            malformed.append(
                f"group[{pos}] "
                "cluster_indexes无效"
            )

            continue

        for x in ids:

            try:

                actual.append(
                    int(x)
                )

            except Exception:

                malformed.append(
                    f"group[{pos}]非法编号：{x}"
                )

    duplicates = sorted(
        {
            x
            for x in actual
            if actual.count(x) > 1
        }
    )

    missing = sorted(
        set(expected) - set(actual)
    )

    extra = sorted(
        set(actual) - set(expected)
    )

    if (
        duplicates
        or missing
        or extra
        or malformed
    ):

        log_conflict(
            date,
            (
                f"STAGE 1B / ROUND {round_no} "
                f"/ WINDOW {window_no}"
            ),
            "V6 Global Merge窗口覆盖异常。",
            {
                "duplicate": duplicates,
                "missing": missing,
                "extra": extra,
                "malformed": malformed,
                "groups": groups
            }
        )

        raise RuntimeError(
            "❌ Global Merge覆盖异常 "
            f"Duplicate={duplicates} "
            f"Missing={missing} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )

    return groups


# ============================================================
# BUILD MERGED CLUSTERS
# ============================================================

def build_window_merged_clusters(
    window,
    groups,
    round_no,
    window_no
):

    out = []

    for gp, g in enumerate(
        groups,
        1
    ):

        if not isinstance(
            g,
            dict
        ):
            raise RuntimeError(
                "❌ Global Merge group不是对象"
            )

        ids = []

        for ci in g[
            "cluster_indexes"
        ]:

            ci = int(ci)

            if not (
                1 <= ci <= len(window)
            ):

                raise RuntimeError(
                    "❌ Global Merge引用"
                    f"不存在Cluster：{ci}"
                )

            source_cluster = window[
                ci - 1
            ]

            source_ids = source_cluster.get(
                "article_indexes",
                []
            )

            if not isinstance(
                source_ids,
                list
            ):

                raise RuntimeError(
                    "❌ Global Merge源Cluster "
                    "article_indexes非法"
                )

            ids.extend(
                source_ids
            )

        unique_ids = sorted(
            set(
                map(
                    int,
                    ids
                )
            )
        )

        if not unique_ids:
            raise RuntimeError(
                "❌ V6 Global Merge产生空Cluster"
            )

        out.append(
            {
                "cluster_id": (
                    f"R{round_no:02d}"
                    f"W{window_no:03d}"
                    f"G{gp:03d}"
                ),
                "event_title": g.get(
                    "event_title",
                    "未命名事件"
                ),
                "event_reason": g.get(
                    "reason",
                    ""
                ),
                "article_indexes": unique_ids
            }
        )

    return out


# ============================================================
# GLOBAL ARTICLE GRAPH MERGE
# ============================================================

def merge_overlapping_results(
    results,
    news_count
):
    """
    将不同Overlap窗口的结果转换成全局事件关系。

    关键原则：

    - 同一窗口内AI明确把两个Cluster放进同一个group：
      → 建立连接。

    - 不同窗口产生的结果有共同ARTICLE：
      → 建立连接。

    - 最终通过连通分量形成全局事件候选。

    这样不会因为：

        dedup[sig] = c

    而把Overlap窗口中有价值的信息直接丢掉。
    """

    if not results:
        return []

    parent = list(
        range(
            news_count + 1
        )
    )

    def find(x):

        while parent[x] != x:
            parent[x] = parent[
                parent[x]
            ]

            x = parent[x]

        return x

    def union(a, b):

        ra = find(a)
        rb = find(b)

        if ra != rb:
            parent[rb] = ra

    all_candidates = []

    # --------------------------------------------------------
    # Every merged candidate
    # --------------------------------------------------------

    for window_result in results:

        for c in window_result:

            ids = sorted(
                set(
                    map(
                        int,
                        c.get(
                            "article_indexes",
                            []
                        )
                    )
                )
            )

            if not ids:
                continue

            all_candidates.append(
                {
                    "article_indexes": ids,
                    "event_title": c.get(
                        "event_title",
                        "未命名事件"
                    ),
                    "event_reason": c.get(
                        "event_reason",
                        ""
                    ),
                    "cluster_id": c.get(
                        "cluster_id",
                        ""
                    )
                }
            )

            # ------------------------------------------------
            # Connect all articles in the same candidate
            # ------------------------------------------------

            first = ids[0]

            for article_id in ids[1:]:
                union(
                    first,
                    article_id
                )

    # --------------------------------------------------------
    # Components
    # --------------------------------------------------------

    components = {}

    for article_id in range(
        1,
        news_count + 1
    ):

        root = find(
            article_id
        )

        components.setdefault(
            root,
            []
        ).append(
            article_id
        )

    # --------------------------------------------------------
    # Best metadata per component
    # --------------------------------------------------------

    final = []

    for root, ids in sorted(
        components.items(),
        key=lambda x: min(x[1])
    ):

        candidates = [
            c
            for c in all_candidates
            if set(
                c["article_indexes"]
            ) & set(ids)
        ]

        if candidates:

            best = max(
                candidates,
                key=lambda c: (
                    len(
                        c["article_indexes"]
                    ),
                    len(
                        c.get(
                            "event_reason",
                            ""
                        )
                    )
                )
            )

            title = best.get(
                "event_title",
                "未命名事件"
            )

            reason = best.get(
                "event_reason",
                ""
            )

        else:

            title = "未命名事件"
            reason = ""

        final.append(
            {
                "cluster_id": (
                    f"GLOBAL-{len(final)+1:04d}"
                ),
                "event_title": title,
                "event_reason": reason,
                "article_indexes": sorted(
                    ids
                )
            }
        )

    # --------------------------------------------------------
    # Final coverage
    # --------------------------------------------------------

    allidx = [
        i
        for c in final
        for i in c[
            "article_indexes"
        ]
    ]

    if (
        len(allidx) != news_count
        or len(allidx)
        != len(set(allidx))
        or set(allidx)
        != set(
            range(
                1,
                news_count + 1
            )
        )
    ):

        raise RuntimeError(
            "❌ Global Merge全局Article覆盖失败"
        )

    return final


# ============================================================
# GLOBAL MERGE
# ============================================================

def merge_all_clusters(
    date,
    clusters,
    news_count
):

    current = clusters

    print(
        "\n"
        + "=" * 70
        + "\nSTAGE 1B — V6 GLOBAL EVENT MERGING\n"
        + "=" * 70
    )

    for rnd in range(
        1,
        MAX_GLOBAL_MERGE_ROUNDS + 1
    ):

        before = len(
            current
        )

        print(
            f"\nGLOBAL MERGE ROUND {rnd} "
            f"| Input Clusters: {before}"
        )

        if before <= 1:
            break

        windows = build_merge_windows(
            current
        )

        print(
            f"Windows: {len(windows)} "
            f"| Size: {GLOBAL_MERGE_WINDOW_SIZE} "
            f"| Overlap: {GLOBAL_MERGE_OVERLAP}"
        )

        results = []

        for wi, w in enumerate(
            windows,
            1
        ):

            print(
                f"🔹 Window {wi}/{len(windows)} "
                f"| size={len(w)}"
            )

            groups = merge_cluster_window(
                date,
                w,
                rnd,
                wi
            )

            merged_window = (
                build_window_merged_clusters(
                    w,
                    groups,
                    rnd,
                    wi
                )
            )

            results.append(
                merged_window
            )

        merged = merge_overlapping_results(
            results,
            news_count
        )

        after = len(
            merged
        )

        print(
            f"✅ Round {rnd}: "
            f"{before} -> {after}"
        )

        current = merged

        if after >= before:

            print(
                "🟢 GLOBAL MERGE CONVERGED"
            )

            break

    # ========================================================
    # FINAL EVENT UNITS
    # ========================================================

    final = []

    for i, c in enumerate(
        current,
        1
    ):

        ids = sorted(
            set(
                map(
                    int,
                    c.get(
                        "article_indexes",
                        []
                    )
                )
            )
        )

        final.append(
            {
                "event_id": (
                    f"EVT-{date}-{i:04d}"
                ),
                "event_title": c.get(
                    "event_title",
                    "未命名事件"
                ),
                "event_reason": c.get(
                    "event_reason",
                    ""
                ),
                "article_indexes": ids
            }
        )

    allidx = [
        i
        for c in final
        for i in c[
            "article_indexes"
        ]
    ]

    if (
        len(allidx) != news_count
        or len(allidx)
        != len(set(allidx))
        or set(allidx)
        != set(
            range(
                1,
                news_count + 1
            )
        )
    ):

        raise RuntimeError(
            f"❌ {date} 最终Event Units覆盖失败"
        )

    print(
        f"\n✅ FINAL EVENT UNITS: "
        f"{len(final)}"
    )

    print(
        f"✅ ARTICLE COVERAGE: "
        f"{len(allidx)}/{news_count}"
    )

    return final


# ============================================================
# BUILD EVENT UNITS
# ============================================================

def build_event_units(
    date,
    clusters,
    news
):

    out = []

    for c in clusters:

        arts = []

        for i in c[
            "article_indexes"
        ]:

            if not (
                1 <= i <= len(news)
            ):

                raise RuntimeError(
                    f"❌ {c['event_id']} "
                    f"引用不存在文章：{i}"
                )

            item = news[
                i - 1
            ]

            m = item[
                "metadata"
            ]

            arts.append(
                {
                    "index": i,
                    "path": str(
                        item["path"]
                    ),
                    "title": m.get(
                        "title",
                        "Untitled"
                    ),
                    "source": m.get(
                        "source",
                        "Unknown"
                    ),
                    "source_url": m.get(
                        "source_url",
                        ""
                    ),
                    "source_status": m.get(
                        "source_status",
                        ""
                    ),
                    "content_status": m.get(
                        "content_status",
                        ""
                    ),
                    "body": item["body"]
                }
            )

        out.append(
            {
                "event_id": c[
                    "event_id"
                ],
                "date": date,
                "event_title": c.get(
                    "event_title",
                    "未命名事件"
                ),
                "event_reason": c.get(
                    "event_reason",
                    ""
                ),
                "articles": arts
            }
        )

    return out


# ============================================================
# EVENT SYNTHESIS
# ============================================================

def synthesize_event(
    event
):

    blocks = []

    for a in event[
        "articles"
    ][:MAX_ARTICLES_PER_EVENT_CONTEXT]:

        blocks.append(
            f"""
### 来源文章 #{a['index']}

标题：
{a['title']}

来源：
{a['source']}

链接：
{a['source_url']}

source_status：
{a['source_status']}

content_status：
{a['content_status']}

内容：

{a['body'][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}
""".strip()
        )

    prompt = f"""
你正在执行748686自生长知识系统V6第二层事件知识综合。

日期：
{event['date']}

事件ID：
{event['event_id']}

事件名称：
{event['event_title']}

第一轮事件判断：
{event['event_reason']}

============================================================
同一事件的多来源输入
============================================================

{chr(10).join(blocks)}

============================================================
任务
============================================================

把来源综合成一个高质量事件知识单元。

要求：

1. 识别共同事实。

2. 保留来源独有信息。

3. 保留不同地区视角。

4. 区分事实与推测。

5. 不编造。

6. source_status不是fetched时，
   不得声称完整阅读原文。

7. 冲突必须明确指出。

8. 资料不足必须明确说明。

============================================================
输出
============================================================

输出标准中文Markdown。

必须包含：

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

## 事件结论
""".strip()

    return call_ai(
        prompt,
        (
            "你是跨来源新闻综合专家。"
            "严格依据输入，不得编造。"
            "输出标准中文Markdown。"
        ),
        0.2
    )


# ============================================================
# EVENT UNIT FILES
# ============================================================

def event_unit_filename(e):

    return (
        f"{e['event_id']}_"
        f"{safe_name(e['event_title'])}.md"
    )


def save_event_unit(
    date,
    event,
    content
):

    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    p = target / event_unit_filename(
        event
    )

    sources = "\n".join(
        f"- {a['source']} | "
        f"{a['title']} | "
        f"{a['source_url']}"
        for a in event[
            "articles"
        ]
    )

    p.write_text(
        f"""---
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

{content}

## 原始来源映射

{sources}
""",
        encoding="utf-8"
    )

    return p


# ============================================================
# EVENT INDEX
# ============================================================

def save_aggregation_index(
    date,
    events
):

    data = []

    for e in events:

        data.append(
            {
                "event_id": e[
                    "event_id"
                ],
                "date": e[
                    "date"
                ],
                "event_title": e.get(
                    "event_title",
                    "未命名事件"
                ),
                "event_reason": e.get(
                    "event_reason",
                    ""
                ),
                "source_count": len(
                    e["articles"]
                ),
                "articles": [
                    {
                        "index": a[
                            "index"
                        ],
                        "title": a[
                            "title"
                        ],
                        "source": a[
                            "source"
                        ],
                        "source_url": a[
                            "source_url"
                        ],
                        "path": a[
                            "path"
                        ]
                    }
                    for a in e[
                        "articles"
                    ]
                ]
            }
        )

    p = (
        event_units_dir(date)
        / EVENT_INDEX_FILE
    )

    write_json(
        p,
        data
    )

    return p


def load_event_index(
    date
):

    p = (
        event_units_dir(date)
        / EVENT_INDEX_FILE
    )

    if not p.exists():
        return None

    try:

        d = read_json(
            p,
            None
        )

    except Exception:

        return None

    return (
        d
        if isinstance(
            d,
            list
        ) and d
        else None
    )


# ============================================================
# EVENT FILE VALIDATION
# ============================================================

def event_unit_file_valid(
    path,
    event_id
):

    if (
        not path.exists()
        or path.stat().st_size <= 0
    ):
        return False

    try:

        m, b = parse_front_matter(
            path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        )

    except Exception:

        return False

    return (
        bool(b.strip())
        and m.get("event_id")
        == event_id
        and m.get("status")
        == "completed"
    )


def inspect_event_units(
    date
):

    target = event_units_dir(
        date
    )

    if not target.exists():

        return {
            "exists": False,
            "complete": False,
            "index": None,
            "missing": [],
            "invalid": [],
            "unexpected": []
        }

    idx = load_event_index(
        date
    )

    if idx is None:

        return {
            "exists": True,
            "complete": False,
            "index": None,
            "missing": [],
            "invalid": [],
            "unexpected": []
        }

    missing = []
    invalid = []
    ids = []

    for e in idx:

        if not isinstance(
            e,
            dict
        ):
            invalid.append(
                "INDEX_ENTRY_NOT_OBJECT"
            )
            continue

        eid = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

        if not eid:
            invalid.append(
                "EMPTY_EVENT_ID"
            )
            continue

        ids.append(
            eid
        )

        matches = list(
            target.glob(
                f"{eid}_*.md"
            )
        )

        if not matches:

            missing.append(
                eid
            )

        elif not any(
            event_unit_file_valid(
                p,
                eid
            )
            for p in matches
        ):

            invalid.append(
                eid
            )

    complete = (
        bool(ids)
        and not missing
        and not invalid
    )

    return {
        "exists": True,
        "complete": complete,
        "index": idx,
        "missing": missing,
        "invalid": invalid,
        "unexpected": []
    }


def mark_event_units_complete(
    date,
    n,
    e
):

    p = (
        event_units_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    p.write_text(
        f"""EVENT_UNITS_COMPLETE
date: {date}
original_enriched_news: {n}
final_event_units: {e}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
""",
        encoding="utf-8"
    )

    return p


def remove_event_units_complete(
    date
):

    p = (
        event_units_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    if p.exists():
        p.unlink()


# ============================================================
# REBUILD FROM INDEX
# ============================================================

def rebuild_events_from_index(
    date,
    index,
    news
):

    out = []

    for e in index:

        if not isinstance(
            e,
            dict
        ):

            raise RuntimeError(
                "❌ Event Index存在非法条目"
            )

        arts = []

        article_records = e.get(
            "articles",
            []
        )

        if not isinstance(
            article_records,
            list
        ):

            raise RuntimeError(
                f"❌ {e.get('event_id')} "
                "articles不是数组"
            )

        for r in article_records:

            if not isinstance(
                r,
                dict
            ):

                raise RuntimeError(
                    f"❌ {e.get('event_id')} "
                    "存在非法Article Index"
                )

            i = int(
                r["index"]
            )

            if not (
                1 <= i <= len(news)
            ):

                raise RuntimeError(
                    f"❌ {e.get('event_id')} "
                    f"引用不存在文章：{i}"
                )

            item = news[
                i - 1
            ]

            m = item[
                "metadata"
            ]

            arts.append(
                {
                    "index": i,
                    "path": str(
                        item["path"]
                    ),
                    "title": m.get(
                        "title",
                        "Untitled"
                    ),
                    "source": m.get(
                        "source",
                        "Unknown"
                    ),
                    "source_url": m.get(
                        "source_url",
                        ""
                    ),
                    "source_status": m.get(
                        "source_status",
                        ""
                    ),
                    "content_status": m.get(
                        "content_status",
                        ""
                    ),
                    "body": item["body"]
                }
            )

        out.append(
            {
                "event_id": str(
                    e["event_id"]
                ),
                "date": date,
                "event_title": e.get(
                    "event_title",
                    "未命名事件"
                ),
                "event_reason": e.get(
                    "event_reason",
                    ""
                ),
                "articles": arts
            }
        )

    return out


# ============================================================
# EVENT INDEX COVERAGE
# ============================================================

def validate_event_index_coverage(
    date,
    events,
    n
):

    ids = []
    eids = set()

    for e in events:

        if e["event_id"] in eids:

            raise RuntimeError(
                f"❌ {date} Event Index重复"
                f"event_id：{e['event_id']}"
            )

        eids.add(
            e["event_id"]
        )

        ids.extend(
            a["index"]
            for a in e["articles"]
        )

    if (
        set(ids)
        != set(
            range(
                1,
                n + 1
            )
        )
        or len(ids)
        != len(set(ids))
    ):

        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败"
        )


# ============================================================
# COMPLETE EXISTING EVENT UNITS
# ============================================================

def complete_existing_event_units(
    date,
    events,
    n
):

    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    generated = 0

    for i, e in enumerate(
        events,
        1
    ):

        matches = target.glob(
            f"{e['event_id']}_*.md"
        )

        if any(
            event_unit_file_valid(
                p,
                e["event_id"]
            )
            for p in matches
        ):

            print(
                f"[{i}/{len(events)}] "
                f"⏭️ 已存在："
                f"{e['event_id']}"
            )

            continue

        print(
            f"[{i}/{len(events)}] "
            f"🔨 生成："
            f"{e['event_id']}"
        )

        content = synthesize_event(
            e
        )

        if not content.strip():

            raise RuntimeError(
                f"❌ {e['event_id']} "
                "综合结果为空"
            )

        p = save_event_unit(
            date,
            e,
            content
        )

        if not event_unit_file_valid(
            p,
            e["event_id"]
        ):

            raise RuntimeError(
                f"❌ {e['event_id']} "
                "保存验证失败"
            )

        generated += 1

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    for e in events:

        if not any(
            event_unit_file_valid(
                p,
                e["event_id"]
            )
            for p in target.glob(
                f"{e['event_id']}_*.md"
            )
        ):

            raise RuntimeError(
                f"❌ {e['event_id']} "
                "最终缺失"
            )

    marker = mark_event_units_complete(
        date,
        n,
        len(events)
    )

    print(
        f"✅ EVENT UNITS COMPLETE "
        f"| new={generated} "
        f"total={len(events)} "
        f"| {marker}"
    )

    return True


# ============================================================
# STAGE 1
# ============================================================

def run_stage_1(
    date
):

    print(
        f"\n"
        f"{'=' * 70}\n"
        f"STAGE 1 — EVENT UNIT GENERATION V6: "
        f"{date}\n"
        f"{'=' * 70}"
    )

    inspection = inspect_event_units(
        date
    )

    if inspection[
        "complete"
    ]:

        print(
            f"✅ {date} EventUnits已经完整，"
            "跳过AI聚合。"
        )

        return False

    news = load_all_enriched_news(
        date
    )

    # --------------------------------------------------------
    # Existing Index → Resume
    # --------------------------------------------------------

    if inspection[
        "index"
    ] is not None:

        print(
            f"🔄 {date} 检测到已有Event Index，"
            "进入断点续跑。"
        )

        events = rebuild_events_from_index(
            date,
            inspection["index"],
            news
        )

        validate_event_index_coverage(
            date,
            events,
            len(news)
        )

        return complete_existing_event_units(
            date,
            events,
            len(news)
        )

    # --------------------------------------------------------
    # Fresh aggregation
    # --------------------------------------------------------

    remove_event_units_complete(
        date
    )

    initial = build_initial_clusters(
        date,
        news
    )

    final = merge_all_clusters(
        date,
        initial,
        len(news)
    )

    events = build_event_units(
        date,
        final,
        news
    )

    validate_event_index_coverage(
        date,
        events,
        len(news)
    )

    p = save_aggregation_index(
        date,
        events
    )

    print(
        f"✅ Event Index saved: {p}"
    )

    return complete_existing_event_units(
        date,
        events,
        len(news)
    )


# ============================================================
# STAGE 2 — LOAD EVENT UNITS
# ============================================================

def load_saved_event_units(
    date
):

    target = event_units_dir(
        date
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

    idx = load_event_index(
        date
    )

    if idx is None:

        raise RuntimeError(
            f"❌ {date} Event Index不存在或无效"
        )

    files = []

    for e in idx:

        if not isinstance(
            e,
            dict
        ):

            raise RuntimeError(
                "❌ Event Index存在非法Event"
            )

        eid = str(
            e.get(
                "event_id",
                ""
            )
        )

        matches = sorted(
            target.glob(
                f"{eid}_*.md"
            )
        )

        valid = next(
            (
                p
                for p in matches
                if event_unit_file_valid(
                    p,
                    eid
                )
            ),
            None
        )

        if valid is None:

            raise RuntimeError(
                f"❌ EventUnit缺失或无效："
                f"{eid}"
            )

        files.append(
            (
                e,
                valid
            )
        )

    return files


# ============================================================
# STAGE 2 — ONE SKILL
# ============================================================

def run_one_skill(
    event,
    skill
):

    content = event[
        1
    ].read_text(
        encoding="utf-8",
        errors="replace"
    )

    event_meta = event[0]

    prompt = f"""
你正在执行748686自生长知识系统V6的27 Skills深度处理。

事件：
{event_meta.get('event_title', '')}

Event ID：
{event_meta.get('event_id', '')}

Skill名称：
{skill['name']}

============================================================
Skill规则
============================================================

{skill['content']}

============================================================
EventUnit原文
============================================================

{content[:30000]}

============================================================
任务
============================================================

请严格按照该Skill完成深度处理。

不要编造。

只使用EventUnit提供的信息。

输出可直接写入知识库的中文Markdown。
""".strip()

    return call_ai(
        prompt,
        (
            "你是748686知识系统Skill执行器。"
            "严格执行Skill规则，不得编造。"
        ),
        0.2
    )


# ============================================================
# STAGE 2
# ============================================================

def run_stage_2(
    date
):

    files = load_saved_event_units(
        date
    )

    skills = load_skills()

    routes = load_routes()

    print(
        f"\nSTAGE 2 — 27 SKILLS "
        f"| Events={len(files)} "
        f"| Skills={len(skills)}"
    )

    # --------------------------------------------------------
    # Prefer configured route categories.
    # Preserve deterministic order.
    # --------------------------------------------------------

    route_values = []
    selected_names = set()

    for category, names in routes.items():

        if not isinstance(
            names,
            list
        ):
            continue

        for name in names:

            if (
                name in skills
                and name not in selected_names
            ):

                route_values.append(
                    skills[name]
                )

                selected_names.add(
                    name
                )

    selected = (
        route_values
        or [
            skills[k]
            for k in sorted(skills)
        ]
    )

    outroot = event_units_dir(
        date
    )

    for ei, event in enumerate(
        files,
        1
    ):

        eid = event[0].get(
            "event_id",
            ""
        )

        edir = (
            outroot
            / eid
        )

        edir.mkdir(
            parents=True,
            exist_ok=True
        )

        for si, skill in enumerate(
            selected,
            1
        ):

            outfile = (
                edir
                / (
                    f"{safe_name(skill['name'])}"
                    .replace(
                        ".md",
                        ""
                    )
                    + ".md"
                )
            )

            if (
                outfile.exists()
                and outfile.stat().st_size > 0
            ):

                print(
                    f"[{ei}/{len(files)}]"
                    f"[{si}/{len(selected)}] "
                    f"⏭️ {outfile.name}"
                )

                continue

            print(
                f"[{ei}/{len(files)}]"
                f"[{si}/{len(selected)}] "
                f"🤖 {skill['name']}"
            )

            result = run_one_skill(
                event,
                skill
            )

            if not result.strip():

                raise RuntimeError(
                    f"❌ Skill结果为空："
                    f"{eid} / {skill['name']}"
                )

            outfile.write_text(
                result,
                encoding="utf-8"
            )

    marker = (
        outroot
        / SKILLS_COMPLETE_FILE
    )

    marker.write_text(
        f"""SKILLS_COMPLETE
date: {date}
events: {len(files)}
skills: {len(selected)}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
""",
        encoding="utf-8"
    )

    print(
        f"✅ STAGE 2 COMPLETE: {date}"
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=(
            "748686 Knowledge "
            "Pipeline V6.1"
        )
    )

    ap.add_argument(
        "--date",
        required=True
    )

    ap.add_argument(
        "--stage",
        choices=[
            "aggregation",
            "skills",
            "all"
        ],
        default="aggregation"
    )

    args = ap.parse_args()

    try:

        if args.stage in (
            "aggregation",
            "all"
        ):

            run_stage_1(
                args.date
            )

        if args.stage in (
            "skills",
            "all"
        ):

            run_stage_2(
                args.date
            )

    except KeyboardInterrupt:

        print(
            "\n❌ 用户中断"
        )

        return 130

    except Exception as e:

        print(
            "\n❌ Knowledge Pipeline "
            f"V6 FAILED: {e}",
            file=sys.stderr
        )

        return 1

    print(
        "\n✅ Knowledge Pipeline V6 "
        f"finished: {args.date} / "
        f"{args.stage}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
