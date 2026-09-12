#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Task 3 — EventUnit Synthesis
V6.5.4

TASK 3职责
==========

    1. 读取 Task 2 Global Merge 最终结果
    2. 验证 Task 2 ARTICLE 100% 覆盖
    3. 验证最终 Global Event ID
    4. 将 Final Event Components 转换为 EventUnit
    5. 建立 _event_index.json
    6. 对每个 EventUnit 执行第二层 AI 多来源综合
    7. 保存 EventUnit Markdown
    8. 每完成 30 个新 EventUnit，立即 Git checkpoint
    9. 最后一批 EventUnit 立即 Git checkpoint
   10. 验证所有 EventUnit 文件
   11. 所有 EventUnit 完整后生成 _COMPLETE
   12. 最终 Git checkpoint

完整架构：

    Task 1 Cluster
        ↓
    Task 2 Global Merge
        ↓
    Task 3 EventUnit Synthesis
        ↓
    EventUnit Validation
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
        eN
        zH

本文件绝不执行：

    upper()
    lower()

自动大小写转换。


重要原则
========

    _COMPLETE 只能由 Task 3 生成。

    YAML 不得 touch _COMPLETE。

    EventUnit Validator 不得生成 EventUnit。

    EventUnit Validator 不得创建 _COMPLETE。

    只有在：

        ARTICLE Coverage 100%
        +
        Event ID 全部合法
        +
        Event Index Coverage 100%
        +
        所有 EventUnit Markdown 有效

    全部成立之后，

        才允许生成 _COMPLETE。


