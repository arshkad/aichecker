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
        def _find_regular_moves(self, piece, moves):
        """Find all regular (non-jump) moves for a piece."""
        directions = self._get_directions(piece)

        for dr, dc in directions:
            row, col = piece.row + dr, piece.col + dc
            if 0 <= row < 8 and 0 <= col < 8 and self.board.board[row][col] == 0:
                moves[(row, col)] = []

    def _get_directions(self, piece):
        """Get valid movement directions based on piece type."""
        if piece.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.color == 'r':  # Red moves down
            return [(1, -1), (1, 1)]
        else:  # Black moves up
            return [(-1, -1), (-1, 1)]

    def _find_jumps(self, piece, row, col, captured, moves, visited):
        """Recursively find all jump moves for a piece. 
        Args:
            piece (Piece): The piece to find jumps for.
            row (int): The current row of the piece.
            col (int): The current column of the piece.
            captured (list): List of captured pieces during this jump sequence.
            moves (dict): Dictionary to store valid jump moves.
            visited (set): Set of visited positions to avoid cycles.
        """
        # After the first jump, any piece can move in any direction
        directions = self._get_directions(piece) if not captured else [
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]
       for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            jump_row, jump_col = row + 2*dr, col + 2*dc

            if (0 <= mid_row < 8 and 0 <= mid_col < 8 and
                    0 <= jump_row < 8 and 0 <= jump_col < 8):

                mid_piece = self.board.board[mid_row][mid_col]
                end_square = self.board.board[jump_row][jump_col]

                if (mid_piece != 0 and mid_piece.color != piece.color and
                    end_square == 0 and
                    (mid_row, mid_col) not in captured and
                        (jump_row, jump_col) not in visited):

                    # Add this jump to moves
                    new_captured = captured + [(mid_row, mid_col)]
                    moves[(jump_row, jump_col)] = new_captured

                    # Check for additional jumps (temporarily remove the jumped piece)
                    temp = self.board.board[mid_row][mid_col]
                    self.board.board[mid_row][mid_col] = 0

                    visited_with_jump = visited.union({(jump_row, jump_col)})
                    self._find_jumps(piece, jump_row, jump_col,
                                     new_captured, moves, visited_with_jump)

                    # Restore the jumped piece
                    self.board.board[mid_row][mid_col] = temp
