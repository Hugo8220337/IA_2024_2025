import cv2
import numpy as np
import pyautogui
from utils import image_utils

def capture_screenshot():
    """Captura o ecrã e converte a imagem para o formato BGR do OpenCV."""
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def process_frame(screenshot_cv, yolo_model=None):
    """Realiza a detecção de objetos (caso o modelo esteja carregado)
    e retorna o frame resultante para exibição."""
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

def save_frame(frame, config):
    """Guarda o frame se a opção estiver ativada na configuração."""
    if config.get("save_screenshots", True):
        save_path = config.get("screenshot_path", "C:\\Windows\\Temp\\screenshots")
        image_utils.save_screenshot(frame, save_path)