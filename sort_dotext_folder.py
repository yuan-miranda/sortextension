import os
import sys
import shutil


def append_duplicate_counter(dest_dir, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    candidate = filename
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{base} ({counter}){ext}"
        counter += 1
    return os.path.join(dest_dir, candidate)


def move_or_merge_folder(src, dst):
    if not os.path.exists(dst):
        shutil.move(src, dst)
    else:
        # merge extension folders to dotext's extension folders
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                move_or_merge_folder(s, d)
            else:
                if os.path.exists(d):
                    d = append_duplicate_counter(dst, item)
                shutil.move(s, d)
        os.rmdir(src)


def move_dot_folders(path):
    dotext_folder = os.path.join(path, "dotext")
    os.makedirs(dotext_folder, exist_ok=True)
    moved = False

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)
        if os.path.isdir(entry_path) and entry.startswith(".") and len(entry) > 1:
            dest_path = os.path.join(dotext_folder, entry)
            move_or_merge_folder(entry_path, dest_path)
            moved = True
    return moved


if __name__ == "__main__":
    if sys.argv[1:]:
        target_path = sys.argv[1]
        if os.path.isdir(target_path):
            if not move_dot_folders(target_path):
                print("No .xxx folders found to move.")
        else:
            print(f"{target_path} is not a valid directory.")
    else:
        print("Please provide the path to a directory.")
