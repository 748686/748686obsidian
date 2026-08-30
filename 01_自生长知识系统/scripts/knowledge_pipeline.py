#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统 - Knowledge Pipeline V6.2

================================================================
V6.2
================================================================

Stage 1:
Enriched News
    ↓
AI Batch Clustering
    ↓
Stable Cluster Membership
    ↓
Overlapping Global Merge
    ↓
EventUnits

Stage 2:
EventUnits
    ↓
27 Skills Deep Processing


================================================================
V6.2 GLOBAL MERGE ENGINE
================================================================

V6.1 的 Global Merge 使用：

    Window
      ↓
    AI Groups
      ↓
    Article Index Dedup
      ↓
    新 Cluster

这种方式会导致：

    Window overlap
        ↓
    新 Cluster 重建
        ↓
    下一轮重新切窗
        ↓
    Cluster membership 丢失
        ↓
    Global coverage 异常

典型错误：

    Global Merge覆盖异常
    Duplicate=[]
    Missing=[4]
    Extra=[]
    Malformed=[]


V6.2 改为：

    Initial Cluster
        ↓
    member_cluster_ids
        ↓
    Overlapping Windows
        ↓
    AI 判断需要合并的 Cluster
        ↓
    Union / Connected Components
        ↓
    Stable Global Cluster Membership
        ↓
    下一轮继续

重要：

- ARTICLE ID 只负责文章覆盖
- Cluster ID 只负责 Cluster 覆盖
- overlap 可以重复进入多个 Window
- Window 重叠不会再被当成 Duplicate
- 每个原始 Cluster 永久保留 membership
- 每一轮都验证 Cluster membership 完整覆盖
- 最终 EventUnit 再验证 ARTICLE 1..N 恰好一次
- 只有“本轮没有任何实际合并”才判定 Converged


================================================================
V6.2 保留
================================================================

- Batch Size = 40
- Global Merge Window = 30
- Global Merge Overlap = 15
- 跨来源事件聚类
- 跨语言事件聚类
- ARTICLE 自动冲突修复
- 多轮 Global Merge
- Event Index
- EventUnit 断点续跑
- EventUnit 完成机制
- Stage 2
- 27 Skills
- 已完成 Skill 跳过
- AGNES API
- AI 请求节流
- HTTP 429 自动重试
- Retry-After
- 指数退避
- 随机抖动

================================================================
API
================================================================

Base URL:
https://api.agnes-ai.cn/v1

Model:
agnes-2.5-flash

Key:
AGNES_API_KEY
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ============================================================
# PATHS
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
# FILE / EVENT CONSTANTS
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnits"

EVENT_INDEX_FILE = "_event_index.json"

EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"

SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"


# ============================================================
# AGNES API
# ============================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"

AGNES_MODEL = "agnes-2.5-flash"

AGNES_API_KEY_ENV = "AGNES_API_KEY"


# ============================================================
# AI SETTINGS
# ============================================================

DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180


# ============================================================
# ANTI-429 SETTINGS
# ============================================================

AI_REQUEST_THROTTLE_SECONDS = 1.5

AI_MAX_429_RETRIES = 5

AI_429_BACKOFF_BASE = 10

AI_429_BACKOFF_MAX = 180

AI_429_JITTER_MAX = 3

_LAST_AI_REQUEST_TIME = 0.0


# ============================================================
# PIPELINE SETTINGS
# ============================================================

AGGREGATION_BATCH_SIZE = 40

GLOBAL_MERGE_WINDOW_SIZE = 30

GLOBAL_MERGE_OVERLAP = 15

MAX_GLOBAL_MERGE_ROUNDS = 12

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2


# ============================================================
# TIMEZONE
# ============================================================

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


# ============================================================
# CONFLICT LOG
# ============================================================

def log_conflict(date, stage, message, details=None):

    LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

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

        f.write(
            "\n".join(lines)
        )

    print(
        f"⚠️ {message}"
    )

    print(
        f"   Conflict log: "
        f"{conflict_log_path(date)}"
    )


# ============================================================
# JSON
# ============================================================

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


# ============================================================
# AI JSON PARSER
# ============================================================

def parse_ai_json(result, context):

    text = str(result).strip()

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

    try:

        return json.loads(text)

    except Exception as e:

        raise RuntimeError(
            f"❌ AI JSON解析失败：{context}\n\n"
            f"{text[:5000]}"
        ) from e


# ============================================================
# SAFE FILE NAME
# ============================================================

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
# AI THROTTLE
# ============================================================

def wait_for_ai_throttle():

    global _LAST_AI_REQUEST_TIME

    now_mono = time.monotonic()

    elapsed = (
        now_mono
        - _LAST_AI_REQUEST_TIME
    )

    remaining = (
        AI_REQUEST_THROTTLE_SECONDS
        - elapsed
    )

    if remaining > 0:

        print(
            f"   ⏳ AI请求节流等待 "
            f"{remaining:.1f}s"
        )

        time.sleep(
            remaining
        )

    _LAST_AI_REQUEST_TIME = (
        time.monotonic()
    )


