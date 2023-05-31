"""
The Files Merger script is designed to merge files with similar naming patterns located in a specified directory.
It automates the process of opening, reading, and merging files into a single consolidated file.

Created by: Sun Zhu, 2023-05-31, version 0.0
"""

# ////////// IMPORTS //////////
# ======== Standard library imports ========
import os
import pandas as pd
# ======== Local library imports ========
import path
# ////////// CONFIG //////////

# ////////// CLASS //////////

# ////////// UTILS //////////

# merge xls files in the specified folder
def merge_xls_files(folder_path, merged_file_path, ignore_index=True):
    """
    Merge xls files in the specified folder.
    :param folder_path: the folder path
    :param merged_file_path: the merged file path
    :return:
    """
    # Get all the files in the folder with the specified extension
    files = path.get_files_in_folder(folder_path, ext=".xls")

    # Merge the files
    df = pd.DataFrame()
    # load the first file
    df = df.append(pd.read_excel(os.path.join(folder_path, files[0])), ignore_index=False)
    # load the rest files, the rest files should have the same columns as the first file, the first row could be ignored
    for file in files:
        file_path = os.path.join(folder_path, file)
        df = df.append(pd.read_excel(file_path), ignore_index=True)
    df.to_excel(merged_file_path, index=False)

# ///////// TEST CASE ////////

# ======== Test1: merge_xls_files ========
def test_merge_xls_files():
    """
    Test the function merge_xls_files().
    :return:
    """
    # Define the folder path
    folder_path = "your files folder path"      # the folder contains the files to be merged

    # Define the merged file path
    merged_file_path = "your merged file path"  # the path to save the merged file
    # Merge the files
    merge_xls_files(folder_path, merged_file_path)
    print("test_merge_xls_files() passed!")

# ////////// MAIN //////////

if __name__ == "__main__":
    # ======== Test1: merge_xls_files ========
    test_merge_xls_files()  # Passed!
    pass
