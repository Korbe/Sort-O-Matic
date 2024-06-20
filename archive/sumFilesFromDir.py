import os
import shutil

def move_files_to_base(src_dir):
    # Ensure that the source directory exists
    if not os.path.exists(src_dir):
        print("Source directory does not exist.")
        return

    # Recursively retrieve all files in the source directory and its subdirectories
    for foldername, subfolders, filenames in os.walk(src_dir):
        for filename in filenames:
            src_path = os.path.join(foldername, filename)
            dest_path = os.path.join(src_dir, filename)

            # Check if the file already exists in the base directory
            if os.path.exists(dest_path):
                print(f"File '{filename}' already exists in the base directory.")
                filename = filename + "- copy"
                
            shutil.move(src_path, dest_path)
            print(f"Moved '{filename}' to the base directory.")

# Example usage:
source_directory = 'D:\MediaSorted'

move_files_to_base(source_directory)
