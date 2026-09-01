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

# Shared infrastructure from knowledge_common.py.
# Task 1 keeps its own cluster-specific validation and Global-ID repair logic.
from knowledge_common import (
    call_ai,
    create_global_cluster_registry,
    load_all_enriched_news,
    log_conflict,
    parse_ai_json,
    read_json,
    write_json_atomic,
)

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

EVENT_UNITS_SUFFIX = "EventUnit"
EVENT_INDEX_FILE = "_event_index.json"
EVENT_UNITS_COMPLETE_FILE = "_COMPLETE"
SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"
GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"
INITIAL_CLUSTERS_FILE = "_initial_clusters.json"
MERGED_CLUSTERS_FILE = "_merged_clusters.json"

AGNES_BASE_URL = os.getenv("AI_BASE_URL", "https://api.agnes-ai.cn/v1").rstrip("/")
AGNES_MODEL = os.getenv("AI_MODEL", "agnes-2.5-flash")
AGNES_API_KEY_ENV = "AGNES_API_KEY"

DEFAULT_TEMPERATURE = 0.3
AI_TIMEOUT = 180
AI_REQUEST_THROTTLE_SECONDS = 1.5
AI_MAX_429_RETRIES = 5
AI_429_BACKOFF_BASE = 10
AI_429_BACKOFF_MAX = 180
AI_429_JITTER_MAX = 3
_LAST_AI_REQUEST_TIME = 0.0

AGGREGATION_BATCH_SIZE = 30
GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"
GLOBAL_MERGE_WINDOW_SIZE = 30
GLOBAL_MERGE_OVERLAP = 0
MAX_ARTICLES_PER_EVENT_CONTEXT = 30
ARTICLE_CLUSTER_CONTENT_LIMIT = 3500
ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000
CLUSTER_REPAIR_ATTEMPTS = 2
RECOVERY_BATCH_SIZES = (30, 15, 8, 4, 2, 1)
BEIJING_TZ = ZoneInfo("Asia/Shanghai")
SUPPORTED_LANGUAGES = ("EN", "ZH")
CURRENT_LANGUAGE = None

def normalize_language(language):
    value = str(language or "").strip().upper()
    if value not in SUPPORTED_LANGUAGES:
        raise RuntimeError(f"❌ 不支持的语言：{language}")
    return value

def now():
    return datetime.now(BEIJING_TZ)

def event_units_root(date):
    return RAW_NEWS / f"{date}-EventUnit"

def language_dir(date, language=None):
    if language is None:
        language = getattr(sys.modules[__name__], "CURRENT_LANGUAGE", None)
    lang = normalize_language(language).lower()
    return event_units_root(date) / lang

def event_units_dir(date, language=None):
    return language_dir(date, language) / "event_units"

def articles_dir(date, language=None):
    return language_dir(date, language) / "articles"

def conflict_log_path(date):
    return LOGS / f"{date}_event_aggregation_conflicts.log"

def global_merge_checkpoint_path(date, language=None):
    return event_units_dir(date, language) / GLOBAL_MERGE_CHECKPOINT_FILE

def initial_clusters_path(date, language=None):
    return language_dir(date, language) / INITIAL_CLUSTERS_FILE

def merged_clusters_path(date, language=None):
    return language_dir(date, language) / MERGED_CLUSTERS_FILE

def write_text_atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass
        raise


def build_article_digest(item, index):
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


def inspect_cluster_assignment(clusters, expected_indexes):
    expected = set(map(int, expected_indexes))
    occ, malformed = {}, []

    for pos, c in enumerate(clusters, 1):
        if not isinstance(c, dict):
            malformed.append(
                f"cluster[{pos}]不是对象"
            )
            continue

        ids = c.get("article_indexes")

        if not isinstance(ids, list):
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
            occ.setdefault(i, []).append(pos)

    duplicate = {
        i: p for i, p in occ.items()
        if len(p) > 1
    }
    actual = set(occ)

    return {
        "duplicate": duplicate,
        "missing": sorted(expected - actual),
        "extra": sorted(actual - expected),
        "malformed": malformed
    }


