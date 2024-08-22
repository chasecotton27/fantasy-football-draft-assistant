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

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=0)
        self.grid_rowconfigure(6, weight=0)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_columnconfigure(2, weight=1)

        self.title_frame = tk.Frame(self, bg='lightcoral')
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.draft_order_frame = tk.Frame(self, bg='lightgreen')
        self.draft_order_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')

        self.team_roster_title_frame = tk.Frame(self, bg='lightcoral')
        self.team_roster_title_frame.grid(row=2, column=0, sticky='nsew')

        self.player_filters_frame = tk.Frame(self, bg='lightcoral')
        self.player_filters_frame.grid(row=2, column=1, sticky='nsew')

        self.draft_history_title_frame = tk.Frame(self, bg='lightcoral')
        self.draft_history_title_frame.grid(row=2, column=2, sticky='nsew')

        self.team_name_frame = tk.Frame(self, bg='lightgreen')
        self.team_name_frame.grid(row=3, column=0, sticky='nsew')

        self.column_titles_frame = tk.Frame(self, bg='lightgreen')
        self.column_titles_frame.grid(row=3, column=1, sticky='nsew')

        self.league_name_frame = tk.Frame(self, bg='lightgreen')
        self.league_name_frame.grid(row=3, column=2, sticky='nsew')

        self.team_roster_frame = tk.Frame(self, bg='lightcoral', width=300)
        self.team_roster_frame.grid(row=4, column=0, sticky='nsew')

        self.available_players_frame = tk.Frame(self, bg='lightcoral', width=600)
        self.available_players_frame.grid(row=4, column=1, sticky='nsew')

        self.draft_history_frame = tk.Frame(self, bg='lightcoral', width=300)
        self.draft_history_frame.grid(row=4, column=2, sticky='nsew')

        self.recommendations_title_frame = tk.Frame(self, bg='lightgreen')
        self.recommendations_title_frame.grid(row=5, column=0, columnspan=3, sticky='nsew')

        self.recommendations_frame = tk.Frame(self, bg='lightcoral')
        self.recommendations_frame.grid(row=6, column=0, columnspan=3, sticky='nsew')

        # Create variables for number of players on a team and instantiate draft_order
        num_team_players = sum(self.my_draft.position_count.values())
        self.draft_order = []

        # Populate draft_order with team names if drafting style is standard
        if self.my_draft.drafting_style == 'Standard':
            for _ in range(num_team_players):
                for i in range(1, self.my_draft.num_teams + 1):
                    for team in self.my_teams:
                        if team.draft_position == i:
                            self.draft_order.append(team.team_name)
                            break

        # Populate draft_order with team names if drafting style is snake
        elif self.my_draft.drafting_style == 'Snake':
            forward = True
            for _ in range(num_team_players):
                if forward:
                    for i in range(1, self.my_draft.num_teams + 1):
                        for team in self.my_teams:
                            if team.draft_position == i:
                                self.draft_order.append(team.team_name)
                                break
                else:
                    for i in range(self.my_draft.num_teams, 0, -1):
                        for team in self.my_teams:
                            if team.draft_position == i:
                                self.draft_order.append(team.team_name)
                                break
                forward = not forward

        # Display starting state for UI frames
        self.create_scrollable_frame(self.team_roster_frame)
        self.create_scrollable_frame(self.available_players_frame)
        self.create_scrollable_frame(self.draft_history_frame)
        self.display_static_frames()
        self.display_draft_order()
        self.display_team_roster()
        self.display_available_players()

    def create_scrollable_frame(self, frame):
        # Create a canvas within the frame
        canvas = tk.Canvas(frame, bg="lightyellow")
        canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the right of the canvas
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Configure the grid for the parent frame
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)

        # Create a scrollable frame inside the canvas
        scrollable_frame = tk.Frame(canvas, bg="lightgrey")
        scrollable_frame.grid(row=0, column=0, sticky='nsew')

        # Bind the scroll region to the size of the scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Add the scrollable frame to the canvas
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        # Configure the scrollbar to work with the canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind the canvas to adjust the scrollable frame width
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas_window, width=e.width))

        # Store the scrollable frame object as an attribute to access later
        if frame == self.team_roster_frame:
            self.team_roster_scrollable_frame = scrollable_frame
        elif frame == self.available_players_frame:
            self.available_players_scrollable_frame = scrollable_frame
        elif frame == self.draft_history_frame:
            self.draft_history_scrollable_frame = scrollable_frame

    def display_static_frames(self):
        # Create title label
        self.title_frame.grid_columnconfigure(0, weight=1)
        title_label = tk.Label(self.title_frame, text='Draft Board', font=('Arial', 12))
        title_label.grid(row=0, column=0, sticky='nsew')

        # Create team roster title label
        self.team_roster_title_frame.grid_columnconfigure(0, weight=1)
        team_roster_title_label = tk.Label(self.team_roster_title_frame, text='Team Roster', font=('Arial', 12))
        team_roster_title_label.grid(row=0, column=0, sticky='nsew')

        # Create player filters buttons
        filter_texts = ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'D/ST']
        filter_commands = [self.show_all, self.show_qbs, self.show_rbs, self.show_wrs, self.show_tes, self.show_ks, self.show_dsts]

        for i in range(7):
            self.player_filters_frame.grid_columnconfigure(i, weight=1)
            tk.Button(self.player_filters_frame, text=filter_texts[i], font=('Arial', 8), command=filter_commands[i]).grid(row=0, column=i, padx=2, pady=5, sticky='nsew')

        # Create draft history title label
        self.draft_history_title_frame.grid_columnconfigure(0, weight=1)
        draft_history_title_label = tk.Label(self.draft_history_title_frame, text='Draft History', font=('Arial', 12))
        draft_history_title_label.grid(row=0, column=0, sticky='nsew')

        # Create team name label
        self.team_name_frame.grid_columnconfigure(0, weight=1)
        team_name_label = tk.Label(self.team_name_frame, text='My Team Name', font=('Arial', 8))
        team_name_label.grid(row=0, column=0, sticky='nsew')

        # Create column titles labels
        column_texts = ['Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP', '']

        for i in range(7):
            self.column_titles_frame.grid_columnconfigure(i, weight=1)
            tk.Label(self.column_titles_frame, text=column_texts[i], anchor='w', font=('Arial', 8)).grid(row=0, column=i, sticky='nsew')

        # Create league name label
        self.league_name_frame.grid_columnconfigure(0, weight=1)
        league_name_label = tk.Label(self.league_name_frame, text='My League Name', font=('Arial', 8))
        league_name_label.grid(row=0, column=0, sticky='nsew')

        # Create recommendations title label
        self.recommendations_title_frame.grid_columnconfigure(0, weight=1)
        recommendations_title_label = tk.Label(self.recommendations_title_frame, text='Recommendations', font=('Arial', 12))
        recommendations_title_label.grid(row=0, column=0, sticky='nsew')

    def display_draft_order(self):
        # Number of teams in the draft
        num_teams = self.my_draft.num_teams

        # Clear any existing labels in the draft_order_frame
        for widget in self.draft_order_frame.winfo_children():
            widget.destroy()

        # Configure the grid to ensure labels expand as needed
        self.draft_order_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, num_teams + 1):
            self.draft_order_frame.grid_columnconfigure(i, weight=1)
        self.draft_order_frame.grid_columnconfigure(num_teams + 1, weight=1)

        # Create labels for each team in the draft
        for i in range(num_teams):
            team_name = self.draft_order[i]
            team_name_label = tk.Label(self.draft_order_frame, text=team_name, font=('Arial', 8))
            team_name_label.grid(row=0, column=i+1, padx=5, pady=10, sticky="nsew")

    def display_team_roster(self):
        # Clear the current roster display
        for widget in self.team_roster_scrollable_frame.winfo_children():
            widget.destroy()

        # Configure the grid to ensure labels expand as needed
        self.team_roster_scrollable_frame.grid_columnconfigure(0, weight=1)

        # Get the current drafting team
        current_team_name = self.draft_order[0]
        current_team = None
        for team in self.my_teams:
            if team.team_name == current_team_name:
                current_team = team
                break

        # Track which positions have already been labeled
        labeled_positions = set()
        row = 0

        # Display the roster in the user roster frame
        for position, count in self.my_draft.position_count.items():
            if position not in labeled_positions:
                # Create a label for the position only once
                position_label = tk.Label(self.team_roster_scrollable_frame, text=position, anchor='w', font=('Arial', 8))
                position_label.grid(row=row, column=0, sticky="ew", padx=5, pady=2)
                labeled_positions.add(position)
                row += 1

            # Create labels for the players
            for _ in range(count):
                player_name = ''
                for player in current_team.roster:
                    if player[5] == position:
                        player_name = player[2]
                        break

                # Create label for the player name (empty if not drafted yet)
                player_name_label = tk.Label(self.team_roster_scrollable_frame, text=player_name, anchor='w', font=('Arial', 8))
                player_name_label.grid(row=row, column=0, sticky="ew", padx=5, pady=2)

                row += 1

    def display_available_players(self):
        # Clear previous player widgets
        for widget in self.available_players_scrollable_frame.winfo_children():
            widget.destroy()

        self.available_players_scrollable_frame.grid_columnconfigure(0, weight=1)
        row = 0

        # Create a label for each player
        for player in self.my_player_board.players:
            player_frame = tk.Frame(self.available_players_scrollable_frame, bg='lightgrey', pady=2)
            player_frame.grid(row=row, column=0, sticky='nsew')

            player_frame.grid_columnconfigure(0, weight=1)
            player_frame.grid_columnconfigure(1, weight=3)
            player_frame.grid_columnconfigure(2, weight=1)
            player_frame.grid_columnconfigure(3, weight=1)
            player_frame.grid_columnconfigure(4, weight=1)
            player_frame.grid_columnconfigure(5, weight=1)
            player_frame.grid_columnconfigure(6, weight=1)

            rank_label = tk.Label(player_frame, text=player[1], anchor="w", font=('Arial', 8))
            rank_label.grid(row=0, column=0, sticky='nsew')

            name_label = tk.Label(player_frame, text=player[2], anchor="w", font=('Arial', 8))
            name_label.grid(row=0, column=1, sticky='nsew')

            team_label = tk.Label(player_frame, text=player[3], anchor="w", font=('Arial', 8))
            team_label.grid(row=0, column=2, sticky='nsew')

            bye_label = tk.Label(player_frame, text=player[4], anchor="w", font=('Arial', 8))
            bye_label.grid(row=0, column=3, sticky='nsew')

            position_label = tk.Label(player_frame, text=player[5], anchor="w", font=('Arial', 8))
            position_label.grid(row=0, column=4, sticky='nsew')

            avg_adp_label = tk.Label(player_frame, text=player[12], anchor="w", font=('Arial', 8))
            avg_adp_label.grid(row=0, column=5, sticky='nsew')

            draft_button = tk.Button(player_frame, text="DRAFT", command=self.draft_player)
            draft_button.grid(row=0, column=6, sticky='nsew')

            row += 1

    def show_all(self):
        # Filter and update player board with all players
        self.my_player_board.players = self.my_player_board.filter_all_players()
        self.display_available_players()

    def show_qbs(self):
        # Filter and update player board with quarterbacks
        self.my_player_board.players = self.my_player_board.filter_qbs()
        self.display_available_players()

    def show_rbs(self):
        # Filter and update player board with running backs
        self.my_player_board.players = self.my_player_board.filter_rbs()
        self.display_available_players()

    def show_wrs(self):
        # Filter and update player board with wide receivers
        self.my_player_board.players = self.my_player_board.filter_wrs()
        self.display_available_players()

    def show_tes(self):
        # Filter and update player board with tight ends
        self.my_player_board.players = self.my_player_board.filter_tes()
        self.display_available_players()

    def show_ks(self):
        # Filter and update player board with kickers
        self.my_player_board.players = self.my_player_board.filter_ks()
        self.display_available_players()

    def show_dsts(self):
        # Filter and update player board with defenses / special teams
        self.my_player_board.players = self.my_player_board.filter_dsts()
        self.display_available_players()

    def draft_player(self):
        pass
