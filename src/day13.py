
from map_lib import Point
import re
import math
import logging
from re import Pattern
from re import Match

adjust: int = 10000000000000

button_re = r'Button [AB]: X\+(\d+), Y\+(\d+)'
button_pattern = re.compile(button_re)

prize_re = r'Prize: X=(\d+), Y=(\d+)'
prize_pattern = re.compile(prize_re)

def read_tuple(line: str, pattern: Pattern) -> tuple[int, int]:
    match: Match[str] = pattern.match(line.strip())
    return (int(match.group(1)), int(match.group(2)))

def calc_b(prize, button_a, button_b):
    b = (prize[1] - ((prize[0] * button_a[1]) / button_a[0])) / (button_b[1] - ((button_b[0] * button_a[1]) / button_a[0]))
    return round(b)

def calc_a(b: int, prize: tuple[int, int], xa: int, xb: int):
    return (prize[0] - (b * xb)) / xa

def price(a: int, b: int):
    return 3 * a + b

logger = logging.getLogger(__name__)

with open('data/day13/data.txt') as input_file:
    # logging.basicConfig(level=logging.DEBUG)
    total_price = 0
    while True:
        button_a = read_tuple(input_file.readline(), button_pattern)
        button_b = read_tuple(input_file.readline(), button_pattern)
        prize = read_tuple(input_file.readline(), prize_pattern)
        prize = (prize[0] + adjust, prize[1] + adjust)
        logger.debug(f'button1: {button_a}, button2: {button_b}, prize: {prize}')
        b = int(calc_b(prize, button_a, button_b))
        a = int(calc_a(b, prize, button_a[0], button_b[0]))
        lands_at = (a*button_a[0]+b*button_b[0], a*button_a[1]+b*button_b[1])
        if lands_at == prize:
            run_price = price(a, b)
            logger.debug(f' solution: a={a}, b={b}, price {run_price}')
            total_price += price(a, b)
        else:
            diff_vector = (prize[0] - lands_at[0], prize[1] - lands_at[1])
            diff = math.sqrt(diff_vector[0]**2 + diff_vector[1]**2)
            logger.debug(f'no solution; lands at {lands_at}, should {prize} - diff {diff}')
        if input_file.readline() == '':
            break
    print(f'total price: {total_price}')
