from ultralytics import YOLO
from bot.handlers.pokemon_selection_handler import PokemonSelectionDetectionHandler
from bot.action_pipeline import ActionPipeline
from bot.handlers.attack_detetion_handler import AttackDetectionHandler
from bot.handlers.batle_detection_handler import BattleDetectionHandler
from utils.contants import CONFIG_SCREENSHOT_DEFAULT_DELAY
from utils.config import Config

import utils.frame_utils as frame_utils

class BotController:
    def __init__(self, gui, configs: Config):
        self.gui = gui
        self.configs = configs

        self.running = False
        self.yolo_model = None

        # Initialize the action pipeline
        self.action_pipeline = ActionPipeline()
        self.action_pipeline.add_handler(BattleDetectionHandler())
        self.action_pipeline.add_handler(AttackDetectionHandler())
        self.action_pipeline.add_handler(PokemonSelectionDetectionHandler())


    def start_bot(self):
        """
        Start the bot by capturing a screenshot and processing it with the YOLO model.
        """
        self.running = True
        self.update_loop()
    
    def stop_bot(self):
        """
        Stop the bot by setting the running state to False.
        """
        self.running = False

    def update_loop(self):
        """
        Main loop for the bot. It captures a screenshot, processes it with the YOLO model,
        and updates the GUI with the processed image.
        """
        if not self.running:
            return

        # Get the delay for taking screenshots from the configuration
        screenshot_delay = self.configs.get("screenshot_delay", CONFIG_SCREENSHOT_DEFAULT_DELAY)
        
        # Capture a screenshot of the current screen
        screenshot_cv = frame_utils.capture_screenshot()
        
        # Process the screenshot using the YOLO model
        frame_to_show, detections = frame_utils.process_frame(screenshot_cv, self.yolo_model)
        
        # Update the GUI with the processed image
        self.gui.update_image(frame_to_show)
        
        # Save the processed frame to a file
        frame_utils.save_frame(frame_to_show, self.configs)

        # Process the detections through the action pipeline
        self.action_pipeline.process(detections, screenshot_cv)
            
        # Schedule the next iteration of the loop after the specified delay
        self.gui.get_root().after(screenshot_delay, self.update_loop)

    def load_model(self, file_path):
        """
        Load the YOLO model from the specified file path.
        """
        # Load the YOLO model
        self.yolo_model = YOLO(file_path)

        # Update the GUI with the loaded model status
        self.gui.update_model_status(f"Model loaded: {file_path}")
        self.gui.enable_toggle() 
