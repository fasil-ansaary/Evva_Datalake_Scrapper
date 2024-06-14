ignore = "ignore"
mapbox_access_token = "pk.eyJ1IjoiZXZ2YWhlYWx0aCIsImEiOiJjbGp5anJjY2IwNGlnM2RwYmtzNGR0aGduIn0.Nx4jv-saalq2sdw9qKuvbQ"
value_error_message = "Could not retrieve location information from the address."
webpage_class_tag = "//div[@class='content sc-ifAKCX cFlEyZ sc-bdVaJa jgrpHL']"
line_break = '\n'
dollar_sign = '$'
header = ['Care Type', 'Name', 'Address', 'Review Count', 'Distance_from_Zip_to_Address',
          'City_Corres_to_Zip', 'State_Corres_to_Zip', 'Zipcode_feeded_to_scrape']
write_mode = 'w'
csv_extension = ".csv"
file_path = "/home/evva-datalake-scrapper/Evva_Datalake_Scrapper/resources/"
mac_path = "/Users/fasil/Desktop/scrapper script/Evva_Datalake_Scrapper/resources/"
caretype_to_url_mapper = {
    'Assisted Living' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=assisted-living&location=",
    'Memory Care' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=memory-care-facilities&location=",
    'Adult Day Care' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=adult-day-care&location=",
    'Independent Living' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=independent-living&location=",
    'Senior Apartments' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=senior-apartments&location=",
    'Nursing Homes' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=nursing-homes&location=",
    'Home Health Agency' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=home-health-agencies&location=",
    'Geriatric Care Managers CAR' : "https://www.caring.com/local/search?utf8=%E2%9C%93&type=geriatric-care-managers&location=",
    
}
alive_progress_logger = 'alive_progress'
geriatrics_csv_file = 'Geriatrics_data_scrapped.csv'
geriatrics_success_logger = "Geriatric data successfully scrapped for all locations."
scrape_message = "Successfully scrapped for care type "

community_resource_finder_url_mapper = {    
    # "Alzheimer Association Chapters" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=84&location=",
    # "Alzheimer Early Stage Programs" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=94&location=",
    # "AARP Events" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=89&location=",
    # "Adult Day Care" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=1&location=",
    # "Alzheimer Education Programs" :"https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=93&location=",
    # "Relocation Advisors" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=48&location=",
    # "AARP State Offices" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=87&location=",
    # "Transportation" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=64&location=",
    # "Skilled Nursing" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=2&location=",
    # "Neurologists" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=77&location=",
    # "Elder Law Attorneys" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=11&location=",
    # "Area Agency on Aging" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=7&location=",
    # "Neurologists" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=77&location=",
    # "Independent Living CR" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=28&location=",
    "Home Health Care" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=17&location=",
    # "Home Care" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=16&location=",
    # "Geriatricians" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=75&location=",
    # "Geriatric Psychiatrists" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=76&location=",
    # "Geriatric Care Managers" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=15&location=",
    # "Elder Law Attorneys" : "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=11&location=",
}




state_id = 'state_id'

zipcode = 'zip'
mow_url = 'https://www.mealsonwheelsamerica.org/signup/aboutmealsonwheels/find-programs?filter='
header_column = ["Name", "Address", "Contact"]
geriatrics_url_to_scrape = "https://account.americangeriatrics.org/findageriatricshealthcareprofessional"
states_to_scrape = ["Michigan","Illinois","California", "Texas", "New York", "Georgia"]
states_to_scrape_testing = ["Alabama"]
geriatrics_header_column = [
                                "Full Name", "Designation", "Primary Role",
                                "Address", "Contact", "Discipline", "Specialty", 
                                "State", "Primary Affiliation"
                                ]
Name = "Name"
Designation = "Designation"
Primary_Affiliation = "Primary Affiliation"
Primary_Role = "Primary Role"
Address = "Address"
Phone = "Phone"
Fax_Number = "Fax Number"
Discipline = "Discipline"
Clinical_Specialty = "Specialty"
Secondary_Specialty = "Secondary Specialty"
State = "State"
Lattitude = "Lattitude"
Longitude = "Longitude"
Zipcode = "Zipcode"
City = "City"
Contact = "Contact"

inplace_json_file = "data.json"

NoSuchElementExceptionLog = "No service available at this pin code"
meals_on_wheels_csv_file = "meals_on_wheels.csv"
meals_on_wheels_success_log = "Meals on wheels data successfully scrapped for all locations."

geriatrics_web_page_form_control = 'form-control'
geriatrics_web_page_search_control = '//div[@class="form-group"]/div/p/input'
geriatrics_web_page_row_spanner = '//div[@class="row"]/div/ul/li/span'
geriatrics_web_page_next_button = "//a[normalize-space()='Next']"
geriatrics_web_page_get_page_num = '/html/body/div[2]/div[2]/div/div/form/div[1]/div[3]/div'
dot = "."
empty_string = ""
mow_web_page_view_more_button_tag = '//div/p/a[contains(@class, "thebutton")]'
mow_web_page_name_tag = '//div[@class="findmeal-result"]/div/h2'
mow_web_page_address_tag = '//div[@class="findmeal-result"]/div/p'
mow_web_page_contact_tag = '//div[@class="findmeal-result"]/div/p/a'

azure_map_key = "NvKCUdW1a-bsKFSdgOswNqsugMyg-A0TdApdnbvpg4g"