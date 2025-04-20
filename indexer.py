"""
Scan Data/*.txt, build global inverted index
(trie, occurrence_lists, id2name) -> index.pkl
"""

import os
import re
import pickle
from collections import Counter
from nltk.corpus import stopwords
from trie import Trie

TOKEN_RE = re.compile(r"[^a-z0-9]+")
STOP = set(stopwords.words("english"))
DATA_DIR = "Data"


def tokenize(text: str):
    words = TOKEN_RE.sub(" ", text.lower()).split()
    return [w for w in words if w and w not in STOP]


def build_index(doc_dir=DATA_DIR, out_file="index.pkl"):
    trie = Trie()
    occ_lists = []              # list[dict{docID:freq}]
    id2name = []                # filename list

    for doc_id, fname in enumerate(sorted(os.listdir(doc_dir))):
        id2name.append(fname)
        path = os.path.join(doc_dir, fname)
        with open(path, encoding="utf-8") as fh:
            tokens = tokenize(fh.read())
        freq = Counter(tokens)

        # insert every token
        for w, f in freq.items():
            idx = trie.search(w)
            if idx is None:
                idx = len(occ_lists)
                trie.insert(w, idx)
                occ_lists.append({})
            occ_lists[idx][doc_id] = f

    # store as sorted list for efficient merging
    occ_lists = [sorted(d.items()) for d in occ_lists]

    with open(out_file, "wb") as f:
        pickle.dump((trie, occ_lists, id2name), f)
    print(f"[+] Indexed {len(id2name)} docs -> {out_file}")


if __name__ == "__main__":
    build_index()
