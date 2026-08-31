#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统 - Knowledge Pipeline V6.5.2

Global Cluster Contract
=======================

AI:
    Local Cluster ID only:
        C001 / C002 / C003 / ...

Python Global Registry:
    EVT-YYYYMMDD-NNNNNN

正式 Global ID:
    EVT-YYYYMMDD-NNNNNN

禁止：
    EVT-YYYY-MM-DD-NNNNNN
    REC-...
    GM-...
    C001 作为 Global ID

核心原则：
1. AI 永远不生产 Global ID。
2. Global ID 只能由 Python Registry Producer 生成。
3. Registry 以 ARTICLE membership 为幂等键。
4. Resume / Recovery 不重复注册同一 ARTICLE membership。
5. Registry 与 Global Merge checkpoint 必须一致。
6. Validator 严格，不放宽格式。
7. Stage 1A AI阶段只验证 Local Cluster + ARTICLE coverage。
8. 注册完成后才进入 Global Cluster membership validation。
9. 保留原有 Recovery / Union-Find / Global Merge / EventUnit / Skills。
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


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

EVENT_UNITS_SUFFIX = "EventUnits"
EVENT_INDEX_FILE = "_event_index.json"
EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"
GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"
GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"


# ============================================================
# VERSION / GLOBAL ID CONTRACT
# ============================================================

PIPELINE_VERSION = "6.5.2"

GLOBAL_ID_PATTERN = re.compile(
    r"^EVT-\d{8}-\d{6}$"
)

LOCAL_CLUSTER_ID_PATTERN = re.compile(
    r"^C\d{3,}$"
)

GLOBAL_ID_PREFIX = "EVT"

RECOVERY_BATCH_SIZES = (30, 15, 8, 4, 2, 1)

AGGREGATION_BATCH_SIZE = 30

GLOBAL_MERGE_WINDOW_SIZE = 30
GLOBAL_MERGE_OVERLAP = 15


# ============================================================
# AI
# ============================================================

AGNES_BASE_URL = "https://api.agnes-ai.cn/v1"
AGNES_MODEL = "agnes-2.5-flash"
AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3
AI_TIMEOUT = 180

AI_REQUEST_THROTTLE_SECONDS = 1.5
AI_MAX_429_RETRIES = 5
AI_429_BACKOFF_BASE = 10
AI_429_BACKOFF_MAX = 180
AI_429_JITTER_MAX = 3

_LAST_AI_REQUEST_TIME = 0.0


MAX_ARTICLES_PER_EVENT_CONTEXT = 30
ARTICLE_CLUSTER_CONTENT_LIMIT = 3500
ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


# ============================================================
# BASIC UTILITIES
# ============================================================

def now():
    return datetime.now(BEIJING_TZ)


def compact_date(date: str) -> str:
    """
    2026-08-29 -> 20260829
    20260829  -> 20260829
    """
    value = str(date).strip().replace("-", "")
    if not re.fullmatch(r"\d{8}", value):
        raise RuntimeError(
            f"❌ 非法日期：{date}"
        )
    return value


def formal_global_id(date: str, sequence: int) -> str:
    """
    唯一 Global ID Producer 格式。

    EVT-YYYYMMDD-NNNNNN
    """
    d = compact_date(date)

    if sequence < 1:
        raise RuntimeError(
            f"❌ Global sequence非法：{sequence}"
        )

    if sequence > 999999:
        raise RuntimeError(
            f"❌ Global sequence超过六位：{sequence}"
        )

    return f"{GLOBAL_ID_PREFIX}-{d}-{sequence:06d}"


def validate_global_id(global_id: str):
    """
    严格 Global ID Validator。
    不允许任何旧格式。
    """
    value = str(global_id or "").strip()

    if not GLOBAL_ID_PATTERN.fullmatch(value):
        raise RuntimeError(
            f"❌ 非法Global Cluster ID：{value}"
        )

    return True


def validate_local_cluster_id(local_id: str):
    value = str(local_id or "").strip()

    if not LOCAL_CLUSTER_ID_PATTERN.fullmatch(value):
        raise RuntimeError(
            f"❌ 非法Local Cluster ID：{value}"
        )

    return True


def event_units_dir(date):
    return RAW_NEWS / f"{date}-{EVENT_UNITS_SUFFIX}"


def conflict_log_path(date):
    return LOGS / f"{date}_event_aggregation_conflicts.log"


def global_merge_checkpoint_path(date):
    return (
        event_units_dir(date)
        / GLOBAL_MERGE_CHECKPOINT_FILE
    )


def global_cluster_registry_path(date):
    return (
        event_units_dir(date)
        / GLOBAL_CLUSTER_REGISTRY_FILE
    )


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
        f.write("\n".join(lines))

    print(f"⚠️ {message}")
    print(
        f"   Conflict log: "
        f"{conflict_log_path(date)}"
    )


def read_json(path, default=None):
    if not path.exists():
        return {} if default is None else default

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


