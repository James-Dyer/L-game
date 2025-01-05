# The L Game

The L Game was invented by Edward de Bono in 1967\. It is a two player game played on a 4x4 board, with each player having one 3x2 shaped “L piece”, and there are two 1x1 neutral pieces.   
![L-Game board visualized](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/L_Game_start_position.svg/330px-L_Game_start_position.svg.png)

*The L-Game initial board. ([https://en.wikipedia.org/wiki/L\_game](https://en.wikipedia.org/wiki/L_game))*

Each player takes turns moving their L piece, and then optionally moving a neutral piece. The game ends when one player cannot move their L piece to a new position on their turn.

This was an assigned lab project for UC Merced’s Fall 2024 CSE175 course, Intro to Artificial Intelligence. ([Archived link](http://web.archive.org/web/20241211222812/https://faculty.ucmerced.edu/mcarreira-perpinan/teaching/CSE175/L-game.html))

## Features:

* Multiple Gameplay Options:  
  * Play against the computer, another human, or watch computer vs. computer.  
  * Play can further be customized (See [Commands and Flags](https://github.com/James-Dyer/L-game/blob/main/README.md#commands-and-flags))  
* Inter-project compatible API:  
  * The formatting of game’s input/output is standardized, so compatible projects can play games against each other. (More on project page linked above)  
* CPU Strategies:  
  * Implemented Minimax and Alpha-Beta Pruning up to a user defined depth.  
  * Developed a heuristic evaluation function for efficient decisions.  
  * Optimized for performance using appropriate data structures and algorithms, as well as caching strategies.

Refer to `report.pdf` for further documentation.

## Installation and Usage

* Requires Python 3.x or higher  
* To play the game, run `python3 L-Game.py`

## How to play

The playing board is represented by a 4x4 grid printed to the terminal. The top left corner is (1,1) while the bottom right corner is (4,4). X goes horizontally and Y vertically.

Moves entered through the terminal and are formatted as followed: 1 2 E 4 3 1 1 where (1, 2\) is the position of the corner of the L piece, E is the direction of the short end of the L piece (out of N, S, E, W), and a neutral piece is moved from (4, 3\) to (1, 1). If a neutral piece is not being moved, the last 2 pairs of numbers can be omitted.

#### Commands and flags

There is some extra functionality to my program, both for debugging and for a better user experience. When launching the game from the command line, you can use the following flags:

* **\--randomCPU:** Makes the player 2 CPU choose moves at random, letting you test your AI against a strategically weak opponent.  
* **\--debug:** Enables various statistics about the game such as nodes evaluated, execution time (per turn), execution time (in total), etc. It also enables printing the traceback of exceptions.  
* **\--stepbystep:** When playing computer vs computer, enabling this flag will pause the game between each computer’s turn, letting the user examine the board and any relevant information, then proceed when they are ready.


In addition, you can use the following commands at the command line while playing a game:

* **help():** Provides the player with a possible legal move.  
* **save():** Prints a string that represents the current game state. This string can later be used to reinitialize the board in the exact same configuration as an initial state.  
* **quit():** Allows the user to gracefully exit the program while playing.  
* **0:** Typing ‘0’ will return a list of all the possible moves the current player can make.

## License

This project is licensed under the Apache-2.0 License. See `LICENSE` for details.
