
import re
from functools import cmp_to_key

order_pattern = re.compile("(\d+)\|(\d+)")

orderings = {}

def read_order(line: str):
    match = order_pattern.match(line)
    if match != None:
        left = int(match.group(1))
        right = int(match.group(2))
        after_list = orderings.get(left)
        if after_list:
            after_list.append(right)
        else:
            orderings[left] = [right]
        return True
    else:
        return False

def compare_by_ordering(p1: int, p2: int):
    if p2 in orderings.get(p1):
        return -1
    elif p1 in orderings.get(p2):
        return 1
    else:
        return 0

correct_value_sum = 0
incorrect_value_sum = 0

with open("day5/data.txt") as input_file:
    reading_order = True
    for line in input_file.readlines():
        if reading_order:
            reading_order = read_order(line)
        else:
            pages = [int(page) for page in re.split(",", line)]
            resorted = sorted(pages, key=cmp_to_key(compare_by_ordering))
            middle_value = resorted[int(len(resorted)/2)]
            if pages == resorted:
                correct_value_sum = correct_value_sum + middle_value
            else:
                incorrect_value_sum = incorrect_value_sum + middle_value

print(f"result correctly sorted: {correct_value_sum}")
print(f"result incorrectly sorted: {incorrect_value_sum}")