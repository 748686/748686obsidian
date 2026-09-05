#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Daily — Layered Daily Report Compiler

VERSION: V4.0

======================================================================
核心架构
======================================================================

Task 4
    ↓
大量 Event Analysis
    ↓
Event ID 去重
    ↓
Batch Compression
    ↓
Batch 01
Batch 02
Batch 03
...
    ↓
Intermediate Brief
    ↓
Final Daily Report AI
    ↓
05_日报/YYYY/MM/YYYY-MM-DD.md


======================================================================
V4.0 核心修复
======================================================================

旧架构：

    570 Analysis
        ↓
    一个巨大 Prompt
        ↓
    Final Daily AI
        ↓
    HTTP 400 / Context 过大


新架构：

    570 Analysis
        ↓
    分批压缩
        ↓
    Batch 01
    Batch 02
    ...
        ↓
    Intermediate Brief
        ↓
    Final Daily AI


======================================================================
DATE CONTRACT
======================================================================

本程序绝不自行计算业务日期。

业务日期必须由外层 Workflow / Task 4 日期契约传入：

    --day-before YYYY-MM-DD
    --yesterday YYYY-MM-DD
    --today YYYY-MM-DD

例如：

    --day-before 2026-09-03
    --yesterday  2026-09-04
    --today      2026-09-05

本程序随后严格处理：

    2026-09-03
    2026-09-04
    2026-09-05

禁止：

    datetime.now() 决定业务日期
    Asia/Shanghai 决定业务日期
    系统当前日期决定业务日期


======================================================================
LANGUAGE CONTRACT
======================================================================

Task 4 仍然严格使用：

    en
    zh

本 Daily 模块读取：

    Raw News/YYYY-MM-DD-EventUnit/en/event_units/
    Raw News/YYYY-MM-DD-EventUnit/zh/event_units/

不进行大小写转换。

======================================================================
EVENT DEDUPLICATION
======================================================================

同一个 Event ID 可能同时存在：

    en Analysis
    zh Analysis

Daily 层只把它视为一个 Event。

优先：

    zh

如果 zh 不存在：

    en

这样避免最终日报重复报道同一个事件。

======================================================================
BATCH CONTRACT
======================================================================

默认：

    15 个 Event Analysis / Batch

每个 Analysis 在 Batch Prompt 中最多读取：

    3500 字符

Batch AI 只负责：

    压缩
    提取
    去除低价值细节
    保留重要事实
    保留 Event ID
    保留来源信息
    保留关键数字
    保留人物 / 公司 / 产品
    保留重大变化
    保留趋势 / 异常

Batch AI 不负责：

    写最终日报
    编造事实
    改写成最终日报结构


======================================================================
INTERMEDIATE CONTRACT
======================================================================

所有 Batch Summary 完成后：

    Batch 01
    Batch 02
    ...
        ↓
    Intermediate Brief AI

Intermediate AI 负责：

    1. 跨 Batch 去重
    2. 合并同一事件
    3. 判断重要性
    4. 提炼当天核心变化
    5. 形成日报核心素材
    6. 区分事实 / 分析
    7. 保留关键 Event ID

Intermediate Brief 仍然不是最终日报。


======================================================================
FINAL DAILY REPORT
======================================================================

最终 AI 同时读取：

    日报 Skill
    +
    Intermediate Brief
    +
    必要的统计信息

并严格按照：

    Skills/05.汇报写作/日报编写助手.md

生成最终日报。


======================================================================
OUTPUT
======================================================================

最终：

    05_日报/YYYY/MM/YYYY-MM-DD.md


======================================================================
IDEMPOTENCE
======================================================================

已有非空日报：

    SKIP

已有非空 Batch Summary：

    REUSE

已有非空 Intermediate Brief：

    REUSE

只有缺失内容才继续调用 AI。


======================================================================
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime

