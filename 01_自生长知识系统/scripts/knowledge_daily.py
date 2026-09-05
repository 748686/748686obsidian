#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Knowledge Daily Compiler
V2.0

======================================================================
职责
======================================================================

读取 Task 4 已完成的 EventUnit Analysis 文件，
严格检查：

    前天
    昨天
    今天

三天的日报是否存在。

规则：

    已存在 → SKIP
    不存在 → 读取当天全部 Analysis
             → AI 生成
             → 立即落盘
             → 再处理下一天

======================================================================
核心处理契约
======================================================================

1. 只处理最近三天：
       DAY_BEFORE
       YESTERDAY
       TODAY

2. 每一天独立处理。

3. 一天生成完成后立即落盘。

4. 已经存在的日报绝对不重复生成。

5. 不因为某一天已经存在而影响另外两天。

6. 不修改 Task 4 的任何文件。

7. 同时读取：
       en
       zh

8. 最终一天只生成一份中文日报。

9. 语言目录严格使用：
       en
       zh

   禁止：
       EN
       ZH

10. 日期统一使用：
       Asia/Shanghai

======================================================================
输入
======================================================================

Raw News/
└── YYYY-MM-DD-EventUnit/
    ├── en/
    │   └── event_units/
    │       ├── EVT-....md
    │       └── EVT-...._analysis.md
    │
    └── zh/
        └── event_units/
            ├── EVT-....md
            └── EVT-...._analysis.md

======================================================================
输出
======================================================================

05_日报/
└── YYYY/
    └── MM/
        └── YYYY-MM-DD.md

例如：

05_日报/
└── 2026/
    └── 09/
        ├── 2026-09-04.md
        ├── 2026-09-05.md
        └── 2026-09-06.md

======================================================================
执行示例
======================================================================

如果今天是：

2026-09-06

检查：

2026-09-04
2026-09-05
2026-09-06

如果：

2026-09-04.md 已存在
2026-09-05.md 不存在
2026-09-06.md 不存在

则：

2026-09-04 → SKIP

2026-09-05
    ↓
读取全部 Analysis
    ↓
生成
    ↓
立即保存

2026-09-06
    ↓
读取全部 Analysis
    ↓
生成
    ↓
立即保存

======================================================================
"""

from __future__ import annotations

import os
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


# ======================================================================
# SYSTEM CONFIG
# ======================================================================

TIMEZONE = ZoneInfo("Asia/Shanghai")

SUPPORTED_LANGUAGES = (
    "en",
    "zh",
)


# ======================================================================
# PATH
# ======================================================================

SCRIPT_DIR = Path(__file__).resolve().parent

ROOT_DIR = SCRIPT_DIR.parent

RAW_NEWS_DIR = (
    ROOT_DIR / "Raw News"
)

DAILY_DIR = (
    ROOT_DIR / "05_日报"
)


# ======================================================================
# AI CONFIG
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

AI_THROTTLE_SECONDS = float(
    os.getenv(
        "KNOWLEDGE_AI_THROTTLE",
        "1.5",
    )
)


# ======================================================================
# LOG
# ======================================================================

def log(message: str) -> None:
    """
    统一日志输出。
    """
    print(
        message,
        flush=True,
    )


# ======================================================================
# DATE
# ======================================================================

def get_shanghai_now() -> datetime:
    """
    获取北京时间。

    GitHub Actions runner 通常运行在 UTC，
    因此不能直接使用 datetime.now() 判断系统日期。
    """
    return datetime.now(
        TIMEZONE
    )


def get_target_dates() -> list[str]:
    """
    返回严格三天：

        前天
        昨天
        今天

    顺序严格按照：

        前天 → 昨天 → 今天
    """

    now = get_shanghai_now()

    return [
        (
            now
            - timedelta(days=2)
        ).strftime("%Y-%m-%d"),

        (
            now
            - timedelta(days=1)
        ).strftime("%Y-%m-%d"),

        now.strftime("%Y-%m-%d"),
    ]


# ======================================================================
# FILE UTIL
# ======================================================================

def safe_read(
    path: Path,
) -> str:
    """
    UTF-8 安全读取。
    """

    return path.read_text(
        encoding="utf-8",
        errors="replace",
    )


def safe_write(
    path: Path,
    content: str,
) -> None:
    """
    原子写入。

    先写 .tmp，
    成功后 replace 正式文件。

    防止 GitHub Actions 在写文件过程中
    产生半截 Markdown。
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    tmp_path = path.with_suffix(
        path.suffix + ".tmp"
    )

    tmp_path.write_text(
        content,
        encoding="utf-8",
    )

    tmp_path.replace(
        path
    )


