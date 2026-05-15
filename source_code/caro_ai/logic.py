import random


class Game_Caro:
    def __init__(self, size = 15):
        self.size = size;
        self.board = [['.' for _ in range(size)] for _ in range(size)]
        self.current_player = 'X'

    # GIAO DI?N
    def display_board(self):
        print (" ", end='')
        for i in range(self.size):
            print(f" {i}", end='')
        print()

        for idx, row in enumerate(self.board):
            print(f"{idx} " + ' '.join(row))

        for i in range(self.get_available_moves(self.board).__len__()):
            print(self.get_available_moves(self.board)[i], end=' ')
        print()

    # Th?c hi?n b??c ?i
    def make_move(self, x, y):
        if self.board[x][y] == '.':
            self.board[x][y] = self.current_player
            if self.is_draw(self.board):
                print("It's a draw!")
                return True

            if self.check_win(x, y, self.board):
                self.display_board()
                print(f"Player {self.current_player} wins!")
                return True
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return False
        else:
            print("Invalid move. Try again.")
            return False

    # Ki?m tra th?ng thua sau n??c ?i nh?t ??nh
    def check_win(self, x, y, board):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            for d in [1, -1]:
                nx, ny = x + d * dx, y + d * dy
                while 0 <= nx < len(board) and 0 <= ny < len(board) and board[nx][ny] == board[x][y]:
                    count += 1
                    nx += d * dx
                    ny += d * dy
            if count >= 4:
                return True
        return False

    def is_draw(self, board):
        return all(cell != '.' for row in board for cell in row)
    
    # Tìm các n??c ?i kh? thi ?u tiên l?y theo các n??c ?ã ???c ?ánh
    def get_available_moves(self, board):
        moves = set()
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != '.':
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = i + dx, j + dy
                            if 0 <= nx < len(board) and 0 <= ny < len(board) and board[nx][ny] == '.':
                                moves.add((nx, ny))
        
        if not moves: moves.add((random.randint(1,len(board) - 2), random.randint(1, len(board) - 2)))
        return list(moves)
