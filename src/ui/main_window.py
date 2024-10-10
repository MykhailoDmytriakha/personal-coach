import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from ..audio.recorder import AudioRecorder
from ..audio.transcriber import Transcriber
from ..data.diary_entry import DiaryEntry
from ..ai.chat import ChatBot
from ..data.user_profile import UserProfile
from ..data.task_manager import TaskManager
from .settings_window import SettingsWindow
from ..data.user_info import UserInfo
import threading
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow:
    def __init__(self, master, config):
        self.master = master
        self.master.title("Personal Coach")
        self.master.geometry("800x600")
        self.config = config

        icon_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'app_icon.png')
        if os.path.exists(icon_path):
            icon = tk.PhotoImage(file=icon_path)
            self.master.iconphoto(True, icon)
        
        self.audio_recorder = AudioRecorder(config['recordings_folder'])
        self.transcriber = Transcriber()
        self.diary_entry = DiaryEntry(config['user_data_folder'])
        self.chatbot = ChatBot(config['user_data_folder'])
        self.user_profile = UserProfile(config['user_data_folder'])
        self.task_manager = TaskManager(config['user_data_folder'])
        self.user_info = UserInfo(config['user_data_folder'])
        
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

        # Status label
        self.status_label = ttk.Label(top_frame, text="Status: Idle")
        self.status_label.grid(column=0, row=0, padx=5, pady=5)

        # Settings button
        self.settings_button = ttk.Button(top_frame, text="⚙", width=3, command=self.open_settings)
        self.settings_button.grid(column=1, row=0, padx=5, pady=5, sticky=tk.E)

        # Notebook for different sections
        self.notebook = ttk.Notebook(main_container)
        self.notebook.grid(column=0, row=1, sticky=(tk.N, tk.W, tk.E, tk.S))
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Chat Tab
        chat_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(chat_frame, text="Chat")
        chat_frame.columnconfigure(0, weight=1)
        chat_frame.rowconfigure(0, weight=1)

        # Chat text area
        self.chat_text = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, width=70, height=20)
        self.chat_text.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.tag_configure("user", justify="left", foreground="blue")
        self.chat_text.tag_configure("ai", justify="left", foreground="green")
        self.chat_text.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.chat_text.bind("<Command-a>", self.select_all)
        self.chat_text.bind("<Control-a>", self.select_all)


        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(0, weight=1)

        # Text input
        self.text_input = ttk.Entry(input_frame)
        self.text_input.grid(column=0, row=0, sticky=(tk.W, tk.E))
        self.text_input.bind("<Return>", self.on_enter_press)

        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.grid(column=1, row=0, padx=(5, 0))

        # Record button
        self.record_button = ttk.Button(input_frame, text="🎤", width=3, command=self.toggle_recording)
        self.record_button.grid(column=2, row=0, padx=(5, 0))

        # Tasks Tab
        tasks_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tasks_frame, text="Tasks")
        self.tasks_text = scrolledtext.ScrolledText(tasks_frame, wrap=tk.WORD, width=70, height=20)
        self.tasks_text.pack(expand=True, fill=tk.BOTH)
        self.tasks_text.config(state=tk.NORMAL)
        self.tasks_text.pack(expand=True, fill=tk.BOTH)
        self.tasks_text.bind("<Command-a>", self.select_all)
        self.tasks_text.bind("<Control-a>", self.select_all)

        # User Profile Tab
        user_profile_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(user_profile_frame, text="User Profile")
        self.user_profile_text = scrolledtext.ScrolledText(user_profile_frame, wrap=tk.WORD, width=70, height=20)
        self.user_profile_text.pack(expand=True, fill=tk.BOTH)
        self.user_profile_text.config(state=tk.NORMAL)
        self.user_profile_text.pack(expand=True, fill=tk.BOTH)
        self.user_profile_text.bind("<Command-a>", self.select_all)
        self.user_profile_text.bind("<Control-a>", self.select_all)

        # User Info Tab
        user_info_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(user_info_frame, text="User Info")
        self.user_info_text = scrolledtext.ScrolledText(user_info_frame, wrap=tk.WORD, width=70, height=20)
        self.user_info_text.pack(expand=True, fill=tk.BOTH)
        self.user_info_text.config(state=tk.NORMAL)
        self.user_info_text.bind("<Command-a>", self.select_all)
        self.user_info_text.bind("<Control-a>", self.select_all)
        

        # Diary Entries Tab
        diary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(diary_frame, text="Diary Entries")
        self.diary_text = scrolledtext.ScrolledText(diary_frame, wrap=tk.WORD, width=70, height=20)
        self.diary_text.pack(expand=True, fill=tk.BOTH)
        self.diary_text.config(state=tk.NORMAL)
        self.diary_text.pack(expand=True, fill=tk.BOTH)
        self.diary_text.bind("<Command-a>", self.select_all)
        self.diary_text.bind("<Control-a>", self.select_all)

        self.update_diary()
        self.update_user_profile()
        self.update_tasks()
        self.update_user_info()
    
    def select_all(self, event):
        event.widget.tag_add(tk.SEL, "1.0", tk.END)
        event.widget.mark_set(tk.INSERT, "1.0")
        event.widget.see(tk.INSERT)
        return 'break'
    
    def open_settings(self):
        try:
            SettingsWindow(self.master, self.config)
        except Exception as e:
            logging.error(f"Error opening settings window: {e}", exc_info=True)
            self.show_error(f"Error opening settings: {e}")

    def toggle_recording(self):
        if not self.audio_recorder.is_recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.audio_recorder.start_recording()
        self.record_button.config(text="⏹")
        self.status_label.config(text="Status: Recording...")

    def stop_recording(self):
        audio_file = self.audio_recorder.stop_recording()
        self.record_button.config(text="🎤")
        self.status_label.config(text="Status: Processing...")
        threading.Thread(target=self.process_recording, args=(audio_file,), daemon=True).start()

    def process_recording(self, audio_file):
        try:
            text = self.transcriber.transcribe(audio_file, language=self.config['default_language'])
            if not text:
                self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))
                return
            
            self.master.after(0, lambda: self.update_chat("user", text))
            self.process_input(text)
        except Exception as e:
            logging.error(f"Error in process_recording: {e}", exc_info=True)
            self.master.after(0, lambda: self.show_error(f"Error in processing recording: {e}"))
            self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))

    def on_enter_press(self, event):
        self.send_message()

    def send_message(self):
        text = self.text_input.get()
        if text:
            self.text_input.delete(0, tk.END)
            self.update_chat("user", text)
            self.process_input(text)

    def process_input(self, text):
        try:
            self.diary_entry.save_entry(text)
            ai_response = self.chatbot.get_response(text)
            
            if isinstance(ai_response, dict):
                self.master.after(0, lambda: self.update_chat("ai", ai_response.get('output', '')))
                self.master.after(0, lambda: self.update_tasks(ai_response.get('tasks', [])))
                self.master.after(0, lambda: self.update_user_profile(ai_response.get('user_profile', [])))
                self.master.after(0, lambda: self.update_user_info(ai_response.get('new_user_info', [])))
            else:
                logging.error(f"Unexpected AI response format: {ai_response}")
                self.master.after(0, lambda: self.show_error("Unexpected response from AI. Please try again."))
            
            self.master.after(0, lambda: self.update_diary())
            self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))
        except Exception as e:
            logging.error(f"Error in process_input: {e}", exc_info=True)
            self.master.after(0, lambda: self.show_error(f"Error in processing input: {e}"))
            self.master.after(0, lambda: self.status_label.config(text="Status: Idle"))

    def update_chat(self, sender, text):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender.capitalize()}: {text}\n\n", sender)
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.NORMAL)

    def update_tasks(self, tasks):
        self.tasks_text.config(state=tk.NORMAL)
        self.tasks_text.delete(1.0, tk.END)
        for task in tasks:
            self.tasks_text.insert(tk.END, f"- {task}\n")
        self.tasks_text.config(state=tk.NORMAL)

    def update_diary(self):
        logging.info("Updating diary display")
        try:
            if self.diary_entry.has_entries():
                entries = self.diary_entry.get_entries()
                self.diary_text.config(state=tk.NORMAL)
                self.diary_text.delete(1.0, tk.END)
                for entry in entries:
                    self.diary_text.insert(tk.END, f"{entry['timestamp']}\n{entry['content']}\n\n")
                self.diary_text.config(state=tk.NORMAL)
                logging.info(f"Displayed {len(entries)} diary entries")
            else:
                self.diary_text.config(state=tk.NORMAL)
                self.diary_text.delete(1.0, tk.END)
                self.diary_text.insert(tk.END, "No entries found. Start writing to create your first entry!")
                self.diary_text.config(state=tk.NORMAL)
                logging.info("No diary entries to display")
        except Exception as e:
            logging.error(f"Error in update_diary: {e}", exc_info=True)
            self.show_error(f"Error updating diary: {e}")
    
    def update_user_profile(self, new_profile_data=None):
        try:
            if new_profile_data:
                self.user_profile.update_profile(new_profile_data)
            
            profile_data = self.user_profile.get_profile()
            self.user_profile_text.config(state=tk.NORMAL)
            self.user_profile_text.delete(1.0, tk.END)
            for item in profile_data:
                self.user_profile_text.insert(tk.END, f"{item['timestamp']})\n• {item['item']}\n\n")
            self.user_profile_text.config(state=tk.NORMAL)
        except Exception as e:
            logging.error(f"Error in update_user_profile: {e}", exc_info=True)
            self.show_error(f"Error updating user profile: {e}")
    
    def update_user_info(self, new_info_data=None):
        try:
            if new_info_data:
                self.user_info.update_info(new_info_data)
            
            info_data = self.user_info.get_info()
            self.user_info_text.config(state=tk.NORMAL)
            self.user_info_text.delete(1.0, tk.END)
            for item in info_data:
                self.user_info_text.insert(tk.END, f"{item['timestamp']})\n• {item['item']}\n\n")
            self.user_info_text.config(state=tk.NORMAL)
            logging.info(f"Updated user info display with {len(info_data)} items")
        except Exception as e:
            logging.error(f"Error in update_user_info: {e}", exc_info=True)
            self.show_error(f"Error updating user info: {e}")
    
    def update_tasks(self, new_tasks=None):
        if new_tasks:
            self.task_manager.add_tasks(new_tasks)
        
        tasks = self.task_manager.get_tasks()
        self.tasks_text.delete(1.0, tk.END)
        for task in tasks:
            status = "[X]" if task['completed'] else "[ ]"
            self.tasks_text.insert(tk.END, f"{status} {task['id']}: {task['task']}\n")

    def add_task(self):
        task = self.new_task_entry.get()
        if task:
            self.task_manager.add_tasks([task])
            self.new_task_entry.delete(0, tk.END)
            self.update_tasks()

    def show_error(self, message):
        logging.error(message)
        messagebox.showerror("Error", message)