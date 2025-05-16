"""
Tic Tac Toe Game with GUI

This module implements a Tic Tac Toe game with a graphical user interface using Tkinter.
The game features an AI opponent with adjustable difficulty levels, sound effects,
score tracking, and visual animations.

The player plays as 'X' and the AI plays as 'O'. The first player to get three marks
in a row (horizontally, vertically, or diagonally) wins the game.
"""

import tkinter as tk
from tkinter import messagebox, Scale
import random
import math
import os
import threading

# Constants
PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "
COLORS = {
    'bg': '#f4ebc1',
    'button_bg': '#baa892',
    'button_active_bg': '#f0d9b5',
    'text': '#5b5b5b',
    'winner': '#82c09a'
}

class SoundManager:
    """
    Sound Manager class to handle all sound-related functionality.

    This class manages sound effects for the game using Tkinter's bell() method.
    It supports different sound types for various game events and can play
    sequences of sounds for special events like winning or losing.
    """
    def __init__(self):
        """
        Initialize the SoundManager with default settings.

        Sets up default volume, sound types with their properties, and
        predefined sound sequences for game outcomes.
        """
        # Default volume (0.0 to 1.0)
        self.volume = 0.7

        # Store the root window reference (will be set later)
        self.root = None

        # Define sound types with their properties
        self.sound_types = {
            'player_move': {'pitch': 1.0, 'duration': 1},
            'bot_move': {'pitch': 0.8, 'duration': 1},
            'game_start': {'pitch': 1.2, 'duration': 2},
            'reset_game': {'pitch': 0.9, 'duration': 1},
            'change_difficulty': {'pitch': 1.1, 'duration': 1},
            'invalid_move': {'pitch': 0.7, 'duration': 1}
        }

        # Define sequences for win, lose, draw
        self.sequences = {
            'win': [{'pitch': 1.0, 'duration': 1}, {'pitch': 1.2, 'duration': 1}, {'pitch': 1.5, 'duration': 1}],
            'lose': [{'pitch': 1.5, 'duration': 1}, {'pitch': 1.2, 'duration': 1}, {'pitch': 1.0, 'duration': 1}],
            'draw': [{'pitch': 1.0, 'duration': 1}, {'pitch': 1.0, 'duration': 1}, {'pitch': 1.0, 'duration': 1}]
        }

    def set_root(self, root):
        """
        Set the root window reference.

        Args:
            root: The Tkinter root window object
        """
        self.root = root

    def play_sound(self, sound_name):
        """
        Play a sound by name using tkinter bell.

        Args:
            sound_name (str): The name of the sound to play, must be a key in self.sound_types
                              (e.g., 'player_move', 'bot_move', etc.)

        Returns:
            None
        """
        if not self.root:
            return

        if sound_name in self.sound_types:
            # Get the sound properties
            props = self.sound_types[sound_name]

            # Adjust volume (bell doesn't support volume, so we'll just ring it multiple times)
            rings = max(1, int(self.volume * props['duration']))

            # Ring the bell
            for _ in range(rings):
                try:
                    self.root.bell()
                except Exception as e:
                    print(f"Error playing sound: {e}")

    def play_sequence(self, sequence_name):
        """
        Play a sequence of sounds for special events.

        Args:
            sequence_name (str): The name of the sequence to play, must be a key in self.sequences
                                (e.g., 'win', 'lose', 'draw')

        Returns:
            None
        """
        if not self.root:
            return

        if sequence_name in self.sequences:
            sequence = self.sequences[sequence_name]

            # Play each sound in the sequence
            for sound in sequence:
                # Adjust volume (bell doesn't support volume, so we'll just ring it multiple times)
                rings = max(1, int(self.volume * sound['duration']))

                # Ring the bell
                for _ in range(rings):
                    try:
                        self.root.bell()
                    except Exception as e:
                        print(f"Error playing sound: {e}")

                    # Small delay between rings
                    self.root.after(50)

                # Delay between sounds in sequence
                self.root.after(100)

    def set_volume(self, volume):
        """
        Set volume for sounds.

        Args:
            volume (float): Volume level between 0.0 (silent) and 1.0 (maximum)
        """
        self.volume = volume

    def cleanup(self):
        """
        Clean up resources used by the sound manager.

        This method is called when the application is shutting down.
        Currently, there are no resources to clean up when using tkinter bell.
        """
        # Nothing to clean up with tkinter bell
        pass

