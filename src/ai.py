"""BookMind — LM Studio AI 引擎"""
import json
import urllib.request
from typing import Optional

API_BASE = "http://localhost:1234/v1"
DEFAULT_MODEL = "google/gemma-4-e4b"

class AIEngine:
    def __init__(self, model: str = DEFAULT_MODEL, api_base: str = API_BASE):
        self.model = model
        self.api_base = api_base
    
    def chat(self, system: str, user: str, 
             temperature: float = 0.3, max_tokens: int = 1024) -> str:
        """Send a chat completion request to LM Studio."""
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        req = urllib.request.Request(
            f"{self.api_base}/chat/completions",
            data=json.dumps(payload).encode('utf-8'),
            method='POST'
        )
        req.add_header('Content-Type', 'application/json')
        
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                result = json.loads(resp.read())
                return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"[AI Error] {e}"
    
    def summarize(self, text: str, max_length: str = "详细") -> str:
        """Generate a summary of the given text."""
        system = "你是一位专业的书籍分析师。请用中文输出高质量的内容总结。"
        user = f"""请对以下文本进行{max_length}总结，提取核心观点：

{text[:2800]}"""
        return self.chat(system, user)
    
    def extract_insights(self, text: str) -> str:
        """Extract key insights and knowledge from text."""
        system = "你是一位知识萃取专家。从文本中提取可用的知识、方法和洞见。"
        user = f"""从以下内容中提取：
1. 🔑 **核心观点**（3-5个）
2. 💡 **关键洞见**（最重要的发现）
3. 🛠 **可操作方法**（如何应用到实践）
4. 📝 **金句摘录**（最有价值的原文）

文本：
{text[:2800]}"""
        return self.chat(system, user, temperature=0.4, max_tokens=800)
    
    def generate_skill_card(self, text: str) -> str:
        """Generate a skill card from knowledge."""
        system = "你是一位技能设计师。将知识提炼为可复用的技能卡片。"
        user = f"""将以下知识转化为一张**技能卡片**，格式如下：

# [技能名称]

## 适用场景
- 什么时候使用这个技能

## 核心步骤
1. ...
2. ...
3. ...

## 关键要点
- 注意事项

## 相关技能
- 关联其他知识

知识来源：
{text[:2500]}"""
        return self.chat(system, user, temperature=0.5, max_tokens=1000)
