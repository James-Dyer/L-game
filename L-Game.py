import copy
import sys
import random

initial_state = {
    'player1': {'position': (2, 0), 'orientation': 'W'},
    'player2': {'position': (1, 3), 'orientation': 'E'},
    'neutral': [(0, 0), (3, 3)],
    'turn': 1,  # 1 for Player 1's turn, 2 for Player 2's turn
    'bypass_player': None,
    'game_mode': 'PvP',
    'depth': 2,
}

orientations = {
    'N': {'E': [(0, 0), (-1, 0), (-2, 0), (0, -1)], 'W': [(0, 0), (1, 0), (2, 0), (0, -1)]},
    'E': {'N': [(0, 0), (0, 1), (0, 2), (1, 0)], 'S':[(0, 0), (0, -1), (0, -2), (1, 0)]},
    'S': {'E': [(0, 0), (-1, 0), (-2, 0), (0, 1)], 'W':[(0, 0), (1, 0), (2, 0), (0, 1)]},
    'W': {'N': [(0, 0), (0, 1), (0, 2), (-1, 0)], 'S':[(0, 0), (0, -1), (0, -2), (-1, 0)]}
}


# Build a 2D array game board based off the current game state and display it
def buildBoard(state):
    board = [['.' for i in range(4)] for i in range(4)]

    """ 
    Relative orientations for L-pieces with primary and secondary orientations
    Secondary orientations are determined by which half the piece is positioned on
    """

    # place player 1 onto the board
    if (state['bypass_player'] != 'player1'):

        p1_pos = state['player1']['position']
        p1_orient = state['player1']['orientation']
        p1_secondary_orient = getSecondaryOrientation(p1_pos, p1_orient)
        for rx, ry in orientations[p1_orient][p1_secondary_orient]:
            x, y = p1_pos[0] + rx, p1_pos[1] + ry
            if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
                board[y][x] = '1'
            else:
                print("x1:", x)
                print("y1:", y)
                print("pxo: ", p1_orient, " , ", p1_secondary_orient)
                raise Exception("Attempted to place P1 into invalid position")
    
    # place player 2 onto the board
    if (state['bypass_player'] != 'player2'):
        p2_pos = state['player2']['position']
        p2_orient = state['player2']['orientation']
        p2_secondary_orient = getSecondaryOrientation(p2_pos, p2_orient)
        for rx, ry in orientations[p2_orient][p2_secondary_orient]:
            x, y = p2_pos[0] + rx, p2_pos[1] + ry
            if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
                board[y][x] = '2'
            else:
                raise Exception("Attempted to place P2 into invalid position")

    # place neutral squares onto the board
    n_pos = state['neutral']
    for x, y in n_pos:
        if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
            board[y][x] = 'N'
        else:
            raise Exception("Attempted to place Neutral 1x1 into invald position")
    
    return board

def getSecondaryOrientation(position, orientation):
    """
    Determine the secondary orientation of a piece based on its position
    and primary orientation 
    """
    x, y = position

    if (orientation == 'E' or orientation == 'W'):
        if y == 0 or y == 1:
            secondary_orient = 'N' 
        else:
            secondary_orient = 'S'
    if (orientation == 'N' or orientation == 'S'):
        if x == 0 or x == 1:
            secondary_orient = 'W' 
        else:
            secondary_orient = 'E' 
        
    return secondary_orient


