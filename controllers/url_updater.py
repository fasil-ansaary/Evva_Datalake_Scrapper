def url_updater(url_to_scrape, zipcode):
    """
    This function updates the url with the desired zipcode provided

    Args:
        url_to_scrape (str): The url required to scrape upon
        zipcode (str): The zipcode that is to be appended at the end of the url

    Returns:
        url: The url along with the zipcode
    """
    url = url_to_scrape + str(zipcode)
    return url