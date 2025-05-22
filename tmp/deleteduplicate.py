from collections import defaultdict
import hashlib
import os
import sys


def chunk_reader(fobj, chunk_size=1024):
    while chunk := fobj.read(chunk_size):
        yield chunk


def get_hash(filename, first_chunk_only=False, hash_func=hashlib.sha1):
    hashobj = hash_func()
    try:
        with open(filename, "rb") as f:
            if first_chunk_only:
                hashobj.update(f.read(1024))
            else:
                for chunk in chunk_reader(f):
                    hashobj.update(chunk)
    except (OSError, IOError) as e:
        print(f"Error reading file {filename}: {e}")
        return None
    return hashobj.digest()


def check_for_duplicates(paths):
    hashes_by_size = defaultdict(list)
    hashes_on_1k = defaultdict(list)
    hashes_full = {}

    # group files by size
    for path in paths:
        for dirpath, _, filenames in os.walk(path):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(full_path)
                    hashes_by_size[file_size].append(full_path)
                except (OSError,):
                    continue

    # group files by size and hash
    for size, files in hashes_by_size.items():
        if len(files) < 2:
            continue

        for filename in files:
            small_hash = get_hash(filename, first_chunk_only=True)
            if small_hash:
                hashes_on_1k[(small_hash, size)].append(filename)

    for files in hashes_on_1k.values():
        if len(files) < 2:
            continue

        for filename in files:
            full_hash = get_hash(filename, first_chunk_only=False)
            if not full_hash:
                continue

            duplicate = hashes_full.get(full_hash)
            if duplicate:
                try:
                    os.remove(filename)
                    print("Deleted: {}".format(filename))
                except (OSError,):
                    print(f"Error deleting file {filename}: {e}")
            else:
                hashes_full[full_hash] = filename


if __name__ == "__main__":
    if sys.argv[1:]:
        # iterate over all folders in the directory
        folders = os.listdir(sys.argv[1])
        for folder in folders:
            path = os.path.join(sys.argv[1], folder)
            if os.path.isdir(path):
                check_for_duplicates([path])
    else:
        print("Please pass the path to a directory to check for duplicates.")
