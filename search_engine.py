import pickle
import re
from trie import Trie

TOKEN_RE = re.compile(r"[^a-z0-9]+")


def tokenize(query: str):
    return [w for w in TOKEN_RE.sub(" ", query.lower()).split() if w]


class SearchEngine:
    def __init__(self, index_path="index.pkl"):
        with open(index_path, "rb") as f:
            self.trie, self.occ_lists, self.id2name = pickle.load(f)

    @staticmethod
    def _intersect(a, b):
        i = j = 0
        out = []
        while i < len(a) and j < len(b):
            d1, f1 = a[i]
            d2, f2 = b[j]
            if d1 == d2:
                out.append((d1, f1 + f2))   # add frequencies
                i += 1
                j += 1
            elif d1 < d2:
                i += 1
            else:
                j += 1
        return out

    def search(self, query: str, top_k: int = 20):
        tokens = tokenize(query)
        if not tokens:
            return []

        lists = []
        for t in tokens:
            idx = self.trie.search(t)
            if idx is None:
                return []
            lists.append(self.occ_lists[idx])

        result = lists[0]
        for lst in lists[1:]:
            result = self._intersect(result, lst)
            if not result:
                break

        result.sort(key=lambda x: x[1], reverse=True)
        return [(self.id2name[d], score) for d, score in result[:top_k]]
    
    def tokenize(self, text: str):
        return tokenize(text)