def valid_issues(i):
    return not any([
        i["duplicate"],
        i["missing"],
        i["extra"],
        i["malformed"]
    ])


def normalize_clusters(cs):
    out = []
    for c in cs:
        if not isinstance(c, dict):
            out.append(c)
            continue

        d = dict(c)
        ids = d.get("article_indexes", [])

        if isinstance(ids, list):
            d["article_indexes"] = [
                int(x)
                if str(x).lstrip("-").isdigit()
                else x
                for x in ids
            ]

        out.append(d)

    return out


def cluster_news_batch(date, items, indexes):
    expected = [int(x) for x in indexes]

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
- cluster_id 只是本批次 Local Cluster ID，例如 C001、C002；不要生成 EVT-/REC-/GM- 等Global ID。
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

    clusters = data.get("clusters")

    if not isinstance(clusters, list):
        raise RuntimeError(
            f"❌ {date} 第一轮聚类结果缺少clusters"
        )

    return normalize_clusters(clusters)


def repair_cluster_news_batch(
    date,
    items,
    indexes,
    broken,
    issues,
    attempt
):
    expected = [int(x) for x in indexes]

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
3. Missing=0；
4. Duplicate=0；
5. Extra=0；
6. 不得遗漏任何ARTICLE；
7. 只输出JSON，不要解释。

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

    clusters = data.get("clusters")

    if not isinstance(clusters, list):
        raise RuntimeError(
            "❌ 聚类修复结果缺少clusters"
        )

    return normalize_clusters(clusters)


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


