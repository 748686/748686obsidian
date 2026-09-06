#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Growth Engine V3.0

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
本程序职责
======================================================================

1. 检查 08_知识库 的知识资产质量
2. 检查 09_知识图谱 的关系质量
3. 参考最近日报、周报、专题报告
4. 判断：
      - 哪些知识需要更新
      - 哪些知识重复
      - 哪些知识存在冲突
      - 哪些实体之间存在新关系
      - 哪些知识存在缺口
      - 哪些内容值得形成专题
5. 将真正的知识增长结果写入：

      08_知识库/
      09_知识图谱/
      07_专题报告/     ← 仅记录值得形成专题的候选

6. 只将程序运行状态写入：

      00_System/运行日志/knowledge_growth/

======================================================================
明确禁止
======================================================================

❌ 不向 00_System 写知识成果
❌ 不向 00_System 写知识分析报告
❌ 不向 00_System 写专题报告
❌ 不修改 Task 4
❌ 不修改 Raw News
❌ 不自动修改 10_用户资料
❌ 不把所有新闻机械复制进知识库
❌ 不把每一次运行都重复追加同一条知识

======================================================================
时间
======================================================================

固定使用 Asia/Shanghai
======================================================================
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

AGNES_API_KEY = os.getenv("AGNES_API_KEY")

AI_TIMEOUT = int(
    os.getenv("KNOWLEDGE_GROWTH_TIMEOUT", "180")
)

AI_RETRIES = int(
    os.getenv("KNOWLEDGE_GROWTH_RETRIES", "3")
)

