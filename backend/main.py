from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io

import os

from parser import extract_text_from_pdf, chunk_text
from vectorstore import build_vectorstore, retrieve_relevant_chunks, save_vectorstore, load_vectorstore
from llm import generate_answer, generate_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage
session = {
    "index": None,
    "chunks": None,
    "summary": None
}

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    # Load from disk if already embedded, otherwise parse + build + save.
    # Skips PDF parsing entirely on the cached path so re-uploads stay fast.
    if os.path.exists("vectorstore.faiss"):
        print("Loading existing vector store...")
        index, chunks = load_vectorstore()
    else:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)

        text = extract_text_from_pdf(pdf_file)
        if not text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from this PDF.")

        chunks = chunk_text(text, chunk_size=1000, overlap=100)

        print("Building vector store from scratch...")
        index, chunks = build_vectorstore(chunks)
        save_vectorstore(index, chunks)

    session["index"] = index
    session["chunks"] = chunks

    # Generate summary with retry
    session["summary"] = generate_summary(chunks)

    return {"status": "ready", "chunk_count": len(chunks)}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    if session["index"] is None:
        raise HTTPException(status_code=400, detail="No report uploaded yet.")

    relevant_chunks = retrieve_relevant_chunks(
        request.question,
        session["index"],
        session["chunks"]
    )

    answer = generate_answer(request.question, relevant_chunks)

    return {
        "answer": answer,
        "sources": relevant_chunks
    }

@app.get("/summary")
def get_summary():
    if session["summary"] is None:
        raise HTTPException(status_code=400, detail="No report uploaded yet.")

    return {"summary": session["summary"]}