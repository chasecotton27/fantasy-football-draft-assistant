# Logic for processing ADP data
import csv

# Define the Player class
class Player:
    def __init__(self, name, rank, team, bye, position, adp_espn, adp_sleeper, adp_nfl, adp_rtsports, avg_adp):
        self.name = name
        self.rank = rank
        self.team = team
        self.bye = bye
        self.position = position
        self.adp_espn = adp_espn
        self.adp_sleeper = adp_sleeper
        self.adp_nfl = adp_nfl
        self.adp_rtsports = adp_rtsports
        self.avg_adp = avg_adp

    # Convert player object to dictionary for database insertion
    def to_dict(self):
        return {
            "name": self.name,
            "rank": self.rank,
            "team": self.team,
            "bye": self.bye,
            "position": self.position,
            "adp_espn": self.adp_espn,
            "adp_sleeper": self.adp_sleeper,
            "adp_nfl": self.adp_nfl,
            "adp_rtsports": self.adp_rtsports,
            "avg_adp": self.avg_adp
        }

# Function to process CSV data and return a list of Player objects and dict objects
def process_csv(file_path):
    players = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            player = Player(
                name=row['Player'],
                rank=row['Rank'],
                team=row['Team'],
                bye=row['Bye'],
                position=row['POS'],
                adp_espn=row['ESPN'],
                adp_sleeper=row['Sleeper'],
                adp_nfl=row['NFL'],
                adp_rtsports=row['RTSports'],
                avg_adp=row['AVG']
            )

            try:
                player.rank = int(player.rank)
            except:
                player.rank = 'none'
            try:
                player.bye = int(player.bye)
            except:
                player.bye = 'none'
            try:
                player.adp_espn = float(player.adp_espn)
            except:
                player.adp_espn = 'none'
            try:
                player.adp_sleeper = float(player.adp_sleeper)
            except:
                player.adp_sleeper = 'none'
            try:
                player.adp_nfl = float(player.adp_nfl)
            except:
                player.adp_nfl = 'none'
            try:
                player.adp_rtsports = float(player.adp_rtsports)
            except:
                player.adp_rtsports = 'none'
            try:
                player.avg_adp = float(player.avg_adp)
            except:
                player.avg_adp = 'none'

            players.append(player)

    return players

# Function to insert Player objects into a database table
def store_players_in_db(players, db_table):
    for player in players:
        db_table.insert_player(
            name=player.name,
            rank=player.rank,
            team=player.team,
            bye=player.bye,
            position=player.position,
            adp_espn=player.adp_espn,
            adp_sleeper=player.adp_sleeper,
            adp_nfl=player.adp_nfl,
            adp_rtsports=player.adp_rtsports,
            avg_adp=player.avg_adp
        )
