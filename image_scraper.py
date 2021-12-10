from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests

# import player names from csv data and save to a list for dynamic url querying
player_names = []

data = pd.read_csv("nhl_statistics.csv")
for i in data["Player"]:
  player_names.append(i.lower().replace(" ", "-").strip())

count = 0
# use player names and BS to scrape player images
for name in player_names:
  try:
    req = Request(f"https://frozenpool.dobbersports.com/players/{name}", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req, timeout=10).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    # player images
    images = soup.find_all('img')
    # player name and team rostered on
    player_team = str(soup.h3).lower()
    #string manipuation for saving player and team name in respective files/folders
    name = player_team[7:player_team.rfind('(')].strip().replace('\xa0', '-')
    team = player_team[player_team.find('/>')+2:-5].strip().replace(' ', '-').replace('.', '')
    
    # for each image url scraped from frozen tools, request and save the image
    for item in images:
      if "uploadfiles" in item['src']:
        #using the requests library, save the images locally
        url = item['src']
        r=requests.get(url)

        # this is done to split up my data for testing
        if count % 10 == 0:
          with open(f'./images/test/{name}.jpg', 'wb') as f:
            f.write(r.content)
        elif team == 'seattle-kraken' or team == '':
          print("skipped") # since the seattle kraken are not in a 2020-21 dataset, we skip these players, as their jerseys and teams will not match up
        else:
          with open(f'./images/{team}/{name}.jpg', 'wb') as f:
            f.write(r.content)
        count = count + 1
  except:
    print("error")
    pass
