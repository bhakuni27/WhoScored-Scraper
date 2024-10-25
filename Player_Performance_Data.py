# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import json

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

# List to store players' data
players_data = []
cookie_flag = True

# Mapping of event symbols to their meanings
symbol_dict = {
    "1": "Assits",
    "16": "Goals",
    "17": "Card",
    "51": "ErrorLeadstoGoal",
    "58": "PenaltySaved",
    "15": "PenaltyMissed"
}

# Function to extract and summarize player statistics for a team
def get_team_players_summary(players_stats,date,defensive_stat_button,venue):
    player_list = []
    pos = []
    pos_meta_data = players_stats.find_all('span',{'class':'player-meta-data'})
    # Extract positions of players
    for i in range(len(pos_meta_data)):
        if pos_meta_data[i].text.split()[0] == ',':
            pos.append(pos_meta_data[i].text.split()[1])
    
    # Extract player statistics
    for i in range(len(players_stats.find_all('span',{'class':'iconize iconize-icon-left'}))):
        player_record = {}
        symbol_stats = {}
        player_record["Name"] = players_stats.find_all('span',{'class':'iconize iconize-icon-left'})[i].text
        current_age = players_stats.find_all('span',{'class':'player-meta-data','style':'padding-left: 3px;'})[i].text
        player_record["Age"] = int(current_age) - (23 - int(date))
        player_record["Position"] = pos[i*2]
        player_record["Shots"] = players_stats.find_all('td',{'class':'ShotsTotal'})[i].text.replace("\t","")
        player_record["SoT"] = players_stats.find_all('td',{'class':'ShotOnTarget'})[i].text.replace("\t","")
        player_record["KeyPasses"] = players_stats.find_all('td',{'class':'KeyPassTotal'})[i].text.replace("\t","")
        player_record["PassAccuracy"] = players_stats.find_all('td',{'class':'PassSuccessInMatch'})[i].text.replace("\t","")
        player_record["AerialsWon"] = players_stats.find_all('td',{'class':'DuelAerialWon'})[i].text.replace("\t","")
        player_record["Touches"] = players_stats.find_all('td',{'class':'Touches'})[i].text.replace("\t","")
        player_record["Rating"] = players_stats.find_all('td',{'class':'rating'})[i].text
        incident = players_stats.find_all('td',{'style':'text-align: left'})[i]
        if len(incident.find_all('span')) > 1:
            for j in range(1,len(incident.find_all('span'))):
                value = incident.find_all('span')[j]["data-type"]
                if value in symbol_dict:
                    if value == '16':
                        if 'data-event-satisfier-goalnormal' in incident.find_all('span')[j].attrs:
                            symbol_stats["Goals"] = symbol_stats.get("Goals",0) + 1
                        elif 'data-event-satisfier-penaltyscored' in incident.find_all('span')[j].attrs:
                            symbol_stats["PenaltyScored"] = symbol_stats.get("PenaltyScored",0) + 1
                            symbol_stats["Goals"] = symbol_stats.get("Goals",0) + 1
                        elif 'data-event-satisfier-goalown' in incident.find_all('span')[j].attrs:
                            symbol_stats["OwnGoals"] = symbol_stats.get("OwnGoals",0) + 1
                    elif value == '17':
                        if 'data-event-satisfier-redcard' in incident.find_all('span')[j].attrs:
                            symbol_stats["RedCard"] = symbol_stats.get("RedCard",0) + 1
                        elif 'data-event-satisfier-yellowcard' in incident.find_all('span')[j].attrs:
                            symbol_stats["YellowCard"] = symbol_stats.get("YellowCard",0) + 1
                    else:
                        symbol_stats[symbol_dict[value]] = symbol_stats.get(symbol_dict[value],0) + 1
        player_record["Goals"] = symbol_stats.get("Goals",0)
        player_record["Assits"] = symbol_stats.get("Assits",0)
        player_record["YellowCard"] = symbol_stats.get("YellowCard",0)
        player_record["RedCard"] = symbol_stats.get("RedCard",0)
        player_record["PenaltyScored"] = symbol_stats.get("PenaltyScored",0)
        player_record["PenaltySaved"] = symbol_stats.get("PenaltySaved",0)
        player_record["PenaltyMissed"] = symbol_stats.get("PenaltyMissed",0)
        player_record["OwnGoals"] = symbol_stats.get("OwnGoals",0)
        player_record["ErrorLeadstoGoal"] = symbol_stats.get("ErrorLeadstoGoal",0)
        player_list.append(player_record)

    # Extract additional defensive statistics    
    defensive_stat_button.click()
    time.sleep(2)
    soup = BeautifulSoup(''.join(driver.page_source), 'html.parser')
    defensive_stats = soup.find('div',{'id':'statistics-table-'+venue+'-defensive'})
    for i in range(len(defensive_stats.find_all('span',{'class':'iconize iconize-icon-left'}))):
        player_list[i]["TackleWon"] = defensive_stats.find_all('td',{'class':'TackleWonTotal'})[i].text.replace("\t","")
        player_list[i]["Interception"] = defensive_stats.find_all('td',{'class':'InterceptionAll'})[i].text.replace("\t","")
        player_list[i]["Clearance"] = defensive_stats.find_all('td',{'class':'ClearanceTotal'})[i].text.replace("\t","")
        player_list[i]["ShotBlocked"] = defensive_stats.find_all('td',{'class':'ShotBlocked'})[i].text.replace("\t","")
        player_list[i]["Fouls"] = defensive_stats.find_all('td',{'class':'FoulCommitted'})[i].text.replace("\t","")    
    
    return player_list

