import os
from config import media_extensions, months
from timestamp_extractor import get_oldest_timestamp, hasTimestamp

mediaPathMapping = {}

def sort(source,  target):
    processed_files = 0    
    errors = ""

    for current, _, files in os.walk(source):
        for file in files:
            
            try:
                process_image(current, target, file)
                processed_files+=1
            except Exception  as ex:
                errors+=f"\nError:{ex} at file {os.path.join(current, file)}"
            
    
    
    return mediaPathMapping, processed_files, errors
        

def process_image(source, target, file):
    filePath = os.path.join(source, file)
    extension = os.path.splitext(file)[1].lower()
    
    # if file not supported
    if  extension not in media_extensions:
        mediaPathMapping[filePath]=os.path.join(target, "#Unsupported", file)
        return
    
    oldest_timestamp = get_oldest_timestamp(filePath)

    if oldest_timestamp:
        process_valid_image(filePath, target, oldest_timestamp)
    else:
        mediaPathMapping[filePath]=os.path.join(target, "#Skipped", file)
       
       
def process_valid_image(image_path, target, timestamp):
    filename = os.path.basename(image_path)

    target_path = os.path.join(target, str( timestamp.year), f"{timestamp.month:02d}-{months[timestamp.month - 1]}")
    
    new_filename = get_unique_filename(target_path, filename, timestamp)
    
    mediaPathMapping[image_path]=os.path.join(target_path, new_filename)     


def get_unique_filename(directory : str, filename : str, timestamp : str) -> str:
    base, extension = os.path.splitext(filename)
    
    timestamp = timestamp.strftime('%Y-%m-%d')
    filename = timestamp
    
    count = 2
    while os.path.exists(os.path.join(directory, f"{filename}{extension}")):
        filename = f"{timestamp}_{count}"
        count += 1

    return f"{filename}{extension}"