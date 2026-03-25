# This is layout of checkers pieces and board

class Piece:
    def __init__(self, row, col, color, king=False):
        self.row = row
        self.col = col
        self.color = color  # "r" or "b"
        self.king = king

    def make_king(self):
        self.king = True

    def __repr__(self):
        '''Return a string representation of the piece for display purposes'''
        return self.color.upper() if self.king else self.color

class Board:
    def __init__(self):
        self.board = []
        self.create_board()

    def create_board(self):
        """
        Places pieces in initial configuration:
        - Red occupies rows 0 to 2
        - Black occupies rows 5 to 7
        - Pieces only on dark squares (even+odd or odd+even)
        """
        for row in range(8):
            self.board.append([])
            for col in range(8):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.board[row].append(Piece(row, col, "r"))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, "b"))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def print_board(self):
        """Print the board in a readable format"""
        for row in self.board:
            print([str(p) if p != 0 else "." for p in row])

if __name__ == "__main__":
    board = Board()
    board.print_board()
