import tkinter as tk
from tkinter import messagebox
from game import Game
from AI import MinimaxAI
import random

class CheckersUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers Game")
        self.game = Game()

        self.menu_frame = tk.Frame(self.root)
        self.board_frame = tk.Frame(self.root)

        # Colors for the board - enhanced contrast for visibility
        self.light_square = "#F5F5F5"  # Lighter white
        self.dark_square = "#A9A9A9"   # Darker gray for better contrast
        self.highlight_color = "#5CDB5C"  # Brighter green for valid moves
        self.selected_color = "#4DA6FF"  # Brighter blue for selected piece

        # This allows PvP or AI
        self.game_mode = None
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        # Store valid moves for the selected piece
        self.valid_moves = {}
        # Initialize the AI with the black color
        self.ai = MinimaxAI("b")  

        # Status label to show whose turn it is
        self.status_frame = tk.Frame(self.root)
        self.status_label = tk.Label(self.status_frame, text="", font=("Arial", 12))
        
        self.start_menu()

    def start_menu(self):
        '''This creates the start menu'''
        self.menu_frame.pack(fill=tk.BOTH, expand=True)
        tk.Label(self.menu_frame, text="Welcome to Competitive Checkers!",
                 font=("Arial", 16)).pack(pady=10)
        tk.Button(self.menu_frame, text="Player vs Player", width=20,
                  command=lambda: self.start_game("pvp")).pack(pady=5)
        tk.Button(self.menu_frame, text="Player vs AI", width=20,
                  command=lambda: self.start_game("ai")).pack(pady=5)
        tk.Button(self.menu_frame, text="Quit", width=20,
                  command=self.root.quit).pack(pady=5)

    def start_game(self, mode):
        '''This starts the game'''
        self.game_mode = mode
        self.menu_frame.pack_forget()
        self.status_frame.pack(fill=tk.X, pady=5)
        self.status_label.pack()
        self.board_frame.pack(padx=10, pady=10)
        self.create_board()
        self.update_board()
        self.update_status()

