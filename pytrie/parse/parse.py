import pytrie.trie.trie as trie


def match_prefix_seq(trie_objet, word):
    if bool(trie.search(trie_objet, word, max_cost=2)):
        return len(word)
    return False
