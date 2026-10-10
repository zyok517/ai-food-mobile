import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    if 60 <= d['idx'] <= 63:
        print(f"PROMPT_{d['idx']:03d}={d['prompt']}")
