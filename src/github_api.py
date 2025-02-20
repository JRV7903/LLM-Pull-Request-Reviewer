# import requests
# from src.config import GITHUB_ACCESS_TOKEN, GITHUB_API_URL

# def get_pr_changes(repo, pull_request_number):
#     headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
#     url = f"{GITHUB_API_URL}/repos/{repo}/pulls/{pull_request_number}"
    
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
    
#     pr_data = response.json()
#     diff_url = pr_data["diff_url"]
    
#     diff_response = requests.get(diff_url, headers=headers)
#     diff_response.raise_for_status()
    
#     return diff_response.text

# def comment_on_pr(repo, pull_request_number, comment):
#     headers = {
#         "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
#         "Accept": "application/vnd.github.v3+json"
#     }
#     url = f"{GITHUB_API_URL}/repos/{repo}/issues/{pull_request_number}/comments"
    
#     data = {"body": comment}
#     response = requests.post(url, json=data, headers=headers)
#     response.raise_for_status()
    
#     return response.json()
