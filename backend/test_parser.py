from parser import extract_text_from_pdf, chunk_text

with open("HVN_Annual_Report_2025_FINAL_FOR_RELEASE_290825v2.pdf", "rb") as f:
    text = extract_text_from_pdf(f)
    chunks = chunk_text(text)

print(f"Total characters extracted: {len(text)}")
print(f"Total chunks created: {len(chunks)}")
print(f"\n--- Sample chunk ---\n{chunks[5]}")