import requests
from src.config import GITHUB_ACCESS_TOKEN, GITHUB_API_URL

repo = "yourusername/yourrepo"
webhook_url = "https://your-deployed-url.com/webhook"

headers = {
    "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# payload = {
#     "name": "web",
#     "active": True,
#     "events": ["pull_request"],
#     "config": {
#         "url": webhook_url,
#         "content_type": "json"
#     }
# }

response = requests.post(f"{GITHUB_API_URL}/repos/{repo}/hooks", json=payload, headers=headers)
print(response.json())
