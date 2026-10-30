import json, urllib.request
try:
    req = urllib.request.Request("http://100.117.93.31:8787/api/body/feed?limit=5",
                                 headers={"X-Token": "hk-rpH2Hj8G0IHQBlrx"})
    with urllib.request.urlopen(req, timeout=10) as r:
        d = json.loads(r.read())
    print("feed ok, last_id=", d.get("last_id"), "posture=", d.get("now", {}).get("posture"))
except Exception as e:
    print("feed 失败:", repr(e)[:120])
