#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
748686 自生长知识系统
Weekly Report V2

周报不再简单拼接过去7天日报。

数据来源：

05_日报
08_知识库
07_专题报告

然后由 AI 进行：

1. 本周十大事件
2. 趋势变化
3. 跨新闻关联
4. 行业变化
5. 机会
6. 风险
7. 知识增长
8. 人物 / 公司 / 技术变化
9. 专题研究方向
10. 下周追踪事项
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen


# ============================================================
# 路径
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

REPORTS = ROOT / "05_日报"
KNOWLEDGE = ROOT / "08_知识库"
TOPICS = ROOT / "07_专题报告"
WEEKLY = ROOT / "06_周报"


# ============================================================
# 时间
# ============================================================

def now():

    return datetime.now(
        timezone(
            timedelta(hours=8)
        )
    )


# ============================================================
# AI
# ============================================================

def call_ai(prompt):

    api_key = os.getenv(
        "AI_API_KEY",
        ""
    )

    base_url = os.getenv(
        "AI_BASE_URL",
        "https://api.openai.com/v1"
    ).rstrip("/")

    model = os.getenv(
        "AI_MODEL",
        ""
    )

    if not api_key:

        raise RuntimeError(
            "缺少 AI_API_KEY"
        )

    if not model:

        raise RuntimeError(
            "缺少 AI_MODEL"
        )

    payload = json.dumps(
        {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "你是748686自生长知识系统的战略知识分析师。"
                        "严格依据输入。"
                        "不得编造事实。"
                        "输出中文Markdown。"
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

    request = Request(
        base_url + "/chat/completions",
        data=payload,
        headers={
            "Authorization":
                "Bearer " + api_key,
            "Content-Type":
                "application/json",
        },
    )

    with urlopen(
        request,
        timeout=180,
    ) as response:

        data = json.loads(
            response.read().decode(
                "utf-8"
            )
        )

    return data[
        "choices"
    ][0][
        "message"
    ][
        "content"
    ]


# ============================================================
# 读取最近7天文件
# ============================================================

def recent_files(
    directory,
    days=7
):

    files = sorted(
        directory.rglob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return files[:days]


# ============================================================
# 读取文件
# ============================================================

def read_files(
    files,
    max_each=25000
):

    sections = []

    for path in files:

        try:

            text = path.read_text(
                encoding="utf-8",
                errors="replace"
            )

            sections.append(
                f"""
============================================================
FILE: {path}
============================================================

{text[:max_each]}
"""
            )

        except Exception as exc:

            print(
                f"⚠️ 文件读取失败：{path}"
            )

            print(exc)

    return "\n\n".join(
        sections
    )


# ============================================================
# 主程序
# ============================================================

def main():

    current = now()

    year = current.strftime(
        "%Y"
    )

    week = current.isocalendar().week

    print("=" * 70)

    print(
        "748686 WEEKLY REPORT V2"
    )

    print("=" * 70)

    print(
        f"Year : {year}"
    )

    print(
        f"Week : W{week:02d}"
    )

    # --------------------------------------------------------
    # 获取日报
    # --------------------------------------------------------

    report_files = recent_files(
        REPORTS,
        7
    )

    print()
    print(
        f"Daily reports: {len(report_files)}"
    )

    if not report_files:

        raise RuntimeError(
            "没有找到日报"
        )

    # --------------------------------------------------------
    # 获取知识卡片
    # --------------------------------------------------------

    knowledge_files = recent_files(
        KNOWLEDGE,
        7
    )

    print(
        f"Knowledge files: {len(knowledge_files)}"
    )

    # --------------------------------------------------------
    # 获取专题
    # --------------------------------------------------------

    topic_files = recent_files(
        TOPICS,
        7
    )

    print(
        f"Topic files: {len(topic_files)}"
    )

    # --------------------------------------------------------
    # 读取
    # --------------------------------------------------------

    daily_text = read_files(
        report_files
    )

    knowledge_text = read_files(
        knowledge_files,
        max_each=18000
    )

    topic_text = read_files(
        topic_files,
        max_each=18000
    )

    # --------------------------------------------------------
    # Prompt
    # --------------------------------------------------------

    prompt = f"""
# 748686 自生长知识系统周报

当前周：
{year} W{week:02d}

---

# 最近7天日报

{daily_text[:90000]}

---

# 最近7天知识卡片

{knowledge_text[:50000]}

---

# 最近7天专题候选

{topic_text[:50000]}

---

请生成真正的“知识周报”。

注意：

不能简单拼接7天日报。

必须进行跨天归纳、比较和趋势判断。

要求：

1. 找出本周最重要的十大事件。
2. 找出本周最明显的5个趋势。
3. 判断哪些趋势是短期波动，哪些可能成为长期趋势。
4. 找出本周反复出现的人物。
5. 找出本周反复出现的公司。
6. 找出本周反复出现的技术。
7. 找出本周重要行业变化。
8. 找出机会。
9. 找出风险。
10. 判断本周知识库新增了什么。
11. 判断哪些专题值得进入下一阶段深度研究。
12. 给出下周重点追踪清单。
13. 对不确定的信息明确标记。
14. 不得编造事实。

输出以下结构：

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

至少5个趋势。

# 三、人物变化

| 人物 | 本周动态 | 为什么重要 |
|---|---|---|

# 四、公司变化

| 公司 | 本周动态 | 战略意义 |
|---|---|---|

# 五、技术变化

| 技术 | 本周进展 | 影响 |
|---|---|---|

# 六、行业变化

分别分析：

- 科技
- 金融
- 商业
- 政策
- 媒体
- 消费
- AI
- 国际局势

# 七、机会

列出本周真正值得关注的机会。

# 八、风险

列出本周值得关注的风险。

# 九、本周知识增长

回答：

“相比上周，我们真正多知道了什么？”

# 十、专题研究方向

从最近7天新闻中选择最值得深入研究的专题。

# 十一、下周重点追踪

| 优先级 | 项目 | 追踪原因 | 观察指标 |
|---|---|---|---|

# 十二、一句话周结论

用一句话总结本周。
"""

    # --------------------------------------------------------
    # AI
    # --------------------------------------------------------

    print()
    print(
        "Generating weekly report..."
    )

    result = call_ai(
        prompt
    )

    # --------------------------------------------------------
    # 输出
    # --------------------------------------------------------

    target = (
        WEEKLY
        / year
    )

    target.mkdir(
        parents=True,
        exist_ok=True
    )

    path = (
        target
        / f"W{week:02d}.md"
    )

    content = f"""---
year: {year}
week: {week}
type: weekly_report
status: generated
---

# {year} W{week:02d} 自生长知识周报

{result}
"""

    path.write_text(
        content,
        encoding="utf-8"
    )

    print()
    print("=" * 70)

    print(
        "✅ WEEKLY REPORT V2 COMPLETE"
    )

    print("=" * 70)

    print(
        f"Output: {path}"
    )


if __name__ == "__main__":

    main()
