import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from hashlib import md5

model = SentenceTransformer("all-MiniLM-L6-v2")
EMBEDDING_CACHE_DIR = "cache/embeddings"

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def store_embeddings(text, video_id):
    os.makedirs(EMBEDDING_CACHE_DIR, exist_ok=True)
    embed_path = os.path.join(EMBEDDING_CACHE_DIR, f"{video_id}.json")

    if os.path.exists(embed_path):
        return  # already stored

    chunks = chunk_text(text)
    embeddings = model.encode(chunks).tolist()

    with open(embed_path, "w") as f:
        json.dump({"chunks": chunks, "embeddings": embeddings}, f)

def query_embeddings(question, video_id, top_k=3):
    embed_path = os.path.join(EMBEDDING_CACHE_DIR, f"{video_id}.json")
    with open(embed_path, "r") as f:
        data = json.load(f)

    question_embedding = model.encode([question])[0]
    index = faiss.IndexFlatL2(len(question_embedding))
    index.add(np.array(data["embeddings"]))
    D, I = index.search(np.array([question_embedding]), top_k)

    return " ".join([data["chunks"][i] for i in I[0]])
