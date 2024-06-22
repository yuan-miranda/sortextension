import os

files_moved = []
path = os.getcwd()

files = os.listdir(path)
for file in files:
    if file == 'main.py' or file == 'log.txt':
        continue

    file_path = os.path.join(path, file)
    if not os.path.isfile(file_path):
        continue

    file_extension = os.path.splitext(file)[1]
    if not file_extension:
        continue

    new_file_path = os.path.join(path, file_extension)
    os.makedirs(new_file_path, exist_ok=True)
    
    os.rename(file_path, os.path.join(new_file_path, file))
    files_moved.append(os.path.join(new_file_path, file))

with open("log.txt", "w") as file:
    file.write("\n".join(files_moved))

print("Files moved successfully, check log.txt to see the list of files moved.")