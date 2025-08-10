from pydantic import BaseModel, field_validator, Field, constr, conint
from typing import Optional, Annotated, Literal, Required
from datetime import datetime

class occurrenceApi(BaseModel):

    scientificname: Optional[str] = Field(None, 
                                          description="Scientific name. Leave empty to include all taxa.", 
                                          examples=["Delphinus delphis", "Alosa pseudoharengus"])
    taxonid: Optional[str] = Field(None, description="Taxon AphiaID.")
    datasetid: Optional[str] = Field(None, description="Dataset UUID.")
    areaid: Optional[str] = Field(None, description="Area ID.")
    instituteid: Optional[str] = Field(None, description="Institute ID.")
    nodeid: Optional[str] = Field(None, description="Node UUID.")
    
    startdate: Optional[str] = Field(None, description="Start date formatted as YYYY-MM-DD. Fetch records after this date.")
    enddate: Optional[str] = Field(None, description="End date formatted as YYYY-MM-DD.")
    
    startdepth: Optional[int] = Field(None, description="Start depth, in meters.")
    enddepth: Optional[int] = Field(None, description="End depth, in meters.")
    
    geometry: Optional[str] = Field(None, description="Geometry, formatted as WKT or GeoHash.")
    
    redlist: Optional[bool] = Field(None, description="Red List species only, true/false.")
    hab: Optional[bool] = Field(None, description="HAB species only, true/false.")
    wrims: Optional[bool] = Field(None, description="WRiMS species only, true/false.")
    mof: Optional[bool] = Field(None, description="Include MeasurementOrFact records, true/false.")
    dna: Optional[bool] = Field(None, description="Include DNADerivedData records, true/false.")
    
    extensions: Optional[str] = Field(None, description="Extensions to include (e.g. MeasurementOrFact, DNADerivedData).")
    hasextensions: Optional[str] = Field(None, description="Extensions that need to be present (e.g. MeasurementOrFact, DNADerivedData).")
    
    qcfields: Optional[bool] = Field(None, description="Include lists of missing and invalid fields, true/false.")
    dropped: Optional[str] = Field(None, description="Include dropped records (include) or get dropped records exclusively (true).")
    absence: Optional[str] = Field(None, description="Include absence records (include) or get absence records exclusively (true).")
    event: Optional[str] = Field(None, description="Include pure event records (include) or get pure event records exclusively (true).")
    
    flags: Optional[str] = Field(None, description="Comma separated list of quality flags which need to be set.")
    exclude: Optional[str] = Field(None, description="Comma separated list of quality flags to be excluded.")
    
    fields: Optional[str] = Field(None, description="Fields to be included in the result set.")
    after: Optional[str] = Field(None, description="Occurrence UUID up to which to skip.")
    size: Optional[int] = Field(None, description="Response size.")
    
    measurementtype: Optional[str] = Field(None, description="Measurement type to be present for occurrence.")
    measurementtypeid: Optional[str] = Field(None, description="Measurement type ID to be present for occurrence.")
    measurementvalue: Optional[str] = Field(None, description="Measurement value to be present for occurrence.")
    measurementvalueid: Optional[str] = Field(None, description="Measurement value ID to be present for occurrence.")
    measurementunit: Optional[str] = Field(None, description="Measurement unit to be present for occurrence.")
    measurementunitid: Optional[str] = Field(None, description="Measurement unit ID to be present for occurrence.")

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


class occurrenceLookupApi(BaseModel):
    id: Optional[str] = Field(None, description="occurrence record id",
                              examples=["00000002-3cef-4bc1-8540-2c20b4798855"])

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
    

class statisticsApi(BaseModel):
    scientificname: Optional[Annotated[str, Field(description="Scientific name. Leave empty to include all taxa.")]] = None
    taxonid: Optional[Annotated[str, Field(description="Taxon AphiaID.")]] = None
    areaid: Optional[Annotated[str, Field(description="Area ID.")]] = None
    datasetid: Optional[Annotated[str, Field(description="Dataset UUID.")]] = None
    nodeid: Optional[Annotated[str, Field(description="Node UUID.")]] = None

    startdate: Optional[Annotated[str, Field(description="Start date formatted as YYYY-MM-DD.")]] = None
    enddate: Optional[Annotated[str, Field(description="End date formatted as YYYY-MM-DD.")]] = None

    startdepth: Optional[Annotated[int, Field(ge=0, description="Start depth, in meters (must be >= 0).")]] = None
    enddepth: Optional[Annotated[int, Field(ge=0, description="End depth, in meters (must be >= 0).")]] = None

    geometry: Optional[Annotated[str, Field(description="Geometry, formatted as WKT or GeoHash.")]] = None

    redlist: Optional[Annotated[bool, Field(description="Red List species only.")]] = None
    hab: Optional[Annotated[bool, Field(description="HAB species only.")]] = None
    wrims: Optional[Annotated[bool, Field(description="WRiMS species only.")]] = None

    dropped: Optional[Annotated[Literal["include", "true"], Field(description="Include dropped records or only dropped.")]] = None
    absence: Optional[Annotated[Literal["include", "true"], Field(description="Include absence records or only absence.")]] = None

    flags: Optional[Annotated[str, Field(description="Comma-separated list of quality flags to include.")]] = None
    exclude: Optional[Annotated[str, Field(description="Comma-separated list of quality flags to exclude.")]] = None

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
    

class facetsAPIParams(BaseModel):
    facets: Required[list] = Field(None, description="Comma separated list of facets", examples= ["originalScientificName,flags", "node_id"])
    composite: Optional[bool] = Field(None, description="Composite aggregation")
    scientificname: Optional[str] = Field(None, description="Scientific name. Leave empty to include all taxa", examples=["brachyura", "Cancer borealis"])
    taxonid: Optional[str] = Field(None, description="Taxon AphiaID")
    areaid: Optional[str] = Field(None, description="Area ID")
    datasetid: Optional[str] = Field(None, description="Dataset UUID")
    nodeid: Optional[str] = Field(None, description="Node UUID")
    startdate: Optional[str] = Field(None, description="Start date formatted as YYYY-MM-DD")
    enddate: Optional[str] = Field(None, description="End date formatted as YYYY-MM-DD")
    startdepth: Optional[int] = Field(None, ge=0, description="Start depth in meters")
    enddepth: Optional[int] = Field(None, ge=0, description="End depth in meters")
    geometry: Optional[str] = Field(None, description="Geometry, formatted as WKT or GeoHash", examples=["POLYGON((140 -40, 150 -40, 150 -30, 140 -30, 140 -40))"])
    redlist: Optional[bool] = Field(None, description="Red List species only")
    hab: Optional[bool] = Field(None, description="HAB species only")
    wrims: Optional[bool] = Field(None, description="WRiMS species only")
    dropped: Optional[str] = Field(None, description="Include dropped records (include) or only dropped (true)")
    absence: Optional[str] = Field(None, description="Include absence records (include) or only absence (true)")
    flags: Optional[str] = Field(None, description="Comma separated list of quality flags which need to be set")
    exclude: Optional[str] = Field(None, description="Comma separated list of quality flags to be excluded")

    @field_validator('startdate', 'enddate')
    def validate_date_format(cls, value):
        if value is None:
            return value
        allowed_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y"]
        for fmt in allowed_formats:
            try:
                dt = datetime.strptime(value, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError("Incorrect date format. Allowed: YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY")

    @field_validator('enddepth')
    def validate_depth_range(cls, value, values):
        start_depth = values.get('startdepth')
        if start_depth is not None and value is not None and value < start_depth:
            raise ValueError("enddepth must be greater than or equal to startdepth")
        return value