from __future__ import annotations
from copy import deepcopy
from typing import Iterable
from collections import Counter

from src.point import Point
from src.square import Square
from src.house import (
    ROW, COL, BLOCK,
    create_trackers
)
from src.settings import (
    _FIELD_SIDE, _BLOCK_SIDE,
    _NUMBER_STR_TEMPLATE_LEN,
    _NUMBER_RANGE
)


class Sudoku:
    def __init__(self, set_squares: dict[tuple[int, int], int] = {}) -> None:
        """Create sudoku with the given set squares

        Args:
            set_squares (dict[tuple[int, int], int], optional): set squares.
            Key is point where to place number, value is number. 
            Defaults to {}.
        """
        self._field: dict[Point, Square]
        self._points: dict[tuple[int, int], Point]
        self._connections: dict[Point, set[Point]]
        
        self._construct_field(set_squares)
        
        self._to_solve = _FIELD_SIDE ** 2
        self._solved = False
        
    def _construct_field(
        self, set_squares: dict[tuple[int, int], int]
    ) -> None:
        """Construct field and points dictionary

        Args:
            set_squares (dict[tuple[int, int], int]): set squares.
            Key is point where to place number, value is number.
        """
        self._points = {}
        self._field = {}
        
        for x in range(_FIELD_SIDE):
            for y in range(_FIELD_SIDE):
                p = Point(x, y)
                self._points[x, y] = p
                self._field[p] = Square(set_squares.get((x, y)))
        
    def solve(self) -> Sudoku:
        """Solve sudoku

        Returns:
            Sudoku: solved sudoku
        """
        f = deepcopy(self)
        f.solve_inplace()
        return f
    
    def solve_inplace(self) -> None:
        """Solve sudoku without creating new object
        """
        if self._solved:
            return
        
        self._construct_connections()
        self._initial_domain_cut()
        
        limit = 0
        
        while self._to_solve and limit < 10:
            limit += 1
            self._hidden_single()
            # print(self)
            self._pairs()
            # print(self)
        
        self._solved = True
        
    def _construct_connections(self) -> None:
        """Construct squares connections
        """
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
        """Cut domains from the initially got set squares
        """
        for p in self._field:
            if self._field[p].assigned:
                self._to_solve -= 1
                self._collapse(p)
            
    def _collapse(self, p: Point, exclude: Iterable[Point] = ()) -> None:
        """Collapse square connections graph

        Args:
            p (Point): point to collapse around
            exclude (Iterable[Point], optional): points to exclude from collapse.
            Defaults to ().
        """
        n = self._field[p].number
        to_collapse_next = []
        
        for conn in self._connections[p]:
            if conn in exclude:
                continue
            
            if self._field[conn].reduce_domain(n):
                self._to_solve -= 1
                to_collapse_next.append(conn)
        
        self._remove_connection(p)
        
        for conn in to_collapse_next:
            self._collapse(conn)
        
    def _remove_connection(self, conn: Point) -> None:
        """Remove point from all connections

        Args:
            conn (Point): point to remove
        """
        for p in self._connections:
            self._connections[p].discard(conn)
    
    def _hidden_single(self) -> None:
        """Hidden single sudoku technique
        """
        rng = range(_FIELD_SIDE)
        
        for n in _NUMBER_RANGE:
            for k in rng:
                stats = create_trackers()
                
                xstart = k // _BLOCK_SIDE * _BLOCK_SIDE
                ystart = k % _BLOCK_SIDE * _BLOCK_SIDE
                
                for l in rng:
                    if self._field[k, l].in_domain(n):
                        stats[ROW].append((k, l))
                        
                    if self._field[l, k].in_domain(n):
                        stats[COL].append((l, k))
                        
                    x = xstart + l // _BLOCK_SIDE
                    y = ystart + l % _BLOCK_SIDE
                        
                    if self._field[x, y].in_domain(n):
                        stats[BLOCK].append((x, y))
                        
                for stat in stats.values():
                    if len(stat) == 1:
                        p = stat[0]
                        self._field[p].set_number(n)
                        self._collapse(p)

    def _pairs(self) -> None:
        """Hidden pair and pointing pair sudoku technique
        """
        rng = range(_FIELD_SIDE)

        for k in rng:
            trackers = create_trackers()
            stats = create_trackers()
            
            xstart = k // _BLOCK_SIDE * _BLOCK_SIDE
            ystart = k % _BLOCK_SIDE * _BLOCK_SIDE

            for l in rng:
                x = xstart + l // _BLOCK_SIDE
                y = ystart + l % _BLOCK_SIDE

                trackers[ROW].append((k, l))
                trackers[COL].append((l, k))
                trackers[BLOCK].append((x, y))
                stats[ROW].append(tuple(sorted(self._field[k, l].domain)))
                stats[COL].append(tuple(sorted(self._field[l, k].domain)))
                stats[BLOCK].append(tuple(sorted(self._field[x, y].domain)))

            for house, doms in stats.items():
                # Hidden pair
                counter = Counter(doms)
                del counter[()]

                for dom, count in counter.items():
                    if not (count == len(dom) == 2):
                        continue
                    
                    for i, p in enumerate(trackers[house]):
                        if doms[i] == dom:
                            continue

                        for n in dom:
                            if self._field[p].reduce_domain(n):
                                self._to_solve -= 1
                                self._remove_connection(p)
                                    
                # Pointing pair
                # TODO  

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
