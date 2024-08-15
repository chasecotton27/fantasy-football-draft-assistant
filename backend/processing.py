# Logic for processing data
import csv
from backend.database import DatabaseTable

# Define the CSVFile class
class CSVFile:
    def __init__(self, file_path, table_name):
        self.file_path = file_path
        self.table_name = table_name
        self.process_csv()

    # Method to process CSV data and insert all players into a database table
    def process_csv(self):
        db_table = DatabaseTable(self.table_name)

        with open(self.file_path, 'r') as file:
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
                    db_table.insert_player(rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp)

# Define the Player class
# Might need a method for inserting a Player ob
class Player:
    def __init__(self, player_id, db_table):
        self.player_id = player_id
        self.db_table = db_table
        player_data = db_table.fetch_player(player_id)
        (
            self.rank, self.name, self.team, self.bye,
            self.position, self.adp_espn, self.adp_yahoo, self.adp_cbs,
            self.adp_sleeper, self.adp_nfl, self.adp_rtsports, self.avg_adp
        ) = player_data

    # Method to draft a player by removing that player from a database table
    # Not sure if any other logic is needed here
    def draft_player(self):
        self.db_table.remove_player(self.player_id)

    # Method to upgrade a player's rank by updating that player's rank in a database table
    # Need to make sure that I am not relying on a list of Player objects throughout the application workflow, whereas I want to rely on the database instead
    def upgrade_player_rank(self):
        pass

    # Method to downgrade a player's rank by updating that player's rank in a database table
    def downgrade_player_rank(self):
        pass

class Team:
    def __init__(self):
        pass

class League:
    def __init__(self):
        pass
