
from map_lib import Point, Map, print_map
import logging

logger = logging.getLogger(__name__)


def neighbors(p: Point) -> list[Point]:
    return [ p.translate(d) for d in [ (-1, 0), (0, -1), (1, 0), (0, 1) ] ]

class Region:
    def __init__(self, value: str):
        self.value = value
        self.points: set[Point] = set()

    def area(self):
        return len(self.points)

    def add_point(self, p: Point):
        self.points.add(p)

    def belongs(self, value: str, p: Point):
        if len(self.points) == 0:
            return True
        for contained_point in self.points:
            if contained_point.is_neighbor(p):
                return True
        return False
    
    def merge(self, other):
        if self.value != other.value:
            raise ValueError(f'incompatible values {self.value}, {other.value}')
        self.points = self.points.union(other.points)

    def __repr__(self):
        return f'{self.value} - {self.points}'

class Garden(Map):
    def __init__(self):
        super().__init__()
        self.regions: dict[str, list[Region]] = {}
    
    def add_line(self, line: str):
        super().add_line(line)
        y = len(self.data)-1

        for x in range(len(line)):
            current_point = Point(y, x)
            value = self.value_at(current_point)
            current_regions = self.regions.get(value)
            new_regions: list[Region] = []
            new_region: Region = Region(value)
            new_region.add_point(current_point)
            if current_regions:
                for region in current_regions:
                    if region.belongs(value, current_point):
                        new_region.merge(region)
                    else:
                        new_regions.append(region)
                new_regions.append(new_region)
                self.regions[value] = new_regions
            else:
                self.regions[value] = [ new_region ]

    
def perimeter_points(region: Region, garden: Map) -> set[Point]:
    result: list[Point] = []
    for p in region.points:
        for n in neighbors(p):
            if not n in region.points:
                result.append(n)
    return result

def number_of_sides(points: set[Point]) -> int:
    horizontal = { point.y for point in points}
    vertical = { point.x for point in points}
    return len(horizontal) + len(vertical)

def price(region: Region, garden: Map) -> int:
    return region.area() * len(perimeter_points(region, garden))

def main():
    logging.basicConfig(level=logging.DEBUG)
    garden: Garden = Garden()
    with open('data/day12/sample.map') as map_file:
        for line in map_file.readlines():
            logger.debug('reading line')
            garden.add_line(line.strip())
    print_map(garden, logger=logger, level=logging.DEBUG)
    total_price = 0
    logger.debug('regions:')
    for v, rs in garden.regions.items():
        logger.debug(f'{v}')
        for region in rs:
            perimeter = perimeter_points(region, garden)
            current_price = price(region, garden)
            sides = number_of_sides(perimeter)
            logger.debug(f'{region}\n  area: { region.area() }\n  perimeter ({len(perimeter)}, {sides} sides): {perimeter}\n  price: {current_price}')
            total_price += current_price
    print(f'total price: {total_price}')

if __name__ == '__main__':
    main()