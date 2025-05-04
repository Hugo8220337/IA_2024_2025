import numpy
from typing import List
from bot.handlers.BaseDetectionHandler import BaseDetectionHandler
from bot.handlers.action_handler import ActionHandler
from utils import ocr_utils
from utils.contants import POKEMON_TEXT_X1_OFFSET, POKEMON_TEXT_X2_OFFSET, POKEMON_TEXT_Y1_OFFSET, POKEMON_TEXT_Y2_OFFSET
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
    
    def handle(self, detections: List[Detection], image: numpy.ndarray) -> None:
        if not self._is_choosing_pokemon(detections):
            return
        
        print("Pokemon selection detected!")

        # Iterate through the detections to find pokemons text in the selection screen
        pokemons = []
        for detection in detections:
            if detection.name.lower().startswith("pokemon"):
                pokemon_text = self._get_pokemon_text(detection, image)
                pokemons.append(pokemon_text)
                print(f"Pokemon text: {pokemon_text}")
        
        # Perform battle detection actions