import pandas as pd
import resources.constants as constants
def zipcode_extractor():
    """
    This function takes a list of state names and returns the corresponding zips for the state.  
    """
    df = pd.read_csv('/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/uszips.csv')
    states_to_scrape = ["MI", "IL", "CA", "TX", "NY", "GA"]
    zipcodes = []
    for states in states_to_scrape:
        filtered_values = df.loc[df[constants.state_id] == states, constants.zipcode].values
        for value in filtered_values:
            zipcodes.append(value)
    return zipcodes