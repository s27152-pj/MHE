import random


def evaluate(solution, items, capacity):

    total_weight = 0
    total_value = 0
    for include, (weight, value) in zip(solution, items):
        if include:
            total_weight += weight
            total_value += value
    return total_value if total_weight <= capacity else 0


def random_solution(n):

    return [random.randint(0, 1) for _ in range(n)]


def neighbors(solution):

    for i in range(len(solution)):
        neighbor = solution.copy()
        neighbor[i] = neighbor[i] ^ 1
        yield neighbor