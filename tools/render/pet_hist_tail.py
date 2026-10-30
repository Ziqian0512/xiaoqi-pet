import json
import sqlite3

c = sqlite3.connect("file:/home/ubuntu/dspet/data/data_v4.db?mode=ro", uri=True)
c.row_factory = sqlite3.Row
row = c.execute(
    "select content from conversations where user_id="
    "'webchat:FriendMessage:webchat!pet!pet-main' order by updated_at desc limit 1").fetchone()
msgs = json.loads(row["content"])
print("条数:", len(msgs))
for m in msgs[-6:]:
    role = m.get("role")
    content = m.get("content")
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict):
                t = p.get("type")
                if t == "text":
                    parts.append(str(p.get("text"))[:120])
                elif t == "think":
                    parts.append("[think] " + str(p.get("think"))[:60])
        content = " / ".join(parts)
    print(" %-9s | %s" % (role, str(content)[:200].replace("\n", " ")))
