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

    def has_valid_moves(self, color):
        """Check if a player has any valid moves."""
        # Save original turn
        original_turn = self.turn
        self.turn = color

        # Check if any piece has valid moves
        pieces = self.board.get_all_pieces(color)
        has_moves = any(self.get_valid_moves(piece) for piece in pieces)

        # Restore original turn
        self.turn = original_turn
        return has_moves

    def move(self, piece, row, col):
        """Move a piece and handle captures and promotions."""
        if not isinstance(piece, Piece):
            raise ValueError(f"Expected a Piece, got {type(piece)}")

        # Get the valid moves to check for captures
        valid_moves = self.get_valid_moves(piece)

        # Check if this is a valid move
        if (row, col) not in valid_moves:
            raise ValueError(
                f"Invalid move to ({row}, {col}) for piece at ({piece.row}, {piece.col})")

        # Move the piece
        self.board.board[piece.row][piece.col] = 0
        piece.row, piece.col = row, col
        self.board.board[row][col] = piece

        # Handle captures
        jumped = valid_moves.get((row, col), [])
        for j_row, j_col in jumped:
            self.remove_piece(j_row, j_col)

        # Promote to king if reaching end row
                if (piece.color == "r" and row == 7) or (piece.color == "b" and row == 0):
            piece.make_king()

        return jumped  # Return list of captured pieces for UI feedback

    def remove_piece(self, row, col):
        """Remove a piece from the board."""
        self.board.board[row][col] = 0

    def is_game_over(self):
        """Check if the game is over (no pieces or no moves for either side)."""
        red_count, black_count = self.board.count_pieces()

        # If one side has no pieces, we're done
        if red_count == 0 or black_count == 0:
            return True

        # Check moves for both players
        red_can_move = self.has_valid_moves("r")
        black_can_move = self.has_valid_moves("b")

        # Game is over if either side has no moves
        return not (red_can_move and black_can_move)

    def get_winner(self):
        """Determine the winner of the game."""
        red_count, black_count = self.board.count_pieces()

        # Check piece count
        if red_count == 0:
            return "Black"
        if black_count == 0:
            return "Red"

        # Check mobility
        red_can_move = self.has_valid_moves("r")
        black_can_move = self.has_valid_moves("b")

        if not red_can_move:
                        return "Black"
        if not black_can_move:
            return "Red"
        
        return None
        