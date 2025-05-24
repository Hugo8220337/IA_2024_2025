from typing import List

import numpy
from utils import image_utils, pyautogui_utils
from utils.ollama_utils import call_ollama
from bot.handlers.BaseDetectionHandler import BaseDetectionHandler
from bot.handlers.action_handler import ActionHandler
from utils.contants import ATTACK_TEXT_X1_OFFSET, ATTACK_TEXT_X2_OFFSET, ATTACK_TEXT_Y1_OFFSET, ATTACK_TEXT_Y2_OFFSET, POKEMON_ATTACK_PROMPT
from utils.frame_utils import Detection
from utils import ocr_utils

class AttackDetectionHandler(ActionHandler, BaseDetectionHandler):
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
    
    def _get_attacks_json(self, detections: List[Detection], image: numpy.ndarray) -> dict:
        attacks = {}
        attack_boxes = {}

        # Collect original attack boxes (no offset)
        for det in detections:
            if det.confidence >= 0.5 and det.name.lower().startswith("attack"):
                attacks[det.name] = {"name": det.name, "type": ""}
                attack_boxes[det.name] = det.coordinates

        # Assign types to attacks based on spatial inclusion
        for det in detections:
            if det.confidence >= 0.5 and det.name.lower().startswith("type"):
                for attack_name, box in attack_boxes.items():
                    if image_utils.is_inside(det.coordinates, box):
                        attacks[attack_name]["type"] = det.name
                        break

        # Adjust boxes for better OCR reading
        coords_list = [
            [
                int(box[0]) + ATTACK_TEXT_X1_OFFSET,
                int(box[1]) + ATTACK_TEXT_Y1_OFFSET,
                int(box[2]) - ATTACK_TEXT_X2_OFFSET,
                int(box[3]) - ATTACK_TEXT_Y2_OFFSET,
            ]
            for box in attack_boxes.values()
        ]

        # Read texts via OCR
        texts = ocr_utils.read_texts_in_squares([image] * len(coords_list), coords_list)

        # Update attack names from OCR text
        for attack_name, text in zip(attack_boxes.keys(), texts):
            lines = [line.strip() for line in text.splitlines() if line.strip()] if text else []
            if lines:
                attacks[attack_name]["name"] = " ".join(lines)

        return {"attacks": attacks}

        
 
    def handle(self, detections: List[Detection], image) -> None:
        if not self._is_attacking(detections):
            return

        print("Attack detected!")

        my_name = self.get_my_pokemon_name(detections)
        enemy_name = self.get_enemy_pokemon_name(detections)

        attacks_json = self._get_attacks_json(detections, image)

        # Convert the attacks JSON to a string format for the prompt
        prompt = POKEMON_ATTACK_PROMPT.format(
            enemy_pokemon=enemy_name,
            my_pokemon=my_name,
            attacks=attacks_json
        )
        response = call_ollama(prompt=prompt).lower()

        def click_attack(attack_label: str) -> bool:
            attack_button = next((a for a in detections if a.name.lower() == attack_label), None)
            if attack_button:
                x_min, y_min, x_max, y_max = attack_button.coordinates
                x, y = image_utils.calculate_middle(x_min, y_min, x_max, y_max)
                pyautogui_utils.perform_click(x, y)
                return True
            return False

        # Try to click the detected attack in the response
        selected_attack = next((label for label in attacks_json["attacks"] if label in response), None)

        if selected_attack and click_attack(selected_attack):
            return
        
        # Fallback: click "attack1" by default
        if not click_attack("attack1"):
            print("No valid attack button found to click.")
