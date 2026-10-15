from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_core.documents import Document

# 1. Initialize your tiny local embedding model cleanly
print("Initializing embedding model...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# 2. Prepare sample data (Simulating your database documents)
documents = [
    Document(page_content="Express.js is a minimal backend framework for Node.js.", metadata={"source": "mern"}),
    Document(page_content="Python uses virtual environments (venv) to manage packages.", metadata={"source": "python"}),
    Document(page_content="Vector databases store data as math arrays to search by meaning.", metadata={"source": "ai"})
]

# 3. Create a local vector store (Saved right into a local folder)
print("Creating local vector index...")
db = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")

# 4. Search the data semantically (by meaning, not exact words)
query = "How do I handle dependencies in Python?"
print(f"\nSearching for: '{query}'")

# Fetch the top matching document
docs = db.similarity_search(query, k=1)

print("\n--- Best Match Found ---")
if docs:
    print(docs[0].page_content)
    print(f"Source metadata: {docs[0].metadata}")
else:
    print("No matching documents found.")
