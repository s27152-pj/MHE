import argparse
import sys
import time
import matplotlib.pyplot as plt
from full_enumeration import full_enumeration
from hill_climbing import hill_climb_deterministic, hill_climb_random
from tabu_search import tabu_search
from simulated_annealing import simulated_annealing
from genetic_algorithm import genetic_algorithm


def load_items(filename):

    items = []
    with open(filename, 'r') as f:
        for line in f:
            w, v = map(int, line.strip().split())
            items.append((w, v))
    return items


def run_method(name, func, items, capacity, **kwargs):

    start = time.time()
    result = func(items, capacity, **kwargs)
    duration = time.time() - start

    if isinstance(result, tuple) and len(result) == 2:
        solution, value = result
        return value, duration, None
    elif isinstance(result, tuple) and len(result) == 3:
        solution, value, convergence = result
        return value, duration, convergence
    else:
        return None, duration, None

class DummyFile(object):
    def write(self, x): pass

def run_comparison_experiment(items, capacity, suppress):
    if suppress == True:
        sys.stdout = DummyFile()

    results = {
        "Hill Climbing Deterministic": [],
        "Hill Climbing Random": [],
        "Genetic Algorithm": [],
        "Tabu Search": [],
        "Simulated Annealing": [],
    }

    hc_params = {"max_iterations": 1000}
    ga_params = {"population_size": 50, "max_generations": 100}
    tabu_params = {"max_iterations": 1000, "tabu_size": 10, "allow_backtrack": False}
    sa_params = {
        "initial_temp": 1000.0,
        "final_temp": 0.1,
        "alpha": 0.95,
        "max_iter": 1000,
        "cooling_schedule": "exponential",
    }

    hc_values = []
    hc_times = []
    for _ in range(5):
        value, duration, _ = run_method(
            "Hill Climbing", hill_climb_deterministic, items, capacity, **hc_params
        )
        hc_values.append(value)
        hc_times.append(duration)

    results["Hill Climbing Deterministic"] = (hc_values, hc_times)

    hc_values = []
    hc_times = []
    for _ in range(5):
        value, duration, _ = run_method(
            "Hill Climbing", hill_climb_random, items, capacity, **hc_params
        )
        hc_values.append(value)
        hc_times.append(duration)

    results["Hill Climbing Random"] = (hc_values, hc_times)

    ga_values = []
    ga_times = []
    ga_convergences = []
    for _ in range(5):
        value, duration, convergence = run_method(
            "Genetic Algorithm", genetic_algorithm, items, capacity, **ga_params
        )
        ga_values.append(value)
        ga_times.append(duration)
        ga_convergences.append(convergence)

    results["Genetic Algorithm"] = (ga_values, ga_times)

    tabu_values = []
    tabu_times = []
    for _ in range(5):
        value, duration, _ = run_method(
            "Tabu Search", tabu_search, items, capacity, **tabu_params
        )
        tabu_values.append(value)
        tabu_times.append(duration)

    results["Tabu Search"] = (tabu_values, tabu_times)

    sa_values = []
    sa_times = []
    for _ in range(5):
        value, duration, _ = run_method(
            "Simulated Annealing", simulated_annealing, items, capacity, **sa_params
        )
        sa_values.append(value)
        sa_times.append(duration)

    results["Simulated Annealing"] = (sa_values, sa_times)

    if suppress:
        sys.stdout = sys.__stdout__

    plot_comparison_results(results)


def plot_comparison_results(results):

    plt.figure(figsize=(10, 6))

    plt.subplot(2, 1, 1)
    for method, (values, _) in results.items():
        plt.plot(values, label=method)
    plt.title("Wartości najlepszych rozwiązań")
    plt.xlabel("Powtórzenie")
    plt.ylabel("Wartość rozwiązania")
    plt.xticks(range(5))
    plt.legend()

    plt.subplot(2, 1, 2)
    for method, (_, times) in results.items():
        plt.plot(times, label=method)
    plt.title("Czas wykonania")
    plt.xlabel("Powtórzenie")
    plt.ylabel("Czas (sekundy)")
    plt.xticks(range(5))
    plt.legend()

    plt.tight_layout()
    plt.show()

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")

    parser.add_argument("--capacity", type=int, default=55)
    parser.add_argument("--algorithm", type=str, choices=["enum", "hcd", "hcr", "tabu", "sa", "ga", "compare"], default="compare")
    parser.add_argument("--max_iterations", type=int, default=500)

    parser.add_argument("--tabu_size", type=int, default=None)
    parser.add_argument("--allow_backtrack", type=int, choices=[0, 1], default=0)

    parser.add_argument("--cooling_schedule", type=str, choices=["exponential", "linear"], default="exponential")
    parser.add_argument("--alpha", type=float, default=0.95)


    parser.add_argument("--population_size", type=int, default=30)
    parser.add_argument("--max_generations", type=int, default=50)
    parser.add_argument("--stagnation_limit", type=int, default=10)
    parser.add_argument("--elite_size", type=int, default=2)
    parser.add_argument("--crossover_method", type=str, choices=["one_point", "uniform"], default="one_point")
    parser.add_argument("--mutation_method", type=str, choices=["swap", "bit_flip"], default="swap")
    parser.add_argument("--stop_condition", type=str, choices=["stagnation_limit", "max_generations"], default="stagnation_limit")

    parser.add_argument("--suppress", type=int, choices=[0, 1], default=0)

    args = parser.parse_args()
    items = load_items(args.input_file)

    if args.algorithm == "compare":
        run_comparison_experiment(items, args.capacity, suppress=args.suppress)
    elif args.algorithm == "enum":
        value, duration, _ = run_method("full_enumeration", full_enumeration, items, args.capacity)
        print(f"Full Enumeration: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")
    elif args.algorithm == "hcd":
        value, duration, _ = run_method("Hill Climbing Deterministic", hill_climb_deterministic, items, args.capacity,
                                        max_iterations=args.max_iterations)
        print(f"Hill Climbing: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")
    elif args.algorithm == "hcr":
        value, duration, _ = run_method("Hill Climbing Random", hill_climb_random, items, args.capacity,
                                        max_iterations=args.max_iterations)
        print(f"Hill Climbing: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")
    elif args.algorithm == "tabu":
        value, duration, _ = run_method("Tabu Search", tabu_search, items, args.capacity,
                                        max_iterations=args.max_iterations, tabu_size=args.tabu_size, allow_backtrack=args.allow_backtrack)
        print(f"Tabu Search: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")
    elif args.algorithm == "sa":
        value, duration, _ = run_method("Simulated Annealing", simulated_annealing, items, args.capacity,
                                        max_iter=args.max_iterations, cooling_schedule=args.cooling_schedule, alpha=args.alpha,)
        print(f"Simulated Annealing: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")
    elif args.algorithm == "ga":
        value, duration, _ = run_method("Genetic Algorithm", genetic_algorithm, items, args.capacity,
                                        population_size=args.population_size, max_generations=args.max_generations, stagnation_limit=args.stagnation_limit,
                                        crossover_method=args.crossover_method, mutation_method=args.mutation_method, stop_condition=args.stop_condition,
                                        elite_size=args.elite_size)
        print(f"Genetic Algorithm: Najlepsza wartość = {value}, Czas wykonywania = {duration:.4f}s")


if __name__ == "__main__":
    main()
