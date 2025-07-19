from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from youtube_utils import download_audio
from transcriber import transcribe_audio
from embedder import store_embeddings, query_embeddings
from qna import answer_query
from hashlib import md5

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "YouTube QnA Bot backend is running!"}

@app.post("/process")
async def process_video(video_url: str = Form(...), question: str = Form(...)):
    try:
        video_id = md5(video_url.encode()).hexdigest()
        audio_path = download_audio(video_url)
        transcript = transcribe_audio(audio_path)
        store_embeddings(transcript, video_id)
        context = query_embeddings(question, video_id)
        answer = answer_query(question, context)
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
