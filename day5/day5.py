
import re
from functools import cmp_to_key

order_pattern = re.compile("(\d+)\|(\d+)")


def read_order(line: str):
    match = order_pattern.match(line)
    if match != None:
        return (int(match.group(1)), int(match.group(2)))
    else:
        return None

orderings = {}

def required_after(p1: int, p2: int):
    order_after = orderings.get(p1)
    if order_after:
        if p2 in order_after:
            return True
    return False


def compare_by_ordering(p1: int, p2: int):
    if required_after(p1, p2):
        return -1
    elif required_after(p2, p1):
        return 1
    else:
        return 0


center_value_sum = 0

with open("day5/data.txt") as input_file:
    reading_order = True
    for line in input_file.readlines():
        if (reading_order):
            new_order = read_order(line)
            if new_order:
                after_list = orderings.get(new_order[0])
                if after_list:
                    after_list.append(new_order[1])
                else:
                    orderings[new_order[0]] = [new_order[1]]
            else:
                reading_order = False
        else:
            pages = [int(page) for page in re.split(",", line)]
            resorted = sorted(pages, key=cmp_to_key(compare_by_ordering))
            if pages == resorted:
                middle_value = pages[int(len(pages)/2)]
                print(f"correctly sorted: {pages}, center: {middle_value}")
                center_value_sum = center_value_sum + middle_value

print(f"result: {center_value_sum}")