#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Common V6.5.3

统一语言契约：

    en
    zh

全系统严格使用小写语言标识。

禁止：
    EN
    ZH

禁止任何语言大小写转换。

语言参数必须在进入系统时就是：
    en
    zh

整个系统中的目录、CLI、Task、Rule、Skill、EventUnit
全部遵循同一语言契约。
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
# SYSTEM ROOTS
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


# ============================================================
# EVENT UNIT FILE CONTRACT
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnit"

EVENT_INDEX_FILE = "_event_index.json"
EVENT_UNITS_COMPLETE_FILE = "_COMPLETE"
SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = "_global_merge_checkpoint.json"
INITIAL_CLUSTERS_FILE = "_initial_clusters.json"
MERGED_CLUSTERS_FILE = "_merged_clusters.json"


# ============================================================
# AI CONFIGURATION
# ============================================================

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


# ============================================================
# KNOWLEDGE PIPELINE CONFIGURATION
# ============================================================

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
    1,
)


# ============================================================
# TIMEZONE
# ============================================================

BEIJING_TZ = ZoneInfo("Asia/Shanghai")


# ============================================================
# LANGUAGE CONTRACT
#
# 全系统唯一合法语言：
#
#     en
#     zh
#
# 严禁：
#
#     EN
#     ZH
#
# 不做任何大小写转换。
# ============================================================

SUPPORTED_LANGUAGES = (
    "en",
    "zh",
)


CURRENT_LANGUAGE = None


# ============================================================
# LANGUAGE VALIDATION
# ============================================================

def normalize_language(language):
    """
    严格验证语言标识。

    注意：
    本函数名称保留，是为了兼容现有 Task / Common 调用。

    但 V6.5.3 开始不再做任何大小写转换。

    合法：
        en
        zh

    非法：
        EN
        ZH
        En
        Zh
        eN
        zH
        其他任何值
    """

    value = str(language or "").strip()

    if value not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            f"❌ 不支持的语言：{language}\n"
            f"语言必须严格使用小写：en 或 zh"
        )

    return value


# ============================================================
# TIME
# ============================================================

def now():
    return datetime.now(BEIJING_TZ)


# ============================================================
# EVENT UNIT PATHS
# ============================================================

def event_units_root(date):
    return RAW_NEWS / f"{date}-EventUnit"


def language_dir(date, language=None):
    """
    返回指定日期、指定语言的 EventUnit 语言目录。

    语言必须已经是严格小写：
        en
        zh

    本函数不进行任何大小写转换。
    """

    if language is None:
        language = getattr(
            sys.modules[__name__],
            "CURRENT_LANGUAGE",
            None
        )

    lang = normalize_language(language)

    return event_units_root(date) / lang


def event_units_dir(date, language=None):
    return language_dir(date, language) / "event_units"


def articles_dir(date, language=None):
    return language_dir(date, language) / "articles"


def conflict_log_path(date):
    return LOGS / f"{date}_event_aggregation_conflicts.log"


def global_merge_checkpoint_path(date, language=None):
    return (
        event_units_dir(date, language)
        / GLOBAL_MERGE_CHECKPOINT_FILE
    )


def initial_clusters_path(date, language=None):
    return (
        language_dir(date, language)
        / INITIAL_CLUSTERS_FILE
    )


def merged_clusters_path(date, language=None):
    return (
        language_dir(date, language)
        / MERGED_CLUSTERS_FILE
    )


# ============================================================
# ATOMIC TEXT WRITE
# ============================================================

def write_text_atomic(path, text):
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


# ============================================================
# CONFLICT LOG
# ============================================================

def log_conflict(
    date,
    stage,
    message,
    details=None
):
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
            detail,
        ]

    lines += [
        "=" * 80,
        "",
    ]

    with conflict_log_path(date).open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print(f"⚠️ {message}")
    print(
        f"   Conflict log: "
        f"{conflict_log_path(date)}"
    )


# ============================================================
# JSON
# ============================================================

def read_json(path, default=None):

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


# ============================================================
# AI JSON PARSER
# ============================================================

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
            f"❌ AI JSON解析失败：{context}\n\n"
            f"{text[:5000]}"
        )


# ============================================================
# SAFE FILE NAME
# ============================================================

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

    return (
        text[:120]
        or "未命名"
    )


# ============================================================
# FRONT MATTER
# ============================================================

def parse_front_matter(content):

    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:
        return {}, content

    data = {}

    for line in parts[1].strip().splitlines():

        if ":" not in line:
            continue

        k, v = line.split(
            ":",
            1
        )

        data[k.strip()] = (
            v.strip()
            .strip('"')
            .strip("'")
        )

    return (
        data,
        parts[2].lstrip()
    )


# ============================================================
# AI REQUEST THROTTLE
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

        time.sleep(
            remaining
        )

    _LAST_AI_REQUEST_TIME = (
        time.monotonic()
    )


# ============================================================
# RETRY-AFTER
# ============================================================

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


# ============================================================
# 429 BACKOFF
# ============================================================