def write_json_atomic(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:
        payload = json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )

        tmp.write_text(
            payload,
            encoding="utf-8"
        )

        json.loads(
            tmp.read_text(
                encoding="utf-8"
            )
        )

        with tmp.open("rb") as f:
            os.fsync(f.fileno())

        tmp.replace(path)

    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass

        raise


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
    except Exception:
        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:
            candidate = text[start:end + 1]

            try:
                return json.loads(candidate)
            except Exception:
                pass

        raise RuntimeError(
            f"❌ AI JSON解析失败：{context}\n\n"
            f"{text[:5000]}"
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

    parts = content.split("---", 2)

    if len(parts) < 3:
        return {}, content

    data = {}

    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue

        k, v = line.split(":", 1)

        data[k.strip()] = (
            v.strip()
            .strip('"')
            .strip("'")
        )

    return data, parts[2].lstrip()


# ============================================================
# AI REQUEST
# ============================================================

def wait_for_ai_throttle():
    global _LAST_AI_REQUEST_TIME

    elapsed = (
        time.monotonic()
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


def parse_retry_after(headers):
    if headers is None:
        return None

    value = headers.get("Retry-After")

    if value is None:
        return None

    try:
        seconds = float(
            str(value).strip()
        )

        return (
            seconds
            if seconds >= 0
            else None
        )

    except ValueError:
        return None


def calculate_429_backoff(retry_number):
    base = min(
        AI_429_BACKOFF_BASE
        * (2 ** (retry_number - 1)),
        AI_429_BACKOFF_MAX
    )

    return min(
        base
        + random.uniform(
            0,
            AI_429_JITTER_MAX
        ),
        AI_429_BACKOFF_MAX
    )


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

    payload = json.dumps({
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
    }, ensure_ascii=False).encode()

    req = Request(
        AGNES_BASE_URL + "/chat/completions",
        data=payload,
        headers={
            "Authorization":
                f"Bearer {key}",
            "Content-Type":
                "application/json",
            "Accept":
                "application/json",
            "User-Agent":
                "748686-Knowledge-Pipeline/6.5.2"
        },
        method="POST"
    )

    for attempt in range(
        AI_MAX_429_RETRIES + 1
    ):
        wait_for_ai_throttle()

        try:
            with urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as r:
                raw = (
                    r.read()
                    .decode("utf-8")
                )

            try:
                data = json.loads(raw)
            except Exception as e:
                raise RuntimeError(
                    "❌ AGNES.ai 返回不是合法JSON\n"
                    + raw[:3000]
                ) from e

            try:
                result = (
                    data["choices"][0]
                    ["message"]["content"]
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

            return str(result).strip()

        except HTTPError as e:
            body = ""

            try:
                body = (
                    e.read()
                    .decode(
                        "utf-8",
                        errors="replace"
                    )
                )
            except Exception:
                pass

            if e.code == 429:
                if attempt >= AI_MAX_429_RETRIES:
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
                    source = "Retry-After"
                else:
                    wait_seconds = (
                        calculate_429_backoff(
                            retry_number
                        )
                    )
                    source = "指数退避"

                print(
                    f"⚠️ AGNES.ai HTTP 429 — "
                    f"Retry {retry_number}/"
                    f"{AI_MAX_429_RETRIES}, "
                    f"Wait {wait_seconds:.1f}s, "
                    f"Source={source}"
                )

                if body:
                    print(
                        "   Response:",
                        re.sub(
                            r"\s+",
                            " ",
                            body
                        ).strip()[:1000]
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


# ============================================================
# NEWS
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
        x for x in items
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
# LOCAL CLUSTER VALIDATION
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

        # 修改这里：优先取 local_cluster_id，再取 cluster_id
        local_id = (
            c.get("local_cluster_id")
            or c.get("cluster_id")
        )

        try:
            validate_local_cluster_id(
                local_id
            )
        except Exception as e:
            malformed.append(
                f"cluster[{pos}]Local ID异常：{e}"
            )

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
                    f"cluster[{pos}]非法ARTICLE ID：{v}"
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
        "missing":
            sorted(
                expected - actual
            ),
        "extra":
            sorted(
                actual - expected
            ),
        "malformed": malformed
    }


def valid_issues(issues):
    return not any([
        issues["duplicate"],
        issues["missing"],
        issues["extra"],
        issues["malformed"]
    ])


def normalize_clusters(clusters):
    out = []

    for c in clusters:
        if not isinstance(c, dict):
            out.append(c)
            continue

        d = dict(c)

        local_id = (
            d.get("local_cluster_id")
            or d.get("cluster_id")
            or ""
        )

        d["local_cluster_id"] = (
            str(local_id).strip()
        )

        d["cluster_id"] = (
            d["local_cluster_id"]
        )

        ids = d.get(
            "article_indexes",
            []
        )

        if isinstance(ids, list):
            normalized = []

            for x in ids:
                try:
                    normalized.append(
                        int(x)
                    )
                except Exception:
                    normalized.append(x)

            d["article_indexes"] = (
                normalized
            )

        out.append(d)

    return out


# ============================================================
# AI LOCAL CLUSTER
# ============================================================

def cluster_news_batch(
    date,
    items,
    indexes
):
    expected = [
        int(x)
        for x in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[i]
        )
        for i, item in enumerate(items)
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.2第一层事件聚类。
日期：{date}

{joined}

任务：
识别哪些新闻属于同一个现实世界的具体事件。

支持跨来源、跨语言。

不要因为关键词、公司、行业、国家相同就强行合并。
无法确定时宁可分开。

绝对覆盖ARTICLE编号：
{json.dumps(expected)}

每篇必须且只能属于一个cluster。
无法与其他文章合并的文章必须单独成为cluster。

最重要的ID规则：
- 你只能生成Local Cluster ID。
- Local Cluster ID只能是C001、C002、C003……
- 严禁生成EVT-...
- 严禁生成REC-...
- 严禁生成GM-...
- 不得把Local Cluster ID当作Global ID。
- Global ID完全由Python Registry生成。

只输出JSON。
不要Markdown。
不要解释。
不要复制正文。

格式：
{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "统一事件名称",
      "event_reason": "一句话判断"
    }}
  ]
}}"""

    try:
        result = call_ai(
            prompt,
            (
                "你是全球新闻事件聚类专家。"
                "每篇ARTICLE必须且只能属于一个cluster。"
                "只能产生C001/C002形式Local Cluster ID。"
                "绝不产生Global ID。"
                "只输出合法JSON。"
            ),
            0
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类"
        )

    except RuntimeError as first_error:
        compact_prompt = f"""748686 V6.5.2 新闻事件聚类JSON修复。

日期：{date}
ARTICLE范围：{json.dumps(expected)}

文章：
{joined}

重新聚类。

严格要求：
1. 每个ARTICLE恰好一次；
2. 同一具体现实事件合并；
3. 不同事件分开；
4. 不能确定宁可分开；
5. cluster_id只能是C001/C002/C003；
6. 严禁EVT-/REC-/GM-；
7. 每个cluster只返回cluster_id、article_indexes、event_title、event_reason；
8. 不输出正文；
9. 只输出JSON。

格式：
{{
  "clusters": [
    {{
      "cluster_id": "C001",
      "article_indexes": [1],
      "event_title": "事件",
      "event_reason": "判断"
    }}
  ]
}}"""

        print(
            "   ⚠️ 第一轮聚类JSON解析失败，"
            "启动同批次紧凑JSON重试："
            f"{first_error}"
        )

        result = call_ai(
            compact_prompt,
            (
                "你是新闻聚类JSON修复器。"
                "只输出合法JSON。"
                "Local ID只能使用C001/C002形式。"
            ),
            0
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类紧凑重试"
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

    return normalize_clusters(
        clusters
    )


def repair_cluster_news_batch(
    date,
    items,
    indexes,
    broken,
    issues,
    attempt
):
    expected = [
        int(x)
        for x in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[i]
        )
        for i, item in enumerate(items)
    )

    prompt = f"""修复748686 V6.5.2 ARTICLE覆盖冲突。

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
1. cluster_id只能是Local Cluster ID；
2. Local Cluster ID只能是C001/C002/C003……；
3. 不得生成EVT-/REC-/GM-；
4. 同事件合并；
5. 不同事件分开；
6. 每篇ARTICLE恰好一次；
7. Missing=0；
8. Duplicate=0；
9. Extra=0；
10. 不得遗漏ARTICLE；
11. 只输出JSON。

只输出：
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
            (
                "你是新闻事件聚类冲突修复专家。"
                "必须完整覆盖输入ARTICLE。"
                "只产生Local Cluster ID。"
            ),
            0
        ),
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
            "❌ 聚类修复结果缺少clusters"
        )

    return normalize_clusters(
        clusters
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
            "Local Cluster ARTICLE覆盖验证失败。",
            issues
        )

    raise RuntimeError(
        f"❌ {context} 聚类覆盖失败：{issues}"
    )


def _safe_covered_indexes(
    clusters,
    expected_indexes
):
    issues = inspect_cluster_assignment(
        clusters,
        expected_indexes
    )

    if (
        issues["duplicate"]
        or issues["extra"]
        or issues["malformed"]
    ):
        return []

    expected = {
        int(x)
        for x in expected_indexes
    }

    actual = set()

    for cluster in clusters:
        for value in cluster.get(
            "article_indexes",
            []
        ):
            actual.add(
                int(value)
            )

    return sorted(
        actual & expected
    )


# ============================================================
# GLOBAL CLUSTER REGISTRY
# ============================================================

def create_global_cluster_registry(date):
    """
    Registry 是持久化 Global ID Ledger。

    注意：
    Registry 的 sequence 绝不因为 Recovery
    或 Stage 1 resume 而重置。
    """
    return {
        "version": PIPELINE_VERSION,
        "date": str(date),
        "date_compact": compact_date(date),
        "next_sequence": 1,
        "registered": []
    }


def normalize_registry(registry, date):
    if not isinstance(
        registry,
        dict
    ):
        raise RuntimeError(
            "❌ Global Registry格式异常"
        )

    if registry.get(
        "version"
    ) != PIPELINE_VERSION:
        raise RuntimeError(
            "❌ Global Registry版本异常"
        )

    if str(
        registry.get("date")
    ) != str(date):
        raise RuntimeError(
            "❌ Global Registry日期不一致"
        )

    if (
        registry.get("date_compact")
        != compact_date(date)
    ):
        raise RuntimeError(
            "❌ Global Registry日期compact值异常"
        )

    try:
        next_sequence = int(
            registry.get(
                "next_sequence",
                1
            )
        )
    except Exception as e:
        raise RuntimeError(
            "❌ Global Registry next_sequence非法"
        ) from e

    if next_sequence < 1:
        raise RuntimeError(
            "❌ Global Registry next_sequence必须>=1"
        )

    registered = registry.get(
        "registered",
        []
    )

    if not isinstance(
        registered,
        list
    ):
        raise RuntimeError(
            "❌ Global Registry registered不是数组"
        )

    normalized = []

    seen_global = set()
    seen_membership = set()

    for item in registered:
        if not isinstance(
            item,
            dict
        ):
            raise RuntimeError(
                "❌ Global Registry存在非法记录"
            )

        gid = str(
            item.get(
                "global_cluster_id",
                ""
            )
        ).strip()

        validate_global_id(gid)

        local_id = str(
            item.get(
                "local_cluster_id",
                ""
            )
        ).strip()

        validate_local_cluster_id(
            local_id
        )

        articles = item.get(
            "article_indexes",
            []
        )

        if not isinstance(
            articles,
            list
        ) or not articles:
            raise RuntimeError(
                f"❌ Registry {gid} article_indexes非法"
            )

        membership = tuple(
            sorted(
                set(
                    int(x)
                    for x in articles
                )
            )
        )

        if not membership:
            raise RuntimeError(
                f"❌ Registry {gid} membership为空"
            )

        if gid in seen_global:
            raise RuntimeError(
                f"❌ Registry重复Global ID：{gid}"
            )

        if membership in seen_membership:
            raise RuntimeError(
                "❌ Registry重复ARTICLE membership："
                f"{membership}"
            )

        seen_global.add(gid)
        seen_membership.add(
            membership
        )

        normalized.append({
            "global_cluster_id": gid,
            "local_cluster_id": local_id,
            "source": str(
                item.get(
                    "source",
                    ""
                )
            ),
            "article_indexes": list(
                membership
            )
        })

    registry["next_sequence"] = (
        next_sequence
    )

    registry["registered"] = (
        normalized
    )

    return registry


