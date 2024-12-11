import csv
import logging
from functools import cache


logger = logging.getLogger(__name__)

@cache
def stone_count_after_steps(stone: int, steps: int) -> int:
    if steps == 0:
        return 1
    if stone == 0:
        return stone_count_after_steps(1, steps-1)
    insc_str = str(stone)
    if len(insc_str) % 2 == 0:
        center: int = int(len(insc_str)/2)
        left_part = int(insc_str[:center])
        right_part = int(insc_str[center:])
        return stone_count_after_steps(left_part, steps-1) + stone_count_after_steps(right_part, steps-1)
    return stone_count_after_steps(stone*2024, steps-1)

@cache
def transform_stone(old_stone: int) -> list[int]:
    if old_stone == 0:
        return [ 1 ]
    insc_str = str(old_stone)
    if len(insc_str) % 2 == 0:
        center: int = int(len(insc_str)/2)
        left_part = int(insc_str[:center])
        right_part = int(insc_str[center:])
        return [ left_part, right_part ]
    new_stone_number = old_stone * 2024
    return [ new_stone_number ]

def create_stone_line(stone_line:list):
    new_stone_line: list[int] = []
    for item in stone_line:
        new_stone_line.extend(transform_stone(item))
    return new_stone_line

def main():
    logging.basicConfig(level=logging.INFO)
    with open('data/day11/data.input', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
        for line in reader:
            logger.debug(f'{line}')
            print(f'{sum([stone_count_after_steps(int(stone), 75) for stone in line])}')

if __name__ == '__main__':
    main()