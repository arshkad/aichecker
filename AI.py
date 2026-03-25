# AI.py

from copy import deepcopy
from game import Game
from board import Piece


class MinimaxAI:
    def __init__(self, color, max_depth=1):  # Reduced default depth for better performance
        self.color = color
        self.max_depth = max_depth

    def choose_move(self, game):
        """Choose the best move using minimax algorithm with alpha-beta pruning."""
        # Work on a clone of the board so we never touch the real one
        board_copy = deepcopy(game.board)

        def minimax(state, depth, alpha, beta, maximizing):
            # Base case: reached max depth or no pieces left
            if depth == 0 or state.is_terminal():
                return self.evaluate(state), None

            best_move = None
            if maximizing:
                max_eval = float('-inf')
                for move in self.get_valid_moves_with_pieces(state, self.color):
                    p_clone, (tr, tc), captured = move

                    # Skip invalid moves
                    if not isinstance(p_clone, Piece):
                        continue

                    # Create a deep copy of the board to simulate the move
                    next_state = deepcopy(state)

                    # Get the copy of the piece from the copied board
                    from_r, from_c = p_clone.row, p_clone.col
                    piece_copy = next_state.board[from_r][from_c]

                    # Make the move on the copied board
                    next_state.make_move((piece_copy, (tr, tc), captured))

                    # Evaluate the resulting position
                    eval_score, _ = minimax(
                        next_state, depth-1, alpha, beta, False)
                                # Update the best move if this is better
                    if eval_score > max_eval:
                        max_eval = eval_score
                        best_move = move

                    # Alpha-beta pruning
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break

                return max_eval, best_move
            else:
                min_eval = float('inf')
                opponent = 'r' if self.color == 'b' else 'b'

                for move in self.get_valid_moves_with_pieces(state, opponent):
                    p_clone, (tr, tc), captured = move

                    # Skip invalid moves
                    if not isinstance(p_clone, Piece):
                        continue

                    # Create a deep copy of the board to simulate the move
                    next_state = deepcopy(state)

                    # Get the copy of the piece from the copied board
                    from_r, from_c = p_clone.row, p_clone.col
                    piece_copy = next_state.board[from_r][from_c]

                    # Make the move on the copied board
                    next_state.make_move((piece_copy, (tr, tc), captured))

                    # Evaluate the resulting position
                    eval_score, _ = minimax(
                        next_state, depth-1, alpha, beta, True)

                    # Update the best move if this is better
                    if eval_score < min_eval:
                        min_eval = eval_score
                        best_move = move

                    # Alpha-beta pruning
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break

                return min_eval, best_move

        # Run minimax on the board copy
        _, best_move = minimax(board_copy, self.max_depth,
                               float('-inf'), float('inf'), True)

        # If no valid moves, return None
        if best_move is None:
            return None

        # Convert the best move to the format expected by the UI
        piece, (to_r, to_c), jumped = best_move
        from_r, from_c = piece.row, piece.col

        # Find the corresponding real piece on the actual game board
        real_piece = game.board.board[from_r][from_c]

        return real_piece, (to_r, to_c), jumped

    def get_valid_moves_with_pieces(self, board, color):
        """Get all valid moves for a given color, with the associated pieces."""
        moves = []
        for piece in board.get_all_pieces(color):
            # Get all valid moves for this piece
            for (to_r, to_c), captured in self.get_piece_moves(board, piece).items():
                moves.append((piece, (to_r, to_c), captured))
        return moves

    def get_piece_moves(self, board, piece):
        """Get all valid moves for a specific piece."""
        moves = {}

        # Check normal moves (non-jumps)
        directions = self.get_directions(piece)
        for dr, dc in directions:
            row, col = piece.row + dr, piece.col + dc
            if 0 <= row < 8 and 0 <= col < 8 and board.board[row][col] == 0:
                moves[(row, col)] = []
                # Check for jumps
        self.check_jumps(board, piece, piece.row, piece.col, [], moves, set())

        return moves

    def get_directions(self, piece):
        """Get valid movement directions based on piece type."""
        if piece.king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece.color == 'r':  # Red moves down
            return [(1, -1), (1, 1)]
        else:  # Black moves up
            return [(-1, -1), (-1, 1)]

    def check_jumps(self, board, piece, row, col, captured, moves, visited):
        """Recursively check for jump moves."""
        directions = self.get_directions(piece) if not captured else [
            (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            mid_row, mid_col = row + dr, col + dc
            jump_row, jump_col = row + 2*dr, col + 2*dc

            # Check if jump is valid
            if (0 <= mid_row < 8 and 0 <= mid_col < 8 and
                0 <= jump_row < 8 and 0 <= jump_col < 8 and
                board.board[mid_row][mid_col] != 0 and
                board.board[mid_row][mid_col].color != piece.color and
                board.board[jump_row][jump_col] == 0 and
                (mid_row, mid_col) not in captured and
                    (jump_row, jump_col) not in visited):

                # Add this jump to moves
                new_captured = captured + [(mid_row, mid_col)]
                moves[(jump_row, jump_col)] = new_captured

                # Check for additional jumps
                visited_with_jump = visited.union({(jump_row, jump_col)})
                self.check_jumps(board, piece, jump_row, jump_col,
                                 new_captured, moves, visited_with_jump)

    def evaluate(self, state):
        """Evaluate the board position for the AI player."""
        # Count material
        # Kings are worth more than regular pieces
        material_value = 0
        position_value = 0
        king_value = 1.5  

        for row in range(8):
            for col in range(8):
                piece = state.board[row][col]
                if piece != 0:
                    # Material value
                    piece_value = king_value if piece.king else 1
                                   if piece.color == self.color:
                        material_value += piece_value

                        # Positional bonuses
                        if piece.color == 'b':  # Black moves up
                            # Closer to promotion
                            position_value += (7 - row) * 0.1
                        else:  # Red moves down
                            position_value += row * 0.1  # Closer to promotion

                        # Edge bonus
                        if col == 0 or col == 7:
                            position_value += 0.2
                    else:
                        material_value -= piece_value

                        # Same positional considerations for opponent
                        if piece.color == 'b':
                            position_value -= (7 - row) * 0.1
                        else:
                            position_value -= row * 0.1

                        if col == 0 or col == 7:
                            position_value -= 0.2

        return material_value + position_value



                       
