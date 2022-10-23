House = str

ROW: House = 'row'
COL: House = 'col'
BLOCK: House = 'block'


class HouseStat:
    def __init__(self) -> None:
        self.count = 0
        self.point = None


def create_stats() -> dict[House, HouseStat]:
    return {
        'row': HouseStat(),
        'col': HouseStat(),
        'block': HouseStat()
    }