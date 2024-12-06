from enum import Enum
from typing import NamedTuple

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def turn_right(self):
        new_value: int = (self.value + 1) % 4
        return Direction(new_value)


moves: dict[int, tuple[int, int]] = {
    Direction.UP:    (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN:  (1, 0),
    Direction.LEFT:  (0, -1)}

def movement(d: Direction) -> tuple[int, int]:
    return moves[d]


class Point(NamedTuple):
    y: int
    x: int

    def move(self, dir: Direction):
        dy, dx = movement(dir)
        return Point(self.y + dy, self.x + dx)

class Guard:
    def __init__(self, pos: Point, dir: Direction):
        self.position = pos
        self.direction = dir

    def move(self):
        self.position = self.position.move(self.direction)

    def turn(self):
        self.direction = self.direction.turn_right()

direction_indicators: dict[str, Direction] = {
    '^': Direction.UP,
    '>': Direction.RIGHT,
    'V': Direction.DOWN,
    '<': Direction.LEFT
}

def find_guard(line: str, y: int) -> Guard:
    for i, dir in direction_indicators.items():
        if i in line:
            return Guard(Point(y, line.index(i)), dir)
    return None

def read_data(filename: str) -> tuple[list[list[bool]], Guard]:
    maze: list[list[bool]] = []
    guard: Guard = None
    with open(filename) as map_file:
        for y, line in enumerate(map_file.readlines()):
            maze_line: list[bool] = [(item == "#") for item in line.strip()]
            maze.append(maze_line)
            if guard is None:
                guard = find_guard(line, y)
    for l in maze:
        out = ["#" if p else "-" for p in l]
        print(f"{out}")
    return (maze, guard)


def main():
    maze, guard = read_data('day6/data.map')
    for l in maze:
        out = ["#" if p else "-" for p in l]
        print(f"{out}")
    print(f"guard at {guard.position} facing {guard.direction}")

    def out_of_bounds(y: int, x: int):
        if y < 0 or x < 0:
            return True
        if y >= len(maze) or x >= len(maze[0]):
            return True
        return False
    
    visited: set[Point] = { guard.position }
    
    while True:
        y, x = guard.position.move(guard.direction)
        if out_of_bounds(y, x):
            break
        if (maze[y][x]):
            guard.turn()
            print(f"turned {guard.direction}")
        else:
            guard.move()
            visited.add(guard.position)
            print(f"moved to {guard.position} ({len(visited)} fields visited)")
    
    print(f"{len(visited)} fields visited")


if __name__ == "__main__":
    main()