# Create global sound manager instance
sound_manager = SoundManager()

# List to track active threads
active_threads = []

# Flag to indicate that the application is shutting down
is_shutting_down = False

# Game logic with sound effects
def player_turn(row, column):
    """
    Handle the player's turn when they click on a cell.

    This function is called when the player clicks on a cell in the game board.
    It updates the board state, plays a sound effect, and triggers the bot's turn
    if the game hasn't been won yet.

    Args:
        row (int): The row index of the clicked cell (0-2)
        column (int): The column index of the clicked cell (0-2)

    Returns:
        None
    """
    if board[row][column] == EMPTY and not check_winner():
        board[row][column] = PLAYER_X
        board_buttons[row][column].config(text=PLAYER_X)
        window.update_idletasks()
        # Play player move sound
        sound_manager.play_sound('player_move')
        if not check_winner():
            bot_turn()
    else:
        # Play invalid move sound if the cell is already occupied
        sound_manager.play_sound('invalid_move')

def bot_turn():
    """
    Handle the bot's turn after the player has made a move.

    This function uses the minimax algorithm to determine the best move for the bot,
    updates the board state, plays a sound effect, and checks if the game has been won.

    Returns:
        None
    """
    move = find_best_move(bot_difficulty)
    if move:
        row, column = move
        board[row][column] = PLAYER_O
        button = board_buttons[row][column]
        button.config(text=PLAYER_O)
        window.update_idletasks()
        # Play bot move sound
        sound_manager.play_sound('bot_move')
        highlight_winning_move(button)
        check_winner()

def check_winner():
    """
    Check if the game has been won or if it's a tie.

    This function checks if either player has won the game or if the game is a tie.
    It plays appropriate sound sequences, shows a message box, and updates the score.

    Returns:
        bool: True if the game is over (win or tie), False otherwise
    """
    if check_winning_condition(PLAYER_X):
        sound_manager.play_sequence('win')
        messagebox.showinfo("Game Over", f"Player {PLAYER_X} wins!")
        increment_score(PLAYER_X)
        return True
    if check_winning_condition(PLAYER_O):
        sound_manager.play_sequence('lose')
        messagebox.showinfo("Game Over", f"Player {PLAYER_O} wins!")
        increment_score(PLAYER_O)
        return True
    if not any(EMPTY in row for row in board):
        sound_manager.play_sequence('draw')
        messagebox.showinfo("Game Over", "It's a tie!")
        increment_score("Tie")
        return True
    return False


# Initialize the main window
def initialize_window():
    """
    Initialize and configure the main Tkinter window.

    Creates a new Tkinter window with the appropriate title, size, and background color.

    Returns:
        tk.Tk: The configured Tkinter root window
    """
    window = tk.Tk()
    window.title("Tic-Tac-Toe")
    window.geometry("400x450")  # Adjusted size to include score
    window.configure(bg=COLORS['bg'])
    return window

# Display the board as buttons
def create_board(window):
    """
    Create the game board with interactive buttons.

    Creates a 3x3 grid of buttons that represent the game board. Each button
    is configured with appropriate styling and connected to the player_turn function.

    Args:
        window (tk.Tk): The Tkinter root window

    Returns:
        list: A 2D list of button objects representing the game board
    """
    board_frame = tk.Frame(window, bg=COLORS['bg'])
    board_frame.pack(expand=True)
    board_buttons = []
    for row in range(3):
        row_button = []
        for column in range(3):
            button = tk.Button(board_frame, text=EMPTY, font=('normal', 40, 'normal'), width=3, height=1,
                               bg=COLORS['button_bg'], fg=COLORS['text'], activebackground=COLORS['button_active_bg'],
                               command=lambda r=row, c=column: player_turn(r, c))
            button.grid(row=row, column=column, padx=5, pady=5)
            row_button.append(button)
        board_buttons.append(row_button)
    return board_buttons

# Reset the game board
def reset_game():
    """
    Reset the game board to its initial state.

    Clears all marks from the board, resets the board data structure,
    updates the scoreboard, and plays a reset game sound.

    Returns:
        None
    """
    global board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    for row_buttons in board_buttons:
        for button in row_buttons:
            button.config(text=EMPTY, bg=COLORS['button_bg'])
    update_scoreboard()
    # Play reset game sound
    sound_manager.play_sound('reset_game')


