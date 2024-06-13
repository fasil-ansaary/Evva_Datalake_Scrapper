import json
import pandas as pd
from alive_progress import alive_bar
import logging
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from controllers.state_city_identifier import find_city_state_from_zip
from controllers.map_controller import get_coordinates
from controllers.zipcode_extractor import zipcode_extractor
import resources.constants as constants
from controllers.url_updater import url_updater
from bs4 import BeautifulSoup
import requests
import warnings
import time

warnings.filterwarnings(constants.ignore)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(constants.alive_progress_logger)

zipcodes = zipcode_extractor()


class Community_resource_scrapper:
    def __init__(self):
        self.names =[]
        self.links =[]
        self.addresses = []
        self.contact = []        
        self.program = []
        # self.lattitude = []
        self.distances = []
        self.state = []
        self.city = []
        self.zipcode = []
        self.gen_information_data= []
        self.staff_information_data = []
        self.service_offered_data = []
        self.financial_information_data = []
        self.availability_information_data = []
        self.pricing_availability_data = []
        self.overview_information_data = []
        self.features_data = []
        self.experiences_data = []
    
    def community_resource_scrapper(self):                  
        for i in constants.community_resource_finder_url_mapper:   
            file_name = '_'.join(list(i.split()))                        
            csv_sys_path = file_name+constants.csv_extension
            self.options = Options()
            self.options.headless = True
            self.driver = webdriver.Chrome(options=self.options)                
            scrapping_url = constants.community_resource_finder_url_mapper[i]
            care_type = i              
            with alive_bar(len(zipcodes)) as bar:                               
                bar.title(f'Scrapping {i}:')    
                for zip in zipcodes:
                    com_res_url = url_updater(scrapping_url, zip)
                    self.com_res_url_scrapper(com_res_url, care_type, zip)                                            
                    bar()            
            df = pd.DataFrame(
                {
                    'Program' : self.program, 'Name': self.names, 'Links': self.links, 'Contacts': self.contact,
                    'Distance': self.distances, 'Address': self.addresses, 'General Information': self.gen_information_data,
                    'Staff Information': self.staff_information_data,
                    'Services':self.service_offered_data,
                    'Financial Information':self.financial_information_data,
                    'Availability':self.availability_information_data,
                    'Pricing and Availability':self.pricing_availability_data, 
                    # 'Overview of Services':self.overview_information_data,
                    'Experiences': self.experiences_data,
                    'Zipcode_feeded_to_scrape': self.zipcode
                    }
                )
            df.drop_duplicates(subset=['Address'], inplace=True)            
            df.to_csv(csv_sys_path, index=False)
            logger.info(constants.scrape_message+str(care_type))   
        
        
    
    def com_res_url_scrapper(self, url, program_name, zip):
        self.driver.get(url)
        scrapped_links = []
        while True:
            try:
                pagesource = self.driver.page_source
                soup = BeautifulSoup(pagesource, 'html.parser')
                boxs = soup.find_all('div', {'class': 'ibox float-e-margins careseeker-result'})
                for box in boxs:
                    l = 0
                    #print(box)
                    self.program.append(program_name)
                    self.zipcode.append(zip)
                    try:                                                
                        self.names.append(box.find('a').text.strip())
                    except:
                        self.names.append("NIL")
                    try:                        
                        l = "https://www.communityresourcefinder.org"+box.find('a')['href']
                        self.links.append(l)
                        scrapped_links.append(l)
                    except:
                        self.links.append("NIL")
                    try:                        
                        dis = box.find('p', {'class': 'distance'}).text
                        self.distances.append(dis)
                    except:
                        self.distances.append("NIL")
                    try:
                        add = box.find('input', {'id': 'Address'})['value']
                        self.addresses.append(add)                        
                    except:
                        self.addresses.append("NIL")
                        
                    try:
                        ph = box.find('i', {'class': 'fa fa-phone'}).findNext('a').text
                        self.contact.append(ph)
                    except:
                        self.contact.append("NIL")
                        
                WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.LINK_TEXT, 'Next')))
                self.driver.find_element(By.LINK_TEXT, 'Next').click()
            except Exception as e:                
                break
        length = len(scrapped_links)
        s = 0
        while s < length:
                response = requests.get(scrapped_links[s])
                soup = BeautifulSoup(response.content, "html.parser")
                for h2 in soup.find_all('h2'):
                    h2.string = h2.string + '-'
                    
                time.sleep(5)
                # General Information
                try:       
                    general_info = soup.find("div", id= "tabS2P11").get_text(strip=True, separator=' ')
                    self.gen_information_data.append(general_info) 
                except:
                    self.gen_information_data.append("nil")
                    
                try:            
                    # Staff Information
                    staff_info = soup.find("div", id= "tabS3P11").get_text(strip=True, separator=' ')
                    self.staff_information_data.append(staff_info) 
                except:
                    self.staff_information_data.append("nil")
                    
                try:            
                    # Services Offered
                    services_info= soup.find("div",id= "tabS6P11").get_text(strip=True, separator=' ')
                    self.service_offered_data.append(services_info)
                except:
                    self.service_offered_data.append("nil")
                
                try:    
                    # Pricing & Availability
                    pricing_availability_info = soup.find("div", id= "tabS9P11").get_text(strip=True, separator=' ')
                    self.pricing_availability_data.append(pricing_availability_info)
                except:
                    self.pricing_availability_data.append("nil")
                    
                try:
                    # Experience Information
                    experiences = soup.find("div", id= "tabS8P11").get_text(strip=True, separator=' ')
                    self.experiences_data.append(experiences)
                except:
                    self.experiences_data.append("nil")   
                try:
                    # Financial Information
                    financial_info = soup.find("div", id= "tabS4P11").get_text(strip=True, separator=' ')
                    self.financial_information_data.append(financial_info)
                except:
                    self.financial_information_data.append("nil")  
                
                try:
                    # Availability
                    availability_info = soup.find("div", id= "tabS5P11").get_text(strip=True, separator=' ')
                    self.availability_information_data.append(availability_info)
                except:
                    self.availability_information_data.append("nil")
                # try:
                #     overview_info = soup.find("div", id= "tabP16").get_text(strip=True, separator=' ')
                #     self.overview_information_data.append(overview_info)
                # except:
                #     self.overview_information_data.append("nil")
                s+=1
        
                
        
        
if __name__ == '__main__':
    community_resource_scrapper = Community_resource_scrapper()
    
    community_resource_scrapper.community_resource_scrapper()
    