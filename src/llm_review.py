import logging
import openai
import time
import json
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class LLMReviewer:
    """Uses OpenAI's LLM to review code changes."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        openai.api_key = api_key
        
        self.review_prompt_template = """
        You are an expert code reviewer. Review the following code diff and provide constructive feedback.
        Focus on:
        1. Code correctness
        2. Performance issues
        3. Security vulnerabilities
        4. Code style and best practices
        5. Potential bugs or edge cases
        
        Here's the code diff:
        ```
        {diff}
        ```
        
        Static analysis results:
        {static_analysis}
        
        Format your response as a JSON array of comments, where each comment has:
        - path: the file path
        - line: the line number to comment on
        - body: your detailed comment
        
        Example:
        [
            {{"path": "src/main.py", "line": 42, "body": "Consider using a context manager here to ensure resources are properly closed."}},
            {{"path": "src/utils.py", "line": 15, "body": "This function has a potential division by zero error if the input is 0."}}
        ]
        """
    
    def review_code(self, diff: str, static_analysis: Optional[Dict] = None) -> List[Dict]:
        """
        Review code changes using the LLM.
        
        Args:
            diff: The git diff of the changes
            static_analysis: Optional static analysis results
            
        Returns:
            List of review comments
        """
        static_analysis_str = json.dumps(static_analysis, indent=2) if static_analysis else "No static analysis results available."
        
        prompt = self.review_prompt_template.format(
            diff=diff[:4000],
            static_analysis=static_analysis_str
        )
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert code reviewer."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                
                review_text = response["choices"][0]["message"]["content"].strip()
                
                review_comments = self._extract_json(review_text)
                
                if isinstance(review_comments, list):
                    return review_comments
                else:
                    logger.error("LLM response is not a valid JSON array")
                    return [{"path": "", "line": 0, "body": review_text}]
                
            except openai.error.RateLimitError:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
