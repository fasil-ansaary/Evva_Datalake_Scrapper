from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
# import resources.constants as constants

def get_coordinates(address, list, attempt=1, max_attempts=5):
    """
    This function uses mapbox api to get the locations coordinates in lattitude and in longitude.

    Args:
        address (str): address of the location to get coordinates for.
        list (list): list of scrapped details

    Raises:
        ValueError: Value error incase the location is not found by mapbox api

    Returns:
        list: list of scrapped details along with the coordinates.
    """
    geocoder = Nominatim(user_agent="evva-datalake-scrapper")    
    try:
        location = geocoder.geocode(address)
        if location:
            latitude, longitude = location.latitude, location.longitude
            list.extend([latitude, longitude])
            return list
        else:
            list.extend(['Not Found', 'Not Found'])
            return list
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return get_coordinates(address, list, attempt=attempt+1)
        raise
    
    