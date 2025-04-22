import tkinter as tk
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
from utils.config import Config
from gui.menu_bar import MenuBar
import pyautogui
from ultralytics import YOLO

class PokeMMOBotApp:
    def __init__(self, root):
        self.root = root

        # Carregar configuração usando a classe Config.
        self.config = Config.get_instance("config.json")

        self.root.title("PokeNoob - Bot for noobs")
        self.running = False
        self.status_text = tk.StringVar(value="Inativo")
        self.model_status_text = tk.StringVar(value="Nenhum modelo carregado")
        self.yolo_model = None
        self.setup_gui()
        self.menu_bar = MenuBar(self.root, self)

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack()
        ttk.Label(frame, textvariable=self.model_status_text, foreground="blue").pack(pady=5)
        self.label_img = ttk.Label(frame)
        self.label_img.pack(pady=10)
        # Disable the activate button until a model is loaded.
        self.btn_toggle = ttk.Button(frame, text="Ativar", command=self.toggle_bot, state=tk.DISABLED)
        self.btn_toggle.pack()
        ttk.Label(frame, textvariable=self.status_text).pack(pady=5)

    def toggle_bot(self):
        self.running = not self.running
        self.status_text.set("Ativo" if self.running else "Inativo")
        self.btn_toggle.config(text="Desativar" if self.running else "Ativar")
        print("Bot iniciado!" if self.running else "Bot parado!")
        if self.running:
            self.update_loop()

    def update_loop(self):
        if not self.running:
            return

        # Get the screenshot delay from the configuration (default to 4000ms if not set)
        screenshot_delay = self.config.get("screenshot_delay", 4000)

        # Capture a screenshot and convert it to OpenCV format (BGR)
        screenshot = pyautogui.screenshot()
        screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Start with the original screenshot as the frame to display
        frame_to_show = screenshot_cv

        # If a YOLO model is loaded, perform object detection
        if self.yolo_model is not None:
            results = self.yolo_model(screenshot_cv)
            if results and len(results) > 0:
                # Get bounding boxes from the results (if available)
                boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes.xyxy is not None else np.array([])
                if boxes.size > 0:
                    print(f"Detected {len(boxes)} objects:")
                    for i, box in enumerate(boxes):
                        print(f"  -- Object {i+1}: {box}")
                # Update the frame with detection overlays
                frame_to_show = results[0].plot()


        # Update the GUI with the new image
        self.update_image(frame_to_show)

        # Schedule the next update
        self.root.after(screenshot_delay, self.update_loop)

    def update_image(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb_image).resize((800, 480))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.label_img.imgtk = img_tk  # Prevent garbage collection.
        self.label_img.config(image=img_tk)

    def load_model(self, file_path):
        self.yolo_model = YOLO(file_path)
        self.model_status_text.set(f"Modelo carregado: {file_path}")
        print(f"Modelo carregado: {file_path}")
        # Enable the activate button once a model is loaded.
        self.btn_toggle.config(state=tk.NORMAL)