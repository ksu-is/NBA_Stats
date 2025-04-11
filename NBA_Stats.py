from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguedashplayerstats
import pandas as pd
import re

all_players = players._get_players()

def player_stats(answer):
    stats = pd.DataFrame()
    player_id = None
    # Check if the input is a player name or a season
    if re.match(r'^[a-zA-Z\s]+$', answer):
        # Search for the player by name
        player = next((player for player in all_players if player['full_name'].lower() == answer), None)
        if player:
            player_id = player['id']
            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()[0]
            stats = career_stats[['SEASON_ID', 'TEAM_ID', 'PTS', 'REB', 'AST']]
            stats.columns = ['Season', 'Team ID', 'Points', 'Rebounds', 'Assists']
        else:
            print("Player not found.")
    else:
        # Assume the input is a season
        season_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=answer).get_data_frames()[0]
        stats = season_stats[['PLAYER_ID', 'PLAYER_NAME', 'PTS', 'REB', 'AST']]
        stats.columns = ['Player ID', 'Player Name', 'Points', 'Rebounds', 'Assists']





if __name__ == "__main__":
    answer = input('Enter the name of an NBA Player or a season(e.g."2022-23")').strip().lower()