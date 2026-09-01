#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Knowledge Pipeline V6.5.3 modular architecture."""

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


# ======================================================================
# 基础路径契约
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]

# 所有实际目录名称统一使用小写
SYSTEM = ROOT / "00_system"
SKILLS = ROOT / "skills"
RAW_NEWS = ROOT / "raw news"
REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"
TOPICS = ROOT / "07_专题报告"
KNOWLEDGE = ROOT / "08_知识库"

LOGS = SYSTEM / "运行日志"
ROUTES_FILE = SYSTEM / "skill_routes.json"


# ======================================================================
# 文件名称契约
# ======================================================================

EVENT_UNITS_SUFFIX = "eventunit"

EVENT_INDEX_FILE = "_event_index.json"
EVENT_UNITS_COMPLETE_FILE = "_COMPLETE"
SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"
INITIAL_CLUSTERS_FILE = "_initial_clusters.json"
MERGED_CLUSTERS_FILE = "_merged_clusters.json"

GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"


# ======================================================================
# AI 配置
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AI_BASE_URL",
    "https://api.agnes-ai.cn/v1"
).rstrip("/")

AGNES_MODEL = os.getenv(
    "AI_MODEL",
    "agnes-2.5-flash"
)

AGNES_API_KEY_ENV = "AGNES_API_KEY"


DEFAULT_TEMPERATURE = 0.3

AI_TIMEOUT = 180

AI_REQUEST_THROTTLE_SECONDS = 1.5

AI_MAX_429_RETRIES = 5

AI_429_BACKOFF_BASE = 10

AI_429_BACKOFF_MAX = 180

AI_429_JITTER_MAX = 3

_LAST_AI_REQUEST_TIME = 0.0


# ======================================================================
# 聚类参数
# ======================================================================

AGGREGATION_BATCH_SIZE = 30

GLOBAL_MERGE_WINDOW_SIZE = 30

GLOBAL_MERGE_OVERLAP = 0

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2

RECOVERY_BATCH_SIZES = (
    30,
    15,
    8,
    4,
    2,
    1
)


# ======================================================================
# 时间 / 语言
# ======================================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")

SUPPORTED_LANGUAGES = (
    "EN",
    "ZH"
)

CURRENT_LANGUAGE = None


# ======================================================================
# LANGUAGE
# ======================================================================

def normalize_language(language):
    """
    内部逻辑语言统一使用 EN / ZH。
    实际文件系统目录统一通过 .lower() 生成：
        EN -> en
        ZH -> zh
    """

    value = str(
        language or ""
    ).strip().upper()

    if value not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ 不支持的语言：{language}"
        )

    return value


# ======================================================================
# 时间
# ======================================================================

def now():
    return datetime.now(
        BEIJING_TZ
    )


# ======================================================================
# EventUnit 路径
# ======================================================================

def event_units_root(date):
    """
    统一目录：

    raw news/
        YYYY-MM-DD-eventunit/
            en/
            zh/
    """

    return RAW_NEWS / (
        f"{date}-{EVENT_UNITS_SUFFIX}"
    )


def language_dir(
    date,
    language=None
):
    if language is None:
        language = getattr(
            sys.modules[__name__],
            "CURRENT_LANGUAGE",
            None
        )

    lang = normalize_language(
        language
    ).lower()

    return (
        event_units_root(date)
        / lang
    )


def event_units_dir(
    date,
    language=None
):
    return (
        language_dir(
            date,
            language
        )
        / "event_units"
    )


def articles_dir(
    date,
    language=None
):
    return (
        language_dir(
            date,
            language
        )
        / "articles"
    )


# ======================================================================
# 日志路径
# ======================================================================

def conflict_log_path(date):
    return LOGS / (
        f"{date}_event_aggregation_conflicts.log"
    )


# ======================================================================
# Checkpoint / Cluster 文件路径
# ======================================================================

def global_merge_checkpoint_path(
    date,
    language=None
):
    return (
        event_units_dir(
            date,
            language
        )
        / GLOBAL_MERGE_CHECKPOINT_FILE
    )


def initial_clusters_path(
    date,
    language=None
):
    return (
        language_dir(
            date,
            language
        )
        / INITIAL_CLUSTERS_FILE
    )


def merged_clusters_path(
    date,
    language=None
):
    return (
        language_dir(
            date,
            language
        )
        / MERGED_CLUSTERS_FILE
    )


# ======================================================================
# Atomic Write
# ======================================================================

def write_text_atomic(
    path,
    text
):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:
        tmp.write_text(
            text,
            encoding="utf-8"
        )

        tmp.replace(path)

    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass

        raise


# ======================================================================
# ARTICLE DIGEST
# ======================================================================

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


# ======================================================================
# Cluster Coverage Inspection
# ======================================================================

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
                f"cluster[{pos}] article_indexes不是数组"
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

    actual = set(
        occ
    )

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
    return not any([
        i["duplicate"],
        i["missing"],
        i["extra"],
        i["malformed"]
    ])


