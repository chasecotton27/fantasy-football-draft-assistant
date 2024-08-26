import tkinter as tk
from tkinter import ttk
from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft
from ui.team_setup_frame import TeamSetupFrame

class DraftSetupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Create scoring format label
        self.scoring_format_label = tk.Label(self, text = 'Select Scoring Format:')
        self.scoring_format_label.pack(pady = 10)

        # Create scoring format combobox and store it as a variable
        self.scoring_format_var = tk.StringVar(value = 'Standard')
        self.scoring_format_menu = ttk.Combobox(self, textvariable = self.scoring_format_var)
        self.scoring_format_menu['values'] = ('Standard', 'Half PPR', 'Full PPR')
        self.scoring_format_menu.pack()

        # Create position count label
        self.position_count_label = tk.Label(self, text = 'Enter Position Counts:')
        self.position_count_label.pack(pady = 10)

        # Initialize list of positions and a dictionary for position entries
        self.positions = ['QB', 'RB', 'WR', 'TE', 'Flex', 'K', 'DST', 'Bench']
        self.position_entries = {}

        for position in self.positions:
            # Create position label
            position_label = tk.Label(self, text = f'{position}:')
            position_label.pack()
            position_entry = tk.Entry(self)
            position_entry.pack()

            # Add position entry to positions entries dictionary
            self.position_entries[position] = position_entry

        # Create drafting style label
        self.drafting_style_label = tk.Label(self, text = 'Select Drafting Style:')
        self.drafting_style_label.pack(pady = 10)

        # Create drafting style combobox and store it as a variable
        self.drafting_style_var = tk.StringVar(value = 'Standard')
        self.drafting_style_menu = ttk.Combobox(self, textvariable = self.drafting_style_var)
        self.drafting_style_menu['values'] = ('Standard', 'Snake')
        self.drafting_style_menu.pack()

        # Create team count label
        self.team_count_label = tk.Label(self, text = 'Enter the number of teams:')
        self.team_count_label.pack(pady = 10)

        # Create team count entry and store it as a variable
        self.team_count_var = tk.IntVar(value = 12)
        self.team_count_entry = tk.Entry(self, textvariable = self.team_count_var)
        self.team_count_entry.pack()

        # Create next button to finalize draft setup
        self.next_button = tk.Button(self, text = 'Next', command = self.submit_draft_settings)
        self.next_button.pack(pady = 20)

    def submit_draft_settings(self):
        # Collect draft settings data
        scoring_format = self.scoring_format_var.get()
        position_count = {position: int(entry.get()) for position, entry in self.position_entries.items()}
        drafting_style = self.drafting_style_var.get()
        num_teams = self.team_count_var.get()

        # Create Draft object from input from the user
        my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)

        # Conditional logic to determine which CSV file to create a database from
        if my_draft.scoring_format == 'Standard':
            db_table_name = 'standard_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Standard.csv'
        elif my_draft.scoring_format == 'Half PPR':
            db_table_name = 'half_ppr_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Half_PPR.csv'
        elif my_draft.scoring_format == 'Full PPR':
            db_table_name = 'full_ppr_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Full_PPR.csv'

        # Create DatabaseTable object
        my_db_table = DatabaseTable(db_table_name)

        # Create CSVFile object (no need to store as a variable)
        CSVFile(csv_file_path, my_db_table)

        # Show next frame after completing draft setup
        self.controller.show_frame(TeamSetupFrame, my_draft, my_db_table)
