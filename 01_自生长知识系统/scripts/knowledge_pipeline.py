#!/usr/bin/env python3
"""
748686 自生长知识系统
负责：
1. 读取 Horizon 生成的日报
2. 按日期归档
3. 读取 Skills
4. 调用 OpenAI-compatible API 生成知识处理结果
5. 生成日报、知识卡片、周报/专题基础文件
"""

import os, json, re, shutil, subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SYSTEM = ROOT / "00_System"
SKILLS = ROOT / "Skills"
NEWS = ROOT / "01_新闻"
REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"
TOPICS = ROOT / "07_专题报告"
KNOWLEDGE = ROOT / "08_知识库"
LOGS = SYSTEM / "运行日志"

def now():
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)

def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def safe_name(s):
    s = re.sub(r'[\\/:*?"<>|]', "_", s)
    return s[:100].strip() or "未命名"

def call_ai(prompt):
    api_key = os.getenv("AI_API_KEY", "")
    base = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("AI_MODEL", "")
    if not api_key or not model:
        raise RuntimeError("缺少 AI_API_KEY 或 AI_MODEL")

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你是748686自生长知识系统的知识工程师。严格依据输入，不编造事实。输出Markdown。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }).encode("utf-8")

    req = Request(
        base + "/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    )
    with urlopen(req, timeout=180) as r:
        data = json.loads(r.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"]

def load_skills():
    result = {}
    for p in SKILLS.rglob("*.md"):
        try:
            result[p.name] = p.read_text(encoding="utf-8")
        except Exception:
            pass
    return result

def horizon_summary():
    # Horizon 默认将日报放在其 data/summaries 下。
    # workflow 会把 horizon 仓库放在临时目录，因此这里寻找最近的 Markdown。
    candidates = list(Path("/tmp/horizon/data/summaries").glob("*.md"))
    if not candidates:
        candidates = list(Path("/tmp/horizon/data/summaries").rglob("*.md"))
    if not candidates:
        raise FileNotFoundError("没有找到 Horizon 生成的日报")
    return max(candidates, key=lambda p: p.stat().st_mtime).read_text(encoding="utf-8")

def main():
    t = now()
    date = t.strftime("%Y-%m-%d")
    year, month = t.strftime("%Y"), t.strftime("%m")

    for d in [NEWS, REPORTS, WEEKLY, TOPICS, KNOWLEDGE, LOGS]:
        d.mkdir(parents=True, exist_ok=True)

    day_dir = NEWS / year / month / date
    day_dir.mkdir(parents=True, exist_ok=True)

    summary = horizon_summary()
    (day_dir / f"{date}_Horizon日报.md").write_text(summary, encoding="utf-8")

    skills = load_skills()
    if not skills:
        raise RuntimeError("Skills 文件夹为空，请先放入27个Skill文件。")

    # 为避免一次请求过大，优先使用最相关的通用技能。
    preferred = [
        "总结文章.md", "金字塔原理.md", "四维价值模型.md",
        "日报编写助手.md", "周报编写助手.md"
    ]
    selected = {k:v for k,v in skills.items() if k in preferred}
    skill_text = "\n\n".join(f"## SKILL: {k}\n{v}" for k,v in selected.items())

    prompt = f"""日期：{date}

下面是 Horizon 今日新闻摘要：
---BEGIN HORIZON---
{summary[:50000]}
---END HORIZON---

下面是系统核心 Skills：
---BEGIN SKILLS---
{skill_text[:50000]}
---END SKILLS---

请生成一份“自生长知识日报”，要求：
1. 保留事实与原始来源，不虚构。
2. 提取今日最重要事件。
3. 识别重复事件与共同主题。
4. 提炼趋势、机会、风险。
5. 提取值得进入长期知识库的实体：人物、公司、产品、技术、行业、概念。
6. 给每个实体写一条简洁知识卡片。
7. 给出“明日值得继续追踪”的项目。
8. 最后列出“可进一步生成的专题报告”。
"""

    report = call_ai(prompt)
    report_path = REPORTS / year / month
    report_path.mkdir(parents=True, exist_ok=True)
    report_path = report_path / f"{date}.md"
    report_path.write_text(f"# {date} 自生长知识日报\n\n{report}\n", encoding="utf-8")

    # 保存运行日志
    log = LOGS / f"{date}.md"
    log.write_text(
        f"# {date} 运行日志\n\n"
        f"- 时间：{t.isoformat()}\n"
        f"- Horizon日报：成功\n"
        f"- Skills数量：{len(skills)}\n"
        f"- 自生长日报：成功\n",
        encoding="utf-8"
    )

    # GitHub Actions 中让后续步骤知道输出位置
    print(f"DAILY_REPORT={report_path}")

if __name__ == "__main__":
    main()
