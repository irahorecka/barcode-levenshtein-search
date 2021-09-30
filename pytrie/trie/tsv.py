import csv


def open_tsv(tsv_path):
    with open(tsv_path) as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        return [row.pop() for row in rd]
