"""小祈联动纯逻辑的测试（G20 §5.2：零 Qt，可直接单测）。"""

from datetime import datetime, timedelta, timezone

from pet import xiaoqi_logic as L

CATS = {
    "idles": ["待机"],
    "clicks": ["摸摸头", "点一下"],
    "acts": ["开心", "跳舞", "吃东西", "睡觉", "挥手"],
    "moves": ["走两步"],
    "turns": ["转身"],
}


def test_resolve_exact_and_alias():
    assert L.resolve_action("dance", {"acts": ["dance"]}) == "dance"
    assert L.resolve_action("dance", CATS, {"dance": ["跳舞"]}) == "跳舞"


def test_resolve_falls_back_to_keyword_then_none():
    assert L.resolve_action("eat", CATS, {"eat": ["吃"]}) == "吃东西"
    assert L.resolve_action("nonexistent", CATS) is None
    assert L.resolve_action("dance", {}) is None


def test_paginate_short_and_long():
    assert L.paginate("") == []
    assert L.paginate("好呀") == ["好呀"]
    long = "一" * 120
    pages = L.paginate(long, max_chars=50, max_pages=3)
    assert len(pages) == 3
    assert all(len(p) <= 100 for p in pages)


def test_is_fresh_window():
    now = datetime(2026, 10, 30, 12, 0, 0)
    fresh_ts = (now - timedelta(seconds=60)).strftime("%Y-%m-%d %H:%M:%S")
    old_ts = (now - timedelta(seconds=600)).strftime("%Y-%m-%d %H:%M:%S")
    assert L.is_fresh(fresh_ts, now, 300)
    assert not L.is_fresh(old_ts, now, 300)


def test_dedupe_by_cursor():
    items = [{"id": 1}, {"id": 2}, {"id": 2}, {"id": 3}, {"id": "x"}]
    assert [i["id"] for i in L.dedupe(items, 1)] == [2, 3]


def test_bubble_plan_merges_overflow():
    now = datetime(2026, 10, 30, 12, 0, 0)
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    items = [{"kind": "said", "ts": ts, "text": "第一句"}, {"kind": "said", "ts": ts, "text": "第二句"},
             {"kind": "said", "ts": ts, "text": "第三句"}, {"kind": "said", "ts": ts, "text": "第四句"}]
    pages = L.bubble_plan(items, now, 300, max_items=3, max_chars=20)
    assert len(pages) <= 3
    assert pages  # 至少有内容


def test_pick_action_for_item():
    now_item = {"kind": "said", "quadrant": "活泼"}
    assert L.pick_action_for_item(now_item, CATS) == "开心"
    act_item = {"kind": "act", "extra": {"action": "dance"}}
    assert L.pick_action_for_item(act_item, CATS) == "跳舞"
