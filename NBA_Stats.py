import pandas as pd
import re
import time
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguedashplayerstats
print(players.get_players()[:1])

all_players = players._get_players()

def player_stats(answer):
    print("Searching for player...")
    time.sleep(2)  # Simulate a delay for the search
    stats = pd.DataFrame()
    
    # Check if the input is a player name or a season
    if re.match(r'^[a-zA-Z\s]+$', answer):
        # Search for the player by name
        player = next((player for player in all_players if player['full_name'].lower() == answer), None)
        
        if player:
            print("Player found:", player['full_name'])
            player_id = player['id']

            career_stats = playercareerstats.PlayerCareerStats(player_id=player_id).get_data_frames()
            career_df = career_stats[0]

            if career_df.empty:
                print("No stats found for,", answer)
            else:
                print("Career stats for", answer)
                print(career_df)


if __name__ == "__main__":
    while True:
        answer = input("Enter player name (or 'exit' to quit): ").strip()
        if answer.lower() == 'exit':
            break
        player_stats(answer)
       
        