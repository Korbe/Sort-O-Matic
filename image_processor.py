

import os
import shutil
import time
from io_helper import create_directory, move_file
from config import media_extensions, months
from timestamp_extractor import get_oldest_timestamp, hasTimestamp



def sort(source,  target):
    processed_files = 0
    start_time = time.time()
    
    errors = ""

    for current, _, files in os.walk(source):
        for file in files:
            try:
                process_image(current, target, file)
                processed_files+=1
            except Exception  as ex:
                errors+=f"\nError:{ex} at file {os.path.join(current, file)}"
            
    end_time = time.time()
    elapsed_time = end_time - start_time




def move_unsupported_file(source, target, file):
        unsupportedPath = os.path.join(target, "#Unsupported")
        create_directory(unsupportedPath)
        move_file(source, os.path.join(unsupportedPath, file))
        

def process_image(source, target, file):
    print(f"\nProcessing {file}")
    
    # if file not supported
    if os.path.splitext(file)[2].lower() not in media_extensions:
        move_unsupported_file()
        print(f"MOVED\tFiletype not supported {file}")
        return None
    
    file = os.path.join(source, file)
    
    oldest_timestamp = get_oldest_timestamp(file)

    if oldest_timestamp:
        process_valid_image(file, target, oldest_timestamp)
        return True
    else:
        process_invalid_image(file, target)
        return False
       
       
       
       
       
def process_valid_image(image_path, target, timestamp):
    year = timestamp.year
    month = timestamp.month
    month_name = months[month - 1]
    filename = os.path.basename(image_path)

    target_path = os.path.join(target, str(year), f"{month:02d}-{month_name}")
    
    new_filename = get_unique_filename(target_path, filename, timestamp)
    
    if "Kopie" in filename or "copy" in filename:
        target_path = os.path.join(target_path, "#Copy")
    elif "dupl" in filename:
        target_path = os.path.join(target_path, "#Duplicates")
           
    create_directory(target_path)
    move_file(image_path, os.path.join(target_path, new_filename))
    print(f"Moved {filename} to {target_path}")

def process_invalid_image(image_path, target):
    skipped_directory = os.path.join(target, "#Skipped")
    skipped_filepath = os.path.join(skipped_directory, filename)
    filename = os.path.basename(image_path)
    
    create_directory(skipped_directory)
    
    move_file(image_path, skipped_filepath)
    print(f"Skipped {filename}, moved to {skipped_filepath}")


def get_unique_filename(directory : str, filename : str, timestamp : str) -> str:
    filename, extension = os.path.splitext(filename)
    
    timestamp = timestamp.strftime('%Y-%m-%d')
    
    found_date, format = hasTimestamp(filename)
    if found_date:
        filename.replace(found_date, timestamp)
    else:
        filename = f"{timestamp}_{filename}"

    count = 1
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{filename}-dupl-{count:03d}"
        count += 1

    return f"{filename}.{extension}"