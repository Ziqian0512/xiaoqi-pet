import json
import sqlite3

DB = "file:/home/ubuntu/dspet/data/data_v4.db?mode=ro"
c = sqlite3.connect(DB, uri=True)
c.row_factory = sqlite3.Row

rows = list(c.execute(
    "select conversation_id, user_id, length(content) n, updated_at from conversations"
    " where user_id like '%pet%' order by updated_at desc limit 6"))
for r in rows:
    print(dict(r))

row = c.execute(
    "select content from conversations where user_id="
    "'webchat:FriendMessage:webchat!pet!' order by updated_at desc limit 1").fetchone()
if row:
    msgs = json.loads(row["content"])
    print("\n条数:", len(msgs))
    for m in msgs[-5:]:
        print(" ", m.get("role"), "|", str(m.get("content"))[:90].replace("\n", " "))
else:
    print("\n没有 webchat!pet! 这条会话")
