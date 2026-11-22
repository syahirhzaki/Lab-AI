"""
GA Assignment - Genetic Algorithm for Delivery Route Optimisation
Student: SYAHIRAH BINTI MOHD ZAKI (22010391)

The delivery van starts at depot A, visits B, C, D, E, F and G exactly once,
and returns to A. A Genetic Algorithm searches for the visiting order with the
shortest total distance.

Run:  python ga_delivery_route.py
"""

import random

# ---------------------------------------------------------------------
# Dataset: symmetric distance matrix in kilometres (from the assignment)
# ---------------------------------------------------------------------
LOCATIONS = ["A", "B", "C", "D", "E", "F", "G"]
DISTANCE_KM = [
    #  A  B  C  D  E  F  G
    [0, 4, 8, 6, 7, 9, 5],  # A
    [4, 0, 5, 7, 3, 8, 6],  # B
    [8, 5, 0, 4, 6, 3, 7],  # C
    [6, 7, 4, 0, 5, 6, 8],  # D
    [7, 3, 6, 5, 0, 4, 6],  # E
    [9, 8, 3, 6, 4, 0, 5],  # F
    [5, 6, 7, 8, 6, 5, 0],  # G
]
INDEX = {name: i for i, name in enumerate(LOCATIONS)}
DEPOT = "A"
DELIVERY_STOPS = ["B", "C", "D", "E", "F", "G"]

# ---------------------------------------------------------------------
# GA settings
# ---------------------------------------------------------------------
RANDOM_SEED = 42        # fixed seed so the experiment can be reproduced
POPULATION_SIZE = 30
GENERATIONS = 100       # at least 50 required
TOURNAMENT_SIZE = 3
CROSSOVER_RATE = 0.9
MUTATION_RATE = 0.2
ELITE_COUNT = 2


def distance(a, b):
    """Distance in km between two named locations."""
    return DISTANCE_KM[INDEX[a]][INDEX[b]]


def full_route(chromosome):
    """Add the depot at the start and the end: A -> ... -> A."""
    return [DEPOT] + list(chromosome) + [DEPOT]


def route_distance(chromosome):
    """Fitness: total km of the round trip, including the return to depot A.
    Lower is better."""
    route = full_route(chromosome)
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))


def is_valid(chromosome):
    """Every delivery stop appears exactly once (no repeats, none missing)."""
    return sorted(chromosome) == sorted(DELIVERY_STOPS)


def create_initial_population(rng):
    """Step 1: random valid routes, each a shuffled order of B-G."""
    population = []
    for _ in range(POPULATION_SIZE):
        chromosome = DELIVERY_STOPS[:]
        rng.shuffle(chromosome)
        population.append(chromosome)
    return population


def tournament_selection(population, rng):
    """Step 2: pick TOURNAMENT_SIZE random routes and return the shortest one."""
    contestants = rng.sample(population, TOURNAMENT_SIZE)
    return min(contestants, key=route_distance)


def order_crossover(parent1, parent2, rng):
    """Step 3: Order Crossover (OX).
    Copy a random slice from parent 1, then fill the remaining positions with the
    missing stops in the order they appear in parent 2. The child therefore
    always contains every stop exactly once."""
    size = len(parent1)
    start, end = sorted(rng.sample(range(size), 2))
    child = [None] * size
    child[start:end + 1] = parent1[start:end + 1]

    fill = [stop for stop in parent2 if stop not in child]
    for i in range(size):
        if child[i] is None:
            child[i] = fill.pop(0)
    return child


def swap_mutation(chromosome, rng):
    """Step 4: swap two delivery stops. The route stays valid."""
    mutated = chromosome[:]
    i, j = rng.sample(range(len(mutated)), 2)
    mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


def run_ga(seed=RANDOM_SEED, verbose=True):
    rng = random.Random(seed)
    population = create_initial_population(rng)
    history = []

    for generation in range(1, GENERATIONS + 1):
        # Evaluate fitness and sort: shortest route first
        population.sort(key=route_distance)
        best = population[0]
        history.append(route_distance(best))
        if verbose and (generation == 1 or generation % 10 == 0):
            print(f"Generation {generation:3d} | best distance {route_distance(best):2d} km | "
                  f"{' -> '.join(full_route(best))}")

        # Elitism: copy the best routes unchanged into the next generation
        next_population = [route[:] for route in population[:ELITE_COUNT]]

        # Fill the rest with children: selection -> crossover -> mutation
        while len(next_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, rng)
            parent2 = tournament_selection(population, rng)
            if rng.random() < CROSSOVER_RATE:
                child = order_crossover(parent1, parent2, rng)
            else:
                child = parent1[:]
            if rng.random() < MUTATION_RATE:
                child = swap_mutation(child, rng)
            assert is_valid(child)
            next_population.append(child)

        population = next_population

    population.sort(key=route_distance)
    return population[0], history


if __name__ == "__main__":
    print("GA Delivery Route Optimisation")
    print(f"Seed {RANDOM_SEED} | population {POPULATION_SIZE} | generations {GENERATIONS} | "
          f"tournament {TOURNAMENT_SIZE} | crossover {CROSSOVER_RATE} | mutation {MUTATION_RATE} | "
          f"elites {ELITE_COUNT}\n")

    best_route, history = run_ga()
    print("\nBest route found:", " -> ".join(full_route(best_route)))
    print("Total distance:", route_distance(best_route), "km")
    print("First generation reaching this distance:", history.index(history[-1]) + 1)
