from scan import scan_files, get_file_text
import re


# https://regex101.com/
# https://developers.google.com/edu/python/regular-expressions

def find_name(text):
    match = re.search(r'([a-zA-Z]{2,25}\s([a-zA-Z]{2,25}))', text)
    if match:
        return True
    return False