from knowledge_common import (
    ROOT,
    SKILLS,
    RAW_NEWS,
    REPORTS,
    call_ai,
    event_units_dir,
    now,
    write_text_atomic,
)


# ======================================================================
# VERSION
# ======================================================================

VERSION = "V4.0"


# ======================================================================
# CONFIG
# ======================================================================

BATCH_SIZE = 15

MAX_ANALYSIS_CHARS = 3500

MAX_BATCH_SUMMARY_CHARS = 12000

MAX_INTERMEDIATE_BATCH_CHARS = 14000

MAX_FINAL_INPUT_CHARS = 45000


# ======================================================================
# PATHS
# ======================================================================

DAILY_SKILL_PATH = (
    SKILLS
    / "05.汇报写作"
    / "日报编写助手.md"
)


DAILY_RUNTIME_ROOT = (
    ROOT
    / "00_System"
    / "运行日志"
    / "knowledge_daily"
)


# ======================================================================
# DATE VALIDATION
# ======================================================================

DATE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}$"
)


def validate_date(
    date: str,
) -> str:

    if not isinstance(
        date,
        str,
    ):

        raise ValueError(
            f"Invalid date type: {type(date).__name__}"
        )

    if not DATE_RE.fullmatch(
        date
    ):

        raise ValueError(
            f"Invalid date format: {date!r}. "
            "Expected YYYY-MM-DD."
        )

    try:

        datetime.strptime(
            date,
            "%Y-%m-%d",
        )

    except ValueError as exc:

        raise ValueError(
            f"Invalid calendar date: {date!r}"
        ) from exc

    return date


# ======================================================================
# READ / WRITE
# ======================================================================

def read_text(
    path: Path,
) -> str:

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def write_text(
    path: Path,
    text: str,
) -> None:

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    write_text_atomic(
        path,
        text.rstrip() + "\n",
    )


# ======================================================================
# DAILY REPORT PATH
# ======================================================================

def daily_report_path(
    date: str,
) -> Path:

    validate_date(date)

    return (
        REPORTS
        / date[:4]
        / date[5:7]
        / f"{date}.md"
    )


# ======================================================================
# RUNTIME PATH
# ======================================================================

def runtime_dir(
    date: str,
) -> Path:

    validate_date(date)

    return (
        DAILY_RUNTIME_ROOT
        / date
    )


# ======================================================================
# SKILL
# ======================================================================

def load_daily_skill() -> str:

    if not DAILY_SKILL_PATH.exists():

        raise FileNotFoundError(
            "日报 Skill 不存在：\n"
            f"{DAILY_SKILL_PATH}"
        )

    skill = read_text(
        DAILY_SKILL_PATH
    ).strip()

    if not skill:

        raise RuntimeError(
            "日报 Skill 文件为空：\n"
            f"{DAILY_SKILL_PATH}"
        )

    return skill


# ======================================================================
# EVENT ID
# ======================================================================

EVENT_ID_RE = re.compile(
    r"\bEVT-\d{8}-\d{6}\b"
)


def extract_event_id(
    text: str,
    path: Path,
) -> str:

    match = re.search(
        r"(?m)^event_id\s*:\s*([^\s]+)\s*$",
        text,
    )

    if match:

        event_id = match.group(1).strip()

        if EVENT_ID_RE.fullmatch(
            event_id
        ):

            return event_id

    match = EVENT_ID_RE.search(
        text
    )

    if match:

        return match.group(0)

    match = EVENT_ID_RE.search(
        path.name
    )

    if match:

        return match.group(0)

    raise ValueError(
        f"Unable to determine Event ID:\n{path}"
    )


# ======================================================================
# EVENT ANALYSIS DISCOVERY
# ======================================================================

