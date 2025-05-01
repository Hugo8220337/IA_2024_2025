from typing import List
from bot.handlers.action_handler import ActionHandler
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
    
    def handle(self, detections: List[Detection]) -> None:
        if not self._is_in_battle(detections):
            return
        
        # Perform battle detection actions
        print("Battle detected!")
        
        