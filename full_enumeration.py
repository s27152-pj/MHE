from itertools import product
from knapsack_problem import evaluate

def full_enumeration(items, capacity):

    n = len(items)
    best_solution = None
    best_value = 0

    for solution in product([0, 1], repeat=n):
        value = evaluate(solution, items, capacity)

        print(f"Sprawdzam rozwiązanie: {list(solution)} -> wartość = {value}")

        if value > best_value:
            best_value = value
            best_solution = list(solution)
    return best_solution, best_value