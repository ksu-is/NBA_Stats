import pandas as pd
import re
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import playerdashboardbygeneralsplits
from nba_api.stats.endpoints import leaguedashplayerstats


# Initialize the statistic finder function
def player_stats():
    while True:
        print("Welcome to the NBA Player Stats Program!")
        print("This program allows you to search for NBA player stats.")

        # Receive user input for player name
        search = input("Enter the name of a player or 'q' to exit: ").strip().lower()
        if search == "q":
            print("Exiting the program.")
            break
        elif search == "":
            print("No input provided.")
            continue
        
         
        print("Searching for player...")
        time.sleep(2)  

        # Use regex to find players with similar names
        matches = players.find_players_by_full_name(search)

        if not matches:
            print("Player not found. Try again.")
            continue

        elif len(matches) > 1:
            print("Multiple players found:")
            for index, player in enumerate(matches):
                print(f"{index + 1}. {player['full_name']} (Active: {player['is_active']})")
            choice = input("Select the player by number (or 'q' to quit): ")
            
            if choice.lower() == 'q':
                break
            try:
                selected = matches[int(choice) - 1]
            except (IndexError, ValueError):
                print("Invalid selection.")
                continue
        else:
            selected = matches[0]
    
        # Display player information
        player_id = selected['id']
        full_name = selected['full_name']
        print("Player found!")

        # Get player stats
        print("Fetching player stats...")
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_df = career_stats.get_data_frames()[0]
        career_df['Avg_MIN'] = career_df['MIN'] / career_df['GP']
        career_df['Avg_PTS'] = career_df['PTS'] / career_df['GP']
        career_df['Avg_AST'] = career_df['AST'] / career_df['GP']
        career_df['Avg_REB'] = career_df['REB'] / career_df['GP']
        career_df['Avg_STL'] = career_df['STL'] / career_df['GP']
        career_df['Avg_BLK'] = career_df['BLK'] / career_df['GP']
        career_df['Avg_TOV'] = career_df['TOV'] / career_df['GP']
        career_df[['Avg_MIN','Avg_PTS', 'Avg_AST', 'Avg_REB', 'Avg_STL', 'Avg_BLK', 'Avg_TOV','FG_PCT','FT_PCT','FG3_PCT']] = career_df[['Avg_MIN','Avg_PTS', 'Avg_AST', 'Avg_REB', 'Avg_STL', 'Avg_BLK', 'Avg_TOV','FG_PCT','FT_PCT','FG3_PCT']].round(2)
        season_stats = (career_df[['SEASON_ID','TEAM_ABBREVIATION','GP','MIN','Avg_PTS','Avg_AST','Avg_REB','Avg_STL','Avg_BLK','Avg_TOV','FG_PCT','FT_PCT','FG3_PCT']].copy())
        season_stats = season_stats.rename(columns={'SEASON_ID': 'Season', 'TEAM_ABBREVIATION': 'Team', 'GP': 'GP', 'MIN': 'MIN', 'Avg_PTS': 'PPG', 'Avg_AST': 'APG', 'Avg_REB': 'RPG', 'Avg_STL': 'SPG', 'Avg_BLK': 'BPG', 'Avg_TOV': 'TOV', 'FG_PCT': 'FG%', 'FT_PCT': 'FT%', 'FG3_PCT': '3P%'})   
    
    print("Career Stats for", full_name)
    print("-----------------------------------------------------")
    print(season_stats.to_string(index=False))
    
    print("Legend:\nPPG = Points Per Game \nAPG = Assists Per Game \nRPG = Rebounds Per Game \nSPG = Steals Per Game \nBPG = Blocks Per Game \nTOV = Turnovers \nFG% = Field Goal Percentage \nFT% = Free Throw Percentage \n3P% = Three Point Percentage")


if __name__ == "__main__":
    player_stats()







       
        