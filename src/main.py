from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.webhook_handler import process_webhook
from src.config import WEBHOOK_SECRET
import hmac
import hashlib

app = FastAPI()

@app.post("/webhook")
async def github_webhook(request: Request):
    # Verify webhook signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        raise HTTPException(status_code=400, detail="No signature provided")
    
    body = await request.body()
    expected_signature = "sha256=" + hmac.new(WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Process the webhook
    event_type = request.headers.get("X-GitHub-Event")
    payload = await request.json()
    
    if event_type == "pull_request":
        process_webhook(payload)
        return JSONResponse(content={"message": "Webhook processed successfully"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Event type not supported"}, status_code=200)

@app.get("/")
def read_root():
    return {"message": "LLM Pull Request Reviewer API is running"}
