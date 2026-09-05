#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Asset Compiler V1.0

======================================================================
职责
======================================================================

将 Task 4 Event Analysis 编译为长期知识资产。

输入：

    Raw News/
        YYYY-MM-DD-EventUnit/
            en/
                event_units/
                    *_analysis.md

            zh/
                event_units/
                    *_analysis.md

    05_日报/
        YYYY/MM/YYYY-MM-DD.md

输出：

    01_新闻/
        YYYY/MM/YYYY-MM-DD-新闻资产索引.md

    02_资料/
        YYYY/MM/YYYY-MM-DD-资料索引.md

    03_文章/
        YYYY/MM/YYYY-MM-DD-文章候选.md

    04_图片/
        YYYY/MM/YYYY-MM-DD-图片索引.md

    07_专题报告/
        YYYY/MM/YYYY-MM/YYYY-MM-DD-专题候选.md

    08_知识库/
        主题/
        产品/
        人物/
        公司/
        技术/
        概念/
        行业/

    09_知识图谱/
        YYYY/MM/YYYY-MM-DD-关系图谱.md

    00_System/
        运行日志/
            knowledge_asset/
                YYYY-MM-DD_COMPLETE

======================================================================
核心思想
======================================================================

不是：

    新闻
      ↓
    复制成知识卡片

而是：

    Event Analysis
          ↓
    判断长期价值
          ↓
    提取实体
          ↓
    提取事实
          ↓
    提取关系
          ↓
    判断 CREATE / UPDATE / SKIP
          ↓
    写入知识库
          ↓
    建立知识图谱

======================================================================
重要规则
======================================================================

1. 严格使用小写 en / zh。
2. 不修改 Task 3。
3. 不修改 Task 4。
4. 不删除已有知识。
5. 不覆盖已有知识中的历史内容。
6. 更新知识时采用追加方式。
7. 不把推测写成事实。
8. AI 输出必须是 JSON。
9. AI JSON 失败会重试。
10. 日期处理使用 Asia/Shanghai。
11. 每一天独立处理。
12. 一天成功后立即落盘。
13. 已完成日期直接跳过。
14. 中途失败不会写 COMPLETE。
15. 10_用户资料绝不由新闻自动生成。
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# ROOT
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]


# ======================================================================
# 输入
# ======================================================================

RAW_NEWS = ROOT / "Raw News"

DAILY = ROOT / "05_日报"


# ======================================================================
# 输出
# ======================================================================

NEWS = ROOT / "01_新闻"

MATERIALS = ROOT / "02_资料"

ARTICLES = ROOT / "03_文章"

IMAGES = ROOT / "04_图片"

TOPICS = ROOT / "07_专题报告"

KNOWLEDGE = ROOT / "08_知识库"

GRAPH = ROOT / "09_知识图谱"


# ======================================================================
# 状态
# ======================================================================

SYSTEM_LOG = (
    ROOT
    / "00_System"
    / "运行日志"
    / "knowledge_asset"
)


# ======================================================================
# 时区
# ======================================================================

TIMEZONE = timezone(
    timedelta(hours=8)
)


# ======================================================================
# AI
# ======================================================================

AI_BASE_URL = os.getenv(
    "AI_BASE_URL",
    "https://api.openai.com/v1"
).rstrip("/")


AI_MODEL = os.getenv(
    "AI_MODEL",
    ""
)


AI_API_KEY = os.getenv(
    "AI_API_KEY",
    ""
)


AI_TIMEOUT = 180

AI_RETRIES = 5

AI_RETRY_BASE = 5

AI_THROTTLE_SECONDS = 1.2


# ======================================================================
# 知识类型
# ======================================================================

KNOWLEDGE_TYPES = (
    "主题",
    "产品",
    "人物",
    "公司",
    "技术",
    "概念",
    "行业",
)


# ======================================================================
# 时间
# ======================================================================

def now() -> datetime:

    return datetime.now(
        TIMEZONE
    )


# ======================================================================
# 文件判断
# ======================================================================

def is_nonempty_file(
    path: Path
) -> bool:

    try:

        return (
            path.is_file()
            and path.stat().st_size > 0
        )

    except Exception:

        return False


# ======================================================================
# 安全文件名
# ======================================================================

def safe_filename(
    name: str
) -> str:

    name = str(name).strip()

    if not name:

        return "未命名"

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

    return name[:120]


