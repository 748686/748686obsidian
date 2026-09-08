import json
from common import CONFIG,env_required,request_json
from validate import exam as validate_exam
from agnes_generate import ARTICLE_TYPES
def generate(article,difficulty,type_key,words):
    key=env_required(CONFIG['agnes']['api_key']); url=CONFIG['agnes']['base_url'].rstrip('/')+'/chat/completions'
    prompt={'task':'基于指定英语短文生成100分配套试卷','difficulty':f'{difficulty}星','article_type':ARTICLE_TYPES[type_key],'article':article,'target_words':words,'score_scheme':{'listening':30,'single_choice':10,'multiple_choice':10,'cloze':10,'reading':10,'translation':10,'writing':10},'requirements':['所有答案与题目严格一致','听力原文必须与听力题完全一致','只输出JSON','总分必须100'],'schema':{'total_score':100,'listening':{'part_a':[],'part_b':[],'part_c':[],'scripts':[]},'single_choice':[],'multiple_choice':[],'cloze':[],'reading':[],'translation':[],'writing':[],'answers':{}}}
    data=request_json('POST',url,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},json={'model':CONFIG['agnes']['model'],'temperature':0.2,'messages':[{'role':'system','content':'你是严谨的英语考试命题专家，只输出合法JSON。'},{'role':'user','content':json.dumps(prompt,ensure_ascii=False)}]})
    e=json.loads(data['choices'][0]['message']['content']); validate_exam(e); return e
def render(e,title,difficulty,type_name):
    return f"英语短文注记配套试卷 — {title}\n{difficulty}星难度 | 文体：{type_name} | 满分：100分\n\n"+json.dumps(e,ensure_ascii=False,indent=2)
