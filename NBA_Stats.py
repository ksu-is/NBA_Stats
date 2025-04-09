from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import re

all_players = players._get_players()

def get_stats():
    print("Welcome to the NBA Stats Presenter!")

    while True:
        get_name = input("Enter the name of a player to see their stats (or type 'exit' to quit): ").strip()
        if get_name.lower() == 'exit':
            print("Thank you for using the NBA Stats Presenter!")
            break
        if not get_name:
            print("Please enter a valid name.")
            continue
        player_id = None
        player_name = None
        for player in all_players:
            if re.search(get_name, player['full_name'], re.IGNORECASE):
                player_id = player['id']
                player_name = player['full_name']
                break
        if player_id is None:
            print("Player not found. Please try again.")
            continue
        else:
            print(f"Player found: {player_name}")
            print("Fetching stats...")
            try:
                career_stats = commonplayerinfo.CommonPlayerInfo(player_id=player_id).get_data_frames()[0]
                print(f"An error occurred while fetching stats: {e}")
                continue
            print(career_stats)

get_stats()