def _safe_covered_indexes(
    clusters,
    expected_indexes
):
    """
    只有不存在 Duplicate / Extra / Malformed 时，
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
        int(x) for x in expected_indexes
    }
    actual = set()

    for cluster in clusters:
        for value in cluster.get(
            "article_indexes",
            []
        ):
            actual.add(int(value))

    return sorted(
        actual & expected
    )


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
    Missing-only 可以安全隔离Missing。
    Duplicate/Extra/Malformed必须整批隔离。
    AI异常不再直接终止整个任务。
    """
    expected = [
        int(x) for x in indexes
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

        # Missing-only：安全保留已经唯一出现的文章。
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
                    f"{len(safe)} 篇，隔离 "
                    f"{len(unresolved)} 篇：{unresolved}"
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
        # 这一批整体隔离。
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
        # 429耗尽、网络、JSON等异常：
        # 本批隔离，不让整天任务结束。
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


def _global_id_date_token(date):
    """Return the canonical YYYYMMDD token used by Global Cluster IDs."""
    value = str(date).strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise RuntimeError(f"❌ 非法日期格式：{date}；Global ID要求YYYYMMDD对应日期")
    return value.replace("-", "")


def _canonical_global_cluster_id(date, sequence):
    """Canonical Global Cluster ID: EVT-YYYYMMDD-000001."""
    if int(sequence) < 1:
        raise RuntimeError(f"❌ {date} Global Cluster Registry sequence非法：{sequence}")
    return f"EVT-{_global_id_date_token(date)}-{int(sequence):06d}"


def _repair_registry_global_ids(date, registry):
    """
    Repair legacy registry entries whose IDs used EVT-YYYY-MM-DD-XXXXXX.

    The current V6.5.3 contract is EVT-YYYYMMDD-XXXXXX.  A failed run may
    have already persisted legacy IDs before validation rejected them, so the
    registry must be normalized before Task 1 allocates another ID.
    """
    changed = False
    registered = registry.get("registered", [])
    if not isinstance(registered, list):
        raise RuntimeError(f"❌ {date} Global Cluster Registry registered异常")

    canonical_re = re.compile(r"^EVT-\d{8}-\d{6}$")
    legacy_re = re.compile(r"^EVT-(\d{4})-(\d{2})-(\d{2})-(\d{6})$")

    for entry in registered:
        if not isinstance(entry, dict):
            raise RuntimeError(f"❌ {date} Global Cluster Registry存在非法记录")
        gid = str(entry.get("global_cluster_id", "")).strip()
        if canonical_re.fullmatch(gid):
            continue
        m = legacy_re.fullmatch(gid)
        if m:
            entry["global_cluster_id"] = (
                f"EVT-{m.group(1)}{m.group(2)}{m.group(3)}-{m.group(4)}"
            )
            changed = True
        else:
            raise RuntimeError(
                f"❌ {date} Global Cluster Registry存在无法修复的Global ID：{gid}"
            )

    # next_sequence must always be strictly greater than every registered ID.
    max_seq = 0
    for entry in registered:
        gid = str(entry.get("global_cluster_id", "")).strip()
        m = re.fullmatch(r"EVT-\d{8}-(\d{6})", gid)
        if m:
            max_seq = max(max_seq, int(m.group(1)))

    next_sequence = int(registry.get("next_sequence", 1))
    if next_sequence <= max_seq:
        registry["next_sequence"] = max_seq + 1
        changed = True

    if changed:
        _persist_task1_registry(date, registry)
        print(f"   🔧 Global Registry已修复为V6.5.3 canonical Global ID格式 | next_sequence={registry['next_sequence']}")

    return registry


def _persist_task1_registry(date, registry):
    """Persist the registry at the real date path without legacy ID generation."""
    write_json_atomic(
        global_cluster_registry_path(date),
        {
            "version": "6.5.3",
            "date": str(date),
            "next_sequence": int(registry["next_sequence"]),
            "registered": registry["registered"],
            "saved_at": now().isoformat(),
        },
    )


def _register_global_cluster_ids(date, clusters, registry, source):
    """
    Task 1 Global-ID allocator.

    IMPORTANT: knowledge_common._register_global_cluster_ids() in the older
    shared file generated EVT-YYYY-MM-DD-XXXXXX, while the V6.5.3 validator
    requires EVT-YYYYMMDD-XXXXXX.  Task 1 therefore allocates IDs here and
    writes the registry to the correct YYYY-MM-DD directory.
    """
    out = []
    for c in clusters:
        d = dict(c)
        local_id = str(
            d.get("local_cluster_id") or d.get("cluster_id") or ""
        ).strip()
        if not local_id:
            raise RuntimeError(
                f"❌ {date} Global Registry收到空Local Cluster ID"
            )

        seq = int(registry["next_sequence"])
        global_id = _canonical_global_cluster_id(date, seq)
        registry["next_sequence"] = seq + 1

        d["local_cluster_id"] = local_id
        d["cluster_id"] = global_id
        d["member_cluster_ids"] = [global_id]
        d["global_id_source"] = "python_global_registry"
        d["global_registry_source"] = source

        registry["registered"].append({
            "global_cluster_id": global_id,
            "local_cluster_id": local_id,
            "source": source,
            "article_indexes": sorted(
                set(int(x) for x in d.get("article_indexes", []))
            ),
        })
        out.append(d)

    _persist_task1_registry(date, registry)
    return out


def _make_cluster_records(batch_identifier, clusters):
    """只建立 Local Cluster；绝不在这里生成 Global ID。"""
    out = []
    for c in clusters:
        indexes = sorted(set(int(x) for x in c.get("article_indexes", [])))
        if not indexes:
            continue
        local_id = str(c.get("cluster_id", "C001")).strip()
        out.append({
            "cluster_id": local_id,
            "local_cluster_id": local_id,
            "event_title": c.get("event_title", "未命名事件"),
            "event_reason": c.get("event_reason", ""),
            "article_indexes": indexes,
            "batch_identifier": batch_identifier
        })
    return out


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

    local_records = _make_cluster_records(batch_no, clusters)
    allc.extend(_register_global_cluster_ids(date, local_records, registry, context))


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
                "cluster_id": f"C{index:03d}",
                "article_indexes": [index],
                "event_title": (
                    title[:120]
                    if title
                    else "未命名事件"
                ),
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
            recovered.extend(clusters)

        elif status == "partial":
            safe = _safe_covered_indexes(
                clusters,
                sub_indexes
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
                    item["article_indexes"] = (
                        sorted(set(ids))
                    )
                    safe_clusters.append(item)

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
        sorted(set(pending))
    )


def build_initial_clusters(date, news, registry=None):
    allc = []
    total = len(news)
    if registry is None:
        registry = read_json(global_cluster_registry_path(date), None)
        if not isinstance(registry, dict):
            registry = create_global_cluster_registry(date)
            _persist_task1_registry(date, registry)

    print("\n" + "=" * 70)
    print(
        "STAGE 1A — AI EVENT CLUSTERING V6.5.3"
    )
    print("=" * 70)
    print(f"Input Enriched News: {total}")
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
                    item["article_indexes"] = (
                        sorted(set(ids))
                    )
                    safe_clusters.append(item)

            if safe_clusters:
                validate_cluster_coverage(
                    safe_clusters,
                    safe,
                    f"{date} Batch "
                    f"{normal_batch_no} SAFE PART",
                    date
                )

                local_records = _make_cluster_records(normal_batch_no, safe_clusters)
                allc.extend(_register_global_cluster_ids(
                    date, local_records, registry,
                    f"Batch {normal_batch_no} SAFE PART"
                ))

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

        local_records = _make_cluster_records(
            f"RECOVERY PASS {pass_no}", recovered
        )
        allc.extend(_register_global_cluster_ids(
            date, local_records, registry, f"Recovery Pass {pass_no}"
        ))

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
                    sorted(set(pending))
            }
        )

        raise RuntimeError(
            "❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE："
            f"{sorted(set(pending))}"
        )

    validate_cluster_coverage(
        allc,
        range(1, total + 1),
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

def validate_initial_clusters_file(date, clusters, news_count, language):
    if not isinstance(clusters,list) or not clusters:
        return False
    try:
        validate_cluster_coverage(clusters, range(1,news_count+1), f"{date} {language} INITIAL FILE", date)
        validate_global_cluster_membership(date, clusters, "INITIAL CLUSTERS", [c["cluster_id"] for c in clusters])
    except Exception:
        return False
    return True


def save_initial_clusters(date, language, clusters):
    write_json_atomic(initial_clusters_path(date, language), {
        "version":"6.5.3", "date":str(date), "language":normalize_language(language), "clusters":clusters, "saved_at":now().isoformat()
    })


def load_initial_clusters(date, language, news_count):
    p=initial_clusters_path(date, language)
    if not p.exists():
        return None
    data=read_json(p,None)
    clusters=data.get("clusters") if isinstance(data,dict) else None
    if not validate_initial_clusters_file(date,clusters,news_count,language):
        return None
    return clusters


def run_task_1(date, language):
    lang=normalize_language(language)
    root=language_dir(date,lang); root.mkdir(parents=True,exist_ok=True)
    articles_dir(date,lang).mkdir(parents=True,exist_ok=True)
    event_units_dir(date,lang).mkdir(parents=True,exist_ok=True)
    news=load_all_enriched_news(date,lang)
    existing=load_initial_clusters(date,lang,len(news))
    if existing is not None:
        print(f"♻️ TASK 1: reuse valid initial clusters | {date}/{lang} | clusters={len(existing)}")
        return existing
    registry_file=global_cluster_registry_path(date)
    registry=read_json(registry_file,None) if registry_file.exists() else None
    if not isinstance(registry,dict) or registry.get("date")!=str(date):
        registry=create_global_cluster_registry(date)
        persist_global_cluster_registry(date,registry)
    else:
        validate_registry_basic(date,registry)
        registry=_repair_registry_global_ids(date,registry)
    clusters=build_initial_clusters(date,news,registry=registry)
    validate_global_cluster_membership(date,clusters,"TASK 1 FINAL",[c["cluster_id"] for c in clusters])
    validate_global_article_coverage(date,clusters,len(news),"TASK 1 FINAL")
    save_initial_clusters(date,lang,clusters)
    print(f"✅ TASK 1 COMPLETE | {date}/{lang} | articles={len(news)} | clusters={len(clusters)}")
    return clusters


def validate_registry_basic(date,registry):
    if not isinstance(registry,dict) or registry.get("date")!=str(date):
        raise RuntimeError(f"❌ {date} Global Cluster Registry异常")
    if not isinstance(registry.get("next_sequence"),int) or registry["next_sequence"]<1:
        raise RuntimeError(f"❌ {date} Global Cluster Registry next_sequence异常")
    if not isinstance(registry.get("registered"),list):
        raise RuntimeError(f"❌ {date} Global Cluster Registry registered异常")


def validate_global_cluster_membership(date,clusters,context,expected_original_ids=None):
    seen_current=set(); seen_original=set(); malformed=[]; dupc=[]; dupo=[]
    for pos,c in enumerate(clusters,1):
        if not isinstance(c,dict): malformed.append(f"cluster[{pos}]不是对象"); continue
        cid=str(c.get("cluster_id","")).strip()
        if not cid or not re.fullmatch(r"EVT-\d{8}-\d{6}",cid): malformed.append(f"cluster[{pos}]非法Global cluster_id：{cid}")
        elif cid in seen_current: dupc.append(cid)
        else: seen_current.add(cid)
        members=c.get("member_cluster_ids")
        if not isinstance(members,list) or not members: malformed.append(f"cluster[{pos}]member_cluster_ids无效"); continue
        for member in members:
            member=str(member).strip()
            if not member: malformed.append(f"cluster[{pos}]存在空member_cluster_id"); continue
            if member in seen_original: dupo.append(member)
            else: seen_original.add(member)
    expected=set(map(str,expected_original_ids or []))
    missing=sorted(expected-seen_original) if expected_original_ids is not None else []
    extra=sorted(seen_original-expected) if expected_original_ids is not None else []
    if malformed or dupc or dupo or missing or extra:
        log_conflict(date,context,"Global Cluster membership验证失败。",{"malformed":malformed,"duplicate_current":dupc,"duplicate_original":dupo,"missing_original":missing,"extra_original":extra})
        raise RuntimeError(f"❌ {context} Global Cluster membership异常")


def validate_global_article_coverage(date,clusters,news_count,context):
    allidx=[]; malformed=[]
    for pos,c in enumerate(clusters,1):
        ids=c.get("article_indexes") if isinstance(c,dict) else None
        if not isinstance(ids,list): malformed.append(f"cluster[{pos}] article_indexes不是数组"); continue
        for x in ids:
            try: allidx.append(int(x))
            except Exception: malformed.append(f"cluster[{pos}]非法ARTICLE：{x}")
    expected=set(range(1,news_count+1)); actual=set(allidx)
    dup=sorted({x for x in allidx if allidx.count(x)>1}); missing=sorted(expected-actual); extra=sorted(actual-expected)
    if dup or missing or extra or malformed:
        log_conflict(date,context,"Global Article coverage异常。",{"duplicate":dup,"missing":missing,"extra":extra,"malformed":malformed})
        raise RuntimeError(f"❌ {context} Article覆盖异常 Duplicate={dup} Missing={missing} Extra={extra} Malformed={malformed}")


def main():
    ap=argparse.ArgumentParser(description="748686 Knowledge Task 1 - Cluster V6.5.3")
    ap.add_argument("--date",required=True); ap.add_argument("--language",choices=["EN","ZH"],required=True)
    args=ap.parse_args(); run_task_1(args.date,args.language); return 0

if __name__=="__main__": sys.exit(main())
