import re

mult_pattern = "mul\((\d+),(\d+)\)"
mult_exp = re.compile(mult_pattern)

disable_pattern = "don't\(\).*?(do\(\)|$)"


def calculate_line(line: str):
    matches = mult_exp.findall(line)
    multiplied = [int(t[0]) * int(t[1]) for t in matches]
    return sum(multiplied)


# read into single line - don'()s stay valid over line boundaries
with open('day3/data.mem', newline='') as input_file:
    line = input_file.read().replace('\n', '')

total = calculate_line(line)

disabled = re.sub(disable_pattern, "", line)
total_enabled = calculate_line(disabled)

print(f"result: {total}")
print(f"enabled only: {total_enabled}")