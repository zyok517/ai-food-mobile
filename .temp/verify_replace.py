# -*- coding: utf-8 -*-
# 校验替换后 app.js 中737行的图片文件是否都存在于 dist/dish-images/
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APP = r'E:\竞赛\ai+食\ai-food-mobile\dist\app.js'
IMGDIR = r'E:\竞赛\ai+食\ai-food-mobile\dist\dish-images'

with open(APP, encoding='utf-8') as f:
    lines = f.readlines()

loose = re.compile(r"^\s*\[(\d+),'(.+?)',(.*),'([0-9]+\.jpg)'\],?\s*$")
found = 0
bad = []
for l in lines:
    m = loose.match(l.rstrip())
    if m and m.group(4):
        found += 1
        img = m.group(4)
        if not os.path.exists(os.path.join(IMGDIR, img)):
            bad.append((int(m.group(1)), img))

print('含新图片引用的行数:', found)
print('图片文件缺失:', bad if bad else '无')
# 引用图片编号范围
imgs = set()
for l in lines:
    m = loose.match(l.rstrip())
    if m:
        imgs.add(m.group(4))
print('引用的不同图片数:', len(imgs))