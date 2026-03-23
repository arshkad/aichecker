# This module defines the Board and Piece classes for a checkers game.

class Piece:
    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color  # "r" or "b"
        self.king = king    # Flag for king status

    def make_king(self):
        self.king = True

    def __repr__(self):
        return self.color.upper() if self.king else self.color


class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        """Initialize the checkers board with pieces in starting positions."""
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if (row + col) % 2 == 1:  # Only use dark squares
                    if row < 3:
                        self.board[row].append(Piece(row, col, "r"))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, "b"))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
