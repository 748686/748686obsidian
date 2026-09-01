#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Common V6.5.3

公共基础模块。

本文件只负责：

    1. 系统根目录
    2. 文件路径
    3. 严格语言验证
    4. 时间
    5. JSON读写
    6. 原子文件写入
    7. Front Matter解析
    8. AI请求
    9. AI JSON解析
    10. Conflict Log
    11. Global Cluster Registry
    12. Global Cluster基本验证
    13. 公共EventUnit路径

本文件不负责：

    Task 1 — Cluster
    Task 2 — Global Merge
    Task 3 — EventUnit
    Task 4 — 27 Skills

尤其禁止把Task业务逻辑重新放回本文件。

LANGUAGE CONTRACT
=================

系统唯一合法语言：

    en
    zh

禁止：

    EN
    ZH
    En
    Zh
    eN
    zH

禁止任何大小写转换。

Filesystem：

    Raw News/
        YYYY-MM-DD-EventUnit/
            _global_cluster_registry.json
            en/
            zh/
"""

from __future__ import annotations

import json
import os
import random
import re
import time

from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


# ============================================================
# ROOT
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
# FILE CONTRACT
# ============================================================

EVENT_UNITS_SUFFIX = "EventUnit"

EVENT_INDEX_FILE = "_event_index.json"

EVENT_UNITS_COMPLETE_FILE = "_COMPLETE"

SKILLS_COMPLETE_FILE = "_SKILLS_COMPLETE"

GLOBAL_MERGE_CHECKPOINT_FILE = (
    "_global_merge_checkpoint.json"
)

INITIAL_CLUSTERS_FILE = (
    "_initial_clusters.json"
)

MERGED_CLUSTERS_FILE = (
    "_merged_clusters.json"
)

GLOBAL_CLUSTER_REGISTRY_FILE = (
    "_global_cluster_registry.json"
)


# ============================================================
# PIPELINE COMMON CONFIGURATION
# ============================================================

AGGREGATION_BATCH_SIZE = 30

GLOBAL_MERGE_WINDOW_SIZE = 30

GLOBAL_MERGE_OVERLAP = 0

MAX_ARTICLES_PER_EVENT_CONTEXT = 30

ARTICLE_CLUSTER_CONTENT_LIMIT = 3500

ARTICLE_AGGREGATION_CONTENT_LIMIT = 8000


# ------------------------------------------------------------
# Recovery policy
# ------------------------------------------------------------

# 正常：
#
#     30
#
# 失败：
#
#     30
#     15
#     8
#     4
#     2
#     1
#
# 最终Singleton安全落地。

RECOVERY_BATCH_SIZES = (
    30,
    15,
    8,
    4,
    2,
    1,
)


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
# TIME
# ============================================================

BEIJING_TZ = ZoneInfo(
    "Asia/Shanghai"
)


def now():
    return datetime.now(
        BEIJING_TZ
    )


# ============================================================
# LANGUAGE CONTRACT
# ============================================================

SUPPORTED_LANGUAGES = (
    "en",
    "zh"
)

CURRENT_LANGUAGE = None


def validate_language(language):
    """
    严格验证language。

    不进行任何大小写转换。
    """

    if not isinstance(
        language,
        str
    ):
        raise RuntimeError(
            f"❌ language必须是小写字符串：{language!r}"
        )

    if language not in SUPPORTED_LANGUAGES:
        raise RuntimeError(
            "❌ language非法。"
            f"收到={language!r}；"
            "只允许：en / zh"
        )

    return language


# ============================================================
# PATHS
# ============================================================

def event_units_root(date):
    return (
        RAW_NEWS /
        f"{date}-EventUnit"
    )


def language_dir(
    date,
    language
):
    lang = validate_language(
        language
    )

    return (
        event_units_root(date) /
        lang
    )


def event_units_dir(
    date,
    language
):
    return (
        language_dir(
            date,
            language
        ) /
        "event_units"
    )


def articles_dir(
    date,
    language
):
    return (
        language_dir(
            date,
            language
        ) /
        "articles"
    )


def initial_clusters_path(
    date,
    language
):
    return (
        language_dir(
            date,
            language
        ) /
        INITIAL_CLUSTERS_FILE
    )


def merged_clusters_path(
    date,
    language
):
    return (
        language_dir(
            date,
            language
        ) /
        MERGED_CLUSTERS_FILE
    )


def global_merge_checkpoint_path(
    date,
    language
):
    return (
        event_units_dir(
            date,
            language
        ) /
        GLOBAL_MERGE_CHECKPOINT_FILE
    )


def conflict_log_path(date):
    return (
        LOGS /
        f"{date}_event_aggregation_conflicts.log"
    )


# ============================================================
# GLOBAL REGISTRY PATH
# ============================================================

def global_cluster_registry_path(
    date
):
    """
    Global Registry由en / zh共同使用。

    正确：

        Raw News/
            YYYY-MM-DD-EventUnit/
                _global_cluster_registry.json

    language不参与路径。
    """

    return (
        event_units_root(date)
        /
        GLOBAL_CLUSTER_REGISTRY_FILE
    )


# ============================================================
# ATOMIC TEXT WRITE
# ============================================================

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


# ============================================================
# JSON
# ============================================================

def read_json(
    path,
    default=None
):
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
    data
):
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


def write_json_atomic(
    path,
    data
):
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


# ============================================================
# FRONT MATTER
# ============================================================

def parse_front_matter(
    content
):
    if not content.startswith("---"):
        return {}, content

    parts = content.split(
        "---",
        2
    )

    if len(parts) < 3:
        return {}, content

    data = {}

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

        data[
            key.strip()
        ] = (
            value.strip()
            .strip('"')
            .strip("'")
        )

    return (
        data,
        parts[2].lstrip()
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
                if isinstance(
                    details,
                    str
                )
                else json.dumps(
                    details,
                    ensure_ascii=False,
                    indent=2
                )
            )

        except Exception:

            detail = str(
                details
            )

        lines += [
            "DETAILS:",
            detail,
        ]

    lines += [
        "=" * 80,
        "",
    ]

    with conflict_log_path(
        date
    ).open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(lines)
        )

    print(
        f"⚠️ {message}"
    )

    print(
        f"   Conflict log: "
        f"{conflict_log_path(date)}"
    )


# ============================================================
# AI JSON PARSER
# ============================================================

def parse_ai_json(
    result,
    context
):
    text = str(
        result
    ).strip()

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

        return json.loads(
            text
        )

    except Exception:

        start = text.find(
            "{"
        )

        end = text.rfind(
            "}"
        )

        if (
            start >= 0
            and end > start
        ):

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
# AI THROTTLE
# ============================================================

def wait_for_ai_throttle():

    global _LAST_AI_REQUEST_TIME

    elapsed = (
        time.monotonic()
        -
        _LAST_AI_REQUEST_TIME
    )

    remaining = (
        AI_REQUEST_THROTTLE_SECONDS
        -
        elapsed
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
# RETRY AFTER
# ============================================================

def parse_retry_after(
    headers
):
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
        *
        (
            2 **
            (
                retry_number - 1
            )
        ),
        AI_429_BACKOFF_MAX
    )

    return min(
        base
        +
        random.uniform(
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
        +
        "/chat/completions",
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
            ) as response:

                raw = (
                    response
                    .read()
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
                    "❌ AGNES.ai返回不是合法JSON\n"
                    +
                    raw[:3000]
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
                    "❌ AGNES.ai返回格式异常\n"
                    +
                    json.dumps(
                        data,
                        ensure_ascii=False
                    )[:5000]
                ) from e

            if not str(
                result
            ).strip():

                raise RuntimeError(
                    "❌ AGNES.ai返回空内容"
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
                "❌ AGNES.ai网络连接失败\n"
                f"{e.reason}"
            ) from e

        except TimeoutError as e:

            raise RuntimeError(
                "❌ AGNES.ai请求超时"
            ) from e

        except Exception as e:

            raise RuntimeError(
                f"❌ AGNES.ai请求失败：{e}"
            ) from e

    raise RuntimeError(
        "❌ AGNES.ai请求异常结束"
    )


# ============================================================
# GLOBAL CLUSTER REGISTRY
# ============================================================

def create_global_cluster_registry(
    date
):
    """
    创建当天Global Cluster Registry。

    Registry由en / zh共同使用。

    AI Local ID：

        C001
        C002

    Python Global ID：

        EVT-YYYYMMDD-000001
        EVT-YYYYMMDD-000002
    """

    return {
        "version": "6.5.3",
        "date": str(date),
        "next_sequence": 1,
        "registered": []
    }


def validate_registry_basic(
    date,
    registry
):
    if not isinstance(
        registry,
        dict
    ):

        raise RuntimeError(
            f"❌ {date} Global Cluster Registry不是对象"
        )

    if registry.get(
        "date"
    ) != str(date):

        raise RuntimeError(
            f"❌ {date} Global Cluster Registry日期异常"
        )

    next_sequence = registry.get(
        "next_sequence"
    )

    if (
        not isinstance(
            next_sequence,
            int
        )
        or isinstance(
            next_sequence,
            bool
        )
        or next_sequence < 1
    ):

        raise RuntimeError(
            f"❌ {date} Global Cluster Registry "
            "next_sequence异常"
        )

    registered = registry.get(
        "registered"
    )

    if not isinstance(
        registered,
        list
    ):

        raise RuntimeError(
            f"❌ {date} Global Cluster Registry "
            "registered异常"
        )

    # ----------------------------------------------------------
    # Registry内部唯一性检查
    # ----------------------------------------------------------

    global_ids = set()
    local_source_pairs = set()

    for pos, item in enumerate(
        registered,
        1
    ):

        if not isinstance(
            item,
            dict
        ):

            raise RuntimeError(
                f"❌ {date} Registry "
                f"registered[{pos}]不是对象"
            )

        gid = str(
            item.get(
                "global_cluster_id",
                ""
            )
        ).strip()

        if not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            gid
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

        global_ids.add(
            gid
        )

        local_id = str(
            item.get(
                "local_cluster_id",
                ""
            )
        ).strip()

        source = str(
            item.get(
                "source",
                ""
            )
        ).strip()

        if local_id and source:

            pair = (
                source,
                local_id
            )

            if pair in local_source_pairs:

                # 同一个source下相同Local ID重复注册
                # 通常说明同一批数据被重复提交。
                raise RuntimeError(
                    f"❌ {date} Registry存在重复Local ID："
                    f"source={source}, "
                    f"local={local_id}"
                )

            local_source_pairs.add(
                pair
            )


def persist_global_cluster_registry(
    date,
    registry
):
    validate_registry_basic(
        date,
        registry
    )

    write_json_atomic(
        global_cluster_registry_path(
            date
        ),
        {
            "version": "6.5.3",

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
    唯一Global Cluster ID生成入口。

    AI产生Local ID。

    Python Registry产生Global ID。

    Global ID：

        EVT-YYYYMMDD-000001

    注意：

        source + local_cluster_id
        必须唯一。

    不允许同一来源的同一个Local ID
    被重复注册。
    """

    validate_registry_basic(
        date,
        registry
    )

    source = str(
        source
    ).strip()

    if not source:

        raise RuntimeError(
            f"❌ {date} Registry source不能为空"
        )

    out = []

    existing_pairs = {
        (
            str(
                item.get(
                    "source",
                    ""
                )
            ).strip(),
            str(
                item.get(
                    "local_cluster_id",
                    ""
                )
            ).strip()
        )
        for item in registry[
            "registered"
        ]
        if isinstance(
            item,
            dict
        )
    }

    batch_pairs = set()

    for cluster in clusters:

        if not isinstance(
            cluster,
            dict
        ):

            raise RuntimeError(
                f"❌ {date} Registry收到非对象Cluster"
            )

        d = dict(
            cluster
        )

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
                f"❌ {date} Registry收到空Local Cluster ID"
            )

        # ------------------------------------------------------
        # Local ID格式
        # ------------------------------------------------------

        if not re.fullmatch(
            r"C\d{3,}",
            local_id
        ):

            raise RuntimeError(
                f"❌ AI Local Cluster ID非法："
                f"{local_id}"
            )

        # ------------------------------------------------------
        # AI绝不能产生Global ID
        # ------------------------------------------------------

        if re.fullmatch(
            r"(EVT|REC|GM)-.*",
            local_id,
            flags=re.I
        ):

            raise RuntimeError(
                f"❌ AI Local Cluster ID非法："
                f"{local_id}"
            )

        pair = (
            source,
            local_id
        )

        if pair in existing_pairs:

            raise RuntimeError(
                f"❌ Global Registry重复注册："
                f"source={source}, "
                f"local_cluster_id={local_id}"
            )

        if pair in batch_pairs:

            raise RuntimeError(
                f"❌ 当前批次存在重复Local Cluster ID："
                f"source={source}, "
                f"local_cluster_id={local_id}"
            )

        batch_pairs.add(
            pair
        )

        # ------------------------------------------------------
        # Global ID
        # ------------------------------------------------------

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

        # ------------------------------------------------------
        # 输出Cluster
        # ------------------------------------------------------

        d[
            "local_cluster_id"
        ] = local_id

        d[
            "cluster_id"
        ] = global_id

        # Stage 1A：
        #
        # 每个Initial Cluster自己的成员
        # 就是自己。
        #
        # 后续Global Merge才会形成：
        #
        # member_cluster_ids:
        # [
        #     EVT-...
        #     EVT-...
        # ]

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

        # ------------------------------------------------------
        # Registry record
        # ------------------------------------------------------

        article_indexes = []

        for value in d.get(
            "article_indexes",
            []
        ):

            try:

                article_indexes.append(
                    int(value)
                )

            except Exception:

                raise RuntimeError(
                    f"❌ {date} Registry收到非法ARTICLE："
                    f"{value}"
                )

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
                            article_indexes
                        )
                    )
            }
        )

        existing_pairs.add(
            pair
        )

        out.append(
            d
        )

    persist_global_cluster_registry(
        date,
        registry
    )

    return out


