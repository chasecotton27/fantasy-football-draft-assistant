# Tests for database interactions
from backend.adp_processor import Player, process_csv, store_players_in_db
from backend.database import DatabaseTable

# Create database table object
full_ppr_table = DatabaseTable('full_ppr')

# Process CSV data and return list of player objects
players = process_csv('adp-data/8_11_24_ADP_Rankings_Full_PPR.csv')

# Store data from player objects into database table
store_players_in_db(players, full_ppr_table)

# Fetch all players from database table
fetched_players = full_ppr_table.fetch_all_players()

# Print first 10 players from the fetched list of players
for player in fetched_players[:5]:
  print(player)

# Print last 10 players from the fetched list of players
for player in fetched_players[-5:]:
  print(player)