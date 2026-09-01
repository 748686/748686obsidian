#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Pipeline V6.5.3

V6.5.3 changes
------------------------------------------------------------
1. 保留 V6.5.0 Global Merge checkpoint / Union-Find /
   metadata history 架构。

2. Stage 1A AI 聚类失败不再直接终止整个任务。

3. AI覆盖异常自动修复；修复失败后进入 Recovery Queue。

4. Recovery Queue 按：
   30 -> 15 -> 8 -> 4 -> 2 -> 1
   逐级缩小。

5. Missing-only 时：
   安全覆盖部分保留；
   Missing 文章进入 Recovery Queue。

6. Duplicate / Extra / Malformed 时：
   整批隔离，避免污染后续 Global Merge。

7. 单篇 Recovery 最终自动作为 Singleton Event Cluster 保留。

8. 最终仍强制 ARTICLE 1..N 恰好覆盖一次；
   未解决文章禁止进入 Global Merge。

9. 原始 ARTICLE 编号始终保持不变。

10. EventUnit / Skill resume 行为保持不变。

11. Global ID 正式格式：
    EVT-YYYYMMDD-NNNNNN

12. AI 只产生 Local Cluster ID：
    C001 / C002 / ...

13. Global ID 唯一由 Python Global Registry 产生。

14. EN / ZH 共用当天 Global Registry。

15. Global Merge checkpoint 按 DATE + LANGUAGE 隔离。

16. Global Merge 每一轮重新对“当前 Cluster”连续分组：
    30 / 30 / 30 / ... / remainder

17. Global Merge 不使用 overlap。

18. 每一轮必须完成全部窗口后，才能根据本轮 Union-Find
    结果重建 Cluster 并进入下一轮。

19. 示例：
    137 -> 30 / 30 / 30 / 30 / 17
        -> 91

     91 -> 30 / 30 / 30 / 1
        -> 64

     64 -> 30 / 30 / 4
        -> 下一轮

20. 当完整一轮没有发生任何实际合并时：
    Global Merge CONVERGED。

21. Global Merge 窗口中的 Cluster 不重叠。
    跨窗口的潜在同事件关系通过“下一轮重新分组”继续获得比较机会。

22. 每一个 DATE + LANGUAGE 由外部 Workflow 作为独立
    Processing Unit 执行。

    固定顺序：
    2026-08-29 EN
    2026-08-29 ZH
    2026-08-30 EN
    2026-08-30 ZH
    2026-08-31 EN
    2026-08-31 ZH

    Python 本身只负责一个 DATE + LANGUAGE Unit。
------------------------------------------------------------
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
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from zoneinfo import ZoneInfo


# ==============================================================
# PATHS
# ==============================================================

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


# ==============================================================
# FILE CONTRACTS
# ==============================================================

EVENT_UNITS_SUFFIX = "EventUnit"

EVENT_INDEX_FILE = "_event_index.json"

EVENT_UNITS_COMPLETE_FILE = "_EVENT_UNITS_COMPLETE"

SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"

GLOBAL_CLUSTER_REGISTRY_FILE = "_global_cluster_registry.json"


# ==============================================================
# AI CONFIG
# ==============================================================

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


# ==============================================================
# PIPELINE CONFIG
# ==============================================================

# Stage 1A
AGGREGATION_BATCH_SIZE = 30

# Stage 1B
# --------------------------------------------------------------
# 每一轮 Global Merge 都从当前 Cluster 第1个开始，
# 连续每30个形成一个窗口。
#
# 例如：
#
# 137 -> 30 / 30 / 30 / 30 / 17
# 91  -> 30 / 30 / 30 / 1
# 64  -> 30 / 30 / 4
#
# 注意：
# 不再使用 15 overlap。
# --------------------------------------------------------------

GLOBAL_MERGE_WINDOW_SIZE = 30

GLOBAL_MERGE_OVERLAP = 0

# 一个 EventUnit 最多向第二层 AI 提供多少篇原始文章
MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000

CLUSTER_REPAIR_ATTEMPTS = 2


# Stage 1A Recovery
RECOVERY_BATCH_SIZES = (
    30,
    15,
    8,
    4,
    2,
    1,
)


BEIJING_TZ = ZoneInfo("Asia/Shanghai")


# ==============================================================
# LANGUAGE
# ==============================================================

CURRENT_LANGUAGE = None

SUPPORTED_LANGUAGES = (
    "EN",
    "ZH",
)


# ==============================================================
# TIME
# ==============================================================

def now():
    return datetime.now(BEIJING_TZ)


# ==============================================================
# DIRECTORY HELPERS
# ==============================================================

def event_units_root(date):
    """
    当天 EventUnit 总目录：

    YYYY-MM-DD-EventUnit
    """
    return RAW_NEWS / f"{date}-EventUnit"


def language_dir(date, language=None):
    lang = language or CURRENT_LANGUAGE

    if lang not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ 未设置合法语言批次：{lang}"
        )

    return (
        event_units_root(date)
        / lang
    )


def event_units_dir(date):
    """
    当前语言 EventUnit 实际结果目录。
    """
    return (
        language_dir(date)
        / "event_units"
    )


def articles_dir(date):
    return (
        language_dir(date)
        / "articles"
    )


def conflict_log_path(date):
    return (
        LOGS
        / f"{date}_{CURRENT_LANGUAGE}_event_aggregation_conflicts.log"
    )


def global_merge_checkpoint_path(date):
    """
    Global Merge checkpoint 必须按 DATE + LANGUAGE 隔离。

    例如：

    2026-08-29-EventUnit/
        EN/
            event_units/
                _global_merge_checkpoint.json

        ZH/
            event_units/
                _global_merge_checkpoint.json
    """
    return (
        event_units_dir(date)
        / GLOBAL_MERGE_CHECKPOINT_FILE
    )


def global_cluster_registry_path(date):
    """
    Global Registry 属于 DATE 总目录。

    EN / ZH 共用。

    例如：

    2026-08-29-EventUnit/
        _global_cluster_registry.json
    """
    return (
        event_units_root(date)
        / GLOBAL_CLUSTER_REGISTRY_FILE
    )


# ==============================================================
# LOGGING
# ==============================================================

def log_conflict(
    date,
    stage,
    message,
    details=None,
):
    LOGS.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = [
        "",
        "=" * 80,
        f"TIME: {now().isoformat()}",
        f"DATE: {date}",
        f"LANGUAGE: {CURRENT_LANGUAGE}",
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
                    indent=2,
                )
            )
        except Exception:
            detail = str(details)

        lines += [
            "DETAILS:",
            detail,
        ]

    lines += [
        "=" * 80,
        "",
    ]

    with conflict_log_path(date).open(
        "a",
        encoding="utf-8",
    ) as f:
        f.write(
            "\n".join(lines)
        )

    print(
        f"⚠️ {message}"
    )

    print(
        f" Conflict log: "
        f"{conflict_log_path(date)}"
    )


# ==============================================================
# JSON
# ==============================================================

def read_json(
    path,
    default=None,
):
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


def write_json(
    path,
    data,
):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def write_json_atomic(
    path,
    data,
):
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    try:
        payload = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        )

        tmp.write_text(
            payload,
            encoding="utf-8",
        )

        json.loads(
            tmp.read_text(
                encoding="utf-8"
            )
        )

        with tmp.open("rb") as f:
            os.fsync(
                f.fileno()
            )

        tmp.replace(path)

    except Exception:
        try:
            if tmp.exists():
                tmp.unlink()
        except Exception:
            pass

        raise


# ==============================================================
# AI JSON
# ==============================================================

def parse_ai_json(
    result,
    context,
):
    text = str(
        result
    ).strip()

    if text.startswith("```"):
        text = re.sub(
            r"^```(?:json)?\s*",
            "",
            text,
            flags=re.I,
        )

        text = re.sub(
            r"\s*```$",
            "",
            text,
        ).strip()

    try:
        return json.loads(text)

    except Exception:
        start = text.find("{")
        end = text.rfind("}")

        if start >= 0 and end > start:
            candidate = text[
                start:end + 1
            ]

            try:
                return json.loads(
                    candidate
                )
            except Exception:
                pass

        raise RuntimeError(
            f"❌ AI JSON解析失败："
            f"{context}\n\n"
            f"{text[:5000]}"
        )


# ==============================================================
# SAFE NAME
# ==============================================================

def safe_name(text):
    text = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        str(text or ""),
    )

    text = re.sub(
        r"\s+",
        " ",
        text,
    ).strip()

    return (
        text[:120]
        or "未命名"
    )


# ==============================================================
# FRONT MATTER
# ==============================================================

def parse_front_matter(content):
    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2,
    )

    if len(parts) < 3:
        return {}, content

    data = {}

    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue

        k, v = line.split(
            ":",
            1,
        )

        data[
            k.strip()
        ] = (
            v.strip()
            .strip('"')
            .strip("'")
        )

    return (
        data,
        parts[2].lstrip(),
    )


# ==============================================================
# AI THROTTLE
# ==============================================================

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
            f" ⏳ AI请求节流等待 "
            f"{remaining:.1f}s"
        )

        time.sleep(
            remaining
        )

    _LAST_AI_REQUEST_TIME = (
        time.monotonic()
    )


def parse_retry_after(headers):
    if headers is None:
        return None

    value = headers.get(
        "Retry-After"
    )

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


def calculate_429_backoff(
    retry_number,
):
    base = min(
        AI_429_BACKOFF_BASE
        * (
            2
            ** (
                retry_number - 1
            )
        ),
        AI_429_BACKOFF_MAX,
    )

    return min(
        base
        + random.uniform(
            0,
            AI_429_JITTER_MAX,
        ),
        AI_429_BACKOFF_MAX,
    )


