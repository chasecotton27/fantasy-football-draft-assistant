import tkinter as tk
from tkinter import ttk
from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft
from ui.team_setup_frame import TeamSetupFrame

class DraftSetupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create position count label
        self.position_count_label = tk.Label(self, text='Enter Position Counts:')
        self.position_count_label.pack(padx=520, pady=12)

        # Use a single frame for position entries to reduce widget clutter
        self.position_entries_frame = tk.Frame(self)
        self.position_entries_frame.pack(padx=520, pady=12)

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
        self.scoring_format_label = tk.Label(self, text='Select Scoring Format:')
        self.scoring_format_label.pack(pady=10)
        self.scoring_format_var = tk.StringVar(value='Standard')
        self.scoring_format_menu = ttk.Combobox(self, textvariable=self.scoring_format_var, values=('Standard', 'Half PPR', 'Full PPR'), state='readonly')
        self.scoring_format_menu.pack(padx=520, pady=12)

        # Create drafting style label and combobox
        self.drafting_style_label = tk.Label(self, text='Select Drafting Style:')
        self.drafting_style_label.pack(pady=10)
        self.drafting_style_var = tk.StringVar(value='Standard')
        self.drafting_style_menu = ttk.Combobox(self, textvariable=self.drafting_style_var, values=('Standard', 'Snake'), state='readonly')
        self.drafting_style_menu.pack(padx=520, pady=12)

        # Create team count label and entry
        self.team_count_label = tk.Label(self, text='Enter the number of teams:')
        self.team_count_label.pack(pady=10)
        self.team_count_var = tk.IntVar(value=12)
        self.team_count_entry = tk.Entry(self, textvariable=self.team_count_var, width=5)
        self.team_count_entry.pack(padx=520, pady=12)

        # Create next button to finalize draft setup
        self.next_button = tk.Button(self, text='Next', command=self.submit_draft_settings)
        self.next_button.pack(padx=520, pady=12)

        # Cache last draft settings to avoid unnecessary reloads
        self.last_settings = None

    def submit_draft_settings(self):
        # Collect draft settings data
        scoring_format = self.scoring_format_var.get()
        try:
            position_count = {position: int(entry.get()) for position, entry in self.position_entries.items()}
        except ValueError:
            position_count = {position: 1 for position in self.positions}

        drafting_style = self.drafting_style_var.get()
        num_teams = self.team_count_var.get()

        # Cache settings to avoid unnecessary reloads
        settings_tuple = (scoring_format, tuple(position_count.items()), drafting_style, num_teams)
        if self.last_settings == settings_tuple:
            # If settings haven't changed, don't reload database
            self.controller.show_frame(TeamSetupFrame, self.my_draft, self.my_db_table, self.my_csv_file)
            return

        self.last_settings = settings_tuple

        # Create Draft object from input from the user
        my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)

        # Conditional logic to determine which CSV file to create a database from
        if my_draft.scoring_format == 'Standard':
            db_table_name = 'standard_table'
            csv_file_path = 'adp-data/8_20_25_ADP_Rankings_Standard.csv'
        elif my_draft.scoring_format == 'Half PPR':
            db_table_name = 'half_ppr_table'
            csv_file_path = 'adp-data/8_20_25_ADP_Rankings_Half_PPR.csv'
        else:
            db_table_name = 'full_ppr_table'
            csv_file_path = 'adp-data/8_20_25_ADP_Rankings_Full_PPR.csv'

        # Create DatabaseTable object
        my_db_table = DatabaseTable(db_table_name)

        # Create CSVFile object (no need to store as a variable)
        my_csv_file = CSVFile(csv_file_path, my_db_table)

        # Store for caching
        self.my_draft = my_draft
        self.my_db_table = my_db_table
        self.my_csv_file = my_csv_file

        # Show next frame after completing draft setup
        self.controller.show_frame(TeamSetupFrame, my_draft, my_db_table, my_csv_file)
