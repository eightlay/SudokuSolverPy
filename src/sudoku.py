from __future__ import annotations
from copy import deepcopy

from src.settings import (
    _FIELD_SIDE, _BLOCK_SIDE,
    _NUMBER_STR_TEMPLATE_LEN
)
from src.point import Point
from src.square import Square


class Sudoku:
    def __init__(self, set_squares: dict[tuple[int, int], int]) -> None:
        self._field: dict[Point, Square]
        self._points: dict[tuple[int, int], Point]
        self._connections: dict[Point, set[Point]]
        
        self._construct_field(set_squares)
        
        self._solved = False
        
    def _construct_field(
        self, set_squares: dict[tuple[int, int], int]
    ) -> None:
        self._points = {}
        self._field = {}
        
        for x in range(_FIELD_SIDE):
            for y in range(_FIELD_SIDE):
                p = Point(x, y)
                self._points[x, y] = p
                self._field[p] = Square(set_squares.get((x, y)))
        
    def solve(self) -> Sudoku:
        f = deepcopy(self)
        f.solve_inplace()
        return f
    
    def solve_inplace(self) -> None:
        if self._solved:
            return
        
        self._construct_connections()
        self._initial_domain_cut()
        
        
        self._solved = True
        
    def _construct_connections(self) -> None:
        self._connections = {p: set([]) for p in self._field}
        
        def add_conn(p: Point, i: int, j: int) -> None:
            conn = self._points[i, j]
            self._connections[p].add(conn)
            self._connections[conn].add(p)
        
        for p in self._field:
            for k in range(p.y + 1, _FIELD_SIDE):
                add_conn(p, p.x, k)
                
            for k in range(p.x + 1, _FIELD_SIDE):
                add_conn(p, k, p.y)
                
            xoff = p.x // _BLOCK_SIDE * _BLOCK_SIDE
            yoff = p.y // _BLOCK_SIDE * _BLOCK_SIDE
            
            for ib in range(_BLOCK_SIDE):
                for jb in range(_BLOCK_SIDE):
                    i = ib + xoff
                    j = jb + yoff
                    
                    if i != p.x and j != p.y:
                        add_conn(p, i, j)
                        
    def _initial_domain_cut(self) -> None:
        for p in self._field:
            if self._field[p].assigned:
                self._collapse(p)
            
    def _collapse(self, p: Point) -> None:
        n = self._field[p].number
        to_collapse_next = []
        
        for conn in self._connections[p]:
            flag = not self._field[conn].assigned
            flag &= self._field[conn].reduce_domain(n)
            
            if flag:
                to_collapse_next.append(conn)
        
        self._remove_connection(p)
        
        for conn in to_collapse_next:
            self._collapse(conn)
        
    def _remove_connection(self, conn: Point) -> None:
        for p in self._connections:
            self._connections[p].discard(conn)

    def __str__(self) -> str:
        result = ""
        row_delim = "-" * int(
            _FIELD_SIDE * _NUMBER_STR_TEMPLATE_LEN 
            + _FIELD_SIDE / _BLOCK_SIDE + 1
        ) + '\n'
        
        for x in range(_FIELD_SIDE):
            if x % _BLOCK_SIDE == 0:
                result += row_delim
            
            for y in range(_FIELD_SIDE):
                if y % _BLOCK_SIDE == 0:
                    result += "|"

                result += str(self._field[x, y])
                
            result += "|\n"
        
        return result + row_delim