# ==============================================================
# AI CALL
# ==============================================================

def call_ai(
    prompt,
    system_prompt=None,
    temperature=DEFAULT_TEMPERATURE,
):
    key = os.getenv(
        AGNES_API_KEY_ENV,
        "",
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
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": temperature,
        },
        ensure_ascii=False,
    ).encode()

    req = Request(
        AGNES_BASE_URL
        + "/chat/completions",
        data=payload,
        headers={
            "Authorization":
                f"Bearer {key}",
            "Content-Type":
                "application/json",
            "Accept":
                "application/json",
            "User-Agent":
                "748686-Knowledge-Pipeline/6.5.3",
        },
        method="POST",
    )

    for attempt in range(
        AI_MAX_429_RETRIES + 1
    ):
        wait_for_ai_throttle()

        try:
            with urlopen(
                req,
                timeout=AI_TIMEOUT,
            ) as r:
                raw = (
                    r.read()
                    .decode(
                        "utf-8"
                    )
                )

            try:
                data = json.loads(
                    raw
                )
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
                        ensure_ascii=False,
                    )[:5000]
                ) from e

            if not str(
                result
            ).strip():
                raise RuntimeError(
                    "❌ AGNES.ai 返回空内容"
                )

            return str(
                result
            ).strip()

        except HTTPError as e:
            body = ""

            try:
                body = (
                    e.read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )
            except Exception:
                pass

            if e.code == 429:
                if (
                    attempt
                    >= AI_MAX_429_RETRIES
                ):
                    print(
                        "❌ AGNES.ai HTTP 429 — "
                        "已达到最大自动重试次数"
                    )

                    raise RuntimeError(
                        "❌ AGNES.ai HTTP 429："
                        "自动重试次数耗尽"
                    ) from e

                retry_number = (
                    attempt + 1
                )

                retry_after = (
                    parse_retry_after(
                        e.headers
                    )
                )

                if retry_after is not None:
                    wait_seconds = min(
                        retry_after,
                        AI_429_BACKOFF_MAX,
                    )
                    source = (
                        "Retry-After"
                    )

                else:
                    wait_seconds = (
                        calculate_429_backoff(
                            retry_number
                        )
                    )
                    source = (
                        "指数退避"
                    )

                print(
                    f"⚠️ AGNES.ai HTTP 429 — "
                    f"Retry "
                    f"{retry_number}/"
                    f"{AI_MAX_429_RETRIES}, "
                    f"Wait "
                    f"{wait_seconds:.1f}s, "
                    f"Source={source}"
                )

                if body:
                    print(
                        " Response:",
                        re.sub(
                            r"\s+",
                            " ",
                            body,
                        ).strip()[:1000],
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


# ==============================================================
# SKILLS
# ==============================================================

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
                errors="replace",
            ),
        }

    return out


def load_routes():
    routes = read_json(
        ROUTES_FILE,
        {},
    )

    if not routes:
        raise RuntimeError(
            "skill_routes.json为空或不存在"
        )

    return routes


def route_skills(
    category,
    routes,
    skills,
):
    selected = []

    for name in routes.get(
        category,
        [],
    ):
        if name not in skills:
            raise RuntimeError(
                "❌ skill_routes.json引用不存在Skill："
                f"{name}"
            )

        selected.append(
            skills[name]
        )

    return selected


# ==============================================================
# ENRICHED NEWS
# ==============================================================

def get_enriched_files(
    date,
    language,
):
    root = (
        RAW_NEWS
        / f"{date}-Enriched"
        / language
    )

    if not root.exists():
        raise FileNotFoundError(
            f"没有找到 "
            f"{date} / {language} "
            f"Enriched目录：{root}"
        )

    return sorted(
        root.rglob("*.md")
    )


def load_news_file(path):
    content = path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    meta, body = (
        parse_front_matter(
            content
        )
    )

    return {
        "path": path,
        "metadata": meta,
        "body": body,
        "content": content,
    }


def load_all_enriched_news(
    date,
    language,
):
    files = get_enriched_files(
        date,
        language,
    )

    print(
        f"Enriched files: "
        f"{len(files)}"
    )

    if not files:
        raise RuntimeError(
            f"❌ {date} / {language} "
            "没有Enriched新闻"
        )

    items = [
        load_news_file(p)
        for p in files
    ]

    items = [
        x
        for x in items
        if x["metadata"]
        .get(
            "title",
            "",
        )
        .strip()
    ]

    if not items:
        raise RuntimeError(
            f"❌ {date} / {language} "
            "没有有效新闻"
        )

    def score(x):
        try:
            return float(
                x["metadata"].get(
                    "horizon_score",
                    0,
                )
            )
        except Exception:
            return 0

    items.sort(
        key=score,
        reverse=True,
    )

    print(
        f"Valid news: "
        f"{len(items)}"
    )

    return items


# ==============================================================
# ARTICLE DIGEST
# ==============================================================

def build_article_digest(
    item,
    index,
):
    m = item["metadata"]

    return (
        f"[ARTICLE {index}] "
        f"标题："
        f"{m.get('title', 'Untitled')} "
        f"来源："
        f"{m.get('source', 'Unknown')} "
        f"原文链接："
        f"{m.get('source_url', '')} "
        f"来源状态："
        f"{m.get('source_status', '')} "
        f"内容状态："
        f"{m.get('content_status', '')} "
        f"内容："
        f"{item['body'][:ARTICLE_CLUSTER_CONTENT_LIMIT]}"
    )


