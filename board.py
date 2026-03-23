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
    def count_pieces(self):
        """Return number of pieces remaining for both players."""
        red = black = 0
        for row in self.board:
            for piece in row:
                if piece != 0:
                    if piece.color == "r":
                        red += 1
                    else:
                        black += 1
        return red, black

    def get_all_moves(self, color):
        """Generate all valid moves for the given color."""
        moves = []
        for piece in self.get_all_pieces(color):
            if not isinstance(piece, Piece):
                continue

            # Check for normal moves (non-jumps)
            directions = self._get_directions(piece)

            for dr, dc in directions:
                row, col = piece.row + dr, piece.col + dc
                if 0 <= row < 8 and 0 <= col < 8 and self.board[row][col] == 0:
                    moves.append((piece, (row, col), []))

            # Check for jump moves
            self._check_jumps(piece, piece.row, piece.col, [], moves, set())

        return moves
           def _get_directions(self, piece):
        """Get valid movement directions based on piece type."""
        if piece.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.color == 'r':  # Red moves down
            return [(1, -1), (1, 1)]
        else:  # Black moves up
            return [(-1, -1), (-1, 1)]

    def _check_jumps(self, piece, row, col, captured, moves, visited):
        """ Recursively check for valid jump moves.
        Args:
            piece (Piece): The piece to check for jumps.
            row (int): Current row of the piece.
            col (int): Current column of the piece.
            captured (list): List of captured pieces in this jump sequence.
            moves (list): List to store valid moves.
            visited (set): Set of visited positions to avoid cycles.
        """
        
        # Kings can jump in any direction
        # Regular pieces can only jump in their forward direction initially
        # After first jump, all pieces can jump in any direction
        directions = self._get_directions(piece) if not captured else [
            (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            jump_row, jump_col = row + 2*dr, col + 2*dc

            # Check if jump is valid
            if (0 <= mid_row < 8 and 0 <= mid_col < 8 and
                0 <= jump_row < 8 and 0 <= jump_col < 8 and
                self.board[mid_row][mid_col] != 0 and
                self.board[mid_row][mid_col].color != piece.color and
                self.board[jump_row][jump_col] == 0 and
                (mid_row, mid_col) not in captured and
                    (jump_row, jump_col) not in visited):

                # Add this jump to moves
                    new_captured = captured + [(mid_row, mid_col)]
                moves.append((piece, (jump_row, jump_col), new_captured))

                # Check for additional jumps
                visited_with_jump = visited.union({(jump_row, jump_col)})
                self._check_jumps(piece, jump_row, jump_col,
                                  new_captured, moves, visited_with_jump)
