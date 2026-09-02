#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 3 — EventUnit Synthesis
V6.5.3

TASK 3职责
==========

    1. 读取 Task 2 Global Merge 最终结果
    2. 验证 Task 2 ARTICLE 100% 覆盖
    3. 验证最终 Global Event ID
    4. 将 Final Event Components 转换为 EventUnit
    5. 建立 _event_index.json
    6. 对每个 EventUnit 执行第二层 AI 多来源综合
    7. 保存 EventUnit Markdown
    8. 验证所有 EventUnit 文件
    9. 所有 EventUnit 完整后生成 _COMPLETE

重要架构：

    Task 1 Cluster
        ↓
    Task 2 Global Merge
        ↓
    Task 3 EventUnit Synthesis
        ↓
    EventUnit Validator
        ↓
    Task 4 Skills

语言协议
========

    只允许：

        en
        zh

禁止：

        EN
        ZH
        En
        Zh

本文件绝不执行 upper() / lower() 自动转换。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from knowledge_common import (
    ROOT,
    RAW_NEWS,
    EVENT_INDEX_FILE,
    EVENT_UNITS_COMPLETE_FILE,
    MERGED_CLUSTERS_FILE,
    MAX_ARTICLES_PER_EVENT_CONTEXT,
    ARTICLE_AGGREGATION_CONTENT_LIMIT,
    call_ai,
    load_all_enriched_news,
    normalize_language,
    now,
    parse_front_matter,
    read_json,
    safe_name,
    write_json,
)


# ==============================================================
# LANGUAGE
# ==============================================================

CURRENT_LANGUAGE = None


# ==============================================================
# PATH CONTRACT
# ==============================================================

EVENT_UNITS_SUFFIX = "eventunit"


