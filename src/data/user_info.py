import os
import sqlite3
import datetime
from ..utils.config import get_config

class UserInfo:
    def __init__(self, user_data_folder):
        config = get_config()
        self.db_path = os.path.join(user_data_folder, 'user_data.db')
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_info (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    timestamp TEXT
                )
            ''')

    def update_info(self, new_items):
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO user_info (item, timestamp) VALUES (?, ?)', 
                               [(item, timestamp) for item in new_items])

    def get_info(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT item, timestamp FROM user_info ORDER BY timestamp DESC')
            return [{'item': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]

    def get_latest_info(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT item FROM user_info 
                WHERE timestamp = (SELECT MAX(timestamp) FROM user_info)
            ''')
            return [row[0] for row in cursor.fetchall()]

    def clear_info(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_info')