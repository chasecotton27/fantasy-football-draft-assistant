import sys
from pathlib import Path

# Allow running this script directly (python scripts/quick_draft.py) by putting the
# project root on sys.path, since it isn't a package itself.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import tkinter as tk
from ui.draft_board_frame import DraftBoardFrame
from backend.repository import PlayerRepository
from backend.processing import CSVFile, Draft, Team, SCORING_FORMAT_CSV_PATHS


class QuickDraftApp(tk.Tk):
    def __init__(self, my_draft, my_player_repository, my_csv_file, my_teams):
        super().__init__()
        self.title('Fantasy Football Draft Assistant')
        self.geometry('1200x600')
        self.minsize(900, 500)

        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = DraftBoardFrame(parent=self.container, controller=self, my_draft=my_draft,
                                 my_player_repository=my_player_repository, my_csv_file=my_csv_file,
                                 my_teams=my_teams)
        frame.grid(row=0, column=0, sticky='nsew')
        frame.tkraise()


if __name__ == '__main__':
    scoring_format = 'Full PPR'
    position_count = {'QB': 1, 'RB': 2, 'WR': 2, 'TE': 1, 'Flex': 1, 'K': 1, 'DST': 1, 'Bench': 7}
    drafting_style = 'Snake'
    num_teams = 12

    my_draft = Draft(scoring_format, position_count, drafting_style, num_teams)
    my_player_repository = PlayerRepository()
    my_csv_file = CSVFile(SCORING_FORMAT_CSV_PATHS[scoring_format], my_player_repository)

    team_names = [
        'Team Bryant', 'Show us your TDs', '1-2 Punch', 'NC BrownMambas',
        'San Antonio Bean and Cheese', 'Hold my D--ker', 'Team ROBINSON', 'afghaNAVstan',
        'Shauna Cotton', 'Blane SUPER MEGA Qweef', 'Bobby Boucher', 'Debby Gallagher',
    ]
    draft_positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    my_teams = [
        Team(team_name, draft_position, my_player_repository, my_draft)
        for team_name, draft_position in zip(team_names, draft_positions)
    ]

    app = QuickDraftApp(my_draft, my_player_repository, my_csv_file, my_teams)
    app.mainloop()
