from PIL import Image
import os
import hashlib

def image_hash(file_path):
    """Calculate the MD5 hash of an image file."""
    with open(file_path, 'rb') as f:
        image_data = f.read()
        return hashlib.md5(image_data).hexdigest()

def find_duplicate_images(directory):
    image_hashes = {}
    duplicate_images = []

    # Loop through all image files in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                file_path = os.path.join(root, filename)
                hash_value = image_hash(file_path)

                # Check if the hash is already in the dictionary
                if hash_value in image_hashes:
                    duplicate_images.append((file_path, image_hashes[hash_value]))
                else:
                    image_hashes[hash_value] = file_path

    return duplicate_images

# Specify the directory containing the images
image_directory = os.getcwd() + '\img'

# Find and print duplicate images
duplicate_images = find_duplicate_images(image_directory)
if duplicate_images:
    print("Duplicate Images Found:")
    for image1, image2 in duplicate_images:
        print(f"{image1} is a duplicate of {image2}")
else:
    print("No duplicate images found in the directory.")