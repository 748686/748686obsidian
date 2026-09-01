#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 1 — Cluster
V6.5.3

职责：

    Enriched News
        ↓
    AI Local Clustering
        ↓
    Coverage Validation
        ↓
    Repair
        ↓
    Recovery Queue
        ↓
    Global Registry
        ↓
    Initial Clusters

本Task只负责：

    新闻 → Initial Clusters

本Task不负责：

    Global Merge
    EventUnit
    27 Skills
    Article Generation
    Knowledge Generation

LANGUAGE CONTRACT
=================

唯一合法：

    en
    zh

禁止：

    EN
    ZH
    En
    Zh

禁止任何大小写转换。

AI Local Cluster ID：

    C001
    C002
    C003

Global Cluster ID：

    EVT-YYYY-MM-DD-000001

Global ID只能由Python Global Registry产生。
"""


from __future__ import annotations

import argparse
import json
import re
import sys


# ============================================================
# COMMON IMPORT
# ============================================================

try:

    from knowledge_common import (
        AGGREGATION_BATCH_SIZE,
        ARTICLE_CLUSTER_CONTENT_LIMIT,
        INITIAL_CLUSTERS_FILE,
        RECOVERY_BATCH_SIZES,
        RAW_NEWS,

        create_global_cluster_registry,
        global_cluster_registry_path,
        initial_clusters_path,

        log_conflict,
        now,
        parse_ai_json,

        persist_global_cluster_registry,
        read_json,

        register_global_cluster_ids,

        validate_global_article_coverage,
        validate_global_cluster_membership,
        validate_language,

        write_json_atomic,

        call_ai,
    )

except ImportError as e:

    raise RuntimeError(
        "❌ 无法导入knowledge_common.py。"
        "请确认两个文件位于同一个scripts目录。"
    ) from e


# ============================================================
# CLUSTER REPAIR CONFIG
# ============================================================

CLUSTER_REPAIR_ATTEMPTS = 2


# ============================================================
# ENRICHED NEWS
# ============================================================

def load_all_enriched_news(
    date,
    language
):
    """
    读取指定日期、指定语言的全部Enriched新闻。
    """

    lang = validate_language(
        language
    )

    root = (
        RAW_NEWS
        /
        f"{date}-Enriched"
        /
        lang
    )

    if not root.exists():

        raise FileNotFoundError(
            f"没有找到 "
            f"{date}/{lang} Enriched目录："
            f"{root}"
        )

    files = sorted(
        root.rglob("*.md")
    )

    print(
        f"Enriched files: "
        f"{len(files)}"
    )

    if not files:

        raise RuntimeError(
            f"❌ {date}/{lang} 没有Enriched新闻"
        )

    items = []

    for path in files:

        content = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        metadata = {}

        body = content

        if content.startswith("---"):

            parts = content.split(
                "---",
                2
            )

            if len(parts) >= 3:

                for line in (
                    parts[1]
                    .strip()
                    .splitlines()
                ):

                    if ":" not in line:
                        continue

                    key, value = line.split(
                        ":",
                        1
                    )

                    metadata[
                        key.strip()
                    ] = (
                        value.strip()
                        .strip('"')
                        .strip("'")
                    )

                body = (
                    parts[2]
                    .lstrip()
                )

        title = str(
            metadata.get(
                "title",
                ""
            )
        ).strip()

        if not title:
            continue

        items.append(
            {
                "path": path,
                "metadata": metadata,
                "body": body,
                "content": content
            }
        )

    if not items:

        raise RuntimeError(
            f"❌ {date}/{lang} 没有有效Enriched新闻"
        )

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
    metadata = item[
        "metadata"
    ]

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
{item["body"][:ARTICLE_CLUSTER_CONTENT_LIMIT]}"""