# ==============================================================
# CLUSTER COVERAGE
# ==============================================================

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

    occ = {}

    malformed = []

    for pos, c in enumerate(
        clusters,
        1,
    ):
        if not isinstance(
            c,
            dict,
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

        for v in ids:
            try:
                i = int(v)
            except Exception:
                malformed.append(
                    f"cluster[{pos}] "
                    f"非法ARTICLE ID：{v}"
                )
                continue

            occ.setdefault(
                i,
                [],
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
            malformed,
    }


def valid_issues(i):
    return not any(
        [
            i["duplicate"],
            i["missing"],
            i["extra"],
            i["malformed"],
        ]
    )


def normalize_clusters(cs):
    out = []

    for c in cs:
        if not isinstance(
            c,
            dict,
        ):
            out.append(c)
            continue

        d = dict(c)

        ids = d.get(
            "article_indexes",
            [],
        )

        if isinstance(
            ids,
            list,
        ):
            d[
                "article_indexes"
            ] = [
                int(x)
                if str(x)
                .lstrip("-")
                .isdigit()
                else x
                for x in ids
            ]

        out.append(d)

    return out


# ==============================================================
# STAGE 1A — INITIAL AI CLUSTERING
# ==============================================================

def cluster_news_batch(
    date,
    items,
    indexes,
):
    expected = [
        int(x)
        for x in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[i],
        )
        for i, item
        in enumerate(items)
    )

    prompt = f"""
你正在执行748686自生长知识系统V6.5.3第一层事件聚类。

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

重要输出限制：

- cluster_id只是本批次Local Cluster ID，例如C001、C002。
- 不要生成EVT-/REC-/GM-等Global ID。
- Global Cluster ID由Python全局注册器统一生成。
- 只输出JSON。
- 不要Markdown。
- 不要解释。
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
}}
"""

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

        compact_prompt = f"""
748686 V6.5.3 新闻事件聚类JSON修复。

日期：{date}

ARTICLE范围：
{json.dumps(expected)}

文章：

{joined}

重新聚类。

严格要求：

1. 每个ARTICLE恰好一次。
2. 同一具体现实事件合并。
3. 不同事件分开。
4. 不能确定宁可分开。
5. 每个cluster只返回：
   cluster_id
   article_indexes
   event_title
   event_reason
6. event_title不超过40字。
7. event_reason不超过80字。
8. 绝对不要输出文章正文。
9. 只输出JSON。
10. 不要代码围栏。
11. 不要解释。

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
}}
"""

        print(
            " ⚠️ 第一轮聚类JSON解析失败，"
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


# ==============================================================
# STAGE 1A — REPAIR
# ==============================================================

def repair_cluster_news_batch(
    date,
    items,
    indexes,
    broken,
    issues,
    attempt,
):
    expected = [
        int(x)
        for x in indexes
    ]

    joined = "\n\n".join(
        build_article_digest(
            item,
            expected[i],
        )
        for i, item
        in enumerate(items)
    )

    prompt = f"""
修复748686 V6.5.3 ARTICLE覆盖冲突。

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
    indent=2,
)}

检测问题：

{json.dumps(
    issues,
    ensure_ascii=False,
    indent=2,
)}

重新判断全部文章。

要求：

1. cluster_id只能是Local Cluster ID，例如C001。
2. 不得生成EVT-/REC-/GM- ID。
3. 同事件合并。
4. 不同事件分开。
5. 每篇ARTICLE恰好一次。
6. Missing=0。
7. Duplicate=0。
8. Extra=0。
9. Malformed=0。
10. 不得遗漏任何ARTICLE。
11. 只输出JSON。
12. 不要解释。

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
}}
"""

    data = parse_ai_json(
        call_ai(
            prompt,
            (
                "你是新闻事件聚类冲突修复专家。"
                "必须完整覆盖输入ARTICLE。"
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


# ==============================================================
# CLUSTER VALIDATION
# ==============================================================

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
        f"❌ {context} "
        f"聚类覆盖失败："
        f"{issues}"
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

    才允许保留已经唯一出现的ARTICLE。
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
        int(x)
        for x in expected_indexes
    }

    actual = set()

    for cluster in clusters:
        for value in cluster.get(
            "article_indexes",
            [],
        ):
            actual.add(
                int(value)
            )

    return sorted(
        actual & expected
    )


# ==============================================================
# STAGE 1A — AI CLUSTER + REPAIR
# ==============================================================

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

    V6.5.3原则：

    Missing-only：
        安全保留已唯一覆盖ARTICLE。
        Missing进入Recovery Queue。

    Duplicate / Extra / Malformed：
        整批隔离。

    AI异常：
        整批隔离。
        不终止整个日期Unit。
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
            "AI第一次聚类返回非法ARTICLE归属，启动自动修复。",
            {
                "issues": issues,
                "clusters": clusters,
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

                issues = (
                    inspect_cluster_assignment(
                        clusters,
                        expected,
                    )
                )

                if valid_issues(
                    issues
                ):
                    print(
                        " ✅ Cluster conflict "
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
                    str(repair_error),
                )

        final_issues = (
            inspect_cluster_assignment(
                clusters or [],
                expected,
            )
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
            safe = _safe_covered_indexes(
                clusters,
                expected,
            )

            unresolved = sorted(
                set(expected)
                - set(safe)
            )

            if safe and unresolved:
                print(
                    f" 🟡 Missing-only："
                    f"安全保留 {len(safe)} 篇，"
                    f"隔离 {len(unresolved)} 篇："
                    f"{unresolved}"
                )

                log_conflict(
                    date,
                    f"STAGE 1A / {batch_label}",
                    "修复失败，但仅存在Missing；"
                    "安全覆盖部分保留，"
                    "Missing进入Recovery Queue。",
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

        # ------------------------------------------------------
        # Duplicate / Extra / Malformed
        # ------------------------------------------------------

        print(
            f" 🔴 Batch结果不安全，"
            f"整批进入Recovery Queue："
            f"{expected}"
        )

        log_conflict(
            date,
            f"STAGE 1A / {batch_label}",
            "自动修复失败；整批隔离，"
            "防止错误结果污染Global Merge。",
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
            "本批AI异常；整批隔离进入Recovery Queue，不终止任务。",
            str(e),
        )

        print(
            " 🔴 AI exception isolated into "
            f"Recovery Queue: {expected}"
        )

        return (
            "failed",
            [],
            expected,
        )


# ==============================================================
# GLOBAL CLUSTER REGISTRY
# ==============================================================

def create_global_cluster_registry(
    date,
):
    """
    Python Global Cluster Registry。

    AI Local ID 与 Global ID 完全分离。

    AI：
        C001
        C002

    Python：
        EVT-YYYYMMDD-000001
        EVT-YYYYMMDD-000002
    """

    return {
        "date":
            str(date),

        "next_sequence":
            1,

        "registered":
            [],
    }


def persist_global_cluster_registry(
    date,
    registry,
):
    write_json_atomic(
        global_cluster_registry_path(
            date
        ),
        {
            "version":
                "6.5.3",

            "date":
                registry["date"],

            "next_sequence":
                int(
                    registry[
                        "next_sequence"
                    ]
                ),

            "registered":
                registry[
                    "registered"
                ],

            "saved_at":
                now().isoformat(),
        },
    )


def validate_global_registry(
    date,
    registry,
):
    if not isinstance(
        registry,
        dict,
    ):
        raise RuntimeError(
            f"❌ {date} Global Registry不是对象"
        )

    if registry.get(
        "date"
    ) != str(date):
        raise RuntimeError(
            f"❌ {date} Global Registry日期不一致"
        )

    try:
        next_sequence = int(
            registry.get(
                "next_sequence",
                0,
            )
        )
    except Exception as e:
        raise RuntimeError(
            f"❌ {date} Global Registry next_sequence非法"
        ) from e

    if next_sequence < 1:
        raise RuntimeError(
            f"❌ {date} Global Registry next_sequence非法"
        )

    registered = registry.get(
        "registered"
    )

    if not isinstance(
        registered,
        list,
    ):
        raise RuntimeError(
            f"❌ {date} Global Registry registered非法"
        )

    global_ids = set()

    max_seq = 0

    for r in registered:
        if not isinstance(
            r,
            dict,
        ):
            raise RuntimeError(
                f"❌ {date} Global Registry存在非法记录"
            )

        gid = str(
            r.get(
                "global_cluster_id",
                "",
            )
        ).strip()

        if not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            gid,
        ):
            raise RuntimeError(
                f"❌ {date} Registry存在非法Global ID："
                f"{gid}"
            )

        if gid in global_ids:
            raise RuntimeError(
                f"❌ {date} Registry存在重复Global ID："
                f"{gid}"
            )

        global_ids.add(gid)

        seq = int(
            gid[-6:]
        )

        max_seq = max(
            max_seq,
            seq,
        )

    if next_sequence <= max_seq:
        raise RuntimeError(
            f"❌ {date} Registry next_sequence="
            f"{next_sequence} "
            f"<= max_seq={max_seq}"
        )


def register_global_cluster_ids(
    date,
    clusters,
    registry,
    source,
):
    """
    唯一的 Global Cluster ID 生成入口。

    AI：
        C001/C002

    Registry：
        EVT-YYYYMMDD-NNNNNN

    Recovery 使用同一 Registry，
    不会重新使用已经分配过的序号。
    """

    validate_global_registry(
        date,
        registry,
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

        if not local_id:
            raise RuntimeError(
                f"❌ {date} Global Registry收到空Local Cluster ID"
            )

        seq = int(
            registry[
                "next_sequence"
            ]
        )

        global_id = (
            f"EVT-{date}-{seq:06d}"
        )

        registry[
            "next_sequence"
        ] = seq + 1

        d[
            "local_cluster_id"
        ] = local_id

        d[
            "cluster_id"
        ] = global_id

        d[
            "member_cluster_ids"
        ] = [
            global_id
        ]

        d[
            "global_id_source"
        ] = "python_global_registry"

        d[
            "global_registry_source"
        ] = source

        registry[
            "registered"
        ].append(
            {
                "global_cluster_id":
                    global_id,

                "local_cluster_id":
                    local_id,

                "source":
                    source,

                "article_indexes":
                    sorted(
                        set(
                            int(x)
                            for x
                            in d.get(
                                "article_indexes",
                                [],
                            )
                        )
                    ),
            }
        )

        out.append(d)

    persist_global_cluster_registry(
        date,
        registry,
    )

    return out


# ==============================================================
# LOCAL CLUSTER RECORD
# ==============================================================

def _make_cluster_records(
    batch_identifier,
    clusters,
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
                    [],
                )
            )
        )

        if not indexes:
            continue

        local_id = str(
            c.get(
                "cluster_id",
                "C001",
            )
        ).strip()

        out.append(
            {
                "cluster_id":
                    local_id,

                "local_cluster_id":
                    local_id,

                "event_title":
                    c.get(
                        "event_title",
                        "未命名事件",
                    ),

                "event_reason":
                    c.get(
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


# ==============================================================
# APPEND SAFE CLUSTERS
# ==============================================================

def _append_safe_clusters(
    allc,
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

    local_records = (
        _make_cluster_records(
            batch_no,
            clusters,
        )
    )

    allc.extend(
        register_global_cluster_ids(
            date,
            local_records,
            registry,
            context,
        )
    )


# ==============================================================
# RECOVERY PASS
# ==============================================================

def _recovery_pass(
    date,
    news,
    indexes,
    recovery_pass_no,
    batch_size,
    registry,
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
            batch_size,
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

    for sub_no, sub_indexes in enumerate(
        sub_batches,
        1,
    ):
        items = [
            news[index - 1]
            for index in sub_indexes
        ]

        label = (
            f"RECOVERY "
            f"{recovery_pass_no} / "
            f"BATCH {sub_no}"
        )

        print(
            f" 🔹 {label}: "
            f"{sub_indexes}"
        )

        # ------------------------------------------------------
        # 单篇最终安全降级为 Singleton
        # ------------------------------------------------------

        if len(
            sub_indexes
        ) == 1:
            index = sub_indexes[0]

            title = (
                news[index - 1]
                ["metadata"]
                .get(
                    "title",
                    "未命名事件",
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
                        "该文章在恢复阶段作为独立事件单元保留。",
                }
            )

            print(
                f" 🟢 Singleton安全保留："
                f"ARTICLE {index}"
            )

            continue

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
            safe = (
                _safe_covered_indexes(
                    clusters,
                    sub_indexes,
                )
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
                        [],
                    )
                    if int(x)
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


# ==============================================================
# STAGE 1A
# ==============================================================
# INITIAL 30-BATCH + RECOVERY
# ==============================================================

def build_initial_clusters(
    date,
    news,
    registry=None,
):
    allc = []

    total = len(
        news
    )

    if registry is None:
        registry = read_json(
            global_cluster_registry_path(
                date
            ),
            None,
        )

        if not isinstance(
            registry,
            dict,
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

    validate_global_registry(
        date,
        registry,
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "STAGE 1A — "
        "AI EVENT CLUSTERING V6.5.3"
    )

    print(
        "=" * 70
    )

    print(
        f"Input Enriched News: "
        f"{total}"
    )

    print(
        f"Normal Batch Size: "
        f"{AGGREGATION_BATCH_SIZE}"
    )

    print(
        "Failure Policy: isolate -> "
        "recovery queue -> "
        "30/15/8/4/2/1 -> singleton"
    )

    pending = []

    normal_batch_no = 0

    # ==========================================================
    # 第一阶段：正常30篇连续处理
    # ==========================================================

    for start in range(
        0,
        total,
        AGGREGATION_BATCH_SIZE,
    ):
        normal_batch_no += 1

        end = min(
            start
            + AGGREGATION_BATCH_SIZE,
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
            f"\n🔹 Cluster Batch "
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
                (
                    f"CLUSTER BATCH "
                    f"{normal_batch_no}"
                ),
            )
        )

        if status == "complete":

            _append_safe_clusters(
                allc,
                clusters,
                normal_batch_no,
                indexes,
                date,
                (
                    f"Batch "
                    f"{normal_batch_no}"
                ),
                registry,
            )

            print(
                f" Clusters generated: "
                f"{len(clusters)}"
            )

        elif status == "partial":

            safe = (
                _safe_covered_indexes(
                    clusters,
                    indexes,
                )
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
                        [],
                    )
                    if int(x)
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
                validate_cluster_coverage(
                    safe_clusters,
                    safe,
                    (
                        f"{date} "
                        f"Batch "
                        f"{normal_batch_no} "
                        "SAFE PART"
                    ),
                    date,
                )

                local_records = (
                    _make_cluster_records(
                        normal_batch_no,
                        safe_clusters,
                    )
                )

                allc.extend(
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

            pending.extend(
                unresolved
            )

            print(
                f" 🟡 Safe clusters kept="
                f"{len(safe_clusters)} | "
                f"Pending={len(pending)}"
            )

        else:

            pending.extend(
                unresolved
            )

            print(
                f" 🔴 Entire batch isolated | "
                f"Pending={len(pending)}"
            )

    # ==========================================================
    # 第二阶段：Recovery Queue
    # ==========================================================

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
                registry,
            )
        )

        local_records = (
            _make_cluster_records(
                f"RECOVERY PASS {pass_no}",
                recovered,
            )
        )

        allc.extend(
            register_global_cluster_ids(
                date,
                local_records,
                registry,
                f"Recovery Pass {pass_no}",
            )
        )

        pending.extend(
            unresolved
        )

        print(
            f" Recovery Pass "
            f"{pass_no}: "
            f"recovered="
            f"{len(recovered)} | "
            f"still_pending="
            f"{len(pending)}"
        )

    # ==========================================================
    # 最终安全闸
    # ==========================================================

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
            },
        )

        raise RuntimeError(
            "❌ V6.5.3 Stage 1A最终仍有未处理ARTICLE："
            f"{sorted(set(pending))}"
        )

    validate_cluster_coverage(
        allc,
        range(
            1,
            total + 1,
        ),
        f"{date} Stage 1A GLOBAL",
        date,
    )

    validate_global_cluster_membership(
        date,
        allc,
        "STAGE 1A INITIAL",
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


# ==============================================================
# GLOBAL MERGE WINDOW
# ==============================================================

def build_merge_windows(
    clusters,
):
    """
    V6.5.3：

    每一轮都重新从当前 Cluster 第1个开始。

    严格连续30个。

    不重叠。

    示例：

        137
        -> 30 / 30 / 30 / 30 / 17

        91
        -> 30 / 30 / 30 / 1

        64
        -> 30 / 30 / 4

        31
        -> 30 / 1

        30
        -> 30

    下一轮重新从当前 Cluster 重新切窗。
    """

    if GLOBAL_MERGE_OVERLAP != 0:
        raise RuntimeError(
            "❌ V6.5.3 Global Merge禁止使用Overlap。"
            "GLOBAL_MERGE_OVERLAP必须为0。"
        )

    if GLOBAL_MERGE_WINDOW_SIZE <= 0:
        raise RuntimeError(
            "❌ Global Merge Window Size必须大于0"
        )

    if not clusters:
        return []

    windows = []

    for start in range(
        0,
        len(clusters),
        GLOBAL_MERGE_WINDOW_SIZE,
    ):
        end = min(
            start
            + GLOBAL_MERGE_WINDOW_SIZE,
            len(clusters),
        )

        windows.append(
            clusters[
                start:end
            ]
        )

    return windows


# ==============================================================
# GLOBAL MERGE WINDOW AI
# ==============================================================

def merge_cluster_window(
    date,
    window,
    round_no,
    window_no,
):
    blocks = []

    for i, c in enumerate(
        window,
        1,
    ):
        blocks.append(
            f"""
[CLUSTER {i}]

Cluster ID：
{c['cluster_id']}

原始Cluster成员：
{json.dumps(
    c.get(
        'member_cluster_ids',
        [],
    ),
    ensure_ascii=False,
)}

事件名称：
{c.get(
    'event_title',
    '未命名事件',
)}

事件判断：
{c.get(
    'event_reason',
    '',
)}

文章数量：
{len(
    c.get(
        'article_indexes',
        [],
    )
)}

文章编号：
{json.dumps(
    c.get(
        'article_indexes',
        []),
)}
"""
        )

    expected = list(
        range(
            1,
            len(window) + 1,
        )
    )

    prompt = f"""
你正在执行748686自生长知识系统V6.5.3全局事件归并。

日期：
{date}

轮次：
{round_no}

窗口：
{window_no}

本窗口Cluster数量：
{len(window)}

注意：

这是一个不重叠窗口。

本轮窗口只是：

当前Cluster列表
→ 连续每30个一个窗口
→ 最后不足30个的余数形成最后窗口。

本窗口中的Cluster不能与本轮其他窗口直接比较。

但是下一轮会重新对所有当前Cluster进行连续30分组，
因此本轮不能因为窗口边界而创造跨窗口合并。

{chr(10).join(blocks)}

判断这些Cluster是否属于同一个：

“具体现实世界事件”。

可以合并：

- 同一政策发布
- 同一公司重大动作
- 同一事故
- 同一产品发布
- 同一具体现实事件
- 同一正在持续发展的单一现实事件

不得合并：

- 同公司不同事件
- 同人物不同事件
- 同国家不同事件
- 同产业不同事件
- 同趋势不同具体事件
- 仅关键词相同
- 仅主题相同

无法确认时宁可分开。

要求：

1. 每个输入Cluster必须且只能进入一个group。
2. 不得遗漏。
3. 不得重复。
4. 不得创造Cluster编号。
5. 一个group可以只有一个Cluster。
6. Cluster ID是Python已经注册的Global ID。
7. 必须原样引用Cluster ID。
8. 不得修改Cluster ID。
9. 不得重新编号。
10. 不得生成REC-/GM-替代ID。
11. 不需要返回文章编号。
12. 只根据当前窗口中的Cluster判断。
13. 只输出JSON。
14. 不要Markdown。
15. 不要解释。

输入Cluster编号：

{json.dumps(expected)}

只输出：

{{
  "groups": [
    {{
      "group_id": "G001",
      "cluster_indexes": [1, 4],
      "event_title": "统一事件名称",
      "reason": "为什么这些Cluster属于同一个现实世界事件"
    }}
  ]
}}
"""

    data = parse_ai_json(
        call_ai(
            prompt,
            (
                "你是全球新闻事件归并专家。"
                "必须覆盖全部输入Cluster。"
                "每个Cluster恰好一次。"
                "这是具体事件合并，不是主题分类。"
            ),
            0,
        ),
        (
            f"{date} Global Merge "
            f"Round {round_no} "
            f"Window {window_no}"
        ),
    )

    groups = data.get(
        "groups"
    )

    if not isinstance(
        groups,
        list,
    ):
        raise RuntimeError(
            "❌ Global Merge缺少groups"
        )

    actual = []

    malformed = []

    for p, g in enumerate(
        groups,
        1,
    ):
        if not isinstance(
            g,
            dict,
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
                list,
            )
            or not ids
        ):
            malformed.append(
                f"group[{p}]"
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
            (
                f"STAGE 1B / ROUND "
                f"{round_no} / WINDOW "
                f"{window_no}"
            ),
            "V6.5.3 Global Merge窗口AI输出覆盖异常。",
            {
                "duplicate":
                    dup,

                "missing":
                    miss,

                "extra":
                    extra,

                "malformed":
                    malformed,

                "groups":
                    groups,
            },
        )

        raise RuntimeError(
            f"❌ Global Merge窗口AI输出异常 "
            f"Duplicate={dup} "
            f"Missing={miss} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )

    return groups


# ==============================================================
# APPLY WINDOW GROUPS
# ==============================================================

def apply_window_groups(
    uf,
    window,
    groups,
    round_no,
    window_no,
):
    records = []

    for gp, g in enumerate(
        groups,
        1,
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
                cid,
            ):
                merged = True

        records.append(
            {
                "group_id":
                    g.get(
                        "group_id",
                        f"G{gp:03d}",
                    ),

                "cluster_ids":
                    ids,

                "event_title":
                    str(
                        g.get(
                            "event_title",
                            "未命名事件",
                        )
                    ).strip(),

                "reason":
                    str(
                        g.get(
                            "reason",
                            "",
                        )
                    ).strip(),

                "merged":
                    merged,

                "round":
                    round_no,

                "window":
                    window_no,
            }
        )

    return records


# ==============================================================
# METADATA HISTORY
# ==============================================================

def _metadata_record_valid(r):
    return bool(
        str(
            r.get(
                "event_title",
                "",
            )
        ).strip()
        or str(
            r.get(
                "reason",
                "",
            )
        ).strip()
    )


def merge_metadata_histories(
    history,
    records,
    uf,
):
    if not isinstance(
        history,
        dict,
    ):
        history = {}

    for r in records:
        ids = [
            str(x)
            for x in r.get(
                "cluster_ids",
                [],
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
                    "",
                ),

            "reason":
                r.get(
                    "reason",
                    "",
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
                        0,
                    )
                ),

            "window":
                int(
                    r.get(
                        "window",
                        0,
                    )
                ),
        }

        history.setdefault(
            root,
            [],
        ).append(
            item
        )

    merged = {}

    for old_root, entries in history.items():
        if not entries:
            continue

        first_ids = (
            entries[-1].get(
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
            [],
        ).extend(
            entries
        )

    return merged


# ==============================================================
# CHOOSE METADATA
# ==============================================================

def choose_component_metadata(
    member_ids,
    by_id,
    history,
    uf,
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
                "",
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
                "",
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
        if r.get(
            "merged"
        )
        and len(
            r.get(
                "cluster_ids",
                [],
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
                [],
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
                [],
            )
        ) == 1
        and _metadata_record_valid(r)
    ]

    def score(r):
        return (
            len(
                r.get(
                    "cluster_ids",
                    [],
                )
            ),

            1
            if r.get(
                "merged"
            )
            else 0,

            len(
                str(
                    r.get(
                        "reason",
                        "",
                    )
                )
            ),

            len(
                str(
                    r.get(
                        "event_title",
                        "",
                    )
                )
            ),

            -int(
                r.get(
                    "round",
                    0,
                )
            ),

            -int(
                r.get(
                    "window",
                    0,
                )
            ),
        )

    candidate = max(
        actual
        or multi
        or [],
        key=score,
        default=None,
    )

    if candidate:
        title = str(
            candidate.get(
                "event_title",
                "",
            )
        ).strip()

        reason = str(
            candidate.get(
                "reason",
                "",
            )
        ).strip()

    else:
        title = max(
            old_titles,
            key=len,
            default="",
        )

        reason = max(
            old_reasons,
            key=len,
            default="",
        )

        if (
            not title
            and not reason
            and singleton
        ):
            candidate = max(
                singleton,
                key=score,
            )

            title = str(
                candidate.get(
                    "event_title",
                    "",
                )
            ).strip()

            reason = str(
                candidate.get(
                    "reason",
                    "",
                )
            ).strip()

    return (
        title or "未命名事件",
        reason,
    )


# ==============================================================
# REBUILD GLOBAL CLUSTERS
# ==============================================================

def rebuild_global_clusters(
    current,
    uf,
    metadata_history,
):
    by_id = {
        c["cluster_id"]: c
        for c in current
    }

    rebuilt = []

    for root, member_ids in (
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

            c = by_id[
                cid
            ]

            articles.extend(
                c.get(
                    "article_indexes",
                    [],
                )
            )

            originals.extend(
                c.get(
                    "member_cluster_ids",
                    [],
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
                uf,
            )
        )

        rebuilt.append(
            {
                # 保留组件中最早注册的Global ID。
                # 避免Global ID漂移。
                "cluster_id":
                    min(member_ids),

                "event_title":
                    title,

                "event_reason":
                    reason,

                "article_indexes":
                    articles,

                "member_cluster_ids":
                    originals,
            }
        )

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


# ==============================================================
# GLOBAL MEMBERSHIP VALIDATION
# ==============================================================

def validate_global_cluster_membership(
    date,
    clusters,
    context,
    expected_original_ids=None,
):
    seen_current = set()

    seen_original = set()

    malformed = []

    duplicate_current = []

    duplicate_original = []

    for pos, c in enumerate(
        clusters,
        1,
    ):
        if not isinstance(
            c,
            dict,
        ):
            malformed.append(
                f"cluster[{pos}]不是对象"
            )
            continue

        cid = str(
            c.get(
                "cluster_id",
                "",
            )
        ).strip()

        if not cid:
            malformed.append(
                f"cluster[{pos}]缺少cluster_id"
            )

        elif not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            cid,
        ):
            malformed.append(
                f"cluster[{pos}]非法Global cluster_id："
                f"{cid}"
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
                list,
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
            expected
            - seen_original
        )

        extra_original = sorted(
            seen_original
            - expected
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
                    extra_original,
            },
        )

        raise RuntimeError(
            f"❌ {context} Global Cluster membership异常："
            f"Malformed={malformed} "
            f"DuplicateCurrent={duplicate_current} "
            f"DuplicateOriginal={duplicate_original} "
            f"MissingOriginal={missing_original} "
            f"ExtraOriginal={extra_original}"
        )


# ==============================================================
# GLOBAL ARTICLE COVERAGE
# ==============================================================

def validate_global_article_coverage(
    date,
    clusters,
    news_count,
    context,
):
    allidx = []

    malformed = []

    for pos, c in enumerate(
        clusters,
        1,
    ):
        if not isinstance(
            c,
            dict,
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
            list,
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
            news_count + 1,
        )
    )

    actual = set(
        allidx
    )

    duplicate = sorted(
        {
            x
            for x in allidx
            if allidx.count(x) > 1
        }
    )

    missing = sorted(
        expected
        - actual
    )

    extra = sorted(
        actual
        - expected
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
                    malformed,
            },
        )

        raise RuntimeError(
            f"❌ {context} Article覆盖异常 "
            f"Duplicate={duplicate} "
            f"Missing={missing} "
            f"Extra={extra} "
            f"Malformed={malformed}"
        )


# ==============================================================
# UNION FIND
# ==============================================================

class UnionFind:

    def __init__(
        self,
        values,
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
        value,
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
            self.parent[
                value
            ] = self.find(
                p
            )

        return self.parent[
            value
        ]

    def union(
        self,
        a,
        b,
    ):
        a = str(a)
        b = str(b)

        ra = self.find(
            a
        )

        rb = self.find(
            b
        )

        if ra == rb:
            return False

        if (
            self.rank[ra]
            < self.rank[rb]
        ):
            ra, rb = rb, ra

        self.parent[
            rb
        ] = ra

        if (
            self.rank[ra]
            == self.rank[rb]
        ):
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
                [],
            ).append(
                value
            )

        return result

    def to_checkpoint(
        self,
    ):
        for v in list(
            self.parent
        ):
            self.find(
                v
            )

        return {
            "parent":
                dict(
                    self.parent
                ),

            "rank":
                dict(
                    self.rank
                ),
        }

    @classmethod
    def from_checkpoint(
        cls,
        values,
        data,
    ):
        """
        从checkpoint恢复Union-Find。

        注意：
        此方法必须位于UnionFind类内部。
        """

        uf = cls(
            values
        )

        if not isinstance(
            data,
            dict,
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
                dict,
            )
            or not isinstance(
                rank,
                dict,
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
                    parent,
                )
            )
            != expected
            or
            set(
                map(
                    str,
                    rank,
                )
            )
            != expected
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint Universe不一致"
            )

        uf.parent = {
            str(k):
                str(v)
            for k, v
            in parent.items()
        }

        try:
            uf.rank = {
                str(k):
                    int(v)
                for k, v
                in rank.items()
            }

        except Exception as e:
            raise RuntimeError(
                "❌ Union-Find checkpoint rank非法"
            ) from e

        for k, v in (
            uf.parent.items()
        ):
            if v not in uf.parent:
                raise RuntimeError(
                    "❌ Union-Find checkpoint"
                    f"存在非法parent："
                    f"{k}->{v}"
                )

        if any(
            v < 0
            for v in uf.rank.values()
        ):
            raise RuntimeError(
                "❌ Union-Find checkpoint"
                "存在非法rank"
            )

        uf.components()

        return uf


# ==============================================================
# GLOBAL MERGE CHECKPOINT
# ==============================================================

def save_global_merge_checkpoint(
    date,
    round_no,
    current,
    original_cluster_ids,
    completed_windows=None,
    status="running",
    uf=None,
    window_count=None,
    metadata_history=None,
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
                    for x
                    in completed_windows
                )
            ),

        "window_count":
            (
                int(window_count)
                if window_count is not None
                else None
            ),

        "window_size":
            GLOBAL_MERGE_WINDOW_SIZE,

        "window_overlap":
            0,

        "original_cluster_ids":
            sorted(
                str(x)
                for x
                in original_cluster_ids
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
                    dict,
                )
                else {}
            ),

        "saved_at":
            now().isoformat(),
    }

    write_json_atomic(
        global_merge_checkpoint_path(
            date
        ),
        data,
    )


