from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team, PlayerBoard

# Instantiate Draft object to query user for scoring format, position count, and drafting style
my_draft = Draft()

# Tests
print(my_draft.scoring_format)
print(my_draft.position_count)
print(my_draft.drafting_style)

# Conditional logic for user input regarding scoring format, position count, and drafting style
if my_draft.scoring_format == 'Standard':
  db_table_name = 'standard_table'
  csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Standard.csv'
elif my_draft.scoring_format == 'Half PPR':
  db_table_name = 'half_ppr_table'
  csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Half_PPR.csv'
elif my_draft.scoring_format == 'Full PPR':
  db_table_name = 'full_ppr_table'
  csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Full_PPR.csv'

# Tests
print(db_table_name)
print(csv_file_path)

# Instantiate DatabaseTable object to create a database table and a reference object
my_db_table = DatabaseTable(db_table_name)

# Tests
print(my_db_table)

# Instantiate CSVFile object to process CSV data and populate the database table with players
my_csv_file = CSVFile(csv_file_path, my_db_table)

# Tests
print(my_csv_file)

# Instantiate PlayerBoard object to create an empty list of players
my_player_board = PlayerBoard(my_db_table)

# Tests
print(my_player_board)

# Set the player board to the entire database of players and count the number of players
all_players = my_player_board.filter_all_players()
player_count = my_player_board.player_count

# Tests
for player in all_players[:5]:
  print(player)
print(player_count)

# Apply different filters to the player board to retrieve different subsets of players from the database
player = my_player_board.filter_player(100)
qbs = my_player_board.filter_qbs()
rbs = my_player_board.filter_rbs()
wrs = my_player_board.filter_wrs()
tes = my_player_board.filter_tes()
ks = my_player_board.filter_ks()
dsts = my_player_board.filter_dsts()
players_from_team = my_player_board.filter_players_from_team('NE')
players_with_bye = my_player_board.filter_players_with_bye(10)

# Tests
filtered_player_boards = [all_players, player, qbs, rbs, wrs, tes, ks, dsts, players_from_team, players_with_bye]
for player_board in filtered_player_boards:
  i = 1
  for player in player_board:
    if i > 5:
      break
    else:
      print(player)
      i += 1

# Instantiate Team object to create a team without players
my_team = Team('My Team', my_db_table)

# Tests
print(my_team)

# Draft players and add them to the team's roster while removing them from the database
my_team.draft_player(2)
my_team.draft_player(4)
my_team.draft_player(6)
my_team.draft_player(8)

# Tests
for player in my_team.roster:
  print(player)

# Reset the player board to the entire database of players to confirm the drafted players are removed
all_players = my_player_board.filter_all_players()
for player in all_players[:5]:
  print(player)
