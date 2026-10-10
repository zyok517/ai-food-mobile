# -*- coding: utf-8 -*-
# 压缩717张菜品图到 dist/dish-images/（640x640, JPEG q80）
import os, io, sys, time
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
SRC = r'E:\竞赛\ai+食\ai-food-mobile\data\dish-images'
DST = r'E:\竞赛\ai+食\ai-food-mobile\dist\dish-images'
os.makedirs(DST, exist_ok=True)

files = sorted([f for f in os.listdir(SRC) if f.endswith('.jpg')])
print('源图片:', len(files), '张')
t0 = time.time()
done = 0
for fn in files:
    src_path = os.path.join(SRC, fn)
    dst_path = os.path.join(DST, fn)
    # 已存在且源未更新则跳过（断点续传）
    if os.path.exists(dst_path) and os.path.getmtime(dst_path) >= os.path.getmtime(src_path):
        done += 1
        continue
    img = Image.open(src_path).convert('RGB')
    img = img.resize((640, 640), Image.LANCZOS)
    img.save(dst_path, 'JPEG', quality=80, optimize=True)
    done += 1
    if done % 100 == 0:
        print('  已处理', done, '/', len(files))

total = sum(os.path.getsize(os.path.join(DST, f)) for f in os.listdir(DST) if f.endswith('.jpg'))
print('完成: {} 张, 耗时 {:.1f}s, 总大小 {:.1f} MB'.format(
    len(os.listdir(DST)), time.time() - t0, total / 1024 / 1024))