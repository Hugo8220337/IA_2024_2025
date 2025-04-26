import cv2
import numpy as np
import pyautogui
from utils.contants import CONFIG_SCREENSHOT_DEFAULT_PATH
from utils import image_utils

def capture_screenshot():
    """
    Captures the screen and converts the image to OpenCV's BGR format.
    """
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def process_frame(screenshot_cv, yolo_model=None):
    """Performs object detection (if the model is loaded)
    and returns the resulting frame for display."""
    frame_to_show = screenshot_cv.copy()

    if yolo_model:
        results = yolo_model(screenshot_cv)

        if results and len(results) > 0:
            boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes.xyxy is not None else np.array([])
            if boxes.size > 0:
                print(f"Detected {len(boxes)} objects:")
                for i, box in enumerate(boxes):
                    print(f"  -- Object {i+1}: {box}")
            frame_to_show = results[0].plot()

    return frame_to_show

def save_frame(frame, configs):
    """
    Saves the frame if the option is enabled in the configuration.
    """
    is_screenshots_active = configs.get("save_screenshots", True)
    if is_screenshots_active:
        save_path = configs.get("screenshot_path", CONFIG_SCREENSHOT_DEFAULT_PATH)
        image_utils.save_screenshot(frame, save_path)