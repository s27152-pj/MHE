import random
import math
from knapsack_problem import evaluate, neighbors, random_solution


def simulated_annealing(
        items, capacity,
        initial_temp=1000.0,
        final_temp=0.1,
        alpha=0.95,
        max_iter=1000,
        cooling_schedule="exponential"
):

    current = random_solution(len(items))
    current_value = evaluate(current, items, capacity)
    best = current
    best_value = current_value

    T = initial_temp
    iteration = 0

    while T > final_temp and iteration < max_iter:
        print(f"\nIteracja {iteration + 1}: Temperatura: {T:.3f}")

        neighbor = random.choice(list(neighbors(current)))
        neighbor_value = evaluate(neighbor, items, capacity)
        delta = neighbor_value - current_value

        print(f"  Bieżące rozwiązanie: {current} -> wartość: {current_value}")
        print(f"  Rozważany sąsiad: {neighbor} -> wartość: {neighbor_value}")

        if delta > 0 or random.random() < math.exp(delta / T):
            current = neighbor
            current_value = neighbor_value
            print(f"  Akceptacja.")

            if current_value > best_value:
                best = current
                best_value = current_value
                print(f"  Nowe najlepsze rozwiązanie: {best} -> wartość: {best_value}")
        else:
            print("  Brak akceptacji.")

        if cooling_schedule == "exponential":
            T *= alpha
        elif cooling_schedule == "linear":
            T -= (initial_temp - final_temp) / max_iter
        else:
            raise ValueError("Nieznany schemat chłodzenia.")

        iteration += 1

    return best, best_value