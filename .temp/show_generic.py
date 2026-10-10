import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

generic = [d for d in data if 'A plate of Chinese dish,' in d['prompt']]
for d in generic:
    print(f"{d['idx']:03d}|||{d['name']}|||{d['window']}")