# Minimax algorithm to determine the best move for the bot with difficulty levels
def minimax(board, depth, is_maximizing, difficulty):
    """
    Implement the minimax algorithm for the AI opponent.

    This recursive algorithm evaluates all possible moves and their outcomes
    to determine the optimal move for the AI. The difficulty parameter limits
    the depth of the search tree.

    Args:
        board (list): The current game board state as a 2D list
        depth (int): The current depth in the search tree
        is_maximizing (bool): True if maximizing player's turn, False if minimizing
        difficulty (int): The maximum depth to search

    Returns:
        int: The score of the board position (-1 for player win, 0 for draw, 1 for AI win)
    """
    if check_winning_condition(PLAYER_X):
        return -1
    if check_winning_condition(PLAYER_O):
        return 1
    if not any(EMPTY in row for row in board):
        return 0

    if depth >= difficulty:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_O
                    score = minimax(board, depth + 1, False, difficulty)
                    board[r][c] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = PLAYER_X
                    score = minimax(board, depth + 1, True, difficulty)
                    board[r][c] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# Find the best move for the bot
def find_best_move(difficulty):
    """
    Find the best move for the AI opponent using the minimax algorithm.

    Evaluates all possible moves on the current board and selects the one
    with the highest score according to the minimax algorithm.

    Args:
        difficulty (int): The difficulty level that determines search depth

    Returns:
        tuple: The (row, column) coordinates of the best move, or None if no moves are available
    """
    best_score = -math.inf
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                board[r][c] = PLAYER_O
                score = minimax(board, 0, False, difficulty)
                board[r][c] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (r, c)
    return best_move


# Animation for winning move
def highlight_winning_move(button):
    """
    Create a visual animation to highlight a button.

    This function creates a thread that animates a button by changing its background
    color repeatedly. It includes safety checks to handle application shutdown gracefully.

    Args:
        button (tk.Button): The button to animate

    Returns:
        None
    """
    def animate_highlight():
        try:
            for _ in range(3):
                # Check if the application is shutting down
                if is_shutting_down:
                    return

                try:
                    button.config(bg=COLORS['winner'])
                    window.update()
                except Exception:
                    # Button might have been destroyed
                    return

                # Use a loop with short sleeps instead of a single long wait
                # This allows more frequent checking of is_shutting_down
                for _ in range(15):  # 15 * 10ms = 150ms
                    if is_shutting_down:
                        return
                    try:
                        window.after(10)  # 10ms sleep
                    except Exception:
                        return

                # Check again after the delay
                if is_shutting_down:
                    return

                try:
                    button.config(bg=COLORS['button_bg'])
                    window.update()
                except Exception:
                    # Button might have been destroyed
                    return

                # Use a loop with short sleeps again
                for _ in range(15):  # 15 * 10ms = 150ms
                    if is_shutting_down:
                        return
                    try:
                        window.after(10)  # 10ms sleep
                    except Exception:
                        return
        except Exception as e:
            print(f"Error in animate_highlight: {e}")
        finally:
            # Remove this thread from active_threads when done
            if threading.current_thread() in active_threads:
                active_threads.remove(threading.current_thread())

    # Don't start a new thread if we're shutting down
    if is_shutting_down:
        return

    thread = threading.Thread(target=animate_highlight)
    thread.daemon = True  # Set as daemon thread so it will exit when the main program exits
    thread.start()
    # Add thread to active_threads list
    active_threads.append(thread)

# Check winning condition
def check_winning_condition(player):
    """
    Check if a player has won the game.

    Checks all possible winning combinations to see if the specified player
    has three marks in a row (horizontally, vertically, or diagonally).

    Args:
        player (str): The player to check for ('X' or 'O')

    Returns:
        bool: True if the player has won, False otherwise
    """
    for line in winning_combinations:
        b1, b2, b3 = line
        if board[b1[0]][b1[1]] == board[b2[0]][b2[1]] == board[b3[0]][b3[1]] == player:
            return True
    return False


# Increment score
def increment_score(player):
    """
    Increment the score for a player and update the scoreboard.

    Args:
        player (str): The player whose score to increment ('X', 'O', or 'Tie')

    Returns:
        None
    """
    score[player] += 1
    update_scoreboard()

# Update the scoreboard
def update_scoreboard():
    """
    Update the scoreboard display with current scores.

    Updates the text of the scoreboard label to show the current scores
    for both players and ties.

    Returns:
        None
    """
    scoreboard.config(text=f"X Wins: {score['X']} | O Wins: {score['O']} | Ties: {score['Tie']}")

