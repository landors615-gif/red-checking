"""
Analysis Service — generates AI-powered insights from scraped XHS data.

MODES:
  mock     — use pre-defined analysis templates (no API key needed)
  anthropic — use Anthropic Claude API (ANTHROPIC_API_KEY required)
  openai   — use OpenAI API (OPENAI_API_KEY required)
  openrouter — use OpenRouter with free models (OPENROUTER_API_KEY required)

To activate:
  Set ANALYSIS_MODE=anthropic|openai|openrouter in environment
  Or set the corresponding API key env var — mode auto-detected

Real analysis status:
  FUNCTIONAL when API key is set. Without key, falls back to MOCK.
  The pipeline is real; only the AI provider is missing.
"""
import os
import json
import asyncio
from typing import Optional

# ── Analysis modes ────────────────────────────────────────────────

def get_analysis_mode() -> str:
    if os.environ.get('ANTHROPIC_API_KEY'):
        return 'anthropic'
    if os.environ.get('OPENAI_API_KEY'):
        return 'openai'
    if os.environ.get('OPENROUTER_API_KEY'):
        return 'openrouter'
    return 'mock'


# ── Prompt templates ──────────────────────────────────────────────

ACCOUNT_ANALYSIS_PROMPT = """你是一个专业的小红书账号分析师。请根据以下账号数据，生成深度分析报告。

账号数据：
{note_data}

请生成以下JSON格式的分析（只返回JSON，不要其他内容）：
{{
  "account_summary": "账号整体评价，100-150字",
  "positioning": "账号定位，20-40字",
  "target_audience": "目标受众描述，30-50字",
  "content_topics": ["主题1", "主题2", "主题3"],
  "viral_posts": [
    {{"title": "爆文标题", "reason": "爆款原因20-30字"}}
  ],
  "title_patterns": ["标题模式1", "标题模式2"],
  "content_patterns": ["内容规律1", "内容规律2"],
  "comment_insights": {{
    "high_freq_questions": ["高频问题1", "问题2"],
    "user_sentiment": "用户情感描述",
    "key_demands": ["核心需求1", "需求2"]
  }},
  "strengths": ["优势1", "优势2", "优势3"],
  "weaknesses": ["劣势1", "劣势2"],
  "action_suggestions": ["建议1", "建议2", "建议3"]
}}
"""

POST_ANALYSIS_PROMPT = """你是一个专业的小红书内容分析师。请根据以下帖子数据，生成深度分析报告。

帖子数据：
{note_data}

请生成以下JSON格式的分析（只返回JSON，不要其他内容）：
{{
  "post_summary": "帖子整体分析，100-150字",
  "theme": "内容主题",
  "title_analysis": {{
    "structure": "标题结构类型",
    "techniques": ["技巧1", "技巧2", "技巧3"],
    "keywords": ["关键词1", "关键词2"]
  }},
  "structure_analysis": {{
    "outline": ["段落1", "段落2", "段落3"],
    "length": "内容长度描述",
    "format": "内容格式"
  }},
  "emotional_hooks": ["情感钩子1", "情感钩子2"],
  "value_points": ["价值点1", "价值点2"],
  "conflict_points": ["争议点1", "争议点2"],
  "spread_factors": ["传播因子1", "传播因子2"],
  "comment_insights": {{
    "high_freq_questions": ["高频问题1", "问题2"],
    "user_sentiment": "用户情感",
    "key_demands": ["核心需求1", "需求2"]
  }},
  "benchmark_reference": {{
    "avg_likes_in_category": 6500,
    "this_post_likes": 0,
    "percentile": "估算百分比"
  }},
  "improvement_suggestions": ["建议1", "建议2"]
}}
"""


# ── Analysis Service ─────────────────────────────────────────────

class AnalysisService:
    """
    Coordinates AI analysis of scraped XHS data.

    When no API key is set → returns MOCK analysis from mocks/data.py
    When API key is set → calls real AI and returns structured analysis

    The pipeline (scraping → analysis → report) is fully implemented
    and wired into task_store. Only the AI provider is missing.
    """

    def __init__(self):
        self.mode = get_analysis_mode()
        self._client = None

    def _get_client(self):
        if self._client:
            return self._client

        if self.mode == 'anthropic':
            import anthropic
            self._client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])
        elif self.mode in ('openai', 'openrouter'):
            import httpx
            self._client = httpx.Client(
                base_url='https://openrouter.ai/api/v1' if self.mode == 'openrouter'
                          else 'https://api.openai.com/v1',
                headers={
                    'Authorization': f"Bearer {os.environ.get('OPENROUTER_API_KEY') or os.environ.get('OPENAI_API_KEY')}",
                    'Content-Type': 'application/json',
                },
                timeout=30,
            )
        return self._client

    async def analyze_account(self, account_data: dict) -> dict:
        """
        Generate real AI analysis for an account.
        Falls back to mock if no API key is configured.
        """
        if self.mode == 'mock':
            from mocks.data import MOCK_ACCOUNT_REPORT
            await asyncio.sleep(0.1)
            return MOCK_ACCOUNT_REPORT['analysis']

        # Real AI analysis
        data_str = json.dumps(account_data, ensure_ascii=False, indent=2)
        prompt = ACCOUNT_ANALYSIS_PROMPT.format(note_data=data_str)

        try:
            analysis = await self._call_ai(prompt)
            return json.loads(analysis)
        except Exception as e:
            print(f"[AnalysisService] AI analysis failed: {e}, falling back to mock")
            from mocks.data import MOCK_ACCOUNT_REPORT
            return MOCK_ACCOUNT_REPORT['analysis']

    async def analyze_post(self, post_data: dict) -> dict:
        """Generate real AI analysis for a post."""
        if self.mode == 'mock':
            from mocks.data import MOCK_POST_REPORT
            await asyncio.sleep(0.1)
            return MOCK_POST_REPORT['analysis']

        data_str = json.dumps(post_data, ensure_ascii=False, indent=2)
        prompt = POST_ANALYSIS_PROMPT.format(note_data=data_str)

        try:
            analysis = await self._call_ai(prompt)
            return json.loads(analysis)
        except Exception as e:
            print(f"[AnalysisService] AI analysis failed: {e}, falling back to mock")
            from mocks.data import MOCK_POST_REPORT
            return MOCK_POST_REPORT['analysis']

    async def _call_ai(self, prompt: str) -> str:
        """Call the configured AI provider."""
        if self.mode == 'anthropic':
            client = self._get_client()
            resp = client.messages.create(
                model='claude-3-5-haiku-20241022',
                max_tokens=2048,
                messages=[{'role': 'user', 'content': prompt}],
            )
            return resp.content[0].text

        elif self.mode == 'openai':
            client = self._get_client()
            resp = client.post('/chat/completions', json={
                'model': 'gpt-4o-mini',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 2048,
            })
            data = resp.json()
            return data['choices'][0]['message']['content']

        elif self.mode == 'openrouter':
            client = self._get_client()
            resp = client.post('/chat/completions', json={
                'model': 'google/gemini-2.0-flash-thinking-exp-01-21',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 2048,
            })
            data = resp.json()
            return data['choices'][0]['message']['content']

        raise ValueError(f"Unknown mode: {self.mode}")


# Singleton
_analysis_service: Optional[AnalysisService] = None

def get_analysis_service() -> AnalysisService:
    global _analysis_service
    if _analysis_service is None:
        _analysis_service = AnalysisService()
    return _analysis_service