# ======================================================================
# DAILY PATH
# ======================================================================

def daily_output_path(
    date_str: str,
) -> Path:
    """
    根据日期生成日报路径。

    YYYY-MM-DD
        ↓
    05_日报/YYYY/MM/YYYY-MM-DD.md
    """

    year = date_str[:4]

    month = date_str[5:7]

    return (
        DAILY_DIR
        / year
        / month
        / f"{date_str}.md"
    )


# ======================================================================
# DAILY EXISTENCE CHECK
# ======================================================================

def daily_exists(
    date_str: str,
) -> bool:
    """
    检查指定日期日报是否已经存在。

    只检查正式 .md 文件。

    .tmp 不算完成。
    """

    path = daily_output_path(
        date_str
    )

    return (
        path.exists()
        and path.is_file()
        and path.stat().st_size > 0
    )


# ======================================================================
# EVENT ID
# ======================================================================

def extract_event_id(
    path: Path,
) -> str:
    """
    从 Analysis 文件名提取 EVT ID。

    例如：

    EVT-20260906-000123_xxx_analysis.md

    → EVT-20260906-000123
    """

    match = re.search(
        r"(EVT-\d{8}-\d{6})",
        path.name,
    )

    if match:
        return match.group(1)

    return path.stem.replace(
        "_analysis",
        "",
    )


# ======================================================================
# ANALYSIS DISCOVERY
# ======================================================================

def discover_analysis(
    date_str: str,
) -> list[dict[str, Any]]:
    """
    获取指定日期全部 Task 4 Analysis。

    严格扫描：

    Raw News/
        YYYY-MM-DD-EventUnit/
            en/event_units/*_analysis.md
            zh/event_units/*_analysis.md

    不依赖目录是否存在来判断完成。

    真正以 Analysis 文件为准。
    """

    results: list[
        dict[str, Any]
    ] = []

    date_root = (
        RAW_NEWS_DIR
        / f"{date_str}-EventUnit"
    )

    if not date_root.exists():

        log(
            f"⚠️ EVENTUNIT DIRECTORY MISSING | "
            f"{date_root}"
        )

        return results

    for language in SUPPORTED_LANGUAGES:

        event_dir = (
            date_root
            / language
            / "event_units"
        )

        if not event_dir.exists():

            log(
                f"   ⚠️ NO {language} "
                f"EVENT DIRECTORY"
            )

            continue

        files = sorted(
            event_dir.glob(
                "*_analysis.md"
            )
        )

        log(
            f"   {language.upper()} "
            f"Analysis files: "
            f"{len(files)}"
        )

        for path in files:

            if not path.is_file():
                continue

            content = safe_read(
                path
            )

            if not content.strip():

                log(
                    f"   ⚠️ EMPTY ANALYSIS | "
                    f"{path.name}"
                )

                continue

            event_id = (
                extract_event_id(
                    path
                )
            )

            results.append(
                {
                    "date": date_str,
                    "language": language,
                    "event_id": event_id,
                    "path": path,
                    "content": content,
                }
            )

    # --------------------------------------------------------------
    # 稳定排序
    # --------------------------------------------------------------

    results.sort(
        key=lambda item: (
            item["event_id"],
            item["language"],
        )
    )

    return results


# ======================================================================
# EVENT UNIT DISCOVERY
# ======================================================================

