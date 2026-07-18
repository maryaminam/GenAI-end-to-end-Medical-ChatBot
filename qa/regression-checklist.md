# Regression Checklist

- [ ] Homepage at `/` renders the chat shell without console errors.
- [ ] Welcome message and quick-action chips are visible on first load.
- [ ] Typing a prompt and pressing Enter sends the message.
- [ ] Clicking a quick-action chip fills and submits the prompt.
- [ ] `/get` returns text and the UI appends the bot reply.
- [ ] Typing indicator appears during the request and disappears afterward.
- [ ] The input and send button are disabled while waiting, then re-enabled.
- [ ] `/chat` still returns JSON with a `response` property.
- [ ] Answers stay grounded in the PDF corpus and do not invent unsupported medical facts.
- [ ] Unsupported questions produce a clear fallback message.
- [ ] App startup still works when Ollama is present and when it is unavailable.
- [ ] Index-building still loads the PDF from `Data/` and uses the current chunking settings.
