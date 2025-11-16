import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
# =======================================================
# stage 3: Chunking
# =======================================================

# 1. Load cleaned data
try:
    df = pd.read_csv("data/iti_sample_clean.csv")
    print(f"Clean data loaded successfully. Number of rows: {len(df)}")
except FileNotFoundError:
    print("Error: File iti_sample_clean.csv not found. Make sure it exists.")
    exit()

# 2. Prepare the recursive splitter (Recursive Text Splitter)
# It attempts splitting based on separators in order: paragraphs, newlines, sentences, etc.
text_splitter = RecursiveCharacterTextSplitter(
    # The separators the splitter will try in order
    separators=["\n\n", "\n", ". ", " ", ""], 
    # Maximum chunk size
    chunk_size=600,
    # Overlap between each chunk to maintain context
    chunk_overlap=50,  
    length_function=len
)

# 3. Apply splitting on column 'clean'
all_chunks = []

for index, row in df.iterrows():
    # Split the clean text in column 'clean'
    # Each row is treated as a separate document
    chunks = text_splitter.create_documents([row['clean']])
    
    # Save the resulting chunks
    for chunk in chunks:
        all_chunks.append({
            "url": row["url"],
            "chunk": chunk.page_content, # the split text
            "source_doc_index": index # can be used to trace original document
        })

# 4. Create new dataframe and save it
chunks_df_recursive = pd.DataFrame(all_chunks)

# Save chunks to a new CSV file
chunks_df_recursive.to_csv("data/iti_chunks_sample.csv", index=False)
print("✅ File iti_chunks_sample.csv saved successfully.")
print(f"Total number of generated chunks: {len(chunks_df_recursive)}")

# 5. Show a sample of results
print("\nFirst 5 rows of chunks created using RecursiveCharacterTextSplitter:")
print(chunks_df_recursive.head())
