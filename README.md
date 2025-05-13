# IA_2024_2025
This repository contains scripts and applications for training and inference using YOLO models, as well as a bot with a graphical interface for automation and real-time interaction.

## Contents

- **Training Notebooks**  
  - `pokemon_dataset_training.ipynb`: Notebook for downloading the dataset, training, and evaluating the YOLO model for Pokémon detection.  
  - `attack_effectiveness_training.ipynb`: Notebook for training a classification model (Random Forest) that predicts attack effectiveness based on the data in the CSV file `datasets/attack_attempts.csv`.

- **Bot and GUI Application**  
  - The main application is located in `app/main.py`.  
  - The bot uses an action pipeline with handlers to detect battles, attacks, and Pokémon selection from screenshots.  
  - The graphical interface (Tkinter) is defined in `app/gui/app_gui.py`, and the menu bar is in `app/gui/menu_bar.py`.

- **Utilities**  
  - Functions for frame processing, OCR, configuration management, coordinate scaling, and more are located in `app/utils/`.

## Requirements

- Python 3.x  
- Required dependencies are listed in `app/requirements.txt`.

## Installation and Execution Instructions

1. **Clone the Repository and Set Up a Virtual Environment**  
   - Clone the repository:
     ```sh
     git clone https://github.com/Hugo8220337/IA_2024_2025.git
     ```
   - Navigate to the project folder:
     ```sh
     cd IA_2024_2025
     ```
   - Create and activate a virtual environment:
     ```sh
     python -m venv .venv
     # On Windows:
     .venv\Scripts\activate
     # On Linux/Mac:
     source .venv/bin/activate
     ```

2. **Install Dependencies**  
   - Install the required dependencies:
     ```sh
     pip install -r app/requirements.txt
     ```

3. **Environment Configuration**  
   - Rename the file [.env.example](https://github.com/Hugo8220337/IA_2024_2025/blob/dev/.env.example) to `.env` and replace `ROBOFLOW_PRIVATE_API_KEY` with your private key.
   - If needed, modify the `config.json` file or adjust settings through the graphical interface (under the “Options” section) to define parameters such as the path for saving screenshots and the interval between them. Note that the `config.json` file is generated during the program's first execution.

4. **Run Training Notebooks**  
   - Start Jupyter Notebook:
     ```sh
     jupyter notebook
     ```
   - Open and execute the notebooks:
     - [pokemon_dataset_training.ipynb](https://github.com/Hugo8220337/IA_2024_2025/blob/dev/pokemon_dataset_training.ipynb) for training the Pokémon detection model.
     - [attack_effectiveness_training.ipynb](https://github.com/Hugo8220337/IA_2024_2025/blob/dev/attack_effectiveness_training.ipynb) for training the attack effectiveness prediction model.

5. **Run the Bot Application with Graphical Interface**  
   - Run the main application:
     ```sh
     python app/main.py
     ```
   - In the graphical interface, use the “Select Model” option in the **File** menu to load the YOLO model file (e.g., `best.pt` generated after training).
   - After loading the model, activate the bot using the “Activate” button. The bot will periodically capture screenshots, process the images, and execute actions based on the implemented handlers.

## Local Language Model (LLM) Integration

This project integrates a local Large Language Model (LLM) using [**Ollama**](https://ollama.com/) to generate text-based decisions, messages, or support interactions within the bot.

### Model Used

We use the [`phi:chat`](https://ollama.com/library/phi) model, which is lightweight and works well on machines **without a GPU**, making it ideal for development on low-spec systems.

### Running the Model Locally

To run the model locally, first make sure Ollama is installed. Then, pull and run the Phi chat model with:

```sh
ollama run phi:chat
```

## Notes
- Ensure you have the necessary permissions to capture the screen. On Linux systems using the Wayland display server, you may need to configure environment variables, such as DISPLAY, to ensure proper functionality.
- Adjust parameters and offsets (defined in app/utils/contants.py) as needed for your screen and application context.
