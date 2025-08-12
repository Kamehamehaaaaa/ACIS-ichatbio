from ichatbio.types import AgentEntrypoint
import utils
from instructor.exceptions import InstructorRetryException

from schema import instituteSearch

import requests
import http

from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentEntrypoint

from utils import search_helper as search
from utils import utils

entrypoint= AgentEntrypoint(
    id="all_institutes",
    description="Get institute records from OBIS. No params returns all institutes supported by obis",
    parameters=None
)

async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        await process.log("Generating search parameters for fetching institute records")
        
        try:
            params = await search._generate_search_parameters(request, entrypoint, instituteSearch)
        except Exception as e:
            await process.log("Error generating params.")

            return
        
        await process.log("Generated search parameters", data=params)

        await process.log("Querying OBIS")
        try:
            
            url = utils.generate_obis_url("institute", params)
            await process.log(f"Sending a GET request to the OBIS institute API at {url}")

            response = requests.get(url)
            code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

            if response.ok:
                await process.log(f"Response code: {code}")
            else:
                await process.log(f"Response code: {code} - something went wrong!")
                return
            
            response_json = response.json()
            
            total_institutes = response_json.get("total", 0)

            await process.log(
                text=f"The API query using URL {url} returned {total_institutes} institute records in OBIS"
            )

            await process.create_artifact(
                mimetype="application/json",
                description="OBIS data for the prompt: " + request,
                uris=[url],
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_record_count": total_institutes,
                }
            )

            await context.reply(f"I have successfully searched for institutes and found {total_institutes} records. I've created an artifact with the results.")

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species occurrences.")
