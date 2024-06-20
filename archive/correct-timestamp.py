import os
import sys
from PIL import Image
from datetime import datetime

# Replace 'your_folder_path' with the actual path to your image folder
image_folder = os.getcwd() + '\check'

# Replace 'new_datetime' with the timestamp you want to set (in the format 'YYYY:MM:DD HH:MM:SS')
new_datetime = '2012:08:01 12:00:00'

try:
    # Convert the new_datetime string to a datetime object
    new_datetime_obj = datetime.strptime(new_datetime, '%Y:%m:%d %H:%M:%S')

    for root, dirs, files in os.walk(image_folder):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, filename)

                # Update LastWriteTime and CreationTime properties in Windows
                os.utime(image_path, (new_datetime_obj.timestamp(), new_datetime_obj.timestamp()))

                # Open the image and update the EXIF attribute DateTimeOriginal
                with Image.open(image_path) as img:
                    exif_data = img.info.get('exif', b'')
                    exif_data = exif_data.replace(b'DateTimeOriginal', new_datetime.encode('utf-8'))
                    img.save(image_path, exif=exif_data)

                print(f'Processed: {image_path}')

    print('All images processed successfully.')

except Exception as e:
    print(f'An error occurred: {str(e)}')