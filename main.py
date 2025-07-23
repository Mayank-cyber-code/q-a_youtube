from fastapi import FastAPI, Request
import httpx

app = FastAPI()

# Updated ngrok public URL for your local transcript fetcher API
LOCAL_TRANSCRIPT_API_URL = "https://4a2c738dbc17.ngrok-free.app/fetch_transcript"

def your_qa_chain(transcript: str, question: str) -> str:
    # Placeholder QA logic — replace with your own LLM/QA system
    return f"Transcript length: {len(transcript)} characters\nQuestion was: {question}"

@app.post("/api/ask")
async def ask(request: Request):
    data = await request.json()
    video_url = data.get("video_url")
    question = data.get("question")
    if not video_url or not question:
        return {"error": "Both video_url and question are required."}

    # Call your local transcript fetcher API via ngrok tunnel
    async with httpx.AsyncClient() as client:
        response = await client.post(LOCAL_TRANSCRIPT_API_URL, json={"video_url": video_url})
        if response.status_code != 200:
            return {"error": "Failed to fetch transcript", "details": response.text}

        transcript = response.json().get("transcript")
        if not transcript:
            return {"error": "Transcript not found"}

    # Run QA logic on the fetched transcript and question
    answer = your_qa_chain(transcript, question)
    return {"answer": answer}
