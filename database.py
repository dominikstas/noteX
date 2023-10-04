# database.py
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()

        # Utwórz tabelę 'settings', jeśli nie istnieje
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                dark_mode INTEGER
            )
        ''')

    def load_dark_mode_setting(self):
        self.c.execute('SELECT dark_mode FROM settings WHERE id = 1')
        result = self.c.fetchone()

        if result:
            return bool(result[0])
        else:
            return False

    def save_dark_mode_setting(self, dark_mode):
        self.c.execute('INSERT OR REPLACE INTO settings (id, dark_mode) VALUES (1, ?)', (int(dark_mode),))
        self.conn.commit()
