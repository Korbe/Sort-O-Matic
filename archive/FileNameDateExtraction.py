import re
from datetime import datetime

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



def getDateFromString(datestring : str, date_format : str) -> datetime|None:
    try:
        return datetime.strptime(datestring, date_format)
    except Exception as error:
        pass
    
    return None


date_regex_replacements = {
    'd': r'\d{1,2}',
    'Y': r'\d{4}',
    'y': r'\d{2}',
    'm': r'\d{1,2}',
    '.': r"\.",
}

# Convert date format into a regular expression
def format_to_regex(date_format):
    regex_format = date_format
    
    for pattern, replacement in date_regex_replacements.items():
        regex_format = regex_format.replace(pattern, replacement)

    return regex_format

# Create an array of regular expressions
date_format_regexes = [format_to_regex(format) for format in date_formats]
datetime_formats = [format.replace('Y','%Y').replace('y','%y').replace('m','%m').replace('d','%d') for format in date_formats]

# Example filenames
example_filenames = [
    "file_1.1.2023.txt",
    "data_2023-01-15.csv",
    "report_15/02/22.pdf",
    "log_21.03.19.txt",
    "document_3 February 2022.docx",
    "invoice_2023/03/18.pdf",
    "photo_23.07.1998.jpg",
    "letter_10-July-2021.doc",
    "birthday_25.Dec.98.txt",
    "event_2022 March 12.pptx",
    "booking_2022-08-05.csv",
    "receipt_31.01.22.pdf",
    "memo_10-05-21.txt",
    "presentation_22.June.2023.pptx",
    "2023-10-25",
    "2023_10_25",
    "2023.05.15",
    "20230712",
    "05_08_2023",
    "05-08-2023",
    "08.03.2023",
    "05_08_23",
    "05-08-23",
    "08.03.23",
    "29022023",
    "290223",
    
    'document_31.12.23.txt',
    'report_05.11.23.pdf',
    'file_11.05.23.doc',
    'presentation_23.12.2023.ppt',
    'memo_05.11.23.txt',
    'assignment_23.05.2023.docx',
    'data_05.11.23.csv',
    'note_31.12.2023.txt',
    'project_23.12.2023.doc',
    'log_05.11.23.txt',
    'record_23.05.2023.doc',
    'invoice_05.11.23.pdf',
    'agenda_23.05.2023.docx',
    'plan_05.11.23.txt',
    'letter_23.12.2023.doc',
    'spreadsheet_05.11.23.xls',
    'contract_23.05.2023.pdf',
    'article_05.11.23.txt',
    'presentation_31.12.2023.pptx',
    'summary_23.12.2023.doc',
    'manual_05.11.23.pdf',
    'draft_23.05.2023.txt',
    'document_05.11.23.docx',
    'report_23.12.2023.pdf',
    'file_05.11.23.doc',
    'memo_23.05.2023.txt',
    'assignment_05.11.23.docx',
    'data_23.12.2023.csv',
    'note_05.11.23.txt',
    'project_23.12.2023.doc',
    'log_05.11.23.txt',
    'record_23.05.2023.doc',
    'invoice_05.11.23.pdf',
    'agenda_23.12.2023.docx',
    'plan_05.11.23.txt',
    'letter_23.12.2023.doc',
    'spreadsheet_05.11.23.xls',
    'contract_23.05.2023.pdf',
    'article_05.11.23.txt',
    'presentation_31.12.23.pptx',
    'summary_23.12.2023.doc',
    'manual_05.11.23.pdf',
    'draft_23.05.2023.txt',
    'document_05.11.23.docx',
    'report_23.12.2023.pdf',
    'file_05.11.23.doc',
    'memo_23.05.2023.txt',
    'assignment_05.11.23.docx',
    'data_23.12.2023.csv',
    'note_05.11.23.txt',
]

def getDateTimeDetails(string) -> (str|None, str|None, datetime|None):
    
    format = None
    match = None
    
    for i, pattern in enumerate(date_format_regexes):
        regMatch = re.search(pattern, string)
        if regMatch:
            try:
                match = regMatch.group()
                format = date_formats[i]

                return match, format, datetime.strptime(match, datetime_formats[i])
            
            except Exception as exception:
                pass
            
    return match, format, None


dates_found = []
dates_not_found = []

# Test the example filenames
for filename in example_filenames:
    matched, format, date = getDateTimeDetails(filename)
    if date:
        dates_found.append(f"Filename:\t {filename}\nDate:\t\t {matched}\tFormat {format} converts to => {date}\n")
    else:
        dates_not_found.append(f"Filename:\t {filename}\t\tMatched: {matched}\tFormat {format} converts to => {date}\n")
        


for text in dates_found:
    print(text);
    
print("\n\n");
    
for text in dates_not_found:
    print(text);




