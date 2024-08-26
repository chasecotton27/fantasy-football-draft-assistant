from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team, PlayerBoard

# --------------------- SETUP OF ACTUAL STARTING STATE ----------------------

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

# -------------------- SETUP OF SIMULATED STARTING STATE --------------------

# Setup from draft_setup_frame
sim_scoring_format = 'Full PPR'
sim_position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 7}
sim_drafting_style = 'Snake'
sim_num_teams = 12
sim_my_draft = Draft(sim_scoring_format, sim_position_count, sim_drafting_style, sim_num_teams)
sim_db_table_name = 'sim_full_ppr_table'
sim_csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Full_PPR.csv'
sim_my_db_table = DatabaseTable(sim_db_table_name, 'sim_players.db')
sim_my_csv_file = CSVFile(sim_csv_file_path, sim_my_db_table)

# Setup from team_setup_frame
sim_my_teams = []
for i in range(1, sim_my_draft.num_teams + 1):
    sim_team_name = f'Team_{str(i)}'
    sim_team = Team(sim_team_name, i, sim_my_db_table, sim_my_draft)
    sim_my_teams.append(sim_team)

# Abstracted setup from draft_board_frame
sim_my_player_board = PlayerBoard(sim_my_db_table)
sim_draft_order = []
reverse = False
for _ in range(16):
    if not reverse:
        for sim_team in sim_my_teams:
            sim_draft_order.append(sim_team.team_name)
        reverse = True
    elif reverse:
        for sim_team in sim_my_teams[::-1]:
            sim_draft_order.append(sim_team.team_name)
        reverse = False
sim_draft_selections = []

# --------------------------- SIMULATE THE DRAFT ----------------------------

# Initialize flag to determine when to stop simulation
starting_lineup_full = False

# Simulate and print draft picks
for sim_draft_turn in sim_draft_order:
    for sim_team in sim_my_teams:
        if sim_team.team_name == sim_draft_turn:
            print()
            print(f'Before pick: {sim_team.filled_roster_positions}')
            target_player = sim_team.simulate_draft_pick()
            if target_player == None:
                starting_lineup_full = True
                break
            print(target_player)
            sim_team.draft_player(target_player[0])
            print(f'After pick: {sim_team.filled_roster_positions}')
            sim_draft_selections.append([sim_team.team_name, target_player[2]])
            sim_my_player_board = PlayerBoard(sim_my_db_table)
            print()
            break
    # Check if starting lineup is full to determine whether to continue
    if starting_lineup_full:
        break

# I NOW HAVE TEAM.FILLED_ROSTER_POSITIONS AND TEAM.REQUIRED_ROSTER_POSITIONS TO WORK WITH
# I ALSO HAVE SIMULATE_DRAFT_PICK(), WHICH RETURNS THE TARGET PLAYER FOR THE DRAFTING TEAM
# I AM NOW ABLE TO SIMULATE THE ENTIRE DRAFT
# NOW NEED TO FIGURE OUT HOW TO USE THE SIMULATION DATA TO PREDICT FUTURE STATE OF PLAYERBOARD AND PROVIDE RECOMMENDATIONS
