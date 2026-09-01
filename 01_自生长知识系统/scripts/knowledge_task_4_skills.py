#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""748686 自生长知识系统 - Task 4: 27 Skills V6.5.3."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from knowledge_common import (ROOT, SKILLS_COMPLETE_FILE, load_saved_event_units, load_skills, load_routes, safe_name, call_ai, normalize_language, now, event_units_dir)

MAX_SKILL_CONTEXT=30000

def run_one_skill(event,skill):
    content=event[1].read_text(encoding="utf-8",errors="replace")
    prompt=f"""你正在执行748686自生长知识系统V6.5.3的27 Skills深度处理。

事件：{event[0].get('event_title','')}
Event ID：{event[0].get('event_id','')}
Skill名称：{skill['name']}

Skill规则：
{skill['content']}

EventUnit原文：
{content[:MAX_SKILL_CONTEXT]}

请严格按照该Skill完成深度处理。
不要编造。
只使用EventUnit提供的信息。
输出可直接写入知识库的中文Markdown。"""
    return call_ai(prompt,"你是748686知识系统Skill执行器。严格执行Skill规则，不得编造。",0.2)

def select_skills(skills,routes):
    selected=[]; names=set()
    for _,route_names in routes.items():
        for name in route_names:
            if name not in skills: raise RuntimeError(f"❌ skill_routes.json引用不存在Skill：{name}")
            if name not in names: selected.append(skills[name]); names.add(name)
    return selected or [skills[k] for k in sorted(skills)]

def run_task_4(date,language):
    lang=normalize_language(language)
    files=load_saved_event_units(date,lang)
    skills=load_skills(); routes=load_routes(); selected=select_skills(skills,routes)
    outroot=event_units_dir(date,lang)
    marker=outroot/SKILLS_COMPLETE_FILE
    # marker is valid only if every expected Event x Skill output exists; otherwise rebuild missing only.
    print(f"\nTASK 4 — 27 SKILLS | Events={len(files)} | Skills={len(selected)} | {date}/{lang}")
    for ei,event in enumerate(files,1):
        eid=str(event[0].get("event_id","")).strip()
        if not eid: raise RuntimeError("❌ Event缺少event_id")
        edir=outroot/eid; edir.mkdir(parents=True,exist_ok=True)
        for si,skill in enumerate(selected,1):
            outfile=edir/f"{safe_name(skill['name']).replace('.md','')}.md"
            if outfile.exists() and outfile.stat().st_size>0:
                print(f"[{ei}/{len(files)}][{si}/{len(selected)}] ⏭️ {outfile.name}"); continue
            print(f"[{ei}/{len(files)}][{si}/{len(selected)}] 🤖 {skill['name']}")
            result=run_one_skill(event,skill)
            if not result.strip(): raise RuntimeError(f"❌ Skill结果为空：{eid} / {skill['name']}")
            tmp=outfile.with_name(outfile.name+".tmp"); tmp.write_text(result,encoding="utf-8"); tmp.replace(outfile)
    # Final completeness check.
    missing=[]
    for event,_ in files:
        eid=str(event.get("event_id","")).strip()
        edir=outroot/eid
        for skill in selected:
            p=edir/f"{safe_name(skill['name']).replace('.md','')}.md"
            if not p.exists() or p.stat().st_size<=0: missing.append(f"{eid}/{p.name}")
    if missing: raise RuntimeError(f"❌ TASK 4仍有缺失Skill文件：{missing[:30]}")
    marker.write_text(f"SKILLS_COMPLETE\ndate: {date}\nlanguage: {lang}\nevents: {len(files)}\nskills: {len(selected)}\ncompleted_at: {now().isoformat()}\ntimezone: Asia/Shanghai\n",encoding="utf-8")
    print(f"✅ TASK 4 COMPLETE | {date}/{lang}")
    return True

def main():
    ap=argparse.ArgumentParser(description="748686 Knowledge Task 4 - 27 Skills V6.5.3")
    ap.add_argument("--date",required=True); ap.add_argument("--language",choices=["EN","ZH"],required=True)
    args=ap.parse_args(); run_task_4(args.date,args.language); return 0
if __name__=="__main__": sys.exit(main())
