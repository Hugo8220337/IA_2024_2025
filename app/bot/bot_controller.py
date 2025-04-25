from ultralytics import YOLO
from utils.contants import CONFIG_INSTANCE, CONFIG_SCREENSHOT_DEFAULT_DELAY
from utils.config import Config

import utils.frame_utils as frame_utils

class BotController:
    def __init__(self, gui):
        self.gui = gui
        
        self.config = Config.get_instance(CONFIG_INSTANCE)
        self.running = False
        self.yolo_model = None

    def toggle_bot(self):
        self.running = not self.running
        print("Bot iniciado!" if self.running else "Bot parado!")
        if self.running:
            self.update_loop()

    def update_loop(self):
        if not self.running:
            return

        screenshot_delay = self.config.get("screenshot_delay", CONFIG_SCREENSHOT_DEFAULT_DELAY)

        screenshot_cv = frame_utils.capture_screenshot() 

        # Process the screenshot with YOLO model if loaded
        frame_to_show = frame_utils.process_frame(screenshot_cv, self.yolo_model)
        self.gui.update_image(frame_to_show)

        # Save the screenshot if the option is enabled
        frame_utils.save_frame(frame_to_show, self.config)

        # Schedule the next screenshot
        self.gui.root.after(screenshot_delay, self.update_loop)

    def load_model(self, file_path):
        self.yolo_model = YOLO(file_path)
        self.gui.update_model_status(f"Modelo carregado: {file_path}")
        print(f"Modelo carregado: {file_path}")
        self.gui.enable_toggle()