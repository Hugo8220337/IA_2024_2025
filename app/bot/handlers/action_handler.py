from typing import List
from utils.frame_utils import Detection

"""
Base class for handling actions based on detections.
This class defines the interface for handling actions based on the detections
detected by the YOLO model.
"""
class ActionHandler:
    def handle(self, detections: List[Detection]) -> None:
        """
        Process the list of detections.
        """
        pass