# backend/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .rag_chain import answer_question

app = FastAPI(
    title="Medicine Info RAG Assistant",
    description="Provides leaflet-based info about medicines. Not medical advice.",
)

# Allow frontend (Streamlit) to call this API easily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev; later you can restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/chat", response_model=AnswerResponse)
async def chat(req: QuestionRequest):
    answer, sources = answer_question(req.question)
    return AnswerResponse(answer=answer, sources=sources)

