import os
import shutil
from PIL import Image

def get_oldest_timestamp(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data and 36867 in exif_data:
                timestamp_str = exif_data[36867]
                return timestamp_str.split()[0]
    except (AttributeError, KeyError, IndexError, IOError, ValueError):
        pass
    return None

def main():
    source_directory = input("Enter the source directory (default is current directory): ")
    if not source_directory:
        source_directory = os.getcwd()

    target_base_directory = input("Enter the target base directory: ")

    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(root, filename)
                oldest_timestamp = get_oldest_timestamp(image_path)
                if oldest_timestamp:
                    year = oldest_timestamp.split(':')[0]

                    target_directory = os.path.join(target_base_directory, year)
                    os.makedirs(target_directory, exist_ok=True)

                    target_path = os.path.join(target_directory, filename)
                    shutil.move(image_path, target_path)
                    print(f"Moved {filename} to {target_directory}")

if __name__ == "__main__":
    main()
