# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 21:04:28 2020

@author: Alberto
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

month_dict = {'January': '1',
 'February': '2',
 'March': '3',
 'April': '4',
 'May': '5',
 'June': '6',
 'July': '7',
 'August': '8',
 'September': '9',
 'October': '10',
 'November': '11',
 'December': '12'}


def formatString(string):
    
    string = string.replace('\n', '')
    string = string.replace('\xa0', '')
            
    return string


def returnDate(date):
    
    month = month_dict[formatString(date[0])]
    year = date[2]
    day = re.search('[0-9]*', date[1]).group(0)

    return day +'-'+ month +'-'+ year

patch_info = pd.read_csv('patch_info.csv')

champion_names = pd.read_csv('all_champions.csv')

save_locations = [''] # put other paths if necessary

patch_id = []
champion = []
patch_date = []
change_description = []

for i in range(len(patch_info)):

    url_check = patch_info.loc[i, 'Info URL']

    driver = webdriver.Chrome("chromedriver.exe")
    
    driver.get(url_check)
    
    
    content = driver.page_source
    
    soup = BeautifulSoup(content, 'html.parser')
    
    
    patch_id.append(soup.find('h1', {'class': 'page-header__title'}).get_text())


    date_info = soup.find('td', {'class': 'pi-horizontal-group-item pi-data-value pi-font pi-border-color pi-item-spacing'}).get_text().split(' ')
    patch_date.append(returnDate(date_info))
    
    
    champion_info = soup.findAll('dl')
    first_added = False # There may be a more elegant way to do this
    
    for idx, j in enumerate(champion_info):
                
        champion_name = j.find('span', {'style': 'white-space:normal;'})
    
        if champion_name is not None:
    
            champion_name = champion_name.get_text()
            
            if champion_name in champion_names['Champion Name'].tolist():
                
                changes = j.find_next_sibling()
                
                #print(champion_name)
                #print("==========")
                
                changes = changes.findAll('li')
                info_sets = [li.find_parent().find_parent().name for li in changes]
                info_sets_2nd = [li.find_parent().find_parent().find_parent().find_parent().name for li in changes]
                
                #print(info_sets)
                #print(info_sets_2nd)
                
                idxs = np.where(np.isin(info_sets, 'div'))
                idxs = list(idxs[0]) # This is done because the previous line returns an unhelping tuple
                
                ctr = 0
                champion_updates_count = 0
                for x in idxs:
                    
                    text = changes[x].get_text()
                    text = re.sub('<img [^>]*', '', text) 
                    text = text.replace(' >', '') # There may be a more elegant way to do this
                    
                    text_cells = text.split('\n')
                    text_cells = [x for x in text_cells if len(x) > 0] # There may be a more elegant way to do this
                    
                    if len(text_cells) == 2: # This is, just [div, li]
                        
                        change_description.append({text_cells[0]: text_cells[1]})
                        champion_updates_count = champion_updates_count +1
                        
                    else:
                        
                        if info_sets_2nd[ctr-1] != 'li': # In case everything are divs (e.g. [div, div, div, div])
                            
                            change_description.append({text_cells[0]: [x for idx, x in enumerate(text_cells) if idx > 0] })
                            champion_updates_count = champion_updates_count +1
                            
                        else: 
                            
                            li_idxs = np.where(np.isin(info_sets_2nd[ctr:ctr+len(text_cells)], 'li'))
                            
                            li_idxs = list(li_idxs[0]) # This is done because the previous line returns an unhelping tuple
                            
                            if len(li_idxs) > 1:
                            
                                diff_li_idxs = np.diff(li_idxs) # Difference between indexes will never be > 2
                                
                                li_twos = np.where(np.isin(diff_li_idxs, 2))
                                li_twos = list(li_twos[0])
                                
                                if len(li_twos) == 0: # All are 1s and can be coupled in the same array
                                    
                                    item = [text_cells[x] for x in li_idxs]
                                    for text_idx in np.flip(np.arange(len(text_cells)-len(li_idxs))):
                                        item = {text_cells[text_idx]: item}
                                
                                else:
                                    
                                    li_set = []
                                    coupled = {}
                                    for cell in np.flip(np.arange(1, len(info_sets_2nd))):
                                    
                                        if info_sets_2nd[cell] == 'li':
                                        
                                            li_set.append(text_cells[cell])
                                        
                                        elif info_sets_2nd[cell] == 'div':
                                            
                                            coupled[text_cells[cell]] = li_set
                                            li_set = []
                                            
                                    change_description.append({text_cells[0]: coupled})
                                    champion_updates_count = champion_updates_count +1

                                        
                            else: # There is only one li
                                
                                item = text_cells[-1]
                                for text_idx in np.flip(np.arange(len(text_cells)-1)):
                                    item = {text_cells[text_idx]: item}
                                    
                                change_description.append(item)
                                champion_updates_count = champion_updates_count +1


                                
                                    
                            #print("*********")
                            #print(li_idxs)
                            
                
                    ctr = ctr + len(text_cells)
                                        
                    #print(text_cells)

                    #print("xxxxxxxxxx")
                   
                    
                if first_added == True:
                    
                    patch_id.append(patch_id[-1])
                    patch_date.append(patch_date[-1])
                    
        
                #print(champion_updates_count)
                
                initial_change_idx = len(change_description) - champion_updates_count
                for content in change_description[initial_change_idx +1: ]:
                    
                    change_description[initial_change_idx].update( content )
                    
                del(change_description[initial_change_idx +1 : ])
                
                champion.append(champion_name)
                first_added = True

driver.close()

patchInfo_detail = pd.DataFrame({'ID': patch_id, 'Champion': champion, 'Date': patch_date, 'Change Description': change_description}) 

for path in save_locations:
    
    patchInfo_detail.to_csv(path + 'patchInfo_detail.csv', index=False, sep=',')
