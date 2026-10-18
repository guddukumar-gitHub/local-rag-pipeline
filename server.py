from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

# 1. Initialize the FastAPI server instance
app = FastAPI(title="Local AI Engineering RAG API")

# 2. Boot up our lightweight AI components safely
print("Loading local embeddings and LLM configuration...")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = ChatOllama(model="llama3.2:1b", temperature=0.1)

# 3. Connect to the existing vector store
# It reads from the local folder directory directly
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

# 4. Define the validation schema for incoming JSON payloads
class QuestionRequest(BaseModel):
    question: str

# 5. Build the API endpoint
@app.post("/api/ask")
async def ask_local_ai(payload: QuestionRequest):
    try:
        user_query = payload.question
        
        # Retrieval: Fetch the best match document block from ChromaDB
        matching_docs = db.similarity_search(user_query, k=1)
        
        if not matching_docs:
            return {"answer": "I couldn't find any relevant context data in my database."}
            
        retrieved_context = matching_docs[0].page_content
        
        # Construct the System Prompt
        system_prompt = f"""
        Task: Answer the question using ONLY the facts found in the Context below.
        Rule: Be extremely direct. Do not say "Based on the context". Do not guess or add outside assumptions.

        Context:
        {retrieved_context}

        Question:
        {user_query}

        Answer:
        """

        
        # Generation: Ask Llama 3.2:1b to process the answer text
        response = llm.invoke(system_prompt)
        
        # Send a clean JSON block back to the caller client
        return {
            "query": user_query,
            "context_used": retrieved_context,
            "answer": response.content
        }
        
    except Exception as e:
        # Graceful error handling
        raise HTTPException(status_code=500, detail=str(e))
