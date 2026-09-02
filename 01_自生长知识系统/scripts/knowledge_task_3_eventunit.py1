#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Knowledge Task 3 V6.5.3."""

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


# ==============================================================
# PATH CONTRACT
#
# 所有实际文件系统目录统一锁死为小写。
#
# 00_system/
# skills/
# raw news/
#
# YYYY-MM-DD-eventunit/
# ├── en/
# │   ├── articles/
# │   └── event_units/
# │
# └── zh/
#     ├── articles/
#     └── event_units/
#
# 注意：
# 这里不再进行任何 EN/ZH -> en/zh 的大小写转换。
# CLI、内部变量、目录协议全部直接使用 en / zh。
# ==============================================================

ROOT = Path(__file__).resolve().parents[1]

SYSTEM = ROOT / "00_system"
SKILLS = ROOT / "skills"
RAW_NEWS = ROOT / "raw news"

REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"
TOPICS = ROOT / "07_专题报告"
KNOWLEDGE = ROOT / "08_知识库"

LOGS = SYSTEM / "运行日志"
ROUTES_FILE = SYSTEM / "skill_routes.json"


# ==============================================================
# EVENT UNIT PATH CONTRACT
# ==============================================================

EVENT_UNITS_SUFFIX = "eventunit"

EVENT_INDEX_FILE = "_event_index.json"
EVENT_UNITS_COMPLETE_FILE = "_COMPLETE"
SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"
INITIAL_CLUSTERS_FILE = "_initial_clusters.json"
MERGED_CLUSTERS_FILE = "_merged_clusters.json"


# ==============================================================
# AI CONFIG
# ==============================================================

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


# ==============================================================
# PROCESS CONFIG
# ==============================================================

AGGREGATION_BATCH_SIZE = 30

GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"

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


# ==============================================================
# TIME / LANGUAGE
# ==============================================================
#
# 语言协议正式锁死：
#
#     en
#     zh
#
# 不再接受 EN / ZH。
# 不再调用 upper() / lower() 做转换。
# ==============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")

SUPPORTED_LANGUAGES = (
    "en",
    "zh"
)

CURRENT_LANGUAGE = None


# ==============================================================
# LANGUAGE CONTRACT
# ==============================================================
#
# 这里故意不做任何大小写转换。
#
# 正确：
#     normalize_language("en") -> "en"
#     normalize_language("zh") -> "zh"
#
# 错误：
#     EN
#     ZH
#
# 如果上游传入错误大小写，直接失败。
# 这样可以尽早发现路径协议不一致。
# ==============================================================

def normalize_language(language):
    value = str(
        language or ""
    ).strip()

    if value not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ 不支持的语言：{language} "
            f"；语言协议必须是 en 或 zh"
        )

    return value


# ==============================================================
# TIME
# ==============================================================

def now():
    return datetime.now(
        BEIJING_TZ
    )


# ==============================================================
# PATH HELPERS
# ==============================================================

def event_units_root(date):
    """
    统一目录：

        raw news/
        └── YYYY-MM-DD-eventunit/
    """

    return (
        RAW_NEWS
        / f"{date}-{EVENT_UNITS_SUFFIX}"
    )


def language_dir(
    date,
    language=None
):
    """
    统一语言目录：

        en
        zh

    注意：
    不再进行任何大小写转换。
    """

    if language is None:
        language = getattr(
            sys.modules[__name__],
            "CURRENT_LANGUAGE",
            None
        )

    lang = normalize_language(
        language
    )

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


def conflict_log_path(date):
    return (
        LOGS
        / f"{date}_event_aggregation_conflicts.log"
    )


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


# ==============================================================
# ATOMIC TEXT
# ==============================================================

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

        tmp.replace(
            path
        )

    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass

        raise


# ==============================================================
# FINAL EVENT ID VALIDATION
#
# 注意：
# Global Event ID 正式协议仍然是：
#
# EVT-YYYYMMDD-NNNNNN
#
# 这里的大写 EVT 是 ID 协议，
# 不是目录大小写问题，因此保留。
# ==============================================================

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

    bad = [
        x
        for x in ids
        if not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            x
        )
    ]

    if bad:
        raise RuntimeError(
            f"❌ {date} Final EventUnit存在非法Global ID："
            f"{bad[:20]}"
        )


