import io
P = r"E:\dsh-pet-projects\dspet-main\docs\XIAOQI-BODY.md"
s = io.open(P, encoding="utf-8").read()

SECTION = """

---

## 13. 3D / VRM 路线（2026-10-30 晚定：走 B，不走图生视频）

### 13.1 为什么放弃"2D 图生视频"

| 需求 | 2D 图生视频 | 骨骼（VRM） |
|---|---|---|
| 桌宠待机/点击 | 够用 | 够用 |
| 跳舞（全身） | 每条重生成，一致性难 | 动作库重定向，随便换 |
| **直播**（实时） | **做不到**（是视频不是身体） | 实时驱动，标准 VTuber 方案 |
| 短视频/换装 | 每条重烤 | 换材质/换动作，几分钟一条 |
| 表面成本 | 每条几毛到几块 | 前期建模贵，之后近乎零 |

结论：桌宠只是第一个渲染器；**直播/短视频要的是同一副身体**，所以必须骨骼化。

### 13.2 目标架构

```
                 ┌── xiaoqi.vrm（唯一本体：人形骨架 + 表情 blendshape + 头发物理）
                 │
   ┌─────────────┴──────────────┐
   │                            │
桌宠（现在）                直播 / 短视频
烘焙 WebM 素材             实时驱动 VRM
640×360 VP9 alpha          VSeeFace / Warudo / VMC
   │                            │
   └──── 同一份 act 协议 ────────┘
```

**关键点**：`act` 抽象 id（dance / eat / sleep）不变，多一个渲染器而已。

### 13.3 VRM 从哪来：三条支路

| 支路 | 工具 | 像不像 | 表情/物理 | 时间 |
|---|---|---|---|---|
| **V1 VRoid** | VRoid Studio（免费） | 中等（VRoid 画风，但脸/发/衣可调） | **原生完整**（眨眼、口型、情绪、头发物理） | 捏 2–4 小时 |
| **V2 Tripo → Blender** | Tripo 图生 3D + Blender + VRM Add-on | **最像**（直接吃锚点图） | 要手动加 blendshape、绑头发物理 | 1–3 天，且 Double 双马尾容易糊 |
| **V3 Live2D** | Cubism | **最像（2D 原样）** | 表情参数完整 | 外包 ¥2k–6k；全身舞蹈难 |

**推荐顺序：先 V2 试一次（验证三视图/双马尾会不会糊），不行退 V1，再不行上 V3。**

### 13.4 今晚就能验的一件事

用 Tripo 把 `docs/body/xiaoqi-main-v3-final.png` 跑成 3D，只看三件事：

1. **双马尾**：两条辫子有没有糊成一片
2. **猫耳发箍**：是独立结构还是粘在头发上
3. **脸**：正脸还原度（眼睛、泪痣、下巴）

三项里糊两项 → 放弃 V2，直接 VRoid 重捏。

### 13.5 烘焙管线（桌宠用）

```
VRM → Blender 摆动作（或 Mixamo/VRMA 导入 + 重定向）
     → 渲 640×360、24fps、透明背景（EEVEE，film transparent）
     → ffmpeg 编码 VP9 alpha（同现有素材规格）
     → assets/characters/xiaoqi/videos/<分类>/<动作名>.webm
```

这一步是纯脚本，我可以写；素材只要 3 条就能让桌宠"活"过来（待机 / 跳舞 / 挥手）。

### 13.6 表情与直播

- VRM 的 expressions（happy / angry / sad / relaxed / surprised + blink + viseme）对应她的情绪系统：
  `self_emotion` → blendshape 权重，走 VMC/OSC 推给 VSeeFace
- 直播时"她在说话"用 viseme 驱动口型；桌宠冒泡时也可以顺手推一次表情

### 13.7 成本与风险

| 风险 | 缓解 |
|---|---|
| Tripo 出糊 | 先验一次，糊就走 VRoid |
| VRoid 捏得不像她 | 用 LOOK 的"必须像"逐项对；发型/配色可改，脸型受限于 VRoid 模板 |
| 动作来源 | Mixamo（免费）、VRMA 动作库、自己 K 几条 |
| 头发物理 | VRM SpringBone，双马尾要做 2 组，猫耳不绑 |
"""

if "## 13. 3D / VRM 路线" not in s:
    s = s.rstrip() + SECTION
    io.open(P, "w", encoding="utf-8", newline="\n").write(s)
print("写入 §13:", "## 13. 3D / VRM 路线" in io.open(P, encoding="utf-8").read())
