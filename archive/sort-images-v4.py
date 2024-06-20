import time
import os
import shutil
from datetime import datetime
import re
from PIL import Image
from PIL.ExifTags import TAGS

#   todo dont overwrite files already there
#   overwritte with the same Name no no no
# x rename to year-month-day_oldName images cannot have the same name anymore
# x sort them into months 1_Januar 2_February or german 
#   make mont changeable

moveFiles = False    

months = ["Jän", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

date_formats = [
    'Y-m-d',     # 2023-10-25   
    'Y_m_d',     # 2023_10_25    
    'Y.m.d',     # 2023.05.15
    
    'Ymd',       # 20230712
    
    'd_m_Y',     # 05_08_2023
    'd-m-Y',     # 05-08-2023
    'd.m.Y',     # 08.03.2023
    
    'd_m_y',     # 05_08_23
    'd-m-y',     # 05-08-23
    'd.m.y',     # 08.03.23
    
    'dmY',       # 29022023
    'dmy',       # 290223
]

date_regex_replacements = {
    'd': r'\d{1,2}',
    'Y': r'\d{4}',
    'y': r'\d{2}',
    'm': r'\d{1,2}',
    '[_\-\.]': r'[_\-\.]'
}

image_extensions = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.tif',
    '.tiff',
    '.webp',
    '.heic',
    '.svg',
    '.raw',
    '.ico',
    '.eps',
    '.nef'
]

video_extensions = [
    '.mp4',
    '.mov',
    '.mkv',
    '.avi',
    '.wmv',
    '.flv',
    '.webm',
    '.3gp',
    '.m4v',
    '.mpg',
    '.mpeg',
    '.mts',
    '.m2ts',
    '.ts',
    '.vob'
]

media_extensions = image_extensions + video_extensions

# Convert date format into a regular expression
def format_to_regex(date_format):
    regex_format = date_format
    
    for pattern, replacement in date_regex_replacements.items():
        regex_format = regex_format.replace(pattern, replacement)

    return f"^{regex_format}$"

# Create an array of regular expressions
date_format_regexes = [format_to_regex(date_format) for date_format in date_formats]


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

def extract_timestamp_from_file(filepath):
    try:
        timestamps = [
            datetime.fromtimestamp(os.path.getctime(filepath)),  # creation_time
            datetime.fromtimestamp(os.path.getmtime(filepath)),  # modification_time
            datetime.fromtimestamp(os.path.getatime(filepath)),  # access_time
        ]
        
        return min(timestamps)
    except OSError:
        pass
    
    return None

def extract_timestamp_from_filename(filename):
    
    date, format = hasTimestamp(filename)
    
    if(date is None and format is None):
        return None
    
    try:
        return datetime.strptime(date, format)
    except ValueError:
        pass# Invalid date for the current format
            
    return None

def hasTimestamp(string):
    
    for index, pattern in enumerate(date_format_regexes):
        match = re.search(pattern, string)
        if match:
            return match.group(), date_formats[index]
            
    return None, None

def is_valid_image(file_path):
    try:
        with Image.open(file_path) as img:
            # Check if the file is a valid image
            return True
    except (IOError, OSError, Exception):
        # An exception is raised if the file is not a valid image
        return False

def extract_timestamp_from_exif(filepath):
    
    if not is_valid_image(filepath):
        return None
    
    try:
        timestamps = []
        img = Image.open(filepath)
        exif_data = img._getexif()

        if exif_data is None:
            return None
            
        for tag, value in exif_data.items():
            try:
                tag_name = TAGS.get(tag)
                
                if tag_name is None or type(value) is not str:
                    continue

                # Check if the tag name contains 'date' or 'time'
                if ('date' in tag_name.lower() or 'time' in tag_name.lower()) and len(value) >= 6:
                    try:
                        timestamps.append(datetime.strptime(value, '%Y:%m:%d %H:%M:%S'))
                    except ValueError as e:
                        print(f'{tag}\t -\t{tag_name} - \tAn ValueError occurred while reading Exif: {e}')
                        pass
            except Exception as e:
                print(f'{tag}\t -\t{tag_name} - \tAn Exception occurred while reading Exif: {e}')
            
        return min(timestamps)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

def move_file(source_path, target_path):
    if moveFiles:
        shutil.move(source_path, target_path)
    else:
        shutil.copy(source_path, target_path)

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

