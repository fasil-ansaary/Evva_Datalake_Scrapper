"""
This module scrapes information from a specified website, processes the data, and saves it into CSV format.

Modules:
    - json: Used to parse JSON data.
    - pandas as pd: Used to create and manipulate dataframes.
    - alive_progress: Used to display progress bars.
    - logging: Used for logging information.
    - requests: Used for making HTTP requests.
    - bs4 (BeautifulSoup): Used for parsing HTML and XML documents.
    - selenium: Used for web scraping.
    - csv: Used for reading and writing CSV files.
    - sys: Used for system-specific parameters and functions.
    - warnings: Used to handle warnings.

Classes:
    - Caring_scrapper: Scrapes information from a specified website and processes the data.

Functions:
    - __init__(self): Initializes the class.
    - run_caring_scrapper(self, states_to_scrape): Runs the scraper to collect data from the website for specified states.
    - scrape_care_type_info(self, url, zip, care_type, scrapped_list): Scrapes information from the given URL for a specific care type.

Usage:
    To run the script, pass the states to be scraped as a command-line argument.
"""
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
import sys
import warnings

warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)


class Caring_scrapper:
    """
    A class to scrape information from a specified website and process the data.

    Methods:
        run_caring_scrapper(self, states_to_scrape): Runs the scraper to collect data from the website for specified states.
        scrape_care_type_info(self, url, zip, care_type, scrapped_list): Scrapes information from the given URL for a specific care type.
    """
    def run_caring_scrapper(self, states_to_scrape):
        """
        Runs the scraper to collect data from the website for specified states.

        This function iterates through specified states and zip codes, collects the data,
        and saves the data into CSV format.

        Args:
            states_to_scrape (list): List of states to scrape data for.
        """
        for state in states_to_scrape:
            zipcodes = zipcode_extractor(state)  
            for i in constants.caretype_to_url_mapper: 
                self.options = Options()
                self.options.headless = True
                self.driver = webdriver.Chrome(options=self.options)
                scrapped_list = []
                scrapping_url = constants.caretype_to_url_mapper[i]
                care_type = i
                file_name = '_'.join(list(i.split())) 
                with alive_bar(len(zipcodes)) as bar:
                    bar.title(f'Scrapping {i} for {state}:')
                    for zip in zipcodes:
                        # Set up Selenium                
                        my_url = url_updater(scrapping_url,zip)
                            # Call the function to scrape information
                        scrapped_list=self.scrape_care_type_info(my_url, zip, care_type, scrapped_list)
                        # Quit the browser
                        bar()
                self.driver.quit()
                df = pd.DataFrame(scrapped_list, columns=constants.header)
                df.drop_duplicates(subset=['Address'], inplace=True)
                df.reset_index(inplace=True, drop=True)
                file_path = "./resources/"+file_name+constants.csv_extension
                df.to_csv(file_path, index=False)
                logger.info(constants.scrape_message+str(care_type))
    
    def scrape_care_type_info(self, url, zip, care_type, scrapped_list):
        """
        Scrapes information from the given URL for a specific care type.

        This function opens the specified URL, collects data, and appends it to the scrapped_list.

        Args:
            url (str): The URL to scrape information from.
            zip (str): The zip code being processed.
            care_type (str): The type of care being scraped.
            scrapped_list (list): The list to append scraped data to.

        Returns:
            list: Updated scrapped_list with the scraped data.
        """
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
    states_obtained = sys.argv[1]
    states_to_scrape = [i for i in states_obtained.split(',')]
    caring_scrapping = Caring_scrapper()
    caring_scrapping.run_caring_scrapper(states_to_scrape=states_to_scrape)