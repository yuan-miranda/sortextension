import os
import time
import sys


def deorganize_files(directory):
    directory = os.path.abspath(directory)

    if not os.path.exists(directory):
        print(f"'{directory}' does not exist.")
        return

    files = os.listdir(directory)
    for file in files:
        if file in ("main.py"):
            continue

        target_dir = os.path.join(directory, file)

        if os.path.isdir(target_dir):
            for item in os.listdir(target_dir):
                os.rename(os.path.join(target_dir, item), os.path.join(directory, item))


def deorganize_files_continuously(directory, interval=1):
    while True:
        try:
            deorganize_files(directory)
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"Deorganizing files in '{directory}' every {interval} seconds.")
        time.sleep(interval)


if __name__ == "__main__":
    args = sys.argv[1:]
    auto_mode = "auto" in args
    directory = next((arg for arg in args if arg != "auto"), os.getcwd())

    if auto_mode:
        deorganize_files_continuously(directory, interval=5)
    else:
        deorganize_files(directory)
