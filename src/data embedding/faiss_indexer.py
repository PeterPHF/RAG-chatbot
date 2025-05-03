import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import re

# Load the embeddings and chunks from the file
data = np.load('.../../data/embeddings/gfg_embeddings.npz', allow_pickle=True)
chunk_embeddings = data['embeddings']
chunks = data['chunks']

def create_faiss_index(embeddings):
    dimension = embeddings.shape[1] # e.g., 384 for all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index

# Create FAISS index
faiss_index  = create_faiss_index(chunk_embeddings)
print(f"FAISS index created with {faiss_index.ntotal} vectors.")

# Save index and chunks
faiss.write_index(faiss_index, ".../../data/embeddings/vector_index.faiss")


