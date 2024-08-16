import tkinter as tk
from backend.processing import Team
from ui.draft_board_frame import DraftBoardFrame

class TeamSetupFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table

        # Title label
        self.title_label = tk.Label(self, text = 'Team Setup', font = ('Arial', 14))
        self.title_label.pack(pady = 10)

        # Frame to hold team widgets
        self.teams_frame = tk.Frame(self)
        self.teams_frame.pack()

        # Initialize variables to hold team name and draft position for an arbitrary number of teams
        self.team_name_vars = []
        self.team_position_vars = []

        for i in range(self.my_draft.num_teams):
            # Team name setup
            team_name_label = tk.Label(self.teams_frame, text = f'Team {i + 1} Name:')
            team_name_label.grid(row = i, column = 0, padx = 5, pady = 5)
            team_name_var = tk.StringVar()
            team_name_entry = tk.Entry(self.teams_frame, textvariable = team_name_var)
            team_name_entry.grid(row = i, column = 1, padx = 5, pady = 5)
            self.team_name_vars.append(team_name_var)

            # Draft position setup
            team_position_label = tk.Label(self.teams_frame, text = f'Team {i + 1} Draft Position:')
            team_position_label.grid(row = i, column = 2, padx = 5, pady = 5)
            team_position_var = tk.IntVar()
            team_position_entry = tk.Entry(self.teams_frame, textvariable = team_position_var)
            team_position_entry.grid(row = i, column = 3, padx = 5, pady = 5)
            self.team_position_vars.append(team_position_var)

        # Next button to finalize team setup
        self.next_button = tk.Button(self, text = 'Next', command = self.submit_teams_settings)
        self.next_button.pack(pady = 20)

    # Method to process teams settings
    def submit_teams_settings(self):
        my_teams = []
        i = 1

        # Create Team objects from input from the user
        for name_var, position_var in zip(self.team_name_vars, self.team_position_vars):
            team_var_name = f'team_{str(i)}'
            team_var_name = Team(name_var.get(), position_var.get(), self.my_db_table)
            my_teams.append(team_var_name)
            i +=  1

        # Show next frame after collecting teams data
        self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_db_table, my_teams)
