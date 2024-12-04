
search_modes = [(-1, -1), (-1, 0), (-1, 1)]
search_modes = search_modes + [(0, -1), (0, 1)]
search_modes = search_modes + [(1, -1), (1, 0), (1, 1)]

search_term = "XMAS"

def is_out_of_bounds(lines: list, point: tuple):
    y = point[0]
    x = point[1]
    # out of bounds checks
    if y < 0 or x < 0:
        return True
    if y >= len(lines) or x >= len(lines[y]):
        return True
    return False

def apply_search_mode(point: tuple, search_mode: tuple):
    return(point[0] + search_mode[0], point[1] + search_mode[1])

def neighboring_search_modes(search_mode: tuple):
    return ()

def has_neighboring_m(lines: list, center_y: int, center_x: int, search_mode: tuple):
    return False

def character_matches(lines: list, check_for: str, point: tuple):
    if is_out_of_bounds(lines, point):
        return False
    character = lines[point[0]][point[1]]
    return character == check_for

def find_in_direction(lines: list, point: tuple, index: int, search_mode: tuple):
    if character_matches(lines, search_term[index], point):
    # current position matches expected character - continue search
        new_index = index + 1
        if new_index == len(search_term):
            return 1
        new_candidate = apply_search_mode(point, search_mode)
        return find_in_direction(lines, new_candidate, new_index, search_mode)
    # current character mismatch
    return 0

def find_from(lines: list, point: tuple):
    result = 0
    for mode in search_modes:
        result = result + find_in_direction(lines, point, 0, mode)
    return result

with open('day4/data.txt', newline='') as input_file:
    lines = input_file.readlines()

xmas_count = 0
for y in range(0, len(lines)):
    line = lines[y]
    for x in range(0, len(line)):
        xmas_count = xmas_count + find_from(lines, (y, x))

print(f"{xmas_count} matches found")