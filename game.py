import pygame
import os
import math
from time import sleep

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
    '''
      Initializes game Instance using passed in GameBoard Instance and Screen Size
      Additionally calculates the pixel dimensions of the board tiles based on the number of columns and the screen size. 
        - Board size is doubled in the calculation to include tile space needed for hints
      Pieces sizes are used to calculate total board time dimensions
      All image files are loaded and saved to a dictionary
    '''
    self.board = board
    self.rects = {}
    self.screen_size = screen_size
    self.piece_size = (self.screen_size[0] // math.floor(self.board.get_size()[1] * 2), self.screen_size[1] // math.floor(self.board.get_size()[0] * 2))
    self.board_dimensions = (self.piece_size[0] * self.board.size[1] + self.piece_size[0], self.piece_size[1] * self.board.size[0] + self.piece_size[1])
    self.load_images()

  def run(self):
    pygame.init()
    '''
      - Creates the main window frame for the game with specified size
      - Draws the static elements (hints & button)
      - Begins Game loop of listening for events.
    '''
    self.screen = pygame.display.set_mode(self.screen_size)
    self.draw_row_hints()
    self.draw_col_hints()
    self.draw_check_button()
    # Start game loop of listening for events
    # When the quit event is triggered, end the loop
    running = True
    won = False
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
          position = pygame.mouse.get_pos()
          won = self.handle_click(position, won) # Will only return true if click button is clicked and win condition met
      if won:
        self.draw_win_banner()
        sound = pygame.mixer.Sound(relative_path('sounds/win.wav'))
        sound.play()
        running = False
      self.draw_board() #Redraw the updated board
      pygame.display.flip() # Refreshes game window.
    if won: sleep(2) # Allows time for win sound to play and banner to be seen
    pygame.quit()

  def draw_board(self):
    # Set top-left to center of top-left quadrant to center the grid on screen
    top_left = (self.screen_size[0] - self.board_dimensions[0], self.screen_size[1] - self.board_dimensions[1])
    self.rects['board'] = top_left
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
    '''
      Iterates through each of the row hints in the GameBoard instance and draws them to the screen.
      The top-left position of the first element must be offset from the board by the number of hints * piece dimensions
      to ensure no overlap with the board.
    '''
    font = pygame.font.Font(pygame.font.get_default_font(), 24) # Loads default system font
    for i in range(len(self.board.row_hints)):
      num_hints = len(self.board.row_hints[i])
      for j in range(num_hints):
        text = self.board.row_hints[i][j]
        hint = pygame.font.Font.render(font, str(text), False, (255,255,255))
        top_left = (self.screen_size[0] - self.board_dimensions[0] - ((num_hints - j) * self.piece_size[1]), (self.screen_size[1] - self.board_dimensions[1] + (i * self.piece_size[1]) + (self.piece_size[1] // 4)) )
        self.screen.blit(hint, top_left)
  
  def draw_col_hints(self):
    '''
      Iterates through each of the column hints in the GameBoard instance and draws them to the screen.
      The top-left position of the first element must be offset from the board by the number of hints * piece dimensions
      to ensure no overlap with the board.
    '''
    font = pygame.font.Font(pygame.font.get_default_font(), 24)
    for i in range(len(self.board.col_hints)):
      num_hints = len(self.board.col_hints[i])
      for j in range(num_hints):
        text = self.board.col_hints[i][j]
        hint = pygame.font.Font.render(font, str(text), False, (255,255,255))
        top_left = (self.screen_size[0] - self.board_dimensions[0] + (i * self.piece_size[0]) + (self.piece_size[0] // 4) , (self.screen_size[1] - self.board_dimensions[1] - ((num_hints - j) * self.piece_size[1])) )
        self.screen.blit(hint, top_left)

  def draw_check_button(self):
    '''
      Draws the static "Check Button" on the screen by blitting the "Check" sprite
    '''
    image = self.images['check']
    top_left = ( self.screen_size[0] - 3 * self.piece_size[0], 0 + self.piece_size[1] * 0.5)
    self.rects['check'] = top_left
    self.screen.blit(image, top_left)
  
  def draw_win_banner(self):
    '''
      Draws the static "Winner Banner" on the screen by blitting the "Winner" sprite
    '''
    image = self.images['winner']
    top_left = (self.piece_size[0], 2 * self.piece_size[1])
    self.rects['win'] = top_left
    self.screen.blit(image, top_left)

  def load_images(self):
    # Map the file name to the image object created by pygame
    self.images = {}
    for file_name in os.listdir(relative_path('tiles')):
      if not file_name.endswith('.png'): continue # If the file isn't a png, don't load it
      image = pygame.image.load(r'tiles/' + file_name) # Load image file
      if not file_name == 'winner.png':
        scale_size = self.piece_size if not file_name == 'check.png' else (self.piece_size[0]*2, self.piece_size[1])
        image = pygame.transform.scale(image, scale_size) #Scale image based on game window and needed rows/cols
      # create new entry in dict with filename as key
      self.images[file_name.split('.')[0]] = image

  def get_image(self, piece):
    '''
      returns the tile image to match the state of the tile.
    '''
    if piece.clicked:
      return self.images['selected']
    else:
      return self.images['unselected']
  
  def handle_click(self, position, won):
    if won: return # If the game is over, clicks no longer change anything
    board_coords = self.get_board_coords(position) # Checks if click occurred on the board. If so, returns index of piece clicked
    if board_coords: 
      piece = self.board.get_piece(board_coords[0], board_coords[1]) #Get the Piece instance at the Board coords
      self.board.handle_click(piece) # Toggle the clicked state of the Piece
    elif self.clicked_check(position):  # Checks if click occured on the "Check Button", if so, check for win condition.
      return self.check_answers()

  def get_board_coords(self, position):
    '''
      Input: Mouse position tuple in pixels of screen window.
      Creates bounding rectangle for the board
      If mouse position is within bounding rect, calculates and returns Piece index
    '''
    min_board_x = self.rects['board'][0]
    max_board_x = min_board_x + (self.board.get_size()[0] * self.piece_size[0])
    min_board_y = self.rects['board'][1]
    max_board_y = min_board_x + (self.board.get_size()[1] * self.piece_size[1])
    if min_board_x <= position[0] <= max_board_x and min_board_y <= position[1] <= max_board_y:
      row = (position[1] - min_board_y) // self.piece_size[1]
      col = (position[0] - min_board_x) // self.piece_size[0]
      return row, col
    return None
  
  def clicked_check(self, position):
    '''
      Input: Mouse position tuple
      Creates bounding rect for the Check button
      Returns boolean value for if click occured in this bounding rect
    '''
    min_check_x = self.rects['check'][0]
    max_check_x = min_check_x + 2 * self.piece_size[0]
    min_check_y = self.rects['check'][1]
    max_check_y = min_check_y + 2 * self.piece_size[1]
    return min_check_x <= position[0] <= max_check_x and min_check_y <= position[1] <= max_check_y

  def check_answers(self):
    '''
      Iterates through each piece to determine if its clicked state matches 
      its "is_selected" state generated during board creation.
    '''
    for row in range(self.board.size[0]):
      for col in range(self.board.size[1]):
        piece = self.board.get_piece(row, col)
        if not piece.is_selected == piece.clicked:
          sound = pygame.mixer.Sound(relative_path('sounds/error.wav'))
          sound.play()
          return False
    return True