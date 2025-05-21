import os
import yaml
from pydantic import BaseModel, field_validator, ValidationError
from datetime import datetime
import requests
from openai import OpenAI
import json
from typing import Optional
from urllib.parse import urlencode

class occurrenceApi(BaseModel):
    scientificname: Optional[str] = None
    taxonid: Optional[str] = None
    datasetid: Optional[str] = None
    startdate: Optional[str] = None
    enddate: Optional[str] = None

    @field_validator('startdate', 'enddate')
    def validate_date_format(cls, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")


class obis:
    def __init__(self):
        self.api_key = self.getValue("OPEN_API_KEY")
        self.obis_url = self.getValue("OBIS_URL")
        self.prompt = ""
        self.payload = ""
        self.error = ""

    def getApiPayload(self):
        if len(self.prompt) == 0:
            return
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": self.prompt}],
            temperature=0
        )

        # if response.status_code != 200:
        #     print("Error:", response.status_code, response.text)

        # print(response.choices[0].message.content)
        self.payload = response.choices[0].message.content
        return 0
    
    def extract_params_dict(self):
        if len(self.payload) == 0:
            return
        data = json.loads(self.payload)
        self.payload = urlencode(data)

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

            Return only the python dictionary
        """

    def verify_payload(self):
        try:
            m = occurrenceApi.model_validate_json(self.payload)
            print(m)
        except ValidationError as e:
            print(e)

    def query_obis_api(self):
        print(self.getPayload())
        response = requests.get(self.obis_url+'/occurrence?'+self.payload)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"OBIS API error {response.status_code}: {response.text}")
        return None


    def getValue(self, key):
        value = os.getenv(key)

        if value == None:
            with open('env.yaml', 'r') as file:
                data = yaml.safe_load(file)
            
            value = data[key]

        return value
    
    def getPayload(self):
        return self.payload
    
    def getApiKey(self):
        return self.api_key


if __name__=="__main__":
    obis = obis()
    userInput = input("Enter Search Query: \n")
    obis.build_prompt(user_input=userInput)
    obis.getApiPayload()
    obis.verify_payload()
    print(obis.getPayload())
    obis.extract_params_dict()
    print(obis.query_obis_api())