def getLegalActions(state):
    """
    Returns all of the possible valid moves the player can make in form:
    ((playerpos), 'Orient', (oldNeutralPos), (newNeutralPos))
    """

    # Get current player's data
    player = state['turn']
    player_key = 'player1' if player == 1 else 'player2'
    other_player_key = 'player2' if player == 1 else 'player1'
    player_pos = state[player_key]['position']
    player_orient = state[player_key]['orientation']
    neutral1_pos = state['neutral'][0]
    neutral2_pos = state['neutral'][1]
    player_secondary_orient = getSecondaryOrientation(player_pos, player_orient)

    # Remove the current player's piece from the board (as they are "picking it up")
    state['bypass_player'] = player_key

    board = buildBoard(state)
    legal_actions = set()
    orientations = ['N', 'E', 'S', 'W']

    # Generate all possible L-piece moves
    for x in range(4):
        for y in range(4):
            for orient in orientations:
                
                if (x == player_pos[0] and y == player_pos[1] and orient == player_orient):
                    # Edge case: Can't place piece in the same spot as it was originally at
                    continue

                if isValidLMove((x, y), orient, board):
                    # Make a state with the new move
                    copied_state = copy.deepcopy(state)
                    copied_state[player_key]['position'] = x, y
                    copied_state[player_key]['orientation'] = orient
                    copied_state['bypass_player'] = None

                    new_board = buildBoard(copied_state)
                    new_secondary_orient = getSecondaryOrientation((x,y), orient)

                    # Get all possible neutral piece moves for each neutral piece
                    neutral_moves_1 = getNeutralMoves(new_board, neutral1_pos)
                    neutral_moves_2 = getNeutralMoves(new_board, neutral2_pos)
                    for oldpos, newpos in neutral_moves_1:
                        # Special format for when a neutral piece is not moved
                        if oldpos == newpos:
                            legal_actions.add(((x, y), orient, None, None))
                        else:
                            legal_actions.add(((x, y), orient, oldpos, newpos))
                    for oldpos, newpos in neutral_moves_2:
                        if oldpos == newpos:
                            legal_actions.add(((x, y), orient, None, None))
                        else:
                            legal_actions.add(((x, y), orient, oldpos, newpos))
    state['bypass_player'] = None


    return legal_actions

def isValidLMove(position, orientation, board):
    """
    Check if moving the L-piece to the given position with orientation is valid.
    """
    secondary_orient = getSecondaryOrientation(position, orientation)

    for rx, ry in orientations[orientation][secondary_orient]:
        x, y = position[0] + rx, position[1] + ry
        
        if not (0 <= x < 4 and 0 <= y < 4):
            return False
            
        if board[y][x] != '.':  # Occupied by another piece
            return False
    
    return True

def getNeutralMoves(board, oldpos):
    moves = []

    for x in range(4):
        for y in range(4):
            if board[y][x] == '.' or (x == oldpos[0] and y == oldpos[1]):
                moves.append((oldpos, (x, y)))
    return moves

def playerTurn(state):
    """
    Game logic for manually playing the game.
    Called for each player's turn
    """

    # Get current player's data
    player = state['turn']
    player_key = 'player1' if player == 1 else 'player2'
    other_player_key = 'player2' if player == 1 else 'player1'
    player_pos = state[player_key]['position']
    player_orient = state[player_key]['orientation']
    neutral1_pos = state['neutral'][0]
    neutral2_pos = state['neutral'][1]
    player_secondary_orient = getSecondaryOrientation(player_pos, player_orient)
    legal_actions = getLegalActions(state)

    board = buildBoard(state)
    printBoard(board)

    if is_terminal(state):
        terminalState(player)
        return

    # Wait for player input
    while True:
        try: 
            playerInput = getPlayerInput(player, state, board)

            # Check if its a valid move
            if playerInput in legal_actions:
                
                # Update player position
                player_pos, player_orient, old_neutral_pos, neutral_pos = playerInput
                state[player_key]['position'] = player_pos
                state[player_key]['orientation'] = player_orient

                # Update neutral positions
                if neutral_pos != None:
                    if state['neutral'][0] == old_neutral_pos:
                        state['neutral'][0] = neutral_pos
                    else:
                        state['neutral'][1] = neutral_pos

                # Update player turn
                state['turn'] = state['turn']%2 + 1

                break
                
            else:
                print(f"{playerInput} not in legalMoves")
                raise ValueError("Not a legal move")

        except ValueError as e: 
            print(f"\nInvalid input: {e}. Please try again.\n")
            continue

     # Proceed to next turn
    if state['game_mode'] == 'PvP':
        playerTurn(state)
    elif state['game_mode'] == 'PvC':
        computerTurn(state)
    else:
        raise Exception("Something went wrong with the gamemode selection")
    return

