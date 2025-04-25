import cv2
from ultralytics import YOLO
from utils.config import Config
from utils.frame_utils import capture_screenshot, process_frame, save_frame

class BotController:
    def __init__(self, gui):
        self.gui = gui
        
        self.config = Config.get_instance("config.json")
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

        screenshot_delay = self.config.get("screenshot_delay", 4000)
        screenshot_cv = capture_screenshot()
        frame_to_show = process_frame(screenshot_cv, self.yolo_model)
        self.gui.update_image(frame_to_show)
        save_frame(frame_to_show, self.config)
        self.gui.root.after(screenshot_delay, self.update_loop)

    def load_model(self, file_path):
        self.yolo_model = YOLO(file_path)
        self.gui.update_model_status(f"Modelo carregado: {file_path}")
        print(f"Modelo carregado: {file_path}")
        self.gui.enable_toggle()