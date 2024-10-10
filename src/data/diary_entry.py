import sqlite3
import datetime
import os
import logging
from ..utils.config import get_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DiaryEntry:
    def __init__(self, user_data_folder):
        self.db_path = os.path.join(user_data_folder, 'user_data.db')
        self._create_table()
        logging.info(f"DiaryEntry initialized with database path: {self.db_path}")

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS diary_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    content TEXT
                )
            ''')
        logging.info("Diary entries table created or verified")

    def save_entry(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO diary_entries (timestamp, content) VALUES (?, ?)', (timestamp, text))
        logging.info(f"New diary entry saved with timestamp: {timestamp}")

    def get_entries(self):
        logging.info("Attempting to retrieve diary entries")
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT id, timestamp, content FROM diary_entries ORDER BY timestamp DESC')
            entries = cursor.fetchall()
            logging.info(f"Retrieved {len(entries)} diary entries")
            return [{'id': row['id'], 'timestamp': row['timestamp'], 'content': row['content']} for row in entries]

    def get_entry_dates(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT date(timestamp) FROM diary_entries ORDER BY date(timestamp) DESC')
            dates = [row[0] for row in cursor.fetchall()]
            logging.info(f"Retrieved {len(dates)} unique entry dates")
            return dates

    def delete_entry(self, entry_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM diary_entries WHERE id = ?', (entry_id,))
            deleted = cursor.rowcount > 0
            logging.info(f"Deleted entry with ID {entry_id}: {'Success' if deleted else 'Failed'}")
            return deleted

    def has_entries(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM diary_entries')
            count = cursor.fetchone()[0]
            logging.info(f"Diary has {count} entries")
            return count > 0

    def has_entries_for_period(self, period):
        logging.info(f"Checking for entries in period: {period}")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            now = datetime.datetime.now()
            if period == 'day':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - datetime.timedelta(days=now.weekday())
                start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'month':
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == 'year':
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                raise ValueError(f"Invalid period: {period}")
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM diary_entries 
                WHERE date(substr(timestamp, 1, 10)) >= date(?)
            ''', (start_date_str,))
            
            count = cursor.fetchone()[0]
            has_entries = count > 0
            logging.info(f"Period {period} has entries: {has_entries} (Count: {count}, Start date: {start_date_str})")
            return has_entries

    def get_entries_for_period(self, period):
        logging.info(f"Retrieving diary entries for period: {period}")
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            now = datetime.datetime.now()
            if period == 'day':
                start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'week':
                start_date = now - datetime.timedelta(days=now.weekday())
                start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period == 'month':
                start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            elif period == 'year':
                start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            else:
                raise ValueError(f"Invalid period: {period}")
            
            start_date_str = start_date.strftime('%Y-%m-%d')
            
            cursor.execute('''
                SELECT id, timestamp, content 
                FROM diary_entries 
                WHERE date(substr(timestamp, 1, 10)) >= date(?)
                ORDER BY timestamp DESC
            ''', (start_date_str,))
            
            entries = cursor.fetchall()
            entry_count = len(entries)
            logging.info(f"Retrieved {entry_count} entries for period: {period}")
            
            if entry_count == 0:
                logging.info(f"No entries found for period: {period}")
                return []
            
            return [{'id': row['id'], 'timestamp': row['timestamp'], 'content': row['content']} for row in entries]