# Loop through each match URL
for match_url in matches_urls:
    driver.get(BASE_URL+match_url)
    time.sleep(2)
    
    # Handle the cookie agreement if needed
    if cookie_flag:
        agree_cookies = driver.find_element(By.CLASS_NAME,"css-1wc0q5e")
        agree_cookies.click()
        time.sleep(2)
        cookie_flag = False

    # Extract match information    
    soup = BeautifulSoup(''.join(driver.page_source), 'html.parser')
    match_header = soup.find('div', {'class':'match-header'})
    player_data = {}
    player_data["Date"] = match_header.find_all('dd')[-1].text.split()[-1]
    player_data["HomeTeam"] = match_header.find_all('a')[0].text
    player_data["AwayTeam"] = match_header.find_all('a')[1].text
    player_data["HTManager"] = soup.find_all('span',{'class':'manager-name'})[0].text
    player_data["ATManager"] = soup.find_all('span',{'class':'manager-name'})[1].text
    player_data["Attendance"] = soup.find('span',{'class':'attendance'})["title"]
    try:
        player_data["Referee"] = soup.find('span',{'class':'referee'})["title"]
    except:
        player_data["Referee"] = ""
    
    # Click player statistics button
    player_stats_button = driver.find_element(By.ID,'sub-sub-navigation').find_elements(By.TAG_NAME,'a')[1]
    player_stats_button.click()
    time.sleep(2)

    # Extract and summarize player data for both teams
    soup = BeautifulSoup(''.join(driver.page_source), 'html.parser')
    defensive_stat_button = driver.find_element(By.ID,'live-player-stats').find_elements(By.LINK_TEXT,'Defensive')
    player_data["home_players"] = get_team_players_summary(soup.find('div',{'id':'live-player-home-summary'}),
                                                           player_data["Date"][-2:],defensive_stat_button[0],'home')
    player_data["away_players"] = get_team_players_summary(soup.find('div',{'id':'live-player-away-summary'}),
                                                           player_data["Date"][-2:],defensive_stat_button[1],'away')
    
    players_data.append(player_data)


# Close the WebDriver
driver.close()
# Stop the WebDriver server
server.stop()

# Write players' data to a JSON file
with open('players_data.json', 'w') as players_data_file:
     players_data_file.write(json.dumps(players_data))