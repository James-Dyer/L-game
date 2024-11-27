import copy

initialState = {
    'player1': {'position': (0, 1), 'orientation': 'N'},
    'player2': {'position': (0, 2), 'orientation': 'S'},
    'neutral': [(2, 0), (3, 1)],
    'turn': 1,  # 1 for Player 1's turn, 2 for Player 2's turn
    'bypassPlayer': 'None'
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
    if (state['bypassPlayer'] != 'player1'):

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
                raise Exception("Attempted to place P1 into invald position")
    
    # place player 2 onto the board
    if (state['bypassPlayer'] != 'player2'):
        p2_pos = state['player2']['position']
        p2_orient = state['player2']['orientation']
        p2_secondary_orient = getSecondaryOrientation(p2_pos, p2_orient)
        for rx, ry in orientations[p2_orient][p2_secondary_orient]:
            x, y = p2_pos[0] + rx, p2_pos[1] + ry
            if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
                board[y][x] = '2'
            else:
                raise Exception("Attempted to place P2 into invald position")

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
    state['bypassPlayer'] = player_key

    board = buildBoard(state)
    legal_actions = []
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
                    copied_state['bypassPlayer'] = 'None'

                    new_board = buildBoard(copied_state)
                    new_secondary_orient = getSecondaryOrientation((x,y), orient)
                    print("pos: ", copied_state[player_key], new_secondary_orient)
                    printBoard(new_board)

                    # Get all possible neutral piece moves for each neutral piece
                    neutral_moves_1 = getNeutralMoves(new_board, neutral1_pos)
                    neutral_moves_2 = getNeutralMoves(new_board, neutral2_pos)
                    for oldpos, newpos in neutral_moves_1:
                        legal_actions.append(((x, y), orient, oldpos, newpos))
                    for oldpos, newpos in neutral_moves_2:
                        legal_actions.append(((x, y), orient, oldpos, newpos))

    if (len(legal_actions) == 0):
        terminalState()
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

    board = buildBoard(state)
    printBoard(board)

    # Wait for player input
    playerInput = getPlayerInput(player)
    print(playerInput)

def getPlayerInput(playerID):
    """
    Prompts for the player's input string and validates it against the expected format
    """

    while True:
        try:
            user_input = input("Player " + str(playerID) + " to move...\n")

            parts = user_input.split()
            
            # Validate length
            if not (len(parts) == 3 or len(parts) == 7):
                raise ValueError("Input must be 3 or 7 elements: 'x y orientation' or 'x y orientation' a b c d\n"
                                    "where a neutral piece is moved from (a, b) to (c, d)")

            # Validate player coords (x, y)
            try:
                x, y = (int(parts[0]) - 1, int(parts[1]) - 1)
            except ValueError:
                raise ValueError("Coordinates (x, y) must be integers between 1 and 4.")
            
            if not (0 <= x < 4 and 0 <= y < 4):
                raise ValueError("Coordinates (x, y) must be between 1 and 4.")

            # Validate orientation
            orient = parts[2].upper()
            if orient not in {'N', 'E', 'S', 'W'}:
                raise ValueError("Orientation must be one of 'N', 'S', 'E', 'W'.")

            # Validate neutral coordinates
            if len(parts) == 7:
                try:
                    a, b, c, d = map(int, parts[3:7])
                    a, b, c, d = a - 1, b - 1, c - 1, d - 1  # Adjust for 0-based indexing
                except ValueError:
                    raise ValueError("Neutral piece coordinates (a, b, c, d) must all be integers.")

                if not (0 <= a < 4 and 0 <= b < 4 and 0 <= c < 4 and 0 <= d < 4):
                    raise ValueError("Both coordinates (a, b) and (c, d) must be between 1 and 4.")

        except ValueError as e:
            print(f"\nInvalid input: {e} Please try again.\n")
            continue
        
        if (len(parts) == 3):
            return ((x, y), orient, (None, None), (None, None))
        else:
            return ((x, y), orient, (a, b), (c, d))

def terminalState():
    raise Exception('Not implemented yet')
    
def printBoard(board):
    print("    1 2 3 4")  # Column headers
    print("  +---------+")
    for i, row in enumerate(board):
        print(f"{i + 1} | " + " ".join(row) + " |")  # Row headers with row content
    print("  +---------+")
    print('')

def main():
    playerTurn(initialState)

if __name__ == "__main__":
    main()