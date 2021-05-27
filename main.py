from lib.game import Game
from lib.game_board import GameBoard


SIZE = (6,6)        # Recommended  5 <= SIZE <= 15
PROBABILITY = 0.7   # Recommended 0.3 <= PROBABILITY <= 0.8

board = GameBoard(SIZE, PROBABILITY)
screen_size = (SIZE[0] * 80, SIZE[1] * 80)
game = Game(board, screen_size)
game.run()