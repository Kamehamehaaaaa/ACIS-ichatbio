from ichatbio.types import AgentEntrypoint
# from ichatbio.types import Message, TextMessage, ProcessMessage, ArtifactMessage
import utils
from openai import OpenAI, AsyncOpenAI

import instructor
from instructor.exceptions import InstructorRetryException

from schema import statisticsApi
from tenacity import AsyncRetrying

import requests
import http

from ichatbio.agent import IChatBioAgent
from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentCard, AgentEntrypoint

from utils import search_helper as search
from utils import utils

from entrypoints import statistics

entrypoint= AgentEntrypoint(
    id="statistics_year",
    description="Gets number of presence records of species per year from OBIS",
    parameters=None
)


async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        await process.log("Generating search parameters for statistics of species by year")
        
        try:
            # pass parent entrypoint for extensions
            params = await search._generate_search_parameters(request, statistics.entrypoint, statisticsApi)
        except Exception as e:
            await process.log("Error generating params.")

            return
        
        await process.log("Generated search parameters", data=params)

        await process.log("Querying OBIS")
        try:
            
            url = utils.generate_obis_extension_url("statistics", params, "years", True)
            await process.log(f"Sending a GET request to the OBIS statistics API at {url}")

            response = requests.get(url)
            code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

            if response.ok:
                await process.log(f"Response code: {code}")
            else:
                await process.log(f"Response code: {code} - something went wrong!")
                return
            
            response_json = response.json()

            await process.log(
                text=f"The API query using URL {url} returned statistics for species from OBIS"
            )

            record_count = response_json.get("records", 0)

            await process.log(response_json)

            await process.create_artifact(
                mimetype="application/json",
                description="OBIS data for the prompt: " + request,
                uris=[url],
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_record_count": record_count
                }
            )

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species statistics.")
