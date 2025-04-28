import tkinter as tk

from bot.bot_controller import BotController
from utils.config import Config
from gui.menu_bar_tabs.file_tab import FileTab
from gui.menu_bar_tabs.option_tab import OptionsTab

class MenuBar:
    def __init__(self, root: tk, bot_controller: BotController, configs: Config):
        self.root = root
        self.bot_controller = bot_controller
        self.configs = configs

        self.menu = tk.Menu(root)

        # Configure the menu bar
        self.root.config(menu=self.menu)

        # Initialize the tabs
        self.init_menus()

    def init_menus(self):
        """
        Initializes the menus of the menu bar.
        """
        # Initialize the File tab
        self.file_tab = FileTab(self.menu, self.bot_controller)
        
        # Initialize the Options tab
        self.options_tab = OptionsTab(self.root, self.configs)
        self.menu.add_cascade(label="Options", menu=self._create_options_cascade())

    def _create_options_cascade(self):
        """
        Creates the options submenu.
        """
        options_submenu = tk.Menu(self.menu, tearoff=0)
        options_submenu.add_command(label="Edit Configurations", command=self.options_tab.open_options)
        return options_submenu