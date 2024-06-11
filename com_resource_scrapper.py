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
        # self.longitude = []
        self.state = []
        self.city = []
        self.zipcode = []
        # self.general_information_data= []
        # self.staff_info = []
        self.service_offered = []
        # self.pricing = []
        # self.financial = []
        # self.avail = []
    
    def community_resource_scrapper(self):                  
        for i in constants.community_resource_finder_url_mapper:   
            file_name = '_'.join(list(i.split()))            
            df = pd.DataFrame( 
                { 
                'Program' : self.program,
                'Name': self.names, 'Links': self.links, 'Contacts': self.contact, 
                'Address': self.addresses,'Zipcode' : self.zipcode,
                })            
            csv_sys_path = constants.file_path+file_name+constants.csv_extension
            df.to_csv(csv_sys_path, index=False)
            self.options = Options()
            self.options.headless = True
            self.driver = webdriver.Chrome(options=self.options)                
            scrapping_url = constants.community_resource_finder_url_mapper[i]
            care_type = i              
            with alive_bar(len(zipcodes)) as bar:                               
                bar.title(f'Scrapping {i}:')    
                for zip in zipcodes:
                    com_res_url = url_updater(scrapping_url, zip)
                    self.com_res_url_scrapper(com_res_url, care_type, csv_sys_path)                                            
                    bar()
            df = pd.read_csv(csv_sys_path)
            df.drop_duplicates(subset=['Address'], inplace=True)            
            df.to_csv(csv_sys_path, index=False)
            logger.info(constants.scrape_message+str(care_type))   
        
        
    
    def com_res_url_scrapper(self, url, program_name, dataframe_path):
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
                    try:                        
                        self.program.append(program_name)
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
                        add = box.find('input', {'id': 'Address'})['value']
                        self.addresses.append(add)                        
                        # coord = get_coordinates(add,[])
                        # self.lattitude.append(coord[0])
                        # self.longitude.append(coord[1])
                        self.zipcode.append(add[-5:])
                        # city_state_info = find_city_state_from_zip(add[-5:], [])
                        # self.city.append(city_state_info[0])
                        # self.state.append(city_state_info[1])
                    except:
                        self.addresses.append("NIL")
                        # self.city.append("NIL")
                        # self.state.append("NIL")
                        self.zipcode.append("NIL")
                        # self.lattitude.append("NIL")
                        # self.longitude.append("NIL")
                        
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
        df = pd.read_csv(dataframe_path)
        df['Program'] = self.program
        df['Name'] = self.names 
        df['Links']= self.links 
        df['Contacts'] = self.contact 
        df['Address'] = self.addresses
        df['Zipcode'] = self.zipcode
        df.to_csv(dataframe_path, index=False)
        self.program = []
        self.addresses= []
        self.names = []
        self.links = []
        self.zipcode = []
        self.contact = []
        
                
        
        
if __name__ == '__main__':
    community_resource_scrapper = Community_resource_scrapper()
    
    community_resource_scrapper.community_resource_scrapper()
    