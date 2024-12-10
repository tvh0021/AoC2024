### AoC 2024, Day 3
### Trung Ha

import re
import numpy as np

from sol_D1 import read_input


def get_sum_of_mul(this_data: str) -> int:
    """Get the sum of all instances of mul(a,b) in the input string

    Args:
        this_data (str): The input string

    Returns:
        int: The sum of all instances of mul(a,b) in the input string
    """
    total_sum = 0
    row_split = re.split(r"mul\(", this_data)
    for anelem in row_split:
        try:
            result = re.match(r"(\d+),(\d+)\)", anelem).groups()
            total_sum += int(result[0]) * int(result[1])
        except AttributeError:
            pass
    return total_sum


if __name__ == "__main__":
    # Read input
    data = read_input("input_D3.txt")
    # print("\n".join(data))
    print(f"Number of rows: {len(data)}")

    # join all rows into one string, avoid the pitfall of having a "don't()" at the end of a row and it not being counted when the next row starts
    data = "".join(data)
    print("raw data: ", data)

    # Part 1
    # Search all instances where the input has "mul(", separate into chunks
    # Then, for each split, check if first element is a number, followed by a comma, then another number, then a closing parenthesis
    sum_of_mul = get_sum_of_mul(data)

    print(f"Part 1 answer: {sum_of_mul}")

    # Part 2
    # Now we search for all instances of "do()" and "don't()", separate the "do()" into a list, throw out the "don't()"
    # Then, rerun part 1
    presplit_data = []
    row_keep = re.split(r"do\(\)", data)
    # print(row_keep)
    for elem in row_keep:
        if "don't()" not in elem:
            presplit_data.append(elem)
        else:
            row_remain = re.split(r"don't\(\)", elem)
            # print(len(row_remain))
            presplit_data.append(row_remain[0])
            # print(row_remain[0])

    # print(presplit_data)
    sum_of_mul = 0
    for i in range(len(presplit_data)):
        print(f"row {i}: {presplit_data[i]}")
        this_sum_of_mul = get_sum_of_mul(presplit_data[i])
        sum_of_mul += this_sum_of_mul

    print(f"Part 2 answer: {sum_of_mul}")
