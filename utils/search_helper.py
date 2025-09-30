from openai import AsyncOpenAI
from utils import prompt_helper as prompt
from utils import utils as utils
import instructor
from ichatbio.types import AgentEntrypoint

from schema import countryFromRequest, placeFromRequest

from geopy.geocoders import Nominatim
#import geohash
import pygeohash as pgh
from shapely.geometry import Polygon
import sys

async def _generate_search_parameters(request: str, entrypoint: AgentEntrypoint, returnModel):
    system_prompt = prompt.build_system_prompt(entrypoint.id)
        
    client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"), base_url=utils.getValue("OPENAI_BASE_URL"))
    
    instructor_client = instructor.patch(client)

    req = await instructor_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=returnModel,
        messages=[
            {"role": "system",
                "content": system_prompt},
            {"role": "user", "content": request}],
        temperature=0,
    )

    generation = req.model_dump(exclude_none=True, by_alias=True)
    return generation    

async def get_country_from_request(request):
    client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"), base_url=utils.getValue("OPENAI_BASE_URL"))

    instructor_client = instructor.patch(client)

    req = await instructor_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=countryFromRequest,
        messages=[
            {"role": "system",
             "content": "You are a assistant that extracts the country from the request and "
                            "returns a python dictionary with the key as 'country' and value as the extracted"
                            "country name"},
            {"role": "user", "content": request}],
        temperature=0,
    )

    generation = req.model_dump(exclude_none=True, by_alias=True)
    return generation

async def place_to_geohash_wkt(place_name: str, geohash_length: int = 6):
    # Geocode the place
    geolocator = Nominatim(user_agent="geo_converter")
    location = geolocator.geocode(place_name)

    if not location:
        raise ValueError(f"Could not geocode place: {place_name}")

    lat, lon = location.latitude, location.longitude

    # Geohash
    gh = pgh.encode(lat, lon, precision=geohash_length)

    # Get geohash bounds (min lat, min lon, max lat, max lon)
    #lat_min, lon_min, lat_max, lon_max = decode_exactly_pygeohash(gh)
    lat_c, lon_c, lat_err, lon_err = pgh.decode_exactly(gh)

    # Bounding box of geohash cell
    lat_min = round(lat_c - lat_err,2)
    lat_max = round(lat_c + lat_err,2)
    lon_min = round(lon_c - lon_err,2)
    lon_max = round(lon_c + lon_err,2)

    # WKT polygon for geohash cell
    polygon = Polygon([
        (lon_min, lat_min),
        (lon_min, lat_max),
        (lon_max, lat_max),
        (lon_max, lat_min),
        (lon_min, lat_min)
    ])
    wkt_polygon = polygon.wkt

    return  wkt_polygon


def decode_exactly_pygeohash(gh):
    """
    Returns (lat, lon, lat_err, lon_err) similar to geohash.decode_exactly()
    """
    lat, lon, lat_err, lon_err = pgh.decode_exactly(gh)
    return lat, lon, lat - lat_err, lon - lon_err, lat + lat_err, lon + lon_err


async def get_place_from_request(request):
    client = AsyncOpenAI(api_key=utils.getValue("OPEN_API_KEY"), base_url=utils.getValue("OPENAI_BASE_URL"))

    instructor_client = instructor.patch(client)

    req = await instructor_client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=placeFromRequest,
        messages=[
            {"role": "system",
                "content": "You are a assistant that extracts the place or region from the request and "
                            "returns a python dictionary with the key as 'place' and value as the extracted "
                            "place or region name. If no place or region can be found in the request return an "
                            "empty dictionary"},
            {"role": "user", "content": request}],
        temperature=0,
    )

    generation = req.model_dump(exclude_none=True, by_alias=True)
    return generation
