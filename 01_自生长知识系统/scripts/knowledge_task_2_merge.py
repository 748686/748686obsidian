#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Knowledge Pipeline V6.5.3 modular architecture."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

# Shared infrastructure from knowledge_common.py.
# Do NOT use wildcard import: Task 2 keeps its own Global Merge validation.
from knowledge_common import (
    call_ai,
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
SUPPORTED_LANGUAGES = ("en", "zh")
CURRENT_LANGUAGE = None

def normalize_language(language):
    value = str(language or "").strip()
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
    lang = normalize_language(language)
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


def _windows(clusters, step):
    out, s = [], 0

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

    groups = data.get("groups")

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

        if not isinstance(ids, list) or not ids:
            malformed.append(
                f"group[{p}]cluster_indexes无效"
            )
            continue

        for x in ids:
            try:
                actual.append(int(x))
            except Exception:
                malformed.append(
                    f"group[{p}]非法编号：{x}"
                )

    dup = sorted({
        x for x in actual
        if actual.count(x) > 1
    })

    miss = sorted(
        set(expected) - set(actual)
    )

    extra = sorted(
        set(actual) - set(expected)
    )

    if dup or miss or extra or malformed:
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
            for x in g["cluster_indexes"]
        ]

        ids = [
            window[i - 1]["cluster_id"]
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
        ).append(item)

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
                uf.find(member_ids[0])
                == uf.find(root)
            ):
                entries.extend(rs)
        except Exception:
            pass

    actual = [
        r for r in entries
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
        r for r in entries
        if len(
            r.get(
                "cluster_ids",
                []
            )
        ) > 1
        and _metadata_record_valid(r)
    ]

    singleton = [
        r for r in entries
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

        if not title and not reason and singleton:
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

        rebuilt.append({
            # 合并后的组件保留最早注册的 Global ID，避免 ID 漂移。
            "cluster_id": min(member_ids),
            "event_title": title,
            "event_reason": reason,
            "article_indexes": articles,
            "member_cluster_ids": originals
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

        if not cid:
            malformed.append(
                f"cluster[{pos}]缺少cluster_id"
            )

        elif not re.fullmatch(r"EVT-\d{8}-\d{6}", cid):
            malformed.append(
                f"cluster[{pos}]非法Global cluster_id：{cid}"
            )

        elif cid in seen_current:
            duplicate_current.append(cid)

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
                "malformed": malformed,
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
        if not isinstance(c, dict):
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
        x for x in allidx
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
                "duplicate": duplicate,
                "missing": missing,
                "extra": extra,
                "malformed": malformed
            }
        )

        raise RuntimeError(
            f"❌ {context} Article覆盖异常 "
            f"Duplicate={duplicate} "
            f"Missing={missing} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )


class UnionFind:
    def __init__(self, values):
        values = [
            str(x)
            for x in values
        ]
        self.parent = {
            v: v for v in values
        }
        self.rank = {
            v: 0 for v in values
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
        a, b = str(a), str(b)

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
        "version": "6.5.2",
        "date": date,
        "language": CURRENT_LANGUAGE,
        "status": status,
        "round": int(round_no),
        "completed_windows": sorted(
            set(
                int(x)
                for x in completed_windows
            )
        ),
        "window_count":
            int(window_count)
            if window_count is not None
            else None,
        "window_size": GLOBAL_MERGE_WINDOW_SIZE,
        "window_overlap": 0,
        "original_cluster_ids":
            sorted(
                str(x)
                for x in original_cluster_ids
            ),
        "current_clusters": current,
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
        global_merge_checkpoint_path(date, CURRENT_LANGUAGE),
        data
    )


def load_global_merge_checkpoint(date):
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
        or
        data.get("date") != date
        or
        data.get("language") not in (None, CURRENT_LANGUAGE)
    ):
        return None

    saved_overlap=data.get("window_overlap")
    if saved_overlap is not None and int(saved_overlap) != 0:
        log_conflict(date,"GLOBAL MERGE CHECKPOINT","检测到旧版Overlap checkpoint，禁止恢复。",{"window_overlap":saved_overlap})
        return None

    return data


def remove_global_merge_checkpoint(date):
    p = global_merge_checkpoint_path(
        date
    )

    if p.exists():
        p.unlink()


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
                    sorted(actual_original),
                "expected":
                    sorted(expected_original)
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
            str(c["cluster_id"])
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


def merge_all_clusters(
    date,
    clusters,
    news_count
):
    current = clusters

    original_cluster_ids = sorted(
        str(c["cluster_id"])
        for c in clusters
    )

    print("\n" + "=" * 70)
    print(
        "STAGE 1B — V6.5.3 GLOBAL EVENT MERGING"
    )
    print("=" * 70)

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
                checkpoint["round"]
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
                    str(c["cluster_id"])
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
            before = len(current)

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
                str(c["cluster_id"])
                for c in current
            ]

            print(
                f"Windows: {window_count} | "
                f"Size: {GLOBAL_MERGE_WINDOW_SIZE} | "
                f"Overlap: {GLOBAL_MERGE_OVERLAP}"
            )

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
                str(c["cluster_id"]),
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

def save_merged_clusters(date,language,clusters):
    write_json_atomic(merged_clusters_path(date,language), {"version":"6.5.3","date":str(date),"language":normalize_language(language),"clusters":clusters,"saved_at":now().isoformat()})


def load_merged_clusters(date,language,news_count):
    p=merged_clusters_path(date,language)
    if not p.exists(): return None
    data=read_json(p,None); clusters=data.get("clusters") if isinstance(data,dict) else None
    if not isinstance(clusters,list) or not clusters: return None
    try:
        validate_global_cluster_membership(date,clusters,"TASK 2 SAVED",None)
        validate_global_article_coverage(date,clusters,news_count,"TASK 2 SAVED")
    except Exception: return None
    return clusters


def run_task_2(date,language):
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE=normalize_language(language)
    initial_path=initial_clusters_path(date,CURRENT_LANGUAGE)
    if not initial_path.exists():
        raise RuntimeError(f"❌ TASK 2找不到TASK 1结果：{initial_path}")
    news=load_all_enriched_news(date,CURRENT_LANGUAGE)
    existing=load_merged_clusters(date,CURRENT_LANGUAGE,len(news))
    if existing is not None:
        print(f"♻️ TASK 2: reuse valid merged clusters | {date}/{CURRENT_LANGUAGE} | clusters={len(existing)}")
        return existing
    data=read_json(initial_path,None)
    initial=data.get("clusters") if isinstance(data,dict) else None
    if not isinstance(initial,list) or not initial: raise RuntimeError("❌ TASK 1结果无效")
    validate_global_article_coverage(date,initial,len(news),"TASK 2 INITIAL")
    final=merge_all_clusters(date,initial,len(news))
    save_merged_clusters(date,CURRENT_LANGUAGE,final)
    remove_global_merge_checkpoint(date,CURRENT_LANGUAGE)
    print(f"✅ TASK 2 COMPLETE | {date}/{CURRENT_LANGUAGE} | clusters={len(final)}")
    return final


def main():
    ap=argparse.ArgumentParser(description="748686 Knowledge Task 2 - Global Merge V6.5.3")
    ap.add_argument("--date",required=True); ap.add_argument("--language",choices=["en","zh"],required=True)
    args=ap.parse_args(); run_task_2(args.date,args.language); return 0

if __name__=="__main__": sys.exit(main())