def find_eventunit(
    date_str: str,
    event_id: str,
    preferred_language: str,
) -> str:
    """
    根据 EVT ID 找 EventUnit 原文。

    优先读取与 Analysis 相同语言。

    找不到时再尝试另一语言。

    注意：

    这里只用于日报上下文，
    不修改任何 EventUnit。
    """

    date_root = (
        RAW_NEWS_DIR
        / f"{date_str}-EventUnit"
    )

    languages = [
        preferred_language
    ]

    for language in SUPPORTED_LANGUAGES:

        if language not in languages:
            languages.append(
                language
            )

    for language in languages:

        event_dir = (
            date_root
            / language
            / "event_units"
        )

        if not event_dir.exists():
            continue

        candidates = sorted(
            event_dir.glob(
                f"{event_id}*.md"
            )
        )

        for path in candidates:

            if "_analysis" in path.name:
                continue

            if not path.is_file():
                continue

            return safe_read(
                path
            )

    return ""


# ======================================================================
# CONTEXT BUILDER
# ======================================================================

def build_context(
    date_str: str,
    analyses: list[dict[str, Any]],
) -> str:
    """
    构造当天日报 AI 上下文。

    每个 Event 独立一个区块。

    同时提供：

        Event ID
        Language
        Analysis
        EventUnit
    """

    blocks: list[str] = []

    for index, item in enumerate(
        analyses,
        start=1,
    ):

        event_id = item[
            "event_id"
        ]

        language = item[
            "language"
        ]

        analysis = item[
            "content"
        ]

        eventunit = (
            find_eventunit(
                date_str,
                event_id,
                language,
            )
        )

        block = f"""
============================================================
EVENT {index}
============================================================

EVENT_ID:
{event_id}

LANGUAGE:
{language}

------------------------------------------------------------
TASK 4 ANALYSIS
------------------------------------------------------------

{analysis}

------------------------------------------------------------
EVENT UNIT
------------------------------------------------------------

{eventunit}
"""

        blocks.append(
            block.strip()
        )

    return "\n\n".join(
        blocks
    )


# ======================================================================
# AI CLIENT
# ======================================================================

def ai_generate(
    prompt: str,
) -> str:
    """
    调用 AGNES / OpenAI-compatible API。

    支持：

        throttle
        retry
        exponential backoff
    """

    if not AGNES_API_KEY:

        raise RuntimeError(
            "AGNES_API_KEY is not configured."
        )

    try:

        from openai import OpenAI

    except ImportError as exc:

        raise RuntimeError(
            "openai package is required."
        ) from exc

    # --------------------------------------------------------------
    # 请求节流
    # --------------------------------------------------------------

    if AI_THROTTLE_SECONDS > 0:

        time.sleep(
            AI_THROTTLE_SECONDS
        )

    client = OpenAI(
        api_key=AGNES_API_KEY,
        base_url=AGNES_BASE_URL,
        timeout=AI_TIMEOUT,
    )

    last_error: Exception | None = None

    for attempt in range(
        1,
        AI_RETRIES + 1,
    ):

        try:

            log(
                f"   🤖 DAILY AI REQUEST "
                f"{attempt}/{AI_RETRIES}"
            )

            response = (
                client
                .chat
                .completions
                .create(
                    model=AGNES_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "你是748686自生长知识系统的"
                                "知识日报编译器。"
                                "你的任务是把当天已经通过"
                                "Task 4 的全部事件分析编译成"
                                "一份高质量中文知识日报。"
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                    temperature=0.2,
                )
            )

            text = (
                response
                .choices[0]
                .message
                .content
            )

            if not text:

                raise RuntimeError(
                    "AI returned empty content."
                )

            text = text.strip()

            if not text:

                raise RuntimeError(
                    "AI returned blank content."
                )

            return text

        except Exception as exc:

            last_error = exc

            log(
                f"   ⚠️ DAILY AI RETRY "
                f"{attempt}/{AI_RETRIES} | "
                f"{exc}"
            )

            if attempt < AI_RETRIES:

                sleep_seconds = (
                    3 * attempt
                )

                log(
                    f"   ⏳ WAIT "
                    f"{sleep_seconds}s"
                )

                time.sleep(
                    sleep_seconds
                )

    raise RuntimeError(
        "Daily AI generation failed: "
        f"{last_error}"
    )


# ======================================================================
# PROMPT
# ======================================================================

