# **ITI Info Chatbot (RAG + FAISS + Local Qwen Model)**

A fully local Retrieval-Augmented Generation (RAG) chatbot for answering questions about the ITI website using:

* **Custom Web Scraping**
* **Data Cleaning + Chunking**
* **Sentence-Transformers Embeddings**
* **FAISS Vector Index**
* **Local Qwen2.5-Instruct Model (No paid APIs)**
* **Streamlit Web Interface**

This project runs **100% offline**, and is fully open-source.

---

#  **Project Structure**

```
ITI_CHATBOT/
│
├── data/
│   ├── iti_full_website_data.csv
│   ├── iti_sample_clean.csv
│   ├── iti_chunks_sample.csv
│   ├── iti_metadata.pkl
│   ├── iti_faiss_index.bin
│
├── scraper/
│   ├── 01_scrapper.py
│   ├── 02_cleaner.py
│   ├── 03_chuncker.py
│   ├── 04_embedding.py
│   ├── 05_sematic_search.py
│
├── web/
│   └── st.py
│
├── README.md
└── requirements.txt
```

---

#  **Project Pipeline**

### **1️⃣ Web Scraping**

The scraper starts from a **predefined list of ITI URLs** instead of discovering pages automatically.
This is done because:

* Many ITI pages (tracks, diploma details, programs) are **not reachable** through direct navigation.
* Some pages use **dynamic routing and GUID-based URLs**, which normal crawlers cannot find.
* Using a curated list ensures **complete coverage**, prevents crawling irrelevant sections, and makes results **consistent and reproducible**.
* This keeps scraping fast, predictable, and focused only on educational content.

Output saved to → `data/iti_full_website_data.csv`

---

### **2️⃣ Data Cleaning**

* Removes menus, footers, navigation, repeated sections
* Strips HTML
* Removes noise & special characters
* Saves cleaned text → `data/iti_sample_clean.csv`

---

### **3️⃣ Chunking**

* Uses `RecursiveCharacterTextSplitter`
* Chunk size: 600 chars
* Overlap: 50
* Saves chunks → `data/iti_chunks_sample.csv`

---

### **4️⃣ Embeddings + FAISS Index**

* Embedding model: **all-MiniLM-L6-v2**
* Vector index: **FAISS IndexFlatL2**
* Saves:

  * `iti_metadata.pkl`
  * `iti_faiss_index.bin`

---

### **5️⃣ Retrieval & Generation**

* Retrieves most relevant chunks
* Supports “latest news” priority
* Compresses context for the LLM
* Local generation using **Qwen2.5-1.5B-Instruct**

---

### **6️⃣ Streamlit Web App**

Run with:

```
streamlit run web/st.py
```

Features:
✔ Context retrieval
✔ Qwen-generated answer
✔ Source URLs
✔ Toggle to display retrieved context

---

#  **Installation**

```
pip install -r requirements.txt
```

Recommended packages:

```
streamlit
sentence-transformers
transformers
accelerate
safetensors
faiss-cpu
pandas
numpy
torch
selenium
webdriver-manager
beautifulsoup4
```

GPU users should install CUDA-enabled PyTorch.
CPU-only machines should install standard PyTorch.

---

#  **Running Each Stage**

### Scraper

```
python scraper/01_scrapper.py
```

### Cleaner

```
python scraper/02_cleaner.py
```

### Chunker

```
python scraper/03_chuncker.py
```

### Build Embeddings + FAISS Index

```
python scraper/04_embedding.py
```

### Semantic Search Test

```
python scraper/05_sematic_search.py
```

### Streamlit App

```
streamlit run web/st.py
```

---

#  **Qwen Model Download (First Run Only)**

Downloads automatically:

```
Qwen/Qwen2.5-1.5B-Instruct
```

Size: ~1.5GB
Cached after first download.

---

#  **Example Queries**

* “Tell me about Industrial Automation track”
* “ما هي الشروط للتقديم في Post Graduates؟”
* “آخر أخبار ITI”
* “Track description for Digital IC Design”

---

#  **Notes**

* Works **100% offline** after model download
* No paid APIs used
* Add more links in the scraper to expand dataset
* Metadata + FAISS must match version

---

#  **Future Improvements**

* Add citations (URL + snippet)
* Add streaming responses
* Improve scraper (Requests instead of Selenium)
* Deduplicate pages using canonical URLs
* Add Docker Compose support

---

#  **Contributors**

* **Fatma Asran** — Developer

---

#  **License**

Open-source – free to use for education & research.

---