from pathlib import Path
import base64, json, os, re, time, requests
ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config/settings.json").read_text(encoding="utf-8"))
def env_required(name):
    v=os.getenv(name)
    if not v: raise RuntimeError(f"缺少环境变量: {name}")
    return v
def normalize(s): return re.sub(r"\s+", " ", s.strip().lower())
def safe_filename(s): return re.sub(r'[\\/:*?"<>|]', '_', s).strip()[:120]
def request_json(method,url,headers=None,**kwargs):
    last=None
    for i in range(5):
        try:
            r=requests.request(method,url,headers=headers,timeout=180,**kwargs)
            if r.status_code < 400: return r.json()
            if r.status_code not in (429,500,502,503,504): r.raise_for_status()
            last=RuntimeError(f"HTTP {r.status_code}: {r.text[:500]}")
        except Exception as e:
            last=e
        time.sleep(min(30,2**i))
    raise last
def save_b64(data,path):
    path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(base64.b64decode(data))
