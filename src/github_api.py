import requests
from src.config import GITHUB_ACCESS_TOKEN, GITHUB_API_URL

headers = {
    "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_pr_changes(repo, pr_number):
    """Fetches the changed files in a pull request."""
    url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def comment_on_pr(repo, pr_number, comment):
    """Posts a comment on the pull request."""
    url = f"{GITHUB_API_URL}/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": comment}
    requests.post(url, headers=headers, json=payload)