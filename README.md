# NBA Statistics Presenter

 This program is designed to gather and present up-to-date statistics from the NBA. The casual fans, down to the most diehard NBA fans, can use this program to learn more about basketball or their favorite players. Users can enter the name of a player or a season and be presented with the associated statistics. Beyond the typical stats of points, rebounds, and assists, users will be able to observe advanced stats such as box plus-minus and win shares, and true shooting percentage. 

# How to use
1. Step 1: Use your terminal to install the NBA API  
    pip install nba_api
2. Step 2: Import the following libraries
    import pandas as pd  
    import re  
    import time  
    from nba_api.stats.static import players  
    from nba_api.stats.endpoints import playercareerstats  
    from nba_api.stats.static import teams  
    from tabulate import tabulate   
