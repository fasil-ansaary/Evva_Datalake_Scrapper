import pandas as pd
def zipcode_extractor(state_to_scrape):
    """
    This function takes a list of state names and returns the corresponding zips for the state.  
    """
    # df = pd.read_csv('/Users/fasil/Desktop/scrapper script/Evva_Datalake_Scrapper/resources/uszips.csv')
    # df = pd.read_csv('C:/Users/v2-scrapper/Desktop/Evva_Datalake_Scrapper/resources/uszips.csv')
    df = pd.read_csv('/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/uszips.csv')
    zipcodes = []
    filtered_values = df.loc[df['state_id'] == state_to_scrape, 'zip'].values
    for value in filtered_values:
        zipcodes.append(value)
    return zipcodes