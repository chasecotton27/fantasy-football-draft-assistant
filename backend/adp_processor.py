# Logic for processing ADP data
import csv

# Define the Player class
class Player:
    def __init__(self, rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp):
        self.rank = rank
        self.name = name
        self.team = team
        self.bye = bye
        self.position = position
        self.adp_espn = adp_espn
        self.adp_yahoo = adp_yahoo
        self.adp_cbs = adp_cbs
        self.adp_sleeper = adp_sleeper
        self.adp_nfl = adp_nfl
        self.adp_rtsports = adp_rtsports
        self.avg_adp = avg_adp

    # Method to convert Player object to dictionary for database insertion
    def to_dict(self):
        return {
            'rank': self.rank,
            'name': self.name,
            'team': self.team,
            'bye': self.bye,
            'position': self.position,
            'adp_espn': self.adp_espn,
            'adp_yahoo': self.adp_yahoo,
            'adp_cbs': self.adp_cbs,
            'adp_sleeper': self.adp_sleeper,
            'adp_nfl': self.adp_nfl,
            'adp_rtsports': self.adp_rtsports,
            'avg_adp': self.avg_adp
        }

# Function to process CSV data, add players to the database, and return a list of Player objects
def process_csv(file_path, db_table):
    players = []

    with open(file_path, 'r') as file:
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

            player = Player(
                rank = rank,
                name = name,
                team = team,
                bye = bye,
                position = position,
                adp_espn = adp_espn,
                adp_yahoo = adp_yahoo,
                adp_cbs = adp_cbs,
                adp_sleeper  =adp_sleeper,
                adp_nfl = adp_nfl,
                adp_rtsports = adp_rtsports,
                avg_adp = avg_adp
            )

            players.append(player)
            store_player_in_db(player, db_table)

    return players

# Function to insert one player into a database table
def store_player_in_db(player, db_table):
    db_table.insert_player(
        rank = player.rank,
        name = player.name,
        team = player.team,
        bye = player.bye,
        position = player.position,
        adp_espn = player.adp_espn,
        adp_yahoo = player.adp_yahoo,
        adp_cbs = player.adp_cbs,
        adp_sleeper = player.adp_sleeper,
        adp_nfl = player.adp_nfl,
        adp_rtsports = player.adp_rtsports,
        avg_adp = player.avg_adp
    )

# Function to insert all players into a database table
def store_all_players_in_db(players, db_table):
    for player in players:
        db_table.insert_player(
            rank = player.rank,
            name = player.name,
            team = player.team,
            bye = player.bye,
            position = player.position,
            adp_espn = player.adp_espn,
            adp_yahoo = player.adp_yahoo,
            adp_cbs = player.adp_cbs,
            adp_sleeper = player.adp_sleeper,
            adp_nfl = player.adp_nfl,
            adp_rtsports = player.adp_rtsports,
            avg_adp = player.avg_adp
        )