# ============================================================
# GLOBAL CLUSTER MEMBERSHIP VALIDATION
# ============================================================

def validate_global_cluster_membership(
    date,
    clusters,
    context,
    expected_original_ids=None
):
    """
    Global Cluster Membership基础验证。

    重要：

    Stage 1A INITIAL：

        cluster_id = EVT-...
        member_cluster_ids = [自己的EVT-...]

    Global Merge之后：

        cluster_id = EVT-...
        member_cluster_ids = [
            原始EVT-...,
            原始EVT-...,
            ...
        ]

    因此这里不要求：
        member_cluster_ids必须属于
        expected_original_ids

    expected_original_ids如果传入，
    才进行严格成员集合检查。
    """

    seen_current = set()

    seen_original = set()

    malformed = []

    duplicate_current = []

    duplicate_original = []

    self_membership_errors = []

    for pos, cluster in enumerate(
        clusters,
        1
    ):

        if not isinstance(
            cluster,
            dict
        ):

            malformed.append(
                f"cluster[{pos}]不是对象"
            )

            continue

        cid = str(
            cluster.get(
                "cluster_id",
                ""
            )
        ).strip()

        # ------------------------------------------------------
        # Current Global ID
        # ------------------------------------------------------

        if not cid or not re.fullmatch(
            r"EVT-\d{8}-\d{6}",
            cid
        ):

            malformed.append(
                f"cluster[{pos}]"
                f"非法Global cluster_id：{cid}"
            )

        elif cid in seen_current:

            duplicate_current.append(
                cid
            )

        else:

            seen_current.add(
                cid
            )

        # ------------------------------------------------------
        # Member Cluster IDs
        # ------------------------------------------------------

        members = cluster.get(
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

        local_seen = set()

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

            if not re.fullmatch(
                r"EVT-\d{8}-\d{6}",
                member
            ):

                malformed.append(
                    f"cluster[{pos}]"
                    f"非法member_cluster_id：{member}"
                )

                continue

            if member in local_seen:

                malformed.append(
                    f"cluster[{pos}]"
                    f"member_cluster_ids内部重复：{member}"
                )

            local_seen.add(
                member
            )

            if member in seen_original:

                duplicate_original.append(
                    member
                )

            else:

                seen_original.add(
                    member
                )

        # ------------------------------------------------------
        # Stage 1A Initial Cluster必须自包含
        # ------------------------------------------------------

        if (
            len(members) == 1
            and str(
                members[0]
            ).strip() != cid
        ):

            self_membership_errors.append(
                {
                    "cluster_id":
                        cid,

                    "member_cluster_ids":
                        members
                }
            )

    # ==========================================================
    # expected_original_ids
    # ==========================================================

    expected = set(
        map(
            str,
            expected_original_ids or []
        )
    )

    missing = (
        sorted(
            expected -
            seen_original
        )
        if expected_original_ids is not None
        else []
    )

    extra = (
        sorted(
            seen_original -
            expected
        )
        if expected_original_ids is not None
        else []
    )

    # ==========================================================
    # IMPORTANT:
    #
    # Stage 1A INITIAL调用时：
    #
    # expected_original_ids = None
    #
    # 因此这里只检查：
    #
    # 1. Global ID合法
    # 2. Global ID不重复
    # 3. member ID合法
    # 4. member不重复
    # 5. Initial singleton/self-membership正确
    #
    # 不把Registry历史记录混入当前Cluster验证。
    # ==========================================================

    if (
        malformed
        or duplicate_current
        or duplicate_original
        or self_membership_errors
        or missing
        or extra
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

                "self_membership_errors":
                    self_membership_errors,

                "missing_original":
                    missing,

                "extra_original":
                    extra
            }
        )

        raise RuntimeError(
            f"❌ {context} Global Cluster membership异常"
        )


# ============================================================
# GLOBAL ARTICLE COVERAGE VALIDATION
# ============================================================

def validate_global_article_coverage(
    date,
    clusters,
    news_count,
    context
):
    all_indexes = []

    malformed = []

    for pos, cluster in enumerate(
        clusters,
        1
    ):

        ids = (
            cluster.get(
                "article_indexes"
            )
            if isinstance(
                cluster,
                dict
            )
            else None
        )

        if not isinstance(
            ids,
            list
        ):

            malformed.append(
                f"cluster[{pos}] "
                "article_indexes不是数组"
            )

            continue

        for value in ids:

            try:

                all_indexes.append(
                    int(value)
                )

            except Exception:

                malformed.append(
                    f"cluster[{pos}]"
                    f"非法ARTICLE：{value}"
                )

    expected = set(
        range(
            1,
            news_count + 1
        )
    )

    actual = set(
        all_indexes
    )

    duplicate = sorted(
        {
            x
            for x in all_indexes
            if all_indexes.count(x) > 1
        }
    )

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