def discover_analysis_files(
    date: str,
) -> dict[str, dict[str, Path]]:

    validate_date(date)

    result: dict[
        str,
        dict[str, Path],
    ] = {}

    for language in (
        "en",
        "zh",
    ):

        directory = (
            event_units_dir(
                date,
                language,
            )
        )

        if not directory.exists():

            raise FileNotFoundError(
                f"Task 4 EventUnit directory "
                f"does not exist:\n{directory}"
            )

        for path in sorted(
            directory.glob(
                "*_analysis.md"
            )
        ):

            if not path.is_file():

                continue

            try:

                text = read_text(
                    path
                )

                if not text.strip():

                    print(
                        f"   ⚠️ EMPTY ANALYSIS | "
                        f"{path}"
                    )

                    continue

                event_id = extract_event_id(
                    text,
                    path,
                )

            except Exception as exc:

                print(
                    f"   ⚠️ INVALID ANALYSIS | "
                    f"{path} | {exc}"
                )

                continue

            result.setdefault(
                event_id,
                {},
            )[language] = path

    return result


# ======================================================================
# DEDUPLICATION
# ======================================================================

def select_canonical_analysis(
    event_id: str,
    language_paths: dict[str, Path],
) -> tuple[str, Path]:

    # ==============================================================
    # 优先 zh
    # ==============================================================

    if "zh" in language_paths:

        return (
            "zh",
            language_paths["zh"],
        )

    if "en" in language_paths:

        return (
            "en",
            language_paths["en"],
        )

    raise RuntimeError(
        f"No analysis available for {event_id}"
    )


# ======================================================================
# LOAD DEDUPED ANALYSES
# ======================================================================

def load_deduplicated_analyses(
    date: str,
) -> list[dict[str, str]]:

    grouped = discover_analysis_files(
        date
    )

    records: list[
        dict[str, str]
    ] = []

    for event_id in sorted(
        grouped.keys()
    ):

        language, path = (
            select_canonical_analysis(
                event_id,
                grouped[event_id],
            )
        )

        text = read_text(
            path
        ).strip()

        if not text:

            continue

        records.append(
            {
                "event_id": event_id,
                "language": language,
                "path": str(path),
                "analysis": text,
            }
        )

    return records


# ======================================================================
# BATCH SPLIT
# ======================================================================

def split_batches(
    records: list[dict[str, str]],
) -> list[list[dict[str, str]]]:

    return [
        records[index:index + BATCH_SIZE]
        for index in range(
            0,
            len(records),
            BATCH_SIZE,
        )
    ]


# ======================================================================
# BATCH SUMMARY PATH
# ======================================================================

def batch_summary_path(
    date: str,
    batch_number: int,
) -> Path:

    return (
        runtime_dir(date)
        / f"batch_{batch_number:03d}.md"
    )


# ======================================================================
# BUILD BATCH PROMPT
# ======================================================================

