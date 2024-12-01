### AoC 2024, Day 1
### Trung Ha

import re
import numpy as np


def read_input(file_name):
    with open(file_name, "r") as f:
        return f.read().splitlines()


if __name__ == "__main__":
    data = read_input("input_D1.txt")
    # print(data)

    # Part 1
    # Get each column of the input data
    list_1 = []
    list_2 = []

    for i in range(len(data)):
        this_line = re.findall(r"\d+", data[i])
        list_1.append(int(this_line[0]))
        list_2.append(int(this_line[1]))

    # print(list_1)
    # print(list_2)

    # Sort lists
    list_1.sort()
    list_2.sort()

    # print(list_1)
    # print(list_2)

    # Find the difference between each pair, sum the result up
    total_difference = 0
    for i in range(len(list_1)):
        total_difference += abs(list_2[i] - list_1[i])

    print(f"Part 1 answer : {total_difference}")

    # Part 2
    # Convert the lists to numpy arrays
    array_1 = np.array(list_1)
    array_2 = np.array(list_2)

    # Count the occurrence of each number in the right array
    unique, counts = np.unique(array_2, return_counts=True)
    # print(unique)
    # print(counts)

    # Loop through the left array, find the number of occurrence of each number in the right array
    total_similarity = 0
    for i, num in enumerate(array_1):
        if num in unique:
            # print(
            #     f"Number {num} appears {counts[np.where(unique == num)[0][0]]} times in the right array"
            # )
            total_similarity += counts[np.where(unique == num)[0][0]] * num

    print(f"Part 2 answer : {total_similarity}")
