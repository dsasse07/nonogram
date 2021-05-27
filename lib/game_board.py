from lib.piece import Piece
import random

class GameBoard():
  def __init__(self, size, probability):
    '''
      Initializes game board of specific size. Uses probability to determine selected tiles.
    '''
    self.size = size
    self.probability = probability
    self.cols = {} # Stores array for each col for hint generation
    self.rows = {} # Stores array for each row for hint generation
    self.setBoard() # Creates a size[0] x size[1] board of Piece instances
    self.row_hints = self.get_row_hints()
    self.col_hints = self.get_col_hints()

  def setBoard(self):
    '''
      creates size[0] x size[1] board of game Pieces.
      Additionally creates arrays for row/value cols with string elements
      These string arrays will be used to generate hints
    '''
    self.board = []
    for i in range(self.size[0]):
      row = []
      for j in range(self.size[1]):
        is_selected = random.random() < self.probability
        self.add_to_row(i, is_selected)
        self.add_to_col(j, is_selected)
        piece = Piece(is_selected)
        row.append(piece)
      self.board.append(row)
  
  def get_size(self):
    return self.size
  
  def get_piece(self, row, col):
    '''
      Returns Piece instance at speficied index of the board
    '''
    return self.board[row][col]

  def add_to_row(self, row, is_selected):
    '''
      Creates string value from Piece boolean state
    '''
    value = ' '
    if is_selected: value = '*'
    if row in self.rows: self.rows[row].append(value)
    else: self.rows[row] = [value]

  def add_to_col(self, col, is_selected):
    '''
      Creates string value from Piece boolean state
    '''
    value = ' '
    if is_selected: value = '*'
    if col in self.cols: self.cols[col].append(value)
    else: self.cols[col] = [value]

  def get_row_hints(self):
    '''
      INPUT: The completed game board matrix
      - Iterate through each row, to determien the lengths of sequential
        filled spaces to use as the hints.
      - Ex: if row == ['*', '*', ' ', ' ', '*'], row_hint == [2,1]
      OUTPUT: List of row_hint lists
    '''
    row_hints = []
    for row in self.rows:
      this_row = self.rows[row]
      sequence = self._count_sequence(this_row)
      row_hints.append(sequence)
    return row_hints

  def get_col_hints(self):
    '''
      INPUT: The columns dictionary created during board creation
      - Iterate through each key in cols, to determine the lengths of sequential
        filled spaces to use as the hints.
      - Ex: if col['0'] == ['*', '*', ' ', ' ', '*'], col_hint == [2,1]
      OUTPUT: List of col_hints lists
    '''
    col_hints = []
    for col in self.cols:
      sequence = self._count_sequence(self.cols[col])
      col_hints.append(sequence)
    return col_hints

  def _count_sequence(self, list):
    '''
      INPUT: a list of spaces (Ex: ['*', '*', ' ', ' ', '*'])
      - join list to a string (Ex: '**  *')
      - split the string where there are spaces (Ex: ['**', '', '*')
      - iterate through these groups, and append the lengths that are > 0 to the list
      OUTPUT: List ints representing sequential sequence lengths
    '''
    sequences = ''.join(list).split(" ")
    list_counts = []
    for group in sequences:
      if len(group) > 0:
        list_counts.append(len(group))
    return list_counts
  
  def handle_click(self, piece):
    '''
      Takes in a piece and toggles its clicked state
    '''
    piece.clicked = not piece.clicked
