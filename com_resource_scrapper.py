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

zipcodes = zipcode_extractor()[:2]


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
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)     
        scrapping_url = "https://www.communityresourcefinder.org/ProviderSearch/Search?ProfileDefinitionId=75&location="
        care_type = "Geriatricians"
        file_name = "Geriatricians"
        with alive_bar(len(zipcodes)) as bar:              
            bar.title(f'Scrapping {care_type}:')
            for zip in zipcodes:
                com_res_url = url_updater(scrapping_url, zip)
                self.com_res_url_scrapper(com_res_url, care_type)                                            
                bar()    
        # print(
        #     len(self.program),
        #     len(self.names),
        #     len(self.links),
        #     len(self.contact),
        #     len(self.addresses),
        #     len(self.city),
        #     len(self.state),
        #     len(self.zipcode),
        #     len(self.general_information_data),
        #     len(self.early_stage_programs_data),
        #     len(self.education_programs_data),
        #     len(self.support_groups_data),
        #     len(self.social_engagement_programs_data),
            
        # )
        df = pd.DataFrame( 
            { 
            'Program' : self.program,
            'Name': self.names, 'Links': self.links, 'Contacts': self.contact, 
            'Address': self.addresses,
            'City':self.city, 'State': self.state, 'Zipcode' : self.zipcode,
            # 'General Information' : self.general_information_data, 
            # 'Staff Information' : self.staff_info,
            'Service Offered' : self.service_offered,
            # 'Pricing' : self.pricing,
            # 'Financial Information' : self.financial,
            # 'Availability' : self.avail
            })
        df.drop_duplicates(subset=['Address'], inplace=True)
        df.to_csv(constants.file_path+file_name+constants.csv_extension, index=False)
        logger.info(constants.scrape_message+str(care_type))   
        
        
    
    def com_res_url_scrapper(self, url, program_name):
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
                        city_state_info = find_city_state_from_zip(add[-5:], [])
                        self.city.append(city_state_info[0])
                        self.state.append(city_state_info[1])
                    except:
                        self.addresses.append("NIL")
                        self.city.append("NIL")
                        self.state.append("NIL")
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
        length = len(scrapped_links)
        # print(length)
        s = 0
        while s < length:

            response = requests.get(scrapped_links[s])
            soup = BeautifulSoup(response.content, "html.parser")
            for h2 in soup.find_all('h2'):
                h2.string = h2.string + '-'
                
            time.sleep(5)
            # try:       
            #     general_info = soup.find("div", id= "tab-0").get_text(strip=True, separator=' ')
            #     # print(general_info)
            #     self.general_information_data.append(general_info) 
            # except:
            #     # print("nil")
            #     self.general_information_data.append("nil")

            # try:
            #     early_stage_info = soup.find("div", id= "tab-1").get_text(strip=True, separator=' ')
            #     # print(early_stage_info)
            #     self.staff_info.append(early_stage_info)
            # except:
            #     # print("nil")
            #     self.staff_info.append("nil")

            try:            
                # Staff Information
                education_info = soup.find("div", id= "tab-0").get_text(strip=True, separator=' ')
                # print(education_info)
                self.service_offered.append(education_info) 
            except:
                # print("nil")
                self.service_offered.append("nil")

            # try:            
            #     social_engagement_info= soup.find("div",id= "tab-4").get_text(strip=True, separator=' ')
            #     # print(social_engagement_info)
            #     self.avail.append(social_engagement_info)
            # except:
            #     # print("nil")
            #     self.avail.append("nil")
            # try:            
            #     social_engagement_info= soup.find("div",id= "tab-3").get_text(strip=True, separator=' ')
            #     # print(social_engagement_info)
            #     self.financial.append(social_engagement_info)
            # except:
            #     # print("nil")
            #     self.financial.append("nil")

            s+=1
                
        
        
if __name__ == '__main__':
    community_resource_scrapper = Community_resource_scrapper()
    
    community_resource_scrapper.community_resource_scrapper()
    