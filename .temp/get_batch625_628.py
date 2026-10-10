import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
for d in data:
    if 625 <= d['idx'] <= 628:
        print(f"IDX={d['idx']:03d}")
        print(f"NAME={d['name']}")
        print(f"PROMPT={d['prompt']}")
        print("---")