import json
import re

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_unique.json', 'r', encoding='utf-8') as f:
    dishes = json.load(f)

# Filter out invalid entries
valid_dishes = []
for d in dishes:
    name = d['name']
    # Skip header rows
    if name in ('菜名', '窗口', '价格', None, ''):
        continue
    if d['window'] in ('窗口', None, ''):
        continue
    if d['price'] in ('价格', None, ''):
        continue
    valid_dishes.append(d)

print(f"Valid dishes: {len(valid_dishes)} (filtered from {len(dishes)})")

# Build prompts for each dish
STYLE = "cartoon style illustration, flat design, cute kawaii food illustration, warm cream background, soft warm colors, appetizing, simple and clean, no text"

def build_prompt(name, window):
    """Build an English image generation prompt based on dish name and window."""
    # Translate common ingredients/dish types
    prompt = translate_dish(name, window)
    return f"{prompt}, {STYLE}"

def translate_dish(name, window):
    """Translate Chinese dish name to English description for image prompt."""
    n = name.lower().strip()

    # Try specific matches first
    descriptions = {
        # Water dumplings
        "鲜肉大葱水饺": "A plate of Chinese boiled dumplings with fresh pork and scallion filling, steaming hot, plump dumpling wrappers with scallion bits, a small dipping sauce dish, wooden chopsticks",
        "鲜肉白菜水饺": "A plate of Chinese boiled dumplings with fresh pork and napa cabbage filling, steaming hot, plump dumplings with cabbage bits, a small dipping sauce dish, wooden chopsticks",
        "鲜肉芹菜水饺": "A plate of Chinese boiled dumplings with fresh pork and celery filling, steaming hot, plump dumplings with green celery bits, a small dipping sauce dish, wooden chopsticks",
        "韭菜鸡蛋水饺": "A plate of Chinese boiled dumplings with chive and egg filling, steaming hot, plump dumplings with green chive bits and golden egg, a small dipping sauce dish, wooden chopsticks",
        "鲜肉玉米水饺": "A plate of Chinese boiled dumplings with fresh pork and corn kernels filling, steaming hot, plump dumplings with yellow corn bits, a small dipping sauce dish, wooden chopsticks",
        "鲜肉韭菜水饺": "A plate of Chinese boiled dumplings with fresh pork and chive filling, steaming hot, plump dumplings with green chive bits, a small dipping sauce dish, wooden chopsticks",
        "鲜肉茴香水饺": "A plate of Chinese boiled dumplings with fresh pork and fennel filling, steaming hot, plump dumplings with green fennel bits, a small dipping sauce dish, wooden chopsticks",
        "混搭水饺": "A plate of mixed Chinese boiled dumplings with assorted colorful fillings, steaming hot, colorful plump dumplings with different colored wrappers, a small dipping sauce dish, wooden chopsticks",
        "牛肉大葱水饺": "A plate of Chinese boiled dumplings with beef and scallion filling, steaming hot, plump dumplings with scallion bits, a small dipping sauce dish, wooden chopsticks",
        "台湾烤肠": "A grilled Taiwanese sausage on a stick, golden brown with grill marks",
        "鲜肉云吞面": "A bowl of Chinese wonton noodle soup with fresh pork wontons, wontons and noodles in golden broth, green scallions on top",
        "醪糟汤圆": "A bowl of sweet fermented rice wine balls, white glutinous rice balls in milky sweet soup",
        "玫瑰汤圆": "A bowl of rose flavored glutinous rice balls, pink-tinged white rice balls in light pink sweet soup, rose petals",
        "桂花汤圆": "A bowl of osmanthus flower flavored glutinous rice balls, white rice balls in clear sweet soup with golden osmanthus flowers",
        "方便面+蛋+青菜": "A bowl of instant noodles with a fried egg and green bok choy, curly noodles in a bowl",
    }

    if name in descriptions:
        return descriptions[name]

    # Generic translation by keywords
    return generic_translate(name, window)

