import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data:
    if 197 <= d['idx'] <= 200:
        print(f"IDX={d['idx']:03d}")
        print(f"NAME={d['name']}")
        print(f"PROMPT={d['prompt']}")
        print("---")