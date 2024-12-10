### AoC 2024, Day 5
### Trung Ha

import re
import numpy as np

from sol_D1 import read_input


if __name__ == "__main__":
    data = read_input("input_D5.txt")
    # print(data)

    # Divide the data into two parts, the lookup table and the sequences
    sep_idx = data.index("")
    lookup_table = data[:sep_idx]
    sequences = data[sep_idx + 1 :]

    # print("Table:", lookup_table)
    # print("Sequences:", sequences)

    # Separate the lookup table into dicts
    lookup_dict = {}
    for line in lookup_table:
        key, value = line.split("|")
        # print("Key:", key)
        # print("Value:", value)
        if int(key) in lookup_dict.keys():
            lookup_dict[int(key)] += [int(value)]
        else:
            lookup_dict[int(key)] = [int(value)]

    # print("Lookup dict:", lookup_dict)

    # Part 1
    # To check for correct ordering of each sequence, we need to check backwards.
    # If the last element of the sequence is a key in the lookup table, then no other
    # element can be in the value list of that key. If the last element is not a key, then
    # the second last element becomes the key, and so on.

    invalid_sequences = []
    sum_middle_elements = 0
    for sequence in sequences:
        # print("Sequence:", sequence)
        sequence = list(map(int, sequence.split(",")))
        sequence_original = sequence.copy()
        # print("Sequence:", sequence)

        this_line_flag = True
        while this_line_flag and len(sequence) > 0:
            # pop the last element of the sequence, using it as the key
            last_element = sequence.pop()
            if last_element in lookup_dict.keys():
                # check if any of the remaining elements are in the value list of the key
                if any(x in lookup_dict[last_element] for x in sequence):
                    # print("Invalid sequence")
                    this_line_flag = False
                    invalid_sequences.append(sequence_original)
                    break
                else:
                    if len(sequence) == 0:
                        # print("Valid sequence, moving to next sequence")
                        # record the middle element of the valid sequence for later
                        sum_middle_elements += sequence_original[
                            len(sequence_original) // 2
                        ]
                        break
                    # print("Valid element, checking next element in sequence")
                    continue
            else:
                # print("Not a key, checking the next element")
                continue

    print("Part 1 answer:", sum_middle_elements)

    # Part 2
    # We need to find the sum of the middle elements of the invalid sequences (after fixing them)

    # print("Invalid sequences:", invalid_sequences)

    # To fix the invalid sequences, we do the same process as in Part 1, but not popping the last element,
    # and instead, we check if the last element is in the value list of the second last element. If it is, then
    # the second last element is moved to the position immediately after the last element, and so on.

    sum_middle_elements_fixed = 0
    for sequence in invalid_sequences:
        # sequence_original = sequence.copy()
        original_length = len(sequence)

        # debugging a potential bug
        if len(sequence) % 2 == 0:
            print("Even length sequence:", sequence)

        # print("Invalid sequence:", sequence)
        this_index = len(sequence) - 1
        run_again_flag = True  # totally cheating here; rerun one more time to make sure the entire sequence is fixed
        while this_index >= 1:
            this_element = sequence[this_index]
            # print("Checking element:", this_element)
            if this_element in lookup_dict.keys():
                for elem in sequence[:this_index]:
                    # if the element is in the lookup table, then it needs to be moved to behind the key
                    if elem in lookup_dict[this_element]:
                        run_again_flag = True  # if at any point a faulty element is found, rerun the entire sequence at the end to make sure the new order is correct
                        sequence.remove(elem)
                        sequence.insert(this_index, elem)
                        # print(f"Moved {elem} to behind {this_element}")
                this_index -= (
                    1  # if no faulty element is found, move to the next element
                )
            else:
                this_index -= 1  # if the element is not in the lookup table, move to the next element

            if this_index == 0 and run_again_flag:
                this_index = len(sequence) - 1
                # print("Rerunning the entire sequence")
                run_again_flag = False
            elif this_index == 0 and not run_again_flag:
                break

        # print("Fixed sequence:", sequence)

        sum_middle_elements_fixed += sequence[len(sequence) // 2]

    print("Part 2 answer:", sum_middle_elements_fixed)