# ============================================================
# RETRY-AFTER
# ============================================================

def parse_retry_after(headers):

    if headers is None:

        return None

    value = headers.get(
        "Retry-After"
    )

    if value is None:

        return None

    value = str(
        value
    ).strip()

    if not value:

        return None

    try:

        seconds = float(
            value
        )

        if seconds < 0:

            return None

        return seconds

    except ValueError:

        return None


# ============================================================
# 429 BACKOFF
# ============================================================

def calculate_429_backoff(
    retry_number
):

    base = (
        AI_429_BACKOFF_BASE
        * (
            2
            ** (
                retry_number - 1
            )
        )
    )

    base = min(
        base,
        AI_429_BACKOFF_MAX
    )

    jitter = random.uniform(
        0,
        AI_429_JITTER_MAX
    )

    return min(
        base + jitter,
        AI_429_BACKOFF_MAX
    )


# ============================================================
# UNIFIED AI CALL
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
        AGNES_BASE_URL
        + "/chat/completions",

        data=payload,

        headers={
            "Authorization":
                f"Bearer {key}",

            "Content-Type":
                "application/json",

            "Accept":
                "application/json",

            "User-Agent":
                "748686-Knowledge-Pipeline/6.2"
        },

        method="POST"
    )

    for attempt in range(
        0,
        AI_MAX_429_RETRIES + 1
    ):

        wait_for_ai_throttle()

        try:

            with urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as r:

                raw = r.read().decode(
                    "utf-8"
                )

            try:

                data = json.loads(
                    raw
                )

            except Exception as e:

                raise RuntimeError(
                    "❌ AGNES.ai 返回不是合法JSON\n"
                    + raw[:3000]
                ) from e

            try:

                result = (
                    data["choices"][0]
                    ["message"]
                    ["content"]
                )

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

            return str(
                result
            ).strip()

        except HTTPError as e:

            body = ""

            try:

                body = e.read().decode(
                    "utf-8",
                    errors="replace"
                )

            except Exception:

                body = ""

            if e.code == 429:

                if attempt >= AI_MAX_429_RETRIES:

                    print(
                        "\n❌ AGNES.ai HTTP 429"
                        " — 已达到最大自动重试次数"
                    )

                    print(
                        f"   最大重试次数："
                        f"{AI_MAX_429_RETRIES}"
                    )

                    if body:

                        print(
                            "   Server Response:\n"
                            f"{body[:3000]}"
                        )

                    raise RuntimeError(
                        "❌ AGNES.ai HTTP 429："
                        "自动重试次数耗尽"
                    ) from e

                retry_number = (
                    attempt + 1
                )

                retry_after = (
                    parse_retry_after(
                        e.headers
                    )
                )

                if retry_after is not None:

                    wait_seconds = min(
                        retry_after,
                        AI_429_BACKOFF_MAX
                    )

                    wait_source = (
                        "Retry-After"
                    )

                else:

                    wait_seconds = (
                        calculate_429_backoff(
                            retry_number
                        )
                    )

                    wait_source = (
                        "指数退避"
                    )

                print(
                    "\n⚠️ AGNES.ai HTTP 429 "
                    "— 触发自动重试"
                )

                print(
                    f"   Retry: "
                    f"{retry_number}/"
                    f"{AI_MAX_429_RETRIES}"
                )

                print(
                    f"   Wait: "
                    f"{wait_seconds:.1f}s"
                )

                print(
                    f"   Source: "
                    f"{wait_source}"
                )

                if body:

                    compact_body = re.sub(
                        r"\s+",
                        " ",
                        body
                    ).strip()

                    print(
                        "   Response: "
                        f"{compact_body[:1000]}"
                    )

                time.sleep(
                    wait_seconds
                )

                continue

            raise RuntimeError(
                f"❌ AGNES.ai HTTP错误 "
                f"{e.code}\n"
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

    raise RuntimeError(
        "❌ AGNES.ai 请求异常结束"
    )


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

            "content":
                p.read_text(
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

    if not routes:

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

    for name in routes.get(
        category,
        []
    ):

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
        f"Enriched files: "
        f"{len(files)}"
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
        if x["metadata"]
        .get(
            "title",
            ""
        )
        .strip()
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
        f"Valid news: "
        f"{len(items)}"
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

    return f"""[ARTICLE {index}]

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
{item["body"][:ARTICLE_CLUSTER_CONTENT_LIMIT]}"""


# ============================================================
# CLUSTER VALIDATION
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

                i = int(v)

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
        i: p
        for i, p in occ.items()
        if len(p) > 1
    }

    actual = set(
        occ
    )

    return {
        "duplicate": duplicate,

        "missing":
            sorted(
                expected - actual
            ),

        "extra":
            sorted(
                actual - expected
            ),

        "malformed":
            malformed
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

    out = []

    for c in cs:

        if not isinstance(
            c,
            dict
        ):

            out.append(c)

            continue

        d = dict(c)

        ids = d.get(
            "article_indexes",
            []
        )

        if isinstance(
            ids,
            list
        ):

            d[
                "article_indexes"
            ] = [
                (
                    int(x)
                    if str(x)
                    .lstrip("-")
                    .isdigit()
                    else x
                )
                for x in ids
            ]

        out.append(d)

    return out


# ============================================================
# STAGE 1A
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
        for i, x in enumerate(
            items
        )
    )

    prompt = f"""你正在执行748686自生长知识系统V6.2第二层事件聚合。
日期：{date}

{joined}

任务：识别哪些新闻属于同一个现实世界事件。

支持：
- 跨来源
- 跨语言

不要因为：
- 关键词相同
- 公司相同
- 行业相同
- 国家相同

就强行合并。

无法确定时宁可分开。

绝对覆盖：
ARTICLE编号为：
{json.dumps(expected)}

每篇必须且只能属于一个cluster。

不得：
- 遗漏ARTICLE
- 重复ARTICLE
- 创造ARTICLE编号

无法与其他文章合并的文章必须单独成为cluster。

只输出JSON：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "统一事件名称",
      "event_reason": "事件判断"
    }}
  ]
}}"""

    data = parse_ai_json(
        call_ai(
            prompt,
            "你是全球新闻事件聚类专家。"
            "每篇ARTICLE必须且只能属于一个cluster。",
            0
        ),
        f"{date} 第一轮新闻聚类"
    )

    cs = data.get(
        "clusters"
    )

    if not isinstance(
        cs,
        list
    ):

        raise RuntimeError(
            f"❌ {date} 第一轮聚类结果缺少clusters"
        )

    return normalize_clusters(
        cs
    )


# ============================================================
# CLUSTER REPAIR
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
        for i, x in enumerate(
            items
        )
    )

    prompt = f"""修复748686 V6.2 ARTICLE覆盖冲突。

日期：{date}
第{attempt}次修复

真实ARTICLE：
{json.dumps(expected)}

文章：

{joined}

上次结果：

{json.dumps(
    broken,
    ensure_ascii=False,
    indent=2
)}

检测问题：

{json.dumps(
    issues,
    ensure_ascii=False,
    indent=2
)}

重新判断全部文章。

要求：

- 同事件合并
- 不同事件分开
- 每篇ARTICLE恰好一次
- Missing=0
- Duplicate=0
- Extra=0

只输出JSON：

{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "事件",
      "event_reason": "原因"
    }}
  ]
}}"""

    data = parse_ai_json(
        call_ai(
            prompt,
            "你是新闻事件聚类冲突修复专家。",
            0
        ),
        f"{date} 聚类冲突修复 #{attempt}"
    )

    cs = data.get(
        "clusters"
    )

    if not isinstance(
        cs,
        list
    ):

        raise RuntimeError(
            "❌ 聚类修复结果缺少clusters"
        )

    return normalize_clusters(
        cs
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

    cs = cluster_news_batch(
        date,
        items,
        start
    )

    issues = inspect_cluster_assignment(
        cs,
        expected
    )

    if valid_issues(
        issues
    ):

        return cs

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

        cs = repair_cluster_news_batch(
            date,
            items,
            start,
            cs,
            issues,
            attempt
        )

        issues = inspect_cluster_assignment(
            cs,
            expected
        )

        if valid_issues(
            issues
        ):

            print(
                "   ✅ Cluster conflict "
                "repaired successfully."
            )

            return cs

        log_conflict(
            date,
            f"STAGE 1A / BATCH {batch_no}",
            f"第{attempt}次聚类冲突修复仍然失败。",
            {
                "issues": issues,
                "clusters": cs
            }
        )

    raise RuntimeError(
        f"❌ {date} Batch {batch_no} "
        "ARTICLE聚类覆盖冲突无法自动修复："
        f"{issues}"
    )


# ============================================================
# ARTICLE COVERAGE
# ============================================================

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

    if valid_issues(
        issues
    ):

        return

    if date:

        log_conflict(
            date,
            context,
            "聚类覆盖验证失败。",
            issues
        )

    raise RuntimeError(
        f"❌ {context} 聚类覆盖失败："
        f"{issues}"
    )


# ============================================================
# INITIAL CLUSTERS
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
        f"Input Enriched News: "
        f"{total}"
    )

    print(
        f"Batch Size: "
        f"{AGGREGATION_BATCH_SIZE}"
    )

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE
    ):

        n = (
            start
            // AGGREGATION_BATCH_SIZE
            + 1
        )

        end = min(
            start
            + AGGREGATION_BATCH_SIZE,
            total
        )

        print(
            f"\n🔹 Cluster Batch {n}: "
            f"{start + 1}-{end}/{total}"
        )

        cs = cluster_news_batch_with_repair(
            date,
            news[start:end],
            start + 1,
            n
        )

        validate_cluster_coverage(
            cs,
            range(
                start + 1,
                end + 1
            ),
            f"{date} Batch {n}",
            date
        )

        for ci, c in enumerate(
            cs,
            1
        ):

            cluster_id = (
                f"B{n:03d}-"
                f"{c['cluster_id']}"
            )

            article_indexes = sorted(
                set(
                    int(x)
                    for x
                    in c[
                        "article_indexes"
                    ]
                )
            )

            allc.append(
                {
                    "cluster_id":
                        cluster_id,

                    "event_title":
                        c.get(
                            "event_title",
                            "未命名事件"
                        ),

                    "event_reason":
                        c.get(
                            "event_reason",
                            ""
                        ),

                    "article_indexes":
                        article_indexes,

                    # ==================================================
                    # V6.2:
                    # 永久保存这个 Cluster 最初属于哪个原始 Cluster。
                    # 后续 Global Merge 只能合并 membership，
                    # 不再丢失这个信息。
                    # ==================================================
                    "member_cluster_ids":
                        [
                            cluster_id
                        ]
                }
            )

        print(
            f"   Clusters generated: "
            f"{len(cs)}"
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

    validate_global_cluster_membership(
        date,
        allc,
        "STAGE 1A INITIAL"
    )

    print(
        f"\n✅ Initial Clusters: "
        f"{len(allc)}"
    )

    return allc


# ============================================================
# MERGE WINDOWS
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
            s
            + GLOBAL_MERGE_WINDOW_SIZE,
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
# GLOBAL CLUSTER MEMBERSHIP VALIDATION
# ============================================================

def validate_global_cluster_membership(
    date,
    clusters,
    context
):

    seen_current = set()

    seen_original = set()

    malformed = []

    duplicate_current = []

    duplicate_original = []

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

        cid = str(
            c.get(
                "cluster_id",
                ""
            )
        ).strip()

        if not cid:

            malformed.append(
                f"cluster[{pos}]缺少cluster_id"
            )

        elif cid in seen_current:

            duplicate_current.append(
                cid
            )

        else:

            seen_current.add(
                cid
            )

        members = c.get(
            "member_cluster_ids"
        )

        if not isinstance(
            members,
            list
        ) or not members:

            malformed.append(
                f"cluster[{pos}]"
                "member_cluster_ids无效"
            )

            continue

        for member in members:

            member = str(
                member
            ).strip()

            if not member:

                malformed.append(
                    f"cluster[{pos}]"
                    "存在空member_cluster_id"
                )

                continue

            if member in seen_original:

                duplicate_original.append(
                    member
                )

            else:

                seen_original.add(
                    member
                )

    if (
        malformed
        or duplicate_current
        or duplicate_original
    ):

        log_conflict(
            date,
            context,
            "Global Cluster membership验证失败。",
            {
                "malformed": malformed,
                "duplicate_current":
                    duplicate_current,
                "duplicate_original":
                    duplicate_original
            }
        )

        raise RuntimeError(
            f"❌ {context} "
            "Global Cluster membership异常："
            f"Malformed={malformed} "
            f"DuplicateCurrent={duplicate_current} "
            f"DuplicateOriginal={duplicate_original}"
        )


# ============================================================
# UNION-FIND
# ============================================================

class UnionFind:

    def __init__(
        self,
        values
    ):

        self.parent = {
            value: value
            for value in values
        }

        self.rank = {
            value: 0
            for value in values
        }

    def find(
        self,
        value
    ):

        parent = self.parent[value]

        if parent != value:

            self.parent[value] = (
                self.find(parent)
            )

        return self.parent[value]

    def union(
        self,
        a,
        b
    ):

        ra = self.find(a)

        rb = self.find(b)

        if ra == rb:

            return False

        if (
            self.rank[ra]
            <
            self.rank[rb]
        ):

            ra, rb = rb, ra

        self.parent[rb] = ra

        if (
            self.rank[ra]
            ==
            self.rank[rb]
        ):

            self.rank[ra] += 1

        return True

    def components(self):

        result = {}

        for value in self.parent:

            root = self.find(
                value
            )

            result.setdefault(
                root,
                []
            ).append(
                value
            )

        return result


# ============================================================
# GLOBAL MERGE WINDOW AI
# ============================================================

def merge_cluster_window(
    date,
    window,
    round_no,
    window_no
):

    joined_blocks = []

    for i, c in enumerate(
        window,
        1
    ):

        joined_blocks.append(
            f"""[CLUSTER {i}]
Cluster ID：
{c['cluster_id']}

原始Cluster成员：
{json.dumps(
    c.get(
        'member_cluster_ids',
        []
    ),
    ensure_ascii=False
)}

事件名称：
{c.get(
    'event_title',
    '未命名事件'
)}

事件判断：
{c.get(
    'event_reason',
    ''
)}

文章数量：
{len(
    c.get(
        'article_indexes',
        []
    )
)}

文章编号：
{json.dumps(
    c.get(
        'article_indexes',
        []
    )
)}"""
        )

    joined = "\n\n".join(
        joined_blocks
    )

    expected = list(
        range(
            1,
            len(window) + 1
        )
    )

    prompt = f"""你正在执行748686自生长知识系统V6.2全局事件归并。

日期：
{date}

轮次：
{round_no}

窗口：
{window_no}

{joined}

任务：

判断这些Cluster是否属于同一个“具体现实世界事件”。

可以合并：

- 同一政策发布
- 同一公司重大动作
- 同一事故
- 同一产品发布
- 同一具体现实事件
- 同一正在持续发展的单一现实事件

不得合并：

- 同公司不同事件
- 同人物不同事件
- 同国家不同事件
- 同行业不同事件
- 同趋势不同具体事件
- 仅因为关键词相同
- 仅因为主题相同

无法确认时宁可分开。

重要：

这是“事件归并”，不是主题归类。

输入Cluster编号：

{json.dumps(expected)}

要求：

1. 每个输入Cluster必须且只能进入一个group。
2. 不得遗漏。
3. 不得重复。
4. 不得创造不存在的Cluster编号。
5. 一个group可以只包含一个Cluster。
6. Cluster ID只是身份标识，不要修改。
7. 不需要返回文章编号。
8. 只根据当前窗口中的Cluster进行判断。

只输出JSON：

{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1, 4],
      "event_title": "统一事件名称",
      "reason": "为什么这些Cluster属于同一个现实世界事件"
    }}
  ]
}}"""

    data = parse_ai_json(
        call_ai(
            prompt,
            "你是全球新闻事件归并专家。"
            "必须覆盖全部输入Cluster，每个恰好一次。"
            "这是具体事件合并，不是主题分类。",
            0
        ),
        f"{date} Global Merge "
        f"Round {round_no} "
        f"Window {window_no}"
    )

    groups = data.get(
        "groups"
    )

    if not isinstance(
        groups,
        list
    ):

        raise RuntimeError(
            "❌ Global Merge缺少groups"
        )

    actual = []

    malformed = []

    for p, g in enumerate(
        groups,
        1
    ):

        if not isinstance(
            g,
            dict
        ):

            malformed.append(
                f"group[{p}]不是对象"
            )

            continue

        ids = g.get(
            "cluster_indexes"
        )

        if (
            not isinstance(
                ids,
                list
            )
            or not ids
        ):

            malformed.append(
                f"group[{p}] "
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
                    f"group[{p}]"
                    f"非法编号：{x}"
                )

    dup = sorted(
        {
            x
            for x in actual
            if actual.count(x) > 1
        }
    )

    miss = sorted(
        set(expected)
        - set(actual)
    )

    extra = sorted(
        set(actual)
        - set(expected)
    )

    if (
        dup
        or miss
        or extra
        or malformed
    ):

        log_conflict(
            date,
            f"STAGE 1B / ROUND {round_no} "
            f"/ WINDOW {window_no}",
            "V6.2 Global Merge窗口AI输出覆盖异常。",
            {
                "duplicate": dup,
                "missing": miss,
                "extra": extra,
                "malformed": malformed,
                "groups": groups
            }
        )

        raise RuntimeError(
            "❌ Global Merge窗口AI输出异常 "
            f"Duplicate={dup} "
            f"Missing={miss} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )

    return groups


# ============================================================
# APPLY WINDOW GROUPS TO UNION-FIND
# ============================================================

def apply_window_groups(
    uf,
    window,
    groups,
    round_no,
    window_no
):

    group_records = []

    for gp, g in enumerate(
        groups,
        1
    ):

        indexes = [
            int(x)
            for x
            in g[
                "cluster_indexes"
            ]
        ]

        current_cluster_ids = [
            window[
                i - 1
            ][
                "cluster_id"
            ]
            for i in indexes
        ]

        if not current_cluster_ids:

            raise RuntimeError(
                "❌ Global Merge产生空group"
            )

        anchor = (
            current_cluster_ids[0]
        )

        merged_here = False

        for cid in current_cluster_ids[1:]:

            if uf.union(
                anchor,
                cid
            ):

                merged_here = True

        group_records.append(
            {
                "group_id":
                    g.get(
                        "group_id",
                        f"G{gp:03d}"
                    ),

                "cluster_ids":
                    current_cluster_ids,

                "event_title":
                    g.get(
                        "event_title",
                        "未命名事件"
                    ),

                "reason":
                    g.get(
                        "reason",
                        ""
                    ),

                "merged":
                    merged_here
            }
        )

    return group_records


# ============================================================
# REBUILD GLOBAL CLUSTERS
# ============================================================

def rebuild_global_clusters(
    current,
    uf,
    group_records
):

    by_id = {
        c["cluster_id"]: c
        for c in current
    }

    components = (
        uf.components()
    )

    ai_metadata = {}

    for record in group_records:

        for cid in record[
            "cluster_ids"
        ]:

            root = uf.find(
                cid
            )

            old = ai_metadata.get(
                root
            )

            candidate = {
                "event_title":
                    record.get(
                        "event_title",
                        ""
                    ),

                "event_reason":
                    record.get(
                        "reason",
                        ""
                    )
            }

            if old is None:

                ai_metadata[root] = (
                    candidate
                )

            else:

                old_reason = str(
                    old.get(
                        "event_reason",
                        ""
                    )
                )

                new_reason = str(
                    candidate.get(
                        "event_reason",
                        ""
                    )
                )

                if len(new_reason) > len(
                    old_reason
                ):

                    ai_metadata[root] = (
                        candidate
                    )

    rebuilt = []

    for root, member_ids in components.items():

        member_ids = sorted(
            member_ids
        )

        article_indexes = []

        old_titles = []

        old_reasons = []

        original_members = []

        for cid in member_ids:

            c = by_id[
                cid
            ]

            article_indexes.extend(
                c.get(
                    "article_indexes",
                    []
                )
            )

            old_titles.append(
                str(
                    c.get(
                        "event_title",
                        ""
                    )
                )
            )

            old_reasons.append(
                str(
                    c.get(
                        "event_reason",
                        ""
                    )
                )
            )

            original_members.extend(
                c.get(
                    "member_cluster_ids",
                    []
                )
            )

        metadata = ai_metadata.get(
            root,
            {}
        )

        title = str(
            metadata.get(
                "event_title",
                ""
            )
        ).strip()

        reason = str(
            metadata.get(
                "event_reason",
                ""
            )
        ).strip()

        if not title:

            title = max(
                old_titles,
                key=len,
                default="未命名事件"
            )

        if not reason:

            reason = max(
                old_reasons,
                key=len,
                default=""
            )

        article_indexes = sorted(
            set(
                map(
                    int,
                    article_indexes
                )
            )
        )

        original_members = sorted(
            set(
                map(
                    str,
                    original_members
                )
            )
        )

        # ====================================================
        # 新 Cluster ID
        #
        # ID 本身可以改变；
        # 真正稳定的是 member_cluster_ids。
        # ====================================================

        new_cluster_id = (
            "GM-"
            + min(
                original_members
            )
        )

        rebuilt.append(
            {
                "cluster_id":
                    new_cluster_id,

                "event_title":
                    title,

                "event_reason":
                    reason,

                "article_indexes":
                    article_indexes,

                "member_cluster_ids":
                    original_members
            }
        )

    rebuilt.sort(
        key=lambda c:
            min(
                c[
                    "article_indexes"
                ]
            )
    )

    return rebuilt


# ============================================================
# GLOBAL ARTICLE COVERAGE
# ============================================================

def validate_global_article_coverage(
    date,
    clusters,
    news_count,
    context
):

    allidx = []

    malformed = []

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
                f"cluster[{pos}]"
                "article_indexes不是数组"
            )

            continue

        for x in ids:

            try:

                allidx.append(
                    int(x)
                )

            except Exception:

                malformed.append(
                    f"cluster[{pos}]"
                    f"非法ARTICLE：{x}"
                )

    expected = set(
        range(
            1,
            news_count + 1
        )
    )

    actual = set(
        allidx
    )

    duplicate = sorted(
        {
            x
            for x in allidx
            if allidx.count(x) > 1
        }
    )

    missing = sorted(
        expected - actual
    )

    extra = sorted(
        actual - expected
    )

    if (
        duplicate
        or missing
        or extra
        or malformed
    ):

        log_conflict(
            date,
            context,
            "Global Article coverage异常。",
            {
                "duplicate":
                    duplicate,

                "missing":
                    missing,

                "extra":
                    extra,

                "malformed":
                    malformed
            }
        )

        raise RuntimeError(
            f"❌ {context} Article覆盖异常 "
            f"Duplicate={duplicate} "
            f"Missing={missing} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )


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
        + "\nSTAGE 1B — V6.2 GLOBAL EVENT MERGING\n"
        + "=" * 70
    )

    validate_global_cluster_membership(
        date,
        current,
        "STAGE 1B INITIAL"
    )

    validate_global_article_coverage(
        date,
        current,
        news_count,
        "STAGE 1B INITIAL"
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

            print(
                "🟢 GLOBAL MERGE CONVERGED "
                "| only one Cluster remains"
            )

            break

        windows = build_merge_windows(
            current
        )

        print(
            f"Windows: "
            f"{len(windows)} "
            f"| Size: "
            f"{GLOBAL_MERGE_WINDOW_SIZE} "
            f"| Overlap: "
            f"{GLOBAL_MERGE_OVERLAP}"
        )

        # ====================================================
        # V6.2:
        # Union-Find 针对“本轮输入 Cluster”建立。
        # ====================================================

        current_ids = [
            c["cluster_id"]
            for c in current
        ]

        uf = UnionFind(
            current_ids
        )

        round_group_records = []

        for wi, w in enumerate(
            windows,
            1
        ):

            print(
                f"🔹 Window {wi}/"
                f"{len(windows)} "
                f"| size={len(w)}"
            )

            groups = merge_cluster_window(
                date,
                w,
                rnd,
                wi
            )

            records = apply_window_groups(
                uf,
                w,
                groups,
                rnd,
                wi
            )

            round_group_records.extend(
                records
            )

        components = (
            uf.components()
        )

        after = len(
            components
        )

        actual_merge_happened = (
            after < before
        )

        print(
            f"   Union Components: "
            f"{after}"
        )

        if actual_merge_happened:

            print(
                f"   🔗 Actual merges: "
                f"{before - after}"
            )

        else:

            print(
                "   ℹ️ 本轮没有发生任何实际Cluster合并"
            )

        merged = rebuild_global_clusters(
            current,
            uf,
            round_group_records
        )

        # ====================================================
        # 每轮结束立即做双重覆盖验证
        # ====================================================

        validate_global_cluster_membership(
            date,
            merged,
            f"STAGE 1B ROUND {rnd}"
        )

        validate_global_article_coverage(
            date,
            merged,
            news_count,
            f"STAGE 1B ROUND {rnd}"
        )

        print(
            f"✅ Round {rnd}: "
            f"{before} -> {len(merged)}"
        )

        current = merged

        # ====================================================
        # 真正 Convergence：
        # 必须是本轮没有发生任何 Union。
        # ====================================================

        if not actual_merge_happened:

            print(
                "🟢 GLOBAL MERGE CONVERGED"
            )

            break

    else:

        print(
            f"⚠️ Global Merge达到最大轮次："
            f"{MAX_GLOBAL_MERGE_ROUNDS}"
        )

    # ========================================================
    # 最终 Global Cluster 验证
    # ========================================================

    validate_global_cluster_membership(
        date,
        current,
        "STAGE 1B FINAL"
    )

    validate_global_article_coverage(
        date,
        current,
        news_count,
        "STAGE 1B FINAL"
    )

    final = []

    for i, c in enumerate(
        current,
        1
    ):

        final.append(
            {
                "event_id":
                    f"EVT-{date}-{i:04d}",

                "event_title":
                    c.get(
                        "event_title",
                        "未命名事件"
                    ),

                "event_reason":
                    c.get(
                        "event_reason",
                        ""
                    ),

                "article_indexes":
                    sorted(
                        set(
                            map(
                                int,
                                c[
                                    "article_indexes"
                                ]
                            )
                        )
                    )
            }
        )

    # ========================================================
    # 最终 EventUnit ARTICLE 覆盖
    # ========================================================

    validate_global_article_coverage(
        date,
        final,
        news_count,
        "STAGE 1B FINAL EVENT UNITS"
    )

    print(
        f"\n✅ FINAL EVENT UNITS: "
        f"{len(final)}"
    )

    print(
        f"✅ ARTICLE COVERAGE: "
        f"{news_count}/{news_count}"
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

            if not 1 <= i <= len(news):

                raise RuntimeError(
                    f"❌ {c['event_id']} "
                    f"引用不存在文章：{i}"
                )

            m = news[
                i - 1
            ][
                "metadata"
            ]

            arts.append(
                {
                    "index":
                        i,

                    "path":
                        str(
                            news[
                                i - 1
                            ]["path"]
                        ),

                    "title":
                        m.get(
                            "title",
                            "Untitled"
                        ),

                    "source":
                        m.get(
                            "source",
                            "Unknown"
                        ),

                    "source_url":
                        m.get(
                            "source_url",
                            ""
                        ),

                    "source_status":
                        m.get(
                            "source_status",
                            ""
                        ),

                    "content_status":
                        m.get(
                            "content_status",
                            ""
                        ),

                    "body":
                        news[
                            i - 1
                        ]["body"]
                }
            )

        out.append(
            {
                "event_id":
                    c["event_id"],

                "date":
                    date,

                "event_title":
                    c["event_title"],

                "event_reason":
                    c["event_reason"],

                "articles":
                    arts
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
            f"""### 来源文章 #{a['index']}
标题：{a['title']}
来源：{a['source']}
链接：{a['source_url']}
source_status：{a['source_status']}
content_status：{a['content_status']}

内容：
{a['body'][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}"""
        )

    prompt = f"""你正在执行748686自生长知识系统V6.2第二层事件知识综合。

日期：
{event['date']}

事件ID：
{event['event_id']}

事件名称：
{event['event_title']}

第一轮事件判断：
{event['event_reason']}

同一事件的多来源输入：

{chr(10).join(blocks)}

把来源综合成一个高质量事件知识单元。

要求：

1. 识别共同事实
2. 保留来源独有信息
3. 保留不同地区视角
4. 区分事实与推测
5. 不编造
6. source_status不是fetched时不得声称完整阅读原文
7. 冲突明确指出
8. 资料不足明确说明

输出标准中文Markdown，包含：

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
"""

    return call_ai(
        prompt,
        "你是跨来源新闻综合专家。"
        "严格依据输入，不得编造。"
        "输出标准中文Markdown。",
        0.2
    )


# ============================================================
# EVENT UNIT FILE
# ============================================================

def event_unit_filename(
    e
):

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

    p = (
        target
        / event_unit_filename(
            event
        )
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
                "event_id":
                    e["event_id"],

                "date":
                    e["date"],

                "event_title":
                    e["event_title"],

                "event_reason":
                    e["event_reason"],

                "source_count":
                    len(
                        e["articles"]
                    ),

                "articles":
                    [
                        {
                            "index":
                                a["index"],

                            "title":
                                a["title"],

                            "source":
                                a["source"],

                            "source_url":
                                a["source_url"],

                            "path":
                                a["path"]
                        }
                        for a
                        in e["articles"]
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
        )
        and d
        else None
    )


# ============================================================
# EVENT UNIT VALIDATION
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
        bool(
            b.strip()
        )
        and m.get(
            "event_id"
        ) == event_id
        and m.get(
            "status"
        ) == "completed"
    )


def inspect_event_units(
    date
):

    target = event_units_dir(
        date
    )

    if not target.exists():

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

            "unexpected":
                []
        }

    idx = load_event_index(
        date
    )

    if idx is None:

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

            "unexpected":
                []
        }

    missing = []

    invalid = []

    ids = []

    for e in idx:

        eid = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

        ids.append(
            eid
        )

        matches = list(
            target.glob(
                f"{eid}_*.md"
            )
        ) if eid else []

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
        "exists":
            True,

        "complete":
            complete,

        "index":
            idx,

        "missing":
            missing,

        "invalid":
            invalid,

        "unexpected":
            []
    }


