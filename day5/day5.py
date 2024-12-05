
import re
from functools import cmp_to_key

order_pattern = re.compile("(\d+)\|(\d+)")

class OrderingSorter:
    def __init__(self):
        self.orderings = {}

    def add_order(self, left: int, right: int):
        after_list = self.orderings.get(left)
        if after_list:
            after_list.append(right)
        else:
            self.orderings[left] = [right]

    def is_after(self, p1, p2):
        after_list = self.orderings.get(p1)
        return after_list and p2 in after_list

    def compare_by_ordering(self, p1: int, p2: int):
        if self.is_after(p1, p2):
            return -1
        elif self.is_after(p2, p1):
            return 1
        else:
            return 0


correct_value_sum = 0
incorrect_value_sum = 0

sorter = OrderingSorter()

with open("day5/sample.txt") as input_file:
    reading_order = True
    for line in input_file.readlines():
        if line == "\n":
            reading_order = False
            continue

        if reading_order:
            match = order_pattern.match(line)
            sorter.add_order(int(match.group(1)), int(match.group(2)))
        else:
            pages = [int(page) for page in re.split(",", line)]
            resorted = sorted(pages, key=cmp_to_key(sorter.compare_by_ordering))
            middle_value = resorted[int(len(resorted)/2)]
            if pages == resorted:
                correct_value_sum = correct_value_sum + middle_value
            else:
                incorrect_value_sum = incorrect_value_sum + middle_value

print(f"result correctly sorted: {correct_value_sum}")
print(f"result incorrectly sorted: {incorrect_value_sum}")