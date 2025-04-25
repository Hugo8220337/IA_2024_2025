import tkinter as tk
from tkinter import filedialog

class FileTab:
    def __init__(self, parent_menu, app):
        self.app = app
        self.menu = tk.Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label="File", menu=self.menu)
        self.create_menu()

    def create_menu(self):
        self.menu.add_command(label="Selecionar Modelo", command=self.select_model)

    def select_model(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Modelo YOLO",
            filetypes=[("Model Files", "*.pt"), ("All Files", "*.*")]
        )
        if file_path:
            self.app.load_model(file_path)