def build_prompt(
    date_str: str,
    analyses: list[dict[str, Any]],
) -> str:
    """
    构造日报 Prompt。
    """

    context = build_context(
        date_str,
        analyses,
    )

    return f"""
你是“748686 自生长知识系统”的知识日报编译器。

现在需要生成：

# {date_str} 知识日报

你获得的是 {date_str} 当天所有已经通过 Task 4 的 EventUnit Analysis，
同时提供对应 EventUnit 作为事实上下文。

============================================================
核心任务
============================================================

不要简单复制或者逐条罗列新闻。

你需要把当天全部事件分析进行一次“知识编译”。

必须：

1. 综合当天全部事件。
2. 合并相同主题。
3. 识别跨事件关系。
4. 找出真正重要的变化。
5. 提取值得进入长期知识库的信息。
6. 找出值得继续追踪的问题。
7. 为下一阶段 Knowledge Asset 提供结构化线索。
8. 同时吸收 en 和 zh 的分析。
9. 同一个事件不能因为语言不同重复写两次。
10. 必须保留重要 Event ID。
11. 只能根据输入内容写作。
12. 不得凭空补充事实。
13. 推测必须明确标记为“推测”。
14. 信息不足时必须明确写“待验证”。
15. 不要把推测写成事实。

============================================================
日报定位
============================================================

这不是传统新闻摘要。

它是：

“当天知识状态的编译结果”。

因此应该重点回答：

今天发生了什么？

为什么重要？

发生了哪些变化？

哪些事件之间存在关系？

哪些知识值得进入长期知识库？

哪些问题值得继续追踪？

============================================================
输出格式
============================================================

请严格使用以下 Markdown 结构：

# {date_str} 知识日报

## 一、今日核心事件

挑选当天真正重要的核心事件。

每个事件说明：

- 发生了什么
- 为什么重要
- 影响范围
- Event ID

不要为了数量而堆砌事件。

---

## 二、今日重要变化

从全部事件中寻找真正的“变化”。

可以包括：

- 政策变化
- 公司变化
- 产品变化
- 技术变化
- 市场变化
- 行业变化
- 人物变化
- 地缘或社会变化

---

## 三、主题与趋势

跨事件进行综合。

不要按照新闻来源逐条写。

寻找：

- 重复出现的主题
- 正在升温的主题
- 正在变化的趋势
- 潜在长期趋势

---

## 四、人物与组织

提取值得关注的：

- 人物
- 公司
- 组织
- 政府机构
- 研究机构

说明他们为什么值得关注。

---

## 五、技术与产品

提取：

- 新技术
- AI 模型
- 产品
- 平台
- 芯片
- 软件
- 技术路线

重点说明变化，而不是只写名称。

---

## 六、跨事件关联

这是本日报的重要部分。

主动寻找：

事件 A
↓
事件 B

之间是否存在：

- 因果关系
- 竞争关系
- 上下游关系
- 技术关系
- 公司关系
- 市场关系
- 政策关系
- 时间上的连续关系

如果只是推测，必须明确写：

“推测 / 待验证”。

---

## 七、今日新增知识

判断今天有哪些信息值得进入长期知识库。

按照：

### 公司

### 人物

### 产品

### 技术

### 概念

### 行业

### 主题

分类。

---

## 八、值得继续追踪的问题

列出未来应该继续观察的问题。

优先关注：

- 尚未解决的问题
- 正在快速变化的问题
- 信息冲突的问题
- 可能形成长期趋势的问题

---

## 九、知识库更新建议

明确指出：

### 新增

哪些实体应该进入知识库。

### 更新

哪些已有实体应该更新。

### 关系

哪些实体之间应该建立关系。

### 冲突

哪些信息存在冲突。

### 缺口

哪些知识还缺失。

---

## 十、事件索引

列出本日报使用的全部 Event ID。

按照：

- Event ID
- 主题
- 语言来源

整理。

============================================================
语言要求
============================================================

最终输出使用中文。

英文来源可以翻译成中文。

不要生成英文日报。

============================================================
重要限制
============================================================

不要：

- 编造新闻
- 编造人物
- 编造公司
- 编造数字
- 编造因果关系
- 把模型推测写成事实
- 把两个语言版本当成两个不同事件
- 输出与日报无关的解释

============================================================
输入资料
============================================================

以下是当天全部 Task 4 Analysis 与 EventUnit：

{context}
"""


