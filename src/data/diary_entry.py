import os
import datetime
import json
from ..utils.config import get_config

class DiaryEntry:
    def __init__(self, diary_folder):
        self.diary_folder = diary_folder

    def save_entry(self, text):
        """
        Save a new diary entry.
        """
        today = datetime.date.today()
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        entry = {
            "timestamp": f"{today} {current_time}",
            "content": text
        }
        
        filename = os.path.join(self.diary_folder, f"diary_entry_{today}.json")
        
        entries = []
        if os.path.exists(filename):
            with open(filename, "r", encoding='utf-8') as file:
                entries = json.load(file)
        
        entries.append(entry)
        
        with open(filename, "w", encoding='utf-8') as file:
            json.dump(entries, file, ensure_ascii=False, indent=2)

    def get_entries(self, date=None):
        """
        Retrieve diary entries for a specific date or all entries if date is None.
        """
        if date is None:
            date = datetime.date.today()
        
        filename = os.path.join(self.diary_folder, f"diary_entry_{date}.json")
        
        if os.path.exists(filename):
            with open(filename, "r", encoding='utf-8') as file:
                return json.load(file)
        return []

    def get_entry_dates(self):
        """
        Get a list of dates for which diary entries exist.
        """
        dates = []
        for filename in os.listdir(self.diary_folder):
            if filename.startswith("diary_entry_") and filename.endswith(".json"):
                date_str = filename[12:-5]  # Extract date from filename
                dates.append(datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
        return sorted(dates, reverse=True)

    def delete_entry(self, date, index):
        """
        Delete a specific diary entry.
        """
        filename = os.path.join(self.diary_folder, f"diary_entry_{date}.json")
        if os.path.exists(filename):
            with open(filename, "r", encoding='utf-8') as file:
                entries = json.load(file)
            if 0 <= index < len(entries):
                del entries[index]
                with open(filename, "w", encoding='utf-8') as file:
                    json.dump(entries, file, ensure_ascii=False, indent=2)
                return True
        return False