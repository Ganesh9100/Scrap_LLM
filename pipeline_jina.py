from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from sentence_transformers import SentenceTransformer
import numpy as np
import os

# Mapping
url_to_file = {
    "url1": "path/to/file1.txt",
    "url2": "path/to/file2.txt",
}

# Step 1: Create initial URL retrieval index
url_texts = []
urls = []
for url, file_path in url_to_file.items():
    with open(file_path, 'r') as f:
        content = f.read(500)  # First 500 characters as summary
    url_texts.append(content)
    urls.append(url)

# Embed summaries
model = SentenceTransformer('all-MiniLM-L6-v2')
url_embeddings = model.encode(url_texts)

def find_best_url(query):
    query_emb = model.encode([query])[0]
    scores = np.dot(url_embeddings, query_emb)
    best_idx = int(np.argmax(scores))
    return urls[best_idx]

# Step 2: Load & chunk
def get_relevant_chunks(file_path, query):
    with open(file_path, 'r') as f:
        full_text = f.read()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([full_text])

    # Embed and create in-memory FAISS
    faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings())
    relevant_docs = faiss_index.similarity_search(query, k=3)

    return "\n".join([doc.page_content for doc in relevant_docs])

# Main pipeline
def rag_pipeline(query):
    best_url = find_best_url(query)
    file_path = url_to_file[best_url]
    context = get_relevant_chunks(file_path, query)

    final_prompt = f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    # Send to LLM of your choice here
    print(f"Answering using: {best_url}\n")
    print(final_prompt)

# Example
rag_pipeline("What is tablet unlimited plan?")



# 5. Function to embed using sentence-transformer in Langchain-compatible format
class SentenceTransformerEmbeddings:
    def __init__(self, model):
        self.model = model

    def embed_documents(self, texts):
        return self.model.encode(texts).tolist()

    def embed_query(self, text):
        return self.model.encode([text])[0].tolist()

embedding_wrapper = SentenceTransformerEmbeddings(embedding_model)
