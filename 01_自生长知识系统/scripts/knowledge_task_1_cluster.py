#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 1 — Cluster
V6.5.3

TASK 1职责
==========

    1. 读取当天指定语言的Enriched News
    2. 30篇一组进行AI事件聚类
    3. 验证ARTICLE完整覆盖
    4. Duplicate / Extra / Malformed自动隔离
    5. AI失败进入Recovery Queue
    6. Recovery：
           30
           15
           8
           4
           2
           1
    7. 最终生成Initial Clusters
    8. Global Cluster ID由Python Registry统一生成
    9. 写入_initial_clusters.json

LANGUAGE CONTRACT
=================

只允许：

    en
    zh

禁止任何大小写转换。

命令行：

    --language en
    --language zh


GLOBAL CLUSTER ID
=================

正式格式：

    EVT-YYYYMMDD-000001

例如：

    EVT-20260830-000001

AI只能产生：

    C001
    C002

AI禁止产生：

    EVT-
    REC-
    GM-
"""


from __future__ import annotations

import argparse
import json
import re
import sys

from pathlib import Path

from knowledge_common import (
    AGGREGATION_BATCH_SIZE,
    ARTICLE_CLUSTER_CONTENT_LIMIT,
    CLUSTER_REPAIR_ATTEMPTS
    if False
    else None,
)

from knowledge_common import (
    call_ai,
    create_global_cluster_registry,
    global_cluster_registry_path,
    load_all_enriched_news,
    log_conflict,
    parse_ai_json,
    persist_global_cluster_registry,
    read_json,
    register_global_cluster_ids,
    validate_global_article_coverage,
    validate_global_cluster_membership,
    validate_language,
    validate_registry_basic,
    write_json_atomic,
)


# ============================================================
# LOCAL TASK CONFIG
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

INITIAL_CLUSTERS_FILE = (
    "_initial_clusters.json"
)

RECOVERY_BATCH_SIZES = (
    30,
    15,
    8,
    4,
    2,
    1,
)

CLUSTER_REPAIR_ATTEMPTS = 2

SUPPORTED_LANGUAGES = (
    "en",
    "zh",
)


# ============================================================
# LANGUAGE
# ============================================================

def normalize_language(
    language,
):
    """
    严格语言验证。

    不进行任何大小写转换。
    """

    if not isinstance(
        language,
        str,
    ):
        raise RuntimeError(
            f"❌ language必须是小写字符串：{language!r}"
        )

    if language not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ language非法：{language!r}；"
            "只允许：en / zh"
        )

    return language


# ============================================================
# PATHS
# ============================================================

def event_units_root(
    date,
):
    return (
        RAW_NEWS /
        f"{date}-EventUnit"
    )


def language_dir(
    date,
    language,
):
    lang = normalize_language(
        language
    )

    return (
        event_units_root(date) /
        lang
    )


def event_units_dir(
    date,
    language,
):
    return (
        language_dir(
            date,
            language,
        ) /
        "event_units"
    )


def initial_clusters_path(
    date,
    language,
):
    return (
        language_dir(
            date,
            language,
        ) /
        INITIAL_CLUSTERS_FILE
    )


# ============================================================
# ARTICLE DIGEST
# ============================================================

def build_article_digest(
    item,
    index,
):
    metadata = item.get(
        "metadata",
        {}
    )

    body = str(
        item.get(
            "body",
            ""
        )
    )

    return f"""[ARTICLE {index}]
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
{body[:ARTICLE_CLUSTER_CONTENT_LIMIT]}"""


# ============================================================
# CLUSTER COVERAGE
# ============================================================

def inspect_cluster_assignment(
    clusters,
    expected_indexes,
):
    expected = set(
        map(
            int,
            expected_indexes,
        )
    )

    occurrences = {}

    malformed = []

    for pos, cluster in enumerate(
        clusters,
        1
    ):

        if not isinstance(
            cluster,
            dict,
        ):

            malformed.append(
                f"cluster[{pos}]不是对象"
            )

            continue

        ids = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            ids,
            list,
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

        for value in ids:

            try:
                index = int(value)

            except Exception:

                malformed.append(
                    f"cluster[{pos}]"
                    f"非法ARTICLE ID：{value}"
                )

                continue

            occurrences.setdefault(
                index,
                []
            ).append(
                pos
            )

    duplicate = {
        index: positions
        for index, positions
        in occurrences.items()
        if len(positions) > 1
    }

    actual = set(
        occurrences
    )

    return {
        "duplicate":
            duplicate,

        "missing":
            sorted(
                expected -
                actual
            ),

        "extra":
            sorted(
                actual -
                expected
            ),

        "malformed":
            malformed,
    }


def valid_issues(
    issues,
):
    return not any(
        [
            issues["duplicate"],
            issues["missing"],
            issues["extra"],
            issues["malformed"],
        ]
    )


def normalize_clusters(
    clusters,
):
    out = []

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict,
        ):

            out.append(
                cluster
            )

            continue

        item = dict(
            cluster
        )

        ids = item.get(
            "article_indexes",
            []
        )

        if isinstance(
            ids,
            list,
        ):

            normalized = []

            for value in ids:

                try:
                    normalized.append(
                        int(value)
                    )

                except Exception:
                    normalized.append(
                        value
                    )

            item[
                "article_indexes"
            ] = normalized

        out.append(
            item
        )

    return out


# ============================================================
# AI CLUSTER
# ============================================================

def cluster_news_batch(
    date,
    items,
    indexes,
):
    expected = [
        int(value)
        for value in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[pos],
        )
        for pos, item
        in enumerate(items)
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.3第一层事件聚类。

日期：
{date}

{joined}

任务：
识别哪些新闻属于同一个现实世界的具体事件。

规则：

1. 支持跨来源、跨语言判断。
2. 不要因为关键词相同就强行合并。
3. 不要因为公司、国家、行业相同就强行合并。
4. 无法确定时宁可分开。
5. 同一个现实世界具体事件应该合并。
6. 每一篇ARTICLE必须且只能属于一个cluster。
7. 无法与其他文章合并的ARTICLE必须单独成为cluster。

ARTICLE覆盖要求：

{json.dumps(expected, ensure_ascii=False)}

重要输出限制：

- cluster_id只能是Local Cluster ID，例如C001、C002。
- 不要生成EVT- ID。
- 不要生成REC- ID。
- 不要生成GM- ID。
- Global Cluster ID由Python Registry统一生成。
- event_title尽量短。
- event_reason尽量短，一句话即可。
- 不要复制文章正文。
- 只输出JSON。
- 不要Markdown。
- 不要解释。

输出格式：

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
                "只输出合法JSON。"
            ),
            0,
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类",
        )

    except RuntimeError as first_error:

        compact_prompt = f"""748686 V6.5.3 新闻事件聚类JSON修复。

