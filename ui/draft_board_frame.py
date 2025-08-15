import tkinter as tk
from tkinter import ttk
from backend.processing import PlayerBoard
from backend.recommendations import Simulation

class DraftBoardFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_db_table, my_csv_file, my_teams):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_db_table = my_db_table
        self.my_csv_file = my_csv_file
        self.my_teams = my_teams

        # Create PlayerBoard object once, reuse for filtering
        self.my_player_board = PlayerBoard(my_db_table)

        # Configure rows and columns for main frame (unchanged)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1 if i == 4 else 0)
        for i in range(3):
            self.grid_columnconfigure(i, weight=2 if i == 1 else 1)

        # Create frames (unchanged)
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
        self.recommendations_round_frame = tk.Frame(self, bg='lightcoral')
        self.recommendations_round_frame.grid(row=6, column=0, columnspan=3, sticky='nsew')
        self.recommendations_frame = tk.Frame(self, bg='lightcoral')
        self.recommendations_frame.grid(row=7, column=0, columnspan=3, sticky='nsew')

        # Initialize draft order efficiently
        self.draft_order = self._generate_draft_order()

        # Initialize list for draft selections
        self.draft_selections = []

        # Create scrollable frames
        self.create_scrollable_frame(self.team_roster_frame)
        self.create_scrollable_frame(self.draft_history_frame)

        # Create Treeview for available players
        self.player_tree = ttk.Treeview(self.available_players_frame, columns=('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'), show='headings', selectmode='browse')
        for col in ('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'):
            self.player_tree.heading(col, text=col)
            self.player_tree.column(col, anchor='w', width=80)
        self.player_tree.grid(row=0, column=0, sticky='nsew')
        self.available_players_frame.grid_rowconfigure(0, weight=1)
        self.available_players_frame.grid_columnconfigure(0, weight=1)

        # Add draft button below Treeview
        self.draft_button = tk.Button(self.available_players_frame, text='DRAFT SELECTED PLAYER', command=self.draft_selected_player)
        self.draft_button.grid(row=1, column=0, sticky='ew', pady=5)

        # Display starting state for dynamic frames
        self.display_static_frames()
        self.display_draft_order()
        self.display_team_roster()
        self.display_available_players()

    def _generate_draft_order(self):
        # Use a single pass to generate draft order, avoid nested loops
        order = []
        team_lookup = {team.draft_position: team.team_name for team in self.my_teams}
        picks = sum(self.my_draft.position_count.values())
        if self.my_draft.drafting_style == 'Standard':
            for _ in range(picks):
                for i in range(1, self.my_draft.num_teams + 1):
                    order.append(team_lookup[i])
        elif self.my_draft.drafting_style == 'Snake':
            forward = True
            for _ in range(picks):
                rng = range(1, self.my_draft.num_teams + 1) if forward else range(self.my_draft.num_teams, 0, -1)
                for i in rng:
                    order.append(team_lookup[i])
                forward = not forward
        return order

    def create_scrollable_frame(self, frame):
        # Unchanged, but only create scrollable frames once
        canvas = tk.Canvas(frame, bg='lightyellow')
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=0)
        scrollable_frame = tk.Frame(canvas, bg='lightgrey')
        scrollable_frame.grid(row=0, column=0, sticky='nsew')
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas_window, width=e.width))
        if frame == self.team_roster_frame:
            self.team_roster_scrollable_frame = scrollable_frame
        elif frame == self.available_players_frame:
            self.available_players_scrollable_frame = scrollable_frame
        elif frame == self.draft_history_frame:
            self.draft_history_scrollable_frame = scrollable_frame

    def display_static_frames(self):
        # Configure title frame and create label
        self.title_frame.grid_columnconfigure(0, weight = 1)
        title_label = tk.Label(self.title_frame, text = 'Draft Board', font = ('Arial', 12))
        title_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Configure team roster title frame and create label
        self.team_roster_title_frame.grid_columnconfigure(0, weight = 1)
        team_roster_title_label = tk.Label(self.team_roster_title_frame, text = 'Team Roster', font = ('Arial', 12))
        team_roster_title_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Configure player filters frame and create buttons
        filter_texts = ['All', 'QB', 'RB', 'WR', 'TE', 'K', 'D/ST']
        filter_commands = [self.show_all, self.show_qbs, self.show_rbs, self.show_wrs, self.show_tes, self.show_ks, self.show_dsts]
        for i in range(7):
            self.player_filters_frame.grid_columnconfigure(i, weight = 1)
            tk.Button(self.player_filters_frame, text = filter_texts[i], font = ('Arial', 8), command = filter_commands[i]).grid(row = 0, column = i, padx = 2, pady = 5, sticky = 'nsew')

        # Configure draft history title frame and create label
        self.draft_history_title_frame.grid_columnconfigure(0, weight = 1)
        draft_history_title_label = tk.Label(self.draft_history_title_frame, text = 'Draft History', font = ('Arial', 12))
        draft_history_title_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Configure team name frame and create label
        self.team_name_frame.grid_columnconfigure(0, weight = 1)
        team_name_label = tk.Label(self.team_name_frame, text = 'My Team Name', font = ('Arial', 8))
        team_name_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Configure column titles frame and create labels
        column_texts = ['Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP', '']
        for i in range(7):
            self.column_titles_frame.grid_columnconfigure(i, weight = 1)
            tk.Label(self.column_titles_frame, text = column_texts[i], anchor = 'w', font = ('Arial', 8)).grid(row = 0, column = i, sticky = 'nsew')

        # Configure league name frame and create label
        self.league_name_frame.grid_columnconfigure(0, weight = 1)
        league_name_label = tk.Label(self.league_name_frame, text = 'My League Name', font = ('Arial', 8))
        league_name_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Create recommendations title frame and create label
        self.recommendations_title_frame.grid_columnconfigure(0, weight = 1)
        recommendations_title_label = tk.Label(self.recommendations_title_frame, text = 'Recommendations', font = ('Arial', 12))
        recommendations_title_label.grid(row = 0, column = 0, sticky = 'nsew')

        # Create recommendations round frame and create labels
        recommendation_texts = ['Recommended Pick', 'Predicted Availability Next Pick', 'Predicted Availability in Two Picks']
        for i in range(3):
            self.recommendations_round_frame.grid_columnconfigure(i, weight = 1)
            tk.Label(self.recommendations_round_frame, text = recommendation_texts[i], font = ('Arial', 8)).grid(row = 0, column = i, sticky = 'nsew')

    def display_draft_order(self):
        # Clear widgets efficiently
        for widget in self.draft_order_frame.winfo_children():
            widget.destroy()
        self.draft_order_frame.grid_columnconfigure(0, weight=1)
        for i in range(1, self.my_draft.num_teams + 2):
            self.draft_order_frame.grid_columnconfigure(i, weight=1)
        for i, team_name in enumerate(self.draft_order[:self.my_draft.num_teams]):
            tk.Label(self.draft_order_frame, text=team_name, font=('Arial', 8)).grid(row=0, column=i+1, padx=5, pady=10, sticky='nsew')

    def display_team_roster(self):
        # Clear any existing widgets in the frame
        for widget in self.team_roster_scrollable_frame.winfo_children():
            widget.destroy()

        # Configure the grid to ensure labels expand as needed
        self.team_roster_scrollable_frame.grid_columnconfigure(0, weight = 1)

        # Get the current drafting team
        current_team_name = self.draft_order[0]
        for team in self.my_teams:
            if team.team_name ==  current_team_name:

                # Track which positions have already been labeled
                labeled_positions = set()
                labeled_players = set()
                filled_positions = []
                row = 0

                # Display the roster in the team roster frame
                for position, count in self.my_draft.position_count.items():
                    # Create a label for the position only once
                    if position not in labeled_positions:
                        position_label = tk.Label(self.team_roster_scrollable_frame, text = position, anchor = 'w', font = ('Arial', 8))
                        position_label.grid(row = row, column = 0, sticky = 'ew', padx = 5, pady = 2)
                        labeled_positions.add(position)
                        row += 1

                    # Create labels for the players
                    for _ in range(count):
                        player_name = ''
                        for player in team.roster:
                            if position in player[5] and player[2] not in labeled_players:
                                player_name = player[2]
                                labeled_players.add(player_name)
                                filled_positions.append(position)
                                break
                            elif position == 'Flex' and player[2] not in labeled_players:
                                rb_count = filled_positions.count('RB')
                                wr_count = filled_positions.count('WR')
                                te_count = filled_positions.count('TE')
                                if 'RB' in player[5] and rb_count == self.my_draft.position_count['RB'] and self.my_draft.position_count['Flex'] >= 1:
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'WR' in player[5] and wr_count == self.my_draft.position_count['WR'] and self.my_draft.position_count['Flex'] >= 1:
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'TE' in player[5] and te_count == self.my_draft.position_count['TE'] and self.my_draft.position_count['Flex'] >= 1:
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                            elif position == 'Bench' and player[2] not in labeled_players:
                                qb_count = filled_positions.count('QB')
                                rb_count = filled_positions.count('RB')
                                wr_count = filled_positions.count('WR')
                                te_count = filled_positions.count('TE')
                                flex_count = filled_positions.count('Flex')
                                k_count = filled_positions.count('K')
                                dst_count = filled_positions.count('DST')
                                if (('QB' in player[5] and qb_count == self.my_draft.position_count['QB']) or ('RB' in player[5] and rb_count == self.my_draft.position_count['RB'] and flex_count == self.my_draft.position_count['Flex'])
                                    or ('WR' in player[5] and wr_count == self.my_draft.position_count['WR'] and flex_count == self.my_draft.position_count['Flex'])
                                    or ('TE' in player[5] and te_count == self.my_draft.position_count['TE'] and flex_count == self.my_draft.position_count['Flex'])
                                    or (('RB' in player[5] or 'WR' in player[5] or 'TE' in player[5]) and flex_count == self.my_draft.position_count['Flex'])
                                    or ('K' in player[5] and k_count == self.my_draft.position_count['K']) or ('DST' in player[5] and dst_count == self.my_draft.position_count['DST'])):
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break

                        # Create label for the player name (empty if not drafted yet)
                        player_name_label = tk.Label(self.team_roster_scrollable_frame, text = player_name, anchor = 'w', font = ('Arial', 8))
                        player_name_label.grid(row = row, column = 0, sticky = 'ew', padx = 5, pady = 2)

                        # Increment row to move to the next position/player
                        row += 1

                break

    def display_available_players(self):
        # Update Treeview instead of recreating widgets
        self.player_tree.delete(*self.player_tree.get_children())
        for player in self.my_player_board.players:
            self.player_tree.insert('', 'end', values=(player[1], player[2], player[3], player[4], player[5], player[13]))

    def draft_selected_player(self):
        selected = self.player_tree.selection()
        if not selected:
            return
        player_values = self.player_tree.item(selected[0])['values']
        # Find player in database using name, team, position
        player = self.my_db_table.find_player(player_values[1], player_values[2], player_values[4])
        if not player:
            return
        player_id = player[0]
        drafting_team_name = self.draft_order[0]
        for team in self.my_teams:
            if team.team_name == drafting_team_name:
                team.draft_player(player_id)
                self.draft_selections.append([team.team_name, player[0], player[2]])
                break
        del self.draft_order[0]
        self.my_player_board = PlayerBoard(self.my_db_table)
        my_sim = Simulation(self.my_teams, self.my_player_board, self.draft_order)
        self.recommended_player = my_sim.recommend_player(self.my_player_board.players, self.draft_order[0])
        recommended_future_players = my_sim.recommend_future_players()
        self.recommended_players_next_round = recommended_future_players[0]
        self.recommended_players_two_rounds = recommended_future_players[1]
        self.display_draft_order()
        self.display_team_roster()
        self.display_available_players()
        self.display_draft_history()
        self.display_recommendations()

    def display_draft_history(self):
        # Clear any existing widgets in the frame
        for widget in self.draft_history_scrollable_frame.winfo_children():
            widget.destroy()

        # Configure the grid and initialize row
        self.draft_history_scrollable_frame.grid_columnconfigure(0, weight = 1)
        num_rows = len(self.draft_selections)
        rows = list(range(num_rows, 0 ,-1))
        i = 0

        # Create a frame for each selection
        for selection in reversed(self.draft_selections):
            selection_frame = tk.Frame(self.draft_history_scrollable_frame, bg = 'lightgrey', pady = 2)
            selection_frame.grid(row = i, column = 0, sticky = 'nsew')

            # Configure columns for selection frame
            selection_frame.grid_columnconfigure(0, weight = 1)
            selection_frame.grid_columnconfigure(1, weight = 1)
            selection_frame.grid_columnconfigure(2, weight = 1)
            selection_frame.grid_columnconfigure(3, weight = 1)

            # Create pick number label
            pick_number = tk.Label(selection_frame, text = str(rows[i]), anchor = 'w', font = ('Arial', 8))
            pick_number.grid(row = 0, column = 0, sticky = 'nsew')

            # Create team name label
            team_name_label = tk.Label(selection_frame, text = selection[0], anchor = 'w', font = ('Arial', 8))
            team_name_label.grid(row = 0, column = 1, sticky = 'nsew')

            # Create selected label
            selected_label = tk.Label(selection_frame, text = 'selected', anchor = 'w', font = ('Arial', 8))
            selected_label.grid(row = 0, column = 2, sticky = 'nsew')

            # Create player name label
            player_name_label = tk.Label(selection_frame, text = selection[2], anchor = 'w', font = ('Arial', 8))
            player_name_label.grid(row = 0, column = 3, sticky = 'nsew')

            i += 1

    def display_recommendations(self):
        # Clear any existing widgets in the frame
        for widget in self.recommendations_frame.winfo_children():
            widget.destroy()

        for i in range(3):
            self.recommendations_frame.grid_columnconfigure(i, weight = 1)
            if i == 0:
                recommended_player = tk.Label(self.recommendations_frame, text = self.recommended_player[2], font = ('Arial', 8))
                recommended_player.grid(row = 0, column = 0, sticky = 'nsew')
            elif i == 1:
                recommended_next_round_1 = tk.Label(self.recommendations_frame, text = self.recommended_players_next_round[0][2], font = ('Arial', 8))
                recommended_next_round_1.grid(row = 0, column = 1, sticky = 'nsew')
                recommended_next_round_2 = tk.Label(self.recommendations_frame, text = self.recommended_players_next_round[1][2], font = ('Arial', 8))
                recommended_next_round_2.grid(row = 1, column = 1, sticky = 'nsew')
                recommended_next_round_3 = tk.Label(self.recommendations_frame, text = self.recommended_players_next_round[2][2], font = ('Arial', 8))
                recommended_next_round_3.grid(row = 2, column = 1, sticky = 'nsew')
                recommended_next_round_4 = tk.Label(self.recommendations_frame, text = self.recommended_players_next_round[3][2], font = ('Arial', 8))
                recommended_next_round_4.grid(row = 3, column = 1, sticky = 'nsew')
                recommended_next_round_5 = tk.Label(self.recommendations_frame, text = self.recommended_players_next_round[4][2], font = ('Arial', 8))
                recommended_next_round_5.grid(row = 4, column = 1, sticky = 'nsew')
            elif i == 2:
                recommended_two_rounds_1 = tk.Label(self.recommendations_frame, text = self.recommended_players_two_rounds[0][2], font = ('Arial', 8))
                recommended_two_rounds_1.grid(row = 0, column = 2, sticky = 'nsew')
                recommended_two_rounds_2 = tk.Label(self.recommendations_frame, text = self.recommended_players_two_rounds[1][2], font = ('Arial', 8))
                recommended_two_rounds_2.grid(row = 1, column = 2, sticky = 'nsew')
                recommended_two_rounds_3 = tk.Label(self.recommendations_frame, text = self.recommended_players_two_rounds[2][2], font = ('Arial', 8))
                recommended_two_rounds_3.grid(row = 2, column = 2, sticky = 'nsew')
                recommended_two_rounds_4 = tk.Label(self.recommendations_frame, text = self.recommended_players_two_rounds[3][2], font = ('Arial', 8))
                recommended_two_rounds_4.grid(row = 3, column = 2, sticky = 'nsew')
                recommended_two_rounds_5 = tk.Label(self.recommendations_frame, text = self.recommended_players_two_rounds[4][2], font = ('Arial', 8))
                recommended_two_rounds_5.grid(row = 4, column = 2, sticky = 'nsew')

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

    def draft_player(self, player_frame):
        # Identify which team is drafting from draft order list
        drafting_team_name = self.draft_order[0]
        # Identify which player frame contians the draft button that was pressed
        player_data = player_frame.winfo_children()
        # Use player data from player frame to fetch player from database
        player = self.my_db_table.find_player(player_data[1].cget('text'), player_data[2].cget('text'), player_data[4].cget('text'))
        player_id = player[0]
        # Add player to team's roster, remove player from database table, and add selection entry to dict
        for team in self.my_teams:
            if team.team_name == drafting_team_name:
                team.draft_player(player_id)
                self.draft_selections.append([team.team_name, player[0], player[2]])
                break
        # Remove first position of draft order list
        del self.draft_order[0]
        # Recreate PlayerBoard object
        self.my_player_board = PlayerBoard(self.my_db_table)
        # SIMULATIONS
        my_sim = Simulation(self.my_teams, self.my_player_board, self.draft_order)
        self.recommended_player = my_sim.recommend_player(self.my_player_board.players, self.draft_order[0])
        recommended_future_players = my_sim.recommend_future_players()
        self.recommended_players_next_round = recommended_future_players[0]
        self.recommended_players_two_rounds = recommended_future_players[1]
        # Display draft order, team roster, available players, and draft history frames
        self.display_draft_order()
        self.display_team_roster()
        self.display_available_players()
        self.display_draft_history()
        self.display_recommendations()