def calculate_429_backoff(
    retry_number
):

    base = min(
        AI_429_BACKOFF_BASE
        * (
            2 ** (
                retry_number - 1
            )
        ),
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


# ============================================================
# AI CALL
# ============================================================

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

    payload = json.dumps(
        {
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
        },
        ensure_ascii=False
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
                "748686-Knowledge-Pipeline/6.5.3"
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

                result = (
                    data[
                        "choices"
                    ][0][
                        "message"
                    ][
                        "content"
                    ]
                )

            except Exception as e:

                raise RuntimeError(
                    "❌ AGNES.ai 返回格式异常\n"
                    +
                    json.dumps(
                        data,
                        ensure_ascii=False
                    )[:5000]
                ) from e

            if not str(result).strip():

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
                        errors="replace"
                    )
                )

            except Exception:

                pass

            if e.code == 429:

                if attempt >= (
                    AI_MAX_429_RETRIES
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
                        AI_429_BACKOFF_MAX
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


# ============================================================
# SKILL ROUTES
# ============================================================

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


def route_skills(
    category,
    routes,
    skills
):

    selected = []

    for name in routes.get(
        category,
        []
    ):

        if name not in skills:

            raise RuntimeError(
                f"❌ skill_routes.json引用不存在Skill："
                f"{name}"
            )

        selected.append(
            skills[name]
        )

    return selected


# ============================================================
# ENRICHED NEWS
# ============================================================

def get_enriched_files(
    date,
    language
):
    """
    获取指定日期、指定小写语言的 Enriched 新闻。

    语言目录严格为：

        Raw News/
        └── DATE-Enriched/
            ├── en/
            └── zh/

    不进行任何大小写转换。
    """

    lang = normalize_language(
        language
    )

    root = (
        RAW_NEWS
        / f"{date}-Enriched"
        / lang
    )

    if not root.exists():

        raise FileNotFoundError(
            f"没有找到 "
            f"{date} / {lang} "
            f"Enriched目录：{root}"
        )

    return sorted(
        root.rglob("*.md")
    )


# ============================================================
# LOAD NEWS FILE
# ============================================================

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


# ============================================================
# LOAD ALL ENRICHED NEWS
# ============================================================

def load_all_enriched_news(
    date,
    language
):

    files = get_enriched_files(
        date,
        language
    )

    print(
        f"Enriched files: "
        f"{len(files)}"
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
        x
        for x in items
        if x["metadata"]
        .get(
            "title",
            ""
        )
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
        f"Valid news: "
        f"{len(items)}"
    )

    return items


# ============================================================
# GLOBAL CLUSTER REGISTRY
# ============================================================

def global_cluster_registry_path(
    date
):

    return (
        event_units_root(date)
        / GLOBAL_CLUSTER_REGISTRY_FILE
    )


def create_global_cluster_registry(
    date
):
    """
    Python 全局 Cluster 注册器。

    AI Local ID 与 Global ID 完全分离。

    AI：
        C001
        C002
        ...

    Python：
        EVT-YYYYMMDD-000001
        EVT-YYYYMMDD-000002
        ...
    """

    return {
        "date": str(date),
        "next_sequence": 1,
        "registered": []
    }


def persist_global_cluster_registry(
    date,
    registry
):

    write_json_atomic(
        global_cluster_registry_path(
            date
        ),
        {
            "version": "6.5.3",
            "date": registry["date"],
            "next_sequence": int(
                registry["next_sequence"]
            ),
            "registered":
                registry["registered"],
            "saved_at":
                now().isoformat()
        }
    )


def register_global_cluster_ids(
    date,
    clusters,
    registry,
    source
):
    """
    唯一的 Global Cluster ID 生成入口。

    AI 只能产生：

        C001
        C002
        ...

    Python 注册器统一产生：

        EVT-YYYYMMDD-000001
        EVT-YYYYMMDD-000002
        ...

    Recovery 使用同一注册器，
    因此不会重新使用已经分配过的序号。
    """

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
                f"❌ {date} "
                f"Global Registry收到空Local Cluster ID"
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
        ] = (
            "python_global_registry"
        )

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
                                []
                            )
                        )
                    )
            }
        )

        out.append(d)

    persist_global_cluster_registry(
        date,
        registry
    )

    return out


# ============================================================
# LOAD SAVED EVENT UNITS
# ============================================================

def load_saved_event_units(
    date,
    language
):
    """
    加载已经完成的 EventUnit。

    语言严格使用：

        en
        zh

    不进行大小写转换。
    """

    lang = normalize_language(
        language
    )

    target = event_units_dir(
        date,
        lang
    )

    marker = (
        language_dir(
            date,
            lang
        )
        / EVENT_UNITS_COMPLETE_FILE
    )

    if not marker.exists():

        raise RuntimeError(
            f"❌ {date} / {lang} "
            f"EventUnits尚未完成，"
            f"禁止进入27 Skills阶段"
        )

    idx = load_event_index(
        date,
        lang
    )

    if idx is None:

        raise RuntimeError(
            f"❌ {date} / {lang} "
            f"Event Index不存在或无效"
        )

    files = []

    for e in idx:

        eid = str(
            e.get(
                "event_id",
                ""
            )
        ).strip()

        matches = (
            sorted(
                target.glob(
                    f"{eid}_*.md"
                )
            )
            if eid
            else []
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
                f"❌ EventUnit缺失或无效："
                f"{eid}"
            )

        files.append(
            (
                e,
                valid
            )
        )

    return files


# ============================================================
# EVENT INDEX
# ============================================================

def load_event_index(
    date,
    language=None
):

    p = (
        event_units_dir(
            date,
            language
        )
        / EVENT_INDEX_FILE
    )

    if not p.exists():
        return None

    try:

        d = read_json(
            p,
            None
        )

    except Exception:

        return None

    return (
        d
        if isinstance(d, list)
        and d
        else None
    )


# ============================================================
# EVENT UNIT VALIDATION
# ============================================================

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
        m.get("event_id")
        == event_id
    ) and (
        m.get("status")
        == "completed"
    )