def  get_oldest_timestamp(image_path):
    # Extract timestamps
    file_date = extract_timestamp_from_file(image_path)
    exif_date = extract_timestamp_from_exif(image_path)
    filename_date = extract_timestamp_from_filename(os.path.basename(image_path))

    #filter all timestamps which are not null/none
    timestamps = [
        ts for ts in [file_date, exif_date, filename_date]
        if ts is not None
    ]
    
    oldest_timestamp = None

    if timestamps:
        oldest_timestamp = min(timestamps)
        print(f"Extracted timestamps:\nFile\t - \t{file_date}\nEXIF\t - \t{exif_date}\nFilename - \t{filename_date}")
    else:
        print("No valid timestamps found")
        
    return oldest_timestamp

def process_image(source_directory, target_base_directory, filename):
    _, extension = os.path.splitext(filename)
    
    print(f"\nProcessing {filename}")
    
    if extension.lower() not in media_extensions:
        unsupportedPath = os.path.join(target_base_directory, "#Unsupported")
        create_directory(unsupportedPath)
        shutil.copy(source_directory, os.path.join(unsupportedPath, filename))
        print(f"Moved {filename} to unsupported folder due to extension {extension}")
        raise Exception(f"Moved {filename} to unsupported folder due to extension {extension}")
    
    image_path = os.path.join(source_directory, filename)
    
    oldest_timestamp = get_oldest_timestamp(image_path)

    if oldest_timestamp:
        process_valid_image(image_path, oldest_timestamp, target_base_directory)
    else:
        process_invalid_image(image_path, target_base_directory)
       
def process_valid_image(image_path, timestamp, target_base_directory):
    year = timestamp.year
    month = timestamp.month
    month_name = months[month - 1]
    filename = os.path.basename(image_path)

    target_path = os.path.join(target_base_directory, str(year), f"{month:02d}-{month_name}")
    
    new_filename = get_unique_filename(target_path, filename, timestamp)
    
    if "Kopie" in filename or "copy" in filename:
        target_path = os.path.join(target_path, "#Copy")
    elif "dupl" in filename:
        target_path = os.path.join(target_path, "#Duplicates")
           
    create_directory(target_path)
    move_file(image_path, os.path.join(target_path, new_filename))
    print(f"Moved {filename} to {target_path}")




def process_invalid_image(image_path, target_base_directory):
    skipped_directory = os.path.join(target_base_directory, "#Skipped")
    skipped_filepath = os.path.join(skipped_directory, filename)
    filename = os.path.basename(image_path)
    
    create_directory(skipped_directory)
    
    move_file(image_path, skipped_filepath)
    print(f"Skipped {filename}, moved to {skipped_filepath}")

def getPath(text, type):
    path = input(text)

    if(not os.path.exists(path)):
        if(type == "source"):
            raise Exception(f"Enter a valid path! {path} does not exist")
        if(type == "target"):
            create_directory(path)
            print(f"Directory {path} created")
    
    return path
    
def main():
    
    print("- Sort Images -")
    #source_path = getPath("Enter the source directory ([enter] default current directory): ", "source")
    #target_path = getPath("Enter the target base directory ([enter] default current directory\processed-images): ", "target")
    
    source_path = os.getcwd() + '\source'
    target_path = os.getcwd() + '\\target'
    
    # Create the the template folder
    create_template_folder(os.path.join(target_path, "Vorlage"))
    
    print(f"Source: {source_path}")
    print(f"Target: {target_path}")
    
    print("Starting sorting process...")
    print("-" * 40)
    print("\n")

    total = 0
    moves = 0
    directories = 0
    start_time = time.time()
    
    errors = ""

    for source_directory, dirs, files in os.walk(source_path):
        for filename in files:
            total+=1
            
            try:
                process_image(source_directory, target_path, filename)
                moves+=1
            except Exception  as ex:
                errors+=f"\nError:{ex} at file {os.path.join(source_directory, filename)}"
            
        directories+=1
            
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n")
    print("-" * 40)
    print(f"Sort process completed in {int(elapsed_time // 60)} minutes and {int(elapsed_time % 60)} seconds")
    print(f"Moved {moves}/{total} files from {directories} directories")
    print("\n" + errors)

if __name__ == "__main__":
    main()