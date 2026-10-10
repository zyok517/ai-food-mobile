# -*- coding: utf-8 -*-
# 验证 app.js 数据行格式与 id 连续性
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'E:\竞赛\ai+食\ai-food-mobile\dist\app.js', encoding='utf-8') as f:
    lines = f.readlines()

pat = re.compile(r"^\s*\[(\d+),'([^']+)',.*,'([0-9a-z]+\.jpg)'\],?\s*$")
data_lines = []
for i, l in enumerate(lines, 1):
    m = pat.match(l.rstrip())
    if m:
        data_lines.append((i, int(m.group(1)), m.group(2), m.group(3)))

print('匹配数据行:', len(data_lines))
print('id范围:', data_lines[0][1], '-', data_lines[-1][1])
ids = [d[1] for d in data_lines]
idset = set(ids)
missing = [i for i in range(1, 738) if i not in idset]
print('1-737缺失id:', missing if missing else '无')
dup = [i for i in idset if ids.count(i) > 1]
print('重复id:', dup if dup else '无')
print('首行:', data_lines[0])
print('末3行:')
for d in data_lines[-3:]:
    print(' ', d)
# 图片文件名种类
imgs = set(d[3] for d in data_lines)
print('当前图片文件名种数:', len(imgs))