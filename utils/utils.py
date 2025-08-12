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
    if api == "facet":
        tmp = payload["facets"]
        facets = tmp[0]
        for i in tmp[1:]:
            facets = facets + "," + i
        payload["facets"] = facets
    params = urlencode(payload)
    obis_url = "https://api.obis.org/"
    url = obis_url+api+'?'+params
    return url

def generate_obis_extension_url(api, payload, extensionParam, paramsRequired):
    try:
        extensionValue = payload.pop(extensionParam)
    except Exception as e:
        return ""

    params = urlencode(payload)
    obis_url = "https://api.obis.org/"
    if paramsRequired:
        url = obis_url+api+"/"+extensionValue+'?'+params
    else:
        url = obis_url+api+"/"+extensionValue
    return url

def generate_mapper_obis_url(api, payload):
    params = urlencode(payload)
    obis_url = "https://mapper.obis.org/"
    url = obis_url+api+'?'+params
    return url