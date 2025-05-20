from typing import Dict, List

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
        """
        Extract attack names and types from detections using batch OCR.
        If the OCR result does not capture a type, searches for a detection whose name
        starts with "type" within the attack detection's coordinates.
        Returns:
        {
            "attacks": {
                "attack1": {"name": "", "type": ""},
                ...
            }
        }
        """
        attacks = {}
        coords_list = []
        valid_attack_detections = []

        for detection in detections:
            if detection.confidence < 0.5 or not detection.name.lower().startswith("attack"):
                continue

            x1 = int(detection.coordinates[0]) + ATTACK_TEXT_X1_OFFSET
            y1 = int(detection.coordinates[1]) + ATTACK_TEXT_Y1_OFFSET
            x2 = int(detection.coordinates[2]) - ATTACK_TEXT_X2_OFFSET
            y2 = int(detection.coordinates[3]) - ATTACK_TEXT_Y2_OFFSET
            coords_list.append([x1, y1, x2, y2])
            valid_attack_detections.append(detection)

        if not coords_list:
            return {"attacks": {}}

        # Create a list of images (same image repeated for each region) and perform batch OCR.
        images_list = [image] * len(coords_list)
        texts = ocr_utils.read_texts_in_squares(images_list, coords_list)

        attack_num = 1
        for detection, text in zip(valid_attack_detections, texts):
            if text:
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                if lines:
                    if len(lines) >= 2:
                        name = " ".join(lines[:-1])
                        atype = lines[-1]
                    else:
                        name = lines[0]
                        atype = ""
                else:
                    name, atype = "", ""
            else:
                name, atype = "", ""

            # If OCR did not detect a type, try to find a secondary detection with a "type" prefix.
            if not atype:
                for other in detections:
                    if other.name.lower().startswith("type"):
                        if image_utils.is_inside(other.coordinates, detection.coordinates):
                            atype = other.name.lower().replace("type", "").strip("_ ")
                            break

            attacks[f"attack{attack_num}"] = {"name": name, "type": atype}
            attack_num += 1

        return {"attacks": attacks}
    
    def handle(self, detections: List[Detection], image) -> None:
        if not self._is_attacking(detections):
            return

        print("Attack detected!")

        my_name = self.get_my_pokemon_name(detections)
        enemy_name = self.get_enemy_pokemon_name(detections)

        attacks_json = self._get_attacks_json(detections, image)

        prompt = POKEMON_ATTACK_PROMPT.format(
            enemy_pokemon=enemy_name,
            my_pokemon=my_name,
            attacks=attacks_json
        )
        response = call_ollama(prompt=prompt).lower()

        # Verify if the response contains any of the buttons
        selected_attack = next((label for label in attacks_json["attacks"] if label in response), None)
        
        if selected_attack:
            attack_button = next((attack for attack in detections if attack.name.lower() == selected_attack), None)
            if attack_button:
                x_min, y_min, x_max, y_max = attack_button.coordinates
                x, y = image_utils.calculate_middle(x_min, y_min, x_max, y_max)
                pyautogui_utils.perform_click(x, y)
            else:
                print("Coordinates not found for selected attack!")
        else:
            print("Unknown action detected!")        