def load_global_merge_checkpoint(
    date,
):
    p = (
        global_merge_checkpoint_path(
            date
        )
    )

    if not p.exists():
        return None

    try:
        data = read_json(
            p,
            None,
        )

    except Exception as e:
        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Checkpoint JSON读取失败，将忽略checkpoint。",
            str(e),
        )

        return None

    if not isinstance(
        data,
        dict,
    ):
        return None

    if (
        data.get(
            "version"
        )
        not in (
            "6.4",
            "6.4.1",
            "6.4.2",
            "6.5.0",
            "6.5.1",
            "6.5.2",
            "6.5.3",
        )
        or data.get(
            "date"
        ) != date
        or (
            data.get(
                "language"
            )
            not in (
                None,
                CURRENT_LANGUAGE,
            )
        )
    ):
        return None

    # ----------------------------------------------------------
    # V6.5.3 checkpoint必须明确记录：
    # overlap = 0
    #
    # 老版本checkpoint若是15 overlap，
    # 不允许继续恢复到新算法。
    # ----------------------------------------------------------

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
            "检测到旧版Overlap checkpoint，"
            "禁止在V6.5.3算法中继续恢复。",
            {
                "window_overlap":
                    saved_overlap
            },
        )

        return None

    return data


def remove_global_merge_checkpoint(
    date,
):
    p = (
        global_merge_checkpoint_path(
            date
        )
    )

    if p.exists():
        p.unlink()


