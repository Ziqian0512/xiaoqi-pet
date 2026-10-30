import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\xiaoqi_link.py"
s = io.open(P, encoding="utf-8").read()
if "收到 feed" not in s:
    s = s.replace("""    def _on_feed(self, data: dict) -> None:
        try:""",
"""    def _on_feed(self, data: dict) -> None:
        try:
            log.info("xiaoqi: 收到 feed items=%d last_id=%s", len(data.get("items") or []),
                     data.get("last_id"))""")
    s = s.replace("""        except Exception:  # noqa: BLE001
            return""",
"""        except Exception:  # noqa: BLE001
            log.exception("xiaoqi: 处理 feed 失败")
            return""")
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了 feed 日志")
