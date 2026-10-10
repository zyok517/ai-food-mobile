import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    if 44 <= d['idx'] <= 47:
        print(f"PROMPT_{d['idx']:03d}={d['prompt']}")
