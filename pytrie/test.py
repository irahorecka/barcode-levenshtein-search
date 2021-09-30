import trie

word = trie.TrieNode()
word.insert("TANNNNCCAGCATTANGCAG")
print(trie.search(word, "TCGGGGCCAGCATTAGGCGG", 10))
