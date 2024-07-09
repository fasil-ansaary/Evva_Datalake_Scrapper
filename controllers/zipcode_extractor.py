import pandas as pd
def zipcode_extractor(state_to_scrape):
    """
    This function extracts the list of ZIP codes corresponding to a given state name.
    
    Args:
        state_to_scrape (str): A string representing the abbreviation of the US state for which zipcodes are desired.
        This should be in all uppercase letters.
        
    Returns:
        list: List of ZIP codes corresponding to the given state name. If no zips found, an empty list is returned.    
    """
    # for windows based VM uncomment the below file hierarchy
    df = pd.read_csv('C:/Users/v2-scrapper/Desktop/Evva_Datalake_Scrapper/resources/uszips.csv')
    
    # for linux based VM uncomment the below file hierarchy
    # df = pd.read_csv('/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/uszips.csv')
    zipcodes = []
    filtered_values = df.loc[df['state_id'] == state_to_scrape, 'zip'].values
    for value in filtered_values:
        zipcodes.append(value)
    return zipcodes