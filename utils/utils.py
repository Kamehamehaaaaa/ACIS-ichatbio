import importlib
import os
import yaml
from urllib.parse import urlencode

def getValue(key):
    value = os.getenv(key)

    if value == None:
        with open('env.yaml', 'r') as file:
            data = yaml.safe_load(file)
        
        value = data[key]

    return value

def generate_obis_url(api, payload):
    params = urlencode(payload)
    obis_url = "https://api.obis.org/"
    url = obis_url+api+'?'+params
    return url