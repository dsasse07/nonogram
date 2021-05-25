'''
          [1,2,1], [1,2], [4,1], [2], [3,2], [2,1]
[1,1,2]   * - * - * *
[2,2]     - * * - * *
[1,1,1]   * - * - * -
[4]       * * * * - -
[1,3]     - * - * * *
[1,1,1]   * - * - * -


'''
import random
import tkinter

NUM_COL = 6
NUM_ROW = 6

def main():
  board, cols = make_board()
  row_hints = get_row_hints(board)
  col_hints = get_col_hints(cols)

def make_board():
  '''
    - Create a NUM_ROW x NUM_COL sized matrix.
    - randomly assign each cell to either be "*" or " " to indicate
      the state of that cell of the board
    - We also create a dictionary of the values going down each column
      to eliminate a nested loop later
  '''
  board = []
  cols = {}
  for i in range(NUM_ROW):
    row = []
    for j in range(NUM_COL):
      if random.random() > 0.5:
        row.append('*')
        if j in cols: cols[j].append('*')
        else: cols[j] = ['*']
      else: 
        row.append(' ')
        if j in cols: cols[j].append(' ')
        else: cols[j] = [' ']
    board.append(row)
  return board, cols

def get_row_hints(board):
  '''
    INPUT: The completed game board matrix
    - Iterate through each row, to determien the lengths of sequential
      filled spaces to use as the hints.
    - Ex: if row == ['*', '*', ' ', ' ', '*'], row_hint == [2,1]
    OUTPUT: List of row_hint lists
  '''
  row_hints = []
  for row in board:
    sequence = count_sequence(row)
    row_hints.append(sequence)
  return row_hints

def get_col_hints(cols):
  '''
    INPUT: The columns dictionary created during board creation
    - Iterate through each key in cols, to determine the lengths of sequential
      filled spaces to use as the hints.
    - Ex: if col['0'] == ['*', '*', ' ', ' ', '*'], col_hint == [2,1]
    OUTPUT: List of col_hints lists
  '''
  col_hints = []
  for col in cols:
    sequence = count_sequence(cols[col])
    col_hints.append(sequence)
  return col_hints

def count_sequence(list):
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

main()
