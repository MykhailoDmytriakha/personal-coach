import os
import sqlite3
import datetime
from ..utils.config import get_config

class UserProfile:
    def __init__(self, user_data_folder):
        config = get_config()
        self.db_path = os.path.join(user_data_folder, 'user_data.db')
        self._create_tables()

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create user_profile table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT,
                    timestamp TEXT
                )
            ''')
            
            # Create user_context table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_context (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    context TEXT,
                    period TEXT,
                    timestamp TEXT
                )
            ''')

    def update_profile(self, new_items):
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO user_profile (item, timestamp) VALUES (?, ?)', 
                               [(item, timestamp) for item in new_items])

    def get_profile(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT item, timestamp FROM user_profile ORDER BY timestamp DESC')
            return [{'item': row[0], 'timestamp': row[1]} for row in cursor.fetchall()]

    def clear_profile(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM user_profile')
    
    def store_context(self, context, period):
        timestamp = datetime.datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO user_context (context, period, timestamp)
                VALUES (?, ?, ?)
            ''', (context, period, timestamp))

    def get_latest_context(self, period):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT context FROM user_context
                WHERE period = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (period,))
            result = cursor.fetchone()
            return result[0] if result else None

    def context_needs_update(self, period):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT timestamp FROM user_context
                WHERE period = ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (period,))
            result = cursor.fetchone()
            if not result:
                return True
            
            last_update = datetime.datetime.fromisoformat(result[0])
            now = datetime.datetime.now()
            
            if period == 'day':
                return last_update.date() != now.date()
            elif period == 'week':
                return last_update.isocalendar()[1] != now.isocalendar()[1] or last_update.year != now.year
            elif period == 'month':
                return last_update.month != now.month or last_update.year != now.year
            elif period == 'year':
                return last_update.year != now.year
            else:
                return True 