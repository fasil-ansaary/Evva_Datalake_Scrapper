import pandas as pd
from resources.constants import state_id, zipcode
def zipcode_extractor():
    """
    This function takes a list of state names and returns the corresponding zips for the state.  
    """
    df = pd.read_csv('/Users/fasil/Desktop/evva/uszips.csv')
    states_to_scrape = ["MI", "IL", "CA", "TX", "NY", "GA"]
    zipcodes = []
    for states in states_to_scrape:
        filtered_values = df.loc[df[state_id] == states, zipcode].values
        for value in filtered_values:
            zipcodes.append(value)
    return zipcodes