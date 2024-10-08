import sqlite3
import os
from ..utils.config import get_config

class TaskManager:
    def __init__(self, user_data_folder):
        config = get_config()
        self.db_path = os.path.join(user_data_folder, 'user_data.db')
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT,
                    completed INTEGER DEFAULT 0
                )
            ''')

    def add_tasks(self, tasks):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany('INSERT INTO tasks (task) VALUES (?)', 
                               [(task,) for task in tasks])

    def get_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, task, completed FROM tasks')
            return [{'id': row[0], 'task': row[1], 'completed': bool(row[2])} for row in cursor.fetchall()]

    def complete_task(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))

    def delete_task(self, task_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))

    def clear_completed_tasks(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE completed = 1')