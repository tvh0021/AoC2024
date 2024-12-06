### AoC 2024, Day 6
### Trung Ha

import re
import numpy as np

from sol_D1 import read_input

# Let's try to visualize the path
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the directions based on the original input symbol
direction_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def traverse_map(
    binary_map: np.ndarray,
    starting_location: np.ndarray,
    current_direction_symbol: str,
    turning_sequence: list,
):

    current_location = starting_location
    current_direction = np.array(direction_map[current_direction_symbol])
    cell_already_visited = {tuple(current_location)}

    # For part 2, we need to keep track of the direction when the cell was first visited
    cell_and_direction_already_visited = {
        tuple(current_location): current_direction_symbol
    }

    while True:

        next_location = current_location + current_direction
        # If hit the edge of the map, stop
        if (
            next_location[0] < 0
            or next_location[0] >= binary_map.shape[0]
            or next_location[1] < 0
            or next_location[1] >= binary_map.shape[1]
        ):
            break

        # If hit obstacle, turn right
        if binary_map[next_location[0], next_location[1]] == 1:
            new_direction_symbol = turning_sequence[
                (turning_sequence.index(current_direction_symbol) + 1)
                % len(turning_sequence)
            ]  # move to the next symbol in the turning sequence, unless it's the last one, then go back to the first one
            current_direction = direction_map[new_direction_symbol]
            current_direction_symbol = new_direction_symbol
            next_location = current_location + current_direction

        binary_map[next_location[0], next_location[1]] = 3
        cell_already_visited.add(tuple(next_location))

        # For part 2, if the cell has been visited before, save the direction it used to cross that cell
        if tuple(next_location) in cell_and_direction_already_visited.keys():
            cell_and_direction_already_visited[
                tuple(next_location)
            ] += current_direction_symbol
        else:
            cell_and_direction_already_visited[tuple(next_location)] = (
                current_direction_symbol
            )

        current_location = next_location

    return binary_map, cell_and_direction_already_visited


def check_right(
    current_location: np.ndarray, current_direction_symbol: str, turning_sequence: list
):
    right_turn_direction_symbol = turning_sequence[
        (turning_sequence.index(current_direction_symbol) + 1) % len(turning_sequence)
    ]
    right_turn_direction = direction_map[right_turn_direction_symbol]
    right_turn_location = current_location + right_turn_direction
    return right_turn_location, right_turn_direction_symbol


def find_if_line_repeats(
    cell_and_direction_already_visited: dict,
    current_location: np.ndarray,
    current_direction_symbol: str,
):
    # Check if the current location or any of its forward locations have been visited before, if so, check if it's the same direction
    # If it is, then it has made a loop - PROBLEM: potentially you have to search forward until termination for each location

    while True:
        if tuple(current_location) in cell_and_direction_already_visited.keys():
            if (
                cell_and_direction_already_visited[tuple(current_location)]
                == current_direction_symbol
            ):
                return True
            else:

                continue


if __name__ == "__main__":
    data = read_input("test_input_D6.txt")
    # print(data)

    # Read data in as a binary 2d array
    # 0 = free space, 1 = obstacle

    binary_array = np.zeros((len(data), len(data[0])), dtype=int)
    current_direction = np.array([0, 0])
    current_direction_symbol = ""
    current_location = np.array([0, 0])
    # cell_already_visited = set()

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == "#":
                binary_array[i][j] = 1
            elif data[i][j] in ["<", ">", "^", "v"]:
                binary_array[i][j] = 2
                current_location = np.array([i, j])
                # cell_already_visited.add(tuple(current_location))
                current_direction = np.array(direction_map[data[i][j]])
                current_direction_symbol = data[i][j]

    print(binary_array.shape)
    # print(f"Map:\n {binary_array}")
    # print(f"Starting direction: {current_direction_symbol}")
    # print(f"Starting location: {cell_already_visited}")

    # Part 1
    # Define the turning directions - for part 1 these are the right turns only
    turning_map = ["^", ">", "v", "<"]  # order of the directions

    populated_binary_array, cell_already_visited = traverse_map(
        binary_array, current_location, current_direction_symbol, turning_map
    )

    print(f"Map after traversal:\n {populated_binary_array}")
    print(f"Location visited: {cell_already_visited}")
    print(f"Part 1 answer: {len(cell_already_visited)}")

    # Part 2
    # For part 2, to find all locations for obstacles to make a loop, observe that in order to make a loop,
    # if at any point the guard makes a right turn and the resulting direction is the same as the original
    # direction when it last crossed that location, then it has made a loop

    # Modify the traverse_map function to return both the visited cells and the direction it used to cross that cell

    # Find all locations where the path crosses itself
    for key, value in cell_already_visited.items():
        if len(value) > 1:
            print(f"Location {key} has been crossed {len(value)} times")
