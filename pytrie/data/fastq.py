def open_fastq(fastq_path, filter_):
    with open(fastq_path, "r") as file:
        for line in file.readlines():
            if filter_(line):
                yield line.strip()
