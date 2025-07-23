import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production!
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read ngrok URL from environment variable with fallback default
LOCAL_TRANSCRIPT_API_URL = os.getenv(
    "LOCAL_TRANSCRIPT_API_URL",
    "https://b2445003ef29.ngrok-free.app/fetch_transcript"  # fallback ngrok URL
)

def your_qa_chain(transcript: str, question: str) -> str:
    # Replace this with your actual QA or LLM implementation
    return f"Transcript length: {len(transcript)} characters\nQuestion was: {question}"

@app.get("/")
async def root():
    return {"message": "YouTube Transcript Q&A backend is running."}

@app.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    video_url = data.get("video_url")
    question = data.get("question")
    if not video_url or not question:
        return {"error": "Both video_url and question are required."}

    async with httpx.AsyncClient() as client:
        response = await client.post(LOCAL_TRANSCRIPT_API_URL, json={"video_url": video_url})
        if response.status_code != 200:
            return {"error": "Failed to fetch transcript", "details": response.text}

        transcript = response.json().get("transcript")
        if not transcript:
            return {"error": "Transcript not found"}

    answer = your_qa_chain(transcript, question)
    return {"answer": answer}
