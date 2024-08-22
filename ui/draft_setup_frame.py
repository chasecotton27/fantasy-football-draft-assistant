import tkinter as tk
from tkinter import ttk
from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft
from ui.team_setup_frame import TeamSetupFrame

class DraftSetupFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Scoring format setup
        self.scoring_format_label = tk.Label(self, text = 'Select Scoring Format:')
        self.scoring_format_label.pack(pady = 10)
        self.scoring_format_var = tk.StringVar(value = 'Standard')
        self.scoring_format_menu = ttk.Combobox(self, textvariable = self.scoring_format_var)
        self.scoring_format_menu['values'] = ('Standard', 'Half PPR', 'Full PPR')
        self.scoring_format_menu.pack()

        # Position count setup
        self.position_count_label = tk.Label(self, text = 'Enter Position Counts:')
        self.position_count_label.pack(pady = 10)
        self.positions = ['QB', 'RB', 'WR', 'TE', 'Flex', 'K', 'D/ST', 'Bench']
        self.position_entries = {}

        for position in self.positions:
            label = tk.Label(self, text = f'{position}:')
            label.pack()
            entry = tk.Entry(self)
            entry.pack()
            self.position_entries[position] = entry

        # Drafting style setup
        self.drafting_style_label = tk.Label(self, text = 'Select Drafting Style:')
        self.drafting_style_label.pack(pady = 10)
        self.drafting_style_var = tk.StringVar(value = 'Standard')
        self.drafting_style_menu = ttk.Combobox(self, textvariable = self.drafting_style_var)
        self.drafting_style_menu['values'] = ('Standard', 'Snake')
        self.drafting_style_menu.pack()

        # Number of teams setup
        self.team_count_label = tk.Label(self, text = 'Enter the number of teams:')
        self.team_count_label.pack(pady = 10)
        self.team_count_var = tk.IntVar(value = 12)
        self.team_count_entry = tk.Entry(self, textvariable = self.team_count_var)
        self.team_count_entry.pack()

        # Next button to go to TeamSetupFrame
        self.next_button = tk.Button(self, text = 'Next', command = self.submit_draft_settings)
        self.next_button.pack(pady = 20)

    def submit_draft_settings(self):
        # Collect draft settings data
        scoring_format = self.scoring_format_var.get()
        position_count = {position: int(entry.get()) for position, entry in self.position_entries.items()}
        drafting_style = self.drafting_style_var.get()
        num_teams = self.team_count_var.get()

        # Create Draft object and process
        my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)

        # Conditional logic for user input regarding scoring format
        if my_draft.scoring_format == 'Standard':
            db_table_name = 'standard_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Standard.csv'
        elif my_draft.scoring_format == 'Half PPR':
            db_table_name = 'half_ppr_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Half_PPR.csv'
        elif my_draft.scoring_format == 'Full PPR':
            db_table_name = 'full_ppr_table'
            csv_file_path = 'adp-data/8_11_24_ADP_Rankings_Full_PPR.csv'

        # Instantiate DatabaseTable object to create a database table and a reference object
        my_db_table = DatabaseTable(db_table_name)

        # Instantiate CSVFile object to process CSV data and populate the database table with players
        CSVFile(csv_file_path, my_db_table)

        # Pass data to the next frame
        self.controller.show_frame(TeamSetupFrame, my_draft, my_db_table)
