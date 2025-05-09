import random
from knapsack_problem import evaluate

def generate_population(size, item_count):
    population = [[random.randint(0, 1) for _ in range(item_count)] for _ in range(size)]
    print(f"Nowa populacja: {population}")
    return population


def crossover_one_point(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    #print(f"Krzyżowanie (punktowe) między {parent1} i {parent2} w punkcie {point}")
    return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

def crossover_uniform(parent1, parent2):
    #print(f"Krzyżowanie (jednostkowe) między {parent1} i {parent2}")
    child1 = [p1 if random.random() < 0.5 else p2 for p1, p2 in zip(parent1, parent2)]
    child2 = [p2 if random.random() < 0.5 else p1 for p1, p2 in zip(parent1, parent2)]
    return child1, child2


def mutation_bit_flip(solution, mutation_rate=0.05):
    mutated_solution = [bit if random.random() > mutation_rate else 1 - bit for bit in solution]
    #print(f"Mutacja (bit-flip) rozwiązania {solution} -> {mutated_solution}")
    return mutated_solution

def mutation_swap(solution):
    idx1, idx2 = random.sample(range(len(solution)), 2)
    solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
    #print(f"Mutacja (swap) rozwiązania {solution} -> {solution}")
    return solution


def genetic_algorithm(
    items,
    capacity,
    population_size=50,
    crossover_method="one_point",
    mutation_method="bit_flip",
    stop_condition="generation_limit",
    max_generations=100,
    stagnation_limit=10,
    elite_size=1
):
    item_count = len(items)
    population = generate_population(population_size, item_count)
    best_solution = max(population, key=lambda sol: evaluate(sol, items, capacity))
    best_score = evaluate(best_solution, items, capacity)
    generations = 0
    stagnation = 0
    convergence = [best_score]

    print(f"Startowe rozwiązanie: {best_solution} -> wartość: {best_score}")

    while True:
        print(f"\nGeneracja {generations + 1}:")
        population.sort(key=lambda sol: evaluate(sol, items, capacity), reverse=True)
        new_population = population[:elite_size]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population, 2)

            if crossover_method == "uniform":
                child1, child2 = crossover_uniform(parent1, parent2)
            else:
                child1, child2 = crossover_one_point(parent1, parent2)

            # Mutacja
            if mutation_method == "swap":
                child1 = mutation_swap(child1)
                child2 = mutation_swap(child2)
            else:
                child1 = mutation_bit_flip(child1)
                child2 = mutation_bit_flip(child2)

            new_population.extend([child1, child2])

        population = new_population[:population_size]
        generations += 1

        current_best = max(population, key=lambda sol: evaluate(sol, items, capacity))
        current_score = evaluate(current_best, items, capacity)
        convergence.append(current_score)

        print(f"Najlepsze rozwiązanie w generacji {generations}: {current_best} -> wartość: {current_score}")

        if current_score > best_score:
            best_score = current_score
            best_solution = current_best
            stagnation = 0
            print(f"Nowe najlepsze rozwiązanie: {best_solution} -> wartość: {best_score}")
        else:
            stagnation += 1
            print(f"Brak poprawy rozwiązania. Liczba stagnacji: {stagnation}/{stagnation_limit}")

        if stop_condition == "stagnation_limit":
            if stagnation >= stagnation_limit:
                print(f"Zakończenie: osiągnięto limit stagnacji ({stagnation_limit})")
                break
        else:
            if generations >= max_generations:
                print(f"Zakończenie: osiągnięto maksymalną liczbę generacji ({max_generations})")
                break

    return best_solution, best_score, convergence