def computerTurn(state):

    # Get current player's data
    player = state['turn']
    player_key = 'player1' if player == 1 else 'player2'
    other_player_key = 'player2' if player == 1 else 'player1'
    player_pos = state[player_key]['position']
    player_orient = state[player_key]['orientation']
    neutral1_pos = state['neutral'][0]
    neutral2_pos = state['neutral'][1]
    player_secondary_orient = getSecondaryOrientation(player_pos, player_orient)
    legal_actions = getLegalActions(state)

    board = buildBoard(state)

    print("Computer's turn...")
    printBoard(board)

    if is_terminal(state):
        terminalState(player)
        return

    _, best_action = minimax(state, state['depth'], float('-inf'), float('inf'), True)

    if best_action is None:
        terminalState(player)
        return

    # Update state with the best action
    if player == 2:
        list_legal_actions = list(legal_actions)
        best_action = list_legal_actions[random.randint(0, len(list_legal_actions) - 1)]
    state = apply_action(state, best_action)

    # Print the computer's move in the required format
    print("Computer's move:")
    print(format_move(best_action))

    # Proceed to next turn
    if state['game_mode'] == 'PvC':
        playerTurn(state)
    elif state['game_mode'] == 'CvC':
        computerTurn(state)
    else:
        raise Exception("Something went wrong with the gamemode selection")
    return

def evaluate_state(state):
    player = state['turn']
    opponent = 1 if player == 2 else 2

    # Get legal moves for both players
    state['turn'] = player
    player_moves = len(getLegalActions(state))

    state['turn'] = opponent
    opponent_moves = len(getLegalActions(state))

    state['turn'] = player  # Reset turn

    # Check for terminal state
    if opponent_moves == 0:
        return float('inf')  # Winning state
    if player_moves == 0:
        return float('-inf')  # Losing state

    # Heuristic: difference in legal moves
    return player_moves - opponent_moves

