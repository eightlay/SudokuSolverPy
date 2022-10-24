from src.settings import _NUMBER_RANGE, _NUMBER_STR_TEMPLATE


class Square:
    def __init__(self, set_number: int | None = None) -> None:
        if set_number is not None and set_number not in _NUMBER_RANGE:
            raise ValueError(f"can't assign Square to number {set_number}")
        
        self._number = set_number
        self._domain = set([] if set_number else _NUMBER_RANGE)
        
    @property
    def number(self) -> int | None:
        return self._number
        
    @property
    def assigned(self) -> bool:
        return self.number is not None
    
    @property
    def domain(self) -> set[int]:
        return self._domain.copy()
    
    def set_number(self, n: int) -> bool:
        if n in self._domain:
            self._domain.clear()
            self._number = n
            return True
        return False
        
    def reduce_domain(self, n: int) -> bool:
        if self.assigned:
            return False
        
        self._domain.discard(n)
        
        if len(self._domain) == 1:
            self._number = self._domain.pop()

        return self.assigned
    
    def in_domain(self, n: int) -> bool:
        return n in self._domain
        
    def __str__(self) -> str:
        return (
            _NUMBER_STR_TEMPLATE.format(self.number)
            if self.assigned
            else "   "
        )
