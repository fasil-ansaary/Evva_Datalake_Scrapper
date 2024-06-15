#@V2scrapperevva
#v2-scrapper
import json
import pandas as pd
from alive_progress import alive_bar
import logging
import os
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
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
    
    def community_resource_scrapper(self, states_to_scrape):    
        # states_to_scrape = sys.argv[1]#["NY"]#, "MI", "IL", "CA", "TX", "NY", "GA"]
        for state in states_to_scrape:
            zipcodes = zipcode_extractor(state)  
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
            for i in constants.community_resource_finder_url_mapper:                          
                file_name = '_'.join(list(i.split()))                 
                csv_sys_path = file_name+"_"+state+constants.csv_extension
                if not os.path.exists(csv_sys_path):
                    df.to_csv(csv_sys_path, index=False)
                else:
                    df = pd.read_csv(csv_sys_path)
                    zipcodes_already_scrapped = df['Zipcode_feeded_to_scrape'].tolist()
                    zipcodes = [item for item in zipcodes if item not in zipcodes_already_scrapped]
                self.options = Options()
                self.options.headless = True
                self.driver = webdriver.Chrome(options=self.options)                
                scrapping_url = constants.community_resource_finder_url_mapper[i]
                url_specific_id = re.findall(r'\d+', scrapping_url)[0]
                care_type = i              
                with alive_bar(len(zipcodes)) as bar:                               
                    bar.title(f'Scrapping {i} for {state}:')    
                    for zip in zipcodes:
                        com_res_url = url_updater(scrapping_url, zip)
                        self.com_res_url_scrapper(com_res_url, care_type, zip, url_specific_id)                                            
                        df = pd.read_csv(csv_sys_path)
                        try:
                            df = df.reindex(range(len(df) + len(self.program)))
                            # Appending the new values
                            df['Program'].iloc[-len(self.program):] = self.program
                            df['Name'].iloc[-len(self.names):] = self.names
                            df['Links'].iloc[-len(self.links):] = self.links
                            df['Contacts'].iloc[-len(self.contact):] = self.contact
                            df['Distance'].iloc[-len(self.distances):] = self.distances
                            df['Address'].iloc[-len(self.addresses):] = self.addresses
                            df['General Information'].iloc[-len(self.gen_information_data):] = self.gen_information_data
                            df['Staff Information'].iloc[-len(self.staff_information_data):] = self.staff_information_data
                            df['Services'].iloc[-len(self.service_offered_data):] = self.service_offered_data
                            df['Financial Information'].iloc[-len(self.financial_information_data):] = self.financial_information_data
                            df['Availability'].iloc[-len(self.availability_information_data):] = self.availability_information_data
                            df['Pricing and Availability'].iloc[-len(self.pricing_availability_data):] = self.pricing_availability_data
                            df['Experiences'].iloc[-len(self.experiences_data):] = self.experiences_data
                            df['Zipcode_feeded_to_scrape'].iloc[-len(self.zipcode):] = self.zipcode
                            df.drop_duplicates(subset=['Address'], inplace=True)  
                            df.to_csv(csv_sys_path, index=False)                            
                        except Exception as e:  
                            print(e)
                        self.clean_constructors()
                        bar()                                                      
                logger.info(constants.scrape_message+str(care_type))               
    
    def clean_constructors(self):
        self.names.clear()
        self.links.clear()
        self.addresses.clear()
        self.contact.clear()     
        self.program.clear()
        self.distances.clear()
        self.zipcode.clear()
        self.gen_information_data.clear()
        self.staff_information_data.clear()
        self.service_offered_data.clear()
        self.financial_information_data.clear()
        self.availability_information_data.clear()
        self.pricing_availability_data.clear()
        self.overview_information_data.clear()
        self.features_data.clear()
        self.experiences_data.clear()
        
    
    def com_res_url_scrapper(self, url, program_name, zip, url_specific_id):
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
                        self.names.append(box.find('a').text.strip())
                        self.program.append(program_name)
                        self.zipcode.append(zip)   
                    except:
                        self.names.append("NIL")
                        self.program.append(program_name)
                        self.zipcode.append(zip) 
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
            try:
                response = requests.get(scrapped_links[s])
                soup = BeautifulSoup(response.content, "html.parser")
                for h2 in soup.find_all('h2'):
                    h2.string = h2.string + '-'
                
                #ids for scrapping
                gen_id = "tabS2P"+url_specific_id
                staff_id = "tabS3P"+url_specific_id
                service_id = "tabS6P"+url_specific_id
                pricing_id = "tabS9P"+url_specific_id
                exp_id = "tabS8P"+url_specific_id
                financial_id = "tabS4P"+url_specific_id
                availability_id = "tabS5P"+url_specific_id
                time.sleep(5)
                # General Information
                try:                           
                    general_info = soup.find("div", id= gen_id).get_text(strip=True, separator=' ')
                    self.gen_information_data.append(general_info) 
                except:
                    self.gen_information_data.append("nil")
                    
                try:            
                    # Staff Information
                    staff_info = soup.find("div", id= staff_id).get_text(strip=True, separator=' ')
                    self.staff_information_data.append(staff_info) 
                except:
                    self.staff_information_data.append("nil")
                    
                try:            
                    # Services Offered
                    services_info= soup.find("div",id= service_id).get_text(strip=True, separator=' ')
                    self.service_offered_data.append(services_info)
                except:
                    self.service_offered_data.append("nil")
                
                try:    
                    # Pricing & Availability
                    pricing_availability_info = soup.find("div", id= pricing_id).get_text(strip=True, separator=' ')
                    self.pricing_availability_data.append(pricing_availability_info)
                except:
                    self.pricing_availability_data.append("nil")
                    
                try:
                    # Experience Information
                    experiences = soup.find("div", id= exp_id).get_text(strip=True, separator=' ')
                    self.experiences_data.append(experiences)
                except:
                    self.experiences_data.append("nil")   
                try:
                    # Financial Information
                    financial_info = soup.find("div", id= financial_id).get_text(strip=True, separator=' ')
                    self.financial_information_data.append(financial_info)
                except:
                    self.financial_information_data.append("nil")  
                
                try:
                    # Availability
                    availability_info = soup.find("div", id= availability_id).get_text(strip=True, separator=' ')
                    self.availability_information_data.append(availability_info)
                except:
                    self.availability_information_data.append("nil")
                # try:
                #     overview_info = soup.find("div", id= "tabP73").get_text(strip=True, separator=' ')
                #     self.overview_information_data.append(overview_info)
                # except:
                #     self.overview_information_data.append("nil")
                s+=1   
            except Exception as e:    
                print(f'{e} for zip:{zip}')            
                s+=1   
        
        
if __name__ == '__main__':
    states_to_scrape = [sys.argv[1]]
    community_resource_scrapper = Community_resource_scrapper()
    
    community_resource_scrapper.community_resource_scrapper(states_to_scrape=states_to_scrape)
    