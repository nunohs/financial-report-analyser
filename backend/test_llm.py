import os
from vectorstore import build_vectorstore, retrieve_relevant_chunks, save_vectorstore, load_vectorstore
from parser import extract_text_from_pdf, chunk_text
from llm import generate_answer

# Only rebuild if vectorstore doesn't exist yet
if os.path.exists("vectorstore.faiss"):
    print("Loading existing vector store...")
    index, chunks = load_vectorstore()
else:
    print("Building vector store from scratch...")
    with open("HVN_Annual_Report_2025_FINAL_FOR_RELEASE_290825v2.pdf", "rb") as f:
        text = extract_text_from_pdf(f)
    chunks = chunk_text(text, chunk_size=1000, overlap=100)
    index, chunks = build_vectorstore(chunks)
    save_vectorstore(index, chunks)

question = "What risks did management highlight?"
relevant = retrieve_relevant_chunks(question, index, chunks)
answer = generate_answer(question, relevant)

print(answer)