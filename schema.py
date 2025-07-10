from pydantic import BaseModel, field_validator, Field
from typing import Optional
from datetime import datetime

class occurrenceApi(BaseModel):
    scientificname: Optional[str] = Field(None, 
                                          description="full scientific name", 
                                          examples=["Delphinus delphis", "Alosa pseudoharengus"])
    taxonid: Optional[str] = Field(None, description="Taxon AphiaID.")
    datasetid: Optional[str] = Field(None, description="dataset UUID")
    startdate: Optional[str] = Field(None, 
                                     description="Start date of query. Fetch records after this date. Should be of format YYYY-MM-DD")
    enddate: Optional[str] = Field(None, 
                                   description="End date of query. Fetch records before this date. Should be of format YYYY-MM-DD. Should be greater than startdate")
    areaid: Optional[str] = Field(None, description="")
    instituteid: Optional[str] = Field(None, description="")
    nodeid: Optional[str] = Field(None, description="")
    startdepth: Optional[int] = Field(None, 
                                      description="start depth of creature instance recorded in meters")
    enddepth: Optional[int] = Field(None, description="")
    geometry: Optional[str] = Field(None, description="")
    absence: Optional[str] = Field(None, 
                                   description="Include absence records (include) or get absence records exclusively (true).")
    id: Optional[str] = Field(None, description="ID of the record that needs to be fetched")

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


class checklistApi(BaseModel):
    scientificname: Optional[str] = Field(None, 
                                          description="full scientific name", 
                                          examples=["Delphinus delphis", "Alosa pseudoharengus"])
    taxonid: Optional[str] = Field(None, description="Taxon AphiaID.")
    datasetid: Optional[str] = Field(None, description="dataset UUID")
    startdate: Optional[str] = Field(None, 
                                     description="Start date of query. Fetch records after this date. Should be of format YYYY-MM-DD")
    enddate: Optional[str] = Field(None, 
                                   description="End date of query. Fetch records before this date. Should be of format YYYY-MM-DD. Should be greater than startdate")
    areaid: Optional[str] = Field(None, description="")
    instituteid: Optional[str] = Field(None, description="")
    nodeid: Optional[str] = Field(None, description="")
    startdepth: Optional[int] = Field(None, 
                                      description="start depth of creature instance recorded in meters")
    enddepth: Optional[int] = Field(None, description="")
    geometry: Optional[str] = Field(None, description="")
    absence: Optional[str] = Field(None, 
                                   description="Include absence records (include) or get absence records exclusively (true).")

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