"""
Constants for the application
"""
CONFIG_INSTANCE = "config.json" # Configuration file path
CONFIG_SCREENSHOT_DEFAULT_DELAY = 4000  # 4 seconds
CONFIG_SCREENSHOT_DEFAULT_OPTION = True  # Default option to save screenshots
CONFIG_SCREENSHOT_DEFAULT_PATH = "./screenshots" # A directory that always exists on Windows systems
CONFIG_SHOW_TAKEN_SCREENSHOTS = True  # Default option to show taken screenshots
"""
Constants for image processing
"""
ATTACK_TEXT_X1_OFFSET = 32  # Offset added to the left coordinate
ATTACK_TEXT_Y1_OFFSET = 37  # Offset added to the top coordinate
ATTACK_TEXT_X2_OFFSET = 36  # Offset subtracted from the right coordinate
ATTACK_TEXT_Y2_OFFSET = 69  # Offset subtracted from the bottom coordinate

POKEMON_TEXT_X1_OFFSET = 79  # Offset added to the left coordinate
POKEMON_TEXT_Y1_OFFSET = 23  # Offset added to the top coordinate
POKEMON_TEXT_X2_OFFSET = 44  # Offset subtracted from the right coordinate
POKEMON_TEXT_Y2_OFFSET = 64  # Offset subtracted from the bottom coordinate

"""
Constants for OLLAMA
""" 
OLLAMA_MODEL_ENDPOINT = "http://localhost:11434/api/generate"  # End point for OLLAMA
OLLAMA_MODEL = "tinyllama"  # Default model for OLLAMA

"""
Prompt for LLM
"""
POKEMON_BATTLE_PROMPT = (
    "You are playing Pokémon HeartGold and are currently on the battle screen with four options available: "
    "Fight, Bag, Pokémon, and Run. Based on the provided situation, decide the best action to take.\n\n"
    "You must respond with only one of the following options:\n\n"
    "- fight_button – if the best action is to attack the opponent.\n\n"
    "- pokemon_button – if the best action is to switch to another Pokémon.\n\n"
    "- run_button – if the best action is to flee the battle.\n\n"
    "- bag_button – if the best action is to use an item from your bag.\n\n"
    "Some information may be missing, vague, or poorly written. Always try to interpret the context and choose the best option.\n\n"
    "Respond with only the button name (fight_button, pokemon_button, run_button, or bag_button). No explanations or additional text.\n\n"
    "Situation: {data}\n\n"
    "Action:"
)