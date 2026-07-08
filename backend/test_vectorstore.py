import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from parser import extract_text_from_pdf, chunk_text
from vectorstore import build_vectorstore, retrieve_relevant_chunks

with open("HVN_Annual_Report_2025_FINAL_FOR_RELEASE_290825v2.pdf", "rb") as f:
    text = extract_text_from_pdf(f)

chunks = chunk_text(text)
index, chunks = build_vectorstore(chunks)

results = retrieve_relevant_chunks("what were the main risks?", index, chunks)
for i, chunk in enumerate(results):
    print(f"\n--- Chunk {i+1} ---\n{chunk}")