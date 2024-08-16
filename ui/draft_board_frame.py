import tkinter as tk
from backend.processing import PlayerBoard

class DraftBoardFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table, my_teams):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table
        self.my_teams = my_teams

        # Title label
        self.title_label = tk.Label(self, text = 'Draft Board', font = ('Arial', 14))
        self.title_label.pack(pady=10)