def persist_global_cluster_registry(
    date,
    registry
):
    registry = normalize_registry(
        registry,
        date
    )

    write_json_atomic(
        global_cluster_registry_path(date),
        {
            "version":
                PIPELINE_VERSION,
            "date":
                registry["date"],
            "date_compact":
                registry["date_compact"],
            "next_sequence":
                int(
                    registry[
                        "next_sequence"
                    ]
                ),
            "registered":
                registry["registered"],
            "saved_at":
                now().isoformat()
        }
    )


def load_global_cluster_registry(
    date,
    create_if_missing=True
):
    path = global_cluster_registry_path(
        date
    )

    if not path.exists():
        if not create_if_missing:
            return None

        registry = (
            create_global_cluster_registry(
                date
            )
        )

        persist_global_cluster_registry(
            date,
            registry
        )

        return registry

    registry = read_json(
        path,
        None
    )

    if registry is None:
        raise RuntimeError(
            "❌ Global Registry读取失败"
        )

    return normalize_registry(
        registry,
        date
    )


def _registry_membership_key(
    article_indexes
):
    return tuple(
        sorted(
            set(
                int(x)
                for x in article_indexes
            )
        )
    )


def registry_find_by_membership(
    registry,
    article_indexes
):
    key = _registry_membership_key(
        article_indexes
    )

    for record in registry[
        "registered"
    ]:
        if (
            _registry_membership_key(
                record["article_indexes"]
            )
            == key
        ):
            return record

    return None


def registry_find_by_global_id(
    registry,
    global_id
):
    validate_global_id(
        global_id
    )

    for record in registry[
        "registered"
    ]:
        if (
            record[
                "global_cluster_id"
            ]
            == global_id
        ):
            return record

    return None


def register_global_cluster_ids(
    date,
    clusters,
    registry,
    source
):
    """
    唯一 Global ID Producer。

    幂等规则：
        同一 ARTICLE membership
        => 永远复用同一 Global ID。

    因此：
        Recovery
        Resume
        重跑
        checkpoint恢复

    都不会重复注册同一Global ID。
    """

    registry = normalize_registry(
        registry,
        date
    )

    out = []

    for c in clusters:
        d = dict(c)

        local_id = str(
            d.get(
                "local_cluster_id"
            )
            or d.get(
                "cluster_id"
            )
            or ""
        ).strip()

        validate_local_cluster_id(
            local_id
        )

        article_indexes = sorted(
            set(
                int(x)
                for x in d.get(
                    "article_indexes",
                    []
                )
            )
        )

        if not article_indexes:
            raise RuntimeError(
                "❌ Global Registry收到空ARTICLE membership"
            )

        existing = (
            registry_find_by_membership(
                registry,
                article_indexes
            )
        )

        if existing:
            global_id = existing[
                "global_cluster_id"
            ]

            validate_global_id(
                global_id
            )

            print(
                f"   ♻️ Registry复用Global ID："
                f"{global_id} | "
                f"ARTICLE={article_indexes}"
            )

        else:
            sequence = int(
                registry[
                    "next_sequence"
                ]
            )

            global_id = formal_global_id(
                date,
                sequence
            )

            validate_global_id(
                global_id
            )

            registry[
                "next_sequence"
            ] = sequence + 1

            registry[
                "registered"
            ].append({
                "global_cluster_id":
                    global_id,
                "local_cluster_id":
                    local_id,
                "source":
                    source,
                "article_indexes":
                    article_indexes
            })

            print(
                f"   🆕 Registry注册Global ID："
                f"{global_id} | "
                f"ARTICLE={article_indexes}"
            )

        d["local_cluster_id"] = local_id
        d["cluster_id"] = global_id
        d["member_cluster_ids"] = [
            global_id
        ]
        d["global_id_source"] = (
            "python_global_registry"
        )
        d["global_registry_source"] = (
            source
        )

        out.append(d)

        # 每个ID立即落盘。
        # 防止AI后续失败导致已经注册的ID丢失。
        persist_global_cluster_registry(
            date,
            registry
        )

    return out


def validate_registry_against_clusters(
    date,
    registry,
    clusters,
    context
):
    registry = normalize_registry(
        registry,
        date
    )

    registry_by_id = {
        r["global_cluster_id"]: r
        for r in registry[
            "registered"
        ]
    }

    seen_membership = set()

    for pos, c in enumerate(
        clusters,
        1
    ):
        if not isinstance(c, dict):
            raise RuntimeError(
                f"❌ {context} cluster[{pos}]不是对象"
            )

        gid = str(
            c.get(
                "cluster_id",
                ""
            )
        ).strip()

        validate_global_id(
            gid
        )

        if gid not in registry_by_id:
            raise RuntimeError(
                f"❌ {context} Global ID不在Registry："
                f"{gid}"
            )

        membership = (
            _registry_membership_key(
                c.get(
                    "article_indexes",
                    []
                )
            )
        )

        if not membership:
            raise RuntimeError(
                f"❌ {context} {gid} membership为空"
            )

        registry_membership = (
            _registry_membership_key(
                registry_by_id[gid][
                    "article_indexes"
                ]
            )
        )

        if membership != registry_membership:
            raise RuntimeError(
                f"❌ {context} Registry membership不一致："
                f"{gid} "
                f"checkpoint={membership} "
                f"registry={registry_membership}"
            )

        if membership in seen_membership:
            raise RuntimeError(
                f"❌ {context}存在重复membership："
                f"{membership}"
            )

        seen_membership.add(
            membership
        )


