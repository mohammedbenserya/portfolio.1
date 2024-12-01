# myapp/services/google_lens.py

import requests
import re
import json
from bs4 import BeautifulSoup

def upload_to_google_lens(image_file):
    url = 'https://lens.google.com/v3/upload'
    params = {
        'hl': 'en-MA',
        're': 'df',
        'st': '1732827546007',
        'vpw': '928',
        'vph': '755',
        'ep': 'subb'
    }
    response = requests.post(
        url,
        params=params,
        files={'encoded_image': ('image.jpg', image_file.read(), 'image/jpeg')}
    )
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def parse_af_callback_data(text):
    """
    Parse AF_initDataCallback format text into a Python dictionary.
    """
    match = re.search(r'AF_initDataCallback\((.*)\);$', text)
    if not match:
        raise ValueError("Invalid input format: Expected AF_initDataCallback format")
    data_str = match.group(1)
    data_str = re.sub(r'([{,])\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*:', r'\1"\2":', data_str)
    data_str = data_str.replace("'", '"')
    data_str = data_str.replace('undefined', 'null')
    data = json.loads(data_str)
    return data

def get_match(parsed_data):
    text_data = ""
    for item in parsed_data.get('data', []):
        if isinstance(item, list) and len(item) > 4 and isinstance(item[3], str):
            text_data += "\n".join(item[4][0][0])
    return  text_data






