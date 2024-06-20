import os
import shutil
from datetime import datetime
import re
from PIL import Image
from PIL.ExifTags import TAGS

#todo dont overwrite files already there
#overwritte with the same Name no no no
# rename to year-month-day_oldName images cannot have the same anymore
# sort them into months 1_Januar 2_February or german make it changeable

date_formats = [
    '%Y-%m-%d',     # 2023-10-25   
    '%Y_%m_%d',     # 2023_10_25    
    '%Y.%m.%d',     # 2023.05.15
    '%Y%m%d',       # 20230712
    '%d_%m_%Y',     # 05_08_2023
    '%d-%m-%Y',     # 05-08-2023
    '%d.%m.%Y',     # 08.03.2023
    '%d_%m_%y',     # 05_08_23
    '%d-%m-%y',     # 05-08-23
    '%d.%m.%y',     # 08.03.23
    '%d%m%Y',       # 29022023
    '%d%m%y',       # 290223
]

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
    '.psd',
    '.pdf',
    '.ai'
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
    for date_format in date_formats:
        pattern = date_format.replace('%d', r'\d{2}').replace('%m', r'\d{2}').replace('%Y', r'\d{4}') \
                             .replace('%y', r'\d{2}').replace('-', r'[-_/]').replace('.', r'[./_]')
        match = re.search(pattern, filename)
        if match:
            extracted_date = match.group()
            try:
                parsed_date = datetime.strptime(extracted_date, date_format)
                return parsed_date
            except ValueError:
                pass  # Invalid date for the current format
    return None

def extract_timestamp_from_exif(filepath):
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
    os.makedirs(directory_path, exist_ok=True)

def move_file(source_path, target_path):
    shutil.move(source_path, target_path)

def process_image(source_directory, target_base_directory, filename):
    _, extension = os.path.splitext(filename)
    
    if extension.lower() in media_extensions:
        image_path = os.path.join(source_directory, filename)
        print(f"Processing {filename}...")
        
        # Extract timestamps
        timestamp_file = extract_timestamp_from_file(image_path)
        timestamp_filename = extract_timestamp_from_filename(filename)
        timestamp_exif = extract_timestamp_from_exif(image_path)
        
        timestamps = [
            ts for ts in [timestamp_filename, timestamp_exif, timestamp_file]
            	if ts is not None
        ]
        
        if timestamps:
            oldest_timestamp = min(timestamps)
            print(f"Filename - \t{timestamp_filename} \nEXIF\t - \t{timestamp_exif}, \nFile\t - \t{timestamp_file}")
        else:
            oldest_timestamp = None
            print("No valid timestamps found")

        if oldest_timestamp:
            process_valid_image(image_path, filename, oldest_timestamp, target_base_directory)
        else:
            process_invalid_image(image_path, filename, target_base_directory)
    else:
        print(f"Skipped {filename} due to not supported extension {extension}")

def process_valid_image(image_path, filename, timestamp, target_base_directory):
    year = timestamp.year
    target_directory = os.path.join(target_base_directory, str(year))
    create_directory(target_directory)

    if "- Kopie" in filename or "- copy" in filename:
        copy_folder = os.path.join(target_directory, "copy")
        create_directory(copy_folder)
        target_path = os.path.join(copy_folder, filename)
    else:
        target_path = os.path.join(target_directory, filename)

    move_file(image_path, target_path)
    print(f"Moved {filename} to {target_path}")

def process_invalid_image(image_path, filename, target_base_directory):
    skipped_directory = os.path.join(target_base_directory, "skipped")
    create_directory(skipped_directory)
    skipped_path = os.path.join(skipped_directory, filename)
    move_file(image_path, skipped_path)
    print(f"Skipped {filename}, moved to {skipped_path}")

def main():
    #source_directory = input("Enter the source directory (default is current directory): ")
    #if not source_directory:
    source_directory = os.getcwd() + '\images'

    #target_base_directory = input("Enter the target base directory (default is current directory): ")
    #if not target_base_directory:
    target_base_directory = os.getcwd() + '\processed-images'

    print("Starting image sorting process...")
    print("-" * 40)

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            process_image(root, target_base_directory, filename)

    print("-" * 40)
    print("Image sorting process completed.")

if __name__ == "__main__":
    main()