Git 持久化原则
==============

    EventUnit 不允许等整个 Task 3 完成后才统一 Git 保存。

    每生成 30 个新的、有效的 EventUnit：

        EventUnit 文件写盘
              ↓
        文件验证
              ↓
        git add
              ↓
        git commit
              ↓
        git push

    最后一批不足 30 个时：

        立即 Git checkpoint。

    普通异常发生时，如果当前 batch 已经有新生成文件：

        尝试 checkpoint 当前已生成文件
        ↓
        再抛出原始异常

    因此下一次运行：

        已存在且有效 EventUnit
            ↓
        直接跳过
            ↓
        从第一个缺失 / 无效 EventUnit继续

    _COMPLETE 仍然只在全部 EventUnit 验证通过后生成。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from knowledge_common import (
    RAW_NEWS,
    EVENT_INDEX_FILE,
    EVENT_UNITS_COMPLETE_FILE,
    MERGED_CLUSTERS_FILE,
    MAX_ARTICLES_PER_EVENT_CONTEXT,
    ARTICLE_AGGREGATION_CONTENT_LIMIT,
    call_ai,
    load_all_enriched_news,
    validate_language,
    validate_global_article_coverage,
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
# PATH / FILE CONTRACT
# ==============================================================

EVENT_UNITS_SUFFIX = "EventUnit"

# --------------------------------------------------------------
# Task 3 Git Batch Persistence
# --------------------------------------------------------------

EVENT_UNIT_GIT_BATCH_SIZE = 30

# knowledge_task_3_eventunit.py
#     └── scripts/
#          └── knowledge_task_3_eventunit.py
#
# parents[0] = scripts
# parents[1] = 01_自生长知识系统
# parents[2] = 748686obsidian repository root
#
REPO_ROOT = Path(
    __file__
).resolve().parents[2]


def event_units_root(date):
    """
    Raw News/
    └── YYYY-MM-DD-EventUnit/
    """

    return (
        RAW_NEWS
        / f"{date}-{EVENT_UNITS_SUFFIX}"
    )


def language_dir(
    date,
    language=None,
):
    if language is None:
        language = CURRENT_LANGUAGE

    lang = validate_language(
        language
    )

    return (
        event_units_root(date)
        / lang
    )


def event_units_dir(
    date,
    language=None,
):
    return (
        language_dir(
            date,
            language,
        )
        / "event_units"
    )


def articles_dir(
    date,
    language=None,
):
    return (
        language_dir(
            date,
            language,
        )
        / "articles"
    )


def merged_clusters_path(
    date,
    language=None,
):
    """
    Task 2 Global Merge output contract：

    Raw News/
    └── YYYY-MM-DD-EventUnit/
        ├── en/
        │   └── _merged_clusters.json
        │
        └── zh/
            └── _merged_clusters.json
    """

    return (
        language_dir(
            date,
            language,
        )
        / MERGED_CLUSTERS_FILE
    )


# ==============================================================
# ATOMIC TEXT WRITE
# ==============================================================

def write_text_atomic(
    path,
    text,
):
    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:

        tmp.write_text(
            text,
            encoding="utf-8",
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
# GIT CHECKPOINT
# ==============================================================

def run_git_command(
    command,
    label,
):
    """
    Execute Git command from repository root.

    IMPORTANT:
        Git cwd MUST be repository root.

    This prevents the previous path error:

        01_自生长知识系统/
        01_自生长知识系统/
        Raw News/...

    which happened when project-root cwd was combined
    with repo-root-relative git paths.
    """

    print(
        f"▶️ {label}"
    )

    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if result.stdout.strip():
        print(
            result.stdout.strip()
        )

    if result.returncode != 0:

        if result.stderr.strip():
            print(
                result.stderr.strip()
            )

        raise RuntimeError(
            f"❌ Git command failed: "
            f"{' '.join(command)}"
        )

    return result


def git_checkpoint(
    date,
    reason,
):
    """
    Persist current Task 3 EventUnit state.

    This function intentionally stages the complete
    date/language EventUnit tree.

    It does NOT create _COMPLETE by itself.

    _COMPLETE remains controlled by Task 3 final validation.
    """

    lang = validate_language(
        CURRENT_LANGUAGE
    )

    event_root = (
        f"01_自生长知识系统/"
        f"Raw News/"
        f"{date}-EventUnit/"
        f"{lang}"
    )

    print()
    print(
        "============================================================"
    )
    print(
        "TASK 3 GIT CHECKPOINT"
    )
    print(
        "============================================================"
    )

    print(
        f"DATE     : {date}"
    )

    print(
        f"LANGUAGE : {lang}"
    )

    print(
        f"REASON   : {reason}"
    )

    print(
        f"REPO     : {REPO_ROOT}"
    )

    print(
        f"PATH     : {event_root}"
    )

    # ----------------------------------------------------------
    # Git identity
    # ----------------------------------------------------------

    run_git_command(
        [
            "git",
            "config",
            "user.name",
            "748686 Knowledge Bot",
        ],
        "git config user.name",
    )

    run_git_command(
        [
            "git",
            "config",
            "user.email",
            "41898282+github-actions[bot]@users.noreply.github.com",
        ],
        "git config user.email",
    )

    # ----------------------------------------------------------
    # Stage Task 3 date/language directory
    # ----------------------------------------------------------

    run_git_command(
        [
            "git",
            "add",
            "--",
            event_root,
        ],
        "git add Task 3 EventUnit",
    )

    # ----------------------------------------------------------
    # Check whether there are staged changes.
    #
    # This avoids creating empty commits.
    # ----------------------------------------------------------

    staged = subprocess.run(
        [
            "git",
            "diff",
            "--cached",
            "--quiet",
        ],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    if staged.returncode == 0:

        print(
            "ℹ️ GIT CHECKPOINT: no staged changes"
        )

        print(
            "============================================================"
        )

        return False

    if staged.returncode != 1:

        stderr = (
            staged.stderr.strip()
            or "unknown git diff error"
        )

        raise RuntimeError(
            f"❌ git diff --cached failed: "
            f"{stderr}"
        )

    # ----------------------------------------------------------
    # Commit
    # ----------------------------------------------------------

    commit_message = (
        f"chore(knowledge-task3): "
        f"{date}/{lang} checkpoint {reason}"
    )

    run_git_command(
        [
            "git",
            "commit",
            "-m",
            commit_message,
        ],
        "git commit Task 3 checkpoint",
    )

    # ----------------------------------------------------------
    # Push
    # ----------------------------------------------------------

    run_git_command(
        [
            "git",
            "push",
            "origin",
            "HEAD:main",
        ],
        "git push Task 3 checkpoint",
    )

    print(
        "✅ TASK 3 GIT CHECKPOINT PUSHED"
    )

    print(
        "============================================================"
    )

    return True


# ==============================================================
# GLOBAL EVENT ID VALIDATION
# ==============================================================

EVENT_ID_PATTERN = re.compile(
    r"EVT-\d{8}-\d{6}"
)


def validate_final_event_ids(
    date,
    events,
):
    if not isinstance(
        events,
        list,
    ):
        raise RuntimeError(
            f"❌ {date} Final Event Components 不是数组"
        )

    ids = []

    for position, event in enumerate(
        events,
        1,
    ):

        if not isinstance(
            event,
            dict,
        ):
            raise RuntimeError(
                f"❌ {date} Final Event Components "
                f"component[{position}]不是对象"
            )

        event_id = str(
            event.get(
                "event_id",
                "",
            )
        ).strip()

        if not event_id:
            raise RuntimeError(
                f"❌ {date} Final Event Components "
                f"component[{position}]缺少event_id"
            )

        ids.append(
            event_id
        )

    duplicates = sorted(
        {
            event_id
            for event_id in ids
            if ids.count(event_id) > 1
        }
    )

    if duplicates:
        raise RuntimeError(
            f"❌ {date} Final Event Components "
            f"存在重复 event_id："
            f"{duplicates[:20]}"
        )

    bad = [
        event_id
        for event_id in ids
        if not EVENT_ID_PATTERN.fullmatch(
            event_id
        )
    ]

    if bad:
        raise RuntimeError(
            f"❌ {date} Final Event Components "
            f"存在非法 Global Event ID："
            f"{bad[:20]}"
        )

    print(
        f"✅ FINAL EVENT ID VALIDATION | "
        f"count={len(ids)}"
    )


# ==============================================================
# BUILD EVENT UNITS
# ==============================================================

def build_event_units(
    date,
    clusters,
    news,
):
    events = []

    for component_position, cluster in enumerate(
        clusters,
        1,
    ):

        if not isinstance(
            cluster,
            dict,
        ):
            raise RuntimeError(
                f"❌ component[{component_position}]不是对象"
            )

        event_id = str(
            cluster.get(
                "event_id",
                "",
            )
        ).strip()

        if not event_id:
            raise RuntimeError(
                f"❌ component[{component_position}] "
                f"缺少event_id"
            )

        event_title = str(
            cluster.get(
                "event_title",
                "",
            )
        ).strip()

        if not event_title:
            event_title = "Untitled Event"

        event_reason = str(
            cluster.get(
                "event_reason",
                "",
            )
        ).strip()

        article_indexes = cluster.get(
            "article_indexes"
        )

        if not isinstance(
            article_indexes,
            list,
        ):
            raise RuntimeError(
                f"❌ {event_id} "
                f"article_indexes不是数组"
            )

        if not article_indexes:
            raise RuntimeError(
                f"❌ {event_id} "
                f"article_indexes为空"
            )

        articles = []

        for raw_index in article_indexes:

            if isinstance(
                raw_index,
                bool,
            ):
                raise RuntimeError(
                    f"❌ {event_id}存在非法ARTICLE ID："
                    f"{raw_index}"
                )

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

            if not isinstance(
                item,
                dict,
            ):
                raise RuntimeError(
                    f"❌ {event_id} ARTICLE {index} "
                    f"新闻对象非法"
                )

            metadata = item.get(
                "metadata",
                {},
            )

            if not isinstance(
                metadata,
                dict,
            ):
                metadata = {}

            articles.append({
                "index": index,

                "path": str(
                    item.get(
                        "path",
                        "",
                    )
                ),

                "title": str(
                    metadata.get(
                        "title",
                        "Untitled",
                    )
                    or "Untitled"
                ),

                "source": str(
                    metadata.get(
                        "source",
                        "Unknown",
                    )
                    or "Unknown"
                ),

                "source_url": str(
                    metadata.get(
                        "source_url",
                        "",
                    )
                    or ""
                ),

                "source_status": str(
                    metadata.get(
                        "source_status",
                        "",
                    )
                    or ""
                ),

                "content_status": str(
                    metadata.get(
                        "content_status",
                        "",
                    )
                    or ""
                ),

                "body": str(
                    item.get(
                        "body",
                        "",
                    )
                    or ""
                ),
            })

        events.append({
            "event_id": event_id,

            "date": date,

            "event_title": event_title,

            "event_reason": event_reason,

            "articles": articles,
        })

    return events


# ==============================================================
# EVENT INDEX COVERAGE
# ==============================================================

def validate_event_index_coverage(
    date,
    events,
    news_count,
):
    if not isinstance(
        events,
        list,
    ):
        raise RuntimeError(
            f"❌ {date} Event Index输入不是数组"
        )

    event_ids = set()

    article_occurrences = {}

    for event_position, event in enumerate(
        events,
        1,
    ):

        if not isinstance(
            event,
            dict,
        ):
            raise RuntimeError(
                f"❌ Event[{event_position}]不是对象"
            )

        event_id = str(
            event.get(
                "event_id",
                "",
            )
        ).strip()

        if not event_id:
            raise RuntimeError(
                f"❌ Event[{event_position}]缺少event_id"
            )

        if event_id in event_ids:
            raise RuntimeError(
                f"❌ {date} Event Index重复event_id："
                f"{event_id}"
            )

        event_ids.add(
            event_id
        )

        articles = event.get(
            "articles"
        )

        if not isinstance(
            articles,
            list,
        ):
            raise RuntimeError(
                f"❌ {event_id} articles不是数组"
            )

        if not articles:
            raise RuntimeError(
                f"❌ {event_id} articles为空"
            )

        for article in articles:

            if not isinstance(
                article,
                dict,
            ):
                raise RuntimeError(
                    f"❌ {event_id}存在非法ARTICLE对象"
                )

            try:
                index = int(
                    article["index"]
                )

            except Exception:
                raise RuntimeError(
                    f"❌ {event_id}存在非法ARTICLE index"
                )

            if isinstance(
                article.get("index"),
                bool,
            ):
                raise RuntimeError(
                    f"❌ {event_id}存在非法ARTICLE index"
                )

            article_occurrences.setdefault(
                index,
                [],
            ).append(
                event_id
            )

    expected = set(
        range(
            1,
            news_count + 1,
        )
    )

    actual = set(
        article_occurrences.keys()
    )

    missing = sorted(
        expected - actual
    )

    extra = sorted(
        actual - expected
    )

    duplicate = {
        index: event_ids_for_article
        for index, event_ids_for_article
        in article_occurrences.items()
        if len(event_ids_for_article) > 1
    }

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
            f"{dict(list(duplicate.items())[:20])}"
        )

    if actual != expected:
        raise RuntimeError(
            f"❌ {date} Event Index覆盖率失败："
            f"{len(actual)}/{news_count}"
        )

    print(
        f"✅ EVENT INDEX ARTICLE Coverage: "
        f"{news_count}/{news_count}"
    )


# ==============================================================
# LANGUAGE-SPECIFIC AI INSTRUCTIONS
# ==============================================================

def synthesis_language_instruction():

    if CURRENT_LANGUAGE == "en":

        return """
Output language:

    English

Use clear, professional English Markdown.

Do NOT translate the source material mechanically.

Preserve factual distinctions between sources.
"""

    if CURRENT_LANGUAGE == "zh":

        return """
输出语言：

    中文

使用清晰、专业、自然的中文 Markdown。

不要机械翻译来源。

必须保留不同来源之间的事实差异。
"""

    raise RuntimeError(
        f"❌ Invalid CURRENT_LANGUAGE："
        f"{CURRENT_LANGUAGE}"
    )


# ==============================================================
# AI EVENT SYNTHESIS
# ==============================================================

def synthesize_event(
    event,
):
    blocks = []

    articles = event[
        "articles"
    ][
        :MAX_ARTICLES_PER_EVENT_CONTEXT
    ]

    for article in articles:

        blocks.append(
            f"""### ARTICLE #{article['index']}
Title: {article['title']}
Source: {article['source']}
URL: {article['source_url']}
source_status: {article['source_status']}
content_status: {article['content_status']}

Content:
{article['body'][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}"""
        )

    joined = "\n\n".join(
        blocks
    )

    language_instruction = (
        synthesis_language_instruction()
    )

    prompt = f"""
You are performing the second-layer EventUnit synthesis
for the 748686 Self-Growing Knowledge System V6.5.3.

Date:
{event['date']}

Event ID:
{event['event_id']}

Event Title:
{event['event_title']}

First-layer Global Merge Event Reason:
{event['event_reason']}

Source Articles:

{joined}


YOUR TASK
=========

Transform these source articles into one high-quality
EventUnit knowledge document.


STRICT RULES
============

1. Only use information contained in the supplied material.

2. Never invent facts.

3. Never fabricate quotations.

4. Never fabricate numbers, dates, people, organizations,
   locations, causes, consequences or relationships.

5. Identify facts independently supported by multiple sources.

6. Preserve information that is unique to a single source.

7. Identify differences between sources.

8. If sources contradict each other, explicitly state the conflict.

9. Do not silently resolve factual conflicts.

10. If information is insufficient, explicitly state that
    the matter cannot currently be determined.

11. source_status and content_status must be respected.

12. If a source was not successfully fetched, do not claim
    that its complete original article was reviewed.

13. Do not treat repeated reporting as independent proof
    when the sources appear to reproduce the same information.

14. Distinguish clearly between:
       confirmed fact
       source-reported claim
       analysis
       uncertainty

15. Do not introduce unrelated background information.

16. Do not generate fictional context.

17. The final EventUnit must remain traceable to the
    supplied ARTICLE sources.


REQUIRED SECTIONS
=================

# Event Name

## Event Overview

## Core Facts

## Cross-Source Verification

## Unique Information by Source

## Different Country / Regional Perspectives

## Information Differences and Conflicts

## Known Current Impact

## What Cannot Currently Be Determined

## Sources

## Event Conclusion


{language_instruction}
"""

    system_prompt = """
You are the second-layer multi-source event synthesis engine
of the 748686 Self-Growing Knowledge System.

Your primary objectives are:

    factual accuracy
    source traceability
    conflict detection
    uncertainty preservation
    cross-source synthesis

You must never fabricate information.

You must not turn speculation into fact.
"""

    result = call_ai(
        prompt,
        system_prompt,
        0.2,
    )

    if not isinstance(
        result,
        str,
    ):
        result = str(
            result or ""
        )

    result = result.strip()

    if not result:
        raise RuntimeError(
            f"❌ {event['event_id']} AI综合结果为空"
        )

    return result


# ==============================================================
# EVENT UNIT FILENAME
# ==============================================================

def event_unit_filename(
    event,
):
    title = safe_name(
        event["event_title"]
    )

    if not title:
        title = "event"

    return (
        f"{event['event_id']}_"
        f"{title}.md"
    )


# ==============================================================
# SAVE EVENT UNIT
# ==============================================================

def save_event_unit(
    date,
    event,
    content,
):
    target = event_units_dir(
        date,
        CURRENT_LANGUAGE,
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        target
        / event_unit_filename(
            event
        )
    )

    sources = "\n".join(
        (
            f"- ARTICLE {article['index']} | "
            f"{article['source']} | "
            f"{article['title']} | "
            f"{article['source_url']}"
        )
        for article
        in event["articles"]
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

## 第一层 Global Merge 事件判断

{event['event_reason']}

## 第二层 AI 多来源综合

{content}

## 原始来源映射

{sources}
"""

    write_text_atomic(
        path,
        text,
    )

    return path


# ==============================================================
# EVENT UNIT FILE VALIDATION
# ==============================================================

def event_unit_file_valid(
    path,
    event_id,
):
    path = Path(
        path
    )

    if (
        not path.exists()
        or not path.is_file()
        or path.stat().st_size <= 0
    ):
        return False

    try:

        text = path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        metadata, body = parse_front_matter(
            text
        )

    except Exception:
        return False

    if not isinstance(
        metadata,
        dict,
    ):
        return False

    if not isinstance(
        body,
        str,
    ):
        body = str(
            body or ""
        )

    return (
        bool(
            body.strip()
        )
        and metadata.get(
            "event_id"
        ) == event_id
        and metadata.get(
            "status"
        ) == "completed"
        and metadata.get(
            "type"
        ) == "event_unit"
        and metadata.get(
            "language"
        ) == CURRENT_LANGUAGE
    )


# ==============================================================
# EVENT INDEX
# ==============================================================

def save_event_index(
    date,
    events,
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
                        article["path"],
                }

                for article
                in event["articles"]
            ],
        })

    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE,
        )
        / EVENT_INDEX_FILE
    )

    write_json(
        path,
        data,
    )

    return path


def load_event_index(
    date,
):
    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE,
        )
        / EVENT_INDEX_FILE
    )

    if not path.exists():
        return None

    try:

        data = read_json(
            path,
            None,
        )

    except Exception:
        return None

    if not isinstance(
        data,
        list,
    ):
        return None

    if not data:
        return None

    return data


# ==============================================================
# INSPECT EXISTING EVENT UNITS
# ==============================================================

def inspect_event_units(
    date,
):
    target = event_units_dir(
        date,
        CURRENT_LANGUAGE,
    )

    if not target.exists():
        return {
            "exists": False,
            "complete": False,
            "index": None,
            "missing": [],
            "invalid": [],
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
        }

    missing = []
    invalid = []
    ids = []

    for event in index:

        if not isinstance(
            event,
            dict,
        ):
            invalid.append(
                "<malformed>"
            )
            continue

        event_id = str(
            event.get(
                "event_id",
                "",
            )
        ).strip()

        if not event_id:

            invalid.append(
                "<empty-event-id>"
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
                event_id,
            )
            for path in matches
        ):

            invalid.append(
                event_id
            )

    complete = (
        bool(ids)
        and len(ids) == len(set(ids))
        and not missing
        and not invalid
    )

    return {
        "exists": True,
        "complete": complete,
        "index": index,
        "missing": missing,
        "invalid": invalid,
    }


# ==============================================================
# COMPLETE MARKER
# ==============================================================

def mark_event_units_complete(
    date,
    article_count,
    event_count,
):
    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE,
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
        text,
    )

    return path


def remove_event_units_complete(
    date,
):
    path = (
        language_dir(
            date,
            CURRENT_LANGUAGE,
        )
        / EVENT_UNITS_COMPLETE_FILE
    )

    if path.exists():

        path.unlink()

        print(
            f"⚠️ Removed stale _COMPLETE: "
            f"{path}"
        )


# ==============================================================
# FINAL EVENTUNIT MATERIALIZATION
# ==============================================================

def complete_existing_event_units(
    date,
    events,
    article_count,
):
    target = event_units_dir(
        date,
        CURRENT_LANGUAGE,
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated = 0
    skipped = 0

    total = len(
        events
    )

    # ----------------------------------------------------------
    # Number of NEW EventUnits generated since last Git checkpoint
    #
    # IMPORTANT:
    #
    # Existing valid EventUnits do NOT count toward this number.
    #
    # The requirement is:
    #
    #     every 30 NEW EventUnits
    #
    # immediately checkpoint.
    # ----------------------------------------------------------

    pending_since_checkpoint = 0

    try:

        for position, event in enumerate(
            events,
            1,
        ):

            event_id = event[
                "event_id"
            ]

            matches = list(
                target.glob(
                    f"{event_id}_*.md"
                )
            )

            valid_existing = any(
                event_unit_file_valid(
                    path,
                    event_id,
                )
                for path in matches
            )

            if valid_existing:

                print(
                    f"[{position}/{total}] "
                    f"⏭️ EXISTING VALID EVENTUNIT | "
                    f"{event_id}"
                )

                skipped += 1

                continue

            print(
                f"[{position}/{total}] "
                f"🔨 SYNTHESIZING EVENTUNIT | "
                f"{event_id}"
            )

            content = synthesize_event(
                event
            )

            if not content.strip():

                raise RuntimeError(
                    f"❌ {event_id} "
                    f"综合结果为空"
                )

            path = save_event_unit(
                date,
                event,
                content,
            )

            if not event_unit_file_valid(
                path,
                event_id,
            ):

                raise RuntimeError(
                    f"❌ {event_id} "
                    f"保存后验证失败："
                    f"{path}"
                )

            print(
                f"   ✅ SAVED | {path}"
            )

            generated += 1
            pending_since_checkpoint += 1

            print(
                f"   📦 Pending Git checkpoint: "
                f"{pending_since_checkpoint}/"
                f"{EVENT_UNIT_GIT_BATCH_SIZE}"
            )

            # --------------------------------------------------
            # EVERY 30 NEW EVENTUNITS
            # --------------------------------------------------

            if (
                pending_since_checkpoint
                >= EVENT_UNIT_GIT_BATCH_SIZE
            ):

                git_checkpoint(
                    date,
                    (
                        f"after "
                        f"{generated} newly generated "
                        f"EventUnits"
                    ),
                )

                pending_since_checkpoint = 0

        # ------------------------------------------------------
        # FINAL PARTIAL BATCH
        #
        # Example:
        #
        #     17 new EventUnits remain
        #
        # They MUST NOT wait for another 13.
        # Persist immediately.
        # ------------------------------------------------------

        if pending_since_checkpoint > 0:

            print()
            print(
                "📦 FINAL PARTIAL EVENTUNIT BATCH"
            )

            print(
                f"Pending new EventUnits: "
                f"{pending_since_checkpoint}"
            )

            git_checkpoint(
                date,
                (
                    f"final partial batch "
                    f"({pending_since_checkpoint} "
                    f"new EventUnits)"
                ),
            )

            pending_since_checkpoint = 0

        # ======================================================
        # FINAL EVENTUNIT FILE CHECK
        # ======================================================

        print()
        print(
            "------------------------------------------------------------"
        )
        print(
            "FINAL EVENTUNIT FILE VALIDATION"
        )
        print(
            "------------------------------------------------------------"
        )

        missing = []
        invalid = []

        for event in events:

            event_id = event[
                "event_id"
            ]

            matches = list(
                target.glob(
                    f"{event_id}_*.md"
                )
            )

            if not matches:

                missing.append(
                    event_id
                )

                continue

            if not any(
                event_unit_file_valid(
                    path,
                    event_id,
                )
                for path in matches
            ):

                invalid.append(
                    event_id
                )

        if missing:

            raise RuntimeError(
                f"❌ EventUnit最终缺失："
                f"{missing[:50]}"
            )

        if invalid:

            raise RuntimeError(
                f"❌ EventUnit最终验证失败："
                f"{invalid[:50]}"
            )

        # ======================================================
        # EVENT INDEX MUST STILL MATCH
        # ======================================================

        index = load_event_index(
            date
        )

        if index is None:

            raise RuntimeError(
                "❌ 最终 EventUnit 验证时 "
                "_event_index.json 不存在或无效"
            )

        if len(index) != len(events):

            raise RuntimeError(
                f"❌ Event Index数量与Final Event Components不一致："
                f"index={len(index)} "
                f"events={len(events)}"
            )

        # ======================================================
        # ONLY NOW CREATE _COMPLETE
        # ======================================================

        marker = mark_event_units_complete(
            date,
            article_count,
            len(events),
        )

        print()
        print(
            "------------------------------------------------------------"
        )
        print(
            "EVENTUNIT MATERIALIZATION COMPLETE"
        )
        print(
            "------------------------------------------------------------"
        )

        print(
            f"Generated : {generated}"
        )

        print(
            f"Existing  : {skipped}"
        )

        print(
            f"Total     : {len(events)}"
        )

        print(
            f"Articles  : {article_count}"
        )

        print(
            f"_COMPLETE : {marker}"
        )

        # ------------------------------------------------------
        # FINAL CHECKPOINT
        #
        # This captures:
        #
        #     _event_index.json
        #     _COMPLETE
        #     any remaining Task 3 files
        #
        # If the final batch was already checkpointed because
        # it was exactly 30, this will normally only commit
        # _COMPLETE.
        # ------------------------------------------------------

        git_checkpoint(
            date,
            "final EventUnit validation and _COMPLETE",
        )

        return True

    except Exception as exc:

        # ------------------------------------------------------
        # FAILURE RECOVERY CHECKPOINT
        #
        # If an ordinary Python exception happens after some
        # EventUnits have already been successfully written
        # since the last checkpoint, preserve them immediately.
        #
        # This does NOT replace the 30-file checkpoint mechanism.
        # It is an additional safety net.
        #
        # Hard process termination / runner cancellation cannot
        # execute this block; therefore the 30-file checkpoint
        # remains the primary durable recovery mechanism.
        # ------------------------------------------------------

        if pending_since_checkpoint > 0:

            print()
            print(
                "⚠️ TASK 3 FAILED WITH UNCHECKPOINTED "
                "EVENTUNITS"
            )

            print(
                f"Pending files: "
                f"{pending_since_checkpoint}"
            )

            try:

                git_checkpoint(
                    date,
                    (
                        f"failure recovery checkpoint "
                        f"({pending_since_checkpoint} "
                        f"new EventUnits)"
                    ),
                )

                print(
                    "✅ FAILURE RECOVERY CHECKPOINT SAVED"
                )

            except Exception as checkpoint_error:

                print()
                print(
                    "❌ FAILURE RECOVERY CHECKPOINT "
                    "ALSO FAILED"
                )

                print(
                    f"Checkpoint error: "
                    f"{checkpoint_error}"
                )

        raise exc


# ==============================================================
# TASK 3
# ==============================================================

def run_task_3(
    date,
    language,
):
    global CURRENT_LANGUAGE

    # ----------------------------------------------------------
    # STRICT LANGUAGE CONTRACT
    #
    # IMPORTANT:
    #
    # validate_language() ONLY accepts:
    #
    #     en
    #     zh
    #
    # No upper/lower conversion is performed.
    # ----------------------------------------------------------

    CURRENT_LANGUAGE = validate_language(
        language
    )

    lang = CURRENT_LANGUAGE

    # ----------------------------------------------------------
    # BUILD DIRECTORIES
    # ----------------------------------------------------------

    root = language_dir(
        date,
        lang,
    )

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    articles_dir(
        date,
        lang,
    ).mkdir(
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

    # ----------------------------------------------------------
    # LOAD ENRICHED NEWS
    # ----------------------------------------------------------

    news = load_all_enriched_news(
        date,
        lang,
    )

    if not isinstance(
        news,
        list,
    ):
        raise RuntimeError(
            f"❌ load_all_enriched_news返回非法结果："
            f"{type(news).__name__}"
        )

    if not news:

        raise RuntimeError(
            f"❌ {date}/{lang} "
            f"没有Enriched News"
        )

    # ----------------------------------------------------------
    # HEADER
    # ----------------------------------------------------------

    print()
    print("=" * 70)
    print(
        "TASK 3 — EVENTUNIT SYNTHESIS V6.5.4"
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

    print(
        f"GIT BATCH SIZE : "
        f"{EVENT_UNIT_GIT_BATCH_SIZE}"
    )

    print(
        f"GIT REPOSITORY : "
        f"{REPO_ROOT}"
    )

    # ----------------------------------------------------------
    # EXISTING COMPLETE RECOVERY
    # ----------------------------------------------------------

    inspection = inspect_event_units(
        date
    )

    if inspection[
        "complete"
    ]:

        print()
        print(
            f"♻️ TASK 3 EXISTING COMPLETE | "
            f"{date}/{lang}"
        )

        print(
            f"Event Index : "
            f"{len(inspection['index'])}"
        )

        return True

    # ----------------------------------------------------------
    # STALE COMPLETE MARKER
    # ----------------------------------------------------------

    remove_event_units_complete(
        date
    )

    # ----------------------------------------------------------
    # TASK 2 OUTPUT
    # ----------------------------------------------------------

    merged_path = merged_clusters_path(
        date,
        lang,
    )

    if not merged_path.exists():

        raise RuntimeError(
            f"❌ TASK 3找不到TASK 2 Global Merge结果："
            f"{merged_path}"
        )

    print()
    print(
        "------------------------------------------------------------"
    )
    print(
        "TASK 2 GLOBAL MERGE RESULT"
    )
    print(
        "------------------------------------------------------------"
    )

    print(
        f"Path : {merged_path}"
    )

    # ----------------------------------------------------------
    # READ TASK 2
    # ----------------------------------------------------------

    data = read_json(
        merged_path,
        None,
    )

    if not isinstance(
        data,
        dict,
    ):

        raise RuntimeError(
            "❌ TASK 2结果不是JSON对象"
        )

    final = data.get(
        "clusters"
    )

    if not isinstance(
        final,
        list,
    ):

        raise RuntimeError(
            "❌ TASK 2结果clusters不存在或不是数组"
        )

    if not final:

        raise RuntimeError(
            "❌ TASK 2结果clusters为空"
        )

    print(
        f"FINAL EVENT COMPONENTS : "
        f"{len(final)}"
    )

    # ----------------------------------------------------------
    # TASK 2 ARTICLE COVERAGE
    # ----------------------------------------------------------

    validate_global_article_coverage(
        date,
        final,
        len(news),
        "TASK 3 / TASK 2 RESULT",
    )

    # ----------------------------------------------------------
    # FINAL GLOBAL EVENT IDS
    # ----------------------------------------------------------

    validate_final_event_ids(
        date,
        final,
    )

    # ----------------------------------------------------------
    # BUILD EVENT UNITS
    # ----------------------------------------------------------

    events = build_event_units(
        date,
        final,
        news,
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
    # EVENT INDEX ARTICLE COVERAGE
    # ----------------------------------------------------------

    validate_event_index_coverage(
        date,
        events,
        len(news),
    )

    # ----------------------------------------------------------
    # EVENT ID SECOND VALIDATION
    # ----------------------------------------------------------

    validate_final_event_ids(
        date,
        events,
    )

    # ----------------------------------------------------------
    # SAVE EVENT INDEX
    # ----------------------------------------------------------

    index_path = save_event_index(
        date,
        events,
    )

    print(
        f"✅ EVENT INDEX SAVED | "
        f"{index_path}"
    )

    # ----------------------------------------------------------
    # SECOND-LAYER AI MATERIALIZATION
    #
    # Inside this function:
    #
    #     every 30 NEW EventUnits
    #         ↓
    #     git checkpoint
    #
    # Existing valid EventUnits:
    #
    #     skip
    #
    # Final partial batch:
    #
    #     checkpoint immediately
    # ----------------------------------------------------------

    complete_existing_event_units(
        date,
        events,
        len(news),
    )

    # ----------------------------------------------------------
    # FINAL
    # ----------------------------------------------------------

    print()
    print("=" * 70)

    print(
        f"✅ TASK 3 COMPLETE | "
        f"{date}/{lang} | "
        f"events={len(events)} | "
        f"articles={len(news)}"
    )

    print("=" * 70)

    return True


# ==============================================================
# MAIN
# ==============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Task 3 "
            "EventUnit Synthesis V6.5.4"
        )
    )

    parser.add_argument(
        "--date",
        required=True,
        help="YYYY-MM-DD",
    )

    parser.add_argument(
        "--language",
        choices=(
            "en",
            "zh",
        ),
        required=True,
        help="Only en or zh",
    )

    args = parser.parse_args()

    # ----------------------------------------------------------
    # STRICT LANGUAGE VALIDATION
    #
    # argparse choices + validate_language 双重保护。
    #
    # 绝不自动转换大小写。
    # ----------------------------------------------------------

    language = validate_language(
        args.language
    )

    run_task_3(
        args.date,
        language,
    )

    return 0


# ==============================================================
# ENTRY POINT
# ==============================================================

if __name__ == "__main__":
    sys.exit(
        main()
    )
