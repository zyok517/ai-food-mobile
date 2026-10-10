import json

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Specific prompts for the 84 generic fallback dishes
patches = {
    235: "A plate of rice with two types of meat combo, half and half, char siu and pork chop",
    240: "A bowl of spicy dry pot stir-fry, various vegetables and meat in spicy sauce, no broth",
    241: "A healthy customized meal plate, balanced portions of vegetables, protein and grains",
    258: "A plate of stir-fried spicy boiled egg slices, golden egg pieces with chili peppers, Hunan style",
    259: "A plate of stir-fried tofu skin with pork, savory brown sauce",
    260: "A plate of stir-fried wood ear mushroom with pork, dark savory sauce",
    261: "A plate of stir-fried garlic sprouts with pork, green and brown",
    262: "A plate of stir-fried pickled radish with pork, sour and savory",
    263: "A plate of stir-fried pickled green beans with pork, sour and spicy",
    264: "A plate of stir-fried celery with pork, green and white, savory",
    265: "A plate of stir-fried potato slices with pork, golden potatoes with meat",
    268: "A plate of Jiangxi style stir-fried pork, spicy green peppers and pork slices",
    269: "A plate of stir-fried garlic sprouts with cured meat, smoky savory",
    271: "A plate of farmhouse one bowl fragrant, eggs, pork and peppers in one bowl, spicy",
    272: "A plate of stir-fried king oyster mushroom with cured meat, earthy and smoky",
    275: "A plate of stir-fried smoked bamboo shoots with cured meat, dark and smoky",
    276: "A plate of stir-fried spicy beef slices, red chili and tender beef",
    311: "A set meal of braised pork belly with sweet potato noodles, dark glossy sauce, Anhui style",
    361: "A plate of crispy fried pork chunks, golden brown, Sichuan style",
    368: "A plate of grilled cartilage meatballs and sausages, crispy grilled",
    369: "A bowl of assorted meatball feast, various meatballs in savory broth",
    373: "A cream puff pastry, golden round shell with cream filling, dusted with sugar",
    376: "A sandwich, two slices of bread with lettuce, meat and cheese",
    377: "Oreo cookie dessert, chocolate cookies with cream filling, crushed and decorated",
    380: "A chocolate mochi, dark round chewy mochi with chocolate filling",
    381: "A blueberry bagel, golden ring-shaped bread with blueberry bits",
    382: "A coconut cream stick bread, long golden bread with coconut filling",
    383: "A blueberry cheese bread, soft bread with blueberry cream cheese filling",
    385: "A cranberry cream pastry, golden bread with red cranberry bits",
    386: "A strawberry sweet pastry, pink decorated bread with strawberry",
    387: "An egg tart, golden yellow custard in flaky pastry shell",
    388: "A Swiss cake roll, soft sponge cake rolled with cream, spiral cross-section",
    391: "A red velvet cake box, layered red cake with white cream in a box",
    392: "A black forest cake slice, chocolate cake with cherries and cream",
    393: "A tiramisu dessert, layered coffee flavored cake with cocoa powder",
    394: "A snow mochi, white round chewy mochi with cream filling",
    395: "A glazed donut, golden ring donut with sweet glaze and colorful sprinkles",
    396: "A crab snack cake, golden square cake with crab pattern",
    397: "A cheese bread bun, soft fluffy bread with cream cheese filling",
    419: "A bowl of Cantonese clear tonic soup, light nourishing soup with various ingredients",
    420: "A bowl of taro sago coconut milk dessert, creamy white with taro chunks",
    421: "A bowl of red bean sweet paste, warm dark red sweet soup",
    422: "A bowl of mung bean sweet paste, warm green sweet soup",
    423: "A bowl of Cantonese double skin milk pudding, silky white pudding in bowl",
    424: "A bowl of snow fungus papaya pear soup, nourishing sweet soup with white fungus",
    425: "A bowl of mango sago dessert, yellow creamy mango with sago pearls",
    426: "A bowl of fruit sago dessert, colorful fruits with sago pearls in coconut milk",
    427: "A glass of sugarcane water chestnut drink, clear sweet refreshing drink",
    428: "A glass of apple astragalus tonic water, warm herbal health drink",
    430: "A cup of hot apple pear orange fruit tea, warm fruity tea drink",
    449: "A bowl of breakfast noodles, simple noodles in clear broth, morning meal",
    477: "A bowl of Sichuan style boiled meat slices in spicy broth, red oil surface, Mao style",
    478: "A bowl of Sichuan style boiled meat rolls in spicy broth, red oil surface",
    479: "A bowl of Sichuan style boiled crispy pork in spicy broth, red oil surface",
    481: "A bowl of Sichuan style boiled ham in spicy broth, red oil surface",
    550: "A clay pot of spicy pork slices, sizzling hot spicy meat in stone pot",
    551: "A clay pot of silky egg with minced pork, golden egg and meat in hot pot",
    552: "A clay pot of beef tendon and offal stew, rich dark broth, sizzling hot",
    553: "A clay pot of crispy pork and vegetables, sizzling hot stew",
    576: "A plate of rice topped with tomato and silky beef slices, red tangy sauce",
    577: "A plate of rice topped with spicy silky beef slices, red chili oil sauce",
    580: "A plate of crispy fried pumpkin slices, golden battered pumpkin, sweet and crispy",
    593: "A wrap with two types of meat filling, crispy golden wrap, roast duck and specialty meat",
    607: "A Chinese style hamburger patty sandwich, grilled meat patty in bun",
    609: "A golden shrimp burger, crispy shrimp patty in bun with lettuce",
    610: "A pineapple beef burger, beef patty with grilled pineapple slice in bun",
    612: "A fruit pie pastry, golden crispy pie with taro/pineapple/red bean filling choices",
    613: "A plate of fried sweet potato balls, golden crispy balls",
    614: "A serving of French fries, golden crispy potato sticks, fast food style",
    615: "A deep-fried banana with crispy batter, golden brown crust",
    617: "A plate of spicy chicken wing roots, red spicy marinated wings, fried crispy",
    631: "A light healthy meal plate, fresh vegetables, lean protein and grains, diet friendly",
    649: "A plate of cold rice noodles with sesame sauce, chewy cold noodles with cucumber, Liangpi style",
    651: "A bowl of spicy Chongqing wontons in numbing chili broth, red oil and Sichuan pepper",
    652: "A plate of dry mixed Chongqing wontons without soup, tossed in chili oil and sesame",
    653: "A plate of wontons tossed with chopped chili, red spicy no soup",
    654: "A plate of wontons with tomato salsa sauce, red tangy Spanish style sauce",
    655: "A bowl of all-vegetable light diet noodles, green vegetables and noodles in clear broth",
    663: "A small bowl of Beijing fried sauce noodles, breakfast portion, sesame sauce and noodles",
    673: "A small Xi'an steamed glutinous rice cake with dates, sticky sweet traditional snack",
    674: "A large Xi'an steamed glutinous rice cake with dates, sticky sweet traditional snack",
    699: "A plate of stir-fried thick noodles, Xinjiang style, spicy and savory",
    708: "A plate of Xinjiang stir-fried rice noodles and naan half-half combo, spicy red sauce",
    718: "A personal mini hot pot, one person portion, bubbling broth with vegetables and meat",
}

STYLE = "cartoon style illustration, flat design, cute kawaii food illustration, warm cream background, soft warm colors, appetizing, simple and clean, no text"

patched_count = 0
for d in data:
    if d['idx'] in patches:
        d['prompt'] = f"{patches[d['idx']]}, {STYLE}"
        patched_count += 1

print(f"Patched {patched_count} dishes")

# Verify no more generic fallbacks
generic = [d for d in data if 'A plate of Chinese dish,' in d['prompt']]
print(f"Remaining generic fallbacks: {len(generic)}")
for d in generic:
    print(f"  {d['idx']:03d}: {d['name']}")

with open(r'E:\竞赛\ai+食\ai-food-mobile\.temp\dishes_with_prompts.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
