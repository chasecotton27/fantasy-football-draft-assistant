# SQLite interaction layer
import sqlite3

# Define the DatabaseTable class
class DatabaseTable:
    def __init__(self, table_name, db_name='players.db'):
        self.table_name = table_name
        self.db_name = db_name
        self.create_table()

    # Method to create the table
    def create_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rank INTEGER,
            team TEXT,
            bye INTEGER,
            position TEXT,
            adp_espn REAL,
            adp_sleeper REAL,
            adp_nfl REAL,
            adp_rtsports REAL,
            avg_adp REAL
        )
        ''')
        conn.commit()
        conn.close()

    # Method to insert player data into the table
    def insert_player(self, name, rank, team, bye, position, adp_espn, adp_sleeper, adp_nfl, adp_rtsports, avg_adp):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO {self.table_name} (name, rank, team, bye, position, adp_espn, adp_sleeper, adp_nfl, adp_rtsports, avg_adp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, rank, team, bye, position, adp_espn, adp_sleeper, adp_nfl, adp_rtsports, avg_adp))
        conn.commit()
        conn.close()

    # Method to fetch all players
    def fetch_all_players(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to update player rank
    def update_player_rank(self, player_id, new_rank):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {self.table_name} SET rank = ? WHERE player_id = ?", (new_rank, player_id))
        conn.commit()
        conn.close()
