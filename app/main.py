import tkinter as tk
from utils.ocr_utils import OCRReaderSingleton
from utils.config import Config
from utils.contants import CONFIG_INSTANCE
from gui.app_gui import AppGUI
from bot.bot_controller import BotController
from gui.menu_bar import MenuBar

def main():
    root = tk.Tk()

    configs = Config.get_instance(CONFIG_INSTANCE)
    
    bot_controller = BotController(
        gui=None,
        configs=configs
    )

    # Set up the main application GUI
    gui = AppGUI(root, bot_controller, configs)

    # Set up the bot controller with the GUI
    bot_controller.gui = gui

    menu_bar = MenuBar(root, bot_controller, configs)

    # Configure the menu bar
    root.config(menu=menu_bar.menu)

    # Load the OCR reader instance on startup, to avoid delays in the first use
    OCRReaderSingleton.get_instance()  

    # Configure the main window
    root.mainloop()

if __name__ == "__main__":
    main()