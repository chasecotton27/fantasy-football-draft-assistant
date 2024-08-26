import sqlite3

# Define the DatabaseTable class
class DatabaseTable:
    def __init__(self, table_name, db_name = 'players.db'):
        self.table_name = table_name
        self.db_name = db_name
        self.delete_table()
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

    # Method to delete a database table
    def delete_table(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'DROP TABLE IF EXISTS {self.table_name}')
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

    # Method to find a player from a database table
    def find_player(self, name, team, position):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE name = ? AND team = ? AND position LIKE ?', (name, team, f'%{position}%'))
        row = cursor.fetchone()
        conn.close()

        return row

    # Method to find the player with the lowest ADP from a database table
    def find_lowest_adp(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} ORDER BY rank LIMIT 1')
        row = cursor.fetchone()
        conn.close()

        return row

    # Method to fetch a player from a database table
    def fetch_player(self, player_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE player_id = ?', (player_id,))
        row = cursor.fetchone()
        conn.close()

        return row

    # Method to fetch all players from a database table
    def fetch_all_players(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name}')
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all QBs from a database table
    def fetch_qbs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%QB%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all RBs from a database table
    def fetch_rbs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%RB%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all WRs from a database table
    def fetch_wrs(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%WR%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all TEs from a database table
    def fetch_tes(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%TE%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all Ks from a database table
    def fetch_ks(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%K%',))
        rows = cursor.fetchall()
        conn.close()

        return rows

    # Method to fetch all DSTs from a database table
    def fetch_dsts(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {self.table_name} WHERE position LIKE ?', ('%DST%',))
        rows = cursor.fetchall()
        conn.close()

        return rows
