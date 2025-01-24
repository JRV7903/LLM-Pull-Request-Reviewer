from fastapi import FastAPI
from src.webhook_handler import router as webhook_router

app = FastAPI()

app.include_router(webhook_router)

@app.get("/")
def read_root():
    return {"message": "LLM Pull Request Reviewer API is running"}
