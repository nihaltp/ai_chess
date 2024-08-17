This project is a chess GUI built using Pygame. As a beginner, I'm developing it step by step, focusing on adding features gradually to enhance both functionality and my learning experience.


## Table of Contents

- [Project Goals](#project-goals)
- [Setup Instructions](#setup-instructions)
- [How to Play](#how-to-play)
- [Features](#features)
- [Contributing](#contributing)


## Project Goals

This project is being developed step by step, with the following goals in mind:

- **Player Info Box**: Display the player's name and indicate whose turn it is.
- **Timer**: Implement a countdown timer for each player to make the game more competitive.
- **Settings Menu**:
  - Change the background color to suit the player's preference.
  - Customize the board color for a personalized look.
- **AI Integration**:
  - Start with Stockfish, the powerful chess engine.
  - Eventually add a machine learning-based AI for an alternative challenge.


## Setup Instructions

### Prerequisites
- Python 3.x
- Pygame
- python-chess
- Stockfish (Download the executable and place it in the `stockfish` folder)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/nihaltp/ai_chess.git
   cd ai_chess
   ```

2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the game**:
   ```bash
   python main.py
   ```


## How to Play
Start the Game: Run the main.py file to start the game.

### Controls

    Click on the pieces to select and move them.
    Use the settings menu to customize your game experience.
    The game will automatically switch between players after each move.
    The game will end when a player checkmates the other player or when the timer runs out.


### Objective

- Checkmate the opponent's king while managing your time.
- Strategize your moves to outplay the AI or human opponent.


### Features

    - AI
    - Undo/Redo
    - Checkmate
    - Draw
    - Castling
    - Promotion
    - Piece Movement
    - Piece Selection
    - Game History
    - Save/Load Game [Coming soon]
    - Timer [Coming soon]
    - Settings [Coming soon]
    - Customizable Board [Coming soon]
    - Customizable Background [Coming soon]
    - Customizable Pieces [Coming soon]
    - Customizable Colors [Coming soon]
    - Customizable Font [Coming soon]
    - Customizable Timer [Coming soon]
    - Customizable AI [Coming soon]
    - Customizable Objective [Coming soon]
    - Customizable Game History [Coming soon]
    - Customizable Game Over [Coming soon]

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.


![Python](https://img.shields.io/badge/python-blue)
![Python-Chess](https://img.shields.io/badge/python--chess-orange)
![Pygame](https://img.shields.io/badge/pygame-green)


# ai_chess