#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Asset Compiler V2.0

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

    08_知识库/
        主题/
        产品/
        人物/
        公司/
        技术/
        概念/
        行业/

        主题/
            知识缺口/
            知识矛盾/

    09_知识图谱/
        YYYY/MM/YYYY-MM-DD.md

状态：

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

    Task 4 Event Analysis
            ↓
       判断长期价值
            ↓
        提取实体
            ↓
        提取新事实
            ↓
        判断 CREATE / UPDATE / SKIP
            ↓
       写入长期知识
            ↓
       建立知识关系
            ↓
      发现知识缺口
            ↓
      发现潜在知识矛盾

======================================================================
本程序明确不负责
======================================================================

❌ 不生成 01_新闻 日报资产索引
❌ 不生成 02_资料 候选文件
❌ 不生成 03_文章 候选文件
❌ 不生成 04_图片 候选文件
❌ 不生成 07_专题报告 日报级候选
❌ 不写入 10_用户资料
❌ 不修改 Task 3
❌ 不修改 Task 4

这些属于其他知识利用/增长机制。

======================================================================
本程序负责
======================================================================

✅ 08_知识库
    长期知识实体

✅ 09_知识图谱
    知识之间的关系

✅ 08_知识库/主题/知识缺口
    尚未解决的问题

✅ 08_知识库/主题/知识矛盾
    需要进一步验证的冲突

✅ 00_System/运行日志/knowledge_asset
    仅保存运行状态与 COMPLETE 标记

======================================================================
重要规则
======================================================================

