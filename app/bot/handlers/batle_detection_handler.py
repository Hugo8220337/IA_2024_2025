import numpy
from typing import List
from utils import pyautogui_utils
from bot.handlers.action_handler import ActionHandler
from utils import image_utils
from utils.frame_utils import Detection

class BattleDetectionHandler(ActionHandler):
    def _is_in_battle(self, detections: List[Detection]) -> bool:
        """
        Check if the detection indicates a battle.
        Returns True if at least 3 valid battle signals are detected.
        """
        battle_buttons = {"fight_button", "bag_button", "nun_button", "pokemon_button"}
        positives = sum(
            1 for detection in detections
            if detection.confidence >= 0.5 and detection.name.lower() in battle_buttons
        )
        return positives >= 3
    
    def _get_battle_buttons(self, detections: List[Detection]) -> dict[str, Detection]:
        """
        Get the coordinates of the battle buttons from the detections.
        Returns a dictionary with button names as keys and their coordinates as values.
        """
        battle_buttons = {"fight_button": None, "bag_button": None, "nun_button": None, "pokemon_button": None}
        
        for detection in detections:
            if detection.name.lower() in battle_buttons:
                battle_buttons[detection.name.lower()] = detection
        
        return battle_buttons
    
    def handle(self, detections: List[Detection], image: numpy.ndarray) -> None:
        if not self._is_in_battle(detections):
            return
        
        print("Battle detected!")


        # Process the battle buttons
        buttons = self._get_battle_buttons(detections)
        fight_button = buttons.get("fight_button")
        
        x_min, y_min, x_max, y_max = fight_button.coordinates

        
        x, y = image_utils.calculate_middle(x_min, y_min, x_max, y_max)

        pyautogui_utils.perform_click(x, y)