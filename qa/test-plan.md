# System Under Test

This repository is a Flask-based medical chatbot. The browser UI loads `templates/index.html`, which sends user prompts to the `/get` route with a form field named `msg`. `app.py` builds a Pinecone retriever from an existing index named `genai-medical-chatbot`, then either runs a LangChain retrieval-augmented generation chain with Ollama (`llama3`) or falls back to retrieval-only responses when Ollama is unavailable. There is also a separate JSON endpoint at `/chat` that returns `{"response": ...}` but the current UI does not call it.

The indexing script in `store_index.py` loads every PDF in `Data/`, splits them into 500-character chunks with 20-character overlap, embeds them with `sentence-transformers/all-MiniLM-L6-v2`, and writes them into Pinecone. The only data file in `Data/` is a single large source document: `The-Gale-Encyclopedia-of-Medicine-3rd-Edition-staibabussalamsula.ac_.id_.pdf` (4,505 pages). The visible content is an encyclopedia-style medical reference covering broad topics such as diabetes, hypertension, heart disease, obesity, asthma, appendicitis, and many more indexed entries. The UI in `templates/index.html` is a self-contained chat screen with inline CSS/JS, welcome content, quick-action prompts, disabled-input loading states, and a typing indicator; `static/style.css` exists but is not referenced by the current template. `req.txt` pins Flask, LangChain, Pinecone, `python-dotenv`, `pypdf`, `sentence-transformers`, `langchain-community`, `langchain-pinecone`, `langchain_openai`, `langchain_experimental`, and the local editable package install.

Ollama is installed in this environment and `llama3:latest` is available locally, so the LLM-backed path is theoretically runnable once the Pinecone environment/index is configured. Full end-to-end startup still depends on valid `PINECONE_API_KEY` access and a populated Pinecone index.

## Test Objectives

1. Verify the homepage renders the chat UI and quick actions.
2. Verify `/get` accepts form posts and returns a text answer.
3. Verify `/chat` accepts JSON and returns `{"response": ...}`.
4. Verify retrieval uses the medical encyclopedia content, not invented facts.
5. Verify the app degrades cleanly when Ollama or Pinecone access is missing.
6. Verify the indexer chunks and stores the PDF corpus consistently.

## Scope

In scope:

- Flask routes in `app.py`
- Pinecone indexing logic in `store_index.py`
- Medical source corpus in `Data/`
- Chat UI in `templates/index.html`
- Runtime dependencies listed in `req.txt`

Out of scope for this first QA pass:

- Refactoring the app into a different architecture
- Replacing Pinecone with another vector store
- Adding new medical knowledge beyond the PDF corpus

## Test Strategy

Use a mix of smoke tests, negative-path checks, retrieval checks, and UI interaction checks. Prefer actual runtime verification whenever credentials and local models are available. When a path cannot be executed in this environment, record the blocker explicitly instead of assuming behavior.

## Assumptions

- The Pinecone index `genai-medical-chatbot` already exists for runtime retrieval tests.
- `PINECONE_API_KEY` is available when running live application checks.
- The single PDF in `Data/` is the authoritative medical source for retrieval answers.

## Verification Notes

- Ollama CLI is present locally.
- `llama3:latest` is installed locally.
- The PDF corpus is very large, so expected answers should be judged for topical relevance and grounding, not for exact wording.
