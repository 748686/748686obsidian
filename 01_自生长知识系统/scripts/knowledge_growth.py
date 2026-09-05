#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Growth Engine

职责
======================================================================
对已经形成的知识库进行周期性健康检查。

输入
======================================================================
05_日报
06_周报
07_专题报告
08_知识库
09_知识图谱
00_System/knowledge_growth_queue

输出
======================================================================
00_System/
└── knowledge_growth/
    ├── YYYY-MM-DD.json
    └── YYYY-MM-DD.md

检查类型
======================================================================
NEW
UPDATE
CONFLICT
MISSING
RELATION
RESEARCH
ARTICLE_CANDIDATE
REPORT_CANDIDATE

重要原则
======================================================================
Growth 不直接删除知识。
Growth 不直接覆盖冲突知识。
Growth 不允许 AI 自己决定任意文件路径。
Growth 首先发现问题，然后形成增长队列。

这对应 Karpathy LLM Knowledge Base 的核心：
知识库不仅被写入，还需要持续 lint / health check，
发现缺失、矛盾和新的关联。
"""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent

DAILY_DIR = ROOT_DIR / "05_日报"
WEEKLY_DIR = ROOT_DIR / "06_周报"
REPORT_DIR = ROOT_DIR / "07_专题报告"
KNOWLEDGE_DIR = ROOT_DIR / "08_知识库"
GRAPH_DIR = ROOT_DIR / "09_知识图谱"

QUEUE_DIR = (
    ROOT_DIR
    / "00_System"
    / "knowledge_growth_queue"
)

GROWTH_DIR = (
    ROOT_DIR
    / "00_System"
    / "knowledge_growth"
)

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


# ======================================================================
# UTIL
# ======================================================================

def log(message: str) -> None:
    print(message, flush=True)


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
) -> Any:

    if not path.exists():
        return None

    try:

        return json.loads(
            read_text(path)
        )

    except Exception:

        return None


# ======================================================================
# RECENT DOCUMENTS
# ======================================================================

def recent_files(
    directory: Path,
    days: int = 7,
) -> list[Path]:

    if not directory.exists():
        return []

    cutoff = datetime.now() - timedelta(
        days=days
    )

    result = []

    for path in directory.rglob("*"):

        if not path.is_file():
            continue

        try:

            modified = datetime.fromtimestamp(
                path.stat().st_mtime
            )

        except OSError:

            continue

        if modified >= cutoff:
            result.append(path)

    return sorted(
        result,
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


# ======================================================================
# KNOWLEDGE INDEX
# ======================================================================

def build_knowledge_index() -> list[dict[str, str]]:

    result = []

    if not KNOWLEDGE_DIR.exists():
        return result

    for path in KNOWLEDGE_DIR.rglob(
        "*.md"
    ):

        relative = path.relative_to(
            KNOWLEDGE_DIR
        )

        text = read_text(path)

        title = path.stem

        match = re.search(
            r"^#\s+(.+)$",
            text,
            re.MULTILINE,
        )

        if match:
            title = match.group(1).strip()

        result.append(
            {
                "title": title,
                "path": str(relative),
                "content": text[:6000],
            }
        )

    return result


# ======================================================================
# GRAPH
# ======================================================================

def load_graph() -> str:

    path = (
        GRAPH_DIR
        / "relations.jsonl"
    )

    if not path.exists():
        return ""

    return read_text(path)[
        :30000
    ]


# ======================================================================
# QUEUE
# ======================================================================

def load_queues() -> dict[str, Any]:

    result = {}

    if not QUEUE_DIR.exists():
        return result

    for path in QUEUE_DIR.glob(
        "*.json"
    ):

        data = load_json(path)

        if data is not None:
            result[path.stem] = data

    return result


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

    response = (
        client.chat.completions.create(
            model=AGNES_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是748686知识库健康检查器。"
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


# ======================================================================
# PROMPT
# ======================================================================

def build_prompt(
    knowledge_index: list[dict[str, str]],
    graph: str,
    queues: dict[str, Any],
    recent_daily: list[Path],
    recent_weekly: list[Path],
) -> str:

    knowledge_text = "\n\n".join(
        [
            (
                f"PATH: {item['path']}\n"
                f"TITLE: {item['title']}\n"
                f"{item['content']}"
            )
            for item in knowledge_index
        ]
    )

    daily_text = "\n\n".join(
        [
            read_text(path)[:8000]
            for path in recent_daily[:7]
        ]
    )

    weekly_text = "\n\n".join(
        [
            read_text(path)[:12000]
            for path in recent_weekly[:2]
        ]
    )

    queue_text = json.dumps(
        queues,
        ensure_ascii=False,
        indent=2,
    )

    return f"""
你是748686自生长知识系统的 Knowledge Growth Engine。

你的任务不是重新总结新闻。

你的任务是对知识库进行 Health Check。

核心思想：

原始资料经过LLM编译成为长期知识后，
知识库应该持续被检查：

