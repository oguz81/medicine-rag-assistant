## ILAÇ ASISTANI-- backend
## Oguz Demirtas

# backend/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .rag_chain import answer_question

app = FastAPI(
    title="İLAÇ ASİSTANI",
    description="Prospektüsten bilgiler verir. Tıbbi nitelik taşımaz",
)

# Frontend, API'yı çağırır
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # daha sonra degistirebilirsin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question: str
    medicine_name_input: str

class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]

@app.post("/chat", response_model=AnswerResponse)
async def chat(req: QuestionRequest):
    answer, sources = answer_question(question=req.question,
                                       medicine_name_input=req.medicine_name_input)
    return AnswerResponse(answer=answer, sources=sources)