# ==============================================================
# BUILD EVENT UNITS
# ==============================================================

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
            ][
                "metadata"
            ]

            arts.append({
                "index": i,

                "path":
                    str(
                        news[
                            i - 1
                        ][
                            "path"
                        ]
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
                    ][
                        "body"
                    ]
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


# ==============================================================
# AI EVENT SYNTHESIS
# ==============================================================

def synthesize_event(event):

    blocks = []

    for a in event[
        "articles"
    ][
        :MAX_ARTICLES_PER_EVENT_CONTEXT
    ]:

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

    prompt = f"""你正在执行748686自生长知识系统V6.5.3第二层事件知识综合。
日期：{event['date']}
事件ID：{event['event_id']}
事件名称：{event['event_title']}
第一轮事件判断：{event['event_reason']}

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


# ==============================================================
# EVENT UNIT FILENAME
# ==============================================================

def event_unit_filename(e):

    return (
        f"{e['event_id']}_"
        f"{safe_name(e['event_title'])}.md"
    )


# ==============================================================
# SAVE EVENT UNIT
# ==============================================================

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
        / event_unit_filename(event)
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
language: {CURRENT_LANGUAGE}
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


# ==============================================================
# SAVE EVENT INDEX
# ==============================================================

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

            "language":
                CURRENT_LANGUAGE,

            "event_title":
                e["event_title"],

            "event_reason":
                e["event_reason"],

            "source_count":
                len(
                    e["articles"]
                ),

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


# ==============================================================
# EVENT UNIT FILE VALIDATION
# ==============================================================

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
        ) == event_id
    ) and (
        m.get(
            "status"
        ) == "completed"
    )


# ==============================================================
# INSPECT EVENT UNITS
# ==============================================================

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

        ids.append(
            eid
        )

        matches = (
            list(
                target.glob(
                    f"{eid}_*.md"
                )
            )
            if eid
            else []
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

    return {
        "exists": True,

        "complete":
            bool(ids)
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


# ==============================================================
# COMPLETE MARKER
# ==============================================================
#
# 注意：
# _COMPLETE 是当前系统已有完成标记协议。
#
# 虽然目录统一小写，
# 但这里不擅自修改为 _complete，
# 因为这属于上下游文件名契约。
# ==============================================================

def mark_event_units_complete(
    date,
    n,
    e
):

    p = (
        language_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    p.write_text(
        f"""EVENT_UNITS_COMPLETE
date: {date}
language: {CURRENT_LANGUAGE}
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
        language_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    if p.exists():
        p.unlink()


# ==============================================================
# REBUILD EVENTS FROM INDEX
# ==============================================================

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
                    f"❌ {e.get('event_id')}引用不存在文章：{i}"
                )

            m = news[
                i - 1
            ][
                "metadata"
            ]

            arts.append({
                "index":
                    i,

                "path":
                    str(
                        news[
                            i - 1
                        ][
                            "path"
                        ]
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
                    ][
                        "body"
                    ]
            })

        out.append({
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
        })

    return out


# ==============================================================
# EVENT INDEX COVERAGE VALIDATION
# ==============================================================

def validate_event_index_coverage(
    date,
    events,
    n
):

    ids = []
    eids = set()

    for e in events:

        event_id = e[
            "event_id"
        ]

        if event_id in eids:

            raise RuntimeError(
                f"❌ {date} Event Index重复event_id："
                f"{event_id}"
            )

        eids.add(
            event_id
        )

        ids.extend(
            a["index"]
            for a in e[
                "articles"
            ]
        )

    if (
        set(ids)
        != set(
            range(
                1,
                n + 1
            )
        )
        or
        len(ids)
        != len(set(ids))
    ):

        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败"
        )


# ==============================================================
# COMPLETE EXISTING EVENT UNITS
# ==============================================================

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

    # ----------------------------------------------------------
    # 最终再次验证所有 EventUnit
    # ----------------------------------------------------------

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


# ==============================================================
# TASK 3
# ==============================================================