def validate_global_cluster_membership(
    date,
    clusters,
    context,
    expected_original_ids=None,
    registry=None
):
    """
    严格 Global Cluster membership Validator。

    Global ID：
        EVT-YYYYMMDD-NNNNNN

    member_cluster_ids：
        必须也是正式Global ID。

    不接受：
        C001
        EVT-YYYY-MM-DD-000001
        REC-...
        GM-...
    """

    seen_current = set()
    seen_original = set()

    malformed = []
    duplicate_current = []
    duplicate_original = []

    for pos, c in enumerate(
        clusters,
        1
    ):
        if not isinstance(c, dict):
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

        try:
            validate_global_id(cid)
        except Exception:
            malformed.append(
                f"cluster[{pos}]非法Global cluster_id：{cid}"
            )

        if cid in seen_current:
            duplicate_current.append(
                cid
            )
        else:
            seen_current.add(cid)

        members = c.get(
            "member_cluster_ids"
        )

        if (
            not isinstance(
                members,
                list
            )
            or not members
        ):
            malformed.append(
                f"cluster[{pos}]"
                "member_cluster_ids无效"
            )
            continue

        for member in members:
            member = str(
                member
            ).strip()

            try:
                validate_global_id(
                    member
                )
            except Exception:
                malformed.append(
                    f"cluster[{pos}]非法member_cluster_id："
                    f"{member}"
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

    missing_original = []
    extra_original = []

    if expected_original_ids is not None:
        expected = {
            str(x).strip()
            for x in expected_original_ids
        }

        for x in expected:
            try:
                validate_global_id(x)
            except Exception:
                raise RuntimeError(
                    f"❌ expected_original_ids包含非法Global ID：{x}"
                )

        missing_original = sorted(
            expected - seen_original
        )

        extra_original = sorted(
            seen_original - expected
        )

    if (
        malformed
        or duplicate_current
        or duplicate_original
        or missing_original
        or extra_original
    ):
        log_conflict(
            date,
            context,
            "Global Cluster membership验证失败。",
            {
                "malformed":
                    malformed,
                "duplicate_current":
                    duplicate_current,
                "duplicate_original":
                    duplicate_original,
                "missing_original":
                    missing_original,
                "extra_original":
                    extra_original
            }
        )

        raise RuntimeError(
            f"❌ {context} Global Cluster membership异常："
            f"Malformed={malformed} "
            f"DuplicateCurrent={duplicate_current} "
            f"DuplicateOriginal={duplicate_original} "
            f"MissingOriginal={missing_original} "
            f"ExtraOriginal={extra_original}"
        )

    if registry is not None:
        validate_registry_against_clusters(
            date,
            registry,
            clusters,
            context
        )


# ============================================================
# LOCAL CLUSTER RECORD
# ============================================================

def _make_cluster_records(
    batch_identifier,
    clusters
):
    out = []

    for c in clusters:
        indexes = sorted(
            set(
                int(x)
                for x in c.get(
                    "article_indexes",
                    []
                )
            )
        )

        if not indexes:
            continue

        local_id = str(
            c.get(
                "local_cluster_id"
            )
            or c.get(
                "cluster_id"
            )
            or ""
        ).strip()

        validate_local_cluster_id(
            local_id
        )

        out.append({
            "cluster_id":
                local_id,
            "local_cluster_id":
                local_id,
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
                indexes,
            "batch_identifier":
                batch_identifier
        })

    return out


# ============================================================
# RECOVERY
# ============================================================

def cluster_news_batch_with_repair(
    date,
    items,
    indexes,
    batch_label
):
    expected = [
        int(x)
        for x in indexes
    ]

    clusters = None

    try:
        clusters = cluster_news_batch(
            date,
            items,
            expected
        )

        issues = inspect_cluster_assignment(
            clusters,
            expected
        )

        if valid_issues(issues):
            return (
                "complete",
                clusters,
                []
            )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            "AI第一次聚类返回非法ARTICLE归属，"
            "启动自动修复。",
            {
                "issues":
                    issues,
                "clusters":
                    clusters
            }
        )

        for attempt in range(
            1,
            CLUSTER_REPAIR_ATTEMPTS + 1
        ):
            try:
                clusters = (
                    repair_cluster_news_batch(
                        date,
                        items,
                        expected,
                        clusters,
                        issues,
                        attempt
                    )
                )

                issues = inspect_cluster_assignment(
                    clusters,
                    expected
                )

                if valid_issues(issues):
                    print(
                        "   ✅ Cluster conflict "
                        "repaired successfully."
                    )

                    return (
                        "complete",
                        clusters,
                        []
                    )

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    f"第{attempt}次聚类冲突修复仍然失败。",
                    {
                        "issues":
                            issues,
                        "clusters":
                            clusters
                    }
                )

            except Exception as repair_error:
                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    f"第{attempt}次聚类修复失败。",
                    str(repair_error)
                )

        final_issues = (
            inspect_cluster_assignment(
                clusters or [],
                expected
            )
        )

        # Missing-only
        if (
            final_issues["missing"]
            and not final_issues["duplicate"]
            and not final_issues["extra"]
            and not final_issues["malformed"]
        ):
            safe = _safe_covered_indexes(
                clusters,
                expected
            )

            unresolved = sorted(
                set(expected)
                - set(safe)
            )

            if safe and unresolved:
                return (
                    "partial",
                    clusters,
                    unresolved
                )

        # Duplicate / Extra / Malformed
        return (
            "failed",
            [],
            expected
        )

    except Exception as e:
        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            "本批AI异常；整批隔离进入Recovery Queue。",
            str(e)
        )

        return (
            "failed",
            [],
            expected
        )


def _recovery_pass(
    date,
    news,
    indexes,
    recovery_pass_no,
    batch_size
):
    indexes = sorted(
        set(
            int(x)
            for x in indexes
        )
    )

    sub_batches = [
        indexes[i:i + batch_size]
        for i in range(
            0,
            len(indexes),
            batch_size
        )
    ]

    recovered = []
    pending = []

    print(
        f"\n🛠️ RECOVERY PASS "
        f"{recovery_pass_no} | "
        f"Articles={len(indexes)} | "
        f"BatchSize={batch_size}"
    )

    for sub_no, sub_indexes in enumerate(
        sub_batches,
        1
    ):
        items = [
            news[index - 1]
            for index in sub_indexes
        ]

        label = (
            f"RECOVERY {recovery_pass_no} / "
            f"BATCH {sub_no}"
        )

        if len(sub_indexes) == 1:
            index = sub_indexes[0]

            title = (
                news[index - 1]["metadata"]
                .get(
                    "title",
                    "未命名事件"
                )
                .strip()
            )

            recovered.append({
                "cluster_id":
                    f"C{index:03d}",
                "local_cluster_id":
                    f"C{index:03d}",
                "article_indexes":
                    [index],
                "event_title":
                    title[:120]
                    if title
                    else "未命名事件",
                "event_reason":
                    "该文章在恢复阶段作为独立事件单元保留。"
            })

            print(
                f"      🟢 Singleton安全保留："
                f"ARTICLE {index}"
            )

            continue

        status, clusters, unresolved = (
            cluster_news_batch_with_repair(
                date,
                items,
                sub_indexes,
                label
            )
        )

        if status == "complete":
            recovered.extend(
                clusters
            )

        elif status == "partial":
            safe = _safe_covered_indexes(
                clusters,
                sub_indexes
            )

            safe_set = set(safe)
            safe_clusters = []

            for cluster in clusters:
                ids = []

                for x in cluster.get(
                    "article_indexes",
                    []
                ):
                    i = int(x)

                    if i in safe_set:
                        ids.append(i)

                if ids:
                    item = dict(cluster)
                    item[
                        "article_indexes"
                    ] = sorted(
                        set(ids)
                    )

                    safe_clusters.append(
                        item
                    )

            if safe_clusters:
                validate_cluster_coverage(
                    safe_clusters,
                    safe,
                    f"{date} {label} SAFE PART",
                    date
                )

                recovered.extend(
                    safe_clusters
                )

            pending.extend(
                unresolved
            )

        else:
            pending.extend(
                sub_indexes
            )

    return (
        recovered,
        sorted(
            set(pending)
        )
    )


# ============================================================
# STAGE 1A INITIAL
# ============================================================

