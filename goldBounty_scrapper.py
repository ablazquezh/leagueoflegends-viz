# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 13:07:28 2020

@author: Alberto
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


save_locations = [''] # put other paths if necessary


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://leagueoflegends.fandom.com/wiki/Kill")


def formatString(string, input_type):
    
    string = string.replace('\n', '')
    string = string.replace('\xa0', '')
    
    if len(string) == 0:
    
        string = np.nan
        
    elif len(string) > 1:
        
        if input_type == 0:
            
            string = '-' + string[1]
            
        elif input_type == 1 or input_type == 2:
            
            string = string[0]
        
    return string


tier = []
consec_kills = []
consec_deaths = []
kill_bounty = []
assist_bounty = []


content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table', {'class': 'article-table'})

table_headers = table.findAll('th')

table_rows = table.findAll('tr')


for i in table_rows:
    
    for idx, j in enumerate(i.findAll('td')):
        
        if idx == 0:
        
            got = j.get_text()
            
            got = formatString(got, 0)
            
            tier.append(float(got))
            
        elif idx ==1:
            
            got = j.get_text()
            
            got = formatString(got, 1)
            
            consec_kills.append(float(got))
            
        elif idx ==2:
            
            got = j.get_text()
            
            got = formatString(got, 2)
                
            consec_deaths.append(float(got))
            
        elif idx ==3:
            
            got = j.find('span', {'style': 'white-space:normal;'}).get_text()
            
            kill_bounty.append(float(got))
            
        elif idx ==4:
            
            got = j.find('span', {'style': 'white-space:normal;'}).get_text()
            
            assist_bounty.append(float(got))
            

driver.close()

gold_info = pd.DataFrame({'Tier': tier,'Consecutive Kills': consec_kills,
                          'Consecutive Deaths': consec_deaths, 'Kill Bounty': kill_bounty,
                          'Assist Bounty': assist_bounty}) 

for path in save_locations:
    
    gold_info.to_csv(path + 'gold_info.csv', index=False, sep=',')
