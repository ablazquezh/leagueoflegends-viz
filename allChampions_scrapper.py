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
champion_role1 = []
champion_role2 = []
champion_last_patch_change= []
champion_ability_cost_type = []
champion_range_type = []
champion_damage_type = []

content = driver.page_source

soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table', {'class': 'wikitable sortable jquery-tablesorter'})

table_rows = table.findAll('td', {'style': 'text-align:left;'})

for i in table_rows:
    
    champion_names.append(i['data-sort-value'])
        
    role1 = i.find_next('td')
    role2 = role1.find_next('td')
    
    champion_role1.append(role1['data-sort-value'])
    
    if 'data-sort-value' in role2.attrs:
      champion_role2.append(role2['data-sort-value'])
      
    last_change = role2.find_next('td').find_next('td')
    
    champion_last_patch_change.append(last_change.find('a')['title'])
    
    
    champion_info_url = "https://leagueoflegends.fandom.com/" + i.find('a')['href']
    
    driver.get(champion_info_url)
    
    champion_info_content = driver.page_source

    champion_info_soup = BeautifulSoup(champion_info_content, 'html.parser')
    
    champion_info_table = champion_info_soup.find('tbody')
    
    # Needs two find_next commands to skip the first section ("Role") - There may be a more elegant way to do this.
    champion_other_info = champion_info_table.find_next('th', {'class' : 'data-label'}).find_next('th', {'class' : 'data-label'})
    
    
    champion_other_info = champion_other_info.find_next('td', {'class' : 'data-value'})
    
    champion_ability_cost_type_info = champion_other_info.find_next('span')
    champion_ability_cost_type.append(champion_ability_cost_type_info['data-param'])
    
    
    champion_range_type_info = champion_other_info.find_next('span').find_next('span')
    champion_range_type.append(champion_range_type_info['data-param'])
    
    
    champion_damage_type_info = champion_other_info.find_next('span').find_next('span').find_next('span')
    champion_damage_type_info = champion_damage_type_info.find_next('a')
    champion_damage_type.append(champion_damage_type_info.get_text())
    
        
driver.close()


all_champions_info = pd.DataFrame({'Champion Name': champion_names, 'Role1': champion_role1, 'Role2': champion_role2,
                                   'Last Change Patch': champion_last_patch_change,
                                   'Ability Cost Type': champion_ability_cost_type, 'Range Type': champion_range_type, 'Damage Type': champion_damage_type}) 

for path in save_locations:
    
    all_champions_info.to_csv(path + 'all_champions_info.csv', index=False, sep=',')

