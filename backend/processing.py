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

                if name == None or rank == None:
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
    def __init__(self, team_name, draft_position, db_table):
        self.team_name = team_name
        self.draft_position = draft_position
        self.db_table = db_table
        self.roster = []

    # Method to draft a player and add them to a team's roster while removing them from a database table
    def draft_player(self, player_id):
        player = self.db_table.fetch_player(player_id)
        self.roster.append(player[0])
        self.db_table.remove_player(player_id)

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
