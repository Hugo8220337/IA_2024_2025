import cv2
import numpy as np
import pyautogui
from utils.contants import CONFIG_SCREENSHOT_DEFAULT_PATH
from utils import image_utils
from dataclasses import dataclass


def capture_screenshot():
    """
    Captures the screen and converts the image to OpenCV's BGR format.
    """
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)



@dataclass
class Detection:
    coordinates: np.ndarray # [x_min, y_min, x_max, y_max]
    image_size: tuple[int, int] # (width, height)
    confidence: float
    name: str

def process_frame(screenshot_cv, yolo_model=None) -> tuple[any, list]:
    """
    Processes the screenshot frame with the YOLO model (if provided) and returns:
      - a modified frame (with overlaid detections, if any)
      - a list of detection objects containing coordinates, confidence and name

    :param screenshot_cv: The screenshot image in OpenCV BGR format.
    :param yolo_model: YOLO model instance for processing the image.
    :return: Tuple containing the processed image and a list of detections.
    """
    # Create a copy of the original screenshot to draw on
    frame_to_show = screenshot_cv.copy()
    # List to accumulate detection results
    detections = []

    # Process the frame if a valid YOLO model is provided
    if yolo_model:
        # Run the YOLO model on the screenshot
        results = yolo_model(screenshot_cv)

        # Check if there are results from the model
        if results and len(results) > 0:
            # Get the first result in case of batch processing
            r0 = results[0]
            # Ensure the detection results (bounding boxes) exist
            if r0.boxes.xyxy is not None:
                # Retrieve bounding boxes, confidence scores, and class predictions
                boxes = r0.boxes.xyxy.cpu().numpy()
                confidences = r0.boxes.conf.cpu().numpy()
                classes = r0.boxes.cls.cpu().numpy().astype(int)
                # Obtain the mapping from class indices to names, default to {} if not available
                class_names = yolo_model.names if hasattr(yolo_model, 'names') else {}
                
                # Iterate over each detection's components
                for box, conf, cls in zip(boxes, confidences, classes):
                    name = class_names.get(cls, "Unknown")  # Get the class name using the index
                    # Create a Detection dataclass instance to store all details
                    detection = Detection(
                        coordinates=box,
                        image_size=screenshot_cv.shape[:2],  # (height, width)
                        confidence=conf,
                        name=name
                    )
                    detections.append(detection)
                
                # Generate a visual representation of the detections on the frame
                frame_to_show = r0.plot()

    # Return the processed frame and the list of detection details
    return frame_to_show, detections

def save_frame(frame, configs):
    """
    Saves the frame if the option is enabled in the configuration.
    """
    is_screenshots_active = configs.get("save_screenshots", True)
    if is_screenshots_active:
        save_path = configs.get("screenshot_path", CONFIG_SCREENSHOT_DEFAULT_PATH)
        image_utils.save_screenshot(frame, save_path)