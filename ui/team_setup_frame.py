import tkinter as tk
from backend.processing import Team
from ui.draft_board_frame import DraftBoardFrame

class TeamSetupFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table

        # Create title label
        self.title_label = tk.Label(self, text = 'Team Setup', font = ('Arial', 14))
        self.title_label.pack(pady = 10)

        # Create teams frame
        self.teams_frame = tk.Frame(self)
        self.teams_frame.pack()

        # Initialize lists to store teams names and their draft positions
        self.team_names = []
        self.draft_positions = []

        # Loop through the number of teams from previous frame
        for i in range(self.my_draft.num_teams):
            # Create team name label
            team_name_label = tk.Label(self.teams_frame, text = f'Team {i + 1} Name:')
            team_name_label.grid(row = i, column = 0, padx = 5, pady = 5)

            # Create team name entry and store it as a variable
            team_name_var = tk.StringVar()
            team_name_entry = tk.Entry(self.teams_frame, textvariable = team_name_var)
            team_name_entry.grid(row = i, column = 1, padx = 5, pady = 5)

            # Add team name variable to the list
            self.team_names.append(team_name_var)

            # Create draft position label
            draft_position_label = tk.Label(self.teams_frame, text = f'Team {i + 1} Draft Position:')
            draft_position_label.grid(row = i, column = 2, padx = 5, pady = 5)

            # Create draft position entry and store it as a variable
            draft_position_var = tk.IntVar()
            draft_position_entry = tk.Entry(self.teams_frame, textvariable = draft_position_var)
            draft_position_entry.grid(row = i, column = 3, padx = 5, pady = 5)

            # Add draft position variable to the list
            self.draft_positions.append(draft_position_var)

        # Create next button to finalize team setup
        self.next_button = tk.Button(self, text = 'Next', command = self.submit_teams_settings)
        self.next_button.pack(pady = 20)

    # Method to process teams settings
    def submit_teams_settings(self):
        my_teams = []
        i = 1

        # Create Team objects from input from the user
        for name_var, position_var in zip(self.team_names, self.draft_positions):
            team_var_name = f'team_{str(i)}'
            team_var_name = Team(name_var.get(), position_var.get(), self.my_db_table, self.my_draft)
            my_teams.append(team_var_name)
            i +=  1

        # Show next frame after completing team setup
        self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_db_table, my_teams)
