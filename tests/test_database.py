# Tests for database interactions
from backend.processing import process_csv
from backend.database import DatabaseTable

# Create database table objects for full PPR, half PPR, and standard
full_ppr_table = DatabaseTable('full_ppr')
half_ppr_table = DatabaseTable('half_ppr')
standard_table = DatabaseTable('standard')

# Process CSV data and return list of player objects for each table
players_full_ppr = process_csv('adp-data/8_11_24_ADP_Rankings_Full_PPR.csv', full_ppr_table)
players_half_ppr = process_csv('adp-data/8_11_24_ADP_Rankings_Half_PPR.csv', half_ppr_table)
players_standard = process_csv('adp-data/8_11_24_ADP_Rankings_Standard.csv', standard_table)

# Fetch all players from each database table
fetched_players_full_ppr = full_ppr_table.fetch_all_players()
fetched_players_half_ppr = half_ppr_table.fetch_all_players()
fetched_players_standard = standard_table.fetch_all_players()

# Print first 10 players from the fetched lists of players
for player in fetched_players_full_ppr[:5]:
  print(player)
for player in fetched_players_half_ppr[:5]:
  print(player)
for player in fetched_players_standard[:5]:
  print(player)

# Print last 10 players from the fetched lists of players
for player in fetched_players_full_ppr[-5:]:
  print(player)
for player in fetched_players_half_ppr[-5:]:
  print(player)
for player in fetched_players_standard[-5:]:
  print(player)

# Fetch filtered players by QB position - CURRENTLY TRYING TO CALL METHOD ON LIST OF PLAYER OBJECTS, NEED TO CALL METHOD ON PLAYERS OBJECT
filtered_qbs_full_ppr = players_full_ppr.filter_qbs(full_ppr_table)
filtered_qbs_half_ppr = players_half_ppr.filter_qbs(half_ppr_table)
filtered_qbs_standard = players_standard.filter_qbs(standard_table)

# Print filtered players by QB position
print(filtered_qbs_full_ppr)
print(filtered_qbs_half_ppr)
print(filtered_qbs_standard)

# Fetch specific player from each table
fetched_player_full_ppr = full_ppr_table.fetch_player_by_name('Josh Allen')
fetched_player_half_ppr = half_ppr_table.fetch_player_by_name('Patrick Mahomes II')
fetched_player_standard = standard_table.fetch_player_by_name('Lamar Jackson')

# Print specific fetched players
print(fetched_player_full_ppr)
print(fetched_player_half_ppr)
print(fetched_player_standard)

# Delete specific player from each table
full_ppr_table.remove_player('Josh Allen')
half_ppr_table.remove_player('Patrick Mahomes II')
standard_table.remove_player('Lamar Jackson')

# Fetch specific (deleted) player from each table
fetched_player_full_ppr = full_ppr_table.fetch_player_by_name('Josh Allen')
fetched_player_half_ppr = half_ppr_table.fetch_player_by_name('Patrick Mahomes II')
fetched_player_standard = standard_table.fetch_player_by_name('Lamar Jackson')

# Print specific fetched players
print(fetched_player_full_ppr)
print(fetched_player_half_ppr)
print(fetched_player_standard)
