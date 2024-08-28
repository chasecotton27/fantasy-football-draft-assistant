import csv

# Define the Data class
class CSVFile:
    def __init__(self, csv_file_path, db_table):
        self.csv_file_path = csv_file_path
        self.db_table = db_table
        self.add_players_to_db_table()

    # Method to process CSV data and insert all players into a database table
    def add_players_to_db_table(self):
        with open(self.csv_file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    rank = int(row['Rank'])
                except:
                    rank = None
                try:
                    name = row['Player']
                except:
                    name = None
                try:
                    team = row['Team']
                except:
                    team = None
                try:
                    bye = int(row['Bye'])
                except:
                    bye = None
                try:
                    position = row['POS']
                except:
                    position = None
                try:
                    adp_espn = float(row['ESPN'])
                except:
                    adp_espn = None
                try:
                    adp_yahoo = float(row['Yahoo'])
                except:
                    adp_yahoo = None
                try:
                    adp_cbs = float(row['CBS'])
                except:
                    adp_cbs = None
                try:
                    adp_sleeper = float(row['Sleeper'])
                except:
                    adp_sleeper = None
                try:
                    adp_nfl = float(row['NFL'])
                except:
                    adp_nfl = None
                try:
                    adp_rtsports = float(row['RTSports'])
                except:
                    adp_rtsports = None
                try:
                    avg_adp = float(row['AVG'])
                except:
                    avg_adp = None

                if name == 1 and None or rank == 1 and None:
                    pass
                else:
                    self.db_table.insert_player(rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp)

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
        elif player_position not in self.required_roster_positions and (player_position == 'RB' or player_position == 'WR' or player_position == 'TE') and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')

    def determine_target_positions(self):
        # Check how many players are needed for each position
        qbs_needed = self.required_roster_positions.count('QB')
        rbs_needed = self.required_roster_positions.count('RB')
        wrs_needed = self.required_roster_positions.count('WR')
        tes_needed = self.required_roster_positions.count('TE')
        flexs_needed = self.required_roster_positions.count('Flex')
        ks_needed = self.required_roster_positions.count('K')
        dsts_needed = self.required_roster_positions.count('DST')

        # Initialize target positions list
        target_positions = []

        # Check for any obvious positions that require multiple players
        if qbs_needed >= 2:
            target_positions.append('QB')
        if rbs_needed >= 2:
            target_positions.append('RB')
        elif wrs_needed >=2 and rbs_needed:
            target_positions.append('RB')
        if wrs_needed >= 2:
            target_positions.append('WR')
        elif rbs_needed >= 2 and wrs_needed:
            target_positions.append('WR')
        if tes_needed >= 2:
            target_positions.append('TE')
        if flexs_needed >= 2:
            if 'RB' not in target_positions:
                target_positions.append('RB')
            if 'WR' not in target_positions:
                target_positions.append('WR')
            if 'TE' not in target_positions:
                target_positions.append('TE')
        if ks_needed >= 2:
            target_positions.append('K')
        if dsts_needed >= 2:
            target_positions.append('DST')

        # If there are no obvious positions that need multiple players
        if not target_positions:
            # If equal QBs, RBs, WRs, TEs, and Flexs are needed, then add all
            if qbs_needed == 1 and rbs_needed == 1 and wrs_needed == 1 and tes_needed == 1 and flexs_needed == 1:
                target_positions.append('QB')
                target_positions.append('RB')
                target_positions.append('WR')
                target_positions.append('TE')
            # Check needs in this order: QB -> TE -> RB -> WR -> Flex
            if qbs_needed > rbs_needed or qbs_needed > wrs_needed or qbs_needed > tes_needed or qbs_needed > flexs_needed:
                target_positions.append('QB')
            if tes_needed > qbs_needed or tes_needed > rbs_needed or tes_needed > wrs_needed or tes_needed > flexs_needed:
                target_positions.append('TE')
            if rbs_needed > qbs_needed or rbs_needed > wrs_needed or rbs_needed > tes_needed or rbs_needed > flexs_needed:
                target_positions.append('RB')
            if wrs_needed > qbs_needed or wrs_needed > rbs_needed or wrs_needed > tes_needed or wrs_needed > flexs_needed:
                target_positions.append('WR')
            if qbs_needed and flexs_needed and not rbs_needed and not wrs_needed and not tes_needed:
                if 'QB' not in target_positions:
                    target_positions.append('QB')
            elif flexs_needed > qbs_needed or flexs_needed > rbs_needed or flexs_needed > wrs_needed or flexs_needed > tes_needed:
                if 'RB' not in target_positions and rbs_needed:
                    target_positions.append('RB')
                if 'WR' not in target_positions and wrs_needed:
                    target_positions.append('WR')
                if 'TE' not in target_positions and tes_needed:
                    target_positions.append('TE')
                if not rbs_needed and not wrs_needed and not tes_needed:
                    target_positions.append('RB')
                    target_positions.append('WR')
                    target_positions.append('TE')
            # If starting lineup is filled, then check for K or DST needs
            elif not qbs_needed and not rbs_needed and not wrs_needed and not tes_needed and ks_needed == 1 and dsts_needed == 1:
                target_positions.append('K')
                target_positions.append('DST')
            elif not qbs_needed and not rbs_needed and not wrs_needed and not tes_needed and ks_needed > dsts_needed:
                target_positions.append('K')
            elif not qbs_needed and not rbs_needed and not wrs_needed and not tes_needed and dsts_needed > ks_needed:
                target_positions.append('DST')

        return target_positions

# Define the PlayerBoard class
class PlayerBoard:
    def __init__(self, db_table):
        self.db_table = db_table
        self.players = []
        self.player_count = len(self.players)
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
