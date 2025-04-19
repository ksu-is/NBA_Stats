import pandas as pd
import re
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from tabulate import tabulate


# Initialize the statistic finder function
def player_stats():
    while True:
        print("Welcome to the NBA Player Stats Program!")
        print("This program allows you to search for NBA player stats.")

        # Receive user input for player name
        search = input("Enter the name of a player or 'q' to exit: ").strip().lower()
        if search == "q":
            print("Thank you, exiting the program.")
            return
        elif search == "":
            print("No input provided.")
            continue
        
        print("Searching for player...")
        time.sleep(2)  

        # Use regex to find players with similar names
        matches = players.find_players_by_full_name(search)
        if not matches:
            print("No players found with that name.")
            continue
        elif len(matches) > 1:
            print("Multiple players found with that name. Please be more specific.")
            for i, match in enumerate(matches):
                print("{}: {}".format(i + 1, match['full_name']))
            try:
                choice = int(input("Select a player by number: ")) - 1
                if choice < 0 or choice >= len(matches):
                    print("Invalid choice.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
        else:
            choice = 0

        selected_player = matches[choice]
        player_id = selected_player['id']
        full_name = selected_player['full_name']

        print("Player found: {}".format(full_name))

        # Get player stats
        print("Fetching player stats...")
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_df = career_stats.get_data_frames()[0]

        if career_df.empty:
            print("No career stats available for this player.")
            continue
        
        # Get team names
        nba_teams = teams.get_teams()
        team_name = {team['abbreviation']: team['full_name'] for team in nba_teams}

        # Add historical team names
        team_name.update({
            'NJN': 'New Jersey Nets',
            'PHW': 'Philadelphia Warriors',
            'SFW': 'San Francisco Warriors',
            'SEA': 'Seattle SuperSonics',
            'NOH': 'New Orleans Hornets',
            'CHA': 'Charlotte Bobcats',
            'VAN': 'Vancouver Grizzlies',
            'NOK': 'New Orleans/Oklahoma City Hornets',
            'WSB': 'Washington Bullets',  
            'SDC': 'San Diego Clippers',
            'KCO': 'Kansas City-Omaha Kings',
            'BUF': 'Buffalo Braves',
            'CHH': 'Charlotte Hornets (original)',
            'NYN': 'New York Nets',
            'INA': 'Indianapolis Olympians'
        })
        # Calculations for averages and percentages
        career_df['MPG'] = career_df['MIN'] / career_df['GP']
        career_df['PPG'] = career_df['PTS'] / career_df['GP']
        career_df['APG'] = career_df['AST'] / career_df['GP']
        career_df['RPG'] = career_df['REB'] / career_df['GP']
        career_df['SPG'] = career_df['STL'] / career_df['GP']
        career_df['BPG'] = career_df['BLK'] / career_df['GP']
        career_df['TOV'] = career_df['TOV'] / career_df['GP']
        career_df['FG%'] = (career_df['FG_PCT']*100).round(1)
        career_df['FT%'] = (career_df['FT_PCT']*100).round(1) 
        career_df['3P%'] = (career_df['FG3_PCT']*100).round(1) 
        career_df['Team'] = career_df['TEAM_ABBREVIATION'].map(team_name)
        career_df[['MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%']] = career_df[['MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%']].round(1)
        season_stats = career_df[['SEASON_ID','Team' ,'GP','MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%']].copy()
        

        print("Career Stats for", full_name)
        print(tabulate(season_stats, headers="keys", tablefmt="pipe", showindex=False))
        print("Legend:\nGP - Games Played \nMPG - Minutes Per Game \nPPG - Points Per Game \nAPG - Assists Per Game \nRPG - Rebounds Per Game \nSPG - Steals Per Game \nBPG - Blocks Per Game \nTOV - Turnovers \nFG% - Field Goal Percentage \nFT% - Free Throw Percentage \n3P% - Three Point Percentage")
        
        
if __name__ == "__main__":
    player_stats()







       
        