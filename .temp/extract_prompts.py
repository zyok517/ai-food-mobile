import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Output prompts for dishes 16-50 (idx 16 to 50)
for d in data:
    if 16 <= d['idx'] <= 50:
        print(f"{d['idx']:03d}|||{d['name']}|||{d['prompt']}")
