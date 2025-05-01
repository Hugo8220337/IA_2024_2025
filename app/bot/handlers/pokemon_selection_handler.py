from typing import List
from bot.handlers.action_handler import ActionHandler
from utils.frame_utils import Detection

class PokemonSelectionDetectionHandler(ActionHandler):
    def _is_choosing_pokemon(self, detections: List[Detection]) -> bool:
        """
        Check if the detection indicates a battle.
        Returns True if at least 3 valid battle signals are detected.
        """
        battle_buttons = {"pokemon1", "pokemon2", "pokemon3", "pokemon4", "pokemon5", "pokemon6"}
        positives = sum(
            1 for detection in detections
            if detection.confidence >= 0.7 and detection.name.lower() in battle_buttons
        )
        return positives >= 1
    
    def handle(self, detections: List[Detection], image) -> None:
        if not self._is_choosing_pokemon(detections):
            return
        
        # Perform battle detection actions
        print("Pokemon selection detected!")