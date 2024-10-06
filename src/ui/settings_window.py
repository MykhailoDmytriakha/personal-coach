import tkinter as tk
from tkinter import ttk
import logging

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.title("Settings")
        self.config = config
        self.language_var = tk.StringVar(value=self.config.get('default_language', 'en'))
        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding="10")
        frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

        ttk.Label(frame, text="Language:").grid(column=0, row=0, padx=5, pady=5)
        language_combo = ttk.Combobox(frame, textvariable=self.language_var, values=('en', 'ru', 'fr', 'de', 'es'), width=5)
        language_combo.grid(column=1, row=0, padx=5, pady=5)
        language_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        ttk.Button(frame, text="Close", command=self.destroy).grid(column=0, row=1, columnspan=2, pady=10)

    def on_language_change(self, event):
        selected_language = self.language_var.get()
        self.config['default_language'] = selected_language
        logging.info(f"Language changed to: {selected_language}")