# Pycross

![Pycross Logo](https://i.imgur.com/k58W2eP.png)

[Demo Video](https://youtu.be/np0uua3mhU0)

---  
### Welcome to Pycross

#### Created by Daniel Sasse
This project was built as my Code in Place 2021 final project using Python and the Pygame module.

### Running the Game
* To run the game, clone this repo and install the pygame module. If you do not have Pygame installed, follow these [directions for installing Pygame](https://www.pygame.org/wiki/GettingStarted).
* Once the repo is cloned, and pygame is installed, run `main.py`
* The game will continue until either the window is closed, or the win conditions are met.

### Game Rules
* The Pycross game is a puzzle game in which the players uses the hints to the left and top of the board to determine which tiles in the board should be selected.
* Each row/column hint consists of a sequence of numbers representing the pattern of consequetive tiles that should be selected
* Example:
  * In the example below, the first rows's clue is a '5'. This indicates that there should be 5 consecutive tiles selected in that column.
  * In the first column, the hints "2,2" are given. This indicates that there should be a sequence of 2 tiles in a row touch each other, and then AT LEAST one unselected tile before the next sequence of "2" selected tiles.
  * Use the clues to select all of the tiles which should be selected. When you believe you have it correct, press the green "Check" button to confirm.

__Example "Starting" Board:__
![Pycross Example](https://raw.githubusercontent.com/dsasse07/pycross/main/nonogram.png)

__Example "Completed" Game:__
![Pycross Finished Example](https://raw.githubusercontent.com/dsasse07/pycross/main/nonogram-won.png)

### Difficulty
The difficulty of the game can be increased by increasing the number of tiles in the board, or by reducing the probably that a tile should be selected.

By default, the game will create a 6x6 grid, with a 0.7 (70%) probability that a tile will be selected. If you wish to change these values, adjust `SIZE` and `PROBABILITY` in `main.py`

* `SIZE` should have the format of `(rows_wide, cols_tall)`
* `PROBABILITY` should be a `float` representing the percent chance.
  * Ex: 70% == 0.7
