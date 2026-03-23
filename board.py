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
    def print_board(self):
        """Print a text representation of the board."""
        print("\n  " + " ".join(str(i) for i in range(8)))
        for i, row in enumerate(self.board):
            print(f"{i} " + " ".join(str(p) if p != 0 else "." for p in row))

    def move_piece(self, piece, row, col):
        """Move a piece to a new position and update internal state."""
        if not isinstance(piece, Piece):
            raise ValueError(f"Expected a Piece object, got {type(piece)}")

        self.board[piece.row][piece.col] = 0
        piece.row, piece.col = row, col
        self.board[row][col] = piece

    def remove_piece(self, row, col):
        """Remove a piece from the board (used for captures)."""
        self.board[row][col] = 0

    def get_all_pieces(self, color):
        """Return a list of all pieces of the given color."""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces