import logging
import openai
import json
import time
from typing import Dict, List, Optional
from src.config import settings

logger = logging.getLogger(__name__)

class LLMReviewer:
    """Uses OpenAI's LLM to review code changes."""
    
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL

    def review_code(self, diff: str, static_analysis: Optional[Dict] = None) -> List[Dict]:
        static_analysis_str = json.dumps(static_analysis, indent=2) if static_analysis else "No static analysis results available."
        
        prompt = f"""
        You are an expert code reviewer. Review the following code diff and provide constructive feedback.
        Focus on:
        - Code correctness
        - Performance issues
        - Security vulnerabilities
        - Code style and best practices
        - Potential bugs or edge cases
        
        Code Diff:
        ```
        {diff[:4000]}
        ```
        
        Static Analysis Results:
        {static_analysis_str}
        
        Return JSON format with:
        - path (file path)
        - line (line number)
        - body (your comment)
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=2000
            )
            
            review_text = response["choices"][0]["message"]["content"].strip()
            return self._extract_json(review_text)
        
        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return [{"path": "", "line": 0, "body": "Error processing review"}]

    def _extract_json(self, response_text: str) -> List[Dict]:
        try:
            json_str = response_text.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {e}")
            return [{"path": "", "line": 0, "body": response_text}]
