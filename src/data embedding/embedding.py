from sentence_transformers import SentenceTransformer
import numpy as np

# Load text chunks
def load_chunks(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        raw = f.read()
    chunks = [chunk.strip() for chunk in raw.split("\n\n") if chunk.strip()]
    return chunks

# Embed and save
def embed_and_save(input_txt='gfg_chunks.txt', output_npz='gfg_embeddings.npz'):
    print(" Loading model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("📖 Loading chunks...")
    chunks = load_chunks(input_txt)
    print(f" Total chunks: {len(chunks)}")

    print(" Embedding...")
    embeddings = model.encode(chunks, show_progress_bar=True)

    # Save to compressed .npz file
    np.savez_compressed(output_npz, embeddings=embeddings, chunks=chunks)
    print(f" Embeddings saved as {output_npz}")

# Run
embed_and_save(input_txt='../../data/processed/gfg_chunks.txt', output_npz='../../data/embeddings/gfg_embeddings.npz')