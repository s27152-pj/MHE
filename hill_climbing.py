import random
from knapsack_problem import evaluate, neighbors, random_solution

def hill_climb_deterministic(items, capacity, max_iterations):

    current = random_solution(len(items))
    current_value = evaluate(current, items, capacity)

    for iteration in range(max_iterations):
        improved = False
        best_neighbor = current
        best_value = current_value

        for neighbor in neighbors(current):
            value = evaluate(neighbor, items, capacity)
            if value > best_value:
                best_neighbor = neighbor
                best_value = value
                improved = True

        if improved:
            current = best_neighbor
            current_value = best_value
            print(f"Iteracja {iteration + 1}: wartość = {current_value}, rozwiązanie = {current}")
        else:
            print(f"Brak poprawy w iteracji {iteration + 1}, kończę.")
            break
    return current, current_value


def hill_climb_random(items, capacity, max_iterations):

    current = random_solution(len(items))
    current_value = evaluate(current, items, capacity)

    for iteration in range(max_iterations):
        neighbor = random.choice(list(neighbors(current)))
        neighbor_value = evaluate(neighbor, items, capacity)

        if neighbor_value >= current_value:
            current = neighbor
            current_value = neighbor_value
            print(f"Iteracja {iteration + 1}: wartość = {current_value}, rozwiązanie = {current}")
        else:
            print(f"Brak poprawy w iteracji {iteration + 1}, kończę.")
            break

    return current, current_value
