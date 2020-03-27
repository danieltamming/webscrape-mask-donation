import re
import requests
import string
import argparse
import time

import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup, Comment
from selenium import webdriver
import urllib.request

# url = 'https://getusppe.org/give/'
url = 'https://findthemasks.com/give.html'
df = pd.DataFrame(columns=['State', 'City', 'Location', 'Address', 
						   'Instructions', 'Accepting', 'Open packages?'])

browser = webdriver.Firefox()
browser.get(url)
time.sleep(15)
soup = BeautifulSoup(browser.page_source, "html.parser")

# headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'}
# page = requests.get(url, headers=headers)
# soup = BeautifulSoup(page.text, 'html.parser')
loc_list = soup.find('div', {'id': 'locations-list'})

# print(loc_list.prettify())

# print(100*'#')
labels = ['Address', 'Instructions', 'Accepting', 'Open packages?']

row_dict = {}
i = 0
for state in tqdm(loc_list.find_all('div', {'class': 'state'})):
	row_dict['State'] = state.find('h2').string
	for city in state.find_all('div', {'class': 'city'}):
		row_dict['City'] = city.find('h3').string
		for location in city.find_all('div', {'class': 'location'}):
			row_dict['Location'] = location.find('h4').string
			assert all([label.string in labels for label in location.find_all('label')])
			for str_label in labels:
				label = location.find('label', string=str_label)
				if label is not None:
					row_dict[str_label] = label.next_sibling.get_text(separator='\n')
				else:
					row_dict[str_label] = ''
			# label_list = location.find_all('label')
			# for label, str_label in zip(label_list, labels):
			# 	assert str_label == label.string
			# 	row_dict[str_label] = label.next_sibling.get_text()
			df = df.append(row_dict, ignore_index=True)
df.to_csv('donation_sites.csv')