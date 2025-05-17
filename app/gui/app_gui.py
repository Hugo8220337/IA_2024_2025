import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

from utils.config import Config
from bot.bot_controller import BotController

class AppGUI:
    def __init__(self, root: tk, bot_controller: BotController, configs: Config):
        self._root = root
        self._bot_controller = bot_controller
        self.configs = configs

        self._root.title("Pokémon Bot")
        self.status_text = tk.StringVar(value="Inactive")
        self.model_status_text = tk.StringVar(value="No model loaded")
        self.setup_gui()

    def setup_gui(self):
        """
        Set up the GUI components. 
        """
        frame = ttk.Frame(self._root, padding=10)
        frame.pack()

        # Create a label for the title
        ttk.Label(frame, textvariable=self.model_status_text, foreground="blue").pack(pady=5)
        self.label_img = ttk.Label(frame)
        self.label_img.pack(pady=10)

        # Create a button to load the model
        self.btn_toggle = ttk.Button(frame, text="Activate", command=self.toggle_bot, state=tk.DISABLED)
        self.btn_toggle.pack()
        ttk.Label(frame, textvariable=self.status_text).pack(pady=5)

    def toggle_bot(self):
        """
        Toggle the bot's running state and update the button text accordingly.
        """
        if self._bot_controller.running:
            self._bot_controller.stop_bot()
            self.status_text.set("Inactive")
            self.btn_toggle.config(text="Activate")
        else:
            self._bot_controller.start_bot()
            self.status_text.set("Active")
            self.btn_toggle.config(text="Deactivate")

    def update_model_status(self, text):
        """
        Update the model status text in the GUI.
        """
        self.model_status_text.set(text)

    def update_image(self, frame):
        """
        Update the displayed image in the GUI with the given frame,
        if the option is enabled.
        """
        show_taken_screenshots = self.configs.get("show_taken_screenshots", True)
        if show_taken_screenshots:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img_pil = Image.fromarray(rgb_image).resize((800, 480))
            img_tk = ImageTk.PhotoImage(img_pil)
            self.label_img.imgtk = img_tk  # Prevents garbage collection.
            self.label_img.config(image=img_tk)

    def enable_toggle(self):
        """
        Enable the toggle button in the GUI.
        """
        self.btn_toggle.config(state=tk.NORMAL)
    
    def get_root(self):
        """
        Get the root window of the GUI.
        """
        return self._root