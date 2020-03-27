import requests
import time

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://findthemasks.com/give.html'
browser = webdriver.Firefox()
browser.get(url)
time.sleep(15)
soup = BeautifulSoup(browser.page_source, "html.parser")
loc_list = soup.find('div', {'id': 'locations-list'})
df = pd.DataFrame(columns=['State', 'City', 'Location', 'Address', 
						   'Instructions', 'Accepting', 'Open packages?'])
labels = ['Address', 'Instructions', 'Accepting', 'Open packages?']
row_dict = {}
for state in tqdm(loc_list.find_all('div', {'class': 'state'})):
	row_dict['State'] = state.find('h2').string
	for city in state.find_all('div', {'class': 'city'}):
		row_dict['City'] = city.find('h3').string
		for location in city.find_all('div', {'class': 'location'}):
			row_dict['Location'] = location.find('h4').string
			assert all([label.string in labels for label 
						in location.find_all('label')])
			for str_label in labels:
				label = location.find('label', string=str_label)
				if label is not None:
					row_dict[str_label] = label.next_sibling.get_text(
						separator='\n')
				else:
					row_dict[str_label] = ''
			df = df.append(row_dict, ignore_index=True)
df.to_csv('donation_sites.csv')