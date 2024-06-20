import argparse
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description="Sort-O-Matic is a Python script that organizes images into yearly and monthly folders based on filename information, EXIF data, and file properties")
    parser.add_argument("--source", type=str, default="assets", help="Sourcepath to folder which contains images")
    parser.add_argument("--target", type=str, default="output", help="Targetpath, where images get moved to")
    parser.add_argument("-m", "--move", action="store_true", help="Move files instead of copying them")

    return parser.parse_args()