# Bug Log

| ID | Status | Observation | Impact | Notes |
|---|---|---|---|---|
| BUG-001 | Open risk | `app.py` initializes embeddings and Pinecone access at import time. If `PINECONE_API_KEY` or the index is missing, the app may fail before serving any route. | High | Verify startup in the target environment before release. |
| BUG-002 | Open risk | The template uses only inline CSS/JS; `static/style.css` is present but not referenced by the current UI. | Low | Not a functional bug, but a stale asset risk. |
| BUG-003 | Open risk | `/chat` exists as a JSON API, but the current UI only uses `/get`. | Medium | Confirm whether `/chat` is intentionally public or legacy. |
| BUG-004 | Open risk | The knowledge base is a single encyclopedia PDF with 4,505 pages, so answers should be judged for topical grounding rather than exact phrasing. | Medium | Evaluation must allow for retrieval variability. |
| BUG-005 | Open risk | The app falls back to retrieval-only responses when Ollama is unavailable, but this branch still depends on Pinecone. | Medium | Verify degraded mode with real runtime conditions. |
