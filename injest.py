import os
import re
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss

PDF_DIR = "pdfs"
INDEX_FILE = "faiss.index"
CHUNKS_FILE = "chunks.pkl"

model = SentenceTransformer("paraphrase-MiniLM-L3-v2")


# -------- TEXT EXTRACTION --------
def extract_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


# -------- STRUCTURE TEXT --------
def structure_text(raw_text):
    lines = raw_text.splitlines()
    current_unit = "UNKNOWN"
    current_section = "UNKNOWN"
    structured = []

    for line in lines:
        unit_match = re.search(r"UNIT\s+(\d+)", line, re.I)
        section_match = re.search(r"(\d+\.\d+)", line)

        if unit_match:
            current_unit = unit_match.group(1)

        if section_match:
            current_section = section_match.group(1)

        structured.append(
            f"[UNIT {current_unit} | SECTION {current_section}] {line}"
        )

    return "\n".join(structured)


# -------- SECTION-BASED CHUNKING --------
def split_by_section(text):
    return re.split(
        r"\n(?=\[UNIT\s+\d+\s+\|\s+SECTION\s+\d+\.\d+\])",
        text
    )


def chunk_text(text, size=600, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks


# -------- INGEST --------
all_chunks = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        print(f"📄 Processing {file}")
        raw = extract_text(os.path.join(PDF_DIR, file))
        structured = structure_text(raw)
        structured = f"SOURCE: {file}\n{structured}"

        sections = split_by_section(structured)
        for sec in sections:
            all_chunks.extend(chunk_text(sec))

print(f"✂️ Total chunks created: {len(all_chunks)}")

embeddings = model.encode(all_chunks, show_progress_bar=True)
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(CHUNKS_FILE, "wb") as f:
    pickle.dump(all_chunks, f)

print("✅ Ingestion complete")