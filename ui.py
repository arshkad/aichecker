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
    def create_board(self):
        # Clear any existing buttons
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        
        for row in range(8):
            for col in range(8):
                # Light and dark squares
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                button = tk.Button(self.board_frame, bg=color, width=4, height=2,
                                   command=lambda r=row, c=col: self.on_square_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def update_status(self):
        """Update the status label to show whose turn it is"""
        turn_text = "Red's Turn" if self.game.turn == "r" else "Black's Turn"
        if self.game_mode == "ai":
            turn_text += " (You)" if self.game.turn == "r" else " (AI)"
        self.status_label.config(text=turn_text)

    def update_board(self):
        print("Updating board...")
        for row in range(8):
            for col in range(8):
                piece = self.game.board.board[row][col]
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                                # Check if this is the selected piece
                if self.selected_piece and (row, col) == self.selected_piece:
                    # Highlight selected piece
                    color = self.selected_color  
                
                # Check if this is a valid move square
                elif self.valid_moves and (row, col) in self.valid_moves:
                    #  Highlight valid moves
                    color = self.highlight_color
                
                if piece == 0:
                    self.buttons[row][col].config(text="", bg=color, state=tk.NORMAL)
                else:
                    # Red for 'r', Black for 'b'
                    piece_color = "red" if piece.color == "r" else "black"  
                    piece_text = str(piece)
                    self.buttons[row][col].config(
                        text=piece_text, 
                        fg=piece_color, 
                        bg=color,
                        font=("Arial", 12, "bold"),
                        state=tk.NORMAL if piece.color == self.game.turn else tk.DISABLED
                    )
                            
        self.update_status()
        # Force an update to ensure UI reflects changes#############################self.root.update_idletasks()
        self.root.update()
        print("Board updated.")

    def clear_highlights(self):
        # Clear highlights on the board and reset to original colors
        self.valid_moves = {}  # Clear stored valid moves
        for row in range(8):
            for col in range(8):
                # # Light and dark squares
                # color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                # self.buttons[row][col].config(bg=color)
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                self.buttons[row][col].config(
                    bg=color,
                    highlightbackground=color,  # Reset highlight background
                    highlightthickness=0,  # Reset highlight thickness
                )
        # Force update to ensure highlights are cleared
        self.root.update()########################################

    def highlight_moves(self, row, col):
        '''This highlights the valid moves for the selected piece'''
        piece = self.game.board.board[row][col]
        if not piece or piece == 0:
            return

                


