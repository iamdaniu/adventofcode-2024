
import re
from typing import Callable

line_re = r"(\d+):(.*)"
line_pattern = re.compile(line_re)
number_re = r" (\d+)"
number_pattern = re.compile(number_re)

class Operator:
    def __init__(self, name: str, operation: Callable[[int, int], int]):
        self.name = name
        self.operation = operation

    def apply(self, left: int, right) -> int:
        return self.operation(left, right)
    
    def __repr__(self):
        return self.name

PLUS = Operator("plus", lambda x, y: x + y)
MULT = Operator("times", lambda x, y: x * y)
CONC = Operator("concat", lambda x, y : int(f"{x}{y}"))


class Term:
    def __init__(self, value: int, operator: Operator):
        self.value = value
        self.operator = operator

    def apply(self, other: int) -> int:
        return self.operator.apply(self.value, other)
    
    def __repr__(self):
        return f"{self.operator} {self.value}"


def candidate_terms(right: int) -> list[Term]:
    return [Term(right, PLUS), Term(right, MULT), Term(right, CONC)]

def find_operators(solution: int, stack: list[tuple[int, Term]], values: list[int], current_result: int) -> list[tuple[int, Term]]:
    if len(values) != 0:
        for new_term in candidate_terms(current_result):
            new_current_result = new_term.apply(values[0])
            stack.append(new_term)
            result = find_operators(solution, stack, values[1:], new_current_result)
            if result:
                return result
            else:
                stack.pop()
    else:
        if current_result == solution:
            return stack
        else:
            return None

    

def possible_solution(solution: int, values: list[int]):
    current_result = values[0]
    operators = [(None, current_result)]

def main():
    total_possible = 0
    with open("day7/data.txt") as input_file:
        for line in input_file.readlines():
            m = line_pattern.match(line.strip())
            solution = int(m.group(1))
            values = [int(num) for num in number_pattern.findall(m.group(2))]
            #print(f"line: {line.strip()}, solution: {solution}, terms: {values}")
            ops = find_operators(solution, [], values[1:], values[0])
            #print(f"solution possible? {ops}")
            if ops:
                total_possible = total_possible + solution
    print(f"total: {total_possible}")



if __name__ == "__main__":
    main()