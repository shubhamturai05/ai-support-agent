# AI Customer-Support Agent

A small support chatbot for a business. It finds the most relevant FAQ entries and replies to the customer.
Built with AI-assisted (vibe) coding using Python, SQLite and the Claude API.

## Features
- Retrieves relevant answers from an editable knowledge base (`kb.json`)
- Uses Claude to write natural replies, restricted to the FAQ so it does not make things up
- Works offline without an API key (returns the best FAQ match)
- Logs every conversation to SQLite (`chats.db`)

## Run
```bash
python agent.py                      # offline mode
pip install anthropic
export ANTHROPIC_API_KEY=your_key    # optional: enables Claude replies
python agent.py
```

## Next steps
Swap SQLite for Supabase, connect to WhatsApp/Telegram, add a human-handoff flag.
