import tkinter as tk
from src.ui.main_window import MainWindow
from src.utils.config import get_config

def main():
    config = get_config()
    root = tk.Tk()
    app = MainWindow(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()