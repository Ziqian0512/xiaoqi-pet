import sqlite3
import datetime

DB = "file:/home/ubuntu/dspet/data/state/persona_state.db?mode=ro"
c = sqlite3.connect(DB, uri=True)
c.row_factory = sqlite3.Row
rows = list(c.execute(
    "select ts, umo, substr(user_text,1,20) u, substr(her_text,1,24) h"
    " from recent_turns order by id desc limit 6"))
print("=== 最近对话 ===")
for r in rows[::-1]:
    print(" ", r["ts"], r["umo"][:32], "| 他:", r["u"], "| 她:", r["h"])

c2 = sqlite3.connect("file:/home/ubuntu/dspet/data/data_v4.db?mode=ro", uri=True)
c2.row_factory = sqlite3.Row
rows = list(c2.execute(
    "select start_time, end_time from provider_stats order by start_time desc limit 4"))
print("\n=== 最近 LLM 调用 ===")
for r in rows:
    st = datetime.datetime.fromtimestamp(r["start_time"]).strftime("%m-%d %H:%M:%S")
    dur = (r["end_time"] - r["start_time"]) if r["end_time"] else 0
    print(" ", st, "%.1fs" % dur)
