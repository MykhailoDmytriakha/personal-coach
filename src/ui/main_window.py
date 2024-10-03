import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..audio.recorder import AudioRecorder
from ..audio.transcriber import Transcriber
from ..data.diary_entry import DiaryEntry
from ..ai.chat import ChatBot
from ..ai.task_extractor import TaskExtractor
import threading

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
        print(f"Language changed to: {selected_language}")

class MainWindow:
    def __init__(self, master, config):
        self.master = master
        self.master.title("Personal Coach")
        self.master.geometry("800x600")
        self.config = config
        
        self.audio_recorder = AudioRecorder(config['recordings_folder'])
        self.transcriber = Transcriber()
        self.diary_entry = DiaryEntry(config['diary_entries_folder'])
        self.chatbot = ChatBot()
        self.task_extractor = TaskExtractor()
        
        self.setup_ui()
    
    def setup_ui(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Main container
        main_container = ttk.Frame(self.master, padding="10")
        main_container.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Top frame for controls
        top_frame = ttk.Frame(main_container)
        top_frame.grid(column=0, row=0, sticky=(tk.W, tk.E))
        top_frame.columnconfigure(1, weight=1)

        # Recording controls
        self.record_button = ttk.Button(top_frame, text="Start Recording", command=self.toggle_recording)
        self.record_button.grid(column=0, row=0, padx=5, pady=5)

        self.status_label = ttk.Label(top_frame, text="Status: Idle")
        self.status_label.grid(column=1, row=0, padx=5, pady=5)

        # Settings button
        self.settings_button = ttk.Button(top_frame, text="⚙", width=3, command=self.open_settings)
        self.settings_button.grid(column=2, row=0, padx=5, pady=5)

        # Notebook for different sections
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Chat Tab
        chat_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(chat_frame, text="Chat")
        self.chat_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=70, height=20)
        self.chat_text.pack(expand=True, fill=tk.BOTH)
        self.chat_text.tag_configure("user", justify="right", foreground="blue")
        self.chat_text.tag_configure("ai", justify="left", foreground="green")

        # Tasks Tab
        tasks_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tasks_frame, text="Tasks")
        self.tasks_text = scrolledtext.ScrolledText(tasks_frame, wrap=tk.WORD, width=70, height=10)
        self.tasks_text.pack(expand=True, fill=tk.BOTH)

        # Diary Entries Tab
        diary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(diary_frame, text="Diary Entries")
        self.diary_text = scrolledtext.ScrolledText(diary_frame, wrap=tk.WORD, width=70, height=10)
        self.diary_text.pack(expand=True, fill=tk.BOTH)

        # Bottom frame for additional controls
        bottom_frame = ttk.Frame(main_container)
        bottom_frame.grid(column=0, row=2, sticky=(tk.W, tk.E))
        bottom_frame.columnconfigure(1, weight=1)

        self.clear_button = ttk.Button(bottom_frame, text="Clear All", command=self.clear_all)
        self.clear_button.grid(column=0, row=0, padx=5, pady=5)

        self.save_button = ttk.Button(bottom_frame, text="Save Session", command=self.save_session)
        self.save_button.grid(column=1, row=0, padx=5, pady=5)

        self.load_button = ttk.Button(bottom_frame, text="Load Session", command=self.load_session)
        self.load_button.grid(column=2, row=0, padx=5, pady=5)

    def open_settings(self):
        SettingsWindow(self.master, self.config)

    def toggle_recording(self):
        if not self.audio_recorder.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.audio_recorder.start_recording()
        self.record_button.config(text="Stop Recording")
        self.status_label.config(text="Status: Recording...")

    def stop_recording(self):
        audio_file = self.audio_recorder.stop_recording()
        self.record_button.config(text="Start Recording")
        self.status_label.config(text="Status: Processing...")
        threading.Thread(target=self.process_recording, args=(audio_file,), daemon=True).start()

    def process_recording(self, audio_file):
        try:
            text = self.transcriber.transcribe(audio_file, language=self.config['default_language'])
            if not text:
                self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))
                return
            
            self.master.after(0, lambda: self.update_chat("user", text))
            self.diary_entry.save_entry(text)
            
            ai_response = self.chatbot.get_response(text)
            tasks = self.task_extractor.extract_tasks(text)
            
            self.master.after(0, lambda: self.update_chat("ai", ai_response))
            self.master.after(0, lambda: self.update_tasks(tasks))
            self.master.after(0, lambda: self.update_diary())
            self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))
        except Exception as e:
            print(f"Error: {e}")
            self.master.after(0, lambda: self.show_error(f"Error: {e}"))
            self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))

    def update_chat(self, sender, text):
        self.chat_text.insert(tk.END, f"{sender.capitalize()}: {text}\n\n", sender)
        self.chat_text.see(tk.END)

    def update_tasks(self, tasks):
        self.tasks_text.delete(1.0, tk.END)
        for task in tasks:
            self.tasks_text.insert(tk.END, f"- {task}\n")

    def update_diary(self):
        entries = self.diary_entry.get_entries()
        self.diary_text.delete(1.0, tk.END)
        for entry in entries:
            self.diary_text.insert(tk.END, f"{entry['timestamp']}\n{entry['content']}\n\n")

    def show_error(self, message):
        messagebox.showerror("Error", message)

    def show_info(self, message):
        messagebox.showinfo("Information", message)

    def clear_all(self):
        self.chat_text.delete(1.0, tk.END)
        self.tasks_text.delete(1.0, tk.END)
        self.diary_text.delete(1.0, tk.END)

    def save_session(self):
        # Implement saving the current session
        self.show_info("Session saved successfully!")

    def load_session(self):
        # Implement loading a previous session
        self.show_info("Session loaded successfully!")

    def exit_application(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.master.quit()