import os

import pandas as pd

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def open_csv(filepath, header_names=None):
    """Opens CSV file with option to add header names."""
    if header_names and hasattr(header_names, "__iter__"):
        return pd.read_csv(filepath, sep=",", header=0, names=header_names)
    return pd.read_csv(filepath, sep=",", header=0)


def get_str_pattern_from_pddf(csv_df, colname, str_patterns, contains=True):
    """Gets dataframe where there are string pattern(s) in colname."""
    if isinstance(str_patterns, (tuple, list)):
        str_patterns = "|".join(str_patterns)
    if contains:
        return csv_df[csv_df[colname].str.contains(str_patterns)]
    return csv_df[~csv_df[colname].str.contains(str_patterns)]


def recursively_swap_char(char_iter, search_char, replace_char):
    """
    IN: ['YFG1', 'AGGCG--TTC']
    OUT: (['YFG1', 'AGGCGTTC'], ['YFG1', 'AGGCGNTTC'], ['YFG1', 'AGGCGNNTTC'])
    where '-' is search_char and 'N' is replace_char

    Args:
        char_iter ([type]): [description]
        search_char ([type]): [description]
        replace_char ([type]): [description]
    """

    def recurse(char_iter, collection):
        if search_char in char_iter:
            char_iter = replace_char.join(char_iter.split(search_char, 1))
            # Remove `search_char` from  trimmed iterable and add to `collection`
            stripped_char_iter = "".join(char for char in char_iter if char != search_char)
            collection.append(stripped_char_iter)
            # Pipe untrimmed `char_iter` for subsequent round of replace and trim
            return recurse(char_iter, collection)
        # First item should be stripped of replace_char and prepended to iterable
        if replace_char in collection[0]:
            collection.insert(0, collection[0].replace(replace_char, ""))
        return collection

    return recurse(char_iter, list())


if __name__ == "__main__":
    # Get data path for Thuy's reference barcodes
    DATA_PATH = os.path.join(BASE_DIR, "TN_20210927_alternate_barcodes.csv")
    csv_df = open_csv(DATA_PATH, ["GeneName", "Sequence"])

    # The Sequences contain '-' and 'N'. Get those with '-'
    dashed_seq = get_str_pattern_from_pddf(csv_df, "Sequence", "-", contains=True)
    zipped_dashed_seq = zip(*[dashed_seq[col] for col in dashed_seq])

    # Recursively convert '-' to 'N', adding one 'N' at a time where there are '-'
    variable_nt_collection = []
    for seq in zipped_dashed_seq:
        possible_seqs = recursively_swap_char(seq[1], "-", "N")
        seq_name_iter = (seq[0] for _ in range(len(possible_seqs)))
        variable_nt_collection.extend(list(zip(seq_name_iter, possible_seqs)))

    # Pair new collection with sequences without '-'
    normal_seq = get_str_pattern_from_pddf(csv_df, "Sequence", "-", contains=False)
    zipped_normal_seq = list(zip(*[normal_seq[col] for col in normal_seq]))
    zipped_normal_seq.extend(variable_nt_collection)

    # Export final dataframe
    final_df = pd.DataFrame(zipped_normal_seq, columns=["GeneName", "Sequence"])
    final_df.sort_index(axis=1, inplace=True)
    final_df.to_csv("TN_20210930_alternate_barcodes_exhausted.csv", index=False)
