from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team, PlayerBoard

# -------------------- SIMULATES HEADLESS STARTING STATE OF DRAFT BOARD FRAME --------------------

# Setup from draft_setup_frame
scoring_format = 'Full PPR'
position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 7}
drafting_style = 'Snake'
num_teams = 12
my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)
db_table_name = 'full_ppr_table'
csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Full_PPR.csv'
my_db_table = DatabaseTable(db_table_name)
my_csv_file = CSVFile(csv_file_path, my_db_table)

# Setup from team_setup_frame
my_teams = []
for i in range(1, my_draft.num_teams + 1):
    team_name = f'Team_{str(i)}'
    team = Team(team_name, i, my_db_table, my_draft)
    my_teams.append(team)

# Abstracted setup from draft_board_frame
my_player_board = PlayerBoard(my_db_table)
draft_order = []
reverse = False
for _ in range(16):
    if not reverse:
        for team in my_teams:
            draft_order.append(team.team_name)
        reverse = True
    elif reverse:
        for team in my_teams[::-1]:
            draft_order.append(team.team_name)
        reverse = False
draft_selections = []

# -------------------- SIMULATES HEADLESS STARTING STATE OF DRAFT BOARD FRAME --------------------

'''projected_picks_v1 = []
projected_picks_v2 = []
projected_picks_v3 = []

simulated_roster_team_1 = []
simulated_roster_team_2 = []
simulated_roster_team_3 = []
simulated_roster_team_4 = []
simulated_roster_team_5 = []
simulated_roster_team_6 = []
simulated_roster_team_7 = []
simulated_roster_team_8 = []
simulated_roster_team_9 = []
simulated_roster_team_10 = []
simulated_roster_team_11 = []
simulated_roster_team_12 = []'''

player_id = 1
for team in my_teams:
    print()
    player = my_db_table.fetch_player(player_id)
    print(f'Before pick: {team.filled_roster_positions}')
    team.simulate_draft_pick()
    team.draft_player(player_id)
    print(f'After pick: {team.filled_roster_positions}')
    draft_selections.append([team.team_name, player[2]])
    del draft_order[0]
    my_player_board = PlayerBoard(my_db_table)
    player_id += 1
    print()
for team in my_teams[::-1]:
    print()
    player = my_db_table.fetch_player(player_id)
    print(f'Before pick: {team.filled_roster_positions}')
    team.simulate_draft_pick()
    team.draft_player(player_id)
    print(f'After pick: {team.filled_roster_positions}')
    draft_selections.append([team.team_name, player[2]])
    del draft_order[0]
    my_player_board = PlayerBoard(my_db_table)
    player_id += 1
    print()
for team in my_teams:
    print()
    player = my_db_table.fetch_player(player_id)
    print(f'Before pick: {team.filled_roster_positions}')
    team.simulate_draft_pick()
    team.draft_player(player_id)
    print(f'After pick: {team.filled_roster_positions}')
    draft_selections.append([team.team_name, player[2]])
    del draft_order[0]
    my_player_board = PlayerBoard(my_db_table)
    player_id += 1
    print()
for team in my_teams[::-1]:
    print()
    player = my_db_table.fetch_player(player_id)
    print(f'Before pick: {team.filled_roster_positions}')
    team.simulate_draft_pick()
    team.draft_player(player_id)
    print(f'After pick: {team.filled_roster_positions}')
    draft_selections.append([team.team_name, player[2]])
    del draft_order[0]
    my_player_board = PlayerBoard(my_db_table)
    player_id += 1
    print()

# I NOW HAVE TEAM.FILLED_ROSTER_POSITIONS AND TEAM.REQUIRED_ROSTER_POSITIONS TO WORK WITH
# I ALSO HAVE SIMULATE_DRAFT_PICK(), WHICH AS OF NOW PRINTS THE TARGET PLAYER POSITIONS FOR THE DRAFTING TEAM
