import os
import math
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

timestamps = []

def extract_timestamp_from_exif(filepath):
    try:
        img = Image.open(filepath)
        exif_data = img._getexif()

        

        if exif_data is not None:
            for tag, value in exif_data.items():
                try:
                    tag_name = TAGS.get(tag)
                    
                    if tag_name is None or type(value) is not str:
                        #print(f'{tag}\t -\t{tag_name}')#print(f'{tag}\t -\t{tag_name} - tag_name is {type(tag_name)}')
                        continue

                    # Check if the tag name contains 'date' or 'time'
                    if ('date' in tag_name.lower() or 'time' in tag_name.lower()) and len(value) >= 6:
                        try:
                            date = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            #timestamps.append(date)
                            if tag_name not in timestamps:
                                timestamps.append(f'{tag_name}')
                                
                            #print(f'{tag}\t-\t{tag_name}')#print(f'{tag}\t-\t{tag_name}={value} -\tretrieved')
                        except ValueError as vex:
                            print(f'{tag}\t-\t{tag_name} - value error: {vex}')#print(f'{tag}\t-\t{tag_name}={value} -\terrord')
                            pass
                except Exception as e:
                    print(f'{tag}\t -\t{tag_name} - \tAn error occurred in loop: {e}')
        else:
            print(f"No exif data found");
        return timestamps

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
for root, dirs, files in os.walk(os.getcwd() + '/test'):
        for filename in files:
            #print(f"\n\n{filename} getting processed:")
            timestamps = extract_timestamp_from_exif(os.getcwd() + '/test/' + filename)
            
for timestamp in timestamps:
    print(timestamp)
