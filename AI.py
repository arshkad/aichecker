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
