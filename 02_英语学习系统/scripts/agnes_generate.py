import json
from common import CONFIG, env_required, request_json
DIFFICULTIES={i:f'{i}星' for i in range(1,18)}
ARTICLE_TYPES={'narration':'记叙文','argumentation':'议论文','exposition':'说明文','description':'描写文','letter':'应用文-书信','diary':'应用文-日记','notice':'应用文-通知','poster':'应用文-海报','speech':'应用文-演讲稿','prose':'散文','science':'科技文','news':'新闻报道','review':'评论文','story':'故事','comparison':'对比文','fairy_tale':'童话故事','interview':'采访'}
def generate(words,difficulty,article_type,length):
    key=env_required(CONFIG['agnes']['api_key_env']); url=CONFIG['agnes']['base_url'].rstrip('/')+'/chat/completions'
    payload={'model':CONFIG['agnes']['model'],'temperature':0.4,'messages':[{'role':'system','content':'你是严格的英语教材生成器。只输出合法JSON，不要Markdown代码围栏。'}, {'role':'user','content':json.dumps({'task':'生成英语学习短文','difficulty':f'{difficulty}星','article_type':ARTICLE_TYPES[article_type],'target_length':length,'words':words,'requirements':['所有目标词必须以原形出现在英文文章中','文体必须符合指定类型','难度必须真实改变句法、逻辑、结构和词汇','提供完整中文翻译','短文中的重点短语和语法知识点必须真实存在于文章中'],'schema':{'title':'string','article_en':'string','article_zh':'string','added_vocabulary':'array','phrases':'array','grammar_points':'array','knowledge_structure':'array'}},ensure_ascii=False)}]}
    data=request_json('POST',url,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'},json=payload)
    content=data['choices'][0]['message']['content']; return json.loads(content)
