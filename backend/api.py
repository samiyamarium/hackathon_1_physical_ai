from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from rag_engine import RAGEngine

app = FastAPI()
engine: RAGEngine | None = None

class Query(BaseModel):
    question: str
    selected_text: str | None = None

# Initialize engine on startup
@app.on_event("startup")
async def startup_event():
    global engine
    loop = asyncio.get_running_loop()
    # Initialize RAGEngine in a thread to avoid blocking
    engine = await loop.run_in_executor(None, RAGEngine)

# POST /ask endpoint
@app.post("/ask")
async def ask(q: Query):
    loop = asyncio.get_running_loop()
    # Run blocking answer() in a threadpool
    answer = await loop.run_in_executor(None, engine.answer, q.question, q.selected_text)
    return {"answer": answer}
