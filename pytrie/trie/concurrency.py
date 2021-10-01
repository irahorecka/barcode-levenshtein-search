import concurrent.futures


def map_processes(func, iterable):
    """Map function with iterable object in using process pools."""
    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        result = executor.map(func, iterable, chunksize=125)
    return result
