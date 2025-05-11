from typing import List
from utils import ocr_utils
from utils.frame_utils import Detection

"""
This class is the parent class used for handling common batle actions.
"""
class BaseDetectionHandler:
    def get_my_level(self, detections: List[Detection], image) -> str:
        """
        Get the level of the Pokemon from the detection.
        Returns the level if it starts with "my_level", otherwise returns None.

        Does not work properly
        """

        for detection in detections:
            if detection.name.lower() == "my_level" and detection.confidence >= 0.5:
                x1 = int(detection.coordinates[0]) # + 26
                y1 = int(detection.coordinates[1])
                x2 = int(detection.coordinates[2]) + 2
                y2 = int(detection.coordinates[3]) + 2

                text = ocr_utils.read_text_in_square(image, [x1, y1, x2, y2])

                return text
        return ''

    def get_enemy_level(self, detections: List[Detection], image) -> str:
        """
        Get the level of the enemy Pokemon from the detection.
        Returns the level if it starts with "enemy_level", otherwise returns None.

        Does not work properly
        """
        for detection in detections:
            if detection.name.lower() == "enemy_level" and detection.confidence >= 0.5:
                x1 = int(detection.coordinates[0]) # + 28
                y1 = int(detection.coordinates[1])
                x2 = int(detection.coordinates[2]) + 2
                y2 = int(detection.coordinates[3]) + 2

                text = ocr_utils.read_text_in_square(image, [x1, y1, x2, y2])

                return text
        return ''

    def get_enemy_pokemon_name(self, detections: List[Detection]) -> str:
        """
        Get the name of the enemy Pokemon from the detection.
        """
        # Filter out detections that are not relevant to Pokemon names
        filtered_detections = [
            detection for detection in detections
            if not detection.name.lower().startswith("attack") and
               not detection.name.lower().startswith("type") and
               not detection.name.lower().endswith("level") and
               not detection.name.lower().endswith("button")
        ]

        if not filtered_detections:
            return None

        # Find the detection with the highest x-coordinate that has a confidence > 0.7
        highest_x_detection = max(
            (d for d in filtered_detections if d.confidence > 0.7),
            key=lambda d: d.coordinates[0]
        )

        return highest_x_detection.name
    
    def get_my_pokemon_name(self, detections: List[Detection]) -> str:
        """
        Get the name of the enemy Pokemon from the detection.
        """
        # Filter out detections that are not relevant to Pokemon names
        filtered_detections = [
            detection for detection in detections
            if not detection.name.lower().startswith("attack") and
               not detection.name.lower().startswith("type") and
               not detection.name.lower().endswith("level") and
               not detection.name.lower().endswith("button")
        ]

        if not filtered_detections:
            return None

        # Find the detection with the lowest x-coordinate that has a confidence > 0.7
        lowest_x_detection = min(
            (d for d in filtered_detections if d.confidence > 0.7),
            key=lambda d: d.coordinates[0]
        )

        return lowest_x_detection.name