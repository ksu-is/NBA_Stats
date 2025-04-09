from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from nba_api.stats.endpoints import playerdashboardbyyearoveryear
import pandas as pd
career = playercareerstats.PlayerCareerStats(player_id='203999')

career_df = career.get_data_frames()[0]
career_df = career_df[['SEASON_ID', 'TEAM_ABBREVIATION', 'GP', 'W', 'L', 'W_PCT', 'MIN', 'PTS', 'FG_PCT', 'FT_PCT']]

career.get_json()
career.get_dict()

print(career)