# -*- coding: utf-8 -*-
# 替换 app.js 中737行数据的图片字段为717张新图
# 逻辑：mapping.json 的 original_indices 是原Excel行号 -> 需换算成 app.js 的菜品 id
# 换算公式（由 explore agent 验证）：
#   id <= 82: id = orig
#   83 <= id <= 520: id = orig - 1
#   id >= 521: id = orig - 2
# 菜名需同时校验，防错位
import io, sys, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

APP = r'E:\竞赛\ai+食\ai-food-mobile\dist\app.js'
MAP = r'E:\竞赛\ai+食\ai-food-mobile\data\dish-image-mapping.json'

# 1. 加载映射
with open(MAP, encoding='utf-8') as f:
    mapping = json.load(f)

def orig_to_id(orig):
    if orig <= 82:
        return orig
    elif orig <= 521:
        return orig - 1
    else:
        return orig - 2

# 构建 id -> (image, name) 映射
id_map = {}
for d in mapping['dishes']:
    for orig in d['original_indices']:
        did = orig_to_id(orig)
        if did in id_map:
            # 已有映射（重复菜共用），保留
            continue
        id_map[did] = (d['image'], d['name'])

print('id_map 大小:', len(id_map), '(应为737)')
missing_ids = [i for i in range(1, 738) if i not in id_map]
print('1-737无映射的id:', missing_ids if missing_ids else '无')

# 2. 读取 app.js 并逐行替换
with open(APP, encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

loose = re.compile(r"^\s*\[(\d+),'([^']+)',(.*)$")
# 替换行尾图片字段的正则：匹配最后一组 ,'xxx.jpg'],
img_pat = re.compile(r"^(.*),'[0-9a-zA-Z_]+\.jpg'\],?$")

replaced = 0
name_mismatch = []
new_lines = []
for l in lines:
    m = loose.match(l)
    if m and ".jpg'" in l:
        did = int(m.group(1))
        if did in id_map:
            img, name = id_map[did]
            # 菜名校验（去空格比较）
            jname = m.group(2).replace(' ', '')
            if jname and jname != name.replace(' ', '') and name.replace(' ', '') not in jname and jname not in name.replace(' ', ''):
                name_mismatch.append((did, jname, name))
            mi = img_pat.match(l.rstrip())
            if mi:
                nl = mi.group(1) + ",'" + img + "'],"
                # 保持原有行尾格式（若有逗号）
                new_lines.append(nl)
                replaced += 1
                continue
    new_lines.append(l)

print('替换行数:', replaced)
print('菜名不完全一致的条目数:', len(name_mismatch))
for t in name_mismatch[:10]:
    print('  id={}, app.js={}, mapping={}'.format(*t))

if replaced == 737:
    with open(APP, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    print('已写回 app.js')
else:
    print('!! 替换数异常，未写回。请检查。')