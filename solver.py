import math

class SSolver():
    # initialize board
    def __init__(self, board):
        self.board = board

    # returns the next empty square in the sudoku board
    def next_empty(self, empty_val):
        rows = len(self.board)
        cols = len(self.board[0])

        for r in range(rows):
            for c in range(cols):
                if self.board[r][c] == empty_val: return (r, c)
    
        return None

    def valid(self, board, number, position):
        rows = len(self.board)
        cols = len(self.board[0])
        square_size = int(math.sqrt(rows))
        r, c = position

        # check row
        if number in board[r]: return False

        # check col
        curr_col = [board[row][c] for row in range(rows)]
        if number in curr_col: return False

        # check square
        square_x_idx = c // square_size
        square_y_idx = r // square_size
        for row in range(square_y_idx * square_size, (square_y_idx * square_size) + square_size):
            for col in range(square_x_idx * square_size, (square_x_idx * square_size) + square_size):
                if board[row][col] == number and (row, col) != position:
                    return False
    
    # modifies self.board to solve it
    def solve(self):
        empty_val = 0
        next_empty_pos = self.next_empty(empty_val)

        if not next_empty_pos:
            return True
        else:
            row, col = next_empty_pos

        for i in range(1, 10):
            if self.valid(board=self.board, number=i, position=(row, col)):
                self.board[row][col] = i
                if self.solve():
                    return True

        self.board[row][col] = 0
        return False

