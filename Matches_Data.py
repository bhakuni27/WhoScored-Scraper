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

# Load match URLs from a file and store them in a list
matches_urls = []
with open('match_urls.txt') as match_urls_file:
    for match_url in match_urls_file.readlines():
        matches_urls.append(match_url.replace("\n",""))

# List to store matches data
matches_data = []
cookie_flag = True

# Loop through each match URL
for match_url in matches_urls:
    # Open match URL in the browser
    driver.get(BASE_URL+match_url)
    time.sleep(2)
    
    # Handle cookie agreement if needed
    if cookie_flag:
        agree_cookies = driver.find_element(By.CLASS_NAME,"css-1wc0q5e")
        agree_cookies.click()
        time.sleep(2)
        cookie_flag = False

    # Extract match information    
    soup = BeautifulSoup(''.join(driver.page_source), 'html.parser')
    match_header = soup.find('div', {'class':'match-header'})
    match_data = {}
    match_data["Date"] = match_header.find_all('dd')[-1].text.split()[-1]
    match_data["HomeTeam"] = match_header.find_all('a')[0].text
    match_data["AwayTeam"] = match_header.find_all('a')[1].text
    match_data["HTFG"] = match_header.find_all('dd')[2].text.split()[0]
    match_data["ATFG"] = match_header.find_all('dd')[2].text.split()[2]
    match_data["HTHG"] = match_header.find_all('dd')[1].text.split()[0]
    match_data["ATHG"] = match_header.find_all('dd')[1].text.split()[2]
    match_data["HTFormation"] = soup.find_all('div',{'class':'formation'})[0].text.replace("-","")
    match_data["ATFormation"] = soup.find_all('div',{'class':'formation'})[1].text.replace("-","")
    match_data["HTManager"] = soup.find_all('span',{'class':'manager-name'})[0].text
    match_data["ATManager"] = soup.find_all('span',{'class':'manager-name'})[1].text
    match_data["Attendance"] = soup.find('span',{'class':'attendance'})["title"]
    #Few records for referee are not present
    try:
        match_data["Referee"] = soup.find('span',{'class':'referee'})["title"]
    except:
        match_data["Referee"] = ""
    match_data["HTRating"] = soup.find_all('div',{'class':'team-rating'})[0].text
    match_data["ATRating"] = soup.find_all('div',{'class':'team-rating'})[1].text
    match_data["HTShots"] = soup.find_all('div',{'class':'match-centre-stat-values'})[1].find_all('span')[0].text
    match_data["ATShots"] = soup.find_all('div',{'class':'match-centre-stat-values'})[1].find_all('span')[2].text
    match_data["HTSoT"] = soup.find_all('div',{'class':'match-centre-stat-values'})[11].find_all('span')[0].text
    match_data["ATSoT"] = soup.find_all('div',{'class':'match-centre-stat-values'})[11].find_all('span')[2].text
    match_data["HTShotsBlocked"] = soup.find_all('div',{'class':'match-centre-stat-values'})[13].find_all('span')[0].text
    match_data["ATShotsBlocked"] = soup.find_all('div',{'class':'match-centre-stat-values'})[13].find_all('span')[2].text
    match_data["HTPossession"] = soup.find_all('div',{'class':'match-centre-stat-values'})[2].find_all('span')[0].text
    match_data["ATPossession"] = soup.find_all('div',{'class':'match-centre-stat-values'})[2].find_all('span')[2].text
    match_data["HTPassSuccess"] = soup.find_all('div',{'class':'match-centre-stat-values'})[3].find_all('span')[0].text
    match_data["ATPassSuccess"] = soup.find_all('div',{'class':'match-centre-stat-values'})[3].find_all('span')[2].text
    match_data["HTAerialsWon"] = soup.find_all('div',{'class':'match-centre-stat-values'})[5].find_all('span')[0].text
    match_data["ATAerialsWon"] = soup.find_all('div',{'class':'match-centre-stat-values'})[5].find_all('span')[2].text
    match_data["HTCorners"] = soup.find_all('div',{'class':'match-centre-stat-values'})[7].find_all('span')[0].text
    match_data["ATCorners"] = soup.find_all('div',{'class':'match-centre-stat-values'})[7].find_all('span')[2].text
    match_data["HTFouls"] = soup.find_all('div',{'class':'match-centre-stat-values'})[38].find_all('span')[0].text
    match_data["ATFouls"] = soup.find_all('div',{'class':'match-centre-stat-values'})[38].find_all('span')[2].text
    match_data["HTOffsides"] = soup.find_all('div',{'class':'match-centre-stat-values'})[39].find_all('span')[0].text
    match_data["ATOffsides"] = soup.find_all('div',{'class':'match-centre-stat-values'})[39].find_all('span')[2].text
    
    # Append match data to matches_data list
    matches_data.append(match_data)


# Close the WebDriver
driver.close()
# Stop the WebDriver server
server.stop()

# Create a DataFrame from the collected matches data
df = pd.DataFrame(matches_data)

# Save the DataFrame to a CSV file
df.to_csv('Matches_Data.csv', index=False)