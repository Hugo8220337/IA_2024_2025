import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

class AppGUI:
    def __init__(self, root, bot_controller):
        self.root = root
        self.bot_controller = bot_controller
        self.root.title("PokeNoob - Bot for noobs")
        self.status_text = tk.StringVar(value="Inativo")
        self.model_status_text = tk.StringVar(value="Nenhum modelo carregado")
        self.setup_gui()

    def setup_gui(self):
        frame = ttk.Frame(self.root, padding=10)
        frame.pack()
        ttk.Label(frame, textvariable=self.model_status_text, foreground="blue").pack(pady=5)
        self.label_img = ttk.Label(frame)
        self.label_img.pack(pady=10)
        self.btn_toggle = ttk.Button(frame, text="Ativar", command=self.toggle_bot, state=tk.DISABLED)
        self.btn_toggle.pack()
        ttk.Label(frame, textvariable=self.status_text).pack(pady=5)

    def toggle_bot(self):
        self.bot_controller.toggle_bot()
        self.status_text.set("Ativo" if self.bot_controller.running else "Inativo")
        self.btn_toggle.config(text="Desativar" if self.bot_controller.running else "Ativar")

    def update_model_status(self, text):
        self.model_status_text.set(text)

    def update_image(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb_image).resize((800, 480))
        img_tk = ImageTk.PhotoImage(img_pil)
        self.label_img.imgtk = img_tk  # Previne a coleta de lixo.
        self.label_img.config(image=img_tk)

    def enable_toggle(self):
        self.btn_toggle.config(state=tk.NORMAL)