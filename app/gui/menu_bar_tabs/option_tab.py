import tkinter as tk
from tkinter import filedialog

class OptionsTab:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def open_options(self):
        options_win = tk.Toplevel(self.root)
        options_win.title("Opções de Configuração")
        options_win.geometry("350x250")

        tk.Label(options_win, text="Intervalo entre screenshots (ms):").pack(pady=5)
        delay_var = tk.StringVar(value=str(self.app.config.get("screenshot_delay", 4000)))
        tk.Entry(options_win, textvariable=delay_var).pack(pady=5)

        save_var = tk.BooleanVar(value=self.app.config.get("save_screenshots", True))
        tk.Checkbutton(options_win, text="Guardar screenshots", variable=save_var).pack(pady=5)

        tk.Label(options_win, text="Caminho para salvar screenshots:").pack(pady=5)
        screenshot_path_var = tk.StringVar(value=self.app.config.get("screenshot_path", "C:\\Users\\hugui\\Documents\\GitHub\\IA_2024_2025\\screenshots"))
        tk.Entry(options_win, textvariable=screenshot_path_var, width=40).pack(pady=5)
        
        def browse_path():
            directory = filedialog.askdirectory(initialdir=screenshot_path_var.get())
            if directory:
                screenshot_path_var.set(directory)
        tk.Button(options_win, text="Selecionar Pasta", command=browse_path).pack(pady=5)

        def save_config():
            try:
                new_delay = int(delay_var.get())
                self.app.config.settings["screenshot_delay"] = new_delay
                self.app.config.settings["save_screenshots"] = save_var.get()
                self.app.config.settings["screenshot_path"] = screenshot_path_var.get()
                self.app.config.save()
                print("Configuração atualizada!")
                options_win.destroy()
            except ValueError:
                print("Informe um número válido para o delay!")
        tk.Button(options_win, text="Guardar", command=save_config).pack(pady=10)