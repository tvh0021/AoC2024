### AoC 2024, Day 10
### Trung Ha

import numpy as np
from copy import deepcopy
from sol_D1 import read_input


def find_all_neighbors(arr1_x, arr1_y, arr2_x, arr2_y):
    """Find all elements in arr2 that are Chebyshev neighbors of elements in arr1"""
    neighbor_list = dict()
    for i in range(len(arr1_x)):
        neighbors = []
        for j in range(len(arr2_x)):
            if (
                abs(arr1_x[i] - arr2_x[j]) <= 1
                and abs(arr1_y[i] - arr2_y[j]) <= 1
                and (arr1_x[i] == arr2_x[j] or arr1_y[i] == arr2_y[j])
            ):
                neighbors.append(j)
        neighbor_list[i] = neighbors

    return neighbor_list


if __name__ == "__main__":
    data = read_input("input_D10.txt")
    sep_list = []
    for line in data:
        sep_list.append([int(line[i]) for i in range(len(line))])

    data_array = np.array(sep_list)

    # print(data_array)
    print("Shape of array:", data_array.shape)

    # Part 1
    # Find the number of unique elements in the entire array
    unique_elements = np.unique(data_array)

    # Find the positions of each unique element
    raw_positions = dict()
    for element in unique_elements:
        raw_positions[element] = np.where(data_array == element)

    # print("position dict:", raw_positions)

    # Scan through all unique elements from 0 to 9, for each zero, record all 1s that are its neighbors
    # Then for each 1, record all 2s that are its neighbors, and so on

    list_of_trail_paths = [
        [(int(raw_positions[0][0][i]), int(raw_positions[0][1][i]))]
        for i in range(len(raw_positions[0][0]))
    ]
    # print("List of trail paths:", list_of_trail_paths)

    list_of_linked_elements = []  # a list with elements from 0 to 8
    for i in range(len(unique_elements) - 1):
        list_of_linked_elements.append(
            [
                [(int(raw_positions[i][0][j]), int(raw_positions[i][1][j]))]
                for j in range(len(raw_positions[i][0]))
            ]
        )

    dict_of_trail_paths = dict(zip(unique_elements, list_of_linked_elements))
    # print("Dict of trail paths:", dict_of_trail_paths)
    for i in range(len(unique_elements) - 1):
        # print("Processing elevation ", i)
        this_element_positions = raw_positions[i]
        next_element_positions = raw_positions[i + 1]
        neighbors = find_all_neighbors(
            this_element_positions[0],
            this_element_positions[1],
            next_element_positions[0],
            next_element_positions[1],
        )
        # print("Neighbors of ", i, ":", neighbors)
        this_element_neighbor_x = []
        this_element_neighbor_y = []
        for j in neighbors:
            # print(f"{j}th {i}, neighbors: {neighbors[j]}")
            number_of_neighbors = len(neighbors[j])
            positions_of_neighbors = [
                (int(next_element_positions[0][k]), int(next_element_positions[1][k]))
                for k in neighbors[j]
            ]
            dict_of_trail_paths[i][j].append(positions_of_neighbors)
        # print("List of trail paths for this elevation: \n", dict_of_trail_paths[i])

    # print("Dict of trail paths: \n", dict_of_trail_paths)

    # For each trail head, find all possible paths through the dict_of_trail_paths
    for i in range(9):
        this_elevation = i
        # print("Processing elevation: ", this_elevation)
        number_of_current_trails = len(list_of_trail_paths)
        # print("Number of current trails: ", number_of_current_trails)
        numtrail = 0
        current_trail_list = []
        while numtrail < number_of_current_trails:
            this_trail = []
            this_sequence = list_of_trail_paths.pop()
            # print("Processing trail: ", this_sequence)
            this_element = this_sequence[-1]
            sequence_begin = this_sequence[:-1]
            # print("Processing trail head: ", this_element)
            # print("Sequence begin: ", sequence_begin)

            # find the element in the dict_of_trail_paths
            for j, link in enumerate(dict_of_trail_paths[this_elevation]):
                # print("links: ", link)
                if this_element == link[0]:  # if the beginning of this link is found
                    # print(
                    #     f"Element {this_element} with elevation {this_elevation} has {len(link[1])} neighbors with elevation {this_elevation + 1}"
                    # )
                    # find the neighbors of this element

                    for neighbor in link[1]:
                        if len(sequence_begin) == 0:
                            this_trail.append([this_element, neighbor])
                        else:
                            this_trail.append(sequence_begin + [this_element, neighbor])
                    # print("This trail: \n", this_trail)
            numtrail += 1
            current_trail_list += this_trail
        list_of_trail_paths = deepcopy(current_trail_list)
        # print("List of trail paths: \n", list_of_trail_paths)

    # Remove all trails that do not end at the last elevation
    valid_trails = set([tuple(trail_path) for trail_path in list_of_trail_paths])
    # print("Number of complete trails: ", len(valid_trails))

    # Compute the number of trails with unique start and end points
    unique_trails = set()
    for trail in valid_trails:
        unique_trails.add((trail[0], trail[-1]))

    print("Number of unique trails: ", len(unique_trails))

    # Part 2
    # We already have the list of valid trails
    print("Number of valid trails: ", len(valid_trails))
