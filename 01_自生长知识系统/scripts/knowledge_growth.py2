#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Growth Engine V3.1

======================================================================
核心定位
======================================================================

    Task 4
       ↓
    knowledge_daily.py
       ↓
    05_日报
       ↓
    knowledge_asset.py
       ↓
    08_知识库 + 09_知识图谱
       ↓
    weekly_report.py
       ↓
    06_周报
       ↓
    knowledge_growth.py
       ↓
    知识系统健康检查 + 知识增长 + 知识缺口 + 新关系 + 专题机会


======================================================================
V3.1 核心变化
======================================================================

V3.0：

    全部 Task 4 Analysis
             +
    全部知识库
             +
    全部知识图谱
             +
    日报 / 周报 / 专题
             ↓
        单次 AI 请求

V3.1：

    Task 4 Analysis
             ↓
       EVT-ID 去重
             ↓
       字符数分批
             ↓
    Batch Growth Analysis
             ↓
      候选结果集合
             ↓
       Final Merge AI
             ↓
    CREATE / UPDATE / SKIP
             ↓
    知识库 / 图谱 / 缺口 / 专题


======================================================================
主要修复
======================================================================

1. 修复 HTTP 400 错误信息被吞掉的问题
2. AI 请求自动输出 HTTP 状态及 response body
3. Task 4 Analysis 分批发送
4. 同一 EVT-ID 的 en / zh 永远不会被拆成两个独立事件
5. en / zh 目录严格只允许小写
6. 限制单个 AI 请求最大字符数
7. 限制知识库 inventory 总字符数
8. 限制图谱 inventory 总字符数
9. 限制日报 / 周报 / 专题上下文
10. Batch AI 输出再次压缩后才进入 Final Merge
11. Final Merge 不再读取全部原始新闻 Analysis
12. 防止同一 Event ID 重复计数
13. 防止同一事件造成重复知识更新
14. 只有整个日期成功后才写 COMPLETE
15. API 失败时不会错误写 COMPLETE
16. 保持现有知识文件结构
17. 保持现有知识图谱结构
18. 保持现有专题候选结构
19. 保持现有知识缺口结构
20. 保持现有知识矛盾结构


======================================================================
目录契约
======================================================================

语言目录严格：

    en
    zh

禁止：

    EN
    ZH

不会进行任何大小写转换。


======================================================================
时间
======================================================================

固定使用：

    Asia/Shanghai
