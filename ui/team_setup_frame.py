import tkinter as tk
from backend.processing import Team
from ui.draft_board_frame import DraftBoardFrame

class TeamSetupFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_player_repository, my_csv_file):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_player_repository = my_player_repository
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
            # Plain StringVar (not IntVar) so non-numeric input can't raise an uncaught TclError
            draft_position_var = tk.StringVar(value=str(i + 1))

            tk.Label(self.teams_frame, text=f'Team {i + 1} Name:').grid(row=i, column=0, padx=5, pady=5)
            tk.Entry(self.teams_frame, textvariable=team_name_var).grid(row=i, column=1, padx=5, pady=5)
            tk.Label(self.teams_frame, text=f'Team {i + 1} Draft Position:').grid(row=i, column=2, padx=5, pady=5)
            tk.Entry(self.teams_frame, textvariable=draft_position_var).grid(row=i, column=3, padx=5, pady=5)

            self.team_names.append(team_name_var)
            self.draft_positions.append(draft_position_var)

        # Error message shown when validation fails
        self.error_label = tk.Label(self, text='', fg='red')
        self.error_label.pack(pady=4)

        # Create next button to finalize team setup
        self.next_button = tk.Button(self, text='Next', command=self.submit_teams_settings)
        self.next_button.pack(pady=40)

        # Cache last team settings to avoid unnecessary recreation
        self.last_team_settings = None

    def _show_error(self, message):
        self.error_label.config(text=message)

    def _validate_teams(self):
        names = [name_var.get().strip() for name_var in self.team_names]
        if any(not name for name in names):
            self._show_error('Every team needs a name.')
            return None

        raw_positions = [position_var.get().strip() for position_var in self.draft_positions]
        try:
            positions = [int(value) for value in raw_positions]
        except ValueError:
            self._show_error('Draft positions must be whole numbers.')
            return None

        expected = list(range(1, self.my_draft.num_teams + 1))
        if sorted(positions) != expected:
            self._show_error(f'Draft positions must each be unique, from 1 to {self.my_draft.num_teams}.')
            return None

        self._show_error('')
        return names, positions

    # Method to process teams settings
    def submit_teams_settings(self):
        validated = self._validate_teams()
        if validated is None:
            return
        names, positions = validated

        team_settings_tuple = tuple(zip(names, positions))
        if self.last_team_settings == team_settings_tuple:
            # If settings haven't changed, don't recreate teams
            self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_player_repository, self.my_csv_file, self.my_teams)
            return

        self.last_team_settings = team_settings_tuple

        # Create Team objects from the validated input
        my_teams = [
            Team(name, position, self.my_player_repository, self.my_draft)
            for name, position in zip(names, positions)
        ]
        self.my_teams = my_teams

        # Show next frame after completing team setup
        self.controller.show_frame(DraftBoardFrame, self.my_draft, self.my_player_repository, self.my_csv_file, my_teams)
