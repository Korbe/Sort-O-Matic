# Sort-O-Matic
Sort-O-Matic is a Python script that organizes images into yearly and monthly folders based on filename information and properties and EXIF data. It recursively searches for the oldest available timestamp and sorts the media file in this directory

## Download Python
[Python download](https://www.python.org/downloads/)

## Install packages

    py -m pip install -r requirements.txt

## Start the program

    py sort-o-matic.py -s pathToSource -t pathToTarget


For **help** of the command line parameters enter
    
    py sort-o-matic.py -h



### For video meta data datetime retrieval

**should already be in the root dir**

you need ffprobe.exe in the root directory
download here [FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases) 
