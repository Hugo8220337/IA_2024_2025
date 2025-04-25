import os
from datetime import datetime
import cv2
from PIL import Image

def save_screenshot(screenshot, save_path: str) -> None:
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(save_path, f"screenshot_{timestamp}.png")
    
    # If screenshot is a PIL Image, it will have a 'save' method.
    if hasattr(screenshot, "save"):
        screenshot.save(file_path)
    else:
        # Otherwise, assume it's a numpy array (BGR format) and convert it.
        screenshot_pil = Image.fromarray(cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB))
        screenshot_pil.save(file_path)