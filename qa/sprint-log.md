# Sprint Log

## Sprint Entry 1

Date: 2026-07-18

Completed the initial QA audit of the repository.

Findings captured:

- Flask app exposes `/` for the chat UI, `/get` for form-based responses, and `/chat` for JSON responses.
- The indexer reads a single encyclopedia PDF from `Data/`, chunks it at 500 characters with 20-character overlap, and stores embeddings in Pinecone.
- The UI is fully embedded in `templates/index.html`; `static/style.css` is currently unused.
- Ollama is installed locally and `llama3:latest` is present, but full runtime checks still depend on Pinecone access and a valid index.

Next step:

- Run the live app flow once Pinecone credentials and the index are confirmed, then capture actual answer samples for the eval notes.
