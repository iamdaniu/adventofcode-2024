import csv
import bisect

list1 = []
list2 = []
with open('data/day1.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in spamreader:
        bisect.insort(list1, row[0])
        bisect.insort(list2, row[3])

    def add_tuple(t):
        return abs(int(t[0]) - int(t[1]))
    
    tuples = zip(list1, list2)
    differences = list(map(add_tuple, tuples))
    result = sum(differences)

    print("result: {}".format(result))
