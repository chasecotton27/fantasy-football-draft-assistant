import tkinter as tk
from tkinter import ttk
from backend.processing import PlayerBoard, generate_draft_order
from backend.recommendations import Simulation

class DraftBoardFrame(tk.Frame):
    def __init__(self, parent, controller, my_draft, my_player_repository, my_csv_file, my_teams):
        super().__init__(parent)
        self.controller = controller
        self.my_draft = my_draft
        self.my_player_repository = my_player_repository
        self.my_csv_file = my_csv_file
        self.my_teams = my_teams

        # Create PlayerBoard object once, reuse for filtering
        self.my_player_board = PlayerBoard(my_player_repository)

        # Available-players filter/search state
        self.current_position_filter = None
        self.current_search_text = ''

        # Snapshot of the most recent pick, for single-level undo
        self.last_action = None

        # Configure rows and columns for main frame (unchanged)
        for i in range(8):
            self.grid_rowconfigure(i, weight=1 if i == 4 else 0)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1 if i == 1 else 1)

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
        self.draft_order = generate_draft_order(self.my_teams, self.my_draft)

        # Initialize list for draft selections
        self.draft_selections = []

        # Create Treeview for available players
        self.player_tree = ttk.Treeview(self.available_players_frame, columns=('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'), show='headings', selectmode='browse')
        for col in ('Rank', 'Name', 'Team', 'Bye', 'Position', 'Avg ADP'):
            if col == 'Name':
                self.player_tree.heading(col, text=col, anchor='w')
                self.player_tree.column(col, anchor='w', width=180)
            else:
                self.player_tree.heading(col, text=col, anchor='center')
                self.player_tree.column(col, anchor='center', width=60)
        self.player_tree.grid(row=0, column=0, sticky='nsew')
        self.available_players_frame.grid_rowconfigure(0, weight=1)
        self.available_players_frame.grid_columnconfigure(0, weight=1)

        # Add draft and undo buttons below Treeview
        self.draft_button = tk.Button(self.available_players_frame, text='DRAFT SELECTED PLAYER', command=self.draft_selected_player, bg="#bcbcbc")
        self.draft_button.grid(row=1, column=0, sticky='ew', pady=5)
        self.undo_button = tk.Button(self.available_players_frame, text='UNDO LAST PICK', command=self.undo_last_pick, bg="#bcbcbc", state='disabled')
        self.undo_button.grid(row=2, column=0, sticky='ew', pady=(0, 5))

        # Create Treeview for team roster
        self.team_roster_tree = ttk.Treeview(self.team_roster_frame, columns=('Position', 'Player'), show='headings', selectmode='none')
        self.team_roster_tree.heading('Position', text='Position')
        self.team_roster_tree.heading('Player', text='Player', anchor='w')
        self.team_roster_tree.column('Position', anchor='center', width=80)  # Centered text
        self.team_roster_tree.column('Player', anchor='w', width=120)
        self.team_roster_tree.grid(row=0, column=0, sticky='nsew')
        self.team_roster_frame.grid_rowconfigure(0, weight=1)
        self.team_roster_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview for draft order (horizontal layout with overall pick numbers)
        self.draft_order_tree = ttk.Treeview(
            self.draft_order_frame,
            columns=[f'Team{i+1}' for i in range(self.my_draft.num_teams)],
            show='headings',
            height=1,
            selectmode='none'
        )
        for i in range(self.my_draft.num_teams):
            col_name = f'Team{i+1}'
            self.draft_order_tree.heading(col_name, text=f'Pick {i+1}')  # Will be updated dynamically
            self.draft_order_tree.column(col_name, anchor='center', width=80)
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
        self.draft_history_tree.heading('Team', text='Team', anchor='w')
        self.draft_history_tree.heading('Player', text='Player', anchor='w')
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
            ("All", None),
            ("QB", 'QB'),
            ("RB", 'RB'),
            ("WR", 'WR'),
            ("TE", 'TE'),
            ("K", 'K'),
            ("DST", 'DST'),
        ]
        for i, (label, position_group) in enumerate(filter_buttons):
            btn = tk.Button(self.player_filters_frame, text=label, command=lambda pg=position_group: self.show_position(pg), bg="#bcbcbc")
            btn.grid(row=0, column=i, padx=2, pady=2, sticky='ew')
        self.player_filters_frame.grid_columnconfigure(tuple(range(len(filter_buttons))), weight=1)

        # Add name search, below the filter buttons
        self.search_frame = tk.Frame(self.player_filters_frame)
        self.search_frame.grid(row=1, column=0, columnspan=len(filter_buttons), sticky='ew', pady=(4, 0))
        tk.Label(self.search_frame, text='Search:').pack(side='left', padx=(2, 4))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=2)
        self.search_var.trace_add('write', self._on_search_changed)

    def update_frames_content(self):
        self.display_draft_order()
        self.display_team_roster()
        self.refresh_available_players_display()
        self.display_draft_history()
        self.display_recommendations()

    def display_draft_order(self):
        self.draft_order_tree.delete(*self.draft_order_tree.get_children())
        # Get the teams in draft order for the current round
        team_names = self.draft_order[:self.my_draft.num_teams]
        # Calculate the overall pick number for each team in the current draft order slice
        # The overall pick number is just the index in the full draft_order list + 1
        current_pick_start = len(self.draft_selections)
        pick_numbers = []
        for i in range(self.my_draft.num_teams):
            overall_pick_number = current_pick_start + i + 1
            col_name = f'Team{i+1}'
            self.draft_order_tree.heading(col_name, text=f'{overall_pick_number}')
            pick_numbers.append(overall_pick_number)
        # Insert team names as a single row
        self.draft_order_tree.insert('', 'end', values=tuple(team_names))

    def display_team_roster(self):
        self.team_roster_tree.delete(*self.team_roster_tree.get_children())
        current_team_name = self.draft_order[0] if self.draft_order else None
        for team in self.my_teams:
            if team.team_name == current_team_name:
                position_counts = team.draft.position_count
                filled_positions = []
                labeled_players = set()
                for position, count in position_counts.items():
                    for _ in range(count):
                        player_name = ''
                        for player in team.roster:
                            if position in player.position and player.name not in labeled_players:
                                player_name = player.name
                                labeled_players.add(player_name)
                                filled_positions.append(position)
                                break
                            elif position == 'Flex' and player.name not in labeled_players:
                                rb_count = filled_positions.count('RB')
                                wr_count = filled_positions.count('WR')
                                te_count = filled_positions.count('TE')
                                if 'RB' in player.position and rb_count == team.draft.position_count['RB'] and team.draft.position_count['Flex'] >= 1:
                                    player_name = player.name
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'WR' in player.position and wr_count == team.draft.position_count['WR'] and team.draft.position_count['Flex'] >= 1:
                                    player_name = player.name
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                                elif 'TE' in player.position and te_count == team.draft.position_count['TE'] and team.draft.position_count['Flex'] >= 1:
                                    player_name = player.name
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                            elif position == 'Bench' and player.name not in labeled_players:
                                qb_count = filled_positions.count('QB')
                                rb_count = filled_positions.count('RB')
                                wr_count = filled_positions.count('WR')
                                te_count = filled_positions.count('TE')
                                flex_count = filled_positions.count('Flex')
                                k_count = filled_positions.count('K')
                                dst_count = filled_positions.count('DST')
                                if (('QB' in player.position and qb_count == team.draft.position_count['QB']) or ('RB' in player.position and rb_count == team.draft.position_count['RB'] and flex_count == team.draft.position_count['Flex'])
                                    or ('WR' in player.position and wr_count == team.draft.position_count['WR'] and flex_count == team.draft.position_count['Flex'])
                                    or ('TE' in player.position and te_count == team.draft.position_count['TE'] and flex_count == team.draft.position_count['Flex'])
                                    or (('RB' in player.position or 'WR' in player.position or 'TE' in player.position) and flex_count == team.draft.position_count['Flex'])
                                    or ('K' in player.position and k_count == team.draft.position_count['K']) or ('DST' in player.position and dst_count == team.draft.position_count['DST'])):
                                    player_name = player.name
                                    labeled_players.add(player_name)
                                    filled_positions.append(position)
                                    break
                        self.team_roster_tree.insert('', 'end', values=(position, player_name))
                break

    def refresh_available_players_display(self):
        players = self.my_player_board.filter_by_position(self.current_position_filter)
        if self.current_search_text:
            search_text = self.current_search_text.lower()
            players = [p for p in players if search_text in p.name.lower()]
        self.display_available_players(players)

    def display_available_players(self, players):
        self.player_tree.delete(*self.player_tree.get_children())
        for player in players:
            self.player_tree.insert('', 'end', values=(player.rank, player.name, player.team, player.bye, player.position, player.avg_adp))

    def _recompute_recommendations(self):
        if self.draft_order:
            my_sim = Simulation(self.my_teams, self.my_player_board, self.draft_order)
            self.recommended_player = my_sim.recommend_player_avoiding_cliffs(self.my_player_board.players, self.draft_order[0])
            recommended_future_players = my_sim.recommend_future_players()
            self.recommended_players_next_round = recommended_future_players[0]
            self.recommended_players_two_rounds = recommended_future_players[1]
        else:
            # Draft is complete — nothing left to recommend
            self.recommended_player = None
            self.recommended_players_next_round = []
            self.recommended_players_two_rounds = []

    def draft_selected_player(self):
        selected = self.player_tree.selection()
        if not selected:
            return
        player_values = self.player_tree.item(selected[0])['values']
        player = self.my_player_repository.find_player(player_values[1], player_values[2], player_values[4])
        if not player:
            return
        drafting_team_name = self.draft_order[0]
        for team in self.my_teams:
            if team.team_name == drafting_team_name:
                self.last_action = {
                    'team': team,
                    'player': player,
                    'drafting_team_name': drafting_team_name,
                    'pre_roster': list(team.roster),
                    'pre_filled': list(team.filled_roster_positions),
                    'pre_required': list(team.required_roster_positions),
                }
                team.draft_player(player.player_id)
                self.draft_selections.append([team.team_name, player.player_id, player.name])
                break
        del self.draft_order[0]
        self.my_player_board = PlayerBoard(self.my_player_repository)
        self._recompute_recommendations()
        self.undo_button.config(state='normal')
        self.update_frames_content()

    def undo_last_pick(self):
        if self.last_action is None:
            return
        action = self.last_action
        team = action['team']
        team.roster = action['pre_roster']
        team.filled_roster_positions = action['pre_filled']
        team.required_roster_positions = action['pre_required']
        self.my_player_repository.restore(action['player'])
        self.draft_order.insert(0, action['drafting_team_name'])
        self.draft_selections.pop()
        self.my_player_board = PlayerBoard(self.my_player_repository)
        self._recompute_recommendations()
        self.last_action = None
        self.undo_button.config(state='disabled')
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
        recommended = self.recommended_player.name if self.recommended_player else ''
        # Get lists for next pick and two picks
        next_pick_list = [p.name for p in self.recommended_players_next_round[:5]] if self.recommended_players_next_round else []
        two_picks_list = [p.name for p in self.recommended_players_two_rounds[:5]] if self.recommended_players_two_rounds else []

        # Find the max number of rows needed
        max_rows = max(1, len(next_pick_list), len(two_picks_list))

        for i in range(max_rows):
            rec = recommended if i == 0 else ''
            next_pick = next_pick_list[i] if i < len(next_pick_list) else ''
            two_picks = two_picks_list[i] if i < len(two_picks_list) else ''
            self.recommendations_tree.insert('', 'end', values=(rec, next_pick, two_picks))

    def show_position(self, position_group):
        self.current_position_filter = position_group
        self.refresh_available_players_display()

    def _on_search_changed(self, *args):
        self.current_search_text = self.search_var.get()
        self.refresh_available_players_display()
