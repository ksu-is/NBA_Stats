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
    career_df['Avg_MIN'] = career_df['MIN'] / career_df['GP']
    career_df['Avg_PTS'] = career_df['PTS'] / career_df['GP']
    career_df['Avg_AST'] = career_df['AST'] / career_df['GP']
    career_df['Avg_REB'] = career_df['REB'] / career_df['GP']
    career_df['Avg_STL'] = career_df['STL'] / career_df['GP']
    career_df['Avg_BLK'] = career_df['BLK'] / career_df['GP']
    career_df['Avg_TOV'] = career_df['TOV'] / career_df['GP']
    plus_minus_df = playerdashboardbygeneralsplits.PlayerDashboardByGeneralSplits(player_id=player_id).get_data_frames()[0]
    career_plus_minus = plus_minus_df[plus_minus_df['GROUP_VALUE'] == 'Overall']['PLUS_MINUS'].values[0]
    career_df[['Avg_MIN','Avg_PTS', 'Avg_AST', 'Avg_REB', 'Avg_STL', 'Avg_BLK', 'Avg_TOV','FG_PCT','FT_PCT','FG3_PCT']] = career_df[['Avg_MIN','Avg_PTS', 'Avg_AST', 'Avg_REB', 'Avg_STL', 'Avg_BLK', 'Avg_TOV','FG_PCT','FT_PCT','FG3_PCT']].round(2)
    season_stats = (career_df[['SEASON_ID','TEAM_ABBREVIATION','GP','MIN','Avg_PTS','Avg_AST','Avg_REB','Avg_STL','Avg_BLK','Avg_TOV','FG_PCT','FT_PCT','FG3_PCT', 'PLUS_MINUS']].copy())
    season_stats['Plus-Minus'] = career_plus_minus
    season_stats = season_stats.rename(columns={'SEASON_ID': 'Season', 'TEAM_ABBREVIATION': 'Team', 'GP': 'GP', 'MIN': 'MIN', 'Avg_PTS': 'PPG', 'Avg_AST': 'APG', 'Avg_REB': 'RPG', 'Avg_STL': 'SPG', 'Avg_BLK': 'BPG', 'Avg_TOV': 'TOV', 'FG_PCT': 'FG%', 'FT_PCT': 'FT%', 'FG3_PCT': '3P%', 'PLUS_MINUS': '+/-'})   
    
    
    print("Career Stats for", full_name)
    print("-----------------------------------------------------")
    print(season_stats.to_string(index=False))
    
    print("Legend:\nPPG = Points Per Game \nAPG = Assists Per Game \nRPG = Rebounds Per Game \nSPG = Steals Per Game \nBPG = Blocks Per Game \nTOV = Turnovers \nFG% = Field Goal Percentage \nFT% = Free Throw Percentage \n3P% = Three Point Percentage")


if __name__ == "__main__":
    player_stats()







       
        