def generic_translate(name, window):
    """Generic dish translation based on keywords."""
    parts = []

    # Detect dish type
    if "水饺" in name or "饺子" in name:
        parts.append("A plate of Chinese boiled dumplings")
        filling = name.replace("水饺", "").replace("饺子", "")
        if filling:
            parts.append(f"with {filling} filling")
        parts.append("steaming hot, plump dumpling wrappers, a small dipping sauce dish, wooden chopsticks")
    elif "馄饨" in name or "云吞" in name:
        parts.append("A bowl of Chinese wonton soup")
        if "面" in name:
            parts.append("with noodles")
        parts.append("plump wontons in savory broth, green scallions")
    elif "汤圆" in name:
        flavor = name.replace("汤圆", "")
        parts.append(f"A bowl of {flavor} flavored glutinous rice balls in sweet soup")
    elif "粥" in name:
        parts.append("A bowl of Chinese rice porridge/congee")
        if "小米" in name:
            parts.append("with millet")
        if "南瓜" in name:
            parts.append("and pumpkin")
        if "八宝" in name:
            parts.append("with eight treasure mixed ingredients")
        if "青菜" in name:
            parts.append("with green vegetables")
        if "瘦肉" in name:
            parts.append("and lean meat")
        parts.append("creamy warm porridge in a bowl")
    elif "胡辣汤" in name:
        parts.append("A bowl of spicy pepper soup, hot and spicy soup with tofu and vegetables")
    elif "花生牛奶" in name:
        parts.append("A glass of peanut milk drink, creamy peanut flavored milk")
    elif "烧麦" in name or "烧卖" in name:
        parts.append("A steamer basket of Chinese shumai dumplings, open-topped dumplings with pork filling, steaming hot")
    elif "小笼包" in name:
        if "素" in name:
            parts.append("A steamer basket of vegetable steamed buns, small steamed buns with vegetable filling")
        else:
            parts.append("A steamer basket of meat steamed buns, small steamed buns with juicy meat filling")
    elif "蒸饺" in name:
        parts.append("A steamer basket of Chinese steamed dumplings, plump dumplings with meat filling, steaming hot")
    elif "水煎包" in name:
        parts.append("A plate of pan-fried pork buns, golden crispy bottom, fluffy top, sesame seeds")
    elif "掉渣饼" in name:
        parts.append("A Chinese flatbread with crispy crumbs on top, golden brown, sprinkled with sesame and spices")
    elif "五谷豆浆" in name or "豆浆" in name:
        parts.append("A glass of warm soy milk drink, creamy five-grain soy milk")
    elif "米粉" in name or "米线" in name:
        parts.append("A bowl of Chinese rice noodles")
        if "拌" in name and "汤" not in name:
            parts.append("dry mixed with sauce and toppings")
        else:
            parts.append("in savory broth with toppings")
        if "酸菜" in name:
            parts.append("with pickled vegetables")
        if "鱼" in name:
            parts.append("and fish slices")
        if "牛肉" in name:
            parts.append("and beef slices")
        if "排骨" in name:
            parts.append("and pork ribs")
        if "鸡" in name:
            parts.append("and chicken")
        if "肥肠" in name:
            parts.append("and pork intestine")
        if "酸豆角" in name:
            parts.append("and pickled green beans")
        if "番茄" in name:
            parts.append("and tomato")
        if "肉沫" in name or "肉末" in name:
            parts.append("and minced pork")
        if "笋尖" in name:
            parts.append("and bamboo shoots")
        if "三鲜" in name:
            parts.append("and three fresh ingredients")
        if "鱼豆腐" in name:
            parts.append("and fish tofu")
        if "金汤" in name:
            parts.append("in golden pumpkin broth")
        if "红烧" in name:
            parts.append("braised style")
        if "酸辣" in name:
            parts.append("spicy and sour flavor")
        if "香菇" in name:
            parts.append("with shiitake mushrooms")
    elif "煲" in name:
        parts.append("A clay pot of Chinese stew")
        if "鸡肉" in name or "鸡" in name:
            parts.append("with chicken")
        if "酥肉" in name:
            parts.append("with crispy pork")
        if "排骨" in name:
            parts.append("with pork ribs")
        if "西红柿" in name or "番茄" in name:
            parts.append("with tomato")
        if "牛腩" in name:
            parts.append("with beef brisket")
        if "鱼肉" in name or "鱼" in name:
            parts.append("with fish")
        if "金针菇" in name:
            parts.append("with enoki mushrooms")
        if "肉卷" in name:
            parts.append("and meat rolls")
        if "三鲜" in name:
            parts.append("with three fresh ingredients")
        parts.append("bubbling hot stew in a clay pot")
    elif "肠粉" in name:
        parts.append("A plate of Chinese steamed rice rolls, thin translucent rice noodle rolls with filling, soy sauce drizzle")
    elif "肉夹馍" in name:
        parts.append("A Chinese meat sandwich in a bun, crispy flatbread filled with chopped meat")
        if "肥瘦" in name:
            parts.append("(fat and lean pork)")
        if "纯瘦" in name:
            parts.append("(lean pork only)")
    elif "麻辣拌" in name:
        parts.append("A plate of spicy mixed vegetables and noodles, tossed in chili oil and sesame sauce")
    elif "涮菜" in name:
        parts.append("A bowl of Chinese hot pot style boiled vegetables in spicy broth, various vegetables and tofu")
    elif "牛筋面" in name:
        parts.append("A bowl of chewy beef tendon noodles, thick noodles in spicy sauce with beef")
    elif name.endswith("面") or "拉面" in name or "拌面" in name or "炒面" in name or "热干面" in name or "泡馍" in name or "烩面" in name or "biang" in name:
        parts.append("A bowl of Chinese noodles")
        if "牛肉" in name and "拉面" in name:
            parts.append("with beef, hand-pulled noodles in clear broth")
        elif "拉面" in name:
            parts.append("hand-pulled noodles in broth")
        elif "炒面" in name:
            if "鸡蛋" in name:
                parts.append("stir-fried with egg")
            elif "肉片" in name:
                parts.append("stir-fried with sliced meat")
            elif "牛肉" in name:
                parts.append("stir-fried with beef")
            else:
                parts.append("stir-fried with vegetables")
        elif "拌面" in name or "干拌" in name:
            if "麻酱" in name:
                parts.append("with sesame sauce")
            elif "油泼" in name:
                parts.append("with hot oil chili sauce")
            elif "剁椒" in name:
                parts.append("with chopped chili sauce")
            elif "西红柿" in name or "番茄" in name:
                parts.append("with tomato meat sauce")
            elif "香辣" in name:
                parts.append("with spicy meat sauce")
            elif "三合一" in name:
                parts.append("with three mixed sauces")
            elif "热干" in name:
                if "牛肉" in name:
                    parts.append("with beef, hot dry noodles style with sesame sauce")
                elif "肉酱" in name:
                    parts.append("with meat sauce, hot dry noodles style")
                elif "红油" in name:
                    parts.append("with chili oil, hot dry noodles style")
                else:
                    parts.append("hot dry noodles with sesame sauce")
            else:
                parts.append("mixed with savory sauce")
        elif "泡馍" in name:
            parts.append("with beef, bread pieces soaked in broth")
        elif "烩面" in name:
            parts.append("braised noodles with beef in rich broth")
        elif "biang" in name.lower():
            parts.append("wide belt noodles with spicy sauce and vegetables")
        elif "酸菜" in name:
            parts.append("with pickled cabbage and beef")
        elif "红烧" in name:
            parts.append("with braised beef in rich brown broth")
        elif "大盘鸡" in name:
            parts.append("with big plate chicken, spicy chicken and noodles")
        elif "椒麻" in name:
            parts.append("with pepper sesame chicken")
        elif "西红柿" in name and "鸡蛋" in name:
            parts.append("with tomato and egg, in light tomato broth")
        elif "青菜" in name:
            parts.append("with green vegetables in clear broth")
        elif "肉酱" in name:
            parts.append("with meat sauce")
        else:
            parts.append("in savory broth")
    elif name.endswith("饭") or "饭" in name:
        parts.append("A plate of Chinese rice dish")
        if "叉烧" in name and "鸭腿" in name:
            parts.append("with BBQ char siu pork and duck leg")
        elif "叉烧" in name and "鸡" in name:
            parts.append("with BBQ char siu pork and chicken leg")
        elif "叉烧" in name:
            parts.append("with BBQ char siu pork slices")
        elif "白切鸡" in name:
            parts.append("with white cut poached chicken")
        elif "口水鸡" in name:
            parts.append("with spicy mouth-watering chicken in chili oil")
        elif "烧鸭" in name:
            parts.append("with crispy roast duck")
        elif "焖鸡" in name:
            if "酱香" in name:
                parts.append("with savory braised chicken")
            elif "麻辣" in name:
                parts.append("with spicy braised chicken")
        elif "猪脚" in name:
            parts.append("with braised pig trotters")
        elif "把子肉" in name:
            parts.append("with large braised pork belly slices")
        elif "五花肉" in name:
            parts.append("with crispy pork belly")
        elif "排骨" in name:
            parts.append("with pork ribs")
        elif "腊肠" in name:
            if "广味" in name:
                parts.append("with Cantonese style sausage slices")
            elif "川味" in name:
                parts.append("with Sichuan style sausage slices")
        elif "烤肉" in name:
            if "孜然" in name:
                parts.append("with cumin roast meat")
            else:
                parts.append("with roast meat")
        elif "双拼" in name:
            parts.append("with two types of meat combo")
        elif "鸡排" in name:
            if "黑椒" in name:
                parts.append("with black pepper chicken cutlet")
            elif "麻辣" in name:
                parts.append("with spicy chicken cutlet")
            elif "脆皮" in name:
                parts.append("with crispy fried chicken cutlet")
        elif "奥尔良" in name:
            parts.append("with Orleans style roast chicken")
        elif "翅根" in name:
            parts.append("with crispy chicken wing roots")
        elif "炸鸡" in name:
            if "蒜香" in name:
                parts.append("with garlic flavor fried chicken")
            else:
                parts.append("with fried chicken pieces")
        elif "鸡块" in name:
            parts.append("with spicy chicken nuggets")
        elif "烤鸡" in name:
            parts.append("with half roast chicken")
        parts.append("served with white rice")
    elif "石锅" in name:
        parts.append("A sizzling stone pot dish")
        if "拌饭" in name:
            parts.append("with rice, vegetables, meat and egg, sizzling in a hot stone bowl")
        elif "饭" in name:
            parts.append("with rice and toppings, sizzling hot")
        elif "豆腐" in name:
            parts.append("with tofu, sizzling hot")
        elif "烤鱼" in name or "鱼" in name:
            parts.append("with fish, sizzling hot")
        elif "鸡" in name:
            parts.append("with chicken, sizzling hot")
        elif "牛肉" in name:
            parts.append("with beef, sizzling hot")
        elif "排骨" in name:
            parts.append("with pork ribs, sizzling hot")
        else:
            parts.append("with meat and vegetables, sizzling hot in a stone bowl")
    elif "卷饼" in name or "手抓饼" in name:
        parts.append("A Chinese rolled flatbread wrap with fillings, crispy golden wrap with meat and vegetables")
    elif "煎饼" in name:
        parts.append("A Chinese jianbing crepe, golden crispy crepe with egg, sauce and fillings")
    elif "面包" in name:
        if "菠萝" in name:
            parts.append("A sweet pineapple bread bun, golden yellow with crackled crust")
        else:
            parts.append("Fresh bread buns, golden brown")
    elif name.endswith("炒饭"):
        parts.append("A plate of Chinese fried rice")
        if "蛋" in name or "鸡蛋" in name:
            parts.append("with egg")
        if "扬州" in name:
            parts.append("Yangzhou style with mixed ingredients")
        if "牛肉" in name:
            parts.append("with beef")
        if "排骨" in name:
            parts.append("with pork ribs")
    elif "铁板" in name:
        parts.append("A sizzling iron plate dish")
        if "饭" in name:
            parts.append("with rice, meat and vegetables on a hot iron plate")
        elif "牛肉" in name:
            parts.append("with beef sizzling on iron plate")
        elif "鸡" in name:
            parts.append("with chicken sizzling on iron plate")
        else:
            parts.append("with meat and vegetables sizzling on iron plate")
    elif "盖浇饭" in name or name.endswith("饭"):
        parts.append("A plate of Chinese rice with toppings")
        parts.append("white rice topped with savory meat and vegetables")
    elif "糖水" in name or name.endswith("水") and "饮" not in name:
        parts.append("A bowl of Chinese sweet dessert soup, warm sweet soup with various ingredients")
    elif "麻辣烫" in name:
        parts.append("A bowl of spicy malatang hotpot, various vegetables and meat in spicy red broth")
    elif "蘸水" in name:
        parts.append("A plate of Chinese boiled meat with dipping sauce, tender meat slices with spicy dipping broth")
    elif "盖饭" in name:
        parts.append("A plate of Chinese rice covered with meat and vegetables")
    elif "鸡" in name and "饭" not in name:
        parts.append("A plate of Chinese chicken dish, tender chicken with seasonings")
    elif "鸭" in name:
        parts.append("A plate of Chinese duck dish, sliced duck with sauce")
    elif "鱼" in name:
        parts.append("A plate of Chinese fish dish, cooked fish with sauce and vegetables")
    elif "豆腐" in name:
        parts.append("A plate of Chinese tofu dish, soft tofu with savory sauce")
    elif "汤" in name:
        parts.append("A bowl of Chinese soup, hot savory soup with ingredients")
    elif "奶茶" in name:
        parts.append("A glass of milk tea drink, creamy tea with milk")
    elif "果汁" in name or "饮" in name:
        parts.append("A glass of fresh fruit juice drink")
    else:
        # Fallback
        parts.append(f"A Chinese dish of {name}, served on a plate")

    return ", ".join(parts)

# Generate prompts
results = []
for d in valid_dishes:
    prompt = build_prompt(d['name'], d['window'])
    results.append({
        'idx': d['idx'],
        'name': d['name'],
        'window': d['window'],
        'area': d['area'],
        'price': d['price'],
        'prompt': prompt,
        'original_indices': d['original_indices']
    })

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Generated prompts for {len(results)} dishes")

# Show first 20
for r in results[:20]:
    print(f"{r['idx']:03d}. {r['name']}: {r['prompt'][:80]}...")
