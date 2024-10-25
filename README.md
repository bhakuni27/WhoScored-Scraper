# WhoScored-Scraper

This project is a Python-based web scraper designed to extract player statistics and match summaries from [WhoScored.com](https://www.whoscored.com/). The tool streamlines data collection for those interested in monitoring player performance and match outcomes, providing summarized data that can be easily analyzed for sports analytics and research.

## Prerequisites
Ensure you have **Python3** and **pip** installed on your system. If not, you can download python from [python.org](https://www.python.org/).  
To install the required libraries, run the following commands:
```
pip install beautifulsoup4
pip install pandas
pip install selenium
```

## WebDriver Setup
This project uses **Selenium** for automated browser control. To set up Selenium for your environment:

1. Visit the [Selenium Python documentation](http://selenium-python.readthedocs.io/installation.html) and download the appropriate WebDriver for your browser. This project uses **Microsoft Edge**, so I downloaded **msedgedriver**.
2. Copy the WebDriver executable (e.g., `msedgedriver`) into the same folder as the Python files in this repository.

## Usage
### 1. Clone the Repository
Clone the repository to your local machine:
```
git clone https://github.com/bhakuni27/WhoScored-Scraper.git
cd <repository-folder>
```
### 2. Configure Season URLs
In the file `season_urls.txt`, enter the URLs of the seasons for which you want to collect data.  
>**Important:** Only include the section of the URL after `https://www.whoscored.com`. For example, for the full URL:
>```
>https://www.whoscored.com/Regions/252/Tournaments/2/Seasons/10316/Stages/23400/Show/England-Premier-League-2024-2025
>```
>You should only enter:
>```
>/Regions/252/Tournaments/2/Seasons/10316/Stages/23400/Show/England-Premier-League-2024-2025
>```

### 3. Generate Match URLs
- Open `Match_URLs.py`.
- Edit lines 10 and 20 to specify the path to your WebDriver (`msedgedriver`).
- Run the following command to generate match URLs:
   ```
   python3 Match_URLs.py
   ```
This will create a new file named `match_urls.txt`, which will contain all the URLs of the matches from which data will be extracted.

### 4. Extract Match Summarized Data
- Open `Matches_Data.py`.
- Edit lines 9 and 19 to point to your WebDriver (`msedgedriver`).
- Run the following command to gather match summaries:
   ```
   python3 Matches_Data.py
   ```
This will create a new file named `Matches_Data.csv`, containing summarized data for all the matches listed in `match_urls.txt`.

### 5. Extract Player Performance Data
- Open `Player_Performance_Data.py`.
- Edit lines 10 and 20 to specify the path to your WebDriver (`msedgedriver`).
- Run the following command to gather player performance data:
   ```
   python3 Player_Performance_Data.py
   ```
This will create a new file named `players_data.json`, containing player performance data for all the matches in `match_urls.txt`.

> **NOTE:** This scraper is subject to the availability and structure of data on WhoScored.com. Changes on the website may affect the functionality of this tool.

