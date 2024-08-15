# SQLite interaction layer
import sqlite3

# Define the DatabaseTable class
class DatabaseTable:
    def __init__(self, table_name, db_name = 'players.db'):
        self.table_name = table_name
        self.db_name = db_name
        self.create_table()

    # Method to create a database table
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            rank INTEGER,
            name TEXT,
            team TEXT,
            bye INTEGER,
            position TEXT,
            adp_espn REAL,
            adp_yahoo REAL,
            adp_cbs REAL,
            adp_sleeper REAL,
            adp_nfl REAL,
            adp_rtsports REAL,
            avg_adp REAL
        )
        ''')
        conn.commit()
        conn.close()

    # Method to insert a player into a database table
    def insert_player(self, rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {self.table_name} (rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, avg_adp))
        conn.commit()
        conn.close()

    # Method to remove a player from a database table
    def remove_player(self, player_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'DELETE FROM {self.table_name} WHERE player_id = ?', (player_id,))
        conn.commit()
        conn.close()

    # Method to update a player's rank in a database table
    # Not sure if this method is needed, given I might update a player's rank within the Player class object without affecting the database table
    # Actually, might need this method because I want the database to act as the "source of truth" where it dynamically updates as players are drafted or player ranks are updated
    def update_player_rank(self, player_id, new_rank):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {self.table_name} SET rank = ? WHERE player_id = ?", (new_rank, player_id))
        conn.commit()
        conn.close()

    # Method to fetch the number of players in a database table
    # Use this in the main logic to set the size of a for loop, then create Player objects during each loop
    def fetch_number_of_players(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
        count = cursor.fetchone()[0]
        conn.close()

        return count

    # Method to fetch a player from a database table
    def fetch_player(self, player_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE player_id = ?", (player_id,))
        row = cursor.fetchone()
        conn.close()

        return row

    # Method to fetch all players from a database table
    # Not sure if this method is needed, given I might use fetch_player() within a for loop to create Player objects for the entire database table
    def fetch_all_players(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all QBs from a database table
    def fetch_qbs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%QB%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all RBs from a database table
    def fetch_rbs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%RB%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all WRs from a database table
    def fetch_wrs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%WR%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all TEs from a database table
    def fetch_tes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%TE%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all Ks from a database table
    def fetch_ks(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%K%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all DSTs from a database table
    def fetch_dsts(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE position LIKE ?", ('%DST%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all of a team's players from a database table
    def fetch_teams_players(self, team):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE team = ?", (team,))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetach all players with a specific bye from a database table
    def fetch_players_with_bye(self, bye):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE bye = ?", (bye,))
        rows = cursor.fetchall()
        conn.close()

        return rows
