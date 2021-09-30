class TrieNode:
    """The Trie data structure keeps a set of words, organized with one node for
    each letter. Each node has a branch for each letter that may follow it in the
    set of words (in our case, a string of nucleotides)."""

    def __init__(self):
        self.word = None
        self.children = {}

    def insert(self, word):
        """Builds trie data structure via insertion of characters only if character
        does not exist in children node."""
        # `self` can be thought of as a node.
        for letter in word:
            if letter not in self.children:
                self.children[letter] = TrieNode()
            # Traverse one node down.
            self = self.children[letter]

        self.word = word


def search_concurrent(zipped_args):
    """Dispatch function that maps `zipped_args` to `search`."""
    return search(*zipped_args)


def search(trie, word, max_cost=1):
    """Returns a list of all words that are less than the given maximum distance from
    the target word."""
    # Build first row of Levenshtein's distance matrix.
    current_row = range(len(word) + 1)

    # Recursively search each branch of the trie.
    for letter in trie.children:
        results = search_recursive(trie.children[letter], letter, word, current_row, max_cost)
        # If valid results are found, return results.
        if results:
            return results
    return None


def search_recursive(node, letter, word, previous_row, max_cost):
    """Recursively search through nodes of a Trie object instance. Returns
    found word if the Levenshtein's distance of the last iem in the current
    query row is less than or equal to the maximum cost."""

    def recurse(node, letter, previous_row, results):
        """Inner recursive function. Abstracts away constants passed to
        `search_recursive`."""
        current_row = get_levenshtein_row(letter, word, previous_row)
        if node.word is not None and current_row[-1] <= max_cost:
            # Found a match.
            return tuple((word, node.word, current_row[-1]))

        # Recursively search each branch of the trie if any entries in the
        # row are less than the maximum cost.
        if min(current_row) <= max_cost:
            for letter in node.children:
                return recurse(node.children[letter], letter, current_row, results)
        return None

    # `word` and `max_cost` remain constant - abstract away from inner recursive function.
    return recurse(node, letter, previous_row, list())


def get_levenshtein_row(letter, word, previous_row):
    """Gets subsequent Levenshtein's row given query letter, template word,
    and previous Levenshtein's row value."""
    columns = len(word) + 1
    current_row = [previous_row[0] + 1]

    # Build one row for the letter, with a column for each letter in the target
    # word, plus one for the empty string at column 0.
    for column in range(1, columns):
        insertion_cost = current_row[column - 1] + 1
        deletion_cost = previous_row[column] + 1
        if letter in (word[column - 1], "N"):
            replacement_cost = previous_row[column - 1]
        else:
            replacement_cost = previous_row[column - 1] + 1
        current_row.append(min(insertion_cost, deletion_cost, replacement_cost))

    return current_row