# ======================================================================
# VALIDATE AI OUTPUT
# ======================================================================

def validate_daily_output(
    content: str,
    date_str: str,
) -> None:
    """
    基础输出验证。

    不做语义判断，
    只确保 AI 没有返回明显错误内容。
    """

    if not content.strip():

        raise RuntimeError(
            "Generated daily content is empty."
        )

    if len(content.strip()) < 200:

        raise RuntimeError(
            "Generated daily content is "
            "suspiciously short."
        )

    if f"# {date_str} 知识日报" not in content:

        log(
            "   ⚠️ Daily title mismatch. "
            "Content will still be saved."
        )


# ======================================================================
# GENERATE ONE DAY
# ======================================================================

def generate_one_day(
    date_str: str,
) -> bool:
    """
    处理一天。

    返回：

        True  = 本次生成并落盘
        False = 跳过
    """

    output_path = (
        daily_output_path(
            date_str
        )
    )

    # ==============================================================
    # FIRST CHECK
    # ==============================================================

    if daily_exists(
        date_str
    ):

        log(
            f"⏭️ SKIP DAILY | "
            f"{date_str} | "
            f"already exists"
        )

        log(
            f"   {output_path}"
        )

        return False

    # ==============================================================
    # START
    # ==============================================================

    log("")
    log("=" * 70)
    log(
        f"DAILY PROCESSING | "
        f"{date_str}"
    )
    log("=" * 70)

    log(
        f"📁 OUTPUT | "
        f"{output_path}"
    )

    # ==============================================================
    # DISCOVER ANALYSIS
    # ==============================================================

    analyses = discover_analysis(
        date_str
    )

    log(
        f"📊 TOTAL ANALYSIS | "
        f"{len(analyses)}"
    )

    # ==============================================================
    # NO INPUT
    # ==============================================================

    if not analyses:

        log(
            f"⚠️ NO ANALYSIS | "
            f"{date_str}"
        )

        log(
            "   Daily will NOT be created."
        )

        return False

    # ==============================================================
    # LANGUAGE STATS
    # ==============================================================

    en_count = sum(
        1
        for item in analyses
        if item["language"] == "en"
    )

    zh_count = sum(
        1
        for item in analyses
        if item["language"] == "zh"
    )

    log(
        f"   EN Analysis : {en_count}"
    )

    log(
        f"   ZH Analysis : {zh_count}"
    )

    # ==============================================================
    # BUILD PROMPT
    # ==============================================================

    log(
        "🧠 BUILDING DAILY CONTEXT"
    )

    prompt = build_prompt(
        date_str,
        analyses,
    )

    # ==============================================================
    # AI GENERATION
    # ==============================================================

    log(
        "🤖 GENERATING DAILY"
    )

    content = ai_generate(
        prompt
    )

    # ==============================================================
    # VALIDATE
    # ==============================================================

    validate_daily_output(
        content,
        date_str,
    )

    # ==============================================================
    # IMMEDIATE SAVE
    # ==============================================================

    log(
        "💾 SAVING DAILY"
    )

    safe_write(
        output_path,
        content,
    )

    # ==============================================================
    # POST-SAVE VERIFY
    # ==============================================================

    if not daily_exists(
        date_str
    ):

        raise RuntimeError(
            f"Daily save verification failed: "
            f"{output_path}"
        )

    log(
        f"✅ DAILY SAVED | "
        f"{date_str}"
    )

    log(
        f"   {output_path}"
    )

    return True


# ======================================================================
# THREE-DAY CHECK
# ======================================================================

