months = ["Jän", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

date_formats = [
    'Y-m-d',     # 2023-10-25   
    'Y_m_d',     # 2023_10_25    
    'Y.m.d',     # 2023.05.15
    
    'Ymd',       # 20230712
    
    'd_m_Y',     # 05_08_2023
    'd-m-Y',     # 05-08-2023
    'd.m.Y',     # 08.03.2023
    
    'd_m_y',     # 05_08_23
    'd-m-y',     # 05-08-23
    'd.m.y',     # 08.03.23
    
    'dmY',       # 29022023
    'dmy',       # 290223
]

date_regex_replacements = {
    'd': r'\d{1,2}',
    'Y': r'\d{4}',
    'y': r'\d{2}',
    'm': r'\d{1,2}',
    '[_\-\.]': r'[_\-\.]'
}

image_extensions = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.tif',
    '.tiff',
    '.webp',
    '.heic',
    '.svg',
    '.raw',
    '.ico',
    '.eps',
    '.nef'
]

video_extensions = [
    '.mp4',
    '.mov',
    '.mkv',
    '.avi',
    '.wmv',
    '.flv',
    '.webm',
    '.3gp',
    '.m4v',
    '.mpg',
    '.mpeg',
    '.mts',
    '.m2ts',
    '.ts',
    '.vob'
]

media_extensions = image_extensions + video_extensions

# Convert date format into a regular expression
def format_to_regex(date_format):
    regex_format = date_format
    
    for pattern, replacement in date_regex_replacements.items():
        regex_format = regex_format.replace(pattern, replacement)

    return f"^{regex_format}$"

# Create an array of regular expressions
date_format_regexes = [format_to_regex(date_format) for date_format in date_formats]