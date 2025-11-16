#embedding  # ✅ Stage 4:
import pandas as pd
import numpy as np
import faiss # to use fast search index
from sentence_transformers import SentenceTransformer
import torch
# =======================================================
# ✅ Stage 4: Embeddings and Indexing (Modified)
# =======================================================

# 1. Load the split data (Chunks)
try:
    chunks_df = pd.read_csv("data/iti_chunks_sample.csv")
    print(f"Loaded {len(chunks_df)} data chunks.")
except FileNotFoundError:
    print("Error: File iti_chunks_sample.csv not found.")
    exit()

# 2. Load the model
# Note: This model requires PyTorch and sentence-transformers
MODEL_NAME = 'all-MiniLM-L6-v2'
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SentenceTransformer(MODEL_NAME, device=device)
print(f"✅ Embedding model loaded: {MODEL_NAME}")

# 3. Create embeddings
print("Starting embedding creation... (may take some time)")

# Embeddings are created in batches for faster and more efficient processing
chunks_list = chunks_df["chunk"].tolist()
# embeddings = model.encode(chunks_list, convert_to_numpy=True)
embeddings = model.encode(
    chunks_list,
    convert_to_numpy=True,
    batch_size=64,
    device=device,
    normalize_embeddings=True
)
# CUDA

print(f"✅ Successfully created {len(embeddings)} embeddings.")

# 4. Build FAISS index (Vector Indexing)
# FAISS is an open-source library for fast similarity search
embedding_dim = embeddings.shape[1] # usually 384 for this model
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)
print("✅ FAISS index (Vector Index) built successfully.")

# 5. Save the index and metadata
# Save the text metadata as pickle
chunks_df.to_pickle("data/iti_metadata.pkl") 
# Save fast search index as .bin
faiss.write_index(index, "data/iti_faiss_index.bin") 

print("\n--- Stage 4 Results ---")
print("✅ Saved iti_metadata.pkl (original texts)")
print("✅ Saved iti_faiss_index.bin (fast search index)")
