import os
import json
import sqlite3
from ..utils.config import get_config

class UserProfile:
    def __init__(self, diary_entries_folder):
        self.profile_folder = diary_entries_folder
        os.makedirs(self.profile_folder, exist_ok=True)
        self.db_path = os.path.join(self.profile_folder, 'user_profile.db')
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT
                )
            ''')

    def update_profile(self, new_items):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Insert new items
            cursor.executemany('INSERT INTO user_profile (item) VALUES (?)', 
                               [(item,) for item in new_items])

    def get_profile(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT item FROM user_profile')
            return [row[0] for row in cursor.fetchall()]

    def clear_profile(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_profile')