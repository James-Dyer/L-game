import pytest
from L_Game_copy import getSecondaryOrientation

@pytest.mark.parametrize(
    "orientation, position, expected, should_succeed",
    [
        # Test cases for orientation N
        ('N', (0, 1), 'W', True),
        ('N', (0, 2), 'W', True),
        ('N', (0, 3), 'W', True),
        ('N', (0, 4), 'W', True),

        ('N', (2, 3), 'E', True),
        ('N', (3, 2), 'E', True),
        ('N', (3, 1), 'E', True),

        ('N', (0, 3), 'W', True),
        ('N', (1, 3), 'W', True),
        ('N', (2, 3), 'E', True),
        ('N', (3, 3), 'E', True),

        ('N', (1, 1), 'E', False),
        ('N', (3, 0), 'W', False),
        ('N', (2, 1), 'W', False),
    ]
)

def test_get_secondary_orientation(orientation, position, expected, should_succeed):
    result = getSecondaryOrientation(position, orientation)
    if (should_succeed):
        assert result == expected
    else:
        assert result != expected
        