1. 严格使用小写 en / zh。
2. en / zh 相同 EVT-ID 视为同一个事件。
3. 不修改 Task 3。
4. 不修改 Task 4。
5. 不删除已有知识。
6. 不覆盖已有知识历史。
7. 已有知识采用追加更新。
8. 相同 EVT-ID 不重复写入。
9. 不把推测写成事实。
10. AI 输出必须为 JSON。
11. AI JSON 失败会重试。
12. 日期使用 Asia/Shanghai。
13. 每一天独立处理。
14. 一天成功后立即落盘。
15. 已完成日期直接跳过。
16. 中途失败不会写 COMPLETE。
17. 10_用户资料绝不由新闻自动生成。
"""

from __future__ import annotations

import json
import os
import re
import time

from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen


# ======================================================================
# ROOT
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]


# ======================================================================
# INPUT
# ======================================================================

RAW_NEWS = ROOT / "Raw News"

DAILY = ROOT / "05_日报"


# ======================================================================
# OUTPUT
# ======================================================================

KNOWLEDGE = ROOT / "08_知识库"

GRAPH = ROOT / "09_知识图谱"


# ======================================================================
# SYSTEM STATE
# ======================================================================

SYSTEM_LOG = (
    ROOT
    / "00_System"
    / "运行日志"
    / "knowledge_asset"
)


# ======================================================================
# TIMEZONE
# ======================================================================

TIMEZONE = timezone(
    timedelta(hours=8)
)


# ======================================================================
# AI CONFIG
# ======================================================================

AI_BASE_URL = os.getenv(
    "AI_BASE_URL",
    "https://api.openai.com/v1",
).rstrip("/")


AI_MODEL = os.getenv(
    "AI_MODEL",
    "",
)


AI_API_KEY = os.getenv(
    "AI_API_KEY",
    "",
)


AI_TIMEOUT = 180

AI_RETRIES = 5

AI_RETRY_BASE = 5

AI_THROTTLE_SECONDS = 1.2


# ======================================================================
# KNOWLEDGE TYPES
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
# TIME
# ======================================================================

def now() -> datetime:
    return datetime.now(TIMEZONE)


# ======================================================================
# FILE HELPERS
# ======================================================================

def is_nonempty_file(path: Path) -> bool:
    try:
        return (
            path.is_file()
            and path.stat().st_size > 0
        )
    except Exception:
        return False


def read_text(
    path: Path,
    max_chars: int = 30000,
) -> str:

    try:
        text = path.read_text(
            encoding="utf-8",
            errors="replace",
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


def atomic_write(
    path: Path,
    content: str,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp = path.with_suffix(
        path.suffix + ".tmp"
    )

    try:

        tmp.write_text(
            content,
            encoding="utf-8",
        )

        if not is_nonempty_file(tmp):

            raise RuntimeError(
                f"临时文件为空：{tmp}"
            )

        tmp.replace(path)

    finally:

        if tmp.exists():

            try:
                tmp.unlink()
            except Exception:
                pass


# ======================================================================
# SAFE NAME
# ======================================================================

def safe_filename(name: str) -> str:

    name = str(name).strip()

    if not name:
        return "未命名"

    name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name,
    )

    name = re.sub(
        r"\s+",
        " ",
        name,
    )

    name = name.strip(" .")

    if not name:
        return "未命名"

    return name[:120]


# ======================================================================
# EVENT ID
# ======================================================================

EVENT_ID_PATTERN = re.compile(
    r"(EVT-\d{8}-\d{6})",
    re.IGNORECASE,
)


def extract_event_id(
    path: Path,
) -> str:

    match = EVENT_ID_PATTERN.search(
        path.name
    )

    if match:

        return match.group(1).upper()

    text = read_text(
        path,
        max_chars=5000,
    )

    match = EVENT_ID_PATTERN.search(
        text
    )

    if match:

        return match.group(1).upper()

    return path.stem


# ======================================================================
# TASK 4 ANALYSIS
# ======================================================================

def get_analysis_files(
    target_date: date,
) -> dict[str, list[Path]]:

    root = (
        RAW_NEWS
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + "-EventUnit"
        )
    )

    result = {
        "en": [],
        "zh": [],
    }

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

        result[language] = sorted(
            directory.glob(
                "*_analysis.md"
            ),
            key=lambda p: p.name,
        )

    return result


# ======================================================================
# DEDUPLICATE EN / ZH
# ======================================================================

def group_event_files(
    analysis_files: dict[str, list[Path]],
) -> list[dict]:

    groups: dict[str, dict] = {}

    for language in (
        "en",
        "zh",
    ):

        for path in analysis_files.get(
            language,
            [],
        ):

            event_id = extract_event_id(
                path
            )

            if event_id not in groups:

                groups[event_id] = {
                    "event_id": event_id,
                    "en": None,
                    "zh": None,
                }

            groups[event_id][
                language
            ] = path

    return sorted(
        groups.values(),
        key=lambda x: x["event_id"],
    )


# ======================================================================
# DAILY REPORT
# ======================================================================

def get_daily_file(
    target_date: date,
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
# AI
# ======================================================================

def call_ai(
    prompt: str,
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
你是748686自生长知识系统的长期知识资产编译器。

你的工作不是写新闻摘要。

你的工作是判断一个事件是否值得进入长期知识库。

你必须：

1. 从 Task 4 Event Analysis 提取长期有效知识。
2. 判断实体是否值得长期保存。
3. 判断已有知识应该 CREATE、UPDATE 还是 SKIP。
4. 提取能够被输入直接支持的新事实。
5. 提取能够被输入直接支持的知识关系。
6. 识别知识缺口。
7. 识别需要进一步验证的潜在知识矛盾。

严格依据输入。

禁止编造。

禁止使用输入之外的事实。

不确定的信息降低 confidence。

普通一次性新闻不应该强行变成长期知识。

只输出合法 JSON。

不要输出 Markdown。

不要输出 ```json。

不要输出解释文字。
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
        AI_RETRIES + 1,
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
                timeout=AI_TIMEOUT,
            ) as response:

                raw = (
                    response
                    .read()
                    .decode(
                        "utf-8",
                        errors="replace",
                    )
                )

            data = json.loads(raw)

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

                time.sleep(wait)

    raise RuntimeError(
        "AI 请求最终失败："
        + str(last_error)
    )


# ======================================================================
# JSON
# ======================================================================

def extract_json(
    text: str,
) -> dict:

    text = text.strip()

    try:

        data = json.loads(text)

        if isinstance(data, dict):
            return data

    except Exception:
        pass

    cleaned = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    )

    cleaned = re.sub(
        r"\s*```$",
        "",
        cleaned,
    )

    try:

        data = json.loads(
            cleaned.strip()
        )

        if isinstance(data, dict):
            return data

    except Exception:
        pass

    start = cleaned.find("{")

    end = cleaned.rfind("}")

    if start >= 0 and end > start:

        candidate = cleaned[
            start:end + 1
        ]

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
# EVENT PROMPT
# ======================================================================

def build_event_prompt(
    event_id: str,
    en_path: Path | None,
    zh_path: Path | None,
    daily_text: str,
) -> str:

    en_text = ""

    zh_text = ""

    if en_path is not None:

        en_text = read_text(
            en_path,
            30000,
        )

    if zh_path is not None:

        zh_text = read_text(
            zh_path,
            30000,
        )

    return f"""
