import pandas as pd
import re
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguedashplayerstats
from nba_api.stats.static import teams
from tabulate import tabulate


print("Welcome to the NBA Statistics Presenter! \nThis program allows you to search for NBA player stats.")


# Initialize the statistic finder function
def player_stats():
    while True:
        # Receive user input for player name
        search = input("Enter the name of a player or 'q' to exit: ").strip().lower()
        if search == "q":
            print("Thank you, exiting the program.")
            return
        elif search == "":
            print("No input provided.")
            continue
       
        print("Searching for player...")
        time.sleep(1.5)  # Simulate a delay for the search


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
       
        # Get the selected player
        selected_player = matches[choice]
        player_id = selected_player['id']
        full_name = selected_player['full_name']


        print("Player found: {}".format(full_name))


        # Get player stats
        career_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_df = career_stats.get_data_frames()[0]


        if career_df.empty:
            print("No career stats available for this player.")
            continue
       
        # Get team names
        nba_teams = teams.get_teams()
        team_name = {team['abbreviation']: team['full_name'] for team in nba_teams}


        # Add historical team names(API only returns current teams)
        team_name.update({
             'BUF': 'Buffalo Braves',
            'CHA': 'Charlotte Bobcats',
            'CHH': 'Charlotte Hornets (original)',
            'CIN': 'Cincinnati Royals',
            'INA': 'Indianapolis Olympians',
            'KCO': 'Kansas City-Omaha Kings',
            'MIH': 'Milwaukee Hawks',
            'MPL': 'Minneapoils Lakers',
            'NJN': 'New Jersey Nets',
            'NOH': 'New Orleans Hornets',
            'NOK': 'New Orleans/Oklahoma City Hornets',
            'NYN': 'New York Nets',
            'PHW': 'Philadelphia Warriors',
            'ROC': 'Rochester Royals',
            'SDC': 'San Diego Clippers',
            'SEA': 'Seattle SuperSonics',
            'SFW': 'San Francisco Warriors',
            'STL': 'St.Louis Hawks',
            'SYR': 'Syracuse Nationals',
            'VAN': 'Vancouver Grizzlies',
            'WSB': 'Washington Bullets'
        })


        # Calculations for averages and percentages
        career_df['MPG'] = career_df['MIN'] / career_df['GP']
        career_df['PPG'] = career_df['PTS'] / career_df['GP']
        career_df['APG'] = career_df['AST'] / career_df['GP']
        career_df['RPG'] = career_df['REB'] / career_df['GP']
        career_df['SPG'] = career_df['STL'] / career_df['GP']
        career_df['BPG'] = career_df['BLK'] / career_df['GP']
        career_df['TOV'] = career_df['TOV'] / career_df['GP']
        career_df['FG%'] = (career_df['FG_PCT']*100)
        career_df['FT%'] = (career_df['FT_PCT']*100)
        career_df['3P%'] = (career_df['FG3_PCT']*100)
       
        # Get True Shooting Percentage (TS%)
        career_df['TS%'] = career_df['PTS'] / (2 * (career_df['FGA'] + 0.44 * career_df['FTA']))
        career_df['TS%'] = (career_df['TS%'] * 100)
       
        # Round the stats to one decimal place
        career_df[['MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%','TS%']] = career_df[['MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%','TS%']].round(1)

        # Map team abbreviations to full names
        career_df['Team'] = career_df['TEAM_ABBREVIATION']

        # Filter the DataFrame to include only the relevant columns
        season_stats = career_df[['SEASON_ID','Team' ,'GP','MPG','PPG', 'APG', 'RPG', 'SPG', 'BPG', 'TOV','FG%','FT%','3P%','TS%']].copy()
       
        # Rename SEASON_ID column for clarity
        season_stats.rename(columns={'SEASON_ID': 'Season'}, inplace=True)


        # Format the season column to be more readable
        print("Career Stats for", full_name)
        print(tabulate(season_stats, headers="keys", tablefmt="pipe", showindex=False))
       
        # Add a legend for the stats
        print("Legend:\nGP - Games Played \nMPG - Minutes Per Game \nPPG - Points Per Game \nAPG - Assists Per Game \nRPG - Rebounds Per Game \nSPG - Steals Per Game \nBPG - Blocks Per Game \nTOV - Turnovers \nFG% - Field Goal Percentage \nFT% - Free Throw Percentage \n3P% - Three Point Percentage \nTS% - True Shooting Percentage")
       
# Run the program        
if __name__ == "__main__":
    player_stats() 














       
       



