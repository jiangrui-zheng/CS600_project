class TrieNode:
    __slots__ = ("children", "idx")

    def __init__(self):
        self.children = {}
        self.idx = None               # index into occurrence_lists


class Trie:
    """Compressed-trie storing only index of occurrence list in leaf."""
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, idx: int):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.idx = idx

    def search(self, word: str):
        node = self.root
        for ch in word:
            node = node.children.get(ch)
            if node is None:
                return None
        return node.idx
