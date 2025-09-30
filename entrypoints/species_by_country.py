from ichatbio.types import AgentEntrypoint
# from ichatbio.types import Message, TextMessage, ProcessMessage, ArtifactMessage
import utils
from openai import OpenAI, AsyncOpenAI

import instructor
from instructor.exceptions import InstructorRetryException

from schema import occurrenceApi
from entrypoints import get_occurrence

import requests
import http

from ichatbio.agent import IChatBioAgent
from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentCard, AgentEntrypoint

from utils import search_helper as search
from utils import utils

entrypoint= AgentEntrypoint(
    id="species_by_country",
    description="Get species occurrences records by country from OBIS",
    parameters=None
)

async def get_institutes_by_country(request, process):
    country_res = await search.get_country_from_request(request)

    url = utils.generate_obis_url("institute",{})

    response = requests.get(url)
    await process.log(url)
    code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

    if response.ok == False:
        await process.log("responses is not okay")
        return []

    results = response.json()["results"]
    institutes = []

    for result in results:
        if result["country"] == country_res["country"]:
            institutes.append(result["id"])

    return institutes


async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        institutes = await get_institutes_by_country(request, process)

        await process.log("Generating search parameters for occurrences of species")

        try:
            params = await search._generate_search_parameters(request, get_occurrence.entrypoint, occurrenceApi)
        except Exception as e:
            await process.log("Error generating params.")
            return

        if "areaid" in params:
            del params["areaid"]

        await process.log("Generated search parameters", data=params)

        await process.log("Querying OBIS")
        try:
            records = []
            for institute in institutes:
                params["instituteid"] = institute
                url = utils.generate_obis_url("occurrences", params)
                await process.log("updated params", data=params)
                response = requests.get(url)

                await process.log(url)

                response_json = response.json()

                if response_json == None:
                    continue

                records += response_json.get("results")

                await process.log(url)

            # await process.log(f"Sending a GET request to the OBIS statistics API at {url}")

            # await process.log(
            #     text=f"The API query using URL {url} returned statistics for species from OBIS"
            # )

            record_count = len(records)

            # await process.log(response_json)

            await process.create_artifact(
                mimetype="text/plain",
                description="OBIS data for the prompt: " + request,
                uris=[],
                content=bytes(records),
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_record_count": record_count
                }
            )

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species statistics.")
