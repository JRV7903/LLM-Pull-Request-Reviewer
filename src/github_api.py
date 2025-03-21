import requests
from src.config import settings

def get_pr_changes(repo, pull_request_number):
    headers = {"Authorization": f"token {settings.GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{repo}/pulls/{pull_request_number}"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    pr_data = response.json()
    diff_url = pr_data.get("diff_url")
    
    if not diff_url:
        raise ValueError("No diff URL found in the PR data")
    
    diff_response = requests.get(diff_url, headers=headers)
    diff_response.raise_for_status()
    
    return diff_response.text

def comment_on_pr(repo, pull_request_number, comment):
    headers = {
        "Authorization": f"token {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"https://api.github.com/repos/{repo}/issues/{pull_request_number}/comments"
    
    data = {"body": comment}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    
    return response.json()
