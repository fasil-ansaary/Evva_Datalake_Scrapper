from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
import pandas as pd
from alive_progress import alive_bar
import logging
from zipcode_extractor import zipcode_extractor

credential = AzureKeyCredential("NvKCUdW1a-bsKFSdgOswNqsugMyg-A0TdApdnbvpg4g")

search_client = MapsSearchClient(
    credential=credential,
)

df = pd.read_csv("/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/Assisted Living.csv")
print("Scrapped data size:", df.size)
zipcodes = zipcode_extractor()
print("Total zipcodes scrapped:", len(zipcodes) )
df_cleaned = df.dropna(subset=['State'])
print("Dataset size after cleaning:", df_cleaned.size)
df = df_cleaned
latt = []
long = []
df.rename(columns = {'Lattitue':'Lattitude'}, inplace = True)
with alive_bar(len(df['Address'])) as bar:      
    bar.title('Mapping Coordinates in Progress...')
    for i in df['Address']:
        search_result = search_client.search_address(i)
        latt.append(search_result.results[0].position.lat)
        long.append(search_result.results[0].position.lon)
        bar()
df['Lattitude'] = latt
df['Longitude'] = long
    
df_cleaned.to_csv("/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/Assisted_Living_cleaned.csv", index=False)