def check_three_days() -> None:
    """
    严格执行三天检查。

    前天 → 昨天 → 今天

    每天：

        检查
        ↓
        已存在 → SKIP
        ↓
        缺失 → 生成
        ↓
        立即落盘
        ↓
        下一天
    """

    dates = get_target_dates()

    log("")
    log("=" * 70)
    log("KNOWLEDGE DAILY — THREE DAY CHECK")
    log("=" * 70)

    log(
        f"Timezone : Asia/Shanghai"
    )

    log(
        f"Now      : "
        f"{get_shanghai_now().isoformat()}"
    )

    log("")
    log(
        "Target dates:"
    )

    log(
        f"  DAY_BEFORE : {dates[0]}"
    )

    log(
        f"  YESTERDAY  : {dates[1]}"
    )

    log(
        f"  TODAY      : {dates[2]}"
    )

    generated = 0

    skipped = 0

    unavailable = 0

    failed = 0

    # ==============================================================
    # ONE DAY AT A TIME
    # ==============================================================

    for index, date_str in enumerate(
        dates,
        start=1,
    ):

        log("")
        log(
            "#" * 70
        )

        log(
            f"DAY CHECK "
            f"{index} / {len(dates)}"
        )

        log(
            f"DATE: {date_str}"
        )

        log(
            "#" * 70
        )

        try:

            # ------------------------------------------------------
            # 判断是否已经存在
            # ------------------------------------------------------

            output_path = (
                daily_output_path(
                    date_str
                )
            )

            if daily_exists(
                date_str
            ):

                log(
                    f"⏭️ EXISTS → SKIP | "
                    f"{date_str}"
                )

                log(
                    f"   {output_path}"
                )

                skipped += 1

                continue

            # ------------------------------------------------------
            # 不存在 → 生成
            # ------------------------------------------------------

            created = generate_one_day(
                date_str
            )

            if created:

                generated += 1

            else:

                unavailable += 1

        except Exception as exc:

            failed += 1

            log("")
            log(
                f"❌ DAILY FAILED | "
                f"{date_str}"
            )

            log(
                f"   ERROR: {exc}"
            )

            # ------------------------------------------------------
            # 当前日期失败，不允许继续伪装成成功。
            #
            # 这里直接抛出异常，让 GitHub Actions 标记失败。
            # ------------------------------------------------------

            raise

    # ==============================================================
    # SUMMARY
    # ==============================================================

    log("")
    log("=" * 70)
    log("THREE DAY CHECK COMPLETE")
    log("=" * 70)

    log(
        f"Generated    : {generated}"
    )

    log(
        f"Skipped      : {skipped}"
    )

    log(
        f"No Analysis  : {unavailable}"
    )

    log(
        f"Failed       : {failed}"
    )

    log("")

    # ==============================================================
    # FINAL STATE
    # ==============================================================

    for date_str in dates:

        path = daily_output_path(
            date_str
        )

        if daily_exists(
            date_str
        ):

            log(
                f"✅ {date_str} | "
                f"READY | {path}"
            )

        else:

            log(
                f"⚠️ {date_str} | "
                f"NOT READY"
            )

    log("")
    log(
        "✅ KNOWLEDGE DAILY THREE-DAY CHECK FINISHED"
    )


# ======================================================================
# MAIN
# ======================================================================

def main() -> None:

    log("")
    log("=" * 70)
    log("748686 KNOWLEDGE DAILY COMPILER V2.0")
    log("=" * 70)

    log(
        f"Root: {ROOT_DIR}"
    )

    log(
        f"Raw News: {RAW_NEWS_DIR}"
    )

    log(
        f"Daily: {DAILY_DIR}"
    )

    # --------------------------------------------------------------
    # 基础目录检查
    # --------------------------------------------------------------

    if not ROOT_DIR.exists():

        raise RuntimeError(
            f"Repository root does not exist: "
            f"{ROOT_DIR}"
        )

    if not RAW_NEWS_DIR.exists():

        raise RuntimeError(
            f"Raw News directory does not exist: "
            f"{RAW_NEWS_DIR}"
        )

    # --------------------------------------------------------------
    # 执行严格三天检查
    # --------------------------------------------------------------

    check_three_days()


# ======================================================================
# ENTRY
# ======================================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        log(
            "❌ Interrupted by user."
        )

        sys.exit(130)

    except Exception as exc:

        log("")
        log(
            "=" * 70
        )

        log(
            "❌ KNOWLEDGE DAILY FAILED"
        )

        log(
            f"ERROR: {exc}"
        )

        log(
            "=" * 70
        )

        sys.exit(1)
