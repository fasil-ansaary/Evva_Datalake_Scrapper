import pandas as pd
from azure.core.credentials import AzureKeyCredential
from azure.maps.search import MapsSearchClient
import pandas as pd
import math 
from alive_progress import alive_bar
import logging
pd.options.mode.chained_assignment = None
df = pd.read_csv('./Evva_Datalake_Scrapper/azure/Assisted_Living.csv')
data = df.values.tolist()
for row in data:
    # Check if 'miles' or 'mile' is not in the third position (index 2)
    if 'review' not in row[3] and 'reviews' not in row[3]:
        row.insert(3, ' ')
    if 'Ends in' in row[6]:
        del row[6]
    if type(row[5]) == float and math.isnan(row[5]):
        del row[5]

cleaned_df = pd.DataFrame(data, columns=df.columns.insert(12, ' '))
cleaned_df.to_csv("./Evva_Datalake_Scrapper/azure/Assisted_Living_Cleaned.csv", index=False)



credential = AzureKeyCredential("Azure-key")

search_client = MapsSearchClient(
    credential=credential,
)
print(search_client.search_address("Michigan Community VNa, Franklin, MI,48025").results[0].address)
