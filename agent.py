"""AI Customer-Support Agent
Answers customer questions from a small knowledge base (kb.json).
- With ANTHROPIC_API_KEY set: Claude writes the answer using the retrieved FAQ entries.
- Without a key: falls back to the best-matching FAQ answer (works offline).
Every conversation is saved to chats.db (SQLite).
"""
import json, os, re, sqlite3, datetime

KB = json.load(open(os.path.join(os.path.dirname(__file__), "kb.json"), encoding="utf-8"))
DB = os.path.join(os.path.dirname(__file__), "chats.db")
STOP = {"the", "a", "an", "is", "are", "do", "i", "my", "to", "of", "your", "can", "how", "what", "you", "me", "it"}

def words(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP}

def retrieve(question, k=3):
    qw = words(question)
    scored = [(len(qw & words(e["q"] + " " + e["a"])), e) for e in KB]
    scored = [s for s in scored if s[0] > 0]
    return [e for _, e in sorted(scored, key=lambda s: -s[0])[:k]]

def answer(question):
    hits = retrieve(question)
    if not hits:
        return "Sorry, I don't have that information. A human agent will get back to you shortly."
    if os.getenv("ANTHROPIC_API_KEY"):
        import anthropic  # pip install anthropic
        context = "\n".join(f"Q: {e['q']}\nA: {e['a']}" for e in hits)
        msg = anthropic.Anthropic().messages.create(
            model="claude-sonnet-4-6", max_tokens=300,
            system="You are a polite support agent. Answer ONLY using the FAQ context. "
                   "If the answer is not there, say a human will follow up.",
            messages=[{"role": "user", "content": f"FAQ:\n{context}\n\nCustomer: {question}"}])
        return msg.content[0].text
    return hits[0]["a"]

def log(question, reply):
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS chats(ts TEXT, question TEXT, reply TEXT)")
    con.execute("INSERT INTO chats VALUES(?,?,?)", (datetime.datetime.now().isoformat(), question, reply))
    con.commit(); con.close()

if __name__ == "__main__":
    print("Support agent ready. Type 'quit' to exit.")
    while True:
        q = input("You: ").strip()
        if q.lower() in {"quit", "exit"}:
            break
        r = answer(q); log(q, r)
        print("Agent:", r)
