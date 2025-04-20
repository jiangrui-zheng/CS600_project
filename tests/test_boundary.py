import os
import unittest
from indexer import build_index
from search_engine import SearchEngine

class BoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists("index.pkl"):
            build_index()
        cls.engine = SearchEngine("index.pkl")

    def test_empty_query(self):
        self.assertEqual(self.engine.search(""), [])

    def test_stop_word(self):
        self.assertEqual(self.engine.search("the"), [])

    def test_nonexistent_term(self):
        self.assertEqual(self.engine.search("qwertyuiop"), [])

    def test_special_chars(self):
        self.assertEqual(self.engine.search("@#$%^&*"), [])

    def test_and_logic(self):
        with open("Data/0.txt", encoding="utf-8") as fh:
            first_doc_tokens = self.engine.tokenize(fh.read())
        w1, w2 = first_doc_tokens[0], first_doc_tokens[1]
        res = self.engine.search(f"{w1} {w2}")
        self.assertTrue(res)

    def test_repeated_indexing_no_dup(self):
        res1 = self.engine.search("agatha")
        build_index()                         # rebuild once more
        res2 = SearchEngine("index.pkl").search("agatha")
        self.assertEqual(res1, res2)

if __name__ == "__main__":
    unittest.main()
