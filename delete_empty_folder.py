import os
import sys


def delete_empty_folders(path):
    removed = False
    for dirpath, dirnames, filenames in os.walk(path, topdown=False):
        # check if the directory is empty
        if not dirnames and not filenames:
            try:
                os.rmdir(dirpath)
                removed = True
            except OSError as e:
                print(f"Error deleting folder {dirpath}: {e}")
    return removed


if __name__ == "__main__":
    if sys.argv[1:]:
        target_path = sys.argv[1]
        if os.path.isdir(target_path):
            deleted_any = delete_empty_folders(target_path)
            if not deleted_any:
                print("No empty folders found.")
        else:
            print(f"{target_path} is not a valid directory.")
    else:
        print("Please provide the path to a directory.")
