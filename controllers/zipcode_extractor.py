import pandas as pd
def zipcode_extractor():
    """
    This function takes a list of state names and returns the corresponding zips for the state.  
    """
    df = pd.read_csv('/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/uszips.csv')
    states_to_scrape = ["MI", "IL", "CA", "TX", "NY", "GA","FL"]
    zipcodes = []
    for states in states_to_scrape:
        filtered_values = df.loc[df['state_id'] == states, 'zip'].values
        for value in filtered_values:
            zipcodes.append(value)
    return zipcodes