from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
import resources.constants as constants

def get_coordinates(address, list):
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
    credential = AzureKeyCredential(constants.azure_map_key)

    search_client = MapsSearchClient(
        credential=credential,
    )

    search_result = search_client.search_address(address)
    if search_result:
        latitude, longitude = search_result.results[0].position.lat, search_result.results[0].position.lon
        list.extend([latitude, longitude])
        return list
    else:
        return ['Not Found', 'Not Found']
