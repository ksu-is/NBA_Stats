from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import re

all_players = players._get_players()

def get_stats():
    print("Welcome to the NBA Stats Presenter!")
    player_or_season = input("Enter the name of a player or a season (e.g.,'2022-23'): ").strip().lower()
    if player_or_season == 'exit':
        print("Exiting the program. Goodbye!")
        return