# ======================================================================
# Cluster Normalize
# ======================================================================

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
            d["article_indexes"] = [
                int(x)
                if str(x).lstrip("-").isdigit()
                else x
                for x in ids
            ]

        out.append(d)

    return out


# ======================================================================
# AI 第一轮新闻聚类
# ======================================================================

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

    prompt = f"""你正在执行748686自生长知识系统V6.5.3第一层事件聚类。
日期：{date}

{joined}

任务：识别哪些新闻属于同一个现实世界的具体事件。
支持跨来源、跨语言。
不要因为关键词、公司、行业、国家相同就强行合并。
无法确定时宁可分开。

绝对覆盖ARTICLE编号：{json.dumps(expected)}
每篇必须且只能属于一个cluster。
无法与其他文章合并的文章必须单独成为cluster。

重要输出限制：
- cluster_id只是本批次Local Cluster ID，例如C001、C002；不要生成EVT-/REC-/GM-等Global ID。
- Global Cluster ID由Python全局注册器统一生成。
- 只输出JSON，不要Markdown，不要解释。
- event_title尽量短。
- event_reason尽量短，一句话即可。
- 不要复制文章正文。

只输出：
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
            "你是全球新闻事件聚类专家。"
            "每篇ARTICLE必须且只能属于一个cluster。"
            "只输出合法JSON。",
            0
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类"
        )

    except RuntimeError as first_error:

        compact_prompt = f"""748686 V6.5.3 新闻事件聚类JSON修复。
日期：{date}
ARTICLE范围：{json.dumps(expected)}

文章：
{joined}

重新聚类。严格要求：
1. 每个ARTICLE恰好一次；
2. 同一具体现实事件合并；不同事件分开；
3. 不能确定宁可分开；
4. 每个cluster只返回cluster_id、article_indexes、event_title、event_reason；
5. event_title不超过40字；event_reason不超过80字；
6. 绝对不要输出文章正文；
7. 只输出JSON，不要代码围栏，不要解释。

格式：
{{"clusters":[{{"cluster_id":"C001",
"article_indexes":[1],
"event_title":"事件",
"event_reason":"判断"}}]}}"""

        print(
            "   ⚠️ 第一轮聚类JSON解析失败，"
            f"启动同批次紧凑JSON重试：{first_error}"
        )

        result = call_ai(
            compact_prompt,
            "你是新闻聚类JSON修复器。"
            "只输出合法JSON，绝不输出解释。",
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


# ======================================================================
# Cluster Repair
# ======================================================================

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

    prompt = f"""修复748686 V6.5.3 ARTICLE覆盖冲突。
日期：{date}
第{attempt}次修复
真实ARTICLE：{json.dumps(expected)}

文章：
{joined}

上次结果：
{json.dumps(broken, ensure_ascii=False, indent=2)}

检测问题：
{json.dumps(issues, ensure_ascii=False, indent=2)}

重新判断全部文章。

要求：
1. cluster_id只能是Local Cluster ID（如C001），不得生成EVT-/REC-/GM- ID；
2. 同事件合并；不同事件分开；
3. 每篇ARTICLE恰好一次；
4. Missing=0；
5. Duplicate=0；
6. Extra=0；
7. 不得遗漏任何ARTICLE；
8. 只输出JSON，不要解释。

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
            "你是新闻事件聚类冲突修复专家。"
            "必须完整覆盖输入ARTICLE。",
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


# ======================================================================
# Coverage Validation
# ======================================================================

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


# ======================================================================
# Safe Covered Indexes
# ======================================================================

def _safe_covered_indexes(
    clusters,
    expected_indexes
):
    """
    只有不存在Duplicate / Extra / Malformed时，
    才允许保留已唯一覆盖的ARTICLE。
    """

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


# ======================================================================
# Cluster With Repair
# ======================================================================

def cluster_news_batch_with_repair(
    date,
    items,
    indexes,
    batch_label
):
    """
    返回：

      ("complete", clusters, [])

      ("partial", clusters, missing_indexes)

      ("failed", [], expected_indexes)

    V6.5.3原则：

    Missing-only可以安全隔离Missing。

    Duplicate/Extra/Malformed必须整批隔离。

    AI异常不再直接终止整个任务。
    """

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

        if valid_issues(
            issues
        ):
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
                "issues": issues,
                "clusters": clusters
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

                if valid_issues(
                    issues
                ):

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
                        "issues": issues,
                        "clusters": clusters
                    }
                )

            except Exception as repair_error:

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    f"第{attempt}次聚类修复请求/解析失败。",
                    str(repair_error)
                )

        final_issues = inspect_cluster_assignment(
            clusters or [],
            expected
        )

        # Missing-only：
        # 安全保留已经唯一出现的文章。

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
                set(expected) - set(safe)
            )

            if safe and unresolved:

                print(
                    f"   🟡 Missing-only：安全保留 "
                    f"{len(safe)}篇，隔离 "
                    f"{len(unresolved)}篇：{unresolved}"
                )

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    "修复失败，但仅存在Missing；"
                    "安全覆盖部分保留，"
                    "Missing进入Recovery Queue。",
                    {
                        "safe_covered": safe,
                        "recovery_queue": unresolved,
                        "issues": final_issues
                    }
                )

                return (
                    "partial",
                    clusters,
                    unresolved
                )

        # Duplicate / Extra / Malformed：
        # 整批隔离。

        print(
            f"   🔴 Batch结果不安全，"
            f"整批进入Recovery Queue：{expected}"
        )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            "自动修复失败；整批隔离，"
            "防止错误结果污染Global Merge。",
            {
                "issues": final_issues,
                "recovery_queue": expected
            }
        )

        return (
            "failed",
            [],
            expected
        )

    except Exception as e:

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            "本批AI异常；整批隔离进入Recovery Queue，"
            "不终止任务。",
            str(e)
        )

        print(
            "   🔴 AI exception isolated into "
            f"Recovery Queue: {expected}"
        )

        return (
            "failed",
            [],
            expected
        )


