import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract prompts for a range
for d in data:
    if 16 <= d['idx'] <= 19:
        print(f"PROMPT_{d['idx']:03d}={d['prompt']}")
