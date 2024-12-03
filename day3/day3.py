import re

mult_pattern = "mul\((\d+),(\d+)\)"
disable_pattern = "don't\(\).*?do\(\)"

mult_exp = re.compile(mult_pattern)
disable_exp = re.compile(disable_pattern)

with open('day3/sample.mem', newline='') as input_file:
    lines = input_file.readlines()

total = 0
for line in lines:
#    print(f"line: {line}")
    #disabled = re.sub(disable_pattern, "", line)
    #print(f"disabled: {disabled}")

    matches = mult_exp.findall(line)
    #print(f"matches: {matches}")   
    multiplied = [int(t[0]) * int(t[1]) for t in matches]
    total = total + sum(multiplied)

print(f"result: {total}")