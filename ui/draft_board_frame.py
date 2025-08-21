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
        self.title_frame = tk.Frame(self)
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')
        self.draft_order_frame = tk.Frame(self)
        self.draft_order_frame.grid(row=1, column=0, columnspan=3, sticky='nsew')
        self.team_roster_title_frame = tk.Frame(self)
        self.team_roster_title_frame.grid(row=2, column=0, sticky='nsew')
        self.player_filters_frame = tk.Frame(self)
        self.player_filters_frame.grid(row=2, column=1, sticky='nsew')
        self.draft_history_title_frame = tk.Frame(self)
        self.draft_history_title_frame.grid(row=2, column=2, sticky='nsew')
        self.team_name_frame = tk.Frame(self)
        self.team_name_frame.grid(row=3, column=0, sticky='nsew')
        self.column_titles_frame = tk.Frame(self)
        self.column_titles_frame.grid(row=3, column=1, sticky='nsew')
        self.league_name_frame = tk.Frame(self)
        self.league_name_frame.grid(row=3, column=2, sticky='nsew')
        self.team_roster_frame = tk.Frame(self, width=300)
        self.team_roster_frame.grid(row=4, column=0, sticky='nsew')
        self.available_players_frame = tk.Frame(self, width=600)
        self.available_players_frame.grid(row=4, column=1, sticky='nsew')
        self.draft_history_frame = tk.Frame(self, width=300)
        self.draft_history_frame.grid(row=4, column=2, sticky='nsew')
        self.recommendations_title_frame = tk.Frame(self)
        self.recommendations_title_frame.grid(row=5, column=0, columnspan=3, sticky='nsew')
        self.recommendations_round_frame = tk.Frame(self)
        self.recommendations_round_frame.grid(row=6, column=0, columnspan=3, sticky='nsew')
        self.recommendations_frame = tk.Frame(self)
        self.recommendations_frame.grid(row=7, column=0, columnspan=3, sticky='nsew')

        # Initialize draft order efficiently
        self.draft_order = self._generate_draft_order()

        # Initialize list for draft selections
        self.draft_selections = []

        # Create Treeview for available players
        self.player_tree = ttk.Treeview(self.available_players_frame, columns=('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'), show='headings', selectmode='browse')
        for col in ('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'):
            self.player_tree.heading(col, text=col)
            if col == 'Name':
                self.player_tree.column(col, anchor='w', width=180)
            else:
                self.player_tree.column(col, anchor='center', width=60)
        self.player_tree.grid(row=0, column=0, sticky='nsew')
        self.available_players_frame.grid_rowconfigure(0, weight=1)
        self.available_players_frame.grid_columnconfigure(0, weight=1)

        # Add draft button below Treeview
        self.draft_button = tk.Button(self.available_players_frame, text='DRAFT SELECTED PLAYER', command=self.draft_selected_player, bg="#bcbcbc")
        self.draft_button.grid(row=1, column=0, sticky='ew', pady=5)

        # Create Treeview for team roster
        self.team_roster_tree = ttk.Treeview(self.team_roster_frame, columns=('Position', 'Player'), show='headings', selectmode='none')
        self.team_roster_tree.heading('Position', text='Position')
        self.team_roster_tree.heading('Player', text='Player')
        self.team_roster_tree.column('Position', anchor='center', width=80)  # Centered text
        self.team_roster_tree.column('Player', anchor='w', width=120)
        self.team_roster_tree.grid(row=0, column=0, sticky='nsew')
        self.team_roster_frame.grid_rowconfigure(0, weight=1)
        self.team_roster_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview for draft order (horizontal layout)
        self.draft_order_tree = ttk.Treeview(self.draft_order_frame, columns=[f'Team{i+1}' for i in range(self.my_draft.num_teams)], show='headings', height=1, selectmode='none')
        for i in range(self.my_draft.num_teams):
            col_name = f'Team{i+1}'
            self.draft_order_tree.heading(col_name, text=f'Team {i+1}')
            self.draft_order_tree.column(col_name, anchor='center', width=120)
        self.draft_order_tree.grid(row=0, column=0, sticky='nsew')
        self.draft_order_frame.grid_rowconfigure(0, weight=1)
        self.draft_order_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview for recommendations (vertical stacking for player names)
        self.recommendations_tree = ttk.Treeview(
            self.recommendations_frame,
            columns=('Recommended', 'Next Pick', 'Two Picks'),
            show='headings',
            selectmode='none',
            height=6
        )
        self.recommendations_tree.heading('Recommended', text='Recommended Pick')
        self.recommendations_tree.heading('Next Pick', text='Predicted Availability Next Pick')
        self.recommendations_tree.heading('Two Picks', text='Predicted Availability in Two Picks')
        self.recommendations_tree.column('Recommended', anchor='center', width=120)
        self.recommendations_tree.column('Next Pick', anchor='center', width=180)
        self.recommendations_tree.column('Two Picks', anchor='center', width=180)
        self.recommendations_tree.grid(row=0, column=0, sticky='nsew')
        self.recommendations_frame.grid_rowconfigure(0, weight=1)
        self.recommendations_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview for draft history
        self.draft_history_tree = ttk.Treeview(self.draft_history_frame, columns=('Pick', 'Team', 'Player'), show='headings', selectmode='none')
        self.draft_history_tree.heading('Pick', text='Pick')
        self.draft_history_tree.heading('Team', text='Team')
        self.draft_history_tree.heading('Player', text='Player')
        self.draft_history_tree.column('Pick', anchor='center', width=30)
        self.draft_history_tree.column('Team', anchor='w', width=120)
        self.draft_history_tree.column('Player', anchor='w', width=120)
        self.draft_history_tree.grid(row=0, column=0, sticky='nsew')
        self.draft_history_frame.grid_rowconfigure(0, weight=1)
        self.draft_history_frame.grid_columnconfigure(0, weight=1)

        # Initialize recommendation attributes to avoid AttributeError
        self.recommended_player = None
        self.recommended_players_next_round = []
        self.recommended_players_two_rounds = []

        # Initialize frames content
        self.update_frames_content()

        # Add filter buttons for available players
        filter_buttons = [
            ("All", self.show_all),
            ("QB", self.show_qbs),
            ("RB", self.show_rbs),
            ("WR", self.show_wrs),
            ("TE", self.show_tes),
            ("K", self.show_ks),
            ("DST", self.show_dsts)
        ]
        for i, (label, command) in enumerate(filter_buttons):
            btn = tk.Button(self.player_filters_frame, text=label, command=command, bg="#bcbcbc")
            btn.grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        self.player_filters_frame.grid_columnconfigure(tuple(range(len(filter_buttons))), weight=1)

    def _generate_draft_order(self):
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

    def update_frames_content(self):
        self.display_draft_order()
        self.display_team_roster()
        self.display_available_players()
        self.display_draft_history()
        self.display_recommendations()

    def display_draft_order(self):
        self.draft_order_tree.delete(*self.draft_order_tree.get_children())
        # Lay out team names horizontally in a single row
        team_names = self.draft_order[:self.my_draft.num_teams]
        values = tuple(team_names)
        self.draft_order_tree.insert('', 'end', values=values)

    def display_team_roster(self):
        self.team_roster_tree.delete(*self.team_roster_tree.get_children())
        current_team_name = self.draft_order[0]
        for team in self.my_teams:
            if team.team_name == current_team_name:
                position_counts = team.draft.position_count
                filled_positions = []
                labeled_players = set()
                for position, count in position_counts.items():
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
                                if 'RB' in player[5] and rb_count == team.draft.position_count['RB'] and team.draft.position_count['Flex'] >= 1:
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'WR' in player[5] and wr_count == team.draft.position_count['WR'] and team.draft.position_count['Flex'] >= 1:
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'TE' in player[5] and te_count == team.draft.position_count['TE'] and team.draft.position_count['Flex'] >= 1:
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
                                if (('QB' in player[5] and qb_count == team.draft.position_count['QB']) or ('RB' in player[5] and rb_count == team.draft.position_count['RB'] and flex_count == team.draft.position_count['Flex'])
                                    or ('WR' in player[5] and wr_count == team.draft.position_count['WR'] and flex_count == team.draft.position_count['Flex'])
                                    or ('TE' in player[5] and te_count == team.draft.position_count['TE'] and flex_count == team.draft.position_count['Flex'])
                                    or (('RB' in player[5] or 'WR' in player[5] or 'TE' in player[5]) and flex_count == team.draft.position_count['Flex'])
                                    or ('K' in player[5] and k_count == team.draft.position_count['K']) or ('DST' in player[5] and dst_count == team.draft.position_count['DST'])):
                                    player_name = player[2]
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                        self.team_roster_tree.insert('', 'end', values=(position, player_name))
                break

    def display_available_players(self):
        self.player_tree.delete(*self.player_tree.get_children())
        for player in self.my_player_board.players:
            self.player_tree.insert('', 'end', values=(player[1], player[2], player[3], player[4], player[5], player[13]))

    def draft_selected_player(self):
        selected = self.player_tree.selection()
        if not selected:
            return
        player_values = self.player_tree.item(selected[0])['values']
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
        self.update_frames_content()

    def display_draft_history(self):
        self.draft_history_tree.delete(*self.draft_history_tree.get_children())
        num_rows = len(self.draft_selections)
        rows = list(range(num_rows, 0, -1))
        for i, selection in enumerate(reversed(self.draft_selections)):
            pick_number = str(rows[i])
            team_name = selection[0]
            player_name = selection[2]
            self.draft_history_tree.insert('', 'end', values=(pick_number, team_name, player_name))

    def display_recommendations(self):
        self.recommendations_tree.delete(*self.recommendations_tree.get_children())
        # Recommended pick
        recommended = self.recommended_player[2] if self.recommended_player else ''
        # Get lists for next pick and two picks
        next_pick_list = [p[2] for p in self.recommended_players_next_round[:5]] if self.recommended_players_next_round else []
        two_picks_list = [p[2] for p in self.recommended_players_two_rounds[:5]] if self.recommended_players_two_rounds else []

        # Find the max number of rows needed
        max_rows = max(1, len(next_pick_list), len(two_picks_list))

        for i in range(max_rows):
            rec = recommended if i == 0 else ''
            next_pick = next_pick_list[i] if i < len(next_pick_list) else ''
            two_picks = two_picks_list[i] if i < len(two_picks_list) else ''
            self.recommendations_tree.insert('', 'end', values=(rec, next_pick, two_picks))

    def show_all(self):
        self.my_player_board.players = self.my_player_board.filter_all_players()
        self.display_available_players()

    def show_qbs(self):
        self.my_player_board.players = self.my_player_board.filter_qbs()
        self.display_available_players()

    def show_rbs(self):
        self.my_player_board.players = self.my_player_board.filter_rbs()
        self.display_available_players()

    def show_wrs(self):
        self.my_player_board.players = self.my_player_board.filter_wrs()
        self.display_available_players()

    def show_tes(self):
        self.my_player_board.players = self.my_player_board.filter_tes()
        self.display_available_players()

    def show_ks(self):
        self.my_player_board.players = self.my_player_board.filter_ks()
        self.display_available_players()

    def show_dsts(self):
        self.my_player_board.players = self.my_player_board.filter_dsts()
        self.display_available_players()
