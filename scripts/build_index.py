import os
import sys

# src folder-ai Python path-la add panrom
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.load_document import load_pdf
from src.chunk_text import split_text
from src.embeddings import create_vectorstore


# PDF location
pdf_path = "data/college_handbook.pdf"

# Vector store location
store_path = "store"


print("Loading PDF...")

# 1. PDF-la irundhu text extract
text = load_pdf(pdf_path)

print("PDF loaded successfully!")

# 2. Text-ai chunks-ah split pannum
chunks = split_text(text)

print(f"Total chunks created: {len(chunks)}")

# 3. Chunks-ku embeddings create panni
#    FAISS vector database-la save pannum
create_vectorstore(chunks)

print("Vector store created successfully!")
print(f"Saved in: {store_path}")