def run_task_3(
    date,
    language
):

    global CURRENT_LANGUAGE

    # ----------------------------------------------------------
    # 语言直接锁死为小写：
    #
    #     en
    #     zh
    #
    # 不再做 upper/lower 转换。
    # ----------------------------------------------------------

    CURRENT_LANGUAGE = normalize_language(
        language
    )

    lang = CURRENT_LANGUAGE

    # ----------------------------------------------------------
    # 创建统一小写目录
    #
    # YYYY-MM-DD-eventunit/
    # ├── en/
    # │   ├── articles/
    # │   └── event_units/
    # │
    # └── zh/
    #     ├── articles/
    #     └── event_units/
    # ----------------------------------------------------------

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

    # ----------------------------------------------------------
    # 读取 Enriched News
    # ----------------------------------------------------------

    news = load_all_enriched_news(
        date,
        lang
    )

    print(
        "\n" + "=" * 70
    )

    print(
        "TASK 3 — EVENT UNIT SYNTHESIS V6.5.3"
    )

    print(
        "=" * 70
    )

    print(
        f"DATE     : {date}"
    )

    print(
        f"LANGUAGE : {lang}"
    )

    print(
        f"ARTICLES : {len(news)}"
    )

    print(
        f"EVENTUNIT ROOT : "
        f"{event_units_root(date)}"
    )

    # ----------------------------------------------------------
    # 检查是否已经完成
    # ----------------------------------------------------------

    inspection = inspect_event_units(
        date
    )

    if inspection[
        "complete"
    ]:

        print(
            f"♻️ TASK 3: EventUnits already complete "
            f"| {date}/{lang}"
        )

        return True

    # ----------------------------------------------------------
    # TASK 2结果必须存在
    # ----------------------------------------------------------

    merged_path = merged_clusters_path(
        date,
        lang
    )

    if not merged_path.exists():

        raise RuntimeError(
            f"❌ TASK 3找不到TASK 2结果："
            f"{merged_path}"
        )

    # ----------------------------------------------------------
    # 读取 TASK 2
    # ----------------------------------------------------------

    data = read_json(
        merged_path,
        None
    )

    final = (
        data.get("clusters")
        if isinstance(
            data,
            dict
        )
        else None
    )

    if (
        not isinstance(
            final,
            list
        )
        or not final
    ):

        raise RuntimeError(
            "❌ TASK 2结果无效"
        )

    # ----------------------------------------------------------
    # TASK 2 Global Cluster最终验证
    # ----------------------------------------------------------

    validate_global_article_coverage(
        date,
        final,
        len(news),
        "TASK 3 TASK 2 RESULT"
    )

    validate_final_event_ids(
        date,
        final
    )

    # ----------------------------------------------------------
    # 构建 EventUnit
    # ----------------------------------------------------------

    events = build_event_units(
        date,
        final,
        news
    )

    # ----------------------------------------------------------
    # Event Index覆盖验证
    # ----------------------------------------------------------

    validate_event_index_coverage(
        date,
        events,
        len(news)
    )

    # ----------------------------------------------------------
    # Global Event ID验证
    # ----------------------------------------------------------

    validate_final_event_ids(
        date,
        events
    )

    # ----------------------------------------------------------
    # 保存 Event Index
    # ----------------------------------------------------------

    save_aggregation_index(
        date,
        events
    )

    # ----------------------------------------------------------
    # 生成 EventUnit
    # ----------------------------------------------------------

    complete_existing_event_units(
        date,
        events,
        len(news)
    )

    print(
        f"✅ TASK 3 COMPLETE | "
        f"{date}/{lang} | "
        f"events={len(events)}"
    )

    return True


# ==============================================================
# MAIN
# ==============================================================

def main():

    ap = argparse.ArgumentParser(
        description=
        "748686 Knowledge Task 3 - "
        "EventUnit V6.5.3"
    )

    ap.add_argument(
        "--date",
        required=True
    )

    # ----------------------------------------------------------
    # 语言参数正式锁死为小写。
    #
    # 正确：
    #     --language en
    #     --language zh
    #
    # 不再接受：
    #     EN
    #     ZH
    # ----------------------------------------------------------

    ap.add_argument(
        "--language",
        choices=[
            "en",
            "zh"
        ],
        required=True
    )

    args = ap.parse_args()

    run_task_3(
        args.date,
        args.language
    )

    return 0


# ==============================================================
# ENTRY
# ==============================================================

if __name__ == "__main__":
    sys.exit(
        main()
    )
