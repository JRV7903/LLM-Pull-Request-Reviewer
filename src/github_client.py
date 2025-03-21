import logging
import requests
from typing import Dict, List, Optional
import base64
from src.config import settings

logger = logging.getLogger(__name__)

class GitHubClient:
    """Client for interacting with the GitHub API."""
    
    def __init__(self, repo_owner: str, repo_name: str):
        self.token = settings.GITHUB_TOKEN
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the diff for a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    def post_comment(self, pr_number: int, comment: str) -> Dict:
        """Post a general comment on a pull request."""
        url = f"{self.base_url}/issues/{pr_number}/comments"
        
        payload = {"body": comment}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
