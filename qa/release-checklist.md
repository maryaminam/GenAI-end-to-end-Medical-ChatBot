# Release Checklist

- [ ] Confirm `PINECONE_API_KEY` is set in the target environment.
- [ ] Confirm the Pinecone index `genai-medical-chatbot` exists and is populated.
- [ ] Confirm Ollama is installed if the LLM-backed path is required.
- [ ] Confirm `llama3:latest` is available locally if using offline inference.
- [ ] Run the homepage smoke test and verify the UI loads.
- [ ] Run at least one retrieval question from the encyclopedia corpus.
- [ ] Run one unsupported-query negative test and confirm the fallback text.
- [ ] Verify `/get` and `/chat` both return the documented response formats.
- [ ] Verify the app does not expose unsupported or fabricated medical advice.
- [ ] Review the stale `static/style.css` asset and decide whether to remove or wire it in.
- [ ] Record the runtime result in `qa/sprint-log.md` before shipping.