"""

from __future__ import annotations

import os
import re
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Dict, List, Tuple
from zoneinfo import ZoneInfo
from urllib import request, error


# ======================================================================
# 基础配置
# ======================================================================

TIMEZONE = ZoneInfo("Asia/Shanghai")

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

DAILY_DIR = ROOT / "05_日报"
WEEKLY_DIR = ROOT / "06_周报"
TOPIC_DIR = ROOT / "07_专题报告"
KNOWLEDGE_DIR = ROOT / "08_知识库"
GRAPH_DIR = ROOT / "09_知识图谱"

SYSTEM_LOG_DIR = (
    ROOT
    / "00_System"
    / "运行日志"
    / "knowledge_growth"
)


# ======================================================================
# AI 配置
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1"
).rstrip("/")

AGNES_MODEL = os.getenv(
    "AGNES_MODEL",
    "agnes-2.5-flash"
)

AGNES_API_KEY = os.getenv(
    "AGNES_API_KEY"
)

AI_TIMEOUT = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_TIMEOUT",
        "180"
    )
)

AI_RETRIES = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_RETRIES",
        "3"
    )
)

AI_THROTTLE_SECONDS = float(
    os.getenv(
        "KNOWLEDGE_GROWTH_THROTTLE",
        "1.2"
    )
)


# ======================================================================
# V3.1 分段参数
# ======================================================================

# 一个 batch 最多包含多少个唯一 EVT-ID
BATCH_MAX_EVENTS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_BATCH_EVENTS",
        "24"
    )
)

# 一个 batch 的最大字符数
BATCH_MAX_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_BATCH_CHARS",
        "60000"
    )
)

# 单个 Analysis 文件最大进入 AI 的字符数
MAX_ANALYSIS_CHARS_PER_FILE = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_ANALYSIS_FILE_CHARS",
        "8000"
    )
)

# 知识库总 inventory 上限
MAX_KNOWLEDGE_INVENTORY_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_KNOWLEDGE_CHARS",
        "80000"
    )
)

# 图谱总 inventory 上限
MAX_GRAPH_INVENTORY_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_GRAPH_CHARS",
        "20000"
    )
)

# 日报最大字符数
MAX_DAILY_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_DAILY_CHARS",
        "15000"
    )
)

# 周报总字符数
MAX_WEEKLY_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_WEEKLY_CHARS",
        "20000"
    )
)

# 专题总字符数
MAX_TOPIC_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_TOPIC_CHARS",
        "20000"
    )
)

# Final Merge 中每个 Batch AI 输出最多保留多少字符
MAX_BATCH_RESULT_CHARS = int(
    os.getenv(
        "KNOWLEDGE_GROWTH_BATCH_RESULT_CHARS",
        "12000"
    )
)


# ======================================================================
# 知识类型
# ======================================================================

KNOWLEDGE_TYPES = [
    "主题",
    "产品",
    "人物",
    "公司",
    "技术",
    "概念",
    "行业",
]

KNOWLEDGE_TYPE_DIR = {
    "主题": "主题",
    "产品": "产品",
    "人物": "人物",
    "公司": "公司",
    "技术": "技术",
    "概念": "概念",
    "行业": "行业",
}


# ======================================================================
# 工具函数
# ======================================================================

def now_local() -> datetime:
    return datetime.now(TIMEZONE)


def today_str() -> str:
    return now_local().strftime("%Y-%m-%d")


def log(message: str) -> None:
    print(message, flush=True)


def ensure_dir(path: Path) -> None:
    path.mkdir(
        parents=True,
        exist_ok=True
    )


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def safe_filename(name: str) -> str:
    name = str(name).strip()

    name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name
    )

    name = re.sub(
        r"\s+",
        " ",
        name
    )

    name = name.strip(" .")

    if not name:
        name = "未命名"

    return name[:180]


def read_text(path: Path) -> str:

    try:

        return path.read_text(
            encoding="utf-8"
        )

    except Exception:

        return ""


def atomic_write(
    path: Path,
    content: str
) -> None:

    ensure_dir(
        path.parent
    )

    tmp = path.with_name(
        path.name + ".tmp"
    )

    tmp.write_text(
        content,
        encoding="utf-8"
    )

    tmp.replace(path)


def nonempty_files(
    directory: Path,
    pattern: str = "*.md"
) -> List[Path]:

    if not directory.exists():
        return []

    result = []

    for path in directory.rglob(pattern):

        if not path.is_file():
            continue

        try:

            if path.stat().st_size <= 0:
                continue

        except Exception:

            continue

        result.append(path)

    return sorted(
        result,
        key=lambda p: p.as_posix()
    )


def truncate_text(
    text: str,
    max_chars: int
) -> str:

    text = str(text or "")

    if len(text) <= max_chars:
        return text

    return (
        text[:max_chars]
        + "\n\n[TRUNCATED BY KNOWLEDGE GROWTH ENGINE]"
    )


# ======================================================================
# AI 请求
# ======================================================================

def call_ai(
    system_prompt: str,
    user_prompt: str,
) -> str:

    if not AGNES_API_KEY:

        raise RuntimeError(
            "缺少 AGNES_API_KEY"
        )

    url = (
        AGNES_BASE_URL
        + "/chat/completions"
    )

    payload = {
        "model": AGNES_MODEL,
        "temperature": 0.1,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
    }

    body = json.dumps(
        payload,
        ensure_ascii=False
    ).encode("utf-8")

    headers = {
        "Authorization":
            f"Bearer {AGNES_API_KEY}",
        "Content-Type":
            "application/json",
    }

    log(
        "   AI REQUEST SIZE : "
        f"{len(body):,} bytes"
    )

    last_error = None

    for attempt in range(
        1,
        AI_RETRIES + 1
    ):

        try:

            if attempt > 1:

                time.sleep(
                    AI_THROTTLE_SECONDS
                    * attempt
                )

            req = request.Request(
                url,
                data=body,
                headers=headers,
                method="POST",
            )

            with request.urlopen(
                req,
                timeout=AI_TIMEOUT
            ) as response:

                raw = response.read().decode(
                    "utf-8",
                    errors="replace"
                )

                status_code = response.getcode()

            if status_code != 200:

                raise RuntimeError(
                    f"HTTP {status_code}: "
                    f"{raw[:5000]}"
                )

            try:

                data = json.loads(
                    raw
                )

            except Exception as exc:

                raise RuntimeError(
                    "AI 返回不是合法 JSON："
                    + str(exc)
                )

            content = (
                data
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            # 某些兼容 API 可能返回非字符串
            if isinstance(
                content,
                list
            ):

                parts = []

                for item in content:

                    if isinstance(
                        item,
                        dict
                    ):

                        text = item.get(
                            "text",
                            ""
                        )

                        if text:
                            parts.append(
                                str(text)
                            )

                content = "\n".join(
                    parts
                )

            if not content:

                raise RuntimeError(
                    "AI 返回内容为空"
                )

            return str(
                content
            ).strip()

        except error.HTTPError as exc:

            try:

                error_body = (
                    exc.read()
                    .decode(
                        "utf-8",
                        errors="replace"
                    )
                )

            except Exception:

                error_body = ""

            log(
                f"⚠️ AI HTTP ERROR "
                f"{attempt}/{AI_RETRIES}"
            )

            log(
                f"   STATUS : {exc.code}"
            )

            log(
                f"   URL    : {url}"
            )

            if error_body:

                log(
                    "   BODY   : "
                    + error_body[:5000]
                )

            else:

                log(
                    "   BODY   : <empty>"
                )

            last_error = RuntimeError(
                f"HTTP {exc.code}: "
                f"{error_body[:5000]}"
            )

        except error.URLError as exc:

            log(
                f"⚠️ AI NETWORK ERROR "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            last_error = exc

        except Exception as exc:

            log(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            last_error = exc

    raise RuntimeError(
        f"AI 请求失败: {last_error}"
    )


# ======================================================================
# JSON 提取
# ======================================================================

def extract_json(
    text: str
) -> Dict[str, Any]:

    text = str(
        text or ""
    ).strip()

    # 去除 markdown code fence
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
    )

    try:

        value = json.loads(
            text
        )

        if isinstance(
            value,
            dict
        ):
            return value

    except Exception:
        pass

    # 尝试寻找最外层 JSON
    start = text.find("{")
    end = text.rfind("}")

    if start >= 0 and end > start:

        candidate = text[
            start:end + 1
        ]

        try:

            value = json.loads(
                candidate
            )

            if isinstance(
                value,
                dict
            ):
                return value

        except Exception:
            pass

    raise ValueError(
        "无法解析 AI JSON 输出"
    )


# ======================================================================
# 日期
# ======================================================================

def target_dates() -> List[str]:

    today = now_local().date()

    return [
        (
            today
            - timedelta(days=2)
        ).strftime("%Y-%m-%d"),

        (
            today
            - timedelta(days=1)
        ).strftime("%Y-%m-%d"),

        today.strftime("%Y-%m-%d"),
    ]


# ======================================================================
# Task 4 Analysis
# ======================================================================

def find_analysis_files(
    date_str: str
) -> List[Path]:

    base = (
        RAW_NEWS
        / f"{date_str}-EventUnit"
    )

    result = []

    # 严格只允许小写 en / zh
    for language in (
        "en",
        "zh"
    ):

        directory = (
            base
            / language
            / "event_units"
        )

        if not directory.exists():
            continue

        for path in sorted(
            directory.glob(
                "*_analysis.md"
            )
        ):

            if not path.is_file():
                continue

            try:

                if path.stat().st_size <= 0:
                    continue

            except Exception:

                continue

            result.append(path)

    return result


def extract_event_id(
    path: Path
) -> str:

    match = re.search(
        r"(EVT-\d{8}-\d+)",
        path.name
    )

    if match:

        return match.group(1)

    return path.stem.replace(
        "_analysis",
        ""
    )


def detect_language(
    path: Path
) -> str:

    parts = path.parts

    if "en" in parts:
        return "en"

    if "zh" in parts:
        return "zh"

    # 理论上不会进入这里
    return "unknown"


# ======================================================================
# EVT-ID 分组
# ======================================================================

def group_analysis_by_event(
    paths: List[Path]
) -> Dict[str, List[Path]]:

    grouped: Dict[
        str,
        List[Path]
    ] = {}

    for path in paths:

        event_id = extract_event_id(
            path
        )

        grouped.setdefault(
            event_id,
            []
        ).append(path)

    for event_id in grouped:

        grouped[event_id] = sorted(
            grouped[event_id],
            key=lambda p: (
                detect_language(p),
                p.as_posix()
            )
        )

    return grouped


def render_event(
    event_id: str,
    paths: List[Path]
) -> str:

    chunks = [
        "==================================================",
        f"EVENT_ID: {event_id}",
        "==================================================",
    ]

    for path in paths:

        language = detect_language(
            path
        )

        if language not in (
            "en",
            "zh"
        ):
            continue

        content = read_text(
            path
        )

        if not content.strip():
            continue

        content = truncate_text(
            content,
            MAX_ANALYSIS_CHARS_PER_FILE
        )

        chunks.extend([
            "",
            f"LANGUAGE: {language}",
            f"FILE: {path.relative_to(ROOT)}",
            "--------------------------------------------------",
            content,
        ])

    return "\n".join(
        chunks
    )


def build_event_records(
    paths: List[Path]
) -> List[Tuple[str, str]]:

    grouped = group_analysis_by_event(
        paths
    )

    records = []

    for event_id in sorted(
        grouped.keys()
    ):

        rendered = render_event(
            event_id,
            grouped[event_id]
        )

        if rendered.strip():

            records.append(
                (
                    event_id,
                    rendered
                )
            )

    return records


# ======================================================================
# 分批
# ======================================================================

def build_batches(
    event_records: List[Tuple[str, str]]
) -> List[List[Tuple[str, str]]]:

    batches = []

    current = []

    current_chars = 0

    for event_id, text in event_records:

        text_len = len(text)

        # 单个事件本身超过 batch 上限
        # 仍然单独作为一个 batch
        if (
            text_len > BATCH_MAX_CHARS
            and not current
        ):

            batches.append([
                (
                    event_id,
                    text
                )
            ])

            continue

        # 当前 batch 已有内容，需要判断是否超限
        if current:

            would_exceed_events = (
                len(current)
                >= BATCH_MAX_EVENTS
            )

            would_exceed_chars = (
                current_chars
                + text_len
                > BATCH_MAX_CHARS
            )

            if (
                would_exceed_events
                or would_exceed_chars
            ):

                batches.append(
                    current
                )

                current = []

                current_chars = 0

        current.append(
            (
                event_id,
                text
            )
        )

        current_chars += text_len

    if current:

        batches.append(
            current
        )

    return batches


# ======================================================================
# 日报 / 周报 / 专题
# ======================================================================

def find_daily_report(
    date_str: str
) -> Path | None:

    year, month, _ = date_str.split("-")

    path = (
        DAILY_DIR
        / year
        / month
        / f"{date_str}.md"
    )

    if (
        path.exists()
        and path.stat().st_size > 0
    ):

        return path

    return None


def find_recent_weekly_reports(
    limit: int = 4
) -> List[Path]:

    files = nonempty_files(
        WEEKLY_DIR
    )

    return files[-limit:]


def find_recent_topic_reports(
    limit: int = 10
) -> List[Path]:

    files = nonempty_files(
        TOPIC_DIR
    )

    return files[-limit:]


def build_report_context(
    date_str: str
) -> str:

    sections = []

    # --------------------------------------------------------------
    # 日报
    # --------------------------------------------------------------

    daily = find_daily_report(
        date_str
    )

    if daily:

        daily_text = truncate_text(
            read_text(daily),
            MAX_DAILY_CHARS
        )

        sections.append(
            "================ 日报 ================\n"
            + daily_text
        )

    # --------------------------------------------------------------
    # 周报
    # --------------------------------------------------------------

    weekly_files = (
        find_recent_weekly_reports()
    )

    if weekly_files:

        weekly_chunks = []

        total = 0

        for path in reversed(
            weekly_files
        ):

            text = read_text(
                path
            )

            block = (
                f"\n--- "
                f"{path.relative_to(ROOT)} "
                f"---\n"
                + text
            )

            remaining = (
                MAX_WEEKLY_CHARS
                - total
            )

            if remaining <= 0:
                break

            block = truncate_text(
                block,
                remaining
            )

            weekly_chunks.append(
                block
            )

            total += len(
                block
            )

        if weekly_chunks:

            sections.append(
                "================ 最近周报 ================\n"
                + "\n".join(
                    weekly_chunks
                )
            )

    # --------------------------------------------------------------
    # 专题
    # --------------------------------------------------------------

    topic_files = (
        find_recent_topic_reports()
    )

    if topic_files:

        topic_chunks = []

        total = 0

        for path in reversed(
            topic_files
        ):

            text = read_text(
                path
            )

            block = (
                f"\n--- "
                f"{path.relative_to(ROOT)} "
                f"---\n"
                + text
            )

            remaining = (
                MAX_TOPIC_CHARS
                - total
            )

            if remaining <= 0:
                break

            block = truncate_text(
                block,
                remaining
            )

            topic_chunks.append(
                block
            )

            total += len(
                block
            )

        if topic_chunks:

            sections.append(
                "================ 最近专题 ================\n"
                + "\n".join(
                    topic_chunks
                )
            )

    return "\n\n".join(
        sections
    )


# ======================================================================
# 当前知识库
# ======================================================================

def knowledge_files() -> List[Path]:

    result = []

    for knowledge_type in KNOWLEDGE_TYPES:

        directory = (
            KNOWLEDGE_DIR
            / KNOWLEDGE_TYPE_DIR[
                knowledge_type
            ]
        )

        result.extend(
            nonempty_files(
                directory
            )
        )

    return sorted(
        result,
        key=lambda p: p.as_posix()
    )


def knowledge_inventory(
    max_chars: int = MAX_KNOWLEDGE_INVENTORY_CHARS
) -> str:

    files = knowledge_files()

    chunks = []

    total = 0

    for path in files:

        text = read_text(
            path
        )

        if not text.strip():
            continue

        # 每文件最多 4000 字符
        text = truncate_text(
            text,
            4000
        )

        block = "\n".join([
            "--------------------------------------------------",
            f"FILE: {path.relative_to(ROOT)}",
            "--------------------------------------------------",
            text,
        ])

        remaining = (
            max_chars
            - total
        )

        if remaining <= 0:
            break

        if len(block) > remaining:

            block = truncate_text(
                block,
                remaining
            )

        chunks.append(
            block
        )

        total += len(
            block
        )

    return "\n\n".join(
        chunks
    )


def graph_inventory(
    max_chars: int = MAX_GRAPH_INVENTORY_CHARS
) -> str:

    files = nonempty_files(
        GRAPH_DIR
    )

    chunks = []

    total = 0

    for path in reversed(
        files
    ):

        text = read_text(
            path
        )

        if not text.strip():
            continue

        block = (
            f"\n--- "
            f"{path.relative_to(ROOT)} "
            f"---\n"
            + text
        )

        remaining = (
            max_chars
            - total
        )

        if remaining <= 0:
            break

        if len(block) > remaining:

            block = truncate_text(
                block,
                remaining
            )

        chunks.append(
            block
        )

        total += len(
            block
        )

    return "\n".join(
        reversed(chunks)
    )


# ======================================================================
# AI System Prompt
# ======================================================================

SYSTEM_PROMPT = """
你是 748686 自生长知识系统的长期知识增长引擎。

