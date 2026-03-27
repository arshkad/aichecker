from game import Game
from AI import MinimaxAI

def get_input():
    '''Get input from the player for their move.'''
    while True:
        entry = input("Enter piece ROW (0–7, 'q' to quit, 's' to surrender): ").strip().lower()
        if entry == 'q':
            return None
        if entry == 's':
            return 'surrender'
        
        try:
            from_row = int(entry)
            from_col = int(input("Enter piece COL (0–7): ").strip())
            to_row   = int(input("Enter DESTINATION ROW (0–7): ").strip())
            to_col   = int(input("Enter DESTINATION COL (0–7): ").strip())
        except ValueError:
            print(" Invalid input. Please enter integers or one of 'q'/'s'.\n")
            continue

        # now check bounds
        if not all(0 <= v < 8 for v in (from_row, from_col, to_row, to_col)):
            print(" Coordinates must all be between 0 and 7.\n")
            continue

        return from_row, from_col, to_row, to_col
    
def main():
    '''Main function to run the checkers game.'''
    game = Game()
    show_instructions()
    
    while not game.is_game_over():
        print(f"\nCurrent Turn: {'Red' if game.turn == 'r' else 'Black'}")
        game.board.print_board()

        move = get_input()
        if move is None:
            print("\nGame quit by player.")
            return
            
        if move == 'surrender':
            print(f"\n{'Red' if game.turn == 'r' else 'Black'} surrenders. "
                             f"{'Black' if game.turn == 'r' else 'Red'} wins!")
            return

        from_row, from_col, to_row, to_col = move
        piece = game.board.board[from_row][from_col]

        if piece == 0 or piece.color != game.turn:
            print("Invalid piece selected. Try again.")
            continue

        valid_moves = game.get_valid_moves(piece)

        if (to_row, to_col) in valid_moves:
            game.move(piece, to_row, to_col)

            # Handle capture
            jumped = valid_moves[(to_row, to_col)]
            for j_row, j_col in jumped:
                game.remove_piece(j_row, j_col)

            # Check for additional jumps
            while True:
                valid_moves = game.get_valid_moves(piece)
                additional_jumps = {move: jumps for move, jumps in valid_moves.items() if jumps}
                if additional_jumps:
                    print("\nAdditional jump available!")
                    game.board.print_board()
                    move = get_input()
                    if move is None:
                        print("\nGame quit by player.")
                        return
                    from_row, from_col, to_row, to_col = move
                    if (to_row, to_col) in additional_jumps:
                        game.move(piece, to_row, to_col)
                                                jumped = additional_jumps[(to_row, to_col)]
                        for j_row, j_col in jumped:
                            game.remove_piece(j_row, j_col)
                    else:
                        print("Invalid move. Try again.")
                        continue
                else:
                    break

            game.switch_turn()
        else:
            print("Invalid move. Try again.")
            
        # AI's turn
        if game.turn == 'b':  
            print("AI is making its move...")
            # Initialize the AI with the black color
            ai = MinimaxAI('b')
            # Use the AI to choose the best move
            ai_move = ai.choose_move(game)

            if ai_move is not None:
                piece, (to_row, to_col), captured = ai_move
                game.move(piece, to_row, to_col)  # Apply the move

                # Handle captures
                for j_row, j_col in captured:
                    game.remove_piece(j_row, j_col)
                    
                # Switch turn back to the player
                game.switch_turn()  
            else:
                print("AI has no valid moves. Player wins!")
                break

            continue

        if game.is_game_over():
            break

    # Game is over, show winner
    winner = game.get_winner()
    if winner:
        print(f"\nGame Over! {winner} wins!")
    else:
        print("\nGame Over! It's a draw!")

def show_instructions():
    print("\n" + "="*40)
    print("Welcome to Competitive Checkers!")
    print("="*40)
    print("HOW TO PLAY:")
    print("- Players take turns: Red ('r') goes first, then Black ('b').")
    print("- Pieces move diagonally.")
    print("- To move, enter coordinates as:")
    print("  → ROW and COLUMN of the piece to move")
    print("  → ROW and COLUMN of the destination square")
    print("- Captures and king promotions are automatic")
    print("- Kings are shown as uppercase (R or B)")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()


