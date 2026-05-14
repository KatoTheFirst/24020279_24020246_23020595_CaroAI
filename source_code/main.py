from caro_ai.logic import Game_Caro
from caro_ai.ai.minimax_lv1 import agent
def main():
    ai = agent(depth=3)
    game = Game_Caro(9)
    while True:
        game.display_board()
        try:
            if game.current_player == 'X':
                move = input(f"Player {game.current_player}, enter your move (x y): ")
                x, y = map(int, move.split())
            else:
                print(f"Player {game.current_player} (AI) is making a move...")
                (x, y), nodes, elapsed_time = ai.get_best_move(game)
                print(f"AI chooses: {x} {y}")
                print(f"Nodes visited: {nodes}") 
                print(f"Time taken: {elapsed_time:.2f} seconds)")
            if game.make_move(x, y):
                break
        except ValueError:
            print("Invalid input. Please enter coordinates as 'x y'.")

if __name__ == "__main__":
    main()