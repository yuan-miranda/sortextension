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
        target_dir = os.path.join(directory, file)

        if os.path.isdir(target_dir):
            # iterate through items in the target directory
            for item in os.listdir(target_dir):
                original_path = os.path.join(target_dir, item)
                destination_path = os.path.join(directory, item)

                # if in case of same name, append a number to the filename e.g. file (1).txt
                if os.path.exists(destination_path):
                    base, ext = os.path.splitext(item)
                    counter = 1
                    while True:
                        new_name = f"{base} ({counter}){ext}"
                        new_destination_path = os.path.join(directory, new_name)
                        if not os.path.exists(new_destination_path):
                            destination_path = new_destination_path
                            break
                        counter += 1

                os.rename(original_path, destination_path)


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
