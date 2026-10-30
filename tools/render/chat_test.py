import json, urllib.request, time
t0=time.time()
body=json.dumps({"model":"dspet","messages":[{"role":"user","content":"在吗"}],"stream":False}).encode()
req=urllib.request.Request("http://100.117.93.31:8787/v1/chat/completions",data=body,headers={"Content-Type":"application/json"})
try:
    with urllib.request.urlopen(req,timeout=120) as r:
        d=json.loads(r.read())
    print("耗时 %.1fs" % (time.time()-t0))
    print("回复:", d["choices"][0]["message"]["content"][:80])
except Exception as e:
    print("失败 %.1fs" % (time.time()-t0), repr(e)[:180])
