import requests
from src.config import GITHUB_ACCESS_TOKEN, GITHUB_API_URL, WEBHOOK_URL, WEBHOOK_SECRET

def setup_webhook(repo):
    headers = {
        "Authorization": f"token {GITHUB_ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "name": "web",
        "active": True,
        "events": ["pull_request"],
        "config": {
            "url": WEBHOOK_URL,
            "content_type": "json",
            "secret": WEBHOOK_SECRET
        }
    }

    response = requests.post(f"{GITHUB_API_URL}/repos/{repo}/hooks", json=payload, headers=headers)

    if response.status_code == 201:
        print(f"✅ Webhook successfully set up for {repo}")
    else:
        print(f"❌ Failed to set up webhook for {repo}. Status code: {response.status_code}")
        try:
            print(response.json())
        except requests.exceptions.JSONDecodeError:
            print("⚠️ Error: Could not decode response JSON.")

if __name__ == "__main__":
    repo = "yourusername/yourrepo"  # Change this to your actual GitHub repo
    setup_webhook(repo)