def build_batch_prompt(
    date: str,
    batch_number: int,
    total_batches: int,
    batch: list[dict[str, str]],
) -> str:

    sections: list[str] = []

    for index, record in enumerate(
        batch,
        start=1,
    ):

        analysis = record[
            "analysis"
        ]

        if len(analysis) > MAX_ANALYSIS_CHARS:

            analysis = (
                analysis[
                    :MAX_ANALYSIS_CHARS
                ]
                + "\n\n[Analysis truncated for batch compression]"
            )

        sections.append(
            f"""
============================================================
EVENT {index}
============================================================

Event ID:
{record["event_id"]}

Language:
{record["language"]}

Analysis:
{analysis}
"""
        )

    source_text = "\n".join(
        sections
    )

    return f"""
你是 748686 自生长知识系统的「日报 Batch Compression Engine」。

当前日报业务日期：

{date}

当前 Batch：

{batch_number} / {total_batches}

你的任务不是写最终日报。

你的任务是把这一批 Event Analysis 压缩成高密度、可靠的日报素材。

============================================================
硬性要求
============================================================

1. 只使用输入的 Event Analysis。
2. 不得编造任何事实。
3. 不得补充输入中不存在的数据。
4. 不得改变事实含义。
5. 不要写最终日报。
6. 不要写开场白。
7. 不要写结尾总结套话。
8. 删除低价值重复内容。
9. 同一事件的重复信息合并。
10. 保留重要 Event ID。
11. 保留关键人物。
12. 保留关键公司 / 机构。
13. 保留关键产品 / 技术。
14. 保留关键数字。
15. 保留重大政策 / 决策 / 行动。
16. 保留明显变化。
17. 保留异常事件。
18. 保留值得进入日报的趋势。
19. 明确区分「事实」和「分析/判断」。
20. 如果某条信息无法确认，不要自行补全。

============================================================
建议输出结构
============================================================

# Batch {batch_number} Summary

## 高重要性事件

逐条列出真正值得进入日报的事件。

每条尽量包含：

- Event ID
- 事件
- 核心事实
- 关键数字
- 关键人物 / 机构
- 变化 / 影响
- 事实与判断区分

## 重要变化

提取本批事件中的重要变化。

## 趋势与信号

只提取输入中有依据的趋势。

## 次要但值得关注

保留少量可能值得最终日报判断的信息。

============================================================
原始 Event Analysis
============================================================

{source_text}

只输出 Batch Summary Markdown。
"""


# ======================================================================
# BATCH SUMMARY
# ======================================================================

def generate_batch_summary(
    date: str,
    batch_number: int,
    total_batches: int,
    batch: list[dict[str, str]],
) -> str:

    path = batch_summary_path(
        date,
        batch_number,
    )

    if (
        path.exists()
        and path.stat().st_size > 0
    ):

        print(
            f"   ♻️ REUSE BATCH SUMMARY | "
            f"{batch_number}/{total_batches}"
        )

        return read_text(
            path
        ).strip()

    print(
        f"   🤖 BATCH COMPRESS | "
        f"{batch_number}/{total_batches} | "
        f"Events={len(batch)}"
    )

    prompt = build_batch_prompt(
        date,
        batch_number,
        total_batches,
        batch,
    )

    result = call_ai(
        prompt
    ).strip()

    if not result:

        raise RuntimeError(
            f"Batch {batch_number} "
            "AI output is empty."
        )

    if len(result) > MAX_BATCH_SUMMARY_CHARS:

        result = (
            result[
                :MAX_BATCH_SUMMARY_CHARS
            ]
            + "\n\n[Batch summary truncated]"
        )

    write_text(
        path,
        result,
    )

    print(
        f"   ✅ BATCH SAVED | {path}"
    )

    return result


# ======================================================================
# INTERMEDIATE PATH
# ======================================================================

def intermediate_path(
    date: str,
) -> Path:

    return (
        runtime_dir(date)
        / "intermediate.md"
    )


# ======================================================================
# BUILD INTERMEDIATE PROMPT
# ======================================================================

