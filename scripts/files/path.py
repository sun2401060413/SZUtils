"""
Some scripts for path operations.

Created by Sun Zhu, 2023-05-31, version 0.0
"""

# ////////// IMPORT //////////
import os

# ////////// CONFIG //////////

# ////////// CLASS //////////

# ////////// UTILS //////////
def get_file_name(file_path):
    """
    Get the file name from the file path.
    """
    return os.path.split(file_path)[-1]

def get_file_name_without_ext(file_path):
    """
    Get the file name without extension from the file path.
    """
    return os.path.splitext(get_file_name(file_path))[0]

def get_file_ext(file_path):
    """
    Get the file extension from the file path.
    """
    return os.path.splitext(get_file_name(file_path))[1]

# Get all the files in the folder with the specified extension
def get_files_in_folder(folder_path, ext=None):
    """
    Get all the files in the folder with the specified extension.
    """
    files = []
    for file in os.listdir(folder_path):
        if ext is None or get_file_ext(file) == ext:
            files.append(file)
    return files

# ///////// TEST CASE ////////

# ////////// MAIN //////////

if __name__ == "__main__":
    pass