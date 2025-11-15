# ITI Info Chatbot — Full Streamlit app (RAG + FAISS + Qwen2.5-Instruct local)
# ---------------------------------------------------------------------------
# Usage:
# 1) Put `iti_metadata.pkl` and `iti_faiss_index.bin` in the data folder.
# 2) Install requirements (see below).
# 3) Run: streamlit run ITI_RAG_Qwen_Streamlit.py
#
# Requirements (recommended):
# pip install streamlit sentence-transformers transformers accelerate safetensors faiss-cpu pandas numpy torch
# If you have CUDA GPU, install torch with the right CUDA version.

import streamlit as st
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import re

# -------------------------------------------------------
# Page config
# -------------------------------------------------------
st.set_page_config(page_title="ITI Info Chatbot (Qwen)", layout="wide")
st.title("🎓 ITI Info Chatbot — (Open-Source Qwen2.5)")

# -------------------------------------------------------
# Helper: cached resource loaders
# -------------------------------------------------------
@st.cache_resource
def load_rag_components(metadata_path: str = "data/iti_metadata.pkl", faiss_path: str = "data/iti_faiss_index.bin"):
    """Load embedding model, metadata dataframe and faiss index."""
    embed_model = SentenceTransformer('all-MiniLM-L6-v2')
    df = pd.read_pickle(metadata_path)
    index = faiss.read_index(faiss_path)
    return embed_model, index, df

@st.cache_resource
def load_qwen_model(model_name: str = "Qwen/Qwen2.5-1.5B-Instruct"):
    """Load Qwen tokenizer + model. Use CPU if no GPU is available."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        low_cpu_mem_usage=True
    )

    if device == "cpu":
        model.to("cpu")

    model.eval()
    return tokenizer, model, device

# -------------------------------------------------------
# Load components
# -------------------------------------------------------
with st.spinner("Loading components (this may take a few seconds)..."):
    try:
        MODEL_EMBED, FAISS_INDEX, METADATA_DF = load_rag_components()
        TOKENIZER, QWEN_MODEL, QWEN_DEVICE = load_qwen_model()
        st.success("✅ All chatbot components loaded successfully.")
    except Exception as e:
        st.error(f"❌ Error loading components: {e}")
        st.stop()

# -------------------------------------------------------
# Retrieval function
# -------------------------------------------------------
def retrieve_context(query: str, top_k: int = 2, max_context_chars: int = 450):
    query_embedding = MODEL_EMBED.encode(query, convert_to_numpy=True).reshape(1, -1)
    distances, indices = FAISS_INDEX.search(query_embedding, 20)
    candidate_rows = METADATA_DF.iloc[indices[0]].copy()
    candidate_rows['distance'] = distances[0]

    news_keywords = ["news", "latest", "new", "update", "أخبار", "جديد", "أحدث"]
    is_news_query = any(kw in query.lower() for kw in news_keywords)

    if is_news_query:
        candidate_rows['is_news'] = candidate_rows['chunk'].apply(
            lambda x: 1 if any(kw in str(x).lower() for kw in news_keywords) else 0
        )
        final = candidate_rows.sort_values(by=['is_news', 'distance'], ascending=[False, True]).head(top_k)
    else:
        final = candidate_rows.sort_values(by='distance', ascending=True).head(top_k)

    context_text = " ".join(final['chunk'].tolist())
    if len(context_text) > max_context_chars:
        context_text = context_text[:max_context_chars] + "..."

    source_url = None
    if 'url' in final.columns:
        ulist = list(final['url'].dropna().unique())
        source_url = ulist[0] if len(ulist) > 0 else ""

    return context_text.strip(), source_url or ""

# -------------------------------------------------------
# Generation using Qwen model
# -------------------------------------------------------

def clean_generated_text(text: str, prompt_tail: str = "\n\n") -> str:
    if "الإجابة:" in text:   # original Arabic marker
        text = text.split("الإجابة:", 1)[-1]
    if "Answer:" in text:
        text = text.split("Answer:", 1)[-1]

    text = text.replace(prompt_tail, " ").strip()

    for sep in ["?", ".", "!", "\n"]:
        if sep in text:
            parts = text.split(sep)
            candidate = parts[0].strip()
            if len(candidate) > 2:
                return candidate + sep
    return text


def generate_final_answer(context: str, query: str, max_new_tokens: int = 200):
    if not context.strip():
        return "Sorry, no information is available for this question."

    prompt = f"""
You are an intelligent assistant specialized in ITI information.
Answer ONLY using the information provided in the (context).
If the information is not available, say: "Information not available."

Context:
{context}

Question:
{query}

Answer:
""".strip()

    inputs = TOKENIZER(prompt, return_tensors="pt")

    if QWEN_DEVICE == 'cuda' and torch.cuda.is_available():
        inputs = {k: v.to('cuda') for k, v in inputs.items()}
    else:
        inputs = {k: v.to('cpu') for k, v in inputs.items()}

    with torch.no_grad():
        outputs = QWEN_MODEL.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            eos_token_id=TOKENIZER.eos_token_id,
            pad_token_id=TOKENIZER.pad_token_id,
            repetition_penalty=1.1
        )

    decoded = TOKENIZER.decode(outputs[0], skip_special_tokens=True)
    answer = clean_generated_text(decoded, prompt_tail=prompt)

    if len(answer) > 400:
        answer = answer[:400].rsplit(' ', 1)[0] + '...'
    return answer.strip()

# -------------------------------------------------------
# Streamlit UI
# -------------------------------------------------------
st.markdown("---")
col1, col2 = st.columns([3, 1])
with col1:
    user_query = st.text_input("Ask me about ITI:")
with col2:
    show_ctx = st.checkbox("Show retrieved context", value=False)

if user_query:
    with st.spinner("Searching, retrieving context, and generating..."):
        ctx, src = retrieve_context(user_query, top_k=2)
        answer = generate_final_answer(ctx, user_query)

    st.subheader("💬 Final Answer:")
    st.success(answer)

    if show_ctx:
        st.subheader("📚 Retrieved Context:")
        st.code(ctx)

    st.subheader("🔗 Source:")
    if src:
        st.markdown(f"[Click here to visit source]({src})")
    else:
        st.write("No source link available in the retrieved data.")

# Footer
st.markdown("---")
st.markdown(
    "**Installation Note:** To run the app locally use: `pip install streamlit sentence-transformers transformers accelerate safetensors faiss-cpu pandas numpy torch`  \n\n"
    "If your device supports GPU, install the correct torch version for faster generation."
)