# 748686 长期知识资产编译

## Event ID

{event_id}

---

## English Task 4 Analysis

文件：

{en_path if en_path else "不存在"}

内容：

{en_text if en_text else "无"}

---

## Chinese Task 4 Analysis

文件：

{zh_path if zh_path else "不存在"}

内容：

{zh_text if zh_text else "无"}

---

## 当日日报

{daily_text[:12000] if daily_text else "无"}

---

请判断这个事件是否产生了值得长期保存的知识。

注意：

en 与 zh 如果属于同一个 Event ID，只能视为一个事件。

不得因为语言不同而重复创建或更新同一个知识。

返回：

{{
  "event_id": "{event_id}",
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
  "knowledge_gaps": [
    {{
      "question": "",
      "reason": "",
      "importance": 1
    }}
  ],
  "contradictions": [
    {{
      "subject": "",
      "description": "",
      "reason": "",
      "importance": 1
    }}
  ]
}}

规则：

1. long_term_value 使用 0-5。
2. 没有长期价值时可以返回空 knowledge_assets。
3. 普通一次性新闻不要强行建立知识。
4. 不要把所有出现的人物都变成人物知识。
5. 不要把所有出现的公司都变成公司知识。
6. 不要把所有出现的产品都变成产品知识。
7. 只有具有持续意义的实体才进入知识库。
8. importance 必须为 1-5。
9. confidence 必须为 0-1。
10. action 只能是 create、update、skip。
11. new_facts 只能写输入明确支持的事实。
12. changes 只能写输入明确支持的变化。
13. related_entities 只能来自输入。
14. relationships 必须有输入证据支持。
15. knowledge_gaps 是需要继续研究的问题，不是事实。
16. contradictions 是需要进一步验证的问题，不得直接宣布某个事实为错误。
17. 不得编造外部信息。
18. 不得使用输入之外的知识补全答案。
""".strip()


# ======================================================================
# NORMALIZE KNOWLEDGE ASSETS
# ======================================================================

def normalize_assets(
    data: dict,
    event_id: str,
) -> list[dict]:

    result = []

    raw_assets = data.get(
        "knowledge_assets",
        [],
    )

    if not isinstance(
        raw_assets,
        list,
    ):
        return result

    for asset in raw_assets:

        if not isinstance(
            asset,
            dict,
        ):
            continue

        asset_type = str(
            asset.get(
                "type",
                "",
            )
        ).strip()

        name = str(
            asset.get(
                "name",
                "",
            )
        ).strip()

        if asset_type not in KNOWLEDGE_TYPES:
            continue

        if not name:
            continue

        action = str(
            asset.get(
                "action",
                "skip",
            )
        ).strip().lower()

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
                    1,
                )
            )

        except Exception:

            importance = 1

        importance = max(
            1,
            min(
                5,
                importance,
            ),
        )

        try:

            confidence = float(
                asset.get(
                    "confidence",
                    0,
                )
            )

        except Exception:

            confidence = 0

        confidence = max(
            0,
            min(
                1,
                confidence,
            ),
        )

        new_facts = asset.get(
            "new_facts",
            [],
        )

        changes = asset.get(
            "changes",
            [],
        )

        related = asset.get(
            "related_entities",
            [],
        )

        if not isinstance(
            new_facts,
            list,
        ):
            new_facts = []

        if not isinstance(
            changes,
            list,
        ):
            changes = []

        if not isinstance(
            related,
            list,
        ):
            related = []

        result.append(
            {
                "event_id": event_id,
                "type": asset_type,
                "name": name,
                "action": action,
                "importance": importance,
                "confidence": confidence,
                "summary": str(
                    asset.get(
                        "summary",
                        "",
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
                "related_entities": [
                    str(x).strip()
                    for x in related
                    if str(x).strip()
                ],
            }
        )

    return result


# ======================================================================
# KNOWLEDGE PATH
# ======================================================================

def knowledge_path(
    asset_type: str,
    name: str,
) -> Path:

    return (
        KNOWLEDGE
        / asset_type
        / (
            safe_filename(name)
            + ".md"
        )
    )


# ======================================================================
# FIND EXISTING KNOWLEDGE
# ======================================================================

def find_existing_knowledge(
    asset_type: str,
    name: str,
) -> Path | None:

    exact = knowledge_path(
        asset_type,
        name,
    )

    if exact.is_file():
        return exact

    directory = (
        KNOWLEDGE
        / asset_type
    )

    if not directory.is_dir():
        return None

    target = (
        name.strip().lower()
    )

    for path in directory.glob(
        "*.md"
    ):

        if (
            path.stem
            .strip()
            .lower()
            == target
        ):
            return path

    return None


# ======================================================================
# EVENT ALREADY RECORDED
# ======================================================================

def event_already_recorded(
    path: Path,
    event_id: str,
) -> bool:

    if not path.is_file():
        return False

    text = read_text(
        path,
        max_chars=300000,
    )

    if not text:
        return False

    return event_id in text


# ======================================================================
# CREATE KNOWLEDGE
# ======================================================================

def create_knowledge_content(
    asset: dict,
    target_date: date,
) -> str:

    facts = asset.get(
        "new_facts",
        [],
    )

    related = asset.get(
        "related_entities",
        [],
    )

    facts_text = "\n".join(
        f"- {item}"
        for item in facts
    )

    if not facts_text:
        facts_text = "- 暂无结构化事实"

    related_text = "\n".join(
        f"- [[{item}]]"
        for item in related
    )

    if not related_text:
        related_text = "- 暂无"

    event_id = asset[
        "event_id"
    ]

    return f"""---
