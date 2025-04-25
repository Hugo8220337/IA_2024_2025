from utils.contants import CONFIG_INSTANCE, CONFIG_SCREENSHOT_DEFAULT_DELAY, CONFIG_SCREENSHOT_DEFAULT_OPTION, CONFIG_SCREENSHOT_DEFAULT_PATH

import json
import os


class Config:
    _instance = None

    def __init__(self, config_file=CONFIG_INSTANCE):
        if Config._instance is not None:
            raise Exception("Esta classe é um singleton!")
        
        self.config_file = config_file
        self.settings = {}

        self.load_config()
        Config._instance = self

    @classmethod
    def get_instance(cls, config_file=CONFIG_INSTANCE):
        if cls._instance is None:
            cls._instance = Config(config_file)
        return cls._instance

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        else:
            # File not found: create with default settings
            self.settings = {
                "screenshot_delay": CONFIG_SCREENSHOT_DEFAULT_DELAY,
                "save_screenshots": CONFIG_SCREENSHOT_DEFAULT_OPTION,
                "screenshot_path": CONFIG_SCREENSHOT_DEFAULT_PATH  # A directory that always exists on Windows systems
            }
            self.save()

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def save(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)