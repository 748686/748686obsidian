import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import ROOT,CONFIG
from input_parser import parse
from vision_extract import extract
from agnes_generate import generate as gen_article,ARTICLE_TYPES
from validate import article
from render_markdown import render
from exam_generate import generate as gen_exam,render as render_exam

def main():
 p=argparse.ArgumentParser(); p.add_argument('--date',required=True); p.add_argument('--difficulty',type=int,choices=range(1,18),required=True); p.add_argument('--article-type',choices=ARTICLE_TYPES,required=True); p.add_argument('--length',type=int,required=True); p.add_argument('--exam',choices=['yes','no'],default='no'); p.add_argument('--image',choices=['yes','no'],default='no'); p.add_argument('--audio',choices=['yes','no'],default='no'); p.add_argument('--audio-format',choices=['mp3','m4a','wav'],default='mp3'); p.add_argument('--speed',type=float,default=1.0); a=p.parse_args()
 inp=ROOT/'input'/f'{a.date}.md'; words,images=parse(inp,CONFIG['limits']['max_words'])
 for im in images: words += extract(im)
 uniq={}; [uniq.setdefault(w['word'].lower(),w) for w in words]; words=list(uniq.values())
 out=ROOT/'output'/a.date; out.mkdir(parents=True,exist_ok=True)
 art=gen_article(words,a.difficulty,a.article_type,a.length); article(art,words)
 note_dir=out/'英语短文注记'; note_dir.mkdir(exist_ok=True)
 note=render(art,words,a.difficulty,ARTICLE_TYPES[a.article_type],a.date); (note_dir/f'{a.difficulty}星_{ARTICLE_TYPES[a.article_type]}.md').write_text(note,encoding='utf-8')
 if a.exam=='yes':
  e=gen_exam(art,a.difficulty,a.article_type,words); ed=out/'配套试卷'; ed.mkdir(exist_ok=True); (ed/f'{a.difficulty}星_{ARTICLE_TYPES[a.article_type]}_试卷.md').write_text(render_exam(e,art['title'],a.difficulty,ARTICLE_TYPES[a.article_type]),encoding='utf-8')
 manifest={'date':a.date,'difficulty':a.difficulty,'article_type':ARTICLE_TYPES[a.article_type],'length':a.length,'exam':a.exam,'image':a.image,'audio':a.audio,'audio_format':a.audio_format,'speed':a.speed,'target_words':words,'article_title':art['title']}; (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
 print(f'完成: {out}')
if __name__=='__main__': main()
