# Local RAG API with Ollama

A local retrieval-augmented generation (RAG) demo. It indexes Markdown and
plain-text files from `knowledge_dir` in Chroma, retrieves the closest matching
text for a question, and uses a local Ollama model to generate an answer.

## Requirements

- Python 3.12 or newer
- [Ollama](https://ollama.com/) installed and running

## Setup

Create and activate a virtual environment, then install the project and API
dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt fastapi uvicorn
```

Download the embedding and chat models:

```powershell
ollama pull nomic-embed-text
ollama pull llama3.2:1b
```

Add `.txt` or `.md` files to `knowledge_dir` (subdirectories are searched too),
then build the local vector index:

```powershell
python ingest.py
```

Start the API:

```powershell
python -m uvicorn server:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive API documentation
is available at `http://127.0.0.1:8000/docs`.

## Ask a question

Send a `POST` request to `/api/ask` with a JSON `question`:

```powershell
Invoke-RestMethod -Method Post `
  -Uri http://127.0.0.1:8000/api/ask `
  -ContentType "application/json" `
  -Body '{"question":"What does the company policy say?"}'
```

The response includes the original `query`, the retrieved `context_used`, and
the generated `answer`. The answer is based on the single closest matching
document chunk; if no indexed context is found, the API returns a message
indicating that.

## Project files

- `server.py` — FastAPI application; retrieves context from Chroma and generates answers with Ollama.
- `ingest.py` — reads `.txt` and `.md` files from `knowledge_dir`, splits them into chunks, and stores their embeddings.
- `knowledge_dir/` — source documents to index.
- `requirements.txt` — LangChain, Ollama, and Chroma dependencies.

The first ingestion creates the local `chroma_db` directory. It is generated
data and is excluded from Git. To rebuild the index from scratch, remove
`chroma_db` and run `python ingest.py` again.
