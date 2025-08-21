import sqlite3

# Define the DatabaseTable class
class DatabaseTable:
    def __init__(self, table_name, db_name='players.db'):
        self.table_name = table_name
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.delete_table()
        self.create_table()

    def __del__(self):
        self.conn.close()

    # Method to create a database table
    def create_table(self):
        self.cursor.execute(f'''
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
            adp_fantrax REAL,
            avg_adp REAL
        )
        ''')
        self.conn.commit()

    # Method to delete a database table
    def delete_table(self):
        self.cursor.execute(f'DROP TABLE IF EXISTS {self.table_name}')
        self.conn.commit()

    # Method to insert a player into a database table
    def insert_player(self, rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp):
        self.cursor.execute(f'''
        INSERT INTO {self.table_name} (rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rank, name, team, bye, position, adp_espn, adp_yahoo, adp_cbs, adp_sleeper, adp_nfl, adp_rtsports, adp_fantrax, avg_adp))
        self.conn.commit()

    # Method to remove a player from a database table
    def remove_player(self, player_id):
        self.cursor.execute(f'DELETE FROM {self.table_name} WHERE player_id = ?', (player_id,))
        self.conn.commit()

    # Method to find a player from a database table
    def find_player(self, name, team, position):
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE name = ? AND team = ? AND position LIKE ?', (name, team, f'%{position}%'))
        return self.cursor.fetchone()

    # Method to find the player with the lowest ADP from a database table
    def find_lowest_adp(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name} ORDER BY rank LIMIT 1')
        return self.cursor.fetchone()

    # Method to fetch a player from a database table
    def fetch_player(self, player_id):
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE player_id = ?', (player_id,))
        return self.cursor.fetchone()

    # Method to fetch all players from a database table
    def fetch_all_players(self):
        self.cursor.execute(f'SELECT * FROM {self.table_name}')
        return self.cursor.fetchall()

    # Generic method to fetch by position
    def fetch_by_position(self, position):
        self.cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', (f'%{position}%',))
        return self.cursor.fetchall()

    # Replace individual fetch_* methods with generic fetch_by_position for speed and maintainability
    def fetch_qbs(self):
        return self.fetch_by_position('QB')

    def fetch_rbs(self):
        return self.fetch_by_position('RB')

    def fetch_wrs(self):
        return self.fetch_by_position('WR')

    def fetch_tes(self):
        return self.fetch_by_position('TE')

    def fetch_ks(self):
        return self.fetch_by_position('K')

    def fetch_dsts(self):
        return self.fetch_by_position('DST')
