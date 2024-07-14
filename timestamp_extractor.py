import os
import re
from datetime import datetime
import subprocess
from exif import Image as ExifImage
from config import date_format_regexes, date_formats, strptime_formats, video_extensions
from env import PRINT_ANALYZES_DETAIL

def hasTimestamp(string):
    for index, pattern in enumerate(date_format_regexes):
        match = re.search(pattern, string)
        if match:
            return match.group(), date_formats[index], strptime_formats[index]
            
    return None, None, None #datestring, dateformat, strptime_format

def get_oldest_timestamp(image_path):
    # Extract timestamps
    file_date = extract_timestamp_from_file(image_path)
    filename_date = extract_timestamp_from_filename(os.path.basename(image_path))
            
    if os.path.splitext(image_path)[1].lower() in video_extensions:
        meta_date = extract_timestamp_from_video(image_path)
    else:
         meta_date = extract_timestamp_from_exif_image(image_path)
    

    #filter all timestamps which are not null/none
    timestamps = [
        ts for ts in [file_date, filename_date, meta_date]
        if ts is not None
    ]
    
    oldest_timestamp = None

    if timestamps:
        oldest_timestamp = min(timestamps)
        if(PRINT_ANALYZES_DETAIL):
            print(f"File - \t{file_date}\nName - \t{filename_date}\nMeta - \t{meta_date}")
        
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

def extract_timestamp_from_filename(filename):
    
    date, format, strptime_format = hasTimestamp(filename)
    
    if(date is None and format is None and strptime_format is None):
        return None
    
    try:
        return datetime.strptime(date, strptime_format)
    except ValueError as ex:
        pass# Invalid date for the current format
            
    return None

def extract_timestamp_from_exif_image(file_path):
    try:
            # Extract EXIF data using exif library
            with open(file_path, 'rb') as img_file:
                exif_img = ExifImage(img_file)


            dates_with_tags = []
            
            date_tags = [
                'datetime',
                'datetime_original',
                'datetime_digitized',
                'gps_datestamp'
            ]
            
            # Extract dates from the EXIF tags
            for tag in date_tags:
                if hasattr(exif_img, tag):
                    date_str = getattr(exif_img, tag)
                    if tag == 'gps_datestamp':
                        # GPS date does not include time, we add a default time
                        date_str += ' 00:00:00'
                    try:
                        date, format, strptime_format = hasTimestamp(date_str)
        
                        timestamp = datetime.strptime(date, strptime_format)
                        dates_with_tags.append(timestamp)
                    except ValueError:
                        pass
            
            # If dates were found, return the oldest one
            if dates_with_tags:
                return min(dates_with_tags)
            else:
                return None
    
    except (IOError, OSError, Exception) as ex:
        return None

def extract_timestamp_from_video(video_path):
    try:
        
        #Command to run ffprobe and extract relevant tags
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format_tags=creation_time', 
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]  
        
        # Run the command and capture output
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        
        date, format, strptime_format = hasTimestamp(output)
        
        timestamp = datetime.strptime(date, strptime_format)
        
        return timestamp
    
    except subprocess.CalledProcessError as ex:
        print(f"Error running ffprobe on {video_path}: {ex}")
        return None
    except Exception as ex:
        print(f"Unexpected error processing {video_path}: {ex}")
        return None