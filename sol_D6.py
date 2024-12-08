### AoC 2024, Day 6
### Trung Ha

import re
import numpy as np

from sol_D1 import read_input

from tqdm import tqdm
import time
import copy
from multiprocessing import Pool

# Define the directions based on the original input symbol
direction_map = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def traverse_map(
    binary_map: np.ndarray,
    starting_location: np.ndarray,
    current_direction_symbol: str,
    turning_sequence: list,
    cell_and_direction_already_visited: dict = None,
):

    current_location = starting_location
    current_direction = direction_map[current_direction_symbol]
    cell_already_visited = {tuple(current_location)}

    # For part 2, we need to keep track of the direction when the cell was visited before
    if cell_and_direction_already_visited is None:
        cell_and_direction_already_visited = {
            tuple(current_location): current_direction_symbol
        }

    in_a_loop = False
    loop_elements = 0
    start_time = time.time()

    while True:

        next_location = current_location + current_direction
        # If hit the edge of the map, stop
        if (
            next_location[0] < 0
            or next_location[0] >= binary_map.shape[0]
            or next_location[1] < 0
            or next_location[1] >= binary_map.shape[1]
        ):
            # print(f"Hit the edge of the map at location {current_location}")
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

        # # If in a loop, stop
        # if is_a_loop(
        #     cell_and_direction_already_visited,
        #     next_location,
        #     current_direction_symbol,
        # ):
        #     # print(f"Loop detected at location {current_location}")
        #     # in_a_loop = True
        #     # break
        #     loop_elements += 1

        # if loop_elements > 10000:
        #     in_a_loop = True
        #     break

        # binary_map[next_location[0], next_location[1]] = 3
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

        # worst coding practice ever, time the loop
        if time.time() - start_time > 1.5:
            in_a_loop = True
            break

    # if in_a_loop:
    # print(f"Loop detected at location {current_location}")

    return binary_map, cell_and_direction_already_visited, in_a_loop


def turn_right(current_direction_symbol: str, turning_sequence: list):
    right_turn_direction_symbol = turning_sequence[
        (turning_sequence.index(current_direction_symbol) + 1) % len(turning_sequence)
    ]
    return right_turn_direction_symbol


def put_obstacle_in_front(
    binary_map: np.ndarray, current_location: np.ndarray, current_direction_symbol: str
):
    new_map = copy.deepcopy(binary_map)
    current_direction = direction_map[current_direction_symbol]
    next_location = current_location + current_direction
    if (
        next_location[0] < 0
        or next_location[0] >= binary_map.shape[0]
        or next_location[1] < 0
        or next_location[1] >= binary_map.shape[1]
    ):
        print(f"Hit the edge of the map at location {current_location}")
        return new_map
    else:
        new_map[next_location[0], next_location[1]] = 1
    return new_map


def is_a_loop(
    cell_and_direction_already_visited: dict,
    current_location: np.ndarray,
    current_direction_symbol: str,
):
    """Check if the next location has been visited before and if it has, check if the direction is the same as before

    Args:
        cell_and_direction_already_visited (dict): a dictionary of locations and the direction it used to arrive at that location
        current_location (np.ndarray): the current location
        current_direction_symbol (str): the current direction in string format
    """
    # next_location = current_location + direction_map[current_direction_symbol]

    if tuple(current_location) in cell_and_direction_already_visited.keys():
        # for direction_symbol in cell_and_direction_already_visited[
        #     tuple(current_location)
        # ]:
        #     if direction_symbol == current_direction_symbol:
        #         return True
        if (
            current_direction_symbol
            in cell_and_direction_already_visited[tuple(current_location)]
        ):
            return True
    else:
        return False


def search_path_parallel(
    binary_map, turning_sequence, cell_and_direction_already_visited
):
    path_checkers = []
    for key, value in cell_already_visited.items():
        if len(value) == 1:
            path_checkers.append([key, value])
        else:
            for i in range(len(value)):
                path_checkers.append([key, value[i]])

    # this_map = copy.deepcopy(binary_map)

    print(f"Number of paths needed to check: {len(path_checkers)}")

    with Pool() as p:
        items = [
            (
                copy.deepcopy(binary_map),
                path_checkers[k][0],
                path_checkers[k][1],
                turning_sequence,
                copy.deepcopy(cell_and_direction_already_visited),
            )
            for k in range(len(path_checkers))
        ]
        # print(f"Items: {items}")

        # number_of_loops = 0
        # results = p.starmap(search_path, items)
        for i in enumerate(p.starmap(search_path, items)):
            print(f"Path {i[0]}: {i[1]}")
        number_of_loops = 0  # sum(results)

    return number_of_loops


def search_path(
    binary_map: np.ndarray,
    starting_location: np.ndarray,
    current_direction_symbol: str,
    turning_sequence: list,
    cell_and_direction_already_visited: dict,
):
    new_array = put_obstacle_in_front(
        binary_map, starting_location, current_direction_symbol
    )
    # print(f"Starting location: {starting_location}")
    # print(f"Starting direction: {current_direction_symbol}")
    # print(f"Turning sequence: {turning_sequence}")
    # print(f"Visited cells: {cell_and_direction_already_visited}")
    print(f"New array: {new_array}")

    _, _, loop = traverse_map(
        new_array,
        starting_location,
        current_direction_symbol,
        turning_sequence,
        cell_and_direction_already_visited,
    )
    return 1 if loop else 0


if __name__ == "__main__":
    data = read_input("input_D6.txt")
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
                binary_array[i, j] = 1
            elif data[i][j] in ["<", ">", "^", "v"]:
                binary_array[i, j] = 2
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

    populated_binary_array, cell_already_visited, _ = traverse_map(
        binary_array, current_location, current_direction_symbol, turning_map
    )

    # print(f"Map after traversal:\n {populated_binary_array}")
    # print(f"Location visited: {cell_already_visited}")
    print(f"Part 1 answer: {len(cell_already_visited)} \n")

    # Part 2
    # For part 2, to find all locations for obstacles to make a loop, observe that in order to make a loop,
    # if at any point the guard makes a right turn and the resulting direction is the same as the original
    # direction when it last crossed that location, then it has made a loop

    # Brute force, for all N - 1 locations, turn right and check if the path loops

    path_checkers = []
    for key, value in cell_already_visited.items():
        if len(value) == 1:
            path_checkers.append([key, value])
        else:
            for i in range(len(value)):
                path_checkers.append([key, value[i]])

    print(f"Number of paths needed to check: {len(path_checkers)}")

    # Evolve all the paths
    number_of_loops = 0
    for i in tqdm(range(len(path_checkers))):

        # print(
        #     f"Parameters: starting location: {path_checkers[i][0]}, starting direction: {path_checkers[i][1]}"
        # )
        new_array = put_obstacle_in_front(
            binary_array, np.array(path_checkers[i][0]), path_checkers[i][1]
        )
        # print(f"New array:\n{new_array}")
        _, cell_and_direction_already_visited, loop = traverse_map(
            new_array,
            np.array(path_checkers[i][0]),
            path_checkers[i][1],
            turning_map,
            copy.deepcopy(cell_already_visited),
        )
        # print(f"Visited cells: {cell_and_direction_already_visited}")

        if loop:
            number_of_loops += 1

    # number_of_loops = search_path_parallel(
    #     binary_array, turning_map, cell_already_visited
    # )

    print(f"Number of loops: {number_of_loops}")
