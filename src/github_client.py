import logging
import requests
from typing import Dict, List, Optional
import base64

logger = logging.getLogger(__name__)

class GitHubClient:
    """Client for interacting with the GitHub API."""
    
    def __init__(self, token: str, repo_owner: str, repo_name: str):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Get the diff for a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}"
        headers = {**self.headers, "Accept": "application/vnd.github.v3.diff"}
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.text
    
    def get_pr_files(self, pr_number: int) -> List[Dict]:
        """Get the list of files changed in a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}/files"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_file_content(self, file_path: str, ref: Optional[str] = None) -> str:
        """Get the content of a file from the repository."""
        url = f"{self.base_url}/contents/{file_path}"
        if ref:
            url += f"?ref={ref}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        content = response.json()["content"]
        return base64.b64decode(content).decode("utf-8")
    
    def post_review(self, pr_number: int, review_comments: List[Dict]) -> Dict:
        """Post a review with comments on a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}/reviews"
        
        payload = {
            "commit_id": self._get_latest_commit_sha(pr_number),
            "body": "AI-powered code review",
            "event": "COMMENT",
            "comments": review_comments
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def post_comment(self, pr_number: int, comment: str) -> Dict:
        """Post a general comment on a pull request."""
        url = f"{self.base_url}/issues/{pr_number}/comments"
        
        payload = {"body": comment}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        return response.json()
    
    def _get_latest_commit_sha(self, pr_number: int) -> str:
        """Get the SHA of the latest commit in a pull request."""
        url = f"{self.base_url}/pulls/{pr_number}/commits"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        commits = response.json()
        return commits[-1]["sha"]
