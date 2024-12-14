
import re
from enum import Enum
import logging
from map_lib import Map
from map_lib import print_map
from map_lib import Point

logger = logging.getLogger(__name__)

class Setup(Enum):
    SAMPLE = ('sample.txt', (7, 11))
    FULL = ('data.txt', (103, 101))
    SINGLE = ('single.txt', (7, 11))

setup = Setup.FULL


line_re = 'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'
line_pattern = re.compile(line_re)

def parse_line(line: str) -> tuple[tuple[int], tuple[int]]:
    match = line_pattern.match(line)
    return (Point(int(match.group(2)), int(match.group(1))), (int(match.group(4)), int(match.group(3))))

def move_robot(seconds: int, robot: tuple[tuple[int, int], tuple[int, int]], region: tuple[int, int]) -> tuple[Point, tuple[int, int]]:
    position, velocity = robot
    new_position = Point(
        (position.y + (seconds * velocity[0])) % region[0],
        (position.x + (seconds * velocity[1])) % region[1]
    )
    return (new_position, velocity)

def in_region(point: Point, region: tuple[Point, Point]) -> bool:
    topleft = region[0]
    bottomright = region[1]
    in_region = point.x >= topleft.x and point.x < bottomright.x
    in_region &= point.y >= topleft.y and point.y < bottomright.y
    return in_region

def create_quadrants() -> dict[int, tuple[Point, tuple[int, int]]]:
    result = {}
    center_x = int(setup.value[1][1]/2)
    center_y = int(setup.value[1][0]/2)
    logger.debug(f'center: ({center_y}, {center_x})')
    for q in range(4):
        y1 = int(q / 2) * (center_y+1)
        x1 = int(q % 2) * (center_x+1)
        x2 = x1 + center_x
        y2 = y1 + center_y
        result[q] = (Point(y1, x1), Point(y2, x2))
    logger.debug('quadrants:')
    for i in range(4):
        logger.debug(f'{i}: {result[i]}')
    return result

def create_map(robots: list[tuple[Point, tuple[int, int]]]):
    to_display = Map(setup.value[1][0], setup.value[1][1])
    for robot in robots:
        to_display.mark(position=robot[0], mark='x')
    print_map(to_display)

def calculate_safety(robots: list[tuple[Point, tuple[int, int]]]):
    quadrants = create_quadrants()
    result_list: dict[int, int] = {}
    robot_list = []
    for robot in robots:
        moved = move_robot(100, robot, setup.value[1])
        robot_list.append(moved)
        logger.debug(f'moved robot {robot} to {moved}')
        for i, q in quadrants.items():
            if in_region(moved[0], q):
                result_list[i] = result_list.setdefault(i, 0) + 1
                logger.debug(f'{moved} counting in {q} (quadrant {i}) - count now {result_list[i]}')
                break
    create_map(robot_list)
    logger.debug(f'all numbers:')
    safety = 1
    for q in range(4):
        logger.debug(f'quadrant {q}: {result_list.get(q)}')
        safety *= result_list.setdefault(q, 1)
    print(f'result: {safety}')

def xmas_tree_candidate(robots: list[tuple[Point, tuple[int, int]]]) -> bool:
    points = [robot[0] for robot in robots]
    center_x = int(setup.value[1][1] / 2)
    candidate = Point(0, center_x) in points
    #candidate &= Point(setup.value[1][0]-1, 0) in points
    return candidate

def main():
    logging.basicConfig(level=logging.DEBUG)
    with open(f'data/day14/{setup.value[0]}') as input_file:
        robots = []
        for line in input_file.readlines():
            robot = parse_line(line)
            robots.append(robot)
            # logger.debug(f'p={robot[0]}, v={robot[1]}')
    calculate_safety(robots)
    i = 0
    while True:
        print(f'step {i}')
        if xmas_tree_candidate(robots):
            create_map(robots)
            input()
        robots = [move_robot(1, r, setup.value[1]) for r in robots]
        i += 1



if __name__ == '__main__':
    main()