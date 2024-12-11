import csv
import logging


logger = logging.getLogger(__name__)

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
    with open('data/day11/data.input', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
        for line in reader:
            logger.debug(f'{line}')
            stone_line = [int(item) for item in line]
            for i in range (25):
                stone_line = create_stone_line(stone_line)
                logger.debug(f'{stone_line}')
            print(len(stone_line))

if __name__ == '__main__':
    main()