# ======================================================================
# AI
# ======================================================================

def call_ai(
    prompt: str
) -> str:

    if not AI_API_KEY:

        raise RuntimeError(
            "缺少环境变量 AI_API_KEY"
        )

    if not AI_MODEL:

        raise RuntimeError(
            "缺少环境变量 AI_MODEL"
        )

    payload = json.dumps(
        {
            "model": AI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": """
你是748686自生长知识系统的知识资产编译器。

你的任务不是写新闻摘要。

你的任务是从 Event Analysis 中识别：

1. 值得长期保存的知识
2. 人物
3. 公司
4. 产品
5. 技术
6. 概念
7. 行业
8. 主题
9. 新事实
10. 新关系
11. 值得深入研究的问题

严格依据输入。

不得编造。

不得使用输入之外的事实。

不确定时降低 confidence。

如果没有长期价值，可以 SKIP。

必须返回合法 JSON。

不要输出 Markdown。

不要输出 ```json。

只输出 JSON。
""".strip(),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.1,
        },
        ensure_ascii=False,
    ).encode("utf-8")

    last_error = None

    for attempt in range(
        1,
        AI_RETRIES + 1
    ):

        try:

            if AI_THROTTLE_SECONDS > 0:

                time.sleep(
                    AI_THROTTLE_SECONDS
                )

            request = Request(
                AI_BASE_URL
                + "/chat/completions",
                data=payload,
                headers={
                    "Authorization":
                        "Bearer "
                        + AI_API_KEY,
                    "Content-Type":
                        "application/json",
                },
                method="POST",
            )

            with urlopen(
                request,
                timeout=AI_TIMEOUT
            ) as response:

                raw = (
                    response
                    .read()
                    .decode(
                        "utf-8",
                        errors="replace"
                    )
                )

            data = json.loads(
                raw
            )

            result = (
                data
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
            )

            if not result.strip():

                raise RuntimeError(
                    "AI 返回空内容"
                )

            return result.strip()

        except Exception as exc:

            last_error = exc

            print(
                f"⚠️ AI RETRY "
                f"{attempt}/{AI_RETRIES}"
            )

            print(
                f"   {type(exc).__name__}: "
                f"{exc}"
            )

            if attempt < AI_RETRIES:

                wait = (
                    AI_RETRY_BASE
                    * attempt
                )

                print(
                    f"   ⏳ 等待 {wait}s"
                )

                time.sleep(
                    wait
                )

    raise RuntimeError(
        "AI 请求最终失败："
        + str(last_error)
    )


# ======================================================================
# JSON 提取
# ======================================================================

def extract_json(
    text: str
) -> dict:

    text = text.strip()

    # --------------------------------------------------------------
    # 直接 JSON
    # --------------------------------------------------------------

    try:

        data = json.loads(
            text
        )

        if isinstance(data, dict):

            return data

    except Exception:

        pass

    # --------------------------------------------------------------
    # 去掉 Markdown fence
    # --------------------------------------------------------------

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned
    )

    try:

        data = json.loads(
            cleaned.strip()
        )

        if isinstance(data, dict):

            return data

    except Exception:

        pass

    # --------------------------------------------------------------
    # 找第一个 JSON object
    # --------------------------------------------------------------

    start = cleaned.find("{")

    end = cleaned.rfind("}")

    if start >= 0 and end > start:

        candidate = (
            cleaned[
                start:end + 1
            ]
        )

        try:

            data = json.loads(
                candidate
            )

            if isinstance(data, dict):

                return data

        except Exception:

            pass

    raise ValueError(
        "无法解析 AI JSON"
    )


# ======================================================================
# 读取文件
# ======================================================================

def read_text(
    path: Path,
    max_chars: int = 30000
) -> str:

    try:

        text = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        return text[:max_chars]

    except Exception as exc:

        print(
            f"⚠️ 读取失败：{path}"
        )

        print(
            f"   {exc}"
        )

        return ""


# ======================================================================
# Task 4 Analysis
# ======================================================================

def get_analysis_files(
    target_date: date
) -> list[Path]:

    root = (
        RAW_NEWS
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-EventUnit"
        )
    )

    files = []

    # --------------------------------------------------------------
    # 严格 lowercase
    # --------------------------------------------------------------

    for language in (
        "en",
        "zh",
    ):

        directory = (
            root
            / language
            / "event_units"
        )

        if not directory.is_dir():

            continue

        files.extend(
            sorted(
                directory.glob(
                    "*_analysis.md"
                )
            )
        )

    return sorted(
        files,
        key=lambda p: p.name
    )


# ======================================================================
# 对应日报
# ======================================================================

def get_daily_file(
    target_date: date
) -> Path:

    return (
        DAILY
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + ".md"
        )
    )


# ======================================================================
# 分析单个 Event
# ======================================================================

def build_event_prompt(
    analysis_path: Path,
    analysis_text: str,
    daily_text: str,
) -> str:

    return f"""
# 748686 知识资产编译

请分析下面一个 Task 4 Event Analysis。

文件：

{analysis_path}

---

# Event Analysis

{analysis_text}

---

# 当日日报上下文

{daily_text[:12000]}

---

请判断这个事件是否产生了值得长期保存的知识。

返回以下 JSON：

{{
  "event_id": "",
  "long_term_value": 0,
  "summary": "",
  "knowledge_assets": [
    {{
      "type": "主题|产品|人物|公司|技术|概念|行业",
      "name": "",
      "action": "create|update|skip",
      "importance": 1,
      "confidence": 0.0,
      "summary": "",
      "new_facts": [
        ""
      ],
      "changes": [
        ""
      ],
      "source": "",
      "related_entities": [
        ""
      ]
    }}
  ],
  "relationships": [
    {{
      "from": "",
      "relation": "",
      "to": "",
      "evidence": ""
    }}
  ],
  "article_candidates": [
    {{
      "title": "",
      "reason": "",
      "priority": 1
    }}
  ],
  "topic_candidates": [
    {{
      "title": "",
      "reason": "",
      "priority": 1
    }}
  ],
  "material_candidates": [
    {{
      "title": "",
      "reason": ""
    }}
  ],
  "image_candidates": [
    {{
      "description": "",
      "reason": ""
    }}
  ],
  "new_questions": [
    ""
  ]
}}

规则：

1. 没有长期价值的实体 action 必须为 skip。
2. 不要把普通新闻人物全部变成人物知识卡片。
3. 不要把普通公司出现全部变成公司知识卡片。
4. 只有具有持续意义的实体才进入知识库。
5. importance 只能使用 1-5。
6. confidence 必须是 0-1。
7. source 必须保留 Event Analysis 文件路径。
8. related_entities 只能来自输入。
9. relationships 只能来自输入能够支持的关系。
10. 不得补充输入之外的事实。
11. 如果只是一次性事件，不要强行创建长期知识。
12. 如果一个已有知识发生明确变化，应使用 update。
""".strip()


# ======================================================================
# 标准化资产
# ======================================================================

def normalize_assets(
    data: dict,
    source: Path
) -> list[dict]:

    result = []

    assets = data.get(
        "knowledge_assets",
        []
    )

    if not isinstance(
        assets,
        list
    ):

        return result

    for asset in assets:

        if not isinstance(
            asset,
            dict
        ):

            continue

        asset_type = str(
            asset.get(
                "type",
                ""
            )
        ).strip()

        name = str(
            asset.get(
                "name",
                ""
            )
        ).strip()

        action = str(
            asset.get(
                "action",
                "skip"
            )
        ).strip().lower()

        if asset_type not in KNOWLEDGE_TYPES:

            continue

        if not name:

            continue

        if action not in (
            "create",
            "update",
            "skip",
        ):

            action = "skip"

        try:

            importance = int(
                asset.get(
                    "importance",
                    1
                )
            )

        except Exception:

            importance = 1

        importance = max(
            1,
            min(
                5,
                importance
            )
        )

        try:

            confidence = float(
                asset.get(
                    "confidence",
                    0
                )
            )

        except Exception:

            confidence = 0

        confidence = max(
            0,
            min(
                1,
                confidence
            )
        )

        new_facts = asset.get(
            "new_facts",
            []
        )

        changes = asset.get(
            "changes",
            []
        )

        related = asset.get(
            "related_entities",
            []
        )

        if not isinstance(
            new_facts,
            list
        ):

            new_facts = []

        if not isinstance(
            changes,
            list
        ):

            changes = []

        if not isinstance(
            related,
            list
        ):

            related = []

        result.append(
            {
                "type": asset_type,
                "name": name,
                "action": action,
                "importance": importance,
                "confidence": confidence,
                "summary": str(
                    asset.get(
                        "summary",
                        ""
                    )
                ).strip(),
                "new_facts": [
                    str(x).strip()
                    for x in new_facts
                    if str(x).strip()
                ],
                "changes": [
                    str(x).strip()
                    for x in changes
                    if str(x).strip()
                ],
                "source": str(
                    source
                ),
                "related_entities": [
                    str(x).strip()
                    for x in related
                    if str(x).strip()
                ],
            }
        )

    return result


# ======================================================================
# 知识文件路径
# ======================================================================

def knowledge_path(
    asset_type: str,
    name: str
) -> Path:

    directory = (
        KNOWLEDGE
        / asset_type
    )

    filename = (
        safe_filename(name)
        + ".md"
    )

    return (
        directory
        / filename
    )


# ======================================================================
# 查找同名知识
# ======================================================================

def find_existing_knowledge(
    asset_type: str,
    name: str
) -> Path | None:

    exact = knowledge_path(
        asset_type,
        name
    )

    if exact.is_file():

        return exact

    directory = (
        KNOWLEDGE
        / asset_type
    )

    if not directory.is_dir():

        return None

    target = name.strip().lower()

    for path in directory.glob(
        "*.md"
    ):

        if path.stem.strip().lower() == target:

            return path

    return None


# ======================================================================
# 新知识模板
# ======================================================================

def create_knowledge_content(
    asset: dict,
    target_date: date
) -> str:

    facts = asset.get(
        "new_facts",
        []
    )

    related = asset.get(
        "related_entities",
        []
    )

    facts_text = "\n".join(
        f"- {x}"
        for x in facts
    )

    if not facts_text:

        facts_text = "- 暂无结构化事实"

    related_text = "\n".join(
        f"- [[{x}]]"
        for x in related
    )

    if not related_text:

        related_text = "- 暂无"

    return f"""---
type: {asset["type"]}
name: {asset["name"]}
status: active
importance: {asset["importance"]}
confidence: {asset["confidence"]}
created_from: {target_date}
---

# {asset["name"]}

## 核心定义

{asset["summary"]}

## 新增事实

{facts_text}

## 与其他知识的关系

{related_text}

## 来源

- {asset["source"]}

## 首次进入知识库

{target_date.isoformat()}

## 更新记录

- {target_date.isoformat()}：由 Task 4 Event Analysis 编译进入知识库。
"""


# ======================================================================
# 更新已有知识
# ======================================================================

def append_knowledge_update(
    path: Path,
    asset: dict,
    target_date: date
) -> None:

    existing = read_text(
        path,
        max_chars=200000
    )

    if not existing.strip():

        existing = create_knowledge_content(
            asset,
            target_date
        )

    facts = asset.get(
        "new_facts",
        []
    )

    changes = asset.get(
        "changes",
        []
    )

    related = asset.get(
        "related_entities",
        []
    )

    block = []

    block.append(
        "\n\n---\n\n"
    )

    block.append(
        f"## 知识更新 · "
        f"{target_date.isoformat()}\n"
    )

    if asset.get(
        "summary"
    ):

        block.append(
            "\n### 本次变化\n\n"
        )

        block.append(
            asset["summary"]
            + "\n"
        )

    if facts:

        block.append(
            "\n### 新增事实\n\n"
        )

        for fact in facts:

            block.append(
                f"- {fact}\n"
            )

    if changes:

        block.append(
            "\n### 变化\n\n"
        )

        for change in changes:

            block.append(
                f"- {change}\n"
            )

    if related:

        block.append(
            "\n### 相关知识\n\n"
        )

        for item in related:

            block.append(
                f"- [[{item}]]\n"
            )

    block.append(
        "\n### 来源\n\n"
    )

    block.append(
        f"- {asset['source']}\n"
    )

    updated = (
        existing
        + "".join(block)
    )

    atomic_write(
        path,
        updated
    )


# ======================================================================
# 原子写入
# ======================================================================

def atomic_write(
    path: Path,
    content: str
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    tmp = path.with_suffix(
        path.suffix
        + ".tmp"
    )

    try:

        tmp.write_text(
            content,
            encoding="utf-8"
        )

        if not is_nonempty_file(
            tmp
        ):

            raise RuntimeError(
                f"临时文件为空：{tmp}"
            )

        tmp.replace(
            path
        )

    finally:

        if tmp.exists():

            try:

                tmp.unlink()

            except Exception:

                pass


# ======================================================================
# 写知识资产
# ======================================================================

def save_knowledge_asset(
    asset: dict,
    target_date: date
) -> Path | None:

    action = asset[
        "action"
    ]

    if action == "skip":

        return None

    path = find_existing_knowledge(
        asset["type"],
        asset["name"]
    )

    if action == "create":

        if path is not None:

            # AI 判断 create，
            # 但实际已经存在。
            # 为安全起见，转为 update。
            append_knowledge_update(
                path,
                asset,
                target_date
            )

            return path

        path = knowledge_path(
            asset["type"],
            asset["name"]
        )

        content = create_knowledge_content(
            asset,
            target_date
        )

        atomic_write(
            path,
            content
        )

        return path

    if action == "update":

        if path is None:

            path = knowledge_path(
                asset["type"],
                asset["name"]
            )

            content = create_knowledge_content(
                asset,
                target_date
            )

            atomic_write(
                path,
                content
            )

            return path

        append_knowledge_update(
            path,
            asset,
            target_date
        )

        return path

    return None


# ======================================================================
# 关系标准化
# ======================================================================

def normalize_relationships(
    all_results: list[dict]
) -> list[dict]:

    relationships = []

    seen = set()

    for result in all_results:

        raw = result.get(
            "relationships",
            []
        )

        if not isinstance(
            raw,
            list
        ):

            continue

        for item in raw:

            if not isinstance(
                item,
                dict
            ):

                continue

            source = str(
                item.get(
                    "from",
                    ""
                )
            ).strip()

            relation = str(
                item.get(
                    "relation",
                    ""
                )
            ).strip()

            target = str(
                item.get(
                    "to",
                    ""
                )
            ).strip()

            evidence = str(
                item.get(
                    "evidence",
                    ""
                )
            ).strip()

            if not source:
                continue

            if not relation:
                continue

            if not target:
                continue

            key = (
                source.lower(),
                relation.lower(),
                target.lower()
            )

            if key in seen:

                continue

            seen.add(key)

            relationships.append(
                {
                    "from": source,
                    "relation": relation,
                    "to": target,
                    "evidence": evidence,
                }
            )

    return relationships


# ======================================================================
# 候选文件
# ======================================================================

def save_index_file(
    path: Path,
    title: str,
    target_date: date,
    rows: list[str]
) -> None:

    if rows:

        body = "\n".join(
            rows
        )

    else:

        body = (
            "本日没有形成符合条件的候选项。"
        )

    content = f"""---
date: {target_date.isoformat()}
type: knowledge_asset_index
status: generated
---

# {title}

日期：

{target_date.isoformat()}

{body}
"""

    atomic_write(
        path,
        content
    )


# ======================================================================
# 关系图谱
# ======================================================================

def save_graph(
    target_date: date,
    relationships: list[dict]
) -> Path:

    path = (
        GRAPH
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-关系图谱.md"
        )
    )

    rows = []

    rows.append(
        f"# {target_date.isoformat()} 知识关系图谱"
    )

    rows.append("")

    rows.append(
        "本文件由 Task 4 Event Analysis "
        "自动编译。"
    )

    rows.append("")

    if not relationships:

        rows.append(
            "本日没有形成足够证据支持的新增关系。"
        )

    else:

        rows.append(
            "| 起点 | 关系 | 终点 | 证据 |"
        )

        rows.append(
            "|---|---|---|---|"
        )

        for item in relationships:

            rows.append(
                "| "
                + item["from"]
                + " | "
                + item["relation"]
                + " | "
                + item["to"]
                + " | "
                + item["evidence"]
                + " |"
            )

    atomic_write(
        path,
        "\n".join(rows)
        + "\n"
    )

    return path


# ======================================================================
# 完成标记
# ======================================================================

def complete_marker(
    target_date: date
) -> Path:

    return (
        SYSTEM_LOG
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "_COMPLETE"
        )
    )


def mark_complete(
    target_date: date,
    stats: dict
) -> None:

    marker = complete_marker(
        target_date
    )

    content = json.dumps(
        {
            "date":
                target_date.isoformat(),
            "completed_at":
                now().isoformat(),
            "stats":
                stats,
        },
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
    target_date: date
) -> bool:

    print()
    print("=" * 70)

    print(
        f"KNOWLEDGE ASSET DATE"
    )

    print(
        f"DATE : {target_date}"
    )

    print("=" * 70)

    marker = complete_marker(
        target_date
    )

    # --------------------------------------------------------------
    # 已完成
    # --------------------------------------------------------------

    if is_nonempty_file(
        marker
    ):

        print(
            "⏭️ ASSETS ALREADY COMPLETE"
        )

        print(
            f"   {target_date}"
        )

        return True

    # --------------------------------------------------------------
    # Task 4
    # --------------------------------------------------------------

    analysis_files = (
        get_analysis_files(
            target_date
        )
    )

    print(
        f"Task 4 Analysis : "
        f"{len(analysis_files)}"
    )

    if not analysis_files:

        print(
            "⏭️ 本日没有 Task 4 Analysis"
        )

        print(
            "   不创建伪知识资产。"
        )

        return False

    # --------------------------------------------------------------
    # 日报
    # --------------------------------------------------------------

    daily_path = get_daily_file(
        target_date
    )

    daily_text = ""

    if is_nonempty_file(
        daily_path
    ):

        daily_text = read_text(
            daily_path,
            30000
        )

    else:

        print(
            "ℹ️ 本日日报不存在，"
            "Asset Compiler 仍可根据 Task 4 运行。"
        )

    # --------------------------------------------------------------
    # 统计
    # --------------------------------------------------------------

    stats = {
        "analysis_files":
            len(analysis_files),
        "processed_events":
            0,
        "knowledge_created":
            0,
        "knowledge_updated":
            0,
        "knowledge_skipped":
            0,
        "relationships":
            0,
        "article_candidates":
            0,
        "topic_candidates":
            0,
        "material_candidates":
            0,
        "image_candidates":
            0,
        "new_questions":
            0,
    }

    all_results = []

    article_candidates = []

    topic_candidates = []

    material_candidates = []

    image_candidates = []

    new_questions = []

    # --------------------------------------------------------------
    # 一个 Event 一个 Event 处理
    # --------------------------------------------------------------

    for index, analysis_path in enumerate(
        analysis_files,
        start=1
    ):

        print()
        print(
            f"[{index}/{len(analysis_files)}] "
            f"PROCESSING EVENT"
        )

        print(
            f"   {analysis_path.name}"
        )

        analysis_text = read_text(
            analysis_path,
            30000
        )

        if not analysis_text.strip():

            print(
                "   ⚠️ Analysis 为空，跳过"
            )

            continue

        prompt = build_event_prompt(
            analysis_path,
            analysis_text,
            daily_text
        )

        raw_result = call_ai(
            prompt
        )

        try:

            result = extract_json(
                raw_result
            )

        except Exception as exc:

            print(
                "   ❌ JSON 解析失败"
            )

            print(
                f"   {exc}"
            )

            raise

        all_results.append(
            result
        )

        stats[
            "processed_events"
        ] += 1

        assets = normalize_assets(
            result,
            analysis_path
        )

        # ----------------------------------------------------------
        # 知识资产
        # ----------------------------------------------------------

        for asset in assets:

            action = asset[
                "action"
            ]

            if action == "skip":

                stats[
                    "knowledge_skipped"
                ] += 1

                continue

            saved = save_knowledge_asset(
                asset,
                target_date
            )

            if saved is None:

                continue

            if action == "create":

                stats[
                    "knowledge_created"
                ] += 1

                print(
                    "   ✅ CREATE"
                )

            elif action == "update":

                stats[
                    "knowledge_updated"
                ] += 1

                print(
                    "   🔄 UPDATE"
                )

            print(
                f"      {saved}"
            )

        # ----------------------------------------------------------
        # 候选
        # ----------------------------------------------------------

        raw_articles = result.get(
            "article_candidates",
            []
        )

        if isinstance(
            raw_articles,
            list
        ):

            for item in raw_articles:

                if isinstance(
                    item,
                    dict
                ):

                    article_candidates.append(
                        item
                    )

        raw_topics = result.get(
            "topic_candidates",
            []
        )

        if isinstance(
            raw_topics,
            list
        ):

            for item in raw_topics:

                if isinstance(
                    item,
                    dict
                ):

                    topic_candidates.append(
                        item
                    )

        raw_materials = result.get(
            "material_candidates",
            []
        )

        if isinstance(
            raw_materials,
            list
        ):

            for item in raw_materials:

                if isinstance(
                    item,
                    dict
                ):

                    material_candidates.append(
                        item
                    )

        raw_images = result.get(
            "image_candidates",
            []
        )

        if isinstance(
            raw_images,
            list
        ):

            for item in raw_images:

                if isinstance(
                    item,
                    dict
                ):

                    image_candidates.append(
                        item
                    )

        raw_questions = result.get(
            "new_questions",
            []
        )

        if isinstance(
            raw_questions,
            list
        ):

            new_questions.extend(
                str(x).strip()
                for x in raw_questions
                if str(x).strip()
            )

    # ==================================================================
    # 汇总关系
    # ==================================================================

    relationships = normalize_relationships(
        all_results
    )

    stats[
        "relationships"
    ] = len(
        relationships
    )

    stats[
        "article_candidates"
    ] = len(
        article_candidates
    )

    stats[
        "topic_candidates"
    ] = len(
        topic_candidates
    )

    stats[
        "material_candidates"
    ] = len(
        material_candidates
    )

    stats[
        "image_candidates"
    ] = len(
        image_candidates
    )

    stats[
        "new_questions"
    ] = len(
        new_questions
    )

    # ==================================================================
    # 01 新闻索引
    # ==================================================================

    news_dir = (
        NEWS
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
    )

    news_path = (
        news_dir
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-新闻资产索引.md"
        )
    )

    news_rows = []

    news_rows.append(
        "## 来源"
    )

    news_rows.append("")

    for path in analysis_files:

        news_rows.append(
            f"- `{path}`"
        )

    news_rows.append("")

    news_rows.append(
        "## 说明"
    )

    news_rows.append("")

    news_rows.append(
        "本文件不是原始新闻副本。"
        "原始事件保留在 Raw News。"
    )

    save_index_file(
        news_path,
        f"{target_date} 新闻资产索引",
        target_date,
        news_rows
    )

    # ==================================================================
    # 02 资料
    # ==================================================================

    material_dir = (
        MATERIALS
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
    )

    material_path = (
        material_dir
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-资料索引.md"
        )
    )

    material_rows = []

    material_rows.append(
        "## 资料候选"
    )

    material_rows.append("")

    if material_candidates:

        for item in material_candidates:

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

            if title:

                material_rows.append(
                    f"- **{title}**"
                )

                if reason:

                    material_rows.append(
                        f"  - 原因：{reason}"
                    )

    else:

        material_rows.append(
            "本日没有形成资料候选。"
        )

    save_index_file(
        material_path,
        f"{target_date} 资料索引",
        target_date,
        material_rows
    )

    # ==================================================================
    # 03 文章
    # ==================================================================

    article_dir = (
        ARTICLES
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
    )

    article_path = (
        article_dir
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-文章候选.md"
        )
    )

    article_rows = []

    article_rows.append(
        "## 文章候选"
    )

    article_rows.append("")

    if article_candidates:

        for item in article_candidates:

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

            if title:

                article_rows.append(
                    f"- **P{priority}｜{title}**"
                )

                if reason:

                    article_rows.append(
                        f"  - 原因：{reason}"
                    )

    else:

        article_rows.append(
            "本日没有形成文章候选。"
        )

    save_index_file(
        article_path,
        f"{target_date} 文章候选",
        target_date,
        article_rows
    )

    # ==================================================================
    # 04 图片
    # ==================================================================

    image_dir = (
        IMAGES
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
    )

    image_path = (
        image_dir
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-图片索引.md"
        )
    )

    image_rows = []

    image_rows.append(
        "## 图片候选"
    )

    image_rows.append("")

    if image_candidates:

        for item in image_candidates:

            description = str(
                item.get(
                    "description",
                    ""
                )
            ).strip()

            reason = str(
                item.get(
                    "reason",
                    ""
                )
            ).strip()

            if description:

                image_rows.append(
                    f"- **{description}**"
                )

                if reason:

                    image_rows.append(
                        f"  - 原因：{reason}"
                    )

    else:

        image_rows.append(
            "本日没有形成图片候选。"
        )

    save_index_file(
        image_path,
        f"{target_date} 图片索引",
        target_date,
        image_rows
    )

    # ==================================================================
    # 07 专题
    # ==================================================================

    topic_dir = (
        TOPICS
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
    )

    topic_path = (
        topic_dir
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-专题候选.md"
        )
    )

    topic_rows = []

    topic_rows.append(
        "## 专题候选"
    )

    topic_rows.append("")

    if topic_candidates:

        for item in topic_candidates:

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

            if title:

                topic_rows.append(
                    f"- **P{priority}｜{title}**"
                )

                if reason:

                    topic_rows.append(
                        f"  - 原因：{reason}"
                    )

    else:

        topic_rows.append(
            "本日没有形成专题候选。"
        )

    save_index_file(
        topic_path,
        f"{target_date} 专题候选",
        target_date,
        topic_rows
    )

    # ==================================================================
    # 09 知识图谱
    # ==================================================================

    graph_path = save_graph(
        target_date,
        relationships
    )

    print()
    print(
        f"✅ Graph saved: {graph_path}"
    )

    # ==================================================================
    # 新问题
    # ==================================================================

    question_path = (
        SYSTEM_LOG
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "_new_questions.md"
        )
    )

    question_rows = [
        f"# {target_date} 新知识问题",
        "",
    ]

    if new_questions:

        seen_questions = set()

        for question in new_questions:

            key = question.lower()

            if key in seen_questions:

                continue

            seen_questions.add(
                key
            )

            question_rows.append(
                f"- {question}"
            )

    else:

        question_rows.append(
            "本日没有形成新的研究问题。"
        )

    atomic_write(
        question_path,
        "\n".join(
            question_rows
        )
        + "\n"
    )

    # ==================================================================
    # COMPLETE
    # ==================================================================

    mark_complete(
        target_date,
        stats
    )

    print()
    print(
        "============================================================"
    )

    print(
        "✅ KNOWLEDGE ASSET DATE COMPLETE"
    )

    print(
        f"DATE : {target_date}"
    )

    print(
        f"Events       : "
        f"{stats['processed_events']}"
    )

    print(
        f"Created      : "
        f"{stats['knowledge_created']}"
    )

    print(
        f"Updated      : "
        f"{stats['knowledge_updated']}"
    )

    print(
        f"Skipped      : "
        f"{stats['knowledge_skipped']}"
    )

    print(
        f"Relationships : "
        f"{stats['relationships']}"
    )

    print(
        f"Questions    : "
        f"{stats['new_questions']}"
    )

    print(
        "============================================================"
    )

    return True


# ======================================================================
# 最近三天
# ======================================================================

def get_target_dates() -> list[date]:
    """
    与 knowledge_daily.py 保持一致：

        前天
        昨天
        今天

    """

    today = now().date()

    return [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today,
    ]


# ======================================================================
# MAIN
# ======================================================================

def main():

    current = now()

    print()
    print("=" * 70)

    print(
        "748686 KNOWLEDGE ASSET COMPILER V1.0"
    )

    print("=" * 70)

    print(
        f"Current time : "
        f"{current.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        "Timezone     : Asia/Shanghai"
    )

    print()

    dates = get_target_dates()

    print(
        "Target dates:"
    )

    for target_date in dates:

        print(
            f"   - {target_date}"
        )

    # ==================================================================
    # 严格按日期顺序处理
    # ==================================================================

    for target_date in dates:

        try:

            process_date(
                target_date
            )

        except Exception as exc:

            print()
            print("=" * 70)

            print(
                "❌ KNOWLEDGE ASSET FAILED"
            )

            print(
                f"DATE : {target_date}"
            )

            print(
                f"ERROR: "
                f"{type(exc).__name__}: {exc}"
            )

            print("=" * 70)

            raise

    # ==================================================================
    # 完成
    # ==================================================================

    print()
    print("=" * 70)

    print(
        "✅ KNOWLEDGE ASSET COMPILER COMPLETE"
    )

    print("=" * 70)

    print(
        "Processed dates:"
    )

    for target_date in dates:

        print(
            f"   ✓ {target_date}"
        )

    print()


# ======================================================================
# ENTRY
# ======================================================================

if __name__ == "__main__":

    main()