AI_THROTTLE_SECONDS = float(
    os.getenv("KNOWLEDGE_GROWTH_THROTTLE", "1.2")
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
    path.mkdir(parents=True, exist_ok=True)


def sha256_text(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def safe_filename(name: str) -> str:
    """
    知识实体名称 → 安全 Markdown 文件名
    """
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


def atomic_write(path: Path, content: str) -> None:
    ensure_dir(path.parent)

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


# ======================================================================
# AI 调用
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
                    "utf-8"
                )

            data = json.loads(raw)

            content = (
                data
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not content:
                raise RuntimeError(
                    "AI 返回内容为空"
                )

            return content.strip()

        except Exception as exc:

            last_error = exc

            log(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

    raise RuntimeError(
        f"AI 请求失败: {last_error}"
    )


# ======================================================================
# JSON 提取
# ======================================================================

def extract_json(text: str) -> Dict[str, Any]:

    text = text.strip()

    # 去掉 markdown code fence
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
        value = json.loads(text)

        if isinstance(value, dict):
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

            if isinstance(value, dict):
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

    # 严格只使用小写 en / zh
    for language in ("en", "zh"):

        directory = (
            base
            / language
            / "event_units"
        )

        if not directory.exists():
            continue

        for path in sorted(
            directory.glob("*_analysis.md")
        ):

            if path.is_file():

                try:
                    if path.stat().st_size <= 0:
                        continue
                except Exception:
                    continue

                result.append(path)

    return result


def extract_event_id(path: Path) -> str:

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


def load_analysis(
    paths: List[Path]
) -> str:

    chunks = []

    for path in paths:

        content = read_text(path)

        if not content.strip():
            continue

        event_id = extract_event_id(
            path
        )

        language = (
            "en"
            if "/en/" in path.as_posix()
            else "zh"
        )

        chunks.append(
            "\n".join([
                "==================================================",
                f"EVENT_ID: {event_id}",
                f"LANGUAGE: {language}",
                f"FILE: {path.relative_to(ROOT)}",
                "==================================================",
                content,
            ])
        )

    return "\n\n".join(chunks)


# ======================================================================
# 日报 / 周报 / 专题报告
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


def build_context(
    date_str: str,
    analysis_text: str,
) -> str:

    sections = []

    daily = find_daily_report(
        date_str
    )

    if daily:

        sections.append(
            "================ 日报 ================\n"
            + read_text(daily)
        )

    weekly_files = (
        find_recent_weekly_reports()
    )

    if weekly_files:

        weekly_text = []

        for path in weekly_files:
            weekly_text.append(
                f"\n--- {path.relative_to(ROOT)} ---\n"
                + read_text(path)
            )

        sections.append(
            "================ 最近周报 ================\n"
            + "\n".join(weekly_text)
        )

    topic_files = (
        find_recent_topic_reports()
    )

    if topic_files:

        topic_text = []

        for path in topic_files:

            topic_text.append(
                f"\n--- {path.relative_to(ROOT)} ---\n"
                + read_text(path)
            )

        sections.append(
            "================ 最近专题 ================\n"
            + "\n".join(topic_text)
        )

    sections.append(
        "================ Task 4 全部分析 ================\n"
        + analysis_text
    )

    return "\n\n".join(sections)


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
            nonempty_files(directory)
        )

    return result


def knowledge_inventory(
    max_chars_per_file: int = 6000
) -> str:

    files = knowledge_files()

    chunks = []

    for path in files:

        text = read_text(path)

        if not text.strip():
            continue

        if len(text) > max_chars_per_file:
            text = text[
                :max_chars_per_file
            ]

        chunks.append(
            "\n".join([
                "--------------------------------------------------",
                f"FILE: {path.relative_to(ROOT)}",
                "--------------------------------------------------",
                text,
            ])
        )

    return "\n\n".join(chunks)


def graph_inventory(
    max_chars: int = 30000
) -> str:

    files = nonempty_files(
        GRAPH_DIR
    )

    chunks = []

    total = 0

    for path in files:

        text = read_text(path)

        if not text.strip():
            continue

        block = (
            f"\n--- {path.relative_to(ROOT)} ---\n"
            + text
        )

        if (
            total
            + len(block)
            > max_chars
        ):
            break

        chunks.append(block)

        total += len(block)

    return "\n".join(chunks)


# ======================================================================
# Prompt
# ======================================================================

SYSTEM_PROMPT = """
你是一个长期运行的知识库成长引擎。

你的任务不是写新闻摘要。

你的任务是：

从当天全部 Task 4 Event Analysis、日报、周报、专题报告、
已有知识库和已有知识图谱中判断：

1. 什么信息值得成为长期知识；
2. 什么已有知识应该更新；
3. 哪些知识重复；
4. 哪些知识之间存在新的可靠关系；
5. 哪些地方存在知识缺口；
6. 哪些地方存在潜在矛盾；
7. 哪些问题值得后续研究；
8. 哪些方向值得形成专题。

必须遵守：

- 不编造事实；
- 不因为新闻出现一次就创建知识资产；
- 优先处理具有长期价值的信息；
- 同一个事件的 en 和 zh Analysis 是同一个事件，不得重复计算；
- 已有知识优先 UPDATE，而不是 CREATE；
- 只有证据不足时才进入 knowledge_gaps；
- 不把普通新闻事实强行变成长期知识；
- 关系必须有证据；
- 不推断用户个人信息；
- 不产生任何 10_用户资料内容；
- 输出必须是合法 JSON；
- 不要输出 markdown；
- 不要输出解释文字。
"""


def build_growth_prompt(
    date_str: str,
    context: str,
    inventory: str,
    graph: str,
) -> str:

    return f"""
当前处理日期：

{date_str}

下面是当天及已有知识上下文。

========================
上下文
========================

{context}

========================
已有知识库
========================

{inventory}

========================
已有知识图谱
========================

{graph}

请进行一次“知识系统成长分析”。

请严格输出以下 JSON：

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
      "reason": "为什么认为存在缺口",
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

重要：

如果没有足够证据，不要 CREATE。

如果已有知识已经包含该信息，不要重复 UPDATE。

同一个 EVT-ID 即使同时出现在 en 和 zh 中，也只能算一个事件来源。
"""


# ======================================================================
# JSON 验证
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

    for key in result:

        value = data.get(key)

        if key == "growth_summary":

            if isinstance(value, dict):
                result[key] = value

        else:

            if isinstance(value, list):
                result[key] = value

    return result


def valid_knowledge_type(
    value: Any
) -> bool:

    return value in KNOWLEDGE_TYPES


def clean_event_ids(
    value: Any
) -> List[str]:

    if not isinstance(value, list):
        return []

    result = []

    for item in value:

        if not isinstance(item, str):
            continue

        match = re.search(
            r"EVT-\d{8}-\d+",
            item
        )

        if match:
            event_id = match.group(0)

            if event_id not in result:
                result.append(
                    event_id
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

    text = read_text(path)

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
        item.get("summary", "")
    ).strip()

    facts = item.get(
        "new_facts",
        []
    )

    if not isinstance(facts, list):
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
                    f"- {entity_type}：{entity_name}"
                )

        lines.append("")

    lines.extend([
        "## 知识生命周期",
        "",
        f"- 首次创建：{date_str}",
        f"- 最近更新：{date_str}",
        "",
    ])

    content = "\n".join(
        lines
    ).rstrip() + "\n"

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

    existing = read_text(path)

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

        lines.append(
            "### 新增事实"
        )

        lines.append("")

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

    # 更新 frontmatter 的 last_updated
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

    existing = read_text(path)

    if not existing:

        existing = (
            f"# 知识图谱关系｜{date_str}\n\n"
        )

    added = 0

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

        # 去重
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

    existing = read_text(path)

    if not existing:

        existing = (
            f"# 专题候选｜{date_str}\n\n"
            "> 本文件记录值得进一步研究的专题方向，不等于正式专题报告。\n\n"
        )

    added = 0

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
                f"- 相关实体：{entity_text}\n"
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

    existing = read_text(path)

    if not existing:

        existing = (
            f"# 知识缺口｜{date_str}\n\n"
        )

    added = 0

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

    existing = read_text(path)

    if not existing:

        existing = (
            f"# 知识矛盾待核查｜{date_str}\n\n"
            "> 这里记录待验证的潜在矛盾，不代表系统已经判定事实冲突。\n\n"
        )

    added = 0

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

        marker = (
            f"## {topic}"
        )

        if marker in existing:
            continue

        existing += (
            f"{marker}\n\n"
            f"- 矛盾描述：{description}\n"
            f"- 证据：{evidence}\n\n"
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
# 单日处理
# ======================================================================

def process_date(
    date_str: str
) -> Dict[str, Any]:

    log("")
    log("=" * 72)
    log(
        f"KNOWLEDGE GROWTH | {date_str}"
    )
    log("=" * 72)

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
    # 去重事件
    # --------------------------------------------------------------

    event_ids = []

    for path in analysis_files:

        event_id = extract_event_id(
            path
        )

        if event_id not in event_ids:
            event_ids.append(
                event_id
            )

    log(
        f"Unique Event IDs  : "
        f"{len(event_ids)}"
    )

    # --------------------------------------------------------------
    # 加载全部 Analysis
    # --------------------------------------------------------------

    analysis_text = load_analysis(
        analysis_files
    )

    context = build_context(
        date_str,
        analysis_text
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

    # --------------------------------------------------------------
    # AI
    # --------------------------------------------------------------

    prompt = build_growth_prompt(
        date_str,
        context,
        inventory,
        graph
    )

    log(
        "🧠 AI KNOWLEDGE GROWTH"
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
            f"❌ JSON ERROR | {exc}"
        )

        raise

    result = normalize_result(
        data
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

    for item in result[
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

                changed = update_knowledge_file(
                    path,
                    date_str,
                    item
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

                changed = update_knowledge_file(
                    path,
                    date_str,
                    item
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
            result[
                "relationships"
            ]
        )
    )

    # --------------------------------------------------------------
    # 知识缺口
    # --------------------------------------------------------------

    gaps_added = append_gaps(
        date_str,
        result[
            "knowledge_gaps"
        ]
    )

    # --------------------------------------------------------------
    # 矛盾
    # --------------------------------------------------------------

    contradictions_added = (
        append_contradictions(
            date_str,
            result[
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
            result[
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
        "processed_analysis_files": len(
            analysis_files
        ),
        "unique_event_ids": len(
            event_ids
        ),
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
    log("#" * 72)
    log(
        "748686 自生长知识系统"
    )
    log(
        "KNOWLEDGE GROWTH ENGINE V3.0"
    )
    log("#" * 72)

    log(
        f"ROOT     : {ROOT}"
    )

    log(
        f"TIMEZONE : {TIMEZONE}"
    )

    log(
        f"DATE     : {today_str()}"
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
    for date_str in dates:

        result = process_date(
            date_str
        )

        results.append(
            result
        )

        # 日期之间稍微节流
        time.sleep(
            AI_THROTTLE_SECONDS
        )

    log("")
    log("#" * 72)
    log(
        "KNOWLEDGE GROWTH FINISHED"
    )
    log("#" * 72)

    for result in results:

        log(
            f"{result.get('date')} "
            f"| {result.get('status')}"
        )


if __name__ == "__main__":
    main()
