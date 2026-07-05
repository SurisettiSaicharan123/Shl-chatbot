from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.chatbot import chat

app = FastAPI(title="SHL Assessment Recommender")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve CSS and JS files
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")


class ChatRequest(BaseModel):
    messages: list


# Home page
@app.get("/")
def home():
    return FileResponse("app/frontend/index.html")


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Chat API
@app.post("/chat")
def chat_api(request: ChatRequest):
    return chat(request.messages)