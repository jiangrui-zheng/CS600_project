from search_engine import SearchEngine

engine = SearchEngine("index.pkl")

print("Mini‑Search‑Engine CLI  —  type a query, or 'quit' to exit")
while True:
    q = input("QUERY> ").strip()
    if not q or q.lower() in ("quit", "exit"):
        break
    hits = engine.search(q)
    if not hits:
        print("  No documents matched.\n")
        continue
    for fname, score in hits:
        print(f"  {score:4d}  {fname}")
    print()