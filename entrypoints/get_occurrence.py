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

# async def _generate_search_parameters(request: str):
#     system_prompt = utils.build_system_prompt(entrypoint.id)
        
#     client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"))
#     # yield TextMessage(text="OpenApi client initialized.")

#     print(client)
    
#     instructor_client = instructor.patch(client)

#     req: occurrenceApi = await instructor_client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         response_model=occurrenceApi,
#         messages=[
#             {"role": "system",
#                 "content": system_prompt},
#             {"role": "user", "content": request}],
#         temperature=0,
#     )

#     generation = req.model_dump(exclude_none=True, by_alias=True)
#     return generation


async def run(request: str, context: ResponseContext):

    # Start a process to log the agent's actions
    async with context.begin_process(summary="Searching Ocean Biodiversity Information System") as process:
        process: IChatBioAgentProcess

        await process.log("Generating search parameters for species occurrences")
        
        try:
            params = await search._generate_search_parameters(request, entrypoint, occurrenceApi)
        except Exception as e:
            await process.log("Error generating params.")

            return
        
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

            # print(code, matching_count, record_count)
            # print(response_json)

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

            # yield ArtifactMessage(
            #     mimetype="application/json",
            #     description="OBIS data for the prompt: " + request,
            #     uris=[url],
            #     content=response.content,
            #     metadata={
            #         "api_query_url": url
            #     }
            # )

        except InstructorRetryException as e:
            print(e)
            await process.log("Sorry, I couldn't find any species occurrences.")
