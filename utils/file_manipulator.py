import os
import shutil

def clear_folder(folder_path):
    for entry in os.listdir(folder_path):
        # get the path to the file/subfolder
        entry_path = os.path.join(folder_path, entry)
        try:
            if os.path.isdir(entry_path):
                # if this entry is a subdirectory, remove it and its content
                shutil.rmtree(entry_path)
            elif os.path.isfile(entry_path) or os.path.islink(entry_path):
                # if this entry is a file or a symbolic link, just remove it
                os.unlink(entry_path)
        except Exception as e:
            print(f"Failed to delete {entry_path}. Reason: {e}") 
