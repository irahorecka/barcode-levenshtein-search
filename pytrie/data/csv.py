import pandas as pd


def open_csv(csv_path, headers=True, header_names=None):
    """Opens CSV file and returns pandas dataframe to caller."""
    if headers:
        return pd.read_csv(csv_path)
    if header_names and hasattr(header_names, "__iter__"):
        return pd.read_csv(csv_path, sep=",", header=0, names=header_names)
    return pd.read_csv(csv_path, sep=",", header=0)