def build_intermediate_prompt(
    date: str,
    batch_summaries: list[str],
) -> str:

    sections: list[str] = []

    for index, summary in enumerate(
        batch_summaries,
        start=1,
    ):

        if len(summary) > MAX_INTERMEDIATE_BATCH_CHARS:

            summary = (
                summary[
                    :MAX_INTERMEDIATE_BATCH_CHARS
                ]
                + "\n\n[Batch summary truncated for intermediate merge]"
            )

        sections.append(
            f"""
============================================================
BATCH {index}
============================================================

{summary}
"""
        )

    combined = "\n".join(
        sections
    )

    return f"""
你是 748686 自生长知识系统的「日报 Intermediate Brief Compiler」。

日报业务日期：

{date}

现在已经完成所有 Batch Compression。

你需要把所有 Batch Summary 进一步压缩、去重、合并，形成「日报核心素材」。

============================================================
重要
============================================================

你现在仍然不是在写最终日报。

不要按照最终日报 Skill 写文章。

你的输出将直接提供给下一阶段 Final Daily Report AI。

============================================================
任务
============================================================

1. 跨 Batch 去重。
2. 合并同一事件。
3. 合并同一主题下的相关事件。
4. 判断事件重要性。
5. 提取当天最重要的新事实。
6. 提取当天最重要的变化。
7. 提取重要数字。
8. 提取重要人物 / 公司 / 机构。
9. 提取政策 / 决策 / 行动。
10. 提取技术 / 产品变化。
11. 提取市场 / 行业变化。
12. 提取异常 / 风险信号。
13. 提取跨事件连接。
14. 删除重复和低价值内容。
15. 不得编造。
16. 不得使用 Batch 中没有的信息。
17. 不得把推测写成事实。
18. 尽可能保留 Event ID，方便最终日报追溯。

============================================================
输出结构
============================================================

# Daily Intermediate Brief

## 一、今日最高优先级事件

列出最重要的事件。

## 二、重要事实与变化

按照重要性整理。

## 三、关键人物 / 公司 / 机构

只保留与当天事件直接相关的实体。

## 四、关键数字

只保留有明确来源于输入材料的数字。

## 五、行业 / 市场 / 技术变化

提取有依据的变化。

## 六、政策 / 决策 / 行动

提取重要政策和行动。

## 七、风险 / 异常 / 预警

只保留有依据的信息。

## 八、跨事件连接

指出多个事件之间真正存在的关系。

## 九、值得最终日报重点关注的问题

列出需要 Final Daily AI 特别关注的问题。

============================================================
Batch Summaries
============================================================

{combined}

只输出 Intermediate Brief Markdown。
"""


# ======================================================================
# GENERATE INTERMEDIATE
# ======================================================================

def generate_intermediate(
    date: str,
    batch_summaries: list[str],
) -> str:

    path = intermediate_path(
        date
    )

    if (
        path.exists()
        and path.stat().st_size > 0
    ):

        print(
            f"   ♻️ REUSE INTERMEDIATE | {path}"
        )

        return read_text(
            path
        ).strip()

    print(
        f"   🧠 INTERMEDIATE MERGE | "
        f"Batches={len(batch_summaries)}"
    )

    prompt = build_intermediate_prompt(
        date,
        batch_summaries,
    )

    result = call_ai(
        prompt
    ).strip()

    if not result:

        raise RuntimeError(
            f"{date} Intermediate Brief "
            "AI output is empty."
        )

    write_text(
        path,
        result,
    )

    print(
        f"   ✅ INTERMEDIATE SAVED | {path}"
    )

    return result


# ======================================================================
# FINAL INPUT PATH
# ======================================================================

def final_input_path(
    date: str,
) -> Path:

    return (
        runtime_dir(date)
        / "final_input.md"
    )


# ======================================================================
# BUILD FINAL INPUT
# ======================================================================

def build_final_input(
    date: str,
    intermediate: str,
) -> str:

    if len(intermediate) > MAX_FINAL_INPUT_CHARS:

        intermediate = (
            intermediate[
                :MAX_FINAL_INPUT_CHARS
            ]
            + "\n\n[Intermediate Brief truncated]"
        )

    content = f"""# Daily Report Final Input

业务日期：

{date}

============================================================
Intermediate Brief
============================================================

{intermediate}

============================================================
End Final Input
============================================================
"""

    return content


# ======================================================================
# SAVE FINAL INPUT
# ======================================================================

def save_final_input(
    date: str,
    intermediate: str,
) -> str:

    path = final_input_path(
        date
    )

    if (
        path.exists()
        and path.stat().st_size > 0
    ):

        print(
            f"   ♻️ REUSE FINAL INPUT | {path}"
        )

        return read_text(
            path
        ).strip()

    content = build_final_input(
        date,
        intermediate,
    )

    write_text(
        path,
        content,
    )

    print(
        f"   ✅ FINAL INPUT SAVED | {path}"
    )

    return content


