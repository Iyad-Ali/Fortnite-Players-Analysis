import pandas as pd
import requests
import json
from bs4 import BeautifulSoup


# Scraping player names from TRN fortnite tracker

# function to get the name from the html tag
def get_names(html_names):
    names = []
    for name in html_names:
        names.append(name.getText())
    return names

# list to contain all players tags
all_players = []

for page in range(1, 16):
    res = requests.get(f"https://fortnitetracker.com/leaderboards/kbm/Score?mode=all&page={page}")
    soup = BeautifulSoup(res.text, 'html.parser')
    html_names = soup.select(".trn-lb-entry__name")

    players = get_names(html_names)
    all_players.extend(players)
    print(f'scraped page: {page}')

# Dataframe of our data
Fortnite_players_stats =  pd.DataFrame(
columns=['Player', 'Solo score', 'Solo top1', 'Solo top3', 'Solo kd', 'Solo winRatio', 'Solo matches', 'Solo kills',
             'Solo minutesPlayed', 'Duos score', 'Duos top1', 'Duos top3', 'Duos kd', 'Duos winRatio', 'Duos matches', 'Duos kills',
             'Duos minutesPlayed', 'Trios score', 'Trios top1', 'Trios top3', 'Trios kd', 'Trios winRatio', 'Trios matches', 'Trios kills',
             'Trios minutesPlayed', 'Squads score', 'Squads top1', 'Squads top3', 'Squads kd', 'Squads winRatio', 'Squads matches',
             'Squads kills', 'Squads minutesPlayed', 'LTM score', 'LTM top1', 'LTM top3', 'LTM kd', 'LTM winRatio', 'LTM matches',
             'LTM kills', 'LTM minutesPlayed'])

# list for player stats 
stats = ['score', 'top1', 'top3', 'kd', 'winRatio',
         'matches', 'kills', 'minutesPlayed']

# list of each game mode
game_modes = ['p2', 'p9', 'trios', 'p10', 'ltm']

# dictionary for each game mode and its known name
modes_dict = {'p2': "Solo",  'p9': "Duos",
              'trios': "Trios", 'p10': "Squads", 'ltm': "LTM"}

# Extracting the data from TRN fortnite tracker API

TOKEN = "26fc6abc-883a-4c30-824d-c18c72c0c3d8" # API token
headers = {"TRN-Api-Key": TOKEN}

for i in range(len(all_players)):
    url = f'https://api.fortnitetracker.com/v1/profile/pc/{all_players[i]}'
    r = requests.get(url, headers=headers)
    data = r.json()
    
    # check if player doesn't exist or account is private
    if len(data)<2:
        print(data)
   
    else:
        
        # features dict containing player tag
        features_dict = {"Player": data["epicUserHandle"]}

        # filling features dict with player stats
        for mode in game_modes:
            for stat in stats:

                try:
                    features_dict[f"{modes_dict[mode]} {stat}"] = data["stats"][mode][stat]["value"]
                except:
                    print(f"{mode} data not found")


        # dataframe of single player
        player_df = pd.DataFrame(features_dict,
                                 columns=['Player', 'Solo score', 'Solo top1', 'Solo top3', 'Solo kd', 'Solo winRatio', 'Solo matches', 'Solo kills',
                                          'Solo minutesPlayed', 'Duos score', 'Duos top1', 'Duos top3', 'Duos kd', 'Duos winRatio', 'Duos matches', 'Duos kills',
                                          'Duos minutesPlayed', 'Trios score', 'Trios top1', 'Trios top3', 'Trios kd', 'Trios winRatio', 'Trios matches', 'Trios kills',
                                          'Trios minutesPlayed', 'Squads score', 'Squads top1', 'Squads top3', 'Squads kd', 'Squads winRatio', 'Squads matches',
                                          'Squads kills', 'Squads minutesPlayed', 'LTM score', 'LTM top1', 'LTM top3', 'LTM kd', 'LTM winRatio', 'LTM matches',
                                          'LTM kills', 'LTM minutesPlayed'], index=[0])
        
        # add player row to main dataframe
        Fortnite_players_stats = pd.concat(
            [Fortnite_players_stats, player_df], ignore_index=True)

        print(f"got {all_players[i]} data, remaining {len(all_players)-i-1}")
    

Fortnite_players_stats.to_csv("Fortnite_players_stats.csv", index = False) # save to csv file
