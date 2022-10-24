from src.point import Point

House = str
"""Sudoku house (row, col, block)"""

ROW: House = 'row'
"""Row house"""
COL: House = 'col'
"""Column house"""
BLOCK: House = 'block'
"""Block house"""


def create_trackers() -> dict[House, list]:
    """Create trackers for houses

    Returns:
        dict[House, list]: houses trackers
    """
    return {
        'row': [],
        'col': [],
        'block': []
    }