def build_initial_clusters(
    date,
    news
):
    allc = []
    total = len(news)

    registry = (
        load_global_cluster_registry(
            date,
            create_if_missing=True
        )
    )

    print("\n" + "=" * 70)
    print(
        "STAGE 1A — AI EVENT CLUSTERING "
        "V6.5.2"
    )
    print("=" * 70)
    print(
        f"Input Enriched News: {total}"
    )
    print(
        f"Normal Batch Size: "
        f"{AGGREGATION_BATCH_SIZE}"
    )
    print(
        "Global ID: "
        "EVT-YYYYMMDD-NNNNNN"
    )
    print(
        "AI ID: "
        "C001/C002/C003..."
    )

    pending = []

    normal_batch_no = 0

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE
    ):
        normal_batch_no += 1

        end = min(
            start + AGGREGATION_BATCH_SIZE,
            total
        )

        indexes = list(
            range(
                start + 1,
                end + 1
            )
        )

        items = news[start:end]

        print(
            f"\n🔹 Cluster Batch "
            f"{normal_batch_no}: "
            f"{indexes[0]}-{indexes[-1]}/{total}"
        )

        status, clusters, unresolved = (
            cluster_news_batch_with_repair(
                date,
                items,
                indexes,
                f"CLUSTER BATCH {normal_batch_no}"
            )
        )

        if status == "complete":
            validate_cluster_coverage(
                clusters,
                indexes,
                f"Stage 1A Local Batch "
                f"{normal_batch_no}",
                date
            )

            local_records = (
                _make_cluster_records(
                    normal_batch_no,
                    clusters
                )
            )

            registered = (
                register_global_cluster_ids(
                    date,
                    local_records,
                    registry,
                    f"Batch {normal_batch_no}"
                )
            )

            allc.extend(
                registered
            )

        elif status == "partial":
            safe = _safe_covered_indexes(
                clusters,
                indexes
            )

            safe_set = set(safe)
            safe_clusters = []

            for cluster in clusters:
                ids = [
                    int(x)
                    for x in cluster.get(
                        "article_indexes",
                        []
                    )
                    if int(x) in safe_set
                ]

                if ids:
                    item = dict(cluster)
                    item[
                        "article_indexes"
                    ] = sorted(
                        set(ids)
                    )

                    safe_clusters.append(
                        item
                    )

            if safe_clusters:
                local_records = (
                    _make_cluster_records(
                        normal_batch_no,
                        safe_clusters
                    )
                )

                registered = (
                    register_global_cluster_ids(
                        date,
                        local_records,
                        registry,
                        (
                            f"Batch "
                            f"{normal_batch_no} "
                            f"SAFE PART"
                        )
                    )
                )

                allc.extend(
                    registered
                )

            pending.extend(
                unresolved
            )

        else:
            pending.extend(
                unresolved
            )

    # Recovery
    for pass_no, batch_size in enumerate(
        RECOVERY_BATCH_SIZES,
        1
    ):
        if not pending:
            break

        current_pending = sorted(
            set(pending)
        )

        pending = []

        recovered, unresolved = (
            _recovery_pass(
                date,
                news,
                current_pending,
                pass_no,
                batch_size
            )
        )

        local_records = (
            _make_cluster_records(
                f"RECOVERY PASS {pass_no}",
                recovered
            )
        )

        registered = (
            register_global_cluster_ids(
                date,
                local_records,
                registry,
                f"Recovery Pass {pass_no}"
            )
        )

        allc.extend(
            registered
        )

        pending.extend(
            unresolved
        )

    if pending:
        raise RuntimeError(
            "❌ Stage 1A最终仍有未处理ARTICLE："
            f"{sorted(set(pending))}"
        )

    # ========================================================
    # Stage 1A final validation
    # ========================================================

    validate_cluster_coverage(
        allc,
        range(1, total + 1),
        f"{date} Stage 1A GLOBAL ARTICLE",
        date
    )

    original_ids = [
        c["cluster_id"]
        for c in allc
    ]

    # 这里才进入 Global membership validator。
    validate_global_cluster_membership(
        date,
        allc,
        "STAGE 1A INITIAL",
        original_ids,
        registry
    )

    print(
        f"\n✅ Initial Global Clusters: "
        f"{len(allc)}"
    )

    print(
        f"✅ ARTICLE Coverage: "
        f"{total}/{total}"
    )

    print(
        f"✅ Registry next_sequence: "
        f"{registry['next_sequence']}"
    )

    return allc


# ============================================================
# GLOBAL MERGE
# ============================================================

def build_merge_windows(clusters):
    if len(clusters) <= GLOBAL_MERGE_WINDOW_SIZE:
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


