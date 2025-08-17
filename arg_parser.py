import argparse
from env import DEFAULT_SOURCE, DEFAULT_TARGET, MOVE_FILES, KEEP_NAMES


def parse_arguments():
    parser = argparse.ArgumentParser(description="Sort-O-Matic is a Python script that organizes images into yearly and monthly folders based on filename information, EXIF data, and file properties")
    parser.add_argument("-s", "--source", type=str, default=DEFAULT_SOURCE, help="Sourcepath to the folder which contains images")
    parser.add_argument("-t", "--target", type=str, default=DEFAULT_TARGET, help="Targetpath, where images should get copied/moved to")
    parser.add_argument("-m", "--move", default=MOVE_FILES, action="store_true", help="Move files instead of copying them (copy is default)")
    parser.add_argument("-k", "--keepnames", default=KEEP_NAMES, action="store_true", help="Keeps the original name as suffix")
    
    arguments = parser.parse_args()
    
    print("Arguments provided:")
    for arg_name, arg_value in vars(arguments).items():
        print(f"{arg_name}: {arg_value}")
    
    return arguments

# Parse arguments and store them in a global variable
args = parse_arguments()