import csv
import sys
from pathlib import Path


# Resolve adp-data/ to an absolute path so CSV loading doesn't depend on the
# current working directory -- necessary once this app is packaged with
# PyInstaller, where the working directory at launch isn't guaranteed to be the
# project/bundle directory.
def _adp_data_dir():
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle (onefile or onedir): _MEIPASS is where --add-data
        # resources land in both modes.
        return Path(getattr(sys, '_MEIPASS', Path(sys.executable).resolve().parent)) / 'adp-data'
    return Path(__file__).resolve().parent.parent / 'adp-data'


ADP_DATA_DIR = _adp_data_dir()

SCORING_FORMAT_CSV_PATHS = {
    'Standard': str(ADP_DATA_DIR / 'adp_standard.csv'),
    'Half PPR': str(ADP_DATA_DIR / 'adp_half_ppr.csv'),
    'Full PPR': str(ADP_DATA_DIR / 'adp_full_ppr.csv'),
}


# Define the Data class
class CSVFile:
    def __init__(self, csv_file_path, player_repository):
        self.csv_file_path = csv_file_path
        self.player_repository = player_repository
        self.add_players_to_repository()

    # Method to process CSV data and insert all players into the repository
    def add_players_to_repository(self):
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
                if name and rank is not None:
                    self.player_repository.add_player(
                        rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs,
                        adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp
                    )


# Define the Draft class
class Draft:
    def __init__(self, scoring_format, position_count, drafting_style, num_teams):
        self.scoring_format = scoring_format
        self.position_count = position_count
        self.drafting_style = drafting_style
        self.num_teams = num_teams


# Define the Team class
class Team:
    def __init__(self, team_name, draft_position, player_repository, draft):
        self.team_name = team_name
        self.draft_position = draft_position
        self.player_repository = player_repository
        self.draft = draft
        self.roster = []
        self.filled_roster_positions = []
        self.required_roster_positions = []

        # Initialize required roster positions list
        for position, count in self.draft.position_count.items():
            self.required_roster_positions.extend([position] * count)

    # Method to draft a player and add them to a team's roster while removing them from the repository
    def draft_player(self, player_id):
        player = self.player_repository.fetch_player(player_id)
        self.roster.append(player)
        self.player_repository.remove_player(player_id)

        drafted_player = self.roster[-1]
        player_position = drafted_player.position_group

        # Update filled roster positions
        self.filled_roster_positions.append(player_position)

        # Update required roster positions
        if player_position in self.required_roster_positions:
            self.required_roster_positions.remove(player_position)
        elif player_position == 'RB' and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        elif player_position == 'WR' and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        elif player_position == 'TE' and 'Flex' in self.required_roster_positions:
            self.required_roster_positions.remove('Flex')
        elif 'Bench' in self.required_roster_positions:
            self.required_roster_positions.remove('Bench')
        # else: roster is already full for this position (an "overdraft" beyond the
        # configured roster shape) — tolerate it rather than crashing.


# Define the PlayerBoard class
class PlayerBoard:
    def __init__(self, player_repository):
        self.player_repository = player_repository
        self.players = []
        self.player_count = 0
        self.filter_all_players()

    # Method to erase a player board before fetching from the repository and repopulating it
    def erase_player_board(self):
        self.players = []

    # Method to populate the player board, optionally filtered to one position group
    def filter_by_position(self, position_group=None):
        self.erase_player_board()
        if position_group is None:
            self.players = self.player_repository.fetch_all_players()
        else:
            self.players = self.player_repository.fetch_by_position(position_group)
        self.player_count = len(self.players)
        return self.players

    def filter_all_players(self):
        return self.filter_by_position(None)


# Generate the pick order (team name per pick) for the whole draft
def generate_draft_order(my_teams, my_draft):
    order = []
    team_lookup = {team.draft_position: team.team_name for team in my_teams}
    picks = sum(my_draft.position_count.values())
    if my_draft.drafting_style == 'Standard':
        for _ in range(picks):
            for i in range(1, my_draft.num_teams + 1):
                order.append(team_lookup[i])
    elif my_draft.drafting_style == 'Snake':
        forward = True
        for _ in range(picks):
            rng = range(1, my_draft.num_teams + 1) if forward else range(my_draft.num_teams, 0, -1)
            for i in rng:
                order.append(team_lookup[i])
            forward = not forward
    return order
