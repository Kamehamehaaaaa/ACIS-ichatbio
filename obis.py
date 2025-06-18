import os
import yaml
from pydantic import BaseModel, field_validator, ValidationError
from pydantic import Field
from datetime import datetime
import requests
from openai import OpenAI, AsyncOpenAI
import json
from typing import Optional, Literal, override, AsyncGenerator
from urllib.parse import urlencode

import instructor
from instructor.exceptions import InstructorRetryException

from ichatbio.agent import IChatBioAgent
from ichatbio.types import AgentCard, AgentEntrypoint
from ichatbio.types import Message, TextMessage, ArtifactMessage

import a2a.types
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from ichatbio.agent_executor import IChatBioAgentExecutor

from ichatbio.server import run_agent_server

import asyncio


class occurrenceApi(BaseModel):
    scientificname: Optional[str] = None
    taxonid: Optional[str] = None
    datasetid: Optional[str] = None
    startdate: Optional[str] = None
    enddate: Optional[str] = None
    areaid: Optional[str] = None
    instituteid: Optional[str] = None
    nodeid: Optional[str] = None
    startdepth: Optional[int] = None
    enddepth: Optional[int] = None
    geometry: Optional[str] = None
    id: Optional[str] = None

    @field_validator('startdate', 'enddate')
    def validate_date_format(cls, value):
        allowed_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for format in allowed_formats:
            try:
                dt = datetime.strptime(value, format)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError("Incorrect date format. Allowed formats: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY")


class OBISAgent(IChatBioAgent):
    def __init__(self):
        self.api_key = getValue("OPEN_API_KEY")
        self.client = None
        self.prompt = ""
        self.payload = ""
        self.agent_card = AgentCard(
            name="Ocean Biodiversity Information Systems data source",
            description="Retrieves data from OBIS.",
            icon=None,
            entrypoints=[
                AgentEntrypoint(
                    id="get_occurrence",
                    description="Returns occurrence of species from OBIS",
                    parameters=None
                )
            ],
        )

    @override
    def get_agent_card(self) -> AgentCard:
        return self.agent_card
    
    @override
    async def run(self, request: str, entrypoint: str, params: Optional[BaseModel], **kwargs) -> AsyncGenerator[Message, None]:
        if not entrypoint == "get_occurrence":
            # Complain
            pass


        try:
            self.build_prompt(request)
            
            self.client = AsyncOpenAI(api_key=self.api_key)
            yield TextMessage(text="OBIS client initialized.")

            print(self.client)
            
            instructor_client = instructor.patch(self.client)

            req: occurrenceApi = await instructor_client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_model=occurrenceApi,
                messages=[
                    {"role": "system",
                        "content": "You are an assistant that generates query parameters for the OBIS API's `/occurrence` endpoint."},
                    {"role": "user", "content": self.prompt}],
                temperature=0
            )
# instructor issue capture
            print(self.agent_card.entrypoints[0].id)

            obis_query = OBISRequest(obis_url=getValue("OBIS_URL"), payload=req)
            url = obis_query.query_obis_api()
            response = requests.get(url)

            yield TextMessage(text="OBIS data received.")
            yield ArtifactMessage(
                mimetype="text/html",
                description="OBIS data for the prompt: " + self.prompt ,
                content=response.content,
                metadata={
                    "api_query_url": url
                }
            )

        except InstructorRetryException as e:
            print(e)
            yield TextMessage(text="Sorry, I couldn't find any species occurrences.")


    def initializeAgent(self):
        self.client = AsyncOpenAI(api_key=self.api_key)
        yield TextMessage(text="OBIS client initialized.")


    # async def executeAgent(self, params: Optional[BaseModel]):
    #     instructor_client = instructor.patch(self.client)

    #     req: OBISRequest = await instructor_client.chat.completions.create(
    #         model="gpt-3.5-turbo",
    #         response_model=OBISRequest,
    #         messages=[
    #             {"role": "system",
    #                 "content": "You are an assistant that generates query parameters for the OBIS API's `/occurrence` endpoint."},
    #             {"role": "user", "content": self.prompt}],
    #         temperature=0
    #     )

    #     url = req.query_obis_api(params.format)
    #     response = requests.get(url)

    #     yield TextMessage(text="OBIS data received.")
    #     yield ArtifactMessage(
    #         mimetype="text/html",
    #         description="OBIS data for the prompt: " + self.prompt ,
    #         content=response.content,
    #         metadata={
    #             "api_query_url": url
    #         }
    #     )

    def build_prompt(self, user_input):
        if user_input == None or len(user_input) == 0:
            return
        
        self.prompt = f"""
            You are an assistant that generates query parameters for the OBIS API's `/occurrence` endpoint.
            Given a natural language request, extract the relevant parameters and return a valid Python dictionary named `params`. 
            The natural language input is: {user_input}

            Supported parameters:
            - `scientificname`: full scientific name (e.g., "Delphinus delphis")
            - `taxonid`: Taxon AphiaID.
            - `datasetid`: dataset UUID
            - `startdate`: start date of query
            - `enddate`: end date of query
            - `areaid`: area id.
            - `instituteid`: institute id
            - `nodeid`: node id
            - `startdepth`: start depth of creature instance recorded in meters
            - `enddepth`: end depth of creature instance recorded in meters
            - `geometry`: geometry formatted as WKT or GeoHash

            Return only the python dictionary
        """

def getValue(key):
    value = os.getenv(key)

    if value == None:
        with open('env.yaml', 'r') as file:
            data = yaml.safe_load(file)
        
        value = data[key]

    return value

class OBISRequest(BaseModel):

    # supportsAuthenticatedExtendedCard: bool = False

    obis_url: str
    payload: occurrenceApi

    def query_obis_api(self):
        params = urlencode(self.payload.model_dump(exclude_none=True))
        obis_url = "https://api.obis.org"
        url = obis_url+'/occurrence?'+params
        return url


async def main():
    response = agent.run(userInput, "get_occurrence", occurrenceApi())
    messages = [m async for m in response]
    print(messages)

if __name__=="__main__":
    agent = OBISAgent()
    userInput = input("Enter Search Query: \n")
    # obis.build_prompt(user_input=userInput)
    # run_agent_server(agent, host="127.0.0.1", port=8080)
    asyncio.run(main())
    # obis.getApiPayload()
    # obis.verify_payload()
    # print(obis.getPayload())
    # obis.extract_params_dict()
    # print(obis.query_obis_api())
