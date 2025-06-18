import importlib
import os
import yaml
from urllib.parse import urlencode

def build_system_prompt(api):
    SYSTEM_PROMPT_TEMPLATE = """
        You translate user requests into parameters for the OBIS {api} API.

        # Query format

        Here is a description of how iDigBio queries are formatted:

        [BEGIN QUERY FORMAT DOC]

        {query_format_doc}

        [END QUERY FORMAT DOC]

        # Examples

        {examples_doc}
    """

    query_format_doc = importlib.resources.files().joinpath("resources", api+".md").read_text()
    examples_doc = importlib.resources.files().joinpath("resources", api+"_examples.md").read_text()

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        api=api,
        query_format_doc=query_format_doc,
        examples_doc=examples_doc,
    ).strip()

    return prompt


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