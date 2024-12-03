import csv

def calculate_differences(report):
    return [int(report[v+1])-int(report[v]) for v in range(0, len(report)-1)]

class ListInfo:
    def __init__(self, list):
        self.original_list = list
        self.differences = calculate_differences(list)
        self.list_length = len(self.differences)
        self.negative_indices = []
        self.positive_indices = []
        self.zero_indices = []
        self.threshold_exceed_indices = []

        for index in range(0, len(self.differences)):
            difference = self.differences[index]
            if difference < 0:
                self.negative_indices.append(index)
            elif difference > 0:
                self.positive_indices.append(index)
            else:
                self.zero_indices.append(index)
            if abs(difference) < 1 or abs(difference) > 3:
                self.threshold_exceed_indices.append(index)

        sd = max(len(self.negative_indices), len(self.positive_indices))
        self.sign_differences = len(self.differences) - sd


def is_safe(info: ListInfo, dampen = 0):
#    print(f"checking safety of {info.original_list}")
    if len(info.zero_indices) > dampen:
        return False
    if info.sign_differences > dampen:
        return False
    # we cannot dampen a threshold error for a strictly ascending or descending list
    if info.sign_differences != 0:
        corrections = set(info.zero_indices)
        corrections.update(info.threshold_exceed_indices)
        if len(info.positive_indices) < len(info.negative_indices):
            corrections.update(info.positive_indices)
        else:
            corrections.update(info.negative_indices)

        if len(corrections) == 0:
            return True
        if len(corrections) <= dampen:
            remove_index = list(corrections)[0]
            corrected_list = [info.original_list[i] for i in range(0, len(info.original_list)) if i != remove_index]
            corrected_info = ListInfo(corrected_list)
            print(f"{info.original_list}: trying corrected version by removing {remove_index}: {corrected_list}")
            result = is_safe(corrected_info, dampen - 1)
            if result:
                print("this is ok")
            return result
    else:
        return len(info.threshold_exceed_indices) == 0


def format_info(info):
    return f"neg: {info.negative_indices} pos: {info.positive_indices} th: {info.threshold_exceed_indices}"

with open('day2/data.csv', newline='') as csvfile:

    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    
    def count_errors(error_list):
        filtered = [error for error in error_list if error == False]
        return len(filtered)

    #differences = [calculate_differences(x) for x in reader]
    infos = [ListInfo(d) for d in reader]

    safe = [l for l in infos if is_safe(l)]
    print("safe:", len(safe))

    dampened_safe = [l for l in infos if is_safe(l, 1)]
    print("safe:", len(dampened_safe))

