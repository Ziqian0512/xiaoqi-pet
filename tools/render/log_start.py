import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\xiaoqi_link.py"
s = io.open(P, encoding="utf-8").read()
if "start() 被调用" not in s:
    s = s.replace("""    def start(self) -> None:
        conf = self._conf()""",
"""    def start(self) -> None:
        conf = self._conf()
        log.info("xiaoqi: start() 被调用 enabled=%s base=%s conf_path=%s",
                 conf["enabled"], conf["base_url"], self._conf_path())""")
    s = s.replace("""        if not conf["enabled"] or self._poller is not None:
            return""",
"""        if not conf["enabled"] or self._poller is not None:
            log.info("xiaoqi: 跳过启动（enabled=%s, poller=%s）", conf["enabled"], self._poller is not None)
            return""")
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("加了启动日志")
