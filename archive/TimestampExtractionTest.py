import unittest
from datetime import datetime
import re

date_formats = [
    '%Y-%m-%d',     # 2023-10-25   
    '%Y_%m_%d',     # 2023_10_25    
    '%Y.%m.%d',     # 2023.05.15
    '%Y%m%d',       # 20230712
    
    '%d-%m-%Y',     # 05-08-2023
    '%d.%m.%Y',     # 08.03.2023
    '%d-%m-%y',     # 05-08-23
    '%d.%m.%y',     # 08.03.23
    '%d%m%Y',       # 29022023
    '%d%m%y',       # 290223
]
#'%y_%m_%d',     # 23_06_23
#'%y-%m-%d',     # 23-10-25
#'%Y%m-%d',      # 202312-06
#'%y-%m%d',      # 23-1003
#'%Y-%m%d',      # 2023-0715
#'%Y%m/%d',      # 202303/22
#'%Y/%m/%d',     # 2023/11/30
#'%d/%m/%Y',     # 07/06/2023
#'%d/%m/%y',     # 04/01/23
#'%H-%M-%S_%d-%m-%Y',  # 13-45-22_05-08-2023
#'%Y%m%d-%H%M%S',      # 20230712-154322
#'%y%m%d',       # 230803
#'%y%m-%d',      # 231008-01
#'%y%m/%d',      # 230911/14
#'%Y%m%d%H%M%S',  # 20230815123456
#'%d%m%y%H%M%S',  # 290823123456
#'%Y%m%d%H%M',    # 202307121230

def extract_timestamp_from_filename(filename):
    for date_format in date_formats:
        pattern = date_format.replace('%d', r'\d{2}').replace('%m', r'\d{2}').replace('%Y', r'\d{4}') \
                             .replace('%y', r'\d{2}').replace('-', r'[-_/]').replace('.', r'[./_]')
        match = re.search(pattern, filename)
        if match:
            extracted_date = match.group()
            try:
                parsed_date = datetime.strptime(extracted_date, date_format)
                return parsed_date
            except ValueError:
                pass  # Invalid date for the current format
    return None

# Define unit tests
class TestExtractTimestampFromFilename(unittest.TestCase):
    def test_valid_filenames(self):
        filenames = [
            "23.11.2014.png",
            "2014.11.23.png",
            "20150510_124212.jpg",
            "file_05-08-2023.txt",
            "2023_10_25_document.pdf",
            "20230712-154322-report.txt",
        ]
        expected_dates = [
            datetime(2014, 11, 23),
            datetime(2014, 11, 23),
            datetime(2015, 5, 10),
            datetime(2023, 8, 5),
            datetime(2023, 10, 25),
            datetime(2023, 7, 12),
        ]

        for filename, expected_date in zip(filenames, expected_dates):
            with self.subTest(filename=filename):
                extracted_date = extract_timestamp_from_filename(filename)
                self.assertEqual(extracted_date, expected_date)

    def test_invalid_filenames(self):
        invalid_filenames = [
            "file_no_date.txt",
            "2023_99_99_invalid.txt",
            "invalid_date_20211501.txt",
        ]

        for filename in invalid_filenames:
            with self.subTest(filename=filename):
                extracted_date = extract_timestamp_from_filename(filename)
                self.assertIsNone(extracted_date)

if __name__ == "__main__":
    unittest.main()