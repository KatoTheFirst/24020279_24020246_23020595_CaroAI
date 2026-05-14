class Game_Caro:
    def __init__(self, size = 15):
        self.size = size;
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'
    def display_board(self):
        print (" ", end='')
        for i in range(self.size):
            print(f" {i}", end='')
        print()

        for idx, row in enumerate(self.board):
            print(f"{idx} " + ' '.join(row))

        for i in range(self.get_available_moves().__len__()):
            print(self.get_available_moves()[i], end=' ')
        print()
    def make_move(self, x, y):
        if self.board[x][y] == '.':
            self.board[x][y] = self.current_player
            if self.is_draw():
                print("It's a draw!")
                return True

            if self.check_win(x, y):
                self.display_board()
                print(f"Player {self.current_player} wins!")
                return True
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return False
        else:
            print("Invalid move. Try again.")
            return False
    def check_win(self, x, y):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for d in [1, -1]:
                nx, ny = x + d * dx, y + d * dy
                while 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == self.board[x][y]:
                    count += 1
                    nx += d * dx
                    ny += d * dy
            if count >= 4:
                return True
        return False
    def is_draw(self):
        return all(cell != '.' for row in self.board for cell in row)
    def get_available_moves(self):
        moves = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != '.':
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = i + dx, j + dy
                            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == '.':
                                moves.add((nx, ny))
        
        if not moves: moves.add((self.size//2, self.size//2))
        return list(moves)
        
    def undo_move(self, x, y):
        self.board[x][y] = '.'
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def test_move(self, x, y):
        self.board[x][y] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
