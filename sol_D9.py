### AoC 2024, Day 9
### Trung Ha

import numpy as np
from itertools import permutations

from sol_D1 import read_input


def calculate_checksum(long_list):
    multiples = [i * long_list[i] for i in range(len(long_list)) if long_list[i] > 0]
    return sum(multiples)


if __name__ == "__main__":
    data = read_input("input_D9.txt")
    # print(data)

    # Part 1
    # Separate the data into a list of files and free space
    # This question can be thought of as a two-pointer problem
    data = data[0]
    width_file_list = [int(data[i]) for i in range(0, len(data), 2)]
    width_space_list = [int(data[i]) for i in range(1, len(data), 2)]

    # print("Width of file list:", width_file_list)
    # print("Width of space list:", width_space_list)

    # print("Total width of files:", sum(width_file_list))
    # print("Total width of spaces:", sum(width_space_list))

    # We know how many spaces are in total (sum of width_space_list)
    # Find how many files are in total
    number_of_files = len(width_file_list)

    # Assign identifiers to files:
    identifiers = [i for i in range(number_of_files)]
    # print("Identifiers:", identifiers)

    # Use the identifiers as keys to a dict, with the values being the width of the files
    file_dict = dict(zip(identifiers, width_file_list))
    # print("File dict:", file_dict)

    # Work backward from the last file to distribute into the free spaces until
    a_long_list = []
    left_id = 0
    right_id = len(file_dict) - 1
    add_to_left = True

    while len(a_long_list) < sum(width_file_list):
        # first, add the left index to the list (starting from 0)
        if add_to_left:
            a_long_list.extend(file_dict[left_id] * [left_id])
        # then, add the right index to the list into the free spaces (starting from the largest id)

        # if the file is smaller than the space, add the file to the space, then reserve the free space left
        # if the file is larger than the space, add only part of the file to the space, then move on
        # if the file is equal to the space, add the whole file to the space, then move on
        this_available_space = width_space_list.pop(0)  # get the leftmost free space
        # print("This available space:", this_available_space)
        # print("Considering file id:", right_id)
        if file_dict[right_id] < this_available_space:
            a_long_list.extend(file_dict[right_id] * [right_id])
            # add the remaining free space back to the width_space_list
            width_space_list.insert(0, this_available_space - file_dict[right_id])

            right_id -= 1
            add_to_left = False
        elif file_dict[right_id] == this_available_space:
            a_long_list.extend(file_dict[right_id] * [right_id])
            right_id -= 1
            left_id += 1
            add_to_left = True
        else:
            a_long_list.extend(this_available_space * [right_id])
            file_dict[right_id] -= this_available_space
            left_id += 1
            add_to_left = True

        # print("Long list:", a_long_list)

    # Trim the list to the correct length
    a_long_list = a_long_list[: sum(width_file_list)]
    # print("Final long list:", a_long_list)

    # Calculate the checksum of the list
    checksum = calculate_checksum(a_long_list)
    print("Part 1 answer:", checksum)

    # Part 2
    # For this part, instead of squeezing in partial files into the free spaces,
    # we will just add the files that can fit in the free spaces

    width_file_list = [int(data[i]) for i in range(0, len(data), 2)]
    width_space_list = [int(data[i]) for i in range(1, len(data), 2)]
    file_dict = dict(zip(identifiers, width_file_list))

    # Work backward from the last file to distribute into the free spaces until
    # you run out of indices to move
    a_long_list = []
    left_id = 0
    right_ids_id = len(file_dict) - 1
    add_to_left = True

    # print("Width of file list:", width_file_list)
    # print("Width of space list:", width_space_list)
    # print("File dict:", file_dict)
    # print("left_id:", left_id)
    # print("right_id:", right_id)

    # Make a long list with -1 as placeholders (free spaces)
    for i in range(len(width_file_list) - 1):
        a_long_list.extend([i] * width_file_list[i])
        a_long_list.extend([-1] * width_space_list[i])
    a_long_list.extend([len(width_file_list) - 1] * width_file_list[-1])
    with open("output_ori_D9.txt", "w") as f:
        f.write(str(a_long_list))
    right_list_id = len(a_long_list) - 1
    # print("Long list:", a_long_list)

    # Track ids that have been moved
    ids_moved = set()
    ids_considered = set()

    while right_list_id >= 1:
        start_print = False

        # Special case: if left_id >= right_list_id, move left_id back to the left-most free space
        # and move right_ids_id to the left (skip the file)
        if left_id >= right_list_id:
            left_id = 0
            ids_considered.add(right_ids_id)
            right_list_id -= (
                file_dict[right_ids_id] + width_space_list[right_ids_id - 1]
            )
            right_ids_id -= 1
            outer_break_flag = False
            while a_long_list[left_id] != -1:
                left_id += 1
                if left_id >= right_list_id:  # stop if there are no more free spaces
                    outer_break_flag = True
                    break
            if outer_break_flag:
                break
            # print("Left id reset to:", left_id)

        # if a_long_list[right_list_id] == 3722:
        #     start_print = True
        #     print("Left id:", left_id)
        #     print("Number at left_id:", a_long_list[left_id])
        #     print("Right list id:", right_list_id)
        #     print("Number at right_list_id:", a_long_list[right_list_id])
        #     print(
        #         "Long list:",
        #         a_long_list[left_id - 5 : left_id + 10]
        #         + ["..."]
        #         + a_long_list[right_list_id - 15 : right_list_id + 1],
        #     )

        if a_long_list[left_id] != -1:
            left_id += 1
        else:
            # Count how many free spaces are there, compare with the file width of the right-most file
            # If the file width is smaller, add the file to the free spaces

            # count free spaces:
            count = 0
            tracking_id = left_id
            while a_long_list[tracking_id] == -1:
                count += 1
                tracking_id += 1
            if start_print:
                print("Free spaces:", count)
                print(f"File: {right_ids_id}, width: {file_dict[right_ids_id]}")

            if count >= file_dict[right_ids_id]:
                # add the file to the free spaces
                a_long_list[left_id : left_id + file_dict[right_ids_id]] = [
                    right_ids_id
                ] * file_dict[right_ids_id]
                # change the moved ids to -1
                a_long_list[
                    right_list_id - file_dict[right_ids_id] + 1 : right_list_id + 1
                ] = [-1] * file_dict[right_ids_id]
                ids_moved.add(right_ids_id)
                left_id += count

            else:  # if the file is too large, move the left_id to the next free space
                left_id += count
                continue

            ids_considered.add(right_ids_id)
            right_list_id -= (
                file_dict[right_ids_id] + width_space_list[right_ids_id - 1]
            )
            right_ids_id -= 1

            # if start_print:
            # print("Long list:", a_long_list[left_id : right_list_id + 10])
            # print("Set of moved ids:", ids_moved)

    # print("Final long list:", a_long_list)

    # Calculate the checksum of the list
    checksum = calculate_checksum(a_long_list)
    print("Part 2 answer:", checksum)

    # # Save the checksum list to a file
    # with open("output_D9.txt", "w") as f:
    #     f.write(str(a_long_list))
