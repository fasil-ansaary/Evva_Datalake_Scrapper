from uszipcode import SearchEngine
def find_city_state_from_zip(zip_code, list):
    """
    This function takes the zipcode and the list of scrapped details and finds out the major city and state 
    corresponding to the zipcode and appends them to the list and returns them back.
    Args:
        zip_code (str): zipcode of the request
        list (list): list of scrapped details

    Returns:
        list: list of scrapped details along with the state and city
    """
    search = SearchEngine()
    zipcode = search.by_zipcode(zip_code)
    city = zipcode.major_city
    state = zipcode.state
    list.extend([city, state])
    return list
