from PIL import Image
import numpy as np
src = r"E:\dsh-pet-projects\dspet-main\docs\body\xiaoqi-main-v3-final.png"
im = Image.open(src).convert("RGB")
a = np.asarray(im).astype(np.int16)
# 非白像素掩码（阈值放宽，避免阴影被当内容）
mask = (np.abs(255 - a).max(axis=2) > 12)
ys, xs = np.where(mask)
y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
print("内容框:", (x0, y0, x1, y1), "原尺寸:", im.size)
pad = 20
box = (max(0, x0-pad), max(0, y0-pad), min(im.width, x1+pad), min(im.height, y1+pad))
crop = im.crop(box)
# Tripo 喜欢 2 的幂附近、长边 <= 2048；这里保持原比例
out = r"E:\dsh-pet-projects\build\tripo-in-white.png"
crop.save(out)
print("输出:", out, crop.size)
