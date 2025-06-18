from ichatbio.types import AgentEntrypoint
from ichatbio.types import Message, TextMessage, ProcessMessage, ArtifactMessage
import utils
from openai import OpenAI, AsyncOpenAI

import instructor
from instructor.exceptions import InstructorRetryException

from schema import occurrenceApi
from tenacity import AsyncRetrying

import requests
import http


entrypoint= AgentEntrypoint(
    id="get_occurrence",
    description="Returns occurrence of species from OBIS",
    parameters=None
)

async def _generate_search_parameters(request: str):
    system_prompt = utils.build_system_prompt(entrypoint.id)
        
    client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"))
    # yield TextMessage(text="OpenApi client initialized.")

    print(client)
    
    instructor_client = instructor.patch(client)

    req: occurrenceApi = await instructor_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=occurrenceApi,
        messages=[
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": request}],
        temperature=0,
    )

    generation = req.model_dump(exclude_none=True, by_alias=True)
    return generation


async def run(request: str):

    yield ProcessMessage(summary="Searching Ocean Biodiversity Information System",
                         description="Generating search parameters for species occurrences")
    
    try:
        params = await _generate_search_parameters(request)
    except Exception as e:
        yield ProcessMessage("Error generating params.")

        return
    
    yield ProcessMessage(description=f"Generated search parameters", data=params)

    try:
        
        url = utils.generate_obis_url("occurrence", params)
        yield ProcessMessage(description=f"Sending a GET request to the OBIS occurrence API at {url}")

        response = requests.get(url)
        code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

        if response.ok:
            yield ProcessMessage(description=f"Response code: {code}")
        else:
            yield ProcessMessage(description=f"Response code: {code} - something went wrong!")
            return
        
        response_json = response.json()
        
        matching_count = response_json.get("total", 0)
        record_count = len(response_json.get("results", []))

        print(code, matching_count, record_count)

        yield TextMessage(
            text=f"The API query using URL {url} returned {record_count} out of {matching_count} matching records in OBIS"
        )

        yield ArtifactMessage(
            mimetype="application/json",
            description="OBIS data for the prompt: " + request,
            uris=[url],
            metadata={
                "data_source": "OBIS",
                "portal_url": "",
                "retrieved_record_count": record_count,
                "total_matching_count": matching_count
            }
        )

    except InstructorRetryException as e:
        print(e)
        yield TextMessage(text="Sorry, I couldn't find any species occurrences.")
