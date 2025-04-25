import tkinter as tk
from tkinter import filedialog

class MenuBar:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.menu = tk.Menu(root)
        self.root.config(menu=self.menu)
        self.create_menu()

    def create_menu(self):
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Selecionar Modelo", command=self.select_model)
        self.menu.add_cascade(label="File", menu=file_menu)
        
        # Add Options menu
        options_menu = tk.Menu(self.menu, tearoff=0)
        options_menu.add_command(label="Editar Configurações", command=self.open_options)
        self.menu.add_cascade(label="Opções", menu=options_menu)

    def select_model(self):
        file_path = filedialog.askopenfilename(
            title="Selecionar Modelo YOLO",
            filetypes=[("Model Files", "*.pt"), ("All Files", "*.*")]
        )
        if file_path:
            self.app.load_model(file_path)

    def open_options(self):
        # Create a new window for options
        options_win = tk.Toplevel(self.root)
        options_win.title("Opções de Configuração")
        options_win.geometry("350x250")

        # Label and entry for screenshot delay
        tk.Label(options_win, text="Intervalo entre screenshots (ms):").pack(pady=5)
        delay_var = tk.StringVar(value=str(self.app.config.get("screenshot_delay", 4000)))
        delay_entry = tk.Entry(options_win, textvariable=delay_var)
        delay_entry.pack(pady=5)

        # Checkbox for save_screenshots
        save_var = tk.BooleanVar(value=self.app.config.get("save_screenshots", True))
        tk.Checkbutton(options_win, text="Guardar screenshots", variable=save_var).pack(pady=5)

        # Label, entry and button for screenshot_path
        tk.Label(options_win, text="Caminho para salvar screenshots:").pack(pady=5)
        screenshot_path_var = tk.StringVar(value=self.app.config.get("screenshot_path", "C:\\Users\\hugui\\Documents\\GitHub\\IA_2024_2025\\screenshots"))
        screenshot_path_entry = tk.Entry(options_win, textvariable=screenshot_path_var, width=40)
        screenshot_path_entry.pack(pady=5)
        def browse_path():
            directory = filedialog.askdirectory(initialdir=screenshot_path_var.get())
            if directory:
                screenshot_path_var.set(directory)
        tk.Button(options_win, text="Selecionar Pasta", command=browse_path).pack(pady=5)

        # Save button: update config and write to file
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
