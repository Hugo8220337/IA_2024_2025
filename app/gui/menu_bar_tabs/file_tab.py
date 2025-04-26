import tkinter as tk
from tkinter import Menu, filedialog

from bot.bot_controller import BotController

class FileTab:
    def __init__(self, parent_menu: Menu, bot_controller: BotController):
        self.bot_controller = bot_controller
        self.menu = tk.Menu(parent_menu, tearoff=0)

        parent_menu.add_cascade(label="File", menu=self.menu)
        self.create_menu()

    def create_menu(self):
        """
        Create the File menu items.
        """
        self.menu.add_command(label="Selecionar Modelo", command=self.select_model)

    def select_model(self):
        """
        Open a file dialog to select a YOLO model file.
        """
        file_path = filedialog.askopenfilename(
            title="Selecionar Modelo YOLO",
            filetypes=[("Model Files", "*.pt"), ("All Files", "*.*")]
        )
        if file_path:
            self.bot_controller.load_model(file_path)