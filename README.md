# Ollama semantic search demo

A small Python example that embeds sample documents with Ollama's
`nomic-embed-text` model, stores them locally in Chroma, and searches for the
most relevant document.

## Requirements

- Python 3.12 or newer
- [Ollama](https://ollama.com/) installed and running

## Setup

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Download the embedding model:

```powershell
ollama pull nomic-embed-text
```

To index `.txt` and `.md` files in `knowledge_dir`, run:

```powershell
python ingest.py
```

Run the demo:

```powershell
python app.py
```

The first run creates a local `chroma_db` directory. It is generated data and
is excluded from Git; remove that directory to rebuild the index from scratch.

## Project files

- `app.py` — sample documents, embedding setup, and semantic search.
- `ingest.py` — indexes text and Markdown files from `knowledge_dir`.
- `requirements.txt` — pinned direct Python dependencies.
