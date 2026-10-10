# -*- coding: utf-8 -*-
# 生成菜品-图片对应表 JSON：dish-image-mapping.json（供前端引用）
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json'
DST = r'E:\竞赛\ai+食\ai-food-mobile\data\dish-image-mapping.json'

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

result = {
    "version": "2.0",
    "image_dir": "data/dish-images",
    "image_size": "2048x2048",
    "total_dishes": len(data),
    "total_images": len(data),
    "note": "idx即图片编号（如idx=17对应017.jpg），idx=83在原Excel中不存在，已跳过",
    "dishes": []
}

for d in data:
    result["dishes"].append({
        "idx": d["idx"],
        "image": "{:03d}.jpg".format(d["idx"]),
        "name": d["name"],
        "window": d["window"],
        "area": d["area"],
        "price": d["price"],
        "original_indices": d["original_indices"]
    })

with open(DST, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("OK ->", DST)
print("dishes:", len(result["dishes"]))
print("idx range:", result["dishes"][0]["idx"], "-", result["dishes"][-1]["idx"])
# 校验文件是否真实存在
import os
missing = [d["idx"] for d in result["dishes"]
           if not os.path.exists(r'E:\竞赛\ai+食\ai-food-mobile\data\dish-images\{:03d}.jpg'.format(d["idx"]))]
print("缺失图片:", missing if missing else "无")