# ==============================================================
# CHECKPOINT VALIDATION
# ==============================================================

def validate_checkpoint(
    date,
    checkpoint,
    expected_original_ids,
    news_count,
):
    if not checkpoint:
        return False

    current = checkpoint.get(
        "current_clusters"
    )

    if (
        not isinstance(
            current,
            list,
        )
        or not current
    ):
        return False

    expected_original = {
        str(x)
        for x
        in expected_original_ids
    }

    actual_original = {
        str(x)
        for x
        in checkpoint.get(
            "original_cluster_ids",
            [],
        )
    }

    if (
        actual_original
        != expected_original
    ):
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
                    ),
            },
        )

        return False

    try:
        validate_global_cluster_membership(
            date,
            current,
            "CHECKPOINT MEMBERSHIP",
            expected_original_ids,
        )

        validate_global_article_coverage(
            date,
            current,
            news_count,
            "CHECKPOINT ARTICLE COVERAGE",
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
        "round_completed",
    ):
        return False

    if status == "round_completed":
        return True

    uf_data = checkpoint.get(
        "union_find"
    )

    if not isinstance(
        uf_data,
        dict,
    ):
        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "running checkpoint缺少完整Union-Find状态。",
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
            uf_data,
        )

        uf.components()

    except Exception as e:
        log_conflict(
            date,
            "GLOBAL MERGE CHECKPOINT",
            "Union-Find checkpoint验证失败。",
            str(e),
        )

        return False

    completed = checkpoint.get(
        "completed_windows",
        [],
    )

    if not isinstance(
        completed,
        list,
    ):
        return False

    try:
        completed = [
            int(x)
            for x
            in completed
        ]

    except Exception:
        return False

    if (
        len(
            set(completed)
        )
        != len(completed)
        or any(
            x < 1
            for x
            in completed
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
            for x
            in completed
        )
    ):
        return False

    history = checkpoint.get(
        "metadata_history",
        {},
    )

    if not isinstance(
        history,
        dict,
    ):
        return False

    return True


