from map_lib import Point
from map_lib import Map
from map_lib import print_map

def read_map(filename: str) -> Map:
    result: Map = Map()
    with open(filename) as mapfile:
        for line in mapfile.readlines():
            result.add_line(line)
    return result

def antinodes(tower_map: Map, frequency: str) -> set[Point]:
    points = tower_map.points_with_interest(frequency)
    result = set()
    for first in range(len(points)-1):
        point_1 = points[first]
        for second in range(first+1, len(points)):
            point_2 = points[second]
            diff = Point(point_1.y - point_2.y, point_1.x - point_2.x)

            #print(f"checking points {point_1} and {point_2}, diff {diff}")
            for candidate in [Point(point_1.y + diff.y, point_1.x + diff.x), Point(point_2.y - diff.y, point_2.x - diff.x) ]:
                if (not tower_map.out_of_bounds(candidate)):
                    #print(f"antinode found: {candidate}")
                    result.add(candidate)
                    tower_map.mark(candidate, "#")
                # else:
                #     print("out of bounds")
    #print(f"antinodes for {frequency}: {points}")
    return result



def main():
    tower_map = read_map('data/day8/data.map')
    all_antinodes = set()
    for frequency in tower_map.interesting_points():
        #print(f"checking frequency {frequency} - {tower_map.points_with_interest(frequency)}")
        frequency_antinodes = antinodes(tower_map, frequency)
        all_antinodes.update(frequency_antinodes)
    print(f"{len(all_antinodes)} antinodes: {all_antinodes}")
    #print_map(tower_map)


if __name__ == '__main__':
    main()