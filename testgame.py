from game import Game
from board import Piece

'''An attempt at unit tests for the checkers game logic.
   These tests cover basic moves, captures, 
   king promotions, and game over conditions.'''

def test_basic_move():
    game = Game()

    # Move red piece from (2, 1) to (3, 0)
    piece = game.board.board[2][1]
    valid_moves = game.get_valid_moves(piece)
    assert (3, 0) in valid_moves, "Move (2,1) to (3,0) should be valid"

    game.move(piece, 3, 0)
    assert game.board.board[3][0] == piece, "Piece should have moved to (3,0)"
    assert game.board.board[2][1] == 0, "Original square should now be empty"

def test_king_promotion():
    game = Game()

    # Simulate a red piece one step away from kinging
    piece = Piece(6, 1, "r")
    game.board.board[6][1] = piece
    game.move(piece, 7, 0)

    assert piece.king is True, "Red piece should be promoted to king"
    assert str(piece) == "R", "King representation should be uppercase 'R'"

def test_capture_move():
    game = Game()

    # Set up red piece and black enemy in range
    red_piece = Piece(2, 1, "r")
    black_piece = Piece(3, 2, "b")
    game.board.board[2][1] = red_piece
    game.board.board[3][2] = black_piece

    # Destination should be (4, 3) if capture is valid
   valid_moves = game.get_valid_moves(red_piece)
    assert (4, 3) in valid_moves, "Capture move should be available"
    assert valid_moves[(4, 3)] == [(3, 2)], "Capture path should show jumped piece"

    game.move(red_piece, 4, 3)
    game.remove_piece(3, 2)
    assert game.board.board[3][2] == 0, "Black piece should be removed after capture"
    assert game.board.board[4][3] == red_piece, "Red piece should land correctly after jump"

def test_multiple_jump_paths():
    game = Game()

    # Clear the board
    game.board.board = [[0 for _ in range(8)] for _ in range(8)]

    # Place a red piece
    red_piece = Piece(2, 3, "r")
    game.board.board[2][3] = red_piece

    # Place black pieces for two possible jump paths
    game.board.board[3][2] = Piece(3, 2, "b")  # left path
    game.board.board[5][0] = Piece(5, 0, "b")  # left path second jump

    game.board.board[3][4] = Piece(3, 4, "b")  # right path
    game.board.board[5][6] = Piece(5, 6, "b")  # right path second jump

    game.board.board[5][2] = Piece(5, 2, "b")  # right path second jump

    # First move from (2,3) to (4,1) OR (4,5) should be possible
    valid_moves = game.get_valid_moves(red_piece)
    assert (4, 1) in valid_moves or (4, 5) in valid_moves, "First capture move in both directions should be available"

    # Choose one path and ensure second jump exists
    game.move(red_piece, 4, 1)
    assert game.board.board[3][2] == 0  # captured
    assert game.board.board[4][1] == red_piece


    next_moves = game.get_valid_moves(red_piece)
    assert (6, -1) not in next_moves  # invalid
    assert (6, -1) not in next_moves and (6, 3) in next_moves, "Second jump along the same path should be detected"

    # Complete second jump
    game.move(red_piece, 6, 3)
    assert game.board.board[5][2] == 0   # second capture
    assert game.board.board[6][3] == red_piece

def test_illegal_move_rejected():
    game = Game()

    # Try to move a red piece illegally (diagonal two-square move without capture)
    piece = game.board.board[2][1]
    invalid_target = (4, 3)  # Not a valid jump since no enemy in between

    valid_moves = game.get_valid_moves(piece)
    assert invalid_target not in valid_moves, "Illegal move should not be allowed"

def test_backward_movement_non_king():
    game = Game()

    # Place a red piece
    piece = game.board.board[2][1]

    # Attempt to move backward
    invalid_target = (1, 0)  # Backward move
    valid_moves = game.get_valid_moves(piece)
    assert invalid_target not in valid_moves, "Non-king pieces should not move backward"
def test_king_movement():
    game = Game()

    # Promote a piece to king
    piece = Piece(4, 4, "r", king=True)
    game.board.board[4][4] = piece

    # Test all diagonal directions
    valid_moves = game.get_valid_moves(piece)
    assert (3, 3) in valid_moves, "King should move backward-left"
    assert (3, 5) in valid_moves, "King should move backward-right"
    assert (5, 3) in valid_moves, "King should move forward-left"
    assert (5, 5) in valid_moves, "King should move forward-right"

def test_turn_enforcement():
    game = Game()

    # Attempt to move a black piece during red's turn
    black_piece = game.board.board[5][0]
    valid_moves = game.get_valid_moves(black_piece)
    assert not valid_moves, "Black pieces should not move during red's turn"

def test_edge_of_board():
    game = Game()
    #clear out all default pieces so we only have this one on the board
    game.board.board = [[0 for _ in range(8)] for _ in range(8)]    
    
    # Place a red piece near the edge
    piece = Piece(0, 1, "r")
    game.board.board[0][1] = piece

    # Attempt to move off the board
    valid_moves = game.get_valid_moves(piece)
    assert (1, 0) in valid_moves, "Move within bounds should be valid"
    assert (-1, -1) not in valid_moves, "Move off the board should not be valid"

def test_game_over_no_pieces():
    game = Game()

    # Remove all black pieces
    game.board.board = [[0 for _ in range(8)] for _ in range(8)]
    game.board.board[0][1] = Piece(0, 1, "r")  # Only one red piece remains

    assert game.is_game_over(), "Game should end when one player has no pieces"
    assert game.get_winner() == "Red", "Red should win when black has no pieces"

def test_game_over_no_moves():
    game = Game()

    # Set up a scenario where black has no valid moves
    game.board.board = [[0 for _ in range(8)] for _ in range(8)]
    game.board.board[0][1] = Piece(0, 1, "r")
    game.board.board[0][3] = Piece(0, 3, "r")
    game.board.board[1][2] = Piece(1, 2, "b")  # Black piece blocked by red

    assert game.is_game_over(), "Game should end when one player has no valid moves"
    assert game.get_winner() == "Red", "Red should win when black has no valid moves"

def test_multi_jump_mixed_directions():
    game = Game()

    # Clear the board
    game.board.board = [[0 for _ in range(8)] for _ in range(8)]

    # Place a red piece
    red_piece = Piece(2, 3, "r")
    game.board.board[2][3] = red_piece

    # Place black pieces for mixed-direction jumps
    game.board.board[3][2] = Piece(3, 2, "b")  # left path
    game.board.board[5][2] = Piece(5, 2, "b")  # right path
    # First move from (2,3) to (4,1) should be possible
    valid_moves = game.get_valid_moves(red_piece)
    assert (4, 1) in valid_moves, "First capture move should be available"

    # Perform the first jump
    game.move(red_piece, 4, 1)
    game.remove_piece(3, 2)
    assert game.board.board[3][2] == 0, "First captured piece should be removed"
    assert game.board.board[4][1] == red_piece, "Red piece should land correctly"

    # Check for the second jump in a different direction
    valid_moves = game.get_valid_moves(red_piece)
    assert (6, 3) in valid_moves, "Second jump in a different direction should be available"

def run_all_tests():
    test_basic_move()
    test_king_promotion()
    test_capture_move()
    test_multiple_jump_paths()
    test_illegal_move_rejected()
    test_backward_movement_non_king()
    test_king_movement()
    test_turn_enforcement()
    test_edge_of_board()
    test_game_over_no_pieces()
    test_game_over_no_moves()
    test_multi_jump_mixed_directions()
    print("All tests passed. Congratualation! :)")

if __name__ == "__main__":
    run_all_tests()



