import tkinter as tk

from gui.menu_bar_tabs.file_tab import FileTab
from gui.menu_bar_tabs.option_tab import OptionsTab

class MenuBar:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.init_menus()

    def init_menus(self):
        # Inicializa o tab File
        self.file_tab = FileTab(self.menu, self.app)
        
        # Inicializa o tab de Opções
        self.options_tab = OptionsTab(self.root, self.app)
        self.menu.add_cascade(label="Opções", menu=self._create_options_cascade())

    def _create_options_cascade(self):
        options_submenu = tk.Menu(self.menu, tearoff=0)
        options_submenu.add_command(label="Editar Configurações", command=self.options_tab.open_options)
        return options_submenu