日期：
{date}

ARTICLE范围：
{json.dumps(expected)}

文章：
{joined}

重新聚类。

严格要求：

1. 每个ARTICLE恰好出现一次。
2. 同一具体现实事件合并。
3. 不同事件分开。
4. 不能确定宁可分开。
5. cluster_id只能是C001、C002等Local ID。
6. 禁止EVT-。
7. 禁止REC-。
8. 禁止GM-。
9. event_title不超过40字。
10. event_reason不超过80字。
11. 不得输出文章正文。
12. 只输出JSON。
13. 不要代码围栏。
14. 不要解释。

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
                "只输出合法JSON，绝不输出解释。"
            ),
            0,
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类紧凑重试",
        )

    clusters = data.get(
        "clusters"
    )

    if not isinstance(
        clusters,
        list,
    ):

        raise RuntimeError(
            f"❌ {date} 第一轮聚类结果缺少clusters"
        )

    return normalize_clusters(
        clusters
    )


# ============================================================
# CLUSTER REPAIR
# ============================================================

def repair_cluster_news_batch(
    date,
    items,
    indexes,
    broken,
    issues,
    attempt,
):
    expected = [
        int(value)
        for value in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[pos],
        )
        for pos, item
        in enumerate(items)
    )

    prompt = f"""修复748686 V6.5.3 ARTICLE覆盖冲突。

日期：
{date}

第{attempt}次修复。

真实ARTICLE：

{json.dumps(expected, ensure_ascii=False)}

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

1. cluster_id只能是Local Cluster ID。
2. 例如C001、C002。
3. 不得生成EVT-。
4. 不得生成REC-。
5. 不得生成GM-。
6. 同事件合并。
7. 不同事件分开。
8. 每篇ARTICLE恰好一次。
9. Missing必须为0。
10. Duplicate必须为0。
11. Extra必须为0。
12. Malformed必须为0。
13. 不得遗漏任何ARTICLE。
14. 只输出JSON。
15. 不要解释。

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
                "只输出合法JSON。"
            ),
            0,
        ),
        f"{date} 聚类冲突修复 #{attempt}",
    )

    clusters = data.get(
        "clusters"
    )

    if not isinstance(
        clusters,
        list,
    ):

        raise RuntimeError(
            "❌ 聚类修复结果缺少clusters"
        )

    return normalize_clusters(
        clusters
    )


# ============================================================
# VALIDATION
# ============================================================

def validate_cluster_coverage(
    clusters,
    expected,
    context,
    date=None,
):
    issues = inspect_cluster_assignment(
        clusters,
        expected,
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
            issues,
        )

    raise RuntimeError(
        f"❌ {context} 聚类覆盖失败：{issues}"
    )


def _safe_covered_indexes(
    clusters,
    expected_indexes,
):
    """
    只有不存在：

        Duplicate
        Extra
        Malformed

    时，才允许保留安全覆盖部分。
    """

    issues = inspect_cluster_assignment(
        clusters,
        expected_indexes,
    )

    if (
        issues["duplicate"]
        or issues["extra"]
        or issues["malformed"]
    ):

        return []

    expected = {
        int(value)
        for value
        in expected_indexes
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
        actual &
        expected
    )


# ============================================================
# BATCH WITH REPAIR
# ============================================================

def cluster_news_batch_with_repair(
    date,
    items,
    indexes,
    batch_label,
):
    """
    返回：

        ("complete", clusters, [])

        ("partial", clusters, missing_indexes)

        ("failed", [], expected_indexes)

    V6.5.3：

        Missing-only
            →
        安全隔离Missing

        Duplicate / Extra / Malformed
            →
        整批隔离

        AI异常
            →
        整批进入Recovery Queue
    """

    expected = [
        int(value)
        for value in indexes
    ]

    clusters = None

    try:

        clusters = cluster_news_batch(
            date,
            items,
            expected,
        )

        issues = inspect_cluster_assignment(
            clusters,
            expected,
        )

        if valid_issues(
            issues
        ):

            return (
                "complete",
                clusters,
                [],
            )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            (
                "AI第一次聚类返回非法ARTICLE归属，"
                "启动自动修复。"
            ),
            {
                "issues":
                    issues,
                "clusters":
                    clusters,
            },
        )

        for attempt in range(
            1,
            CLUSTER_REPAIR_ATTEMPTS + 1,
        ):

            try:

                clusters = (
                    repair_cluster_news_batch(
                        date,
                        items,
                        expected,
                        clusters,
                        issues,
                        attempt,
                    )
                )

                issues = inspect_cluster_assignment(
                    clusters,
                    expected,
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
                        [],
                    )

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    f"第{attempt}次聚类冲突修复仍然失败。",
                    {
                        "issues":
                            issues,
                        "clusters":
                            clusters,
                    },
                )

            except Exception as repair_error:

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    f"第{attempt}次聚类修复请求/解析失败。",
                    str(
                        repair_error
                    ),
                )

        final_issues = inspect_cluster_assignment(
            clusters or [],
            expected,
        )

        # ----------------------------------------------------
        # Missing-only
        # ----------------------------------------------------

        if (
            final_issues["missing"]
            and not final_issues["duplicate"]
            and not final_issues["extra"]
            and not final_issues["malformed"]
        ):

            safe = _safe_covered_indexes(
                clusters,
                expected,
            )

            unresolved = sorted(
                set(expected) -
                set(safe)
            )

            if safe and unresolved:

                print(
                    "   🟡 Missing-only：安全保留 "
                    f"{len(safe)} 篇，隔离 "
                    f"{len(unresolved)} 篇："
                    f"{unresolved}"
                )

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    (
                        "修复失败，但仅存在Missing；"
                        "安全覆盖部分保留，"
                        "Missing进入Recovery Queue。"
                    ),
                    {
                        "safe_covered":
                            safe,
                        "recovery_queue":
                            unresolved,
                        "issues":
                            final_issues,
                    },
                )

                return (
                    "partial",
                    clusters,
                    unresolved,
                )

        # ----------------------------------------------------
        # Unsafe batch
        # ----------------------------------------------------

        print(
            "   🔴 Batch结果不安全，"
            "整批进入Recovery Queue："
            f"{expected}"
        )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            (
                "自动修复失败；整批隔离，"
                "防止错误结果污染Global Merge。"
            ),
            {
                "issues":
                    final_issues,
                "recovery_queue":
                    expected,
            },
        )

        return (
            "failed",
            [],
            expected,
        )

    except Exception as e:

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            (
                "本批AI异常；整批隔离进入"
                "Recovery Queue，不终止任务。"
            ),
            str(e),
        )

        print(
            "   🔴 AI exception isolated into "
            f"Recovery Queue: {expected}"
        )

        return (
            "failed",
            [],
            expected,
        )


# ============================================================
# CLUSTER RECORDS
# ============================================================

def _make_cluster_records(
    batch_identifier,
    clusters,
):
    """
    这里只建立Local Cluster。

    Global ID统一交给Common Registry。
    """

    out = []

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict,
        ):
            continue

        indexes = []

        for value in cluster.get(
            "article_indexes",
            []
        ):

            try:
                indexes.append(
                    int(value)
                )
            except Exception:
                pass

        indexes = sorted(
            set(indexes)
        )

        if not indexes:
            continue

        local_id = str(
            cluster.get(
                "cluster_id",
                "C001",
            )
        ).strip()

        if not local_id:

            raise RuntimeError(
                "❌ Cluster缺少Local Cluster ID"
            )

        out.append(
            {
                "cluster_id":
                    local_id,

                "local_cluster_id":
                    local_id,

                "event_title":
                    cluster.get(
                        "event_title",
                        "未命名事件",
                    ),

                "event_reason":
                    cluster.get(
                        "event_reason",
                        "",
                    ),

                "article_indexes":
                    indexes,

                "batch_identifier":
                    batch_identifier,
            }
        )

    return out


# ============================================================
# REGISTER SAFE CLUSTERS
# ============================================================

def _append_safe_clusters(
    all_clusters,
    clusters,
    batch_no,
    expected_indexes,
    date,
    context,
    registry,
):
    validate_cluster_coverage(
        clusters,
        expected_indexes,
        context,
        date,
    )

    local_records = _make_cluster_records(
        batch_no,
        clusters,
    )

    registered = register_global_cluster_ids(
        date,
        local_records,
        registry,
        context,
    )

    all_clusters.extend(
        registered
    )


# ============================================================
# RECOVERY PASS
# ============================================================

def _recovery_pass(
    date,
    news,
    indexes,
    recovery_pass_no,
    batch_size,
):
    indexes = sorted(
        set(
            int(value)
            for value in indexes
        )
    )

    sub_batches = [
        indexes[pos:pos + batch_size]
        for pos in range(
            0,
            len(indexes),
            batch_size,
        )
    ]

    recovered = []

    pending = []

    print(
        "\n🛠️ RECOVERY PASS "
        f"{recovery_pass_no} | "
        f"Articles={len(indexes)} | "
        f"BatchSize={batch_size} | "
        f"SubBatches={len(sub_batches)}"
    )

    for sub_no, sub_indexes in enumerate(
        sub_batches,
        1,
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

        # ----------------------------------------------------
        # Singleton
        # ----------------------------------------------------

        if len(
            sub_indexes
        ) == 1:

            index = sub_indexes[0]

            title = str(
                news[index - 1]
                .get(
                    "metadata",
                    {}
                )
                .get(
                    "title",
                    "未命名事件",
                )
            ).strip()

            recovered.append(
                {
                    "cluster_id":
                        f"C{index:03d}",

                    "article_indexes":
                        [index],

                    "event_title":
                        (
                            title[:120]
                            if title
                            else "未命名事件"
                        ),

                    "event_reason":
                        "该文章在恢复阶段作为独立事件单元保留。",
                }
            )

            print(
                "      🟢 Singleton安全保留："
                f"ARTICLE {index}"
            )

            continue

        # ----------------------------------------------------
        # AI Recovery
        # ----------------------------------------------------

        status, clusters, unresolved = (
            cluster_news_batch_with_repair(
                date,
                items,
                sub_indexes,
                label,
            )
        )

        if status == "complete":

            recovered.extend(
                clusters
            )

        elif status == "partial":

            safe = _safe_covered_indexes(
                clusters,
                sub_indexes,
            )

            safe_set = set(
                safe
            )

            safe_clusters = []

            for cluster in clusters:

                ids = []

                for value in cluster.get(
                    "article_indexes",
                    []
                ):

                    try:
                        index = int(value)
                    except Exception:
                        continue

                    if index in safe_set:
                        ids.append(
                            index
                        )

                if ids:

                    item = dict(
                        cluster
                    )

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
                    date,
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
        ),
    )


# ============================================================
# BUILD INITIAL CLUSTERS
# ============================================================

def build_initial_clusters(
    date,
    news,
    registry,
):
    all_clusters = []

    total = len(
        news
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
        "Normal Batch Size: "
        f"{AGGREGATION_BATCH_SIZE}"
    )

    print(
        "Failure Policy: isolate -> "
        "recovery queue -> "
        "30/15/8/4/2/1 -> singleton"
    )

    pending = []

    normal_batch_no = 0

    # ========================================================
    # NORMAL 30-ARTICLE PROCESSING
    # ========================================================

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE,
    ):

        normal_batch_no += 1

        end = min(
            start +
            AGGREGATION_BATCH_SIZE,
            total,
        )

        indexes = list(
            range(
                start + 1,
                end + 1,
            )
        )

        items = news[
            start:end
        ]

        print(
            "\n🔹 Cluster Batch "
            f"{normal_batch_no}: "
            f"{indexes[0]}-"
            f"{indexes[-1]}/"
            f"{total}"
        )

        status, clusters, unresolved = (
            cluster_news_batch_with_repair(
                date,
                items,
                indexes,
                f"CLUSTER BATCH {normal_batch_no}",
            )
        )

        # ----------------------------------------------------
        # Complete
        # ----------------------------------------------------

        if status == "complete":

            _append_safe_clusters(
                all_clusters,
                clusters,
                normal_batch_no,
                indexes,
                date,
                f"Batch {normal_batch_no}",
                registry,
            )

            print(
                "   Clusters generated: "
                f"{len(clusters)}"
            )

        # ----------------------------------------------------
        # Partial
        # ----------------------------------------------------

        elif status == "partial":

            safe = _safe_covered_indexes(
                clusters,
                indexes,
            )

            safe_set = set(
                safe
            )

            safe_clusters = []

            for cluster in clusters:

                ids = []

                for value in cluster.get(
                    "article_indexes",
                    []
                ):

                    try:
                        index = int(value)
                    except Exception:
                        continue

                    if index in safe_set:
                        ids.append(
                            index
                        )

                if ids:

                    item = dict(
                        cluster
                    )

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
                    f"{date} Batch "
                    f"{normal_batch_no} SAFE PART",
                    date,
                )

                local_records = (
                    _make_cluster_records(
                        normal_batch_no,
                        safe_clusters,
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
                            "SAFE PART"
                        ),
                    )
                )

                all_clusters.extend(
                    registered
                )

            pending.extend(
                unresolved
            )

            print(
                "   🟡 Safe clusters kept="
                f"{len(safe_clusters)} | "
                f"Pending={len(pending)}"
            )

        # ----------------------------------------------------
        # Failed
        # ----------------------------------------------------

        else:

            pending.extend(
                unresolved
            )

            print(
                "   🔴 Entire batch isolated | "
                f"Pending={len(pending)}"
            )

    # ========================================================
    # RECOVERY QUEUE
    # ========================================================

    for pass_no, batch_size in enumerate(
        RECOVERY_BATCH_SIZES,
        1,
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
            )
        )

        local_records = (
            _make_cluster_records(
                f"RECOVERY PASS {pass_no}",
                recovered,
            )
        )

        if local_records:

            registered = (
                register_global_cluster_ids(
                    date,
                    local_records,
                    registry,
                    f"Recovery Pass {pass_no}",
                )
            )

            all_clusters.extend(
                registered
            )

        pending.extend(
            unresolved
        )

        print(
            f"   Recovery Pass {pass_no}: "
            f"recovered={len(recovered)} | "
            f"still_pending={len(pending)}"
        )

    # ========================================================
    # FINAL SAFETY GATE
    # ========================================================

    if pending:

        log_conflict(
            date,
            "STAGE 1A / FINAL RECOVERY",
            (
                "Recovery Queue仍有未处理ARTICLE，"
                "禁止进入Global Merge。"
            ),
            {
                "pending_articles":
                    sorted(
                        set(pending)
                    )
            },
        )

        raise RuntimeError(
            "❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE："
            f"{sorted(set(pending))}"
        )

    # ========================================================
    # GLOBAL COVERAGE
    # ========================================================

    validate_global_article_coverage(
        date,
        all_clusters,
        total,
        "STAGE 1A GLOBAL",
    )

    validate_global_cluster_membership(
        date,
        all_clusters,
        "STAGE 1A INITIAL",
        [
            cluster[
                "cluster_id"
            ]
            for cluster in all_clusters
        ],
    )

    print(
        "\n✅ Initial Clusters: "
        f"{len(all_clusters)}"
    )

    print(
        "✅ ARTICLE Coverage: "
        f"{total}/{total}"
    )

    return all_clusters


# ============================================================
# INITIAL CLUSTER FILE
# ============================================================

def validate_initial_clusters_file(
    date,
    clusters,
    news_count,
    language,
):
    if (
        not isinstance(
            clusters,
            list,
        )
        or not clusters
    ):
        return False

    try:

        validate_global_article_coverage(
            date,
            clusters,
            news_count,
            f"{date} {language} INITIAL FILE",
        )

        validate_global_cluster_membership(
            date,
            clusters,
            "INITIAL CLUSTERS",
            [
                cluster[
                    "cluster_id"
                ]
                for cluster in clusters
                if isinstance(
                    cluster,
                    dict,
                )
            ],
        )

    except Exception:

        return False

    return True


def save_initial_clusters(
    date,
    language,
    clusters,
):
    lang = normalize_language(
        language
    )

    write_json_atomic(
        initial_clusters_path(
            date,
            lang,
        ),
        {
            "version":
                "6.5.3",

            "date":
                str(date),

            "language":
                lang,

            "clusters":
                clusters,

            "saved_at":
                __import__(
                    "knowledge_common"
                ).now().isoformat(),
        },
    )


def load_initial_clusters(
    date,
    language,
    news_count,
):
    lang = normalize_language(
        language
    )

    path = initial_clusters_path(
        date,
        lang,
    )

    if not path.exists():
        return None

    data = read_json(
        path,
        None,
    )

    clusters = (
        data.get(
            "clusters"
        )
        if isinstance(
            data,
            dict,
        )
        else None
    )

    if not validate_initial_clusters_file(
        date,
        clusters,
        news_count,
        lang,
    ):

        print(
            "   ⚠️ Existing "
            "_initial_clusters.json "
            "validation failed; "
            "rebuilding Task 1."
        )

        return None

    return clusters


# ============================================================
# TASK 1
# ============================================================

def run_task_1(
    date,
    language,
):
    lang = normalize_language(
        language
    )

    root = language_dir(
        date,
        lang,
    )

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    event_units_dir(
        date,
        lang,
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    news = load_all_enriched_news(
        date,
        lang,
    )

    print(
        "\n============================================================"
    )

    print(
        "TASK 1 — CLUSTER"
    )

    print(
        f"DATE     : {date}"
    )

    print(
        f"LANGUAGE : {lang}"
    )

    print(
        f"ENRICHED : {len(news)}"
    )

    print(
        "============================================================"
    )

    # --------------------------------------------------------
    # Reuse valid existing result
    # --------------------------------------------------------

    existing = load_initial_clusters(
        date,
        lang,
        len(news),
    )

    if existing is not None:

        print(
            "♻️ TASK 1: reuse valid "
            "initial clusters | "
            f"{date}/{lang} | "
            f"clusters={len(existing)}"
        )

        return existing

    # --------------------------------------------------------
    # Registry
    # --------------------------------------------------------

    registry_path = (
        global_cluster_registry_path(
            date
        )
    )

    registry = None

    if registry_path.exists():

        registry = read_json(
            registry_path,
            None,
        )

    if (
        not isinstance(
            registry,
            dict,
        )
        or registry.get(
            "date"
        ) != str(date)
    ):

        registry = (
            create_global_cluster_registry(
                date
            )
        )

        persist_global_cluster_registry(
            date,
            registry,
        )

    else:

        validate_registry_basic(
            date,
            registry,
        )

    # --------------------------------------------------------
    # Build
    # --------------------------------------------------------

    clusters = build_initial_clusters(
        date,
        news,
        registry,
    )

    # --------------------------------------------------------
    # Final validation
    # --------------------------------------------------------

    validate_global_cluster_membership(
        date,
        clusters,
        "TASK 1 FINAL",
        [
            cluster[
                "cluster_id"
            ]
            for cluster in clusters
        ],
    )

    validate_global_article_coverage(
        date,
        clusters,
        len(news),
        "TASK 1 FINAL",
    )

    save_initial_clusters(
        date,
        lang,
        clusters,
    )

    print(
        "\n✅ TASK 1 COMPLETE | "
        f"{date}/{lang} | "
        f"articles={len(news)} | "
        f"clusters={len(clusters)}"
    )

    return clusters


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 1 "
            "- Cluster V6.5.3"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
    )

    parser.add_argument(
        "--language",
        choices=[
            "en",
            "zh",
        ],
        required=True,
    )

    args = parser.parse_args()

    run_task_1(
        args.date,
        args.language,
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
