import tkinter as tk
from backend.processing import Team
from ui.draft_board_frame import DraftBoardFrame

class TeamSetupFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table, my_csv_file):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table
        self.my_csv_file = my_csv_file

        # Create title label
        self.title_label = tk.Label(self, text='Team Setup', font=('Arial', 14))
        self.title_label.pack(pady=40)

        # Create teams frame
        self.teams_frame = tk.Frame(self)
        self.teams_frame.pack()

        # Initialize lists to store teams names and their draft positions
        self.team_names = []
        self.draft_positions = []

        # Use a single loop to create all widgets and cache variables
        for i in range(self.my_draft.num_teams):
            team_name_var = tk.StringVar()
            draft_position_var = tk.IntVar()

            tk.Label(self.teams_frame, text=f'Team {i + 1} Name:').grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(self.teams_frame, textvariable=team_name_var).grid(row=i, column=1, padx=5, pady=5)
            tk.Label(self.teams_frame, text=f'Team {i + 1} Draft Position:').grid(row=i, column=2, padx=5, pady=5)
            tk.Entry(self.teams_frame, textvariable=draft_position_var).grid(row=i, column=3, padx=5, pady=5)

            self.team_names.append(team_name_var)
            self.draft_positions.append(draft_position_var)

        # Create next button to finalize team setup
        self.next_button = tk.Button(self, text='Next', command=self.submit_teams_settings)
        self.next_button.pack(pady=40)

        # Cache last team settings to avoid unnecessary recreation
        self.last_team_settings = None

    # Method to process teams settings
    def submit_teams_settings(self):
        # Collect team settings data
        team_settings_tuple = tuple((name_var.get(), position_var.get()) for name_var, position_var in zip(self.team_names, self.draft_positions))
        if self.last_team_settings == team_settings_tuple:
            # If settings haven't changed, don't recreate teams
            self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_db_table, self.my_csv_file, self.my_teams)
            return

        self.last_team_settings = team_settings_tuple

        # Create Team objects from input from the user using list comprehension
        my_teams = [
            Team(name_var.get(), position_var.get(), self.my_db_table, self.my_draft)
            for name_var, position_var in zip(self.team_names, self.draft_positions)
        ]
        self.my_teams = my_teams

        # Show next frame after completing team setup
        self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_db_table, self.my_csv_file, my_teams)
