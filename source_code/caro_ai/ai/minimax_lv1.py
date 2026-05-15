import time
import math

class agent:
    def __init__(self, depth: int = 3, ai_player: str = 'O'):
        self.depth = depth
        self.ai_player = ai_player
        self.node_visted = 0

    # Hàm đánh giá
    def _evaluate(self, size):
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x in range(size):
            for y in range(size):
                if self.board[x][y] != '.':
                    player = self.board[x][y]
                    for dx, dy in directions:
                        close = 0
                        count = 1
                        nx, ny = x -dx, y - dy
                        if 0 <= nx < size and 0 <= ny < size:
                            if self.board[nx][ny] == player:
                                continue
                            if self.board[nx][ny] == '.':
                                pass
                            else:
                                close += 1

                        for d in range(1, 4):
                            nx, ny = x + d * dx, y + d * dy
                            if 0 <= nx < size and 0 <= ny < size:
                                if self.board[nx][ny] == player:
                                    count += 1
                                if self.board[nx][ny] == '.':
                                    pass
                                else:
                                    close += 1
                            else:
                                break
                        point = 0
                        if close == 2: continue # Chuỗi bị chặn cả hai đầu không có giá trị
                        elif count == 3 and close == 1: point = 1000
                        elif count == 3 and close == 0: point = 4000 # Chuỗi 3 không bị chặn có giá trị cao hơn
                        elif count == 2 and close == 1: point = 100
                        elif count == 2 and close == 0: point = 1000 # Chuỗi 2 không bị chặn có giá trị cao hơn
            
                        if player == self.ai_player: # Lượt máy
                            score += point
                        else: # Lượt người
                            # Điểm âm cho người chơi và trọng số cao hơn để AI ưu tiên chặn
                            score -= point * 5
        return score

    # Minimax lv 1
    def _minimax(self, game, depth, maximizing, x, y):
        self.node_visted += 1
        if game.check_win(x, y, self.board):
            return -(500000 + depth) if maximizing else 500000 + depth
        if depth == 0 or game.is_draw(self.board):
            return self._evaluate(game.size)

        if maximizing:
            max_eval = -math.inf
            for move in game.get_available_moves(self.board):
                x, y = move
                self._test_move(x, y)
                eval = self._minimax(game, depth - 1, False, x, y)
                self._undo_move(x, y)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = math.inf
            for move in game.get_available_moves(self.board):
                x, y = move
                self._test_move(x, y)
                eval = self._minimax(game, depth - 1, True, x, y)
                self._undo_move(x, y)
                min_eval = min(min_eval, eval)
            return min_eval

    # Tìm nước đi tốt nhất bằng minimax 
    def get_best_move(self, game):  
        self.node_visted = 0
        start_time = time.time()

        self.board = [row.copy() for row in game.board]
        self.player = game.current_player 
        best_score = -math.inf
        move_to_make = None
        best_local = -math.inf

        for move in game.get_available_moves(self.board):
            x, y = move
            self._test_move(x, y)
            score = self._minimax(game, self.depth - 1, False, x, y)
            local = self._evaluate(game.size)
            self._undo_move(x, y)
            if score > best_score:
                best_score = score
                move_to_make = (x, y)
            elif score == best_score and local > best_local:
                move_to_make = (x, y)
                best_local = local
        return move_to_make, self.node_visted, time.time() - start_time

    def _test_move(self, x, y):
        self.board[x][y] = self.player
        self.player = 'O' if self.player == 'X' else 'X'

    def _undo_move(self, x, y):
        self.board[x][y] = '.'
        self.player = 'O' if self.player == 'X' else 'X'