def event_units_root(date):
    """
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
    if language is None:
        language = CURRENT_LANGUAGE

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
# GLOBAL EVENT ID VALIDATION
# ==============================================================

def validate_final_event_ids(
    date,
    events
):
    if not isinstance(events, list):
        raise RuntimeError(
            f"❌ {date} Final Event Components 不是数组"
        )

    ids = []

    for e in events:

        if not isinstance(e, dict):
            raise RuntimeError(
                f"❌ {date} Final Event Components 存在非法对象"
            )

        event_id = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

        if not event_id:
            raise RuntimeError(
                f"❌ {date} Final Event Components 存在空 event_id"
            )

        ids.append(
            event_id
        )

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            f"❌ {date} Final Event Components 存在重复 event_id"
        )

    import re

    bad = [
        event_id
        for event_id in ids
        if not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            event_id
        )
    ]

    if bad:
        raise RuntimeError(
            f"❌ {date} Final Event Components 存在非法 Global Event ID："
            f"{bad[:20]}"
        )


# ==============================================================
# TASK 2 ARTICLE COVERAGE
# ==============================================================

def validate_global_article_coverage(
    date,
    clusters,
    news_count,
    stage
):
    """
    Task 2 最终结果必须：

        ARTICLE 1..N
        每篇恰好出现一次

    注意：

    这里验证的是最终 Global Merge Component
    的 ARTICLE 归属。

    不允许：

        missing
        duplicate
        extra
        malformed

    """

    if not isinstance(
        clusters,
        list
    ):
        raise RuntimeError(
            f"❌ {stage}：clusters 不是数组"
        )

    expected = set(
        range(
            1,
            news_count + 1
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
            dict
        ):
            malformed.append(
                f"component[{pos}]不是对象"
            )
            continue

        article_indexes = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            article_indexes,
            list
        ):
            malformed.append(
                f"component[{pos}] article_indexes不是数组"
            )
            continue

        if not article_indexes:
            malformed.append(
                f"component[{pos}] article_indexes为空"
            )
            continue

        for value in article_indexes:

            try:
                index = int(value)

            except Exception:
                malformed.append(
                    f"component[{pos}]非法ARTICLE ID：{value}"
                )
                continue

            occurrences.setdefault(
                index,
                []
            ).append(
                pos
            )

    actual = set(
        occurrences
    )

    missing = sorted(
        expected - actual
    )

    extra = sorted(
        actual - expected
    )

    duplicate = {
        index: positions
        for index, positions
        in occurrences.items()
        if len(positions) > 1
    }

    if malformed:
        raise RuntimeError(
            f"❌ {stage} ARTICLE覆盖验证失败："
            f"malformed={malformed[:20]}"
        )

    if missing:
        raise RuntimeError(
            f"❌ {stage} ARTICLE覆盖验证失败："
            f"missing={missing[:50]}"
        )

    if extra:
        raise RuntimeError(
            f"❌ {stage} ARTICLE覆盖验证失败："
            f"extra={extra[:50]}"
        )

    if duplicate:
        raise RuntimeError(
            f"❌ {stage} ARTICLE重复归属："
            f"{dict(list(duplicate.items())[:20])}"
        )

    if (
        actual != expected
        or len(occurrences) != news_count
    ):
        raise RuntimeError(
            f"❌ {stage} ARTICLE覆盖数量异常："
            f"{len(occurrences)}/{news_count}"
        )

    print(
        f"✅ {stage} ARTICLE Coverage: "
        f"{news_count}/{news_count}"
    )


# ==============================================================
# BUILD EVENT UNITS
# ==============================================================

def build_event_units(
    date,
    clusters,
    news
):
    events = []

    for cluster in clusters:

        event_id = str(
            cluster.get(
                "event_id",
                ""
            )
        ).strip()

        if not event_id:
            raise RuntimeError(
                f"❌ {date} Final Component 缺少 event_id"
            )

        event_title = str(
            cluster.get(
                "event_title",
                "未命名事件"
            )
        ).strip()

        event_reason = str(
            cluster.get(
                "event_reason",
                ""
            )
        ).strip()

        article_indexes = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            article_indexes,
            list
        ):
            raise RuntimeError(
                f"❌ {event_id} article_indexes不是数组"
            )

        if not article_indexes:
            raise RuntimeError(
                f"❌ {event_id} article_indexes为空"
            )

        articles = []

        for raw_index in article_indexes:

            try:
                index = int(
                    raw_index
                )
            except Exception:
                raise RuntimeError(
                    f"❌ {event_id}存在非法ARTICLE ID："
                    f"{raw_index}"
                )

            if not (
                1 <= index <= len(news)
            ):
                raise RuntimeError(
                    f"❌ {event_id}引用不存在文章："
                    f"{index}"
                )

            item = news[
                index - 1
            ]

            metadata = item[
                "metadata"
            ]

            articles.append({
                "index": index,

                "path": str(
                    item["path"]
                ),

                "title": metadata.get(
                    "title",
                    "Untitled"
                ),

                "source": metadata.get(
                    "source",
                    "Unknown"
                ),

                "source_url": metadata.get(
                    "source_url",
                    ""
                ),

                "source_status": metadata.get(
                    "source_status",
                    ""
                ),

                "content_status": metadata.get(
                    "content_status",
                    ""
                ),

                "body": item.get(
                    "body",
                    ""
                )
            })

        events.append({
            "event_id": event_id,

            "date": date,

            "event_title": (
                event_title
                or "未命名事件"
            ),

            "event_reason":
                event_reason,

            "articles":
                articles
        })

    return events


# ==============================================================
# EVENT INDEX COVERAGE
# ==============================================================

def validate_event_index_coverage(
    date,
    events,
    news_count
):
    ids = []
    event_ids = set()

    for event in events:

        event_id = event[
            "event_id"
        ]

        if event_id in event_ids:
            raise RuntimeError(
                f"❌ {date} Event Index重复event_id："
                f"{event_id}"
            )

        event_ids.add(
            event_id
        )

        for article in event[
            "articles"
        ]:
            ids.append(
                int(
                    article["index"]
                )
            )

    expected = set(
        range(
            1,
            news_count + 1
        )
    )

    actual = set(
        ids
    )

    missing = sorted(
        expected - actual
    )

    extra = sorted(
        actual - expected
    )

    duplicate = sorted(
        index
        for index in actual
        if ids.count(index) > 1
    )

    if missing:
        raise RuntimeError(
            f"❌ {date} Event Index缺少ARTICLE："
            f"{missing[:50]}"
        )

    if extra:
        raise RuntimeError(
            f"❌ {date} Event Index存在Extra ARTICLE："
            f"{extra[:50]}"
        )

    if duplicate:
        raise RuntimeError(
            f"❌ {date} Event Index存在重复ARTICLE："
            f"{duplicate[:50]}"
        )

    if actual != expected:
        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败"
        )

    print(
        f"✅ EVENT INDEX ARTICLE Coverage: "
        f"{news_count}/{news_count}"
    )


# ==============================================================
# AI EVENT SYNTHESIS
# ==============================================================

def synthesize_event(
    event
):
    blocks = []

    articles = event[
        "articles"
    ][
        :MAX_ARTICLES_PER_EVENT_CONTEXT
    ]

    for article in articles:

        blocks.append(
            f"""### 来源文章 #{article['index']}
