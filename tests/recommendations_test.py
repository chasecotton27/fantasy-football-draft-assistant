from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team, PlayerBoard
from backend.recommendations import Simulation

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

# --------------------------- SIMULATE THE DRAFT ----------------------------

draft_order_copy = draft_order
i = 1

for team_name in draft_order_copy:
    for team in my_teams:
        if team.team_name == team_name:
            team.draft_player(i)
            del draft_order[0]
            my_player_board = PlayerBoard(my_db_table)
            my_sim = Simulation(my_teams, my_player_board, draft_order)
            recommended_player = my_sim.recommend_player()
            picks_to_sim_next_pick = my_sim.determine_picks_to_sim(1)
            picks_to_sim_two_picks = my_sim.determine_picks_to_sim(2)
            available_players_next_pick = my_sim.predict_available_players(picks_to_sim_next_pick)
            available_players_two_picks = my_sim.predict_available_players(picks_to_sim_two_picks)
            recommended_players_next_pick = my_sim.recommend_future_players(available_players_next_pick)
            recommended_players_two_picks = my_sim.recommend_future_players(available_players_two_picks)
            print(recommended_player)
            print(recommended_players_next_pick)
            print(recommended_players_two_picks)
            i += 1
            break
