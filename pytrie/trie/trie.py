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

    results = []
    # Recursively search each branch of the trie.
    for letter in trie.children:
        search_recursive(trie.children[letter], letter, word, current_row, results, max_cost)
    if results:
        # Return shortest sequence found within score (sequence @ index 0, score @ index 1)
        return sorted(results, key=lambda x: x[0], reverse=True).pop()[0]
    return None


def search_recursive(node, letter, word, previous_row, results, max_cost):
    """Recursively search through nodes of a Trie object instance. Returns
    found word if the Levenshtein's distance of the last iem in the current
    query row is less than or equal to the maximum cost."""

    def recurse(node, letter, previous_row, results, num_recurse=0):
        """Inner recursive function. Abstracts away constants passed to
        `search_recursive`."""
        num_recurse += 1
        current_row = get_levenshtein_row(letter, word, previous_row)
        # Recursively search each branch of the trie if any entries in the
        # row are less than the maximum cost.
        if min(current_row) <= max_cost:
            for letter in node.children:
                output = recurse(node.children[letter], letter, current_row, results, num_recurse)
                # Optimization for exiting as soon as output found
                if not output:
                    continue
                return output

        # This is useful if the comparator sequence is longer than the reference sequences.
        if current_row[num_recurse] <= max_cost and node.word:
            results.append((node.word, current_row[num_recurse]))
        return results

    # `word` and `max_cost` remain constant - abstract away from inner recursive function.
    return recurse(node, letter, previous_row, results)


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
