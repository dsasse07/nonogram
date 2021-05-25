import pygame
import os
import math

'''
  Used to allow relative path importing
'''
dirname = os.path.dirname(__file__)
def relative_path(r_path):
  return os.path.join(dirname, r_path)

'''
    This file initializes the game instance and running logic.
'''
from game_board import GameBoard

class Game():
  def __init__(self, board, screen_size):
    self.board = board
    self.screen_size = screen_size
    self.piece_size = (self.screen_size[0] // math.floor(self.board.get_size()[1] * 2), self.screen_size[1] // math.floor(self.board.get_size()[0] * 2))
    self.board_dimensions = (self.piece_size[0] * self.board.size[1] + self.piece_size[0], self.piece_size[1] * self.board.size[0] + self.piece_size[1])
    self.load_images()

  def run(self):
    pygame.init()
    # Creates the main window frame for the game with specified size
    self.screen = pygame.display.set_mode(self.screen_size)
    running = True

    # Start game loop of listening for events
    # When the quit event is triggered, end the loop
    self.draw_row_hints()
    self.draw_col_hints()
    self.draw_check_button()
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          self.handle_click(position)
      self.draw_board()

      pygame.display.flip()
    pygame.quit()

  def draw_board(self):
    # Set top-left to center of top-left quadrant to center the grid on screen
    top_left = (self.screen_size[0] - self.board_dimensions[0], self.screen_size[1] - self.board_dimensions[1])
    # Iterate through each piece of the game board and "blit" its image
    for row in range(self.board.get_size()[0]):
      for col in range(self.board.get_size()[1]):
        piece = self.board.get_piece(row, col)
        image = self.get_image(piece)
        self.screen.blit(image, top_left)
        #Shift current "top-left position for next tile to the right"
        top_left = top_left[0] + self.piece_size[0], top_left[1]
      # Shift top-left to the next row down, and back to original left pos.
      top_left = self.screen_size[0] - self.board_dimensions[0], top_left[1] + self.piece_size[1]
    
  def draw_row_hints(self):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    for i in range(len(self.board.row_hints)):
      num_hints = len(self.board.row_hints[i])
      for j in range(num_hints):
        text = self.board.row_hints[i][j]
        hint = pygame.font.Font.render(font, str(text), False, (255,255,255))
        top_left = (self.screen_size[0] - self.board_dimensions[0] - ((num_hints - j) * self.piece_size[1]), (self.screen_size[1] - self.board_dimensions[1] + (i * self.piece_size[1]) + (self.piece_size[1] // 4)) )
        self.screen.blit(hint, top_left)
  
  def draw_col_hints(self):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    for i in range(len(self.board.col_hints)):
      num_hints = len(self.board.col_hints[i])
      for j in range(num_hints):
        text = self.board.col_hints[i][j]
        hint = pygame.font.Font.render(font, str(text), False, (255,255,255))
        top_left = (self.screen_size[0] - self.board_dimensions[0] + (i * self.piece_size[0]) + (self.piece_size[0] // 4) , (self.screen_size[1] - self.board_dimensions[1] - ((num_hints - j) * self.piece_size[1])) )
        self.screen.blit(hint, top_left)

  def draw_check_button(self):
    image = self.images['check']
    top_left = ( self.screen_size[0] // 2 + self.piece_size[0], self.screen_size[1] - self.piece_size[1])
    self.screen.blit(image, top_left)

  def load_images(self):
    # Map the file name to the image object created by pygame
    self.images = {}
    for file_name in os.listdir(relative_path('tiles')):
      if not file_name.endswith('.png'): continue # If the file isn't a png, don't load it
      image = pygame.image.load(r'tiles/' + file_name) # Load image file
      scale_size = self.piece_size if not file_name == 'check.png' else (self.piece_size[0]*2, self.piece_size[1])
      image = pygame.transform.scale(image, scale_size) #Scale image based on game window and needed rows/cols
      # create new entry in dict with filename as key
      self.images[file_name.split('.')[0]] = image

  def get_image(self, piece):
    if piece.clicked:
      return self.images['selected']
    else:
      return self.images['unselected']
  
  def handle_click(self, position):
    min_board_x = self.screen_size[0] - self.board_dimensions[0]
    max_board_x = self.screen_size[0] - self.piece_size[0]
    min_board_y = self.screen_size[1] - self.board_dimensions[1]
    max_board_y = self.screen_size[1] - self.piece_size[1]
    if min_board_x <= position[0] <= max_board_x and min_board_y <= position[1] <= max_board_y:
      row = (position[1] - min_board_y) // self.piece_size[1]
      col = (position[0] - min_board_x) // self.piece_size[0]
      piece = self.board.get_piece(row,col)
      self.board.handle_click(piece)
    min_check_x = self.screen_size[0] // 2 + self.piece_size[0]
    max_check_x = min_check_x + (2* self.piece_size[0])
    min_check_y = self.screen_size[1] - self.piece_size[1]
    max_check_y = self.screen_size[1]
    if min_check_x <= position[0] <= max_check_x and min_check_y <= position[1] <= max_check_y:
      self.check_answers()
  
  def check_answers(self):
    for row in range(self.board.size[0]):
      for col in range(self.board.size[1]):
        if self.board.answers[row][col] == '*' and not self.board.get_piece(row, col).clicked:
          print('wrong')
          return False
        if self.board.answers[row][col] == ' ' and self.board.get_piece(row, col).clicked:
          print('wrong')
          return False
    print('correct')
    return True
  
  # def _marked_and_incorrect(self, i, j):
  #   return self.board.get_piece(i,j).clicked and not self.board.answers[i][j] == '*'
  
  # def _unmarked_and_correct(self, i, j):
  #   return not self.board.get_piece(i,j).clicked and self.board.answers[i][j] == '*'
