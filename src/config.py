import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
GITHUB_API_URL = "https://api.github.com"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Validate required environment variables
required_vars = ["GITHUB_ACCESS_TOKEN", "OPENAI_API_KEY", "WEBHOOK_SECRET", "WEBHOOK_URL"]
for var in required_vars:
    if not globals()[var]:
        raise ValueError(f"Missing required environment variable: {var}")
