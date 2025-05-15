import os
import sys

def get_size(path):
    """Returns the total size of a file or folder."""
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def human_readable_size(size):
    """Converts size in bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

def list_files_and_sizes(directory):
    """Lists all files and folders in the given directory with their sizes, sorted by size."""
    if not os.path.exists(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return
    
    contents = os.listdir(directory)
    items_with_sizes = [(item, get_size(os.path.join(directory, item))) for item in contents]
    items_with_sizes.sort(key=lambda x: x[1], reverse=True)
    
    print(f"Contents of '{directory}':\n")
    for item, size in items_with_sizes:
        print(f"{item}: {human_readable_size(size)}")

if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    list_files_and_sizes(directory)