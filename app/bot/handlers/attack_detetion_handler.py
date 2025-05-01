from typing import List
from bot.handlers.action_handler import ActionHandler
from utils.frame_utils import Detection

class AttackDetectionHandler(ActionHandler):
    def _is_attacking(self, detections: List[Detection]) -> bool:
        """
        Check if the detection indicates an attack.
        Returns True if either:
        - at least 3 valid attack button signals are detected, or
        - there is at least one detection with a name starting with "attack" and
            at least one with a name starting with "type".
        """
        attack_buttons = {"attack_button", "special_button", "item_button"}
        positives = sum(
            1 for detection in detections
            if detection.confidence >= 0.5 and detection.name.lower() in attack_buttons
        )
        
        has_attack_prefix = any(
            detection.confidence >= 0.5 and detection.name.lower().startswith("attack")
            for detection in detections
        )
        has_type_prefix = any(
            detection.confidence >= 0.5 and detection.name.lower().startswith("type")
            for detection in detections
        )
        
        return positives >= 3 or (has_attack_prefix and has_type_prefix)
    
    def handle(self, detections: List[Detection]) -> None:
        if not self._is_attacking(detections):
            return
        
        # Perform
        print("Attack detected!")