# ======================================================================
# FINAL DAILY PROMPT
# ======================================================================

def build_final_daily_prompt(
    date: str,
    skill: str,
    intermediate: str,
) -> str:

    if len(intermediate) > MAX_FINAL_INPUT_CHARS:

        intermediate = (
            intermediate[
                :MAX_FINAL_INPUT_CHARS
            ]
            + "\n\n[Intermediate Brief truncated]"
        )

    return f"""
你是 748686 自生长知识系统的 Final Daily Report Engine。

现在生成正式日报。

============================================================
日报业务日期
============================================================

{date}

这个日期已经由外层 Workflow / Task 4 日期契约确定。

不得修改日期。

============================================================
日报 Skill
============================================================

下面是系统指定的日报 Skill。

你必须完整遵守这个 Skill 的要求、结构、格式和写作规则：

---------------- SKILL BEGIN ----------------

{skill}

---------------- SKILL END ----------------

============================================================
日报核心素材
============================================================

下面是前面经过 Batch Compression 和 Intermediate Merge
得到的日报核心素材。

这是你生成最终日报的主要信息来源。

---------------- INTERMEDIATE BEGIN ----------------

{intermediate}

---------------- INTERMEDIATE END ----------------

============================================================
最终生成要求
============================================================

1. 严格按照日报 Skill 编写。
2. 不得编造。
3. 只使用提供的核心素材。
4. 不要把没有依据的推测写成事实。
5. 可以对素材进行结构化、排序、归纳和表达优化。
6. 删除明显重复内容。
7. 保留真正重要的事实。
8. 保留关键数字。
9. 保留重要人物 / 公司 / 机构。
10. 保留重大政策 / 决策 / 行动。
11. 保留重要趋势和变化。
12. 如果 Skill 要求特定章节，必须全部遵守。
13. 不要输出任何 AI 工作过程。
14. 不要解释自己如何生成日报。
15. 不要输出「以下是日报」之类的前置说明。
16. 直接输出最终 Markdown。
17. 不要添加虚假的来源。
18. 不要添加输入材料之外的事实。
19. 日报日期必须是：

{date}

只输出最终日报 Markdown。
"""


# ======================================================================
# GENERATE FINAL DAILY REPORT
# ======================================================================

def generate_final_daily_report(
    date: str,
    skill: str,
    intermediate: str,
) -> str:

    report_path = daily_report_path(
        date
    )

    if (
        report_path.exists()
        and report_path.stat().st_size > 0
    ):

        print(
            f"   ⏭️ DAILY REPORT EXISTS | "
            f"{report_path}"
        )

        return read_text(
            report_path
        ).strip()

    print(
        f"   📝 FINAL DAILY AI | {date}"
    )

    prompt = build_final_daily_prompt(
        date,
        skill,
        intermediate,
    )

    result = call_ai(
        prompt
    ).strip()

    if not result:

        raise RuntimeError(
            f"{date} Final Daily Report "
            "AI output is empty."
        )

    write_text(
        report_path,
        result,
    )

    print(
        f"   ✅ DAILY REPORT SAVED | "
        f"{report_path}"
    )

    return result


# ======================================================================
# RUNTIME MANIFEST
# ======================================================================

def runtime_manifest_path(
    date: str,
) -> Path:

    return (
        runtime_dir(date)
        / "manifest.json"
    )


def write_runtime_manifest(
    date: str,
    analysis_count: int,
    batch_count: int,
    report_path: Path,
) -> None:

    payload = {
        "version": VERSION,
        "date": date,
        "analysis_count": analysis_count,
        "batch_size": BATCH_SIZE,
        "batch_count": batch_count,
        "deduplication": "Event ID; zh preferred over en",
        "pipeline": [
            "Task 4 Analysis",
            "Event ID Deduplication",
            "Batch Compression",
            "Intermediate Merge",
            "Final Daily Report AI",
        ],
        "report_path": str(
            report_path
        ),
        "status": "COMPLETE",
        "completed_at": now().isoformat(),
    }

    write_text(
        runtime_manifest_path(date),
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
        ),
    )


