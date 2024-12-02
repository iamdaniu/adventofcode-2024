import csv
import bisect
import collections

list1 = []
list2 = []
with open('day1/data.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in spamreader:
        bisect.insort(list1, row[0])
        bisect.insort(list2, row[3])

    def add_tuple(t):
        return abs(int(t[0]) - int(t[1]))
    
    tuples = zip(list1, list2)
    differences = list(map(add_tuple, tuples))
    result = sum(differences)

    print("difference: {}".format(result))

    # similarity score
    occurrences_list2 = collections.Counter(list2)
    single_similarity = map(lambda v: int(v)*int(occurrences_list2[v]), list1)
    result = sum(single_similarity)

    print("similarities: {}".format(result))

