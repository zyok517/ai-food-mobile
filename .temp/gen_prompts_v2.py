import json
import re

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_unique.json', 'r', encoding='utf-8') as f:
    dishes = json.load(f)

# Filter out invalid entries
valid_dishes = []
for d in dishes:
    name = d['name']
    if name in ('菜名', '窗口', '价格', None, ''):
        continue
    if d['window'] in ('窗口', None, ''):
        continue
    if d['price'] in ('价格', None, ''):
        continue
    valid_dishes.append(d)

print(f"Valid dishes: {len(valid_dishes)}")

STYLE = "cartoon style illustration, flat design, cute kawaii food illustration, warm cream background, soft warm colors, appetizing, simple and clean, no text"

def translate(name, window):
    n = name

    # ---- Specific exact matches ----
    exact = {
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
    if name in exact:
        return exact[name]

    # ---- Pattern-based matching ----

    # 水饺/饺子
    if "水饺" in name or "饺子" in name:
        filling = name.replace("水饺", "").replace("饺子", "")
        return f"A plate of Chinese boiled dumplings with {filling} filling, steaming hot, plump dumpling wrappers, a small dipping sauce dish, wooden chopsticks"

    # 馄饨/云吞
    if "馄饨" in name or "云吞" in name:
        desc = "A bowl of Chinese wonton soup with plump wontons in savory broth, green scallions"
        if "面" in name: desc += ", noodles"
        if "鲜虾" in name or "虾仁" in name: desc = "A bowl of Chinese wonton soup with shrimp wontons, plump wontons in savory broth"
        return desc

    # 汤圆
    if "汤圆" in name:
        flavor = name.replace("汤圆", "")
        return f"A bowl of {flavor} flavored glutinous rice balls in sweet soup"

    # 粥
    if "粥" in name:
        desc = "A bowl of Chinese rice porridge/congee"
        if "小米" in name: desc += " with millet"
        if "南瓜" in name: desc += " and pumpkin"
        if "八宝" in name: desc += " with eight treasure mixed ingredients"
        if "青菜" in name: desc += " with green vegetables"
        if "瘦肉" in name: desc += " and lean meat"
        if "皮蛋" in name: desc += " with century egg"
        if "鱼片" in name: desc += " with fish slices"
        return desc + ", creamy warm porridge in a bowl"

    # 胡辣汤
    if "胡辣汤" in name:
        return "A bowl of spicy pepper soup, hot and spicy soup with tofu, vegetables and beef slices"

    # 花生牛奶
    if "花生牛奶" in name:
        return "A glass of peanut milk drink, creamy peanut flavored milk"

    # 烧麦/烧卖
    if "烧麦" in name or "烧卖" in name:
        return "A steamer basket of Chinese shumai dumplings, open-topped dumplings with pork filling, steaming hot"

    # 小笼包
    if "小笼包" in name:
        if "素" in name:
            return "A steamer basket of vegetable steamed buns, small steamed buns with vegetable filling"
        return "A steamer basket of meat steamed buns, small steamed buns with juicy meat filling"

    # 蒸饺
    if "蒸饺" in name:
        return "A steamer basket of Chinese steamed dumplings, plump dumplings with meat filling, steaming hot"

    # 水煎包
    if "水煎包" in name:
        return "A plate of pan-fried pork buns, golden crispy bottom, fluffy top, sesame seeds"

    # 掉渣饼
    if "掉渣饼" in name:
        return "A Chinese flatbread with crispy crumbs on top, golden brown, sprinkled with sesame and spices"

    # 豆浆
    if "豆浆" in name:
        if "五谷" in name:
            return "A glass of warm five-grain soy milk drink, creamy soy milk"
        return "A glass of warm soy milk drink, creamy soy milk"

    # 米粉/米线
    if "米粉" in name or "米线" in name:
        desc = "A bowl of Chinese rice noodles"
        if "拌" in name and "汤" not in name:
            desc += " dry mixed with sauce"
        else:
            desc += " in savory broth"
        if "原味" in name: desc += " original flavor"
        if "原汤" in name: desc += " in original broth"
        if "酸辣" in name: desc += " spicy and sour"
        if "酸菜" in name: desc += " with pickled cabbage"
        if "鱼片" in name or "鱼" in name: desc += " and fish slices"
        if "牛肉" in name: desc += " and beef slices"
        if "排骨" in name: desc += " and pork ribs"
        if "鸡块" in name or "鸡" in name: desc += " and chicken"
        if "鸡杂" in name: desc += " and chicken giblets"
        if "肥肠" in name: desc += " and pork intestine"
        if "酸豆角" in name: desc += " and pickled green beans"
        if "番茄" in name: desc += " and tomato"
        if "肉沫" in name or "肉末" in name: desc += " and minced pork"
        if "笋尖" in name: desc += " and bamboo shoots"
        if "三鲜" in name: desc += " and three fresh ingredients"
        if "鱼豆腐" in name: desc += " and fish tofu"
        if "金汤" in name: desc += " in golden pumpkin broth"
        if "红烧" in name: desc += " braised style"
        if "香菇" in name: desc += " with shiitake mushrooms"
        if "招牌" in name: desc += " signature style"
        return desc + ", topped with fresh herbs"

    # 粉 (standalone - like 素粉, 麻辣拌粉, 牛杂拌粉)
    if name.endswith("粉") and "米粉" not in name and "河粉" not in name:
        if "拌" in name:
            desc = "A plate of mixed rice noodles with sauce"
            if "麻辣" in name: desc += " spicy malatang style"
            if "牛杂" in name: desc += " with beef offal"
            if "素" in name: desc += " with vegetables only"
            return desc + ", tossed with chili oil"
        if "素" in name:
            return "A bowl of plain rice noodles with vegetables in light broth"
        return "A bowl of rice noodles with toppings in savory broth"

    # 煲
    if "煲" in name and "煲饭" not in name:
        desc = "A clay pot of Chinese stew"
        if "鸡肉" in name or "鸡" in name: desc += " with chicken"
        if "酥肉" in name: desc += " with crispy pork"
        if "排骨" in name: desc += " with pork ribs"
        if "西红柿" in name or "番茄" in name: desc += " with tomato"
        if "牛腩" in name: desc += " with beef brisket"
        if "鱼肉" in name or "鱼" in name: desc += " with fish"
        if "金针菇" in name: desc += " with enoki mushrooms"
        if "肉卷" in name: desc += " and meat rolls"
        if "三鲜" in name: desc += " with three fresh ingredients"
        return desc + ", bubbling hot stew in a clay pot"

    # 煲饭
    if "煲饭" in name:
        desc = "A clay pot rice dish"
        if "黑椒" in name: desc += " with black pepper meat"
        if "卤肉" in name: desc += " with braised pork"
        if "腊味" in name: desc += " with cured meat"
        if "排骨" in name: desc += " with pork ribs"
        if "滑鸡" in name: desc += " with silky chicken"
        return desc + ", crispy rice crust at bottom, sizzling hot"

    # 肠粉
    if "肠粉" in name:
        if "肉沫" in name or "肉末" in name:
            return "A plate of Chinese steamed rice rolls with minced pork, thin translucent rice noodle rolls, soy sauce drizzle"
        if "鸡蛋" in name:
            return "A plate of Chinese steamed rice rolls with egg, thin translucent rice noodle rolls, soy sauce drizzle"
        return "A plate of Chinese steamed rice rolls, thin translucent rice noodle rolls with filling, soy sauce drizzle"

    # 肉夹馍
    if "肉夹馍" in name:
        if "肥瘦" in name:
            return "A Chinese meat sandwich, crispy flatbread filled with chopped fat and lean pork"
        if "纯瘦" in name:
            return "A Chinese meat sandwich, crispy flatbread filled with chopped lean pork"
        return "A Chinese meat sandwich, crispy flatbread filled with chopped meat"

    # 麻辣拌
    if "麻辣拌" in name:
        return "A plate of spicy mixed vegetables and noodles, tossed in chili oil and sesame sauce"

    # 涮菜/涮肉
    if "涮菜" in name:
        return "A bowl of Chinese hot pot style boiled vegetables in spicy broth, various vegetables and tofu"
    if "涮肉" in name:
        return "A bowl of Chinese hot pot style boiled meat in spicy broth, tender meat slices"

    # 牛筋面
    if "牛筋面" in name:
        return "A bowl of chewy beef tendon noodles, thick noodles in spicy sauce with beef"

    # 面类
    if any(k in name for k in ["拉面", "拌面", "炒面", "热干面", "泡馍", "烩面", "biang"]) or name.endswith("面"):
        if "拉面" in name:
            if "牛肉" in name: return "A bowl of hand-pulled beef noodles in clear broth, tender beef slices"
            if "青菜" in name: return "A bowl of hand-pulled noodles with green vegetables in clear broth"
            if "肉酱" in name: return "A bowl of hand-pulled noodles with meat sauce in broth"
            return "A bowl of Chinese hand-pulled noodles in savory broth"
        if "炒面" in name:
            if "鸡蛋" in name: return "A plate of stir-fried noodles with egg, golden noodles with scrambled egg"
            if "肉片" in name: return "A plate of stir-fried noodles with sliced meat, savory noodles"
            if "牛肉" in name: return "A plate of stir-fried noodles with beef, savory noodles"
            if "火腿" in name: return "A plate of stir-fried noodles with ham, savory noodles"
            if "素" in name: return "A plate of stir-fried noodles with vegetables"
            return "A plate of Chinese stir-fried noodles with vegetables and sauce"
        if "拌面" in name or "干拌" in name:
            if "麻酱" in name and "鸡丝" in name: return "A bowl of noodles with sesame sauce and shredded chicken, mixed dry"
            if "麻酱" in name: return "A bowl of noodles with sesame sauce, mixed dry"
            if "油泼" in name: return "A bowl of noodles with hot chili oil, Shaanxi style"
            if "剁椒" in name and "肉酱" in name: return "A bowl of noodles with chopped chili and meat sauce, spicy"
            if "香辣" in name and "肉酱" in name: return "A bowl of spicy noodles with meat sauce, chili red"
            if "西红柿" in name and "肉酱" in name: return "A bowl of noodles with tomato and meat sauce, red orange"
            if "特色" in name: return "A bowl of signature dry mixed noodles with special sauce"
            if "三合一" in name: return "A bowl of noodles with three mixed sauces, layered flavors"
            if "热干" in name:
                if "牛肉" in name: return "A bowl of hot dry noodles with beef and sesame sauce, Wuhan style"
                if "肉酱" in name: return "A bowl of hot dry noodles with meat sauce and sesame paste"
                if "红油" in name: return "A bowl of hot dry noodles with chili oil, red and spicy"
                return "A bowl of hot dry noodles with sesame sauce, Wuhan style"
            if "椒麻" in name and "鸡" in name: return "A bowl of noodles with pepper sesame chicken, numbing spicy"
            return "A bowl of Chinese dry mixed noodles with savory sauce"
        if "泡馍" in name:
            return "A bowl of Chinese beef bread soup, torn bread pieces soaked in beef broth"
        if "烩面" in name:
            return "A bowl of braised noodles with beef in rich broth, thick flat noodles"
        if "biang" in name.lower():
            return "A bowl of wide belt noodles with spicy sauce and vegetables, Shaanxi style"
        if "酸菜" in name and "牛肉" in name:
            return "A bowl of noodles with pickled cabbage and beef, sour and spicy"
        if "红烧" in name and "牛肉" in name:
            return "A bowl of braised beef noodles in rich brown broth, tender beef chunks"
        if "大盘鸡" in name:
            return "A plate of big plate chicken with noodles, spicy chicken over wide noodles"
        if "西红柿" in name and "鸡蛋" in name:
            return "A bowl of noodles with tomato and egg, red yellow broth"
        if "牛肉" in name and "面" in name:
            return "A bowl of Chinese beef noodles in savory broth, tender beef slices"
        return "A bowl of Chinese noodles in savory broth"

    # 石锅
    if "石锅" in name:
        if "拌饭" in name: return "A sizzling stone pot bibimbap with rice, vegetables, meat and egg, sizzling in a hot stone bowl"
        if "豆腐" in name: return "A sizzling stone pot tofu dish, bubbling hot tofu in stone bowl"
        if "鱼" in name: return "A sizzling stone pot fish, grilled fish in stone bowl with sauce"
        if "鸡" in name: return "A sizzling stone pot chicken, tender chicken in stone bowl"
        if "牛肉" in name: return "A sizzling stone pot beef, tender beef in stone bowl"
        if "排骨" in name: return "A sizzling stone pot pork ribs, tender ribs in stone bowl"
        if "烤肉" in name: return "A sizzling stone pot roast meat, sizzling in stone bowl"
        if "鸭血" in name: return "A sizzling stone pot with duck blood and vermicelli, sizzling in stone bowl"
        if "粉丝" in name: return "A sizzling stone pot with vermicelli and meat, sizzling in stone bowl"
        if "小酥肉" in name: return "A sizzling stone pot with crispy pork, sizzling in stone bowl"
        if "黑椒" in name: return "A sizzling stone pot with black pepper meat, sizzling in stone bowl"
        if "孜然" in name: return "A sizzling stone pot with cumin meat, sizzling in stone bowl"
        if "丸子" in name: return "A sizzling stone pot with meatballs, sizzling in stone bowl"
        if "红烧肉" in name: return "A sizzling stone pot with braised pork, sizzling in stone bowl"
        if "火鸡面" in name: return "A sizzling stone pot with spicy chicken and noodles, sizzling in stone bowl"
        if "烤鱼" in name: return "A sizzling stone pot grilled fish, sizzling in stone bowl"
        return "A sizzling stone pot dish with meat and vegetables, bubbling hot"

    # 铁板
    if "铁板" in name:
        if "饭" in name: return "A sizzling iron plate rice dish, rice with meat and vegetables on hot iron plate"
        if "牛肉" in name: return "A sizzling iron plate beef, tender beef on hot iron plate"
        if "鸡" in name: return "A sizzling iron plate chicken, tender chicken on hot iron plate"
        if "鱿鱼" in name: return "A sizzling iron plate squid, fresh squid on hot iron plate"
        if "豆腐" in name: return "A sizzling iron plate tofu, sizzling tofu on hot iron plate"
        return "A sizzling iron plate dish with meat and vegetables"

    # 卷饼/手抓饼
    if "卷饼" in name:
        if "鸡肉" in name: return "A Chinese chicken wrap, golden crispy wrap with chicken and vegetables"
        if "牛肉" in name: return "A Chinese beef wrap, golden crispy wrap with beef and vegetables"
        if "烤鸭" in name: return "A Chinese roast duck wrap, golden crispy wrap with duck slices"
        if "里脊" in name: return "A Chinese pork tenderloin wrap, golden crispy wrap with pork"
        return "A Chinese rolled flatbread wrap with fillings, crispy golden wrap"
    if "手抓饼" in name or "抓饼" in name:
        if "鸡蛋" in name: return "A crispy hand-grabbed pancake with egg, flaky golden layers"
        return "A crispy hand-grabbed pancake, flaky golden layers"

    # 煎饼
    if "煎饼" in name:
        if "果子" in name: return "A Chinese jianbing guozi, golden crispy crepe with egg and crispy crackers"
        return "A Chinese jianbing crepe, golden crispy crepe with egg, sauce and fillings"

    # 面包
    if "面包" in name:
        if "菠萝" in name: return "A sweet pineapple bread bun, golden yellow with crackled crust"
        if "红豆" in name: return "A sweet red bean bread bun, soft bread with red bean filling"
        if "肉松" in name: return "A soft bread bun with meat floss, fluffy bread topped with pork floss"
        return "Fresh bread buns, golden brown, soft and fluffy"

    # 炒饭
    if name.endswith("炒饭"):
        if "火腿" in name and "鸡蛋" in name: return "A plate of fried rice with ham and egg, golden fried rice grains"
        if "火腿" in name: return "A plate of fried rice with ham, golden fried rice grains"
        if "鸡蛋" in name: return "A plate of egg fried rice, golden yellow rice grains with scrambled egg"
        if "扬州" in name: return "A plate of Yangzhou fried rice, mixed ingredients, colorful"
        if "牛肉" in name: return "A plate of beef fried rice, savory brown fried rice with beef"
        if "排骨" in name: return "A plate of pork rib fried rice, fried rice with tender ribs"
        if "鸡肉" in name: return "A plate of chicken fried rice, fried rice with chicken pieces"
        if "老干妈" in name and "火腿" in name: return "A plate of spicy fried rice with ham and Lao Gan Ma chili sauce, red tinged"
        if "老干妈" in name and "鸡肉" in name: return "A plate of spicy fried rice with chicken and Lao Gan Ma chili sauce, red tinged"
        if "老干妈" in name and "五花肉" in name: return "A plate of spicy fried rice with pork belly and Lao Gan Ma chili sauce"
        if "老干妈" in name and "腊肠" in name: return "A plate of spicy fried rice with sausage and Lao Gan Ma chili sauce"
        if "菌菇" in name and "火腿" in name: return "A plate of mushroom and ham fried rice, earthy mushrooms and ham"
        if "菌菇" in name and "鸡肉" in name: return "A plate of mushroom and chicken fried rice, earthy mushrooms and chicken"
        if "菌菇" in name and "腊肠" in name: return "A plate of mushroom and sausage fried rice, earthy mushrooms and sausage"
        if "菌菇" in name and "五花肉" in name: return "A plate of mushroom and pork belly fried rice"
        if "菌菇" in name and "全家福" in name: return "A plate of mushroom mixed feast fried rice, colorful with many ingredients"
        if "菌菇" in name: return "A plate of mushroom fried rice, earthy mushroom flavor"
        if "广式" in name and "腊肠" in name: return "A plate of Cantonese sausage fried rice, sweet sausage slices"
        if "奥尔良" in name: return "A plate of Orleans style chicken fried rice, golden chicken pieces"
        if "咖喱" in name: return "A plate of curry fried rice, golden yellow with curry flavor"
        if "腊肉" in name: return "A plate of cured meat fried rice, smoky cured pork"
        if "虾" in name: return "A plate of shrimp fried rice, pink shrimp pieces"
        if "榨菜" in name: return "A plate of pickled mustard fried rice, savory and crunchy"
        if "番茄" in name: return "A plate of tomato fried rice, red tomato flavored rice"
        if " bacon" in name.lower(): return "A plate of bacon fried rice, smoky bacon bits"
        return "A plate of Chinese fried rice with mixed ingredients, golden rice grains"

    # 盖饭/盖浇饭
    if "盖饭" in name or "盖浇饭" in name:
        desc = "A plate of Chinese rice topped with"
        if "剁椒" in name and "鸡蛋" in name: return "A plate of rice topped with chopped chili and egg, spicy red topping"
        if "地三鲜" in name: return "A plate of rice topped with stir-fried eggplant potato and pepper, glossy sauce"
        if "外婆菜" in name and "鸡蛋" in name: return "A plate of rice topped with grandmother's preserved vegetables and egg"
        if "番茄" in name and "牛肉" in name: return "A plate of rice topped with tomato beef, red rich sauce"
        if "咖喱" in name: return "A plate of rice topped with curry sauce, golden yellow curry"
        if "宫保鸡丁" in name: return "A plate of rice topped with Kung Pao chicken, peanuts and dried chili"
        if "鱼香肉丝" in name: return "A plate of rice topped with Yu Xiang shredded pork, sweet and sour sauce"
        if "麻婆豆腐" in name: return "A plate of rice topped with Mapo tofu, spicy red tofu"
        if "回锅肉" in name: return "A plate of rice topped with twice-cooked pork, spicy slices"
        if "青椒" in name and "肉丝" in name: return "A plate of rice topped with green pepper shredded pork"
        if "土豆" in name and "牛肉" in name: return "A plate of rice topped with potato and beef stew"
        if "茄子" in name: return "A plate of rice topped with braised eggplant, glossy purple"
        if "酸菜鱼" in name: return "A plate of rice topped with sour fish, white fish in sour broth"
        if "红烧肉" in name: return "A plate of rice topped with braised pork belly, rich brown sauce"
        if "黄焖鸡" in name: return "A plate of rice topped with braised chicken, golden brown sauce"
        if "辣子鸡" in name: return "A plate of rice topped with spicy chicken, lots of dried chilies"
        if "香菇" in name and "鸡" in name: return "A plate of rice topped with mushroom chicken, earthy and savory"
        if "滑蛋" in name and "虾仁" in name: return "A plate of rice topped with silky scrambled egg and shrimp"
        if "滑蛋" in name and "牛肉" in name: return "A plate of rice topped with silky scrambled egg and beef"
        if "滑蛋" in name and "鸡" in name: return "A plate of rice topped with silky scrambled egg and chicken"
        if "卤肉" in name: return "A plate of rice topped with braised pork, rich dark sauce"
        if "辣椒炒肉" in name: return "A plate of rice topped with stir-fried chili pork, spicy green"
        if "小炒" in name: return "A plate of rice topped with stir-fried meat and vegetables"
        if "农家小炒肉" in name: return "A plate of rice topped with farmhouse stir-fried pork, spicy"
        if "西红柿" in name and "鸡蛋" in name: return "A plate of rice topped with tomato egg, classic red yellow"
        if "肉末" in name or "肉沫" in name: return "A plate of rice topped with minced pork sauce, savory"
        return desc + " savory meat and vegetables, rich sauce over white rice"

    # 烤鱼饭
    if "烤鱼" in name and "饭" in name:
        if "豆花" in name: return "A plate of rice with grilled fish and tofu pudding, spicy Sichuan style"
        if "泡面" in name: return "A plate of rice with grilled fish and instant noodles, spicy"
        if "血旺" in name: return "A plate of rice with grilled fish and blood tofu, spicy red"
        if "年糕" in name: return "A plate of rice with grilled fish and rice cakes, spicy"
        if "土豆粉" in name: return "A plate of rice with grilled fish and potato noodles, spicy"
        if "香煎蛋" in name: return "A plate of rice with grilled fish and fried egg, spicy"
        if "小酥肉" in name: return "A plate of rice with grilled fish and crispy pork, spicy"
        if "嫩鸡柳" in name: return "A plate of rice with grilled fish and chicken tenders, spicy"
        if "全家福丸" in name: return "A plate of rice with grilled fish and assorted meatballs, spicy"
        return "A plate of rice with grilled fish, spicy red sauce"

    # 卤肉XXX饭
    if "卤肉" in name and "饭" in name:
        if "炸茄子" in name: return "A plate of rice with braised pork and fried eggplant, savory"
        if "豆腐" in name: return "A plate of rice with braised pork and tofu, rich dark sauce"
        if "肉肠" in name: return "A plate of rice with braised pork and meat sausage, savory"
        if "肉卷" in name: return "A plate of rice with braised pork and meat rolls"
        if "腊肠" in name: return "A plate of rice with braised pork and cured sausage"
        if "黑椒" in name: return "A plate of rice with braised pork and black pepper meat, clay pot style"
        if "炸鸡" in name: return "A plate of rice with braised pork and fried chicken, dual protein"
        if "鸡腿" in name: return "A plate of rice with braised pork and chicken leg"
        if "鸭腿" in name: return "A plate of rice with braised pork and duck leg"
        if "牛肉" in name: return "A plate of rice with braised pork and beef slices"
        if "雪花鸡排" in name: return "A plate of rice with braised pork and crispy chicken cutlet"
        return "A plate of rice with braised pork, rich dark sauce, Taiwanese style"

    # 甜辣黑鸭饭
    if "黑鸭" in name and "饭" in name:
        return "A plate of rice with spicy black duck, dark spicy sauce, sweet and hot"

    # 钵钵鸡
    if "钵钵鸡" in name:
        return "A bowl of cold Sichuan chicken in spicy oil, skewered chicken pieces in red chili oil"

    # 猪肚鸡
    if "猪肚鸡" in name:
        return "A pot of pork stomach and chicken soup, milky white broth, nourishing"

    # 各种XX饭 (剩余)
    if name.endswith("饭"):
        if "叉烧" in name and "鸭腿" in name: return "A plate of rice with BBQ char siu pork and duck leg, red roasted meat"
        if "叉烧" in name and "鸡" in name: return "A plate of rice with BBQ char siu pork and chicken leg"
        if "叉烧" in name: return "A plate of rice with BBQ char siu pork slices, red glazed edges"
        if "剁椒" in name and "柠檬" in name and "鸡腿" in name: return "A plate of rice with chopped chili lemon chicken leg, spicy tangy"
        if "白切鸡" in name: return "A plate of rice with white cut poached chicken, tender chicken with ginger sauce"
        if "口水鸡" in name: return "A plate of rice with mouth-watering chicken in chili oil, spicy red"
        if "烧鸭" in name: return "A plate of rice with crispy roast duck, golden brown skin"
        if "焖鸡" in name and "酱香" in name: return "A plate of rice with savory braised chicken, rich brown sauce"
        if "焖鸡" in name and "麻辣" in name: return "A plate of rice with spicy braised chicken, red chili sauce"
        if "猪脚" in name: return "A plate of rice with braised pig trotters, glossy dark skin"
        if "把子肉" in name: return "A plate of rice with large braised pork belly slices, rich soy sauce"
        if "五花肉" in name and "脆皮" in name: return "A plate of rice with crispy pork belly, golden crackling skin"
        if "排骨" in name and "经典" in name: return "A plate of rice with classic pork ribs, tender braised ribs"
        if "腊肠" in name and "广味" in name: return "A plate of rice with Cantonese sweet sausage slices"
        if "腊肠" in name and "川味" in name: return "A plate of rice with Sichuan spicy sausage slices"
        if "烤肉" in name and "孜然" in name: return "A plate of rice with cumin roast meat, fragrant spice"
        if "烤肉" in name: return "A plate of rice with roast meat, savory slices"
        if "双拼" in name: return "A plate of rice with two types of meat combo, half and half"
        if "鸡排" in name and "黑椒" in name: return "A plate of rice with black pepper chicken cutlet, crispy outside"
        if "鸡排" in name and "麻辣" in name: return "A plate of rice with spicy chicken cutlet, red spicy crust"
        if "鸡排" in name and "脆皮" in name: return "A plate of rice with crispy fried chicken cutlet, golden brown"
        if "鸡排" in name and "原味" in name and "大" in name: return "A plate of rice with large original flavor chicken cutlet, golden crispy"
        if "鸡排" in name and "招牌" in name and "手枪" in name: return "A plate of rice with signature pistol-shaped chicken leg, crispy golden"
        if "鸡排" in name: return "A plate of rice with chicken cutlet, crispy outside, tender inside"
        if "奥尔良" in name and "鸡肉" in name: return "A plate of rice with Orleans style roast chicken, golden seasoned"
        if "翅根" in name: return "A plate of rice with crispy chicken wing roots, golden brown"
        if "炸鸡" in name and "蒜香" in name: return "A plate of rice with garlic flavor fried chicken, fragrant garlic"
        if "炸鸡" in name: return "A plate of rice with fried chicken pieces, crispy golden"
        if "鸡块" in name and "麦辣" in name: return "A plate of rice with spicy chicken nuggets, McDonald's style"
        if "烤鸡" in name and "半只" in name: return "A plate of rice with half roast chicken, golden crispy skin"
        if "鸡腿" in name and "大" in name and "香酥" in name: return "A plate of rice with crispy large chicken leg, golden brown"
        if "滑蛋" in name and "虾仁" in name: return "A plate of rice with silky scrambled egg and shrimp, golden and pink"
        if "滑蛋" in name and "牛肉" in name: return "A plate of rice with silky scrambled egg and beef, golden and brown"
        if "滑蛋" in name and "鸡" in name: return "A plate of rice with silky scrambled egg and chicken, golden"
        if "滑蛋" in name: return "A plate of rice with silky scrambled egg, golden fluffy egg"
        if "咖喱" in name and "牛肉" in name: return "A plate of rice with curry beef, golden yellow curry sauce"
        if "咖喱" in name and "鸡" in name: return "A plate of rice with curry chicken, golden yellow curry sauce"
        if "咖喱" in name: return "A plate of rice with curry meat and vegetables, golden yellow curry"
        if "日式" in name and "肥牛" in name: return "A plate of rice with Japanese style beef, onion and savory sauce"
        if "肥牛" in name: return "A plate of rice with beef slices, savory onion sauce"
        if "黑椒" in name and "牛柳" in name: return "A plate of rice with black pepper beef tenderloin, peppery dark sauce"
        if "黑椒" in name and "鸡" in name: return "A plate of rice with black pepper chicken, peppery sauce"
        if "黑椒" in name: return "A plate of rice with black pepper meat, peppery sauce"
        if "蜜汁" in name and "烤肉" in name: return "A plate of rice with honey roast meat, sweet glaze"
        if "照烧" in name: return "A plate of rice with teriyaki meat, glossy sweet sauce"
        if "梅菜扣肉" in name: return "A plate of rice with preserved mustard and pork belly, dark savory"
        if "辣子鸡" in name: return "A plate of rice with spicy chicken and dried chilies, red and fiery"
        if "口水鸡" in name: return "A plate of rice with mouth-watering chicken in chili oil"
        if "藤椒" in name: return "A plate of rice with rattan pepper chicken, numbing green pepper"
        if "黄焖鸡" in name: return "A plate of rice with braised chicken, golden brown sauce"
        if "毛血旺" in name: return "A plate of rice with spicy blood curd and offal stew, red spicy broth"
        if "水煮" in name and "牛肉" in name: return "A plate of rice with boiled beef in chili oil, red spicy"
        if "水煮" in name and "鱼" in name: return "A plate of rice with boiled fish in chili oil, red spicy"
        if "水煮" in name and "肉片" in name: return "A plate of rice with boiled meat slices in chili oil, red spicy"
        if "酸菜鱼" in name: return "A plate of rice with sour fish in pickled cabbage broth, white fish green broth"
        if "烤鱼" in name: return "A plate of rice with grilled fish, spicy red sauce"
        if "牛柳" in name: return "A plate of rice with beef tenderloin, savory dark sauce"
        if "牛腩" in name: return "A plate of rice with beef brisket, tender chunks in brown sauce"
        if "牛肉" in name: return "A plate of rice with beef, savory brown sauce"
        if "鸡米花" in name: return "A plate of rice with popcorn chicken, crispy small chicken bites"
        if "鸡腿" in name: return "A plate of rice with chicken leg, golden braised"
        if "鸭腿" in name: return "A plate of rice with duck leg, savory braised"
        if "排骨" in name: return "A plate of rice with pork ribs, tender braised"
        if "肉片" in name: return "A plate of rice with sliced meat, savory sauce"
        if "回锅肉" in name: return "A plate of rice with twice-cooked pork, spicy with peppers"
        if "盐焗" in name: return "A plate of rice with salt-baked chicken, golden skin"
        if "手撕" in name: return "A plate of rice with hand-torn chicken, savory shredded meat"
        if "猪脚" in name: return "A plate of rice with braised pig trotters, glossy dark"
        if "肉饼" in name: return "A plate of rice with meat patty, golden brown"
        if "狮子头" in name: return "A plate of rice with giant meatball, tender juicy meatball in brown sauce"
        return "A plate of Chinese rice with meat and vegetables, savory sauce"

    # 麻辣烫
    if "麻辣烫" in name:
        return "A bowl of spicy malatang hotpot, various vegetables, meat and noodles in spicy red broth"

    # 蘸水
    if "蘸水" in name:
        if "鸭血" in name: return "A plate of boiled duck blood with spicy dipping broth"
        if "毛肚" in name: return "A plate of boiled beef tripe with spicy dipping broth"
        if "牛肉" in name: return "A plate of boiled beef slices with spicy dipping broth"
        if "虾" in name: return "A plate of boiled shrimp with spicy dipping broth"
        if "郡肝" in name: return "A plate of boiled chicken gizzard with spicy dipping broth"
        if "脑花" in name: return "A plate of boiled pork brain with spicy dipping broth"
        if "千层肚" in name: return "A plate of boiled beef omasum with spicy dipping broth"
        if "黄喉" in name: return "A plate of boiled beef aorta with spicy dipping broth"
        if "鹅肠" in name: return "A plate of boiled goose intestine with spicy dipping broth"
        return "A plate of Chinese boiled meat with spicy dipping broth"

    # 广式糖水
    if "糖水" in name:
        if "红豆" in name: return "A bowl of red bean sweet soup, warm sweet dessert"
        if "绿豆" in name: return "A bowl of mung bean sweet soup, warm sweet dessert"
        if "芋头" in name: return "A bowl of taro sweet soup, creamy taro chunks"
        if "番薯" in name or "红薯" in name: return "A bowl of sweet potato sweet soup, golden sweet"
        if "西米" in name: return "A bowl of sago sweet soup with coconut milk, creamy white"
        if "杨枝甘露" in name: return "A bowl of mango pomelo sago, yellow creamy mango dessert"
        if "双皮奶" in name: return "A bowl of double skin milk pudding, silky white pudding"
        if "龟苓膏" in name: return "A bowl of herbal jelly dessert, dark gelatin"
        return "A bowl of Chinese sweet dessert soup, warm and sweet"

    # 饮品
    if "奶茶" in name: return "A glass of milk tea, creamy tea with milk, ice cubes"
    if "果茶" in name: return "A glass of fruit tea, colorful fruit infused tea"
    if "柠檬" in name and ("水" in name or "茶" in name or "饮" in name): return "A glass of lemon water/tea, fresh lemon slices"
    if "酸梅汤" in name: return "A glass of sour plum soup, dark red cool drink"
    if "豆浆" in name: return "A glass of soy milk, creamy white"
    if "可乐" in name: return "A glass of cola with ice, dark fizzy drink"
    if "雪碧" in name: return "A glass of sprite with ice, clear fizzy drink"
    if "果汁" in name: return "A glass of fresh fruit juice, colorful"

    # 汤类
    if name.endswith("汤") or "汤" in name:
        if "牛杂" in name: return "A bowl of beef offal soup, rich beef broth with offal"
        if "素" in name: return "A bowl of vegetable soup, clear broth with vegetables"
        if "鸡蛋" in name and "汤" in name: return "A bowl of egg drop soup, silky egg ribbons in broth"
        if "紫菜" in name: return "A bowl of seaweed egg soup, green seaweed and egg"
        if "番茄" in name: return "A bowl of tomato egg soup, red tangy broth"
        if "冬瓜" in name: return "A bowl of winter melon soup, clear broth with melon"
        if "玉米" in name: return "A bowl of corn soup, golden sweet corn"
        if "排骨" in name: return "A bowl of pork rib soup, rich bone broth with ribs"
        return "A bowl of Chinese soup, hot savory soup with fresh ingredients"

    # 豆制品/小吃
    if "豆腐" in name:
        if "麻婆" in name: return "A plate of Mapo tofu, spicy red tofu with minced pork"
        if "臭豆腐" in name: return "A plate of stinky tofu, golden fried fermented tofu"
        if "铁板" in name: return "A sizzling iron plate tofu, sizzling on hot plate"
        return "A plate of Chinese tofu dish, soft tofu with savory sauce"

    if "鸡肉" in name or "鸡" in name:
        return "A plate of Chinese chicken dish, tender chicken with seasonings"

    if "鸭" in name:
        return "A plate of Chinese duck dish, sliced duck with sauce"

    if "鱼" in name or "烤鱼" in name:
        return "A plate of Chinese fish dish, cooked fish with sauce and vegetables"

    # Fallback
    return f"A plate of Chinese dish, {name}, served on a plate with sauce"

# Generate prompts
results = []
for d in valid_dishes:
    prompt = f"{translate(d['name'], d['window'])}, {STYLE}"
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

# Count generic fallbacks
generic_count = sum(1 for r in results if "A plate of Chinese dish," in r['prompt'])
print(f"Generic fallback prompts: {generic_count}")

# Show some samples
for r in results[14:35]:
    print(f"{r['idx']:03d}. {r['name']}: {r['prompt'][:100]}...")