你不是新闻摘要器。

你的任务是从可靠事件证据中识别真正具有长期价值的知识变化。

必须遵守：

1. 不编造事实。
2. 不因为新闻出现一次就机械创建知识。
3. 优先长期稳定、结构性、可复用的知识。
4. 同一个 EVT-ID 的 en 与 zh 是同一个事件。
5. en 与 zh 可以互相补充证据，但不得重复计算。
6. 已有知识优先 UPDATE，而不是 CREATE。
7. 没有足够证据时使用 skip。
8. 关系必须有明确证据。
9. knowledge_gaps 必须是真正的信息缺口。
10. contradictions 只是待核查的潜在矛盾，不代表已经证明冲突。
11. 不推断用户个人信息。
12. 不产生任何 10_用户资料内容。
13. 输出必须是合法 JSON。
14. 不要输出 markdown。
15. 不要输出解释文字。
16. 所有 source_event_ids 必须使用真实 EVT-ID。
17. 不得虚构 EVT-ID。
18. type 只能是：
    主题、产品、人物、公司、技术、概念、行业。
"""


# ======================================================================
# Batch Prompt
# ======================================================================

def build_batch_prompt(
    date_str: str,
    batch_index: int,
    total_batches: int,
    events: List[Tuple[str, str]],
    report_context: str,
    inventory: str,
    graph: str,
) -> str:

    event_text = "\n\n".join(
        text
        for _, text in events
    )

    event_ids = [
        event_id
        for event_id, _ in events
    ]

    return f"""
