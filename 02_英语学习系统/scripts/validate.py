from common import normalize
def article(a,words):
    for k in ('title','article_en','article_zh','added_vocabulary','phrases','grammar_points'): 
        if not a.get(k): raise ValueError(f'文章缺少字段: {k}')
    t=normalize(a['article_en'])
    missing=[w['word'] for w in words if normalize(w['word']) not in t]
    if missing: raise ValueError('目标词未全部出现: '+', '.join(missing))
def exam(e):
    if e.get('total_score')!=100: raise ValueError('试卷总分必须为100')
