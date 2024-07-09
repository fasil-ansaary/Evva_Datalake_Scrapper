"""
This module scrapes information from the Meals on Wheels website, processes the data, and saves it into CSV and JSON formats.

Modules:
    - json: Used to parse JSON data.
    - pandas as pd: Used to create and manipulate dataframes.
    - alive_progress: Used to display progress bars.
    - logging: Used for logging information.
    - selenium: Used for web scraping.
    - warnings: Used to handle warnings.

Classes:
    - Meals_on_wheels_scrapper: Scrapes Meals on Wheels information from a specified website and processes the data.

Constants:
    - constants: Custom constants used throughout the code.

Functions:
    - __init__(self): Initializes the class with empty lists to store data.
    - run_meals_on_wheels_scrapper(self): Runs the scraper to collect data from the website.
    - scrape_mow_info(self, url, zip): Scrapes information from the given URL for a specific zip code.

Usage:
    To run the script, simply execute it as a standalone program.
"""

import json
import pandas as pd
from alive_progress import alive_bar
import logging
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from controllers.zipcode_extractor import zipcode_extractor
import resources.constants as constants
from controllers.url_updater import url_updater
import warnings

# Ignore all warnings
warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)

class Meals_on_wheels_scrapper:
    """
    A class to scrape Meals on Wheels information from a specified website and process the data.

    Attributes:
        names (list): Stores the names of individuals or organizations.
        addresses (list): Stores the addresses of individuals or organizations.
        contact_numbers (list): Stores the contact numbers of individuals or organizations.
    """
    def __init__(self):
        """
        Initializes the class with empty lists to store data.
        """
        self.names = []
        self.addresses = []
        self.contact_numbers = []
    
    def run_meals_on_wheels_scrapper(self, states_to_scrape):
        """
        Runs the scraper to collect data from the Meals on Wheels website.

        This function opens the website, iterates through specified zip codes, collects the data,
        and saves the data into CSV and JSON formats.
        """
        for state in states_to_scrape:
            zipcodes = zipcode_extractor(state)
            self.options = Options()
            self.options.headless = True
            self.driver = webdriver.Chrome(options=self.options)            
            try:
                with alive_bar(len(zipcodes)) as bar:            
                    bar.title(f'Scrapping for {state}:')    
                    for zip in zipcodes:
                        my_url = url_updater(constants.mow_url, zip)
                        self.scrape_mow_info(my_url, zip)
                        bar()
            except NoSuchElementException:
                logger.info(f"No service found at {zip}")
            finally:
                new_data = []
                for i in range(len(self.names)):
                    data = {
                        i: {
                            constants.Name: self.names[i],
                            constants.Address: self.addresses[i],
                            constants.Contact: self.contact_numbers[i],                                      
                        }
                    }
                    new_data.append(data)

                with open(constants.inplace_json_file, constants.write_mode) as data_file:
                    json.dump(new_data, data_file, indent=4)
                
                data_list = []
                for i in range(len(self.names)):
                    data_list.append(
                        [
                            self.names[i], self.addresses[i], self.contact_numbers[i]                        
                        ])

                df = pd.DataFrame(data_list, columns=constants.header_column)
                df.drop_duplicates(subset=['Address'], inplace=True)
                df.to_csv(constants.meals_on_wheels_csv_file)

            self.driver.quit()
            logger.info(constants.meals_on_wheels_success_log)
        
    def scrape_mow_info(self, url, zip):
        """
        Scrapes information from the given URL for a specific zip code.

        This function opens the specified URL, collects names, addresses, and contact numbers,
        and appends them to the respective class attributes.

        Args:
            url (str): The URL to scrape information from.
            zip (str): The zip code being processed.
        """
        self.driver.get(url)
        try:
            view_more = self.driver.find_element(By.XPATH, constants.mow_web_page_view_more_button_tag)
            while True:
                try:
                    view_more.click()
                except StaleElementReferenceException:
                    break
            
            name = self.driver.find_elements(By.XPATH, constants.mow_web_page_name_tag)
            address = self.driver.find_elements(By.XPATH, constants.mow_web_page_address_tag)
            contact_number = self.driver.find_elements(By.XPATH, constants.mow_web_page_contact_tag)

            for i in name:
                self.names.append(i.text)
                
            for i in contact_number:
                self.contact_numbers.append(i.text)
            
            for i in address:
                self.addresses.append(i.text)

            # REMOVING CONTACT FROM ADDRESS LIST

            for i in self.addresses:
                if i in self.contact_numbers:
                    self.addresses.remove(i)
                
        except NoSuchElementException:
            logger.info(f"No service found at {zip}")
        
if __name__ == '__main__':
    states_obtained = sys.argv[1]
    states_to_scrape = [i for i in states_obtained.split(',')]
    meals_on_wheels_scrapper = Meals_on_wheels_scrapper()
    meals_on_wheels_scrapper.run_meals_on_wheels_scrapper(states_to_scrape=states_to_scrape)