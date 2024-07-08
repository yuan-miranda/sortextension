import os

files_moved = []
path = os.getcwd()

files = os.listdir(path)
for file in files:
    if file == 'main.py' or file == 'log.txt':
        continue

    # current file concatenated with the path
    file_path = os.path.join(path, file)
    if not os.path.isfile(file_path):
        continue

    # get the file extension
    file_extension = os.path.splitext(file)[1]
    if not file_extension:
        continue

    # create a new directory named after the file extension
    new_file_path = os.path.join(path, file_extension)
    os.makedirs(new_file_path, exist_ok=True)
    
    # move the file to the new directory
    if not os.path.exists(os.path.join(new_file_path, file)):
        os.rename(file_path, os.path.join(new_file_path, file))
    else:
        duplicate_count = 1
        while True:
            file = f"{file.split(".")[0]}{duplicate_count}{file_extension}"
            
            # if the current file name already exists in the directory, append a number to the file name
            if not os.path.exists(os.path.join(new_file_path, file)):
                os.rename(file_path, os.path.join(new_file_path, file))
                break
            duplicate_count += 1
    files_moved.append(os.path.join(new_file_path, file))

with open("log.txt", "w") as file:
    file.write("\n".join(files_moved))

print("Files moved successfully, check log.txt to see the list of files moved.")