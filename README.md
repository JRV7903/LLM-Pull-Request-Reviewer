# LLM-Powered GitHub Pull Request Reviewer 🚀

An AI-based GitHub pull request review tool using OpenAI's LLM.

## Features
- **Automatic PR Reviews**: Uses GPT-4 to analyze code changes.
- **Static Code Analysis**: Uses `pylint` and AST for additional checks.
- **GitHub Webhook Integration**: Auto-triggers reviews for PRs.

## Setup
- Install dependencies: `pip install -r requirements.txt`
- Run API: `uvicorn src.main:app --reload`
- Deploy GitHub Webhook: `python scripts/setup_webhook.py`

## Usage
- Open a pull request on GitHub.
- The bot automatically reviews the changes and posts comments.

## Deployment
- Use Docker: `docker build -t llm-pr-reviewer .`
