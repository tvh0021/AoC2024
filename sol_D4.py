### AoC 2024, Day 4
### Trung Ha

import re
import numpy as np

from sol_D1 import read_input


def find_next_neighbor(data_array, current_position, current_value, direction=(0, 0)):
    """
    Find the next neighbor of the current position in the given direction that has the value of current_value + 1

    Args:
    - data_array: a 2d numpy array
    - current_position: a tuple of 2 integers, the current position
    - current_value: an integer, the current value
    - direction: a tuple of 2 integers, the direction to search for the next neighbor

    Returns:
    - a list of 2 elements: the next neighbor's position and the vector from the current position to the next neighbor
    """
    i, j = current_position
    neighbors = [
        (i + 1, j),
        (i - 1, j),
        (i, j + 1),
        (i, j - 1),
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
    ]
    # remove the neighbors whose indices are out of bound or negative
    neighbors = [
        n
        for n in neighbors
        if 0 <= n[0] < numeric_data.shape[0] and 0 <= n[1] < numeric_data.shape[1]
    ]

    # If no direction is given, return all possible directions
    if direction == (0, 0):
        list_of_neighbors = []
        for n in neighbors:
            if data_array[n] == current_value + 1:
                list_of_neighbors.append([n, (n[0] - i, n[1] - j)])

        return list_of_neighbors
    else:
        # If direction is given, return the next neighbor in that direction if it has the value of current_value + 1
        next_neighbor = (i + direction[0], j + direction[1])
        if (
            next_neighbor[0] >= 0
            and next_neighbor[0] < data_array.shape[0]
            and next_neighbor[1] >= 0
            and next_neighbor[1] < data_array.shape[1]
        ):
            if data_array[next_neighbor] == current_value + 1:
                return [next_neighbor, direction]


def find_cross_MAS(data_array, position_a):
    """Find the sequence MAS that makes a sequence of 3

    Args:
        data_array (np.ndarray): numpy 2d array of the data
        position_a (tuple): a tuple of 2 integers, the position of A

    Returns:
        int: 0 if the sequence cannot be completed, 1 if the sequence is completed
    """
    i, j = position_a

    diagonal_neighbors = [
        (i + 1, j + 1),
        (i - 1, j - 1),
        (i - 1, j + 1),
        (i + 1, j - 1),
    ]

    # Check if any of the diagonal neighbors is 0 OR 2, if not, then go to the next check
    if all([(data_array[n] != 0 and data_array[n] != 2) for n in diagonal_neighbors]):

        # Check if the "\" diagonal sequence has different values (M and S or S and M, not M and M or S and S)
        if data_array[i - 1, j - 1] != data_array[i + 1, j + 1]:

            # Check if the "/" diagonal sequence has different values (M and S or S and M, not M and M or S and S)
            if data_array[i - 1, j + 1] != data_array[i + 1, j - 1]:
                return 1

    return 0

    # return number_of_sequences


if __name__ == "__main__":
    data = read_input("input_D4.txt")
    # print(data)

    # Part 1
    # The general idea is to find all the "X" in the data, then search its neighborhood to find "M". If "M" is found,
    # record its relative position to "X", then extend the vector for "A" and "S". Once the sequence is completed, count it.

    # Convert to a 2d numpy array by substituting "X" with 0, "M" with 1, "A" with 2, and "S" with 3
    numeric_data = np.array(
        [
            [0 if x == "X" else 1 if x == "M" else 2 if x == "A" else 3 for x in row]
            for row in data
        ]
    )
    # print(numeric_data)

    # Find all the 0s
    x_positions = np.argwhere(numeric_data == 0)
    # print("X positions:", x_positions)

    # Find all the 1s that are in the neighborhood of 0s
    number_of_sequences = 0
    for x in x_positions:
        # print("x:", x)

        list_of_Ms = find_next_neighbor(numeric_data, x, 0)
        # print("list of Ms\n", list_of_Ms)

        if list_of_Ms is None:
            continue

        # go through the list of Ms to find the next A
        for m in list_of_Ms:
            # print("m:", m)
            next_A = find_next_neighbor(numeric_data, m[0], 1, m[1])
            # print("next A:", next_A)

            if next_A is None:
                continue

            # go through the next A to find the next S
            next_S = find_next_neighbor(numeric_data, next_A[0], 2, next_A[1])
            # print("next S:", next_S)

            if next_S is None:
                continue

            # if S is found, count it
            # print("Sequence found at:", x, m[0], next_A[0], next_S[0])
            number_of_sequences += 1

    print("Part 1 answer:", number_of_sequences)

    # Part 2
    # The general idea in this part is to find all the "A" in the data. Then, search its neighborhood for symmetrical "M...S" on both sides, but not crossing.

    # Find all the 2s
    a_positions = np.argwhere(numeric_data == 2)
    # print("A positions:", a_positions)

    # Eliminate the As that are on the edge since they cannot have symmetrical Ms and Ss
    a_positions = [
        a
        for a in a_positions
        if 0 < a[0] < numeric_data.shape[0] - 1 and 0 < a[1] < numeric_data.shape[1] - 1
    ]
    # print("A positions:", a_positions)
    # print("Number of As:", len(a_positions))

    # Loop through all the As to find the sequence MAS that crosses
    number_of_crosses = 0
    for a in a_positions:
        # print("a:", a)
        # print("neighbor: \n", numeric_data[a[0] - 1 : a[0] + 2, a[1] - 1 : a[1] + 2])
        number_of_crosses += find_cross_MAS(numeric_data, a)

    print("Part 2 answer:", number_of_crosses)
