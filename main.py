from game import Game
from game_board import GameBoard

SIZE = (6,6)
PROBABILITY = 0.7

board = GameBoard(SIZE, PROBABILITY)
screen_size = (SIZE[0] * 80, SIZE[1] * 80)
game = Game(board, screen_size)
game.run()