# ======================================================================
# Local Cluster Records
# ======================================================================

def _make_cluster_records(
    batch_identifier,
    clusters
):
    """
    只建立Local Cluster。
    绝不在这里生成Global ID。
    """

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
                "cluster_id",
                "C001"
            )
        ).strip()

        out.append({
            "cluster_id": local_id,
            "local_cluster_id": local_id,
            "event_title": c.get(
                "event_title",
                "未命名事件"
            ),
            "event_reason": c.get(
                "event_reason",
                ""
            ),
            "article_indexes": indexes,
            "batch_identifier": batch_identifier
        })

    return out


# ======================================================================
# Safe Cluster Append
# ======================================================================

def _append_safe_clusters(
    allc,
    clusters,
    batch_no,
    expected_indexes,
    date,
    context,
    registry
):
    validate_cluster_coverage(
        clusters,
        expected_indexes,
        context,
        date
    )

    local_records = _make_cluster_records(
        batch_no,
        clusters
    )

    allc.extend(
        register_global_cluster_ids(
            date,
            local_records,
            registry,
            context
        )
    )


# ======================================================================
# Recovery Pass
# ======================================================================

def _recovery_pass(
    date,
    news,
    indexes,
    recovery_pass_no,
    batch_size,
    registry
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
        f"\n🛠️ RECOVERY PASS {recovery_pass_no} | "
        f"Articles={len(indexes)} | "
        f"BatchSize={batch_size} | "
        f"SubBatches={len(sub_batches)}"
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

        print(
            f"   🔹 {label}: "
            f"{sub_indexes}"
        )

        # 单篇最终安全降级为singleton。

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

            safe_set = set(
                safe
            )

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

                    item = dict(
                        cluster
                    )

                    item["article_indexes"] = (
                        sorted(
                            set(ids)
                        )
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


# ======================================================================
# Stage 1A
# ======================================================================

def build_initial_clusters(
    date,
    news,
    registry=None
):
    allc = []

    total = len(
        news
    )

    if registry is None:

        registry = read_json(
            global_cluster_registry_path(date),
            None
        )

        if not isinstance(
            registry,
            dict
        ):

            registry = (
                create_global_cluster_registry(
                    date
                )
            )

            persist_global_cluster_registry(
                date,
                registry
            )

    print(
        "\n" + "=" * 70
    )

    print(
        "STAGE 1A — AI EVENT CLUSTERING V6.5.3"
    )

    print(
        "=" * 70
    )

    print(
        f"Input Enriched News: {total}"
    )

    print(
        f"Normal Batch Size: "
        f"{AGGREGATION_BATCH_SIZE}"
    )

    print(
        "Failure Policy: isolate -> "
        "recovery queue -> 30/15/8/4/2/1 -> singleton"
    )

    pending = []

    normal_batch_no = 0

    # ==============================================================
    # 第一阶段：正常30篇连续处理
    # ==============================================================

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

        items = news[
            start:end
        ]

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

            _append_safe_clusters(
                allc,
                clusters,
                normal_batch_no,
                indexes,
                date,
                f"Batch {normal_batch_no}",
                registry
            )

            print(
                f"   Clusters generated: "
                f"{len(clusters)}"
            )

        elif status == "partial":

            safe = _safe_covered_indexes(
                clusters,
                indexes
            )

            safe_set = set(
                safe
            )

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

                    item = dict(
                        cluster
                    )

                    item["article_indexes"] = (
                        sorted(
                            set(ids)
                        )
                    )

                    safe_clusters.append(
                        item
                    )

            if safe_clusters:

                validate_cluster_coverage(
                    safe_clusters,
                    safe,
                    f"{date} Batch "
                    f"{normal_batch_no} SAFE PART",
                    date
                )

                local_records = (
                    _make_cluster_records(
                        normal_batch_no,
                        safe_clusters
                    )
                )

                allc.extend(
                    register_global_cluster_ids(
                        date,
                        local_records,
                        registry,
                        f"Batch {normal_batch_no} SAFE PART"
                    )
                )

            pending.extend(
                unresolved
            )

            print(
                f"   🟡 Safe clusters kept="
                f"{len(safe_clusters)} | "
                f"Pending={len(pending)}"
            )

        else:

            pending.extend(
                unresolved
            )

            print(
                f"   🔴 Entire batch isolated | "
                f"Pending={len(pending)}"
            )

    # ==============================================================
    # 第二阶段：Recovery Queue
    # ==============================================================

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
                batch_size,
                registry
            )
        )

        local_records = (
            _make_cluster_records(
                f"RECOVERY PASS {pass_no}",
                recovered
            )
        )

        allc.extend(
            register_global_cluster_ids(
                date,
                local_records,
                registry,
                f"Recovery Pass {pass_no}"
            )
        )

        pending.extend(
            unresolved
        )

        print(
            f"   Recovery Pass {pass_no}: "
            f"recovered={len(recovered)} | "
            f"still_pending={len(pending)}"
        )

    # ==============================================================
    # 最终安全闸
    # ==============================================================

    if pending:

        log_conflict(
            date,
            "STAGE 1A / FINAL RECOVERY",
            "Recovery Queue仍有未处理ARTICLE，"
            "禁止进入Global Merge。",
            {
                "pending_articles":
                    sorted(
                        set(pending)
                    )
            }
        )

        raise RuntimeError(
            "❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE："
            f"{sorted(set(pending))}"
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

    print(
        f"✅ ARTICLE Coverage: "
        f"{total}/{total}"
    )

    return allc


# ======================================================================
# Initial Cluster File Validation
# ======================================================================

def validate_initial_clusters_file(
    date,
    clusters,
    news_count,
    language
):
    if (
        not isinstance(
            clusters,
            list
        )
        or not clusters
    ):
        return False

    try:

        validate_cluster_coverage(
            clusters,
            range(
                1,
                news_count + 1
            ),
            f"{date} {language} INITIAL FILE",
            date
        )

        validate_global_cluster_membership(
            date,
            clusters,
            "INITIAL CLUSTERS",
            [
                c["cluster_id"]
                for c in clusters
            ]
        )

    except Exception:

        return False

    return True


# ======================================================================
# Save Initial Clusters
# ======================================================================

def save_initial_clusters(
    date,
    language,
    clusters
):
    write_json_atomic(
        initial_clusters_path(
            date,
            language
        ),
        {
            "version": "6.5.3",
            "date": str(date),
            "language": normalize_language(
                language
            ),
            "clusters": clusters,
            "saved_at": now().isoformat()
        }
    )


# ======================================================================
# Load Initial Clusters
# ======================================================================

def load_initial_clusters(
    date,
    language,
    news_count
):
    p = initial_clusters_path(
        date,
        language
    )

    if not p.exists():
        return None

    data = read_json(
        p,
        None
    )

    clusters = (
        data.get(
            "clusters"
        )
        if isinstance(
            data,
            dict
        )
        else None
    )

    if not validate_initial_clusters_file(
        date,
        clusters,
        news_count,
        language
    ):
        return None

    return clusters


# ======================================================================
# TASK 1
# ======================================================================

def run_task_1(
    date,
    language
):
    global CURRENT_LANGUAGE

    lang = normalize_language(
        language
    )

    CURRENT_LANGUAGE = lang

    root = language_dir(
        date,
        lang
    )

    root.mkdir(
        parents=True,
        exist_ok=True
    )

    articles_dir(
        date,
        lang
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    event_units_dir(
        date,
        lang
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    news = load_all_enriched_news(
        date,
        lang
    )

    existing = load_initial_clusters(
        date,
        lang,
        len(news)
    )

    if existing is not None:

        print(
            f"♻️ TASK 1: reuse valid initial clusters | "
            f"{date}/{lang} | "
            f"clusters={len(existing)}"
        )

        return existing

    registry_file = (
        global_cluster_registry_path(
            date
        )
    )

    registry = (
        read_json(
            registry_file,
            None
        )
        if registry_file.exists()
        else None
    )

    if (
        not isinstance(
            registry,
            dict
        )
        or registry.get("date")
        != str(date)
    ):

        registry = (
            create_global_cluster_registry(
                date
            )
        )

        persist_global_cluster_registry(
            date,
            registry
        )

    else:

        validate_registry_basic(
            date,
            registry
        )

    clusters = build_initial_clusters(
        date,
        news,
        registry=registry
    )

    validate_global_cluster_membership(
        date,
        clusters,
        "TASK 1 FINAL",
        [
            c["cluster_id"]
            for c in clusters
        ]
    )

    validate_global_article_coverage(
        date,
        clusters,
        len(news),
        "TASK 1 FINAL"
    )

    save_initial_clusters(
        date,
        lang,
        clusters
    )

    print(
        f"✅ TASK 1 COMPLETE | "
        f"{date}/{lang} | "
        f"articles={len(news)} | "
        f"clusters={len(clusters)}"
    )

    return clusters


# ======================================================================
# Registry Validation
# ======================================================================

def validate_registry_basic(
    date,
    registry
):
    if (
        not isinstance(
            registry,
            dict
        )
        or registry.get("date")
        != str(date)
    ):
        raise RuntimeError(
            f"❌ {date} Global Cluster Registry异常"
        )

    if (
        not isinstance(
            registry.get(
                "next_sequence"
            ),
            int
        )
        or registry["next_sequence"] < 1
    ):
        raise RuntimeError(
            f"❌ {date} Global Cluster Registry next_sequence异常"
        )

    if not isinstance(
        registry.get(
            "registered"
        ),
        list
    ):
        raise RuntimeError(
            f"❌ {date} Global Cluster Registry registered异常"
        )


# ======================================================================
# Global Cluster Membership Validation
# ======================================================================

def validate_global_cluster_membership(
    date,
    clusters,
    context,
    expected_original_ids=None
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

        elif not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            cid
        ):

            malformed.append(
                f"cluster[{pos}]非法Global cluster_id：{cid}"
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

    missing_original = []

    extra_original = []

    if expected_original_ids is not None:

        expected = {
            str(x).strip()
            for x in expected_original_ids
        }

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


# ======================================================================
# Global Article Coverage
# ======================================================================

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


# ======================================================================
# Union Find
# ======================================================================

class UnionFind:

    def __init__(
        self,
        values
    ):
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

    def find(
        self,
        value
    ):
        value = str(
            value
        )

        if value not in self.parent:
            raise KeyError(
                value
            )

        p = self.parent[
            value
        ]

        if p != value:

            self.parent[value] = (
                self.find(p)
            )

        return self.parent[
            value
        ]

    def union(
        self,
        a,
        b
    ):
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

    def to_checkpoint(self):

        for v in list(
            self.parent
        ):

            self.find(v)

        return {
            "parent":
                dict(
                    self.parent
                ),

            "rank":
                dict(
                    self.rank
                )
        }

    @classmethod
    def from_checkpoint(
        cls,
        values,
        data
    ):
        uf = cls(
            values
        )

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
            not isinstance(
                parent,
                dict
            )
            or not isinstance(
                rank,
                dict
            )
        ):

            raise RuntimeError(
                "❌ Union-Find checkpoint缺少parent/rank"
            )

        expected = {
            str(x)
            for x in values
        }

        if (
            set(
                map(
                    str,
                    parent
                )
            )
            != expected
            or
            set(
                map(
                    str,
                    rank
                )
            )
            != expected
        ):

            raise RuntimeError(
                "❌ Union-Find checkpoint Universe不一致"
            )

        uf.parent = {
            str(k): str(v)
            for k, v in parent.items()
        }

        try:

            uf.rank = {
                str(k): int(v)
                for k, v in rank.items()
            }

        except Exception as e:

            raise RuntimeError(
                "❌ Union-Find checkpoint rank非法"
            ) from e

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
                "❌ Union-Find checkpoint"
                "存在非法rank"
            )

        return uf


# ======================================================================
# Global Merge Window
# ======================================================================

def build_merge_windows(
    clusters
):
    if len(clusters) <= GLOBAL_MERGE_WINDOW_SIZE:
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


# ======================================================================
# Global Merge AI
# ======================================================================

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
Cluster ID：
{c['cluster_id']}
原始Cluster成员：
{json.dumps(c.get('member_cluster_ids', []), ensure_ascii=False)}
事件名称：
{c.get('event_title', '未命名事件')}
事件判断：
{c.get('event_reason', '')}
文章数量：
{len(c.get('article_indexes', []))}
文章编号：
{json.dumps(c.get('article_indexes', []))}"""
        )

    expected = list(
        range(
            1,
            len(window) + 1
        )
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.3全局事件归并。
日期：{date}
轮次：{round_no}
窗口：{window_no}

{chr(10).join(blocks)}

判断这些Cluster是否属于同一个“具体现实世界事件”。

可以合并：同一政策发布、同一公司重大动作、同一事故、同一产品发布、同一具体现实事件、同一正在持续发展的单一现实事件。

不得合并：同公司不同事件、同人物不同事件、同国家不同事件、同产业不同事件、同趋势不同具体事件、仅关键词相同、仅主题相同。
无法确认时宁可分开。

要求：
1. 每个输入Cluster必须且只能进入一个group。
2. 不得遗漏、重复、创造Cluster编号。
3. 一个group可以只有一个Cluster。
4. Cluster ID是Python已经注册的Global ID，只能原样引用，不得修改、重编号或生成REC-/GM-替代ID。
5. 不需要返回文章编号。
6. 只根据当前窗口中的Cluster判断。
输入Cluster编号：{json.dumps(expected)}

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
        f"{date} Global Merge Round "
        f"{round_no} Window {window_no}"
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
        set(expected) - set(actual)
    )

    extra = sorted(
        set(actual) - set(expected)
    )

    if (
        dup
        or miss
        or extra
        or malformed
    ):

        log_conflict(
            date,
            f"STAGE 1B / ROUND {round_no} / WINDOW {window_no}",
            "V6.5.3 Global Merge窗口AI输出覆盖异常。",
            {
                "duplicate": dup,
                "missing": miss,
                "extra": extra,
                "malformed": malformed,
                "groups": groups
            }
        )

        raise RuntimeError(
            f"❌ Global Merge窗口AI输出异常 "
            f"Duplicate={dup} Missing={miss} "
            f"Extra={extra} Malformed={malformed}"
        )

    return groups


# ======================================================================
# Apply Window Groups
# ======================================================================

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

        anchor = ids[0]

        merged = False

        for cid in ids[1:]:

            if uf.union(
                anchor,
                cid
            ):

                merged = True

        records.append({
            "group_id": g.get(
                "group_id",
                f"G{gp:03d}"
            ),

            "cluster_ids": ids,

            "event_title": str(
                g.get(
                    "event_title",
                    "未命名事件"
                )
            ).strip(),

            "reason": str(
                g.get(
                    "reason",
                    ""
                )
            ).strip(),

            "merged": merged,

            "round": round_no,

            "window": window_no
        })

    return records


# ======================================================================
# Metadata
# ======================================================================

def _metadata_record_valid(
    r
):
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
            "cluster_ids": ids,

            "event_title": r.get(
                "event_title",
                ""
            ),

            "reason": r.get(
                "reason",
                ""
            ),

            "merged": bool(
                r.get(
                    "merged"
                )
            ),

            "round": int(
                r.get(
                    "round",
                    0
                )
            ),

            "window": int(
                r.get(
                    "window",
                    0
                )
            )
        }

        history.setdefault(
            root,
            []
        ).append(
            item
        )

    merged = {}

    for old_root, entries in history.items():

        if not entries:
            continue

        first_ids = (
            entries[-1]
            .get(
                "cluster_ids"
            )
            or []
        )

        if not first_ids:
            continue

        try:

            root = uf.find(
                first_ids[0]
            )

        except KeyError:

            continue

        merged.setdefault(
            root,
            []
        ).extend(
            entries
        )

    return merged


# ======================================================================
# Component Metadata
# ======================================================================

def choose_component_metadata(
    member_ids,
    by_id,
    history,
    uf
):
    old_titles = []

    old_reasons = []

    for cid in member_ids:

        c = by_id[
            cid
        ]

        if str(
            c.get(
                "event_title",
                ""
            )
        ).strip():

            old_titles.append(
                str(
                    c["event_title"]
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
                    c["event_reason"]
                ).strip()
            )

    entries = []

    for root, rs in history.items():

        try:

            if (
                uf.find(
                    member_ids[0]
                )
                == uf.find(
                    root
                )
            ):

                entries.extend(
                    rs
                )

        except Exception:
            pass

    actual = [
        r
        for r in entries
        if r.get("merged")
        and len(
            r.get(
                "cluster_ids",
                []
            )
        ) > 1
        and _metadata_record_valid(r)
    ]

    multi = [
        r
        for r in entries
        if len(
            r.get(
                "cluster_ids",
                []
            )
        ) > 1
        and _metadata_record_valid(r)
    ]

    singleton = [
        r
        for r in entries
        if len(
            r.get(
                "cluster_ids",
                []
            )
        ) == 1
        and _metadata_record_valid(r)
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
            )
            else 0,

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
            ),

            -int(
                r.get(
                    "window",
                    0
                )
            )
        )

    candidate = max(
        actual or multi or [],
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

        if (
            not title
            and not reason
            and singleton
        ):

            candidate = max(
                singleton,
                key=score
            )

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

    return (
        title or "未命名事件",
        reason
    )


# ======================================================================
# Rebuild Global Clusters
# ======================================================================

def rebuild_global_clusters(
    current,
    uf,
    metadata_history
):
    by_id = {
        c["cluster_id"]: c
        for c in current
    }

    rebuilt = []

    for root, member_ids in uf.components().items():

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

            c = by_id[
                cid
            ]

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

        rebuilt.append({
            # 合并后的组件保留最早注册的Global ID，
            # 避免ID漂移。

            "cluster_id":
                min(member_ids),

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
                c["article_indexes"]
            )
            if c["article_indexes"]
            else 10**12
    )

    return rebuilt


# ======================================================================
# Global Merge Checkpoint
# ======================================================================

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

    data = {
        "version":
            "6.5.3",

        "date":
            date,

        "language":
            CURRENT_LANGUAGE,

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
            int(window_count)
            if window_count is not None
            else None,

        "window_size":
            GLOBAL_MERGE_WINDOW_SIZE,

        "window_overlap":
            0,

        "original_cluster_ids":
            sorted(
                str(x)
                for x in original_cluster_ids
            ),

        "current_clusters":
            current,

        "union_find":
            uf.to_checkpoint()
            if uf is not None
            else None,

        "metadata_history":
            metadata_history
            if isinstance(
                metadata_history,
                dict
            )
            else {},

        "saved_at":
            now().isoformat()
    }

    write_json_atomic(
        global_merge_checkpoint_path(
            date,
            CURRENT_LANGUAGE
        ),
        data
    )


# ======================================================================
# Load Global Merge Checkpoint
# ======================================================================

def load_global_merge_checkpoint(
    date
):
    p = global_merge_checkpoint_path(
        date
    )

    if not p.exists():
        return None

    try:

        data = read_json(
            p,
            None
        )

    except Exception as e:

        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Checkpoint JSON读取失败，将忽略checkpoint。",
            str(e)
        )

        return None

    if not isinstance(
        data,
        dict
    ):
        return None

    if (
        data.get("version")
        not in ("6.5.3",)

        or data.get("date")
        != date

        or data.get("language")
        not in (
            None,
            CURRENT_LANGUAGE
        )
    ):

        return None

    saved_overlap = data.get(
        "window_overlap"
    )

    if (
        saved_overlap is not None
        and int(saved_overlap) != 0
    ):

        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "检测到旧版Overlap checkpoint，禁止恢复。",
            {
                "window_overlap":
                    saved_overlap
            }
        )

        return None

    return data


# ======================================================================
# Remove Checkpoint
# ======================================================================

def remove_global_merge_checkpoint(
    date,
    language=None
):
    p = global_merge_checkpoint_path(
        date,
        language
    )

    if p.exists():
        p.unlink()


# ======================================================================
# Checkpoint Validation
# ======================================================================

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

    if actual_original != expected_original:

        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Checkpoint原始Cluster Universe不一致。",
            {
                "checkpoint":
                    sorted(
                        actual_original
                    ),

                "expected":
                    sorted(
                        expected_original
                    )
            }
        )

        return False

    try:

        validate_global_cluster_membership(
            date,
            current,
            "CHECKPOINT MEMBERSHIP",
            expected_original_ids
        )

        validate_global_article_coverage(
            date,
            current,
            news_count,
            "CHECKPOINT ARTICLE COVERAGE"
        )

    except Exception:

        return False

    status = checkpoint.get(
        "status"
    )

    if status == "converged":
        return True

    if status not in (
        "running",
        "round_completed"
    ):
        return False

    if status == "round_completed":
        return True

    uf_data = checkpoint.get(
        "union_find"
    )

    if not isinstance(
        uf_data,
        dict
    ):

        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "running checkpoint缺少完整Union-Find状态。"
        )

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

    except Exception as e:

        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Union-Find checkpoint验证失败。",
            str(e)
        )

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

        or any(
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


# ======================================================================
# Global Merge
# ======================================================================

def merge_all_clusters(
    date,
    clusters,
    news_count
):
    current = clusters

    original_cluster_ids = sorted(
        str(
            c["cluster_id"]
        )
        for c in clusters
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "STAGE 1B — V6.5.3 GLOBAL EVENT MERGING"
    )

    print(
        "=" * 70
    )

    validate_global_cluster_membership(
        date,
        current,
        "STAGE 1B INITIAL",
        original_cluster_ids
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

    checkpoint_valid = validate_checkpoint(
        date,
        checkpoint,
        original_cluster_ids,
        news_count
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
            "\n♻️ 检测到有效 V6.5.3 "
            f"Global Merge checkpoint | "
            f"status={status} | "
            f"round={checkpoint.get('round')}"
        )

        print(
            f"   Restored clusters: "
            f"{len(current)}"
        )

        if status == "converged":

            final_current = current

        elif status == "round_completed":

            start_round = int(
                checkpoint[
                    "round"
                ]
            )

            completed_windows = []

            uf = None

            metadata_history = {}

            print(
                f"   ▶️ 从下一Round "
                f"{start_round} 开始"
            )

        else:

            start_round = int(
                checkpoint[
                    "round"
                ]
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

            print(
                f"   Completed windows: "
                f"{completed_windows}"
            )

            print(
                f"   ▶️ 从 Window "
                f"{max(completed_windows, default=0) + 1} "
                f"继续"
            )

    else:

        start_round = 1

        completed_windows = []

        uf = None

        metadata_history = {}

        print(
            "\n🆕 未检测到可恢复的"
            "V6.5.3 checkpoint"
        )

    if final_current is None:

        rnd = start_round

        while True:

            before = len(
                current
            )

            print(
                f"\nGLOBAL MERGE ROUND "
                f"{rnd} | Input Clusters: "
                f"{before}"
            )

            if before <= 1:

                print(
                    "🟢 GLOBAL MERGE CONVERGED "
                    "| only one Cluster remains"
                )

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
                and rnd == start_round
                and checkpoint
                and checkpoint.get(
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

            print(
                f"Windows: {window_count} | "
                f"Size: {GLOBAL_MERGE_WINDOW_SIZE} | "
                f"Overlap: {GLOBAL_MERGE_OVERLAP}"
            )

            round_records = []

            for wi in range(
                next_window,
                window_count + 1
            ):

                w = windows[
                    wi - 1
                ]

                print(
                    f"🔹 Window "
                    f"{wi}/{window_count} | "
                    f"size={len(w)}"
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

                round_records.extend(
                    records
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

                print(
                    f"   💾 Window {wi} "
                    f"checkpoint saved"
                )

            components = uf.components()

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

            if not actual_merge_happened:

                print(
                    "   ℹ️ 本轮没有发生任何"
                    "实际Cluster合并"
                )

                validate_global_cluster_membership(
                    date,
                    current,
                    f"STAGE 1B ROUND "
                    f"{rnd} NO-MERGE",
                    original_cluster_ids
                )

                validate_global_article_coverage(
                    date,
                    current,
                    news_count,
                    f"STAGE 1B ROUND "
                    f"{rnd} NO-MERGE"
                )

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

                print(
                    "🟢 GLOBAL MERGE CONVERGED"
                )

                final_current = current

                break

            print(
                f"   🔗 Actual merges: "
                f"{before - after}"
            )

            merged = rebuild_global_clusters(
                current,
                uf,
                metadata_history
            )

            validate_global_cluster_membership(
                date,
                merged,
                f"STAGE 1B ROUND {rnd}",
                original_cluster_ids
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

            print(
                f"   💾 Round {rnd} "
                "completed checkpoint saved | "
                f"next_round={rnd + 1}"
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
        original_cluster_ids
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
                c["article_indexes"]
            )
            if c["article_indexes"]
            else 10**12
    )

    final = []

    for c in ordered:

        final.append({
            "event_id":
                str(
                    c["cluster_id"]
                ),

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
                            c["article_indexes"]
                        )
                    )
                )
        })

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

    existing = (
        load_global_merge_checkpoint(
            date
        )
        or {}
    )

    if existing.get(
        "status"
    ) == "converged":
        pass

    return final


# ======================================================================
# Save Merged Clusters
# ======================================================================

def save_merged_clusters(
    date,
    language,
    clusters
):
    write_json_atomic(
        merged_clusters_path(
            date,
            language
        ),
        {
            "version":
                "6.5.3",

            "date":
                str(date),

            "language":
                normalize_language(
                    language
                ),

            "clusters":
                clusters,

            "saved_at":
                now().isoformat()
        }
    )


# ======================================================================
# Load Merged Clusters
# ======================================================================

def load_merged_clusters(
    date,
    language,
    news_count
):
    p = merged_clusters_path(
        date,
        language
    )

    if not p.exists():
        return None

    data = read_json(
        p,
        None
    )

    clusters = (
        data.get(
            "clusters"
        )
        if isinstance(
            data,
            dict
        )
        else None
    )

    if (
        not isinstance(
            clusters,
            list
        )
        or not clusters
    ):
        return None

    try:

        validate_global_cluster_membership(
            date,
            clusters,
            "TASK 2 SAVED",
            None
        )

        validate_global_article_coverage(
            date,
            clusters,
            news_count,
            "TASK 2 SAVED"
        )

    except Exception:

        return None

    return clusters


# ======================================================================
# TASK 2
# ======================================================================

def run_task_2(
    date,
    language
):
    global CURRENT_LANGUAGE

    CURRENT_LANGUAGE = normalize_language(
        language
    )

    initial_path = (
        initial_clusters_path(
            date,
            CURRENT_LANGUAGE
        )
    )

    if not initial_path.exists():

        raise RuntimeError(
            f"❌ TASK 2找不到TASK 1结果："
            f"{initial_path}"
        )

    news = load_all_enriched_news(
        date,
        CURRENT_LANGUAGE
    )

    existing = load_merged_clusters(
        date,
        CURRENT_LANGUAGE,
        len(news)
    )

    if existing is not None:

        print(
            f"♻️ TASK 2: reuse valid merged clusters | "
            f"{date}/{CURRENT_LANGUAGE} | "
            f"clusters={len(existing)}"
        )

        return existing

    data = read_json(
        initial_path,
        None
    )

    initial = (
        data.get(
            "clusters"
        )
        if isinstance(
            data,
            dict
        )
        else None
    )

    if (
        not isinstance(
            initial,
            list
        )
        or not initial
    ):

        raise RuntimeError(
            "❌ TASK 1结果无效"
        )

    validate_global_article_coverage(
        date,
        initial,
        len(news),
        "TASK 2 INITIAL"
    )

    final = merge_all_clusters(
        date,
        initial,
        len(news)
    )

    save_merged_clusters(
        date,
        CURRENT_LANGUAGE,
        final
    )

    remove_global_merge_checkpoint(
        date,
        CURRENT_LANGUAGE
    )

    print(
        f"✅ TASK 2 COMPLETE | "
        f"{date}/{CURRENT_LANGUAGE} | "
        f"clusters={len(final)}"
    )

    return final


# ======================================================================
# MAIN
# ======================================================================

def main():

    ap = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 2 - "
            "Global Merge V6.5.3"
        )
    )

    ap.add_argument(
        "--date",
        required=True
    )

    ap.add_argument(
        "--language",
        choices=[
            "EN",
            "ZH"
        ],
        required=True
    )

    args = ap.parse_args()

    run_task_2(
        args.date,
        args.language
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
