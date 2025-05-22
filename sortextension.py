import os
import time
import sys

def organize_files(directory):
    directory = os.path.abspath(directory)
    
    if not os.path.exists(directory):
        print(f"'{directory}' does not exist.")
        return

    files = os.listdir(directory)
    for file in files:
        if file in ("main.py"):
            continue

        file_path = os.path.join(directory, file)
        if not os.path.isfile(file_path):
            continue

        file_extension = os.path.splitext(file)[1]
        if not file_extension:
            continue

        new_file_path = os.path.join(directory, file_extension)
        os.makedirs(new_file_path, exist_ok=True)
        
        base_name, file_extension = os.path.splitext(file)
        destination_path = os.path.join(new_file_path, file)
        
        if not os.path.exists(destination_path):
            os.rename(file_path, destination_path)
        else:
            duplicate_count = 1
            while True:
                new_file_name = f"{base_name} ({duplicate_count}){file_extension}"
                new_destination_path = os.path.join(new_file_path, new_file_name)
                
                if not os.path.exists(new_destination_path):
                    os.rename(file_path, new_destination_path)
                    break
                duplicate_count += 1

def organize_files_continuously(directory, interval=1):
    while True:
        try:
            organize_files(directory)
        except Exception as e:
            print(f"An error occurred: {e}")
        print(f"Reorganizing files in '{directory}' every {interval} seconds.")
        time.sleep(interval)

if __name__ == "__main__":
    args = sys.argv[1:]
    auto_mode = "auto" in args
    directory = next((arg for arg in args if arg != "auto"), os.getcwd())
    
    if auto_mode:
        organize_files_continuously(directory, interval=5)
    else:
        organize_files(directory)
