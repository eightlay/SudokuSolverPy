from src.point import Point

House = str

ROW: House = 'row'
COL: House = 'col'
BLOCK: House = 'block'


def create_trackers() -> dict[House, list]:
    return {
        'row': [],
        'col': [],
        'block': []
    }
