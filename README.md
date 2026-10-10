# AI 助食 · 手机版网站

根据 `docs/` 中的产品需求文档与设计建议制作的手机端网站演示版。

## 文件说明

- `dist/index.html`：网站入口
- `dist/style.css`：移动端样式
- `dist/app.js`：页面、示例数据和交互逻辑
- `dist/dish-images/{三位数菜品ID}.jpg`：按菜品 ID 对应的菜品封面（例如 `001.jpg`，当前提供 001-718，共 717 张）
- `dist/food.png`：缺少对应封面时的默认兜底图
- `docs/`：原始需求与设计文档
- `.openai/hosting.json`：现有 Sites 发布配置

## 本地运行

有 Python 3 的电脑上，进入本目录后运行：

```bash
python -m http.server 8000 --directory dist
```

然后在浏览器访问 `http://localhost:8000/`。也可以直接打开 `dist/index.html`，但使用本地服务器更接近部署环境。

## 已实现

推荐页、按食堂抽窗口的转盘、喜欢/跳过/撤销与二次筛选卡片、食堂和窗口浏览、菜品搜索与详情、周榜/月榜、点评、偏好设置、营养分析演示。点评和偏好保存在当前浏览器。

## 当前边界

这是带示例数据的前端演示版。短信登录、云端数据库、真实 AI 对话和图片识别尚未接入。营养信息与榜单数据仅用于界面和流程测试，不应作为真实饮食建议或校园菜品信息。

## 数据库初始化

先执行基础菜品数据，再执行业务扩展表：

```sql
SOURCE database/ai_food_import.sql;
SOURCE database/ai_food_app_schema.sql;
```

`ai_food_import.sql` 提供 2 个食堂、51 个窗口和 737 道菜品，并将 `image_url` 统一设置为三位数菜品 ID 文件名；当前新封面覆盖 001-718（083 以及 719-737 暂无图片，前端使用 `food.png` 兜底）。`ai_food_app_schema.sql` 只新增用户、偏好、点评、排行榜快照和 AI 对话表，不会删除基础菜品数据。
