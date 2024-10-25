# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Set the path to the WebDriver executable
PATH_TO_DRIVER = './msedgedriver'
# Base URL for the website
BASE_URL = 'https://www.whoscored.com'

# Create a WebDriver server instance
server = webdriver.edge.service.Service(PATH_TO_DRIVER)
# Start the server
server.start()

# Connect to the WebDriver using a Remote instance
driver = webdriver.Remote(server.service_url, options=webdriver.EdgeOptions())
# Introduce a delay of 2 seconds
time.sleep(2)

# Read season URLs from a file and store them in a list
season_urls = []
with open('season_urls.txt') as season_urls_file:
    season_urls = season_urls_file.readlines()

# Function to extract match URLs from the page content
def get_match_urls(content):
    soup = BeautifulSoup(''.join(content), 'html.parser')
    matches = soup.find('div', {'class':'divtable-body'})
    matches_rows = matches.find_all('div',{'class':['divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt',
                                                    'divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12']})
    # Extract match URLs from each row
    for match_row in matches_rows:
        matches_urls.append(match_row.find('a',{'class':'result-1 rc'})['href'])
    
    # Extract the title of the previous button
    try:
        prev_button_title = soup.find('a',{'class':'previous button ui-state-default rc-l is-default'})["title"]
    except:
        prev_button_title = soup.find('a',{'class':'previous button ui-state-default rc-l is-disabled'})["title"]
    return prev_button_title

# List to store extracted match URLs
matches_urls = []
cookie_flag = True

# Iterate through each season URL
for season_url in season_urls:
    # Open the season URL in the browser
    driver.get(BASE_URL+season_url)
    print(season_url)
    # Introduce a delay of 2 seconds
    time.sleep(2)
    
    # Handle the cookie agreement if needed
    if cookie_flag:
        agree_cookies = driver.find_element(By.CLASS_NAME,"css-1wc0q5e")
        agree_cookies.click()
        time.sleep(2)
        cookie_flag = False

    # Extract match URLs from the current page    
    prev_week = get_match_urls(driver.page_source)
    
    # Iterate through all weeks of the current season
    while prev_week == 'View previous week':
        prev_week_button = driver.find_element(By.CLASS_NAME,"previous.button.ui-state-default.rc-l.is-default")
        prev_week_button.click()
        time.sleep(2)
        prev_week = get_match_urls(driver.page_source)

# Close the WebDriver
driver.close()
# Stop the WebDriver server
server.stop()

# Write extracted match URLs to a file
with open('match_urls.txt','w') as match_urls_file:
    match_urls_file.writelines('\n'.join(matches_urls))