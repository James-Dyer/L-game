initialState = {
    'player1': {'position': (2, 0), 'orientation': 'W'},
    'player2': {'position': (1, 3), 'orientation': 'E'},
    'neutral': [(0, 0), (3, 3)],
    'turn': 1  # 1 for Player 1's turn, 2 for Player 2's turn
}

# Build a 2D array game board based off the current game state and display it
def buildBoard(state):
    board = [['.' for i in range(4)] for i in range(4)]

    # Relative orientations for L-pieces with primary and secondary orientations
    # Secondary orientations are determined by which half the piece is positioned on
    orientations = {
        'N': {'E': [(0, 0), (1, 0), (2, 0), (0, 1)], 'W': [(0, 0), (-1, 0), (-2, 0), (0, 1)]},
        'E': {'N': [(0, 0), (0, 1), (0, 2), (1, 0)], 'S':[(0, 0), (0, -1), (0, -2), (1, 0)]},
        'S': {'E': [(0, 0), (1, 0), (2, 0), (0, -1)], 'W':[(0, 0), (-1, 0), (-2, 0), (0, -1)]},
        'W': {'N': [(0, 0), (0, 1), (0, 2), (-1, 0)], 'S':[(0, 0), (0, -1), (0, -2), (-1, 0)]}
    }
    
    # place player 1 onto the board
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
            #raise Exception("Attempted to place P1 into invald position")

    # place player 2 onto the board
    p2_pos = state['player2']['position']
    p2_orient = state['player2']['orientation']
    p2_secondary_orient = getSecondaryOrientation(p2_pos, p2_orient)
    for rx, ry in orientations[p2_orient][p2_secondary_orient]:
        x, y = p2_pos[0] + rx, p2_pos[1] + ry
        if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
            board[y][x] = '2'
        else:
            print("x2:", x)
            print("y2:", y)
            #raise Exception("Attempted to place P2 into invald position")

    # place neutral squares onto the board
    n_pos = state['neutral']
    for x, y in n_pos:
        if 0 <= x < 4 and 0 <= y < 4 and board[y][x] == '.':
            board[y][x] = 'N'
        else:
            print("xN:", x)
            print("yN:", y)
            #raise Exception("Attempted to place Neutral 1x1 into invald position")
    
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


def printBoard(board):
    """
    Print the board in a readable format.
    """
    print("  0 1 2 3")  # Column headers
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(row))  # Row headers with row content

def main():
    board = buildBoard(initialState)
    printBoard(board)

if __name__ == "__main__":
    main()