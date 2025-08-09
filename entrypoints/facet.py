from ichatbio.types import AgentEntrypoint
import utils
from openai import OpenAI, AsyncOpenAI

import instructor
from instructor.exceptions import InstructorRetryException

from schema import facetsAPIParams
from tenacity import AsyncRetrying

import requests
import http

from ichatbio.agent import IChatBioAgent
from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentCard, AgentEntrypoint

from utils import search_helper as search
from utils import utils

entrypoint= AgentEntrypoint(
    id="facet",
    description="Returns record counts of one or more facets of species from OBIS",
    parameters=None
)


async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        await process.log("Generating search parameters for species facet")
        
        try:
            params = await search._generate_search_parameters(request, entrypoint, facetsAPIParams)
        except Exception as e:
            await process.log("Error generating params.")

            return
        
        await process.log("Generated search parameters", data=params)

        await process.log("Querying OBIS")
        try:
            
            url = utils.generate_obis_url("facet", params)
            await process.log(f"Sending a GET request to the OBIS occurrence API at {url}")

            response = requests.get(url)
            code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

            if response.ok:
                await process.log(f"Response code: {code}")
            else:
                await process.log(f"Response code: {code} - something went wrong!")
                return
            
            response_json = response.json()
            
            matching_count = response_json.get("total", 0)
            flag_count = len(response_json.get("results", {}))

            await process.log(
                text=f"The API query using URL {url} returned facets for {flag_count} of flags from OBIS"
            )

            await process.create_artifact(
                mimetype="application/json",
                description="OBIS data for the prompt: " + request,
                uris=[url],
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_flag_count": flag_count,
                    "total_matching_count": matching_count
                }
            )

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species occurrences.")
