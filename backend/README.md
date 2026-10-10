# AI 助食 API

在项目根目录执行：

```powershell
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app:app --reload --port 8000
```

接口文档：`http://127.0.0.1:8000/docs`

## DeepSeek 助手

在项目根目录 `.env` 填写 `DEEPSEEK_API_KEY`，然后重启后端。默认使用
`DEEPSEEK_BASE_URL=https://api.deepseek.com`、`DEEPSEEK_MODEL=deepseek-chat`。
密钥只由后端读取，不发送给浏览器。前端访问 `http://localhost:8080/`。

`POST /api/ai/analyze`：message、goal（维持/减脂/增肌）、allergies、dislikes。
每次独立两次模型调用：解析菜名及数量，再生成报告；不发送聊天历史。
后端计算总热量及三大营养素供能占比，前端绘制饼图并对照通用每日参考量。
参考量不是个体推荐量，单餐不会被解释成全天摄入。

优先匹配唯一同名菜品且普通一份的数据库营养值；其他份量或缺失数据采用模型估算，
报告标注来源、分量与 ±25% 的展示区间（此区间是产品提示范围，不是统计置信区间）。
数据库没有膳食纤维字段，未知值保留 null，不能当作零。

本版 RAG 用字符 unigram/bigram 稀疏向量与余弦相似度进行内存检索，
菜品知识来自 MySQL，健康知识来自 `backend/nutrition_knowledge.json` 中的指南摘要。
这是轻量词汇检索，不等同于 PRD 的语义嵌入 + Chroma/Milvus；后续可替换检索层，
当前健康知识也只是三条有来源的摘要，不是完整权威知识库。
无知识命中时提供模型通用回答，并标注仅供参考。照片识别不在本次范围。
未配置密钥、上游鉴权/余额/限流/超时均返回明确错误，不降级成演示答案。

测试：`python -m unittest backend.test_ai_service`。真实模型联调需要有效密钥及网络。
