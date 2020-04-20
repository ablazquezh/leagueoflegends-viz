# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:48:01 2020

@author: Alberto
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


save_locations = [''] # put other paths if necessary


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://leagueoflegends.fandom.com/wiki/Patch")


base_patch_url = 'https:\\leagueoflegends.fandom.com'


lookup_data = {'Season Five': 2015, 'Season Six': 2016, 'Season Seven': 2017,
               'Season Eight': 2018}


season_year = []
info_url = []
patch_id = []
patch_type = []

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

table = soup.find('div', {'class': 'va-collapsible-content mw-collapsible-content'})

table_rows = table.findAll('tr')

preseason = False
for i in table_rows:
   
    match = False
    patch_id_aux = None
    
    for idx, j in enumerate(i.findAll('th')):

        if idx == 0:
        
            got = j.find('a')
            
            if got is not None:
                
                got = got.get_text()
                
                if got in lookup_data:
                    
                    match = True                    
                    preseason = True
                    season_year.append(lookup_data[got])
                    
                else:
                    
                    preseason = False
            
            else:
                
                if idx == 0:
                    
                    got = j.get_text()
                    got = got.replace('\n', '')
                    got = got.replace(' ', '')
                    
                    if got == 'Preseason' and preseason == True: # season year > 0 indicates that the corresponding season has been registered
                        
                        season_year.append(season_year[-1] - 1)
                     
        
        elif idx == 1 and match == True:
            
            got = j.get_text()
            
            got = got.replace('\n', '')
            got = got.replace(' ', '')
            
            patch_id_aux = got
            
    if match == True or preseason == True:
        
        patches = i.find('td')
    
        for idx, j in enumerate(patches.findAll('li')):
            
            got = j.find('a', href=True)
            
            patch_rest_url = got['href']
            patch_rest_id = got.get_text()
    
            if match == True:
                patch_id.append(patch_id_aux.replace('x', patch_rest_id))
                patch_type.append('Regular')
                
            elif preseason == True:
                patch_id.append('V'+patch_rest_id)
                patch_type.append('Preseason')
            
            info_url.append(base_patch_url+patch_rest_url.replace('/', '\\'))
    
            if idx > 0:
                
                season_year.append(season_year[-1])
                        
            
driver.close()

patch_info = pd.DataFrame({'Season Year': season_year, 'Info URL': info_url,
                          'ID': patch_id, 'Patch Type': patch_type}) 

for path in save_locations:
    
    patch_info.to_csv(path + 'patch_info.csv', index=False, sep=',')
