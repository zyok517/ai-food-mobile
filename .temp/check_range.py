import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total dishes: {len(data)}")
print(f"Min idx: {min(d['idx'] for d in data)}")
print(f"Max idx: {max(d['idx'] for d in data)}")
missing = [i for i in range(1, max(d['idx'] for d in data)+1) if i not in [d['idx'] for d in data]]
print(f"Missing idx: {missing}")
