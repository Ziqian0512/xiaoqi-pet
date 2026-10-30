import json, urllib.request, time
body=json.dumps({"model":"dspet","messages":[{"role":"user","content":"在吗"}],"stream":True}).encode()
req=urllib.request.Request("http://100.117.93.31:8787/v1/chat/completions",data=body,
                           headers={"Content-Type":"application/json","Accept":"text/event-stream"})
t0=time.time(); chunks=[]
with urllib.request.urlopen(req,timeout=120) as r:
    for line in r:
        s=line.decode("utf-8","replace").strip()
        if not s.startswith("data:"): continue
        payload=s[5:].strip()
        if payload=="[DONE]": break
        try:
            d=json.loads(payload)
            for ch in d.get("choices",[]):
                delta=ch.get("delta",{})
                if delta.get("content"): chunks.append(delta["content"])
        except ValueError: pass
print("耗时 %.1fs 块数=%d" % (time.time()-t0, len(chunks)))
print("拼起来:", "".join(chunks)[:100])
