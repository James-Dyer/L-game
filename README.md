# The L Game

The L Game was invented by Edward de Bono in 1967\. It is a two player game played on a 4x4 board, with each player having one 3x2 shaped “L piece”, and there are two 1x1 neutral pieces.   
![][image1]  
*The L-Game initial board. ([https://en.wikipedia.org/wiki/L\_game](https://en.wikipedia.org/wiki/L_game))*

Each player takes turns moving their L piece, and then optionally moving a neutral piece. The game ends when one player cannot move their L piece to a new position on their turn.

This was an assigned lab project for UC Merced’s Fall 2024 CSE175 course, Intro to Artificial Intelligence. ([archive](http://web.archive.org/web/20241211222812/https://faculty.ucmerced.edu/mcarreira-perpinan/teaching/CSE175/L-game.html))

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

Refer to `report.docx` for further documentation.

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

[image1]: <data:image/png;base64,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>
