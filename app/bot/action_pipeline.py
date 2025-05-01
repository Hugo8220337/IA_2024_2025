from typing import List
from bot.handlers.action_handler import ActionHandler
from utils.frame_utils import Detection

class ActionPipeline:
    def __init__(self) -> None:
        self.handlers: List[ActionHandler] = []
    
    def add_handler(self, handler: ActionHandler) -> None:
        self.handlers.append(handler)
    
    def process(self, detections: List[Detection], image) -> None:
        # Each handler processes the detections
        for handler in self.handlers:
            handler.handle(detections, image)