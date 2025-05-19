import numpy
import time
from typing import Dict, List
from utils import image_utils, pyautogui_utils
from utils.ollama_utils import call_ollama
from bot.handlers.BaseDetectionHandler import BaseDetectionHandler
from bot.handlers.action_handler import ActionHandler
from utils import ocr_utils
from utils.contants import POKEMON_SELECTION_PROMPT, POKEMON_TEXT_X1_OFFSET, POKEMON_TEXT_X2_OFFSET, POKEMON_TEXT_Y1_OFFSET, POKEMON_TEXT_Y2_OFFSET
from utils.frame_utils import Detection

class PokemonSelectionDetectionHandler(ActionHandler, BaseDetectionHandler):
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
    
    def _get_pokemon_text(self, detection: Detection, image: numpy.ndarray) -> str:
        """
        Get the pokemon text from the detection.
        Returns the text if it starts with "pokemon", otherwise returns None.
        """
        if not detection.name.lower().startswith("pokemon"):
            return ""

        x1 = int(detection.coordinates[0]) + POKEMON_TEXT_X1_OFFSET
        y1 = int(detection.coordinates[1]) + POKEMON_TEXT_Y1_OFFSET
        x2 = int(detection.coordinates[2]) - POKEMON_TEXT_X2_OFFSET
        y2 = int(detection.coordinates[3]) - POKEMON_TEXT_Y2_OFFSET

        # Assuming OCR function is defined elsewhere
        return ocr_utils.read_text_in_square(image, [x1, y1, x2, y2])
    
    def _get_pokemons_json(self, detections: List[Detection], image: numpy.ndarray) -> dict:
        """
        Returns a JSON with the pokemons detected in the selection screen.
        {
            "pokemons": {
                "pokemon1": "pokemonName",
                "pokemon2": "pokemonName",
                ...
                "pokemon6": "pokemonName"
            }
        }
        """
        pokemons = {}
        count = 1
        for detection in detections:
            if detection.name.lower().startswith("pokemon") and count <= 6:
                pokemon_name = self._get_pokemon_text(detection, image)
                if pokemon_name:
                    pokemons[f"pokemon{count}"] = pokemon_name
                    count += 1
        return {"pokemons": pokemons}
    
    def _get_pokemon_labels(self, detections: List[Detection], image: numpy.ndarray) -> Dict[str, Detection]:
        """
        Returns a dictionary mapping pokemon labels (e.g. "pokemon1", "pokemon2", ..., "pokemon6")
        to their corresponding Detection objects.
        """
        pokemon_labels: Dict[str, Detection] = {}
        count = 1
        for detection in detections:
            if detection.name.lower().startswith("pokemon") and count <= 6:
                pokemon_labels[f"pokemon{count}"] = detection
                count += 1
        return pokemon_labels
    
    def _get_back_button(self, detections: List[Detection]) -> Detection:
        """
        Returns the back button detection if found.
        """
        for detection in detections:
            if detection.name.lower() == "back_button":
                return detection
        return None
    
    def handle(self, detections: List[Detection], image: numpy.ndarray) -> None:
        if not self._is_choosing_pokemon(detections):
            return
        
        print("Pokemon selection detected!")

        my_name = self.get_my_pokemon_name(detections)
        enemy_name = self.get_enemy_pokemon_name(detections)
        pokemons = self._get_pokemon_labels(detections, image)
        pokemons_json = self._get_pokemons_json(detections, image)

        prompt = POKEMON_SELECTION_PROMPT.format(
            allowed_labels_str=", ".join(pokemons.keys()),
            enemy_pokemon=enemy_name,
            my_pokemon=my_name,
            pokemons=pokemons_json
        )
        response = call_ollama(prompt=prompt)
        response = response.lower()

        selected_pokemon = next(
            (label for label, name in pokemons_json["pokemons"].items() if name.lower() in response),
            None
        ) 
               
        if not selected_pokemon:
            print("Unknown action detected!")
            return

        target = pokemons[selected_pokemon] if selected_pokemon != "pokemon1" else self._get_back_button(detections)
        if target:
            x, y = image_utils.calculate_middle(*target.coordinates)
            pyautogui_utils.perform_click(x, y)
            if selected_pokemon != "pokemon1":
                time.sleep(0.5)
                pyautogui_utils.perform_click(x, y)
