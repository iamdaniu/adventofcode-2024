
import bisect

class FileMap:
    def __init__(self, short_form: str):
        current_file_index = 0
        self.expanded_map: list[str] = []
        self.last_file_index = -1
        # self.empty_indices: list[int] = []
        # self.file_indices: list[int] = []
        reading_file_size = True
        for c in short_form:
            if reading_file_size:
                to_append = str(current_file_index)
                current_file_index += 1
                self.last_file_index = len(self.expanded_map) + int(c) - 1
            else:
                to_append = '.'
            for i in range(int(c)):
                self.expanded_map.append(to_append)
            reading_file_size = not reading_file_size

    def __str__(self) -> str:
        return f'{self.expanded_map}, files at {self.file_indices}, empty at {self.empty_indices}'
    
    def move_file_to_empty(self, file_index: int, empty_index: int):
        #print(f'{self.expanded_map}: moving {file_index} to {empty_index}')
        self.expanded_map[empty_index] = self.expanded_map[file_index]
        self.expanded_map[file_index] = '.'
        #= self.expanded_map[0:empty_index] + self.expanded_map[file_index] + self.expanded_map[empty_index+1:file_index] + '.' + self.expanded_map[file_index+1:]
        for i in range(file_index, 0, -1):
            if self.expanded_map[i] != '.':
                self.last_file_index = i
                break
        # self.file_indices.remove(file_index)
        # bisect.insort(self.file_indices, empty_index)
        # self.empty_indices.remove(empty_index)
        # bisect.insort(self.empty_indices, file_index)
        #print(f'{self.expanded_map}')

    def first_free_index(self) -> int:
        return self.expanded_map.index('.')

    def last_file_index(self) -> int:
        return self.last_file_index
    
    def packed(self) -> bool:
        return self.first_free_index() > self.last_file_index

    def checksum(self) -> int:
        return sum([index*int(self.expanded_map[index]) for index in range(len(self.expanded_map)) if self.expanded_map[index] != '.'])

#def last_index_with_fileblock(file_map: str)

def main():
    with open('data/day9/data.disk') as input_file:
        line = input_file.readline().strip()
        expanded = FileMap(line)

    #print(f'before pack: {expanded}')
    # counter: int = 0
    while not expanded.packed():
        move_from = expanded.last_file_index
        move_to = expanded.first_free_index()
        expanded.move_file_to_empty(move_from, move_to)
        # counter += 1
        # print(f'{counter}')
    print(f'checksum after pack: {expanded.checksum()}')

if __name__ == "__main__":
    main()