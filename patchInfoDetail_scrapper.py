# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 21:04:28 2020

@author: Alberto
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
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

save_locations = ['', 'C:\\Users\\Alberto\\Desktop\\UNED\\2O CUATRIMESTRE\\VD\\data\\scrapped\\'] # put other paths if necessary

patch_id = []
champion = []
patch_date = []
change_description = []

for i in range(1):#len(patch_info)):

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
                
                #changes = soup.findAll('ul')
                changes =j.find_next_sibling('ul')
                
                
                print(changes)
                print("____________________")
                """
                for k in changes:
                    
                    summary = {}
                    print(k.find('ul'))
            """
                if first_added == True:
                    
                    patch_id.append(patch_id[-1])
                    patch_date.append(patch_date[-1])
                    
        
                champion.append(champion_name)
                first_added = True

driver.close()

patchInfo_detail = pd.DataFrame({'ID': patch_id, 'Champion': champion, 'Date': patch_date}) 

for path in save_locations:
    
    patchInfo_detail.to_csv(path + 'patchInfo_detail.csv', index=False, sep=',')
