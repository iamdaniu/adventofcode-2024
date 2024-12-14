
import re
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class Setup(Enum):
    SAMPLE = ('sample.txt', (11, 7))
    FULL = ('data.txt', (101, 103))

setup = Setup.FULL

line_re = 'p=(\d+),(\d+) v=(-?\d+),(-?\d+)'
line_pattern = re.compile(line_re)

def parse_line(line: str) -> tuple[tuple[int], tuple[int]]:
    match = line_pattern.match(line)
    return ((int(match.group(1)), int(match.group(2))), (int(match.group(3)), int(match.group(4))))

def move_robot(seconds: int, position: tuple[int, int], velocity: tuple[int, int], region: tuple[int, int]) -> tuple[int, int]:
    new_position = (
        (position[0] + (seconds * velocity[0])) % region[0],
        (position[1] + (seconds * velocity[1])) % region[1]
    )
    return new_position

def in_region(point: tuple[int, int], region: tuple[tuple[int, int], tuple[int, int]]) -> bool:
    topleft = region[0]
    bottomright = region[1]
    in_region = point[0] >= topleft[0] and point[0] < bottomright[0]
    in_region &= point[1] >= topleft[1] and point[1] < bottomright[1]
    return in_region

def create_quadrants() -> dict[int, tuple[tuple[int, int], tuple[int, int]]]:
    result = {}
    center_x = int(setup.value[1][0]/2)
    center_y = int(setup.value[1][1]/2)
    logger.debug(f'center: ({center_x},{center_y})')
    for x in range(4):
        x1 = int(x / 2) * (center_x+1)
        y1 = int(x % 2) * (center_y+1)
        x2 = x1 + center_x
        y2 = y1 + center_y
        result[x] = ((x1, y1), (x2, y2))
    return result

# regions = [((x[0]), (x[1])) for x in [
#     ((0, 0), (setup.value[1][0] / 2, setup.value[1][1] / 2)),
#     ((setup.value[1][0] / 2, 0), (setup.value[1][0], setup.value[1][1] / 2)),
#     ((0, setup.value[1][1] / 2), (setup.value[1][0] / 2, setup.value[1][1])),
#     ((setup.value[1][0] / 2, setup.value[1][1] / 2), setup.value[1][0], setup.value[1][1])
# ]
# ]

def main():
    with open(f'data/day14/{setup.value[0]}') as input_file:
        quadrants = create_quadrants()
        in_region((6,6), ((0,4), (5,7)))
        result_list: dict[int, int] = {}
        for line in input_file.readlines():
            robot = parse_line(line)
            # logger.debug(f'p={robot[0]}, v={robot[1]}')
            moved = move_robot(100, robot[0], robot[1], setup.value[1])
            for i, q in quadrants.items():
                if in_region(moved, q):
                    result_list[i] = result_list.setdefault(i, 0) + 1
                    logger.debug(f'{moved} counting in {q} (quadrant {i}) - count now {result_list[i]}')
                    break
        logger.debug(f'all numbers:')
        safety = 1
        for q in range(4):
            logger.debug(f'quadrant {q}: {result_list.get(q)}')
            safety *= result_list.setdefault(q, 1)
        print(f'result: {safety}')



if __name__ == '__main__':
    main()