import re
from pathlib import Path
from common import normalize
PAT=re.compile(r'^\s*(?:[-*+]\s*|\d+[.)]\s+)([A-Za-z][A-Za-z\s\'’-]*)(?:\s*[—–:-]\s*(.+?))?\s*$')
IMG=re.compile(r'!\[[^]]*\]\(([^)]+)\)')
def parse(path,max_words=200):
    text=path.read_text(encoding='utf-8'); words=[]; seen=set()
    for line in text.splitlines():
        m=PAT.match(line)
        if m:
            w=m.group(1).strip(); meaning=(m.group(2) or '').strip()
            k=normalize(w)
            if k and k not in seen: seen.add(k); words.append({'word':w,'meaning':meaning})
    images=[]
    for x in IMG.findall(text):
        p=(path.parent/x).resolve()
        if not p.exists(): p=(path.parent.parent/x).resolve()
        if p.exists(): images.append(p)
    if len(words)>max_words: raise ValueError(f'词汇数量 {len(words)} 超过上限 {max_words}')
    return words,images