# ======================================================================
# PROCESS ONE DATE
# ======================================================================

def process_date(
    date: str,
    daily_skill: str,
) -> None:

    validate_date(
        date
    )

    print()
    print(
        "=" * 70
    )
    print(
        "KNOWLEDGE DAILY — LAYERED COMPILER"
    )
    print(
        "=" * 70
    )
    print(
        f"DATE              : {date}"
    )
    print(
        f"VERSION           : {VERSION}"
    )
    print(
        f"BATCH SIZE        : {BATCH_SIZE}"
    )
    print(
        f"MAX ANALYSIS      : {MAX_ANALYSIS_CHARS} chars"
    )
    print(
        f"DAILY SKILL       : {DAILY_SKILL_PATH}"
    )
    print(
        f"RUNTIME DIR       : {runtime_dir(date)}"
    )
    print(
        "=" * 70
    )

    # ==============================================================
    # Existing final report
    # ==============================================================

    report_path = daily_report_path(
        date
    )

    if (
        report_path.exists()
        and report_path.stat().st_size > 0
    ):

        print()
        print(
            f"⏭️ DAILY REPORT ALREADY EXISTS"
        )
        print(
            f"   {report_path}"
        )

        return

    # ==============================================================
    # Load Task 4 Analysis
    # ==============================================================

    records = load_deduplicated_analyses(
        date
    )

    if not records:

        raise RuntimeError(
            f"❌ {date} 没有可用 Task 4 Analysis"
        )

    print(
        f"Task 4 Analysis : "
        f"{sum("
            "1 "
            "for language_paths "
            "in discover_analysis_files(date).values() "
            "for _ in language_paths"
        )}"
    )

    print(
        f"Unique Events    : "
        f"{len(records)}"
    )

    print(
        f"Languages        : "
        f"zh preferred / en fallback"
    )

    # ==============================================================
    # Split batches
    # ==============================================================

    batches = split_batches(
        records
    )

    print(
        f"Batch Count      : "
        f"{len(batches)}"
    )

    # ==============================================================
    # Batch Compression
    # ==============================================================

    batch_summaries: list[str] = []

    for batch_number, batch in enumerate(
        batches,
        start=1,
    ):

        summary = generate_batch_summary(
            date,
            batch_number,
            len(batches),
            batch,
        )

        if not summary.strip():

            raise RuntimeError(
                f"❌ Empty Batch Summary: "
                f"{batch_number}"
            )

        batch_summaries.append(
            summary
        )

    if len(batch_summaries) != len(
        batches
    ):

        raise RuntimeError(
            "Batch summary count mismatch: "
            f"{len(batch_summaries)} / "
            f"{len(batches)}"
        )

    # ==============================================================
    # Intermediate Merge
    # ==============================================================

    intermediate = generate_intermediate(
        date,
        batch_summaries,
    )

    if not intermediate.strip():

        raise RuntimeError(
            f"❌ {date} Intermediate Brief is empty."
        )

    # ==============================================================
    # Final Input cache
    # ==============================================================

    save_final_input(
        date,
        intermediate,
    )

    # ==============================================================
    # Final Daily Report
    # ==============================================================

    final_report = (
        generate_final_daily_report(
            date,
            daily_skill,
            intermediate,
        )
    )

    if not final_report.strip():

        raise RuntimeError(
            f"❌ {date} Final Daily Report is empty."
        )

    if not report_path.exists():

        raise RuntimeError(
            f"❌ {date} 日报没有生成："
            f"{report_path}"
        )

    if report_path.stat().st_size <= 0:

        raise RuntimeError(
            f"❌ {date} 日报文件为空："
            f"{report_path}"
        )

    # ==============================================================
    # Manifest
    # ==============================================================

    write_runtime_manifest(
        date,
        len(records),
        len(batches),
        report_path,
    )

    # ==============================================================
    # Complete
    # ==============================================================

    print()
    print(
        "=" * 70
    )
    print(
        "DAILY REPORT COMPLETE"
    )
    print(
        "=" * 70
    )
    print(
        f"DATE              : {date}"
    )
    print(
        f"UNIQUE EVENTS     : {len(records)}"
    )
    print(
        f"BATCHES           : {len(batches)}"
    )
    print(
        f"BATCH SIZE        : {BATCH_SIZE}"
    )
    print(
        f"INTERMEDIATE      : {intermediate_path(date)}"
    )
    print(
        f"REPORT            : {report_path}"
    )
    print(
        "=" * 70
    )


