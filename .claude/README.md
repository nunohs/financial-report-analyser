# Financial Report Analyser

A full-stack AI application that lets you upload a company annual report PDF and ask questions about it in plain English — powered by RAG (Retrieval Augmented Generation).

🔗 **[Live Demo](https://financial-report-analyser-theta.vercel.app)** | **[Backend API](https://financial-report-analyser-backend.onrender.com/health)**

> ⚠️ Hosted on Render's free tier — first request may take 30–60 seconds to wake up.

---

## How It Works

1. Upload a company annual report PDF
2. The backend extracts text, chunks it, and builds a FAISS vector index using Gemini embeddings
3. Ask questions in plain English
4. The app retrieves the most relevant chunks and sends them to Gemini to generate a grounded answer
5. Every answer includes expandable source citations so you can verify where the information came from

---

## Features

- 📄 PDF upload with drag and drop
- 🔍 Semantic search via FAISS vector store
- 🤖 AI-generated answers grounded strictly in the document
- 📋 Automatic 5-point report summary on upload
- 💬 Chat interface with conversation history
- 📎 Collapsible source citations per answer
- ⚡ Suggested questions to get started instantly

---

## Tech Stack

**Frontend:** React, TypeScript, Vite, CSS  
**Backend:** Python, FastAPI, pdfplumber, FAISS, NumPy  
**AI:** Google Gemini API (`gemini-embedding-001` for embeddings, `gemini-2.5-flash` for generation)  
**Deployment:** Vercel (frontend), Render (backend)

---

## Architecture

PDF Upload
↓
Text Extraction (pdfplumber)
↓
Chunking (500 words, 50-word overlap)
↓
Embedding (Gemini embedding-001) → FAISS Index
↓
User Question → Embed Query → Retrieve Top 4 Chunks
↓
Gemini 2.5 Flash → Grounded Answer + Sources

---

## Running Locally

**Backend:**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
# Add GEMINI_API_KEY to .env
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
# Add VITE_API_URL=http://localhost:8000 to .env
npm run dev
```

---

## Example Questions

- "What were the main revenue drivers this year?"
- "What risks did management highlight?"
- "How did net profit change year on year?"
- "Summarise the CEO letter"
- "What are the company's growth plans?"