import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Write generic dishes to a JSON file for reading
generic = [d for d in data if 'A plate of Chinese dish,' in d['prompt']]
output = [{"idx": d['idx'], "name": d['name'], "window": d['window']} for d in generic]

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\generic_dishes.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
