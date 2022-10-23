from __future__ import annotations
from copy import deepcopy

from src.settings import (
    _FIELD_W, _FIELD_H, 
    _BLOCK_W, _BLOCK_H,
    _NUMBER_STR_TEMPLATE_LEN
)
from src.point import Point
from src.square import Square


class Sudoku:
    def __init__(self, set_squares: dict[tuple[int, int], int]) -> None:
        self.field = {
            Point(x, y): Square(set_squares.get((x, y)))
            for x in range(_FIELD_H) for y in range(_FIELD_W) 
        }
        self.solved = False
        
    def solve(self) -> Sudoku:
        f = deepcopy(self)
        f.solve_inplace()
        return f
    
    def solve_inplace(self) -> None:
        # TODO
        self.solved = True

    def __str__(self) -> str:
        result = ""
        row_delim = "-" * int(
            _FIELD_W * _NUMBER_STR_TEMPLATE_LEN + _FIELD_W / _BLOCK_W + 1
        ) + '\n'
        
        for x in range(_FIELD_H):
            if x % _BLOCK_H == 0:
                result += row_delim
            
            for y in range(_FIELD_W):
                if y % _BLOCK_W == 0:
                    result += "|"

                result += str(self.field[x, y])
                
            result += "|\n"
        
        return result + row_delim
