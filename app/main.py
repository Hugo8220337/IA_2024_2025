import tkinter as tk
from gui.app_gui import AppGUI
from bot.bot_controller import BotController
from gui.menu_bar import MenuBar

def main():
    root = tk.Tk()

    bot_controller = BotController(None)
    gui = AppGUI(root, bot_controller)

    # Configura o controlador do bot com a GUI
    bot_controller.gui = gui

    menu_bar = MenuBar(root, bot_controller)

    root.config(menu=menu_bar.menu)
    root.mainloop()

if __name__ == "__main__":
    main()