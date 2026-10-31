"""小祈联动（Qt 服务）—— 读服务器的 /api/body/feed，驱动桌宠。

G20 §5.2 的约束：
- 不新增依赖（urllib 轮询），不改 window.py
- 只通过注入的 ``win``（实际是 SharedSubsystems.proxy）调 show_bubble /
  request_link_anim / request_link_idle / cats / isVisible
- 断网静默重试，退避到 30 秒
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
import urllib.error
import urllib.request

from PySide6.QtCore import QObject, QThread, QTimer, Signal

from . import xiaoqi_logic as logic

log = logging.getLogger(__name__)

DEFAULT_BASE = "http://100.117.93.31:8787"
DEFAULT_POLL = 3.0
MAX_BACKOFF = 30.0


class _Poller(QThread):
    """后台线程：定期 GET feed。只发信号，不碰 Qt 界面对象。"""

    got = Signal(object)          # dict: feed 数据
    failed = Signal(str)

    def __init__(self, base_url: str, since: int, poll_seconds: float,
                 token: str = "", parent=None) -> None:
        super().__init__(parent)
        self._base = base_url.rstrip("/")
        self._since = int(since)
        self._poll = max(1.0, float(poll_seconds))
        self._token = token or ""
        self._stop = False
        self._backoff = 0.0

    def set_since(self, since: int) -> None:
        self._since = int(since)

    def stop(self) -> None:
        self._stop = True

    def run(self) -> None:  # noqa: D401
        while not self._stop:
            url = "%s/api/body/feed?since=%d&limit=20" % (self._base, self._since)
            try:
                headers = {"User-Agent": "xiaoqi-link/1.0"}
                if self._token:
                    headers["X-Token"] = self._token
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read(200000))
                self._backoff = 0.0
                last = int(data.get("last_id") or self._since)
                items = data.get("items") or []
                if items:
                    self._since = max(last, int(items[-1].get("id") or last))
                else:
                    self._since = max(self._since, last)
                self.got.emit(data)
            except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
                self._backoff = min(MAX_BACKOFF, (self._backoff or 1.0) * 2)
                self.failed.emit(str(exc)[:120])
            wait = self._backoff if self._backoff else self._poll
            slept = 0.0
            while slept < wait and not self._stop:
                time.sleep(0.2)
                slept += 0.2


class XiaoqiLink(QObject):
    """挂在 SharedSubsystems 上的联动服务（与 AgentLinkManager 同构）。"""

    mood_changed = Signal(str)
    heard = Signal()
    spoke = Signal(str)
    acted = Signal(str)
    pack_changed = Signal(str)

    def __init__(self, win, config, parent=None) -> None:
        super().__init__(parent)
        self.win = win
        self.config = config
        self._poller = None
        self._bubble_timer = QTimer(self)
        self._bubble_timer.setSingleShot(True)
        self._bubble_timer.timeout.connect(self._next_bubble)
        self._queue: list[str] = []
        self._last_quadrant = ""
        self._last_action_at = 0.0
        self._last_heard_at = 0.0
        self._since = 0

    # ---- 配置 ----
    # 不往上游 config.json 里加键（那要动它的 3 处登记 + 快照测试）。
    # 独立读一个 xiaoqi.json：放在桌宠配置目录，或由 XIAOQI_CONF 指定路径。
    def _conf_path(self) -> str:
        import os

        env = os.environ.get("XIAOQI_CONF")
        if env:
            return env
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
        # 装好的版本是 dsh-pet-standalone-webm-chat；源码跑是 dsh-pet-standalone
        for name in ("dsh-pet-standalone-webm-chat", "dsh-pet-standalone"):
            path = os.path.join(base, name, "xiaoqi.json")
            if os.path.isfile(path):
                return path
        return os.path.join(base, "dsh-pet-standalone-webm-chat", "xiaoqi.json")

    def _conf(self) -> dict:
        import json as _json
        import os

        raw = {}
        path = self._conf_path()
        try:
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    loaded = _json.load(f)
                if isinstance(loaded, dict):
                    raw = loaded
        except (OSError, ValueError):
            raw = {}
        return {
            "enabled": bool(raw.get("enabled", False)),
            "base_url": str(raw.get("base_url") or DEFAULT_BASE).rstrip("/"),
            "poll_seconds": float(raw.get("poll_seconds") or DEFAULT_POLL),
            "token": str(raw.get("token") or ""),
        }

    # ---- 生命周期 ----
    def start(self) -> None:
        conf = self._conf()
        log.info("xiaoqi: start() 被调用 enabled=%s base=%s conf_path=%s",
                 conf["enabled"], conf["base_url"], self._conf_path())
        if not conf["enabled"] or self._poller is not None:
            log.info("xiaoqi: 跳过启动（enabled=%s, poller=%s）", conf["enabled"], self._poller is not None)
            return
        self._since = 0
        self._poller = _Poller(conf["base_url"], 0, conf["poll_seconds"],
                               token=str(conf.get("token") or ""), parent=self)
        self._poller.got.connect(self._on_feed)
        self._poller.start()

    def stop(self) -> None:
        if self._poller is not None:
            self._poller.stop()
            self._poller.wait(1500)
            self._poller = None

    def restart_if_needed(self) -> None:
        conf = self._conf()
        if not conf["enabled"]:
            self.stop()
            return
        if self._poller is None:
            self.start()

    # ---- 收数据 ----
    def _on_feed(self, data: dict) -> None:
        try:
            _items = data.get("items") or []
            if _items:
                log.info("xiaoqi: 收到 feed items=%d last_id=%s", len(_items),
                         data.get("last_id"))
            now = logic.parse_ts(data.get("now", {}).get("ts") or "") or datetime.now()
            rules = data.get("rules") or {}
            fresh = int(rules.get("fresh_seconds") or 300)
            now_q = str((data.get("now") or {}).get("quadrant") or "")
            if now_q and now_q != self._last_quadrant:
                self._last_quadrant = now_q
                self.mood_changed.emit(now_q)
                self._play_quadrant(now_q)

            items = logic.dedupe(data.get("items") or [], 0)
            for it in items:
                kind = it.get("kind")
                if kind == "heard":
                    self._on_heard(rules)
                elif kind in ("said", "test"):
                    self._enqueue_bubbles(logic.bubble_plan([it], now, fresh))
                    self.spoke.emit(str(it.get("text") or it.get("label") or ""))
                    self._play_item(it, rules)
                elif kind == "act":
                    self._play_item(it, rules)
                    self.acted.emit(str((it.get("extra") or {}).get("action") or ""))
            self._flush_queue()
        except Exception:  # noqa: BLE001
            log.exception("xiaoqi: 处理 feed 失败")
            return

    # ---- 表现 ----
    def _cats(self) -> dict:
        try:
            cats = getattr(self.win, "cats", None)
            return cats if isinstance(cats, dict) else {}
        except Exception:  # noqa: BLE001
            log.exception("xiaoqi: 处理 feed 失败")
            return {}

    def _play_quadrant(self, quadrant: str) -> None:
        action_id = logic.QUADRANT_ACTION.get(quadrant)
        self._play_action(action_id)

    def _play_item(self, item: dict, rules: dict) -> None:
        if item.get("kind") == "act":
            extra = item.get("extra") or {}
            self._play_action(str(extra.get("action") or ""),
                              hold=bool(extra.get("hold")),
                              priority=int(extra.get("priority") or 0))
            return
        quadrant = str(item.get("quadrant") or "")
        if quadrant:
            self._play_quadrant(quadrant)

    def _play_action(self, action_id: str | None, hold: bool = False,
                     priority: int = 0) -> None:
        if not action_id:
            return
        now = time.time()
        # 两秒内不连播（防抽搐）；但高优先级动作（服务器下发的 act / 她的请求）可以打断
        if not hold and priority < 60 and now - self._last_action_at < 2.0:
            return
        clip = logic.resolve_action(action_id, self._cats())
        if not clip:
            return          # 缺素材不演，不报错
        self._last_action_at = now
        try:
            if not getattr(self.win, "isVisible", lambda: True)():
                return
            self.win.request_link_anim(clip)
        except Exception:  # noqa: BLE001
            log.exception("xiaoqi: 处理 feed 失败")
            return

    def _on_heard(self, rules: dict) -> None:
        if not rules.get("react_heard", True):
            return
        now = time.time()
        if now - self._last_heard_at < 2.0:
            return
        self._last_heard_at = now
        self.heard.emit()
        clip = logic.resolve_action("listen", self._cats()) or logic.resolve_action("idle", self._cats())
        if clip:
            try:
                self.win.request_link_anim(clip)
            except Exception:  # noqa: BLE001
                pass
        self._enqueue_bubbles(["……"])

    def _enqueue_bubbles(self, pages: list) -> None:
        for page in pages or []:
            if page:
                self._queue.append(page)
        while len(self._queue) > 3:
            tail = self._queue[-2:]
            self._queue = self._queue[:-2] + ["　".join(tail)]

    def _flush_queue(self) -> None:
        if self._queue and not self._bubble_timer.isActive():
            self._next_bubble()

    def _next_bubble(self) -> None:
        if not self._queue:
            return
        page = self._queue.pop(0)
        try:
            duration = min(8000, max(2500, 900 + len(page) * 120))
            self.win.show_bubble(page, duration_ms=duration)
        except Exception:  # noqa: BLE001
            pass
        if self._queue:
            self._bubble_timer.start(900)