def merge_cluster_window(
    date,
    window,
    round_no,
    window_no
):
    blocks = []

    for i, c in enumerate(
        window,
        1
    ):
        blocks.append(
            f"""[CLUSTER {i}]
Global Cluster ID：
{c['cluster_id']}
原始Global成员：
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

    expected = list(
        range(
            1,
            len(window) + 1
        )
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.2全局事件归并。

日期：{date}
轮次：{round_no}
窗口：{window_no}

{chr(10).join(blocks)}

判断这些Global Cluster是否属于同一个具体现实世界事件。

可以合并：
同一政策发布、同一公司重大动作、同一事故、
同一产品发布、同一具体现实事件、
同一正在持续发展的单一现实事件。

不得合并：
同公司不同事件、同人物不同事件、
同国家不同事件、同产业不同事件、
同趋势不同具体事件、仅关键词相同、
仅主题相同。

无法确认时宁可分开。

要求：
1. 每个输入Cluster必须且只能进入一个group。
2. 不得遗漏、重复、创造Cluster编号。
3. 一个group可以只有一个Cluster。
4. Cluster ID是Python已经注册的Global ID。
5. Global ID必须原样引用。
6. 不得修改Global ID。
7. 不得生成REC-/GM-。
8. 不得生成新的EVT-。
9. 不需要返回文章编号。

输入Cluster编号：
{json.dumps(expected)}

只输出JSON：
{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1, 4],
      "event_title": "统一事件名称",
      "reason": "为什么属于同一现实世界事件"
    }}
  ]
}}"""

    data = parse_ai_json(
        call_ai(
            prompt,
            (
                "你是全球新闻事件归并专家。"
                "必须覆盖全部输入Cluster。"
                "Global Cluster ID只能原样引用。"
                "不得生成任何新Global ID。"
            ),
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

        if not isinstance(
            ids,
            list
        ) or not ids:
            malformed.append(
                f"group[{p}]cluster_indexes无效"
            )
            continue

        for x in ids:
            try:
                actual.append(
                    int(x)
                )
            except Exception:
                malformed.append(
                    f"group[{p}]非法编号：{x}"
                )

    dup = sorted({
        x
        for x in actual
        if actual.count(x) > 1
    })

    miss = sorted(
        set(expected)
        - set(actual)
    )

    extra = sorted(
        set(actual)
        - set(expected)
    )

    if dup or miss or extra or malformed:
        raise RuntimeError(
            f"❌ Global Merge窗口AI输出异常 "
            f"Duplicate={dup} "
            f"Missing={miss} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )

    return groups


# ============================================================
# UNION FIND
# ============================================================

class UnionFind:

    def __init__(self, values):
        values = [
            str(x)
            for x in values
        ]

        self.parent = {
            v: v
            for v in values
        }

        self.rank = {
            v: 0
            for v in values
        }

    def find(self, value):
        value = str(value)

        if value not in self.parent:
            raise KeyError(value)

        p = self.parent[value]

        if p != value:
            self.parent[value] = (
                self.find(p)
            )

        return self.parent[value]

    def union(self, a, b):
        a = str(a)
        b = str(b)

        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return False

        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra

        self.parent[rb] = ra

        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1

        return True

    def components(self):
        result = {}

        for value in self.parent:
            root = self.find(value)

            result.setdefault(
                root,
                []
            ).append(value)

        return result

    def to_checkpoint(self):
        for v in list(
            self.parent
        ):
            self.find(v)

        return {
            "parent":
                dict(self.parent),
            "rank":
                dict(self.rank)
        }

    @classmethod
    def from_checkpoint(
        cls,
        values,
        data
    ):
        uf = cls(values)

        if not isinstance(
            data,
            dict
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint格式异常"
            )

        parent = data.get(
            "parent"
        )

        rank = data.get(
            "rank"
        )

        if (
            not isinstance(parent, dict)
            or not isinstance(rank, dict)
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint缺少parent/rank"
            )

        expected = {
            str(x)
            for x in values
        }

        if (
            set(map(str, parent))
            != expected
            or
            set(map(str, rank))
            != expected
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint Universe不一致"
            )

        uf.parent = {
            str(k): str(v)
            for k, v in parent.items()
        }

        uf.rank = {
            str(k): int(v)
            for k, v in rank.items()
        }

        for k, v in uf.parent.items():
            if v not in uf.parent:
                raise RuntimeError(
                    "❌ Union-Find checkpoint"
                    f"存在非法parent：{k}->{v}"
                )

        if any(
            v < 0
            for v in uf.rank.values()
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint存在非法rank"
            )

        return uf


def apply_window_groups(
    uf,
    window,
    groups,
    round_no,
    window_no
):
    records = []

    for gp, g in enumerate(
        groups,
        1
    ):
        indexes = [
            int(x)
            for x in g[
                "cluster_indexes"
            ]
        ]

        ids = [
            window[i - 1][
                "cluster_id"
            ]
            for i in indexes
        ]

        for gid in ids:
            validate_global_id(gid)

        anchor = ids[0]
        merged = False

        for cid in ids[1:]:
            if uf.union(
                anchor,
                cid
            ):
                merged = True

        records.append({
            "group_id":
                g.get(
                    "group_id",
                    f"G{gp:03d}"
                ),
            "cluster_ids":
                ids,
            "event_title":
                str(
                    g.get(
                        "event_title",
                        "未命名事件"
                    )
                ).strip(),
            "reason":
                str(
                    g.get(
                        "reason",
                        ""
                    )
                ).strip(),
            "merged":
                merged,
            "round":
                round_no,
            "window":
                window_no
        })

    return records


def _metadata_record_valid(r):
    return bool(
        str(
            r.get(
                "event_title",
                ""
            )
        ).strip()
        or
        str(
            r.get(
                "reason",
                ""
            )
        ).strip()
    )


def merge_metadata_histories(
    history,
    records,
    uf
):
    if not isinstance(
        history,
        dict
    ):
        history = {}

    for r in records:
        ids = [
            str(x)
            for x in r.get(
                "cluster_ids",
                []
            )
        ]

        if not ids:
            continue

        root = uf.find(
            ids[0]
        )

        item = {
            "cluster_ids":
                ids,
            "event_title":
                r.get(
                    "event_title",
                    ""
                ),
            "reason":
                r.get(
                    "reason",
                    ""
                ),
            "merged":
                bool(
                    r.get(
                        "merged"
                    )
                ),
            "round":
                int(
                    r.get(
                        "round",
                        0
                    )
                ),
            "window":
                int(
                    r.get(
                        "window",
                        0
                    )
                )
        }

        history.setdefault(
            root,
            []
        ).append(item)

    merged = {}

    for _, entries in history.items():
        if not entries:
            continue

        ids = (
            entries[-1]
            .get(
                "cluster_ids"
            )
            or []
        )

        if not ids:
            continue

        try:
            root = uf.find(
                ids[0]
            )
        except KeyError:
            continue

        merged.setdefault(
            root,
            []
        ).extend(entries)

    return merged


def choose_component_metadata(
    member_ids,
    by_id,
    history,
    uf
):
    old_titles = []
    old_reasons = []

    for cid in member_ids:
        c = by_id[cid]

        if str(
            c.get(
                "event_title",
                ""
            )
        ).strip():
            old_titles.append(
                str(
                    c[
                        "event_title"
                    ]
                ).strip()
            )

        if str(
            c.get(
                "event_reason",
                ""
            )
        ).strip():
            old_reasons.append(
                str(
                    c[
                        "event_reason"
                    ]
                ).strip()
            )

    entries = []

    for root, rs in history.items():
        try:
            if (
                uf.find(
                    member_ids[0]
                )
                ==
                uf.find(root)
            ):
                entries.extend(rs)
        except Exception:
            pass

    candidates = [
        r
        for r in entries
        if _metadata_record_valid(r)
    ]

    def score(r):
        return (
            len(
                r.get(
                    "cluster_ids",
                    []
                )
            ),
            1 if r.get(
                "merged"
            ) else 0,
            len(
                str(
                    r.get(
                        "reason",
                        ""
                    )
                )
            ),
            len(
                str(
                    r.get(
                        "event_title",
                        ""
                    )
                )
            ),
            -int(
                r.get(
                    "round",
                    0
                )
            )
        )

    candidate = max(
        candidates,
        key=score,
        default=None
    )

    if candidate:
        title = str(
            candidate.get(
                "event_title",
                ""
            )
        ).strip()

        reason = str(
            candidate.get(
                "reason",
                ""
            )
        ).strip()

    else:
        title = max(
            old_titles,
            key=len,
            default=""
        )

        reason = max(
            old_reasons,
            key=len,
            default=""
        )

    return (
        title or "未命名事件",
        reason
    )


def rebuild_global_clusters(
    current,
    uf,
    metadata_history
):
    by_id = {
        c["cluster_id"]:
            c
        for c in current
    }

    rebuilt = []

    for _, member_ids in (
        uf.components().items()
    ):
        member_ids = sorted(
            member_ids
        )

        articles = []
        originals = []

        for cid in member_ids:
            if cid not in by_id:
                raise RuntimeError(
                    "❌ Global Merge rebuild找不到Cluster："
                    f"{cid}"
                )

            c = by_id[cid]

            articles.extend(
                c.get(
                    "article_indexes",
                    []
                )
            )

            originals.extend(
                c.get(
                    "member_cluster_ids",
                    []
                )
            )

        articles = sorted(
            set(
                int(x)
                for x in articles
            )
        )

        originals = sorted(
            set(
                str(x)
                for x in originals
            )
        )

        title, reason = (
            choose_component_metadata(
                member_ids,
                by_id,
                metadata_history,
                uf
            )
        )

        # 保留最早Global ID，避免ID漂移。
        stable_id = min(
            member_ids
        )

        validate_global_id(
            stable_id
        )

        rebuilt.append({
            "cluster_id":
                stable_id,
            "event_title":
                title,
            "event_reason":
                reason,
            "article_indexes":
                articles,
            "member_cluster_ids":
                originals
        })

    rebuilt.sort(
        key=lambda c:
            min(
                c[
                    "article_indexes"
                ]
            )
            if c[
                "article_indexes"
            ]
            else 10**12
    )

    return rebuilt


# ============================================================
# ARTICLE COVERAGE
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

    actual = set(allidx)

    duplicate = sorted({
        x
        for x in allidx
        if allidx.count(x) > 1
    })

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
        raise RuntimeError(
            f"❌ {context} Article覆盖异常 "
            f"Duplicate={duplicate} "
            f"Missing={missing} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )


# ============================================================
# CHECKPOINT
# ============================================================

def save_global_merge_checkpoint(
    date,
    round_no,
    current,
    original_cluster_ids,
    completed_windows=None,
    status="running",
    uf=None,
    window_count=None,
    metadata_history=None
):
    if completed_windows is None:
        completed_windows = []

    registry = load_global_cluster_registry(
        date,
        create_if_missing=False
    )

    if registry is None:
        raise RuntimeError(
            "❌ 保存checkpoint前Registry不存在"
        )

    validate_global_cluster_membership(
        date,
        current,
        "CHECKPOINT BEFORE SAVE",
        original_cluster_ids,
        registry
    )

    data = {
        "version":
            PIPELINE_VERSION,
        "date":
            date,
        "status":
            status,
        "round":
            int(round_no),
        "completed_windows":
            sorted(
                set(
                    int(x)
                    for x in completed_windows
                )
            ),
        "window_count":
            (
                int(window_count)
                if window_count is not None
                else None
            ),
        "original_cluster_ids":
            sorted(
                str(x)
                for x in original_cluster_ids
            ),
        "current_clusters":
            current,
        "union_find":
            (
                uf.to_checkpoint()
                if uf is not None
                else None
            ),
        "metadata_history":
            (
                metadata_history
                if isinstance(
                    metadata_history,
                    dict
                )
                else {}
            ),
        "registry_next_sequence":
            registry[
                "next_sequence"
            ],
        "registry_global_ids":
            sorted(
                r[
                    "global_cluster_id"
                ]
                for r in registry[
                    "registered"
                ]
            ),
        "saved_at":
            now().isoformat()
    }

    write_json_atomic(
        global_merge_checkpoint_path(date),
        data
    )


def load_global_merge_checkpoint(date):
    p = global_merge_checkpoint_path(
        date
    )

    if not p.exists():
        return None

    data = read_json(
        p,
        None
    )

    if not isinstance(
        data,
        dict
    ):
        return None

    if (
        data.get("version")
        != PIPELINE_VERSION
        or
        data.get("date")
        != date
    ):
        return None

    return data


def validate_checkpoint(
    date,
    checkpoint,
    expected_original_ids,
    news_count
):
    if not checkpoint:
        return False

    current = checkpoint.get(
        "current_clusters"
    )

    if (
        not isinstance(
            current,
            list
        )
        or not current
    ):
        return False

    registry = (
        load_global_cluster_registry(
            date,
            create_if_missing=False
        )
    )

    if registry is None:
        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Checkpoint存在但Registry不存在。"
        )
        return False

    expected_original = {
        str(x)
        for x in expected_original_ids
    }

    actual_original = {
        str(x)
        for x in checkpoint.get(
            "original_cluster_ids",
            []
        )
    }

    if (
        actual_original
        != expected_original
    ):
        return False

    try:
        validate_global_cluster_membership(
            date,
            current,
            "CHECKPOINT MEMBERSHIP",
            expected_original_ids,
            registry
        )

        validate_global_article_coverage(
            date,
            current,
            news_count,
            "CHECKPOINT ARTICLE COVERAGE"
        )

    except Exception as e:
        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Checkpoint验证失败。",
            str(e)
        )
        return False

    checkpoint_ids = {
        str(x)
        for x in checkpoint.get(
            "registry_global_ids",
            checkpoint.get(
                "registry_global_ids",
                []
            )
        )
    }

    if checkpoint_ids:
        registry_ids = {
            r[
                "global_cluster_id"
            ]
            for r in registry[
                "registered"
            ]
        }

        if not checkpoint_ids <= registry_ids:
            return False

    status = checkpoint.get(
        "status"
    )

    if status == "converged":
        return True

    if status == "round_completed":
        return True

    if status != "running":
        return False

    uf_data = checkpoint.get(
        "union_find"
    )

    if not isinstance(
        uf_data,
        dict
    ):
        return False

    try:
        current_ids = [
            str(
                c["cluster_id"]
            )
            for c in current
        ]

        uf = UnionFind.from_checkpoint(
            current_ids,
            uf_data
        )

        uf.components()

    except Exception:
        return False

    completed = checkpoint.get(
        "completed_windows",
        []
    )

    if not isinstance(
        completed,
        list
    ):
        return False

    try:
        completed = [
            int(x)
            for x in completed
        ]
    except Exception:
        return False

    if (
        len(set(completed))
        != len(completed)
        or
        any(
            x < 1
            for x in completed
        )
    ):
        return False

    wc = checkpoint.get(
        "window_count"
    )

    if (
        wc is None
        or int(wc) < 1
        or any(
            x > int(wc)
            for x in completed
        )
    ):
        return False

    history = checkpoint.get(
        "metadata_history",
        {}
    )

    if not isinstance(
        history,
        dict
    ):
        return False

    return True


# ============================================================
# GLOBAL MERGE MAIN
# ============================================================

def merge_all_clusters(
    date,
    clusters,
    news_count
):
    current = clusters

    registry = load_global_cluster_registry(
        date,
        create_if_missing=False
    )

    if registry is None:
        raise RuntimeError(
            "❌ Global Merge开始前Registry不存在"
        )

    original_cluster_ids = sorted(
        str(
            c["cluster_id"]
        )
        for c in clusters
    )

    validate_global_cluster_membership(
        date,
        current,
        "STAGE 1B INITIAL",
        original_cluster_ids,
        registry
    )

    validate_global_article_coverage(
        date,
        current,
        news_count,
        "STAGE 1B INITIAL"
    )

    checkpoint = (
        load_global_merge_checkpoint(
            date
        )
    )

    checkpoint_valid = (
        validate_checkpoint(
            date,
            checkpoint,
            original_cluster_ids,
            news_count
        )
    )

    final_current = None

    if checkpoint_valid:
        status = checkpoint.get(
            "status"
        )

        current = checkpoint[
            "current_clusters"
        ]

        print(
            "\n♻️ 检测到有效 V6.5.2 "
            "Global Merge checkpoint"
        )

        print(
            f"   status={status}"
        )

        print(
            f"   round={checkpoint.get('round')}"
        )

        if status == "converged":
            final_current = current

        elif status == "round_completed":
            start_round = int(
                checkpoint["round"]
            )

            completed_windows = []
            uf = None
            metadata_history = {}

        else:
            start_round = int(
                checkpoint["round"]
            )

            completed_windows = [
                int(x)
                for x in checkpoint.get(
                    "completed_windows",
                    []
                )
            ]

            uf = UnionFind.from_checkpoint(
                [
                    str(
                        c["cluster_id"]
                    )
                    for c in current
                ],
                checkpoint[
                    "union_find"
                ]
            )

            metadata_history = (
                checkpoint.get(
                    "metadata_history",
                    {}
                )
            )

    else:
        start_round = 1
        completed_windows = []
        uf = None
        metadata_history = {}

        print(
            "\n🆕 未检测到可恢复的"
            "V6.5.2 checkpoint"
        )

    if final_current is None:
        rnd = start_round

        while True:
            before = len(current)

            if before <= 1:
                save_global_merge_checkpoint(
                    date,
                    rnd,
                    current,
                    original_cluster_ids,
                    [],
                    "converged",
                    None,
                    0,
                    {}
                )

                final_current = current
                break

            windows = build_merge_windows(
                current
            )

            window_count = len(
                windows
            )

            current_ids = [
                str(
                    c["cluster_id"]
                )
                for c in current
            ]

            if not (
                checkpoint_valid
                and
                rnd == start_round
                and
                checkpoint
                and
                checkpoint.get(
                    "status"
                ) == "running"
            ):
                uf = UnionFind(
                    current_ids
                )

                completed_windows = []
                metadata_history = {}

                next_window = 1

            else:
                uf = UnionFind.from_checkpoint(
                    current_ids,
                    checkpoint[
                        "union_find"
                    ]
                )

                completed_windows = [
                    int(x)
                    for x in checkpoint.get(
                        "completed_windows",
                        []
                    )
                ]

                metadata_history = (
                    checkpoint.get(
                        "metadata_history",
                        {}
                    )
                )

                next_window = (
                    max(
                        completed_windows,
                        default=0
                    )
                    + 1
                )

            for wi in range(
                next_window,
                window_count + 1
            ):
                w = windows[
                    wi - 1
                ]

                groups = (
                    merge_cluster_window(
                        date,
                        w,
                        rnd,
                        wi
                    )
                )

                records = (
                    apply_window_groups(
                        uf,
                        w,
                        groups,
                        rnd,
                        wi
                    )
                )

                metadata_history = (
                    merge_metadata_histories(
                        metadata_history,
                        records,
                        uf
                    )
                )

                completed_windows = sorted(
                    set(
                        completed_windows
                        + [wi]
                    )
                )

                save_global_merge_checkpoint(
                    date,
                    rnd,
                    current,
                    original_cluster_ids,
                    completed_windows,
                    "running",
                    uf,
                    window_count,
                    metadata_history
                )

            after = len(
                uf.components()
            )

            if after >= before:
                save_global_merge_checkpoint(
                    date,
                    rnd,
                    current,
                    original_cluster_ids,
                    list(
                        range(
                            1,
                            window_count + 1
                        )
                    ),
                    "converged",
                    uf,
                    window_count,
                    metadata_history
                )

                final_current = current
                break

            merged = rebuild_global_clusters(
                current,
                uf,
                metadata_history
            )

            validate_global_cluster_membership(
                date,
                merged,
                f"STAGE 1B ROUND {rnd}",
                original_cluster_ids,
                registry
            )

            validate_global_article_coverage(
                date,
                merged,
                news_count,
                f"STAGE 1B ROUND {rnd}"
            )

            save_global_merge_checkpoint(
                date,
                rnd + 1,
                merged,
                original_cluster_ids,
                [],
                "round_completed",
                None,
                None,
                {}
            )

            current = merged
            rnd += 1

            checkpoint_valid = True

            checkpoint = (
                load_global_merge_checkpoint(
                    date
                )
            )

    validate_global_cluster_membership(
        date,
        final_current,
        "STAGE 1B FINAL",
        original_cluster_ids,
        registry
    )

    validate_global_article_coverage(
        date,
        final_current,
        news_count,
        "STAGE 1B FINAL"
    )

    ordered = sorted(
        final_current,
        key=lambda c:
            min(
                c[
                    "article_indexes"
                ]
            )
    )

    final = []

    for c in ordered:
        gid = str(
            c["cluster_id"]
        ).strip()

        validate_global_id(
            gid
        )

        final.append({
            "event_id":
                gid,
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
        })

    validate_final_event_ids(
        date,
        final
    )

    validate_global_article_coverage(
        date,
        final,
        news_count,
        "STAGE 1B FINAL EVENT UNITS"
    )

    return final


# ============================================================
# EVENT UNIT
# ============================================================

def validate_final_event_ids(
    date,
    events
):
    ids = [
        str(
            e.get(
                "event_id",
                ""
            )
        ).strip()
        for e in events
    ]

    if any(
        not x
        for x in ids
    ):
        raise RuntimeError(
            f"❌ {date} Final EventUnit存在空event_id"
        )

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            f"❌ {date} Final EventUnit存在重复event_id"
        )

    for x in ids:
        validate_global_id(x)


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
                    f"❌ {c['event_id']}引用不存在文章：{i}"
                )

            m = news[
                i - 1
            ]["metadata"]

            arts.append({
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
            })

        out.append({
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
        })

    return out


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

    prompt = f"""你正在执行748686自生长知识系统V6.5.2第二层事件知识综合。

日期：{event['date']}
事件ID：{event['event_id']}
事件名称：{event['event_title']}
第一层事件判断：{event['event_reason']}

同一事件的多来源输入：
{chr(10).join(blocks)}

把来源综合成一个高质量事件知识单元。

要求：
1. 识别共同事实；
2. 保留来源独有信息；
3. 保留不同地区视角；
4. 区分事实与推测；
5. 不编造；
6. source_status不是fetched时不得声称完整阅读原文；
7. 冲突明确指出；
8. 资料不足明确说明。

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
## 事件结论"""

    return call_ai(
        prompt,
        (
            "你是跨来源新闻综合专家。"
            "严格依据输入，不得编造。"
            "输出标准中文Markdown。"
        ),
        0.2
    )


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
        data.append({
            "event_id":
                e["event_id"],
            "date":
                e["date"],
            "event_title":
                e["event_title"],
            "event_reason":
                e["event_reason"],
            "source_count":
                len(e["articles"]),
            "articles": [
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
                for a in e[
                    "articles"
                ]
            ]
        })

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

    d = read_json(
        p,
        None
    )

    if (
        isinstance(d, list)
        and d
    ):
        return d

    return None


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

    return bool(
        b.strip()
    ) and (
        m.get(
            "event_id"
        )
        == event_id
    ) and (
        m.get(
            "status"
        )
        == "completed"
    )


def inspect_event_units(date):
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

    for e in idx:
        eid = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

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

    return {
        "exists":
            True,
        "complete":
            bool(idx)
            and not missing
            and not invalid,
        "index":
            idx,
        "missing":
            missing,
        "invalid":
            invalid,
        "unexpected":
            []
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


def rebuild_events_from_index(
    date,
    index,
    news
):
    out = []

    for e in index:
        eid = str(
            e["event_id"]
        ).strip()

        validate_global_id(
            eid
        )

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
                    f"❌ {eid}引用不存在文章：{i}"
                )

            m = news[
                i - 1
            ]["metadata"]

            arts.append({
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
            })

        out.append({
            "event_id":
                eid,
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
        })

    return out


def validate_event_index_coverage(
    date,
    events,
    n
):
    ids = []
    eids = set()

    for e in events:
        eid = str(
            e["event_id"]
        ).strip()

        validate_global_id(
            eid
        )

        if eid in eids:
            raise RuntimeError(
                f"❌ {date} Event Index重复event_id："
                f"{eid}"
            )

        eids.add(eid)

        ids.extend(
            a["index"]
            for a in e["articles"]
        )

    expected = set(
        range(
            1,
            n + 1
        )
    )

    if (
        set(ids)
        != expected
        or
        len(ids)
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
        validate_global_id(
            e["event_id"]
        )

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
                f"❌ {e['event_id']}综合结果为空"
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
                f"❌ {e['event_id']}保存验证失败"
            )

        generated += 1

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
                f"❌ {e['event_id']}最终缺失"
            )

    marker = mark_event_units_complete(
        date,
        n,
        len(events)
    )

    print(
        f"✅ EVENT UNITS COMPLETE | "
        f"new={generated} "
        f"total={len(events)} | "
        f"{marker}"
    )

    return True


