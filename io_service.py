import shutil
import os
from PIL import Image
from config import months
from arg_parser import args

def move_file(source_path, target_path):

    if not os.path.exists(source_path):
        print(f"Error: move_file Source path '{source_path}' does not exist.")
        return
    
    counter = 2
    base, ext = os.path.splitext(target_path)
    
    while os.path.exists(target_path):
        target_path = f"{base}_{counter}{ext}"
        counter += 1

    if args.move:
        shutil.move(source_path, target_path)
    else:
        shutil.copy(source_path, target_path)
        

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

def create_template_folder(filepath):
    if not os.path.exists(filepath):
        print(f"create template folder in {filepath}")
        os.makedirs(filepath)
        create_months_folder(filepath)

def create_months_folder(filepath):
        for index, month in enumerate(months):
            folder_name = f"{index + 1:02d}-{month}"  # Prefix the index with zero-padding
            folder_path = os.path.join(filepath, folder_name)
            
            # Check if the subfolder already exists
            if not os.path.exists(folder_path):
                # Create the subfolder
                os.makedirs(folder_path)


def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            # Check if the file is a valid image
            return True
    except (IOError, OSError, Exception):
        # An exception is raised if the file is not a valid image
        return False