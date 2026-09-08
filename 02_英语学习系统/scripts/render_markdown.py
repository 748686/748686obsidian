from common import safe_filename
def render(a,words,difficulty,type_name,date,image=None):
    vocab='<br>'.join(f"{x['word']} — {x.get('meaning','')}" for x in words)
    phrases='<br>'.join(f"{x.get('phrase','')} — {x.get('meaning','')}" for x in a.get('phrases',[])) or '—'
    grammar='<br>'.join(f"{x.get('point','')}：{x.get('explanation','')}" for x in a.get('grammar_points',[])) or '—'
    left=f"**{a['title']}**<br><br>**English**<br>{a['article_en']}<br><br>**中文翻译**<br>{a['article_zh']}"
    if image: left += f"<br><br>![{a['title']}](./{image.name})"
    right=f"**添加的词汇**<br>{vocab}<br><br>**重点短语**<br>{phrases}<br><br>**语法知识点**<br>{grammar}<br><br>**知识结构**<br>{'<br>'.join(a.get('knowledge_structure',[])) or '—'}"
    return f"英语短文注记 — {difficulty}星难度（1篇合集）\n{date}    {type_name}    难度：{difficulty}星\n\n| 学习材料 | 知识整理 |\n|---|---|\n| {left} | {right} |\n"
