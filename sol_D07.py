### AoC 2024, Day 7
### Trung Ha

import numpy as np
from itertools import permutations

from sol_D1 import read_input

operators_p1 = ["*", "+"]
operators_p2 = ["+", "*", "||"]

if __name__ == "__main__":
    data = read_input("input_D7.txt")
    # print(data)

    list_of_results = []
    list_of_components = []

    for line in data:
        result, components = line.split(":")
        list_of_results.append(int(result.strip()))
        list_of_components.append(components.split())

    # print(list_of_results)
    # print(list_of_components)

    # Part 1
    # Evaluate the possible combinations of the components and check if it matches the result

    sum_of_matches = 0
    for i in range(len(list_of_components)):
        components = list_of_components[i]
        result = list_of_results[i]
        # print("Components: ", components)
        # print("Result: ", result)

        number_of_operators = len(components) - 1

        for j in range(len(operators_p1) ** number_of_operators):
            number_of_close_parentheses = 1
            # print("j: ", j)
            binary = format(j, f"0{number_of_operators}b")
            # print("Binary: ", binary)
            expression = "(" * (number_of_operators + 1)
            for k in range(number_of_operators):
                expression += components[k]
                expression += ")" + operators_p1[int(binary[k])]
            expression += components[-1]
            for l in range(number_of_close_parentheses):
                expression += ")"
            # print("Expression: ", expression)
            if eval(expression) == result:
                # print("Expression: ", expression)
                # print("Result: ", result)
                # print("Matched!")
                sum_of_matches += result
                break

    print("Part 1 answer: ", sum_of_matches)

    # Part 2
    # To add a new operator, let's evaluate at each step of the expression and move forward
    # to avoid any precedence of operators

    sum_of_matches = 0
    for i in range(len(list_of_components)):
        components = list_of_components[i]
        result = list_of_results[i]
        # print("Components: ", components)
        # print("Result: ", result)

        number_of_operators = len(components) - 1

        for j in range(len(operators_p2) ** number_of_operators):
            ternary = np.base_repr(j, base=len(operators_p2)).zfill(number_of_operators)
            this_value = int(components[0])
            for k in range(1, len(components)):
                expression = str(this_value)
                if ternary[k - 1] == "0":
                    expression += "+" + components[k]
                    this_value = eval(expression)
                elif ternary[k - 1] == "1":
                    expression += "*" + components[k]
                    this_value = eval(expression)
                else:
                    this_value = int(expression + components[k])
            if this_value == result:
                # print("Expression: ", expression)
                # print("Result: ", result)
                # print("Matched!")
                sum_of_matches += result
                break

    print("Part 2 answer: ", sum_of_matches)