标题：{article['title']}
来源：{article['source']}
链接：{article['source_url']}
source_status：{article['source_status']}
content_status：{article['content_status']}

内容：
{article['body'][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}"""
        )

    joined = "\n\n".join(
        blocks
    )

    prompt = f"""你正在执行748686自生长知识系统V6.5.3第二层事件知识综合。

日期：{event['date']}
事件ID：{event['event_id']}
事件名称：{event['event_title']}

第一层事件判断：
{event['event_reason']}

同一事件的多来源输入：

{joined}

请将这些来源综合为一个高质量事件知识单元。

严格要求：

1. 识别不同来源共同确认的核心事实。
2. 保留来源独有信息。
3. 保留不同国家 / 地区视角。
4. 严格区分事实、判断和推测。
5. 不得编造输入中没有的信息。
6. source_status 不是 fetched 时，不得声称完整阅读了原文。
7. 如果不同来源存在冲突，必须明确指出。
8. 如果资料不足，必须明确说明。
9. 不要因为多个来源重复描述就虚构新的事实。
10. 不要输出与输入来源无关的背景知识。

输出标准中文 Markdown。

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
"""

    result = call_ai(
        prompt,
        (
            "你是748686自生长知识系统的"
            "跨来源新闻事件综合专家。"
            "严格依据输入资料。"
            "不得编造。"
            "输出标准中文Markdown。"
        ),
        0.2
    )

    if not isinstance(
        result,
        str
    ):
        result = str(
            result or ""
        )

    return result.strip()


# ==============================================================
# EVENT UNIT FILENAME
# ==============================================================

def event_unit_filename(
    event
):
    return (
        f"{event['event_id']}_"
        f"{safe_name(event['event_title'])}.md"
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
        date,
        CURRENT_LANGUAGE
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        target
        / event_unit_filename(event)
    )

    sources = "\n".join(
        (
            f"- {article['source']} | "
            f"{article['title']} | "
            f"{article['source_url']}"
        )
        for article in event[
            "articles"
        ]
    )

    text = f"""---
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
"""

    write_text_atomic(
        path,
        text
    )

    return path


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
        metadata, body = parse_front_matter(
            path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        )
    except Exception:
        return False

    return (
        bool(body.strip())
        and metadata.get(
            "event_id"
        ) == event_id
        and metadata.get(
            "status"
        ) == "completed"
        and metadata.get(
            "type"
        ) == "event_unit"
    )


# ==============================================================
# EVENT INDEX
# ==============================================================

def save_event_index(
    date,
    events
):
    data = []

    for event in events:

        data.append({
            "event_id":
                event["event_id"],

            "date":
                event["date"],

            "language":
                CURRENT_LANGUAGE,

            "event_title":
                event["event_title"],

            "event_reason":
                event["event_reason"],

            "source_count":
                len(
                    event["articles"]
                ),

            "articles": [
                {
                    "index":
                        article["index"],

                    "title":
                        article["title"],

                    "source":
                        article["source"],

                    "source_url":
                        article["source_url"],

                    "path":
                        article["path"]
                }

                for article
                in event["articles"]
            ]
        })

    path = (
        event_units_dir(
            date,
            CURRENT_LANGUAGE
        )
        / EVENT_INDEX_FILE
    )

    write_json(
        path,
        data
    )

    return path


def load_event_index(
    date
):
    path = (
        event_units_dir(
            date,
            CURRENT_LANGUAGE
        )
        / EVENT_INDEX_FILE
    )

    if not path.exists():
        return None

    try:
        data = read_json(
            path,
            None
        )
    except Exception:
        return None

    if (
        not isinstance(
            data,
            list
        )
        or not data
    ):
        return None

    return data


# ==============================================================
# INSPECT EXISTING EVENT UNITS
# ==============================================================

def inspect_event_units(
    date
):
    target = event_units_dir(
        date,
        CURRENT_LANGUAGE
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

    index = load_event_index(
        date
    )

    if index is None:
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

    for event in index:

        event_id = str(
            event.get(
                "event_id",
                ""
            )
        ).strip()

        if not event_id:
            invalid.append(
                event_id
            )
            continue

        ids.append(
            event_id
        )

        matches = list(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        if not matches:

            missing.append(
                event_id
            )

        elif not any(
            event_unit_file_valid(
                path,
                event_id
            )
            for path in matches
        ):

            invalid.append(
                event_id
            )

    complete = (
        bool(ids)
        and not missing
        and not invalid
    )

    return {
        "exists": True,
        "complete": complete,
        "index": index,
        "missing": missing,
        "invalid": invalid,
        "unexpected": []
    }


# ==============================================================
# COMPLETE MARKER
# ==============================================================

def mark_event_units_complete(
    date,
    article_count,
    event_count
):
    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE
        )
        / EVENT_UNITS_COMPLETE_FILE
    )

    text = f"""EVENT_UNITS_COMPLETE
date: {date}
language: {CURRENT_LANGUAGE}
original_enriched_news: {article_count}
final_event_units: {event_count}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
"""

    write_text_atomic(
        path,
        text
    )

    return path


def remove_event_units_complete(
    date
):
    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE
        )
        / EVENT_UNITS_COMPLETE_FILE
    )

    if path.exists():
        path.unlink()


# ==============================================================
# COMPLETE EVENT UNITS
# ==============================================================

def complete_existing_event_units(
    date,
    events,
    article_count
):
    target = event_units_dir(
        date,
        CURRENT_LANGUAGE
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    generated = 0

    total = len(
        events
    )

    for position, event in enumerate(
        events,
        1
    ):

        event_id = event[
            "event_id"
        ]

        matches = list(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        if any(
            event_unit_file_valid(
                path,
                event_id
            )
            for path in matches
        ):

            print(
                f"[{position}/{total}] "
                f"⏭️ 已存在：{event_id}"
            )

            continue

        print(
            f"[{position}/{total}] "
            f"🔨 生成：{event_id}"
        )

        content = synthesize_event(
            event
        )

        if not content.strip():
            raise RuntimeError(
                f"❌ {event_id}综合结果为空"
            )

        path = save_event_unit(
            date,
            event,
            content
        )

        if not event_unit_file_valid(
            path,
            event_id
        ):
            raise RuntimeError(
                f"❌ {event_id}保存验证失败"
            )

        generated += 1

    # ----------------------------------------------------------
    # 最终完整性验证
    # ----------------------------------------------------------

    missing = []

    for event in events:

        event_id = event[
            "event_id"
        ]

        matches = list(
            target.glob(
                f"{event_id}_*.md"
            )
        )

        if not any(
            event_unit_file_valid(
                path,
                event_id
            )
            for path in matches
        ):
            missing.append(
                event_id
            )

    if missing:
        raise RuntimeError(
            f"❌ EventUnit最终仍然缺失："
            f"{missing[:50]}"
        )

    # ----------------------------------------------------------
    # 所有 EventUnit 都验证通过
    # 此时才允许生成 _COMPLETE
    # ----------------------------------------------------------

    marker = mark_event_units_complete(
        date,
        article_count,
        len(events)
    )

    print(
        f"✅ EVENT UNITS COMPLETE | "
        f"new={generated} | "
        f"total={len(events)} | "
        f"articles={article_count} | "
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
    # 严格语言协议
    # ----------------------------------------------------------

    CURRENT_LANGUAGE = normalize_language(
        language
    )

    lang = CURRENT_LANGUAGE

    # ----------------------------------------------------------
    # 建立目录
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

    print()
    print("=" * 70)
    print(
        "TASK 3 — EVENT UNIT SYNTHESIS V6.5.3"
    )
    print("=" * 70)

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
    # 已完成则直接恢复
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
    # 如果存在 _COMPLETE 但实际检查失败
    # 删除错误完成标记
    # ----------------------------------------------------------

    remove_event_units_complete(
        date
    )

    # ----------------------------------------------------------
    # Task 2结果
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

    print()
    print(
        "------------------------------------------------------------"
    )
    print(
        "TASK 2 RESULT"
    )
    print(
        "------------------------------------------------------------"
    )

    print(
        f"Path : {merged_path}"
    )

    # ----------------------------------------------------------
    # 读取 Task 2
    # ----------------------------------------------------------

    data = read_json(
        merged_path,
        None
    )

    final = (
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
            final,
            list
        )
        or not final
    ):
        raise RuntimeError(
            "❌ TASK 2结果无效："
            "clusters为空或不存在"
        )

    print(
        f"FINAL EVENT COMPONENTS : "
        f"{len(final)}"
    )

    # ----------------------------------------------------------
    # Task 2 ARTICLE 100% Coverage
    # ----------------------------------------------------------

    validate_global_article_coverage(
        date,
        final,
        len(news),
        "TASK 3 / TASK 2 RESULT"
    )

    # ----------------------------------------------------------
    # Global Event ID
    # ----------------------------------------------------------

    validate_final_event_ids(
        date,
        final
    )

    print(
        f"✅ FINAL EVENT COMPONENT ID VALIDATION | "
        f"count={len(final)}"
    )

    # ----------------------------------------------------------
    # 构建 EventUnit
    # ----------------------------------------------------------

    events = build_event_units(
        date,
        final,
        news
    )

    if len(events) != len(final):
        raise RuntimeError(
            f"❌ EventUnit数量异常："
            f"components={len(final)} "
            f"events={len(events)}"
        )

    print(
        f"EVENT UNITS TO MATERIALIZE : "
        f"{len(events)}"
    )

    # ----------------------------------------------------------
    # Event Index Coverage
    # ----------------------------------------------------------

    validate_event_index_coverage(
        date,
        events,
        len(news)
    )

    # ----------------------------------------------------------
    # 再次验证 Event ID
    # ----------------------------------------------------------

    validate_final_event_ids(
        date,
        events
    )

    # ----------------------------------------------------------
    # 保存 Event Index
    # ----------------------------------------------------------

    index_path = save_event_index(
        date,
        events
    )

    print(
        f"✅ Event Index saved: "
        f"{index_path}"
    )

    # ----------------------------------------------------------
    # 第二层 AI EventUnit Materialization
    # ----------------------------------------------------------

    complete_existing_event_units(
        date,
        events,
        len(news)
    )

    # ----------------------------------------------------------
    # 最终
    # ----------------------------------------------------------

    print()
    print(
        f"✅ TASK 3 COMPLETE | "
        f"{date}/{lang} | "
        f"events={len(events)} | "
        f"articles={len(news)}"
    )

    return True


# ==============================================================
# MAIN
# ==============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 3 "
            "EventUnit V6.5.3"
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
