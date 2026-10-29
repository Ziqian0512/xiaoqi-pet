"""小祈联动（纯逻辑，零 Qt）—— 可单测。

设计见 G20 §2A/2B：
- 服务器只给"抽象动作 id"和文本，渲染细节在这里翻译成当前角色的动画名
- 缺动作就回退 idle，绝不因为缺素材不演而报错
- 气泡有长度分页和队列上限，避免一口气刷屏
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

# 象限 → 首选动作 id（抽象，不是文件名）
QUADRANT_ACTION = {
    "黏人": "cling",
    "活泼": "happy",
    "松弛": "idle",
    "乖软": "idle",
    "带刺": "turn_away",
    "慌": "rub_eyes",
    "懒得理": "turn_away",
    "蔫": "sleep",
}

# 姿态 → 持续动画 id
POSTURE_ACTION = {"awake": None, "sleepy": "rub_eyes", "asleep": "sleep"}


def resolve_action(action_id: str, cats: dict, motion: dict | None = None) -> str | None:
    """抽象 id → 当前角色真实动画名。找不到就按关键词回退，最后回 None。

    cats 是桌宠给的分类：{'idles': [...], 'clicks': [...], 'acts': [...], 'moves': [...], 'turns': [...]}
    motion 是角色包里的映射：{'dance': ['跳舞', 'dance'], ...}
    """
    if not action_id:
        return None
    pools: list[str] = []
    for key in ("acts", "clicks", "idles", "moves", "turns", "idle", "click"):
        value = cats.get(key) if isinstance(cats, dict) else None
        if isinstance(value, (list, tuple)):
            pools.extend(str(x) for x in value)
    if not pools:
        return None

    motion = motion or {}
    wanted = [str(action_id)]
    aliases = motion.get(action_id) or []
    if isinstance(aliases, str):
        aliases = [aliases]
    wanted.extend(str(a) for a in aliases)

    lower = {p.lower(): p for p in pools}
    for word in wanted:
        if word.lower() in lower:
            return lower[word.lower()]
    for word in wanted:
        for p in pools:
            if word.lower() in p.lower():
                return p
    return None


def parse_ts(ts: str) -> datetime | None:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(str(ts), fmt)   # naive：和 datetime.now() 同口径
        except (ValueError, TypeError):
            continue
    return None


def is_fresh(ts: str, now: datetime, fresh_seconds: int) -> bool:
    when = parse_ts(ts)
    if when is None:
        return True
    try:
        return abs((now - when).total_seconds()) <= max(1, int(fresh_seconds))
    except TypeError:
        return True


def dedupe(items: Iterable[dict], last_id: int = 0) -> list:
    """只保留 id 大于游标的，并去重（同一 id 只留一条）。"""
    out, seen = [], set()
    for it in items or []:
        try:
            sid = int(it.get("id"))
        except (TypeError, ValueError):
            continue
        if sid <= int(last_id or 0) or sid in seen:
            continue
        seen.add(sid)
        out.append(it)
    out.sort(key=lambda x: int(x.get("id") or 0))
    return out


def paginate(text: str, max_chars: int = 48, max_pages: int = 3) -> list:
    """长文本分页：优先按句号/换行断，其次硬切。空文本返回 []。"""
    text = (text or "").strip()
    if not text:
        return []
    pages: list[str] = []
    rest = text
    while rest and len(pages) < max_pages:
        if len(rest) <= max_chars:
            pages.append(rest)
            rest = ""
            break
        cut = max_chars
        for mark in ("。", "！", "？", "\n", "，"):
            pos = rest.rfind(mark, 0, max_chars)
            if pos > max_chars // 3:
                cut = pos + 1
                break
        pages.append(rest[:cut])
        rest = rest[cut:].lstrip()
    if rest and pages:
        pages[-1] = (pages[-1] + rest)[:max_chars * 2]
    return pages


def bubble_plan(items: Iterable[dict], now: datetime, fresh_seconds: int = 300,
                 max_items: int = 3, max_chars: int = 48) -> list:
    """把 feed 条目变成"要飘的字"：过滤太旧、合并超出上限、分页。"""
    texts: list[str] = []
    for it in items or []:
        if it.get("kind") not in ("said", "test"):
            continue
        if not is_fresh(it.get("ts", ""), now, fresh_seconds):
            continue
        text = (it.get("text") or it.get("label") or "").strip()
        if not text:
            continue
        texts.extend(paginate(text, max_chars=max_chars, max_pages=2))
    if len(texts) > max_items:
        texts = texts[: max_items - 1] + ["　".join(texts[max_items - 1:])[:max_chars * 2]]
    return texts


def pick_action_for_item(item: dict, cats: dict, motion: dict | None = None) -> str | None:
    """一条 feed → 该播什么。act 用自己的 action，其余按象限。"""
    if not isinstance(item, dict):
        return None
    if item.get("kind") == "act":
        action = str(((item.get("extra") or {}).get("action")) or "")
        return resolve_action(action, cats, motion)
    quadrant = str(item.get("quadrant") or "")
    action_id = QUADRANT_ACTION.get(quadrant)
    return resolve_action(action_id, cats, motion) if action_id else None
