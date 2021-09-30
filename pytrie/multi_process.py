import os
import time

from trie import open_tsv, map_processes, TrieNode, search_concurrent

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")


def make_iterable(item, iterable):
    """Returns iterable of item equal in length to `iterable`."""
    return (item for _ in range(len(iterable)))


if __name__ == "__main__":
    # real.tsv and template.tsv must reside in directory of this py file.
    real_seq = open_tsv(os.path.join(DATA_PATH, "real.tsv"))
    # Slice list to test shorter template sequences. E.g. [:200000]
    template_seq = open_tsv(os.path.join(DATA_PATH, "template.tsv"))[:100000]
    trie = TrieNode()
    for seq in real_seq:
        trie.insert(seq)

    # Make iterables equal in length for mapping to concurrent dispatcher.
    tries = make_iterable(trie, template_seq)
    max_costs = make_iterable(2, template_seq)
    zipped_query = zip(tries, template_seq, max_costs)

    start = time.perf_counter()
    # Concurrently fetch barcode matches.
    mapped_results = map_processes(search_concurrent, zipped_query)

    # Uncomment below to view found results.
    from pprint import pprint

    pprint([result for result in mapped_results if result is not None])
    end = time.perf_counter()
    print(f"Search took {end - start} seconds.")
