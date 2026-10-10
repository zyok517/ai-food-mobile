// Real single-turn assistant. Existing chat history is display-only, never sent as context.
let aiBusy = false;
function aiReport(result) {
  const safe = value => esc(String(value ?? ''));
  const t = result.totals, s = result.shares;
  const foodRows = result.foods.map(x => `<div style="padding:10px 0;border-bottom:1px solid #ddd"><strong>${safe(x.name)}</strong> × ${safe(x.quantity)}<br><small>${safe(x.portion)} · ${safe(x.source)}</small><br>${safe(x.kcal_range[0])}–${safe(x.kcal_range[1])} kcal（中心估算 ${safe(x.kcal)}）</div>`).join('');
  const p = Math.max(0,Math.min(100,Number(s.protein)||0)), f = Math.max(0,Math.min(100-p,Number(s.fat)||0));
  const chart = `<div role="img" aria-label="营养素供能占比：蛋白质${p}%，脂肪${f}%，碳水${safe(s.carbs)}%" style="width:110px;height:110px;border-radius:50%;margin:14px auto;background:conic-gradient(#75b898 0 ${p}%,#edb65c ${p}% ${p+f}%,#d88475 ${p+f}% 100%)"></div><p>蛋白质 ${safe(s.protein)}% · 脂肪 ${safe(s.fat)}% · 碳水 ${safe(s.carbs)}%</p>`;
  const comparison = ['kcal','protein','fat','carbs'].map((k,i)=>`<div><small>${['热量','蛋白质','脂肪','碳水'][i]}</small><b>${safe(t[k])}${i?'g':' kcal'}</b><small>日参考 ${result.daily_reference[k]}${i?'g':' kcal'} · ${Math.round(t[k]/result.daily_reference[k]*100)}%</small></div>`).join('');
  return `${result.intent==='nutrition'?`<strong>${result.scope==='day'?'已输入全天':'本餐'}营养估算</strong>${foodRows}<div class="nutrition" style="margin:12px 0"><b>总热量 ${safe(t.kcal)} kcal</b>${chart}<div class="nutrition-grid">${comparison}</div><p class="meta">每日参考为通用成人示例，不是个人目标。${result.scope==='meal'?'本餐数据不能代表全天摄入。':''}占比按营养素供能计算。</p></div>`:''}<p>${safe(result.answer||result.evaluation)}</p>${result.answer&&result.evaluation?`<p>${safe(result.evaluation)}</p>`:''}<ul>${result.suggestions.map(x=>`<li>${safe(x)}</li>`).join('')}</ul><p class="meta">${result.sources.length?'参考：'+result.sources.map(x=>safe(x.title)).join('；'):'未检索到相关知识，以下为模型通用建议。'}</p><small>${safe(result.disclaimer)}</small>`;
}
ai = function(){return `${head('AI 助手')}<div class="ai-entry"><div class="row between"><h2>✦ 饮食小助手</h2>${tag('DeepSeek','mint')}</div><p style="margin-top:8px;line-height:1.6">输入菜品和分量，分析这一餐或今天的饮食；也可以询问健康饮食问题。</p><small>当前目标：${esc(state.preferences.goal)}。按菜名估算，实际分量和用油会影响结果。</small></div><div class="chips"><button class="chip" data-ai-prompt="我这餐吃了普通一份番茄炒蛋、半份宫保鸡丁和一碗米饭">分析这一餐</button><button class="chip" data-ai-prompt="减脂期间食堂怎么选？">健康问答</button></div><div class="chat" id="chat"><div class="bubble ai">告诉我吃了什么，最好注明几份、几碗或克重。我会结合菜品库和你的饮食目标分析。</div>${state.messages.map(m=>`<div class="bubble ${m.role}">${m.report?aiReport(m.report):esc(m.text||'旧版演示记录，请重新提问获取真实分析。')}</div>`).join('')}${aiBusy?'<div class="bubble ai">正在解析菜品并生成报告，请稍候…</div>':''}</div><div class="ai-compose"><textarea id="ai-input" class="textarea" maxlength="1200" ${aiBusy?'disabled':''} aria-label="输入饮食问题" placeholder="例如：这餐吃了半份宫保鸡丁和一碗米饭">${esc(state.aiInput)}</textarea><button id="ai-send" class="btn small" ${aiBusy?'disabled':''}>${aiBusy?'分析中':'发送'}</button></div><p class="meta">单轮对话，每次请提供完整信息。当前支持文字，不支持照片识别。</p>`};
sendAI = async function(){
  const txt=$('#ai-input')?.value.trim(); if(!txt||aiBusy)return;
  aiBusy=true;state.messages.push({role:'user',text:txt});state.aiInput='';render();
  const controller=new AbortController(), timer=setTimeout(()=>controller.abort(),110000);
  try {
    const response=await fetch(`${API_BASE}/api/ai/analyze`,{method:'POST',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({message:txt,goal:state.preferences.goal,allergies:state.preferences.allergy||'',dislikes:state.preferences.dislike||[]})});
    const data=await response.json();if(!response.ok)throw Error(typeof data.detail==='string'?data.detail:'请求参数或服务异常，请重试');
    state.messages.push({role:'ai',report:data});
  } catch(error) {state.messages.push({role:'ai',text:error.name==='AbortError'?'AI 请求超时，请稍后重试。':error.message==='Failed to fetch'?'无法连接 AI 后端，请确认 8000 端口服务已启动。':error.message});}
  finally {clearTimeout(timer);aiBusy=false;persist();if(state.page==='ai')render();}
};
if(state.page==='ai')render();
