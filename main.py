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

zipcodes = zipcode_extractor()


class Geriatrics_scrapper:
    def __init__(self):
        self.data = []
        self.full_name = []
        self.designation = []
        self.primary_affiliation = []
        self.primary_role = []
        self.address = []
        self.phone = []
        self.fax_number = []
        self.discipline = []
        self.clinical_speciality = []
        self.secondary_speciality = []
        self.lattitude = []
        self.longitude = []
        self.states = []
    
    def csv_conversion(self):
            new_data = []
            for i in range(len(self.full_name)):
                data = {
                    i: {
                        constants.Name: self.full_name[i],
                        constants.Designation: self.designation[i],
                        constants.Primary_Affiliation: self.primary_affiliation[i],
                        constants.Primary_Role: self.primary_role[i],
                        constants.Address: self.address[i],
                        constants.Phone: self.phone[i],
                        constants.Fax_Number: self.fax_number[i],
                        constants.Discipline: self.discipline[i],
                        constants.Clinical_Specialty: self.clinical_speciality[i],
                        constants.Secondary_Specialty: self.secondary_speciality[i],
                        constants.State: self.states[i],
                        constants.Lattitude : self.lattitude[i],
                        constants.Longitude : self.longitude[i]
                    }
                }
                new_data.append(data)

            with open(constants.inplace_json_file, constants.write_mode) as data_file:
                json.dump(new_data, data_file, indent=4)

            data_list = []
            for i in range(len(self.full_name)):
                data_list.append(
                    [
                        self.full_name[i],self. designation[i], self.primary_affiliation[i], self.primary_role[i], 
                        self.address[i], self.phone[i], self.fax_number[i], self.discipline[i],
                        self.clinical_speciality[i], self.secondary_speciality[i],
                        self.states[i], self.lattitude[i], self.longitude[i]
                    ])

            df = pd.DataFrame(data_list, columns=constants.geriatrics_header_column)
            df.to_csv(constants.geriatrics_csv_file)
    
    def run_geriatrics_scrapper(self):
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
                    for i in data_web:
                        self.data.append(i.text)

                    next_button = self.driver.find_element(By.XPATH, constants.geriatrics_web_page_next_button)
                    page_no = self.driver.find_element(By.XPATH, constants.geriatrics_web_page_get_page_num)                
                    page_no = page_no.text.replace(constants.dot, constants.empty_string)
                    x = page_no.split()
                    if x[1] == x[3]:
                        break
                    next_button.click()
                for i in range(0, len(self.data), 10):
                    self.full_name.append(self.data[i])
                    self.designation.append(self.data[i + 1])
                    self.primary_affiliation.append(self.data[i + 2])
                    self.primary_role.append(self.data[i + 3])
                    self.address.append(self.data[i + 4])
                    self.phone.append(self.data[i + 5])
                    self.fax_number.append(self.data[i + 6])
                    self.discipline.append(self.data[i + 7])
                    self.clinical_speciality.append(self.data[i + 8])
                    self.secondary_speciality.append(self.data[i + 9])
                    self.states.append(state)
                    if len(self.data[i + 4]) > 20:
                        shortened_address = self.data[i + 4][:20]
                        get_coords = get_coordinates(shortened_address, [])
                    else:
                        get_coords = get_coordinates(self.data[i + 4], [])
                    self.lattitude.append(get_coords[0])
                    self.longitude.append(get_coords[1])
                logger.info(f'Scrapped geriatrics details for state:{state}')
                bar()
        self.csv_conversion()
        self.driver.quit()
        logger.info(constants.geriatrics_success_logger)
        

    
class Meals_on_wheels_scrapper:
    def __init__(self):
        self.names = []
        self.addresses = []
        self.contact_numbers = []
        self.state = []
        self.city = []
        self.lattitude = []
        self.longitude = []
    
    def run_meals_on_wheels_scrapper(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        try:
            with alive_bar(len(zipcodes)) as bar:            
                for zip in zipcodes:
                    my_url = url_updater(constants.mow_url, zip)
                    self.scrape_mow_info(my_url, zip)
                    bar()
        except NoSuchElementException:
            logger.info(f"No service available at {','.join(find_city_state_from_zip(zip)), zip} zip code")
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
                        constants.Zipcode: str(zip),
                        constants.Lattitude: self.lattitude[i],
                        constants.Longitude: self.longitude[i]                   
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
                        self.city[i], self.state[i], zip, self.lattitude[i],
                        self.longitude[i]                    
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
                lst = []
                lst = find_city_state_from_zip(zip, lst)
                self.city.append(lst[0])
                self.state.append(lst[1])

            for i in address:
                self.addresses.append(i.text)
                if len(i.text) > 20:
                    shortened_address = i.text[:20]
                    get_coords = get_coordinates(shortened_address, [])
                else:
                    get_coords = get_coordinates(i.text, [])
                self.lattitude.append(get_coords[0])
                self.longitude.append(get_coords[1])
                
            # for i in self.addresses:
            #     for j in self.contact_numbers:
            #         if i == j:
            #             self.addresses.remove(i)
            
        except NoSuchElementException:
            logger.info(f"No service available at {','.join(find_city_state_from_zip(zip,[])), zip} zip code")
        
            

class Caring_scrapper:
    def run_caring_scrapper(self):
        for i in constants.caretype_to_url_mapper:
            # Set up Selenium
            self.options = Options()
            self.options.headless = True
            self.driver = webdriver.Chrome(options=self.options)
            scrapped_list = []
            with alive_bar(len(zipcodes)) as bar:            
                for zip in zipcodes[:2]:
                    my_url = url_updater(constants.caretype_to_url_mapper[i],zip)
                    # Call the function to scrape information
                    scrapped_list=self.scrape_care_type_info(my_url, scrapped_list, zip, i)
                    bar()
            # Quit the browser
            self.driver.quit()
            with open(constants.file_path+i+constants.csv_extension, mode=constants.write_mode) as csvfile:
                writer = csv.writer(csvfile)
                # Write header
                writer.writerow(constants.header)
            
                # Write data
                writer.writerows(scrapped_list)

            logger.info(constants.scrape_message+str(i))
    
    def scrape_care_type_info(self, url, scrapped_list, zip, care_type):
        self.driver.get(url)

        # Wait for the entire page to be loaded
        self.driver.implicitly_wait(10)  # Wait for up to 10 seconds

        # Find all elements with the class containing information
        elements = self.driver.find_elements(By.XPATH ,constants.webpage_class_tag)
        # Extract the text from these elements
        lst = [care_type]
        count = 0
        for element in elements:
            for i in element.text.split(constants.line_break):
                i = i.translate({ord(constants.dollar_sign): None})
                if count < 3:
                    lst.append(i)
                    count += 1
                else:
                    continue
        lst.pop()
        lst = find_city_state_from_zip(zip, lst)
        lst.append(zip)
        lst = get_coordinates(lst[1], lst)    
        scrapped_list.append(lst)
        return scrapped_list
    
    
if __name__ == '__main__':
    geriatrics_scrapper = Geriatrics_scrapper()
    meals_on_wheels_scrapper = Meals_on_wheels_scrapper()
    caring_scrapping = Caring_scrapper()
    
    #geriatrics_scrapper.run_geriatrics_scrapper()
    # meals_on_wheels_scrapper.run_meals_on_wheels_scrapper()
    caring_scrapping.run_caring_scrapper()