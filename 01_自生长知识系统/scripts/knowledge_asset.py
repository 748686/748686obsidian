#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Asset Compiler

职责
======================================================================
读取最近三天 Task 4 Analysis，
提取长期知识资产，并增量更新：

01_新闻
02_资料
03_文章
04_图片
07_专题报告
08_知识库
09_知识图谱

核心原则
======================================================================
AI负责：
    知识识别
    实体提取
    关系提取
    内容编译

Python负责：
    文件路径
    文件命名
    JSON
    增量合并
    去重
    安全写入

绝不允许：
    AI直接决定任意文件路径
    自动删除旧知识
    自动覆盖冲突知识
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

RAW_NEWS_DIR = ROOT_DIR / "Raw News"
DAILY_DIR = ROOT_DIR / "05_日报"

NEWS_DIR = ROOT_DIR / "01_新闻"
MATERIAL_DIR = ROOT_DIR / "02_资料"
ARTICLE_DIR = ROOT_DIR / "03_文章"
IMAGE_DIR = ROOT_DIR / "04_图片"
REPORT_DIR = ROOT_DIR / "07_专题报告"
KNOWLEDGE_DIR = ROOT_DIR / "08_知识库"
GRAPH_DIR = ROOT_DIR / "09_知识图谱"

SUPPORTED_LANGUAGES = ("en", "zh")


# ======================================================================
# AI
# ======================================================================

AGNES_BASE_URL = os.getenv(
    "AGNES_BASE_URL",
    "https://api.agnes-ai.cn/v1",
)

AGNES_MODEL = os.getenv(
    "AGNES_MODEL",
    "agnes-2.5-flash",
)

AGNES_API_KEY = os.getenv(
    "AGNES_API_KEY"
)

AI_TIMEOUT = int(
    os.getenv(
        "KNOWLEDGE_AI_TIMEOUT",
        "180",
    )
)

AI_RETRIES = int(
    os.getenv(
        "KNOWLEDGE_AI_RETRIES",
        "3",
    )
)


# ======================================================================
# LOG
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


# ======================================================================
# DATE
# ======================================================================

def target_dates() -> list[str]:

    now = datetime.now()

    return [
        (now - timedelta(days=2)).strftime(
            "%Y-%m-%d"
        ),
        (now - timedelta(days=1)).strftime(
            "%Y-%m-%d"
        ),
        now.strftime(
            "%Y-%m-%d"
        ),
    ]


# ======================================================================
# FILE
# ======================================================================

def read_text(path: Path) -> str:

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def write_text(
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

    tmp.write_text(
        content,
        encoding="utf-8",
    )

    tmp.replace(path)


def load_json(
    path: Path,
    default: Any,
) -> Any:

    if not path.exists():
        return default

    try:

        return json.loads(
            read_text(path)
        )

    except Exception:

        return default


def save_json(
    path: Path,
    data: Any,
) -> None:

    write_text(
        path,
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ),
    )


# ======================================================================
# ANALYSIS DISCOVERY
# ======================================================================

