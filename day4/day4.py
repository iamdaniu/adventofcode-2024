
search_modes = [(-1, -1), (-1, 0), (-1, 1)]
search_modes = search_modes + [(0, -1), (0, 1)]
search_modes = search_modes + [(1, -1), (1, 0), (1, 1)]

search_term = "XMAS"

def find_in_direction(lines: list, cy: int, cx: int, index: int, search_mode: tuple):
    # out of bounds checks
    if cy < 0 or cx < 0:
        return 0
    if cy >= len(lines) or cx >= len(lines[cy]):
        return 0
    character = lines[cy][cx]
    toFind = search_term[index]
    # current position matches expected character - continue search
    if character == toFind:
        new_index = index + 1
        if new_index == len(search_term):
            return 1
        new_cy = cy + search_mode[0]
        new_cx = cx + search_mode[1]
        return find_in_direction(lines, new_cy, new_cx, new_index, search_mode)
    # current character mismatch
    return 0

def find_from(lines: list, y: int, x: int):
    result = 0
    for mode in search_modes:
        result = result + find_in_direction(lines, y, x, 0, mode)
    return result

with open('day4/data.txt', newline='') as input_file:
    lines = input_file.readlines()

xmas_count = 0
for y in range(0, len(lines)):
    line = lines[y]
    for x in range(0, len(line)):
        xmas_count = xmas_count + find_from(lines, y, x)

print(f"{xmas_count} matches found")