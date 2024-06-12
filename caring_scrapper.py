import json
import pandas as pd
from alive_progress import alive_bar
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.select import Select
from controllers.state_city_identifier import find_city_state_from_zip
from controllers.map_controller import get_coordinates
from controllers.zipcode_extractor import zipcode_extractor
import resources.constants as constants
from controllers.url_updater import url_updater
import csv
import warnings

warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)

zipcodes = zipcode_extractor()


class Caring_scrapper:
    def run_caring_scrapper(self):
        for i in constants.caretype_to_url_mapper: 
            self.options = Options()
            self.options.headless = True
            self.driver = webdriver.Chrome(options=self.options)
            scrapped_list = []
            scrapping_url = constants.caretype_to_url_mapper[i]
            care_type = i
            file_name = '_'.join(list(i.split())) 
            with alive_bar(len(zipcodes)) as bar:
                bar.title(f'Scrapping for {i}:')
                for zip in zipcodes:
                    # Set up Selenium                
                    my_url = url_updater(scrapping_url,zip)
                        # Call the function to scrape information
                    scrapped_list=self.scrape_care_type_info(my_url, zip, care_type, scrapped_list)
                    # Quit the browser
                    bar()
            self.driver.quit()
                # with open(constants.file_path+file_name+constants.csv_extension, mode=constants.write_mode) as csvfile:
                #     writer = csv.writer(csvfile)
                #     # Write header
                #     writer.writerow(constants.header)
                
                #     # Write data
                #     writer.writerows(scrapped_list)
            df = pd.DataFrame(scrapped_list, columns=constants.header)
            df.drop_duplicates(subset=['Address'], inplace=True)
            df.reset_index(inplace=True, drop=True)
                # pd.set_option('display.max_columns', None)
                # print(df)
            df.to_csv(file_name+constants.csv_extension, index=False)
            logger.info(constants.scrape_message+str(care_type))
    
    def scrape_care_type_info(self, url, zip, care_type, scrapped_list):
        self.driver.get(url)

        # Wait for the entire page to be loaded
        self.driver.implicitly_wait(1)  # Wait for up to 10 seconds

        # Find all elements with the class containing information
        elements = self.driver.find_elements(By.XPATH ,constants.webpage_class_tag)
        # print(elements)
        # Extract the text from these elements
        
        for element in elements:
            reviews = ''
            distance = ''
            address = ''
            lst2 = [care_type]
            data = element.text
            data = data.replace('$', '')   
            contents = data.split('\n')
            name = contents[0]
            contents.pop(0)
            i = 0
            while i < len(contents):
                if 'special promotion!' in contents[i].lower():
                    contents.remove(contents[i])    
                    i -= 1
                if 'ends in' in contents[i].lower():
                    contents.remove(contents[i])    
                    i -= 1
                if 'review' in contents[i].lower() or 'reviews' in contents[i].lower():
                    reviews = contents[i]
                    contents[i] = ''
                if 'mile' in contents[i].lower() or 'miles' in contents[i].lower():    
                    distance = contents[i]
                    contents[i] = ''
                i += 1
            address = ''.join(contents)
            lst2.extend([name, address, reviews, distance])
            lst2 = find_city_state_from_zip(zip, lst2)
            # lst2 = get_coordinates(lst2[2], lst2)    
            lst2.append(zip)    
            scrapped_list.append(lst2)                    
        return scrapped_list
    
    
if __name__ == '__main__':
    caring_scrapping = Caring_scrapper()
    
    #geriatrics_scrapper.run_geriatrics_scrapper()
    # meals_on_wheels_scrapper.run_meals_on_wheels_scrapper()
    caring_scrapping.run_caring_scrapper()