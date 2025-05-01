from typing import List
from bot.handlers.action_handler import ActionHandler
from utils.frame_utils import Detection
from utils import ocr_utils

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
    
    def _get_attack_text(self, detection: Detection, image) -> str:
        """
        Get the attack text from the detection.
        Returns the text if it starts with "attack", otherwise returns None.
        """
        if not detection.name.lower().startswith("attack"):
            return ""

        x1 = detection.coordinates[0]
        x2 = detection.coordinates[2]
        y1 = detection.coordinates[1] // 2
        y2 = detection.coordinates[3] // 2

        return ocr_utils.read_text_in_square(image, [x1, y1, x2, y2])
    
    def handle(self, detections: List[Detection], image) -> None:
        if not self._is_attacking(detections):
            return
        
        print("Attack detected!")


        for detection in detections:
            if detection.name.lower().startswith("attack"):
                attack_text = self._get_attack_text(detection, image)
                print(f"Attack text: {attack_text}")

        