# ============================================================
# CLUSTER INSPECTION
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

    occurrences = {}

    malformed = []

    for position, cluster in enumerate(
        clusters,
        1
    ):

        if not isinstance(
            cluster,
            dict
        ):

            malformed.append(
                f"cluster[{position}]不是对象"
            )

            continue

        ids = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            ids,
            list
        ):

            malformed.append(
                f"cluster[{position}] "
                "article_indexes不是数组"
            )

            continue

        if not ids:

            malformed.append(
                f"cluster[{position}]为空Cluster"
            )

            continue

        for value in ids:

            try:

                index = int(
                    value
                )

            except Exception:

                malformed.append(
                    f"cluster[{position}]"
                    f"非法ARTICLE ID：{value}"
                )

                continue

            occurrences.setdefault(
                index,
                []
            ).append(
                position
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
                expected - actual
            ),

        "extra":
            sorted(
                actual - expected
            ),

        "malformed":
            malformed
    }


def valid_issues(
    issues
):
    return not any(
        [
            issues["duplicate"],
            issues["missing"],
            issues["extra"],
            issues["malformed"]
        ]
    )


# ============================================================
# NORMALIZE
# ============================================================

def normalize_clusters(
    clusters
):
    output = []

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict
        ):

            output.append(
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
            list
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

        output.append(
            item
        )

    return output


# ============================================================
# SAFE COVERAGE
# ============================================================

def safe_covered_indexes(
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
# AI CLUSTERING
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
            expected[position]
        )
        for position, item
        in enumerate(items)
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.3第一层事件聚类。

日期：
{date}

{joined}

任务：

识别哪些新闻属于同一个现实世界的具体事件。

允许跨来源、跨语言进行事件判断。

不要因为以下因素相同就强行合并：

- 公司相同
- 国家相同
- 行业相同
- 人物相同
- 关键词相同

如果无法确定是否属于同一个具体事件：

宁可分开。

ARTICLE覆盖要求：

{json.dumps(expected, ensure_ascii=False)}

每篇ARTICLE：

必须且只能属于一个cluster。

无法与其他文章确定属于同一事件的ARTICLE：

必须单独成为cluster。

ID要求：

cluster_id只能是Local Cluster ID：

C001
C002
C003

绝对禁止：

EVT-
REC-
GM-

Global Cluster ID由Python Registry生成。

输出要求：

1. 只输出JSON；
2. 不要Markdown；
3. 不要解释；
4. 不要复制文章正文；
5. event_title尽量短；
6. event_reason一句话；
7. 每篇ARTICLE恰好一次。

输出：

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
            0
        )

        data = parse_ai_json(
            result,
            f"{date} 第一轮新闻聚类"
        )

    except RuntimeError as first_error:

        compact_prompt = f"""748686 V6.5.3新闻事件聚类JSON修复。

日期：
{date}

ARTICLE：
{json.dumps(expected, ensure_ascii=False)}

文章：

{joined}

重新完成聚类。

严格要求：

1. 每个ARTICLE恰好一次；
2. 同一具体现实事件合并；
3. 不同事件分开；
4. 无法确定时分开；
5. cluster_id只能是C001、C002等Local ID；
6. 禁止EVT-/REC-/GM-；
7. event_title不超过40字；
8. event_reason不超过80字；
9. 不输出文章正文；
10. 只输出JSON；
11. 不输出代码围栏；
12. 不解释。

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
            "启动紧凑JSON重试："
            f"{first_error}"
        )

        result = call_ai(
            compact_prompt,
            (
                "你是新闻聚类JSON修复器。"
                "只输出合法JSON。"
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


# ============================================================
# REPAIR
# ============================================================

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
            expected[position]
        )
        for position, item
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

1. cluster_id只能是Local Cluster ID；
2. 例如C001、C002；
3. 禁止EVT-/REC-/GM-；
4. 同一事件合并；
5. 不同事件分开；
6. 每篇ARTICLE恰好一次；
7. Missing=0；
8. Duplicate=0；
9. Extra=0；
10. 不得遗漏ARTICLE；
11. 只输出JSON；
12. 不解释。

输出：

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
                "只输出JSON。"
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


# ============================================================
# CLUSTER WITH REPAIR
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
            (
                "AI第一次聚类返回非法ARTICLE归属，"
                "启动自动修复。"
            ),
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
                    (
                        f"第{attempt}次聚类冲突修复"
                        "仍然失败。"
                    ),
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
                    (
                        f"第{attempt}次聚类修复"
                        "请求/解析失败。"
                    ),
                    str(
                        repair_error
                    )
                )

        final_issues = inspect_cluster_assignment(
            clusters or [],
            expected
        )

        # ------------------------------------------------------
        # Missing-only
        # ------------------------------------------------------

        if (
            final_issues["missing"]
            and not final_issues["duplicate"]
            and not final_issues["extra"]
            and not final_issues["malformed"]
        ):

            safe = safe_covered_indexes(
                clusters,
                expected
            )

            unresolved = sorted(
                set(expected)
                -
                set(safe)
            )

            if safe and unresolved:

                print(
                    f"   🟡 Missing-only："
                    f"安全保留{len(safe)}篇，"
                    f"隔离{len(unresolved)}篇："
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
                            final_issues
                    }
                )

                return (
                    "partial",
                    clusters,
                    unresolved
                )

        # ------------------------------------------------------
        # Unsafe
        # ------------------------------------------------------

        print(
            f"   🔴 Batch结果不安全，"
            f"整批进入Recovery Queue："
            f"{expected}"
        )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            (
                "自动修复失败；整批隔离，"
                "防止错误结果污染后续阶段。"
            ),
            {
                "issues":
                    final_issues,

                "recovery_queue":
                    expected
            }
        )

        return (
            "failed",
            [],
            expected
        )

    except Exception as error:

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            (
                "本批AI异常；"
                "整批隔离进入Recovery Queue，"
                "不终止整个Task。"
            ),
            str(error)
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


# ============================================================
# LOCAL CLUSTER RECORDS
# ============================================================

def make_cluster_records(
    batch_identifier,
    clusters
):
    output = []

    for cluster in clusters:

        indexes = sorted(
            set(
                int(x)
                for x in cluster.get(
                    "article_indexes",
                    []
                )
            )
        )

        if not indexes:
            continue

        local_id = str(
            cluster.get(
                "cluster_id",
                ""
            )
        ).strip()

        if not local_id:

            raise RuntimeError(
                "❌ AI返回空Local Cluster ID"
            )

        if re.fullmatch(
            r"(EVT|REC|GM)-.*",
            local_id,
            flags=re.I
        ):

            raise RuntimeError(
                f"❌ AI生成了禁止的Global ID："
                f"{local_id}"
            )

        output.append(
            {
                "cluster_id":
                    local_id,

                "local_cluster_id":
                    local_id,

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
                    indexes,

                "batch_identifier":
                    batch_identifier
            }
        )

    return output


# ============================================================
# APPEND SAFE CLUSTERS
# ============================================================

def append_safe_clusters(
    all_clusters,
    clusters,
    batch_identifier,
    expected_indexes,
    date,
    context,
    registry
):
    issues = inspect_cluster_assignment(
        clusters,
        expected_indexes
    )

    if not valid_issues(
        issues
    ):

        raise RuntimeError(
            f"❌ {context} Cluster coverage异常："
            f"{issues}"
        )

    local_records = (
        make_cluster_records(
            batch_identifier,
            clusters
        )
    )

    global_records = (
        register_global_cluster_ids(
            date,
            local_records,
            registry,
            context
        )
    )

    all_clusters.extend(
        global_records
    )


# ============================================================
# RECOVERY PASS
# ============================================================

def recovery_pass(
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
        indexes[position:position + batch_size]
        for position in range(
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
        f"BatchSize={batch_size} | "
        f"SubBatches={len(sub_batches)}"
    )

    for sub_number, sub_indexes in enumerate(
        sub_batches,
        1
    ):

        items = [
            news[index - 1]
            for index in sub_indexes
        ]

        label = (
            f"RECOVERY "
            f"{recovery_pass_no} / "
            f"BATCH {sub_number}"
        )

        print(
            f"   🔹 {label}: "
            f"{sub_indexes}"
        )

        # ------------------------------------------------------
        # Singleton
        # ------------------------------------------------------

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
                        "该文章在恢复阶段作为独立事件单元保留。"
                }
            )

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

            safe = safe_covered_indexes(
                clusters,
                sub_indexes
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

                    index = int(
                        value
                    )

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

                safe_issues = inspect_cluster_assignment(
                    safe_clusters,
                    safe
                )

                if not valid_issues(
                    safe_issues
                ):

                    raise RuntimeError(
                        f"❌ {label} SAFE PART异常："
                        f"{safe_issues}"
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
# BUILD INITIAL CLUSTERS
# ============================================================

def build_initial_clusters(
    date,
    news,
    registry
):
    all_clusters = []

    total = len(
        news
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "STAGE 1A — "
        "AI EVENT CLUSTERING V6.5.3"
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
        "Failure Policy: "
        "isolate -> recovery queue -> "
        "30/15/8/4/2/1 -> singleton"
    )

    pending = []

    batch_number = 0

    # ==========================================================
    # NORMAL 30-ARTICLE PASS
    # ==========================================================

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE
    ):

        batch_number += 1

        end = min(
            start
            +
            AGGREGATION_BATCH_SIZE,
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
            f"{batch_number}: "
            f"{indexes[0]}-"
            f"{indexes[-1]}/"
            f"{total}"
        )

        status, clusters, unresolved = (
            cluster_news_batch_with_repair(
                date,
                items,
                indexes,
                f"CLUSTER BATCH {batch_number}"
            )
        )

        if status == "complete":

            append_safe_clusters(
                all_clusters,
                clusters,
                batch_number,
                indexes,
                date,
                f"Batch {batch_number}",
                registry
            )

            print(
                f"   Clusters generated: "
                f"{len(clusters)}"
            )

        elif status == "partial":

            safe = safe_covered_indexes(
                clusters,
                indexes
            )

            safe_set = set(
                safe
            )

            safe_clusters = []

            for cluster in clusters:

                ids = [
                    int(value)
                    for value
                    in cluster.get(
                        "article_indexes",
                        []
                    )
                    if int(value)
                    in safe_set
                ]

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

                append_safe_clusters(
                    all_clusters,
                    safe_clusters,
                    (
                        f"Batch "
                        f"{batch_number} SAFE PART"
                    ),
                    safe,
                    date,
                    (
                        f"Batch "
                        f"{batch_number} SAFE PART"
                    ),
                    registry
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

    # ==========================================================
    # RECOVERY
    # ==========================================================

    for pass_number, batch_size in enumerate(
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
            recovery_pass(
                date,
                news,
                current_pending,
                pass_number,
                batch_size,
                registry
            )
        )

        if recovered:

            local_records = (
                make_cluster_records(
                    f"RECOVERY PASS {pass_number}",
                    recovered
                )
            )

            global_records = (
                register_global_cluster_ids(
                    date,
                    local_records,
                    registry,
                    f"Recovery Pass {pass_number}"
                )
            )

            all_clusters.extend(
                global_records
            )

        pending.extend(
            unresolved
        )

        print(
            f"   Recovery Pass "
            f"{pass_number}: "
            f"recovered={len(recovered)} | "
            f"still_pending={len(pending)}"
        )

    # ==========================================================
    # FINAL GATE
    # ==========================================================

    if pending:

        pending = sorted(
            set(pending)
        )

        log_conflict(
            date,
            "STAGE 1A / FINAL RECOVERY",
            (
                "Recovery Queue仍有未处理ARTICLE，"
                "禁止生成Initial Clusters。"
            ),
            {
                "pending_articles":
                    pending
            }
        )

        raise RuntimeError(
            "❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE："
            f"{pending}"
        )

    # ==========================================================
    # GLOBAL VALIDATION
    # ==========================================================

    validate_global_article_coverage(
        date,
        all_clusters,
        total,
        "STAGE 1A GLOBAL"
    )

    validate_global_cluster_membership(
        date,
        all_clusters,
        "STAGE 1A INITIAL"
    )

    print(
        f"\n✅ Initial Clusters: "
        f"{len(all_clusters)}"
    )

    print(
        f"✅ ARTICLE Coverage: "
        f"{total}/{total}"
    )

    return all_clusters


# ============================================================
# INITIAL CLUSTER FILE
# ============================================================

def validate_initial_clusters_file(
    date,
    language,
    clusters,
    news_count
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

        validate_global_article_coverage(
            date,
            clusters,
            news_count,
            f"{date}/{language} INITIAL FILE"
        )

        validate_global_cluster_membership(
            date,
            clusters,
            "INITIAL CLUSTERS"
        )

    except Exception:

        return False

    return True


def save_initial_clusters(
    date,
    language,
    clusters
):
    lang = validate_language(
        language
    )

    write_json_atomic(
        initial_clusters_path(
            date,
            lang
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
                now().isoformat()
        }
    )


def load_initial_clusters(
    date,
    language,
    news_count
):
    lang = validate_language(
        language
    )

    path = initial_clusters_path(
        date,
        lang
    )

    if not path.exists():
        return None

    data = read_json(
        path,
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
        lang,
        clusters,
        news_count
    ):

        return None

    return clusters


# ============================================================
# TASK 1
# ============================================================

def run_task_1(
    date,
    language
):
    """
    Task 1唯一主入口。

    Enriched
        ↓
    Cluster
        ↓
    Initial Clusters
    """

    lang = validate_language(
        language
    )

    # ----------------------------------------------------------
    # Prepare language directory
    # ----------------------------------------------------------

    language_root = (
        RAW_NEWS
        /
        f"{date}-EventUnit"
        /
        lang
    )

    language_root.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------------------------
    # Load Enriched
    # ----------------------------------------------------------

    news = load_all_enriched_news(
        date,
        lang
    )

    # ----------------------------------------------------------
    # Reuse valid checkpoint
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # Shared Global Registry
    # ----------------------------------------------------------

    registry_path = (
        global_cluster_registry_path(
            date
        )
    )

    if registry_path.exists():

        registry = read_json(
            registry_path,
            None
        )

    else:

        registry = None

    if (
        not isinstance(
            registry,
            dict
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
            registry
        )

    # ----------------------------------------------------------
    # Validate Registry
    # ----------------------------------------------------------

    from knowledge_common import (
        validate_registry_basic
    )

    validate_registry_basic(
        date,
        registry
    )

    # ----------------------------------------------------------
    # Build
    # ----------------------------------------------------------

    clusters = build_initial_clusters(
        date,
        news,
        registry
    )

    # ----------------------------------------------------------
    # Final validation
    # ----------------------------------------------------------

    validate_global_cluster_membership(
        date,
        clusters,
        "TASK 1 FINAL"
    )

    validate_global_article_coverage(
        date,
        clusters,
        len(news),
        "TASK 1 FINAL"
    )

    # ----------------------------------------------------------
    # Save
    # ----------------------------------------------------------

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


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 1 - "
            "Cluster V6.5.3"
        )
    )

    parser.add_argument(
        "--date",
        required=True
    )

    parser.add_argument(
        "--language",
        choices=[
            "en",
            "zh"
        ],
        required=True
    )

    args = parser.parse_args()

    # ----------------------------------------------------------
    # Strict language validation
    # ----------------------------------------------------------

    validate_language(
        args.language
    )

    run_task_1(
        args.date,
        args.language
    )

    return 0


if __name__ == "__main__":

    sys.exit(
        main()
    )
