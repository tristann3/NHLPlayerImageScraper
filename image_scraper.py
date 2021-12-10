from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd
import requests

# import player names from csv data and save to a list for dynamic url querying
player_names = {}
#lookup table cooresponding abbreviations to team names
nhl_teams = {
  "ANA" : 'anaheim-ducks',
  "ARI" : 'arizona-coyotes',
  "BOS" : 'boston-bruins',
  "BUF" : 'buffalo-sabres',
  "CGY" : 'calgary-flames',
  "CAR" : 'carolina-hurricanes',
  "CHI" : 'chicago-blackhawks',
  "COL" : 'colorado-avalanche',
  "CBJ" : 'columbus-blue-jackets',
  "DAL" : 'dallas-stars',
  "DET" : 'detroit-red-wings',
  "EDM" : 'edmonton-oilers',
  "FLA" : 'florida-panthers',
  "LAK" : 'los-angeles-kings',
  "MIN" : 'minnesota-wild',
  "MTL" : 'montreal-canadians',
  "NSH" : 'nashville-predators',
  "NJD" : 'new-jersey-devils',
  "NYI" : 'new-york-islanders',
  "NYR" : 'new-york-rangers',
  "OTT" : 'ottawa-senators',
  "PHI" : 'philadelphia-flyers',
  "PIT" : 'pittsburgh-penguins',
  "SJS" : 'san-jose-sharks',
  "STL" : 'st-louis-blues',
  "TBL" : 'tampa-bay-lightning',
  "TOR" : 'toronto-maple-leafs',
  "VAN" : 'vancouver-canucks',
  "VEG" : 'vegas-golden-knights',
  "WSH" : 'washington-capitals',
  "WPG" : 'winnipeg-jets'
}

#read in csv with pandas
data = pd.read_csv("nhl_statistics.csv")

# looping through the csv to save the player name and team name to a dict for later reference
for index, row in data.iterrows():
    player_name = row['Player'].lower().replace(" ", "-").strip()
    team = nhl_teams[row['Tm']]
    player_names[player_name] = team


# use player names and BS to scrape player images
for name, team in player_names.items():
  try:
    req = Request(f"https://frozenpool.dobbersports.com/players/{name}", headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req, timeout=10).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    # scrape all images tags in the webpage
    images = soup.find_all('img')
    
    #for each image url scraped from frozen tools, request and save the player image
    for item in images:
      #upload files was a key in determining which urls were the player images.
      if "uploadfiles" in item['src']:

        #using the requests library, save the images locally
        url = item['src']
        r=requests.get(url)
        with open(f'./images/{team}/{name}.jpg', 'wb') as f:
          f.write(r.content)
  #pass all errors, some players do not play anymore, retired etc.
  except:
    print("error")
    pass
