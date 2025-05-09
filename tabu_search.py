from collections import deque
from knapsack_problem import evaluate, neighbors, random_solution

def tabu_search(items, capacity, max_iterations, tabu_size, allow_backtrack):

    current = random_solution(len(items))
    current_value = evaluate(current, items, capacity)
    best_solution = current
    best_value = current_value

    print(f"Startowe rozwiązanie: {current} -> wartość: {current_value}")

    if tabu_size is None or tabu_size == 0:
        tabu_list = deque()
    else:
        tabu_list = deque(maxlen=tabu_size)
    history = []

    for iteration in range(max_iterations):
        tabu_list.append(tuple(current))
        if allow_backtrack:
            if not history or current != history[-1]:
                history.append(current[:])

        print(f"\nIteracja {iteration + 1}:")
        print(f"Aktualne rozwiązanie: {current} -> wartość: {current_value}")

        candidates = []
        for neighbor in neighbors(current):
            if tuple(neighbor) not in tabu_list:
                value = evaluate(neighbor, items, capacity)
                candidates.append((value, neighbor))
                print(f"  Rozważany sąsiad: {neighbor} -> wartość: {value}")

        if not candidates:
            if allow_backtrack == True and len(history) > 1:
                history.pop()
                current = history.pop()
                current_value = evaluate(current, items, capacity)
                print(f" Brak kandydatów, cofamy się.")
                continue
            else:
                print(f" Brak dostępnych kandydatów, kończę iteracje.")
                break

        candidates.sort(reverse=True)
        best_candidate_value, best_candidate = candidates[0]

        if best_candidate_value > current_value:
            print(f"Znaleziono lepsze rozwiązanie: {best_candidate} -> wartość: {best_candidate_value}")

        current = best_candidate
        current_value = best_candidate_value

        if current_value > best_value:
            best_solution = current
            best_value = current_value
            print(f"Nowe najlepsze rozwiązanie: {best_solution} -> wartość: {best_value}")

    return best_solution, best_value