当前日期：

{date_str}

这是第 {batch_index}/{total_batches} 个事件批次。

本批次唯一 EVT-ID：

{json.dumps(
    event_ids,
    ensure_ascii=False,
    indent=2
)}

============================================================
当天背景
============================================================

{report_context}

============================================================
已有知识库
============================================================

{inventory}

============================================================
已有知识图谱
============================================================

{graph}

============================================================
本批次 Task 4 Analysis
============================================================

{event_text}

============================================================
任务
============================================================

只分析本批次事件。

判断哪些信息可能形成长期知识增长：

- 新知识
- 已有知识更新
- 新关系
- 知识缺口
- 潜在矛盾
- 专题候选

注意：

同一个 EVT-ID 如果同时出现 en 与 zh，只能算一个事件。
不要把同一个事件的两个语言版本当成两个独立来源。

不要为了让结果看起来丰富而强行 CREATE。

请严格输出：

{{
  "knowledge_updates": [
    {{
      "type": "公司|产品|人物|技术|概念|行业|主题",
      "name": "实体名称",
      "action": "create|update|skip",
      "importance": 1,
      "confidence": 0.0,
      "summary": "长期知识摘要",
      "new_facts": [
        "新增事实"
      ],
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "related_entities": [
        {{
          "type": "公司|产品|人物|技术|概念|行业|主题",
          "name": "相关实体"
        }}
      ]
    }}
  ],

  "relationships": [
    {{
      "from_type": "公司|产品|人物|技术|概念|行业|主题",
      "from": "实体A",
      "relation": "关系",
      "to_type": "公司|产品|人物|技术|概念|行业|主题",
      "to": "实体B",
      "evidence": "关系依据",
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "confidence": 0.0
    }}
  ],

  "knowledge_gaps": [
    {{
      "topic": "知识缺口",
      "reason": "为什么存在缺口",
      "priority": 1,
      "suggested_research": "建议研究方向",
      "source_event_ids": []
    }}
  ],

  "contradictions": [
    {{
      "topic": "可能矛盾",
      "description": "矛盾描述",
      "evidence": "证据",
      "source_event_ids": []
    }}
  ],

  "topic_candidates": [
    {{
      "title": "专题名称",
      "reason": "为什么值得形成专题",
      "priority": 1,
      "related_entities": [
        "实体名称"
      ]
    }}
  ]
}}

如果没有足够证据：

knowledge_updates 可以为空；
relationships 可以为空；
knowledge_gaps 可以为空；
contradictions 可以为空；
topic_candidates 可以为空。
"""


# ======================================================================
# Final Merge Prompt
# ======================================================================

def build_merge_prompt(
    date_str: str,
    batch_results: List[Dict[str, Any]],
    report_context: str,
    inventory: str,
    graph: str,
) -> str:

    compact_results = []

    for result in batch_results:

        batch_index = result.get(
            "batch_index"
        )

        raw = result.get(
            "raw",
            ""
        )

        raw = truncate_text(
            raw,
            MAX_BATCH_RESULT_CHARS
        )

        compact_results.append(
            f"""
================ BATCH {batch_index} ================

{raw}
"""
        )

    merged_candidates = "\n".join(
        compact_results
    )

    return f"""
当前处理日期：

{date_str}

你现在负责进行最终 Knowledge Growth Merge。

前面的 Batch AI 已经分别分析了事件。

现在你必须：

1. 合并重复知识；
2. 合并同一实体的多个候选更新；
3. 删除证据不足的 CREATE；
4. 删除重复关系；
5. 判断已有知识应该 UPDATE 还是 SKIP；
6. 检查同一个 EVT-ID 是否被重复计算；
7. 只保留真正有长期价值的知识；
8. 最终输出可直接写入知识系统的结果。

============================================================
当天背景
============================================================

{report_context}

============================================================
已有知识库
============================================================

{inventory}

============================================================
已有知识图谱
============================================================

{graph}

============================================================
Batch AI 候选结果
============================================================

{merged_candidates}

============================================================
最终规则
============================================================

- 同一个 EVT-ID 只能算一次。
- en / zh 同一 EVT-ID 只能算一个事件。
- 已有知识优先 UPDATE。
- 不要因为候选结果中出现 CREATE 就机械 CREATE。
- 必须根据已有知识库重新判断。
- 没有足够证据就 SKIP。
- relationship 必须有证据。
- confidence 必须在 0.0 到 1.0。
- importance / priority 使用 1 到 5。
- source_event_ids 必须来自真实候选结果。
- 不允许创造不存在的 EVT-ID。
- 不允许创建用户个人资料。
- 不要输出 markdown。
- 只输出合法 JSON。

严格输出：

