import os
import sys
import threading
import time
from env import CREATE_TEMPLATE, PRINT_ANALYZES_DETAIL
from image_processor import process_image, sort
from config import media_extensions
from io_helper import create_directory, create_template_folder, move_file
from arg_parser import args

def main():
    if(CREATE_TEMPLATE):
        create_template_folder(os.path.join(args.target, "Vorlage"))
    
    print("-" * 40)
    
    file_count, files_with_correct_type, directory_count = count_files(args.source)
    print(f"{files_with_correct_type} of {file_count} files found with supported type")
    
    if(files_with_correct_type == 0):
        print("No files match supported image or video types")    
        return

    print("Starting sort process...\n")

    
    mediaPathMapping = analyze_media(file_count, directory_count)
    
    print("")
    
    move_files(mediaPathMapping, file_count, directory_count)
    


def analyze_media(file_count, directory_count):
    print("Analyze media...")
     
    if(PRINT_ANALYZES_DETAIL == False):    
        stop_event = threading.Event()
        # Start the spinner in a separate thread
        spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
        spinner_thread.start() 
    
    start_time = time.time()
   
    try:    
        mediaPathMapping, processed_files, errors = sort(args.source, args.target)
        
        end_time = time.time()
        elapsed_time = end_time - start_time
    finally:
        if(PRINT_ANALYZES_DETAIL == False):
            # Stop the spinner
            stop_event.set()
            spinner_thread.join()
        
    print(f"Completed in {int(elapsed_time // 60)} minutes or {elapsed_time:.3f} seconds")
    print(f"Analyzed {processed_files}/{file_count} files in {directory_count} directories")
    
    if(errors):
        print("\n" + errors + "\n")
        
    return mediaPathMapping

def move_files(mediaPathMapping, file_count, directory_count):
    
    print(f"{'Move' if args.move else 'Copy'} files...")
    
    stop_event = threading.Event()
    
    # Start the spinner in a separate thread
    spinner_thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    spinner_thread.start() 
    
    start_time = time.time()
    
    try:  
        for key, value in mediaPathMapping.items():
            create_directory(os.path.dirname(value))
            move_file(key, value)
            
        end_time = time.time()
        elapsed_time = end_time - start_time
    finally:      
        # Stop the spinner
        stop_event.set()
        spinner_thread.join()
        
    print(f"Completed in {int(elapsed_time // 60)} minutes or {elapsed_time:.3f} seconds")
    print(f"{'Moved' if args.move else 'Copied'} {len(mediaPathMapping)}/{file_count} files in {directory_count} directories")


def count_files(directory : str):
    file_count = 0
    directory_count = 0
    files_with_correct_type = 0

    for _, _, files in os.walk(directory):
        directory_count += 1;
        file_count += len(files)
        supported_files = [file for file in files if any(file.endswith(extension) for extension in media_extensions)]
        
        files_with_correct_type += len(supported_files)

    return file_count, files_with_correct_type, directory_count


def getPath(text, type):
    path = input(text)

    if(not os.path.exists(path)):
        if(type == "source"):
            raise Exception(f"Enter a valid path! {path} does not exist")
        if(type == "target"):
            create_directory(path)
            print(f"Directory {path} created")
    
    return path

# Define the spinner animation function
def spinner_animation(stop_event):
    spinner = ['|', '/', '-', '\\']
    while not stop_event.is_set():
        for symbol in spinner:
            if stop_event.is_set():
                break
            sys.stdout.write(f'\r{symbol}')
            sys.stdout.flush()
            time.sleep(0.1)
    
    # Clear the last character
    print('\r ', end='\r', flush=True)


if __name__ == "__main__":
    main()