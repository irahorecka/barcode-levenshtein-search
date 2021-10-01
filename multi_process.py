from collections import defaultdict
import os
import re
import time

from pytrie.data import open_csv, open_fastq
from pytrie.trie import map_processes, TrieNode, search_concurrent

DATA_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
# Gets that only have nucleotides
SEQUENCE_RE = re.compile("^[actg]*$", re.IGNORECASE)
U1_SEQUENCE = "ATGGATGTCCACGAGGTCTCT"


def search_fastq_barcodes(ref_trie, fastq_seqs):
    """
    Concurrently searches agains reference sequences for barcodes found in
    fastq sequences.

    Args:
        fastq_seqs ([Generator]): [An iterable of fastq sequences]
        ref_seqs ([trie.TrieNode]): [A TrieNode object populated with reference sequences]
    """
    # Ignoring the U1 seq - search up to 1_000_000 sequences
    fastq_seqs = [seq[22:] for idx, seq in enumerate(fastq_seqs) if idx < 2000000]
    # Make iterables equal in length for mapping to concurrent dispatcher.
    ref_tries = make_iterable(ref_trie, fastq_seqs)
    # We are using a max cost value of 2.
    max_costs = make_iterable(2, fastq_seqs)
    zipped_query = zip(ref_tries, fastq_seqs, max_costs)

    start = time.perf_counter()
    # Concurrently fetch barcode matches.
    mapped_results = map_processes(search_concurrent, zipped_query)
    end = time.perf_counter()
    print(f"Search took {end - start} seconds.")

    return [result for result in mapped_results if result is not None]


def pair_barcode_to_gene(ref_dict, barcodes):
    """[summary]

    Args:
        ref_df ([type]): [description]
        barcodes ([type]): [description]
    """
    ref_counter = defaultdict(int)
    for barcode in barcodes:
        ref_counter[ref_dict[barcode]] += 1
    from pprint import pprint

    pprint(dict(ref_counter))


def make_iterable(item, iterable):
    """Returns iterable of item equal in length to `iterable`."""
    return (item for _ in range(len(iterable)))


if __name__ == "__main__":
    fastq_path = os.path.join(DATA_PATH, "D1_1_S1_R1_001.fastq")
    fastq_seqs = open_fastq(fastq_path, lambda x: bool(SEQUENCE_RE.match(x)))
    ref_path = os.path.join(DATA_PATH, "TN_20210930_alternate_barcodes_exhausted.csv")
    ref_genes = open_csv(ref_path)["GeneName"].to_list()
    ref_seqs = open_csv(ref_path)["Sequence"].to_list()
    ref_gene_seq_hash = dict(list(zip(ref_seqs, ref_genes)))

    ref_trie = TrieNode()
    for seq in ref_seqs:
        ref_trie.insert(seq)
    results = search_fastq_barcodes(ref_trie, fastq_seqs)
    pair_barcode_to_gene(ref_gene_seq_hash, results)
