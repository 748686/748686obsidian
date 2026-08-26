import os, json, sys
from urllib.request import Request, urlopen

webhook=os.getenv("FEISHU_WEBHOOK","")
path=sys.argv[1] if len(sys.argv)>1 else ""
if not webhook or not path:
    print("未配置飞书Webhook，跳过发送")
    raise SystemExit(0)

text=open(path,encoding="utf-8").read()
text=text[:30000]
payload=json.dumps({
    "msg_type":"text",
    "content":{"text":text}
},ensure_ascii=False).encode()
req=Request(webhook,data=payload,headers={"Content-Type":"application/json"})
with urlopen(req,timeout=30) as r:
    print(r.read().decode())
