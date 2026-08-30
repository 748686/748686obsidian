#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统 - Knowledge Pipeline V6.1

================================================================
V6.1
================================================================

Stage 1:
Enriched News
    ↓
AI Batch Clustering
    ↓
Overlapping Global Merge
    ↓
EventUnits

Stage 2:
EventUnits
    ↓
27 Skills Deep Processing


================================================================
V6.1 新增：AGNES API 防 429 保护
================================================================

1. 普通 AI 请求之间自动节流
2. HTTP 429 自动重试
3. 自动读取 Retry-After
4. 指数退避：
       10s
       20s
       40s
       80s
       160s
5. 随机抖动，避免同时撞限流
6. 429 每次重试都会打印日志
7. 最终失败才终止 Pipeline
8. 与原有断点续跑完全兼容

重要：
- 不改变原有事件聚合逻辑
- 不改变 Batch Size = 40
- 不改变 Global Merge Window = 30
- 不改变 Global Merge Overlap = 15
- 不改变 27 Skills
- 不改变 Event Index
- 不改变 EventUnit 完成机制
- 不改变 Stage 2 已完成 Skill 跳过机制


================================================================
Key guarantees
================================================================

- all valid Enriched News are included; batch size 40
- duplicate/missing/extra article IDs are detected and repaired
- global merge uses 30-cluster windows with 15 overlap,
  repeated until convergence
- one article belongs to exactly one final EventUnit
- valid Event Index is resumable
- incomplete EventUnits are repaired
- Stage 2 only reads completed EventUnits
- AI HTTP 429 automatically retries
- API request rate is throttled
- failed requests do not silently lose articles
- API:
    https://api.agnes-ai.cn/v1
- model:
    agnes-2.5-flash
- key:
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
# V6.1 ANTI-429 SETTINGS
# ============================================================

# 正常情况下，两次 AI 请求之间至少间隔多少秒
#
# 你的整个 Pipeline 是串行执行的，因此这里不需要并发锁。
#
# 1.5 秒可以明显降低连续请求撞限流的概率，
# 同时不会像 5 秒、10 秒那样明显拖慢整个系统。
AI_REQUEST_THROTTLE_SECONDS = 1.5


# HTTP 429 最大自动重试次数
#
# 注意：
# 这里是“重试次数”，不是总请求次数。
#
# 第一次请求失败 429：
#   retry #1
#   retry #2
#   retry #3
#   retry #4
#   retry #5
#
# 一共最多 6 次请求。
AI_MAX_429_RETRIES = 5


# 指数退避初始值
AI_429_BACKOFF_BASE = 10


# 单次自动等待最大值
AI_429_BACKOFF_MAX = 180


# 随机抖动最大值
#
# 例如：
# 10 + random(0, 3)
#
# 可以减少多个任务在相同时间再次撞限流。
AI_429_JITTER_MAX = 3


# 全局记录最近一次 AI 请求时间
#
# 当前 Pipeline 是单线程串行执行，因此不需要 threading.Lock。
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
# V6.1 AI THROTTLE
# ============================================================

def wait_for_ai_throttle():
    """
    保证正常 AI 请求之间至少保持
    AI_REQUEST_THROTTLE_SECONDS 的间隔。

    注意：
    429 的 Retry-After / Backoff 等待由 call_ai()
    单独处理。
    """

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

        time.sleep(remaining)

    _LAST_AI_REQUEST_TIME = time.monotonic()


# ============================================================
# V6.1 RETRY-AFTER PARSER
# ============================================================

def parse_retry_after(headers):

    """
    尝试读取服务器返回的 Retry-After。

    支持：
        Retry-After: 20

    如果无法解析，返回 None。
    """

    if headers is None:
        return None

    value = headers.get(
        "Retry-After"
    )

    if value is None:
        return None

    value = str(value).strip()

    if not value:
        return None

    # 最常见：
    # Retry-After: 10
    try:

        seconds = float(value)

        if seconds < 0:
            return None

        return seconds

    except ValueError:
        return None


# ============================================================
# V6.1 BACKOFF CALCULATOR
# ============================================================

