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
    
    print("Player found!")
    career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_df = career_stats.get_data_frames()[0]
    season_stats = (career_df[['SEASON_ID','TEAM_ABBREVIATION','GP','MIN','PTS','AST','REB','STL','BLK','TOV','FG_PCT','FT_PCT','FG3_PCT']])
    season_stats = season_stats.rename(columns={'SEASON_ID': 'Season', 'TEAM_ABBREVIATION': 'Team', 'GP': 'GP', 'MIN': 'MIN', 'PTS': 'PTS', 'AST': 'AST', 'REB': 'REB', 'STL': 'STL', 'BLK': 'BLK', 'TOV': 'TO', 'FG_PCT': 'FG%', 'FT_PCT': 'FT%', 'FG3_PCT': '3P%'})   
    print("Career Stats for", full_name)
    print("-----------------------------------------------------")
    print(season_stats.to_string(index=False))
    
    print("Legend: GP = Games Played, MIN = Minutes, PTS = Points, AST = Assists, REB = Rebounds, STL = Steals, BLK = Blocks, TO = Turnovers, FG% = Field Goal Percentage, FT% = Free Throw Percentage, 3P% = Three Point Percentage")



if __name__ == "__main__":
    player_stats()







       
        