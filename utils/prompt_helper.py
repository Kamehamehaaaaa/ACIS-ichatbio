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

    query_format_doc = importlib.resources.files().joinpath("../resources", api+".md").read_text()
    examples_doc = importlib.resources.files().joinpath("../resources", api+"_examples.md").read_text()

    prompt = SYSTEM_PROMPT_TEMPLATE.format(
        api=api,
        query_format_doc=query_format_doc,
        examples_doc=examples_doc,
    ).strip()

    return prompt