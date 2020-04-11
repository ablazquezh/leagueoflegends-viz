# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 22:00:02 2020

@author: Alberto
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd


save_locations = [''] # put other paths if necessary


driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")

champion_names = []

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable jquery-tablesorter'})

table_rows = table.findAll('td', {'style': 'text-align:left;'})

for i in table_rows:
    
    champion_names.append(i['data-sort-value'])
        
driver.close()

all_champions = pd.DataFrame({'Champion Name': champion_names}) 

for path in save_locations:
    
    all_champions.to_csv(path + 'all_champions.csv', index=False, sep=',')

