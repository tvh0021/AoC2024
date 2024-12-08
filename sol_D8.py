### AoC 2024, Day 8
### Trung Ha

import numpy as np
from itertools import permutations

from sol_D1 import read_input


def get_positions(data_array, element):
    """Get the positions of a given element in the data array"""
    positions = np.where(data_array == element)
    return positions


def get_vector(p1, p2):
    """Get the vector between two points"""
    return (p2[0] - p1[0], p2[1] - p1[1])


def extend_on_either_side(p1, p2, vector):
    """Extend the vector to find the two elements to either side of the pair"""
    return (p1[0] - vector[0], p1[1] - vector[1]), (
        p2[0] + vector[0],
        p2[1] + vector[1],
    )


def extend_until_edge(p1, p2, vector, shape):
    """Extend the vector until it hits the edge of the array"""
    p_list = [p1, p2]
    while True:
        p2 = (p2[0] + vector[0], p2[1] + vector[1])
        if 0 <= p2[0] < shape[0] and 0 <= p2[1] < shape[1]:
            p_list.append(p2)
        else:
            break
    while True:
        p1 = (p1[0] - vector[0], p1[1] - vector[1])
        if 0 <= p1[0] < shape[0] and 0 <= p1[1] < shape[1]:
            p_list.append(p1)
        else:
            break

    return p_list


if __name__ == "__main__":
    data = read_input("input_D8.txt")
    sep_list = []
    for line in data:
        sep_list.append([line[i] for i in range(len(line))])

    data_array = np.array(sep_list)

    # print(data_array)
    print("Shape of array:", data_array.shape)

    # Part 1
    # Find the number of unique elements in the entire array
    unique_elements = np.unique(data_array)
    # remove the background element
    unique_elements = unique_elements[unique_elements != "."]
    # print("Unique elements: ", unique_elements)
    # print("Number of unique elements: ", len(unique_elements))

    # For each unique element, get the positions of the element
    positions_dict = dict()
    for element in unique_elements:
        positions = get_positions(data_array, element)
        # print(f"Element {element} has positions: {positions}")
        positions_dict[str(element)] = [
            (int(positions[0][i]), int(positions[1][i]))
            for i in range(len(positions[0]))
        ]
    # print("Position dict:", positions_dict)

    # Make pairs of same elements
    pairs_dict = dict()
    for key in positions_dict:
        pairs = list(permutations(positions_dict[key], 2))
        pairs_dict[key] = pairs

    # print("Pair dict": pairs_dict)

    # Find the vector between the pairs
    vector_dict = dict()
    for key in pairs_dict:
        vectors = [get_vector(pair[0], pair[1]) for pair in pairs_dict[key]]
        vector_dict[key] = vectors

    # print("Vector dict:", vector_dict)

    # Apply the vector to find the two elements to either side of each pair
    # a set also removes duplicates
    new_resonance_set = set()
    for key in pairs_dict:
        for i, pair in enumerate(pairs_dict[key]):
            p1, p2 = pair
            vector = vector_dict[key][i]
            p3, p4 = extend_on_either_side(p1, p2, vector)
            new_resonance_set.add(p3)
            new_resonance_set.add(p4)

    # print("New resonance set:", new_resonance_set)

    # Remove all the new elements outside of the array
    new_resonance_set = {
        element
        for element in new_resonance_set
        if 0 <= element[0] < data_array.shape[0]
        and 0 <= element[1] < data_array.shape[1]
    }

    print("Part 1 answer:", len(new_resonance_set))

    # Part 2
    # For this part, just rewrite the extend_on_either_side function to
    # extend the vector until it hits the edge of the array
    extended_resonance_set = set()
    for key in pairs_dict:
        for i, pair in enumerate(pairs_dict[key]):
            p1, p2 = pair
            vector = vector_dict[key][i]
            p_list = extend_until_edge(p1, p2, vector, data_array.shape)
            extended_resonance_set.update(p_list)

    print("Part 2 answer:", len(extended_resonance_set))
