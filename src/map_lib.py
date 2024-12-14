
import logging

from typing import NamedTuple


class Point(NamedTuple):
    y: int
    x: int

    def __str__(self):
        return f'{self.y}/{self.x}'
    
    def translate(self, vector: tuple[int, int]):
        return Point(self.y + vector[0], self.x + vector[1])

    def is_neighbor(self, other) -> bool:
        for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
            if self.translate(direction) == other:
                return True
        return False


class Map:
    def __init__(self):
        self.data = []

    def __init__(self, y: int, x: int):
        self.data = [ '.'*x for i in range(y) ]

    def add_line(self, line: str):
        stripped = line.strip()
        self.data.append(stripped)
    
    def value_at(self, position: Point) -> str:
        return self.data[position.y][position.x]
    
    def out_of_bounds(self, position: Point) -> bool:
        if position.y < 0 or position.x < 0:
            return True
        if position.y > len(self.data)-1:
            return True
        if position.x > len(self.data[0])-1:
            return True

    def mark(self, position: Point, mark: str):
        old_line = self.data[position.y]
        new_line = old_line[0:position.x]
        new_line = new_line + mark
        new_line = new_line + old_line[position.x+1:]
        #new_line = self.data[position.y][0:position.x] + mark + self.data[position.y][position.x+1:]
        self.data[position.y] = new_line

class MapOfInterest(Map):
    def __init__(self, empty_marker = '.'):
        super().__init__()
        self.empty_marker = empty_marker
        self.points_of_interest: dict[str, list[Point]] = {}

    def add_line(self, line: str):
        super().add_line(line)
        stripped = line.strip()
        for i in range(len(stripped)):
            if stripped[i] != self.empty_marker:
                interest = stripped[i]
                current_point: Point = Point(len(self.data)-1, i)
                if (self.points_of_interest.get(interest)):
                    self.points_of_interest.get(interest).append(current_point)
                else:
                    self.points_of_interest[interest] = [ current_point ]
        
    def interesting_points(self) -> list[str]:
        return self.points_of_interest.keys()
    
    def points_with_interest(self, interest: str) -> list[Point]:
        return self.points_of_interest.get(interest)
    
    def mark(self, position: Point, mark: str, overwrite: bool = False):
        if self.data[position.y][position.x] != self.empty_marker and not overwrite:
            return
        super().mark(position, mark)

def print_map(m: Map, logger: logging.Logger = None, level: int = logging.INFO):
    printer = print
    if logger:
        printer = lambda m: logger.log(level, m)
    for line in m.data:
        printer(f'{line}')