type: {asset["type"]}
name: {asset["name"]}
status: active
importance: {asset["importance"]}
confidence: {asset["confidence"]}
created_at: {target_date.isoformat()}
last_updated: {target_date.isoformat()}
---

# {asset["name"]}

## 核心定义

{asset["summary"] or "暂无"}

## 新增事实

{facts_text}

## 与其他知识的关系

{related_text}

## 来源事件

- {event_id}

## 来源文件

- Task 4 Event Analysis

## 更新记录

### {target_date.isoformat()}

- 来源事件：{event_id}
- 本次动作：CREATE
"""


# ======================================================================
# APPEND KNOWLEDGE UPDATE
# ======================================================================

def append_knowledge_update(
    path: Path,
    asset: dict,
    target_date: date,
) -> bool:

    event_id = asset[
        "event_id"
    ]

    if event_already_recorded(
        path,
        event_id,
    ):

        print(
            f"   ⏭️ 已记录事件 "
            f"{event_id}"
        )

        return False

    existing = read_text(
        path,
        max_chars=500000,
    )

    if not existing.strip():

        atomic_write(
            path,
            create_knowledge_content(
                asset,
                target_date,
            ),
        )

        return True

    facts = asset.get(
        "new_facts",
        [],
    )

    changes = asset.get(
        "changes",
        [],
    )

    related = asset.get(
        "related_entities",
        [],
    )

    block = []

    block.append(
        "\n\n---\n\n"
    )

    block.append(
        f"## 知识更新 · "
        f"{target_date.isoformat()}\n\n"
    )

    block.append(
        f"- 来源事件：{event_id}\n"
    )

    block.append(
        f"- 置信度："
        f"{asset['confidence']}\n"
    )

    block.append(
        f"- 重要性："
        f"{asset['importance']}\n"
    )

    if asset.get("summary"):

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

    updated = (
        existing
        + "".join(block)
    )

    atomic_write(
        path,
        updated,
    )

    return True


# ======================================================================
# SAVE KNOWLEDGE
# ======================================================================

def save_knowledge_asset(
    asset: dict,
    target_date: date,
) -> tuple[str, Path | None]:

    action = asset[
        "action"
    ]

    if action == "skip":

        return (
            "skipped",
            None,
        )

    path = find_existing_knowledge(
        asset["type"],
        asset["name"],
    )

    if path is None:

        path = knowledge_path(
            asset["type"],
            asset["name"],
        )

        atomic_write(
            path,
            create_knowledge_content(
                asset,
                target_date,
            ),
        )

        return (
            "created",
            path,
        )

    changed = append_knowledge_update(
        path,
        asset,
        target_date,
    )

    if changed:

        return (
            "updated",
            path,
        )

    return (
        "duplicate",
        path,
    )


# ======================================================================
# RELATIONSHIPS
# ======================================================================

def normalize_relationships(
    all_results: list[dict],
) -> list[dict]:

    relationships = []

    seen = set()

    for result in all_results:

        raw = result.get(
            "relationships",
            [],
        )

        if not isinstance(
            raw,
            list,
        ):
            continue

        for item in raw:

            if not isinstance(
                item,
                dict,
            ):
                continue

            source = str(
                item.get(
                    "from",
                    "",
                )
            ).strip()

            relation = str(
                item.get(
                    "relation",
                    "",
                )
            ).strip()

            target = str(
                item.get(
                    "to",
                    "",
                )
            ).strip()

            evidence = str(
                item.get(
                    "evidence",
                    "",
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
                target.lower(),
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
# KNOWLEDGE GAPS
# ======================================================================

def normalize_gaps(
    all_results: list[dict],
) -> list[dict]:

    result = []

    seen = set()

    for item_result in all_results:

        raw = item_result.get(
            "knowledge_gaps",
            [],
        )

        if not isinstance(
            raw,
            list,
        ):
            continue

        for item in raw:

            if not isinstance(
                item,
                dict,
            ):
                continue

            question = str(
                item.get(
                    "question",
                    "",
                )
            ).strip()

            reason = str(
                item.get(
                    "reason",
                    "",
                )
            ).strip()

            try:

                importance = int(
                    item.get(
                        "importance",
                        1,
                    )
                )

            except Exception:

                importance = 1

            importance = max(
                1,
                min(
                    5,
                    importance,
                ),
            )

            if not question:
                continue

            key = question.lower()

            if key in seen:
                continue

            seen.add(key)

            result.append(
                {
                    "question": question,
                    "reason": reason,
                    "importance": importance,
                }
            )

    return result


# ======================================================================
# CONTRADICTIONS
# ======================================================================

def normalize_contradictions(
    all_results: list[dict],
) -> list[dict]:

    result = []

    seen = set()

    for item_result in all_results:

        raw = item_result.get(
            "contradictions",
            [],
        )

        if not isinstance(
            raw,
            list,
        ):
            continue

        for item in raw:

            if not isinstance(
                item,
                dict,
            ):
                continue

            subject = str(
                item.get(
                    "subject",
                    "",
                )
            ).strip()

            description = str(
                item.get(
                    "description",
                    "",
                )
            ).strip()

            reason = str(
                item.get(
                    "reason",
                    "",
                )
            ).strip()

            try:

                importance = int(
                    item.get(
                        "importance",
                        1,
                    )
                )

            except Exception:

                importance = 1

            importance = max(
                1,
                min(
                    5,
                    importance,
                ),
            )

            if not subject:
                continue

            if not description:
                continue

            key = (
                subject.lower()
                + "|"
                + description.lower()
            )

            if key in seen:
                continue

            seen.add(key)

            result.append(
                {
                    "subject": subject,
                    "description": description,
                    "reason": reason,
                    "importance": importance,
                }
            )

    return result


# ======================================================================
# GRAPH
# ======================================================================

def save_graph(
    target_date: date,
    relationships: list[dict],
) -> Path:

    path = (
        GRAPH
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / (
            target_date.strftime(
                "%Y-%m-%d"
            )
            + ".md"
        )
    )

    rows = []

    rows.append(
        "---"
    )

    rows.append(
        f"date: {target_date.isoformat()}"
    )

    rows.append(
        "type: knowledge_graph"
    )

    rows.append(
        "status: generated"
    )

    rows.append(
        "---"
    )

    rows.append("")

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
        + "\n",
    )

    return path


# ======================================================================
# KNOWLEDGE GAPS FILE
# ======================================================================

def save_knowledge_gaps(
    target_date: date,
    gaps: list[dict],
) -> Path | None:

    if not gaps:
        return None

    directory = (
        KNOWLEDGE
        / "主题"
        / "知识缺口"
    )

    path = (
        directory
        / (
            target_date.isoformat()
            + ".md"
        )
    )

    rows = [
        "---",
        f"date: {target_date.isoformat()}",
        "type: knowledge_gaps",
        "status: active",
        "---",
        "",
        f"# {target_date.isoformat()} 知识缺口",
        "",
    ]

    for index, item in enumerate(
        gaps,
        start=1,
    ):

        rows.append(
            f"## {index}. "
            f"{item['question']}"
        )

        rows.append("")

        rows.append(
            f"- 重要性："
            f"{item['importance']}"
        )

        if item["reason"]:

            rows.append(
                f"- 原因："
                f"{item['reason']}"
            )

        rows.append("")

    atomic_write(
        path,
        "\n".join(rows)
        + "\n",
    )

    return path


# ======================================================================
# CONTRADICTIONS FILE
# ======================================================================

def save_contradictions(
    target_date: date,
    contradictions: list[dict],
) -> Path | None:

    if not contradictions:
        return None

    directory = (
        KNOWLEDGE
        / "主题"
        / "知识矛盾"
    )

    path = (
        directory
        / (
            target_date.isoformat()
            + ".md"
        )
    )

    rows = [
        "---",
        f"date: {target_date.isoformat()}",
        "type: knowledge_contradictions",
        "status: needs_verification",
        "---",
        "",
        f"# {target_date.isoformat()} 知识矛盾",
        "",
    ]

    for index, item in enumerate(
        contradictions,
        start=1,
    ):

        rows.append(
            f"## {index}. "
            f"{item['subject']}"
        )

        rows.append("")

        rows.append(
            f"- 重要性："
            f"{item['importance']}"
        )

        rows.append(
            f"- 描述："
            f"{item['description']}"
        )

        if item["reason"]:

            rows.append(
                f"- 需要验证的原因："
                f"{item['reason']}"
            )

        rows.append("")

    atomic_write(
        path,
        "\n".join(rows)
        + "\n",
    )

    return path


# ======================================================================
# COMPLETE MARKER
# ======================================================================

def complete_marker(
    target_date: date,
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
    stats: dict,
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
        indent=2,
    )

    atomic_write(
        marker,
        content,
    )


# ======================================================================
# PROCESS ONE DATE
# ======================================================================

def process_date(
    target_date: date,
) -> bool:

    print()
    print("=" * 70)

    print(
        "KNOWLEDGE ASSET DATE"
    )

    print(
        f"DATE : {target_date}"
    )

    print("=" * 70)

    marker = complete_marker(
        target_date
    )

    # --------------------------------------------------------------
    # COMPLETE
    # --------------------------------------------------------------

    if is_nonempty_file(marker):

        print(
            "⏭️ ASSETS ALREADY COMPLETE"
        )

        print(
            f"   {target_date}"
        )

        return True

    # --------------------------------------------------------------
    # TASK 4
    # --------------------------------------------------------------

    analysis_files = (
        get_analysis_files(
            target_date
        )
    )

    total_analysis = (
        len(analysis_files["en"])
        + len(analysis_files["zh"])
    )

    print(
        f"Task 4 Analysis : "
        f"{total_analysis}"
    )

    print(
        f"   en : "
        f"{len(analysis_files['en'])}"
    )

    print(
        f"   zh : "
        f"{len(analysis_files['zh'])}"
    )

    if total_analysis == 0:

        print(
            "⏭️ 本日没有 Task 4 Analysis"
        )

        print(
            "   不创建伪知识资产。"
        )

        return False

    # --------------------------------------------------------------
    # GROUP EVENTS
    # --------------------------------------------------------------

    event_groups = group_event_files(
        analysis_files
    )

    print(
        f"Unique Events : "
        f"{len(event_groups)}"
    )

    # --------------------------------------------------------------
    # DAILY
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
            30000,
        )

    else:

        print(
            "ℹ️ 本日日报不存在。"
        )

        print(
            "   继续根据 Task 4 Analysis 编译。"
        )

    # --------------------------------------------------------------
    # STATS
    # --------------------------------------------------------------

    stats = {
        "analysis_files":
            total_analysis,
        "unique_events":
            len(event_groups),
        "processed_events":
            0,
        "knowledge_created":
            0,
        "knowledge_updated":
            0,
        "knowledge_skipped":
            0,
        "knowledge_duplicate":
            0,
        "relationships":
            0,
        "knowledge_gaps":
            0,
        "contradictions":
            0,
    }

    all_results = []

    # --------------------------------------------------------------
    # EVENT LOOP
    # --------------------------------------------------------------

    for index, event in enumerate(
        event_groups,
        start=1,
    ):

        event_id = event[
            "event_id"
        ]

        print()
        print(
            f"[{index}/{len(event_groups)}] "
            f"PROCESSING EVENT"
        )

        print(
            f"   EVENT : {event_id}"
        )

        print(
            f"   en    : "
            f"{event['en'].name if event['en'] else '-'}"
        )

        print(
            f"   zh    : "
            f"{event['zh'].name if event['zh'] else '-'}"
        )

        # ----------------------------------------------------------
        # READ
        # ----------------------------------------------------------

        prompt = build_event_prompt(
            event_id,
            event["en"],
            event["zh"],
            daily_text,
        )

        # ----------------------------------------------------------
        # AI
        # ----------------------------------------------------------

        raw_result = call_ai(
            prompt
        )

        # ----------------------------------------------------------
        # JSON
        # ----------------------------------------------------------

        result = extract_json(
            raw_result
        )

        all_results.append(
            result
        )

        stats[
            "processed_events"
        ] += 1

        # ----------------------------------------------------------
        # KNOWLEDGE
        # ----------------------------------------------------------

        assets = normalize_assets(
            result,
            event_id,
        )

        for asset in assets:

            status, saved = (
                save_knowledge_asset(
                    asset,
                    target_date,
                )
            )

            if status == "created":

                stats[
                    "knowledge_created"
                ] += 1

                print(
                    "   ✅ CREATE"
                )

            elif status == "updated":

                stats[
                    "knowledge_updated"
                ] += 1

                print(
                    "   🔄 UPDATE"
                )

            elif status == "duplicate":

                stats[
                    "knowledge_duplicate"
                ] += 1

            elif status == "skipped":

                stats[
                    "knowledge_skipped"
                ] += 1

            if saved:

                print(
                    f"      {saved}"
                )

    # ==================================================================
    # RELATIONSHIPS
    # ==================================================================

    relationships = normalize_relationships(
        all_results
    )

    stats[
        "relationships"
    ] = len(relationships)

    graph_path = save_graph(
        target_date,
        relationships,
    )

    print()
    print(
        f"✅ Graph saved: {graph_path}"
    )

    # ==================================================================
    # KNOWLEDGE GAPS
    # ==================================================================

    gaps = normalize_gaps(
        all_results
    )

    stats[
        "knowledge_gaps"
    ] = len(gaps)

    gap_path = save_knowledge_gaps(
        target_date,
        gaps,
    )

    if gap_path:

        print(
            f"✅ Knowledge gaps saved: "
            f"{gap_path}"
        )

    # ==================================================================
    # CONTRADICTIONS
    # ==================================================================

    contradictions = (
        normalize_contradictions(
            all_results
        )
    )

    stats[
        "contradictions"
    ] = len(contradictions)

    contradiction_path = (
        save_contradictions(
            target_date,
            contradictions,
        )
    )

    if contradiction_path:

        print(
            f"⚠️ Contradictions saved: "
            f"{contradiction_path}"
        )

    # ==================================================================
    # COMPLETE
    # ==================================================================

    mark_complete(
        target_date,
        stats,
    )

    print()
    print(
        "=" * 70
    )

    print(
        "✅ KNOWLEDGE ASSET DATE COMPLETE"
    )

    print(
        f"DATE : {target_date}"
    )

    print(
        f"Events          : "
        f"{stats['processed_events']}"
    )

    print(
        f"Created         : "
        f"{stats['knowledge_created']}"
    )

    print(
        f"Updated         : "
        f"{stats['knowledge_updated']}"
    )

    print(
        f"Skipped         : "
        f"{stats['knowledge_skipped']}"
    )

    print(
        f"Duplicate       : "
        f"{stats['knowledge_duplicate']}"
    )

    print(
        f"Relationships    : "
        f"{stats['relationships']}"
    )

    print(
        f"Knowledge gaps  : "
        f"{stats['knowledge_gaps']}"
    )

    print(
        f"Contradictions  : "
        f"{stats['contradictions']}"
    )

    print(
        "=" * 70
    )

    return True


# ======================================================================
# TARGET DATES
# ======================================================================

def get_target_dates() -> list[date]:

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
        "748686 KNOWLEDGE ASSET COMPILER V2.0"
    )

    print("=" * 70)

    print(
        "Current time : "
        + current.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
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

    # --------------------------------------------------------------
    # STRICT DATE ORDER
    # --------------------------------------------------------------

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
