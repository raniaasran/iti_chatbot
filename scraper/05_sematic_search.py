# # ✅ Stage 5: Semantic Search

import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import torch
# =======================================================
# ✅ Stage 5: RAG Retrieval
# =======================================================

# 1. Load components (loaded once for speed)
@st.cache_resource
def load_rag_components():
    """Load model, index, and metadata."""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # A. Load the embedding model
        # model = SentenceTransformer('all-MiniLM-L6-v2')
        model = SentenceTransformer('all-MiniLM-L6-v2', device=device) # CUDA
        
        # B. Load metadata (texts and URLs)
        df_metadata = pd.read_pickle("data/iti_metadata.pkl")
        
        # C. Load FAISS index
        index = faiss.read_index("data/iti_faiss_index.bin")
        
        return model, index, df_metadata
    except FileNotFoundError as e:
        st.error(f"Error: RAG files not found. Please make sure to run the 'Embed & Indexing' stages first. Error: {e}")
        return None, None, None

# Load components
MODEL, FAISS_INDEX, METADATA_DF = load_rag_components()

# 2. Modified retrieval function
def retrieve_context(query: str, top_k: int = 5) -> list:
    """
    Retrieves the most relevant texts from the FAISS index,
    with priority logic for news-related queries.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # Convert query to embedding
    #query_embedding = MODEL.encode(query, convert_to_numpy=True)
    query_embedding = MODEL.encode(
        query,
        convert_to_numpy=True,
        device=device,
        batch_size=32
    ) # CUDA

    query_embedding = query_embedding.reshape(1, -1)  # match FAISS input shape
    
    # Search FAISS for nearest neighbors (up to top 20 for filtering)
    distances, indices = FAISS_INDEX.search(query_embedding, 20)
    
    # Extract corresponding metadata
    initial_results = METADATA_DF.iloc[indices[0]].copy()
    initial_results['distance'] = distances[0]
    
    # 3. Logic for handling 'latest news' priority
    news_keywords = ["news", "latest", "جديد", "أحدث", "أخبار"]
    query_lower = query.lower()
    
    # Check if query is news-related
    is_news_query = any(kw in query_lower for kw in news_keywords)
    
    if is_news_query:
        # Give extra score to chunks containing news keywords
        initial_results['is_news'] = initial_results['chunk'].apply(
            lambda x: 1 if any(kw in x.lower() for kw in news_keywords) else 0
        )
        
        # Sort by 'is_news' first then by distance
        initial_results.sort_values(
            by=['is_news', 'distance'], 
            ascending=[False, True],
            inplace=True
        )
        
        # Pick top_k after filtering
        final_context = initial_results.head(top_k)
    else:
        # Default: sort only by distance (semantic similarity)
        final_context = initial_results.sort_values('distance', ascending=True).head(top_k)
        
    # Build final context and URLs
    context_text = " ".join(final_context['chunk'].tolist())
    source_urls = list(final_context['url'].unique())
    
    # Return text context and sources
    return context_text, source_urls


# 4. Generation function (for testing)
# In a real Streamlit app, 'context' is fed into the LLM for answer generation
def generate_answer(context, query):
    # Here we'd call the LLM (e.g., Ollama or Hugging Face)
    # For testing, we display the retrieved context.
    st.write("--- Retrieved context for LLM (for generation) ---")
    st.write(context)
    st.write(f"Sources: {sources}")
    # return LLM_RESPONSE

# =======================================================
# 💡 You can now integrate this logic into your Streamlit app.
# =======================================================

# Example inside Streamlit UI (for demonstration):
if MODEL is not None:
    user_query = st.text_input("Ask me about ITI:")
    if user_query:
        context, sources = retrieve_context(user_query)
        generate_answer(context, user_query)  # LLM is called here in real scenario