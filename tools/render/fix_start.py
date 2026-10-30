import io
P = r"E:\dsh-pet-projects\xiaoqi-pet\pet\app.py"
s = io.open(P, encoding="utf-8").read()
old = """        self._shared = SharedSubsystems(self)  # 4.4b：常开化（T6）"""
new = """        self._shared = SharedSubsystems(self)  # 4.4b：常开化（T6）
        # G20：小祈联动在壳构造时就起——overlay 拓扑下 SharedSubsystems.start()
        # 不会被调用，挂在 start() 里会永远不启动（2026-10-30 实测）。
        try:
            self._shared.xiaoqi.start()
        except Exception:  # noqa: BLE001
            logging.exception("xiaoqi: 联动启动失败")"""
assert old in s and "G20：小祈联动在壳构造时就起" not in s
s = s.replace(old, new, 1)
io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("已改 app.py：构造时启动 xiaoqi")