def calculate_429_backoff(retry_number):

    """
    指数退避：

    retry 1 -> 10s
    retry 2 -> 20s
    retry 3 -> 40s
    retry 4 -> 80s
    retry 5 -> 160s

    再加入 0~3 秒随机抖动。
    """

    base = (
        AI_429_BACKOFF_BASE
        * (2 ** (retry_number - 1))
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
# V6.1 UNIFIED AI CALL
# ============================================================

def call_ai(
    prompt,
    system_prompt=None,
    temperature=DEFAULT_TEMPERATURE
):
    """
    所有 AGNES AI 请求的统一入口。

    V6.1 增加：

    - 普通请求节流
    - 429 自动重试
    - Retry-After 支持
    - 指数退避
    - 随机抖动

    这样 Stage 1A / Stage 1B / Stage 2
    全部自动获得防429能力。
    """

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

    # ========================================================
    # 429 RETRY LOOP
    # ========================================================

    for attempt in range(
        0,
        AI_MAX_429_RETRIES + 1
    ):

        # ----------------------------------------------------
        # 普通请求节流
        # ----------------------------------------------------

        wait_for_ai_throttle()

        try:

            with urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as r:

                raw = r.read().decode(
                    "utf-8"
                )

            # ------------------------------------------------
            # 请求成功
            # ------------------------------------------------

            try:

                data = json.loads(raw)

            except Exception as e:

                raise RuntimeError(
                    "❌ AGNES.ai 返回不是合法JSON\n"
                    + raw[:3000]
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

        except HTTPError as e:

            body = ""

            try:
                body = e.read().decode(
                    "utf-8",
                    errors="replace"
                )
            except Exception:
                body = ""

            # =================================================
            # HTTP 429
            # =================================================

            if e.code == 429:

                # 已经没有重试机会
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
                            f"   Server Response:\n"
                            f"{body[:3000]}"
                        )

                    raise RuntimeError(
                        "❌ AGNES.ai HTTP 429："
                        "自动重试次数耗尽"
                    ) from e

                retry_number = attempt + 1

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

                    # 尽量把服务器返回内容
                    # 压缩到一行，避免日志爆炸
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

            # =================================================
            # 非429 HTTP错误
            # =================================================

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

    files = get_enriched_files(date)

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
        if x["metadata"]
        .get("title", "")
        .strip()
    ]

    if not items:

        raise RuntimeError(
            f"❌ {date} 没有有效新闻"
        )

    def score(x):

        try:

            return float(
                x["metadata"]
                .get(
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

        if not isinstance(c, dict):

            malformed.append(
                f"cluster[{pos}]不是对象"
            )

            continue

        ids = c.get(
            "article_indexes"
        )

        if not isinstance(ids, list):

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

    out = []

    for c in cs:

        if not isinstance(c, dict):

            out.append(c)
            continue

        d = dict(c)

        ids = d.get(
            "article_indexes",
            []
        )

        if isinstance(ids, list):

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
        for i, x in enumerate(items)
    )

    prompt = f"""你正在执行748686自生长知识系统V6第二层事件聚合。
日期：{date}

{joined}

任务：识别哪些新闻属于同一个现实世界事件。支持跨来源、跨语言。不要因为关键词、公司、行业、国家相同就强行合并。无法确定时宁可分开。

绝对覆盖：ARTICLE编号为 {json.dumps(expected)}。每篇必须且只能属于一个cluster；无法合并则单独成cluster；不得遗漏、重复或创造编号。

只输出JSON：
{{"clusters":[{{"cluster_id":"C001","article_indexes":[1],"event_title":"统一事件名称","event_reason":"事件判断"}}]}}"""

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

    if not isinstance(cs, list):

        raise RuntimeError(
            f"❌ {date} 第一轮聚类结果缺少clusters"
        )

    return normalize_clusters(cs)


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
        for i, x in enumerate(items)
    )

    prompt = f"""修复748686 V6 ARTICLE覆盖冲突。
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

重新判断全部文章。同事件合并，不同事件分开；每篇ARTICLE恰好一次；Missing=0 Duplicate=0 Extra=0。

只输出JSON：
{{"clusters":[{{"cluster_id":"C001","article_indexes":[1],"event_title":"事件","event_reason":"原因"}}]}}"""

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

    if not isinstance(cs, list):

        raise RuntimeError(
            "❌ 聚类修复结果缺少clusters"
        )

    return normalize_clusters(cs)


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

    if valid_issues(issues):

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

        if valid_issues(issues):

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
# GLOBAL CLUSTER VALIDATION
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
        f"Input Enriched News: {total}"
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

        for c in cs:

            allc.append(
                {
                    "cluster_id":
                        f"B{n:03d}-{c['cluster_id']}",

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
                        [
                            int(x)
                            for x
                            in c[
                                "article_indexes"
                            ]
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

    print(
        f"\n✅ Initial Clusters: "
        f"{len(allc)}"
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
# GLOBAL MERGE WINDOW
# ============================================================

def merge_cluster_window(
    date,
    window,
    round_no,
    window_no
):

    joined = "\n\n".join(
        f"""[CLUSTER {i}]
Cluster ID：{c['cluster_id']}
事件名称：{c.get('event_title', '未命名事件')}
事件判断：{c.get('event_reason', '')}
文章数量：{len(c.get('article_indexes', []))}
文章编号：{json.dumps(c.get('article_indexes', []))}"""
        for i, c
        in enumerate(
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

    prompt = f"""你正在执行748686自生长知识系统V6全局事件归并。

日期：{date}
轮次：{round_no}
窗口：{window_no}

{joined}

判断Cluster是否属于同一个具体现实世界事件，而不是同主题。

可以合并：
- 同一政策发布
- 同一公司重大动作
- 同一事故
- 同一产品发布
- 同一具体现实事件

不得合并：
- 同公司不同事件
- 同人物不同事件
- 同趋势不同具体事件
- 仅因为关键词相同的新闻

无法确认时宁可分开。

输入Cluster编号：
{json.dumps(expected)}

每个必须且只能进入一个group。
不得遗漏、重复、创造编号。

只输出JSON：
{{"groups":[{{"group_id":"G001","cluster_indexes":[1,4],"event_title":"统一事件名称","reason":"原因"}}]}}"""

    data = parse_ai_json(
        call_ai(
            prompt,
            "你是全球新闻事件归并专家。"
            "必须覆盖全部输入Cluster，每个恰好一次。",
            0
        ),
        f"{date} Global Merge "
        f"Round {round_no} "
        f"Window {window_no}"
    )

    groups = data.get(
        "groups"
    )

    if not isinstance(groups, list):

        raise RuntimeError(
            "❌ Global Merge缺少groups"
        )

    actual = []

    malformed = []

    for p, g in enumerate(
        groups,
        1
    ):

        if not isinstance(g, dict):

            malformed.append(
                f"group[{p}]不是对象"
            )

            continue

        ids = g.get(
            "cluster_indexes"
        )

        if (
            not isinstance(ids, list)
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
            "V6 Global Merge窗口覆盖异常。",
            {
                "duplicate": dup,
                "missing": miss,
                "extra": extra,
                "malformed": malformed,
                "groups": groups
            }
        )

        raise RuntimeError(
            "❌ Global Merge覆盖异常 "
            f"Duplicate={dup} "
            f"Missing={miss} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )

    return groups


# ============================================================
# BUILD WINDOW MERGED CLUSTERS
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

        ids = []

        for ci in g[
            "cluster_indexes"
        ]:

            ids.extend(
                window[
                    int(ci) - 1
                ][
                    "article_indexes"
                ]
            )

        out.append(
            {
                "cluster_id":
                    f"R{round_no:02d}"
                    f"W{window_no:03d}"
                    f"G{gp:03d}",

                "event_title":
                    g.get(
                        "event_title",
                        "未命名事件"
                    ),

                "event_reason":
                    g.get(
                        "reason",
                        ""
                    ),

                "article_indexes":
                    sorted(
                        set(
                            map(
                                int,
                                ids
                            )
                        )
                    )
            }
        )

    return out


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

        before = len(current)

        print(
            f"\nGLOBAL MERGE ROUND {rnd} "
            f"| Input Clusters: {before}"
        )

        if before == 1:
            break

        windows = build_merge_windows(
            current
        )

        print(
            f"Windows: {len(windows)} "
            f"| Size: "
            f"{GLOBAL_MERGE_WINDOW_SIZE} "
            f"| Overlap: "
            f"{GLOBAL_MERGE_OVERLAP}"
        )

        results = []

        for wi, w in enumerate(
            windows,
            1
        ):

            print(
                f"🔹 Window {wi}/"
                f"{len(windows)} "
                f"| size={len(w)}"
            )

            results.append(
                build_window_merged_clusters(
                    w,
                    merge_cluster_window(
                        date,
                        w,
                        rnd,
                        wi
                    ),
                    rnd,
                    wi
                )
            )

        dedup = {}

        for mw in results:

            for c in mw:

                sig = tuple(
                    sorted(
                        set(
                            c[
                                "article_indexes"
                            ]
                        )
                    )
                )

                if not sig:

                    raise RuntimeError(
                        "❌ V6 Global Merge"
                        "产生空Cluster"
                    )

                old = dedup.get(
                    sig
                )

                if (
                    old is None
                    or len(
                        c.get(
                            "event_reason",
                            ""
                        )
                    )
                    >
                    len(
                        old.get(
                            "event_reason",
                            ""
                        )
                    )
                ):

                    dedup[sig] = c

        merged = sorted(
            dedup.values(),
            key=lambda c:
                min(
                    c[
                        "article_indexes"
                    ]
                )
        )

        allidx = [
            i
            for c in merged
            for i in c[
                "article_indexes"
            ]
        ]

        if (
            len(allidx)
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
                f"❌ {date} Global Merge "
                f"Round {rnd} 覆盖异常"
            )

        after = len(merged)

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
                    "index": i,

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

def synthesize_event(event):

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

    prompt = f"""你正在执行748686自生长知识系统V6第二层事件知识综合。

日期：{event['date']}
事件ID：{event['event_id']}
事件名称：{event['event_title']}

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


def load_event_index(date):

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
        if isinstance(d, list)
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
        bool(b.strip())
        and m.get(
            "event_id"
        ) == event_id
        and m.get(
            "status"
        ) == "completed"
    )


def inspect_event_units(date):

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

        eid = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

        ids.append(eid)

        matches = list(
            target.glob(
                f"{eid}_*.md"
            )
        ) if eid else []

        if not matches:

            missing.append(eid)

        elif not any(
            event_unit_file_valid(
                p,
                eid
            )
            for p in matches
        ):

            invalid.append(eid)

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


# ============================================================
# EVENT UNIT COMPLETE MARKER
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

def run_stage_1(date):

    print(
        f"\n{'=' * 70}\n"
        f"STAGE 1 — EVENT UNIT "
        f"GENERATION V6.1: {date}\n"
        f"{'=' * 70}"
    )

    inspection = inspect_event_units(
        date
    )

    if inspection["complete"]:

        print(
            f"✅ {date} EventUnits已经完整，"
            "跳过AI聚合。"
        )

        return False

    news = load_all_enriched_news(
        date
    )

    if inspection["index"] is not None:

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
        f"✅ Event Index saved: {p}"
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

    prompt = f"""你正在执行748686自生长知识系统V6的27 Skills深度处理。

事件：
{event[0].get('event_title', '')}

Event ID：
{event[0].get('event_id', '')}

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

def run_stage_2(date):

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

    # ========================================================
    # Prefer configured route category.
    # Otherwise use all Skills.
    # ========================================================

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
        f"✅ STAGE 2 COMPLETE: {date}"
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    ap = argparse.ArgumentParser(
        description=
        "748686 Knowledge Pipeline V6.1"
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
            f"V6.1 FAILED: {e}",
            file=sys.stderr
        )

        return 1

    print(
        f"\n✅ Knowledge Pipeline "
        f"V6.1 finished: "
        f"{args.date} / "
        f"{args.stage}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
