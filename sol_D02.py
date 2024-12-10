### AoC 2024, Day 1
### Trung Ha


from sol_D1 import read_input
import re
import numpy as np


def check_if_diff_same_sign(row: np.array) -> tuple[bool, int]:
    """
    Check if the differences between consecutive numbers in a row have the same sign,
    and return the index of the troublemaker
    """
    if 0 in row:
        return (False, np.where(row == 0)[0][0])

    sign = np.sign(row[0])
    for i in range(1, len(row)):
        if np.sign(row[i]) != sign:
            return (False, i)

    return (True, -1)


def check_if_diff_at_most_three(row: np.array) -> tuple[bool, int]:
    """
    Check if the differences between consecutive numbers in a row are at most 3,
    and return the index of the troublemaker
    """
    for i in range(len(row)):
        if (row[i]) > 3 or (row[i] < -3):
            return (False, i + 1)

    return (True, -1)


def spot_flaw(list_of_reports: list[np.ndarray]):
    """
    Check if the list of rows passes the two conditions
    """
    # Find the difference between consecutive numbers in each row
    list_of_differences = []
    for i in range(len(list_of_reports)):
        list_of_differences.append(np.ediff1d(list_of_reports[i]))

    # Check conditions
    boolean_array_same_sign = np.zeros(len(list_of_differences), dtype=bool)
    failed_index_same_sign = np.ones(len(list_of_differences), dtype=int) * -1
    for i in range(len(list_of_differences)):
        result, failed_index = check_if_diff_same_sign(list_of_differences[i])
        if result == True:
            # print(f"Row {i} passes the same sign condition")
            boolean_array_same_sign[i] = True
        else:
            # print(f"Row {i} does not pass the same sign condition")
            failed_index_same_sign[i] = failed_index

    boolean_array_at_most_three = np.zeros(len(list_of_differences), dtype=bool)
    failed_index_at_most_three = np.ones(len(list_of_differences), dtype=int) * -1
    for i in range(len(list_of_differences)):
        result, failed_index = check_if_diff_at_most_three(list_of_differences[i])
        if result == True:
            # print(f"Row {i} passes the at most three condition")
            boolean_array_at_most_three[i] = True
        else:
            # print(f"Row {i} does not pass the at most three condition")
            failed_index_at_most_three[i] = failed_index

    # Combine the two conditions
    boolean_array_combined = np.logical_and(
        boolean_array_same_sign, boolean_array_at_most_three
    )

    return boolean_array_combined, failed_index_same_sign, failed_index_at_most_three


if __name__ == "__main__":
    data = read_input("input_D2.txt")
    # print(data)

    # Part 1
    # Convert each row into a numpy array
    list_of_rows = []
    for i in range(len(data)):
        this_row = re.findall(r"\d+", data[i])
        list_of_rows.append(np.array([int(this_row[j]) for j in range(len(this_row))]))
    # print(list_of_rows)

    boolean_array_combined, failed_index_same_sign, failed_index_at_most_three = (
        spot_flaw(list_of_rows)
    )
    number_of_safe_reports = np.sum(boolean_array_combined)
    # print(f"Rows that pass both conditions: {np.where(boolean_array_combined)[0]}")
    print(f"Part 1; number of safe reports: {number_of_safe_reports}")

    # Part 2
    # Reuse part 1, get only the failed rows
    failed_rows = np.where(np.logical_not(boolean_array_combined))[0]
    # print(f"Previously failed rows: {failed_rows}")

    if False:
        # Get the list of indexes of the failed condition of each failed row
        array_of_failed_indexes = np.vstack(
            (
                failed_index_same_sign[failed_rows],
                failed_index_at_most_three[failed_rows],
            )
        )
        # print("Indexes that failed either condition: \n", array_of_failed_indexes.T)

        # Remove the one anomaly and recheck the conditions
        new_list_of_previously_failed_rows = []
        compare_list = []
        for i in range(len(failed_rows)):
            current_failed_indexes = array_of_failed_indexes[:, i]
            # # if the row failed both conditions at different indexes, ignore the row
            # if (-1 not in current_failed_indexes) and (
            #     current_failed_indexes[0] != current_failed_indexes[1]
            # ):
            #     # new_list_of_previously_failed_rows.append(list_of_rows[failed_rows[i]])
            #     continue
            # else:
            # remove the anomaly
            failed_index = current_failed_indexes[current_failed_indexes != -1]
            new_row = np.delete(list_of_rows[failed_rows[i]], failed_index)
            new_list_of_previously_failed_rows.append(new_row)
            compare_list.append((list_of_rows[failed_rows[i]], new_row))

        print("Before and after removing anomalies: ", compare_list)

        # Recheck the conditions
        (
            new_boolean_array_combined,
            new_failed_index_same_sign,
            new_failed_index_at_most_three,
        ) = spot_flaw(new_list_of_previously_failed_rows)
        number_of_new_safe_reports = np.sum(new_boolean_array_combined)
        print("Number of new safe reports: ", number_of_new_safe_reports)
        print(
            f"Part 2; number of safe reports: {number_of_new_safe_reports+number_of_safe_reports}"
        )

        # Check the ones that still fail
        new_failed_rows = np.where(np.logical_not(new_boolean_array_combined))[0]

        # print(
        #     f"Rows that still fail the conditions: {[new_list_of_previously_failed_rows[new_failed_rows[i]] for i in range(len(new_failed_rows))]}"
        # )

    # the smart way didn't work because of this edge case: [1, 3, 2, 4, 5] -> must remove 3; but [32, 35, 37, 40, 37] -> must remove 37
    # let's try the brute force way
    if True:
        # cycle through the failed rows, remove one element at a time, and recheck the conditions
        new_list_of_previously_failed_rows = [
            list_of_rows[failed_rows[i]] for i in range(len(failed_rows))
        ]
        # print("Failed reports: ", new_list_of_previously_failed_rows)
        counter_for_tolerance = 0

        for i in range(len(failed_rows)):
            this_row = new_list_of_previously_failed_rows[i]
            for j in range(len(this_row)):
                new_row = np.delete(this_row, j)
                new_row_diff = np.ediff1d(new_row)
                condition_1, _ = check_if_diff_same_sign(new_row_diff)
                condition_2, _ = check_if_diff_at_most_three(new_row_diff)
                if condition_1 and condition_2:
                    counter_for_tolerance += 1
                    break

        print(f"Number of reports that can be fixed: {counter_for_tolerance}")
        print(
            f"Part 2; number of safe reports: {counter_for_tolerance+number_of_safe_reports}"
        )
