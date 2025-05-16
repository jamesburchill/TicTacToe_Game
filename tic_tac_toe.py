import tkinter as tk
from tkinter import messagebox
import random
import math
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

import pygame
import tkinter as tk
from tkinter import messagebox

# Initialize pygame mixer
pygame.mixer.init()

# Load or define sounds
PLAYER_MOVE_SOUND = pygame.mixer.Sound('player_move.wav')
BOT_MOVE_SOUND = pygame.mixer.Sound('bot_move.wav')

# Define sequences for win, lose, draw
pygame.mixer.set_num_channels(3)
WIN_SOUND = [(500, 200), (600, 200), (700, 200)]  # Ascending tones
LOSE_SOUND = [(700, 200), (600, 200), (500, 200)]  # Descending tones
DRAW_SOUND = [(500, 200), (500, 200), (500, 200)]  # A trivial sequence

def play_sequence(sequence):
    for freq, dur in sequence:
        pygame.mixer.Sound.play(pygame.mixer.Sound(frequency=freq, size=-16))
        pygame.time.wait(dur)

# Add sound logic in player and bot turns
def player_turn(row, column):
    if board[row][column] == EMPTY and not check_winner():
        board[row][column] = PLAYER_X
        board_buttons[row][column].config(text=PLAYER_X)
        window.update_idletasks()
        # Play player move sound
        PLAYER_MOVE_SOUND.play()
        if not check_winner():
            bot_turn()

def bot_turn():
    move = find_best_move(bot_difficulty)
    if move:
        row, column = move
        board[row][column] = PLAYER_O
        button = board_buttons[row][column]
        button.config(text=PLAYER_O)
        window.update_idletasks()
        # Play bot move sound
        BOT_MOVE_SOUND.play()
        highlight_winning_move(button)
        check_winner()

def check_winner():
    if check_winning_condition(PLAYER_X):
        play_sequence(WIN_SOUND)
        messagebox.showinfo("Game Over", f"Player {PLAYER_X} wins!")
        increment_score(PLAYER_X)
        return True
    if check_winning_condition(PLAYER_O):
        play_sequence(LOSE_SOUND)
        messagebox.showinfo("Game Over", f"Player {PLAYER_O} wins!")
        increment_score(PLAYER_O)
        return True
    if not any(EMPTY in row for row in board):
        play_sequence(DRAW_SOUND)
        messagebox.showinfo("Game Over", "It's a tie!")
        increment_score("Tie")
        return True
    return False


# Initialize the main window
def initialize_window():
    window = tk.Tk()
    window.title("Tic-Tac-Toe")
    window.geometry("400x450")  # Adjusted size to include score
    window.configure(bg=COLORS['bg'])
    return window

# Display the board as buttons
def create_board(window):
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
    global board
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    for row_buttons in board_buttons:
        for button in row_buttons:
            button.config(text=EMPTY, bg=COLORS['button_bg'])
    update_scoreboard()

# Handle player's turn
def player_turn(row, column):
    if board[row][column] == EMPTY and not check_winner():
        board[row][column] = PLAYER_X
        board_buttons[row][column].config(text=PLAYER_X)
        window.update_idletasks()  # Force any pending UI updates before checking for a winner
        if not check_winner():
            bot_turn()

# Minimax algorithm to determine the best move for the bot with difficulty levels
def minimax(board, depth, is_maximizing, difficulty):
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

# Bot's turn using the Minimax algorithm with difficulty
def bot_turn():
    move = find_best_move(bot_difficulty)
    if move:
        row, column = move
        board[row][column] = PLAYER_O
        button = board_buttons[row][column]
        button.config(text=PLAYER_O)
        window.update_idletasks()  # Force any pending UI updates before checking for a winner
        highlight_winning_move(button)
        check_winner()

# Animation for winning move
def highlight_winning_move(button):
    def animate_highlight():
        for _ in range(3):
            button.config(bg=COLORS['winner'])
            window.update()
            window.after(150)
            button.config(bg=COLORS['button_bg'])
            window.update()
            window.after(150)
    threading.Thread(target=animate_highlight).start()

# Check winning condition
def check_winning_condition(player):
    for line in winning_combinations:
        b1, b2, b3 = line
        if board[b1[0]][b1[1]] == board[b2[0]][b2[1]] == board[b3[0]][b3[1]] == player:
            return True
    return False

# Check for a winner
def check_winner():
    if check_winning_condition(PLAYER_X):
        messagebox.showinfo("Game Over", f"Player {PLAYER_X} wins!")
        increment_score(PLAYER_X)
        return True
    if check_winning_condition(PLAYER_O):
        messagebox.showinfo("Game Over", f"Player {PLAYER_O} wins!")
        increment_score(PLAYER_O)
        return True
    if not any(EMPTY in row for row in board):
        messagebox.showinfo("Game Over", "It's a tie!")
        increment_score("Tie")
        return True
    return False

# Increment score
def increment_score(player):
    score[player] += 1
    update_scoreboard()

# Update the scoreboard
def update_scoreboard():
    scoreboard.config(text=f"X Wins: {score['X']} | O Wins: {score['O']} | Ties: {score['Tie']}")

# Main function to run the game
def main():
    global board, board_buttons, winning_combinations, scoreboard, score, window, bot_difficulty, difficulty_var
    
    # Initialize Tkinter root window
    window = initialize_window()
    
    # Instantiate Tkinter variable after initializing the window
    difficulty_var = tk.IntVar(value=1)

    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    winning_combinations = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
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

    set_difficulty()  # Set initial bot difficulty
    window.mainloop()

# Function to set difficulty level
def set_difficulty():
    global bot_difficulty
    bot_difficulty = difficulty_var.get() * 2  # Scale up for more challenge on each level

if __name__ == "__main__":
    main()