# ============================================================
# COMPLETE MARKER
# ============================================================

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
# REBUILD EVENTS FROM INDEX
# ============================================================

def rebuild_events_from_index(
    date,
    index,
    news
):

    out = []

    for e in index:

        arts = []

        for r in e.get(
            "articles",
            []
        ):

            i = int(
                r["index"]
            )

            if not 1 <= i <= len(news):

                raise RuntimeError(
                    f"❌ {e.get('event_id')} "
                    f"引用不存在文章：{i}"
                )

            m = news[
                i - 1
            ][
                "metadata"
            ]

            arts.append(
                {
                    "index":
                        i,

                    "path":
                        str(
                            news[
                                i - 1
                            ]["path"]
                        ),

                    "title":
                        m.get(
                            "title",
                            "Untitled"
                        ),

                    "source":
                        m.get(
                            "source",
                            "Unknown"
                        ),

                    "source_url":
                        m.get(
                            "source_url",
                            ""
                        ),

                    "source_status":
                        m.get(
                            "source_status",
                            ""
                        ),

                    "content_status":
                        m.get(
                            "content_status",
                            ""
                        ),

                    "body":
                        news[
                            i - 1
                        ]["body"]
                }
            )

        out.append(
            {
                "event_id":
                    str(
                        e["event_id"]
                    ),

                "date":
                    date,

                "event_title":
                    e.get(
                        "event_title",
                        "未命名事件"
                    ),

                "event_reason":
                    e.get(
                        "event_reason",
                        ""
                    ),

                "articles":
                    arts
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
                f"❌ {date} Event Index"
                f"重复event_id："
                f"{e['event_id']}"
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
        != len(
            set(ids)
        )
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

    for e in events:

        if not any(
            event_unit_file_valid(
                p,
                e["event_id"]
            )
            for p
            in target.glob(
                f"{e['event_id']}_*.md"
            )
        ):

            raise RuntimeError(
                f"❌ {e['event_id']} 最终缺失"
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
        f"\n{'=' * 70}\n"
        f"STAGE 1 — EVENT UNIT "
        f"GENERATION V6.2: {date}\n"
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

    if inspection[
        "index"
    ] is not None:

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
        f"✅ Event Index saved: "
        f"{p}"
    )

    return complete_existing_event_units(
        date,
        events,
        len(news)
    )


# ============================================================
# LOAD SAVED EVENT UNITS
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
            f"❌ {date} Event Index"
            "不存在或无效"
        )

    files = []

    for e in idx:

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
# ONE SKILL
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

    prompt = f"""你正在执行748686自生长知识系统V6.2的27 Skills深度处理。

事件：
{event[0].get(
    'event_title',
    ''
)}

Event ID：
{event[0].get(
    'event_id',
    ''
)}

Skill名称：
{skill['name']}

Skill规则：
{skill['content']}

EventUnit原文：
{content[:30000]}

请严格按照该Skill完成深度处理。

不要编造；
只使用EventUnit提供的信息。

输出可直接写入知识库的中文Markdown。
"""

    return call_ai(
        prompt,
        "你是748686知识系统Skill执行器。"
        "严格执行Skill规则，不得编造。",
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

    route_values = []

    selected_names = set()

    for category, names in routes.items():

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
            for k in sorted(
                skills
            )
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
                / f"{safe_name(skill['name']).replace('.md', '')}.md"
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
                    f"{eid} / "
                    f"{skill['name']}"
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
        f"✅ STAGE 2 COMPLETE: "
        f"{date}"
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=
        "748686 Knowledge Pipeline V6.2"
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
            f"\n❌ Knowledge Pipeline "
            f"V6.2 FAILED: {e}",
            file=sys.stderr
        )

        return 1

    print(
        f"\n✅ Knowledge Pipeline "
        f"V6.2 finished: "
        f"{args.date} / "
        f"{args.stage}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
