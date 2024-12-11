import csv

def transform_stone(old_stone: str) -> list[str]:
    if old_stone == '0':
        return ['1']
    if len(old_stone) % 2 == 0:
        center: int = int(len(old_stone)/2)
        left_part = old_stone[:center]
        right_part = int(old_stone[center:])
        return [ left_part, str(right_part) ]
    new_stone_number = int(old_stone) * 2024
    return [ str(new_stone_number) ]

def create_stone_line(stone_line:list):
    new_stone_line: list[str] = []
    for item in stone_line:
        new_stone_line.extend(transform_stone(item))
    return new_stone_line

with open('data/day11/data.input', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
 
    for line in reader:
        print(f'{line}')
        stone_line = line
        for i in range (25):
            stone_line = create_stone_line(stone_line)
            print(f'{stone_line}')
        print(len(stone_line))
