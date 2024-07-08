"""
This module scrapes geriatrics information from a specified website, processes the data, and saves it into CSV and JSON formats.

Modules:
    - json: Used to parse JSON data.
    - pandas as pd: Used to create and manipulate dataframes.
    - alive_progress: Used to display progress bars.
    - logging: Used for logging information.
    - csv: Used to handle CSV files.
    - selenium: Used for web scraping.
    - warnings: Used to handle warnings.

Classes:
    - Geriatrics_scrapper: Scrapes geriatrics information from a specified website and processes the data.

Constants:
    - constants: Custom constants used throughout the code.

Functions:
    - __init__(self): Initializes the class with empty lists to store data.
    - csv_conversion(self): Converts the scraped data into CSV and JSON formats.
    - run_geriatrics_scrapper(self): Runs the scraper to collect data from the website.

Usage:
    To run the script, simply execute it as a standalone program.
"""

import json
import pandas as pd
from alive_progress import alive_bar
import logging
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support.select import Select
from controllers.state_city_identifier import find_city_state_from_zip
from controllers.nominatim_controller import get_coordinates
from controllers.zipcode_extractor import zipcode_extractor
import resources.constants as constants
from controllers.url_updater import url_updater
import warnings

# Ignore all warnings
warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)


class Geriatrics_scrapper:
    """
    A class to scrape geriatrics information from a specified website and process the data.

    Attributes:
        data (list): Stores raw scraped data.
        full_name (list): Stores the full names of individuals.
        designation (list): Stores the designations of individuals.
        primary_affiliation (list): Stores the primary affiliations of individuals.
        primary_role (list): Stores the primary roles of individuals.
        address (list): Stores the addresses of individuals.
        contact (list): Stores the contact details of individuals.
        fax_number (list): Stores the fax numbers of individuals (currently not used).
        discipline (list): Stores the disciplines of individuals.
        clinical_speciality (list): Stores the clinical specialties of individuals.
        secondary_speciality (list): Stores the secondary specialties of individuals (currently not used).
        latitude (list): Stores the latitudes of addresses.
        longitude (list): Stores the longitudes of addresses.
        states (list): Stores the states of individuals.
    """
    def __init__(self):
        """
        Initializes the class with empty lists to store data.
        """
        self.data = []
        self.full_name = []
        self.designation = []
        self.primary_affiliation = []
        self.primary_role = []
        self.address = []
        self.contact = []
        self.fax_number = []
        self.discipline = []
        self.clinical_speciality = []
        self.secondary_speciality = []
        self.lattitude = []
        self.longitude = []
        self.states = []
    
    def csv_conversion(self):
            """
            Converts the scraped data into CSV and JSON formats.

            The data is first structured into a JSON format and written to a file.
            Then, it is organized into a pandas DataFrame, deduplicated, and saved as a CSV file.
            """
            new_data = []
            for i in range(len(self.full_name)):
                data = {
                    i: {
                        constants.Name: self.full_name[i],
                        constants.Designation: self.designation[i],                        
                        constants.Primary_Role: self.primary_role[i],
                        constants.Address: self.address[i],
                        constants.Contact: self.contact[i],
                        # constants.Fax_Number: self.fax_number[i],
                        constants.Discipline: self.discipline[i],
                        constants.Clinical_Specialty: self.clinical_speciality[i],
                        # constants.Secondary_Specialty: self.secondary_speciality[i],
                        constants.State: self.states[i],
                        constants.Primary_Affiliation: self.primary_affiliation[i]
                    }
                }
                new_data.append(data)

            with open(constants.inplace_json_file, constants.write_mode) as data_file:
                json.dump(new_data, data_file, indent=4)

            data_list = []
            for i in range(len(self.full_name)):
                data_list.append(
                    [
                        self.full_name[i],self. designation[i], self.primary_role[i], 
                        self.address[i], self.contact[i], self.discipline[i],
                        self.clinical_speciality[i],
                        self.states[i], self.primary_affiliation[i]
                    ])

            df = pd.DataFrame(data_list, columns=constants.geriatrics_header_column)
            df.drop_duplicates(subset=['Address'], inplace=True)
            df.to_csv(constants.geriatrics_csv_file)
    
    def run_geriatrics_scrapper(self):
        """
        Runs the scraper to collect data from the website.

        This function opens the website, iterates through specified states, collects the data,
        and calls csv_conversion to save the data into CSV and JSON formats.
        """
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(constants.geriatrics_url_to_scrape)
        
        with alive_bar(len(constants.states_to_scrape)) as bar:
            for state in constants.states_to_scrape:
                drp_dwn = self.driver.find_elements(By.CLASS_NAME, constants.geriatrics_web_page_form_control)
                slt = Select(drp_dwn[1])
                slt.select_by_visible_text(state)
                search_button = self.driver.find_element(By.XPATH, constants.geriatrics_web_page_search_control)
                search_button.click()
                
                while True:
                    data_web = self.driver.find_elements(By.XPATH, constants.geriatrics_web_page_row_spanner)
                    lst = []
                    for i in data_web:                        
                        content = []
                        content.append(i.text)
                        lst.append(content)
                    # print(lst)
                    temp = []
                    temp.extend(lst[0])
                    for i in lst[1:]:
                        if 'Dr. ' in i[0]:                            
                            self.data.append(temp)
                            temp = []
                            temp.extend(i)
                        else:
                            temp.extend(i)
                    self.data.append(temp)
                    
                    try:
                        next_button = self.driver.find_element(By.XPATH, constants.geriatrics_web_page_next_button)
                        page_no = self.driver.find_element(By.XPATH, constants.geriatrics_web_page_get_page_num)                
                        page_no = page_no.text.replace(constants.dot, constants.empty_string)
                        x = page_no.split()
                        if x[1] == x[3]:
                            break
                        next_button.click()
                    except:
                        logger.info("Done")
                for i in self.data:
                    self.full_name.append(i[0])
                    self.designation.append(i[1])
                    self.primary_affiliation.append(i[2])
                    self.primary_role.append(i[3])
                    addr = i[4]
                    addr = addr.replace("\n", ' ')
                    self.address.append(addr)
                    if len(i[6]) > 2 and len(i[5]) > 2:
                        self.contact.append(i[5]+", "+i[6])
                    elif len(i[5]) < 2:
                        self.contact.append(i[6])
                    else:
                        self.contact.append(i[5])
                    # self.fax_number.append(self.data[i + 6])
                    self.discipline.append(i[7])
                    if len(i[9]) > 2:
                        self.clinical_speciality.append(i[8]+", "+i[9])
                    else:
                        self.clinical_speciality.append(i[8])
                    self.states.append(state)           
                logger.info(f'Scrapped geriatrics details for state:{state}')
                bar()
                             
        self.csv_conversion()
        self.driver.quit()
        logger.info(constants.geriatrics_success_logger)
        
    
if __name__ == '__main__':
    geriatrics_scrapper = Geriatrics_scrapper()    
    geriatrics_scrapper.run_geriatrics_scrapper()