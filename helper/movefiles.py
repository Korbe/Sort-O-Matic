import shutil
import os

# List of file paths
file_paths = [
    r"D:\FinalMedia\2022\06-Jun\2022-06-26_23.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-26_24.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-26_25.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-27.jpeg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-27_4.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-27_5.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-28_7.jpg",
    r"D:\FinalMedia\2022\06-Jun\2022-06-29_4.jpg",
    r"D:\FinalMedia\2022\08-Aug\2022-08-15.jpg",
    r"D:\FinalMedia\2022\08-Aug\2022-08-15_2.jpg",
    r"D:\FinalMedia\2022\08-Aug\2022-08-15_2.jpg"
]

# Destination directory
destination_dir = r"D:\Development\Sort-O-Matic\assets\errordFiles"

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Move each file to the destination directory
for file_path in file_paths:
    try:
        shutil.move(file_path, destination_dir)
        print(f"Moved: {file_path}")
    except Exception as e:
        print(f"Error moving {file_path}: {e}")

print("All files processed.")
