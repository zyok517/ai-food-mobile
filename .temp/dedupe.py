import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_all.json', 'r', encoding='utf-8') as f:
    dishes = json.load(f)

seen = {}
unique_dishes = []
for d in dishes:
    name = d['name']
    if name not in seen:
        seen[name] = True
        unique_dishes.append({
            'idx': len(unique_dishes) + 1,
            'name': name,
            'window': d['window'],
            'area': d['area'],
            'sheet': d['sheet'],
            'price': d['price'],
            'original_indices': [d['idx']]
        })
    else:
        for u in unique_dishes:
            if u['name'] == name:
                u['original_indices'].append(d['idx'])
                break

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_unique.json', 'w', encoding='utf-8') as f:
    json.dump(unique_dishes, f, ensure_ascii=False, indent=2)

print(f'Total unique dishes: {len(unique_dishes)}')

for d in unique_dishes[:15]:
    print(f"{d['idx']:03d}. {d['name']} [{d['window']}] {d['price']}")
