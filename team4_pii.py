from scan import scan_files, get_file_text
import re


# https://developers.google.com/edu/python/regular-expressions
# https://regex101.com/
def find_us_phone_numbers(text):
    match = re.search(r'(\d{3}[-.]\d{3}[-.]\d{4})', text)
    if match:
        return True
    return False


def find_twitter_usernames(text):
    match = re.search(r'\B@\w*([A-Za-z0-9_]+)\w*', text)
    if match:
        return True
    return False


def find_email_handle(text):
    match = re.search(r'^([^.@]+)(\.[^.@]+)*@([^.@]+\.)+([^.@]+)$', text)
    if match:
        return True
    return False
