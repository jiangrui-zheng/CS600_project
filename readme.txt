-----------------------------------------------
Files & Folders
-----------------------------------------------
crawler.py ─ download pages in urls.txt → Raw/.html + Data/.txt
indexer.py ─ build <trie, occ_lists> inverted index → index.pkl
search_engine.py ─ CLI search tool (AND + term‑frequency ranking)
main.py ─ entry point for interactive CLI
tests/ ─ six boundary‑condition unit‑tests
urls.txt ─ 6 inter‑linked Wikipedia pages (AI / ML / DL …)
Data/, Raw/ ─ generated at run–time

-----------------------------------------------
Algorithms & Data Structures
-----------------------------------------------
Compressed trie (Section 23.6)
• external nodes store an occurrence‑list ID
Occurrence list — map {docID → term‑frequency}, pre‑sorted by docID
Query evaluation — merge‑intersect lists; sum frequencies as score
Stop‑word filter — NLTK English stop‑list removed at indexing time

-----------------------------------------------
Quick Start
-----------------------------------------------
pip install -r requirements.txt

Download pages & build corpus:
python crawler.py

Build inverted index:
python indexer.py

Interactive search:
python main.py (type a query or ‘quit’)

Run boundary‑condition tests:
python -m unittest discover tests

-----------------------------------------------
Input / Output Samples
-----------------------------------------------
Raw/0.html — full HTML with hyperlinks
Data/0.txt — plain text extracted from same page

-----------------------------------------------
Boundary‑Condition Coverage
-----------------------------------------------
empty_query → "" returns []
stop_words → "the" returns []
nonexistent_term → random token returns []
special_characters → "@#$%" returns []
and_logic → two tokens both in doc0 → non‑empty
repeated_indexing → rebuild index twice yields identical results
