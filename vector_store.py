import numpy as np
import os
import pickle

model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")
    return model
    
INDEX_FILE = "faiss_index.bin"
DATA_FILE = "metadata.pkl"

def get_embedding(text):
    model = get_model()
    return model.encode([text])[0]
    
def load_index():
    import faiss
    if os.path.exists(INDEX_FILE):
        index = faiss.read_index(INDEX_FILE)
        with open(DATA_FILE, "rb") as f:
            metadata = pickle.load(f)
    else:
        index = faiss.IndexFlatL2(384)  # embedding size
        metadata = []
    return index, metadata
    
def add_to_vector_store(text, extra_data):
    import faiss
    index, metadata = load_index()

    embedding = get_embedding(text).astype("float32")
    index.add(np.array([embedding]))

    metadata.append({
        "text": text,
        "data": extra_data
    })

    faiss.write_index(index, INDEX_FILE)
    with open(DATA_FILE, "wb") as f:
        pickle.dump(metadata, f)
        
def search_vector_store(query, k=3):
    index, metadata = load_index()

    query_embedding = get_embedding(query).astype("float32")

    distances, indices = index.search(np.array([query_embedding]), k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            results.append(metadata[idx])

    return results