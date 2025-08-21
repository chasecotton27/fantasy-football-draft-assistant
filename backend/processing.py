import csv

# Define the Data class
class CSVFile:
    def __init__(self, csv_file_path, db_table):
        self.csv_file_path = csv_file_path
        self.db_table = db_table
        self.add_players_to_db_table()

    # Method to process CSV data and insert all players into a database table
    def add_players_to_db_table(self):
        # Use list to batch insert for speed
        players_to_insert = []
        with open(self.csv_file_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    rank = int(row['Rank'])
                except Exception:
                    rank = None
                name = row.get('Player', None)
                team = row.get('Team', None)
                try:
                    bye = int(row['Bye'])
                except Exception:
                    bye = None
                position = row.get('POS', None)
                try:
                    adp_espn = float(row['ESPN'])
                except Exception:
                    adp_espn = None
                try:
                    adp_yahoo = float(row['Yahoo'])
                except Exception:
                    adp_yahoo = None
                try:
                    adp_cbs = float(row['CBS'])
                except Exception:
                    adp_cbs = None
                try:
                    adp_sleeper = float(row['Sleeper'])
                except Exception:
                    adp_sleeper = None
                try:
                    adp_nfl = float(row['NFL'])
                except Exception:
                    adp_nfl = None
                try:
                    adp_rtsports = float(row['RTSports'])
                except Exception:
                    adp_rtsports = None
                try:
                    adp_fantrax = float(row['Fantrax'])
                except Exception:
                    adp_fantrax = None
                try:
                    avg_adp = float(row['AVG'])
                except Exception:
                    avg_adp = None

                # Only add valid players
                if name and rank:
                    players_to_insert.append((rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp))

        # Batch insert for speed
        if players_to_insert:
            self.db_table.cursor.executemany(
                f'''
                INSERT INTO {self.db_table.table_name} (rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''',
                players_to_insert
            )
            self.db_table.conn.commit()

# Define the Draft class
class Draft:
    def __init__(self, scoring_format, position_count, drafting_style, num_teams):
        self.scoring_format = scoring_format
        self.position_count = position_count
        self.drafting_style = drafting_style
        self.num_teams = num_teams

# Define the Team class
class Team:
    def __init__(self, team_name, draft_position, db_table, draft):
        self.team_name = team_name
        self.draft_position = draft_position
        self.db_table = db_table
        self.draft = draft
        self.roster = []
        self.filled_roster_positions = []
        self.required_roster_positions = []
        
        # Initialize required roster positions list
        for position, count in self.draft.position_count.items():
            self.required_roster_positions.extend([position] * count)

    # Method to draft a player and add them to a team's roster while removing them from a database table
    def draft_player(self, player_id):
        player = self.db_table.fetch_player(player_id)
        self.roster.append(player)
        self.db_table.remove_player(player_id)

        # Determine which position from the team's roster was just drafted
        drafted_player = self.roster[-1]
        player_position_rank = drafted_player[5]
        player_position = ''.join([char for char in player_position_rank if char.isalpha()])

        # Update filled roster positions
        self.filled_roster_positions.append(player_position)

        # Update required roster positions
        if player_position in self.required_roster_positions:
            self.required_roster_positions.remove(player_position)
        elif player_position == 'RB' and player_position not in self.required_roster_positions and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        elif player_position == 'WR' and player_position not in self.required_roster_positions and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        elif player_position == 'TE' and player_position not in self.required_roster_positions and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        else:
            self.required_roster_positions.remove('Bench')

# Define the PlayerBoard class
class PlayerBoard:
    def __init__(self, db_table):
        self.db_table = db_table
        self.players = []
        self.player_count = 0
        self.filter_all_players()

    # Method to erase a player board before fetching from a database table and repopulating a player board
    def erase_player_board(self):
        self.players = []

    # Method to populate a player board with all players from a database table
    def filter_all_players(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_all_players()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all QBs from a database table
    def filter_qbs(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_qbs()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all RBs from a database table
    def filter_rbs(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_rbs()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all WRs from a database table
    def filter_wrs(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_wrs()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all TEs from a database table
    def filter_tes(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_tes()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all Ks from a database table
    def filter_ks(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_ks()
        self.player_count = len(self.players)
        return self.players

    # Method to populate a player board with all DSTs from a database table
    def filter_dsts(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_dsts()
        self.player_count = len(self.players)
        return self.players