{{
  "knowledge_updates": [
    {{
      "type": "公司|产品|人物|技术|概念|行业|主题",
      "name": "实体名称",
      "action": "create|update|skip",
      "importance": 1,
      "confidence": 0.0,
      "summary": "长期知识摘要",
      "new_facts": [
        "新增事实"
      ],
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "related_entities": [
        {{
          "type": "公司|产品|人物|技术|概念|行业|主题",
          "name": "相关实体"
        }}
      ]
    }}
  ],

  "relationships": [
    {{
      "from_type": "公司|产品|人物|技术|概念|行业|主题",
      "from": "实体A",
      "relation": "关系",
      "to_type": "公司|产品|人物|技术|概念|行业|主题",
      "to": "实体B",
      "evidence": "关系依据",
      "source_event_ids": [
        "EVT-YYYYMMDD-000001"
      ],
      "confidence": 0.0
    }}
  ],

  "knowledge_gaps": [
    {{
      "topic": "知识缺口",
      "reason": "为什么存在缺口",
      "priority": 1,
      "suggested_research": "建议研究方向",
      "source_event_ids": []
    }}
  ],

  "contradictions": [
    {{
      "topic": "可能矛盾",
      "description": "矛盾描述",
      "evidence": "证据",
      "source_event_ids": []
    }}
  ],

  "topic_candidates": [
    {{
      "title": "专题名称",
      "reason": "为什么值得形成专题",
      "priority": 1,
      "related_entities": [
        "实体名称"
      ]
    }}
  ],

  "growth_summary": {{
    "new_knowledge": 0,
    "updated_knowledge": 0,
    "new_relationships": 0,
    "knowledge_gaps": 0,
    "contradictions": 0,
    "topic_candidates": 0
  }}
}}
"""


# ======================================================================
# JSON Normalize
# ======================================================================

def normalize_result(
    data: Dict[str, Any]
) -> Dict[str, Any]:

    result = {
        "knowledge_updates": [],
        "relationships": [],
        "knowledge_gaps": [],
        "contradictions": [],
        "topic_candidates": [],
        "growth_summary": {},
    }

    if not isinstance(
        data,
        dict
    ):
        return result

    for key in result:

        value = data.get(
            key
        )

        if key == "growth_summary":

            if isinstance(
                value,
                dict
            ):

                result[key] = value

        else:

            if isinstance(
                value,
                list
            ):

                result[key] = value

    return result


def valid_knowledge_type(
    value: Any
) -> bool:

    return value in KNOWLEDGE_TYPES


def clean_event_ids(
    value: Any
) -> List[str]:

    if not isinstance(
        value,
        list
    ):
        return []

    result = []

    for item in value:

        if not isinstance(
            item,
            str
        ):
            continue

        matches = re.findall(
            r"EVT-\d{8}-\d+",
            item
        )

        for event_id in matches:

            if event_id not in result:

                result.append(
                    event_id
                )

    return result


# ======================================================================
# 事件 ID 验证
# ======================================================================

def filter_valid_event_ids(
    event_ids: List[str],
    valid_ids: set[str]
) -> List[str]:

    result = []

    for event_id in event_ids:

        if event_id not in valid_ids:
            continue

        if event_id not in result:

            result.append(
                event_id
            )

    return result


def sanitize_result_event_ids(
    result: Dict[str, Any],
    valid_ids: set[str]
) -> Dict[str, Any]:

    for item in result.get(
        "knowledge_updates",
        []
    ):

        if isinstance(
            item,
            dict
        ):

            ids = clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                )
            )

            item[
                "source_event_ids"
            ] = filter_valid_event_ids(
                ids,
                valid_ids
            )

    for item in result.get(
        "relationships",
        []
    ):

        if isinstance(
            item,
            dict
        ):

            ids = clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                )
            )

            item[
                "source_event_ids"
            ] = filter_valid_event_ids(
                ids,
                valid_ids
            )

    for item in result.get(
        "knowledge_gaps",
        []
    ):

        if isinstance(
            item,
            dict
        ):

            ids = clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                )
            )

            item[
                "source_event_ids"
            ] = filter_valid_event_ids(
                ids,
                valid_ids
            )

    for item in result.get(
        "contradictions",
        []
    ):

        if isinstance(
            item,
            dict
        ):

            ids = clean_event_ids(
                item.get(
                    "source_event_ids",
                    []
                )
            )

            item[
                "source_event_ids"
            ] = filter_valid_event_ids(
                ids,
                valid_ids
            )

    return result


# ======================================================================
# 知识资产路径
# ======================================================================

def knowledge_path(
    knowledge_type: str,
    name: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / KNOWLEDGE_TYPE_DIR[
            knowledge_type
        ]
        / (
            safe_filename(name)
            + ".md"
        )
    )


# ======================================================================
# 已有事件检查
# ======================================================================

def event_already_in_file(
    path: Path,
    event_ids: List[str]
) -> bool:

    if not path.exists():
        return False

    text = read_text(
        path
    )

    if not text:
        return False

    for event_id in event_ids:

        if event_id in text:
            return True

    return False


# ======================================================================
# 创建知识
# ======================================================================

def create_knowledge_file(
    path: Path,
    knowledge_type: str,
    name: str,
    date_str: str,
    item: Dict[str, Any],
) -> bool:

    summary = str(
        item.get(
            "summary",
            ""
        )
    ).strip()

    facts = item.get(
        "new_facts",
        []
    )

    if not isinstance(
        facts,
        list
    ):
        facts = []

    event_ids = clean_event_ids(
        item.get(
            "source_event_ids",
            []
        )
    )

    related = item.get(
        "related_entities",
        []
    )

    lines = [
        "---",
        f"type: {knowledge_type}",
        f"name: {name}",
        "status: active",
        f"created_at: {date_str}",
        f"last_updated: {date_str}",
        "---",
        "",
        f"# {name}",
        "",
        "## 核心知识",
        "",
        summary or "待进一步完善。",
        "",
        f"## 知识更新｜{date_str}",
        "",
    ]

    if facts:

        for fact in facts:

            fact = str(
                fact
            ).strip()

            if fact:

                lines.append(
                    f"- {fact}"
                )

        lines.append("")

    if event_ids:

        lines.extend([
            "### 来源 EventUnit",
            "",
        ])

        for event_id in event_ids:

            lines.append(
                f"- `{event_id}`"
            )

        lines.append("")

    if related:

        lines.extend([
            "### 相关实体",
            "",
        ])

        for entity in related:

            if not isinstance(
                entity,
                dict
            ):
                continue

            entity_type = str(
                entity.get(
                    "type",
                    ""
                )
            ).strip()

            entity_name = str(
                entity.get(
                    "name",
                    ""
                )
            ).strip()

            if (
                entity_type
                and entity_name
            ):

                lines.append(
                    f"- {entity_type}："
                    f"{entity_name}"
                )

        lines.append("")

    lines.extend([
        "## 知识生命周期",
        "",
        f"- 首次创建：{date_str}",
        f"- 最近更新：{date_str}",
        "",
    ])

    content = (
        "\n".join(lines)
        .rstrip()
        + "\n"
    )

    atomic_write(
        path,
        content
    )

    return (
        path.exists()
        and path.stat().st_size > 0
    )


# ======================================================================
# 更新知识
# ======================================================================

def update_knowledge_file(
    path: Path,
    date_str: str,
    item: Dict[str, Any],
) -> bool:

    existing = read_text(
        path
    )

    if not existing:
        return False

    event_ids = clean_event_ids(
        item.get(
            "source_event_ids",
            []
        )
    )

    # 防止重复写入
    if event_ids:

        if event_already_in_file(
            path,
            event_ids
        ):

            return False

    facts = item.get(
        "new_facts",
        []
    )

    if not isinstance(
        facts,
        list
    ):
        facts = []

    summary = str(
        item.get(
            "summary",
            ""
        )
    ).strip()

    lines = [
        "",
        f"## 知识更新｜{date_str}",
        "",
    ]

    if summary:

        lines.extend([
            summary,
            "",
        ])

    if facts:

        lines.extend([
            "### 新增事实",
            "",
        ])

        for fact in facts:

            fact = str(
                fact
            ).strip()

            if fact:

                lines.append(
                    f"- {fact}"
                )

        lines.append("")

    if event_ids:

        lines.extend([
            "### 来源 EventUnit",
            "",
        ])

        for event_id in event_ids:

            lines.append(
                f"- `{event_id}`"
            )

        lines.append("")

    new_content = (
        existing.rstrip()
        + "\n"
        + "\n".join(lines)
        + "\n"
    )

    new_content = re.sub(
        r"^last_updated:\s*.*$",
        f"last_updated: {date_str}",
        new_content,
        count=1,
        flags=re.MULTILINE,
    )

    atomic_write(
        path,
        new_content
    )

    return True


# ======================================================================
# 写入知识图谱
# ======================================================================

def graph_path(
    date_str: str
) -> Path:

    year, month, _ = date_str.split("-")

    return (
        GRAPH_DIR
        / year
        / month
        / f"{date_str}.md"
    )


def append_relationships(
    date_str: str,
    relationships: List[Dict[str, Any]]
) -> int:

    if not relationships:
        return 0

    path = graph_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识图谱关系｜{date_str}\n\n"
        )

    added = 0

    seen_keys = set()

    for rel in relationships:

        if not isinstance(
            rel,
            dict
        ):
            continue

        from_name = str(
            rel.get(
                "from",
                ""
            )
        ).strip()

        relation = str(
            rel.get(
                "relation",
                ""
            )
        ).strip()

        to_name = str(
            rel.get(
                "to",
                ""
            )
        ).strip()

        if not (
            from_name
            and relation
            and to_name
        ):
            continue

        from_type = str(
            rel.get(
                "from_type",
                ""
            )
        ).strip()

        to_type = str(
            rel.get(
                "to_type",
                ""
            )
        ).strip()

        if not valid_knowledge_type(
            from_type
        ):
            continue

        if not valid_knowledge_type(
            to_type
        ):
            continue

        evidence = str(
            rel.get(
                "evidence",
                ""
            )
        ).strip()

        event_ids = clean_event_ids(
            rel.get(
                "source_event_ids",
                []
            )
        )

        relation_key = (
            f"{from_type}:{from_name}"
            f"→{relation}→"
            f"{to_type}:{to_name}"
        )

        if relation_key in seen_keys:
            continue

        seen_keys.add(
            relation_key
        )

        if relation_key in existing:
            continue

        lines = [
            f"- **{from_name}**"
            f"（{from_type}）"
            f" → **{relation}** → "
            f"**{to_name}**"
            f"（{to_type}）"
        ]

        if evidence:

            lines.append(
                f"  - 依据：{evidence}"
            )

        if event_ids:

            lines.append(
                "  - 来源："
                + "、".join(
                    f"`{x}`"
                    for x in event_ids
                )
            )

        lines.append("")

        existing += (
            "\n".join(lines)
            + "\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 专题候选
# ======================================================================

def topic_candidate_path(
    date_str: str
) -> Path:

    year, _, _ = date_str.split("-")

    return (
        TOPIC_DIR
        / year
        / "候选专题"
        / f"{date_str}.md"
    )


def append_topic_candidates(
    date_str: str,
    candidates: List[Dict[str, Any]]
) -> int:

    if not candidates:
        return 0

    path = topic_candidate_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 专题候选｜{date_str}\n\n"
            "> 本文件记录值得进一步研究的专题方向，不等于正式专题报告。\n\n"
        )

    added = 0

    seen_titles = set()

    for item in candidates:

        if not isinstance(
            item,
            dict
        ):
            continue

        title = str(
            item.get(
                "title",
                ""
            )
        ).strip()

        reason = str(
            item.get(
                "reason",
                ""
            )
        ).strip()

        priority = item.get(
            "priority",
            1
        )

        entities = item.get(
            "related_entities",
            []
        )

        if not title:
            continue

        if title in seen_titles:
            continue

        seen_titles.add(
            title
        )

        if title in existing:
            continue

        if not isinstance(
            entities,
            list
        ):
            entities = []

        entity_text = "、".join(
            str(x).strip()
            for x in entities
            if str(x).strip()
        )

        existing += (
            f"## {title}\n\n"
            f"- 优先级：{priority}\n"
            f"- 形成原因：{reason}\n"
        )

        if entity_text:

            existing += (
                f"- 相关实体："
                f"{entity_text}\n"
            )

        existing += "\n"

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 知识缺口
# ======================================================================

def gap_path(
    date_str: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / "主题"
        / "知识缺口"
        / f"{date_str}.md"
    )


def append_gaps(
    date_str: str,
    gaps: List[Dict[str, Any]]
) -> int:

    if not gaps:
        return 0

    path = gap_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识缺口｜{date_str}\n\n"
        )

    added = 0

    seen_topics = set()

    for gap in gaps:

        if not isinstance(
            gap,
            dict
        ):
            continue

        topic = str(
            gap.get(
                "topic",
                ""
            )
        ).strip()

        reason = str(
            gap.get(
                "reason",
                ""
            )
        ).strip()

        priority = gap.get(
            "priority",
            1
        )

        research = str(
            gap.get(
                "suggested_research",
                ""
            )
        ).strip()

        if not topic:
            continue

        if topic in seen_topics:
            continue

        seen_topics.add(
            topic
        )

        marker = (
            f"## {topic}"
        )

        if marker in existing:
            continue

        existing += (
            f"{marker}\n\n"
            f"- 优先级：{priority}\n"
            f"- 缺口原因：{reason}\n"
            f"- 建议研究：{research}\n\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 矛盾记录
# ======================================================================

def contradiction_path(
    date_str: str
) -> Path:

    return (
        KNOWLEDGE_DIR
        / "主题"
        / "知识矛盾"
        / f"{date_str}.md"
    )


def append_contradictions(
    date_str: str,
    contradictions: List[Dict[str, Any]]
) -> int:

    if not contradictions:
        return 0

    path = contradiction_path(
        date_str
    )

    existing = read_text(
        path
    )

    if not existing:

        existing = (
            f"# 知识矛盾待核查｜{date_str}\n\n"
            "> 这里记录待验证的潜在矛盾，不代表系统已经判定事实冲突。\n\n"
        )

    added = 0

    seen_topics = set()

    for item in contradictions:

        if not isinstance(
            item,
            dict
        ):
            continue

        topic = str(
            item.get(
                "topic",
                ""
            )
        ).strip()

        description = str(
            item.get(
                "description",
                ""
            )
        ).strip()

        evidence = str(
            item.get(
                "evidence",
                ""
            )
        ).strip()

        if not topic:
            continue

        if topic in seen_topics:
            continue

        seen_topics.add(
            topic
        )

        marker = (
            f"## {topic}"
        )

        if marker in existing:
            continue

        existing += (
            f"{marker}\n\n"
            f"- 矛盾描述："
            f"{description}\n"
            f"- 证据："
            f"{evidence}\n\n"
        )

        added += 1

    if added:

        atomic_write(
            path,
            existing.rstrip()
            + "\n"
        )

    return added


# ======================================================================
# 运行状态
# ======================================================================

def complete_marker(
    date_str: str
) -> Path:

    return (
        SYSTEM_LOG_DIR
        / f"{date_str}_COMPLETE"
    )


def write_run_state(
    date_str: str,
    state: Dict[str, Any]
) -> None:

    ensure_dir(
        SYSTEM_LOG_DIR
    )

    marker = complete_marker(
        date_str
    )

    content = json.dumps(
        state,
        ensure_ascii=False,
        indent=2
    )

    atomic_write(
        marker,
        content
    )


# ======================================================================
# Batch AI
# ======================================================================

def run_batch_analysis(
    date_str: str,
    batch_index: int,
    total_batches: int,
    events: List[Tuple[str, str]],
    report_context: str,
    inventory: str,
    graph: str,
) -> Dict[str, Any]:

    log("")
    log(
        "------------------------------------------------------------"
    )

    log(
        f"🧠 BATCH {batch_index}/{total_batches}"
    )

    log(
        f"   EVENTS : {len(events)}"
    )

    log(
        "   IDS    : "
        + ", ".join(
            event_id
            for event_id, _ in events
        )
    )

    prompt = build_batch_prompt(
        date_str,
        batch_index,
        total_batches,
        events,
        report_context,
        inventory,
        graph
    )

    raw = call_ai(
        SYSTEM_PROMPT,
        prompt
    )

    try:

        data = extract_json(
            raw
        )

    except Exception as exc:

        log(
            f"❌ BATCH JSON ERROR | "
            f"{exc}"
        )

        log(
            "   RAW OUTPUT:"
        )

        log(
            truncate_text(
                raw,
                5000
            )
        )

        raise

    result = normalize_result(
        data
    )

    return {
        "batch_index": batch_index,
        "event_ids": [
            event_id
            for event_id, _ in events
        ],
        "raw": raw,
        "result": result,
    }


# ======================================================================
# Final Merge AI
# ======================================================================

def run_final_merge(
    date_str: str,
    batch_results: List[Dict[str, Any]],
    report_context: str,
    inventory: str,
    graph: str,
) -> Dict[str, Any]:

    log("")
    log(
        "============================================================"
    )

    log(
        "🧠 FINAL KNOWLEDGE MERGE"
    )

    prompt = build_merge_prompt(
        date_str,
        batch_results,
        report_context,
        inventory,
        graph
    )

    raw = call_ai(
        SYSTEM_PROMPT,
        prompt
    )

    try:

        data = extract_json(
            raw
        )

    except Exception as exc:

        log(
            f"❌ FINAL MERGE JSON ERROR | "
            f"{exc}"
        )

        log(
            "   RAW OUTPUT:"
        )

        log(
            truncate_text(
                raw,
                8000
            )
        )

        raise

    return normalize_result(
        data
    )


# ======================================================================
# 单日处理
# ======================================================================

def process_date(
    date_str: str
) -> Dict[str, Any]:

    log("")
    log(
        "=" * 72
    )

    log(
        f"KNOWLEDGE GROWTH | {date_str}"
    )

    log(
        "=" * 72
    )

    marker = complete_marker(
        date_str
    )

    if marker.exists():

        log(
            f"⏭️ SKIP | "
            f"{date_str} 已完成"
        )

        return {
            "date": date_str,
            "status": "already_complete",
        }

    # --------------------------------------------------------------
    # Task 4 Analysis
    # --------------------------------------------------------------

    analysis_files = find_analysis_files(
        date_str
    )

    log(
        f"Task 4 Analysis : "
        f"{len(analysis_files)}"
    )

    if not analysis_files:

        log(
            "⚠️ 没有 Task 4 Analysis，"
            "本日不标记 COMPLETE"
        )

        return {
            "date": date_str,
            "status": "no_input",
        }

    # --------------------------------------------------------------
    # EVT-ID 去重
    # --------------------------------------------------------------

    event_records = build_event_records(
        analysis_files
    )

    event_ids = [
        event_id
        for event_id, _ in event_records
    ]

    log(
        f"Unique Event IDs  : "
        f"{len(event_ids)}"
    )

    if not event_records:

        log(
            "⚠️ 没有有效 Event Analysis"
        )

        return {
            "date": date_str,
            "status": "no_valid_events",
        }

    # --------------------------------------------------------------
    # 分批
    # --------------------------------------------------------------

    batches = build_batches(
        event_records
    )

    log(
        f"AI Batches        : "
        f"{len(batches)}"
    )

    for index, batch in enumerate(
        batches,
        start=1
    ):

        chars = sum(
            len(text)
            for _, text in batch
        )

        log(
            f"   Batch {index:02d} | "
            f"events={len(batch)} | "
            f"chars={chars:,}"
        )

    # --------------------------------------------------------------
    # 当前知识库
    # --------------------------------------------------------------

    inventory = knowledge_inventory()

    graph = graph_inventory()

    log(
        f"Knowledge Files   : "
        f"{len(knowledge_files())}"
    )

    log(
        f"Knowledge Context : "
        f"{len(inventory):,} chars"
    )

    log(
        f"Graph Context     : "
        f"{len(graph):,} chars"
    )

    # --------------------------------------------------------------
    # 日报 / 周报 / 专题
    # --------------------------------------------------------------

    report_context = build_report_context(
        date_str
    )

    log(
        f"Report Context    : "
        f"{len(report_context):,} chars"
    )

    # --------------------------------------------------------------
    # Batch AI
    # --------------------------------------------------------------

    batch_results = []

    total_batches = len(
        batches
    )

    for batch_index, batch in enumerate(
        batches,
        start=1
    ):

        result = run_batch_analysis(
            date_str,
            batch_index,
            total_batches,
            batch,
            report_context,
            inventory,
            graph
        )

        batch_results.append(
            result
        )

        if batch_index < total_batches:

            time.sleep(
                AI_THROTTLE_SECONDS
            )

    # --------------------------------------------------------------
    # 最终 Merge
    # --------------------------------------------------------------

    final_result = run_final_merge(
        date_str,
        batch_results,
        report_context,
        inventory,
        graph
    )

    # --------------------------------------------------------------
    # 严格验证 Event IDs
    # --------------------------------------------------------------

    valid_ids = set(
        event_ids
    )

    final_result = (
        sanitize_result_event_ids(
            final_result,
            valid_ids
        )
    )

    # --------------------------------------------------------------
    # 统计
    # --------------------------------------------------------------

    created = 0
    updated = 0
    skipped = 0

    # --------------------------------------------------------------
    # 知识资产
    # --------------------------------------------------------------

    for item in final_result[
        "knowledge_updates"
    ]:

        if not isinstance(
            item,
            dict
        ):
            continue

        knowledge_type = str(
            item.get(
                "type",
                ""
            )
        ).strip()

        name = str(
            item.get(
                "name",
                ""
            )
        ).strip()

        action = str(
            item.get(
                "action",
                "skip"
            )
        ).strip().lower()

        confidence = item.get(
            "confidence",
            0
        )

        try:

            confidence = float(
                confidence
            )

        except Exception:

            confidence = 0.0

        if not valid_knowledge_type(
            knowledge_type
        ):
            continue

        if not name:
            continue

        if (
            confidence < 0.5
            and action != "skip"
        ):

            log(
                f"⏭️ LOW CONFIDENCE | "
                f"{knowledge_type} | "
                f"{name}"
            )

            skipped += 1

            continue

        path = knowledge_path(
            knowledge_type,
            name
        )

        if action == "create":

            if path.exists():

                changed = (
                    update_knowledge_file(
                        path,
                        date_str,
                        item
                    )
                )

                if changed:

                    updated += 1

                else:

                    skipped += 1

            else:

                if create_knowledge_file(
                    path,
                    knowledge_type,
                    name,
                    date_str,
                    item
                ):

                    created += 1

        elif action == "update":

            if path.exists():

                changed = (
                    update_knowledge_file(
                        path,
                        date_str,
                        item
                    )
                )

                if changed:

                    updated += 1

                else:

                    skipped += 1

            else:

                if create_knowledge_file(
                    path,
                    knowledge_type,
                    name,
                    date_str,
                    item
                ):

                    created += 1

        else:

            skipped += 1

    # --------------------------------------------------------------
    # 知识图谱
    # --------------------------------------------------------------

    relationships_added = (
        append_relationships(
            date_str,
            final_result[
                "relationships"
            ]
        )
    )

    # --------------------------------------------------------------
    # 知识缺口
    # --------------------------------------------------------------

    gaps_added = append_gaps(
        date_str,
        final_result[
            "knowledge_gaps"
        ]
    )

    # --------------------------------------------------------------
    # 矛盾
    # --------------------------------------------------------------

    contradictions_added = (
        append_contradictions(
            date_str,
            final_result[
                "contradictions"
            ]
        )
    )

    # --------------------------------------------------------------
    # 专题候选
    # --------------------------------------------------------------

    topic_candidates_added = (
        append_topic_candidates(
            date_str,
            final_result[
                "topic_candidates"
            ]
        )
    )

    # --------------------------------------------------------------
    # 状态
    # --------------------------------------------------------------

    state = {
        "date": date_str,
        "status": "complete",
        "engine": "V3.1",
        "processed_analysis_files": len(
            analysis_files
        ),
        "unique_event_ids": len(
            event_ids
        ),
        "ai_batches": len(
            batches
        ),
        "batch_max_events":
            BATCH_MAX_EVENTS,
        "batch_max_chars":
            BATCH_MAX_CHARS,
        "knowledge_created": created,
        "knowledge_updated": updated,
        "knowledge_skipped": skipped,
        "relationships_added":
            relationships_added,
        "knowledge_gaps_added":
            gaps_added,
        "contradictions_added":
            contradictions_added,
        "topic_candidates_added":
            topic_candidates_added,
        "finished_at":
            now_local().isoformat(),
    }

    # --------------------------------------------------------------
    # 只有所有 AI + 写入全部成功后
    # 才生成 COMPLETE
    # --------------------------------------------------------------

    write_run_state(
        date_str,
        state
    )

    log("")
    log(
        f"✅ KNOWLEDGE GROWTH COMPLETE | "
        f"{date_str}"
    )

    log(
        f"   CREATED       : {created}"
    )

    log(
        f"   UPDATED       : {updated}"
    )

    log(
        f"   SKIPPED       : {skipped}"
    )

    log(
        f"   RELATIONSHIPS : "
        f"{relationships_added}"
    )

    log(
        f"   GAPS          : "
        f"{gaps_added}"
    )

    log(
        f"   CONTRADICTION : "
        f"{contradictions_added}"
    )

    log(
        f"   TOPIC         : "
        f"{topic_candidates_added}"
    )

    return state


# ======================================================================
# Main
# ======================================================================

def main() -> None:

    log("")
    log(
        "#" * 72
    )

    log(
        "748686 自生长知识系统"
    )

    log(
        "KNOWLEDGE GROWTH ENGINE V3.1"
    )

    log(
        "#" * 72
    )

    log(
        f"ROOT     : {ROOT}"
    )

    log(
        f"TIMEZONE : {TIMEZONE}"
    )

    log(
        f"DATE     : {today_str()}"
    )

    log(
        f"AI MODEL : {AGNES_MODEL}"
    )

    log(
        f"AI URL   : "
        f"{AGNES_BASE_URL}/chat/completions"
    )

    log(
        f"BATCH EVENTS : "
        f"{BATCH_MAX_EVENTS}"
    )

    log(
        f"BATCH CHARS  : "
        f"{BATCH_MAX_CHARS:,}"
    )

    if not AGNES_API_KEY:

        raise RuntimeError(
            "未设置 AGNES_API_KEY"
        )

    dates = target_dates()

    log(
        "TARGET DATES:"
    )

    for date_str in dates:

        log(
            f"  - {date_str}"
        )

    results = []

    # 严格按日期顺序
    for date_index, date_str in enumerate(
        dates
    ):

        result = process_date(
            date_str
        )

        results.append(
            result
        )

        if date_index < len(dates) - 1:

            time.sleep(
                AI_THROTTLE_SECONDS
            )

    log("")
    log(
        "#" * 72
    )

    log(
        "KNOWLEDGE GROWTH FINISHED"
    )

    log(
        "#" * 72
    )

    for result in results:

        log(
            f"{result.get('date')} "
            f"| {result.get('status')}"
        )


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    main()
