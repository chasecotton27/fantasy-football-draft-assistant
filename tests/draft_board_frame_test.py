import tkinter as tk
from ui.draft_board_frame import DraftBoardFrame
from backend.database import DatabaseTable
from backend.processing import CSVFile, Draft, Team

class DraftApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Fantasy Football Draft Assistant')
        self.geometry('1200x600')

        self.container = tk.Frame(self)
        self.container.grid(row = 0, column = 0, sticky = 'nsew')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.show_frame(DraftBoardFrame, my_draft, my_db_table, my_csv_file, my_teams)

    def show_frame(self, frame_class, *args):
        frame = frame_class(parent = self.container, controller = self, my_draft = args[0],
                            my_db_table = args[1], my_csv_file = args[2], my_teams = args[3])
        frame.grid(row = 0, column = 0, sticky = 'nsew')

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        frame.tkraise()

if __name__ == '__main__':
    scoring_format = 'Full PPR'
    position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 7}
    drafting_style = 'Snake'
    num_teams = 12

    my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)
    my_db_table = DatabaseTable('full_ppr_table')
    my_csv_file = CSVFile('adp-data/8_11_24_ADP_Rankings_Full_PPR.csv', my_db_table)

    team_names = ['Team Bryant', 'Show us your TDs', '1-2 Punch', 'NC BrownMambas', 'San Antonio Bean and Cheese', 'Hold my D--ker', 'Team ROBINSON', 'afghaNAVstan',
                'Shauna Cotton', 'Blane SUPER MEGA Qweef', 'Bobby Boucher', 'Debby Gallagher']
    draft_positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    my_teams = []

    for team_name, draft_position in zip(team_names, draft_positions):
        team  = Team(team_name, draft_position, my_db_table, my_draft)
        my_teams.append(team)

    app = DraftApp()
    app.mainloop()
