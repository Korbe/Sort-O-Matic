import os
import re
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from config import date_format_regexes, date_formats, strptime_formats
from io_helper import is_valid_image
from env import PRINT_ANALYZES_DETAIL


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
        if(PRINT_ANALYZES_DETAIL):
            print(f"File - \t{file_date}\nEXIF - \t{exif_date}\nName - \t{filename_date}")
        
    return oldest_timestamp

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

def hasTimestamp(string):
    
    if(string == "20150403_153433.jpg"):
        let = ""
    
    for index, pattern in enumerate(date_format_regexes):
        match = re.search(pattern, string)
        if match:
            return match.group(), date_formats[index], strptime_formats[index]
            
    return None, None, None #datestring, dateformat, strptime_format

def extract_timestamp_from_filename(filename):
    
    date, format, strptime_format = hasTimestamp(filename)
    
    if(date is None and format is None and strptime_format is None):
        return None
    
    try:
        return datetime.strptime(date, strptime_format)
    except ValueError as ex:
        pass# Invalid date for the current format
            
    return None

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