# Main function to run the game
def main():
    """
    Main function to initialize and run the Tic Tac Toe game.

    This function:
    - Initializes the game board and UI components
    - Sets up event handlers
    - Configures the sound manager
    - Handles window closing and cleanup
    - Starts the main event loop

    Returns:
        None
    """
    global board, board_buttons, winning_combinations, scoreboard, score, window, bot_difficulty, difficulty_var

    # Initialize Tkinter root window
    window = initialize_window()

    # Set the root window reference in the sound manager
    sound_manager.set_root(window)

    # Instantiate Tkinter variable after initializing the window
    difficulty_var = tk.IntVar(value=1)

    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],  # Top row
        [(1, 0), (1, 1), (1, 2)],  # Middle row
        [(2, 0), (2, 1), (2, 2)],  # Bottom row
        [(0, 0), (1, 0), (2, 0)],  # Left column
        [(0, 1), (1, 1), (2, 1)],  # Middle column
        [(0, 2), (1, 2), (2, 2)],  # Right column
        [(0, 0), (1, 1), (2, 2)],  # Diagonal from top-left
        [(0, 2), (1, 1), (2, 0)],  # Diagonal from top-right
    ]
    score = {'X': 0, 'O': 0, 'Tie': 0}

    board_buttons = create_board(window)
    scoreboard = tk.Label(window, text="X Wins: 0 | O Wins: 0 | Ties: 0", bg=COLORS['bg'], font=('normal', 12, 'bold'))
    scoreboard.pack()
    reset_button = tk.Button(window, text="Reset", font=('normal', 12), command=reset_game)
    reset_button.pack(pady=10)
    difficulty_frame = tk.Frame(window, bg=COLORS['bg'])
    difficulty_frame.pack(pady=10)
    tk.Label(difficulty_frame, text="Select Difficulty:", bg=COLORS['bg'], fg=COLORS['text'], font=('normal', 10)).pack(side=tk.LEFT)
    tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty_var, value=1, bg=COLORS['bg'], command=set_difficulty).pack(side=tk.LEFT)
    tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty_var, value=2, bg=COLORS['bg'], command=set_difficulty).pack(side=tk.LEFT)
    tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty_var, value=3, bg=COLORS['bg'], command=set_difficulty).pack(side=tk.LEFT)

    # Add volume control
    volume_frame = tk.Frame(window, bg=COLORS['bg'])
    volume_frame.pack(pady=10)
    tk.Label(volume_frame, text="Volume:", bg=COLORS['bg'], fg=COLORS['text'], font=('normal', 10)).pack(side=tk.LEFT)
    volume_slider = Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                         bg=COLORS['bg'], length=150, 
                         command=lambda v: sound_manager.set_volume(float(v)/100))
    volume_slider.set(int(sound_manager.volume * 100))  # Set initial value
    volume_slider.pack(side=tk.LEFT)

    set_difficulty()  # Set initial bot difficulty

    # Play game start sound
    sound_manager.play_sound('game_start')

    # Add a protocol to handle window close event
    def on_closing():
        try:
            # Clean up sound manager resources
            sound_manager.cleanup()

            # Set the shutting down flag to ensure threads exit
            global is_shutting_down
            is_shutting_down = True

            # Wait for active threads to finish (with timeout)
            threads_to_join = active_threads.copy()
            for thread in threads_to_join:
                if thread.is_alive():
                    try:
                        thread.join(0.5)  # Wait for 500ms max
                    except Exception as e:
                        print(f"Error joining thread: {e}")

            # Clear the active_threads list
            active_threads.clear()
        except Exception as e:
            print(f"Error during cleanup: {e}")
        finally:
            # Destroy the window
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()

# Function to set difficulty level
def set_difficulty():
    """
    Set the difficulty level for the AI opponent.

    Updates the global bot_difficulty variable based on the selected
    difficulty level in the UI. Higher values make the AI more challenging
    by increasing the search depth in the minimax algorithm.

    Returns:
        None
    """
    global bot_difficulty
    bot_difficulty = difficulty_var.get() * 2  # Scale up for more challenge on each level
    # Play change difficulty sound
    sound_manager.play_sound('change_difficulty')

if __name__ == "__main__":
    main()
