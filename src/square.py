from src.settings import _NUMBER_RANGE, _NUMBER_STR_TEMPLATE


class Square:
    def __init__(self, set_number: int | None = None) -> None:
        if set_number is not None and set_number not in _NUMBER_RANGE:
            raise ValueError(f"can't assign Square to number {set_number}")
        
        self.assigned = set_number
        self.domain = set([] if set_number else _NUMBER_RANGE)
        
    def __str__(self) -> str:
        return (
            "   " 
            if self.assigned is None 
            else _NUMBER_STR_TEMPLATE.format(self.assigned)
        )
