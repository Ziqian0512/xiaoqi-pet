# 小祈联动（fork 增量）

这个 fork 只做一件事：让桌宠变成**小祈的身体**——读服务器的 `/api/body/feed`，
把她的姿态、说的话、要做的动作演出来。上游代码尽量不动。

## 改了什么

| 文件 | 性质 | 内容 |
|---|---|---|
| `pet/xiaoqi_logic.py` | 新增 | 纯函数：抽象动作 id → 动画名、新鲜度、去重、分页、气泡计划 |
| `pet/xiaoqi_link.py` | 新增 | Qt 服务：每 3 秒拉一次 feed，驱动 `show_bubble` / `request_link_anim` |
| `pet/multi_window_shared.py` | 两行 | `SharedSubsystems.__init__` 里建 `self.xiaoqi`；`start()` 启动、`stop_all()` 收口 |
| `tests/test_xiaoqi_logic.py` | 新增 | 纯逻辑单测 |

**没有改** `pet/config.py`、`pet/window.py`、`pet/app.py`、`pet/modern_settings_dialog.py`。
配置走独立文件，见下。

## 配置

不往上游 `config.json` 里加键（那要动三处登记 + 快照测试）。单独读一个文件：

```
%APPDATA%\dsh-pet-standalone-webm-chat\xiaoqi.json
```

```json
{
  "enabled": true,
  "base_url": "http://100.117.93.31:8787",
  "poll_seconds": 3
}
```

环境变量 `XIAOQI_CONF` 可以指定别的路径（测试用）。**默认是关闭的**：不放这个文件、
或 `enabled: false`，就一直不连，不影响原来的桌宠行为。

## 它怎么工作

```
每 3 秒 GET {base_url}/api/body/feed?since=<游标>
  ├─ now.quadrant 变了        → 播该心情的动作（2 秒内不连播）
  ├─ items[kind=heard]        → 播"听到"动作 + 冒一个「……」
  ├─ items[kind=said|test]    → 冒气泡（长文本分页，最多 3 条排队）
  ├─ items[kind=act]          → 播 extra.action（priority≥60 可打断节流）
  └─ now.posture=asleep       → 后续接持续姿势（v2，当前只作为数据）
```

动作名解析顺序：抽象 id 在 `proxy.cats` 里 → 关键词匹配 → 回退 `idle`。
**缺素材就不演，不报错**。

## 本地跑（源码模式）

需要 Python 3.11+ 和依赖：

```powershell
cd E:\dsh-pet\xiaoqi-pet
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python -m pet
```

（先在 `xiaoqi.json` 里把 `enabled` 设成 true，并确认服务器地址可达。）

## 还没做

- 持续姿势（睡着时一直趴着）：要做"组合 provider"，见 G20 §2A 第 6 条
- 形象包下载 / 换装：先在控制台管，v1 不动
- 反向回传（桌宠告诉服务器"我在演什么"）
