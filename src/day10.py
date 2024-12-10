
import logging

from map_lib import Point
from map_lib import Map
from map_lib import print_map

logger = logging.getLogger(__name__)

class TopographyMap(Map):
    def __init__(self):
        super().__init__()
        self.trailheads: list[Point] = []

    def add_line(self, line):
        super().add_line(line)
        th_index = line.find('0')
        while th_index != -1:
            self.trailheads.append(Point(len(self.data)-1, th_index))
            th_index = line.find('0', th_index+1)

def neighbors(m: Map, position: Point):
    translations = [(0,1), (0,-1), (1,0), (-1,0)]
    new_points = [position.translate(tr) for tr in translations if not m.out_of_bounds(position.translate(tr))]
    current_index = 0
    while current_index < len(new_points):
        yield new_points[current_index]
        current_index += 1

def read_map(filename: str) -> TopographyMap:
    with open(filename) as map_file:
        topography_map: TopographyMap = TopographyMap()
        for line in map_file.readlines():
            topography_map.add_line(line)
    print_map(topography_map, logger=logger, level=logging.DEBUG)
    logger.debug(f'trailheads: {topography_map.trailheads}')
    for th in topography_map.trailheads:
        for neighbor in neighbors(topography_map, th):
            logger.debug(f'candidate: {neighbor}')
    return topography_map

def get_paths(topography_map: TopographyMap) -> list[list[Point]]:
    paths: list[list[Point]] = [[th] for th in topography_map.trailheads]
    new_paths = []
    for height in range(9):
        for path in paths:
            for neighbor in neighbors(topography_map, path[len(path)-1]):
                if int(topography_map.value_at(neighbor)) == height+1:
                    new_path = list(path)
                    new_path.append(neighbor)
                    new_paths.append(new_path)
            paths = new_paths
            if len(paths) == 0:
                break
        new_paths = []
    return paths

def paths_from_trailhead(paths: list[list[Point]]) -> dict[Point, list[Point]]:
    result: dict[Point, list[list[Point]]] = {}
    for p in paths:
        result.setdefault(p[0], []).append(p)
    return result

def endpoints_from_paths(paths: list[list[Point]]) -> set[Point]:
    return set([p[len(p)-1] for p in paths])

def main():
    logging.basicConfig(level=logging.INFO)
    topography_map = read_map("data/day10/data.map")

    paths = get_paths(topography_map)

    paths_by_trailheads = paths_from_trailhead(paths)

    scores = 0
    ratings = 0
    for th in paths_by_trailheads.keys():
        trailhead_paths = paths_by_trailheads[th]
        endpoints = endpoints_from_paths(trailhead_paths)
        scores += len(endpoints)
        rating = len(trailhead_paths)
        ratings += rating
        logging.debug(f'trailhead {th}: score {len(endpoints)} ({endpoints})')
        logging.debug(f'trailhead {th}: rating {len(trailhead_paths)} ({trailhead_paths})')

    print(f'sum scores: {scores}')
    print(f'sum rating: {ratings}')

if __name__ == '__main__':
    main()