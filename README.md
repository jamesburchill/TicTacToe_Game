**_Aside from this single comment, this entire repo - the code, the folders, the documentation, the logic ... all of it has been written by various AI 'agents', chatbots and other sundry AI tools, prompted into existence by 'yours truly' -- James C. Burchill_**

---

# Tic Tac Toe Game

A simple yet feature-rich implementation of the classic Tic Tac Toe game with a graphical user interface built using Python and Tkinter.

## Features

- Clean and intuitive graphical interface
- Play against an AI opponent with adjustable difficulty levels (Easy, Medium, Hard)
- Sound effects for game events
- Volume control
- Score tracking
- Visual animations for winning moves

## Screenshots

(Screenshots would be added here)

## Installation

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes with Python)

### Steps

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/jamesburchill/TicTacToe_Game
   cd TicTacToe_Game
   ```

2. No additional dependencies are required as the game only uses Python's built-in libraries.

## Usage

1. Run the game:
   ```
   python tic_tac_toe.py
   ```

2. Game Controls:
   - Click on any empty cell to place your 'X' mark
   - The AI will automatically make its move after you
   - Use the "Reset" button to start a new game
   - Select difficulty level using the radio buttons (Easy, Medium, Hard)
   - Adjust volume using the slider

3. Game Rules:
   - You play as 'X', and the AI plays as 'O'
   - The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins
   - If all cells are filled and no player has won, the game is a tie

## Game Difficulty Levels

- **Easy**: The AI makes basic moves with limited lookahead
- **Medium**: The AI uses more advanced strategy with moderate lookahead
- **Hard**: The AI uses the minimax algorithm with deeper lookahead to make optimal moves

## Project Structure

- `tic_tac_toe.py`: Main game file containing all the game logic and UI
- `docs/tasks.md`: Documentation of improvement tasks for the project

## Sound Effects

The game includes sound effects using Tkinter's bell() method for:
- Player moves
- Bot moves
- Game start
- Game reset
- Changing difficulty
- Invalid moves
- Win/lose/draw sequences

The sound system uses different bell patterns to represent different game events.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Python and Tkinter communities for their excellent documentation
- Inspired by classic Tic Tac Toe implementations
