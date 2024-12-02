import csv

with open('day2/data.csv', newline='') as csvfile:

    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    def is_safe(report):
        asc = True
        desc = True
        for v in range(0, len(report)-1):
            difference = int(report[v+1]) - int(report[v])
            asc = asc and difference > 0
            desc = desc and difference < 0
            if not asc and not desc:
                return False
            if abs(difference) < 1 or abs(difference) > 3:
                return False
        return True

    filtered = len([report for report in reader if is_safe(report)])
    print("safe count: {}".format(filtered))
