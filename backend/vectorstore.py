import faiss
import time
import numpy as np
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def embed_text(text: str) -> list[float]:
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = client.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text,
            )
            return result.embeddings[0].values
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 5 * (attempt + 1)  # 5s, 10s, 15s
                print(f"  Embedding failed ({e}), retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise

def build_vectorstore(chunks: list[str]) -> tuple:
    print(f"Embedding {len(chunks)} chunks...")
    embeddings = []
    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        embeddings.append(embedding)
        time.sleep(2)  # 2 second pause between calls
        if (i + 1) % 10 == 0:
            print(f"  Embedded {i + 1}/{len(chunks)} chunks...")

    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)

    vectors = np.array(embeddings, dtype="float32")
    index.add(vectors)

    print("Vector store built successfully.")
    return index, chunks

def retrieve_relevant_chunks(query: str, index, chunks: list[str], k: int = 4) -> list[str]:
    query_embedding = embed_text(query)

    query_vector = np.array([query_embedding], dtype="float32")
    distances, indices = index.search(query_vector, k)

    return [chunks[i] for i in indices[0]]

def save_vectorstore(index, chunks: list[str], path: str = "vectorstore"):
    faiss.write_index(index, f"{path}.faiss")
    with open(f"{path}.chunks", "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk + "\n<CHUNK_END>\n")

def load_vectorstore(path: str = "vectorstore") -> tuple:
    index = faiss.read_index(f"{path}.faiss")
    with open(f"{path}.chunks", "r", encoding="utf-8") as f:
        content = f.read()
    chunks = [c.strip() for c in content.split("<CHUNK_END>") if c.strip()]
    return index, chunks