- 是否出现新知识
- 是否存在知识缺口
- 是否出现冲突
- 是否产生新的实体关系
- 是否出现值得研究的问题
- 是否值得形成文章
- 是否值得形成专题报告

不要编造事实。

如果没有充分证据，不要判定为事实。

请严格输出JSON：

{{
  "growth_items": [
    {{
      "type": "NEW|UPDATE|CONFLICT|MISSING|RELATION|RESEARCH|ARTICLE_CANDIDATE|REPORT_CANDIDATE",
      "priority": "HIGH|MEDIUM|LOW",
      "subject": "对象",
      "description": "发现的问题或机会",
      "evidence": [
        "证据"
      ],
      "recommended_action": "建议下一步"
    }}
  ],
  "health": {{
    "overall": "HEALTHY|ATTENTION|CRITICAL",
    "summary": "总体状态",
    "missing_count": 0,
    "conflict_count": 0,
    "relation_count": 0
  }}
}}

规则：

1. 不允许凭空创造知识。
2. 不允许删除知识。
3. 不允许直接修改知识库。
4. 冲突必须保留为 CONFLICT。
5. 信息不足时使用 MISSING。
6. 发现潜在联系但证据不足时使用 RELATION 或 RESEARCH。
7. ARTICLE_CANDIDATE 表示值得形成长期文章。
8. REPORT_CANDIDATE 表示值得形成专题。
9. HIGH 只用于真正重要的问题。
10. 每个 growth item 必须尽可能给出 evidence。

==============================
KNOWLEDGE BASE
==============================

{knowledge_text}

==============================
GRAPH
==============================

{graph}

==============================
RECENT DAILY
==============================

{daily_text}

==============================
RECENT WEEKLY
==============================

{weekly_text}

==============================
EXISTING QUEUES
==============================

{queue_text}
"""


# ======================================================================
# SAVE
# ======================================================================

def save_growth(
    date_str: str,
    result: dict[str, Any],
) -> None:

    GROWTH_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    json_path = (
        GROWTH_DIR
        / f"{date_str}.json"
    )

    md_path = (
        GROWTH_DIR
        / f"{date_str}.md"
    )

    write_text(
        json_path,
        json.dumps(
            result,
            ensure_ascii=False,
            indent=2,
        ),
    )

    health = result.get(
        "health",
        {},
    )

    items = result.get(
        "growth_items",
        [],
    )

    lines = [
        f"# Knowledge Growth | {date_str}",
        "",
        "## Health",
        "",
        f"**状态：** "
        f"{health.get('overall', 'UNKNOWN')}",
        "",
        health.get(
            "summary",
            "",
        ),
        "",
        "## Growth Items",
        "",
    ]

    if not items:

        lines.append(
            "暂无新的知识增长任务。"
        )

    else:

        for index, item in enumerate(
            items,
            start=1,
        ):

            lines.extend(
                [
                    f"### {index}. "
                    f"{item.get('type', 'UNKNOWN')} "
                    f"| "
                    f"{item.get('priority', 'LOW')}",
                    "",
                    f"**对象：** "
                    f"{item.get('subject', '')}",
                    "",
                    f"**发现：** "
                    f"{item.get('description', '')}",
                    "",
                    "**证据：**",
                    "",
                ]
            )

            for evidence in item.get(
                "evidence",
                [],
            ):

                lines.append(
                    f"- {evidence}"
                )

            lines.extend(
                [
                    "",
                    f"**建议：** "
                    f"{item.get('recommended_action', '')}",
                    "",
                ]
            )

    write_text(
        md_path,
        "\n".join(lines),
    )


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    date_str = datetime.now().strftime(
        "%Y-%m-%d"
    )

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE GROWTH")
    log("=" * 70)

    knowledge_index = (
        build_knowledge_index()
    )

    log(
        f"Knowledge files: "
        f"{len(knowledge_index)}"
    )

    graph = load_graph()

    queues = load_queues()

    recent_daily = recent_files(
        DAILY_DIR,
        days=7,
    )

    recent_weekly = recent_files(
        WEEKLY_DIR,
        days=14,
    )

    prompt = build_prompt(
        knowledge_index,
        graph,
        queues,
        recent_daily,
        recent_weekly,
    )

    raw = ai_generate(
        prompt
    )

    result = json.loads(raw)

    save_growth(
        date_str,
        result,
    )

    health = result.get(
        "health",
        {},
    )

    items = result.get(
        "growth_items",
        [],
    )

    log("")
    log(
        f"Health       : "
        f"{health.get('overall', 'UNKNOWN')}"
    )

    log(
        f"Growth Items : "
        f"{len(items)}"
    )

    log(
        f"Saved        : "
        f"{GROWTH_DIR / date_str}.md"
    )

    log("")
    log(
        "✅ KNOWLEDGE GROWTH COMPLETE"
    )


if __name__ == "__main__":
    main()
