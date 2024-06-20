from PIL import Image, ImageChops

def are_images_equal(image1_path, image2_path):
    try:
        # Open the images using Pillow
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)

        # Check if the dimensions of the images are the same
        if img1.size != img2.size:
            return False

        # Compare pixel-by-pixel
        diff = ImageChops.difference(img1, img2)
        return diff.getbbox() is None

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

# Example usage
image1_path = 'img/1.jpg'
image2_path = 'img/2.jpg'

if are_images_equal(image1_path, image2_path):
    print("The images are equal.")
else:
    print("The images are not equal.")