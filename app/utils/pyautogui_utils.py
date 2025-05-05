import pyautogui
import time

def perform_click(x, y):
    """
    Perform a click at the specified coordinates (x, y).
    """
    pyautogui.moveTo(x, y, duration=0.3)
    pyautogui.mouseDown()
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.mouseUp()