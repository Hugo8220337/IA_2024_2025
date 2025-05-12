from utils.contants import CONFIG_INSTANCE, CONFIG_SCREENSHOT_DEFAULT_DELAY, CONFIG_SCREENSHOT_DEFAULT_OPTION, CONFIG_SCREENSHOT_DEFAULT_PATH
import tkinter as tk
from utils.config import Config
from tkinter import filedialog

class OptionsTab:
    def __init__(self, root: tk, configs: Config):
        self.root = root
        self.configs = configs

    def open_options(self):
        options_win = tk.Toplevel(self.root)
        options_win.title("Opções de Configuração")
        options_win.geometry("350x300")

        # Set default value for screenshot_delay input
        screenshot_delay = self.configs.get("screenshot_delay", CONFIG_SCREENSHOT_DEFAULT_DELAY)
        tk.Label(options_win, text="Intervalo entre screenshots (ms):").pack(pady=5)
        delay_var = tk.StringVar(value=str(screenshot_delay))
        tk.Entry(options_win, textvariable=delay_var).pack(pady=5)

        # Set default value for save_screenshots checkbox
        save_screenshots = self.configs.get("save_screenshots", CONFIG_SCREENSHOT_DEFAULT_OPTION)
        save_var = tk.BooleanVar(value=save_screenshots)
        tk.Checkbutton(options_win, text="Guardar screenshots", variable=save_var).pack(pady=5)

        # Screenshot path input
        screenshot_path = self.configs.get("screenshot_path", CONFIG_SCREENSHOT_DEFAULT_PATH)
        tk.Label(options_win, text="Caminho para guardar screenshots:").pack(pady=5)
        screenshot_path_var = tk.StringVar(value=screenshot_path)
        tk.Entry(options_win, textvariable=screenshot_path_var, width=40).pack(pady=5)
        
        # Button to browse for directory
        def browse_path():
            directory = filedialog.askdirectory(initialdir=screenshot_path_var.get())
            if directory:
                screenshot_path_var.set(directory)
        tk.Button(options_win, text="Selecionar Pasta", command=browse_path).pack(pady=5)

        # Button to save the configuration
        def save_config():
            try:
                self.configs.set("screenshot_delay", int(delay_var.get()))
                self.configs.set("save_screenshots", save_var.get())
                self.configs.set("screenshot_path", screenshot_path_var.get())
                options_win.destroy() # Close the options window
            except ValueError:
                tk.messagebox.showerror("Erro", "Por favor, insira um número válido para o intervalo de screenshots.")
        tk.Button(options_win, text="Guardar", command=save_config).pack(pady=10)