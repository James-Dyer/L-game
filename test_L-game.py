import pytest
from L_Game_copy import getSecondaryOrientation

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
        