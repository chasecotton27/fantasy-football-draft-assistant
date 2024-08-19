import tkinter as tk
from backend.processing import PlayerBoard

class DraftBoardFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table, my_teams):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table
        self.my_teams = my_teams
        self.my_player_board = PlayerBoard(my_db_table)

        # Title label
        self.title_label = tk.Label(self, text='Draft Board', font=('Arial', 14))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Set up grid layout for different widgets on the draft board
        self.create_widgets()

    def create_widgets(self):
        # Top Section
        top_frame = tk.Frame(self, bg="lightblue", height=50)
        top_frame.grid(row=1, column=0, columnspan=3, sticky="ew")
        top_frame.grid_propagate(False)

        # Filter Buttons Section (Above Player List)
        filter_buttons_frame = tk.Frame(self, bg="lightgrey", height=30)
        filter_buttons_frame.grid(row=2, column=1, sticky="ew")
        filter_buttons_frame.grid_propagate(False)

        # Add Filter Buttons
        qb_button = tk.Button(filter_buttons_frame, text="QB", command=self.show_qbs)
        rb_button = tk.Button(filter_buttons_frame, text="RB", command=self.show_rbs)
        wr_button = tk.Button(filter_buttons_frame, text="WR", command=self.show_wrs)
        te_button = tk.Button(filter_buttons_frame, text="TE", command=self.show_tes)
        k_button = tk.Button(filter_buttons_frame, text="K", command=self.show_ks)
        dst_button = tk.Button(filter_buttons_frame, text="D/ST", command=self.show_dsts)

        qb_button.pack(side="left", padx=5, pady=5)
        rb_button.pack(side="left", padx=5, pady=5)
        wr_button.pack(side="left", padx=5, pady=5)
        te_button.pack(side="left", padx=5, pady=5)
        k_button.pack(side="left", padx=5, pady=5)
        dst_button.pack(side="left", padx=5, pady=5)

        # Column Titles Section
        column_titles_frame = tk.Frame(self, bg="lightgrey", height=30)
        column_titles_frame.grid(row=3, column=1, sticky="ew")
        column_titles_frame.grid_propagate(False)

        # Add Column Titles
        rank_label = tk.Label(column_titles_frame, text="Rank", width=10, anchor="w", bg="lightgrey")
        name_label = tk.Label(column_titles_frame, text="Name", width=20, anchor="w", bg="lightgrey")
        team_label = tk.Label(column_titles_frame, text="Team", width=10, anchor="w", bg="lightgrey")
        bye_label = tk.Label(column_titles_frame, text="Bye", width=10, anchor="w", bg="lightgrey")
        position_label = tk.Label(column_titles_frame, text="Position", width=10, anchor="w", bg="lightgrey")
        avg_adp_label = tk.Label(column_titles_frame, text="Avg ADP", width=10, anchor="w", bg="lightgrey")

        rank_label.pack(side="left", padx=5)
        name_label.pack(side="left", padx=5)
        team_label.pack(side="left", padx=5)
        bye_label.pack(side="left", padx=5)
        position_label.pack(side="left", padx=5)
        avg_adp_label.pack(side="left", padx=5)

        # Middle Section (Scrollable Frame)
        middle_frame = tk.Frame(self, bg="white")
        middle_frame.grid(row=4, column=1, sticky="nsew")
        middle_frame.grid_propagate(False)

        # Create a canvas and a scrollbar
        canvas = tk.Canvas(middle_frame, bg="white")
        scrollbar = tk.Scrollbar(middle_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame within the canvas
        self.scrollable_frame = tk.Frame(canvas, bg="white")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Add the frame to a window in the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Load players
        self.display_available_players()

        # Left Section
        left_frame = tk.Frame(self, bg="lightgreen", width=150)
        left_frame.grid(row=2, column=0, sticky="ns", rowspan=3)
        left_frame.grid_propagate(False)

        # Right Section
        right_frame = tk.Frame(self, bg="lightyellow", width=150)
        right_frame.grid(row=2, column=2, sticky="ns", rowspan=3)
        right_frame.grid_propagate(False)

        # Above Bottom Section
        above_bottom_frame = tk.Frame(self, bg="lightgrey", height=30)
        above_bottom_frame.grid(row=5, column=0, columnspan=3, sticky="ew")
        above_bottom_frame.grid_propagate(False)

        # Bottom Section
        bottom_frame = tk.Frame(self, bg="lightcoral", height=50)
        bottom_frame.grid(row=6, column=0, columnspan=3, sticky="ew")
        bottom_frame.grid_propagate(False)

        # Configure the grid to make the middle frame expand
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def display_available_players(self):
        # Clear previous player widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Create a label for each player
        for player in self.my_player_board.players:
            player_frame = tk.Frame(self.scrollable_frame, bg="lightgrey", pady=2)
            player_frame.pack(fill="x", padx=5, pady=2)

            rank_label = tk.Label(player_frame, text=player[1], anchor="w", width=10)
            rank_label.pack(side="left", padx=5)

            name_label = tk.Label(player_frame, text=player[2], anchor="w", width=20)
            name_label.pack(side="left", padx=5)

            team_label = tk.Label(player_frame, text=player[3], anchor="w", width=10)
            team_label.pack(side="left", padx=5)

            bye_label = tk.Label(player_frame, text=player[4], anchor="w", width=10)
            bye_label.pack(side="left", padx=5)

            position_label = tk.Label(player_frame, text=player[5], anchor="w", width=10)
            position_label.pack(side="left", padx=5)

            avg_adp_label = tk.Label(player_frame, text=player[12], anchor="w", width=10)
            avg_adp_label.pack(side="left", padx=5)

    def show_qbs(self):
        # filter and update player board with quarterbacks
        self.my_player_board.players = self.my_player_board.filter_qbs()
        self.display_available_players()

    def show_rbs(self):
        # filter and update player board with running backs
        self.my_player_board.players = self.my_player_board.filter_rbs()
        self.display_available_players()

    def show_wrs(self):
        # filter and update player board with wide receivers
        self.my_player_board.players = self.my_player_board.filter_wrs()
        self.display_available_players()

    def show_tes(self):
        # filter and update player board with tight ends
        self.my_player_board.players = self.my_player_board.filter_tes()
        self.display_available_players()

    def show_ks(self):
        # filter and update player board with kickers
        self.my_player_board.players = self.my_player_board.filter_ks()
        self.display_available_players()

    def show_dsts(self):
        # filter and update player board with defenses / special teams
        self.my_player_board.players = self.my_player_board.filter_dsts()
        self.display_available_players()
