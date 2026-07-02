# Hangman Game

A simple Hangman game written in Python. This was my first Python project, so it does not use any external libraries like Pandas or NumPy. It only uses built-in Python modules.

## Features

- Classic Hangman gameplay with ASCII-art stages
- Player names with persistent score tracking (saved in a JSON file)
- A highscore list that shows each player's score and number of rounds played
- Colored terminal output for correct and wrong guesses
- Input validation (only single letters are accepted)
- Option to clear the highscore list

## How to Play

1. Run the script:
   ```bash
   python hangman.py
   ```
2. Choose an option from the main menu:
   - `1` – Start a new game
   - `2` – Quit the game
   - `3` – Show the highscore list
   - `c` – Clear the highscore list
3. Enter your player name (maximum 15 letters).
4. Try to guess the hidden word one letter at a time. Every wrong guess adds a new part to the hangman drawing. If the full figure is drawn, the game is over.
5. After winning, you can decide if you want to play another round.

## Project Structure

```
├── hangman.py      # Main game file
└── player.json     # Created automatically to store player data
```

## How It Works

The project uses two main classes:

- **Player**: Handles everything related to player data, such as creating a new player, loading existing players, and updating scores and rounds in `player.json`.
- **Game**: Contains the actual game logic, including choosing a random word, checking guesses, and displaying the hangman stages.

Player data is stored in a JSON file (`player.json`), so scores and rounds are saved even after the program is closed.

## Possible Improvements

Since this was my first Python project, there are several things that could be improved in the future:

- Add a larger and more varied word list, or load words from an external file
- Add difficulty levels
- Add unit tests
- Improve error handling for the JSON file

## Notes

This project was built to practice core Python concepts such as classes, file handling with JSON, loops, and basic terminal formatting with ANSI color codes.
