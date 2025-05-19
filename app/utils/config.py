from utils.contants import CONFIG_INSTANCE, CONFIG_SCREENSHOT_DEFAULT_DELAY, CONFIG_SCREENSHOT_DEFAULT_OPTION, CONFIG_SCREENSHOT_DEFAULT_PATH, CONFIG_SHOW_TAKEN_SCREENSHOTS

import json
import os

"""
This module provides a singleton class for managing application configuration settings.
The configuration is stored in a JSON file, and the class provides methods to load,
get, set, and save configuration settings.
"""
class Config:
    _instance = None

    def __init__(self, config_file=CONFIG_INSTANCE):
        if Config._instance is not None:
            raise Exception("This class is a singleton!")
        
        self.config_file = config_file
        self.settings = {}

        self.load_config()
        Config._instance = self

    @classmethod
    def get_instance(cls, config_file=CONFIG_INSTANCE):
        """
        Returns the singleton instance of the Config class.
        If the instance does not exist, it creates one with the provided config_file.
        """
        if cls._instance is None:
            cls._instance = Config(config_file)
        return cls._instance

    def load_config(self):
        """
        Loads the configuration from the config file.
        If the file does not exist, it creates a new one with default settings.
        """

        if os.path.exists(self.config_file):
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        else:
            # File not found: create with default settings
            self.settings = {
                "screenshot_delay": CONFIG_SCREENSHOT_DEFAULT_DELAY,
                "save_screenshots": CONFIG_SCREENSHOT_DEFAULT_OPTION,
                "screenshot_path": CONFIG_SCREENSHOT_DEFAULT_PATH,  # A directory that always exists on Windows systems
                "show_taken_screenshots": CONFIG_SHOW_TAKEN_SCREENSHOTS,
            }
            self.save()

    def get(self, key, default=None):
        """
        Returns the value of the specified key from the settings.
        If the key does not exist, it returns the default value.
        """
        return self.settings.get(key, default)

    def set(self, key, value):
        """
        Sets the value of the specified key in the settings.
        If the key does not exist, it adds it to the settings.
        If the value is None, it removes the key from the settings.
        """
        self.settings[key] = value
        self.save()

    def save(self):
        """
        Saves the current settings to the config file.
        """
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self.settings, f, indent=4)