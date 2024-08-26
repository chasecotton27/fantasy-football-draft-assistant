from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team, PlayerBoard

# I NOW HAVE TEAM.FILLED_ROSTER_POSITIONS AND TEAM.REQUIRED_ROSTER_POSITIONS TO WORK WITH
# I ALSO HAVE SIMULATE_DRAFT_PICK(), WHICH RETURNS THE TARGET PLAYER FOR THE DRAFTING TEAM
# I AM NOW ABLE TO SIMULATE THE ENTIRE DRAFT
# NOW NEED TO FIGURE OUT HOW TO USE THE SIMULATION DATA TO PREDICT FUTURE STATE OF PLAYERBOARD AND PROVIDE RECOMMENDATIONS

class SimulatedDraft:
    def __init__(self, my_db_table, my_csv_file, my_draft, my_teams, draft_order):
        self.my_db_table = my_db_table
        self.my_csv_file = my_csv_file
        self.my_draft = my_draft
        self.my_teams = my_teams
        self.draft_order = draft_order
        self.create_sim_objects()

    def create_sim_objects(self):
        self.sim_my_draft = Draft(self.my_draft.scoring_format, self.my_draft.position_count, self.my_draft.drafting_style, self.my_draft.num_teams)
        sim_db_table_name = f'sim_{self.my_db_table.table_name}'
        sim_db_name = f'sim_{self.my_db_table.db_name}'
        sim_csv_file_path = self.my_csv_file.csv_file_path
        self.sim_my_db_table = DatabaseTable(sim_db_table_name, sim_db_name)
        self.sim_my_csv_file = CSVFile(sim_csv_file_path, self.sim_my_db_table)

        # Abstracted setup from team_setup_frame
        self.sim_my_teams = []
        for team in self.my_teams:
            sim_team_name = f'sim_{team.team_name}'
            sim_team = Team(sim_team_name, team.draft_position, self.sim_my_db_table, self.sim_my_draft)
            self.sim_my_teams.append(sim_team)

        # Abstracted setup from draft_board_frame
        self.sim_my_player_board = PlayerBoard(self.sim_my_db_table)
        self.sim_draft_order = self.draft_order

    def predict_future_availability(self, rounds_to_sim):
        # Determine how many picks to sim in a standard draft
        if self.sim_my_draft.drafting_style == 'Standard':
            picks_to_sim = rounds_to_sim * len(self.sim_my_teams)
        # Determine how many picks to sim in a snake draft
        elif self.sim_my_draft.drafting_style == 'Snake':
            drafting_team = self.sim_draft_order[0]
            occurence_count = 0
            for i, team in enumerate(self.sim_draft_order):
                if team == drafting_team:
                    occurence_count += 1
                    if occurence_count == rounds_to_sim + 1:
                        picks_to_sim = i
                        break

        # Simulate draft picks to predict future state of player board
        for sim_team_name in self.sim_draft_order[0:picks_to_sim]:
            for sim_team in self.sim_my_teams:
                if sim_team.team_name == sim_team_name:
                    target_player = sim_team.simulate_draft_pick()
                    sim_team.draft_player(target_player[0])
                    self.sim_my_player_board = PlayerBoard(self.sim_my_db_table)
                    break

        return self.sim_my_player_board

    def recommend_picks(self):
        pass

        # USE PREDICTED PLAYER BOARD TO FIND FUTURE AVAILABLE PLAYERS WITH VALUABLE ADP FOR THAT ROUND
        # THEN, USE THOSE FUTURE PLAYERS TO DETERMINE WHAT POSITION TO TARGET THIS ROUND
