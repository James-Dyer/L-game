import pytest
from L_Game_copy import getSecondaryOrientation
from L_Game_copy import evaluate_state

@pytest.mark.parametrize(
    "state, expected",
    [
        (
            { # Terminal state, player 2 win
            'player1': {'position': (0, 3), 'orientation': 'N'},
            'player2': {'position': (2, 1), 'orientation': 'S'},
            'neutral': [(2, 0), (3, 3)],
            'turn': 1,  
            'bypass_player': None,
            }, 
        float('-inf')),
        (
            { # Terminal state, player 1 win
            'player1': {'position': (2, 2), 'orientation': 'S'},
            'player2': {'position': (0, 1), 'orientation': 'N'},
            'neutral': [(2, 0), (3, 1)],
            'turn': 2,  
            'bypass_player': None,
            }, 
        float('inf')),
        (
            { # Initial state, player 1's turn
            'player1': {'position': (2, 0), 'orientation': 'W'},
            'player2': {'position': (1, 3), 'orientation': 'E'},
            'neutral': [(0, 0), (3, 3)],
            'turn': 1,  
            'bypass_player': None,
            }, 
        0),
        (
            { # Initial state, player 2's turn
            'player1': {'position': (2, 0), 'orientation': 'W'},
            'player2': {'position': (1, 3), 'orientation': 'E'},
            'neutral': [(0, 0), (3, 3)],
            'turn': 2,  
            'bypass_player': None,
            }, 
        0),
    ]
    
    
)
def test_evaluate_state(state, expected):
    result = evaluate_state(state)
    assert result == expected

@pytest.mark.parametrize(
    "orientation, position, expected, should_succeed",
    [
        # Test cases for orientation N and S
        ('N', (0, 1), 'W', True),
        ('N', (0, 4), 'W', True),
        ('N', (2, 3), 'E', True),
        ('N', (3, 3), 'E', True),
        ('S', (0, 1), 'W', True),
        ('S', (0, 4), 'W', True),
        ('S', (2, 3), 'E', True),
        ('S', (3, 3), 'E', True),

        ('S', (1, 1), 'E', False),
        ('S', (3, 0), 'W', False),
        ('S', (2, 1), 'W', False),
        ('N', (1, 1), 'E', False),
        ('N', (3, 0), 'W', False),
        ('N', (2, 1), 'W', False),

        # Test cases for orientation E and W
        ('E', (0, 0), 'N', True),
        ('E', (0, 1), 'N', True),
        ('E', (2, 2), 'S', True),
        ('E', (3, 3), 'S', True),
        ('W', (0, 1), 'N', True),
        ('W', (0, 4), 'S', True),
        ('W', (2, 3), 'S', True),
        ('W', (3, 3), 'S', True),   
        
        ('E', (1, 1), 'S', False),
        ('E', (3, 0), 'S', False),
        ('E', (2, 1), 'S', False),
        ('W', (1, 2), 'N', False),
        ('W', (3, 3), 'N', False),
        ('W', (2, 3), 'N', False),
    ]
)
def test_get_secondary_orientation(orientation, position, expected, should_succeed):
    result = getSecondaryOrientation(position, orientation)
    if (should_succeed):
        assert result == expected
    else:
        assert result != expected


        