def discover_analysis(
    date_str: str,
) -> list[dict[str, Any]]:

    results = []

    root = (
        RAW_NEWS_DIR
        / f"{date_str}-EventUnit"
    )

    for language in SUPPORTED_LANGUAGES:

        directory = (
            root
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

            content = read_text(path)

            if not content.strip():
                continue

            match = re.search(
                r"(EVT-\d{8}-\d{6})",
                path.name,
            )

            event_id = (
                match.group(1)
                if match
                else path.stem
            )

            results.append(
                {
                    "date": date_str,
                    "language": language,
                    "event_id": event_id,
                    "path": str(path),
                    "content": content,
                }
            )

    return results


# ======================================================================
# AI
# ======================================================================

def ai_generate(
    prompt: str,
) -> str:

    if not AGNES_API_KEY:
        raise RuntimeError(
            "AGNES_API_KEY is not configured."
        )

    from openai import OpenAI

    client = OpenAI(
        api_key=AGNES_API_KEY,
        base_url=AGNES_BASE_URL,
        timeout=AI_TIMEOUT,
    )

    last_error = None

    for attempt in range(
        1,
        AI_RETRIES + 1,
    ):

        try:

            response = (
                client.chat.completions.create(
                    model=AGNES_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "你是748686知识资产编译器。"
                                "必须严格输出JSON。"
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.1,
                )
            )

            text = (
                response
                .choices[0]
                .message
                .content
                .strip()
            )

            if text.startswith("```"):
                text = re.sub(
                    r"^```(?:json)?",
                    "",
                    text.strip(),
                )

                text = re.sub(
                    r"```$",
                    "",
                    text.strip(),
                )

            json.loads(text)

            return text

        except Exception as exc:

            last_error = exc

            log(
                f"⚠️ ASSET AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            if attempt < AI_RETRIES:
                time.sleep(
                    3 * attempt
                )

    raise RuntimeError(
        f"Asset AI failed: {last_error}"
    )


# ======================================================================
# PROMPT
# ======================================================================

def build_asset_prompt(
    date_str: str,
    analyses: list[dict[str, Any]],
) -> str:

    context = "\n\n".join(
        [
            (
                f"EVENT_ID: {x['event_id']}\n"
                f"LANGUAGE: {x['language']}\n"
                f"{x['content']}"
            )
            for x in analyses
        ]
    )

    return f"""
你是748686自生长知识系统的“知识资产编译器”。

日期：
{date_str}

输入是已经通过 Task 4 的事件分析。

你的任务不是写日报。

你的任务是从这些分析中识别应该进入长期知识库的稳定知识。

只能根据输入内容提取，不允许凭空补充事实。

请输出严格JSON：

{{
  "entities": [
    {{
      "name": "实体名称",
      "type": "公司|人物|产品|技术|概念|行业|主题",
      "summary": "稳定、长期有效的知识描述",
      "facts": [
        "事实1",
        "事实2"
      ],
      "event_ids": [
        "EVT-..."
      ]
    }}
  ],
  "relations": [
    {{
      "source": "实体A",
      "relation": "关系",
      "target": "实体B",
      "event_ids": [
        "EVT-..."
      ]
    }}
  ],
  "article_candidates": [
    {{
      "title": "文章标题",
      "reason": "为什么值得形成长期文章",
      "event_ids": []
    }}
  ],
  "report_candidates": [
    {{
      "title": "专题标题",
      "type": "决策分析|市场分析|战略分析|综合报告|行业分析",
      "reason": "为什么值得形成专题",
      "event_ids": []
    }}
  ],
  "missing_knowledge": [
    {{
      "topic": "缺失知识",
      "reason": "为什么需要补充"
    }}
  ],
  "conflicts": [
    {{
      "topic": "冲突对象",
      "description": "冲突内容"
    }}
  ]
}}

重要：

1. entity name必须稳定。
2. 同一个实体不能因为中英文不同重复创建。
3. 不要把一次性事件当成实体。
4. 关系必须有输入依据。
5. 不确定的信息进入 conflicts 或 missing_knowledge。
6. 不要删除旧知识。
7. 不要生成任何文件路径。

输入：

{context}
"""


# ======================================================================
# NORMALIZE
# ======================================================================

def normalize_name(
    name: str,
) -> str:

    name = name.strip()

    name = re.sub(
        r"\s+",
        " ",
        name,
    )

    return name


def safe_filename(
    name: str,
) -> str:

    name = normalize_name(name)

    name = re.sub(
        r'[\\/:*?"<>|]',
        "_",
        name,
    )

    return name[:100]


# ======================================================================
# ENTITY PATH
# ======================================================================

ENTITY_DIRS = {
    "公司": KNOWLEDGE_DIR / "公司",
    "人物": KNOWLEDGE_DIR / "人物",
    "产品": KNOWLEDGE_DIR / "产品",
    "技术": KNOWLEDGE_DIR / "技术",
    "概念": KNOWLEDGE_DIR / "概念",
    "行业": KNOWLEDGE_DIR / "行业",
    "主题": KNOWLEDGE_DIR / "主题",
}


# ======================================================================
# ENTITY UPDATE
# ======================================================================

def update_entity(
    entity: dict[str, Any],
    date_str: str,
) -> None:

    name = normalize_name(
        entity["name"]
    )

    entity_type = entity["type"]

    directory = ENTITY_DIRS.get(
        entity_type
    )

    if directory is None:
        return

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        directory
        / f"{safe_filename(name)}.md"
    )

    old = ""

    if path.exists():
        old = read_text(path)

    facts = entity.get(
        "facts",
        [],
    )

    event_ids = entity.get(
        "event_ids",
        [],
    )

    new_block = f"""

## 知识更新｜{date_str}

{entity.get("summary", "").strip()}

### 新增事实

"""

    for fact in facts:
        new_block += f"- {fact}\n"

    new_block += "\n### 来源事件\n\n"

    for event_id in event_ids:
        new_block += (
            f"- [[{event_id}]]\n"
        )

    if not old:

        content = (
            f"# {name}\n\n"
            f"类型：{entity_type}\n"
            f"{new_block}"
        )

    else:

        if new_block.strip() in old:
            return

        content = (
            old.rstrip()
            + "\n"
            + new_block
        )

    write_text(
        path,
        content,
    )

    log(
        f"✅ KNOWLEDGE UPDATED | "
        f"{entity_type} | {name}"
    )


# ======================================================================
# GRAPH
# ======================================================================

def update_graph(
    relations: list[dict[str, Any]],
) -> None:

    GRAPH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    graph_path = (
        GRAPH_DIR
        / "relations.jsonl"
    )

    existing = set()

    if graph_path.exists():

        for line in graph_path.read_text(
            encoding="utf-8"
        ).splitlines():

            if line.strip():
                existing.add(
                    line.strip()
                )

    with graph_path.open(
        "a",
        encoding="utf-8",
    ) as f:

        for relation in relations:

            record = json.dumps(
                relation,
                ensure_ascii=False,
                sort_keys=True,
            )

            if record in existing:
                continue

            f.write(
                record + "\n"
            )

            existing.add(record)

    log(
        f"✅ GRAPH UPDATED | "
        f"{len(relations)} relations"
    )


# ======================================================================
# CANDIDATE QUEUE
# ======================================================================

def append_queue(
    filename: str,
    records: list[dict[str, Any]],
) -> None:

    if not records:
        return

    queue_dir = (
        ROOT_DIR
        / "00_System"
        / "knowledge_growth_queue"
    )

    queue_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    path = (
        queue_dir
        / filename
    )

    existing = []

    if path.exists():

        try:
            existing = json.loads(
                read_text(path)
            )
        except Exception:
            existing = []

    existing.extend(
        records
    )

    save_json(
        path,
        existing,
    )


# ======================================================================
# PROCESS
# ======================================================================

def process_date(
    date_str: str,
) -> None:

    log("")
    log("=" * 70)
    log(
        f"KNOWLEDGE ASSET | {date_str}"
    )
    log("=" * 70)

    analyses = discover_analysis(
        date_str
    )

    log(
        f"Analysis files: "
        f"{len(analyses)}"
    )

    if not analyses:
        return

    prompt = build_asset_prompt(
        date_str,
        analyses,
    )

    raw = ai_generate(
        prompt
    )

    result = json.loads(raw)

    entities = result.get(
        "entities",
        [],
    )

    relations = result.get(
        "relations",
        [],
    )

    article_candidates = result.get(
        "article_candidates",
        [],
    )

    report_candidates = result.get(
        "report_candidates",
        [],
    )

    missing = result.get(
        "missing_knowledge",
        [],
    )

    conflicts = result.get(
        "conflicts",
        [],
    )

    log(
        f"Entities     : {len(entities)}"
    )

    log(
        f"Relations    : {len(relations)}"
    )

    log(
        f"Articles     : "
        f"{len(article_candidates)}"
    )

    log(
        f"Reports      : "
        f"{len(report_candidates)}"
    )

    log(
        f"Missing      : {len(missing)}"
    )

    log(
        f"Conflicts    : {len(conflicts)}"
    )

    for entity in entities:

        update_entity(
            entity,
            date_str,
        )

    update_graph(
        relations
    )

    append_queue(
        "article_candidates.json",
        article_candidates,
    )

    append_queue(
        "report_candidates.json",
        report_candidates,
    )

    append_queue(
        "missing_knowledge.json",
        missing,
    )

    append_queue(
        "conflicts.json",
        conflicts,
    )


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE ASSET COMPILER")
    log("=" * 70)

    for date_str in target_dates():

        process_date(
            date_str
        )

    log("")
    log(
        "✅ KNOWLEDGE ASSET COMPLETE"
    )


if __name__ == "__main__":
    main()
