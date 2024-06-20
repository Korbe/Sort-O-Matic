import os
import time
from env import PRINT_ARGS
from image_processor import process_image, sort
from config import media_extensions
from io_helper import create_directory, create_template_folder
from arg_parser import parse_arguments


#   todo dont overwrite files already there
#   overwritte with the same Name no no no
# x rename to year-month-day_oldName images cannot have the same name anymore
# x sort them into months 1_Januar 2_February or german 
#   make month changeable



def get_arguments():
    args = parse_arguments();
    
    if(PRINT_ARGS):
        print("Arguments provided:")
        for arg_name, arg_value in vars(args).items():
            print(f"{arg_name}: {arg_value}")
            
    return args;
    
def main():
    

    #source_path = getPath("Enter the source directory ([enter] default current directory): ", "source")
    #target_path = getPath("Enter the target base directory ([enter] default current directory\processed-images): ", "target")
    
    # source_path = os.getcwd() + '\source'
    # target_path = os.getcwd() + '\output'
    
    
    
    args = get_arguments();    
    
    # Create the the template folder
    create_template_folder(os.path.join(args.target, "Vorlage"))
    
    print("-" * 40)
    print("Starting sorting process...\n")

    # sort(args.source, args.target)
    
    # print("")
    # print("-" * 40)
    # print(f"Sort process completed in {int(elapsed_time // 60)} minutes or {int(elapsed_time % 60)} seconds")
    # print(f"Moved {processed_files}/{total} files from {directories} directories")
    # print("\n" + errors)
    
    #print(f"processed_files: {processed_files}")
    #print(f"count_files: {count_files(source_path)}")
    
    



def count_files(directory : str):
    file_count = 0
    directory_count = 0
    files_with_correct_type = 0

    for _, _, files in os.walk(directory):
        directory_count += 1;
        file_count += len(files)
        supported_files = [file for file in files if any(file.endswith(ext) for ext in media_extensions)]
        files_with_correct_type = len(supported_files)

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




if __name__ == "__main__":
    main()