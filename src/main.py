# src/main.py
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hmac
import hashlib
import json
from .config import settings
from .github_client import GitHubClient
from .llm_reviewer import LLMReviewer
from .code_analyzer import CodeAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="LLM Pull Request Reviewer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PullRequestEvent(BaseModel):
    action: str
    pull_request: dict
    repository: dict

def verify_github_webhook(request: Request):
    """Verify that the webhook request came from GitHub using the secret token."""
    if not settings.GITHUB_WEBHOOK_SECRET:
        logger.warning("No webhook secret configured, skipping verification")
        return True
    
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=403, detail="Missing signature header")
    
    body = await request.body()
    
    # Calculate expected signature
    expected_signature = "sha256=" + hmac.new(
        settings.GITHUB_WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    return True

@app.post("/webhook/github")
async def github_webhook(request: Request, verified: bool = Depends(verify_github_webhook)):
    """Handle GitHub webhook events for pull requests."""
    body = await request.body()
    event_type = request.headers.get("X-GitHub-Event")
    
    if event_type != "pull_request":
        return {"message": f"Event type {event_type} ignored"}
    
    try:
        payload = json.loads(body)
        event = PullRequestEvent(**payload)
        
        # Only process opened or synchronized PRs
        if event.action not in ["opened", "synchronize"]:
            return {"message": f"PR action {event.action} ignored"}
        
        # Initialize clients
        github_client = GitHubClient(
            token=settings.GITHUB_TOKEN,
            repo_owner=event.repository["owner"]["login"],
            repo_name=event.repository["name"]
        )
        
        llm_reviewer = LLMReviewer(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL
        )
        
        code_analyzer = CodeAnalyzer()
        
        # Process the pull request
        pr_number = event.pull_request["number"]
        logger.info(f"Processing PR #{pr_number}")
        
        # Get PR diff
        diff = github_client.get_pr_diff(pr_number)
        
        # Analyze code with static analysis
        static_analysis = code_analyzer.analyze(diff)
        
        # Get LLM review
        llm_review = llm_reviewer.review_code(diff, static_analysis)
        
        # Post review comments
        github_client.post_review(pr_number, llm_review)
        
        return {"message": f"Successfully reviewed PR #{pr_number}"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
