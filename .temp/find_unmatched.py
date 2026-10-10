# -*- coding: utf-8 -*-
# 找出未能匹配的51个id的实际行内容
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'E:\竞赛\ai+食\ai-food-mobile\dist\app.js', encoding='utf-8') as f:
    lines = f.readlines()

pat = re.compile(r"^\s*\[(\d+),'([^']+)',.*,'([0-9a-z]+\.jpg)'\],?\s*$")
matched_ids = set()
for l in lines:
    m = pat.match(l.rstrip())
    if m:
        matched_ids.add(int(m.group(1)))

all_ids = set()
# 宽松匹配：找所有以 [数字,' 开头的行
loose = re.compile(r"^\s*\[(\d+),'")
for i, l in enumerate(lines, 1):
    m = loose.match(l)
    if m:
        all_ids.add(int(m.group(1)))

print('宽松匹配总行数:', len(all_ids))
unmatched = sorted(all_ids - matched_ids)
print('宽匹配但严格不匹配的id数:', len(unmatched))
for uid in unmatched[:6]:
    for i, l in enumerate(lines, 1):
        if l.startswith('  [%d,' % uid):
            print('id={} 行{}: {}'.format(uid, i, l[:150]))
            break