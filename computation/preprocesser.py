# This file will contain the preprocessing functions for the data.
import re

def remove_special_characters(body):
    clean_string = re.sub(r'[^\x00-\x7F]+|[\x00-\x1F\x7F-\x9F]+|\s+', ' ', body)
    return clean_string.strip()

def convert_to_string_and_cleanup(record):
    body = record["body"]
    string = str(body)
    string = string[1:-1]
    string = remove_special_characters(string)
    string = string.replace('<p>', ' ')
    string = string.replace('</p>', ' ')
    string = string.replace('<div>', ' ')
    string = string.replace('</div>', ' ')
    string = string.replace('<br>', ' ')
    string = string.replace('<https:>', ' ')
    string = string.replace('</https:>', ' ')
    string = string.strip()
    record["body"] = string
    return record

def combine_subject_and_body(record): # That's how the data was in the training set
    subject = record["subject"]
    body = record["body"]
    string = f'Subject: {subject} {body}'
    record["msg"] = string
    return record