# ======================================================================
# PROCESS THREE DATES
# ======================================================================

def process_three_dates(
    day_before: str,
    yesterday: str,
    today: str,
) -> None:

    day_before = validate_date(
        day_before
    )

    yesterday = validate_date(
        yesterday
    )

    today = validate_date(
        today
    )

    dates = [
        day_before,
        yesterday,
        today,
    ]

    if len(set(dates)) != 3:

        raise ValueError(
            "The three processing dates "
            "must be distinct."
        )

    print()
    print(
        "#" * 70
    )
    print(
        "748686 KNOWLEDGE DAILY V4.0"
    )
    print(
        "TASK 4 → BATCH COMPRESSION → "
        "INTERMEDIATE → FINAL DAILY"
    )
    print(
        "#" * 70
    )
    print(
        f"DAY_BEFORE : {day_before}"
    )
    print(
        f"YESTERDAY  : {yesterday}"
    )
    print(
        f"TODAY      : {today}"
    )
    print(
        "#" * 70
    )

    # ==============================================================
    # Load Skill once
    # ==============================================================

    print()
    print(
        "Loading Daily Report Skill..."
    )

    daily_skill = load_daily_skill()

    print(
        f"✅ Daily Skill loaded | "
        f"{len(daily_skill)} chars"
    )

    # ==============================================================
    # Process strictly in date order
    # ==============================================================

    for index, date in enumerate(
        dates,
        start=1,
    ):

        print()
        print(
            "#" * 70
        )
        print(
            f"DAILY PROCESSING UNIT "
            f"{index} / 3"
        )
        print(
            f"DATE : {date}"
        )
        print(
            "#" * 70
        )

        process_date(
            date,
            daily_skill,
        )

    print()
    print(
        "#" * 70
    )
    print(
        "KNOWLEDGE DAILY — ALL THREE DATES COMPLETE"
    )
    print(
        "#" * 70
    )


# ======================================================================
# CLI
# ======================================================================

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description=(
            "748686 Knowledge Daily V4.0 — "
            "Layered Batch Daily Report Compiler"
        )
    )

    parser.add_argument(
        "--day-before",
        required=True,
        help="Workflow Task date: YYYY-MM-DD",
    )

    parser.add_argument(
        "--yesterday",
        required=True,
        help="Workflow Task date: YYYY-MM-DD",
    )

    parser.add_argument(
        "--today",
        required=True,
        help="Workflow Task date: YYYY-MM-DD",
    )

    return parser.parse_args()


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    args = parse_args()

    process_three_dates(
        day_before=args.day_before,
        yesterday=args.yesterday,
        today=args.today,
    )


# ======================================================================
# ENTRYPOINT
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print(
            "\n❌ Interrupted by user."
        )

        sys.exit(130)

    except Exception as exc:

        print()
        print(
            "=" * 70
        )
        print(
            "❌ KNOWLEDGE DAILY FAILED"
        )
        print(
            "=" * 70
        )
        print(
            f"{type(exc).__name__}: {exc}"
        )
        print(
            "=" * 70
        )

        sys.exit(1)
