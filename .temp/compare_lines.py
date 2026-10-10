# -*- coding: utf-8 -*-
# 对比匹配/未匹配行的差异
import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'E:\竞赛\ai+食\ai-food-mobile\dist\app.js', encoding='utf-8') as f:
    lines = f.readlines()

pat = re.compile(r"^\s*\[(\d+),'([^']+)',.*,'([0-9a-z]+\.jpg)'\],?\s*$")
loose = re.compile(r"^\s*\[(\d+),'")

# 收集全部数据行
all_rows = {}
for i, l in enumerate(lines, 1):
    m = loose.match(l)
    if m:
        all_rows[int(m.group(1))] = l

ok = all_rows[1].rstrip()
bad = all_rows[359].rstrip()
print('OK 行1 :', repr(ok))
print('BAD行359:', repr(bad))
# 长度与逐字符对比
print('长度: ok={}, bad={}'.format(len(ok), len(bad)))
# 严格匹配 bad
print('bad 严格匹配:', bool(pat.match(bad)))
print('ok 严格匹配:', bool(pat.match(ok)))
# 找出所有未匹配id的行尾字符
unmatched_ids = [359, 360, 361, 521, 522, 568, 569, 570]
for uid in unmatched_ids:
    r = all_rows[uid].rstrip()
    print('id={} 尾部30字符: {}'.format(uid, repr(r[-30:])))