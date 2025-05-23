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
OLLAMA_MODEL = "mistral"  # Default model for OLLAMA

"""
Prompt for LLM
"""
POKEMON_BATTLE_PROMPT = (
    "You're in a Pokémon HeartGold battle with these options: Fight, Pokémon, and Run.\n"
    "Reply with only one of the following (no explanations):\n"
    "- fight_button: Default choice.\n"
    "- pokemon_button: Switch if your Pokémon is weak to enemy's type\n"
    "- run_button: Only if you can't win\n\n"
    "Some info may be vague—use your best judgment.\n\n"
    "Situation:\n"
    "Enemy Pokémon: {enemy_pokemon}\n"
    "Your active Pokémon: {my_pokemon}"
)

POKEMON_ATTACK_PROMPT = (
    "You are playing Pokémon and must choose the single best attack out of four options based on type matchups. "
    "Select ONLY ONE attack not list multiple choices. NO EXPLANATION, JUST ONE WORD\n"
    "If any attack names are misspelled or unclear, try to infer and use the correct names.\n\n"
    "Respond strictly with: attack1, attack2, attack3, or attack4. No extra text.\n\n"
    "Enemy Pokémon: {enemy_pokemon}\n"
    "Your Pokémon: {my_pokemon}\n"
    "Available attacks: {attacks}"
)

POKEMON_SELECTION_PROMPT = (
    "You're in a Pokémon battle and must switch to the best option from your team.\n"
    "Choose based on type matchups and the current situation.\n"
    "Respond strictly with ONLY ONE of the following: {allowed_labels_str}. NO EXPLANATION.\n"
    "If any Pokémon names are misspelled or unclear, try to infer and use the correct names.\n\n"
    "Enemy Pokémon: {enemy_pokemon}\n"
    "Current Pokémon: {my_pokemon}\n"
    "Available Team: {pokemons}"
)