#!/usr/bin/env python3
import os, json, re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "05_日报"
WEEKLY = ROOT / "06_周报"

def call_ai(prompt):
    key=os.environ["AI_API_KEY"]
    base=os.getenv("AI_BASE_URL","https://api.openai.com/v1").rstrip("/")
    model=os.environ["AI_MODEL"]
    body=json.dumps({"model":model,"messages":[
        {"role":"system","content":"你是战略知识分析师。严格依据输入，不编造。输出中文Markdown。"},
        {"role":"user","content":prompt}
    ],"ensure_ascii":False).encode()
    req=Request(base+"/chat/completions",data=body,headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
    with urlopen(req,timeout=180) as r: data=json.loads(r.read())
    return data["choices"][0]["message"]["content"]

def main():
    files=sorted(REPORTS.rglob("*.md"))[-7:]
    if len(files)<1: return
    text="\n\n".join(p.read_text(encoding="utf-8")[:20000] for p in files)
    result=call_ai("""请根据下面最近7天（若不足则按已有天数）的知识日报，生成周报。
要求：十大事件、核心趋势、行业变化、机会、风险、知识增长、下周重点追踪、可生成专题。
不要把7篇日报简单拼接，必须进行归纳和趋势判断。

""" + text)
    now=datetime.now(timezone(timedelta(hours=8)))
    year=now.strftime("%Y")
    WEEKLY.mkdir(parents=True,exist_ok=True)
    (WEEKLY/year).mkdir(exist_ok=True)
    (WEEKLY/year/f"W{now.isocalendar().week:02d}.md").write_text(
        f"# {year} W{now.isocalendar().week:02d} 自生长知识周报\n\n{result}\n",encoding="utf-8")

if __name__=="__main__": main()
