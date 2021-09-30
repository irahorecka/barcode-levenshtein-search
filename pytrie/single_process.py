import os
import time

from trie import open_tsv, TrieNode, search

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


if __name__ == "__main__":
    # real.tsv and template.tsv must reside in directory of this py file.
    real_seq = open_tsv(os.path.join(DATA_PATH, "real.tsv"))
    # Slice list to test shorter template sequences. E.g. [:200000]
    template_seq = open_tsv(os.path.join(DATA_PATH, "template.tsv"))[:]
    trie = TrieNode()
    for seq in real_seq:
        trie.insert(seq)

    start = time.perf_counter()
    results = [search(trie, seq, max_cost=2) for seq in template_seq]

    # Uncomment below to view found results.
    # print([result for result in results if result is not None])
    end = time.perf_counter()
    print(f"Search took {end - start} seconds.")
