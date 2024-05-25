import json
import pandas as pd
from alive_progress import alive_bar
import logging
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from collections import OrderedDict
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.select import Select
from controllers.state_city_identifier import find_city_state_from_zip
from controllers.map_controller import get_coordinates
from controllers.zipcode_extractor import zipcode_extractor
import resources.constants as constants
from controllers.url_updater import url_updater
import warnings

# Ignore all warnings
warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)

zipcodes = zipcode_extractor()

class Meals_on_wheels_scrapper:
    def __init__(self):
        self.names = []
        self.addresses = []
        self.contact_numbers = []
        self.state = []
        self.city = []
    
    def run_meals_on_wheels_scrapper(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        try:
            with alive_bar(len(zipcodes)) as bar:            
                bar.title("Zipcodes scrapped for Meals on Wheels:")
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
                        constants.City: self.city[i],
                        constants.State: self.state[i],
                        constants.Zipcode: str(zip)                 
                    }
                }
                new_data.append(data)

            with open(constants.inplace_json_file, constants.write_mode) as data_file:
                json.dump(new_data, data_file, indent=4)
            
            data_list = []
            for i in range(len(self.names)):
                data_list.append(
                    [
                        self.names[i], self.addresses[i], self.contact_numbers[i],
                        self.city[i], self.state[i], zip  
                    ])

            df = pd.DataFrame(data_list, columns=constants.header_column)
            df.to_csv(constants.meals_on_wheels_csv_file)

        self.driver.quit()
        logger.info(constants.meals_on_wheels_success_log)
    
    def scrape_mow_info(self, url, zip):
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
                else:
                    i = i[:-13]
                
            self.names = list(OrderedDict.fromkeys(self.names))
            self.addresses = list(OrderedDict.fromkeys(self.addresses))
            self.contact_numbers = list(OrderedDict.fromkeys(self.contact_numbers))
                        
            for i in self.addresses:                
                get_city_state_info = find_city_state_from_zip(zip, [])
                self.city.append(get_city_state_info[0])
                self.state.append(get_city_state_info[1])  
                
        except NoSuchElementException:
            logger.info(f"No service found at {zip}")
        
if __name__ == '__main__':
    # geriatrics_scrapper = Geriatrics_scrapper()
    meals_on_wheels_scrapper = Meals_on_wheels_scrapper()
    # caring_scrapping = Caring_scrapper()
    
    #geriatrics_scrapper.run_geriatrics_scrapper()
    meals_on_wheels_scrapper.run_meals_on_wheels_scrapper()
    # caring_scrapping.run_caring_scrapper()