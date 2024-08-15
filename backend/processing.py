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
    def __init__(self):
        self.scoring_format = self.set_scoring_format()
        self.position_count = self.set_position_count()
        self.drafting_style = self.set_drafting_style()

    # Method to set the scoring format for the league
    def set_scoring_format(self):
        scoring_format_enum = input('What is the scoring format for this league?\n\n1) Standard\n2) Half PPR\n3) Full PPR\n\nScoring format (1, 2, or 3): ')

        if int(scoring_format_enum) == 1:
            scoring_format = 'Standard'
        elif int(scoring_format_enum) == 2:
            scoring_format = 'Half PPR'
        elif int(scoring_format_enum) == 3:
            scoring_format = 'Full PPR'

        return scoring_format

    # Method to set the position count for each team
    def set_position_count(self):
        print('How many players for each position are on a team?\n')
        qb = int(input('Quarterbacks: '))
        rb = int(input('Running backs: '))
        wr = int(input('Wide receivers: '))
        te = int(input('Tight ends: '))
        flex = int(input('Flex positions: '))
        k = int(input('Kickers: '))
        dst = int(input('Defense and special teams: '))
        bench = int(input('Bench positions: '))

        position_count = {
            'Quarterbacks': qb,
            'Running backs': rb,
            'Wide receivers': wr,
            'Tight ends': te,
            'Flex positions': flex,
            'Kickers': k,
            'Defense and special teams:': dst,
            'Bench positions': bench
        }

        return position_count

    # Method to set the drafting style for the draft
    def set_drafting_style(self):
        drafting_style_enum = input('What is the drafting style for this league?\n\n1) Standard\n2) Snake\n\nDrafting style (1 or 2): ')

        if int(drafting_style_enum) == 1:
            drafting_style = 'Standard'
        elif int(drafting_style_enum) == 2:
            drafting_style = 'Snake'

        return drafting_style

# Define the Team class
class Team:
    def __init__(self):
        pass

    def create_team(self):
        pass

    def delete_team(self):
        pass

    def draft_player(self):
        pass

# Define the PlayerBoard class
class PlayerBoard:
    def __init__(self, db_table):
        self.db_table = db_table
        self.players = []
        self.player_count = len(self.players)

    # Method to erase a player board before fetching from a database table and repopulating a player board
    def erase_player_board(self):
        self.players = []

    # Method to populate a player board with all players from a database table
    def filter_all_players(self):
        self.erase_player_board()
        self.players = self.db_table.fetch_all_players()
        self.player_count = len(self.players)

        return self.players

    # Method to populate a player board with a specific player from a database table
    def filter_player(self, player_id):
        self.erase_player_board()
        self.players = self.db_table.fetch_player(player_id)
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

    # Method to populate a player board with all players on a specific team from a database table
    def filter_players_from_team(self, team):
        self.erase_player_board()
        self.players = self.db_table.fetch_players_from_team(team)
        self.player_count = len(self.players)

        return self.players

    # Method to populate a player board with all players with a specific bye week from a database table
    def filter_players_with_bye(self, bye):
        self.erase_player_board()
        self.players = self.db_table.fetch_players_with_bye(bye)
        self.player_count = len(self.players)

        return self.players

# Define the Player class
class Player:
    def __init__(self, player_id, db_table):
        player_data = db_table.fetch_player(player_id)
        (
            self.player_id, self.rank, self.name, self.team, self.bye,
            self.position, self.adp_espn, self.adp_yahoo, self.adp_cbs,
            self.adp_sleeper, self.adp_nfl, self.adp_rtsports, self.avg_adp
        ) = player_data
