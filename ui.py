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
                       
        valid_moves = self.game.get_valid_moves(piece)
        self.valid_moves = valid_moves  # Store valid moves
        
        # Debug info
        print(f"Highlighting moves for piece at ({row},{col})")
        print(f"Valid moves: {valid_moves}")
        
        # Highlight the selected piece
        self.buttons[row][col].config(bg=self.selected_color)
        
        # Highlight valid moves with a very visible color
        for move_pos in valid_moves:
            r, c = move_pos
            print(f"Highlighting move at ({r},{c})")
            self.buttons[r][c].config(
                # bg=self.highlight_color,
                # relief=tk.RAISED,  # Make button appear raised
                # borderwidth=3  # Make border more visible######################################
                highlightbackground=self.highlight_color,  # Highlight background
                highlightthickness=3,  # Make highlight more visible
            )
        
        # Force update to ensure highlights are visible########################
        self.root.update()

    def ai_move(self):
        """Handles the AI's move"""
        # Ask the AI for its best move
        move = self.ai.choose_move(self.game)
        print(f"AI chose move: {move}")
        
        if move is None:
            messagebox.showinfo("Game Over", "AI has no valid moves. Player wins!")
            self.root.quit()
            return

        # Unpack the move
        orig_piece, (to_row, to_col), captured = move
        from_row, from_col = orig_piece.row, orig_piece.col
        real_piece = self.game.board.board[from_row][from_col]

        print(f"AI moving from ({from_row},{from_col}) to ({to_row},{to_col})")

        # Validate the AI's move
        if not isinstance(real_piece, self.game.board.board[from_row][from_col].__class__):
            print("AI attempted to move an invalid piece.")
            messagebox.showinfo("Error", "AI made an invalid move. Ending game.")
            self.root.quit()
            return

        # Highlight AI's move temporarily
        self.buttons[from_row][from_col].config(bg=self.selected_color)
        self.buttons[to_row][to_col].config(bg=self.highlight_color)
        self.root.update()
        self.root.after(500)  # Pause to show the move

        # Perform the move
        #################self.game.move(real_piece, to_row, to_col)

        old_mand = self.game.mandatory_jumps
        self.game.mandatory_jumps = False
        self.game.move(real_piece, to_row, to_col)
        self.game.mandatory_jumps = old_mand
        # Check if the AI's move resulted in a mandatory jump
        self.game.switch_turn()

        # Update the board display
        self.clear_highlights()
        self.update_board()

        # Check for end of game
        if self.game.is_game_over():
            winner = self.game.get_winner()
            messagebox.showinfo("Game Over", f"{winner} wins!" if winner else "It's a draw!")
            self.root.quit()

    def on_square_click(self, row, col):
        '''This handles the square click event'''
        # If it's AI's turn, ignore clicks
        if self.game_mode == "ai" and self.game.turn == "b":
            print("It's AI's turn. Player interaction is disabled.")
            return

        piece = self.game.board.board[row][col]
        
        # Debug info
        print(f"Clicked on square ({row},{col})")
        if piece != 0:
            print(f"Piece: {piece}, Color: {piece.color}, Turn: {self.game.turn}")
        
        # If first click or clicking on own piece - select piece
        if self.selected_piece is None:
            if piece != 0 and piece.color == self.game.turn:
                self.selected_piece = (row, col)
                self.clear_highlights()
                self.highlight_moves(row, col)
                print(f"Selected piece at ({row},{col})")
            else:
                print("No valid piece selected")
        else:
            # Second click - try to move
            from_row, from_col = self.selected_piece
                        to_row, to_col = row, col
            moving_piece = self.game.board.board[from_row][from_col]
            
            # Check if this is a valid destination
            if (to_row, to_col) in self.valid_moves:
                print(f"Valid move from ({from_row},{from_col}) to ({to_row},{to_col})")
                
                # Highlight the move before executing
                self.buttons[from_row][from_col].config(bg=self.selected_color)
                self.buttons[to_row][to_col].config(bg=self.highlight_color)
                self.root.update()
                self.root.after(200)  # Short pause to show move
                
                # Execute the move
                self.game.move(moving_piece, to_row, to_col)
                self.game.switch_turn()
                self.selected_piece = None
                self.valid_moves = {}  # Clear stored valid moves
                
                # Update display
                self.clear_highlights()
                self.update_board()
                
                # Check for game over
                if self.game.is_game_over():
                    winner = self.game.get_winner()
                    messagebox.showinfo("Game Over", f"{winner} wins!" if winner else "It's a draw!")
                    self.root.quit()
                elif self.game_mode == "ai" and self.game.turn == "b":
                    # Schedule AI move after a delay
                    self.root.after(500, self.ai_move)
            else:
                # Not a valid move - deselect or select new piece
                print("Not a valid move")
                if piece != 0 and piece.color == self.game.turn:
                    # If clicking on another of player's pieces, select that one instead
                    self.selected_piece = (row, col)
                                        self.clear_highlights()
                    self.highlight_moves(row, col)
                    print(f"Selected new piece at ({row},{col})")
                else:
                    # Otherwise just deselect
                    self.selected_piece = None
                    self.valid_moves = {}  # Clear stored valid moves
                    self.clear_highlights()
                    self.update_board()
                    print("Deselected piece")


if __name__ == "__main__":
    root = tk.Tk()
    app = CheckersUI(root)
    root.mainloop()





                


