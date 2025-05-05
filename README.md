# IA_2024_2025

Este repositório contém scripts e aplicações destinados ao treino e à inferência utilizando modelos YOLO, bem como um bot com interface gráfica para automatização e interação em tempo real.

## Conteúdo

- **Notebooks de Treino**  
  - `pokemon_dataset_training.ipynb`: Notebook para efectuar o download do conjunto de dados, realizar o treino e avaliar o modelo YOLO para deteção de Pokémons.  
  - `attack_effectiveness_training.ipynb`: Notebook para o treino de um modelo de classificação (Random Forest) que prevê a eficácia dos ataques com base nos dados do ficheiro CSV `datasets/attack_attempts.csv`.

- **Aplicação Bot e GUI**  
  - A aplicação principal situa-se em `app/main.py`.  
  - O bot utiliza um pipeline de ações com handlers para detectar batalhas, ataques e a seleção de Pokémon a partir de capturas de ecrã.  
  - A interface gráfica (Tkinter) encontra-se definida em `app/gui/app_gui.py` e a barra de menu em `app/gui/menu_bar.py`.

- **Utilitários**  
  - Funções para processamento de frames, OCR, gestão de configurações, escalonamento de coordenadas, entre outras, estão localizadas em `app/utils/`.

## Requisitos

- Python 3.x  
- As dependências necessárias encontram-se listadas em `app/requirements.txt`.

## Instruções de Instalação e Execução

1. **Clonar o Repositório e Configurar o Ambiente Virtual**  
   - Clone o repositório:
     ```sh
     git clone https://github.com/Hugo8220337/IA_2024_2025.git
     ```
   - Navegue até à pasta do projeto:
     ```sh
     cd IA_2024_2025
     ```
   - Crie e ative um ambiente virtual:
     ```sh
     python -m venv .venv
     # No Windows:
     .venv\Scripts\activate
     # No Linux/Mac:
     source .venv/bin/activate
     ```
     
2. **Instalar as Dependências**  
   - Instale as dependências necessárias:
     ```sh
     pip install -r app/requirements.txt
     ```

3. **Configuração do Ambiente**  
   - Renomeie o ficheiro [.env.example](http://_vscodecontentref_/0) para `.env` e substitua `ROBOFLOW_PRIVATE_API_KEY` pela sua chave privada.
   - Se necessário, edite o ficheiro [config.json](http://_vscodecontentref_/1) ou utilize as opções da interface gráfica (em “Opções”) para ajustar configurações, como o caminho para guardar as capturas de ecrã, intervalo entre capturas, etc.

4. **Executar os Notebooks de Treino**  
   - Inicie o Jupyter Notebook:
     ```sh
     jupyter notebook
     ```
   - Abra e execute os notebooks:
     - [pokemon_dataset_training.ipynb](http://_vscodecontentref_/2) para o treino do modelo de deteção de Pokémons.
     - [attack_effectiveness_training.ipynb](http://_vscodecontentref_/3) para o treino do modelo de predição da eficácia dos ataques.

5. **Executar a Aplicação Bot com Interface Gráfica**  
   - Execute a aplicação principal:
     ```sh
     python app/main.py
     ```
   - Na interface gráfica, utilize a opção “Selecionar Modelo” no menu **File** para carregar o ficheiro do modelo YOLO (por exemplo, `best.pt` gerado após o treino).
   - Após carregar o modelo, ative o bot através do botão “Ativar”. O bot efetuará capturas de ecrã periodicamente, processará as imagens e executará ações conforme os handlers implementados.

## Observações

- Certifique-se de possuir permissões para capturar o ecrã (especialmente em sistemas Linux, poderá ser necessário configurar variáveis de ambiente como `DISPLAY`).
- Ajuste os parâmetros e offsets (definidos em [app/utils/contants.py](http://_vscodecontentref_/4)) conforme necessário para o seu ecrã e contexto de aplicação.