# ==============================================================
# GLOBAL MERGE
# ==============================================================

def merge_all_clusters(
    date,
    clusters,
    news_count,
):
    """
    V6.5.3核心算法：

    当前Clusters
        ↓
    Round 1重新切窗
        ↓
    30 / 30 / 30 / ...
        ↓
    所有窗口完成
        ↓
    Union-Find合并
        ↓
    重建Clusters
        ↓
    Round 2重新切窗
        ↓
    30 / 30 / 30 / ...
        ↓
    ...

    不使用15 overlap。

    每轮的窗口只覆盖当前Clusters一次。

    跨窗口事件通过下一轮重新分组继续比较。

    直到某一整轮没有发生任何实际合并。
    """

    current = clusters

    original_cluster_ids = sorted(
        str(
            c["cluster_id"]
        )
        for c in clusters
    )

    print(
        "\n"
        + "=" * 70
    )

    print(
        "STAGE 1B — "
        "V6.5.3 GLOBAL EVENT MERGING"
    )

    print(
        "=" * 70
    )

    print(
        f"Window Size: "
        f"{GLOBAL_MERGE_WINDOW_SIZE}"
    )

    print(
        "Window Overlap: 0"
    )

    validate_global_cluster_membership(
        date,
        current,
        "STAGE 1B INITIAL",
        original_cluster_ids,
    )

    validate_global_article_coverage(
        date,
        current,
        news_count,
        "STAGE 1B INITIAL",
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
            news_count,
        )
    )

    final_current = None

    # ==========================================================
    # RESTORE CHECKPOINT
    # ==========================================================

    if checkpoint_valid:
        status = checkpoint.get(
            "status"
        )

        current = checkpoint[
            "current_clusters"
        ]

        print(
            "\n♻️ 检测到有效 "
            f"V6.5.3 Global Merge checkpoint | "
            f"status={status} | "
            f"round={checkpoint.get('round')}"
        )

        print(
            f" Restored clusters: "
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
                f" ▶️ 从下一Round "
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
                for x
                in checkpoint.get(
                    "completed_windows",
                    [],
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
                ],
            )

            metadata_history = (
                checkpoint.get(
                    "metadata_history",
                    {},
                )
            )

            print(
                f" Completed windows: "
                f"{completed_windows}"
            )

            print(
                f" ▶️ 从 Window "
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

    # ==========================================================
    # GLOBAL MERGE ROUNDS
    # ==========================================================

    if final_current is None:

        rnd = start_round

        while True:

            before = len(
                current
            )

            print(
                "\n"
                + "-" * 70
            )

            print(
                f"GLOBAL MERGE ROUND "
                f"{rnd}"
            )

            print(
                "-" * 70
            )

            print(
                f"Current Clusters: "
                f"{before}"
            )

            # --------------------------------------------------
            # 如果只有1个Cluster
            # --------------------------------------------------

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
                    {},
                )

                final_current = current

                break

            # --------------------------------------------------
            # 每一轮重新切窗
            # --------------------------------------------------

            windows = (
                build_merge_windows(
                    current
                )
            )

            window_count = len(
                windows
            )

            # --------------------------------------------------
            # 明确打印窗口布局
            # --------------------------------------------------

            window_sizes = [
                len(w)
                for w in windows
            ]

            print(
                f"Round {rnd} window layout: "
                f"{' / '.join(map(str, window_sizes))}"
            )

            print(
                f"Windows: "
                f"{window_count}"
            )

            print(
                f"Window Size: "
                f"{GLOBAL_MERGE_WINDOW_SIZE}"
            )

            print(
                "Overlap: 0"
            )

            current_ids = [
                str(
                    c["cluster_id"]
                )
                for c in current
            ]

            # --------------------------------------------------
            # 初始化 / 恢复当前Round
            # --------------------------------------------------

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

                # ----------------------------------------------
                # 恢复running checkpoint
                # ----------------------------------------------

                uf = UnionFind.from_checkpoint(
                    current_ids,
                    checkpoint[
                        "union_find"
                    ],
                )

                completed_windows = [
                    int(x)
                    for x
                    in checkpoint.get(
                        "completed_windows",
                        [],
                    )
                ]

                metadata_history = (
                    checkpoint.get(
                        "metadata_history",
                        {},
                    )
                )

                next_window = (
                    max(
                        completed_windows,
                        default=0,
                    )
                    + 1
                )

            round_records = []

            # --------------------------------------------------
            # 逐窗口完成本轮
            # --------------------------------------------------

            for wi in range(
                next_window,
                window_count + 1,
            ):
                w = windows[
                    wi - 1
                ]

                print(
                    f"\n🔹 Round {rnd} "
                    f"Window "
                    f"{wi}/{window_count} | "
                    f"size={len(w)}"
                )

                groups = (
                    merge_cluster_window(
                        date,
                        w,
                        rnd,
                        wi,
                    )
                )

                records = (
                    apply_window_groups(
                        uf,
                        w,
                        groups,
                        rnd,
                        wi,
                    )
                )

                round_records.extend(
                    records
                )

                metadata_history = (
                    merge_metadata_histories(
                        metadata_history,
                        records,
                        uf,
                    )
                )

                completed_windows = sorted(
                    set(
                        completed_windows
                        + [wi]
                    )
                )

                # ----------------------------------------------
                # 每个Window完成立即保存checkpoint
                # ----------------------------------------------

                save_global_merge_checkpoint(
                    date,
                    rnd,
                    current,
                    original_cluster_ids,
                    completed_windows,
                    "running",
                    uf,
                    window_count,
                    metadata_history,
                )

                print(
                    f" 💾 Round {rnd} "
                    f"Window {wi} "
                    "checkpoint saved"
                )

            # --------------------------------------------------
            # 重要：
            # 必须整轮所有Window都完成以后，
            # 才能计算本轮结果。
            # --------------------------------------------------

            if len(
                completed_windows
            ) != window_count:

                raise RuntimeError(
                    f"❌ Round {rnd} "
                    "并未完整完成所有Window，"
                    "禁止进入下一Round。"
                )

            components = (
                uf.components()
            )

            after = len(
                components
            )

            actual_merge_happened = (
                after < before
            )

            print(
                f"\nRound {rnd} complete."
            )

            print(
                f" Union Components: "
                f"{after}"
            )

            print(
                f" Actual merges: "
                f"{before - after}"
            )

            # --------------------------------------------------
            # 本轮没有任何实际合并
            # --------------------------------------------------

            if not actual_merge_happened:

                print(
                    " ℹ️ 本轮没有发生任何"
                    "实际Cluster合并"
                )

                validate_global_cluster_membership(
                    date,
                    current,
                    (
                        f"STAGE 1B ROUND "
                        f"{rnd} NO-MERGE"
                    ),
                    original_cluster_ids,
                )

                validate_global_article_coverage(
                    date,
                    current,
                    news_count,
                    (
                        f"STAGE 1B ROUND "
                        f"{rnd} NO-MERGE"
                    ),
                )

                save_global_merge_checkpoint(
                    date,
                    rnd,
                    current,
                    original_cluster_ids,
                    list(
                        range(
                            1,
                            window_count + 1,
                        )
                    ),
                    "converged",
                    uf,
                    window_count,
                    metadata_history,
                )

                print(
                    "\n🟢 GLOBAL MERGE CONVERGED"
                )

                final_current = current

                break

            # --------------------------------------------------
            # 本轮发生实际合并
            # --------------------------------------------------

            print(
                f" 🔗 Actual merges: "
                f"{before - after}"
            )

            merged = (
                rebuild_global_clusters(
                    current,
                    uf,
                    metadata_history,
                )
            )

            validate_global_cluster_membership(
                date,
                merged,
                f"STAGE 1B ROUND {rnd}",
                original_cluster_ids,
            )

            validate_global_article_coverage(
                date,
                merged,
                news_count,
                f"STAGE 1B ROUND {rnd}",
            )

            print(
                f"\n✅ Round {rnd}: "
                f"{before} -> "
                f"{len(merged)}"
            )

            # --------------------------------------------------
            # 保存“整轮完成”checkpoint
            #
            # round = 下一轮编号
            # --------------------------------------------------

            save_global_merge_checkpoint(
                date,
                rnd + 1,
                merged,
                original_cluster_ids,
                [],
                "round_completed",
                None,
                None,
                {},
            )

            print(
                f" 💾 Round {rnd} "
                "completed checkpoint saved | "
                f"next_round={rnd + 1}"
            )

            # --------------------------------------------------
            # 下一Round：
            # 必须使用刚刚重建后的Cluster重新切窗。
            # --------------------------------------------------

            current = merged

            rnd += 1

            checkpoint_valid = True

            checkpoint = (
                load_global_merge_checkpoint(
                    date
                )
            )

    # ==========================================================
    # FINAL VALIDATION
    # ==========================================================

    validate_global_cluster_membership(
        date,
        final_current,
        "STAGE 1B FINAL",
        original_cluster_ids,
    )

    validate_global_article_coverage(
        date,
        final_current,
        news_count,
        "STAGE 1B FINAL",
    )

    ordered = sorted(
        final_current,
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

    final = []

    for c in ordered:
        final.append(
            {
                "event_id":
                    str(
                        c[
                            "cluster_id"
                        ]
                    ),

                "event_title":
                    c.get(
                        "event_title",
                        "未命名事件",
                    ),

                "event_reason":
                    c.get(
                        "event_reason",
                        "",
                    ),

                "article_indexes":
                    sorted(
                        set(
                            map(
                                int,
                                c[
                                    "article_indexes"
                                ],
                            )
                        )
                    ),
            }
        )

    validate_global_article_coverage(
        date,
        final,
        news_count,
        "STAGE 1B FINAL EVENT UNITS",
    )

    print(
        f"\n✅ FINAL EVENT UNITS: "
        f"{len(final)}"
    )

    print(
        f"✅ ARTICLE COVERAGE: "
        f"{news_count}/"
        f"{news_count}"
    )

    return final


# ==============================================================
# FINAL EVENT ID
# ==============================================================

def validate_final_event_ids(
    date,
    events,
):
    ids = [
        str(
            e.get(
                "event_id",
                "",
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

    if len(ids) != len(
        set(ids)
    ):
        raise RuntimeError(
            f"❌ {date} Final EventUnit存在重复event_id"
        )

    bad = [
        x
        for x in ids
        if not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            x,
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
    news,
):
    out = []

    for c in clusters:
        arts = []

        for i in c[
            "article_indexes"
        ]:
            if not 1 <= i <= len(news):
                raise RuntimeError(
                    f"❌ {c['event_id']}引用不存在文章："
                    f"{i}"
                )

            m = news[
                i - 1
            ]["metadata"]

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
                            "Untitled",
                        ),

                    "source":
                        m.get(
                            "source",
                            "Unknown",
                        ),

                    "source_url":
                        m.get(
                            "source_url",
                            "",
                        ),

                    "source_status":
                        m.get(
                            "source_status",
                            "",
                        ),

                    "content_status":
                        m.get(
                            "content_status",
                            "",
                        ),

                    "body":
                        news[
                            i - 1
                        ]["body"],
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
                    arts,
            }
        )

    return out


# ==============================================================
# SECOND LAYER EVENT SYNTHESIS
# ==============================================================

def synthesize_event(
    event,
):
    blocks = []

    for a in event[
        "articles"
    ][:MAX_ARTICLES_PER_EVENT_CONTEXT]:

        blocks.append(
            f"""
### 来源文章 #{a['index']}

标题：
{a['title']}

来源：
{a['source']}

链接：
{a['source_url']}

source_status：
{a['source_status']}

content_status：
{a['content_status']}

内容：
{a['body'][:ARTICLE_AGGREGATION_CONTENT_LIMIT]}
"""
        )

    prompt = f"""
你正在执行748686自生长知识系统V6.5.3第二层事件知识综合。

日期：
{event['date']}

事件ID：
{event['event_id']}

事件名称：
{event['event_title']}

第一轮事件判断：
{event['event_reason']}

同一事件的多来源输入：

{chr(10).join(blocks)}

把来源综合成一个高质量事件知识单元。

要求：

1. 识别共同事实。
2. 保留来源独有信息。
3. 保留不同地区视角。
4. 区分事实与推测。
5. 不编造。
6. source_status不是fetched时，
   不得声称完整阅读原文。
7. 冲突明确指出。
8. 资料不足明确说明。

输出标准中文Markdown。

包含：

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
        (
            "你是跨来源新闻综合专家。"
            "严格依据输入，不得编造。"
            "输出标准中文Markdown。"
        ),
        0.2,
    )


# ==============================================================
# EVENT UNIT FILE
# ==============================================================

def event_unit_filename(
    e,
):
    return (
        f"{e['event_id']}_"
        f"{safe_name(e['event_title'])}.md"
    )


def save_event_unit(
    date,
    event,
    content,
):
    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    p = target / (
        event_unit_filename(
            event
        )
    )

    sources = "\n".join(
        f"- {a['source']} | "
        f"{a['title']} | "
        f"{a['source_url']}"
        for a
        in event[
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
        encoding="utf-8",
    )

    return p


# ==============================================================
# EVENT INDEX
# ==============================================================

def save_aggregation_index(
    date,
    events,
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
                                a["path"],
                        }
                        for a
                        in e["articles"]
                    ],
            }
        )

    p = (
        event_units_dir(date)
        / EVENT_INDEX_FILE
    )

    write_json(
        p,
        data,
    )

    return p


def load_event_index(
    date,
):
    p = (
        event_units_dir(date)
        / EVENT_INDEX_FILE
    )

    if not p.exists():
        return None

    try:
        d = read_json(
            p,
            None,
        )
    except Exception:
        return None

    return (
        d
        if isinstance(
            d,
            list,
        )
        and d
        else None
    )


# ==============================================================
# EVENT UNIT VALIDATION
# ==============================================================

def event_unit_file_valid(
    path,
    event_id,
):
    if (
        not path.exists()
        or path.stat().st_size <= 0
    ):
        return False

    try:
        m, b = (
            parse_front_matter(
                path.read_text(
                    encoding="utf-8",
                    errors="replace",
                )
            )
        )

    except Exception:
        return False

    return (
        bool(
            b.strip()
        )
        and m.get(
            "event_id"
        ) == event_id
        and m.get(
            "status"
        ) == "completed"
    )


def inspect_event_units(
    date,
):
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
                [],
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
                [],
        }

    missing = []

    invalid = []

    ids = []

    for e in idx:
        eid = str(
            e.get(
                "event_id",
                "",
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
                eid,
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
            [],
    }


# ==============================================================
# COMPLETE MARKER
# ==============================================================

def mark_event_units_complete(
    date,
    n,
    e,
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
        encoding="utf-8",
    )

    return p


def remove_event_units_complete(
    date,
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
    news,
):
    out = []

    for e in index:
        arts = []

        for r in e.get(
            "articles",
            [],
        ):
            i = int(
                r["index"]
            )

            if not 1 <= i <= len(news):
                raise RuntimeError(
                    f"❌ {e.get('event_id')}引用不存在文章："
                    f"{i}"
                )

            m = news[
                i - 1
            ]["metadata"]

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
                            "Untitled",
                        ),

                    "source":
                        m.get(
                            "source",
                            "Unknown",
                        ),

                    "source_url":
                        m.get(
                            "source_url",
                            "",
                        ),

                    "source_status":
                        m.get(
                            "source_status",
                            "",
                        ),

                    "content_status":
                        m.get(
                            "content_status",
                            "",
                        ),

                    "body":
                        news[
                            i - 1
                        ]["body"],
                }
            )

        out.append(
            {
                "event_id":
                    str(
                        e[
                            "event_id"
                        ]
                    ),

                "date":
                    date,

                "event_title":
                    e.get(
                        "event_title",
                        "未命名事件",
                    ),

                "event_reason":
                    e.get(
                        "event_reason",
                        "",
                    ),

                "articles":
                    arts,
            }
        )

    return out


# ==============================================================
# EVENT INDEX COVERAGE
# ==============================================================

def validate_event_index_coverage(
    date,
    events,
    n,
):
    ids = []

    eids = set()

    for e in events:

        if e[
            "event_id"
        ] in eids:
            raise RuntimeError(
                f"❌ {date} Event Index重复event_id："
                f"{e['event_id']}"
            )

        eids.add(
            e["event_id"]
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
                n + 1,
            )
        )
        or len(ids)
        != len(
            set(ids)
        )
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
    n,
):
    target = event_units_dir(
        date
    )

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    generated = 0

    for i, e in enumerate(
        events,
        1,
    ):
        matches = target.glob(
            f"{e['event_id']}_*.md"
        )

        if any(
            event_unit_file_valid(
                p,
                e["event_id"],
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
            content,
        )

        if not event_unit_file_valid(
            p,
            e["event_id"],
        ):
            raise RuntimeError(
                f"❌ {e['event_id']}保存验证失败"
            )

        generated += 1

    for e in events:
        if not any(
            event_unit_file_valid(
                p,
                e["event_id"],
            )
            for p in target.glob(
                f"{e['event_id']}_*.md"
            )
        ):
            raise RuntimeError(
                f"❌ {e['event_id']}最终缺失"
            )

    marker = (
        mark_event_units_complete(
            date,
            n,
            len(events),
        )
    )

    print(
        f"✅ EVENT UNITS COMPLETE | "
        f"new={generated} "
        f"total={len(events)} | "
        f"{marker}"
    )

    return True


# ==============================================================
# STAGE 1
# ==============================================================

def run_stage_1(
    date,
    language,
):
    global CURRENT_LANGUAGE

    CURRENT_LANGUAGE = str(
        language
    ).upper()

    if CURRENT_LANGUAGE not in (
        SUPPORTED_LANGUAGES
    ):
        raise RuntimeError(
            f"❌ 不支持的语言："
            f"{language}"
        )

    root = (
        event_units_root(date)
    )

    lang_root = (
        language_dir(date)
    )

    articles_root = (
        lang_root
        / "articles"
    )

    events_root = (
        event_units_dir(date)
    )

    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    articles_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    events_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        f"\n{'=' * 70}\n"
        f"STAGE 1 — EVENT UNIT GENERATION V6.5.3\n"
        f"DATE: {date}\n"
        f"LANGUAGE: {CURRENT_LANGUAGE}\n"
        f"OUTPUT: {lang_root}\n"
        f"{'=' * 70}"
    )

    inspection = (
        inspect_event_units(
            date
        )
    )

    # ----------------------------------------------------------
    # EventUnit已完整
    # ----------------------------------------------------------

    if inspection[
        "complete"
    ]:
        print(
            f"✅ {date} / "
            f"{CURRENT_LANGUAGE} "
            "EventUnits已经完整，跳过AI聚合。"
        )

        return False

    news = (
        load_all_enriched_news(
            date,
            CURRENT_LANGUAGE,
        )
    )

    print(
        f"📦 当前批次："
        f"{date} / "
        f"{CURRENT_LANGUAGE} | "
        f"News={len(news)}"
    )

    # ----------------------------------------------------------
    # 如果已有Event Index：
    # 恢复EventUnit生成阶段。
    # ----------------------------------------------------------

    if inspection[
        "index"
    ] is not None:

        events = (
            rebuild_events_from_index(
                date,
                inspection[
                    "index"
                ],
                news,
            )
        )

        validate_event_index_coverage(
            date,
            events,
            len(news),
        )

        return complete_existing_event_units(
            date,
            events,
            len(news),
        )

    remove_event_units_complete(
        date
    )

    # ----------------------------------------------------------
    # Global Registry
    #
    # DATE总目录共享。
    # EN / ZH 不重置。
    # ----------------------------------------------------------

    registry_file = (
        global_cluster_registry_path(
            date
        )
    )

    if registry_file.exists():

        registry = read_json(
            registry_file,
            None,
        )

        if (
            not isinstance(
                registry,
                dict,
            )
            or registry.get(
                "date"
            )
            != str(date)
        ):
            raise RuntimeError(
                f"❌ {date} Global Cluster Registry异常，禁止覆盖"
            )

        validate_global_registry(
            date,
            registry,
        )

        print(
            f"♻️ 继续使用当天 Global Registry："
            f"{registry_file}"
        )

    else:

        registry = (
            create_global_cluster_registry(
                date
            )
        )

        persist_global_cluster_registry(
            date,
            registry,
        )

        print(
            f"🆕 创建当天 Global Registry："
            f"{registry_file}"
        )

    # ----------------------------------------------------------
    # Stage 1A
    # ----------------------------------------------------------

    initial = (
        build_initial_clusters(
            date,
            news,
            registry=registry,
        )
    )

    # ----------------------------------------------------------
    # Stage 1B
    # ----------------------------------------------------------

    final = (
        merge_all_clusters(
            date,
            initial,
            len(news),
        )
    )

    # ----------------------------------------------------------
    # Build Event Units
    # ----------------------------------------------------------

    events = (
        build_event_units(
            date,
            final,
            news,
        )
    )

    validate_event_index_coverage(
        date,
        events,
        len(news),
    )

    validate_final_event_ids(
        date,
        events,
    )

    p = save_aggregation_index(
        date,
        events,
    )

    print(
        f"✅ Event Index saved: "
        f"{p}"
    )

    # ----------------------------------------------------------
    # Global Merge checkpoint：
    # 当前语言完成后清理。
    #
    # Registry不能清理。
    # ----------------------------------------------------------

    remove_global_merge_checkpoint(
        date
    )

    print(
        "🧹 当前语言 Global Merge checkpoint已清理"
    )

    return (
        complete_existing_event_units(
            date,
            events,
            len(news),
        )
    )


# ==============================================================
# LOAD SAVED EVENT UNITS
# ==============================================================

def load_saved_event_units(
    date,
):
    target = event_units_dir(
        date
    )

    marker = (
        language_dir(date)
        / EVENT_UNITS_COMPLETE_FILE
    )

    if not marker.exists():
        raise RuntimeError(
            f"❌ {date} / "
            f"{CURRENT_LANGUAGE} "
            "EventUnits尚未完成，"
            "禁止进入27 Skills阶段"
        )

    idx = load_event_index(
        date
    )

    if idx is None:
        raise RuntimeError(
            f"❌ {date} / "
            f"{CURRENT_LANGUAGE} "
            "Event Index不存在或无效"
        )

    files = []

    for e in idx:
        eid = str(
            e.get(
                "event_id",
                "",
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
                    eid,
                )
            ),
            None,
        )

        if valid is None:
            raise RuntimeError(
                f"❌ EventUnit缺失或无效："
                f"{eid}"
            )

        files.append(
            (
                e,
                valid,
            )
        )

    return files


# ==============================================================
# ONE SKILL
# ==============================================================

def run_one_skill(
    event,
    skill,
):
    content = event[
        1
    ].read_text(
        encoding="utf-8",
        errors="replace",
    )

    prompt = f"""
你正在执行748686自生长知识系统V6.5.3的27 Skills深度处理。

事件：
{event[0].get(
    'event_title',
    ''
)}

Event ID：
{event[0].get(
    'event_id',
    ''
)}

Skill名称：
{skill['name']}

Skill规则：

{skill['content']}

EventUnit原文：

{content[:30000]}

请严格按照该Skill完成深度处理。

不要编造。

只使用EventUnit提供的信息。

输出可直接写入知识库的中文Markdown。
"""

    return call_ai(
        prompt,
        (
            "你是748686知识系统Skill执行器。"
            "严格执行Skill规则，不得编造。"
        ),
        0.2,
    )


# ==============================================================
# STAGE 2 — 27 SKILLS
# ==============================================================

def run_stage_2(
    date,
    language,
):
    global CURRENT_LANGUAGE

    CURRENT_LANGUAGE = str(
        language
    ).upper()

    files = (
        load_saved_event_units(
            date
        )
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
                and name
                not in selected_names
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
            for k in sorted(
                skills
            )
        ]

    outroot = (
        event_units_dir(
            date
        )
    )

    for ei, event in enumerate(
        files,
        1,
    ):
        eid = event[0].get(
            "event_id",
            "",
        )

        edir = (
            outroot
            / eid
        )

        edir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for si, skill in enumerate(
            selected,
            1,
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
                skill,
            )

            if not result.strip():
                raise RuntimeError(
                    f"❌ Skill结果为空："
                    f"{eid} / "
                    f"{skill['name']}"
                )

            outfile.write_text(
                result,
                encoding="utf-8",
            )

    marker = (
        outroot
        / SKILLS_COMPLETE_FILE
    )

    marker.write_text(
        f"""SKILLS_COMPLETE
date: {date}
language: {CURRENT_LANGUAGE}
events: {len(files)}
skills: {len(selected)}
completed_at: {now().isoformat()}
timezone: Asia/Shanghai
""",
        encoding="utf-8",
    )

    print(
        f"✅ STAGE 2 COMPLETE: "
        f"{date} / "
        f"{CURRENT_LANGUAGE}"
    )

    return True


# ==============================================================
# MAIN
# ==============================================================

def main():
    ap = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Pipeline V6.5.3"
        )
    )

    ap.add_argument(
        "--date",
        required=True,
    )

    ap.add_argument(
        "--language",
        choices=[
            "EN",
            "ZH",
        ],
        required=True,
    )

    ap.add_argument(
        "--stage",
        choices=[
            "aggregation",
            "skills",
            "all",
        ],
        default="aggregation",
    )

    args = ap.parse_args()

    try:

        if args.stage in (
            "aggregation",
            "all",
        ):
            run_stage_1(
                args.date,
                args.language,
            )

        if args.stage in (
            "skills",
            "all",
        ):
            run_stage_2(
                args.date,
                args.language,
            )

    except KeyboardInterrupt:
        print(
            "\n❌ 用户中断"
        )

        return 130

    except Exception as e:
        print(
            "\n❌ Knowledge Pipeline "
            f"V6.5.3 FAILED: {e}",
            file=sys.stderr,
        )

        return 1

    print(
        "\n✅ Knowledge Pipeline "
        f"V6.5.3 finished: "
        f"{args.date} / "
        f"{args.language} / "
        f"{args.stage}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(
        main()
    )
