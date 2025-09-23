from ichatbio.types import AgentEntrypoint
# from ichatbio.types import Message, TextMessage, ProcessMessage, ArtifactMessage
import utils
from openai import OpenAI, AsyncOpenAI

import instructor
from instructor.exceptions import InstructorRetryException

from schema import occurrenceApi
from tenacity import AsyncRetrying

import requests
import http

from ichatbio.agent import IChatBioAgent
from ichatbio.agent_response import ResponseContext, IChatBioAgentProcess
from ichatbio.types import AgentCard, AgentEntrypoint

from utils import search_helper as search
from utils import utils

entrypoint= AgentEntrypoint(
    id="get_occurrence",
    description="Returns occurrence of species from OBIS",
    parameters=None
)

async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        place_res = await search.get_place_from_request(request)
        wkt = ""

        if "place" in place_res:
            wkt = await search.place_to_geohash_wkt(place_res["place"], 2)

        await process.log("Generating search parameters for species occurrences")
        
        try:
            params = await search._generate_search_parameters(request, entrypoint, occurrenceApi)
        except Exception as e:
            await process.log("Error generating params.")

            return

        await process.log("Initial params generated", data=params)
        
        if "areaid" in params:
            del params["areaid"]
            await process.log(wkt)
            wkt = str(wkt)
            wkt_updated = wkt.replace("POLYGON ", "POLYGON")
            params["geometry"] = wkt_updated
        
        await process.log("Generated search parameters", data=params)

        await process.log("Querying OBIS")
        try:
            
            url = utils.generate_obis_url("occurrence", params)
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
            record_count = len(response_json.get("results", []))


            #taxonid = response_json["results"][0]["infraorderid"]

            await process.log(
                text=f"The API query using URL {url} returned {record_count} out of {matching_count} matching records in OBIS"
            )

            await process.create_artifact(
                mimetype="application/json",
                description="OBIS data for the prompt: " + request,
                uris=[url],
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_record_count": record_count,
                    "total_matching_count": matching_count
                }
            )

            await process.log("Querying for point data ")
            url = utils.generate_obis_url("occurrence/points", params)
            await process.log(f"Sending a GET request to the OBIS occurrence API at {url}")

            response = requests.get(url)
            code = f"{response.status_code} {http.client.responses.get(response.status_code, '')}"

            if response.ok:
                await process.log(f"Response code: {code}")
            else:
                await process.log(f"Response code: {code} - something went wrong!")
                return

            response_json = response.json()

            record_count = len(response_json.get("coordinates", []))

            await process.log(
                text=f"The API query using URL {url} returned {record_count} points matching records in OBIS"
            )

            await process.create_artifact(
                mimetype="application/json",
                description="OBIS data for the prompt: " + request,
                uris=[url],
                metadata={
                    "data_source": "OBIS",
                    "portal_url": "portal_url",
                    "retrieved_record_count": record_count,
                }
            )
            await context.reply(f"I have successfully searched for occurrences and found {record_count} matching records. I've created an artifact with the results.")

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species occurrences.")
