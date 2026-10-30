import json, urllib.request, time
t0=time.time()
body=json.dumps({"model":"dspet","messages":[{"role":"user","content":"在吗"}],"stream":False}).encode()
req=urllib.request.Request("http://100.117.93.31:8787/v1/chat/completions",data=body,headers={"Content-Type":"application/json"})
try:
    with urllib.request.urlopen(req,timeout=120) as r:
        d=json.loads(r.read())
    print("relay 回复(%.1fs):" % (time.time()-t0), d["choices"][0]["message"]["content"][:60])
except Exception as e:
    print("relay 失败:", repr(e)[:150])
