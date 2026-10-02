from sentence_transformers import SentenceTransformer
import numpy as np
model = SentenceTransformer("all-MiniLM-L6-v2")
def retrieve_documents(question, chunks, index, top_k=3):
    question_embedding = model.encode([question])
    question_embedding = np.array(question_embedding).astype("float32")
    distances, indices = index.search(question_embedding, top_k)
    results = []
    for i in indices[0]:
        results.append(chunks[i])
    return results    