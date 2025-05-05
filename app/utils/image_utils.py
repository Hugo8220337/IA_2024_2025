import os
from datetime import datetime
import cv2
from PIL import Image

def save_screenshot(screenshot, save_path: str) -> None:
    """
    Saves the screenshot to the specified path.
    If the path does not exist, it creates the directory.
    
    Args:
        screenshot: The screenshot to save. Can be a PIL Image or a numpy array (BGR format).
        save_path: The directory where the screenshot will be saved.
    """
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


def scale_coordinates(
        x: float,
        y: float,
        img_width: float,
        img_height: float,
        screen_width: float,
        screen_height: float
) -> tuple[int, int]:
    """
    Scale the coordinates from the image size to the screen size.
    
    Args:
        x: The x-coordinate to scale.
        y: The y-coordinate to scale.
        img_width: The width of the image.
        img_height: The height of the image.
        screen_width: The width of the screen.
        screen_height: The height of the screen.
        
    Returns:
        A tuple containing the scaled x and y coordinates.
    """
    x_scaled = int(x * (screen_width / img_width))
    y_scaled = int(y * (screen_height / img_height))
    return x_scaled, y_scaled

def calculate_middle(x_min: int, y_min: int, x_max: int, y_max: int) -> tuple[int, int]:
    """
    Calculate the middle coordinates of a bounding box.
    
    Args:
        x_min: Minimum x-coordinate of the bounding box.
        y_min: Minimum y-coordinate of the bounding box.
        x_max: Maximum x-coordinate of the bounding box.
        y_max: Maximum y-coordinate of the bounding box.
        
    Returns:
        A tuple containing the middle x and y coordinates.
    """
    return (x_min + x_max) // 2, (y_min + y_max) // 2