from board import Board, Piece

# This file contains the Game class, which manages the game state and logic.
# It handles player turns, valid moves, captures, and game over conditions.
class Game:
    def __init__(self):
        """Initialize the game with a new board and set the starting player."""
        self.board = Board()
        self.turn = "r"
        # International Checkers rules state that jumps are mandatory
        # Force players to take jumps when available
        self.mandatory_jumps = True 
        # self.mandatory_jumps = False  # Allow players to choose between jumps and regular moves
    def switch_turn(self):
        """Switch the current player's turn."""
        self.turn = "b" if self.turn == "r" else "r"

    def get_valid_moves(self, piece):
        """Get all valid moves for a piece.

        Returns:
            dict: Dictionary mapping destination coordinates to list of captured pieces
        """
        if not isinstance(piece, Piece):
            raise ValueError(
                f"Invalid piece passed to get_valid_moves: {piece}")
        if piece.color != self.turn:
            return {}

        moves = {}

        # Check for jumps first
        self._find_jumps(piece, piece.row, piece.col, [], moves, set())

        # If no jumps are available or jumps aren't mandatory, check for regular moves
        if not moves or not self.mandatory_jumps:
            self._find_regular_moves(piece, moves)

        # If jumps are available and mandatory, remove regular moves
        if self.mandatory_jumps and any(jumped for jumped in moves.values()):
            moves = {pos: jumped for pos, jumped in moves.items() if jumped}

        return moves