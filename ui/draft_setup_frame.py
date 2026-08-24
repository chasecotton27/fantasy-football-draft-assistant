import tkinter as tk
from tkinter import ttk
from backend.repository import PlayerRepository
from backend.processing import CSVFile, Draft, SCORING_FORMAT_CSV_PATHS
from ui.team_setup_frame import TeamSetupFrame

class DraftSetupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Center content between two expanding spacer columns instead of fixed padx hacks
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.content_frame = tk.Frame(self)
        self.content_frame.grid(row=0, column=1, sticky='n', pady=20)

        # Create position count label
        self.position_count_label = tk.Label(self.content_frame, text='Enter Position Counts:')
        self.position_count_label.pack(pady=12)

        # Use a single frame for position entries to reduce widget clutter
        self.position_entries_frame = tk.Frame(self.content_frame)
        self.position_entries_frame.pack(pady=12)

        # Initialize list of positions and a dictionary for position entries
        self.positions = ['QB', 'RB', 'WR', 'TE', 'Flex', 'K', 'DST', 'Bench']
        self.position_entries = {}

        # Use grid for position entries for better performance and layout
        for idx, position in enumerate(self.positions):
            position_label = tk.Label(self.position_entries_frame, text=f'{position}:')
            position_label.grid(row=idx, column=0, sticky='w', padx=5, pady=2)
            position_entry = tk.Entry(self.position_entries_frame, width=5)
            position_entry.grid(row=idx, column=1, padx=5, pady=2)
            self.position_entries[position] = position_entry

        # Create scoring format label and combobox
        self.scoring_format_label = tk.Label(self.content_frame, text='Select Scoring Format:')
        self.scoring_format_label.pack(pady=10)
        self.scoring_format_var = tk.StringVar(value='Standard')
        self.scoring_format_menu = ttk.Combobox(self.content_frame, textvariable=self.scoring_format_var, values=('Standard', 'Half PPR', 'Full PPR'), state='readonly')
        self.scoring_format_menu.pack(pady=12)

        # Create drafting style label and combobox
        self.drafting_style_label = tk.Label(self.content_frame, text='Select Drafting Style:')
        self.drafting_style_label.pack(pady=10)
        self.drafting_style_var = tk.StringVar(value='Standard')
        self.drafting_style_menu = ttk.Combobox(self.content_frame, textvariable=self.drafting_style_var, values=('Standard', 'Snake'), state='readonly')
        self.drafting_style_menu.pack(pady=12)

        # Create team count label and entry (plain StringVar so bad input can't raise TclError)
        self.team_count_label = tk.Label(self.content_frame, text='Enter the number of teams:')
        self.team_count_label.pack(pady=10)
        self.team_count_var = tk.StringVar(value='12')
        self.team_count_entry = tk.Entry(self.content_frame, textvariable=self.team_count_var, width=5)
        self.team_count_entry.pack(pady=12)

        # Error message shown when validation fails
        self.error_label = tk.Label(self.content_frame, text='', fg='red')
        self.error_label.pack(pady=4)

        # Create next button to finalize draft setup
        self.next_button = tk.Button(self.content_frame, text='Next', command=self.submit_draft_settings)
        self.next_button.pack(pady=12)

        # Cache last draft settings to avoid unnecessary reloads
        self.last_settings = None

    def _show_error(self, message):
        self.error_label.config(text=message)

    def _validate_settings(self):
        # Validate position counts: must all be non-negative integers
        position_count = {}
        for position, entry in self.position_entries.items():
            raw_value = entry.get().strip()
            try:
                count = int(raw_value)
            except ValueError:
                self._show_error(f'{position} count must be a whole number.')
                return None, None
            if count < 0:
                self._show_error(f'{position} count cannot be negative.')
                return None, None
            position_count[position] = count

        # Validate team count: must be a positive integer
        raw_team_count = self.team_count_var.get().strip()
        try:
            num_teams = int(raw_team_count)
        except ValueError:
            self._show_error('Number of teams must be a whole number.')
            return None, None
        if num_teams < 2:
            self._show_error('Number of teams must be at least 2.')
            return None, None

        self._show_error('')
        return position_count, num_teams

    def submit_draft_settings(self):
        position_count, num_teams = self._validate_settings()
        if position_count is None:
            return

        scoring_format = self.scoring_format_var.get()
        drafting_style = self.drafting_style_var.get()

        # Cache settings to avoid unnecessary reloads
        settings_tuple = (scoring_format, tuple(position_count.items()), drafting_style, num_teams)
        if self.last_settings == settings_tuple:
            # If settings haven't changed, don't reload the player data
            self.controller.show_frame(TeamSetupFrame, self.my_draft, self.my_player_repository, self.my_csv_file)
            return

        self.last_settings = settings_tuple

        # Create Draft object from input from the user
        my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)

        # Load player data for the selected scoring format
        my_player_repository = PlayerRepository()
        my_csv_file = CSVFile(SCORING_FORMAT_CSV_PATHS[my_draft.scoring_format], my_player_repository)

        # Store for caching
        self.my_draft = my_draft
        self.my_player_repository = my_player_repository
        self.my_csv_file = my_csv_file

        # Show next frame after completing draft setup
        self.controller.show_frame(TeamSetupFrame, my_draft, my_player_repository, my_csv_file)
