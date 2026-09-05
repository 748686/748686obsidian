#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Weekly Report V3

======================================================================
职责
======================================================================

Weekly Report 不是简单拼接过去 7 天日报。

它是一个独立的“周级知识编译器”。

数据来源：

    1. 05_日报
       └── 已经完成的每日知识压缩结果

    2. 08_知识库
       └── 持久化知识资产

    3. 07_专题报告
       └── 已有专题 / 专题候选

    4. Raw News/YYYY-MM-DD-EventUnit/{en,zh}/event_units/*_analysis.md
       └── Task 4 分析层
       └── 作为事实校验和必要的细节补充

======================================================================
周报的核心原则
======================================================================

不是：

    日报1
    日报2
    日报3
    ...
    日报7
          ↓
       拼起来

而是：

    日报
      +
    知识库
      +
    专题
      +
    Task 4 Analysis
          ↓
    AI 跨日期比较
          ↓
    趋势识别
          ↓
    知识增长判断
          ↓
    周报

======================================================================
重要规则
======================================================================

1. 严格按照 Asia/Shanghai 判断当前日期和 ISO Week。
2. 严格按照本周日期读取日报。
3. 不按照文件 mtime 判断“最近7天”。
4. 知识库中的历史内容不能冒充本周新增知识。
5. 不得编造事实。
6. 不得把推测写成事实。
7. 不修改 Raw News。
8. 不修改 Task 4 Analysis。
9. 周报不存在才生成。
10. 周报已经存在且非空，则跳过。
11. AI 生成失败时，不创建半成品。
12. 使用临时文件 + replace 原子落盘。
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from datetime import datetime, date, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ======================================================================
# 基础路径
# ======================================================================

ROOT = Path(__file__).resolve().parents[1]

RAW_NEWS = ROOT / "Raw News"

REPORTS = ROOT / "05_日报"

KNOWLEDGE = ROOT / "08_知识库"

TOPICS = ROOT / "07_专题报告"

WEEKLY = ROOT / "06_周报"


# ======================================================================
# 时间
# ======================================================================

TIMEZONE = timezone(
    timedelta(hours=8)
)


def now() -> datetime:
    """
    当前北京时间。
    """

    return datetime.now(
        TIMEZONE
    )


# ======================================================================
# AI 配置
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

AI_THROTTLE_SECONDS = 1.5


# ======================================================================
# 工具
# ======================================================================

def is_nonempty_file(path: Path) -> bool:
    """
    判断文件是否存在且非空。
    """

    try:

        return (
            path.is_file()
            and path.stat().st_size > 0
        )

    except Exception:

        return False


# ======================================================================
# AI
# ======================================================================

def call_ai(prompt: str) -> str:
    """
    OpenAI-compatible API。

    支持：

        AI_BASE_URL
        AI_MODEL
        AI_API_KEY

    例如：

        https://api.agnes-ai.cn/v1
    """

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
                    "content": (
                        "你是748686自生长知识系统的"
                        "周级战略知识分析师。"
                        "\n\n"
                        "你的任务不是总结文字，而是进行"
                        "跨日期知识编译。"
                        "\n\n"
                        "必须严格依据输入材料。"
                        "不得编造事实。"
                        "不得把推测写成事实。"
                        "不得把历史知识冒充本周新增知识。"
                        "对于证据不足的判断必须明确标记。"
                        "\n\n"
                        "输出中文 Markdown。"
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.2,
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
                timeout=AI_TIMEOUT,
            ) as response:

                raw = response.read().decode(
                    "utf-8",
                    errors="replace"
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

            if not result or not result.strip():

                raise RuntimeError(
                    "AI 返回空内容"
                )

            return result.strip()

        except (
            HTTPError,
            URLError,
            TimeoutError,
            json.JSONDecodeError,
            RuntimeError,
            Exception,
        ) as exc:

            last_error = exc

            print(
                f"⚠️ WEEKLY AI RETRY "
                f"{attempt}/{AI_RETRIES}"
            )

            print(
                f"   {type(exc).__name__}: {exc}"
            )

            if attempt < AI_RETRIES:

                wait_seconds = (
                    AI_RETRY_BASE
                    * attempt
                )

                print(
                    f"   ⏳ 等待 "
                    f"{wait_seconds}s"
                )

                time.sleep(
                    wait_seconds
                )

    raise RuntimeError(
        "Weekly AI 请求最终失败: "
        + str(last_error)
    )


# ======================================================================
# ISO Week
# ======================================================================

def get_week_dates(
    current: date
) -> list[date]:
    """
    获取当前 ISO Week 的日期。

    Monday -> Sunday
    """

    weekday = current.weekday()

    monday = (
        current
        - timedelta(days=weekday)
    )

    return [
        monday + timedelta(days=i)
        for i in range(7)
    ]


# ======================================================================
# 日报路径
# ======================================================================

def daily_report_path(
    target_date: date
) -> Path:

    return (
        REPORTS
        / target_date.strftime("%Y")
        / target_date.strftime("%m")
        / (
            target_date.strftime("%Y-%m-%d")
            + ".md"
        )
    )


# ======================================================================
# Task 4 Analysis
# ======================================================================

def analysis_directory(
    target_date: date
) -> Path:

    return (
        RAW_NEWS
        / (
            target_date.strftime("%Y-%m-%d")
            + "-EventUnit"
        )
    )


def collect_analysis_files(
    target_date: date
) -> list[Path]:
    """
    读取指定日期的 Task 4 Analysis。

    严格使用：

        en
        zh

    不进行大小写转换。
    """

    root = analysis_directory(
        target_date
    )

    if not root.is_dir():

        return []

    files = []

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
# 读取文件
# ======================================================================

def read_file(
    path: Path,
    max_chars: int = 25000
) -> str:

    try:

        text = path.read_text(
            encoding="utf-8",
            errors="replace"
        )

        if not text.strip():

            return ""

        return text[:max_chars]

    except Exception as exc:

        print(
            f"⚠️ 文件读取失败：{path}"
        )

        print(
            f"   {exc}"
        )

        return ""


# ======================================================================
# 构造文件输入
# ======================================================================

def build_file_sections(
    files: list[Path],
    max_each: int
) -> str:

    sections = []

    for path in files:

        text = read_file(
            path,
            max_each
        )

        if not text:

            continue

        sections.append(
            "\n".join(
                [
                    "",
                    "=" * 70,
                    f"FILE: {path}",
                    "=" * 70,
                    "",
                    text,
                ]
            )
        )

    return "\n".join(
        sections
    )


# ======================================================================
# 收集本周日报
# ======================================================================

def collect_weekly_daily_reports(
    week_dates: list[date]
) -> tuple[list[Path], list[date]]:
    """
    严格按照本周日期读取日报。

    返回：

        existing_files
        missing_dates
    """

    existing = []

    missing = []

    for target_date in week_dates:

        path = daily_report_path(
            target_date
        )

        if is_nonempty_file(path):

            existing.append(
                path
            )

        else:

            missing.append(
                target_date
            )

    return existing, missing


# ======================================================================
# 收集本周 Task 4 Analysis
# ======================================================================

def collect_weekly_analysis(
    week_dates: list[date]
) -> list[Path]:

    files = []

    for target_date in week_dates:

        files.extend(
            collect_analysis_files(
                target_date
            )
        )

    return files


# ======================================================================
# 知识库文件
# ======================================================================

def collect_knowledge_files(
    max_files: int = 100
) -> list[Path]:
    """
    知识库不是按照 mtime 简单取7个文件。

    周报需要看到知识库的结构性内容。

    这里最多读取 max_files 个 Markdown，
    防止知识库巨大导致 Prompt 无限增长。
    """

    if not KNOWLEDGE.is_dir():

        return []

    files = sorted(
        KNOWLEDGE.rglob("*.md")
    )

    if len(files) <= max_files:

        return files

    # 优先选择最近修改的文件。
    files = sorted(
        files,
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return files[:max_files]


# ======================================================================
# 专题文件
# ======================================================================

def collect_topic_files(
    max_files: int = 50
) -> list[Path]:

    if not TOPICS.is_dir():

        return []

    files = sorted(
        TOPICS.rglob("*.md")
    )

    if len(files) <= max_files:

        return files

    files = sorted(
        files,
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return files[:max_files]


# ======================================================================
# 周报 Prompt
# ======================================================================

def build_prompt(
    current: datetime,
    week_dates: list[date],
    daily_files: list[Path],
    missing_dates: list[date],
    knowledge_files: list[Path],
    topic_files: list[Path],
    analysis_files: list[Path],
) -> str:

    iso_year, iso_week, _ = (
        current.date().isocalendar()
    )

    week_start = week_dates[0]

    week_end = week_dates[-1]

    daily_text = build_file_sections(
        daily_files,
        max_each=30000
    )

    knowledge_text = build_file_sections(
        knowledge_files,
        max_each=16000
    )

    topic_text = build_file_sections(
        topic_files,
        max_each=16000
    )

    analysis_text = build_file_sections(
        analysis_files,
        max_each=12000
    )

    missing_text = "\n".join(
        f"- {d.isoformat()}"
        for d in missing_dates
    )

    if not missing_text:

        missing_text = "无，本周7天日报全部存在。"

    return f"""
# 748686 自生长知识系统
# 周级知识编译任务

当前时间：
{current.strftime("%Y-%m-%d %H:%M:%S")} Asia/Shanghai

ISO Week：
{iso_year} W{iso_week:02d}

本周：
{week_start.isoformat()}
至
{week_end.isoformat()}

---

# 一、本周日报

以下是本周已经实际生成的日报。

注意：

如果某一天日报不存在，
说明该日目前没有完成日报。

不要自行补写缺失日期。

缺失日报：

{missing_text}

日报内容：

{daily_text[:100000]}

---

# 二、持久化知识库

以下内容来自：

08_知识库

注意：

这里可能包含历史知识。

绝对不能因为一个知识卡片出现在输入中，
就把它判断为“本周新增”。

只有当本周材料显示该知识发生了新的变化，
才能判断为本周知识增长。

知识库：

{knowledge_text[:70000]}

---

# 三、专题研究

以下来自：

07_专题报告

它们可以帮助判断：

- 哪些问题已经持续出现；
- 哪些问题正在形成专题；
- 哪些方向值得进一步研究。

专题：

{topic_text[:60000]}

---

# 四、Task 4 Event Analysis

以下是本周 EventUnit 的分析结果。

它是事实校验层。

如果日报和知识库之间存在冲突，
优先回到这些 Event Analysis 判断。

不得编造不存在的事件。

Task 4 Analysis：

{analysis_text[:100000]}

---

# 五、任务

现在生成：

{iso_year} W{iso_week:02d}

真正的“知识周报”。

绝对不要简单拼接日报。

必须进行：

跨日期比较
+
事件归纳
+
趋势识别
+
知识变化判断
+
机会判断
+
风险判断
+
未来追踪

---

# 六、特别要求

## 1. 十大事件

不是简单按照新闻数量排序。

应该综合判断：

- 影响范围
- 持续时间
- 战略意义
- 跨行业影响
- 是否可能改变未来趋势

---

## 2. 趋势

至少找出5个趋势。

每个趋势必须回答：

### 证据

哪些事件支持这个判断？

### 判断

现在发生了什么？

### 长期意义

为什么可能重要？

---

## 3. 短期 vs 长期

明确区分：

- 短期噪音
- 周期性变化
- 中期趋势
- 长期结构性变化

---

## 4. 人物

找出本周反复出现的重要人物。

不要因为人物只出现一次，
就强行认为其重要。

---

## 5. 公司

找出：

- 反复出现的公司
- 战略动作明显的公司
- 行业位置发生变化的公司

---

## 6. 技术

关注：

- 新技术
- 技术突破
- 技术商业化
- 技术竞争
- 技术监管
- AI相关变化

---

## 7. 行业

至少分析：

- 科技
- 金融
- 商业
- 政策
- 媒体
- 消费
- AI
- 国际局势

没有足够证据的行业，
明确写：

“本周证据不足”。

不要为了凑内容编造判断。

---

## 8. 机会

机会必须来自输入材料。

不能写成泛泛而谈的鸡汤。

---

## 9. 风险

明确区分：

- 已发生风险
- 正在形成的风险
- 潜在风险

---

## 10. 知识增长

重点回答：

> 相比本周开始之前，
> 我们真正多知道了什么？

必须区分：

### 新事实

本周新出现的信息。

### 新关系

本周发现的事件、人物、公司、
技术之间的新关联。

### 新判断

通过多个事件组合后得到的新认识。

### 新问题

目前仍然不知道、
但值得继续研究的问题。

---

## 11. 专题

判断哪些问题已经从：

新闻

升级为：

持续性问题

再升级为：

专题研究方向

---

## 12. 下周追踪

每一个追踪事项必须尽量给出：

- 追踪对象
- 原因
- 观察指标
- 什么变化会改变当前判断

---

# 七、输出格式

# 本周核心结论

用5～10句话说明本周真正发生了什么。

# 一、本周十大事件

| 排名 | 事件 | 重要性 | 核心影响 |
|---|---|---|---|

# 二、本周核心趋势

## 趋势1

### 证据

### 判断

### 长期意义

## 趋势2

### 证据

### 判断

### 长期意义

## 趋势3

### 证据

### 判断

### 长期意义

## 趋势4

### 证据

### 判断

### 长期意义

## 趋势5

### 证据

### 判断

### 长期意义

# 三、短期波动与长期趋势

| 类型 | 判断 | 证据 |
|---|---|---|

# 四、人物变化

| 人物 | 本周动态 | 为什么重要 |
|---|---|---|

# 五、公司变化

| 公司 | 本周动态 | 战略意义 |
|---|---|---|

# 六、技术变化

| 技术 | 本周进展 | 影响 |
|---|---|---|

# 七、行业变化

## 科技

## 金融

## 商业

## 政策

## 媒体

## 消费

## AI

## 国际局势

# 八、机会

列出真正值得关注的机会。

# 九、风险

列出真正值得关注的风险。

# 十、本周知识增长

## 新事实

## 新关系

## 新判断

## 新问题

# 十一、专题研究方向

列出最值得进入下一阶段深度研究的专题。

说明：

- 为什么现在值得研究
- 已有证据
- 还缺什么信息

# 十二、下周重点追踪

| 优先级 | 项目 | 追踪原因 | 观察指标 | 判断改变条件 |
|---|---|---|---|---|

# 十三、一句话周结论

用一句话总结本周。

---

再次强调：

不要编造。

不要为了填满模板而创造不存在的信息。

证据不足时明确说明证据不足。

历史知识不能冒充本周新增知识。
"""


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

    tmp_path = path.with_suffix(
        path.suffix + ".tmp"
    )

    try:

        tmp_path.write_text(
            content,
            encoding="utf-8"
        )

        # 写入后立即验证
        if not is_nonempty_file(
            tmp_path
        ):

            raise RuntimeError(
                f"临时文件为空：{tmp_path}"
            )

        tmp_path.replace(
            path
        )

    finally:

        if tmp_path.exists():

            try:

                tmp_path.unlink()

            except Exception:

                pass


# ======================================================================
# 主程序
# ======================================================================

def main():

    current = now()

    current_date = current.date()

    iso_year, iso_week, iso_weekday = (
        current_date.isocalendar()
    )

    week_dates = get_week_dates(
        current_date
    )

    week_start = week_dates[0]

    week_end = week_dates[-1]

    print()
    print("=" * 70)
    print(
        "748686 WEEKLY REPORT V3"
    )
    print("=" * 70)

    print(
        f"Current : "
        f"{current.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print(
        f"Week    : "
        f"{iso_year} W{iso_week:02d}"
    )

    print(
        f"Range   : "
        f"{week_start} -> {week_end}"
    )

    # ------------------------------------------------------------------
    # 输出路径
    # ------------------------------------------------------------------

    output_dir = (
        WEEKLY
        / str(iso_year)
    )

    output_path = (
        output_dir
        / f"W{iso_week:02d}.md"
    )

    print()
    print(
        f"Output  : {output_path}"
    )

    # ------------------------------------------------------------------
    # 已存在则跳过
    # ------------------------------------------------------------------

    if is_nonempty_file(
        output_path
    ):

        print()
        print(
            "⏭️ WEEKLY REPORT ALREADY EXISTS"
        )

        print(
            f"   Skip: {output_path}"
        )

        print()
        print("=" * 70)

        return

    # ------------------------------------------------------------------
    # 日报
    # ------------------------------------------------------------------

    daily_files, missing_dates = (
        collect_weekly_daily_reports(
            week_dates
        )
    )

    print()
    print(
        f"Daily reports : "
        f"{len(daily_files)} / 7"
    )

    if missing_dates:

        print(
            "Missing daily reports:"
        )

        for target_date in missing_dates:

            print(
                f"   - {target_date}"
            )

    # ------------------------------------------------------------------
    # 没有任何日报
    # ------------------------------------------------------------------

    if not daily_files:

        raise RuntimeError(
            "本周没有任何日报，"
            "无法生成 Weekly Report"
        )

    # ------------------------------------------------------------------
    # Task 4 Analysis
    # ------------------------------------------------------------------

    analysis_files = (
        collect_weekly_analysis(
            week_dates
        )
    )

    print(
        f"Task 4 analysis: "
        f"{len(analysis_files)}"
    )

    # ------------------------------------------------------------------
    # 知识库
    # ------------------------------------------------------------------

    knowledge_files = (
        collect_knowledge_files(
            max_files=100
        )
    )

    print(
        f"Knowledge files: "
        f"{len(knowledge_files)}"
    )

    # ------------------------------------------------------------------
    # 专题
    # ------------------------------------------------------------------

    topic_files = (
        collect_topic_files(
            max_files=50
        )
    )

    print(
        f"Topic files    : "
        f"{len(topic_files)}"
    )

    # ------------------------------------------------------------------
    # Prompt
    # ------------------------------------------------------------------

    print()
    print(
        "Building weekly knowledge prompt..."
    )

    prompt = build_prompt(
        current=current,
        week_dates=week_dates,
        daily_files=daily_files,
        missing_dates=missing_dates,
        knowledge_files=knowledge_files,
        topic_files=topic_files,
        analysis_files=analysis_files,
    )

    print(
        f"Prompt chars   : "
        f"{len(prompt):,}"
    )

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------

    print()
    print(
        "Generating weekly report..."
    )

    result = call_ai(
        prompt
    )

    if not result.strip():

        raise RuntimeError(
            "AI 返回空周报"
        )

    # ------------------------------------------------------------------
    # Markdown
    # ------------------------------------------------------------------

    content = f"""---
year: {iso_year}
week: {iso_week}
week_start: {week_start}
week_end: {week_end}
type: weekly_report
status: generated
source:
  - 05_日报
  - 08_知识库
  - 07_专题报告
  - Raw News Task 4 Analysis
generated_at: {current.strftime("%Y-%m-%d %H:%M:%S")}
timezone: Asia/Shanghai
---

# {iso_year} W{iso_week:02d} 自生长知识周报

{result.strip()}
"""

    # ------------------------------------------------------------------
    # 原子落盘
    # ------------------------------------------------------------------

    print()
    print(
        "Saving weekly report..."
    )

    atomic_write(
        output_path,
        content
    )

    # ------------------------------------------------------------------
    # 最终验证
    # ------------------------------------------------------------------

    if not is_nonempty_file(
        output_path
    ):

        raise RuntimeError(
            "周报保存后验证失败"
        )

    print()
    print("=" * 70)
    print(
        "✅ WEEKLY REPORT V3 COMPLETE"
    )
    print("=" * 70)

    print(
        f"Output : {output_path}"
    )

    print(
        f"Daily  : "
        f"{len(daily_files)}/7"
    )

    print(
        f"Analysis : "
        f"{len(analysis_files)}"
    )

    print(
        f"Knowledge : "
        f"{len(knowledge_files)}"
    )

    print(
        f"Topics : "
        f"{len(topic_files)}"
    )

    print()


# ======================================================================
# Entry
# ======================================================================

if __name__ == "__main__":

    main()
