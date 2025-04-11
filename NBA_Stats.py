import pandas as pd
import re
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerdashboardbygeneralsplits
from nba_api.stats.endpoints import leaguedashplayerstats

all_players = players.get_players()

def player_stats():
    answer = input("Enter the name of a player: ").strip().lower()
    if answer == "":
        print("No input provided.")
        return
   
    print("Searching for player...")
    time.sleep(2)  # Simulate a delay for the search
  
    player_id = None
    full_name = None

    for player in all_players:
        if player['full_name'].lower() == answer:
            player_id = player['id']
            full_name = player['full_name']

            break
    if player_id is None:
        print("Player not found.")
        return
    
    print("Player found: " + player['full_name'])
    career_stats = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=player_id).get_data_frames()[0]
    career_stats = career_stats[['PLAYER_NAME','GP','MIN','FG%','3P%','FT%','PTS','REB','AST','STL','BLK','TO','PLUS_MINUS']]
    career_stats = career_stats.rename(columns={'PLAYER_NAME': 'Player', 'GP': 'GP', 'MIN': 'MIN', 'FG%': 'FG%', '3P%': '3P%', 'FT%': 'FT%', 'PTS': 'PTS', 'REB': 'RPG', 'AST': 'APG', 'STL': 'SPG', 'BLK': 'BPG', 'TO': 'TO', '+/-': '+/-'})
    career_stats = career_stats[['Player', 'GP', 'MIN', 'FG%', '3P%', 'FT%', 'PTS', 'RPG', 'APG', 'SPG', 'BPG', 'TO', '+/-']] 
    career_stats = career_stats.dropna()
    print(career_stats.head())
    print("Career stats retrieved.")
    print("Available columns:")
print(career_stats.columns.tolist())



if __name__ == "__main__":
    player_stats()







       
        