# ============================================================
# STAGE 1
# ============================================================

def run_stage_1(date):
    print(
        f"\n{'=' * 70}\n"
        f"STAGE 1 — EVENT UNIT GENERATION "
        f"V6.5.2: {date}\n"
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
        events = (
            rebuild_events_from_index(
                date,
                inspection["index"],
                news
            )
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

    # ========================================================
    # 重要：
    #
    # 这里不再删除 Registry。
    #
    # V6.5.1 的：
    #
    # registry_file.unlink()
    #
    # 已删除。
    #
    # Resume必须保留Global ID Ledger。
    # ========================================================

    registry = load_global_cluster_registry(
        date,
        create_if_missing=True
    )

    initial = build_initial_clusters(
        date,
        news
    )

    # 确保build阶段和当前Registry一致。
    validate_global_cluster_membership(
        date,
        initial,
        "STAGE 1A BEFORE GLOBAL MERGE",
        [
            c["cluster_id"]
            for c in initial
        ],
        registry
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

    validate_final_event_ids(
        date,
        events
    )

    p = save_aggregation_index(
        date,
        events
    )

    print(
        f"✅ Event Index saved: {p}"
    )

    # Registry保留。
    # Global Merge checkpoint完成后才可以清理checkpoint，
    # 但Registry作为Global ID Ledger继续保留。
    checkpoint = (
        global_merge_checkpoint_path(
            date
        )
    )

    if checkpoint.exists():
        checkpoint.unlink()

    print(
        "🧹 Global Merge checkpoint已清理"
    )

    print(
        "🔐 Global Cluster Registry保留"
    )

    return complete_existing_event_units(
        date,
        events,
        len(news)
    )


# ============================================================
# STAGE 2
# ============================================================

def load_saved_event_units(date):
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
        eid = str(
            e.get(
                "event_id",
                ""
            )
        )

        validate_global_id(
            eid
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
                f"❌ EventUnit缺失或无效：{eid}"
            )

        files.append(
            (e, valid)
        )

    return files


def run_one_skill(
    event,
    skill
):
    content = event[1].read_text(
        encoding="utf-8",
        errors="replace"
    )

    eid = event[0].get(
        "event_id",
        ""
    )

    validate_global_id(
        eid
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.2的27 Skills深度处理。

事件：
{event[0].get('event_title', '')}

Event ID：
{eid}

Skill名称：
{skill['name']}

Skill规则：
{skill['content']}

EventUnit原文：
{content[:30000]}

请严格按照该Skill完成深度处理。
不要编造。
只使用EventUnit提供的信息。
输出可直接写入知识库的中文Markdown。"""

    return call_ai(
        prompt,
        (
            "你是748686知识系统Skill执行器。"
            "严格执行Skill规则，不得编造。"
        ),
        0.2
    )


def run_stage_2(date):
    files = load_saved_event_units(
        date
    )

    skills = load_skills()
    routes = load_routes()

    print(
        f"\nSTAGE 2 — 27 SKILLS | "
        f"Events={len(files)} | "
        f"Skills={len(skills)}"
    )

    selected = []
    selected_names = set()

    for category, names in routes.items():
        for name in names:
            if (
                name in skills
                and name not in selected_names
            ):
                selected.append(
                    skills[name]
                )
                selected_names.add(
                    name
                )

    if not selected:
        selected = [
            skills[k]
            for k in sorted(skills)
        ]

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

        validate_global_id(
            eid
        )

        edir = (
            outroot / eid
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
                /
                f"{safe_name(skill['name']).replace('.md', '')}.md"
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
        description=
            "748686 Knowledge Pipeline V6.5.2"
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
        # 强制检查日期。
        compact_date(
            args.date
        )

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
            f"V6.5.2 FAILED: {e}",
            file=sys.stderr
        )
        return 1

    print(
        f"\n✅ Knowledge Pipeline "
        f"V6.5.2 finished: "
        f"{args.date} / {args.stage}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