def minimax(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        return evaluate_state(state), None

    legal_actions = getLegalActions(state)
    if not legal_actions:
        return evaluate_state(state), None

    best_action = None

    if maximizing_player:
        max_eval = float('-inf')
        for action in legal_actions:
            new_state = apply_action(state, action)
            eval, _ = minimax(new_state, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_action = action
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval, best_action
    else:
        min_eval = float('inf')
        for action in legal_actions:
            new_state = apply_action(state, action)
            eval, _ = minimax(new_state, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_action = action
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval, best_action

def apply_action(state, action):
    new_state = copy.deepcopy(state)
    player = new_state['turn']
    player_key = 'player1' if player == 1 else 'player2'

    # Unpack action
    (x, y), orient, old_neutral_pos, new_neutral_pos = action

    # Update player's L-piece
    new_state[player_key]['position'] = (x, y)
    new_state[player_key]['orientation'] = orient

    # Update neutral pieces
    if new_neutral_pos is not None:
        if new_state['neutral'][0] == old_neutral_pos:
            new_state['neutral'][0] = new_neutral_pos
        else:
            new_state['neutral'][1] = new_neutral_pos

    # Switch turn
    new_state['turn'] = 1 if player == 2 else 2

    return new_state

def is_terminal(state):
    legal_actions = getLegalActions(state)
    return len(legal_actions) == 0

def format_move(action):
    (x, y), orient, old_neutral_pos, new_neutral_pos = action
    move_str = f"{x + 1} {y + 1} {orient}"
    if new_neutral_pos is not None:
        a, b = old_neutral_pos
        c, d = new_neutral_pos
        move_str += f" {a + 1} {b + 1} {c + 1} {d + 1}"
    return move_str


def endGame(losingPlayer):
    winningPlayer = losingPlayer%2 + 1
    print(f"Player {losingPlayer} has ran out of moves. \nPlayer {winningPlayer} wins.")
    return


def getPlayerInput(playerID, state, board):
    """
    Prompts for the player's input string and validates it against the expected format
    """

    while True:
        try:
            user_input = '0'
            while (user_input == '0'):
                user_input = input("Player " + str(playerID) + " to move...\n").strip() 

                # Debug command
                if (user_input == '0'):
                    printLegalActions(state, board)

            parts = user_input.split()
            
            # Validate length
            if not (len(parts) == 3 or len(parts) == 7):
                raise ValueError("Input must be 3 or 7 elements: 'x y orientation' or 'x y orientation a b c d'\n"
                                    "where a neutral piece is moved from (a, b) to (c, d)")

            # Validate player coords (x, y)
            try:
                x, y = (int(parts[0]) - 1, int(parts[1]) - 1)
            except ValueError:
                raise ValueError("Coordinates (x, y) must be integers between 1 and 4")
            
            if not (0 <= x < 4 and 0 <= y < 4):
                raise ValueError("Coordinates (x, y) must be between 1 and 4")

            # Validate orientation
            orient = parts[2].upper()
            if orient not in {'N', 'E', 'S', 'W'}:
                raise ValueError("Orientation must be one of 'N', 'S', 'E', 'W'")

            # Validate neutral coordinates
            if len(parts) == 7:
                try:
                    a, b, c, d = map(int, parts[3:7])
                    a, b, c, d = a - 1, b - 1, c - 1, d - 1  # Adjust for 0-based indexing
                except ValueError:
                    raise ValueError("Neutral piece coordinates (a, b, c, d) must all be integers")

                if not (0 <= a < 4 and 0 <= b < 4 and 0 <= c < 4 and 0 <= d < 4):
                    raise ValueError("Both coordinates (a, b) and (c, d) must be between 1 and 4")

        except ValueError as e:
            print(f"\nInvalid input: {e}. Please try again.\n")
            continue
        
        if (len(parts) == 3):
            return ((x, y), orient, None, None)
        else:
            return ((x, y), orient, (a, b), (c, d))
    
def terminalState(losingPlayer):
    winningPlayer = losingPlayer % 2 + 1

    print(f"Player {losingPlayer} has run out of moves. Player {winningPlayer} wins.\n")
    sys.exit()

def mainMenu():
    while True:
        try:
            # Display the menu and get user input
            choice = input(
                "Main menu:\n"
                "   1) Player vs Player\n"
                "   2) Player vs Computer\n"
                "   3) Computer vs Computer\n"
                "   4) Set initial game state\n"
                "   5) Set minimax depth\n\n"
                "Enter a number to make a selection: "
            ).strip()  
            
            # Validate and handle the input
            if choice == '1':
                print("Starting Player vs Player game...")
                initial_state['game_mode'] = 'PvP'
                playerTurn(initial_state)  # Start Player vs Player game

            elif choice == '2':
                print("Starting Player vs Computer game...")
                start_pvc()
                
            elif choice == '3':
                print("Starting Computer vs Computer game...")
                start_cvc()
            elif choice == '4':
                setInitialGameState() 
            elif choice == '5':
                chooseMinimaxDepth()
            else:
                raise ValueError("Invalid choice. Please enter a number between 1 and 5")

        except ValueError as e:
            print("\n--------------------")
            print(f"Error: {e}.\n")

def start_pvc():
    while True:
        try:
            # Determine who has starting turn
            starting_choice = input(
            "\nSelect who makes the first move:\n"
            "   1) Player\n"
            "   2) Computer\n"
            ).strip()

            if not (starting_choice == '1' or starting_choice == '2'):
                raise ValueError("Invalid input")

            initial_state['game_mode'] = 'PvC'

            if starting_choice == '1':
                playerTurn(copy.deepcopy(initial_state))
            elif starting_choice == '2':
                computerTurn(copy.deepcopy(initial_state))

        except ValueError as e:
            print("\n--------------------")
            print(f"Error: {e}. Please enter a number 1 or 2\n")
            continue

def start_cvc():
    initial_state['game_mode'] = 'CvC'
    computerTurn(copy.deepcopy(initial_state))



def setInitialGameState():
    global initial_state

    while(True):
        try:
            user_input = input("\nEnter new game state string: \n")
            parts = user_input.split()
            
            # Validate length
            if not (len(parts) == 10):
                raise ValueError("Input must be 10 elements")

            # Validate player1 coords (x, y)
            try:
                x1, y1 = (int(parts[0]) - 1, int(parts[1]) - 1)
            except ValueError:
                raise ValueError("Coordinates (x1, y1) must be integers between 1 and 4")
            
            if not (0 <= x1 < 4 and 0 <= y1 < 4):
                raise ValueError("Coordinates (x1, y1) must be between 1 and 4")

            # Validate p1 orientation
            orient1 = parts[2].upper()
            if orient1 not in {'N', 'E', 'S', 'W'}:
                raise ValueError("Orientations must be one of 'N', 'S', 'E', 'W'")

            #Validate neutral coords
            try:
                a, b, c, d = map(int, parts[3:7])
                a, b, c, d = a - 1, b - 1, c - 1, d - 1  # Adjust for 0-based indexing
            except ValueError:
                raise ValueError("Neutral piece coordinates (a, b, c, d) must all be integers")

            if not (0 <= a < 4 and 0 <= b < 4 and 0 <= c < 4 and 0 <= d < 4):
                raise ValueError("Both coordinates (a, b) and (c, d) must be between 1 and 4")
            
            # Validate player2 coords (x, y)
            try:
                x2, y2 = (int(parts[7]) - 1, int(parts[8]) - 1)
            except ValueError:
                raise ValueError("Coordinates (x2, y2) must be integers between 1 and 4")
            
            if not (0 <= x2 < 4 and 0 <= y2 < 4):
                raise ValueError("Coordinates (x1, y1) must be between 1 and 4")

            # Validate p2 orientation
            orient2 = parts[9].upper()
            if orient2 not in {'N', 'E', 'S', 'W'}:
                raise ValueError("Orientations must be one of 'N', 'S', 'E', 'W'")

        except ValueError as e:
            print(f"\nInvalid input: {e}. Please try again.\n")
            continue
        
        copied_state = copy.deepcopy(initial_state)

        # Update the initial state
        copied_state['player1']['position'] = (x1, y1)
        copied_state['player1']['orientation'] = (orient1)
        copied_state['player2']['position'] = (x2, y2)
        copied_state['player2']['orientation'] = (orient2)
        copied_state['neutral'] = [(a, b), (c, d)]

        try:
            buildBoard(copied_state)
        except Exception as e:
            print(f"Error: {e}. The initial state is invalid.")
            continue

        initial_state = copy.deepcopy(copied_state)
        print("\n--------------------")
        print("The initial state has been updated.\n")
        mainMenu()
        return
    

def printBoard(board):
    # ANSI escape codes for styling
    RED_BOLD = "\033[1;31m"
    BLUE_BOLD = "\033[1;34m"
    LIGHT_GRAY = "\033[1;30m"
    RESET = "\033[0m"

    print("\n    1 2 3 4")  # Column headers
    print("  +---------+")
    for i, row in enumerate(board):
        # Replace '1' with red background, '2' with blue background, and '.' with light gray
        colored_row = [
            f"{RED_BOLD}1{RESET}" if char == '1' else
            f"{BLUE_BOLD}2{RESET}" if char == '2' else
            f"{LIGHT_GRAY}.{RESET}" if char == '.' else char
            for char in row
        ]
        print(f"{i + 1} | " + " ".join(colored_row) + " |")  # Row headers with row content
    print("  +---------+")
    print('')

def printLegalActions(state, board):
    legal_actions = getLegalActions(state)
    list_of_actions = sorted(list(legal_actions), key=lambda x: (x[0], x[1]))
    print("Legal actions:")
    for action in list_of_actions:
        if (action[3] == None):
            (x, y), orient, _, _ = action
            print(f"{x + 1} {y + 1} {orient} {a + 1} {b + 1}")
        else:
            (x, y), orient, (a, b), (c, d) = action
            print(f"{x + 1} {y + 1} {orient} {a + 1} {b + 1} {c + 1} {d + 1}")
    printBoard(board)

def main():
    mainMenu()

if __name__ == "__main__":
    main()